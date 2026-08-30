#!/usr/bin/env python3
"""Validate skill-routing and marketplace-discovery metadata without dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.4.0"


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


def validate_evals(errors: list[str]) -> None:
    path = ROOT / "evals" / "discovery-prompts.jsonl"
    positives = 0
    negatives = 0
    languages: set[str] = set()
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
        if not isinstance(item.get("prompt"), str) or not isinstance(item.get("invoke"), bool):
            errors.append(f"evals/discovery-prompts.jsonl:{number}: prompt/invoke schema error")
            continue
        positives += int(item["invoke"])
        negatives += int(not item["invoke"])
        languages.add(str(item.get("language", "")))
    if positives < 5 or negatives < 3:
        errors.append("discovery evals require at least 5 positive and 3 negative prompts")
    if not {"en", "zh"}.issubset(languages):
        errors.append("discovery evals must cover English and Chinese prompts")


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
