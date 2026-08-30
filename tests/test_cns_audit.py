import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cns_audit", ROOT / "scripts" / "cns_audit.py")
cns_audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(cns_audit)


class CNSAuditTests(unittest.TestCase):
    def test_doi_cleanup_and_deduplication(self):
        text = "See doi:10.1000/ABC. Also https://doi.org/10.1000/abc."
        self.assertEqual(cns_audit.doi_list(text), ["10.1000/abc"])

    def test_stock_phrase_detection(self):
        report = cns_audit.build_report(Path("sample.txt"), "这说明结果重要。这说明仍需验证。")
        hit = next(item for item in report["stock_phrase_hits"] if item["pattern"] == "zh_this_shows")
        self.assertEqual(hit["count"], 2)

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


if __name__ == "__main__":
    unittest.main()
