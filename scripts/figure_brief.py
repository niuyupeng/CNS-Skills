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

REVIEW_VISUAL_PLAN_TYPE = "review_visual_plan"
REVIEW_ROLES = {
    "graphical_abstract",
    "overview",
    "workflow",
    "framework",
    "evidence_synthesis",
    "roadmap",
    "taxonomy_or_mechanism",
    "decision_aid",
    "table",
    "box",
}
SCENE_GRAMMAR_FIELDS = (
    "scientific_object",
    "experimental_action",
    "measurement_or_test",
    "decision_or_feedback",
    "evidence_boundary",
)
STATIC_CARD_FORMS = {"card_stack", "box_stack", "text_card_stack"}
ACCEPTED_COUNT_BASES = {
    "narrative_roles_and_verified_venue_rules",
    "narrative_roles",
    "verified_venue_rules",
}

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


def missing_scene_fields(item: dict) -> list[str]:
    grammar = item.get("scene_grammar")
    if not isinstance(grammar, dict):
        return list(SCENE_GRAMMAR_FIELDS)
    return [field for field in SCENE_GRAMMAR_FIELDS if not nonempty(grammar.get(field))]


def genuine_cross_study_synthesis(item: dict) -> bool:
    sources = item.get("evidence_sources")
    dimensions = item.get("comparison_dimensions")
    unique_sources = (
        {str(source).strip().casefold() for source in sources}
        if isinstance(sources, list)
        else set()
    )
    return (
        item.get("role") == "evidence_synthesis"
        and item.get("placement") == "main"
        and item.get("cross_study") is True
        and isinstance(sources, list)
        and len(sources) >= 2
        and len(unique_sources) >= 2
        and all(nonempty(source) for source in sources)
        and isinstance(dimensions, list)
        and bool(dimensions)
        and all(nonempty(dimension) for dimension in dimensions)
    )


def validate_review_visual_plan(plan: dict) -> list[str]:
    errors: list[str] = []
    for field in (
        "plan_type",
        "article_type",
        "target_venue",
        "display_count_basis",
        "argument_depends_on_cross_study_comparison",
        "displays",
    ):
        if field not in plan or not nonempty(plan[field]):
            errors.append(f"missing_or_empty:{field}")
    if plan.get("plan_type") != REVIEW_VISUAL_PLAN_TYPE:
        errors.append(f"unsupported_plan_type:{plan.get('plan_type', '')}")
    if not isinstance(plan.get("argument_depends_on_cross_study_comparison"), bool):
        errors.append("argument_depends_on_cross_study_comparison_must_be_boolean")
    if plan.get("display_count_basis") not in ACCEPTED_COUNT_BASES:
        errors.append("display_count_basis_must_use_roles_and_or_verified_venue_rules")
    displays = plan.get("displays")
    if displays is not None and not isinstance(displays, list):
        errors.append("displays_must_be_list")
        return sorted(set(errors))
    for index, item in enumerate(displays or []):
        prefix = f"display_{index + 1}"
        if not isinstance(item, dict):
            errors.append(f"{prefix}_must_be_object")
            continue
        for field in ("id", "role", "reader_question", "supported_claim"):
            if not nonempty(item.get(field)):
                errors.append(f"{prefix}_missing_or_empty:{field}")
        role = item.get("role")
        if role and role not in REVIEW_ROLES:
            errors.append(f"{prefix}_unsupported_role:{role}")
    return sorted(set(errors))


def audit_review_visual_plan(plan: dict) -> dict:
    errors = validate_review_visual_plan(plan)
    if errors:
        return {
            "status": "invalid",
            "errors": errors,
            "route": "stop",
            "plan_type": REVIEW_VISUAL_PLAN_TYPE,
        }

    issues: list[dict] = []

    def issue(code: str, message: str, *, display_id: str = "", severity: str = "error") -> None:
        record = {"code": code, "severity": severity, "message": message}
        if display_id:
            record["display_id"] = display_id
        issues.append(record)

    displays = plan["displays"]
    genuine = [item for item in displays if genuine_cross_study_synthesis(item)]
    comparison_required = plan["argument_depends_on_cross_study_comparison"]
    workflows = [item for item in displays if item.get("role") == "workflow"]

    if comparison_required and not genuine:
        issue(
            "missing_genuine_cross_study_evidence_synthesis",
            "The Review argument depends on cross-study comparison, but no main-text evidence-synthesis display has at least two traceable studies and explicit comparison dimensions.",
        )
        if len(workflows) >= 2:
            issue(
                "additional_workflow_does_not_replace_evidence_synthesis",
                "Multiple workflow figures are present, but an additional workflow cannot substitute for the missing cross-study evidence synthesis.",
            )

    for item in displays:
        display_id = str(item.get("id", ""))
        if item.get("role") == "evidence_synthesis" and not genuine_cross_study_synthesis(item):
            issue(
                "evidence_synthesis_not_genuine",
                "An evidence-synthesis display must be in the main text, compare at least two traceable studies, and declare compatible comparison dimensions.",
                display_id=display_id,
            )

        if item.get("biomedical_scene") is True:
            missing = missing_scene_fields(item)
            if missing:
                issue(
                    "biomedical_scene_grammar_incomplete",
                    "Missing scene layers: " + ", ".join(missing),
                    display_id=display_id,
                )
            if item.get("visual_form") in STATIC_CARD_FORMS:
                issue(
                    "static_card_or_box_stack",
                    "A biomedical scene is represented as repeated text cards rather than scientific objects, actions, tests, decisions, and boundaries.",
                    display_id=display_id,
                )

        icons = item.get("icons", [])
        if icons:
            semantics = item.get("icon_semantics")
            missing_icons = [
                str(icon)
                for icon in icons
                if not isinstance(semantics, dict) or not nonempty(semantics.get(str(icon)))
            ]
            if missing_icons:
                issue(
                    "decorative_icons_without_scientific_semantics",
                    "Icons lack a declared scientific role: " + ", ".join(missing_icons),
                    display_id=display_id,
                )

        if item.get("copy_brand_assets") is True or item.get("imitate_visual_identity") is True:
            issue(
                "proprietary_asset_or_visual_identity_copy",
                "Use independently authored geometry and transferable clarity principles; do not copy a commercial platform's assets, templates, or visual identity.",
                display_id=display_id,
            )

        components = item.get("third_party_visual_components", [])
        if components:
            if not isinstance(components, list):
                issue(
                    "third_party_visual_components_must_be_list",
                    "Third-party visual components must be recorded as a list.",
                    display_id=display_id,
                )
            else:
                for component_index, component in enumerate(components, 1):
                    required = ("name", "source", "license_or_terms", "redistribution_status")
                    if not isinstance(component, dict) or any(
                        not nonempty(component.get(field)) for field in required
                    ):
                        issue(
                            "third_party_visual_provenance_incomplete",
                            f"Third-party component {component_index} lacks source, licence/terms, or redistribution status.",
                            display_id=display_id,
                        )

    role_counts = {
        role: sum(1 for item in displays if item.get("role") == role)
        for role in sorted(REVIEW_ROLES)
        if any(item.get("role") == role for item in displays)
    }
    status = "revise" if any(item["severity"] == "error" for item in issues) else "pass"
    return {
        "status": status,
        "errors": [],
        "route": "review_visual_plan_audit",
        "plan_type": REVIEW_VISUAL_PLAN_TYPE,
        "display_count": len(displays),
        "display_count_basis": plan["display_count_basis"],
        "role_counts": role_counts,
        "genuine_cross_study_synthesis_ids": [str(item.get("id", "")) for item in genuine],
        "issues": issues,
        "qa": [
            "Verify cited studies, comparison dimensions, missingness, and prohibited inference manually.",
            "Inspect every display at final size and in the rendered manuscript.",
            "Recheck the exact venue's display and asset-policy rules before submission.",
        ],
    }


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
    role = spec.get("review_role")
    if role is not None and nonempty(role) and role not in REVIEW_ROLES:
        errors.append(f"unsupported_review_role:{role}")
    if spec.get("biomedical_scene") is True and missing_scene_fields(spec):
        errors.append("biomedical_scene_grammar_incomplete")
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
            "Do not copy commercial scientific-illustration assets, templates, or visual identity.",
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
    if nonempty(spec.get("review_role")):
        base["review_role"] = spec["review_role"]
    if spec.get("biomedical_scene") is True:
        base["scene_grammar"] = spec["scene_grammar"]

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
    scene_text = ""
    if spec.get("biomedical_scene") is True:
        grammar = spec["scene_grammar"]
        scene_text = (
            " Object-based biomedical scene grammar: "
            f"scientific object={grammar['scientific_object']}; "
            f"experimental action={grammar['experimental_action']}; "
            f"measurement/test={grammar['measurement_or_test']}; "
            f"decision/feedback={grammar['decision_or_feedback']}; "
            f"evidence boundary={grammar['evidence_boundary']}. "
            "Every icon must encode one of these scientific roles; do not use a static card or box stack."
        )
    constraints = " ".join(f"- {item}" for item in negatives)
    return (
        f"Create an editable vector scientific schematic ({spec['figure_type']}) in {spec['language']} "
        f"at {spec['width_mm']} mm × {spec['height_mm']} mm. Reader question: {spec['reader_question']} "
        f"Supported claim: {spec['supported_claim']} Layout: {spec['layout']}. Panel jobs: {panel_text}. "
        "Use a restrained, colorblind-safe palette; black or near-black text; redundant labels/shapes; "
        "consistent strokes; generous whitespace; and a reading order that is obvious without a legend. "
        f"{scene_text} "
        f"Evidence sources: {', '.join(map(str, spec['evidence_sources']))}. Constraints: {constraints}"
    )


def route_payload(payload) -> dict:
    if not isinstance(payload, dict):
        return {"status": "invalid", "errors": ["root_must_be_object"], "route": "stop"}
    if payload.get("plan_type") == REVIEW_VISUAL_PLAN_TYPE:
        return audit_review_visual_plan(payload)
    return route(payload)


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
    parser.add_argument("brief", type=Path, help="JSON scientific-figure brief or Review visual plan")
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
        result = route_payload(spec)
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
    if result["status"] in {"invalid", "revise"}:
        return 2
    if result["status"] in {"refused_generation", "blocked_pending_policy"}:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
