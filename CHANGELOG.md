# Changelog

## 0.4.0 — 2026-08-30

- Rewrote skill-selection metadata around high-intent scientific-writing tasks while keeping explicit negative boundaries for literature search alone, reference formatting alone, central-nervous-system queries, generic copywriting, and AI-detector evasion.
- Explicitly enabled implicit invocation in `agents/openai.yaml` and strengthened its task-facing short description and starter prompt.
- Added installable OpenAI/Codex and Claude Code plugin packages, repository marketplaces, and current standalone Agent Skills paths.
- Added bilingual positive and negative routing evaluations for manuscript polishing, Chinese-to-English rewriting, peer review, citation auditing, visual evidence, and near-neighbor non-target tasks.
- Added deterministic plugin-payload synchronization and discovery-metadata checks to CI so the standalone skill and marketplace package cannot silently drift.
- Reworked both README entry pages around concrete user requests and 30-second installation while preserving scientific-integrity boundaries.
- Added public privacy, terms, and support documents for transparent plugin distribution.

## 0.3.0 — 2026-08-30

- Made English the default final deliverable for SCI-journal and international-conference workflows, with Chinese retained for evidence locking, terminology, decisions, and risk reporting.
- Added a claim-first Chinese-to-English reconstruction and back-audit workflow.
- Added venue-aware profiles for Cell, Nature, Science, AAAI, CVPR, NeurIPS, ICML, and ICLR, with mandatory current-policy verification.
- Added figure, table, caption, graphical-abstract, accessibility, image-integrity, and rendered-visual QA rules.
- Added a dependency-free OpenAlex corpus analyzer and an auditable aggregate baseline of 320 abstracts across eight venues; no abstract text is redistributed.
- Added tests for corpus reconstruction, rhetorical-move diagnostics, aggregation, and privacy-preserving manifests.
- Removed a generic ordinal evidence ladder and required separate, namespaced axes so project-defined C0–C4 autonomy or other domain scales cannot be overwritten.
- Added a review-corpus lock, unified `M`/`N/A` scoring, explicit restructuring authority, and scope-aware visual handoff.
- Hardened audit tooling against input-file overwrite, swapped numeric assignments, Unicode signs, compound-unit drift, supplementary cross-reference collisions, CSV formulas, API rate limits, and accidental sharing of local paths or manuscript excerpts.

## 0.2.0 — 2026-08-30

- Defined **CNS** as **Cell, Nature, Science** and standardized the visible brand as **CNS Skills**.
- Added `CNS/top-venue` mode for top-journal and leading-conference revision.
- Added a 12-gate CNS Editorial Standard covering scientific importance, novelty, evidence, figures, reproducibility, integrity, and venue fit.
- Added journal-family, first-page, figure-first, and leading-conference review paths.
- Clarified that CNS is an independent quality benchmark and cannot guarantee acceptance or replace missing evidence.

## 0.1.0 — 2026-08-30

- Introduced the first evidence-first revision workflow.
- Added audit, revise, deep-review, and journal-ready modes.
- Added bilingual natural-academic-style guidance.
- Added claim–citation integrity and review-article references.
- Added a dependency-free DOCX/Markdown/text audit CLI with optional Crossref DOI checks.
- Added tests and continuous integration.
