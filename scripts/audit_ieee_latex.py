#!/usr/bin/env python3
"""Static checks for common IEEE LaTeX manuscript issues."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


RISKY_PACKAGES = {
    "geometry": "IEEE submissions should normally not alter page geometry.",
    "fullpage": "IEEE submissions should normally not alter margins.",
    "titlesec": "Section title formatting is controlled by IEEEtran.",
    "caption": "caption can conflict with IEEEtran caption formatting.",
    "subcaption": "subcaption can conflict with IEEEtran; check venue compatibility.",
    "setspace": "Line spacing changes are usually not allowed in final IEEE format.",
}

ACCEPTED_GRAPHICS = {".ps", ".eps", ".pdf", ".png", ".tif", ".tiff"}
DISCOURAGED_GRAPHICS = {".jpg", ".jpeg", ".gif", ".bmp", ".svg"}
CHINESE_CHAR_RE = re.compile(r"[\u4e00-\u9fff]")
CHINESE_PUNCT_RE = re.compile(r"[\u3000-\u303f\uff00-\uffef]")
UNESCAPED_PERCENT_RE = re.compile(r"(?<!\\)\b\d+(?:\.\d+)?%")
MISSING_UNIT_SPACE_RE = re.compile(
    r"(?<![A-Za-z\\])\b\d+(?:\.\d+)?(?:m|cm|mm|km|s|ms|V|A|W|Hz|N|Pa|rad|deg|K|kg|C)\b"
)
SELF_CITATION_RE = re.compile(
    r"\b(?:in|from|based on|extends?|following)\s+our\s+(?:previous|prior|earlier)?\s*work\s*(?:~?\\cite|\[)",
    re.I,
)
GRANT_RE = re.compile(r"\b(?:grant|award|contract|project)\s*(?:nos?\.?|numbers?|#)?\s*[:#]?\s*[A-Z]{0,6}\d{2,}", re.I)
AFFILIATION_RE = re.compile(r"\b(?:university|institute|laboratory|lab|department|school|college|academy)\b", re.I)
URL_RE = re.compile(r"https?://|github\.com|gitlab\.com|bitbucket\.org", re.I)
DIRTY_BIB_FIELDS = {
    "publisher",
    "issn",
    "isbn",
    "url",
    "arxivId",
    "archivePrefix",
    "eprint",
    "abstract",
    "keywords",
    "language",
}
CAPITALIZATION_TERMS = ("Kalman", "IEEE", "LiDAR", "ROS", "SLAM", "GNSS", "UAV")
IEEE_JOURNAL_ABBREVIATIONS = {
    "IEEE Transactions on Robotics": "IEEE Trans. Robot.",
    "IEEE Transactions on Automatic Control": "IEEE Trans. Automat. Control",
    "IEEE Transactions on Control Systems Technology": "IEEE Trans. Control Syst. Technol.",
    "IEEE Robotics and Automation Letters": "IEEE Robot. Autom. Lett.",
    "IEEE Transactions on Intelligent Transportation Systems": "IEEE Trans. Intell. Transp. Syst.",
}


@dataclass
class Finding:
    level: str
    path: Path
    line: int
    message: str

    def render(self, root: Path) -> str:
        try:
            rel = self.path.relative_to(root)
        except ValueError:
            rel = self.path
        loc = f"{rel}:{self.line}" if self.line else str(rel)
        return f"[{self.level}] {loc} - {self.message}"


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        escaped = False
        out = []
        for ch in line:
            if ch == "%" and not escaped:
                break
            out.append(ch)
            escaped = ch == "\\" and not escaped
            if ch != "\\":
                escaped = False
        lines.append("".join(out))
    return "\n".join(lines)


def line_for(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def read(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def find_main_tex(target: Path) -> Path:
    if target.is_file():
        return target
    candidates = []
    for tex in target.rglob("*.tex"):
        try:
            if "\\documentclass" in read(tex):
                candidates.append(tex)
        except OSError:
            pass
    if not candidates:
        raise SystemExit(f"No main .tex file with \\documentclass found under {target}")
    candidates.sort(key=lambda p: (len(p.parts), str(p)))
    return candidates[0]


def parse_braced_list(command: str, text: str) -> list[tuple[str, int]]:
    pattern = re.compile(r"\\" + re.escape(command) + r"(?:\[[^\]]*\])?\{([^}]*)\}")
    return [(match.group(1), match.start()) for match in pattern.finditer(text)]


def split_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def collect_bib_keys(project_root: Path, bib_names: list[str]) -> set[str]:
    keys: set[str] = set()
    for name in bib_names:
        bib = (project_root / name).with_suffix(".bib")
        if not bib.exists():
            continue
        text = read(bib)
        keys.update(re.findall(r"@\w+\s*\{\s*([^,\s]+)", text))
    return keys


def bib_paths(project_root: Path, bib_names: list[str]) -> list[Path]:
    paths = []
    for name in bib_names:
        bib = (project_root / name).with_suffix(".bib")
        if bib.exists():
            paths.append(bib)
    return paths


def first_match_line(text: str, pattern: re.Pattern[str]) -> int:
    match = pattern.search(text)
    return line_for(text, match.start()) if match else 1


def remove_text_commands(math_text: str) -> str:
    return re.sub(r"\\text(?:rm|it|bf)?\s*\{[^{}]*\}", "", math_text)


def check_math_hygiene(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    math_envs = (
        "equation",
        "equation*",
        "align",
        "align*",
        "IEEEeqnarray",
        "multline",
        "multline*",
        "gather",
        "gather*",
    )
    env_pattern = re.compile(
        r"\\begin\{(" + "|".join(re.escape(env) for env in math_envs) + r")\}(.*?)\\end\{\1\}",
        re.S,
    )
    narrative_re = re.compile(r"\b(?:where|when|if|then|therefore|subject|such|with|and|or)\b", re.I)
    for match in env_pattern.finditer(text):
        body = remove_text_commands(match.group(2))
        if CHINESE_CHAR_RE.search(body):
            findings.append(Finding("WARN", path, line_for(text, match.start()), "Chinese characters found inside a math environment; use English notation or wrap explanatory text in \\text{...}."))
        if narrative_re.search(body):
            findings.append(Finding("WARN", path, line_for(text, match.start()), "Narrative words found inside a math environment; wrap explanatory text in \\text{...}."))
    return findings


def check_bib_files(paths: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    field_pattern = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=", re.M)
    title_pattern = re.compile(r"\btitle\s*=\s*[{'\"](.+?)[}'\"],?\s*$", re.I | re.M)
    journal_pattern = re.compile(r"\bjournal\s*=\s*[{'\"](.+?)[}'\"],?\s*$", re.I | re.M)

    for bib in paths:
        text = read(bib)
        for match in field_pattern.finditer(text):
            field = match.group(1)
            if field in DIRTY_BIB_FIELDS:
                findings.append(Finding("WARN", bib, line_for(text, match.start()), f"Dirty BibTeX field '{field}' should usually be removed for clean IEEEtran output."))

        for match in title_pattern.finditer(text):
            title = match.group(1)
            for term in CAPITALIZATION_TERMS:
                if re.search(rf"\b{re.escape(term)}\b", title) and f"{{{{{term}}}}}" not in title:
                    findings.append(Finding("WARN", bib, line_for(text, match.start()), f"Protect '{term}' capitalization in the title with double braces."))

        for match in journal_pattern.finditer(text):
            journal = match.group(1).strip()
            if journal in IEEE_JOURNAL_ABBREVIATIONS:
                findings.append(Finding("WARN", bib, line_for(text, match.start()), f"Use IEEE abbreviation '{IEEE_JOURNAL_ABBREVIATIONS[journal]}' for journal name."))

    return findings


def check_main(main: Path) -> list[Finding]:
    root = main.parent
    raw = read(main)
    text = strip_comments(raw)
    findings: list[Finding] = []

    doc = re.search(r"\\documentclass(?:\[([^\]]*)\])?\{([^}]*)\}", text)
    if not doc:
        findings.append(Finding("ERROR", main, 1, "Missing \\documentclass."))
    else:
        options = set(split_csv(doc.group(1) or ""))
        cls = doc.group(2)
        if "IEEEtran" not in cls:
            findings.append(Finding("ERROR", main, line_for(text, doc.start()), "Document class is not IEEEtran or an IEEEtran-derived class."))
        if not ({"conference", "journal", "technote", "peerreview", "peerreviewca", "compsoc", "letters", "transmag"} & options):
            findings.append(Finding("WARN", main, line_for(text, doc.start()), "No common IEEEtran mode option found; verify the venue-required class options."))

    if not re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}", text, re.S):
        findings.append(Finding("WARN", main, 1, "Missing abstract environment."))
    if "\\begin{IEEEkeywords}" not in text and "\\begin{keywords}" not in text:
        findings.append(Finding("WARN", main, 1, "Missing IEEEkeywords/keywords environment."))

    if CHINESE_CHAR_RE.search(text):
        findings.append(Finding("WARN", main, first_match_line(text, CHINESE_CHAR_RE), "Chinese characters found in manuscript body; IEEE submissions normally require English text."))
    if CHINESE_PUNCT_RE.search(text):
        findings.append(Finding("WARN", main, first_match_line(text, CHINESE_PUNCT_RE), "Chinese or full-width punctuation found; replace with ASCII punctuation for IEEE LaTeX."))
    for match in UNESCAPED_PERCENT_RE.finditer(raw):
        findings.append(Finding("WARN", main, line_for(raw, match.start()), "Unescaped percent detected in numeric text; write percentages as 10\\%."))
    for match in MISSING_UNIT_SPACE_RE.finditer(text):
        token = match.group(0)
        if token.endswith("C") and "$^\\circ$" in text[max(0, match.start() - 15):match.start()]:
            continue
        findings.append(Finding("WARN", main, line_for(text, match.start()), f"Possible missing space before unit in '{token}'; prefer forms like '10 m' or '3 V'."))

    author_match = re.search(r"\\author\s*\{(.*?)\}\s*\\maketitle", text, re.S)
    if author_match and ("@" in author_match.group(1) or AFFILIATION_RE.search(author_match.group(1))):
        findings.append(Finding("WARN", main, line_for(text, author_match.start()), "Identity-bearing author metadata detected; anonymize for double-blind venues."))
    if re.search(r"\\(?:section\*?|subsection\*?)\{Acknowledg(?:e)?ments?\}|\\begin\{acknowledg(?:e)?ments?\}", text, re.I):
        findings.append(Finding("WARN", main, 1, "Acknowledgment section detected; remove or defer it for double-blind review if required."))
    if GRANT_RE.search(text):
        findings.append(Finding("WARN", main, first_match_line(text, GRANT_RE), "Grant or award number detected; anonymize or remove for double-blind review if required."))
    if SELF_CITATION_RE.search(text):
        findings.append(Finding("WARN", main, first_match_line(text, SELF_CITATION_RE), "First-person self-citation detected; rewrite in third person for double-blind review."))
    if URL_RE.search(text):
        findings.append(Finding("WARN", main, first_match_line(text, URL_RE), "Repository or URL detected; verify it does not reveal author identity during double-blind review."))

    for pkg_match in re.finditer(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", text):
        for package in split_csv(pkg_match.group(1)):
            if package in RISKY_PACKAGES:
                findings.append(Finding("WARN", main, line_for(text, pkg_match.start()), f"Risky package '{package}': {RISKY_PACKAGES[package]}"))

    if re.search(r"\\(?:setlength|addtolength)\s*\{\\(?:textwidth|textheight|oddsidemargin|evensidemargin|topmargin)", text):
        findings.append(Finding("WARN", main, 1, "Manual margin or text block changes detected."))
    if re.search(r"\\vspace\s*\{\s*-\s*", text):
        findings.append(Finding("WARN", main, 1, "Negative \\vspace detected; repeated spacing compression is risky for IEEE submission."))

    bibstyles = [value for value, _ in parse_braced_list("bibliographystyle", text)]
    bibs = [item for value, _ in parse_braced_list("bibliography", text) for item in split_csv(value)]
    cites = [key for value, _ in parse_braced_list("cite", text) for key in split_csv(value)]
    if cites and not bibs and "\\begin{thebibliography}" not in text:
        findings.append(Finding("WARN", main, 1, "Citations found but no bibliography command or thebibliography environment detected."))
    if bibs and not any("IEEEtran" in style for style in bibstyles):
        findings.append(Finding("WARN", main, 1, "BibTeX bibliography is used without \\bibliographystyle{IEEEtran}."))

    bib_keys = collect_bib_keys(root, bibs)
    for key in sorted(set(cites)):
        if bib_keys and key not in bib_keys:
            findings.append(Finding("ERROR", main, 1, f"Citation key '{key}' not found in declared .bib files."))

    findings.extend(check_bib_files(bib_paths(root, bibs)))

    labels = {value for value, _ in parse_braced_list("label", text)}
    refs = {key for command in ("ref", "eqref", "autoref", "cref", "Cref") for value, _ in parse_braced_list(command, text) for key in split_csv(value)}
    for key in sorted(refs - labels):
        findings.append(Finding("ERROR", main, 1, f"Reference key '{key}' has no matching \\label."))

    for inc, idx in parse_braced_list("includegraphics", text):
        image = inc.strip()
        candidates = [root / image]
        if not Path(image).suffix:
            candidates.extend(root / f"{image}{ext}" for ext in ACCEPTED_GRAPHICS | DISCOURAGED_GRAPHICS)
        if not any(path.exists() for path in candidates):
            findings.append(Finding("ERROR", main, line_for(text, idx), f"Included graphic '{image}' was not found."))
        suffix = Path(image).suffix.lower()
        if suffix in DISCOURAGED_GRAPHICS:
            findings.append(Finding("WARN", main, line_for(text, idx), f"Graphic extension '{suffix}' is discouraged for IEEE submission."))
        elif suffix and suffix not in ACCEPTED_GRAPHICS:
            findings.append(Finding("WARN", main, line_for(text, idx), f"Graphic extension '{suffix}' is not in IEEE's common accepted graphics list."))

    float_pattern = re.compile(r"\\begin\{(figure\*?|table\*?)\}(.*?)\\end\{\1\}", re.S)
    for match in float_pattern.finditer(text):
        env, body = match.group(1), match.group(2)
        body_start_line = line_for(text, match.start())
        cap = body.find("\\caption")
        lab = body.find("\\label")
        if cap < 0:
            findings.append(Finding("WARN", main, body_start_line, f"{env} has no caption."))
        if lab < 0:
            findings.append(Finding("WARN", main, body_start_line, f"{env} has no label."))
        if cap >= 0 and lab >= 0 and lab < cap:
            findings.append(Finding("WARN", main, body_start_line, f"{env} label appears before caption; place labels after captions."))
        if env.startswith("table") and cap > body.find("\\begin{tabular}") >= 0:
            findings.append(Finding("WARN", main, body_start_line, "Table caption appears after tabular; IEEE style normally puts table captions above tables."))

    findings.extend(check_math_hygiene(main, text))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit an IEEE LaTeX project for common static issues.")
    parser.add_argument("target", help="Path to a main .tex file or a project directory.")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    main_tex = find_main_tex(target)
    findings = check_main(main_tex)
    root = main_tex.parent

    print(f"Main file: {main_tex}")
    if not findings:
        print("No common IEEE LaTeX issues found by static audit.")
        return 0

    for finding in findings:
        print(finding.render(root))

    errors = sum(1 for finding in findings if finding.level == "ERROR")
    warnings = sum(1 for finding in findings if finding.level == "WARN")
    print(f"Summary: {errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
