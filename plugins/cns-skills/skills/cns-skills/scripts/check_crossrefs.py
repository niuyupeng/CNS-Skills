#!/usr/bin/env python3
"""Audit figure and table caption/reference consistency in DOCX or text files."""

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


VERSION = "0.10.0"
CAPTION_RE = re.compile(
    r"^\s*(?:(?P<scope>Supplementary|Supplemental|Extended\s+Data|补充|扩展数据)\s*)?"
    r"(?P<kind>Fig(?:ure)?|Table|图|表)\s*\.?\s*(?P<number>S?\d+)(?:[A-Za-z])?\b"
    r"\s*(?P<separator>[.．:：|｜]?)",
    re.IGNORECASE,
)
REFERENCE_RE = re.compile(
    r"\b(?:(?P<scope>Supplementary|Supplemental|Extended\s+Data)\s+)?"
    r"(?P<kind>Fig(?:ure)?s?|Tables?)\s*\.?\s*(?P<number>S?\d+)(?:[A-Za-z])?\b|"
    r"(?:(?P<zhscope>补充|扩展数据)\s*)?(?P<zhkind>图|表)\s*(?P<zhnumber>S?\d+)(?:[A-Za-z])?",
    re.IGNORECASE,
)
PROSE_AFTER_LABEL_RE = re.compile(
    r"^(?:shows?|showed|illustrates?|illustrated|demonstrates?|demonstrated|"
    r"presents?|presented|lists?|listed|summari[sz]es?|compares?|provides?|depicts?|indicates?|reveals?)\b|"
    r"^(?:显示|表明|展示|说明|列出|总结|比较|提供|描绘|揭示)",
    re.IGNORECASE,
)


def read_paragraphs(path: Path) -> list[str]:
    if path.suffix.lower() == ".docx":
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
        paragraphs = []
        for xml in xml_parts:
            root = ET.fromstring(xml)
            for paragraph in root.iter(namespace + "p"):
                text = "".join(node.text or "" for node in paragraph.iter() if node.tag in text_tags).strip()
                if text:
                    paragraphs.append(text)
        return paragraphs
    if path.suffix.lower() not in {".txt", ".md", ".markdown"}:
        raise ValueError("supported inputs: .docx, .txt, .md, .markdown")
    return [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def kind_name(value: str) -> str:
    lower = value.lower().rstrip("s")
    return "figure" if lower.startswith("fig") or value == "图" else "table"


def identifier(kind: str, number: str, scope: str | None = None) -> str:
    normalized_number = number.upper()
    normalized_scope = (scope or "").lower().replace(" ", "")
    if normalized_number.startswith("S"):
        if not normalized_scope:
            normalized_scope = "supplementary"
        if normalized_scope in {"supplementary", "supplemental", "补充"}:
            normalized_number = normalized_number[1:]
    scope_name = {
        "supplementary": "supplementary-",
        "supplemental": "supplementary-",
        "补充": "supplementary-",
        "extendeddata": "extended-data-",
        "扩展数据": "extended-data-",
    }.get(normalized_scope, "")
    return f"{scope_name}{kind_name(kind)}:{normalized_number}"


def is_caption(paragraph: str, match: re.Match[str]) -> bool:
    remainder = paragraph[match.end() :].lstrip()
    return not PROSE_AFTER_LABEL_RE.match(remainder)


def audit_paragraphs(paragraphs: list[str]) -> dict[str, Any]:
    caption_candidates: dict[str, list[dict[str, str]]] = {}
    references: Counter[str] = Counter()
    caption_examples: dict[str, str] = {}
    reference_examples: dict[str, list[str]] = {}
    for paragraph in paragraphs:
        caption = CAPTION_RE.match(paragraph)
        if caption and is_caption(paragraph, caption):
            key = identifier(caption.group("kind"), caption.group("number"), caption.group("scope"))
            caption_candidates.setdefault(key, []).append(
                {
                    "language": "zh" if caption.group("kind") in {"图", "表"} else "en",
                    "separator": caption.group("separator") or "",
                    "text": paragraph[:240],
                }
            )
            caption_examples.setdefault(key, paragraph[:240])
            continue
        for match in REFERENCE_RE.finditer(paragraph):
            kind = match.group("kind") or match.group("zhkind")
            number = match.group("number") or match.group("zhnumber")
            scope = match.group("scope") or match.group("zhscope")
            key = identifier(kind, number, scope)
            references[key] += 1
            reference_examples.setdefault(key, []).append(paragraph[:240])

    captions = {key: 1 for key in caption_candidates}
    duplicate_captions: list[dict[str, Any]] = []
    for key, candidates in sorted(caption_candidates.items()):
        by_language: dict[str, list[dict[str, str]]] = {}
        for candidate in candidates:
            by_language.setdefault(candidate["language"], []).append(candidate)
        for same_language in by_language.values():
            if len(same_language) <= 1:
                continue
            separators = {item["separator"] for item in same_language}
            # A common bilingual-manuscript layout uses one heading line plus a
            # same-language post-table takeaway beginning with a vertical bar.
            companion_pair = len(same_language) == 2 and bool(separators & {"|", "｜"}) and len(separators) == 2
            if not companion_pair:
                duplicate_captions.append(
                    {"id": key, "count": len(same_language), "example": same_language[0]["text"]}
                )

    missing_caption = sorted(set(references) - set(captions))
    uncited_caption = sorted(set(captions) - set(references))
    status = "clean" if not (missing_caption or uncited_caption or duplicate_captions) else "issues_found"
    return {
        "status": status,
        "caption_count": len(captions),
        "reference_count": sum(references.values()),
        "captions": dict(sorted(captions.items())),
        "references": dict(sorted(references.items())),
        "references_without_caption": [
            {"id": key, "examples": reference_examples.get(key, [])[:3]} for key in missing_caption
        ],
        "captions_without_reference": [
            {"id": key, "caption": caption_examples.get(key)} for key in uncited_caption
        ],
        "duplicate_captions": duplicate_captions,
    }


def build_report(path: Path, companions: list[Path] | None = None) -> dict[str, Any]:
    companion_paths = companions or []
    paragraphs = read_paragraphs(path)
    for companion in companion_paths:
        paragraphs.extend(read_paragraphs(companion))
    return {
        "tool": "CNS Skills cross-reference checker",
        "version": VERSION,
        "source": str(path.resolve()),
        "companions": [str(item.resolve()) for item in companion_paths],
        "disclaimer": "Heuristic caption/reference audit; ranges, unusual numbering, text boxes, and field codes may require manual inspection.",
        **audit_paragraphs(paragraphs),
    }


def same_path(left: Path, right: Path) -> bool:
    return str(left.resolve()).casefold() == str(right.resolve()).casefold()


def render_text(report: dict[str, Any]) -> str:
    lines = [
        "CNS figure/table cross-reference check",
        f"Status: {report['status']}",
        f"Captions: {report['caption_count']} | in-text references: {report['reference_count']}",
    ]
    if report.get("companions"):
        lines.append(f"Companion artifacts: {len(report['companions'])}")
    for heading, key in (
        ("Reference without caption", "references_without_caption"),
        ("Caption without reference", "captions_without_reference"),
        ("Duplicate caption", "duplicate_captions"),
    ):
        for item in report[key]:
            lines.append(f"{heading}: {item['id']}")
    return "\n".join(lines)


def make_shareable(report: dict[str, Any]) -> dict[str, Any]:
    output = copy.deepcopy(report)
    output["source"] = Path(output["source"]).name
    output["companions"] = [Path(item).name for item in output.get("companions", [])]
    output["shareable_redaction"] = "Local paths and manuscript excerpts removed; identifiers and counts retained."
    for item in output.get("references_without_caption", []):
        item["examples"] = []
    for item in output.get("captions_without_reference", []):
        item["caption"] = None
    for item in output.get("duplicate_captions", []):
        item["example"] = None
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--companion",
        action="append",
        default=[],
        type=Path,
        help="companion DOCX/text artifact whose captions and references should be audited jointly; repeat as needed",
    )
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--shareable", action="store_true", help="redact local paths and manuscript excerpts from JSON output")
    parser.add_argument("--strict", action="store_true", help="exit 2 when issues are found")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    protected_inputs = [args.input, *args.companion]
    if args.json_path and any(same_path(args.json_path, item) for item in protected_inputs):
        print("error: --json must not overwrite an input or companion artifact", file=sys.stderr)
        return 1
    try:
        report = build_report(args.input, args.companion)
    except (OSError, ValueError, zipfile.BadZipFile, KeyError, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(render_text(report))
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        json_report = make_shareable(report) if args.shareable else report
        args.json_path.write_text(json.dumps(json_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 2 if args.strict and report["status"] != "clean" else 0


if __name__ == "__main__":
    raise SystemExit(main())
