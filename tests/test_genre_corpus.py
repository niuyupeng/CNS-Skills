from __future__ import annotations

import csv
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "research" / "genre-corpus-2026"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


class GenreCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.paths = {
            "reviews": CORPUS / "reviews" / "reviews_manifest_200.csv",
            "articles": CORPUS / "articles" / "articles_manifest_200.csv",
            "conferences": CORPUS
            / "conferences"
            / "conference_manifest_200.csv",
        }
        cls.manifests = {
            name: read_csv(path) for name, path in cls.paths.items()
        }

    def test_each_stratum_has_exactly_200_unique_records(self) -> None:
        for name, (_, rows) in self.manifests.items():
            with self.subTest(stratum=name):
                self.assertEqual(len(rows), 200)
                corpus_ids = [row["corpus_id"] for row in rows]
                self.assertTrue(all(corpus_ids))
                self.assertEqual(len(set(corpus_ids)), 200)

        reviews = self.manifests["reviews"][1]
        self.assertEqual(len({row["persistent_id"] for row in reviews}), 200)

        articles = self.manifests["articles"][1]
        self.assertEqual(len({row["doi"] for row in articles}), 200)

        conferences = self.manifests["conferences"][1]
        self.assertEqual(len({row["paper_id"] for row in conferences}), 200)
        self.assertEqual(len({row["canonical_url"] for row in conferences}), 200)

    def test_actual_analysis_levels_are_locked(self) -> None:
        reviews = self.manifests["reviews"][1]
        self.assertEqual(
            Counter(row["actual_analysis_text_level"] for row in reviews),
            Counter({"full_text_xml": 42, "abstract": 157, "title": 1}),
        )

        articles = self.manifests["articles"][1]
        self.assertEqual(
            Counter(row["analysis_level"] for row in articles),
            Counter({"title_plus_pubmed_abstract_plus_pmc_jats_full_text": 200}),
        )

        conferences = self.manifests["conferences"][1]
        self.assertEqual(
            Counter(row["analysis_text_level"] for row in conferences),
            Counter({"full_text_extracted": 195, "abstract_only": 5}),
        )

    def test_conference_sample_is_balanced_and_from_2025(self) -> None:
        rows = self.manifests["conferences"][1]
        self.assertEqual(
            Counter(row["venue"] for row in rows),
            Counter({
                "AAAI": 40,
                "CVPR": 40,
                "NeurIPS": 40,
                "ICML": 40,
                "ICLR": 40,
            }),
        )
        self.assertEqual({row["year"] for row in rows}, {"2025"})
        self.assertTrue(all(row["abstract_word_count"] for row in rows))

    def test_public_manifests_do_not_redistribute_source_prose(self) -> None:
        forbidden_columns = {
            "abstract",
            "abstract_text",
            "article_text",
            "body_text",
            "extracted_text",
            "full_text",
            "full_text_text",
            "jats_xml",
            "pdf_text",
        }
        for name, (headers, _) in self.manifests.items():
            with self.subTest(stratum=name):
                self.assertTrue(forbidden_columns.isdisjoint(headers))

        public_files = [
            path
            for path in CORPUS.rglob("*")
            if path.is_file() and "work" not in path.relative_to(CORPUS).parts
        ]
        self.assertFalse(
            [path for path in public_files if path.suffix.lower() in {".pdf", ".html", ".xml", ".txt"}]
        )

    def test_each_stratum_has_metrics_findings_and_provenance(self) -> None:
        expected = {
            "reviews": ("reviews_metrics.json", "reviews_findings.md"),
            "articles": ("articles_metrics.json", "articles_findings.md"),
            "conferences": ("conference_metrics.json", "conference_findings.md"),
        }
        for name, (metrics_name, findings_name) in expected.items():
            folder = CORPUS / name
            with self.subTest(stratum=name):
                metrics_path = folder / metrics_name
                self.assertTrue(metrics_path.is_file())
                self.assertTrue((folder / findings_name).is_file())
                self.assertTrue((folder / "provenance.md").is_file())
                with metrics_path.open(encoding="utf-8") as handle:
                    self.assertIsInstance(json.load(handle), dict)


if __name__ == "__main__":
    unittest.main()
