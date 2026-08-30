import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("title_audit", ROOT / "scripts" / "title_audit.py")
title_audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(title_audit)


class TitleAuditTests(unittest.TestCase):
    def test_current_long_title_exceeds_nature_snapshot(self):
        item = title_audit.analyze_title(
            "AI-Guided Biomaterials Design: Matching Models to Data, Experiments, and Validation",
            target="nature",
            article_type="review",
            keywords=["AI-Guided Biomaterials Design"],
            allowed_acronyms=["AI"],
            max_characters=None,
        )
        self.assertEqual(item["character_count"], 83)
        self.assertEqual(item["objective_failures"], ["character_count_exceeds_limit:83>75"])

    def test_compact_candidate_passes_objective_nature_length(self):
        item = title_audit.analyze_title(
            "Choosing Models for AI-Guided Biomaterials Design",
            target="nature",
            article_type="review",
            keywords=["AI-Guided", "Biomaterials Design"],
            allowed_acronyms=["AI"],
            max_characters=None,
        )
        self.assertEqual(item["character_count"], 49)
        self.assertFalse(item["objective_failures"])
        self.assertTrue(all(row["present"] for row in item["keyword_coverage"]))

    def test_generic_and_hype_patterns_are_explainable_cautions(self):
        item = title_audit.analyze_title(
            "A Comprehensive Review of Revolutionary Biomaterials: Challenges and Opportunities",
            target="unspecified",
            article_type="review",
            keywords=[],
            allowed_acronyms=[],
            max_characters=None,
        )
        self.assertIn("a_review_of", item["generic_formula_hits"])
        self.assertIn("challenges_opportunities", item["generic_formula_hits"])
        self.assertIn("revolutionary", item["hype_hits"])

    def test_subtitle_overlap_flags_repetition(self):
        overlap = title_audit.subtitle_overlap("Biomaterials Design: Design of Biomaterials")
        self.assertIsNotNone(overlap)
        assert overlap is not None
        self.assertTrue(overlap["possible_redundancy"])

    def test_corpus_summary_detects_duplicate_doi_and_does_not_need_abstracts(self):
        rows = [
            {"title": "One title", "journal": "Nature", "year": "2025", "doi": "10.1/a", "article_type": "review"},
            {"title": "Second title", "journal": "Science", "year": "2026", "doi": "10.1/a", "article_type": "article"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "corpus.csv"
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            summary = title_audit.summarize_corpus(path)
        self.assertEqual(summary["records"], 2)
        self.assertEqual(summary["duplicate_dois"], ["10.1/a"])
        self.assertEqual(summary["duplicate_stable_ids"], ["10.1/a"])
        self.assertFalse(summary["stores_abstract_or_full_text"])

    def test_conference_records_can_use_official_stable_ids_without_dois(self):
        rows = [
            {
                "title": "A conference title",
                "venue": "ICLR",
                "venue_type": "conference",
                "year": "2025",
                "stable_id": "iclr-2025-abc",
                "doi": "",
                "article_type": "Conference paper",
            },
            {
                "title": "A journal title",
                "venue": "Nature",
                "venue_type": "journal",
                "year": "2025",
                "stable_id": "10.1/example",
                "doi": "10.1/example",
                "article_type": "Article",
            },
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mixed.csv"
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            summary = title_audit.summarize_corpus(path)
        self.assertEqual(summary["unique_stable_ids"], 2)
        self.assertEqual(summary["unique_nonempty_dois"], 1)
        self.assertEqual(summary["venue_type_counts"], {"conference": 1, "journal": 1})

    def test_public_100_title_corpus_is_complete_unique_and_text_free(self):
        path = ROOT / "research" / "elite-venue-title-corpus-100.csv"
        self.assertTrue(path.is_file())
        summary = title_audit.summarize_corpus(path)
        self.assertEqual(summary["records"], 100)
        self.assertEqual(summary["unique_normalized_titles"], 100)
        self.assertEqual(summary["unique_stable_ids"], 100)
        self.assertFalse(summary["duplicate_normalized_titles"])
        self.assertFalse(summary["duplicate_stable_ids"])
        self.assertFalse(summary["duplicate_dois"])
        self.assertFalse(summary["stores_abstract_or_full_text"])

    def test_json_output_cannot_overwrite_file_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            title_file = root / "titles.txt"
            title_file.write_text("A title that must survive\n", encoding="utf-8")
            original_title_file = title_file.read_bytes()
            self.assertEqual(
                title_audit.main(["--title-file", str(title_file), "--json", str(title_file)]),
                1,
            )
            self.assertEqual(title_file.read_bytes(), original_title_file)

            corpus = root / "corpus.csv"
            corpus.write_text(
                "title,journal,year,doi\nOne title,Nature,2025,10.1/example\n",
                encoding="utf-8",
            )
            original_corpus = corpus.read_bytes()
            self.assertEqual(
                title_audit.main(["--corpus", str(corpus), "--json", str(corpus)]),
                1,
            )
            self.assertEqual(corpus.read_bytes(), original_corpus)


if __name__ == "__main__":
    unittest.main()
