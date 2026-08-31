from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "manuscript_plan.py"
ASSET = ROOT / "assets" / "manuscript_development_plan.json"

SPEC = importlib.util.spec_from_file_location("manuscript_plan", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def valid_plan() -> dict:
    return json.loads(ASSET.read_text(encoding="utf-8"))


def issue_codes(result: dict) -> set[str]:
    return {item["code"] for item in result.get("issues", [])}


class ManuscriptPlanTests(unittest.TestCase):
    def test_public_asset_is_ready(self) -> None:
        result = MODULE.audit(valid_plan())
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["issues"], [])

    def test_non_object_root_is_invalid(self) -> None:
        result = MODULE.audit([])
        self.assertEqual(result["status"], "invalid")
        self.assertIn("root_must_be_object", result["errors"])
        malformed = valid_plan()
        malformed["artifact_stage"] = []
        self.assertEqual(MODULE.audit(malformed)["status"], "invalid")
        malformed = valid_plan()
        malformed["continuity"]["active_decision_ids"] = {"D1": True}
        self.assertEqual(MODULE.audit(malformed)["status"], "invalid")
        malformed = valid_plan()
        malformed["claims"][0]["evidence_ids"] = {"E1": True}
        self.assertEqual(MODULE.audit(malformed)["status"], "invalid")

    def test_unknown_stage_is_invalid(self) -> None:
        plan = valid_plan()
        plan["artifact_stage"] = "magic_paper"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any(error.startswith("unsupported_artifact_stage") for error in result["errors"]))
        plan = valid_plan()
        del plan["artifact_contract"]["editable"]
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("artifact_contract_missing_or_empty:editable", result["errors"])

    def test_topic_only_cannot_support_first_draft(self) -> None:
        plan = valid_plan()
        plan["artifact_stage"] = "author_first_draft"
        plan["source_sufficiency"] = "topic_only"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("topic_only_cannot_support_draft", issue_codes(result))
        self.assertIn("draft_started_before_author_approval", issue_codes(result))

    def test_topic_only_can_support_provisional_outline(self) -> None:
        plan = valid_plan()
        plan["source_sufficiency"] = "topic_only"
        plan["claims"][0]["status"] = "provisional"
        plan["claims"][0]["evidence_ids"] = []
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "ready")

    def test_format_reference_cannot_establish_meeting_decision(self) -> None:
        plan = valid_plan()
        plan["decision_provenance"][0]["source_id"] = "S2"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("decision_authority_mismatch", issue_codes(result))

    def test_format_reference_cannot_support_claim(self) -> None:
        plan = valid_plan()
        plan["evidence_records"][0]["source_id"] = "S2"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("noncontent_source_used_as_evidence", issue_codes(result))
        plan = valid_plan()
        plan["evidence_records"][0]["exact_support"] = "several recent studies"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("vague_evidence_placeholder", issue_codes(result))
        plan = valid_plan()
        plan["evidence_records"][0]["support_locator"] = "abstract"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("vague_evidence_placeholder", issue_codes(result))
        plan = valid_plan()
        plan["evidence_records"][0]["source_id"] = "S404"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("orphan_evidence_source", issue_codes(result))

    def test_superseded_decision_cannot_be_active(self) -> None:
        plan = valid_plan()
        plan["continuity"]["active_decision_ids"] = ["D1", "D2"]
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("active_and_superseded_decision_conflict", issue_codes(result))
        self.assertIn("superseded_decision_reactivated", issue_codes(result))
        plan = valid_plan()
        plan["decision_provenance"][0]["status"] = "assistant_proposal"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "revise")
        self.assertIn("unapproved_decision_controls_architecture", issue_codes(result))
        plan = valid_plan()
        plan["artifact_stage"] = "author_first_draft"
        plan["source_sufficiency"] = "approved_outline_and_evidence"
        plan["artifact_contract"]["approval_state"] = "author_approved"
        plan["artifact_contract"]["approval_source_id"] = "S1"
        plan["continuity"]["project_record_read"] = False
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("project_continuity_not_read", issue_codes(result))

    def test_competing_primary_axes_require_revision(self) -> None:
        plan = valid_plan()
        plan["positioning_lock"]["competing_primary_axes"] = ["material class", "model class"]
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "revise")
        self.assertIn("competing_primary_axes", issue_codes(result))
        plan = valid_plan()
        plan["genre"] = "original_research"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("genre_positioning_mismatch", issue_codes(result))
        plan = valid_plan()
        plan["genre"] = "original_research"
        plan["positioning_lock"]["article_family"] = "original_research"
        plan["genre_contract"] = {
            "inference_chain": "question to design to result to bounded conclusion",
            "alternative_explanations": ["batch and measurement effects"],
            "result_figure_map": {"C1": "F1"},
        }
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("genre_lock_route_mismatch", issue_codes(result))

    def test_supported_claim_requires_evidence(self) -> None:
        plan = valid_plan()
        plan["claims"][0]["evidence_ids"] = []
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("supported_claim_has_no_evidence", issue_codes(result))
        plan = valid_plan()
        plan["artifact_stage"] = "full_draft"
        plan["source_sufficiency"] = "complete_source_package"
        plan["artifact_contract"]["approval_state"] = "author_approved"
        plan["artifact_contract"]["approval_source_id"] = "S1"
        plan["claims"] = []
        plan["evidence_records"] = []
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("draft_has_no_claim_map", issue_codes(result))
        self.assertIn("draft_has_no_evidence_map", issue_codes(result))

    def test_metadata_only_does_not_establish_complete_draft_claim(self) -> None:
        plan = valid_plan()
        plan["artifact_stage"] = "full_draft"
        plan["source_sufficiency"] = "approved_outline_and_evidence"
        plan["evidence_records"][0]["verification_status"] = "metadata_only"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("claim_outruns_evidence_state", issue_codes(result))
        plan = valid_plan()
        plan["evidence_records"][0]["metadata_status"] = "pending"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("verified_summary_outruns_evidence_states", issue_codes(result))
        plan = valid_plan()
        plan["claims"][0]["claim_type"] = "mechanism"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("claim_type_not_supported_by_evidence_record", issue_codes(result))

    def test_provisional_claim_blocks_complete_draft(self) -> None:
        plan = valid_plan()
        plan["artifact_stage"] = "full_draft"
        plan["source_sufficiency"] = "approved_outline_and_evidence"
        plan["claims"][0]["status"] = "provisional"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("incomplete_claim_in_complete_draft", issue_codes(result))
        plan = valid_plan()
        plan["artifact_stage"] = "full_draft"
        plan["source_sufficiency"] = "complete_source_package"
        plan["artifact_contract"]["approval_state"] = "author_approved"
        plan["artifact_contract"]["approval_source_id"] = "S1"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "ready")

    def test_internal_scaffolding_stays_out_of_reader_copy(self) -> None:
        plan = valid_plan()
        plan["reader_visible_internal_labels"] = ["中心判断", "E1–E5", "author TODO"]
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "revise")
        self.assertIn("internal_scaffolding_exposed", issue_codes(result))

    def test_unresolved_author_question_stays_backstage(self) -> None:
        plan = valid_plan()
        plan["unresolved_items"][0]["reader_visible"] = True
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "revise")
        self.assertIn("unresolved_item_exposed_to_reader", issue_codes(result))

    def test_renaming_alone_is_not_new_architecture(self) -> None:
        plan = valid_plan()
        plan["architecture_delta"] = {}
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "revise")
        self.assertIn("no_substantive_architecture_delta", issue_codes(result))
        plan = valid_plan()
        plan["display_plan"] = []
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "revise")
        self.assertIn("display_plan_missing", issue_codes(result))
        plan = valid_plan()
        del plan["genre_contract"]
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "revise")
        self.assertIn("genre_contract_incomplete", issue_codes(result))

    def test_unapproved_title_drift_is_blocked(self) -> None:
        plan = valid_plan()
        plan["title_lock"]["status"] = "unchanged"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("unapproved_title_drift", issue_codes(result))
        plan = valid_plan()
        plan["artifact_stage"] = "submission_copy"
        plan["artifact_contract"]["approval_state"] = "author_approved"
        plan["title_lock"]["status"] = "proposal"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("proposed_title_in_submission_copy", issue_codes(result))
        plan["genre_lock"] = {
            "source_genre": "narrative_review",
            "working_genre": "perspective",
            "status": "proposal",
        }
        result = MODULE.audit(plan)
        self.assertIn("unapproved_genre_change_in_draft", issue_codes(result))

    def test_one_sentence_brief_honours_exact_length_contract(self) -> None:
        plan = valid_plan()
        plan["artifact_stage"] = "plain_language_brief"
        plan["artifact_contract"]["length_mode"] = "one_sentence"
        plan["artifact_contract"]["planned_sentence_count"] = 3
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "revise")
        self.assertIn("one_sentence_contract_not_respected", issue_codes(result))
        plan = valid_plan()
        plan["artifact_stage"] = "plain_language_brief"
        plan["claims"] = []
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("brief_has_no_scientific_claim", issue_codes(result))

    def test_data_claim_requires_full_readiness_record(self) -> None:
        plan = valid_plan()
        plan["data_or_benchmark_claims"] = True
        plan["data_readiness"] = {"independent_unit": "one synthesis batch"}
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "revise")
        self.assertIn("data_readiness_incomplete", issue_codes(result))

    def test_author_proposal_cannot_be_called_established_benchmark(self) -> None:
        plan = valid_plan()
        plan["data_or_benchmark_claims"] = True
        plan["data_readiness"] = {
            "independent_unit": "one synthesis batch",
            "material_or_population_identity": "composition and identity record",
            "process_batch_or_site": "lab, batch, and protocol",
            "measurement_and_timepoint": "assay and time point",
            "missingness_failures_and_negatives": "retained",
            "provenance_and_version": "source and version recorded",
            "split_or_feedback_eligibility": "group-aware split and feedback flag",
            "standard_status": "author_proposal",
            "described_as": "established_benchmark",
        }
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("author_proposal_misrepresented_as_standard", issue_codes(result))

    def test_complete_literature_claim_requires_audit_trail(self) -> None:
        plan = valid_plan()
        plan["literature_coverage_claim"] = {"status": "verified_complete", "search_sources": ["PubMed"]}
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("unsupported_complete_literature_claim", issue_codes(result))
        plan["literature_coverage_claim"] = {
            "status": "verified_complete",
            "search_sources": ["Google"],
            "search_or_selection_logic": {
                "cutoff_date": "2026-08-31",
                "queries_or_selection_rules": ["done"],
                "article_type_rules": ["yes"],
            },
            "deduplication": {"keys": ["yes"], "process": "done"},
            "version_handling": "yes",
            "record_audit": {"record_count": 1, "manifest_locator": "done"},
        }
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("unsupported_complete_literature_claim", issue_codes(result))
        plan["literature_coverage_claim"] = {
            "status": "verified_complete",
            "search_sources": ["PubMed"],
            "search_or_selection_logic": {
                "cutoff_date": "2026-08-31",
                "queries_or_selection_rules": ["recorded query Q1"],
                "article_type_rules": ["primary studies only for experimental-effect claims"],
            },
            "deduplication": {
                "keys": ["DOI", "normalized title"],
                "process": "retain a single version-linked record",
            },
            "version_handling": "preprint and journal linked",
            "record_audit": {
                "record_count": 1,
                "manifest_locator": "evidence manifest revision 1",
            },
        }
        plan["evidence_records"][0]["verification_status"] = "candidate"
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("complete_literature_claim_contains_unverified_records", issue_codes(result))
        plan = valid_plan()
        plan["artifact_stage"] = "evidence_matrix"
        plan["evidence_records"] = []
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("empty_evidence_matrix", issue_codes(result))

    def test_completion_claim_requires_render_checks_for_docx(self) -> None:
        plan = valid_plan()
        plan["completion_status"] = "completed"
        plan["delivery_checks"] = {"artifact_exists": True, "budget_verified": True}
        result = MODULE.audit(plan)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("completion_checks_failed", issue_codes(result))

    def test_cli_exit_codes_and_json_output(self) -> None:
        ready_plan = valid_plan()
        blocked_plan = copy.deepcopy(ready_plan)
        blocked_plan["artifact_stage"] = "author_first_draft"
        blocked_plan["source_sufficiency"] = "topic_only"
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            ready_path = directory / "ready.json"
            blocked_path = directory / "blocked.json"
            report_path = directory / "report.json"
            ready_path.write_text(json.dumps(ready_plan), encoding="utf-8")
            blocked_path.write_text(json.dumps(blocked_plan), encoding="utf-8")
            ready = subprocess.run(
                [sys.executable, str(SCRIPT), str(ready_path), "--json", str(report_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            blocked = subprocess.run(
                [sys.executable, str(SCRIPT), str(blocked_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            overwrite = subprocess.run(
                [sys.executable, str(SCRIPT), str(ready_path), "--json", str(ready_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(ready.returncode, 0)
            self.assertEqual(blocked.returncode, 3)
            self.assertEqual(overwrite.returncode, 3)
            self.assertIn("cannot overwrite", overwrite.stderr)
            self.assertEqual(json.loads(report_path.read_text(encoding="utf-8"))["status"], "ready")


if __name__ == "__main__":
    unittest.main()
