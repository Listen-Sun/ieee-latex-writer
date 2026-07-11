#!/usr/bin/env python3
"""Resolve IEEE papers without treating publisher anti-bot responses as fatal errors."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from typing import Any


USER_AGENT = "ieee-latex-writer/1.0 scholarly-metadata-lookup"
BLOCK_STATUSES = {403, 418, 429}
IEEE_DOCUMENT_RE = re.compile(r"ieeexplore\.ieee\.org/document/(\d+)", re.I)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)


@dataclass
class Candidate:
    source: str
    title: str = ""
    authors: str = ""
    year: str = ""
    venue: str = ""
    doi: str = ""
    article_number: str = ""
    publisher_url: str = ""
    open_pdf_url: str = ""
    abstract: str = ""
    publication_type: str = ""

    def identity(self) -> tuple[str, str]:
        return (normalize_doi(self.doi), normalize_title(self.title))


def normalize_doi(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value.strip(), flags=re.I)
    return value.rstrip(".,; ").lower()


def normalize_title(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def extract_year(value: Any) -> str:
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        match = re.search(r"\b(?:19|20)\d{2}\b", value)
        return match.group(0) if match else value
    if isinstance(value, dict):
        parts = value.get("date-parts")
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def join_authors(items: Any) -> str:
    if not isinstance(items, list):
        return ""
    names = []
    for item in items:
        if isinstance(item, str):
            names.append(item)
        elif isinstance(item, dict):
            name = item.get("full_name") or item.get("name")
            if not name:
                name = " ".join(part for part in (item.get("given", ""), item.get("family", "")) if part)
            if name:
                names.append(name)
    return ", ".join(names)


def request_json(url: str, timeout: int) -> tuple[int, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return 0, None


def probe_ieee_page(article_number: str, timeout: int) -> dict[str, Any]:
    url = f"https://ieeexplore.ieee.org/document/{article_number}/"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(4096)
            status = response.status
            content_type = response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as error:
        state = "blocked" if error.code in BLOCK_STATUSES else "unavailable"
        return {"url": url, "http_status": error.code, "state": state}
    except (urllib.error.URLError, TimeoutError) as error:
        return {"url": url, "http_status": 0, "state": "network_unavailable", "detail": str(error)}

    text = body.decode("utf-8", errors="replace").lower()
    challenge = any(token in text for token in ("captcha", "access denied", "challenge", "incapsula"))
    if status in BLOCK_STATUSES or (status == 202 and (not body or challenge)):
        state = "blocked"
    elif not body:
        state = "empty_response"
    else:
        state = "publisher_page_reachable"
    return {"url": url, "http_status": status, "state": state, "content_type": content_type}


def ieee_api_lookup(query: str, article_number: str, doi: str, timeout: int) -> tuple[str, list[Candidate]]:
    api_key = os.environ.get("IEEE_XPLORE_API_KEY", "").strip()
    if not api_key:
        return "api_key_missing", []

    parameters = {"apikey": api_key, "format": "json", "max_records": "10", "start_record": "1"}
    if article_number:
        parameters["article_number"] = article_number
    elif doi:
        parameters["doi"] = doi
    else:
        parameters["article_title"] = query
    url = "https://ieeexploreapi.ieee.org/api/v1/search/articles?" + urllib.parse.urlencode(parameters)
    status, data = request_json(url, timeout)
    if status != 200 or not isinstance(data, dict):
        return f"http_{status or 'unavailable'}", []

    candidates = []
    for article in data.get("articles", []) or []:
        authors = article.get("authors", {})
        if isinstance(authors, dict):
            authors = authors.get("authors", [])
        candidates.append(
            Candidate(
                source="IEEE Xplore Metadata API",
                title=article.get("title", ""),
                authors=join_authors(authors),
                year=extract_year(article.get("publication_year")),
                venue=article.get("publication_title", ""),
                doi=normalize_doi(article.get("doi")),
                article_number=str(article.get("article_number", "")),
                publisher_url=article.get("html_url", ""),
                open_pdf_url=article.get("pdf_url", "") if article.get("access_type") == "OPEN_ACCESS" else "",
                abstract=article.get("abstract", ""),
                publication_type=article.get("content_type", ""),
            )
        )
    return "ok", candidates


def crossref_lookup(query: str, doi: str, timeout: int) -> list[Candidate]:
    if doi:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    else:
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": query, "rows": 5})
    status, data = request_json(url, timeout)
    if status != 200 or not isinstance(data, dict):
        return []
    message = data.get("message", {})
    items = [message] if doi else message.get("items", [])
    candidates = []
    for item in items:
        titles = item.get("title", [""])
        venues = item.get("container-title", [""])
        candidates.append(
            Candidate(
                source="Crossref",
                title=titles[0] if titles else "",
                authors=join_authors(item.get("author", [])),
                year=extract_year(item.get("published-print") or item.get("published-online") or item.get("published")),
                venue=venues[0] if venues else "",
                doi=normalize_doi(item.get("DOI")),
                publisher_url=item.get("URL", ""),
                publication_type=item.get("type", ""),
            )
        )
    return candidates


def openalex_lookup(query: str, doi: str, timeout: int) -> list[Candidate]:
    if doi:
        url = "https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(doi, safe="")
    else:
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"search": query, "per-page": 5})
    status, data = request_json(url, timeout)
    if status != 200 or not isinstance(data, dict):
        return []
    items = [data] if doi else data.get("results", [])
    candidates = []
    for item in items:
        primary = item.get("primary_location") or {}
        source = primary.get("source") or {}
        best_oa = item.get("best_oa_location") or {}
        candidates.append(
            Candidate(
                source="OpenAlex",
                title=item.get("display_name", ""),
                authors=", ".join(
                    authorship.get("author", {}).get("display_name", "")
                    for authorship in item.get("authorships", [])
                    if authorship.get("author", {}).get("display_name")
                ),
                year=extract_year(item.get("publication_year")),
                venue=source.get("display_name", ""),
                doi=normalize_doi(item.get("doi")),
                publisher_url=primary.get("landing_page_url", ""),
                open_pdf_url=best_oa.get("pdf_url", ""),
                publication_type=item.get("type", ""),
            )
        )
    return candidates


def semantic_scholar_lookup(query: str, doi: str, timeout: int) -> list[Candidate]:
    fields = "title,authors,year,venue,externalIds,url,openAccessPdf,abstract"
    if doi:
        url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi, safe='')}?fields={fields}"
    else:
        url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(
            {"query": query, "limit": 5, "fields": fields}
        )
    status, data = request_json(url, timeout)
    if status != 200 or not isinstance(data, dict):
        return []
    items = [data] if doi else data.get("data", [])
    candidates = []
    for item in items:
        ids = item.get("externalIds") or {}
        oa = item.get("openAccessPdf") or {}
        candidates.append(
            Candidate(
                source="Semantic Scholar",
                title=item.get("title", ""),
                authors=join_authors(item.get("authors", [])),
                year=extract_year(item.get("year")),
                venue=item.get("venue", ""),
                doi=normalize_doi(ids.get("DOI")),
                publisher_url=item.get("url", ""),
                open_pdf_url=oa.get("url", ""),
                abstract=item.get("abstract") or "",
            )
        )
    return candidates


def dblp_lookup(query: str, timeout: int) -> list[Candidate]:
    url = "https://dblp.org/search/publ/api?" + urllib.parse.urlencode({"q": query, "format": "json", "h": 5})
    status, data = request_json(url, timeout)
    if status != 200 or not isinstance(data, dict):
        return []
    hits = data.get("result", {}).get("hits", {}).get("hit", [])
    candidates = []
    for hit in hits:
        item = hit.get("info", {})
        authors = item.get("authors", {}).get("author", [])
        if isinstance(authors, dict):
            authors = [authors]
        candidates.append(
            Candidate(
                source="DBLP",
                title=re.sub(r"<[^>]+>", "", item.get("title", "")),
                authors=join_authors(authors),
                year=extract_year(item.get("year")),
                venue=item.get("venue", ""),
                doi=normalize_doi(item.get("doi")),
                publisher_url=item.get("url", ""),
                publication_type=item.get("type", ""),
            )
        )
    return candidates


def deduplicate(candidates: list[Candidate]) -> list[Candidate]:
    output = []
    seen: set[tuple[str, str]] = set()
    for candidate in candidates:
        identity = candidate.identity()
        if identity == ("", "") or identity in seen:
            continue
        seen.add(identity)
        output.append(candidate)
    return output


def filter_candidates(
    candidates: list[Candidate], query: str, article_number: str, doi: str, ieee_resolved: bool
) -> list[Candidate]:
    if doi:
        return [candidate for candidate in candidates if normalize_doi(candidate.doi) == doi]
    if article_number and not ieee_resolved:
        return [
            candidate
            for candidate in candidates
            if candidate.article_number == article_number or article_number in candidate.publisher_url
        ]
    if IEEE_DOCUMENT_RE.search(query) or query.isdigit():
        return candidates

    normalized_query = normalize_title(query)
    if len(normalized_query.split()) < 4:
        return candidates
    return [
        candidate
        for candidate in candidates
        if SequenceMatcher(None, normalized_query, normalize_title(candidate.title)).ratio() >= 0.45
    ]


def parse_input(value: str) -> tuple[str, str, str]:
    value = value.strip()
    document_match = IEEE_DOCUMENT_RE.search(value)
    article_number = document_match.group(1) if document_match else (value if value.isdigit() else "")
    doi_match = DOI_RE.search(value)
    doi = normalize_doi(doi_match.group(0)) if doi_match else ""
    return value, article_number, doi


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"Status: {result['status']}",
        f"Query: {result['query']}",
        f"Article number: {result.get('article_number') or 'unknown'}",
        f"DOI: {result.get('doi') or 'unknown'}",
    ]
    probe = result.get("publisher_probe")
    if probe:
        lines.append(f"Publisher probe: {probe.get('state')} (HTTP {probe.get('http_status')})")
    lines.extend([f"IEEE API: {result['ieee_api_status']}", ""])
    candidates = result["candidates"]
    if candidates:
        lines.extend([
            "| Source | Title | Year | Venue | DOI | Open PDF |",
            "| --- | --- | --- | --- | --- | --- |",
        ])
        for item in candidates:
            title = item["title"].replace("|", "\\|")
            venue = item["venue"].replace("|", "\\|")
            lines.append(
                f"| {item['source']} | {title} | {item['year'] or '-'} | {venue or '-'} | {item['doi'] or '-'} | {item['open_pdf_url'] or '-'} |"
            )
    else:
        lines.append("No reliable metadata candidate was resolved.")
    lines.extend(["", "Next actions:"])
    lines.extend(f"- {action}" for action in result["next_actions"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve IEEE paper metadata with legal fallbacks.")
    parser.add_argument("query", help="IEEE URL, article number, DOI, or paper title.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument("--open-browser", action="store_true", help="Open the IEEE page in the user's browser.")
    parser.add_argument("--timeout", type=int, default=20, help="Per-request timeout in seconds.")
    args = parser.parse_args()

    query, article_number, doi = parse_input(args.query)
    publisher_probe = probe_ieee_page(article_number, args.timeout) if article_number else None
    if args.open_browser and article_number:
        webbrowser.open(f"https://ieeexplore.ieee.org/document/{article_number}/")

    ieee_status, ieee_candidates = ieee_api_lookup(query, article_number, doi, args.timeout)
    enrichment_query = ieee_candidates[0].title if ieee_candidates else query
    enrichment_doi = doi or (ieee_candidates[0].doi if ieee_candidates else "")
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(crossref_lookup, enrichment_query, enrichment_doi, args.timeout),
            executor.submit(openalex_lookup, enrichment_query, enrichment_doi, args.timeout),
            executor.submit(dblp_lookup, enrichment_query, args.timeout),
            executor.submit(semantic_scholar_lookup, enrichment_query, enrichment_doi, args.timeout),
        ]
        fallback_candidates = [candidate for future in futures for candidate in future.result()]
    candidates = deduplicate(ieee_candidates + fallback_candidates)
    candidates = filter_candidates(candidates, query, article_number, doi, bool(ieee_candidates))

    blocked = bool(publisher_probe and publisher_probe.get("state") == "blocked")
    if candidates:
        status = "resolved_metadata"
    elif article_number and (blocked or ieee_status == "api_key_missing"):
        status = "needs_ieee_api_key_or_user_pdf"
    else:
        status = "no_reliable_match"

    next_actions = []
    if ieee_status == "api_key_missing" and article_number:
        next_actions.append(
            "Register for the official IEEE Xplore Metadata API, set IEEE_XPLORE_API_KEY locally, and rerun for exact article-number lookup."
        )
    if blocked:
        next_actions.append("Open the publisher URL in the normal browser; do not retry it through automation.")
    if not candidates:
        next_actions.append("Provide the paper title, DOI, BibTeX export, or legally downloaded PDF to continue.")
    elif not any(candidate.open_pdf_url for candidate in candidates):
        next_actions.append("Metadata was found, but no legal open PDF was confirmed; provide a PDF for full-text analysis.")
    else:
        next_actions.append("Use the confirmed open PDF URL for full-text analysis and label its publication version.")

    result = {
        "status": status,
        "query": query,
        "article_number": article_number,
        "doi": doi,
        "publisher_probe": publisher_probe,
        "ieee_api_status": ieee_status,
        "access_level": "metadata_only" if candidates else "unresolved",
        "candidates": [asdict(candidate) for candidate in candidates],
        "next_actions": next_actions,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render_markdown(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
