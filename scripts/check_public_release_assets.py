#!/usr/bin/env python3
"""Fail CI when public claims, local links, or release assets drift."""

from __future__ import annotations

import csv
import json
import re
import sys
import unittest
import zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

PUBLIC_MARKDOWN = (
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "research" / "README.md",
    ROOT / "research" / "genre-corpus-2026" / "README.md",
    ROOT / "examples" / "synthetic-hydrogel-demo" / "README.md",
    ROOT / "distribution" / "README.md",
)

CORPUS_MANIFESTS = {
    "reviews": ROOT / "research" / "genre-corpus-2026" / "reviews" / "reviews_manifest_200.csv",
    "articles": ROOT / "research" / "genre-corpus-2026" / "articles" / "articles_manifest_200.csv",
    "conferences": ROOT / "research" / "genre-corpus-2026" / "conferences" / "conference_manifest_200.csv",
}

REQUIRED_FILES = (
    ROOT / "research" / "genre-corpus-2026" / "conferences" / "conference_metrics.json",
    ROOT / "research" / "genre-corpus-2026" / "conferences" / "conference_findings.md",
    ROOT / "research" / "genre-corpus-2026" / "conferences" / "provenance.md",
    ROOT / "examples" / "synthetic-hydrogel-demo" / "CNS-Skills-synthetic-manuscript-demo.docx",
    ROOT / "examples" / "synthetic-hydrogel-demo" / "CNS-Skills-synthetic-manuscript-demo.pdf",
    ROOT / "examples" / "synthetic-hydrogel-demo" / "demo-preview.png",
    ROOT / "examples" / "synthetic-hydrogel-demo" / "reports" / "claim-citation-risk-report.json",
    ROOT / "examples" / "synthetic-hydrogel-demo" / "reports" / "overclaim-risk-report.json",
    ROOT / "examples" / "synthetic-hydrogel-demo" / "reports" / "cross-reference-risk-report.json",
    ROOT / "examples" / "synthetic-hydrogel-demo" / "reports" / "clean-copy-risk-report.json",
    ROOT / "references" / "visual-production.md",
    ROOT / "research" / "visual-production-study.md",
    ROOT / "assets" / "figure_brief.json",
)

PUBLIC_TOOLS = (
    "cns_audit.py",
    "review_citation_audit.py",
    "review_search_audit.py",
    "title_audit.py",
    "check_invariants.py",
    "check_crossrefs.py",
    "visual_audit.py",
    "figure_brief.py",
    "render_concept_svg.py",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def validate_required_files() -> None:
    for path in REQUIRED_FILES:
        if not path.is_file() or path.stat().st_size < 100:
            fail(f"required public asset is missing or empty: {path.relative_to(ROOT)}")


def markdown_local_targets(path: Path) -> list[Path]:
    text = path.read_text(encoding="utf-8")
    targets: list[Path] = []
    for raw in re.findall(r"!?(?:\[[^\]]*\])\(([^)]+)\)", text):
        target = raw.strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target or any(token in target for token in ("FROZEN_", "${{", "<")):
            continue
        targets.append((path.parent / target).resolve())
    return targets


def validate_local_links() -> None:
    for markdown in PUBLIC_MARKDOWN:
        if not markdown.is_file():
            fail(f"public Markdown entry point is missing: {markdown.relative_to(ROOT)}")
        for target in markdown_local_targets(markdown):
            try:
                target.relative_to(ROOT)
            except ValueError:
                fail(f"local link escapes repository: {markdown.relative_to(ROOT)} -> {target}")
            if not target.exists():
                fail(f"broken local link: {markdown.relative_to(ROOT)} -> {target.relative_to(ROOT)}")


def validate_corpus() -> None:
    prohibited_exact_columns = {"abstract", "full_text", "body_text", "pdf_text", "document_text"}
    for layer, path in CORPUS_MANIFESTS.items():
        if not path.is_file():
            fail(f"missing {layer} corpus manifest: {path.relative_to(ROOT)}")
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fields = set(reader.fieldnames or [])
        if len(rows) != 200:
            fail(f"{layer} manifest has {len(rows)} rows; expected 200")
        corpus_ids = [row.get("corpus_id", "") for row in rows]
        if any(not item for item in corpus_ids) or len(set(corpus_ids)) != 200:
            fail(f"{layer} corpus_id values must be 200 non-empty unique identifiers")
        leaked = fields & prohibited_exact_columns
        if leaked:
            fail(f"{layer} manifest redistributes text columns: {sorted(leaked)}")

    conference = CORPUS_MANIFESTS["conferences"]
    with conference.open(encoding="utf-8-sig", newline="") as handle:
        conference_rows = list(csv.DictReader(handle))
    counts = Counter(row.get("venue", "") for row in conference_rows)
    expected = {"AAAI": 40, "CVPR": 40, "NeurIPS": 40, "ICML": 40, "ICLR": 40}
    if counts != Counter(expected):
        fail(f"conference allocation drifted: {dict(counts)}")
    for field in ("paper_id", "canonical_url"):
        values = [row.get(field, "") for row in conference_rows]
        if any(not item for item in values) or len(set(values)) != 200:
            fail(f"conference {field} values must be 200 non-empty unique identifiers")

    with CORPUS_MANIFESTS["reviews"].open(encoding="utf-8-sig", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    review_levels = Counter(row.get("actual_analysis_text_level", "") for row in review_rows)
    if review_levels != Counter({"full_text_xml": 42, "abstract": 157, "title": 1}):
        fail(f"review analysis-level counts drifted: {dict(review_levels)}")

    with CORPUS_MANIFESTS["articles"].open(encoding="utf-8-sig", newline="") as handle:
        article_rows = list(csv.DictReader(handle))
    article_levels = Counter(row.get("analysis_level", "") for row in article_rows)
    expected_article_level = {"title_plus_pubmed_abstract_plus_pmc_jats_full_text": 200}
    if article_levels != Counter(expected_article_level):
        fail(f"article analysis-level counts drifted: {dict(article_levels)}")

    conference_levels = Counter(row.get("analysis_text_level", "") for row in conference_rows)
    if conference_levels != Counter({"full_text_extracted": 195, "abstract_only": 5}):
        fail(f"conference analysis-level counts drifted: {dict(conference_levels)}")

    metrics_path = ROOT / "research" / "genre-corpus-2026" / "conferences" / "conference_metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    validation = metrics.get("validation", {})
    if validation.get("total_records") != 200:
        fail("conference metrics total_records must equal 200")
    if validation.get("per_venue") != expected:
        fail("conference metrics per_venue does not match the public 40×5 design")
    if validation.get("title_level_analyzed") != 200:
        fail("conference title-level denominator must equal 200")
    if validation.get("abstract_level_analyzed") != 200:
        fail("conference abstract-level denominator must equal 200")
    if validation.get("full_text_level_analyzed") != 195:
        fail("conference full-text denominator must equal 195")


def validate_public_counts() -> None:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    test_count = suite.countTestCases()
    if test_count != 231:
        fail(f"discovered {test_count} tests; update the public proof line and this release gate")

    routing_path = ROOT / "evals" / "discovery-prompts.jsonl"
    routing = [json.loads(line) for line in routing_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(routing) != 68:
        fail(f"discovery prompt count is {len(routing)}; expected 68")

    if len(PUBLIC_TOOLS) != 9:
        fail(f"public tool registry contains {len(PUBLIC_TOOLS)} entries; expected 9")

    for name in PUBLIC_TOOLS:
        if not (ROOT / "scripts" / name).is_file():
            fail(f"missing public tool: scripts/{name}")

    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    for label, text in (("README.md", english), ("README.zh-CN.md", chinese)):
        for claim in ("231", "118", "93", "68", "600"):
            if claim not in text:
                fail(f"{label} no longer exposes the validated {claim} proof count")
    if "9 transparent local tools" not in english:
        fail("README.md no longer exposes the validated 9-tool public count")
    if "9 个透明本地工具" not in chinese:
        fail("README.zh-CN.md no longer exposes the validated 9-tool public count")


def validate_demo_package() -> None:
    demo = ROOT / "examples" / "synthetic-hydrogel-demo"
    docx_path = demo / "CNS-Skills-synthetic-manuscript-demo.docx"
    with zipfile.ZipFile(docx_path) as archive:
        names = set(archive.namelist())
        if "word/document.xml" not in names:
            fail("demo DOCX has no word/document.xml")
        if "word/comments.xml" in names:
            fail("demo DOCX still contains comments")
        xml = archive.read("word/document.xml")
        if b"<w:ins" in xml or b"<w:del" in xml:
            fail("demo DOCX still contains tracked insertions or deletions")
        package_bytes = b"\n".join(archive.read(name) for name in names if name.endswith((".xml", ".rels")))
        if re.search(rb"[A-Za-z]:\\Users\\|/Users/|/home/", package_bytes):
            fail("demo DOCX contains an absolute local user path")

    pdf = (demo / "CNS-Skills-synthetic-manuscript-demo.pdf").read_bytes()
    if not pdf.startswith(b"%PDF-"):
        fail("demo PDF does not have a valid PDF header")
    preview = (demo / "demo-preview.png").read_bytes()
    if not preview.startswith(b"\x89PNG\r\n\x1a\n"):
        fail("demo preview does not have a valid PNG header")

    for report in (demo / "reports").glob("*.json"):
        json.loads(report.read_text(encoding="utf-8"))


def main() -> int:
    try:
        validate_required_files()
        validate_local_links()
        validate_corpus()
        validate_public_counts()
        validate_demo_package()
    except (AssertionError, csv.Error, json.JSONDecodeError, OSError, zipfile.BadZipFile) as exc:
        print(f"public release asset check failed: {exc}", file=sys.stderr)
        return 1
    print("PASS: public links, proof counts, 600-record corpus, and synthetic demo assets are consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
