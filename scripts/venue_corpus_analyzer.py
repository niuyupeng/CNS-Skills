#!/usr/bin/env python3
"""Build a reproducible, aggregate writing profile for selected research venues.

The analyzer downloads OpenAlex metadata and abstract inverted indexes, reconstructs
abstracts in memory, and writes only aggregate statistics plus a metadata manifest.
It never writes abstract text. The output is descriptive evidence for editorial
judgment, not a template for imitating individual authors or venues.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from math import ceil
from pathlib import Path
from typing import Any, Iterable


VERSION = "0.5.0"
OPENALEX_WORKS = "https://api.openalex.org/works"
USER_AGENT = "CNS-Skills/0.5.0 (https://github.com/niuyupeng/CNS-Skills)"

# The conference windows reflect the coverage of these OpenAlex source records,
# not the currency of the venue policies. Current official venue instructions are
# handled separately in references/venue-profiles.md.
VENUES: dict[str, dict[str, str]] = {
    "cell": {
        "label": "Cell",
        "family": "journal",
        "work_type": "article",
        "source_id": "S110447773",
        "from_date": "2024-01-01",
        "to_date": "2026-08-30",
        "coverage_note": "Recent abstract-bearing articles indexed under Cell.",
    },
    "nature": {
        "label": "Nature",
        "family": "journal",
        "work_type": "article",
        "source_id": "S137773608",
        "from_date": "2024-01-01",
        "to_date": "2026-08-30",
        "coverage_note": "Recent abstract-bearing articles indexed under Nature.",
    },
    "science": {
        "label": "Science",
        "family": "journal",
        "work_type": "article",
        "source_id": "S3880285",
        "from_date": "2024-01-01",
        "to_date": "2026-08-30",
        "coverage_note": "Recent abstract-bearing articles indexed under Science.",
    },
    "aaai": {
        "label": "AAAI",
        "family": "conference",
        "work_type": "conference-paper",
        "source_id": "S4210191458",
        "from_date": "2024-01-01",
        "to_date": "2026-08-30",
        "coverage_note": "Recent papers indexed under the AAAI proceedings source.",
    },
    "cvpr": {
        "label": "CVPR",
        "family": "conference",
        "work_type": "conference-paper",
        "source_id": "S4363607701",
        "from_date": "2022-01-01",
        "to_date": "2022-12-31",
        "coverage_note": "CVPR 2022 source snapshot; use current official rules for submission decisions.",
    },
    "neurips": {
        "label": "NeurIPS",
        "family": "conference",
        "work_type": "article",
        "source_id": "S4306420609",
        "from_date": "2021-01-01",
        "to_date": "2021-12-31",
        "coverage_note": "NeurIPS 2021 source snapshot; use current official rules for submission decisions.",
    },
    "icml": {
        "label": "ICML",
        "family": "conference",
        "work_type": "conference-paper",
        "source_id": "S4306419644",
        "from_date": "2021-01-01",
        "to_date": "2021-12-31",
        "coverage_note": "ICML 2021 source snapshot; use current official rules for submission decisions.",
    },
    "iclr": {
        "label": "ICLR",
        "family": "conference",
        "work_type": "conference-paper",
        "source_id": "S4306419637",
        "from_date": "2021-01-01",
        "to_date": "2021-12-31",
        "coverage_note": "ICLR 2021 source snapshot; use current official rules for submission decisions.",
    },
}

MOVE_PATTERNS: dict[str, tuple[str, ...]] = {
    "context": (
        r"\b(?:is|are|has become|remain) (?:a |an )?(?:central|major|important|key|fundamental)\b",
        r"\b(?:recent advances|in recent years|the ability to|understanding how)\b",
    ),
    "gap_or_problem": (
        r"\b(?:however|yet|despite|although)\b",
        r"\b(?:remains? (?:unclear|unknown|challenging)|is poorly understood|has not been)\b",
        r"\b(?:challenge|limitation|bottleneck|lack|scarce|difficult)\b",
    ),
    "contribution": (
        r"\b(?:here|in this (?:work|paper|study)),? we\b",
        r"\bwe (?:introduce|present|propose|develop|derive|design|establish|build)\b",
        r"\bthis (?:work|paper|study) (?:introduces|presents|proposes|develops|establishes)\b",
    ),
    "result": (
        r"\bwe (?:show|find|demonstrate|observe|report|achieve|outperform|reveal)\b",
        r"\b(?:results?|experiments?|analyses?) (?:show|demonstrate|reveal|indicate)\b",
        r"\b(?:improves?|reduces?|increases?|outperforms?|achieves?)\b.{0,45}\b\d",
    ),
    "implication": (
        r"\b(?:these|our) (?:results|findings) (?:suggest|show|establish|provide|open)\b",
        r"\b(?:thereby|thus|therefore|collectively|overall)\b",
        r"\b(?:may|could|should) (?:enable|facilitate|inform|advance|help)\b",
    ),
    "limitation_or_boundary": (
        r"\b(?:limitation|limited by|remains to be|future work|further work)\b",
        r"\b(?:may not|cannot|does not|do not) (?:generalize|establish|capture|account)\b",
        r"\b(?:within|under) (?:the )?(?:tested|studied|evaluated)\b",
    ),
}

STRONG_VERBS = re.compile(
    r"\b(?:demonstrat(?:e|es|ed)|reveal(?:s|ed)?|establish(?:es|ed)?|"
    r"outperform(?:s|ed)?|achiev(?:e|es|ed)|validat(?:e|es|ed)|"
    r"identif(?:y|ies|ied)|enable(?:s|d)?|improv(?:e|es|ed)|reduc(?:e|es|ed)|"
    r"show(?:s|ed)?|find(?:s|ings?)?|found)\b",
    re.IGNORECASE,
)

HEDGES = re.compile(
    r"\b(?:may|might|could|suggest(?:s|ed)?|indicat(?:e|es|ed)|appear(?:s|ed)?|"
    r"likely|potentially|possibly|perhaps|approximately|generally|largely|"
    r"seem(?:s|ed)?|possible)\b",
    re.IGNORECASE,
)

WORD_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:\.\d+)?%?")


def reconstruct_abstract(index: dict[str, list[int]] | None) -> str:
    """Reconstruct an abstract from an OpenAlex inverted index."""
    if not index:
        return ""
    maximum = max((position for positions in index.values() for position in positions), default=-1)
    words = [""] * (maximum + 1)
    for token, positions in index.items():
        for position in positions:
            if position < 0 or position > maximum:
                raise ValueError("abstract inverted index contains an invalid position")
            words[position] = token
    # A small number of legacy OpenAlex records contain unassigned positions.
    # Omitting those gaps preserves every available token and keeps the record
    # usable for aggregate length and rhetorical-move estimates.
    return " ".join(token for token in words if token)


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def split_sentences(text: str) -> list[str]:
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", re.sub(r"\s+", " ", text).strip())
    return [piece.strip() for piece in pieces if piece.strip()]


def describe(values: Iterable[float | int]) -> dict[str, float | int]:
    data = list(values)
    if not data:
        return {"count": 0, "mean": 0.0, "median": 0.0, "stdev": 0.0, "cv": 0.0, "min": 0.0, "max": 0.0}
    mean = statistics.fmean(data)
    stdev = statistics.pstdev(data)
    return {
        "count": len(data),
        "mean": round(mean, 2),
        "median": round(statistics.median(data), 2),
        "stdev": round(stdev, 2),
        "cv": round(stdev / mean, 3) if mean else 0.0,
        "min": round(min(data), 2),
        "max": round(max(data), 2),
    }


def percentage(count: int, denominator: int) -> float:
    return round(100.0 * count / denominator, 1) if denominator else 0.0


def pattern_count(text: str, patterns: Iterable[str]) -> int:
    return sum(len(re.findall(pattern, text, flags=re.IGNORECASE)) for pattern in patterns)


def sentence_move(sentence: str) -> str:
    """Assign one primary rhetorical move, favoring specific moves over context."""
    order = (
        "limitation_or_boundary",
        "contribution",
        "result",
        "gap_or_problem",
        "implication",
        "context",
    )
    for move in order:
        if pattern_count(sentence, MOVE_PATTERNS[move]):
            return move
    return "other"


def record_metrics(record: dict[str, Any]) -> dict[str, Any]:
    title = record.get("title") or ""
    abstract = reconstruct_abstract(record.get("abstract_inverted_index"))
    abstract_words = words(abstract)
    sentences = split_sentences(abstract)
    lower = abstract.lower()
    return {
        "title": title,
        "title_words": len(words(title)),
        "title_has_colon": bool(re.search(r"[:：]", title)),
        "title_has_question": "?" in title,
        "title_has_acronym": bool(re.search(r"\b[A-Z]{2,}(?:-[A-Z0-9]+)?\b", title)),
        "abstract_words": len(abstract_words),
        "abstract_sentences": len(sentences),
        "abstract_sha256": hashlib.sha256(abstract.encode("utf-8")).hexdigest(),
        "sentence_word_lengths": [len(words(sentence)) for sentence in sentences],
        "uses_first_person": bool(re.search(r"\b(?:we|our|ours)\b", lower)),
        "contains_numeric_evidence": bool(re.search(r"\b\d+(?:\.\d+)?\s*%?\b", abstract)),
        "strong_verb_count": len(STRONG_VERBS.findall(abstract)),
        "hedge_count": len(HEDGES.findall(abstract)),
        "move_presence": {
            move: bool(pattern_count(abstract, patterns)) for move, patterns in MOVE_PATTERNS.items()
        },
        "first_sentence_move": sentence_move(sentences[0]) if sentences else "other",
        "final_sentence_move": sentence_move(sentences[-1]) if sentences else "other",
    }


def summarize_venue(records: list[dict[str, Any]], config: dict[str, str]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    metrics = [record_metrics(record) for record in records]
    total_words = sum(item["abstract_words"] for item in metrics)
    sentence_lengths = [length for item in metrics for length in item["sentence_word_lengths"]]
    move_names = list(MOVE_PATTERNS)
    first_moves = Counter(item["first_sentence_move"] for item in metrics)
    final_moves = Counter(item["final_sentence_move"] for item in metrics)
    count = len(metrics)
    aggregate = {
        "venue": config["label"],
        "family": config["family"],
        "openalex_source_id": config["source_id"],
        "sample_window": {"from": config["from_date"], "to": config["to_date"]},
        "coverage_note": config["coverage_note"],
        "sampled_abstracts": count,
        "publication_years": dict(sorted(Counter(str(record.get("publication_year")) for record in records).items())),
        "title": {
            "word_count": describe(item["title_words"] for item in metrics),
            "colon_percent": percentage(sum(item["title_has_colon"] for item in metrics), count),
            "question_percent": percentage(sum(item["title_has_question"] for item in metrics), count),
            "acronym_percent": percentage(sum(item["title_has_acronym"] for item in metrics), count),
        },
        "abstract": {
            "word_count": describe(item["abstract_words"] for item in metrics),
            "sentence_count": describe(item["abstract_sentences"] for item in metrics),
            "sentence_word_count_pooled": describe(sentence_lengths),
            "first_person_percent": percentage(sum(item["uses_first_person"] for item in metrics), count),
            "numeric_evidence_percent": percentage(sum(item["contains_numeric_evidence"] for item in metrics), count),
            "strong_verbs_per_1000_words": round(1000 * sum(item["strong_verb_count"] for item in metrics) / total_words, 2) if total_words else 0.0,
            "hedges_per_1000_words": round(1000 * sum(item["hedge_count"] for item in metrics) / total_words, 2) if total_words else 0.0,
            "rhetorical_move_presence_percent": {
                move: percentage(sum(item["move_presence"][move] for item in metrics), count)
                for move in move_names
            },
            "first_sentence_move_percent": {
                move: percentage(move_count, count) for move, move_count in sorted(first_moves.items())
            },
            "final_sentence_move_percent": {
                move: percentage(move_count, count) for move, move_count in sorted(final_moves.items())
            },
        },
    }
    manifest: list[dict[str, Any]] = []
    for record, item in zip(records, metrics):
        manifest.append(
            {
                "venue": config["label"],
                "family": config["family"],
                "sample_from": config["from_date"],
                "sample_to": config["to_date"],
                "publication_year": record.get("publication_year"),
                "openalex_id": record.get("id"),
                "doi": record.get("doi"),
                "title": item["title"],
                "title_words": item["title_words"],
                "abstract_words": item["abstract_words"],
                "abstract_sentences": item["abstract_sentences"],
                "abstract_sha256": item["abstract_sha256"],
                "sentence_word_lengths": ";".join(str(value) for value in item["sentence_word_lengths"]),
                "title_has_colon": item["title_has_colon"],
                "title_has_question": item["title_has_question"],
                "title_has_acronym": item["title_has_acronym"],
                "uses_first_person": item["uses_first_person"],
                "contains_numeric_evidence": item["contains_numeric_evidence"],
                "strong_verb_count": item["strong_verb_count"],
                "hedge_count": item["hedge_count"],
                "first_sentence_move": item["first_sentence_move"],
                "final_sentence_move": item["final_sentence_move"],
                **{f"move_{move}": item["move_presence"][move] for move in MOVE_PATTERNS},
            }
        )
    return aggregate, manifest


def build_query(config: dict[str, str], per_venue: int, seed: int) -> str:
    if not 1 <= per_venue <= 100:
        raise ValueError("OpenAlex page size must be between 1 and 100")
    filters = ",".join(
        (
            f"primary_location.source.id:{config['source_id']}",
            f"from_publication_date:{config['from_date']}",
            f"to_publication_date:{config['to_date']}",
            "has_abstract:true",
            f"type:{config['work_type']}",
        )
    )
    params = {
        "filter": filters,
        "sample": str(per_venue),
        "seed": str(seed),
        "per-page": str(per_venue),
        "select": "id,title,abstract_inverted_index,publication_year,type,doi",
    }
    return OPENALEX_WORKS + "?" + urllib.parse.urlencode(params)


def fetch_json(url: str, retries: int = 3, timeout: float = 30.0) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(1.0 + attempt)
    raise RuntimeError(f"request failed after {retries} attempts: {last_error}")


def fetch_venue(
    config: dict[str, str], per_venue: int, seed: int, min_abstract_words: int = 80
) -> tuple[list[dict[str, Any]], list[str]]:
    # Oversampling lets us remove metadata stubs and one-line teaser records
    # without choosing papers by citation count or perceived prestige. OpenAlex's
    # supported maximum page size is 100, so larger targets use reproducible
    # independent samples and deduplicate by work ID.
    candidate_count = 100
    attempts = max(3, ceil(per_venue / candidate_count) * 3)
    usable: list[dict[str, Any]] = []
    seen: set[str] = set()
    urls: list[str] = []
    for attempt in range(attempts):
        url = build_query(config, candidate_count, seed + attempt)
        urls.append(url)
        payload = fetch_json(url)
        records = payload.get("results")
        if not isinstance(records, list):
            raise RuntimeError(f"OpenAlex returned no result list for {config['label']}")
        for record in records:
            record_id = record.get("id")
            if not record_id or record_id in seen:
                continue
            seen.add(record_id)
            if (
                record.get("abstract_inverted_index")
                and record.get("title")
                and len(words(reconstruct_abstract(record["abstract_inverted_index"]))) >= min_abstract_words
            ):
                usable.append(record)
                if len(usable) >= per_venue:
                    break
        if len(usable) >= per_venue:
            break
    if not usable:
        raise RuntimeError(f"OpenAlex returned no usable abstract records for {config['label']}")
    return usable[:per_venue], urls


def csv_safe(value: Any) -> Any:
    """Neutralize formula-leading metadata when a CSV is opened in a spreadsheet."""
    if isinstance(value, str) and value.lstrip()[:1] in {"=", "+", "-", "@"}:
        return "'" + value
    return value


def generation_timestamp() -> str:
    source_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if source_epoch is not None:
        try:
            return datetime.fromtimestamp(float(source_epoch), timezone.utc).isoformat()
        except (ValueError, OSError, OverflowError) as exc:
            raise ValueError("SOURCE_DATE_EPOCH must be a valid Unix timestamp") from exc
    return datetime.now(timezone.utc).isoformat()


def write_manifest(path: Path, records: list[dict[str, Any]]) -> None:
    fields = (
        "venue",
        "family",
        "sample_from",
        "sample_to",
        "publication_year",
        "openalex_id",
        "doi",
        "title",
        "title_words",
        "abstract_words",
        "abstract_sentences",
        "abstract_sha256",
        "sentence_word_lengths",
        "title_has_colon",
        "title_has_question",
        "title_has_acronym",
        "uses_first_person",
        "contains_numeric_evidence",
        "strong_verb_count",
        "hedge_count",
        "first_sentence_move",
        "final_sentence_move",
        "move_context",
        "move_gap_or_problem",
        "move_contribution",
        "move_result",
        "move_implication",
        "move_limitation_or_boundary",
    )
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: csv_safe(record.get(field)) for field in fields})


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("research"), help="directory for aggregate JSON and metadata CSV")
    parser.add_argument("--per-venue", type=int, default=40, help="random abstract sample per venue (1-200)")
    parser.add_argument("--seed", type=int, default=20260830, help="OpenAlex reproducibility seed")
    parser.add_argument("--venues", nargs="+", choices=sorted(VENUES), default=list(VENUES), help="venue keys to include")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args(argv)
    if not 1 <= args.per_venue <= 200:
        parser.error("--per-venue must be between 1 and 200")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        generated_at = generation_timestamp()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    aggregates: list[dict[str, Any]] = []
    manifest: list[dict[str, Any]] = []
    requests: list[dict[str, str]] = []
    try:
        for key in args.venues:
            config = VENUES[key]
            records, urls = fetch_venue(config, args.per_venue, args.seed)
            aggregate, venue_manifest = summarize_venue(records, config)
            aggregates.append(aggregate)
            manifest.extend(venue_manifest)
            requests.extend({"venue": config["label"], "url": url} for url in urls)
            print(f"{config['label']}: analyzed {len(records)} abstract(s)", file=sys.stderr)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    aggregate_path = args.output_dir / "venue-corpus-aggregate.json"
    manifest_path = args.output_dir / "venue-corpus-manifest.csv"
    report = {
        "tool": "CNS Skills venue corpus analyzer",
        "version": VERSION,
        "generated_at_utc": generated_at,
        "data_provider": "OpenAlex",
        "sample_seed": args.seed,
        "requested_abstracts_per_venue": args.per_venue,
        "total_analyzed_abstracts": len(manifest),
        "method": "Random source-and-date-filtered candidate samples; records shorter than 80 English tokens were treated as metadata stubs, and abstracts were reconstructed only in memory. Outputs contain aggregate metrics, per-record non-text features, abstract hashes, and metadata, never abstract text.",
        "interpretation_limits": [
            "The sample describes indexed English abstracts, not complete papers or editorial causality.",
            "Source assignment, abstract availability, historical coverage, and heuristic move detection can bias results.",
            "Conference corpus years differ where OpenAlex source coverage is historical; verify current official venue rules separately.",
            "Aggregate frequencies are diagnostic context, not prose templates or acceptance predictors.",
        ],
        "requests": requests,
        "venues": aggregates,
    }
    aggregate_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_manifest(manifest_path, manifest)
    print(f"Wrote {aggregate_path} and {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
