from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import urllib.error
import zipfile
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cns_audit", ROOT / "scripts" / "cns_audit.py")
cns_audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(cns_audit)


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def write_docx_fixture(
    path: Path,
    body_xml: str,
    *,
    styles_xml: str | None = None,
    core_xml: str | None = None,
) -> None:
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<w:document xmlns:w="{W_NS}"><w:body>{body_xml}</w:body></w:document>'
    )
    if styles_xml is None:
        styles_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            f'<w:styles xmlns:w="{W_NS}"><w:docDefaults><w:rPrDefault><w:rPr>'
            '<w:sz w:val="20"/></w:rPr></w:rPrDefault></w:docDefaults></w:styles>'
        )
    if core_xml is None:
        core_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<cp:coreProperties '
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<dc:title>Scientific manuscript</dc:title>'
            '<dc:description>Research review.</dc:description>'
            '</cp:coreProperties>'
        )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document_xml.encode("utf-8"))
        archive.writestr("word/styles.xml", styles_xml.encode("utf-8"))
        archive.writestr("docProps/core.xml", core_xml.encode("utf-8"))


class CNSAuditTests(unittest.TestCase):
    def test_doi_cleanup_and_deduplication(self):
        text = "See doi:10.1000/ABC. Also https://doi.org/10.1000/abc."
        self.assertEqual(cns_audit.doi_list(text), ["10.1000/abc"])

    def test_stock_phrase_detection(self):
        report = cns_audit.build_report(Path("sample.txt"), "这说明结果重要。这说明仍需验证。")
        hit = next(item for item in report["stock_phrase_hits"] if item["pattern"] == "zh_this_shows")
        self.assertEqual(hit["count"], 2)

    def test_editorial_scaffolding_is_flagged_contextually(self):
        text = (
            "本文构建统一比较框架并形成三轴证据剖面。 "
            "We propose a decision-centered framework and an evidence chain."
        )
        report = cns_audit.build_report(Path("sample.txt"), text)
        labels = {item["pattern"] for item in report["editorial_scaffolding_candidates"]}
        self.assertIn("zh_evidence_scaffold", labels)
        self.assertIn("zh_generic_framework", labels)
        self.assertIn("en_evidence_scaffold", labels)
        self.assertIn("en_generic_framework", labels)

    def test_plain_evidence_card_is_flagged_as_scaffolding(self):
        report = cns_audit.build_report(Path("sample.txt"), "作者用证据卡记录每篇论文。")
        by_pattern = {
            item["pattern"]: item["count"]
            for item in report["editorial_scaffolding_candidates"]
        }
        self.assertEqual(by_pattern["zh_evidence_scaffold"], 1)

    def test_legitimate_dataset_and_named_framework_are_not_scaffolding(self):
        text = (
            "The dataset comprised 584 experimentally tested lipids. "
            "The DOME framework specifies data and model reporting requirements."
        )
        report = cns_audit.build_report(Path("sample.txt"), text)
        self.assertEqual(report["editorial_scaffolding_candidates"], [])

    def test_reader_visible_gate_flags_analysis_prompt_and_instruction(self):
        text = (
            "中心判断\n\n"
            "作者提示：请核对这里的引文。\n\n"
            "Agent instruction\n\n"
            "This paragraph reports the measured swelling ratio. [TODO: insert value]"
        )
        report = cns_audit.build_report(Path("sample.txt"), text)
        by_pattern = {
            item["pattern"]: item for item in report["reader_visible_output_candidates"]
        }
        self.assertIn("zh_analysis_label", by_pattern)
        self.assertIn("zh_author_prompt", by_pattern)
        self.assertIn("en_agent_prompt", by_pattern)
        self.assertIn("unresolved_placeholder", by_pattern)
        self.assertIn("reason", by_pattern["zh_analysis_label"])
        self.assertIn("action", by_pattern["zh_analysis_label"])

    def test_unfinished_author_work_is_not_mistaken_for_manuscript_prose(self):
        text = (
            "The current manuscript has not yet incorporated the final database export. "
            "Before submission, the search should be finalized and the references updated. "
            "Additional studies were added to fill specific argument gaps."
        )
        report = cns_audit.build_report(Path("sample.txt"), text)
        patterns = {item["pattern"] for item in report["reader_visible_output_candidates"]}
        self.assertIn("en_unfinished_submission_status", patterns)
        self.assertIn("argument_gap_development_workflow", patterns)
        self.assertEqual(report["clean_copy_gate"]["status"], "fail")

    def test_undefined_internal_shorthand_is_flagged(self):
        text = "E1—E5可以作为正文中的阅读简写，但这里没有解释各级含义。"
        report = cns_audit.build_report(Path("sample.txt"), text)
        patterns = {item["pattern"] for item in report["reader_visible_output_candidates"]}
        self.assertIn("zh_manuscript_process_meta", patterns)
        hit = next(
            item
            for item in report["reader_visible_output_candidates"]
            if item["pattern"] == "undefined_internal_code_scheme"
        )
        self.assertEqual(hit["details"][0]["codes"], ["E1", "E2", "E3", "E4", "E5"])
        self.assertEqual(hit["details"][0]["missing_definitions"], ["E1", "E2", "E3", "E4", "E5"])

    def test_fully_defined_project_classification_is_preserved(self):
        text = (
            "本综述采用C0—C4分级。\n\n"
            "C0，AI只分析已有数据；C1，AI推荐候选并由研究者验证；"
            "C2，实验结果反馈给模型以选择下一轮；"
            "C3，自动化平台执行由AI选择的实验；"
            "C4：体内终点反馈并改变下一轮自主选择。"
        )
        report = cns_audit.build_report(Path("sample.txt"), text)
        patterns = {item["pattern"] for item in report["reader_visible_output_candidates"]}
        self.assertNotIn("undefined_internal_code_scheme", patterns)

    def test_verb_phrase_definitions_for_project_codes_are_preserved(self):
        text = (
            "We use C0–C4 for AI involvement: C0 analyzes existing data; "
            "C1 makes a one-shot recommendation; C2 returns results for the next round; "
            "C3 lets AI select automated experiments; and C4 requires an in vivo endpoint "
            "to change the next autonomous round."
        )
        report = cns_audit.build_report(Path("sample.txt"), text)
        patterns = {item["pattern"] for item in report["reader_visible_output_candidates"]}
        self.assertNotIn("undefined_internal_code_scheme", patterns)

    def test_normal_headings_framework_and_public_figure_ranges_are_preserved(self):
        text = (
            "## Statistical analysis\n\n"
            "The DOME framework specifies data and model reporting requirements.\n\n"
            "Supplementary Figures S1–S5 report the ablation results.\n\n"
            "The TNM system describes tumor categories T1–T4.\n\n"
            "Add the reference standard to each calibration tube."
        )
        report = cns_audit.build_report(Path("sample.txt"), text)
        self.assertEqual(report["reader_visible_output_candidates"], [])

    def test_reference_list_is_excluded_from_prose_rhythm_by_default(self):
        text = (
            "The model was evaluated prospectively.\n\n"
            "References\n\n"
            "Nature Communications reference one. Nature Communications reference two. "
            "Nature Communications reference three. doi:10.1000/example"
        )
        report = cns_audit.build_report(Path("paper.txt"), text)
        self.assertTrue(report["analysis_scope"]["reference_section_excluded"])
        self.assertEqual(report["counts"]["analyzed_body_sentences"], 1)
        self.assertEqual(report["repeated_sentence_openers"], [])
        self.assertEqual(report["dois"], ["10.1000/example"])

    def test_repeated_unnumbered_shaded_callouts_fail_clean_copy_gate(self):
        callout = (
            '<w:tbl><w:tblPr><w:shd w:fill="F1F6FA"/></w:tblPr><w:tr><w:tc>'
            '<w:p><w:r><w:t>When to prioritize</w:t></w:r></w:p>'
            '<w:p><w:r><w:t>Use the model when the data support the decision.</w:t></w:r></w:p>'
            '</w:tc></w:tr></w:tbl>'
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper.docx"
            write_docx_fixture(path, callout * 3)
            report = cns_audit.build_report(path, cns_audit.read_docx(path))
        by_pattern = {item["pattern"]: item for item in report["docx_clean_copy_candidates"]}
        self.assertEqual(by_pattern["repeated_unnumbered_shaded_callouts"]["count"], 3)
        self.assertEqual(by_pattern["repeated_unnumbered_shaded_callouts"]["severity"], "defect")
        self.assertEqual(report["clean_copy_gate"]["status"], "fail")

    def test_strict_clean_copy_returns_diagnostic_exit_code(self):
        callout = (
            '<w:tbl><w:tblPr><w:shd w:fill="F1F6FA"/></w:tblPr><w:tr><w:tc>'
            '<w:p><w:r><w:t>Editorial cue</w:t></w:r></w:p>'
            '<w:p><w:r><w:t>Internal prose.</w:t></w:r></w:p>'
            '</w:tc></w:tr></w:tbl>'
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper.docx"
            write_docx_fixture(path, callout * 3)
            self.assertEqual(cns_audit.main([str(path), "--strict-clean-copy"]), 3)

    def test_numbered_boxes_and_key_points_are_not_callout_leakage(self):
        labels = ["Box 1", "Box 2", "Box 3", "Key Points"]
        body = "".join(
            '<w:tbl><w:tblPr><w:shd w:fill="E8F1F8"/></w:tblPr><w:tr><w:tc>'
            f'<w:p><w:r><w:t>{label}</w:t></w:r></w:p>'
            '<w:p><w:r><w:t>Venue-facing scientific content.</w:t></w:r></w:p>'
            '</w:tc></w:tr></w:tbl>'
            for label in labels
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper.docx"
            write_docx_fixture(path, body)
            report = cns_audit.build_report(path, cns_audit.read_docx(path))
        patterns = {item["pattern"] for item in report["docx_clean_copy_candidates"]}
        self.assertNotIn("repeated_unnumbered_shaded_callouts", patterns)
        self.assertNotIn("unnumbered_shaded_callout_candidate", patterns)
        self.assertEqual(report["clean_copy_gate"]["status"], "pass")

    def test_filename_and_core_property_production_traces_are_flagged(self):
        core_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<cp:coreProperties '
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<dc:creator>Author team</dc:creator>'
            '<cp:lastModifiedBy>CNS Skills</cp:lastModifiedBy>'
            '<dc:title>Scientific manuscript</dc:title>'
            '<dc:description>Generated by Codex, draft version V3.2.</dc:description>'
            '</cp:coreProperties>'
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper_CNS_V3.2_draft.docx"
            write_docx_fixture(path, '<w:p><w:r><w:t>Results</w:t></w:r></w:p>', core_xml=core_xml)
            report = cns_audit.build_report(path, cns_audit.read_docx(path))
        patterns = {item["pattern"] for item in report["docx_clean_copy_candidates"]}
        self.assertIn("filename_tool_identity_trace", patterns)
        self.assertIn("filename_production_trace", patterns)
        self.assertIn("core_property_tool_identity_trace", patterns)
        self.assertIn("core_property_production_trace", patterns)
        self.assertEqual(report["clean_copy_gate"]["status"], "fail")

    def test_scientific_tool_name_in_title_is_not_automatically_a_production_trace(self):
        core_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<cp:coreProperties '
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<dc:creator>Researcher</dc:creator>'
            '<cp:lastModifiedBy>Researcher</cp:lastModifiedBy>'
            '<dc:title>ChatGPT in scientific peer review</dc:title>'
            '<dc:description>A study of ChatGPT use by reviewers.</dc:description>'
            '</cp:coreProperties>'
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ChatGPT_in_scientific_peer_review.docx"
            write_docx_fixture(path, '<w:p><w:r><w:t>Results</w:t></w:r></w:p>', core_xml=core_xml)
            report = cns_audit.build_report(path, cns_audit.read_docx(path))
        patterns = {item["pattern"] for item in report["docx_clean_copy_candidates"]}
        self.assertNotIn("filename_tool_identity_trace", patterns)
        self.assertNotIn("core_property_tool_identity_trace", patterns)

    def test_heading_style_caption_and_within_table_size_drift_are_flagged(self):
        styles_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            f'<w:styles xmlns:w="{W_NS}"><w:docDefaults><w:rPrDefault><w:rPr>'
            '<w:sz w:val="20"/></w:rPr></w:rPrDefault></w:docDefaults>'
            '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="Heading 2"/></w:style>'
            '<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/></w:style>'
            '</w:styles>'
        )
        body = (
            '<w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
            '<w:r><w:t>Table 1 Model comparison</w:t></w:r></w:p>'
            '<w:tbl><w:tr><w:tc><w:p>'
            '<w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:t>Most body text uses eight points.</w:t></w:r>'
            '<w:r><w:rPr><w:sz w:val="24"/></w:rPr><w:t>drift</w:t></w:r>'
            '</w:p></w:tc></w:tr></w:tbl>'
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper.docx"
            write_docx_fixture(path, body, styles_xml=styles_xml)
            report = cns_audit.build_report(path, cns_audit.read_docx(path))
        patterns = {item["pattern"] for item in report["docx_clean_copy_candidates"]}
        self.assertIn("table_caption_uses_heading_style", patterns)
        self.assertIn("within_table_font_size_drift", patterns)

    def test_clean_docx_structure_has_zero_clean_copy_candidates(self):
        styles_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            f'<w:styles xmlns:w="{W_NS}"><w:docDefaults><w:rPrDefault><w:rPr>'
            '<w:sz w:val="20"/></w:rPr></w:rPrDefault></w:docDefaults>'
            '<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/></w:style>'
            '</w:styles>'
        )
        body = (
            '<w:p><w:pPr><w:pStyle w:val="Caption"/></w:pPr>'
            '<w:r><w:t>Table 1 Model comparison</w:t></w:r></w:p>'
            '<w:tbl><w:tr><w:tc><w:p>'
            '<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Header</w:t></w:r>'
            '</w:p></w:tc></w:tr><w:tr><w:tc><w:p>'
            '<w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:t>Uniform table text.</w:t></w:r>'
            '</w:p></w:tc></w:tr></w:tbl>'
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "manuscript.docx"
            write_docx_fixture(path, body, styles_xml=styles_xml)
            report = cns_audit.build_report(path, cns_audit.read_docx(path))
        self.assertEqual(report["docx_clean_copy_candidates"], [])
        self.assertEqual(report["clean_copy_gate"]["status"], "pass")

    def test_partially_defined_internal_scheme_reports_only_missing_codes(self):
        text = (
            "We use Q0–Q2 as an internal coding scheme.\n\n"
            "Q0: no prospective validation.\n\n"
            "Q1: prospective validation without deployment."
        )
        report = cns_audit.build_report(Path("sample.txt"), text)
        hit = next(
            item
            for item in report["reader_visible_output_candidates"]
            if item["pattern"] == "undefined_internal_code_scheme"
        )
        self.assertEqual(hit["details"][0]["missing_definitions"], ["Q2"])

    def test_numeric_claim_with_bracket_citation_is_not_flagged(self):
        sentences = ["准确率为92%[12]。", "准确率为91%。"]
        flagged = cns_audit.numeric_claims_without_citation(sentences)
        self.assertEqual(flagged, ["准确率为91%。"])

    def test_docx_reader(self):
        xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
          <w:body><w:p><w:r><w:t>Hello CNS</w:t></w:r></w:p></w:body>
        </w:document>'''
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.docx"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("word/document.xml", xml)
            self.assertEqual(cns_audit.read_docx(path), "Hello CNS")

    def test_docx_reader_includes_office_math_text(self):
        xml = b'''<?xml version="1.0" encoding="UTF-8"?>
        <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
          xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
          <w:body><w:p><w:r><w:t>Equation: </w:t></w:r><m:oMath><m:r><m:t>5</m:t></m:r></m:oMath></w:p></w:body>
        </w:document>'''
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "math.docx"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("word/document.xml", xml)
            self.assertEqual(cns_audit.read_docx(path), "Equation: 5")

    def test_json_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper.txt"
            path.write_text("Original manuscript", encoding="utf-8")
            self.assertEqual(cns_audit.main([str(path), "--json", str(path)]), 1)
            self.assertEqual(path.read_text(encoding="utf-8"), "Original manuscript")

    def test_shareable_report_removes_path_and_excerpts(self):
        report = cns_audit.build_report(
            Path("private/paper.txt"), "Accuracy increased to 92% without a citation."
        )
        report["repeated_sentence_openers"] = [
            {"opener": "secret start", "count": 3, "examples": ["secret excerpt"]}
        ]
        report["repeated_fragments"] = [{"fragment": "secret fragment", "count": 3}]
        report["editorial_scaffolding_candidates"] = [
            {"pattern": "en_evidence_scaffold", "count": 1, "examples": ["private excerpt"]}
        ]
        report["reader_visible_output_candidates"] = [
            {
                "pattern": "undefined_internal_code_scheme",
                "count": 1,
                "reason": "private-safe reason",
                "action": "private-safe action",
                "examples": ["private excerpt"],
                "details": [{"family": "E", "codes": ["E1", "E2"], "missing_definitions": ["E2"]}],
            }
        ]
        report["docx_clean_copy_candidates"] = [
            {
                "pattern": "core_property_tool_identity_trace",
                "count": 1,
                "severity": "defect",
                "reason": "private-safe reason",
                "action": "private-safe action",
                "examples": ["lastModifiedBy: secret tool"],
                "details": ["lastModifiedBy"],
            }
        ]
        shareable = cns_audit.make_shareable(report)
        self.assertEqual(shareable["source"], "paper.txt")
        self.assertEqual(shareable["numeric_claims_without_nearby_citation"], [])
        self.assertEqual(shareable["numeric_claims_without_nearby_citation_count"], 1)
        self.assertIsNone(shareable["repeated_sentence_openers"][0]["opener"])
        self.assertIsNone(shareable["repeated_fragments"][0]["fragment"])
        self.assertNotIn("examples", shareable["editorial_scaffolding_candidates"][0])
        self.assertNotIn("examples", shareable["reader_visible_output_candidates"][0])
        self.assertNotIn("details", shareable["reader_visible_output_candidates"][0])
        self.assertEqual(shareable["reader_visible_output_candidates"][0]["details_count"], 1)
        self.assertNotIn("examples", shareable["docx_clean_copy_candidates"][0])
        self.assertNotIn("details", shareable["docx_clean_copy_candidates"][0])
        self.assertEqual(shareable["docx_clean_copy_candidates"][0]["details_count"], 1)

    def test_crossref_429_is_retried(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(
                    {
                        "message": {
                            "title": ["Verified title"],
                            "issued": {"date-parts": [[2026]]},
                            "URL": "https://doi.org/10.1000/test",
                        }
                    }
                ).encode("utf-8")

        rate_limit = urllib.error.HTTPError(
            "https://api.crossref.org/works/test", 429, "rate limited", {"Retry-After": "0"}, None
        )
        with mock.patch.object(
            cns_audit.urllib.request, "urlopen", side_effect=[rate_limit, FakeResponse()]
        ), mock.patch.object(cns_audit.time, "sleep") as sleep:
            result = cns_audit.verify_doi("10.1000/test")
        self.assertEqual(result["status"], "verified")
        sleep.assert_called_once()


if __name__ == "__main__":
    unittest.main()
