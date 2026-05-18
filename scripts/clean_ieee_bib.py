#!/usr/bin/env python3
"""Clean BibTeX entries for IEEEtran-style bibliographies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DROP_FIELDS = {
    "abstract",
    "keywords",
    "keyword",
    "language",
    "publisher",
    "issn",
    "isbn",
    "url",
    "file",
    "month",
    "note",
    "eprint",
    "archiveprefix",
    "archivePrefix",
    "primaryclass",
    "primaryClass",
    "copyright",
    "mendeley-groups",
    "annote",
    "address",
}

TITLE_ACRONYMS = [
    "IEEE",
    "TCN",
    "LiDAR",
    "MPC",
    "PPO",
    "RL",
    "DRL",
    "SLAM",
    "UAV",
    "UGV",
    "IMU",
    "ROS",
    "GPU",
    "CPU",
    "CNN",
    "RNN",
    "LSTM",
    "GRU",
    "MLP",
    "GNN",
    "VAE",
    "GAN",
    "MCTS",
    "PID",
    "NMPC",
    "EKF",
    "UKF",
    "HRI",
    "Sim2Real",
    "Transformer",
]


def strip_outer(value: str) -> tuple[str, str, str]:
    value = value.strip()
    if len(value) >= 2 and value[0] == "{" and value[-1] == "}":
        return "{", value[1:-1], "}"
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return '"', value[1:-1], '"'
    return "{", value, "}"


def protect_title(value: str) -> str:
    left, body, right = strip_outer(value)
    for token in TITLE_ACRONYMS:
        pattern = re.compile(r"(?<![A-Za-z0-9{])" + re.escape(token) + r"(?![A-Za-z0-9}])")
        body = pattern.sub("{{" + token + "}}", body)
    return f"{left}{body}{right}"


def find_entries(text: str) -> list[tuple[int, int, str]]:
    entries: list[tuple[int, int, str]] = []
    i = 0
    while True:
        at = text.find("@", i)
        if at == -1:
            break
        brace = text.find("{", at)
        paren = text.find("(", at)
        starts = [pos for pos in (brace, paren) if pos != -1]
        if not starts:
            break
        start = min(starts)
        open_ch = text[start]
        close_ch = "}" if open_ch == "{" else ")"
        depth = 0
        in_quote = False
        escaped = False
        j = start
        while j < len(text):
            ch = text[j]
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_quote = not in_quote
            elif not in_quote and ch == open_ch:
                depth += 1
            elif not in_quote and ch == close_ch:
                depth -= 1
                if depth == 0:
                    entries.append((at, j + 1, text[at : j + 1]))
                    i = j + 1
                    break
            j += 1
        else:
            entries.append((at, len(text), text[at:]))
            break
    return entries


def split_entry(entry: str) -> tuple[str, str, str]:
    match = re.match(r"@(\w+)\s*([{(])\s*([^,]+)\s*,", entry, flags=re.S)
    if not match:
        return "", "", entry
    return match.group(1), match.group(3).strip(), entry[match.end() : -1]


def parse_fields(body: str) -> list[tuple[str, str]]:
    fields: list[tuple[str, str]] = []
    i = 0
    while i < len(body):
        while i < len(body) and body[i] in " \t\r\n,":
            i += 1
        name_start = i
        while i < len(body) and re.match(r"[A-Za-z0-9_\-]", body[i]):
            i += 1
        name = body[name_start:i].strip()
        while i < len(body) and body[i].isspace():
            i += 1
        if not name or i >= len(body) or body[i] != "=":
            break
        i += 1
        while i < len(body) and body[i].isspace():
            i += 1
        value_start = i
        depth = 0
        in_quote = False
        escaped = False
        while i < len(body):
            ch = body[i]
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"' and depth == 0:
                in_quote = not in_quote
            elif not in_quote and ch == "{":
                depth += 1
            elif not in_quote and ch == "}":
                depth -= 1
            elif not in_quote and depth == 0 and ch == ",":
                break
            i += 1
        fields.append((name, body[value_start:i].strip()))
        if i < len(body) and body[i] == ",":
            i += 1
    return fields


def clean_entry(entry: str) -> str:
    entry_type, key, body = split_entry(entry)
    if not entry_type or not key:
        return entry.strip()
    fields = parse_fields(body)
    has_doi = any(name.lower() == "doi" for name, value in fields if value.strip("{}\" "))
    keep_arxiv = entry_type.lower() == "misc" and not has_doi

    cleaned: list[tuple[str, str]] = []
    drop_fields_lower = {field.lower() for field in DROP_FIELDS}
    for name, value in fields:
        lower = name.lower()
        if lower in drop_fields_lower:
            if keep_arxiv and lower in {"url", "eprint", "archiveprefix", "primaryclass", "note"}:
                pass
            else:
                continue
        if lower == "title":
            value = protect_title(value)
        cleaned.append((name, value))

    lines = [f"@{entry_type}{{{key},"]
    for idx, (name, value) in enumerate(cleaned):
        comma = "," if idx < len(cleaned) - 1 else ""
        lines.append(f"  {name} = {value}{comma}")
    lines.append("}")
    return "\n".join(lines)


def clean_bib(text: str) -> str:
    entries = find_entries(text)
    if not entries:
        return text
    output: list[str] = []
    cursor = 0
    for start, end, entry in entries:
        prefix = text[cursor:start].strip()
        if prefix:
            output.append(prefix)
        output.append(clean_entry(entry))
        cursor = end
    suffix = text[cursor:].strip()
    if suffix:
        output.append(suffix)
    return "\n\n".join(output).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean BibTeX for IEEEtran bibliographies.")
    parser.add_argument("bib_file", type=Path, help="Path to the input .bib file")
    args = parser.parse_args()

    input_path = args.bib_file
    if not input_path.exists():
        parser.error(f"file not found: {input_path}")
    if input_path.suffix.lower() != ".bib":
        parser.error("input file must have a .bib extension")

    output_path = input_path.with_name(input_path.stem + "_ieee_clean.bib")
    text = input_path.read_text(encoding="utf-8-sig")
    output_path.write_text(clean_bib(text), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
