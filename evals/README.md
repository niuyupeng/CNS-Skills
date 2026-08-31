# Skill-selection evaluations

`discovery-prompts.jsonl` is a bilingual routing set for the metadata that hosts see before loading the full skill. Each row contains a stable ID, a `development` or `heldout` split, a prompt, an expected `invoke` decision, a language, and the scope reason for that label. Scientific manuscript-title optimization is positive; fiction naming and advertising headlines remain negative.

The set covers direct and indirect requests for scientific positioning, Review outlines, evidence matrices, author-led first drafts, manuscript polishing, Chinese-to-English academic rewriting, peer review, rebuttals, citation/DOI auditing, grant revision, plain-language scientific briefs, and visual-evidence QA. Its negative cases cover fabricated or coursework drafting, central-nervous-system questions, literature search or citation formatting alone, paper summarization, conference-related coding, raw statistical analysis, non-manuscript translation, admissions writing, general illustration, marketing copy, and AI-detector evasion.

Run the structural checks with:

```bash
python scripts/check_discovery_metadata.py
```

Version 0.12.0 contains 76 cases: a 46-case development split (25 invoke, 21 do not invoke) and the unchanged locked 30-case held-out split (15/15). `heldout-lock.json` records a canonical SHA-256 digest. After release, held-out rows are append-only; a factual label correction requires a documented versioned change. Do not edit skill metadata merely to fit known held-out wording.

An independent metadata-only review should receive only the final `name`, `description`, and prompts—not the intended rationale or a keyword checklist. The set includes mixed requests whose legitimate manuscript work should proceed while an acceptance guarantee or detector-evasion clause is refused. It is a scoped regression set, not a measured guarantee that every ChatGPT, Codex, Claude, or other host will route every paraphrase correctly. Host versions, competing installed skills, context budgets, and model behavior can change. Contributions should prioritize realistic false positives and false negatives over keyword repetition.

## Review-search adversarial evaluations

The review-search auditor is tested against 93 independently designed, locked data cases across the [H set](review-search-forward-evaluation-2026-08-30.md), [R2 reevaluation](review-search-forward-reevaluation-2026-08-30.md), [R3 adversarial evaluation](review-search-final-adversarial-evaluation-2026-08-30.md), [R4 fresh-before-fix evaluation](review-search-fourth-round-evaluation-2026-08-30.md), [R5 independent holdout evaluation](review-search-fifth-round-evaluation-2026-08-30.md), and [R6 independent holdout evaluation](review-search-sixth-round-evaluation-2026-08-30.md). Six focused unit probes exercise release-blocking boundaries but overlap this design space and are therefore not counted again as independent counterexamples. Together with baseline, strict-exit, frozen-exit-direction, and disclaimer-boundary checks, these form 118 review-search regression tests within the 276-test suite. The [R5 post-fix reevaluation](review-search-fifth-round-reevaluation-2026-08-30.md) preserves the initial 5/20 result and documents 20/20 after repair; the [R6 post-fix reevaluation](review-search-sixth-round-reevaluation-2026-08-30.md) likewise preserves the initial 3/12 result, including one strict false accept, and documents 12/12 after repair.

These are deterministic structural diagnostics, not estimates of real-world accuracy. The 118 review-search checks are part of the current 276-test suite. In particular, `systematic_record_structurally_complete` means that required textual signals were detected; it does not prove that a supplement exists, a database query runs, screening records are authentic, the review is reproducible, or current reporting guidance is satisfied.
