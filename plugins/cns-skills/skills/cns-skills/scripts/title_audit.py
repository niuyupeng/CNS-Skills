#!/usr/bin/env python3
"""Audit scientific title candidates and summarize a title-metadata corpus.

The diagnostics are deliberately transparent. They report observable features,
venue-rule snapshots, search-term coverage, and phrases that require human
review; they do not predict acceptance or assign a universal title-quality
score.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Optional


VERSION = "0.8.0"
POLICY_SNAPSHOT = "2026-08-30"

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
ACRONYM_RE = re.compile(r"(?<![A-Za-z0-9])(?:[A-Z]{2,}[A-Z0-9]*|[A-Z]\d[A-Z0-9]*)(?![A-Za-z0-9])")

GENERIC_PATTERNS = {
    "a_review_of": re.compile(r"\ba\s+(?:systematic\s+|comprehensive\s+)?review\s+of\b", re.I),
    "recent_advances": re.compile(r"\brecent\s+advances?\b", re.I),
    "advances_challenges": re.compile(r"\badvances?\b.*\bchallenges?\b", re.I),
    "challenges_opportunities": re.compile(r"\bchallenges?\b.*\bopportunit(?:y|ies)\b", re.I),
    "future_perspectives": re.compile(r"\bfuture\s+(?:directions?|perspectives?|prospects?)\b", re.I),
    "progress_prospects": re.compile(r"\bprogress\b.*\bprospects?\b", re.I),
}

HYPE_PATTERNS = {
    "breakthrough": re.compile(r"\bbreakthrough\b", re.I),
    "definitive": re.compile(r"\bdefinitive\b", re.I),
    "first_ever": re.compile(r"\bfirst[- ]ever\b", re.I),
    "game_changing": re.compile(r"\bgame[- ]changing\b", re.I),
    "groundbreaking": re.compile(r"\bgroundbreaking\b", re.I),
    "revolutionary": re.compile(r"\brevolutionary\b", re.I),
    "transformative": re.compile(r"\btransformative\b", re.I),
    "unprecedented": re.compile(r"\bunprecedented\b", re.I),
    "ultimate": re.compile(r"\bultimate\b", re.I),
}

CLAIM_RISK_PATTERNS = {
    "clinical_translation": re.compile(r"\bclinical\s+translation\b", re.I),
    "generalizable": re.compile(r"\bgenerali[sz]able\b", re.I),
    "mechanism": re.compile(r"\bmechanis(?:m|tic)\b", re.I),
    "safe_or_effective": re.compile(r"\b(?:safe|safety|effective|efficacy)\b", re.I),
}

TARGET_SNAPSHOTS = {
    "nature": {
        "max_characters": 75,
        "note": "Nature flagship initial-submission snapshot; verify the live article-type instructions.",
    },
    "science": {
        "max_characters": 96,
        "note": "Science flagship initial-manuscript snapshot; verify the live article-type instructions.",
    },
    "cell": {
        "max_characters": None,
        "note": "No cross-article-type hard limit is encoded; verify the live Cell article-type instructions.",
    },
    "top-conference": {
        "max_characters": None,
        "note": "Conference title rules and proceedings metadata vary by venue and year.",
    },
    "unspecified": {
        "max_characters": None,
        "note": "No venue-specific title limit supplied.",
    },
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "from",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
}


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def pattern_hits(text: str, patterns: dict[str, re.Pattern[str]]) -> list[str]:
    return [name for name, pattern in patterns.items() if pattern.search(text)]


def semantic_tokens(text: str) -> set[str]:
    return {token.casefold() for token in words(text) if token.casefold() not in STOPWORDS}


def subtitle_overlap(title: str) -> Optional[dict[str, Any]]:
    if ":" not in title:
        return None
    main, subtitle = title.split(":", 1)
    main_tokens = semantic_tokens(main)
    subtitle_tokens = semantic_tokens(subtitle)
    if not main_tokens or not subtitle_tokens:
        return None
    shared = sorted(main_tokens & subtitle_tokens)
    ratio = len(shared) / min(len(main_tokens), len(subtitle_tokens))
    return {
        "shared_content_words": shared,
        "overlap_ratio": round(ratio, 3),
        "possible_redundancy": ratio >= 0.5,
    }


def analyze_title(
    title: str,
    target: str,
    article_type: str,
    keywords: Iterable[str],
    allowed_acronyms: Iterable[str],
    max_characters: Optional[int],
) -> dict[str, Any]:
    clean = " ".join(title.split())
    allowed = {item.upper() for item in allowed_acronyms}
    acronyms = sorted({item for item in ACRONYM_RE.findall(clean) if item.upper() not in allowed})
    keyword_rows = [
        {"keyword": keyword, "present": keyword.casefold() in clean.casefold()}
        for keyword in keywords
    ]

    snapshot = TARGET_SNAPSHOTS[target]
    effective_max = max_characters if max_characters is not None else snapshot["max_characters"]
    objective_failures: list[str] = []
    cautions: list[str] = []
    if effective_max is not None and len(clean) > effective_max:
        objective_failures.append(
            f"character_count_exceeds_limit:{len(clean)}>{effective_max}"
        )
    if acronyms:
        cautions.append("unapproved_acronyms")
    if clean.count(":") > 1:
        cautions.append("multiple_colons")
    if clean.endswith("."):
        cautions.append("terminal_period")
    if len(words(clean)) > 20:
        cautions.append("long_title_over_20_words")

    generic = pattern_hits(clean, GENERIC_PATTERNS)
    hype = pattern_hits(clean, HYPE_PATTERNS)
    claim_risks = pattern_hits(clean, CLAIM_RISK_PATTERNS)
    if generic:
        cautions.append("generic_review_formula")
    if hype:
        cautions.append("promotional_or_priority_language")
    if claim_risks:
        cautions.append("claim_terms_require_manuscript_evidence")
    if any(not item["present"] for item in keyword_rows):
        cautions.append("requested_keyword_missing")

    overlap = subtitle_overlap(clean)
    if overlap and overlap["possible_redundancy"]:
        cautions.append("main_subtitle_content_overlap")

    return {
        "title": clean,
        "article_type": article_type,
        "target": target,
        "character_count": len(clean),
        "word_count": len(words(clean)),
        "has_colon": ":" in clean,
        "has_question": "?" in clean,
        "acronyms_requiring_review": acronyms,
        "keyword_coverage": keyword_rows,
        "generic_formula_hits": generic,
        "hype_hits": hype,
        "claim_risk_hits": claim_risks,
        "subtitle_overlap": overlap,
        "target_rule": {
            "policy_snapshot": POLICY_SNAPSHOT,
            "max_characters": effective_max,
            "source": "user override" if max_characters is not None else "bundled advisory snapshot",
            "note": snapshot["note"],
        },
        "objective_failures": objective_failures,
        "cautions": sorted(set(cautions)),
        "manual_checks": [
            "Does the title expose the scientific object and the manuscript's actual contribution or organizing lens?",
            "Does every conclusion-like term remain inside the supplied evidence boundary?",
            "Does the title match the abstract, conclusion, article type, and target audience?",
            "Have the exact live venue and article-type instructions been verified?",
        ],
    }


def percentile(values: list[int], fraction: float) -> float:
    if not values:
        raise ValueError("cannot summarize an empty value list")
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def normalized_title(text: str) -> str:
    return " ".join(words(text.casefold()))


def title_feature_summary(titles: list[str]) -> dict[str, Any]:
    """Return descriptive title features for one explicitly defined stratum."""
    word_counts = [len(words(title)) for title in titles]
    character_counts = [len(title) for title in titles]
    return {
        "records": len(titles),
        "title_words": {
            "median": statistics.median(word_counts),
            "q1": round(percentile(word_counts, 0.25), 2),
            "q3": round(percentile(word_counts, 0.75), 2),
        },
        "title_characters": {
            "median": statistics.median(character_counts),
            "q1": round(percentile(character_counts, 0.25), 2),
            "q3": round(percentile(character_counts, 0.75), 2),
        },
        "feature_percent": {
            "colon": round(100 * sum(":" in title for title in titles) / len(titles), 1),
            "question": round(100 * sum("?" in title for title in titles) / len(titles), 1),
            "acronym": round(100 * sum(bool(ACRONYM_RE.search(title)) for title in titles) / len(titles), 1),
            "generic_review_formula": round(
                100 * sum(bool(pattern_hits(title, GENERIC_PATTERNS)) for title in titles) / len(titles), 1
            ),
        },
    }


def summarize_corpus(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        fields = set(reader.fieldnames or [])
    required = {"title", "year"}
    missing = sorted(required - fields)
    if missing:
        raise ValueError(f"corpus is missing required fields: {', '.join(missing)}")
    if not ({"venue", "journal"} & fields):
        raise ValueError("corpus requires either a venue or journal field")
    if not ({"stable_id", "doi"} & fields):
        raise ValueError("corpus requires either a stable_id or doi field")
    if not rows:
        raise ValueError("corpus contains no records")

    titles = [" ".join(str(row.get("title", "")).split()) for row in rows]
    if any(not title for title in titles):
        raise ValueError("every corpus record requires a nonempty title")
    normalized = [normalized_title(title) for title in titles]
    dois = [str(row.get("doi", "")).strip().casefold() for row in rows if str(row.get("doi", "")).strip()]
    stable_ids = [
        (str(row.get("stable_id", "")).strip() or str(row.get("doi", "")).strip()).casefold()
        for row in rows
    ]
    if any(not stable_id for stable_id in stable_ids):
        raise ValueError("every corpus record requires a stable_id or DOI")
    title_counts = Counter(normalized)
    doi_counts = Counter(dois)
    stable_id_counts = Counter(stable_ids)
    article_field = "article_type" if "article_type" in fields else "genre_role" if "genre_role" in fields else None
    venue_field = "venue" if "venue" in fields else "journal"
    venue_type_field = "venue_type" if "venue_type" in fields else None

    strata: dict[str, dict[str, Any]] = {}
    if venue_type_field:
        grouped: dict[str, list[str]] = {}
        for row, title in zip(rows, titles):
            key = str(row.get(venue_type_field, "")).strip() or "unspecified"
            grouped.setdefault(key, []).append(title)
        strata = {key: title_feature_summary(value) for key, value in sorted(grouped.items())}

    overall = title_feature_summary(titles)

    return {
        "source_file": path.name,
        "records": len(rows),
        "unique_normalized_titles": len(set(normalized)),
        "unique_stable_ids": len(set(stable_ids)),
        "unique_nonempty_dois": len(set(dois)),
        "duplicate_normalized_titles": sorted(title for title, count in title_counts.items() if count > 1),
        "duplicate_stable_ids": sorted(stable_id for stable_id, count in stable_id_counts.items() if count > 1),
        "duplicate_dois": sorted(doi for doi, count in doi_counts.items() if count > 1),
        "years": {
            "minimum": min(int(row["year"]) for row in rows),
            "maximum": max(int(row["year"]) for row in rows),
        },
        "title_words": overall["title_words"],
        "title_characters": overall["title_characters"],
        "feature_percent": overall["feature_percent"],
        "venue_counts": dict(sorted(Counter(row[venue_field] for row in rows).items())),
        "venue_family_counts": (
            dict(sorted(Counter(row.get("venue_family", "") or "unspecified" for row in rows).items()))
            if "venue_family" in fields
            else {"not_provided": len(rows)}
        ),
        "venue_type_counts": (
            dict(sorted(Counter(row.get(venue_type_field, "") or "unspecified" for row in rows).items()))
            if venue_type_field
            else {"not_provided": len(rows)}
        ),
        "title_features_by_venue_type": strata,
        "article_type_counts": (
            dict(sorted(Counter(row.get(article_field, "") or "unspecified" for row in rows).items()))
            if article_field
            else {"not_provided": len(rows)}
        ),
        "stored_fields": sorted(fields),
        "stores_abstract_or_full_text": bool({"abstract", "abstract_text", "full_text"} & fields),
    }


def read_title_file(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("titles", nargs="*", help="one or more quoted title candidates")
    parser.add_argument("--title-file", type=Path, help="UTF-8 file with one title candidate per line")
    parser.add_argument("--corpus", type=Path, help="CSV title-metadata corpus to summarize")
    parser.add_argument(
        "--target",
        choices=sorted(TARGET_SNAPSHOTS),
        default="unspecified",
        help="advisory venue-family rule snapshot",
    )
    parser.add_argument("--article-type", default="unspecified")
    parser.add_argument("--keyword", action="append", default=[], help="required search term; repeat as needed")
    parser.add_argument("--allow-acronym", action="append", default=[], help="approved acronym; repeat as needed")
    parser.add_argument("--max-characters", type=int, help="current user-verified venue limit")
    parser.add_argument("--json", type=Path, help="write the full report as UTF-8 JSON")
    parser.add_argument("--strict", action="store_true", help="return 2 for objective candidate failures or corpus duplicates")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser.parse_args(argv)


def validate_output_path(args: argparse.Namespace) -> None:
    """Refuse to replace either file input with the JSON report."""
    if args.json is None:
        return
    output = args.json.resolve()
    protected = [path.resolve() for path in (args.title_file, args.corpus) if path is not None]
    if output in protected:
        raise ValueError("--json output cannot overwrite --title-file or --corpus input")


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    title_candidates = list(args.titles)
    if args.title_file:
        title_candidates.extend(read_title_file(args.title_file))
    if not title_candidates and args.corpus is None:
        raise ValueError("provide at least one title, --title-file, or --corpus")
    analyses = [
        analyze_title(
            title=title,
            target=args.target,
            article_type=args.article_type,
            keywords=args.keyword,
            allowed_acronyms=args.allow_acronym,
            max_characters=args.max_characters,
        )
        for title in title_candidates
    ]
    report: dict[str, Any] = {
        "tool": "CNS scientific title audit",
        "version": VERSION,
        "policy_snapshot": POLICY_SNAPSHOT,
        "candidate_analyses": analyses,
        "limitations": [
            "Observable title features do not establish scientific quality or acceptance probability.",
            "Corpus frequencies are descriptive and must not be converted into copyable formulas.",
            "Final title selection requires the manuscript's central contribution, evidence boundary, article type, and live venue rules.",
        ],
    }
    if args.corpus:
        report["corpus_summary"] = summarize_corpus(args.corpus)
    return report


def print_report(report: dict[str, Any]) -> None:
    print(f"CNS scientific title audit v{report['version']}")
    for index, item in enumerate(report["candidate_analyses"], 1):
        print(f"[{index}] {item['title']}")
        print(
            f"    {item['character_count']} characters | {item['word_count']} words | "
            f"target={item['target']} | article_type={item['article_type']}"
        )
        if item["objective_failures"]:
            print(f"    objective failures: {', '.join(item['objective_failures'])}")
        if item["cautions"]:
            print(f"    cautions: {', '.join(item['cautions'])}")
        else:
            print("    cautions: none from the transparent pattern checks")
    if "corpus_summary" in report:
        corpus = report["corpus_summary"]
        print(
            f"Corpus: {corpus['records']} records | "
            f"{corpus['unique_normalized_titles']} unique normalized titles | "
            f"{corpus['unique_stable_ids']} unique stable IDs | "
            f"{corpus['unique_nonempty_dois']} unique nonempty DOIs"
        )


def strict_failure(report: dict[str, Any]) -> bool:
    if any(item["objective_failures"] for item in report["candidate_analyses"]):
        return True
    corpus = report.get("corpus_summary")
    if corpus and (
        corpus["duplicate_normalized_titles"]
        or corpus["duplicate_stable_ids"]
        or corpus["duplicate_dois"]
    ):
        return True
    return False


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    try:
        validate_output_path(args)
        report = build_report(args)
    except (OSError, ValueError, csv.Error) as exc:
        print(f"title audit failed: {exc}", file=sys.stderr)
        return 1
    print_report(report)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {args.json}")
    return 2 if args.strict and strict_failure(report) else 0


if __name__ == "__main__":
    raise SystemExit(main())
