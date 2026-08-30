from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "review_search_audit_forward", ROOT / "scripts" / "review_search_audit.py"
)
review_search_audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(review_search_audit)


def load_cases(name: str) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in (ROOT / "evals" / name).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


CASES = load_cases("review-search-forward-cases.jsonl")
SECOND_ROUND_CASES = load_cases("review-search-second-round-cases.jsonl")
FINAL_ADVERSARIAL_CASES = load_cases("review-search-final-adversarial-cases.jsonl")
FOURTH_ROUND_CASES = load_cases("review-search-fourth-round-cases.jsonl")
FIFTH_ROUND_CASES = load_cases("review-search-fifth-round-cases.jsonl")
SIXTH_ROUND_CASES = load_cases("review-search-sixth-round-cases.jsonl")
ALL_CASES = (
    CASES
    + SECOND_ROUND_CASES
    + FINAL_ADVERSARIAL_CASES
    + FOURTH_ROUND_CASES
    + FIFTH_ROUND_CASES
    + SIXTH_ROUND_CASES
)

# Freeze the independent R3 holdout as sixteen distinct data-driven cases.
# These import-time guards do not inflate the reported unit-test count.
_r3_ids = [str(case["id"]) for case in FINAL_ADVERSARIAL_CASES]
if len(_r3_ids) != 16 or len(set(_r3_ids)) != 16:
    raise AssertionError("R3 must contain exactly 16 unique cases")
if sorted(int(case_id.split("_", 1)[0].split("-", 1)[1]) for case_id in _r3_ids) != list(
    range(1, 17)
):
    raise AssertionError("R3 case ordinals must cover R3-01 through R3-16")

# Freeze R4 independently so a truncated or duplicated holdout cannot still
# produce a deceptively green data-driven suite.
_r4_ids = [str(case["id"]) for case in FOURTH_ROUND_CASES]
if len(_r4_ids) != 16 or len(set(_r4_ids)) != 16:
    raise AssertionError("R4 must contain exactly 16 unique cases")
if sorted(case_id.split("_", 1)[0] for case_id in _r4_ids) != [
    f"R4-{ordinal:02d}" for ordinal in range(1, 17)
]:
    raise AssertionError("R4 case ordinals must cover R4-01 through R4-16")

_r5_ids = [str(case["id"]) for case in FIFTH_ROUND_CASES]
if len(_r5_ids) != 20 or len(set(_r5_ids)) != 20:
    raise AssertionError("R5 must contain exactly 20 unique cases")
if sorted(case_id.split("_", 1)[0] for case_id in _r5_ids) != [
    f"R5-{ordinal:02d}" for ordinal in range(1, 21)
]:
    raise AssertionError("R5 case ordinals must cover R5-01 through R5-20")

_r6_ids = [str(case["id"]) for case in SIXTH_ROUND_CASES]
if len(_r6_ids) != 12 or len(set(_r6_ids)) != 12:
    raise AssertionError("R6 must contain exactly 12 unique cases")
if sorted(case_id.split("_", 1)[0] for case_id in _r6_ids) != [
    f"R6-{ordinal:02d}" for ordinal in range(1, 13)
]:
    raise AssertionError("R6 case ordinals must cover R6-01 through R6-12")
if any(case.get("expected_strict_exit") not in {0, 3} for case in FIFTH_ROUND_CASES):
    raise AssertionError("every R5 case must freeze an expected strict exit of 0 or 3")
if any(case.get("expected_strict_exit") not in {0, 3} for case in SIXTH_ROUND_CASES):
    raise AssertionError("every R6 case must freeze an expected strict exit of 0 or 3")

_all_ids = [str(case["id"]) for case in ALL_CASES]
if len(_all_ids) != len(set(_all_ids)):
    raise AssertionError("review-search holdout IDs must be globally unique")

class ReviewSearchForwardCases(unittest.TestCase):
    def assert_case(self, case: dict[str, object]) -> None:
        report = review_search_audit.build_report(
            Path(str(case["id"]) + ".txt"), str(case["text"])
        )
        self.assertEqual(report["declared_review_type"], case["expected_declared_type"])
        self.assertEqual(report["disclosure_pattern"], case["expected_disclosure_pattern"])

        expected_evidence = case["expected_evidence"]
        assert isinstance(expected_evidence, dict)
        for key, expected in expected_evidence.items():
            if key == "selection":
                assert isinstance(expected, dict)
                for selection_key, selection_expected in expected.items():
                    self.assertEqual(
                        report["evidence"]["selection"][selection_key],
                        selection_expected,
                        f"{case['id']}: selection.{selection_key}",
                    )
            else:
                self.assertEqual(
                    report["evidence"].get(key), expected, f"{case['id']}: {key}"
                )

        if "expected_missing_systematic_elements" in case:
            self.assertEqual(
                report["missing_systematic_elements"],
                case["expected_missing_systematic_elements"],
                f"{case['id']}: missing_systematic_elements",
            )

        if "expected_diagnostics" in case:
            self.assertEqual(
                [
                    {"code": item["code"], "level": item["level"]}
                    for item in report["diagnostics"]
                ],
                case["expected_diagnostics"],
                f"{case['id']}: diagnostics",
            )
        else:
            self.assertEqual(
                [item["code"] for item in report["diagnostics"]],
                case["expected_diagnostic_codes"],
                f"{case['id']}: diagnostic codes",
            )

    def test_strict_mode_rejects_missing_query_and_bibliographic_deduplication(self):
        cases = {case["id"]: case for case in ALL_CASES}
        for case_id in (
            "H06_promised_supplement_systematic",
            "H21_domain_term_leakage",
            "R2-01_adjacent_domain_selection_leakage",
            "R2-08_under_preparation_supplement",
            "R3-05_same_paragraph_ts_domain_field_leakage",
            "R3-06_same_paragraph_clinical_record_screening_leakage",
            "R3-07_same_paragraph_instrument_record_dedup_leakage",
            "R3-10_supplement_slated_for_later_deposit",
            "R4-09_tx_assay_field_not_query",
            "R4-10_cross_sentence_patient_record_coreference",
            "R4-12_appendix_future_repository_deposit",
            "R4-13_supplement_explicitly_missing_package",
            "R5-01_chinese_semicolon_clinical_records",
            "R5-02_em_dash_polymer_library_subject",
            "R5-03_two_sentence_clinical_pronoun",
            "R5-11_mh_material_history_field_collision",
            "R5-12_title_abs_key_clinical_variable_collision",
            "R5-14_chinese_future_supplement",
            "R5-15_chinese_explicitly_missing_supplement",
            "R6-01_chinese_specimen_barcode_subject",
            "R6-06_ovid_suffix_rheometer_collision",
            "R6-09_cited_but_embargoed_appendix_missing",
        ):
            with self.subTest(case_id=case_id), tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "review.txt"
                path.write_text(str(cases[case_id]["text"]), encoding="utf-8")
                self.assertEqual(
                    review_search_audit.main([str(path), "--strict-systematic"]), 3
                )

    def test_strict_mode_accepts_structurally_complete_record(self):
        cases = {case["id"]: case for case in ALL_CASES}
        for case_id in (
            "H07_complete_systematic_no_methods_heading",
            "R3-01_chinese_systematic_evaluation_synonym",
            "R3-03_psycinfo_ebsco_tx_proximity_query",
            "R3-11_current_supplement_inverted_information_order",
            "R3-16_pubmed_majr_publication_type_fields",
            "R4-07_negated_narrative_then_final_systematic",
            "R4-08_scopus_field_syntax_in_next_sentence",
            "R4-11_attached_supplement_commands_current",
            "R5-04_two_sentence_bibliographic_pronoun_positive",
            "R5-05_table_title_not_self_type",
            "R5-06_chinese_guideline_name_not_self_type",
            "R5-07_chinese_superseded_plan_final_realist",
            "R5-08_superseded_scoping_final_living",
            "R5-09_mapping_review_complete_methods_outside_gate",
            "R5-10_realist_review_incomplete_outside_gate",
            "R5-13_chinese_current_supplement",
            "R5-16_ambiguous_cross_sentence_source_pronouns",
            "R5-17_explicit_two_sentence_source_coreference",
            "R5-18_chinese_two_sentence_source_roles",
            "R5-19_same_sentence_source_roles_control",
            "R5-20_chinese_natural_inventory_not_query",
            "R6-02_bibliographic_set_cross_paragraph_positive",
            "R6-03_external_editor_comment_not_self_type",
            "R6-04_cancelled_meta_final_critical_review",
            "R6-05_state_of_the_art_review_outside_gate",
            "R6-07_query_in_following_paragraph_positive",
            "R6-08_current_supplement_with_negated_future",
            "R6-10_author_maintained_zotero_collection",
            "R6-11_collective_secondary_source_roles_ambiguous",
            "R6-12_inventory_with_distinct_coverage_and_inference_limits",
        ):
            with self.subTest(case_id=case_id), tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "review.txt"
                path.write_text(str(cases[case_id]["text"]), encoding="utf-8")
                self.assertEqual(
                    review_search_audit.main([str(path), "--strict-systematic"]), 0
                )

    def test_structural_disclaimer_blocks_truth_and_reproducibility_inference(self):
        case = next(
            item
            for item in FOURTH_ROUND_CASES
            if item["id"] == "R4-11_attached_supplement_commands_current"
        )
        report = review_search_audit.build_report(
            Path(str(case["id"]) + ".txt"), str(case["text"])
        )
        self.assertEqual(
            report["disclosure_pattern"], "systematic_record_structurally_complete"
        )
        disclaimer = report["disclaimer"].casefold()
        for boundary in (
            "structural signals only",
            "zero strict-mode exit code is not an acceptance",
            "does not open cited supplements",
            "execute database queries",
            "validate deduplication and screening logs",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, disclaimer)

    def test_r5_strict_exit_codes_match_frozen_gold(self):
        for case in FIFTH_ROUND_CASES:
            with self.subTest(case_id=case["id"]), tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "review.txt"
                path.write_text(str(case["text"]), encoding="utf-8")
                # The CLI prints a human-readable report; suppress it here so a
                # failing subcase leaves the expected and actual exit codes as
                # the only relevant test output.
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
                    io.StringIO()
                ):
                    actual = review_search_audit.main(
                        [str(path), "--strict-systematic"]
                    )
                self.assertEqual(
                    actual,
                    case["expected_strict_exit"],
                    f"{case['id']}: strict exit",
                )

    def test_r6_strict_exit_codes_match_frozen_gold(self):
        for case in SIXTH_ROUND_CASES:
            with self.subTest(case_id=case["id"]), tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "review.txt"
                path.write_text(str(case["text"]), encoding="utf-8")
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
                    io.StringIO()
                ):
                    actual = review_search_audit.main(
                        [str(path), "--strict-systematic"]
                    )
                self.assertEqual(
                    actual,
                    case["expected_strict_exit"],
                    f"{case['id']}: strict exit",
                )


def _make_case_test(case: dict[str, object]):
    def test(self: ReviewSearchForwardCases) -> None:
        self.assert_case(case)

    test.__name__ = "test_" + str(case["id"]).lower()
    test.__doc__ = str(case["gold_reason"])
    return test


for _case in ALL_CASES:
    setattr(
        ReviewSearchForwardCases,
        "test_" + str(_case["id"]).lower(),
        _make_case_test(_case),
    )


if __name__ == "__main__":
    unittest.main()
