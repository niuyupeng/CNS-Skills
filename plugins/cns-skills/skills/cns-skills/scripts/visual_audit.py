#!/usr/bin/env python3
"""Audit DOCX figures, tables, captions, and publication-rendering risks.

The auditor is intentionally dependency-free.  It inspects the OOXML package;
it does not infer scientific truth, image integrity, or venue compliance from
formatting alone.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import struct
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}

W_VAL = f"{{{NS['w']}}}val"
W_STYLE_ID = f"{{{NS['w']}}}styleId"
W_TYPE = f"{{{NS['w']}}}type"
R_EMBED = f"{{{NS['r']}}}embed"

CAPTION_RE = re.compile(
    r"^(?:table|figure|fig\.?|supplement(?:ary|al)\s+(?:table|figure)|"
    r"extended\s+data\s+(?:table|fig\.?)|表|图)\s*[sS]?\d+\b",
    re.IGNORECASE,
)


def qname(prefix: str, local: str) -> str:
    return f"{{{NS[prefix]}}}{local}"


def text_of(element: ET.Element) -> str:
    parts = [node.text or "" for node in element.findall(".//w:t", NS)]
    return "".join(parts).strip()


def paragraph_style_id(element: ET.Element) -> str:
    node = element.find("./w:pPr/w:pStyle", NS)
    return node.get(W_VAL, "") if node is not None else ""


def visible_border(node: ET.Element | None) -> bool:
    if node is None:
        return False
    value = (node.get(W_VAL, "") or "").lower()
    if value in {"", "nil", "none"}:
        return False
    size = node.get(qname("w", "sz"))
    return size is None or size == "" or int(size) > 0


def border_map(parent: ET.Element | None) -> dict[str, dict[str, str]]:
    if parent is None:
        return {}
    result: dict[str, dict[str, str]] = {}
    for name in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = parent.find(f"./w:{name}", NS)
        if node is None:
            continue
        result[name] = {
            "val": node.get(W_VAL, ""),
            "sz": node.get(qname("w", "sz"), ""),
            "color": node.get(qname("w", "color"), ""),
        }
    return result


def border_is_visible(spec: dict[str, str] | None) -> bool:
    if not spec:
        return False
    value = (spec.get("val") or "").lower()
    if value in {"", "nil", "none"}:
        return False
    size = spec.get("sz")
    return not size or int(size) > 0


def style_maps(styles_root: ET.Element | None) -> tuple[dict[str, str], dict[str, dict]]:
    names: dict[str, str] = {}
    table_styles: dict[str, dict] = {}
    if styles_root is None:
        return names, table_styles
    for style in styles_root.findall("./w:style", NS):
        style_id = style.get(W_STYLE_ID, "")
        name_node = style.find("./w:name", NS)
        names[style_id] = name_node.get(W_VAL, style_id) if name_node is not None else style_id
        if style.get(W_TYPE) != "table":
            continue
        base = border_map(style.find("./w:tblPr/w:tblBorders", NS))
        fills: set[str] = set()
        shd = style.find("./w:tblPr/w:shd", NS)
        if shd is not None:
            fill = shd.get(qname("w", "fill"), "")
            if fill:
                fills.add(fill)
        first_row_borders: dict[str, dict[str, str]] = {}
        for conditional in style.findall("./w:tblStylePr", NS):
            if conditional.get(W_TYPE) != "firstRow":
                continue
            for path in ("./w:tcPr/w:tcBorders", "./w:tblPr/w:tblBorders"):
                first_row_borders.update(border_map(conditional.find(path, NS)))
            first_shd = conditional.find("./w:tcPr/w:shd", NS)
            if first_shd is not None:
                fill = first_shd.get(qname("w", "fill"), "")
                if fill:
                    fills.add(fill)
        table_styles[style_id] = {
            "borders": base,
            "first_row_borders": first_row_borders,
            "fills": sorted(fills),
        }
    return names, table_styles


def nonwhite_fill(value: str) -> bool:
    normalized = value.strip().upper()
    return normalized not in {"", "AUTO", "FFFFFF", "NONE", "NIL"}


def next_nonempty_paragraph(
    children: list[ET.Element], start: int, direction: int
) -> ET.Element | None:
    index = start + direction
    while 0 <= index < len(children):
        element = children[index]
        if element.tag == qname("w", "p") and text_of(element):
            return element
        if element.tag in {qname("w", "tbl"), qname("w", "sectPr")}:
            return None
        index += direction
    return None


def caption_record(
    paragraph: ET.Element | None,
    style_names: dict[str, str],
    expected_position: str,
) -> dict:
    if paragraph is None:
        return {"present": False, "position": expected_position, "text": "", "style": ""}
    text = text_of(paragraph)
    style_id = paragraph_style_id(paragraph)
    style_name = style_names.get(style_id, style_id or "Normal")
    return {
        "present": bool(CAPTION_RE.match(text)),
        "position": expected_position,
        "text": text,
        "style": style_name,
    }


def caption_style_ok(style: str) -> bool:
    value = style.lower().replace(" ", "")
    return any(token in value for token in ("caption", "tabletitle", "figuretitle", "题注", "图注", "表题"))


def png_dimensions(data: bytes) -> tuple[int, int] | None:
    if len(data) >= 24 and data.startswith(b"\x89PNG\r\n\x1a\n"):
        return struct.unpack(">II", data[16:24])
    return None


def jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    if len(data) < 4 or not data.startswith(b"\xff\xd8"):
        return None
    offset = 2
    while offset + 9 < len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue
        marker = data[offset + 1]
        offset += 2
        if marker in {0xD8, 0xD9}:
            continue
        if offset + 2 > len(data):
            break
        length = struct.unpack(">H", data[offset : offset + 2])[0]
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            if offset + 7 <= len(data):
                height, width = struct.unpack(">HH", data[offset + 3 : offset + 7])
                return width, height
            break
        if length < 2:
            break
        offset += length
    return None


def raster_dimensions(data: bytes) -> tuple[int, int] | None:
    return png_dimensions(data) or jpeg_dimensions(data)


def issue(code: str, severity: str, detail: str) -> dict[str, str]:
    return {"code": code, "severity": severity, "detail": detail}


def analyze_table(
    element: ET.Element,
    index: int,
    children: list[ET.Element],
    child_index: int,
    style_names: dict[str, str],
    table_styles: dict[str, dict],
    expect_three_line: bool,
) -> dict:
    tbl_pr = element.find("./w:tblPr", NS)
    style_node = tbl_pr.find("./w:tblStyle", NS) if tbl_pr is not None else None
    style_id = style_node.get(W_VAL, "") if style_node is not None else ""
    style_name = style_names.get(style_id, style_id or "Table Normal")
    style_spec = table_styles.get(style_id, {})

    effective_borders = dict(style_spec.get("borders", {}))
    direct_borders = border_map(tbl_pr.find("./w:tblBorders", NS) if tbl_pr is not None else None)
    effective_borders.update(direct_borders)

    rows = element.findall("./w:tr", NS)
    columns = max((len(row.findall("./w:tc", NS)) for row in rows), default=0)
    first_row = rows[0] if rows else None
    repeat_header = (
        first_row is not None and first_row.find("./w:trPr/w:tblHeader", NS) is not None
    )
    cant_split_count = sum(row.find("./w:trPr/w:cantSplit", NS) is not None for row in rows)

    fills = set(style_spec.get("fills", []))
    sizes: set[float] = set()
    first_row_bottom_cells = 0
    first_row_cells = first_row.findall("./w:tc", NS) if first_row is not None else []
    for row_number, row in enumerate(rows):
        for cell in row.findall("./w:tc", NS):
            shd = cell.find("./w:tcPr/w:shd", NS)
            if shd is not None:
                value = shd.get(qname("w", "fill"), "")
                if value:
                    fills.add(value)
            for size_node in cell.findall(".//w:rPr/w:sz", NS):
                value = size_node.get(W_VAL, "")
                if value.isdigit():
                    sizes.add(int(value) / 2)
            if row_number == 0:
                bottom = cell.find("./w:tcPr/w:tcBorders/w:bottom", NS)
                if visible_border(bottom):
                    first_row_bottom_cells += 1

    style_header_bottom = border_is_visible(style_spec.get("first_row_borders", {}).get("bottom"))
    header_rule = bool(first_row_cells) and (
        first_row_bottom_cells == len(first_row_cells) or style_header_bottom
    )
    colored_fills = sorted(value for value in fills if nonwhite_fill(value))
    caption = caption_record(
        next_nonempty_paragraph(children, child_index, -1), style_names, "above"
    )

    issues: list[dict[str, str]] = []
    if not caption["present"]:
        issues.append(issue("table_caption_missing_or_displaced", "error", "No numbered table title immediately above the table."))
    elif not caption_style_ok(caption["style"]):
        issues.append(issue("table_caption_style", "warning", f"Caption uses '{caption['style']}', not a caption/table-title style."))
    if colored_fills:
        severity = "error" if expect_three_line else "warning"
        issues.append(issue("table_color_fill", severity, f"Non-white table fills detected: {', '.join(colored_fills)}."))
    if sizes and min(sizes) < 8.0:
        issues.append(issue("table_text_too_small", "error", f"Smallest explicit table text is {min(sizes):g} pt."))
    if len(sizes) > 1:
        issues.append(issue("table_font_size_drift", "warning", f"Multiple explicit table font sizes detected: {sorted(sizes)}."))
    if len(rows) > 1 and not repeat_header:
        issues.append(issue("header_row_not_repeating", "warning", "The first row is not marked as a repeating header."))
    if rows and cant_split_count < len(rows):
        issues.append(issue("rows_may_split", "warning", f"{len(rows) - cant_split_count} row(s) may split across pages."))

    three_line = {
        "requested": expect_three_line,
        "top_rule": border_is_visible(effective_borders.get("top")),
        "header_rule": header_rule,
        "bottom_rule": border_is_visible(effective_borders.get("bottom")),
        "vertical_rules": any(border_is_visible(effective_borders.get(name)) for name in ("left", "right", "insideV")),
        "interior_horizontal_rules": border_is_visible(effective_borders.get("insideH")),
    }
    if expect_three_line:
        if three_line["vertical_rules"]:
            issues.append(issue("three_line_vertical_rules", "error", "Visible left/right/interior vertical rules conflict with a three-line table."))
        if three_line["interior_horizontal_rules"]:
            issues.append(issue("three_line_interior_rules", "error", "Interior horizontal grid rules conflict with a three-line table."))
        for key, label in (("top_rule", "top"), ("header_rule", "header-bottom"), ("bottom_rule", "bottom")):
            if not three_line[key]:
                issues.append(issue(f"three_line_missing_{key}", "error", f"The {label} rule is missing."))

    return {
        "index": index,
        "rows": len(rows),
        "columns": columns,
        "style_id": style_id,
        "style": style_name,
        "caption": caption,
        "repeat_header": repeat_header,
        "rows_protected_from_splitting": cant_split_count,
        "font_sizes_pt": sorted(sizes),
        "nonwhite_fills": colored_fills,
        "effective_borders": effective_borders,
        "three_line": three_line,
        "issues": issues,
    }


def relationship_map(root: ET.Element | None) -> dict[str, str]:
    if root is None:
        return {}
    return {
        node.get("Id", ""): node.get("Target", "")
        for node in root.findall("./pr:Relationship", NS)
    }


def analyze_figure(
    paragraph: ET.Element,
    index: int,
    children: list[ET.Element],
    child_index: int,
    style_names: dict[str, str],
    relationships: dict[str, str],
    archive: zipfile.ZipFile,
    minimum_raster_dpi: int,
) -> list[dict]:
    results: list[dict] = []
    for drawing_kind in ("inline", "anchor"):
        for drawing in paragraph.findall(f".//wp:{drawing_kind}", NS):
            blip = drawing.find(".//a:blip", NS)
            relation_id = blip.get(R_EMBED, "") if blip is not None else ""
            target = relationships.get(relation_id, "")
            package_target = posixpath.normpath(posixpath.join("word", target)) if target else ""
            extent = drawing.find("./wp:extent", NS)
            width_in = int(extent.get("cx", "0")) / 914400 if extent is not None else 0
            height_in = int(extent.get("cy", "0")) / 914400 if extent is not None else 0
            doc_pr = drawing.find("./wp:docPr", NS)
            alt_text = ""
            if doc_pr is not None:
                alt_text = (doc_pr.get("descr", "") or doc_pr.get("title", "")).strip()

            dimensions = None
            file_format = Path(target).suffix.lower().lstrip(".") if target else ""
            if package_target and package_target in archive.namelist():
                dimensions = raster_dimensions(archive.read(package_target))
            effective_dpi = None
            if dimensions and width_in > 0 and height_in > 0:
                effective_dpi = round(min(dimensions[0] / width_in, dimensions[1] / height_in), 1)

            caption = caption_record(
                next_nonempty_paragraph(children, child_index, 1), style_names, "below"
            )
            issues: list[dict[str, str]] = []
            if not caption["present"]:
                issues.append(issue("figure_caption_missing_or_displaced", "error", "No numbered figure caption immediately below the figure."))
            elif not caption_style_ok(caption["style"]):
                issues.append(issue("figure_caption_style", "warning", f"Caption uses '{caption['style']}', not a caption/figure-title style."))
            if drawing_kind == "anchor":
                issues.append(issue("floating_figure", "warning", "Floating/anchored placement is less stable than inline placement across renderers."))
            if not alt_text:
                issues.append(issue("figure_alt_text_missing", "warning", "Figure has no meaningful alternative text in the DOCX package."))
            if effective_dpi is not None and effective_dpi < minimum_raster_dpi:
                issues.append(issue("raster_dpi_low", "error", f"Effective raster resolution is {effective_dpi:g} dpi; threshold is {minimum_raster_dpi} dpi."))

            results.append({
                "index": index + len(results),
                "kind": drawing_kind,
                "target": target,
                "format": file_format,
                "drawn_size_in": [round(width_in, 3), round(height_in, 3)],
                "pixel_dimensions": list(dimensions) if dimensions else None,
                "effective_dpi": effective_dpi,
                "alt_text": alt_text,
                "caption": caption,
                "issues": issues,
            })
    return results


def build_report(
    path: Path,
    *,
    expect_three_line: bool = False,
    minimum_raster_dpi: int = 300,
) -> dict:
    with zipfile.ZipFile(path) as archive:
        document_root = ET.fromstring(archive.read("word/document.xml"))
        styles_root = (
            ET.fromstring(archive.read("word/styles.xml"))
            if "word/styles.xml" in archive.namelist()
            else None
        )
        rels_root = (
            ET.fromstring(archive.read("word/_rels/document.xml.rels"))
            if "word/_rels/document.xml.rels" in archive.namelist()
            else None
        )
        style_names, table_styles = style_maps(styles_root)
        relationships = relationship_map(rels_root)
        body = document_root.find("./w:body", NS)
        children = list(body) if body is not None else []

        tables: list[dict] = []
        figures: list[dict] = []
        for child_index, element in enumerate(children):
            if element.tag == qname("w", "tbl"):
                tables.append(
                    analyze_table(
                        element,
                        len(tables) + 1,
                        children,
                        child_index,
                        style_names,
                        table_styles,
                        expect_three_line,
                    )
                )
            elif element.tag == qname("w", "p"):
                added = analyze_figure(
                    element,
                    len(figures) + 1,
                    children,
                    child_index,
                    style_names,
                    relationships,
                    archive,
                    minimum_raster_dpi,
                )
                figures.extend(added)

    all_issues = [item for table in tables for item in table["issues"]]
    all_issues.extend(item for figure in figures for item in figure["issues"])
    errors = sum(item["severity"] == "error" for item in all_issues)
    warnings = sum(item["severity"] == "warning" for item in all_issues)
    status = "fail" if errors else "warnings" if warnings else "pass"
    return {
        "tool": "CNS visual audit",
        "source": str(path),
        "scope_note": "OOXML and production QA only; scientific truth, provenance, image integrity, and exact venue compliance still require human verification.",
        "expect_three_line": expect_three_line,
        "minimum_raster_dpi": minimum_raster_dpi,
        "status": status,
        "summary": {
            "tables": len(tables),
            "figures": len(figures),
            "errors": errors,
            "warnings": warnings,
        },
        "tables": tables,
        "figures": figures,
    }


def make_shareable(report: dict) -> dict:
    clean = json.loads(json.dumps(report))
    clean["source"] = Path(clean["source"]).name
    for collection in ("tables", "figures"):
        for item in clean[collection]:
            item["caption"]["text"] = ""
            if collection == "figures":
                item["alt_text"] = "" if item["alt_text"] else ""
    return clean


def print_text(report: dict) -> None:
    summary = report["summary"]
    print("CNS visual audit")
    print(f"Source: {report['source']}")
    print(f"Status: {report['status'].upper()} | tables: {summary['tables']} | figures: {summary['figures']} | errors: {summary['errors']} | warnings: {summary['warnings']}")
    for table in report["tables"]:
        print(f"Table {table['index']}: {table['rows']}x{table['columns']} | style={table['style']} | three-line={table['three_line']}")
        for item in table["issues"]:
            print(f"  - {item['severity'].upper()} {item['code']}: {item['detail']}")
    for figure in report["figures"]:
        dpi = "n/a" if figure["effective_dpi"] is None else f"{figure['effective_dpi']:g}"
        print(f"Figure {figure['index']}: {figure['kind']} {figure['format'] or 'unknown'} | effective dpi={dpi}")
        for item in figure["issues"]:
            print(f"  - {item['severity'].upper()} {item['code']}: {item['detail']}")
    print(report["scope_note"])


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="DOCX file to audit")
    parser.add_argument("--expect-three-line", action="store_true", help="Require top, header-bottom, and bottom rules with no vertical/interior grid rules or color fills")
    parser.add_argument("--minimum-raster-dpi", type=int, default=300, help="Minimum effective DPI for PNG/JPEG figures (default: 300)")
    parser.add_argument("--strict", action="store_true", help="Return exit code 2 when error-severity visual defects remain")
    parser.add_argument("--shareable", action="store_true", help="Remove absolute paths and reader-visible caption text from output")
    parser.add_argument("--json", type=Path, help="Write the report as JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    source = args.source.resolve()
    if not source.is_file() or source.suffix.lower() != ".docx":
        print("visual audit failed: source must be an existing DOCX file", file=sys.stderr)
        return 1
    if args.minimum_raster_dpi <= 0:
        print("visual audit failed: --minimum-raster-dpi must be positive", file=sys.stderr)
        return 1
    if args.json and args.json.resolve() == source:
        print("visual audit failed: JSON output cannot overwrite the source", file=sys.stderr)
        return 1
    try:
        report = build_report(
            source,
            expect_three_line=args.expect_three_line,
            minimum_raster_dpi=args.minimum_raster_dpi,
        )
    except (OSError, KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
        print(f"visual audit failed: {exc}", file=sys.stderr)
        return 1
    if args.shareable:
        report = make_shareable(report)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        print_text(report)
    if args.strict and report["summary"]["errors"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
