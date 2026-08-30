#!/usr/bin/env python3
"""Reproduce the frozen synthetic dataset and its toy retrospective ranking.

This script uses only the Python standard library. It does not simulate real
patients, animals, materials, or experiments. The values are deterministic and
exist only to demonstrate CNS Skills manuscript and audit behavior.
"""

from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "synthetic_data.csv"
HOLDOUT = {4, 7, 10, 13, 16, 18}
FEATURES = ("crosslinker_pct", "peptide_mg_ml", "porogen_fraction")


def generated_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index in range(1, 19):
        crosslinker = round(0.8 + ((index * 7) % 11) * 0.12, 2)
        peptide = round(((index * 5) % 9) * 0.20, 2)
        porogen = round(((index * 3) % 7) * 0.08, 2)
        swelling = round(
            5.2 - 0.9 * crosslinker + 0.55 * porogen + ((index % 3) - 1) * 0.05,
            2,
        )
        reduction = round(
            max(
                0.0,
                min(
                    95.0,
                    18
                    + 38 * peptide
                    + 5 * porogen
                    - 1.5 * crosslinker
                    + ((index % 4) - 1.5) * 1.1,
                ),
            ),
            1,
        )
        viability = round(
            max(
                0.0,
                min(
                    100.0,
                    99
                    - 5 * peptide
                    - 2.2 * porogen
                    - 0.5 * crosslinker
                    + ((index % 5) - 2) * 0.6,
                ),
            ),
            1,
        )
        rows.append(
            {
                "formulation_id": f"H-{index:02d}",
                "crosslinker_pct": f"{crosslinker:.2f}",
                "peptide_mg_ml": f"{peptide:.2f}",
                "porogen_fraction": f"{porogen:.2f}",
                "swelling_ratio": f"{swelling:.2f}",
                "bacterial_reduction_pct": f"{reduction:.1f}",
                "fibroblast_viability_pct": f"{viability:.1f}",
                "split": "holdout" if index in HOLDOUT else "training",
                "independent_batches": "1",
                "technical_wells_per_endpoint": "3",
            }
        )
    return rows


def csv_text(rows: list[dict[str, str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().replace("\r\n", "\n")


def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]
    size = len(augmented)
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        if abs(divisor) < 1e-12:
            raise ValueError("singular synthetic design matrix")
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                current - factor * reference
                for current, reference in zip(augmented[row], augmented[column])
            ]
    return [row[-1] for row in augmented]


def ridge_coefficients(
    rows: list[dict[str, str]], target: str, alpha: float = 1.0
) -> list[float]:
    design = [[1.0, *(float(row[name]) for name in FEATURES)] for row in rows]
    outcomes = [float(row[target]) for row in rows]
    width = len(design[0])
    gram = [
        [sum(row[left] * row[right] for row in design) for right in range(width)]
        for left in range(width)
    ]
    for index in range(1, width):
        gram[index][index] += alpha
    rhs = [sum(row[index] * value for row, value in zip(design, outcomes)) for index in range(width)]
    return solve(gram, rhs)


def predict(row: dict[str, str], coefficients: list[float]) -> float:
    values = [1.0, *(float(row[name]) for name in FEATURES)]
    return sum(value * coefficient for value, coefficient in zip(values, coefficients))


def retrospective_ranking(rows: list[dict[str, str]]) -> list[dict[str, float | str]]:
    training = [row for row in rows if row["split"] == "training"]
    holdout = [row for row in rows if row["split"] == "holdout"]
    reduction_model = ridge_coefficients(training, "bacterial_reduction_pct")
    viability_model = ridge_coefficients(training, "fibroblast_viability_pct")
    ranked = []
    for row in holdout:
        predicted_reduction = predict(row, reduction_model)
        predicted_viability = predict(row, viability_model)
        ranked.append(
            {
                "formulation_id": row["formulation_id"],
                "predicted_reduction_pct": predicted_reduction,
                "predicted_viability_pct": predicted_viability,
                "eligible": "yes" if predicted_viability >= 85.0 else "no",
            }
        )
    return sorted(
        ranked,
        key=lambda row: (
            row["eligible"] == "yes",
            float(row["predicted_reduction_pct"]),
            float(row["predicted_viability_pct"]),
        ),
        reverse=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that synthetic_data.csv matches the deterministic generator",
    )
    args = parser.parse_args()

    rows = generated_rows()
    expected = csv_text(rows)
    if args.check:
        observed = DATA_PATH.read_text(encoding="utf-8").replace("\r\n", "\n")
        if observed != expected:
            print("FAIL: synthetic_data.csv differs from the deterministic generator")
            return 1
        print("PASS: synthetic_data.csv matches the deterministic generator (18 rows)")

    ranking = retrospective_ranking(rows)
    print("Retrospective holdout ranking; viability eligibility threshold = 85%")
    for row in ranking:
        print(
            f"{row['formulation_id']}: predicted reduction "
            f"{float(row['predicted_reduction_pct']):.1f}%, predicted viability "
            f"{float(row['predicted_viability_pct']):.1f}%, eligible={row['eligible']}"
        )
    print("No prospective experiment was selected or run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
