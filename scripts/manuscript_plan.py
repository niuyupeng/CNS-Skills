#!/usr/bin/env python3
"""Audit declarations in an author-led manuscript plan before drafting or delivery."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


VERSION = "0.12.0"
PLAN_TYPE = "manuscript_development_plan"
STAGES = {
    "positioning_brief",
    "one_page_outline",
    "detailed_outline",
    "evidence_matrix",
    "author_first_draft",
    "full_draft",
    "plain_language_brief",
    "submission_copy",
}
GENRES = {"review", "original_research", "leading_conference", "other"}
SOURCE_ROLES = {
    "authoritative_content",
    "format_reference",
    "visual_reference",
    "verified_evidence",
    "candidate_evidence",
    "background_only",
}
DECISION_STATUSES = {
    "author_confirmed",
    "source_explicit",
    "inferred_synthesis",
    "assistant_proposal",
    "pending_author_decision",
    "superseded",
}
CLAIM_STATUSES = {"supported", "author_result", "provisional", "pending", "unsupported"}
EVIDENCE_STATUSES = {
    "verified",
    "author_supplied_result",
    "metadata_only",
    "candidate",
    "pending",
}
CLAIM_TYPES = {
    "background",
    "association",
    "causal",
    "mechanism",
    "experimental_effect",
    "clinical",
    "method",
    "synthesis",
    "novelty",
    "completeness",
}
EVIDENCE_SOURCE_TYPES = {
    "author_result",
    "primary_study",
    "review",
    "perspective_or_commentary",
    "preprint",
    "dataset",
    "protocol_or_standard",
    "other",
}
METADATA_STATUSES = {"verified", "author_supplied", "pending", "not_applicable"}
FULL_TEXT_STATUSES = {"located", "author_supplied", "not_located", "not_applicable"}
ENTAILMENT_STATUSES = {"verified", "author_supplied", "pending", "not_checked"}
PUBLICATION_STATUSES = {
    "published",
    "online_first",
    "preprint",
    "author_unpublished",
    "unknown",
    "not_applicable",
}
SOURCE_SUFFICIENCY = {
    "topic_only",
    "author_notes",
    "verified_literature",
    "author_results",
    "approved_outline_and_evidence",
    "complete_source_package",
}
APPROVAL_STATES = {
    "pending_author_approval",
    "author_approved",
    "source_explicit",
    "not_required",
}
DRAFT_STAGES = {"author_first_draft", "full_draft", "submission_copy"}
COMPLETE_STAGES = {"full_draft", "submission_copy"}
CONTENT_SOURCE_ROLES = {"authoritative_content", "verified_evidence"}
EVIDENCE_SOURCE_ROLES = CONTENT_SOURCE_ROLES | {"candidate_evidence"}
DATA_READINESS_FIELDS = {
    "independent_unit",
    "material_or_population_identity",
    "process_batch_or_site",
    "measurement_and_timepoint",
    "missingness_failures_and_negatives",
    "provenance_and_version",
    "split_or_feedback_eligibility",
}
VAGUE_RECORD = re.compile(
    r"\b(?:several|multiple|various|many)\s+(?:recent\s+)?(?:studies|papers|works)\b|"
    r"近年(?:研究|工作)|多个(?:研究|工作)|多项研究|系列研究",
    flags=re.IGNORECASE,
)
GENERIC_SUPPORT = re.compile(
    r"^\s*(?:verified|checked|yes|doi|abstract|full[- ]?text|paper|article|source|"
    r"record|results?|n/?a|not applicable)\s*$",
    flags=re.IGNORECASE,
)
PLACEHOLDER_VALUE = re.compile(
    r"^\s*(?:done|yes|no|n/?a|tbd|todo|complete|completed|checked|verified|"
    r"recorded|available|provided|same|none|unknown|google)\s*$",
    flags=re.IGNORECASE,
)


def normalize_genre(value) -> str | None:
    if not isinstance(value, str):
        return None
    token = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    aliases = {
        "review": "review",
        "review_article": "review",
        "narrative_review": "review",
        "systematic_review": "review",
        "scoping_review": "review",
        "original_research": "original_research",
        "original_research_article": "original_research",
        "research_article": "original_research",
        "original_article": "original_research",
        "leading_conference": "leading_conference",
        "top_conference": "leading_conference",
        "conference_paper": "leading_conference",
        "other": "other",
    }
    return aliases.get(token)


def meaningful_text(value) -> bool:
    return nonempty_string(value) and PLACEHOLDER_VALUE.fullmatch(value) is None


def nonempty(value) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


def nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value) -> bool:
    return isinstance(value, list) and all(nonempty_string(item) for item in value)


def duplicate_ids(items: list[dict]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        item_id = str(item.get("id", "")).strip()
        if item_id in seen:
            duplicates.add(item_id)
        seen.add(item_id)
    return sorted(item_id for item_id in duplicates if item_id)


def validate(plan) -> list[str]:
    if not isinstance(plan, dict):
        return ["root_must_be_object"]

    errors: list[str] = []
    for field in (
        "plan_type",
        "artifact_stage",
        "genre",
        "target_reader",
        "source_language",
        "final_language",
        "source_sufficiency",
        "artifact_contract",
        "positioning_lock",
        "authoritative_inputs",
        "decision_provenance",
        "claims",
        "evidence_records",
        "section_contracts",
        "display_plan",
        "reader_visible_internal_labels",
        "unresolved_items",
    ):
        if field not in plan:
            errors.append(f"missing:{field}")

    if plan.get("plan_type") != PLAN_TYPE:
        errors.append(f"unsupported_plan_type:{plan.get('plan_type', '')}")
    if not isinstance(plan.get("artifact_stage"), str) or plan.get("artifact_stage") not in STAGES:
        errors.append(f"unsupported_artifact_stage:{plan.get('artifact_stage', '')}")
    if not isinstance(plan.get("genre"), str) or plan.get("genre") not in GENRES:
        errors.append(f"unsupported_genre:{plan.get('genre', '')}")
    if (
        not isinstance(plan.get("source_sufficiency"), str)
        or plan.get("source_sufficiency") not in SOURCE_SUFFICIENCY
    ):
        errors.append(f"unsupported_source_sufficiency:{plan.get('source_sufficiency', '')}")
    for field in ("target_reader", "source_language", "final_language"):
        if field in plan and not nonempty_string(plan.get(field)):
            errors.append(f"missing_or_empty:{field}")

    list_fields = (
        "authoritative_inputs",
        "decision_provenance",
        "claims",
        "evidence_records",
        "section_contracts",
        "display_plan",
        "reader_visible_internal_labels",
        "unresolved_items",
    )
    for field in list_fields:
        if field in plan and not isinstance(plan[field], list):
            errors.append(f"{field}_must_be_list")

    contract = plan.get("artifact_contract")
    if contract is not None and not isinstance(contract, dict):
        errors.append("artifact_contract_must_be_object")
    elif isinstance(contract, dict):
        for field in ("format", "length_or_page_budget"):
            if not nonempty_string(contract.get(field)):
                errors.append(f"artifact_contract_missing_or_empty:{field}")
        if "editable" not in contract:
            errors.append("artifact_contract_missing_or_empty:editable")
        elif not isinstance(contract.get("editable"), bool):
            errors.append("artifact_contract_editable_must_be_boolean")
        if (
            not isinstance(contract.get("approval_state"), str)
            or contract.get("approval_state") not in APPROVAL_STATES
        ):
            errors.append(
                f"artifact_contract_unsupported_approval_state:{contract.get('approval_state', '')}"
            )

    positioning = plan.get("positioning_lock")
    if positioning is not None and not isinstance(positioning, dict):
        errors.append("positioning_lock_must_be_object")
    elif isinstance(positioning, dict):
        for field in (
            "article_type",
            "article_family",
            "central_question",
            "primary_organizing_axis",
            "differentiated_value",
            "boundaries",
        ):
            if field == "boundaries":
                if not nonempty(positioning.get(field)):
                    errors.append(f"positioning_lock_missing_or_empty:{field}")
            elif not nonempty_string(positioning.get(field)):
                errors.append(f"positioning_lock_missing_or_empty:{field}")
        if not string_list(positioning.get("secondary_comparison_axes", [])):
            errors.append("secondary_comparison_axes_must_be_string_list")
        if not string_list(positioning.get("competing_primary_axes", [])):
            errors.append("competing_primary_axes_must_be_string_list")
        boundaries = positioning.get("boundaries")
        if not nonempty_string(boundaries) and not (
            isinstance(boundaries, list) and bool(boundaries) and string_list(boundaries)
        ):
            errors.append("positioning_lock_boundaries_must_be_string_or_string_list")
        family = positioning.get("article_family")
        if not isinstance(family, str) or family not in GENRES:
            errors.append(f"positioning_lock_unsupported_article_family:{family}")

    item_rules = {
        "authoritative_inputs": ("id", "role", "locator"),
        "decision_provenance": ("id", "decision", "status", "source_id"),
        "claims": (
            "id",
            "text",
            "claim_type",
            "status",
            "validation_scope",
            "evidence_ids",
        ),
        "evidence_records": (
            "id",
            "source_id",
            "source_type",
            "verification_status",
            "metadata_status",
            "full_text_status",
            "entailment_status",
            "publication_status",
            "supported_claim_types",
            "validation_scope",
            "support_locator",
            "exact_support",
        ),
        "section_contracts": (
            "id",
            "heading",
            "reader_question",
            "job",
            "claim_ids",
            "evidence_ids",
            "display_roles",
            "evidence_gap",
            "boundary",
        ),
        "display_plan": (
            "id",
            "role",
            "reader_question",
            "claim_ids",
            "evidence_ids",
            "source_class",
            "editable_output",
        ),
        "unresolved_items": ("id", "question", "owner", "reader_visible"),
    }
    for field, required in item_rules.items():
        items = plan.get(field)
        if not isinstance(items, list):
            continue
        for index, item in enumerate(items, 1):
            if not isinstance(item, dict):
                errors.append(f"{field}_{index}_must_be_object")
                continue
            for required_field in required:
                value = item.get(required_field)
                if required_field in {"reader_visible", "editable_output"}:
                    if not isinstance(value, bool):
                        errors.append(f"{field}_{index}_{required_field}_must_be_boolean")
                elif required_field.endswith("_ids") or required_field in {
                    "display_roles",
                    "supported_claim_types",
                }:
                    if not string_list(value):
                        errors.append(f"{field}_{index}_{required_field}_must_be_string_list")
                elif not nonempty_string(value):
                    errors.append(f"{field}_{index}_missing_or_empty:{required_field}")
        for item_id in duplicate_ids([item for item in items if isinstance(item, dict)]):
            errors.append(f"{field}_duplicate_id:{item_id}")

    for index, item in enumerate(plan.get("authoritative_inputs", []) or [], 1):
        if (
            isinstance(item, dict)
            and (not isinstance(item.get("role"), str) or item.get("role") not in SOURCE_ROLES)
        ):
            errors.append(f"authoritative_inputs_{index}_unsupported_role:{item.get('role', '')}")
    for index, item in enumerate(plan.get("decision_provenance", []) or [], 1):
        if (
            isinstance(item, dict)
            and (
                not isinstance(item.get("status"), str)
                or item.get("status") not in DECISION_STATUSES
            )
        ):
            errors.append(f"decision_provenance_{index}_unsupported_status:{item.get('status', '')}")
    for index, item in enumerate(plan.get("claims", []) or [], 1):
        if isinstance(item, dict):
            if not isinstance(item.get("status"), str) or item.get("status") not in CLAIM_STATUSES:
                errors.append(f"claims_{index}_unsupported_status:{item.get('status', '')}")
            if not isinstance(item.get("claim_type"), str) or item.get("claim_type") not in CLAIM_TYPES:
                errors.append(f"claims_{index}_unsupported_claim_type:{item.get('claim_type', '')}")
    for index, item in enumerate(plan.get("evidence_records", []) or [], 1):
        if isinstance(item, dict):
            enum_fields = (
                ("verification_status", EVIDENCE_STATUSES),
                ("source_type", EVIDENCE_SOURCE_TYPES),
                ("metadata_status", METADATA_STATUSES),
                ("full_text_status", FULL_TEXT_STATUSES),
                ("entailment_status", ENTAILMENT_STATUSES),
                ("publication_status", PUBLICATION_STATUSES),
            )
            for field, allowed in enum_fields:
                value = item.get(field)
                if not isinstance(value, str) or value not in allowed:
                    errors.append(f"evidence_records_{index}_unsupported_{field}:{value}")
            supported = item.get("supported_claim_types")
            if not isinstance(supported, list) or not supported:
                errors.append(f"evidence_records_{index}_supported_claim_types_must_be_nonempty")
            elif any(
                not isinstance(claim_type, str) or claim_type not in CLAIM_TYPES
                for claim_type in supported
            ):
                errors.append(f"evidence_records_{index}_unsupported_supported_claim_type")

    labels = plan.get("reader_visible_internal_labels")
    if isinstance(labels, list) and not string_list(labels):
        errors.append("reader_visible_internal_labels_must_be_string_list")

    continuity = plan.get("continuity")
    if continuity is not None:
        if not isinstance(continuity, dict):
            errors.append("continuity_must_be_object")
        else:
            for field in ("active_decision_ids", "superseded_decision_ids"):
                if field in continuity and not string_list(continuity[field]):
                    errors.append(f"continuity_{field}_must_be_string_list")
            if "project_record_read" in continuity and not isinstance(
                continuity["project_record_read"], bool
            ):
                errors.append("continuity_project_record_read_must_be_boolean")

    for lock_name in ("title_lock", "genre_lock"):
        lock = plan.get(lock_name)
        if lock is not None and not isinstance(lock, dict):
            errors.append(f"{lock_name}_must_be_object")
        elif isinstance(lock, dict):
            status = lock.get("status")
            allowed = (
                {"unchanged", "proposal", "author_approved"}
                if lock_name == "title_lock"
                else {"unchanged", "source_explicit", "proposal", "author_approved"}
            )
            if status is not None and (not isinstance(status, str) or status not in allowed):
                errors.append(f"{lock_name}_unsupported_status:{status}")
            for field in (
                ("source_title", "working_title")
                if lock_name == "title_lock"
                else ("source_genre", "working_genre")
            ):
                if field in lock and not nonempty_string(lock.get(field)):
                    errors.append(f"{lock_name}_missing_or_empty:{field}")

    if "genre_contract" in plan and not isinstance(plan.get("genre_contract"), dict):
        errors.append("genre_contract_must_be_object")

    return sorted(set(errors))


def audit(plan) -> dict:
    errors = validate(plan)
    if errors:
        return {
            "status": "invalid",
            "route": "stop",
            "verification_scope": "declared_plan_only",
            "errors": errors,
            "issues": [],
        }

    issues: list[dict] = []

    def issue(code: str, message: str, *, severity: str = "revise", item_id: str = "") -> None:
        record = {"code": code, "severity": severity, "message": message}
        if item_id:
            record["item_id"] = item_id
        issues.append(record)

    stage = plan["artifact_stage"]
    contract = plan["artifact_contract"]
    positioning = plan["positioning_lock"]
    inputs = {item["id"]: item for item in plan["authoritative_inputs"]}
    decisions = {item["id"]: item for item in plan["decision_provenance"]}
    evidence = {item["id"]: item for item in plan["evidence_records"]}
    claims = {item["id"]: item for item in plan["claims"]}

    if positioning.get("article_family") != plan["genre"]:
        issue(
            "genre_positioning_mismatch",
            "The routed genre and the positioning lock disagree; do not draft until the article family is resolved.",
            severity="block",
        )

    if stage == "evidence_matrix" and not evidence:
        issue(
            "empty_evidence_matrix",
            "An evidence matrix must contain at least one traceable evidence or candidate record.",
            severity="block",
        )

    if stage == "author_first_draft" and plan["source_sufficiency"] not in {
        "approved_outline_and_evidence",
        "complete_source_package",
    }:
        issue(
            "first_draft_source_package_insufficient",
            "An author-led first draft requires an approved outline with traceable evidence, or a complete source package.",
            severity="block",
        )

    if stage in COMPLETE_STAGES and plan["source_sufficiency"] != "complete_source_package":
        issue(
            "complete_draft_source_package_insufficient",
            "A full draft or submission copy requires a complete declared source package; notes or verified literature alone are not enough.",
            severity="block",
        )

    if stage in DRAFT_STAGES:
        if not claims:
            issue(
                "draft_has_no_claim_map",
                "A manuscript draft requires at least one consequential claim in the plan.",
                severity="block",
            )
        if not evidence:
            issue(
                "draft_has_no_evidence_map",
                "A manuscript draft requires at least one traceable author-result or literature evidence record.",
                severity="block",
            )

    if stage == "plain_language_brief" and not claims:
        issue(
            "brief_has_no_scientific_claim",
            "A scientific brief must map to at least one bounded manuscript claim rather than a topic alone.",
            severity="block",
        )

    if stage in {
        "one_page_outline",
        "detailed_outline",
        "author_first_draft",
        "full_draft",
        "submission_copy",
    } and not plan["display_plan"]:
        issue(
            "display_plan_missing",
            "Record the visual roles needed by the argument, even when the final decision is that a section needs no display.",
            severity="block" if stage in DRAFT_STAGES else "revise",
        )

    if stage in {"detailed_outline", *DRAFT_STAGES}:
        genre_contract = plan.get("genre_contract")
        missing_genre_fields: list[str] = []
        if not isinstance(genre_contract, dict):
            missing_genre_fields.append("genre_contract")
        elif plan["genre"] == "review":
            for field in ("synthesis_units", "comparison_dimensions", "coverage_boundary"):
                if not nonempty(genre_contract.get(field)):
                    missing_genre_fields.append(field)
        elif plan["genre"] == "original_research":
            for field in ("inference_chain", "alternative_explanations", "result_figure_map"):
                if not nonempty(genre_contract.get(field)):
                    missing_genre_fields.append(field)
        elif plan["genre"] == "leading_conference":
            for field in (
                "contribution",
                "comparators",
                "robustness",
                "error_analysis",
                "page_budget_status",
            ):
                if not nonempty(genre_contract.get(field)):
                    missing_genre_fields.append(field)
        if missing_genre_fields:
            issue(
                "genre_contract_incomplete",
                "The genre-specific development contract is missing: "
                + ", ".join(missing_genre_fields),
                severity="block" if stage in DRAFT_STAGES else "revise",
            )

    if positioning.get("competing_primary_axes"):
        issue(
            "competing_primary_axes",
            "Only one organizing axis may own the main section architecture; move the others to secondary comparisons or obtain an explicit architecture decision.",
        )

    for decision in decisions.values():
        source = inputs.get(decision["source_id"])
        if source is None:
            issue(
                "decision_source_missing",
                "A consequential decision points to an unknown source.",
                severity="block",
                item_id=decision["id"],
            )
            continue
        if decision["status"] in {"author_confirmed", "source_explicit"} and source["role"] in {
            "format_reference",
            "visual_reference",
            "background_only",
        }:
            issue(
                "decision_authority_mismatch",
                "A formatting, visual, or background reference cannot establish an author or meeting decision.",
                severity="block",
                item_id=decision["id"],
            )

    continuity = plan.get("continuity", {})
    if continuity and not isinstance(continuity, dict):
        issue("continuity_must_be_object", "Continuity must be recorded as an object.", severity="block")
    elif isinstance(continuity, dict):
        active = set(continuity.get("active_decision_ids", []))
        retired = set(continuity.get("superseded_decision_ids", []))
        if (active or retired) and continuity.get("project_record_read") is not True:
            issue(
                "project_continuity_not_read",
                "Active or superseded project decisions cannot be used until the declared continuity record has been read.",
                severity="block" if stage in DRAFT_STAGES else "revise",
            )
        overlap = sorted(active & retired)
        if overlap:
            issue(
                "active_and_superseded_decision_conflict",
                "The same decision is marked both active and superseded: " + ", ".join(overlap),
                severity="block",
            )
        for decision_id in active:
            if decision_id not in decisions:
                issue(
                    "active_decision_missing",
                    "An active decision ID is absent from the provenance ledger.",
                    severity="block",
                    item_id=str(decision_id),
                )
            elif decisions[decision_id]["status"] == "superseded":
                issue(
                    "superseded_decision_reactivated",
                    "A superseded decision cannot remain active without a new explicit author decision.",
                    severity="block",
                    item_id=str(decision_id),
                )
            elif decisions[decision_id]["status"] in {
                "assistant_proposal",
                "inferred_synthesis",
                "pending_author_decision",
            }:
                issue(
                    "unapproved_decision_controls_architecture",
                    "An assistant proposal, inference, or pending decision cannot control the active manuscript architecture without author approval.",
                    severity="block" if stage in DRAFT_STAGES else "revise",
                    item_id=str(decision_id),
                )

    if len(inputs) > 1 and stage in {
        "one_page_outline",
        "detailed_outline",
        *DRAFT_STAGES,
    } and not decisions:
        issue(
            "multiple_sources_without_decision_provenance",
            "When several inputs can affect the manuscript, record which source owns each consequential decision.",
            severity="block" if stage in DRAFT_STAGES else "revise",
        )

    title_lock = plan.get("title_lock", {})
    if title_lock:
        if not isinstance(title_lock, dict):
            issue("title_lock_must_be_object", "Title lock must be an object.", severity="block")
        else:
            source_title = str(title_lock.get("source_title", "")).strip()
            working_title = str(title_lock.get("working_title", "")).strip()
            status = title_lock.get("status")
            if source_title and working_title and source_title != working_title and status not in {
                "author_approved",
                "proposal",
            }:
                issue(
                    "unapproved_title_drift",
                    "A changed title must remain a proposal or be explicitly author-approved before it replaces the source title.",
                    severity="block",
                )
            elif (
                stage == "submission_copy"
                and source_title
                and working_title
                and source_title != working_title
                and status != "author_approved"
            ):
                issue(
                    "proposed_title_in_submission_copy",
                    "A submission copy cannot silently promote a proposed title; obtain author approval first.",
                    severity="block",
                )

    genre_lock = plan.get("genre_lock")
    if genre_lock:
        if not isinstance(genre_lock, dict):
            issue("genre_lock_must_be_object", "Genre lock must be an object.", severity="block")
        else:
            source_genre = str(genre_lock.get("source_genre", "")).strip()
            working_genre = str(genre_lock.get("working_genre", "")).strip()
            status = genre_lock.get("status")
            normalized_working_genre = normalize_genre(working_genre)
            if normalized_working_genre is not None and normalized_working_genre != plan["genre"]:
                issue(
                    "genre_lock_route_mismatch",
                    "The genre lock's working article type disagrees with the active genre route and positioning family.",
                    severity="block",
                )
            if source_genre and working_genre and source_genre != working_genre:
                if status not in {"proposal", "author_approved"}:
                    issue(
                        "untracked_genre_drift",
                        "A change in article type must be recorded as a proposal or author-approved decision.",
                        severity="block",
                    )
                elif stage in DRAFT_STAGES and status != "author_approved":
                    issue(
                        "unapproved_genre_change_in_draft",
                        "Do not draft under a changed article type until the author approves the genre change.",
                        severity="block",
                    )

    if plan["source_sufficiency"] == "topic_only" and stage in DRAFT_STAGES:
        issue(
            "topic_only_cannot_support_draft",
            "A topic alone supports positioning, a provisional outline, and an evidence-acquisition plan—not an evidence-complete manuscript draft.",
            severity="block",
        )

    if stage in DRAFT_STAGES and contract.get("approval_state") not in {
        "author_approved",
        "source_explicit",
        "not_required",
    }:
        issue(
            "draft_started_before_author_approval",
            "Do not advance to a manuscript draft while the positioning or outline approval checkpoint is still pending.",
            severity="block",
        )
    elif stage in DRAFT_STAGES:
        approval_source_id = contract.get("approval_source_id")
        approval_source = inputs.get(approval_source_id) if isinstance(approval_source_id, str) else None
        if approval_source is None or approval_source.get("role") != "authoritative_content":
            issue(
                "draft_approval_source_missing",
                "A draft-stage approval must point to an authoritative author or project source; `not_required` is not a provenance bypass.",
                severity="block",
            )

    content_sources = {
        source_id for source_id, item in inputs.items() if item["role"] in CONTENT_SOURCE_ROLES
    }
    if stage in DRAFT_STAGES and not content_sources:
        issue(
            "draft_has_no_authoritative_content",
            "Drafting requires author-owned content or verified evidence; formatting and background references are not sufficient.",
            severity="block",
        )

    for claim in claims.values():
        claim_evidence = claim.get("evidence_ids", [])
        if claim["status"] in {"supported", "author_result"} and not claim_evidence:
            issue(
                "supported_claim_has_no_evidence",
                "A supported or author-result claim must point to a traceable evidence record.",
                severity="block",
                item_id=claim["id"],
            )
        for evidence_id in claim_evidence:
            record = evidence.get(evidence_id)
            if record is None:
                issue(
                    "claim_evidence_missing",
                    "A claim points to an unknown evidence record.",
                    severity="block",
                    item_id=claim["id"],
                )
                continue
            source = inputs.get(record["source_id"])
            if source is None:
                issue(
                    "evidence_source_missing",
                    "An evidence record points to an unknown source.",
                    severity="block",
                    item_id=evidence_id,
                )
            elif source["role"] not in EVIDENCE_SOURCE_ROLES:
                issue(
                    "noncontent_source_used_as_evidence",
                    "A format, visual, or background reference cannot support a manuscript claim.",
                    severity="block",
                    item_id=evidence_id,
                )
            if claim["claim_type"] not in record.get("supported_claim_types", []):
                issue(
                    "claim_type_not_supported_by_evidence_record",
                    "The evidence record does not declare support for this claim type.",
                    severity="block",
                    item_id=claim["id"],
                )
            if record.get("source_type") in {"review", "perspective_or_commentary"} and claim[
                "claim_type"
            ] in {"causal", "mechanism", "experimental_effect", "clinical"}:
                issue(
                    "secondary_source_used_for_primary_claim",
                    "A Review, Perspective, or commentary cannot be the sole record for a specific causal, mechanistic, experimental-effect, or clinical claim.",
                    severity="block",
                    item_id=claim["id"],
                )
            if claim["claim_type"] == "clinical" and not re.search(
                r"\b(?:clinical|human|patient|participant)\b",
                str(record.get("validation_scope", "")),
                flags=re.IGNORECASE,
            ):
                issue(
                    "clinical_claim_scope_mismatch",
                    "A clinical claim requires a record whose declared validation scope includes human participants or clinical evidence.",
                    severity="block",
                    item_id=claim["id"],
                )
            if claim["status"] in {"supported", "author_result"} and record["verification_status"] in {
                "metadata_only",
                "candidate",
                "pending",
            }:
                issue(
                    "claim_outruns_evidence_state",
                    "A supported claim relies on evidence whose entailment or author-result status is not established.",
                    severity="block" if stage in COMPLETE_STAGES else "revise",
                    item_id=claim["id"],
                )
        if stage == "author_first_draft" and claim["status"] in {
            "provisional",
            "pending",
            "unsupported",
        }:
            issue(
                "unfinished_claim_in_first_draft",
                "A reader-visible first draft cannot present a provisional, pending, or unsupported plan item as established prose; omit it or resolve it first.",
                severity="block" if claim["status"] == "unsupported" else "revise",
                item_id=claim["id"],
            )
        if stage in COMPLETE_STAGES and claim["status"] in {"provisional", "pending", "unsupported"}:
            issue(
                "incomplete_claim_in_complete_draft",
                "A complete or submission draft cannot present a provisional, pending, or unsupported claim as finished content.",
                severity="block",
                item_id=claim["id"],
            )

    for record in evidence.values():
        source = inputs.get(record.get("source_id"))
        if source is None:
            issue(
                "orphan_evidence_source",
                "Every evidence record must point to a declared source, even when no current claim cites it.",
                severity="block",
                item_id=record["id"],
            )
        elif source.get("role") not in EVIDENCE_SOURCE_ROLES:
            issue(
                "evidence_record_uses_noncontent_source",
                "An evidence record cannot be grounded in a format, visual, or background-only source.",
                severity="block",
                item_id=record["id"],
            )

        if record.get("verification_status") == "verified":
            required_states = {
                "metadata_status": "verified",
                "full_text_status": "located",
                "entailment_status": "verified",
            }
            mismatched = [
                f"{field}={record.get(field)}"
                for field, required_value in required_states.items()
                if record.get(field) != required_value
            ]
            if record.get("publication_status") in {"unknown", "not_applicable"}:
                mismatched.append(f"publication_status={record.get('publication_status')}")
            if mismatched:
                issue(
                    "verified_summary_outruns_evidence_states",
                    "The summary state `verified` requires verified metadata, located full text, verified entailment, and a known publication state: "
                    + ", ".join(mismatched),
                    severity="block",
                    item_id=record["id"],
                )

        if record.get("verification_status") == "author_supplied_result":
            author_states_ok = (
                record.get("source_type") == "author_result"
                and record.get("metadata_status") in {"author_supplied", "not_applicable"}
                and record.get("full_text_status") in {"author_supplied", "not_applicable"}
                and record.get("entailment_status") == "author_supplied"
                and record.get("publication_status") in {"author_unpublished", "not_applicable"}
            )
            if not author_states_ok:
                issue(
                    "author_result_state_inconsistent",
                    "An author-supplied result must remain distinct from externally verified literature and trace to an author-owned record.",
                    severity="block",
                    item_id=record["id"],
                )

        exact_support = str(record.get("exact_support", ""))
        support_locator = str(record.get("support_locator", ""))
        source_locator = str(inputs.get(record.get("source_id"), {}).get("locator", ""))
        if (
            VAGUE_RECORD.search(exact_support)
            or VAGUE_RECORD.search(source_locator)
            or (
                record.get("verification_status") == "verified"
                and (
                    GENERIC_SUPPORT.fullmatch(exact_support) is not None
                    or GENERIC_SUPPORT.fullmatch(support_locator) is not None
                )
            )
        ):
            issue(
                "vague_evidence_placeholder",
                "A verified evidence record needs a unique source and exact support location; vague placeholders belong in the candidate list.",
                severity="block" if record.get("verification_status") == "verified" else "revise",
                item_id=record["id"],
            )

    for section in plan["section_contracts"]:
        for claim_id in section.get("claim_ids", []):
            if claim_id not in claims:
                issue(
                    "section_claim_missing",
                    "A section contract points to an unknown claim.",
                    severity="block",
                    item_id=section["id"],
                )
        for evidence_id in section.get("evidence_ids", []):
            if evidence_id not in evidence:
                issue(
                    "section_evidence_missing",
                    "A section contract points to an unknown evidence record.",
                    severity="block",
                    item_id=section["id"],
                )
        if stage in {
            "one_page_outline",
            "detailed_outline",
            *DRAFT_STAGES,
        } and not section.get("claim_ids"):
            issue(
                "section_has_no_claim_job",
                "Each planned section needs at least one claim or comparison outcome; a heading alone is not a section contract.",
                severity="block" if stage in DRAFT_STAGES else "revise",
                item_id=section["id"],
            )

    for display in plan["display_plan"]:
        for claim_id in display.get("claim_ids", []):
            if claim_id not in claims:
                issue(
                    "display_claim_missing",
                    "A planned display points to an unknown claim.",
                    severity="block",
                    item_id=display["id"],
                )
        for evidence_id in display.get("evidence_ids", []):
            if evidence_id not in evidence:
                issue(
                    "display_evidence_missing",
                    "A planned display points to an unknown evidence record.",
                    severity="block",
                    item_id=display["id"],
                )
        if not display.get("claim_ids") and not display.get("evidence_ids"):
            issue(
                "display_has_no_argument_mapping",
                "A display needs a mapped claim or evidence role; decoration is not an argument plan.",
                severity="block" if stage in DRAFT_STAGES else "revise",
                item_id=display["id"],
            )

    if stage in {"one_page_outline", "detailed_outline", "author_first_draft", "full_draft", "submission_copy"}:
        if not plan["section_contracts"]:
            issue(
                "missing_section_contracts",
                "This stage requires sections with a reader question, scientific job, evidence mapping, and boundary.",
                severity="block" if stage in DRAFT_STAGES else "revise",
            )

    labels = [str(label).strip() for label in plan["reader_visible_internal_labels"] if str(label).strip()]
    if labels:
        issue(
            "internal_scaffolding_exposed",
            "Editorial labels, prompts, codes, TODOs, or decision scaffolding must stay outside the reader-visible manuscript: "
            + ", ".join(labels),
        )

    for unresolved in plan["unresolved_items"]:
        if unresolved["reader_visible"] is True:
            issue(
                "unresolved_item_exposed_to_reader",
                "Move unresolved author/editor questions to the decision log or requested comments, not the clean manuscript.",
                item_id=unresolved["id"],
            )

    architecture_delta = plan.get("architecture_delta")
    if plan.get("claims_substantive_new_version") is True:
        if not isinstance(architecture_delta, dict) or not any(
            nonempty(architecture_delta.get(field))
            for field in (
                "governing_question_change",
                "primary_axis_change",
                "section_function_change",
                "reader_decision_change",
                "evidence_placement_change",
            )
        ):
            issue(
                "no_substantive_architecture_delta",
                "Renaming, reformatting, or compression alone does not justify calling the artifact a substantively new architecture.",
            )

    if stage == "plain_language_brief" and contract.get("length_mode") == "one_sentence":
        if contract.get("planned_sentence_count") != 1:
            issue(
                "one_sentence_contract_not_respected",
                "A one-sentence brief must be planned and verified as exactly one sentence.",
            )

    if plan.get("data_or_benchmark_claims") is True:
        readiness = plan.get("data_readiness")
        if not isinstance(readiness, dict):
            issue(
                "data_readiness_missing",
                "Dataset or benchmark claims require a data-readiness record.",
                severity="block",
            )
        else:
            missing = sorted(field for field in DATA_READINESS_FIELDS if not nonempty(readiness.get(field)))
            if missing:
                issue(
                    "data_readiness_incomplete",
                    "Dataset or benchmark claims are missing: " + ", ".join(missing),
                    severity="block" if stage in COMPLETE_STAGES else "revise",
                )
            if readiness.get("standard_status") == "author_proposal" and readiness.get("described_as") in {
                "community_standard",
                "established_benchmark",
            }:
                issue(
                    "author_proposal_misrepresented_as_standard",
                    "An author proposal cannot be described as an established community standard or benchmark.",
                    severity="block",
                )

    coverage = plan.get("literature_coverage_claim")
    if coverage:
        if not isinstance(coverage, dict):
            issue("literature_coverage_claim_must_be_object", "Literature coverage claim must be an object.")
        elif coverage.get("status") == "verified_complete":
            missing: list[str] = []
            search_sources = coverage.get("search_sources")
            if not string_list(search_sources) or not search_sources:
                missing.append("search_sources[]")
            elif any(not meaningful_text(item) for item in search_sources):
                missing.append("search_sources[]:specific_databases_or_corpora")
            selection = coverage.get("search_or_selection_logic")
            if not isinstance(selection, dict):
                missing.append("search_or_selection_logic{}")
            else:
                cutoff = selection.get("cutoff_date")
                if not nonempty_string(cutoff) or re.fullmatch(
                    r"\d{4}-\d{2}-\d{2}", cutoff
                ) is None:
                    missing.append("search_or_selection_logic.cutoff_date")
                if not string_list(selection.get("queries_or_selection_rules")) or not selection.get(
                    "queries_or_selection_rules"
                ):
                    missing.append("search_or_selection_logic.queries_or_selection_rules[]")
                elif any(
                    not meaningful_text(item)
                    for item in selection.get("queries_or_selection_rules", [])
                ):
                    missing.append(
                        "search_or_selection_logic.queries_or_selection_rules[]:non_placeholder"
                    )
                if not string_list(selection.get("article_type_rules")) or not selection.get(
                    "article_type_rules"
                ):
                    missing.append("search_or_selection_logic.article_type_rules[]")
                elif any(
                    not meaningful_text(item) for item in selection.get("article_type_rules", [])
                ):
                    missing.append("search_or_selection_logic.article_type_rules[]:non_placeholder")
            deduplication = coverage.get("deduplication")
            if not isinstance(deduplication, dict):
                missing.append("deduplication{}")
            else:
                if not string_list(deduplication.get("keys")) or not deduplication.get("keys"):
                    missing.append("deduplication.keys[]")
                elif any(not meaningful_text(item) for item in deduplication.get("keys", [])):
                    missing.append("deduplication.keys[]:non_placeholder")
                if not nonempty_string(deduplication.get("process")):
                    missing.append("deduplication.process")
                elif not meaningful_text(deduplication.get("process")):
                    missing.append("deduplication.process:non_placeholder")
            if not meaningful_text(coverage.get("version_handling")):
                missing.append("version_handling")
            record_audit = coverage.get("record_audit")
            if not isinstance(record_audit, dict):
                missing.append("record_audit{}")
            else:
                if not isinstance(record_audit.get("record_count"), int) or record_audit.get(
                    "record_count", 0
                ) <= 0:
                    missing.append("record_audit.record_count")
                if not meaningful_text(record_audit.get("manifest_locator")):
                    missing.append("record_audit.manifest_locator")
            if missing:
                issue(
                    "unsupported_complete_literature_claim",
                    "A verified-complete literature claim lacks: " + ", ".join(missing),
                    severity="block",
                )
            unverified = sorted(
                record["id"]
                for record in evidence.values()
                if record.get("verification_status") in {"metadata_only", "candidate", "pending"}
            )
            if unverified:
                issue(
                    "complete_literature_claim_contains_unverified_records",
                    "A verified-complete literature claim still contains unverified records: "
                    + ", ".join(unverified),
                    severity="block",
                )

    if plan.get("completion_status") == "completed":
        checks = plan.get("delivery_checks")
        if not isinstance(checks, dict):
            issue(
                "completion_without_delivery_checks",
                "Do not announce completion without the corresponding file, budget, editability, and render checks.",
                severity="block",
            )
        else:
            required_checks = ["artifact_exists", "budget_verified"]
            if contract.get("editable") is True:
                required_checks.append("editable_source_verified")
            if contract.get("format", "").casefold() in {"docx", "pdf", "pptx"}:
                required_checks.append("rendered_and_inspected")
            failed = [field for field in required_checks if checks.get(field) is not True]
            if failed:
                issue(
                    "completion_checks_failed",
                    "Completion was claimed before these checks passed: " + ", ".join(failed),
                    severity="block",
                )

    status = "ready"
    if any(item["severity"] == "block" for item in issues):
        status = "blocked"
    elif any(item["severity"] == "revise" for item in issues):
        status = "revise"

    return {
        "status": status,
        "route": stage,
        "verification_scope": "declared_plan_only",
        "errors": [],
        "issue_counts": {
            "block": sum(item["severity"] == "block" for item in issues),
            "revise": sum(item["severity"] == "revise" for item in issues),
        },
        "issues": issues,
        "handoff": [
            "Keep decision provenance, evidence states, unresolved questions, and internal labels outside the reader-visible manuscript.",
            "Use the genre-specific writing and visual workflow after this plan is ready.",
            "Independently verify source truth, literature coverage, and the rendered artifact; this audit checks declarations and relationships, not those external facts.",
            "Verify the final artifact against its format and length contract before announcing completion.",
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="JSON manuscript development plan")
    parser.add_argument("--json", type=Path, help="Write the audit result as JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.json and args.json.resolve() == args.plan.resolve():
        print("Plan audit failed: --json cannot overwrite the input plan", file=sys.stderr)
        return 3
    try:
        payload = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Unable to read plan: {exc}", file=sys.stderr)
        return 3
    result = audit(payload)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json:
        try:
            args.json.write_text(rendered + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"Unable to write audit: {exc}", file=sys.stderr)
            return 3
    print(rendered)
    if result["status"] == "ready":
        return 0
    if result["status"] == "revise":
        return 2
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
