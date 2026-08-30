# Skill-selection evaluations

`discovery-prompts.jsonl` is a bilingual routing set for the metadata that hosts see before loading the full skill. Each row contains a prompt, an expected `invoke` decision, a language, and the scope reason for that label.

The set covers direct and indirect requests for scientific manuscript polishing, Chinese-to-English academic rewriting, peer review, rebuttals, citation/DOI auditing, grant revision, and visual-evidence QA. Its negative cases cover central-nervous-system questions, literature search or citation formatting alone, paper summarization, conference-related coding, raw statistical analysis, non-manuscript translation, admissions writing, general illustration, marketing copy, and AI-detector evasion.

Run the structural checks with:

```bash
python scripts/check_discovery_metadata.py
```

On 2026-08-30, an independent metadata-only review using only the final `name` and `description` agreed with all 34 labels: 18 invoke and 16 do not invoke. The set includes mixed requests whose legitimate manuscript work should proceed while an acceptance guarantee or detector-evasion clause is refused. This is a scoped regression set, not a measured guarantee that every ChatGPT, Codex, Claude, or other host will route every paraphrase correctly. Host versions, competing installed skills, context budgets, and model behavior can change. Contributions should prioritize realistic false positives and false negatives over keyword repetition.
