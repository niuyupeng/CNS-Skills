from __future__ import annotations

import importlib.util
import json
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("visual_audit", ROOT / "scripts" / "visual_audit.py")
visual_audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(visual_audit)

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"


def png_header(width: int = 600, height: int = 300) -> bytes:
    return b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + struct.pack(">II", width, height) + b"\x08\x02\x00\x00\x00"


def styles_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
    <w:styles xmlns:w="{W}">
      <w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/></w:style>
      <w:style w:type="table" w:styleId="TableNormal"><w:name w:val="Table Normal"/></w:style>
      <w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>
        <w:tblPr><w:tblBorders>
          <w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/>
          <w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/>
          <w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/>
        </w:tblBorders></w:tblPr>
      </w:style>
    </w:styles>'''


def table_xml(
    *,
    style: str = "TableNormal",
    caption_style: str = "Caption",
    caption: bool = True,
    color_fill: str = "FFFFFF",
    font_half_points: int = 18,
    header_rule: bool = True,
    repeat_header: bool = True,
    protect_rows: bool = True,
    caption_text: str = "Table 1. Results",
) -> str:
    table_caption = (
        f'<w:p><w:pPr><w:pStyle w:val="{caption_style}"/></w:pPr><w:r><w:t>{caption_text}</w:t></w:r></w:p>'
        if caption
        else ""
    )
    borders = '''<w:tblBorders>
      <w:top w:val="single" w:sz="12"/><w:left w:val="nil"/>
      <w:bottom w:val="single" w:sz="12"/><w:right w:val="nil"/>
      <w:insideH w:val="nil"/><w:insideV w:val="nil"/>
    </w:tblBorders>''' if style != "TableGrid" else ""
    header_properties = ("<w:tblHeader/>" if repeat_header else "") + ("<w:cantSplit/>" if protect_rows else "")
    body_properties = "<w:cantSplit/>" if protect_rows else ""
    bottom = '<w:tcBorders><w:bottom w:val="single" w:sz="6"/></w:tcBorders>' if header_rule else ""

    def cell(value: str, header: bool = False) -> str:
        rule = bottom if header else ""
        return f'''<w:tc><w:tcPr>{rule}<w:shd w:fill="{color_fill}"/></w:tcPr>
          <w:p><w:r><w:rPr><w:sz w:val="{font_half_points}"/></w:rPr><w:t>{value}</w:t></w:r></w:p></w:tc>'''

    return table_caption + f'''<w:tbl><w:tblPr><w:tblStyle w:val="{style}"/>{borders}</w:tblPr>
      <w:tr><w:trPr>{header_properties}</w:trPr>{cell("Item", True)}{cell("Value", True)}</w:tr>
      <w:tr><w:trPr>{body_properties}</w:trPr>{cell("A")}{cell("1")}</w:tr>
    </w:tbl>'''


def figure_xml(
    *,
    kind: str = "inline",
    width_inches: float = 2.0,
    height_inches: float = 1.0,
    alt_text: str = "Decision pathway",
    caption_style: str = "Caption",
) -> str:
    cx = int(width_inches * 914400)
    cy = int(height_inches * 914400)
    descr = f' descr="{alt_text}"' if alt_text else ""
    return f'''<w:p><w:r><w:drawing><wp:{kind}>
      <wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="1" name="Figure 1"{descr}/>
      <a:graphic><a:graphicData><a:blip r:embed="rId1"/></a:graphicData></a:graphic>
    </wp:{kind}></w:drawing></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="{caption_style}"/></w:pPr><w:r><w:t>Figure 1. Decision pathway.</w:t></w:r></w:p>'''


def write_docx(path: Path, body: str, *, include_image: bool = False) -> None:
    document = f'''<?xml version="1.0" encoding="UTF-8"?>
    <w:document xmlns:w="{W}" xmlns:a="{A}" xmlns:r="{R}" xmlns:wp="{WP}">
      <w:body>{body}</w:body>
    </w:document>'''
    relationships = f'''<?xml version="1.0" encoding="UTF-8"?>
    <Relationships xmlns="{PR}">
      <Relationship Id="rId1" Type="{R}/image" Target="media/image1.png"/>
    </Relationships>'''
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document.encode("utf-8"))
        archive.writestr("word/styles.xml", styles_xml().encode("utf-8"))
        archive.writestr("word/_rels/document.xml.rels", relationships.encode("utf-8"))
        if include_image:
            archive.writestr("word/media/image1.png", png_header())


def codes(item: dict) -> set[str]:
    return {entry["code"] for entry in item["issues"]}


class VisualAuditTests(unittest.TestCase):
    def report_for(self, body: str, *, include_image: bool = False, expect_three_line: bool = True):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "paper.docx"
        write_docx(path, body, include_image=include_image)
        return visual_audit.build_report(path, expect_three_line=expect_three_line)

    def test_good_three_line_table_passes(self):
        report = self.report_for(table_xml())
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["tables"][0]["issues"], [])

    def test_table_grid_style_is_resolved_and_rejected(self):
        table = self.report_for(table_xml(style="TableGrid"))["tables"][0]
        self.assertIn("three_line_vertical_rules", codes(table))
        self.assertIn("three_line_interior_rules", codes(table))

    def test_colored_fill_is_rejected_for_three_line_default(self):
        table = self.report_for(table_xml(color_fill="D9EAF7"))["tables"][0]
        self.assertIn("table_color_fill", codes(table))

    def test_missing_header_rule_is_detected(self):
        table = self.report_for(table_xml(header_rule=False))["tables"][0]
        self.assertIn("three_line_missing_header_rule", codes(table))

    def test_small_table_text_is_detected(self):
        table = self.report_for(table_xml(font_half_points=15))["tables"][0]
        self.assertIn("table_text_too_small", codes(table))

    def test_missing_caption_is_an_error(self):
        table = self.report_for(table_xml(caption=False))["tables"][0]
        self.assertIn("table_caption_missing_or_displaced", codes(table))

    def test_chinese_supplementary_table_caption_is_recognized(self):
        table = self.report_for(table_xml(caption_text="补充表S1｜完整矩阵"))["tables"][0]
        self.assertNotIn("table_caption_missing_or_displaced", codes(table))

    def test_normal_caption_style_is_a_warning(self):
        table = self.report_for(table_xml(caption_style="Normal"))["tables"][0]
        self.assertIn("table_caption_style", codes(table))

    def test_nonrepeating_header_is_detected(self):
        table = self.report_for(table_xml(repeat_header=False))["tables"][0]
        self.assertIn("header_row_not_repeating", codes(table))

    def test_unprotected_rows_are_detected(self):
        table = self.report_for(table_xml(protect_rows=False))["tables"][0]
        self.assertIn("rows_may_split", codes(table))

    def test_figure_dpi_alt_text_and_caption_pass(self):
        figure = self.report_for(figure_xml(), include_image=True, expect_three_line=False)["figures"][0]
        self.assertEqual(figure["effective_dpi"], 300.0)
        self.assertEqual(figure["issues"], [])

    def test_low_raster_dpi_is_an_error(self):
        figure = self.report_for(
            figure_xml(width_inches=4, height_inches=2), include_image=True, expect_three_line=False
        )["figures"][0]
        self.assertIn("raster_dpi_low", codes(figure))

    def test_anchor_is_a_renderer_warning(self):
        figure = self.report_for(figure_xml(kind="anchor"), include_image=True, expect_three_line=False)["figures"][0]
        self.assertIn("floating_figure", codes(figure))

    def test_missing_alt_text_is_detected(self):
        figure = self.report_for(figure_xml(alt_text=""), include_image=True, expect_three_line=False)["figures"][0]
        self.assertIn("figure_alt_text_missing", codes(figure))

    def test_shareable_report_hides_paths_and_visible_text(self):
        report = self.report_for(table_xml() + figure_xml(), include_image=True)
        shared = visual_audit.make_shareable(report)
        self.assertEqual(shared["source"], "paper.docx")
        self.assertEqual(shared["tables"][0]["caption"]["text"], "")
        self.assertEqual(shared["figures"][0]["alt_text"], "")

    def test_json_output_cannot_overwrite_source(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper.docx"
            write_docx(path, table_xml())
            self.assertEqual(visual_audit.main([str(path), "--json", str(path)]), 1)

    def test_strict_returns_two_for_errors(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper.docx"
            write_docx(path, table_xml(style="TableGrid"))
            self.assertEqual(visual_audit.main([str(path), "--expect-three-line", "--strict"]), 2)

    def test_nonpositive_dpi_threshold_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "paper.docx"
            write_docx(path, table_xml())
            self.assertEqual(visual_audit.main([str(path), "--minimum-raster-dpi", "0"]), 1)

    def test_png_dimensions_are_read_without_third_party_packages(self):
        self.assertEqual(visual_audit.png_dimensions(png_header(1200, 800)), (1200, 800))


if __name__ == "__main__":
    unittest.main()
