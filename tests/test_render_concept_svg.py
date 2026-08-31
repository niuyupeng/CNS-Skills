from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "render_concept_svg", ROOT / "scripts" / "render_concept_svg.py"
)
renderer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(renderer)


def palette() -> dict:
    return {
        "ink": "#162B3A",
        "muted": "#52616B",
        "rule": "#CBD5DC",
        "background": "#FFFFFF",
        "accent": "#176B87",
    }


def flow_spec() -> dict:
    return {
        "id": "Figure 1",
        "title": "Decision pathway",
        "description": "Five stages from a materials problem to validation.",
        "language": "English",
        "layout": "flow",
        "width_px": 2400,
        "height_px": 800,
        "width_mm": 183,
        "height_mm": 61,
        "palette": palette(),
        "nodes": [
            {"id": "problem", "title_lines": ["Problem"], "body_lines": ["Decision to change"]},
            {"id": "data", "title_lines": ["Data"], "body_lines": ["Independent unit"]},
            {"id": "model", "title_lines": ["Model"], "body_lines": ["Candidate family"]},
        ],
        "footer_lines": ["Validation limits the claim."],
    }


def axes_spec() -> dict:
    spec = flow_spec()
    spec["id"] = "Figure 2"
    spec["layout"] = "independent_axes"
    spec.pop("nodes")
    spec["rows"] = [
        {
            "id": "decision",
            "panel": "a",
            "label_lines": ["Decision mode"],
            "directional": True,
            "items": [
                {"title_lines": ["Retrospective"], "subtitle_lines": ["No new choice"]},
                {"title_lines": ["Closed loop"], "subtitle_lines": ["System next round"]},
            ],
        },
        {
            "id": "testing",
            "panel": "b",
            "label_lines": ["Testing context"],
            "items": [
                {"title_lines": ["Acellular"], "subtitle_lines": ["No living cells"]},
                {"title_lines": ["In vivo"], "subtitle_lines": ["Animal endpoint"]},
            ],
        },
    ]
    return spec


class ConceptSVGTests(unittest.TestCase):
    def test_flow_svg_has_metadata_and_real_text(self):
        root = renderer.render(flow_spec())
        payload = renderer.serialize(root).decode("utf-8")
        self.assertIn("<title", payload)
        self.assertIn("Decision pathway", payload)
        self.assertIn("<text", payload)
        self.assertNotIn("<image", payload)
        self.assertNotIn("<script", payload)

    def test_axes_svg_contains_separate_semantic_groups(self):
        root = renderer.render(axes_spec())
        axes = [node for node in root.iter() if node.get("data-axis-id")]
        self.assertEqual([node.get("data-axis-id") for node in axes], ["decision", "testing"])

    def test_only_explicitly_directional_axes_have_arrows(self):
        root = renderer.render(axes_spec())
        lines = [node for node in root.iter() if node.get("data-directional")]
        self.assertEqual([node.get("data-directional") for node in lines], ["true", "false"])
        self.assertIsNotNone(lines[0].get("marker-end"))
        self.assertIsNone(lines[1].get("marker-end"))

    def test_output_is_valid_xml(self):
        payload = renderer.serialize(renderer.render(flow_spec()))
        self.assertEqual(ET.fromstring(payload).tag, f"{{{renderer.SVG_NS}}}svg")

    def test_render_is_deterministic(self):
        first = renderer.serialize(renderer.render(flow_spec()))
        second = renderer.serialize(renderer.render(flow_spec()))
        self.assertEqual(first, second)

    def test_optional_feedback_is_semantically_marked(self):
        spec = flow_spec()
        spec["feedback"] = {"from": 3, "to": 2, "label_lines": ["only after a new round"]}
        payload = renderer.serialize(renderer.render(spec)).decode("utf-8")
        self.assertIn('data-role="conditional-feedback"', payload)

    def test_invalid_palette_is_rejected(self):
        spec = flow_spec()
        spec["palette"]["ink"] = "navy"
        self.assertIn("palette_invalid:ink", renderer.validate(spec))

    def test_unsupported_layout_is_rejected(self):
        spec = flow_spec()
        spec["layout"] = "poster"
        self.assertIn("unsupported_layout:poster", renderer.validate(spec))

    def test_flow_needs_three_nodes(self):
        spec = flow_spec()
        spec["nodes"] = spec["nodes"][:2]
        self.assertIn("flow_requires_at_least_three_nodes", renderer.validate(spec))

    def test_axes_need_two_rows(self):
        spec = axes_spec()
        spec["rows"] = spec["rows"][:1]
        self.assertIn("independent_axes_requires_at_least_two_rows", renderer.validate(spec))

    def test_cli_requires_svg_extension(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "spec.json"
            source.write_text(json.dumps(flow_spec()), encoding="utf-8")
            self.assertEqual(renderer.main([str(source), str(Path(temp_dir) / "out.png")]), 1)

    def test_cli_writes_svg(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "spec.json"
            output = Path(temp_dir) / "figure.svg"
            source.write_text(json.dumps(flow_spec()), encoding="utf-8")
            self.assertEqual(renderer.main([str(source), str(output)]), 0)
            self.assertTrue(output.read_bytes().startswith(b"<?xml"))


if __name__ == "__main__":
    unittest.main()
