#!/usr/bin/env python3
"""CNS manuscript triage: evidence risks, repetition, and prose-pattern diagnostics.

This is deliberately not an AI detector. It uses transparent heuristics to identify
passages that deserve human review. It reads UTF-8 text/Markdown and DOCX files
using only the Python standard library.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET

VERSION = "0.6.0"
CROSSREF_PUBLIC_INTERVAL_SECONDS = 0.22

STOCK_PATTERNS: dict[str, str] = {
    "zh_this_shows": r"这(?:一结果|些结果|一发现)?(?:说明|表明|提示)",
    "zh_note": r"(?:值得注意的是|需要指出的是|不难发现)",
    "zh_future": r"未来(?:仍)?(?:需要|需|应当|可以|有必要)",
    "zh_significance": r"(?:具有|有着)(?:重要|重大)(?:的)?(?:意义|价值)",
    "zh_new_path": r"(?:提供|开辟)了?(?:一种)?新的?(?:思路|路径|可能性)",
    "zh_prospect": r"(?:广阔|巨大)(?:的)?(?:前景|潜力)",
    "en_note": r"\b(?:it is important to note that|notably|it should be noted that)\b",
    "en_landscape": r"\bin (?:today's|the) (?:rapidly )?evolving landscape\b",
    "en_hype": r"\b(?:revolutioni[sz]e|transformative|game[- ]changer|pave the way|unlock)\b",
    "en_future": r"\bfurther research is (?:needed|required)\b",
}

CONTRAST_PATTERNS: dict[str, str] = {
    "zh_not_but": r"不是.{0,45}?而是",
    "zh_not_only": r"不仅.{0,60}?(?:而且|还|也)",
    "en_not_but": r"\bnot\s+.{1,80}?\s+but\b",
    "en_not_only": r"\bnot only\s+.{1,100}?\s+but also\b",
}

# These patterns are deliberately narrower than a word list. The terms below
# can be correct scientific language; the audit flags compound editorial labels
# that often leak from a writer's planning notes into finished review prose.
SCAFFOLD_PATTERNS: dict[str, str] = {
    "zh_evidence_scaffold": (
        r"(?:证据链|证据剖面|证据矩阵|证据图谱|证据轴|证据层|证据边界|"
        r"(?:核心)?证据卡|证据拼接|拼接证据|编织证据)"
    ),
    "zh_generic_framework": (
        r"(?:本文|本综述|我们).{0,30}?(?:提出|构建|建立|采用|使用).{0,18}?"
        r"(?:统一|综合|比较|分析|决策)?框架"
    ),
    "zh_abstract_glue": r"(?:全链条|逻辑闭环|研究图谱|方法图谱|赋能.{0,12}?(?:研究|设计|创新))",
    "en_evidence_scaffold": (
        r"\b(?:evidence chain|evidence profile|evidence matrix|evidence landscape|"
        r"evidence layer|evidence axis|evidence boundary|evidence card|"
        r"evidence[- ]cent(?:er|re)ed)\b"
    ),
    "en_generic_framework": (
        r"\b(?:this review|we)\s+(?:therefore\s+)?(?:propose|present|establish|"
        r"introduce|adopt|use|develop)\b.{0,70}?\b(?:unified |comparison |"
        r"decision[- ]cent(?:er|re)ed )?framework\b"
    ),
    "en_evidence_stitching": r"\b(?:stitch|weav|assembl|bridg)\w*\s+(?:the\s+)?evidence\b",
    "en_abstract_landscape": r"\b(?:rapidly evolving|research|current|broader) landscape\b",
}

HIGH_RISK_TERMS = re.compile(
    r"首次|首个|前所未有|最优|最佳|显著优于|临床可用|临床有效|安全有效|"
    r"因果|自主闭环|完全自主|普遍适用|state[- ]of[- ]the[- ]art|unprecedented|"
    r"first[- ]ever|clinically effective|causes?|universal|fully autonomous",
    re.IGNORECASE,
)

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
CITATION_RE = re.compile(
    r"(?:\[(?:\d{1,3}(?:\s*[-,–]\s*\d{1,3})*)\])|"
    r"(?:\((?:[^()]{0,45}?\b(?:19|20)\d{2}[a-z]?[^()]*)\))|"
    r"(?:\b[A-Z][A-Za-z'’\-]+\s+et\s+al\.?,?\s*(?:19|20)\d{2})"
)
NUMBER_RE = re.compile(r"(?<![A-Za-z])(?:\d+(?:\.\d+)?\s*%?|[一二三四五六七八九十]+倍)")


def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        try:
            xml_parts = [archive.read("word/document.xml")]
        except KeyError as exc:
            raise ValueError("DOCX has no word/document.xml") from exc
        for optional_part in ("word/footnotes.xml", "word/endnotes.xml"):
            if optional_part in archive.namelist():
                xml_parts.append(archive.read(optional_part))
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    math_text = "{http://schemas.openxmlformats.org/officeDocument/2006/math}t"
    paragraphs: list[str] = []
    for xml in xml_parts:
        root = ET.fromstring(xml)
        for paragraph in root.iter(namespace + "p"):
            parts: list[str] = []
            for node in paragraph.iter():
                if node.tag in {namespace + "t", math_text} and node.text:
                    parts.append(node.text)
                elif node.tag == namespace + "tab":
                    parts.append("\t")
                elif node.tag in {namespace + "br", namespace + "cr"}:
                    parts.append("\n")
            text = "".join(parts).strip()
            if text:
                paragraphs.append(text)
    return "\n\n".join(paragraphs)


def read_input(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    if path.suffix.lower() not in {".txt", ".md", ".markdown"}:
        raise ValueError("Supported inputs: .docx, .txt, .md, .markdown")
    return path.read_text(encoding="utf-8-sig")


def split_paragraphs(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]


def split_sentences(text: str) -> list[str]:
    compact = re.sub(r"[\t ]+", " ", text)
    pieces = re.split(r"(?<=[。！？!?；;])\s*|(?<=[.!?])\s+(?=[A-Z0-9])", compact)
    return [re.sub(r"\s+", " ", item).strip() for item in pieces if item.strip()]


def visible_length(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def stats(values: Iterable[int]) -> dict[str, float | int]:
    data = list(values)
    if not data:
        return {"count": 0, "mean": 0.0, "median": 0.0, "stdev": 0.0, "cv": 0.0, "min": 0, "max": 0}
    mean = statistics.fmean(data)
    stdev = statistics.pstdev(data)
    return {
        "count": len(data),
        "mean": round(mean, 2),
        "median": round(statistics.median(data), 2),
        "stdev": round(stdev, 2),
        "cv": round(stdev / mean, 3) if mean else 0.0,
        "min": min(data),
        "max": max(data),
    }


def context_snippet(text: str, start: int, end: int, radius: int = 45) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    return re.sub(r"\s+", " ", text[left:right]).strip()


def pattern_hits(text: str, patterns: dict[str, str]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for label, pattern in patterns.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE | re.DOTALL))
        if matches:
            output.append(
                {
                    "pattern": label,
                    "count": len(matches),
                    "examples": [context_snippet(text, m.start(), m.end()) for m in matches[:3]],
                }
            )
    return sorted(output, key=lambda item: (-item["count"], item["pattern"]))


def sentence_openers(sentences: list[str], width: int = 12) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    examples: dict[str, list[str]] = {}
    for sentence in sentences:
        cleaned = re.sub(r"^[\s\d.、（()\[\]【】]+", "", sentence)
        cleaned = re.sub(r"[\s，,。；;：:、“”‘’\-—]", "", cleaned).lower()
        if len(cleaned) < 6:
            continue
        opener = cleaned[:width]
        counter[opener] += 1
        examples.setdefault(opener, []).append(sentence[:140])
    return [
        {"opener": opener, "count": count, "examples": examples[opener][:3]}
        for opener, count in counter.most_common()
        if count >= 3
    ][:20]


def normalized_ngrams(text: str, size: int = 16) -> list[dict[str, Any]]:
    chunks = re.findall(r"[\u3400-\u9fffA-Za-z0-9]{%d,}" % size, re.sub(r"\s+", "", text))
    counter: Counter[str] = Counter()
    for chunk in chunks:
        if len(chunk) > 120:
            chunk = chunk[:120]
        for index in range(0, len(chunk) - size + 1, max(1, size // 2)):
            gram = chunk[index : index + size].lower()
            if not re.fullmatch(r"\d+", gram):
                counter[gram] += 1
    return [{"fragment": gram, "count": count} for gram, count in counter.most_common(20) if count >= 3]


def doi_list(text: str) -> list[str]:
    dois = []
    for match in DOI_RE.finditer(text):
        doi = match.group(0).rstrip(".,;:)]}，。；：）】").lower()
        if doi not in dois:
            dois.append(doi)
    return dois


def verify_doi(doi: str, timeout: float = 12.0, retries: int = 3) -> dict[str, Any]:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    request = urllib.request.Request(url, headers={"User-Agent": "CNS-Skills/0.6.0 (https://github.com/niuyupeng/CNS-Skills)"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            message = payload.get("message", {})
            title = (message.get("title") or [None])[0]
            issued = message.get("published-print") or message.get("published-online") or message.get("issued") or {}
            date_parts = issued.get("date-parts") or []
            year = date_parts[0][0] if date_parts and date_parts[0] else None
            return {
                "doi": doi,
                "status": "verified",
                "title": title,
                "publisher": message.get("publisher"),
                "type": message.get("type"),
                "year": year,
                "url": message.get("URL"),
            }
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt + 1 < retries:
                retry_value = exc.headers.get("Retry-After", "1") if exc.headers else "1"
                try:
                    delay = float(retry_value)
                except ValueError:
                    delay = 1.0
                time.sleep(min(max(delay, CROSSREF_PUBLIC_INTERVAL_SECONDS), 10.0))
                continue
            return {"doi": doi, "status": "not_found" if exc.code == 404 else "http_error", "http_code": exc.code}
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return {"doi": doi, "status": "network_error", "error": str(exc)}
    return {"doi": doi, "status": "http_error", "http_code": 429}


def numeric_claims_without_citation(sentences: list[str]) -> list[str]:
    output = []
    for sentence in sentences:
        if NUMBER_RE.search(sentence) and not CITATION_RE.search(sentence) and not DOI_RE.search(sentence):
            output.append(sentence[:320])
    return output[:50]


def high_risk_claims(sentences: list[str]) -> list[str]:
    return [sentence[:320] for sentence in sentences if HIGH_RISK_TERMS.search(sentence)][:50]


def build_report(path: Path, text: str, verify_dois: bool = False) -> dict[str, Any]:
    paragraphs = split_paragraphs(text)
    sentences = split_sentences(text)
    dois = doi_list(text)
    report: dict[str, Any] = {
        "tool": "CNS Skills manuscript audit",
        "version": VERSION,
        "disclaimer": "Transparent writing triage; not an AI detector and not a substitute for source reading.",
        "source": str(path.resolve()),
        "counts": {
            "characters_no_space": visible_length(text),
            "paragraphs": len(paragraphs),
            "sentences": len(sentences),
            "dois": len(dois),
        },
        "sentence_length": stats(visible_length(item) for item in sentences),
        "paragraph_length": stats(visible_length(item) for item in paragraphs),
        "stock_phrase_hits": pattern_hits(text, STOCK_PATTERNS),
        "repeated_contrast_hits": pattern_hits(text, CONTRAST_PATTERNS),
        "editorial_scaffolding_candidates": pattern_hits(text, SCAFFOLD_PATTERNS),
        "repeated_sentence_openers": sentence_openers(sentences),
        "repeated_fragments": normalized_ngrams(text),
        "numeric_claims_without_nearby_citation": numeric_claims_without_citation(sentences),
        "high_risk_claim_language": high_risk_claims(sentences),
        "dois": dois,
    }
    if verify_dois:
        results = []
        for index, doi in enumerate(dois):
            if index:
                time.sleep(CROSSREF_PUBLIC_INTERVAL_SECONDS)
            results.append(verify_doi(doi))
        report["doi_verification"] = results
    return report


def render_text(report: dict[str, Any]) -> str:
    counts = report["counts"]
    lines = [
        "CNS manuscript audit",
        f"Source: {report['source']}",
        "Note: This is transparent writing triage, not an AI detector.",
        "",
        f"Characters: {counts['characters_no_space']} | paragraphs: {counts['paragraphs']} | sentences: {counts['sentences']} | DOIs: {counts['dois']}",
        f"Sentence length mean/CV: {report['sentence_length']['mean']} / {report['sentence_length']['cv']}",
        f"Paragraph length mean/CV: {report['paragraph_length']['mean']} / {report['paragraph_length']['cv']}",
        "",
    ]
    for title, key in [
        ("Stock phrase patterns", "stock_phrase_hits"),
        ("Repeated contrast patterns", "repeated_contrast_hits"),
        ("Editorial-scaffolding candidates", "editorial_scaffolding_candidates"),
        ("Repeated sentence openers", "repeated_sentence_openers"),
        ("Repeated fragments", "repeated_fragments"),
    ]:
        items = report[key]
        lines.append(f"{title}: {len(items)} pattern(s)")
        for item in items[:10]:
            label = item.get("pattern") or item.get("opener") or item.get("fragment")
            lines.append(f"  - {label}: {item['count']}")
        lines.append("")
    lines.append(f"Numeric sentences without a recognized nearby citation: {len(report['numeric_claims_without_nearby_citation'])}")
    lines.append(f"High-risk claim-language sentences: {len(report['high_risk_claim_language'])}")
    if "doi_verification" in report:
        counter = Counter(item["status"] for item in report["doi_verification"])
        lines.append("DOI verification: " + ", ".join(f"{key}={value}" for key, value in sorted(counter.items())))
        for item in report["doi_verification"]:
            if item["status"] != "verified":
                lines.append(f"  - {item['doi']}: {item['status']}")
    return "\n".join(lines)


def make_shareable(report: dict[str, Any]) -> dict[str, Any]:
    """Remove local paths and unpublished excerpts from a JSON report copy."""
    output = copy.deepcopy(report)
    output["source"] = Path(output["source"]).name
    output["shareable_redaction"] = "Local paths and manuscript excerpts removed; counts and diagnostics retained."
    for key in (
        "stock_phrase_hits",
        "repeated_contrast_hits",
        "editorial_scaffolding_candidates",
        "repeated_sentence_openers",
    ):
        for item in output.get(key, []):
            item.pop("examples", None)
    for item in output.get("repeated_sentence_openers", []):
        item["opener"] = None
    for item in output.get("repeated_fragments", []):
        item["fragment"] = None
    for key in ("numeric_claims_without_nearby_citation", "high_risk_claim_language"):
        output[key + "_count"] = len(output.get(key, []))
        output[key] = []
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="DOCX, TXT, or Markdown manuscript")
    parser.add_argument("--json", dest="json_path", type=Path, help="write the full report as UTF-8 JSON")
    parser.add_argument("--verify-dois", action="store_true", help="query Crossref for each DOI")
    parser.add_argument("--shareable", action="store_true", help="redact local paths and manuscript excerpts from JSON output")
    parser.add_argument("--strict", action="store_true", help="exit 2 if a DOI is not verified")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser.parse_args(argv)


def same_path(left: Path, right: Path) -> bool:
    return str(left.resolve()).casefold() == str(right.resolve()).casefold()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.json_path and same_path(args.json_path, args.input):
        print("error: --json must not overwrite the input manuscript", file=sys.stderr)
        return 1
    try:
        text = read_input(args.input)
        report = build_report(args.input, text, verify_dois=args.verify_dois)
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(render_text(report))
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        json_report = make_shareable(report) if args.shareable else report
        args.json_path.write_text(json.dumps(json_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.strict and any(item.get("status") != "verified" for item in report.get("doi_verification", [])):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
