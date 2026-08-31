#!/usr/bin/env python3
"""Build or verify the generated cross-platform CNS Skills plugin payload.

The repository root remains the canonical standalone skill. The public plugin
marketplaces require the same skill under ``plugins/cns-skills/skills``. This
script makes that duplication mechanical and fails CI if the two copies drift.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "cns-skills"
PLUGIN_SKILL_ROOT = PLUGIN_ROOT / "skills" / "cns-skills"
TREE_PATHS = (Path("assets"), Path("references"))
FILE_PATHS = (
    Path("SKILL.md"),
    Path("agents/openai.yaml"),
    Path("scripts/cns_audit.py"),
    Path("scripts/check_crossrefs.py"),
    Path("scripts/check_invariants.py"),
    Path("scripts/review_citation_audit.py"),
    Path("scripts/review_search_audit.py"),
    Path("scripts/title_audit.py"),
    Path("scripts/venue_corpus_analyzer.py"),
    Path("scripts/visual_audit.py"),
    Path("scripts/figure_brief.py"),
    Path("scripts/render_concept_svg.py"),
)


def source_map() -> dict[Path, Path]:
    mapping = {relative: ROOT / relative for relative in FILE_PATHS}
    for tree in TREE_PATHS:
        for source in sorted((ROOT / tree).rglob("*")):
            if source.is_file() and "__pycache__" not in source.parts and source.suffix != ".pyc":
                mapping[source.relative_to(ROOT)] = source
    return mapping


def expected_destinations() -> dict[Path, Path]:
    return {PLUGIN_SKILL_ROOT / relative: source for relative, source in source_map().items()}


def write_bundle() -> None:
    expected = expected_destinations()
    PLUGIN_SKILL_ROOT.mkdir(parents=True, exist_ok=True)
    for destination, source in expected.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    for existing in sorted(PLUGIN_SKILL_ROOT.rglob("*"), reverse=True):
        if existing.is_file() and existing not in expected:
            existing.unlink()
        elif existing.is_dir() and not any(existing.iterdir()):
            existing.rmdir()

    shutil.copy2(ROOT / "LICENSE", PLUGIN_ROOT / "LICENSE")


def check_bundle() -> list[str]:
    errors: list[str] = []
    expected = expected_destinations()
    for destination, source in expected.items():
        if not destination.is_file():
            errors.append(f"missing generated file: {destination.relative_to(ROOT)}")
        elif destination.read_bytes() != source.read_bytes():
            errors.append(f"out-of-sync generated file: {destination.relative_to(ROOT)}")

    if PLUGIN_SKILL_ROOT.is_dir():
        for existing in PLUGIN_SKILL_ROOT.rglob("*"):
            if existing.is_file() and existing not in expected:
                errors.append(f"unexpected generated file: {existing.relative_to(ROOT)}")

    plugin_license = PLUGIN_ROOT / "LICENSE"
    if not plugin_license.is_file() or plugin_license.read_bytes() != (ROOT / "LICENSE").read_bytes():
        errors.append("plugin LICENSE is missing or out of sync")
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="regenerate the plugin skill payload")
    mode.add_argument("--check", action="store_true", help="fail if the generated payload has drifted")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.write:
        write_bundle()
    errors = check_bundle()
    if errors:
        print("Plugin bundle check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Plugin bundle is synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
