from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("figure_brief", ROOT / "scripts" / "figure_brief.py")
figure_brief = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(figure_brief)


def scene_display() -> dict:
    return {
        "id": "Figure 1",
        "role": "overview",
        "placement": "main",
        "reader_question": "How does a biomaterial move from formulation to a bounded decision?",
        "supported_claim": "The path connects a material, experiment, readout, decision, and explicit limit.",
        "evidence_sources": ["manuscript scope"],
        "biomedical_scene": True,
        "visual_form": "object_based_scene",
        "scene_grammar": {
            "scientific_object": "hydrogel formulation",
            "experimental_action": "fabricate and expose cells",
            "measurement_or_test": "adhesion and viability assays",
            "decision_or_feedback": "select or reject the formulation",
            "evidence_boundary": "no external laboratory or in vivo transfer",
        },
        "icons": ["hydrogel", "well_plate"],
        "icon_semantics": {
            "hydrogel": "material under design",
            "well_plate": "in vitro viability assay",
        },
        "copy_brand_assets": False,
        "imitate_visual_identity": False,
        "third_party_visual_components": [],
    }


def synthesis_display() -> dict:
    return {
        "id": "Figure 2",
        "role": "evidence_synthesis",
        "placement": "main",
        "reader_question": "What changes when studies are compared on common dimensions?",
        "supported_claim": "Decision role, testing context, and transfer are independent dimensions.",
        "cross_study": True,
        "evidence_sources": ["Study A", "Study B"],
        "comparison_dimensions": ["decision role", "testing context", "generalization boundary"],
        "visual_form": "evidence_landscape",
        "icons": [],
        "icon_semantics": {},
        "copy_brand_assets": False,
        "imitate_visual_identity": False,
        "third_party_visual_components": [],
    }


def valid_plan() -> dict:
    return {
        "schema_version": "1.0",
        "plan_type": "review_visual_plan",
        "article_type": "structured_narrative_review",
        "target_venue": "exact venue pending",
        "display_count_basis": "narrative_roles_and_verified_venue_rules",
        "argument_depends_on_cross_study_comparison": True,
        "displays": [scene_display(), synthesis_display()],
    }


def issue_codes(result: dict) -> set[str]:
    return {item["code"] for item in result.get("issues", [])}


class ReviewBiomedicalVisualPlanTests(unittest.TestCase):
    def test_single_figure_prompt_carries_object_based_scene_contract(self):
        spec = {
            "id": "Figure 1",
            "language": "English",
            "figure_type": "review_schematic",
            "reader_question": "How does the experiment produce a bounded decision?",
            "supported_claim": "A measured result changes a declared material-selection decision.",
            "evidence_sources": ["manuscript Sections 2 and 5"],
            "prohibited_content": ["No clinical promise."],
            "target_venue": "exact venue pending",
            "width_mm": 183,
            "height_mm": 70,
            "layout": "object-based experimental scene",
            "review_role": "workflow",
            "biomedical_scene": True,
            "scene_grammar": scene_display()["scene_grammar"],
        }
        result = figure_brief.route(spec)
        self.assertEqual(result["status"], "ready")
        self.assertIn("Object-based biomedical scene grammar", result["prompt"])
        self.assertIn("do not use a static card or box stack", result["prompt"])

    def test_complete_object_based_plan_passes(self):
        result = figure_brief.audit_review_visual_plan(valid_plan())
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["genuine_cross_study_synthesis_ids"], ["Figure 2"])
        self.assertEqual(result["issues"], [])

    def test_second_workflow_cannot_substitute_for_evidence_synthesis(self):
        plan = valid_plan()
        first = scene_display()
        first["role"] = "workflow"
        second = copy.deepcopy(first)
        second["id"] = "Figure 2"
        plan["displays"] = [first, second]
        result = figure_brief.audit_review_visual_plan(plan)
        self.assertEqual(result["status"], "revise")
        self.assertTrue(
            {
                "missing_genuine_cross_study_evidence_synthesis",
                "additional_workflow_does_not_replace_evidence_synthesis",
            }.issubset(issue_codes(result))
        )

    def test_graphical_abstract_does_not_count_as_evidence_synthesis(self):
        plan = valid_plan()
        abstract = synthesis_display()
        abstract["role"] = "graphical_abstract"
        plan["displays"] = [scene_display(), abstract]
        result = figure_brief.audit_review_visual_plan(plan)
        self.assertIn("missing_genuine_cross_study_evidence_synthesis", issue_codes(result))

    def test_evidence_synthesis_requires_traceable_studies_and_dimensions(self):
        plan = valid_plan()
        plan["displays"][1]["evidence_sources"] = ["Study A"]
        plan["displays"][1]["comparison_dimensions"] = []
        result = figure_brief.audit_review_visual_plan(plan)
        self.assertIn("evidence_synthesis_not_genuine", issue_codes(result))

    def test_incomplete_biomedical_scene_is_actionable(self):
        plan = valid_plan()
        del plan["displays"][0]["scene_grammar"]["measurement_or_test"]
        result = figure_brief.audit_review_visual_plan(plan)
        self.assertIn("biomedical_scene_grammar_incomplete", issue_codes(result))

    def test_static_card_stack_is_rejected_for_biomedical_scene(self):
        plan = valid_plan()
        plan["displays"][0]["visual_form"] = "box_stack"
        result = figure_brief.audit_review_visual_plan(plan)
        self.assertIn("static_card_or_box_stack", issue_codes(result))

    def test_icons_must_have_scientific_semantics(self):
        plan = valid_plan()
        plan["displays"][0]["icons"].append("sparkle")
        result = figure_brief.audit_review_visual_plan(plan)
        self.assertIn("decorative_icons_without_scientific_semantics", issue_codes(result))

    def test_brand_assets_and_visual_identity_are_not_copyable_shortcuts(self):
        plan = valid_plan()
        plan["displays"][0]["copy_brand_assets"] = True
        result = figure_brief.audit_review_visual_plan(plan)
        self.assertIn("proprietary_asset_or_visual_identity_copy", issue_codes(result))

    def test_third_party_components_need_provenance_and_redistribution_status(self):
        plan = valid_plan()
        plan["displays"][0]["third_party_visual_components"] = [
            {"name": "licensed icon", "source": "provider page"}
        ]
        result = figure_brief.audit_review_visual_plan(plan)
        self.assertIn("third_party_visual_provenance_incomplete", issue_codes(result))

    def test_six_figures_plus_one_table_is_not_a_required_count(self):
        small = valid_plan()
        large = valid_plan()
        for number in range(3, 7):
            item = scene_display()
            item["id"] = f"Figure {number}"
            item["role"] = "roadmap" if number == 6 else "framework"
            large["displays"].append(item)
        table = {
            "id": "Table 1",
            "role": "table",
            "placement": "main",
            "reader_question": "Which exact fields support lookup?",
            "supported_claim": "The table preserves exact study attributes.",
        }
        large["displays"].append(table)
        self.assertEqual(figure_brief.audit_review_visual_plan(small)["status"], "pass")
        self.assertEqual(figure_brief.audit_review_visual_plan(large)["status"], "pass")

    def test_fixed_count_quota_is_rejected_as_a_design_basis(self):
        plan = valid_plan()
        plan["display_count_basis"] = "fixed_quota"
        result = figure_brief.audit_review_visual_plan(plan)
        self.assertEqual(result["status"], "invalid")
        self.assertIn(
            "display_count_basis_must_use_roles_and_or_verified_venue_rules",
            result["errors"],
        )

    def test_cli_audits_review_plan_and_uses_nonzero_exit_for_revision(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "plan.json"
            output = Path(temp_dir) / "audit.json"
            plan = valid_plan()
            plan["displays"] = [scene_display()]
            source.write_text(json.dumps(plan), encoding="utf-8")
            self.assertEqual(
                figure_brief.main([str(source), "--json", str(output)]),
                2,
            )
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["status"], "revise")


if __name__ == "__main__":
    unittest.main()
