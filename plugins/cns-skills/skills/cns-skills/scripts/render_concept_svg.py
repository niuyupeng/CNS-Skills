#!/usr/bin/env python3
"""Render deterministic, editable SVG concept figures from a JSON specification."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
ALLOWED_LAYOUTS = {"flow", "independent_axes"}
REQUIRED = (
    "id",
    "title",
    "description",
    "language",
    "layout",
    "width_px",
    "height_px",
    "width_mm",
    "height_mm",
    "palette",
)


def tag(name: str) -> str:
    return f"{{{SVG_NS}}}{name}"


def validate(spec: dict) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED:
        if field not in spec or spec[field] in (None, "", [], {}):
            errors.append(f"missing_or_empty:{field}")
    if spec.get("layout") not in ALLOWED_LAYOUTS:
        errors.append(f"unsupported_layout:{spec.get('layout', '')}")
    for field in ("width_px", "height_px", "width_mm", "height_mm"):
        value = spec.get(field)
        if value is not None and (not isinstance(value, (int, float)) or value <= 0):
            errors.append(f"invalid_positive_number:{field}")
    palette = spec.get("palette", {})
    for field in ("ink", "muted", "rule", "background", "accent"):
        value = palette.get(field)
        if value is None:
            errors.append(f"palette_missing:{field}")
        elif not isinstance(value, str) or not HEX.match(value):
            errors.append(f"palette_invalid:{field}")
    if spec.get("layout") == "flow":
        nodes = spec.get("nodes")
        if not isinstance(nodes, list) or len(nodes) < 3:
            errors.append("flow_requires_at_least_three_nodes")
    if spec.get("layout") == "independent_axes":
        rows = spec.get("rows")
        if not isinstance(rows, list) or len(rows) < 2:
            errors.append("independent_axes_requires_at_least_two_rows")
        elif any(not isinstance(row.get("items"), list) or len(row["items"]) < 2 for row in rows):
            errors.append("each_axis_requires_at_least_two_items")
    return sorted(set(errors))


def add_text(
    parent: ET.Element,
    x: float,
    y: float,
    lines: list[str] | str,
    *,
    size: int,
    fill: str,
    weight: int = 400,
    anchor: str = "start",
    line_gap: float = 1.2,
    css_class: str = "",
) -> ET.Element:
    if isinstance(lines, str):
        lines = [lines]
    node = ET.SubElement(
        parent,
        tag("text"),
        {
            "x": f"{x:g}",
            "y": f"{y:g}",
            "font-size": str(size),
            "font-weight": str(weight),
            "fill": fill,
            "text-anchor": anchor,
            "class": css_class,
        },
    )
    for index, line in enumerate(lines):
        span = ET.SubElement(
            node,
            tag("tspan"),
            {
                "x": f"{x:g}",
                "dy": "0" if index == 0 else f"{size * line_gap:g}",
            },
        )
        span.text = str(line)
    return node


def add_common_root(spec: dict) -> tuple[ET.Element, ET.Element]:
    width = spec["width_px"]
    height = spec["height_px"]
    root = ET.Element(
        tag("svg"),
        {
            "width": f"{spec['width_mm']}mm",
            "height": f"{spec['height_mm']}mm",
            "viewBox": f"0 0 {width} {height}",
            "role": "img",
            "aria-labelledby": "figure-title figure-description",
            "data-cns-layout": spec["layout"],
            "data-cns-id": spec["id"],
        },
    )
    title = ET.SubElement(root, tag("title"), {"id": "figure-title"})
    title.text = spec["title"]
    desc = ET.SubElement(root, tag("desc"), {"id": "figure-description"})
    desc.text = spec["description"]
    style = ET.SubElement(root, tag("style"))
    style.text = (
        "text{font-family:'Noto Sans','Noto Sans CJK SC','Arial',sans-serif;}"
        ".label{letter-spacing:.1px}.step{font-variant-numeric:tabular-nums;}"
    )
    defs = ET.SubElement(root, tag("defs"))
    marker = ET.SubElement(
        defs,
        tag("marker"),
        {
            "id": "arrow",
            "markerWidth": "12",
            "markerHeight": "12",
            "refX": "10",
            "refY": "5",
            "orient": "auto",
            "markerUnits": "strokeWidth",
        },
    )
    ET.SubElement(marker, tag("path"), {"d": "M 0 0 L 10 5 L 0 10 z", "fill": spec["palette"]["accent"]})
    background = ET.SubElement(
        root,
        tag("rect"),
        {
            "x": "0",
            "y": "0",
            "width": str(width),
            "height": str(height),
            "fill": spec["palette"]["background"],
        },
    )
    background.set("data-role", "background")
    content = ET.SubElement(root, tag("g"), {"id": "figure-content"})
    return root, content


def render_flow(spec: dict, parent: ET.Element) -> None:
    width = float(spec["width_px"])
    height = float(spec["height_px"])
    palette = spec["palette"]
    nodes = spec["nodes"]
    # Keep the first and last centred labels inside the canvas.  The generous
    # side margins are deliberate at 183 mm export width.
    left, right = 300.0, width - 300.0
    center_y = height * 0.23
    positions = [left + (right - left) * index / (len(nodes) - 1) for index in range(len(nodes))]

    if spec.get("kicker"):
        add_text(parent, left, 58, spec["kicker"], size=25, fill=palette["muted"], weight=600, css_class="label")

    for index in range(len(nodes) - 1):
        ET.SubElement(
            parent,
            tag("line"),
            {
                "x1": f"{positions[index] + 34:g}",
                "y1": f"{center_y:g}",
                "x2": f"{positions[index + 1] - 47:g}",
                "y2": f"{center_y:g}",
                "stroke": palette["accent"],
                "stroke-width": "7",
                "marker-end": "url(#arrow)",
            },
        )

    feedback = spec.get("feedback")
    if feedback:
        from_index = int(feedback.get("from", len(nodes))) - 1
        to_index = int(feedback.get("to", max(1, len(nodes) - 2))) - 1
        if not (0 <= from_index < len(nodes) and 0 <= to_index < len(nodes)):
            raise ValueError("feedback node indices are outside the flow")
        x_from = positions[from_index]
        x_to = positions[to_index]
        arc_y = center_y - 105
        path = ET.SubElement(
            parent,
            tag("path"),
            {
                "d": f"M {x_from:g} {center_y - 42:g} C {x_from:g} {arc_y:g}, {x_to:g} {arc_y:g}, {x_to:g} {center_y - 42:g}",
                "fill": "none",
                "stroke": palette["accent"],
                "stroke-width": "5",
                "stroke-dasharray": "14 10",
                "marker-end": "url(#arrow)",
                "data-role": "conditional-feedback",
            },
        )
        path.set("opacity", "0.9")
        if feedback.get("label_lines"):
            add_text(
                parent,
                (x_from + x_to) / 2,
                arc_y - 62,
                feedback["label_lines"],
                size=28,
                fill=palette["muted"],
                weight=600,
                anchor="middle",
                line_gap=1.15,
            )

    for index, (x, node) in enumerate(zip(positions, nodes), start=1):
        group = ET.SubElement(parent, tag("g"), {"id": f"node-{index}", "data-node-id": str(node.get("id", index))})
        ET.SubElement(
            group,
            tag("circle"),
            {
                "cx": f"{x:g}",
                "cy": f"{center_y:g}",
                "r": "34",
                "fill": palette["accent"],
            },
        )
        add_text(group, x, center_y + 13, str(index), size=35, fill="#FFFFFF", weight=700, anchor="middle", css_class="step")
        add_text(group, x, center_y + 112, node.get("title_lines", []), size=38, fill=palette["ink"], weight=700, anchor="middle", line_gap=1.15)
        add_text(group, x, center_y + 215, node.get("body_lines", []), size=31, fill=palette["ink"], weight=400, anchor="middle", line_gap=1.22)
        if node.get("boundary_lines"):
            add_text(group, x, center_y + 350, node["boundary_lines"], size=28, fill=palette["muted"], weight=500, anchor="middle", line_gap=1.2)

    footer_lines = spec.get("footer_lines", [])
    if footer_lines:
        y = height - 84
        ET.SubElement(
            parent,
            tag("line"),
            {"x1": f"{left:g}", "y1": f"{y - 42:g}", "x2": f"{right:g}", "y2": f"{y - 42:g}", "stroke": palette["rule"], "stroke-width": "3"},
        )
        add_text(parent, width / 2, y, footer_lines, size=30, fill=palette["muted"], weight=500, anchor="middle", line_gap=1.2)


def render_independent_axes(spec: dict, parent: ET.Element) -> None:
    width = float(spec["width_px"])
    height = float(spec["height_px"])
    palette = spec["palette"]
    rows = spec["rows"]
    left_label = 115.0
    axis_start = width * 0.30
    axis_end = width - 260.0
    top = 130.0
    # Reserve enough room below the final axis for alternating item labels and
    # the footer.  This keeps the physical-size export legible without clipping.
    bottom = height - 245.0
    row_gap = (bottom - top) / max(1, len(rows) - 1)
    row_accents = spec.get("row_accents", [palette["accent"]] * len(rows))

    if spec.get("kicker"):
        add_text(parent, left_label, 55, spec["kicker"], size=25, fill=palette["muted"], weight=600, css_class="label")

    for row_index, row in enumerate(rows):
        y = top + row_index * row_gap
        accent = row_accents[row_index % len(row_accents)]
        group = ET.SubElement(parent, tag("g"), {"id": f"axis-{row_index + 1}", "data-axis-id": str(row.get("id", row_index + 1))})
        add_text(group, left_label, y - 28, row.get("panel", chr(97 + row_index)), size=38, fill=accent, weight=800)
        add_text(group, left_label + 55, y - 28, row.get("label_lines", []), size=36, fill=palette["ink"], weight=700, line_gap=1.15)
        if row.get("axis_note"):
            add_text(group, left_label + 55, y + 66, row["axis_note"], size=27, fill=palette["muted"], weight=500)

        axis_attributes = {
            "x1": f"{axis_start:g}",
            "y1": f"{y:g}",
            "x2": f"{axis_end:g}",
            "y2": f"{y:g}",
            "stroke": accent,
            "stroke-width": "6",
            "data-directional": "true" if row.get("directional", False) else "false",
        }
        if row.get("directional", False):
            axis_attributes["marker-end"] = "url(#arrow)"
        ET.SubElement(group, tag("line"), axis_attributes)
        items = row["items"]
        fractions = row.get("position_fractions")
        if not isinstance(fractions, list) or len(fractions) != len(items):
            fractions = [index / (len(items) - 1) for index in range(len(items))]
        positions = [axis_start + (axis_end - axis_start - 35) * float(fraction) for fraction in fractions]
        for item_index, (x, item) in enumerate(zip(positions, items), start=1):
            marker_shape = row.get("marker", "circle")
            if marker_shape == "square":
                ET.SubElement(group, tag("rect"), {"x": f"{x - 16:g}", "y": f"{y - 16:g}", "width": "32", "height": "32", "rx": "3", "fill": palette["background"], "stroke": accent, "stroke-width": "7"})
            elif marker_shape == "diamond":
                ET.SubElement(group, tag("polygon"), {"points": f"{x:g},{y - 19:g} {x + 19:g},{y:g} {x:g},{y + 19:g} {x - 19:g},{y:g}", "fill": palette["background"], "stroke": accent, "stroke-width": "7"})
            else:
                ET.SubElement(group, tag("circle"), {"cx": f"{x:g}", "cy": f"{y:g}", "r": "16", "fill": palette["background"], "stroke": accent, "stroke-width": "7"})
            add_text(group, x, y - 66, item.get("title_lines", []), size=34, fill=palette["ink"], weight=700, anchor="middle", line_gap=1.1)
            add_text(group, x, y + 88, item.get("subtitle_lines", []), size=28, fill=palette["muted"], weight=400, anchor="middle", line_gap=1.15)

    footer_lines = spec.get("footer_lines", [])
    if footer_lines:
        add_text(parent, width / 2, height - 50, footer_lines, size=30, fill=palette["muted"], weight=600, anchor="middle", line_gap=1.2)


def render(spec: dict) -> ET.Element:
    errors = validate(spec)
    if errors:
        raise ValueError("; ".join(errors))
    root, content = add_common_root(spec)
    if spec["layout"] == "flow":
        render_flow(spec, content)
    else:
        render_independent_axes(spec, content)
    return root


def serialize(root: ET.Element) -> bytes:
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="JSON concept-figure specification")
    parser.add_argument("output", type=Path, help="SVG output path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.spec.is_file():
        print("SVG render failed: input spec does not exist", file=sys.stderr)
        return 1
    if args.output.suffix.lower() != ".svg":
        print("SVG render failed: output must use the .svg extension", file=sys.stderr)
        return 1
    if args.spec.resolve() == args.output.resolve():
        print("SVG render failed: output cannot overwrite the input spec", file=sys.stderr)
        return 1
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        payload = serialize(render(spec))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"SVG render failed: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    print(f"Wrote editable SVG: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
