from __future__ import annotations

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


def base_spec(figure_type: str = "conceptual_flow") -> dict:
    return {
        "id": "Figure 1",
        "language": "English",
        "figure_type": figure_type,
        "reader_question": "When does a model change an experiment?",
        "supported_claim": "A model guides design only when its output changes a declared experimental action.",
        "evidence_sources": ["manuscript Sections 3 and 11"],
        "prohibited_content": ["No clinical promise."],
        "target_venue": "broad-selective journal; exact venue pending",
        "width_mm": 183,
        "height_mm": 72,
        "layout": "five-stage flow",
        "panels": [{"id": "a", "job": "show the decision path"}],
    }


class FigureBriefTests(unittest.TestCase):
    def test_conceptual_flow_routes_to_editable_svg(self):
        result = figure_brief.route(base_spec())
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["route"], "editable_svg")
        self.assertIn("editable vector", result["prompt"])
        self.assertIn("Do not invent data", result["negative_constraints"][0])

    def test_quantitative_figure_requires_data_source(self):
        spec = base_spec("quantitative_plot")
        self.assertIn("quantitative_figure_requires_data_source", figure_brief.validate(spec))

    def test_quantitative_figure_routes_to_code_not_image_generation(self):
        spec = base_spec("quantitative_plot")
        spec["data_source"] = "data/results.csv"
        result = figure_brief.route(spec)
        self.assertEqual(result["route"], "code_from_data")
        self.assertEqual(result["prompt"], "")

    def test_experimental_image_generation_is_refused(self):
        result = figure_brief.route(base_spec("microscopy"))
        self.assertEqual(result["status"], "refused_generation")
        self.assertEqual(result["route"], "authentic_experimental_data_only")

    def test_conceptual_art_waits_for_policy_clearance(self):
        result = figure_brief.route(base_spec("graphical_abstract"))
        self.assertEqual(result["status"], "blocked_pending_policy")
        self.assertEqual(result["prompt"], "")

    def test_permitted_conceptual_art_gets_bounded_prompt(self):
        spec = base_spec("conceptual_art")
        spec["generative_art_permitted"] = True
        result = figure_brief.route(spec)
        self.assertEqual(result["route"], "conceptual_image_generation")
        self.assertIn("illustrative rather than observed data", result["prompt"])

    def test_unsupported_type_is_invalid(self):
        spec = base_spec("marketing_banner")
        result = figure_brief.route(spec)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("unsupported_figure_type:marketing_banner", result["errors"])

    def test_dimensions_must_be_positive(self):
        spec = base_spec()
        spec["width_mm"] = 0
        self.assertIn("invalid_positive_number:width_mm", figure_brief.validate(spec))

    def test_json_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "brief.json"
            path.write_text(json.dumps(base_spec()), encoding="utf-8")
            self.assertEqual(figure_brief.main([str(path), "--json", str(path)]), 1)

    def test_cli_writes_routed_brief(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "brief.json"
            output = Path(temp_dir) / "routed.json"
            source.write_text(json.dumps(base_spec()), encoding="utf-8")
            self.assertEqual(figure_brief.main([str(source), "--json", str(output)]), 0)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["route"], "editable_svg")


if __name__ == "__main__":
    unittest.main()
