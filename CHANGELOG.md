# Changelog

## Unreleased

## 0.10.0 — 2026-08-31

- Added separate Review, original research Article, and leading-conference modes. The Review path synthesizes cross-study evidence, the Article path follows an inference-led Results and figure sequence, and the conference path locks year, track, submission phase, page budget, comparators, robustness, and error analysis instead of transferring one generic top-venue template.
- Added Review visual-architecture guidance that distinguishes venue-specific quantity limits from functional coverage across scope, synthesis, decision, and evidence boundary. A public purposive audit of 14 published Reviews reports an independent-display median of 7 and main-figure median of 4; the *Nature Reviews* subset (n=8) had a main-figure median of 5. These values are design calibration, not quotas, prevalence estimates, or acceptance predictors.
- Expanded the official-source visual record for Nature Reviews and Cell Press Review displays while preserving rule classes and the prohibition on transferring figure counts, three-line-table examples, or generative-image permissions across venues and article types.
- Added repeatable `--companion` inputs to `check_crossrefs.py` so a main manuscript and supplementary artifacts can be audited jointly without turning a legitimate cross-file reference into a false missing-caption result. JSON overwrite protection now covers every supplied companion.
- Expanded deterministic regression coverage from 231 to 241 tests. Advanced skill, CLI, citation, Codex, Claude, marketplace, and generated-plugin metadata to 0.10.0; the public tool set remains nine transparent local tools.

## 0.9.0 — 2026-08-31

- Added an evidence-bounded scientific-visual production route backed by current official-source checks and a public design-lineage note. Quantitative figures route to declared data and code, experimental images require authentic observations and auditable transformations, review schematics route to editable SVG, and conceptual generative art remains conditional on the exact venue policy and disclosure route.
- Added a publication-neutral three-line-table default for ordinary SCI manuscript tables when the verified venue does not prescribe another style: top, header-bottom, and bottom rules without vertical grids or decorative fill. This is explicitly a default, not a universal journal mandate.
- Added `visual_audit.py`, a dependency-free DOCX visual auditor that resolves inherited Word table styles and checks table rules/fills, caption placement and styles, figure placement and alt text, raster dimensions, and effective DPI. Its visual gate remains separate from the clean-copy gate and does not certify scientific truth, image integrity, or venue compliance.
- Added `figure_brief.py` to lock the reader question, supported claim, prohibited inference, source, deliverables, and venue status before production. It routes data figures to code, blocks generative experimental imagery, and permits conceptual generation only after policy clearance.
- Added `render_concept_svg.py` for deterministic, editable `flow` and `independent_axes` SVG schematics with real text and accessibility metadata. These outputs are concept figures, not substitutes for data figures or experimental evidence.
- Expanded the figure and table manifests with production/provenance fields, documented editable SVG and data/code provenance, and strengthened the license/disclosure boundary without importing third-party prompts, templates, code, or publisher artwork.
- Expanded deterministic regression coverage from 191 to 231 tests and the public local-tool set from six auditors to nine transparent tools. Advanced skill, CLI, citation, Codex, and Claude release metadata to 0.9.0.

## 0.8.0 — 2026-08-30

- Added article-type-aware scientific-title optimization and a transparent title auditor, grounded in two deliberately separate 100-record metadata panels: a 70 elite-journal plus 30 accepted main-conference core, and a topic-matched field comparison. Fifty DOI records overlap the panels, yielding 150 distinct titles; these are title studies, not full-paper readings or acceptance rules.
- Added a genre-separated 600-record research corpus covering 200 top Reviews, 200 original research Articles, and 200 accepted leading-conference papers, with per-record provenance, actual title/abstract/full-text analysis levels, and explicit missingness and selection-bias boundaries.
- Added `review_search_audit.py` to distinguish concise narrative scope disclosure, query-shaped but non-reproducible keyword inventories, and incomplete systematic-review records without forcing PRISMA machinery onto narrative Reviews.
- Added genre-aware transfer guidance so Review, original Article, and conference conventions are compared by rhetorical and evidential function rather than copied as surface templates.
- Expanded discovery coverage to 68 bilingual cases and deterministic regression coverage to 191 tests, including 118 review-search tests built around 93 independently designed search-disclosure counterexamples and strict-gate checks; the generated plugin includes the new references and auditors. The frozen R6 holdout is preserved both before repair (3/12 full-field, including one strict false accept) and after repair (12/12), without presenting either result as real-world accuracy.

## 0.7.0 — 2026-08-30

- Added a final clean-submission-copy gate that separates reader-visible manuscript prose from author queries, editorial judgments, prompts, scorecards, and production notes.
- Added DOCX package checks for repeated unnumbered 1×1 shaded callouts, table titles misusing Heading styles, table-font drift, external filename leakage, and tool/draft/version language in core properties.
- Added context protections for formally numbered boxes, venue-required Key Points, and scientifically necessary classifications; compact labels are retained only when their constructs and categories are defined.
- Added `--strict-clean-copy`, which returns a dedicated nonzero exit code when unresolved clean-copy defects remain, and excluded reference lists from prose-rhythm diagnostics by default.
- Expanded deterministic audit coverage from 45 to 60 tests, including held-out forward checks against a contaminated manuscript and its clean distribution copy.

- Rebuilt the English and Chinese GitHub landing pages around **evidence-first manuscript engineering**, with a flagship workflow, a synthetic evidence-boundary demonstration, a verifiable proof matrix, and direct install/star/citation calls to action.
- Added a 1280×640 brand hero and social-preview asset for consistent repository sharing.
- Strengthened citation metadata without implying publisher affiliation or editorial certification.
- Added privacy-aware issue forms and a scientific-integrity pull-request checklist to lower the barrier for serious community contributions.
- Updated GitHub Actions to current Node 24-compatible `actions/checkout@v7` and `actions/setup-python@v7` releases.

## 0.6.0 — 2026-08-30

- Added argument-gap-driven review expansion with an explicit evidence-state machine and a clear structured-narrative versus systematic-review boundary.
- Expanded citation QA from four to six axes: existence, metadata/status, entailment, scope, placement, and independence.
- Added action/autonomy/validation boundary checks; animal validation alone does not establish a high-autonomy or `C4` closed loop.
- Added a defect-to-rule gate so manuscript lessons enter CNS Skills only after counterexample review and held-out forward testing.
- Added `review_citation_audit.py`, a dependency-free numeric-reference and section-coverage audit for DOCX, Markdown, and text, with shareable JSON output.
- Expanded bilingual routing evaluations from 34 to 64 cases and locked a balanced 30-case held-out split with a canonical SHA-256 digest.
- Documented blind A/B naturalness evaluation while preserving the prohibition on AI-detector optimization or evasion claims.
- Expanded open-source design research and strengthened license boundaries: learn principles, record provenance, and do not copy source-available or proprietary content without permission.
- Advanced plugin, marketplace, citation, and CLI version metadata to 0.6.0; the generated plugin now includes the new reference and audit tool.

## 0.5.0 — 2026-08-30

- Added a review-prose naturalness workflow that keeps editorial scaffolding—claim ledgers, evidence cards, evidence chains, comparison frameworks, and evidence profiles—backstage unless the terminology is scientifically necessary.
- Added bilingual, contextual editorial-scaffolding diagnostics to `cns_audit.py`; legitimate uses of datasets, named frameworks, and concrete experimental evidence are not treated as automatic failures.
- Added review-specific guidance to replace meta-language with the actual study, material, measurement, result, comparison, or limitation, without weakening claims or deleting field terms mechanically.
- Expanded deterministic audit tests and advanced all public plugin, marketplace, citation, and CLI version metadata to 0.5.0.

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
