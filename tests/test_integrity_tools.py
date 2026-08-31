import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


invariants = load_script("check_invariants")
crossrefs = load_script("check_crossrefs")


class InvariantTests(unittest.TestCase):
    def test_reports_changed_quantity_and_doi(self):
        source = invariants.extract("Dose 5 mg and yield 92%; p < 0.05; doi:10.1000/ABC [1].")
        revised = invariants.extract("Dose 8 mg and yield 91%; p < 0.05; doi:10.1000/XYZ [1].")
        result = invariants.compare(source, revised)
        self.assertEqual(result["status"], "changed")
        self.assertEqual(result["categories"]["statistics"]["status"], "unchanged")
        self.assertEqual(result["categories"]["dois"]["status"], "changed")
        self.assertEqual(result["categories"]["quantities"]["status"], "changed")
        removed_quantities = {
            item["value"] for item in result["categories"]["quantities"]["removed"]
        }
        self.assertIn("92%", removed_quantities)

    def test_protected_tokens_preserve_exact_counts(self):
        source = invariants.extract("PEG-DA and PEG-DA", ["PEG-DA"])
        revised = invariants.extract("PEGDA", ["PEG-DA"])
        result = invariants.compare(source, revised)
        removed = result["categories"]["protected_tokens"]["removed"]
        self.assertEqual(removed, [{"value": "PEG-DA", "count": 2}])

    def test_order_swap_is_not_reported_clean(self):
        source = invariants.extract("Group A received 5 mg; group B received 10 mg.")
        revised = invariants.extract("Group A received 10 mg; group B received 5 mg.")
        result = invariants.compare(source, revised)
        self.assertEqual(result["categories"]["quantities"]["status"], "unchanged")
        self.assertEqual(result["categories"]["quantity_order"]["status"], "changed")

    def test_unicode_minus_and_compound_unit_changes_are_detected(self):
        source = invariants.extract("Stored at −5 °C; dose 5 mg/kg.")
        revised = invariants.extract("Stored at 5 °C; dose 5 mg/mL.")
        result = invariants.compare(source, revised)
        self.assertEqual(result["categories"]["quantities"]["status"], "changed")

    def test_molar_and_velocity_unit_only_changes_are_detected(self):
        source = invariants.extract("Concentration 5 mol/L; velocity 5 m/s.")
        revised = invariants.extract("Concentration 5 mmol/L; velocity 5 m/min.")
        result = invariants.compare(source, revised)
        self.assertEqual(result["categories"]["quantities"]["status"], "changed")

    def test_case_sensitive_si_units_do_not_collapse(self):
        source = invariants.extract("Concentration 5 mM; stock 5 M.")
        revised = invariants.extract("Length 5 mm; distance 5 m.")
        result = invariants.compare(source, revised)
        self.assertEqual(result["categories"]["quantities"]["status"], "changed")
        self.assertEqual(sum(invariants.extract("invalid 5 k")["quantities"].values()), 0)

    def test_build_report_reads_text_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.txt"
            revised = Path(temp_dir) / "revised.txt"
            source.write_text("n = 20", encoding="utf-8")
            revised.write_text("n = 21", encoding="utf-8")
            self.assertEqual(invariants.build_report(source, revised)["status"], "changed")

    def test_json_output_cannot_overwrite_an_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.txt"
            revised = Path(temp_dir) / "revised.txt"
            source.write_text("5 mg", encoding="utf-8")
            revised.write_text("5 mg", encoding="utf-8")
            self.assertEqual(
                invariants.main([str(source), str(revised), "--json", str(source)]), 1
            )
            self.assertEqual(source.read_text(encoding="utf-8"), "5 mg")

    def test_shareable_invariant_report_removes_directories(self):
        report = {
            "source": "C:/private/source.docx",
            "revised": "C:/private/revised.docx",
            "protected_token_file": "C:/private/tokens.txt",
        }
        shareable = invariants.make_shareable(report)
        self.assertEqual(shareable["source"], "source.docx")
        self.assertEqual(shareable["revised"], "revised.docx")
        self.assertEqual(shareable["protected_token_file"], "tokens.txt")

    def test_author_year_detection_rejects_document_version_year(self):
        extracted = invariants.extract("CNS revision 2026; Smith et al. 2026 reported the result.")
        self.assertEqual(sum(extracted["author_year_citations"].values()), 1)

    def test_office_math_change_is_detected_in_docx(self):
        def document(value):
            return f'''<?xml version="1.0" encoding="UTF-8"?>
            <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
              xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
              <w:body><w:p><w:r><w:t>Equation: </w:t></w:r><m:oMath><m:r><m:t>{value}</m:t></m:r></m:oMath></w:p></w:body>
            </w:document>'''.encode("utf-8")

        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.docx"
            revised = Path(temp_dir) / "revised.docx"
            for path, value in ((source, "5"), (revised, "10")):
                with zipfile.ZipFile(path, "w") as archive:
                    archive.writestr("word/document.xml", document(value))
            self.assertEqual(invariants.build_report(source, revised)["status"], "changed")


class CrossReferenceTests(unittest.TestCase):
    def test_clean_caption_reference_pair(self):
        result = crossrefs.audit_paragraphs(
            ["As shown in Figure 1, performance increased.", "Figure 1. Main result."]
        )
        self.assertEqual(result["status"], "clean")

    def test_missing_uncited_and_duplicate_are_separate(self):
        result = crossrefs.audit_paragraphs(
            [
                "See Fig. 2 and Table 1.",
                "Figure 1. First caption.",
                "Figure 1. Duplicate caption.",
                "Table 1. Comparison.",
            ]
        )
        self.assertEqual(result["status"], "issues_found")
        self.assertEqual(result["references_without_caption"][0]["id"], "figure:2")
        self.assertEqual(result["captions_without_reference"][0]["id"], "figure:1")
        self.assertEqual(result["duplicate_captions"][0]["count"], 2)

    def test_paragraph_starting_figure_shows_is_a_reference(self):
        result = crossrefs.audit_paragraphs(["Figure 1 shows the main result."])
        self.assertEqual(result["caption_count"], 0)
        self.assertEqual(result["references_without_caption"][0]["id"], "figure:1")

    def test_json_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper.txt"
            path.write_text("Figure 1. Caption.", encoding="utf-8")
            self.assertEqual(crossrefs.main([str(path), "--json", str(path)]), 1)
            self.assertEqual(path.read_text(encoding="utf-8"), "Figure 1. Caption.")

    def test_extended_and_supplementary_figures_do_not_collapse_into_main(self):
        result = crossrefs.audit_paragraphs(
            [
                "Figure 1. Main result.",
                "Figure 1 shows the main result.",
                "Supplementary Figure 1 shows the sensitivity analysis.",
                "Extended Data Fig. 1 shows the external cohort.",
            ]
        )
        missing = {item["id"] for item in result["references_without_caption"]}
        self.assertIn("supplementary-figure:1", missing)
        self.assertIn("extended-data-figure:1", missing)
        self.assertNotIn("figure:1", missing)

    def test_shareable_crossref_report_removes_excerpts(self):
        report = {
            "source": "C:/private/paper.docx",
            "references_without_caption": [{"id": "figure:1", "examples": ["secret"]}],
            "captions_without_reference": [{"id": "table:1", "caption": "secret"}],
            "duplicate_captions": [{"id": "table:2", "count": 2, "example": "secret"}],
        }
        shareable = crossrefs.make_shareable(report)
        self.assertEqual(shareable["source"], "paper.docx")
        self.assertEqual(shareable["references_without_caption"][0]["examples"], [])
        self.assertIsNone(shareable["captions_without_reference"][0]["caption"])

    def test_supplementary_s_prefix_and_supplemental_alias_match(self):
        result = crossrefs.audit_paragraphs(
            [
                "Figure S1 shows the sensitivity analysis.",
                "Supplementary Figure S1. Sensitivity analysis.",
                "Supplemental Table 2 lists the parameters.",
                "Table S2. Parameter list.",
            ]
        )
        self.assertEqual(result["status"], "clean")

    def test_companion_artifact_resolves_supplementary_reference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            main = Path(temp_dir) / "paper.txt"
            supplement = Path(temp_dir) / "supplement.txt"
            main.write_text("Supplementary Table S1 lists the complete matrix.\n", encoding="utf-8")
            supplement.write_text("Supplementary Table S1 | Complete matrix.\n", encoding="utf-8")
            result = crossrefs.build_report(main, [supplement])
            self.assertEqual(result["status"], "clean")
            self.assertEqual(result["companions"], [str(supplement.resolve())])

    def test_json_output_cannot_overwrite_companion(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            main = Path(temp_dir) / "paper.txt"
            supplement = Path(temp_dir) / "supplement.txt"
            main.write_text("Supplementary Table S1 lists the matrix.\n", encoding="utf-8")
            supplement.write_text("Supplementary Table S1 | Matrix.\n", encoding="utf-8")
            self.assertEqual(
                crossrefs.main([str(main), "--companion", str(supplement), "--json", str(supplement)]),
                1,
            )
            self.assertEqual(supplement.read_text(encoding="utf-8"), "Supplementary Table S1 | Matrix.\n")


if __name__ == "__main__":
    unittest.main()
