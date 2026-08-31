#!/usr/bin/env python3
"""Validate skill-routing and marketplace-discovery metadata without dependencies."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.9.0"


def load_json(relative: str, errors: list[str]) -> dict[str, Any]:
    path = ROOT / relative
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{relative}: invalid or unreadable JSON ({exc})")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{relative}: root must be an object")
        return {}
    return payload


def skill_frontmatter(errors: list[str]) -> dict[str, str]:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if match is None:
        errors.append("SKILL.md: missing YAML frontmatter")
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"\'')
    return fields


def validate_skill(errors: list[str]) -> None:
    fields = skill_frontmatter(errors)
    if fields.get("name") != "cns-skills":
        errors.append("SKILL.md: name must remain cns-skills")
    if fields.get("license") != "MIT":
        errors.append("SKILL.md: license must remain MIT")
    if fields.get("version") != VERSION:
        errors.append(f"SKILL.md: metadata version must be {VERSION}")
    description = fields.get("description", "")
    if not description or len(description) > 1024:
        errors.append("SKILL.md: description must contain 1-1024 characters")
        return
    if not description.startswith(("Edits", "Edit", "Revises", "Revise", "Polishes", "Polish")):
        errors.append("SKILL.md: front-load the manuscript action in description")
    required_concepts = {
        "scientific/academic manuscript": ("scientific", "academic"),
        "research paper or SCI manuscript": ("research paper", "SCI manuscript"),
        "Chinese-to-English work": ("Chinese drafts", "academic English", "Chinese-to-English"),
        "peer review": ("peer-review", "response to reviewers"),
        "scientific title optimization": ("scientific title optimization", "paper-title"),
        "Chinese title optimization": ("论文题目优化", "SCI标题润色"),
        "citation audit": ("citation", "DOI"),
        "visual evidence": ("figure", "table", "caption"),
        "negative boundary": ("AI-detector evasion", "fabricated evidence"),
    }
    for label, phrases in required_concepts.items():
        if not any(phrase.casefold() in description.casefold() for phrase in phrases):
            errors.append(f"SKILL.md: description lost {label} routing coverage")


def yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*[\"']?(.+?)[\"']?\s*$", text, flags=re.MULTILINE)
    return match.group(1).rstrip("\"'") if match else None


def validate_openai_metadata(errors: list[str]) -> None:
    text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    short = yaml_scalar(text, "short_description") or ""
    prompt = yaml_scalar(text, "default_prompt") or ""
    if not 25 <= len(short) <= 64:
        errors.append("agents/openai.yaml: short_description must be 25-64 characters")
    if "$cns-skills" not in prompt:
        errors.append("agents/openai.yaml: default_prompt must mention $cns-skills")
    if not re.search(r"^\s*allow_implicit_invocation:\s*true\s*$", text, flags=re.MULTILINE):
        errors.append("agents/openai.yaml: implicit invocation must be explicitly enabled")


def validate_plugin_metadata(errors: list[str]) -> None:
    codex = load_json("plugins/cns-skills/.codex-plugin/plugin.json", errors)
    claude = load_json("plugins/cns-skills/.claude-plugin/plugin.json", errors)
    for label, payload in (("Codex", codex), ("Claude", claude)):
        if payload.get("name") != "cns-skills":
            errors.append(f"{label} plugin: name must be cns-skills")
        if payload.get("version") != VERSION:
            errors.append(f"{label} plugin: version must be {VERSION}")
        if payload.get("skills") != "./skills/":
            errors.append(f"{label} plugin: skills path must be ./skills/")

    interface = codex.get("interface", {})
    prompts = interface.get("defaultPrompt", []) if isinstance(interface, dict) else []
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        errors.append("Codex plugin: interface.defaultPrompt must contain 1-3 prompts")
    elif any(not isinstance(prompt, str) or len(prompt) > 128 for prompt in prompts):
        errors.append("Codex plugin: each starter prompt must be a string of at most 128 characters")

    codex_market = load_json(".agents/plugins/marketplace.json", errors)
    claude_market = load_json(".claude-plugin/marketplace.json", errors)
    if codex_market.get("name") != "cns-skills":
        errors.append("OpenAI marketplace: name must be cns-skills")
    if claude_market.get("name") != "cns-skills":
        errors.append("Claude marketplace: name must be cns-skills")
    market_plugins = claude_market.get("plugins", [])
    market_version = (
        market_plugins[0].get("version")
        if isinstance(market_plugins, list)
        and market_plugins
        and isinstance(market_plugins[0], dict)
        else None
    )
    if (
        not isinstance(market_plugins, list)
        or not market_plugins
        or market_version != VERSION
    ):
        errors.append(f"Claude marketplace: plugin version must be {VERSION}")


def validate_version_metadata(errors: list[str]) -> None:
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if not re.search(rf"^version:\s*{re.escape(VERSION)}\s*$", cff, flags=re.MULTILINE):
        errors.append(f"CITATION.cff: version must be {VERSION}")
    for relative in (
        "scripts/cns_audit.py",
        "scripts/check_crossrefs.py",
        "scripts/check_invariants.py",
        "scripts/review_citation_audit.py",
        "scripts/review_search_audit.py",
        "scripts/title_audit.py",
        "scripts/venue_corpus_analyzer.py",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        if f'VERSION = "{VERSION}"' not in text:
            errors.append(f"{relative}: VERSION must be {VERSION}")


def validate_evals(errors: list[str]) -> None:
    path = ROOT / "evals" / "discovery-prompts.jsonl"
    positives = 0
    negatives = 0
    languages: set[str] = set()
    split_labels: dict[str, set[bool]] = {"development": set(), "heldout": set()}
    split_languages: dict[str, set[str]] = {"development": set(), "heldout": set()}
    ids: set[str] = set()
    items: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"evals/discovery-prompts.jsonl: unreadable ({exc})")
        return
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"evals/discovery-prompts.jsonl:{number}: invalid JSON ({exc})")
            continue
        if not isinstance(item, dict):
            errors.append(f"evals/discovery-prompts.jsonl:{number}: row must be an object")
            continue
        if not isinstance(item.get("prompt"), str) or not isinstance(item.get("invoke"), bool):
            errors.append(f"evals/discovery-prompts.jsonl:{number}: prompt/invoke schema error")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            errors.append(f"evals/discovery-prompts.jsonl:{number}: missing id")
        elif item_id in ids:
            errors.append(f"evals/discovery-prompts.jsonl:{number}: duplicate id {item_id}")
        else:
            ids.add(item_id)
        if not isinstance(item.get("reason"), str) or not item["reason"].strip():
            errors.append(f"evals/discovery-prompts.jsonl:{number}: missing reason")
        split = item.get("split")
        if split not in split_labels:
            errors.append(
                f"evals/discovery-prompts.jsonl:{number}: split must be development or heldout"
            )
            continue
        language = str(item.get("language", ""))
        if language not in {"en", "zh"}:
            errors.append(f"evals/discovery-prompts.jsonl:{number}: language must be en or zh")
            continue
        items.append(item)
        positives += int(item["invoke"])
        negatives += int(not item["invoke"])
        languages.add(language)
        split_labels[split].add(item["invoke"])
        split_languages[split].add(language)
    if not 60 <= len(items) <= 80:
        errors.append("discovery evals require 60-80 valid prompts")
    if positives < 20 or negatives < 20:
        errors.append("discovery evals require at least 20 positive and 20 negative prompts")
    if not {"en", "zh"}.issubset(languages):
        errors.append("discovery evals must cover English and Chinese prompts")
    for split in ("development", "heldout"):
        if split_labels[split] != {True, False}:
            errors.append(f"{split} split must include positive and negative prompts")
        if split_languages[split] != {"en", "zh"}:
            errors.append(f"{split} split must include English and Chinese prompts")

    lock = load_json("evals/heldout-lock.json", errors)
    heldout = [item for item in items if item.get("split") == "heldout"]
    canonical = "\n".join(
        json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for item in heldout
    ).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    if lock.get("schema_version") != 1 or lock.get("split") != "heldout":
        errors.append("evals/heldout-lock.json: unsupported lock schema")
    if lock.get("count") != len(heldout):
        errors.append("evals/heldout-lock.json: heldout count mismatch")
    if lock.get("sha256") != digest:
        errors.append("evals/heldout-lock.json: heldout split hash mismatch")


def validate_readme_installation(errors: list[str]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required = (
        "codex plugin marketplace add niuyupeng/CNS-Skills",
        "claude plugin marketplace add niuyupeng/CNS-Skills",
        "~/.agents/skills/cns-skills",
        "~/.claude/skills/cns-skills",
    )
    for snippet in required:
        if snippet not in readme:
            errors.append(f"README.md: missing installation entry `{snippet}`")


def main() -> int:
    errors: list[str] = []
    validate_skill(errors)
    validate_openai_metadata(errors)
    validate_plugin_metadata(errors)
    validate_version_metadata(errors)
    validate_evals(errors)
    validate_readme_installation(errors)
    if errors:
        print("Discovery metadata validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Discovery metadata validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
