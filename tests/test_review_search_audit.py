from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "review_search_audit", ROOT / "scripts" / "review_search_audit.py"
)
review_search_audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(review_search_audit)


def strict_exit(text: str) -> int:
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "review.txt"
        path.write_text(text, encoding="utf-8")
        return review_search_audit.main([str(path), "--strict-systematic"])


class ReviewSearchAuditTests(unittest.TestCase):
    def test_current_style_is_transparent_but_query_like(self):
        text = (
            "This structured narrative review used searches updated through 30 August 2026 "
            "across PubMed, publisher platforms, DOI landing pages, and an author-curated "
            "full-text collection. Search terms paired ‘biomaterial / hydrogel / polymer / "
            "lipid nanoparticle’ with ‘machine learning / graph neural network / transformer / "
            "active learning’. Cases were prioritized when the model changed the experiment. "
            "This is not a systematic review and does not estimate literature coverage."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["declared_review_type"], "structured_narrative")
        self.assertEqual(report["disclosure_pattern"], "transparent_narrative_scope")
        codes = {item["code"] for item in report["diagnostics"]}
        self.assertIn("query_like_inventory_without_executable_query", codes)
        self.assertIn("discovery_and_verification_sources_need_roles", codes)
        self.assertIn("author_collection_boundary_needed", codes)

    def test_concise_narrative_scope_is_not_forced_into_prisma(self):
        text = (
            "We conducted a narrative review of PubMed through 30 August 2026. "
            "We selected studies that changed an experimental decision and used them as "
            "illustrative comparisons rather than an exhaustive census."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["disclosure_pattern"], "transparent_narrative_scope")
        self.assertEqual(report["missing_systematic_elements"], [])
        self.assertEqual(report["diagnostics"], [])

    def test_supplemented_narrative_query_is_not_flagged(self):
        text = (
            "This structured narrative review searched PubMed through 2026. We selected "
            "decision-changing experiments and do not claim comprehensive coverage. "
            "The Supplementary Search Strategy gives the full PubMed query: "
            "(biomaterial[Title/Abstract] OR hydrogel[Title/Abstract]) AND "
            "machine learning[Title/Abstract]."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        codes = {item["code"] for item in report["diagnostics"]}
        self.assertNotIn("query_like_inventory_without_executable_query", codes)
        self.assertTrue(report["evidence"]["supplementary_search_record"])
        self.assertTrue(report["evidence"]["executable_query_markers"])

    def test_incomplete_systematic_review_is_critical(self):
        text = (
            "We conducted a systematic review in PubMed through 2025. Inclusion and exclusion "
            "criteria were predefined."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["disclosure_pattern"], "systematic_record_incomplete")
        self.assertIn("deduplication", report["missing_systematic_elements"])
        self.assertIn("screening_process", report["missing_systematic_elements"])
        self.assertIn("flow_accounting", report["missing_systematic_elements"])

    def test_complete_systematic_record_passes_structural_check(self):
        text = (
            "We conducted a systematic review. PubMed and Embase were searched through "
            "30 August 2026 using (hydrogel[Title/Abstract] OR polymer[Title/Abstract]) AND "
            "machine learning[Title/Abstract]. Inclusion and exclusion criteria were predefined. "
            "Duplicate records were removed. Two reviewers independently screened titles and "
            "abstracts and then full text. The PRISMA flow diagram reports records identified, "
            "screened, and excluded."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["disclosure_pattern"], "systematic_record_structurally_complete")
        self.assertEqual(report["missing_systematic_elements"], [])

    def test_negative_systematic_phrase_does_not_override_narrative_type(self):
        text = "This narrative review is not a systematic review."
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["declared_review_type"], "narrative")

    def test_negative_systematic_phrase_alone_is_not_classified_as_systematic(self):
        texts = (
            "This review is not a systematic review and does not estimate coverage.",
            "本文并未开展系统评价，也不估计文献覆盖率。",
        )
        for text in texts:
            with self.subTest(text=text):
                report = review_search_audit.build_report(Path("review.txt"), text)
                self.assertEqual(report["declared_review_type"], "narrative")

    def test_distinct_type_and_coverage_boundaries_are_not_called_repetition(self):
        text = (
            "This narrative review is not systematic.\n\n"
            "The selected studies are illustrative and not an exhaustive census."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        codes = {item["code"] for item in report["diagnostics"]}
        self.assertNotIn("repeated_non_systematic_disclaimer", codes)
        self.assertEqual(report["evidence"]["coverage_boundary_paragraphs"], 2)

    def test_coverage_purpose_and_final_disclaimer_are_recognized_as_repetition(self):
        text = (
            "This structured narrative review searched PubMed to identify representative "
            "cases rather than to estimate literature coverage.\n\n"
            "Because this is not a systematic review, the selected studies are not an "
            "exhaustive census."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["evidence"]["coverage_boundary_paragraphs"], 2)
        self.assertIn(
            "repeated_non_systematic_disclaimer",
            {item["code"] for item in report["diagnostics"]},
        )

    def test_reference_list_does_not_change_review_classification(self):
        text = (
            "This narrative review selected illustrative studies.\n\nReferences\n\n"
            "A systematic review of hydrogels."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["declared_review_type"], "narrative")

    def test_generic_comparison_dimensions_are_not_a_database(self):
        text = (
            "This narrative review compares validation along three dimensions. "
            "PubMed was searched through 2026; we selected illustrative studies, "
            "not an exhaustive census."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["evidence"]["named_databases"], ["PubMed"])

    def test_chinese_narrative_scope(self):
        text = (
            "本综述采用结构化叙述性综述方法，检索更新至2026年8月30日，以PubMed为主要数据库。"
            "案例优先纳入AI实际改变实验顺序的研究。本研究未按系统综述流程估计文献覆盖率。"
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["declared_review_type"], "structured_narrative")
        self.assertEqual(report["disclosure_pattern"], "transparent_narrative_scope")

    def test_docx_text_is_supported(self):
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:body><w:p><w:r><w:t>This narrative review searched PubMed through 2026. '
            'We selected illustrative cases, not an exhaustive census.</w:t></w:r></w:p>'
            '</w:body></w:document>'
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "review.docx"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("word/document.xml", xml)
            loaded = review_search_audit.read_text(path)
        self.assertIn("narrative review", loaded)

    def test_json_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "review.txt"
            path.write_text("This narrative review selected illustrative studies.", encoding="utf-8")
            original = path.read_bytes()
            exit_code = review_search_audit.main([str(path), "--json", str(path)])
            self.assertEqual(exit_code, 2)
            self.assertEqual(path.read_bytes(), original)

    def test_spectrometer_commands_do_not_satisfy_supplementary_search_record(self):
        text = (
            "We conducted a systematic review. PubMed was searched until 29 August 2026. "
            "Reports were included when they evaluated implanted materials. Search results "
            "were deduplicated. Two authors screened titles, abstracts, and full texts. "
            "A record flow chart gives records identified, screened, and excluded. "
            "The attached Supplement S4 houses the exact platform-specific commands and "
            "execution dates used for every spectrometer."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["evidence"]["supplementary_search_status"], "absent")
        self.assertFalse(report["evidence"]["supplementary_search_record"])
        self.assertEqual(
            report["missing_systematic_elements"], ["executable_query_or_supplement"]
        )
        self.assertEqual(strict_exit(text), 3)

    def test_supplement_that_did_not_include_strategy_is_not_current_evidence(self):
        text = (
            "We conducted a systematic review. PubMed was searched until 29 August 2026. "
            "Reports were included when they evaluated implanted materials. Search results "
            "were deduplicated. Two authors screened titles, abstracts, and full texts. "
            "A record flow chart gives records identified, screened, and excluded. "
            "The supplementary files did not include the search strategy."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertNotEqual(
            report["evidence"]["supplementary_search_status"], "claimed_present"
        )
        self.assertFalse(report["evidence"]["supplementary_search_record"])
        self.assertEqual(strict_exit(text), 3)

    def test_n3_cell_culture_label_is_not_a_proximity_query(self):
        text = (
            "We conducted a systematic review. PubMed was searched until 29 August 2026. "
            "Reports were included when they evaluated implanted materials. Search results "
            "were deduplicated. Two authors screened titles, abstracts, and full texts. "
            "A record flow chart gives records identified, screened, and excluded. "
            "Cells were cultured with N3 fibroblasts."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertFalse(report["evidence"]["executable_query_markers"])
        self.assertEqual(
            report["missing_systematic_elements"], ["executable_query_or_supplement"]
        )
        self.assertEqual(strict_exit(text), 3)

    def test_attributed_unquoted_systematic_title_does_not_override_narrative_type(self):
        text = (
            "This narrative review uses representative examples and does not claim "
            "comprehensive coverage. Lee et al. reported This Systematic Review Reframes "
            "Scaffold Durability as a useful precedent."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertEqual(report["declared_review_type"], "narrative")
        self.assertEqual(report["missing_systematic_elements"], [])

    def test_outcome_follow_up_year_is_not_a_search_cutoff(self):
        text = (
            "We conducted a systematic review. PubMed was searched using "
            "implant[Title/Abstract]. Reports were included when they tested implants; "
            "search results were deduplicated; two authors screened titles, abstracts, and "
            "full texts; a record flow chart gives records identified, screened, and excluded. "
            "Outcomes were followed through 2025."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        self.assertFalse(report["evidence"]["search_date_or_cutoff"])
        self.assertEqual(report["missing_systematic_elements"], ["search_date_or_cutoff"])
        self.assertEqual(strict_exit(text), 3)

    def test_implicit_patient_record_pipeline_across_paragraphs_is_not_literature_selection(self):
        text = (
            "We conducted a systematic review. PubMed was searched until 29 August 2026 "
            "using implant[Title/Abstract]. Reports were included when they tested implants.\n\n"
            "The Results analyzed a hospital registry of electronic medical records.\n\n"
            "Duplicate records were removed; two reviewers independently screened records; "
            "a flow chart gives records identified, screened, and excluded."
        )
        report = review_search_audit.build_report(Path("review.txt"), text)
        selection = report["evidence"]["selection"]
        self.assertFalse(selection["deduplication"])
        self.assertFalse(selection["screening"])
        self.assertFalse(selection["flow_accounting"])
        self.assertEqual(
            report["missing_systematic_elements"],
            ["deduplication", "screening_process", "flow_accounting"],
        )
        self.assertEqual(strict_exit(text), 3)


if __name__ == "__main__":
    unittest.main()
