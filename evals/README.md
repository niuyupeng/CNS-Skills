# Skill-selection evaluations

`discovery-prompts.jsonl` is a bilingual routing set for the metadata that hosts see before loading the full skill. Each row contains a stable ID, a `development` or `heldout` split, a prompt, an expected `invoke` decision, a language, and the scope reason for that label.

The set covers direct and indirect requests for scientific manuscript polishing, Chinese-to-English academic rewriting, peer review, rebuttals, citation/DOI auditing, grant revision, and visual-evidence QA. Its negative cases cover central-nervous-system questions, literature search or citation formatting alone, paper summarization, conference-related coding, raw statistical analysis, non-manuscript translation, admissions writing, general illustration, marketing copy, and AI-detector evasion.

Run the structural checks with:

```bash
python scripts/check_discovery_metadata.py
```

Version 0.6.0 contains 64 cases: the original 34-case development split (18 invoke, 16 do not invoke) and a locked 30-case held-out split (15/15). `heldout-lock.json` records a canonical SHA-256 digest. After release, held-out rows are append-only; a factual label correction requires a documented versioned change. Do not edit skill metadata merely to fit known held-out wording.

An independent metadata-only review should receive only the final `name`, `description`, and prompts—not the intended rationale or a keyword checklist. The set includes mixed requests whose legitimate manuscript work should proceed while an acceptance guarantee or detector-evasion clause is refused. It is a scoped regression set, not a measured guarantee that every ChatGPT, Codex, Claude, or other host will route every paraphrase correctly. Host versions, competing installed skills, context budgets, and model behavior can change. Contributions should prioritize realistic false positives and false negatives over keyword repetition.
