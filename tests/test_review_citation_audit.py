import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "review_citation_audit", ROOT / "scripts" / "review_citation_audit.py"
)
review_audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(review_audit)


def make_docx(path: Path) -> None:
    document = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:body>
        <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>1 Results</w:t></w:r></w:p>
        <w:p><w:r><w:t>First claim [1-2].</w:t></w:r></w:p>
        <w:p><w:r><w:t>Second claim [4].</w:t></w:r></w:p>
        <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>References</w:t></w:r></w:p>
        <w:p><w:r><w:t>1. Alpha. doi:10.1000/alpha.</w:t></w:r></w:p>
        <w:p><w:r><w:t>2. Beta. doi:10.1000/shared.</w:t></w:r></w:p>
        <w:p><w:r><w:t>3. Gamma. doi:10.1000/shared.</w:t></w:r></w:p>
      </w:body>
    </w:document>'''
    styles = b'''<?xml version="1.0" encoding="UTF-8"?>
    <w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="Heading 1"/></w:style>
    </w:styles>'''
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)
        archive.writestr("word/styles.xml", styles)


class ReviewCitationAuditTests(unittest.TestCase):
    def test_ranges_missing_entries_uncited_entries_and_duplicate_dois(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "review.docx"
            make_docx(path)
            report = review_audit.audit(path, review_audit.read_input(path))
        self.assertEqual(report["missing_reference_entries"], [4])
        self.assertEqual(report["uncited_reference_entries"], [3])
        self.assertEqual(report["reference_numbering_gaps"], [])
        self.assertEqual(report["duplicate_dois"][0]["reference_numbers"], [2, 3])
        self.assertEqual(report["sections"][0]["unique_citations"], [1, 2, 4])

    def test_en_dash_range(self):
        self.assertEqual(review_audit.citations("Several studies [2–5, 8]."), [2, 3, 4, 5, 8])

    def test_shareable_report_removes_absolute_path(self):
        report = {"source": "/private/review.docx", "counts": {}}
        self.assertEqual(review_audit.make_shareable(report)["source"], "review.docx")

    def test_markdown_sections_and_numbering_gap(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "review.md"
            path.write_text(
                "# Design\n\nA supported claim [1, 3].\n\n# References\n\n"
                "1. Alpha. doi:10.1000/alpha.\n\n3. Gamma. doi:10.1000/gamma.\n",
                encoding="utf-8",
            )
            report = review_audit.audit(path, review_audit.read_input(path))
        self.assertEqual(report["reference_numbering_gaps"], [2])
        self.assertEqual(report["sections"][0]["section"], "Design")
        self.assertEqual(report["sections"][0]["unique_citations"], [1, 3])

    def test_out_of_order_references_are_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "review.md"
            path.write_text(
                "Claim [1-2].\n\n# References\n\n2. Beta.\n\n1. Alpha.\n",
                encoding="utf-8",
            )
            report = review_audit.audit(path, review_audit.read_input(path))
        self.assertEqual(
            report["out_of_order_reference_numbers"],
            [{"position": 2, "previous": 2, "current": 1}],
        )

    def test_structural_findings_return_diagnostic_exit_code(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "review.md"
            path.write_text("Claim [2].\n\n# References\n\n1. Alpha.\n", encoding="utf-8")
            self.assertEqual(review_audit.main([str(path)]), 2)

    def test_json_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper.txt"
            path.write_text("References", encoding="utf-8")
            self.assertEqual(review_audit.main([str(path), "--json", str(path)]), 1)
            self.assertEqual(path.read_text(encoding="utf-8"), "References")


if __name__ == "__main__":
    unittest.main()
