import csv
import importlib.util
import json
import os
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "venue_corpus_analyzer", ROOT / "scripts" / "venue_corpus_analyzer.py"
)
venue = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(venue)


class VenueCorpusAnalyzerTests(unittest.TestCase):
    def test_reconstruct_abstract_uses_positions(self):
        index = {"We": [0], "show": [1], "robust": [2], "results.": [3]}
        self.assertEqual(venue.reconstruct_abstract(index), "We show robust results.")

    def test_reconstruct_abstract_tolerates_legacy_position_gap(self):
        self.assertEqual(venue.reconstruct_abstract({"One": [0], "three": [2]}), "One three")

    def test_sentence_moves_detect_contribution_and_implication(self):
        self.assertEqual(
            venue.sentence_move("Here, we develop a calibrated model for this task."),
            "contribution",
        )
        self.assertEqual(
            venue.sentence_move("Our findings may enable safer prospective evaluation."),
            "implication",
        )

    def test_summary_contains_aggregate_metrics_but_no_abstract(self):
        record = {
            "id": "https://openalex.org/W1",
            "doi": "https://doi.org/10.1/example",
            "title": "A calibrated model",
            "publication_year": 2026,
            "abstract_inverted_index": {
                "Here,": [0],
                "we": [1],
                "develop": [2],
                "a": [3, 7],
                "model.": [4],
                "Results": [5],
                "show": [6],
                "12%": [8],
                "gain.": [9],
            },
        }
        config = venue.VENUES["cell"]
        aggregate, manifest = venue.summarize_venue([record], config)
        self.assertEqual(aggregate["sampled_abstracts"], 1)
        self.assertEqual(aggregate["abstract"]["numeric_evidence_percent"], 100.0)
        self.assertEqual(manifest[0]["abstract_words"], 10)
        self.assertNotIn("abstract", manifest[0])
        self.assertEqual(len(manifest[0]["abstract_sha256"]), 64)
        self.assertIn("move_contribution", manifest[0])

    def test_query_is_source_date_and_abstract_filtered(self):
        url = venue.build_query(venue.VENUES["aaai"], 40, 7)
        self.assertIn("S4210191458", url)
        self.assertIn("has_abstract%3Atrue", url)
        self.assertIn("sample=40", url)
        self.assertIn("seed=7", url)

    def test_query_rejects_deprecated_page_sizes(self):
        with self.assertRaises(ValueError):
            venue.build_query(venue.VENUES["aaai"], 101, 7)

    def test_csv_formula_prefix_is_neutralized(self):
        self.assertEqual(venue.csv_safe("=1+1"), "'=1+1")
        self.assertEqual(venue.csv_safe("  @cmd"), "'  @cmd")
        self.assertEqual(venue.csv_safe("A normal title"), "A normal title")

    def test_generation_timestamp_respects_source_date_epoch(self):
        with mock.patch.dict(os.environ, {"SOURCE_DATE_EPOCH": "0"}):
            self.assertEqual(venue.generation_timestamp(), "1970-01-01T00:00:00+00:00")

    def test_repository_corpus_artifacts_are_complete_and_text_free(self):
        aggregate = json.loads(
            (ROOT / "research" / "venue-corpus-aggregate.json").read_text(encoding="utf-8")
        )
        with (ROOT / "research" / "venue-corpus-manifest.csv").open(
            encoding="utf-8-sig", newline=""
        ) as stream:
            reader = csv.DictReader(stream)
            rows = list(reader)
            fields = set(reader.fieldnames or [])
        self.assertEqual(aggregate["total_analyzed_abstracts"], 320)
        self.assertEqual(len(rows), 320)
        self.assertFalse({"abstract", "abstract_text", "full_text"} & fields)
        self.assertIn("abstract_sha256", fields)


if __name__ == "__main__":
    unittest.main()
