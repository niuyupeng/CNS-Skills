from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class GenreModeRoutingTests(unittest.TestCase):
    def test_root_skill_routes_three_primary_genres(self):
        skill = read("SKILL.md")
        for reference in (
            "references/review-visual-architecture.md",
            "references/original-research-article-mode.md",
            "references/leading-conference-paper-mode.md",
        ):
            self.assertIn(reference, skill)

    def test_review_mode_treats_counts_as_constraints(self):
        text = read("references/review-visual-architecture.md")
        self.assertIn("page-budget constraint", text)
        self.assertIn("not publisher rules or acceptance predictors", text)
        self.assertRegex(text, re.compile(r"no more than seven.*display items", re.I | re.S))

    def test_review_mode_separates_figures_tables_and_boxes_by_job(self):
        text = read("references/review-visual-architecture.md")
        self.assertIn("Use a **figure**", text)
        self.assertIn("Use a **table**", text)
        self.assertIn("Use a **box**", text)
        self.assertIn("Frankenfigure", text)

    def test_original_article_mode_is_inference_led(self):
        text = read("references/original-research-article-mode.md")
        self.assertIn("Order Results by this inference chain", text)
        self.assertIn("not a mandatory five-figure template", text)
        self.assertIn("independent experimental or sampling unit", text)

    def test_conference_mode_locks_year_track_and_phase(self):
        text = read("references/leading-conference-paper-mode.md")
        self.assertIn("year, track, submission", text)
        self.assertIn("Do not assign a universal figure or table count", text)
        self.assertIn("reviewers are not required to read", text)

    def test_conference_mode_requires_both_ai_and_science_layers(self):
        text = read("references/leading-conference-paper-mode.md")
        self.assertIn("algorithmic layer", text)
        self.assertIn("scientific layer", text)
        self.assertIn("benchmark gain does not by itself", text)

    def test_nature_review_limit_is_not_globalized(self):
        text = read("references/visual-production.md")
        self.assertIn("no more than seven main-text display items", text)
        self.assertIn("provides no universal figure-count rule", text)


if __name__ == "__main__":
    unittest.main()
