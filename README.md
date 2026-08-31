<p align="center">
  <img src=".github/assets/cns-skills-hero.svg" width="100%" alt="CNS Skills — from research decisions to a defensible submission manuscript">
</p>

<div align="center">

## Make every claim earn its place.

**Evidence-first manuscript engineering for top journals and conferences.**

CNS Skills is an open-source scientific-writing Agent Skill for ChatGPT/Codex, Claude Code, and compatible clients. It takes author-owned research from positioning and outline through an evidence-bounded first draft, English reconstruction, figures, tables, peer review, and final-file QA—without inventing the science or leaking the planning machinery into the paper.

[**Quick install**](#quick-install) · [**Public demo**](examples/synthetic-hydrogel-demo/README.md) · [**Run the flagship workflow**](#run-the-flagship-workflow) · [**See the proof**](#proof-not-hype) · [**Cite CNS Skills**](#cite-cns-skills) · [简体中文](README.zh-CN.md)

[![Release](https://img.shields.io/github/v/release/niuyupeng/CNS-Skills?label=release&color=E9B44C)](https://github.com/niuyupeng/CNS-Skills/releases)
[![CI](https://github.com/niuyupeng/CNS-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/niuyupeng/CNS-Skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-0B6E69.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/standard-Agent_Skills-123B5D.svg)](https://agentskills.io/)
[![Cite](https://img.shields.io/badge/cite-CITATION.cff-7A263A.svg)](CITATION.cff)

**12 editorial gates · 8 venue profiles · 320-abstract baseline · 600-record genre corpus · two 100-title panels (150 distinct titles) · 76 routing cases · 276 deterministic tests · 10 transparent local tools**

<sub>Independent MIT-licensed project. CNS means Cell · Nature · Science as an aspirational editorial benchmark; it does not imply affiliation, endorsement, or acceptance.</sub>

</div>

---

## What CNS Skills is

Sentence-level polishing is only one layer. **CNS Skills develops the manuscript without outrunning the science.**

It first distinguishes author decisions, verified evidence, format-only references, assistant proposals, and superseded directions. From there it can position the paper, build an argument-led outline and evidence matrix, or draft only what the supplied science supports. It then routes a Review, an original research Article, or a leading-conference paper to a separate argument and visual contract; reconstructs submission English; audits claim–citation fit; strengthens the figure story; and—when the host provides document rendering—verifies the rendered DOCX or PDF.

The result is not generic “AI-sounding academic prose.” It is a manuscript whose contribution is easier to see, whose claims are easier to defend, and whose unresolved risks are harder to hide.

| Where sentence-level polishing stops | Where CNS Skills continues |
|---|---|
| smoother sentences | central claim, significance, novelty, and paragraph logic |
| a topic list called an outline | an explicit architecture hierarchy, section jobs, evidence roles, display roles, and an exact artifact budget |
| a prompt expanded into a complete paper | an author-led sufficiency gate: topic → provisional plan; approved sources → evidence-bounded draft |
| several files treated as equally authoritative | explicit content, evidence, format, visual, proposal, and superseded-decision roles |
| literal Chinese-to-English translation | claim-first English reconstruction plus bilingual back-audit |
| reference formatting | DOI/status, entailment, scope, placement, and independence checks |
| attractive figures | evidence class, data/code or authentic-image provenance, editable SVG, caption, accessibility, and final-size QA |
| a clean-looking file | invariant checks, cross-references, tables, comments, tracked changes, and page rendering |
| “sounds publishable” | explicit reviewer risks, missing evidence, and venue-fit limits |

> **The rule:** evidence integrity > meaning preservation > logic > authorial voice > elegance.

### One evidence-boundary example

This synthetic example shows the difference between surface polishing and evidence-bounded revision:

| Supplied evidence | Original sentence | CNS audit | Evidence-bounded revision |
|---|---|---|---|
| one *in vitro* experiment | “This platform enables clinical translation.” | the clinical claim exceeds the reported validation | “The platform improved X *in vitro*; *in vivo* performance and clinical utility remain untested.” |

One request can return an **argument-led outline · evidence-bounded first draft or revised manuscript · decision/risk map · citation audit · figure/table QA · rendered-file check when the host supports document rendering**.

The [public synthetic demo](examples/synthetic-hydrogel-demo/README.md) provides the complete input, revised manuscript, shareable audit report, and rendered DOCX example without using confidential research.

## Run the flagship workflow

Attach your approved research materials or manuscript and ask naturally. For source-to-draft work:

```text
Use $cns-skills to lock the article type, reader, current author decisions, source roles, and evidence boundary.
Build an argument-led outline with an explicit architecture hierarchy, section contracts, anchor evidence, and display roles.
Draft only from my approved outline, verified literature, results, notes, figures, and protocols.
Keep decision provenance, evidence states, prompts, TODOs, and editorial labels outside the reader-visible manuscript.
Use English as the final submission language, return unresolved author questions separately, and verify the requested file and page/word budget.
```

For a supplied full manuscript:

```text
Use $cns-skills in English-final + CNS/top-venue mode to revise this manuscript.
Preserve every supported scientific claim, number, citation, and project-defined scale.
Rebuild the argument in field-native submission English rather than translating line by line.
Audit overclaiming, DOI/status, claim–citation alignment, figures, tables, captions, and cross-references.
Read as a domain expert, methods reviewer, editor, and adjacent-field reader.
Return the revised file, a concise decision/risk log, and verify every rendered page.
```

Other high-value requests:

- “Use these meeting notes and verified papers to produce a two-page Review outline; the old outline is format-only.”
- “Turn my approved outline, evidence cards, figures, and lab notes into an English first draft without filling unsupported gaps.”
- “Build a traceable evidence matrix that separates discovered records, DOI/status checks, exact support, validation setting, and pending fields.”
- “Explain this manuscript's central contribution and strongest evidence boundary in exactly one sentence.”
- “Turn this Chinese SCI draft into natural submission English without changing the science.”
- “Review this paper like a demanding Nature or CVPR reviewer.”
- “Strengthen the abstract, introduction, and discussion around one defensible central claim.”
- “Audit every consequential claim against its citation and identify overclaiming.”
- “Expand this review from argument gaps, not from a target reference count.”
- “Read the manuscript, then optimize its English and Chinese scientific titles without overstating the contribution.”
- “Route each figure to data/code, authentic experimental imagery, editable SVG, or policy-cleared conceptual art.”
- “Convert these manuscript tables to the verified venue style or the neutral three-line default, then audit the DOCX.”
- “Prepare an evidence-faithful rebuttal and response-to-reviewers letter.”

When implicit selection is enabled, no special syntax is required. The public [routing evaluation](evals/README.md) includes manuscript tasks and close non-target requests so CNS does not hijack generic translation, identifier lookup, reference-style conversion, central-nervous-system questions, or AI-detector evasion.

## Quick install

### ChatGPT desktop / Codex plugin

```bash
codex plugin marketplace add niuyupeng/CNS-Skills
```

Restart the ChatGPT desktop app, open the Plugins Directory, select the **CNS Skills** source, and install **CNS Skills**. The repository package supports local and repository distribution; listing in a shared global directory remains subject to platform review.

### Claude Code plugin

```bash
claude plugin marketplace add niuyupeng/CNS-Skills
claude plugin install cns-skills@cns-skills
```

Claude can select the skill from the task. Explicit invocation is `/cns-skills:cns-skills`.

### Standalone Agent Skill

```bash
# ChatGPT desktop / Codex
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.agents/skills/cns-skills

# Claude Code
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.claude/skills/cns-skills
```

Releases from v0.4.0 onward include a platform-uploadable ZIP and a SHA-256 checksum. The root skill and generated plugin payload are checked for drift in CI.

For prerequisites, verification, updates, removal, and troubleshooting, use the [complete installation guide](docs/INSTALL.md).

## Proof, not hype

Every number below is inspectable in this repository.

| Public verification asset | What it establishes | What it does **not** establish |
|---|---|---|
| [12-gate editorial standard](references/cns-editorial-standard.md) | a documented 12-dimension selective-venue review surface | acceptance by any journal or conference |
| [8 venue profiles](references/venue-profiles.md) | distinct journal/conference review paths | permanent substitution for current official policies |
| [visual-production workflow](references/visual-production.md) and [source study](research/visual-production-study.md) | an inspectable route from reader question and evidence class to data/code, authentic images, editable SVG, policy-cleared conceptual art, or a Review-plan audit | a universal journal style, permission to fabricate experimental imagery, or automatic venue compliance |
| [320-abstract aggregate baseline](references/venue-corpus-findings.md) | reproducible descriptive venue-language checks | a style-transfer corpus or acceptance model |
| [600-record genre corpus](research/genre-corpus-2026/README.md) | separately audited Review, original Article, and top-conference writing mechanisms with per-record provenance and text-level disclosure | 600 expert close readings, field-wide prevalence, or an acceptance model |
| [three genre-specific playbooks](references/genre-aware-top-venue-writing.md) | separate Review synthesis, original-Article inference, and page-budgeted conference contribution/evaluation logic | one transferable top-venue template or a fixed display count |
| [author-led development workflow](references/manuscript-development.md), [defect study](research/author-led-manuscript-development-study.md), and [synthetic plan contract](assets/manuscript_development_plan.json) | explicit positioning, source authority, outline, evidence, drafting, data-readiness, backstage-scaffold, and completion rules derived from longitudinal failures | source truth, literature completeness, hidden ghostwriting, or automatic manuscript authorship |
| [14-paper Review visual audit](research/top-review-visual-architecture-study.md) | a purposive aggregate calibration: median 7 independent displays and 4 main figures; the *Nature Reviews* subset (n=8) had a main-figure median of 5 | a universal quota, representative prevalence, or an acceptance predictor |
| [100-title elite core](research/elite-venue-title-study.md) | 70 elite-journal titles with DOI metadata plus 30 accepted 2025 main-conference titles with official stable IDs | 100 full-paper readings, a title formula, or an acceptance model |
| [100-title field layer](research/field-journal-title-study.md) | a second topic-matched panel retaining strong field venues including *ACS Nano*, *Advanced Functional Materials*, *Acta Biomaterialia*, and *Biomaterials*; 50 DOI records overlap the core, leaving 150 distinct titles across both panels | 200 distinct titles, a pooled prestige average, or a reason to override article type |
| [76 bilingual routing cases](evals/README.md) | positive and negative discovery regression coverage | guaranteed activation in every agent host |
| 30-case locked held-out split | resistance to metadata overfitting | an external benchmark leaderboard |
| [276 deterministic tests](tests) | observable invariants and CLI behavior, including 118 review-search tests built around 93 independently designed counterexamples, biomedical Review-plan counterexamples, and 22 manuscript-development regressions | semantic proof that every edit is correct |
| 10 dependency-free local tools | transparent manuscript planning diagnostics, safe visual routing, and deterministic concept-SVG generation | source-reading, image-integrity judgment, or author approval |
| source/plugin synchronization in CI | packaged payload matches the root skill | endorsement by OpenAI, Anthropic, or a publisher |

The project deliberately refuses unverifiable marketing claims. There is no fabricated “success rate,” user count, citation count, acceptance rate, or detector-evasion score.

## The CNS Editorial Gate

The `CNS/top-venue` mode tests a manuscript across twelve connected gates:

1. central claim;
2. broad significance;
3. novelty and prior-art boundary;
4. evidence chain;
5. alternative explanations;
6. robustness and generalization;
7. narrative architecture;
8. figure and table story;
9. accessibility across fields;
10. reproducibility and reporting;
11. scientific integrity;
12. exact venue fit.

Cell, Nature, Science, AAAI, CVPR, NeurIPS, ICML, and ICLR have separate profiles. Current official author instructions remain authoritative.

```text
decision/source lock → positioning → outline + evidence matrix → bounded draft
                     → genre argument → natural submission English
                     → citation + visual audit → clean copy → rendered-file QA
```

Eight primary modes keep the artifact proportional to the task: `positioning`, `outline`, `author-led draft`, `audit`, `revise`, `deep-review`, `journal-ready`, and `CNS/top-venue`. Evidence-matrix, plain-language, English-final, bilingual, title, and visual tracks can be added as needed.

## Scientific visuals without invented evidence

CNS classifies a display before choosing a production tool:

| Display class | Default route | Non-negotiable boundary |
|---|---|---|
| quantitative or statistical figure | declared data + plotting code + editable vector export | no image generator and no invented values |
| microscopy, gels/blots, pathology, spectra, or other experimental image | authentic source observation + auditable transformations | no generative creation or content alteration |
| review flow, taxonomy, comparison, or independent-axis schematic | original, deterministic editable SVG with real text and semantic groups | no unsupported causal arrows, rankings, maturity scales, or copied commercial assets |
| conceptual art or graphical abstract | only after the exact venue policy and disclosure route are cleared | illustrative content cannot substitute for data or experimental evidence |

For an ordinary SCI manuscript table whose exact venue does not prescribe another style, CNS uses a publication-neutral three-line default: top, header-bottom, and bottom rules; no vertical grid or decorative fill. This is a default, not a claim that every SCI journal mandates three-line tables. The current venue template always controls.

The visual brief preserves the reader question, supported claim, prohibited inference, provenance, deliverables, and venue status. The same tool audits a Review visual portfolio against six distinct roles: graphical abstract, overview, workflow, framework, evidence synthesis, and roadmap. The concept renderer supports editable `flow` and `independent_axes` SVGs; quantitative figures still require their underlying data and code. The DOCX visual auditor resolves inherited table styles, so a `Table Grid` table cannot pass merely because its direct formatting omits borders.

For biomedical Reviews, CNS can require an object-based scene grammar—scientific object → experimental action → measurement/test → decision or feedback → evidence boundary—and flags static card/box stacks or icons with no scientific role. When the argument depends on comparing studies, at least one main-text figure must perform genuine cross-study evidence synthesis; a second workflow cannot replace it.

For Reviews, CNS checks both the venue's quantity boundary and the display sequence's function. The public 14-paper audit is a design calibration only: its medians prompt a check for missing scope, synthesis, decision, or boundary functions; they never prescribe how many figures another Review should contain. Six figures plus one table may fit one manuscript, but it is not a CNS default or a transferable quota.

CNS does not copy BioRender assets, templates, or visual identity. It transfers only general principles such as object-based biomedical semantics, clear hierarchy, and a readable path, then implements original geometry and records the licence and redistribution status of any author-supplied third-party component.

## Ten transparent local tools

The CLI requires Python 3.9+ and no third-party packages.

```bash
python scripts/cns_audit.py manuscript.docx --strict-clean-copy
python scripts/cns_audit.py manuscript.docx --verify-dois --shareable --json cns-report.json
python scripts/review_citation_audit.py review.docx --shareable --json review-citations.json
python scripts/review_search_audit.py review.docx --shareable --json review-search.json
python scripts/title_audit.py "Provisional manuscript title"
python scripts/manuscript_plan.py assets/manuscript_development_plan.json --json manuscript-plan-audit.json
python scripts/check_invariants.py source.docx revision.docx --shareable --json invariants.json
python scripts/check_crossrefs.py revision.docx --shareable --json crossrefs.json
python scripts/visual_audit.py revision.docx --expect-three-line --strict --shareable --json visual.json
python scripts/figure_brief.py figure-brief.json --json routed-brief.json
python scripts/figure_brief.py assets/review_visual_plan.json --json review-visual-audit.json
python scripts/render_concept_svg.py figure-spec.json figure.svg
```

The audit and checking tools report source-authority conflicts, unsupported drafting, exposed editorial scaffolding, risky claim language, DOI status, review-search disclosure, title architecture, changed scientific invariants, broken cross-references, clean-copy defects, inherited table grids and fills, figure captions, alt text, placement, and effective raster DPI. `manuscript_plan.py` audits the declared development contract; it does not verify that a source is true. `figure_brief.py` returns a bounded production route and refuses generative experimental imagery; `render_concept_svg.py` creates editable concept schematics, not data figures. These tools do not determine citation entailment, prove translation equivalence or image integrity, certify venue compliance, predict acceptance, or act as AI detectors. Non-shareable JSON can contain local paths and unpublished excerpts; use `--shareable` before external distribution.

The full operating contract is [SKILL.md](SKILL.md). Focused references cover [author-led manuscript development](references/manuscript-development.md), [English-first bilingual writing](references/english-first-bilingual.md), [scientific-title optimization](references/scientific-title-optimization.md), [Review writing](references/review-article-mode.md), [Review visual architecture](references/review-visual-architecture.md), [original research Articles](references/original-research-article-mode.md), [leading-conference papers](references/leading-conference-paper-mode.md), [genre-aware transfer](references/genre-aware-top-venue-writing.md), [iterative Review development](references/iterative-review-development.md), [figures and tables](references/figures-tables.md), [scientific visual production](references/visual-production.md), [scientific integrity](references/scientific-integrity.md), and [venue profiles](references/venue-profiles.md).

## Cite CNS Skills

If CNS Skills strengthens a manuscript, review, rebuttal, or research-writing workflow, please **star the repository and cite the software**. Those two signals help other researchers find a rigor-first alternative to generic paper “humanizers.”

GitHub exposes **Cite this repository** from the root [CITATION.cff](CITATION.cff). A copyable BibTeX entry is also provided here:

```bibtex
@software{niu_cns_skills_2026,
  author  = {Niu, Yupeng},
  title   = {CNS Skills: Evidence-First Scientific Manuscript Development and Quality Assurance},
  year    = {2026},
  version = {0.12.0},
  url     = {https://github.com/niuyupeng/CNS-Skills}
}
```

**[Star CNS Skills](https://github.com/niuyupeng/CNS-Skills)** · **[Open the citation file](CITATION.cff)** · **[Download the latest release](https://github.com/niuyupeng/CNS-Skills/releases/latest)**

## Community

The fastest path to a stronger public scientific-writing skill is inspectable criticism.

- Share a workflow or ask a design question in [Discussions](https://github.com/niuyupeng/CNS-Skills/discussions).
- Report a reproducible defect or propose a capability in [Issues](https://github.com/niuyupeng/CNS-Skills/issues).
- Contribute a test, venue correction, language pattern, or privacy-safe benchmark through [CONTRIBUTING.md](CONTRIBUTING.md).
- See the public [roadmap and changelog](CHANGELOG.md) before proposing overlapping work.

<details>
<summary><strong>Design lineage, licensing, and non-copying boundary</strong></summary>

CNS learns reusable principles from inspectable open projects without copying their prose or implementation. The [Agent Skills specification](https://github.com/agentskills/agentskills), [OpenAI Plugins](https://github.com/openai/plugins), and [Anthropic Skills](https://github.com/anthropics/skills) inform packaging and progressive disclosure. [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills), [PaperQA2](https://github.com/Future-House/paper-qa), [OpenScholar](https://github.com/AkariAsai/OpenScholar), [ScholarQABench](https://github.com/AkariAsai/ScholarQABench), and [`ai-peer-review`](https://github.com/poldrack/ai-peer-review) inform auditable scientific workflows, grounded synthesis, and independent-reader evaluation. The open [MQM framework](https://www.themqm.org/) informs typed bilingual-error review.

The [open-source review](research/open-source-skill-review.md) records per-project lessons and license boundaries. Publicly visible is not synonymous with open source: no proprietary phrasebank, publisher text, or source-available document-skill content is copied.

</details>

## Name, affiliation, and limits

“CNS” means **Cell, Nature, and Science** as an aspirational benchmark for clarity, significance, evidence, and cross-disciplinary communication. CNS Skills is independent and is not affiliated with or endorsed by those journals, their publishers, any conference, OpenAI, Anthropic, or the referenced projects.

It does not fabricate evidence, invent references, disguise unsupported claims, guarantee editorial triage or acceptance, or optimize for AI-detector evasion. When the science does not support the intended story, CNS narrows the claim and identifies what evidence or analysis is still missing.

## License

[MIT](LICENSE) © 2026 Yupeng Niu.
