#!/usr/bin/env python3
"""Compare scientific invariants between a source and a revised manuscript.

The check is deliberately conservative: it reports additions and removals of
numbers, quantities, statistical expressions, citations, DOIs, cross-references,
and user-protected tokens. Differences require review; they are not automatically
errors, and the tool never edits either document.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


VERSION = "0.3.0"
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
STAT_RE = re.compile(
    r"\b(?:p|q|r|R\^?2|CI)\s*(?:=|<|>|≤|≥|<=|>=)\s*[-+−]?\d+(?:\.\d+)?(?:\s*%)?",
    re.IGNORECASE,
)
UNIT_TOKEN = (
    r"(?:%|‰|Å|°C|[Ff]old|[Tt]imes?|[Cc]ells?|CFU|[Cc]opies|"
    r"fmol|pmol|nmol|[µμu]mol|mmol|mol|fM|pM|nM|[µμu]M|mM|M|"
    r"pg|ng|[µμu]g|mg|kg|g|nL|[µμu]L|mL|dL|L|"
    r"nm|[µμu]m|mm|cm|km|m|ns|[µμu]s|ms|sec|s|min|hr|h|days?|d|"
    r"Pa|kPa|MPa|GPa|Hz|kHz|MHz|GHz|J|kJ|W|K)"
)
QUANTITY_RE = re.compile(
    rf"(?<![A-Za-zµμ])[-+−]?\d+(?:,\d{{3}})*(?:\.\d+)?\s*{UNIT_TOKEN}"
    rf"(?:\s*(?:/|·|\s)\s*{UNIT_TOKEN}(?:\s*(?:\^?\s*[-−]?[123]|[²³]))?)?"
    rf"(?![A-Za-zµμ])"
)
NUMBER_RE = re.compile(r"(?<![A-Za-z])[-+−]?\d+(?:,\d{3})*(?:\.\d+)?(?:[eE][-+−]?\d+)?")
BRACKET_CITATION_RE = re.compile(r"\[(?:\d{1,4}(?:\s*[-,–]\s*\d{1,4})*)\]")
AUTHOR_YEAR_RE = re.compile(
    r"\b[A-Z][A-Za-z'’\-]{2,}(?:\s+et\s+al\.)?,?\s*\(?(?:19|20)\d{2}[a-z]?\)?"
)
CROSSREF_RE = re.compile(
    r"\b(?:Fig(?:ure)?s?\.?|Tables?|Eq(?:uation)?s?\.?)\s*[S]?[0-9]+[A-Za-z]?|"
    r"(?:图|表|公式)\s*[S]?[0-9]+[A-Za-z]?",
    re.IGNORECASE,
)


def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml_parts = [archive.read("word/document.xml")]
        for optional_part in ("word/footnotes.xml", "word/endnotes.xml"):
            if optional_part in archive.namelist():
                xml_parts.append(archive.read(optional_part))
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    text_tags = {
        namespace + "t",
        "{http://schemas.openxmlformats.org/officeDocument/2006/math}t",
    }
    paragraphs: list[str] = []
    for xml in xml_parts:
        root = ET.fromstring(xml)
        for paragraph in root.iter(namespace + "p"):
            text = "".join(node.text or "" for node in paragraph.iter() if node.tag in text_tags).strip()
            if text:
                paragraphs.append(text)
    return "\n\n".join(paragraphs)


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    if path.suffix.lower() not in {".txt", ".md", ".markdown"}:
        raise ValueError("supported inputs: .docx, .txt, .md, .markdown")
    return path.read_text(encoding="utf-8-sig")


def normalize(value: str, casefold: bool = True) -> str:
    normalized = re.sub(
        r"\s+",
        "",
        value.replace("–", "-").replace("−", "-").replace("≤", "<=").replace("≥", ">="),
    )
    return normalized.casefold() if casefold else normalized


def matches(pattern: re.Pattern[str], text: str, preserve_case: bool = False) -> Counter[str]:
    return Counter(
        normalize(match.group(0).rstrip(".,;:)]}，。；：）】"), casefold=not preserve_case)
        for match in pattern.finditer(text)
    )


def ordered_pairs(pattern: re.Pattern[str], text: str, preserve_case: bool = False) -> Counter[str]:
    sequence = [
        normalize(match.group(0).rstrip(".,;:)]}，。；：）】"), casefold=not preserve_case)
        for match in pattern.finditer(text)
    ]
    return Counter(f"{left} → {right}" for left, right in zip(sequence, sequence[1:]))


def protected_counter(text: str, tokens: list[str]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for token in tokens:
        count = text.count(token)
        if count:
            counter[token] = count
    return counter


def extract(text: str, protected_tokens: list[str] | None = None) -> dict[str, Counter[str]]:
    return {
        "dois": matches(DOI_RE, text),
        "statistics": matches(STAT_RE, text),
        "quantities": matches(QUANTITY_RE, text, preserve_case=True),
        "quantity_order": ordered_pairs(QUANTITY_RE, text, preserve_case=True),
        "numbers": matches(NUMBER_RE, text),
        "number_order": ordered_pairs(NUMBER_RE, text),
        "bracket_citations": matches(BRACKET_CITATION_RE, text),
        "author_year_citations": matches(AUTHOR_YEAR_RE, text),
        "cross_references": matches(CROSSREF_RE, text),
        "protected_tokens": protected_counter(text, protected_tokens or []),
    }


def counter_items(counter: Counter[str]) -> list[dict[str, Any]]:
    return [{"value": value, "count": count} for value, count in sorted(counter.items())]


def compare(source: dict[str, Counter[str]], revised: dict[str, Counter[str]]) -> dict[str, Any]:
    categories: dict[str, Any] = {}
    changed = False
    for category in source:
        removed = source[category] - revised[category]
        added = revised[category] - source[category]
        category_changed = bool(removed or added)
        changed = changed or category_changed
        categories[category] = {
            "status": "changed" if category_changed else "unchanged",
            "source_count": sum(source[category].values()),
            "revised_count": sum(revised[category].values()),
            "removed": counter_items(removed),
            "added": counter_items(added),
        }
    return {"status": "changed" if changed else "clean", "categories": categories}


def load_protected(path: Path | None) -> list[str]:
    if path is None:
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def same_path(left: Path, right: Path) -> bool:
    return str(left.resolve()).casefold() == str(right.resolve()).casefold()


def build_report(source_path: Path, revised_path: Path, protected_path: Path | None = None) -> dict[str, Any]:
    protected = load_protected(protected_path)
    source_text = read_text(source_path)
    revised_text = read_text(revised_path)
    result = compare(extract(source_text, protected), extract(revised_text, protected))
    return {
        "tool": "CNS Skills invariant checker",
        "version": VERSION,
        "source": str(source_path.resolve()),
        "revised": str(revised_path.resolve()),
        "protected_token_file": str(protected_path.resolve()) if protected_path else None,
        "disclaimer": "A difference requires scientific review; it is not automatically an error. This tool does not establish semantic equivalence.",
        **result,
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [
        "CNS scientific invariant check",
        f"Status: {report['status']}",
        "Note: reported changes require review; the checker does not edit files or prove equivalence.",
        "",
    ]
    for name, item in report["categories"].items():
        lines.append(
            f"{name}: {item['status']} (source={item['source_count']}, revised={item['revised_count']})"
        )
        for direction in ("removed", "added"):
            for difference in item[direction][:12]:
                lines.append(f"  {direction}: {difference['value']} × {difference['count']}")
    return "\n".join(lines)


def make_shareable(report: dict[str, Any]) -> dict[str, Any]:
    output = copy.deepcopy(report)
    output["source"] = Path(output["source"]).name
    output["revised"] = Path(output["revised"]).name
    if output.get("protected_token_file"):
        output["protected_token_file"] = Path(output["protected_token_file"]).name
    output["shareable_redaction"] = "Local directory paths removed; invariant values remain in the report."
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--protect-file", type=Path, help="UTF-8 file containing one exact protected token per line")
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--shareable", action="store_true", help="remove local directory paths from JSON output")
    parser.add_argument("--strict", action="store_true", help="exit 2 when any invariant changes")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.json_path and any(
        same_path(args.json_path, protected)
        for protected in (args.source, args.revised, args.protect_file)
        if protected is not None
    ):
        print("error: --json must not overwrite a source, revised, or protected-token file", file=sys.stderr)
        return 1
    try:
        report = build_report(args.source, args.revised, args.protect_file)
    except (OSError, ValueError, zipfile.BadZipFile, KeyError, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(render_text(report))
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        json_report = make_shareable(report) if args.shareable else report
        args.json_path.write_text(json.dumps(json_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 2 if args.strict and report["status"] == "changed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
