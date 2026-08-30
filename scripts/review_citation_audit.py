#!/usr/bin/env python3
"""Audit bracketed numeric citations and reference coverage in review manuscripts.

The tool is intentionally conservative. It can locate missing, uncited, duplicate,
or out-of-order references written as ``[1]`` or ``[1, 2-4]`` and summarize
citation coverage by section. It does not parse author-year or superscript
Vancouver styles, decide whether a citation entails a claim, or decide whether a
manuscript has "enough" references. Those judgments still require source reading.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, NamedTuple
from xml.etree import ElementTree as ET


VERSION = "0.6.0"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"
M_T = "{http://schemas.openxmlformats.org/officeDocument/2006/math}t"

CITATION_RE = re.compile(
    r"\[(?P<body>\d{1,4}(?:\s*(?:,|;|[-\u2012\u2013\u2014])\s*\d{1,4})*)\]"
)
REFERENCE_RE = re.compile(r"^\s*(?P<number>\d{1,4})\s*[.)\u3001]\s*(?P<body>.+)$")
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
REFERENCE_HEADINGS = {"references", "reference", "bibliography", "参考文献", "引用文献"}
CAPTION_HINTS = ("caption", "图表题注", "题注")


class Block(NamedTuple):
    kind: str
    text: str
    style: str = ""


def _paragraph_text(paragraph: ET.Element) -> str:
    parts: list[str] = []
    for node in paragraph.iter():
        if node.tag in {W + "t", M_T} and node.text:
            parts.append(node.text)
        elif node.tag == W + "tab":
            parts.append("\t")
        elif node.tag in {W + "br", W + "cr"}:
            parts.append("\n")
    return "".join(parts).strip()


def _style_id(paragraph: ET.Element) -> str:
    node = paragraph.find(f"./{W}pPr/{W}pStyle")
    return node.get(W + "val", "") if node is not None else ""


def _style_names(styles_xml: bytes | None) -> dict[str, str]:
    if not styles_xml:
        return {}
    root = ET.fromstring(styles_xml)
    names: dict[str, str] = {}
    for style in root.findall(f".//{W}style"):
        style_id = style.get(W + "styleId", "")
        name = style.find(f"./{W}name")
        if style_id and name is not None:
            names[style_id] = name.get(W + "val", style_id)
    return names


def read_docx(path: Path) -> list[Block]:
    with zipfile.ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        styles = _style_names(
            archive.read("word/styles.xml") if "word/styles.xml" in archive.namelist() else None
        )
    body = document.find(f".//{W}body")
    if body is None:
        raise ValueError("DOCX has no document body")
    blocks: list[Block] = []
    for child in body:
        if child.tag == W + "p":
            style_id = _style_id(child)
            blocks.append(Block("paragraph", _paragraph_text(child), styles.get(style_id, style_id)))
        elif child.tag == W + "tbl":
            cells = []
            for cell in child.findall(f".//{W}tc"):
                text = " ".join(
                    item for item in (_paragraph_text(p) for p in cell.findall(f"./{W}p")) if item
                )
                if text:
                    cells.append(text)
            blocks.append(Block("table", " | ".join(cells), "Table"))
    return blocks


def read_text(path: Path) -> list[Block]:
    text = path.read_text(encoding="utf-8-sig")
    blocks: list[Block] = []
    for raw in re.split(r"\n\s*\n+", text):
        paragraph = re.sub(r"\s+", " ", raw).strip()
        if not paragraph:
            continue
        if paragraph.startswith("#"):
            level = len(paragraph) - len(paragraph.lstrip("#"))
            blocks.append(Block("paragraph", paragraph[level:].strip(), f"Heading {level}"))
        else:
            blocks.append(Block("paragraph", paragraph, ""))
    return blocks


def read_input(path: Path) -> list[Block]:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    if path.suffix.lower() in {".txt", ".md", ".markdown"}:
        return read_text(path)
    raise ValueError("Supported inputs: .docx, .txt, .md, .markdown")


def is_reference_heading(block: Block) -> bool:
    return block.text.strip().rstrip(":：").lower() in REFERENCE_HEADINGS


def heading_level(block: Block) -> int | None:
    style = block.style.lower().replace("标题", "heading")
    match = re.search(r"heading\s*([1-9])", style)
    return int(match.group(1)) if match else None


def expand_citation_body(body: str) -> list[int]:
    numbers: list[int] = []
    for item in re.split(r"\s*[,;]\s*", body):
        range_match = re.fullmatch(r"(\d{1,4})\s*[-\u2012\u2013\u2014]\s*(\d{1,4})", item)
        if range_match:
            start, end = map(int, range_match.groups())
            if end >= start and end - start <= 500:
                numbers.extend(range(start, end + 1))
            else:
                numbers.extend([start, end])
        elif item.isdigit():
            numbers.append(int(item))
    return numbers


def citations(text: str) -> list[int]:
    output: list[int] = []
    for match in CITATION_RE.finditer(text):
        output.extend(expand_citation_body(match.group("body")))
    return output


def normalized_doi(text: str) -> str | None:
    match = DOI_RE.search(text)
    if not match:
        return None
    return match.group(0).rstrip(".,;:)]}\uff0c\u3002\uff1b\uff1a\uff09\u3011").lower()


def visible_words(text: str) -> int:
    latin = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text)
    han = re.findall(r"[\u3400-\u9fff]", text)
    return len(latin) + len(han)


def _new_section(title: str) -> dict[str, Any]:
    return {
        "section": title,
        "prose_paragraphs": 0,
        "words_or_han_characters": 0,
        "citation_marks": 0,
        "unique_citations": set(),
        "uncited_prose_paragraphs": 0,
        "longest_uncited_run": 0,
        "_uncited_run": 0,
    }


def _is_prose(block: Block) -> bool:
    if block.kind != "paragraph" or not block.text.strip() or heading_level(block) is not None:
        return False
    style = block.style.lower()
    return not any(hint in style for hint in CAPTION_HINTS)


def audit(path: Path, blocks: list[Block]) -> dict[str, Any]:
    reference_index = next((i for i, block in enumerate(blocks) if is_reference_heading(block)), None)
    main_blocks = blocks if reference_index is None else blocks[:reference_index]
    reference_blocks = [] if reference_index is None else blocks[reference_index + 1 :]

    reference_numbers: list[int] = []
    reference_dois: dict[int, str] = {}
    for block in reference_blocks:
        if block.kind != "paragraph":
            continue
        match = REFERENCE_RE.match(block.text)
        if not match:
            continue
        number = int(match.group("number"))
        reference_numbers.append(number)
        doi = normalized_doi(match.group("body"))
        if doi:
            reference_dois[number] = doi

    all_citations: list[int] = []
    sections: list[dict[str, Any]] = []
    current = _new_section("Front matter")
    sections.append(current)
    for block in main_blocks:
        level = heading_level(block)
        if level == 1:
            current = _new_section(block.text)
            sections.append(current)
            continue
        found = citations(block.text)
        all_citations.extend(found)
        if not _is_prose(block):
            continue
        current["prose_paragraphs"] += 1
        current["words_or_han_characters"] += visible_words(block.text)
        current["citation_marks"] += len(list(CITATION_RE.finditer(block.text)))
        current["unique_citations"].update(found)
        if found:
            current["_uncited_run"] = 0
        else:
            current["uncited_prose_paragraphs"] += 1
            current["_uncited_run"] += 1
            current["longest_uncited_run"] = max(
                current["longest_uncited_run"], current["_uncited_run"]
            )

    section_output: list[dict[str, Any]] = []
    for section in sections:
        section.pop("_uncited_run", None)
        section["unique_citations"] = sorted(section["unique_citations"])
        if section["prose_paragraphs"] or section["unique_citations"]:
            section_output.append(section)

    ref_counter = Counter(reference_numbers)
    doi_counter = Counter(reference_dois.values())
    out_of_order = [
        {
            "position": position + 1,
            "previous": reference_numbers[position - 1],
            "current": reference_numbers[position],
        }
        for position in range(1, len(reference_numbers))
        if reference_numbers[position] < reference_numbers[position - 1]
    ]
    unique_references = set(reference_numbers)
    unique_cited = set(all_citations)
    expected = set(range(1, max(reference_numbers) + 1)) if reference_numbers else set()

    return {
        "tool": "CNS Skills review citation audit",
        "version": VERSION,
        "disclaimer": (
            "Structural citation diagnostics only; citation count does not establish entailment, "
            "quality, completeness, or review sufficiency."
        ),
        "source": str(path.resolve()),
        "numeric_style_detected": bool(reference_numbers or all_citations),
        "reference_heading_found": reference_index is not None,
        "counts": {
            "reference_entries": len(reference_numbers),
            "unique_reference_numbers": len(unique_references),
            "citation_occurrences_expanded": len(all_citations),
            "unique_cited_references": len(unique_cited),
            "references_with_doi": len(reference_dois),
        },
        "missing_reference_entries": sorted(unique_cited - unique_references),
        "uncited_reference_entries": sorted(unique_references - unique_cited),
        "duplicate_reference_numbers": sorted(number for number, count in ref_counter.items() if count > 1),
        "reference_numbering_gaps": sorted(expected - unique_references),
        "out_of_order_reference_numbers": out_of_order,
        "duplicate_dois": [
            {"doi": doi, "reference_numbers": sorted(n for n, value in reference_dois.items() if value == doi)}
            for doi, count in sorted(doi_counter.items())
            if count > 1
        ],
        "sections": section_output,
    }


def make_shareable(report: dict[str, Any]) -> dict[str, Any]:
    output = json.loads(json.dumps(report))
    output["source"] = Path(output["source"]).name
    return output


def render_text(report: dict[str, Any]) -> str:
    counts = report["counts"]
    lines = [
        "CNS review citation audit",
        f"Source: {report['source']}",
        "Note: structural diagnostics only; source reading is still required.",
        "",
        (
            f"References: {counts['reference_entries']} entries / "
            f"{counts['unique_reference_numbers']} unique numbers | "
            f"cited: {counts['unique_cited_references']} unique | "
            f"DOIs: {counts['references_with_doi']}"
        ),
    ]
    for label, key in (
        ("Missing entries", "missing_reference_entries"),
        ("Uncited entries", "uncited_reference_entries"),
        ("Duplicate numbers", "duplicate_reference_numbers"),
        ("Numbering gaps", "reference_numbering_gaps"),
    ):
        values = report[key]
        lines.append(f"{label}: {', '.join(map(str, values)) if values else 'none'}")
    lines.append(
        "Out-of-order entries: "
        + (
            "; ".join(
                f"position {item['position']}: {item['previous']} -> {item['current']}"
                for item in report["out_of_order_reference_numbers"]
            )
            if report["out_of_order_reference_numbers"]
            else "none"
        )
    )
    lines.append(
        "Duplicate DOIs: "
        + (
            "; ".join(f"{item['doi']} ({item['reference_numbers']})" for item in report["duplicate_dois"])
            if report["duplicate_dois"]
            else "none"
        )
    )
    lines.extend(["", "Section coverage:"])
    for section in report["sections"]:
        lines.append(
            f"- {section['section']}: {section['prose_paragraphs']} prose paragraphs, "
            f"{len(section['unique_citations'])} unique citations, "
            f"{section['uncited_prose_paragraphs']} uncited paragraphs, "
            f"longest uncited run {section['longest_uncited_run']}"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", type=Path, help="write the full report as JSON")
    parser.add_argument("--shareable", action="store_true", help="redact the source path")
    parser.add_argument("--version", action="version", version=VERSION)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        source = args.input.resolve()
        if args.json and args.json.resolve() == source:
            print("error: --json output cannot overwrite the input", file=sys.stderr)
            return 1
        report = audit(source, read_input(source))
        if args.shareable:
            report = make_shareable(report)
        if args.json:
            args.json.parent.mkdir(parents=True, exist_ok=True)
            args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(render_text(report))
        structural_flags = (
            "missing_reference_entries",
            "uncited_reference_entries",
            "duplicate_reference_numbers",
            "reference_numbering_gaps",
            "out_of_order_reference_numbers",
            "duplicate_dois",
        )
        if any(report[key] for key in structural_flags):
            return 2
        return 0
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
