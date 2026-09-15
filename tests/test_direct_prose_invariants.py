"""Token-level safeguards for a direct-writing pass, not a prose-quality score.

Semantic behavior is evaluated separately using the synthetic forward cases.
The last test deliberately shows why a clean invariant check needs human review.
"""

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "direct_prose_invariants", ROOT / "scripts" / "check_invariants.py"
)
invariants = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(invariants)


class DirectProseInvariantTests(unittest.TestCase):
    def compare(self, source, revised, protected=()):
        return invariants.compare(
            invariants.extract(source, list(protected)),
            invariants.extract(revised, list(protected)),
        )

    def test_cutting_empty_framing_preserves_measurements(self):
        result = self.compare(
            "It is important to note that after 24 h at 37 °C, A retained 62% [8].",
            "After 24 h at 37 °C, A retained 62% [8].",
        )
        self.assertEqual(result["status"], "clean")

    def test_edit_cannot_silently_change_assay_conditions(self):
        result = self.compare("At 37 °C for 24 h [8].", "At 25 °C for 24 h [8].")
        self.assertEqual(result["categories"]["quantities"]["status"], "changed")

    def test_citation_removal_is_reported(self):
        result = self.compare("The signal decreased [7].", "The signal decreased.")
        self.assertEqual(result["categories"]["bracket_citations"]["status"], "changed")

    def test_locked_chinese_uncertainty_survives_trimming(self):
        source = "需要指出的是，处理可能降低黏附，但尚不能排除粗糙度影响[7]。"
        revised = "处理降低黏附，且排除了粗糙度影响[7]。"
        result = self.compare(source, revised, ["可能", "尚不能排除"])
        self.assertEqual(result["categories"]["protected_tokens"]["status"], "changed")

    def test_clean_tokens_do_not_prove_semantic_equivalence(self):
        result = self.compare(
            "The treatment did not improve strength [6].",
            "The treatment improved strength [6].",
        )
        self.assertEqual(result["status"], "clean")
        # A contextual scientific reviewer must reject this polarity reversal.


if __name__ == "__main__":
    unittest.main()
