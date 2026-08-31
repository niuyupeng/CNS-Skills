#!/usr/bin/env python3
"""Validate a scientific-figure brief and route it to a safe production path."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CONCEPTUAL_VECTOR_TYPES = {
    "conceptual_flow",
    "conceptual_matrix",
    "independent_axes",
    "review_schematic",
}
QUANTITATIVE_TYPES = {"quantitative_plot", "data_figure", "statistical_figure"}
EXPERIMENTAL_IMAGE_TYPES = {
    "experimental_image",
    "microscopy",
    "gel_or_blot",
    "pathology",
    "spectroscopy_image",
}
GENERATIVE_ART_TYPES = {"conceptual_art", "graphical_abstract"}

BASE_REQUIRED = (
    "id",
    "language",
    "figure_type",
    "reader_question",
    "supported_claim",
    "evidence_sources",
    "prohibited_content",
    "target_venue",
    "width_mm",
    "height_mm",
)


def nonempty(value) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(nonempty(item) for item in value)
    return value is not None


def validate(spec: dict) -> list[str]:
    errors: list[str] = []
    for field in BASE_REQUIRED:
        if field not in spec or not nonempty(spec[field]):
            errors.append(f"missing_or_empty:{field}")
    figure_type = spec.get("figure_type", "")
    supported = CONCEPTUAL_VECTOR_TYPES | QUANTITATIVE_TYPES | EXPERIMENTAL_IMAGE_TYPES | GENERATIVE_ART_TYPES
    if figure_type and figure_type not in supported:
        errors.append(f"unsupported_figure_type:{figure_type}")
    for field in ("width_mm", "height_mm"):
        value = spec.get(field)
        if value is not None and (not isinstance(value, (int, float)) or value <= 0):
            errors.append(f"invalid_positive_number:{field}")
    evidence_sources = spec.get("evidence_sources")
    if evidence_sources is not None and not isinstance(evidence_sources, list):
        errors.append("evidence_sources_must_be_list")
    prohibited = spec.get("prohibited_content")
    if prohibited is not None and not isinstance(prohibited, list):
        errors.append("prohibited_content_must_be_list")
    if figure_type in QUANTITATIVE_TYPES and not nonempty(spec.get("data_source")):
        errors.append("quantitative_figure_requires_data_source")
    if figure_type in CONCEPTUAL_VECTOR_TYPES and not nonempty(spec.get("layout")):
        errors.append("conceptual_vector_requires_layout")
    return sorted(set(errors))


def route(spec: dict) -> dict:
    errors = validate(spec)
    if errors:
        return {"status": "invalid", "errors": errors, "route": "stop"}

    figure_type = spec["figure_type"]
    base = {
        "status": "ready",
        "errors": [],
        "id": spec["id"],
        "figure_type": figure_type,
        "reader_question": spec["reader_question"],
        "supported_claim": spec["supported_claim"],
        "evidence_sources": spec["evidence_sources"],
        "target_venue": spec["target_venue"],
        "final_size_mm": [spec["width_mm"], spec["height_mm"]],
        "negative_constraints": [
            "Do not invent data, sample sizes, statistics, mechanisms, citations, or validation stages.",
            "Do not imitate a publisher's proprietary visual identity or claim venue endorsement.",
            "Do not encode meaning by color alone; the figure must remain interpretable in grayscale.",
            *spec["prohibited_content"],
        ],
        "qa": [
            "Verify every label and arrow against the supported claim and cited sources.",
            "Inspect typography, line weight, contrast, clipping, and reading order at final physical size.",
            "Keep the editable source, export, brief, provenance, and human revision record together.",
            "Recheck the current official venue instructions before submission.",
        ],
    }

    if figure_type in EXPERIMENTAL_IMAGE_TYPES:
        base.update(
            {
                "status": "refused_generation",
                "route": "authentic_experimental_data_only",
                "prompt": "",
                "reason": "Experimental observations must come from authentic source data and an auditable transformation history; generative creation or content alteration is not permitted.",
            }
        )
        return base

    if figure_type in QUANTITATIVE_TYPES:
        base.update(
            {
                "route": "code_from_data",
                "prompt": "",
                "production_contract": [
                    f"Use only the declared data source: {spec['data_source']}",
                    "Generate the plot from data and code; preserve the independent unit, denominators, uncertainty, and statistical definitions.",
                    "Return plotting data, code, editable vector export, and the submission export.",
                ],
            }
        )
        return base

    if figure_type in CONCEPTUAL_VECTOR_TYPES:
        base.update(
            {
                "route": "editable_svg",
                "prompt": build_vector_prompt(spec, base["negative_constraints"]),
                "production_contract": [
                    "Return an editable SVG with real text nodes, semantic groups, title/description metadata, and no embedded raster image.",
                    "Keep labels concise and place interpretation in the caption rather than inside decorative callouts.",
                    "Export a high-resolution manuscript preview only after the SVG passes structural and final-size QA.",
                ],
            }
        )
        return base

    permitted = spec.get("generative_art_permitted") is True
    if not permitted:
        base.update(
            {
                "status": "blocked_pending_policy",
                "route": "verify_venue_ai_policy",
                "prompt": "",
                "reason": "Conceptual generative artwork requires explicit venue-policy and disclosure clearance.",
            }
        )
        return base

    base.update(
        {
            "route": "conceptual_image_generation",
            "prompt": build_art_prompt(spec, base["negative_constraints"]),
            "production_contract": [
                "Label the asset as conceptual/illustrative and keep prompt, model/tool, date, output, and human edits in the provenance record.",
                "Add final scientific labels manually in an editable layout rather than trusting generated text.",
                "Do not use the output as experimental evidence or as a substitute for a data figure.",
            ],
        }
    )
    return base


def build_vector_prompt(spec: dict, negatives: list[str]) -> str:
    panels = spec.get("panels", [])
    panel_text = "; ".join(
        f"{panel.get('id', index + 1)}: {panel.get('job', '')}" for index, panel in enumerate(panels)
    ) or "single coherent panel"
    constraints = " ".join(f"- {item}" for item in negatives)
    return (
        f"Create an editable vector scientific schematic ({spec['figure_type']}) in {spec['language']} "
        f"at {spec['width_mm']} mm × {spec['height_mm']} mm. Reader question: {spec['reader_question']} "
        f"Supported claim: {spec['supported_claim']} Layout: {spec['layout']}. Panel jobs: {panel_text}. "
        "Use a restrained, colorblind-safe palette; black or near-black text; redundant labels/shapes; "
        "consistent strokes; generous whitespace; and a reading order that is obvious without a legend. "
        f"Evidence sources: {', '.join(map(str, spec['evidence_sources']))}. Constraints: {constraints}"
    )


def build_art_prompt(spec: dict, negatives: list[str]) -> str:
    constraints = " ".join(f"- {item}" for item in negatives)
    return (
        f"Create a clearly conceptual, non-data scientific illustration in {spec['language']} at "
        f"{spec['width_mm']} mm × {spec['height_mm']} mm. Reader question: {spec['reader_question']} "
        f"Bounded takeaway: {spec['supported_claim']} Use a simple left-to-right or top-to-bottom reading path, "
        "minimal text, restrained color, ample whitespace, and no decorative mechanism beyond the stated evidence. "
        "Leave final labels for manual vector typesetting. The image must be identifiable as illustrative rather than observed data. "
        f"Constraints: {constraints}"
    )


def make_shareable(result: dict) -> dict:
    shared = json.loads(json.dumps(result))
    if "production_contract" in shared:
        shared["production_contract"] = list(shared["production_contract"])
    return shared


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="JSON scientific-figure brief")
    parser.add_argument("--json", type=Path, help="Write routed brief as JSON")
    parser.add_argument("--shareable", action="store_true", help="Emit only the routed brief; source path is never included")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.brief.is_file():
        print("figure brief failed: input JSON does not exist", file=sys.stderr)
        return 1
    if args.json and args.json.resolve() == args.brief.resolve():
        print("figure brief failed: JSON output cannot overwrite the input", file=sys.stderr)
        return 1
    try:
        spec = json.loads(args.brief.read_text(encoding="utf-8"))
        result = route(spec)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"figure brief failed: {exc}", file=sys.stderr)
        return 1
    if args.shareable:
        result = make_shareable(result)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    if result["status"] == "invalid":
        return 2
    if result["status"] in {"refused_generation", "blocked_pending_policy"}:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
