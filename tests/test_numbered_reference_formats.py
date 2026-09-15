"""Anonymous regression cases for bibliography and chapter/panel identifiers."""

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


citations = load("review_citation_audit")
crossrefs = load("check_crossrefs")


class NumberedReferenceFormatsTests(unittest.TestCase):
    def test_bracketed_docx_bibliography_and_body_stay_separate(self):
        paragraphs = ["[1] supports this claim.", "References", "[1] Alpha. doi:10.1000/alpha."]
        xml = '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
        xml += "".join("<w:p><w:r><w:t>" + escape(p) + "</w:t></w:r></w:p>" for p in paragraphs)
        xml += "</w:body></w:document>"
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "anonymous.docx"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("word/document.xml", xml.encode("utf-8"))
            report = citations.audit(path, citations.read_input(path))
        self.assertEqual(report["counts"]["reference_entries"], 1)
        self.assertEqual(report["counts"]["citation_occurrences_expanded"], 1)
        self.assertEqual(report["missing_reference_entries"], [])

    def test_mixed_text_bibliography_formats_keep_diagnostics(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "anonymous.md"
            path.write_text("Claim [1-4].\n\n# References\n\n[1] Alpha.\n\n2. Beta.\n\n3) Gamma.\n\n4、 Delta.", encoding="utf-8")
            report = citations.audit(path, citations.read_input(path))
        self.assertEqual(report["counts"]["reference_entries"], 4)
        self.assertEqual(report["missing_reference_entries"], [])
        self.assertEqual(report["uncited_reference_entries"], [])

    def test_malformed_brackets_are_not_reference_entries(self):
        for text in ("[1. Alpha", "[1) Alpha", "1] Alpha", "[1-3] Alpha", "[1]", "12345. Alpha"):
            with self.subTest(text=text):
                self.assertIsNone(citations.REFERENCE_RE.match(text))

    def test_bracketed_duplicate_and_gap_are_not_hidden(self):
        blocks = [citations.Block("paragraph", p) for p in (
            "Claim [1-3].", "References", "[1] Alpha.", "[3] Gamma.", "[3] Delta.")]
        report = citations.audit(Path("anonymous.txt"), blocks)
        self.assertEqual(report["duplicate_reference_numbers"], [3])
        self.assertEqual(report["reference_numbering_gaps"], [2])
        self.assertEqual(report["missing_reference_entries"], [2])

    def test_chapter_figures_and_panel_calls_resolve_distinct_parents(self):
        report = crossrefs.audit_paragraphs([
            "如图 2-1a 所示，结果提高。另见图2-2b和Figure 2-3c.",
            "图2-1 结构", "图 2-2. 测量", "Figure 2-3. Comparison."])
        self.assertEqual(report["status"], "clean")
        self.assertEqual(report["caption_count"], 3)
        self.assertEqual(report["panel_references"], {"figure:2-1a": 1, "figure:2-2b": 1, "figure:2-3c": 1})

    def test_real_duplicate_chapter_caption_still_fails(self):
        report = crossrefs.audit_paragraphs(["See Figure 2-1a.", "Figure 2-1. Alpha.", "Figure 2-1. Beta."])
        self.assertEqual(report["duplicate_captions"][0]["id"], "figure:2-1")

    def test_missing_chapter_figure_cannot_match_other_chapter(self):
        report = crossrefs.audit_paragraphs(["See Figure 3-2a.", "Figure 3-1. Caption."])
        self.assertEqual(report["references_without_caption"][0]["id"], "figure:3-2")
        self.assertEqual(report["captions_without_reference"][0]["id"], "figure:3-1")

    def test_dotted_and_supplementary_numbers_keep_scope(self):
        report = crossrefs.audit_paragraphs([
            "See Table 2.1 and Fig. S2-1a.", "Table 2.1. Settings.",
            "Supplementary Figure S2-1. Analysis."])
        self.assertEqual(report["status"], "clean")
        self.assertIn("supplementary-figure:2-1a", report["panel_references"])

    def test_chinese_prose_start_is_not_caption(self):
        report = crossrefs.audit_paragraphs(["图2-1a所示为实验结果。"])
        self.assertEqual(report["caption_count"], 0)
        self.assertEqual(report["references_without_caption"][0]["id"], "figure:2-1")

    def test_alphanumeric_tail_is_not_truncated_into_identifier(self):
        report = crossrefs.audit_paragraphs(["See Figure 2-1alpha and 图2-1alpha。"])
        # A partial prefix must not become a spurious call to Figure 2.
        self.assertEqual(report["reference_count"], 0)


if __name__ == "__main__":
    unittest.main()
