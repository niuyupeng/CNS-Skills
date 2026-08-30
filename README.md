<div align="center">
  <img src="assets/cns-icon.svg" width="128" alt="CNS Skills logo">
  <h1>CNS Skills</h1>
  <p><strong>Cell · Nature · Science</strong></p>
  <p><strong>Scientific writing and manuscript revision for ChatGPT/Codex, Claude Code, and Agent Skills-compatible clients.</strong></p>
  <p>SCI paper polishing, Chinese-to-English academic rewriting, peer review, citation/DOI audits, and figure/table/caption QA for top journals and conferences.</p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-0B6E69.svg)](LICENSE)
  [![CI](https://github.com/niuyupeng/CNS-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/niuyupeng/CNS-Skills/actions/workflows/ci.yml)
  [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-123B5D.svg)](https://www.python.org/)
  [![Release](https://img.shields.io/github/v/release/niuyupeng/CNS-Skills?color=7A263A)](https://github.com/niuyupeng/CNS-Skills/releases)

  English · [简体中文](README.zh-CN.md)
</div>

## Start in 30 seconds

### ChatGPT desktop and Codex plugin

Add the public repository marketplace:

```bash
codex plugin marketplace add niuyupeng/CNS-Skills
```

Restart the ChatGPT desktop app, open the Plugins Directory, choose the **CNS Skills** source, install **CNS Skills**, and start a new chat. This repository package is ready for local/repository distribution; global listing in the shared ChatGPT/Codex directory still requires separate platform review.

### Claude Code plugin

```bash
claude plugin marketplace add niuyupeng/CNS-Skills
claude plugin install cns-skills@cns-skills
```

Claude can select the skill automatically from the task description. Explicit plugin invocation is `/cns-skills:cns-skills`.

### Standalone Agent Skill

For current ChatGPT desktop/Codex local discovery:

```bash
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.agents/skills/cns-skills
```

For Claude Code personal discovery:

```bash
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.claude/skills/cns-skills
```

The repository root remains a complete standalone skill. The versioned plugin payload is generated from that same source and checked for drift in CI.

Each GitHub release also provides a platform-uploadable `cns-skills-vX.Y.Z.zip` plus its SHA-256 checksum. The archive contains both OpenAI and Claude plugin manifests around the same provider-neutral skill.

## Ask naturally

You do not need a special prompt when implicit skill selection is enabled. Typical requests include:

- “Polish my SCI manuscript while preserving every claim and citation.”
- “Translate this Chinese draft into natural academic English, not a literal translation.”
- “Review this paper like Reviewer 2 for Nature/CVPR.”
- “Audit citation and DOI validity, claim support, and overclaiming.”
- “Revise my abstract, introduction, and discussion for a top journal.”
- “Design or audit manuscript figures, tables, captions, and a graphical abstract.”

Chinese requests such as “帮我润色这篇 SCI 论文”, “论文中译英”, “回复审稿人”, and “按顶刊/顶会标准审稿” route to the same English-final workflow when scholarly text is supplied. Literature search alone, reference-style conversion alone, generic copywriting, central-nervous-system questions, and AI-detector evasion should not trigger CNS Skills; the public [routing evaluation](evals/README.md) tests both positive and negative cases and states its limitations.

## Why CNS

**CNS means Cell, Nature, and Science.** The name states the benchmark: conceptual clarity, broad significance, evidential depth, disciplined claims, and communication that works beyond a narrow specialty. For conference papers, CNS applies the corresponding top-venue standards for technical novelty, fair baselines, ablations, reproducibility, and error analysis.

Most “humanizers” work at the surface. Most academic-writing agents focus on search and citation formatting. Top-venue revision needs both—and a strict order of operations.

CNS locks claims and evidence before it touches style. It then repairs the argument, gives each paragraph a job, removes formulaic language without flattening disciplinary meaning, audits claim–citation alignment, tests the manuscript through four skeptical readers, and verifies the final file as a rendered artifact.

For SCI journals and international conferences, **English is the default final deliverable**. Chinese remains available as a rigorous reasoning layer for evidence locking, terminology, author decisions, and revision explanations. CNS rebuilds the English argument from a claim map; it does not polish a sentence-by-sentence literal translation.

```text
source lock → claim ledger → argument architecture → paragraph function
            → natural academic voice → citation audit → reader test → file QA
```

The priority is explicit:

> evidence integrity > meaning preservation > logic > voice > elegance

| Verifiable component | Included in v0.4.0 |
|---|---|
| selective-venue review | 12 editorial gates and 8 named venue profiles |
| writing baseline | 320 sampled English abstracts with disclosed years and bias limits |
| bilingual safety | claim reconstruction, protected-token diff, terminology and MQM-style audit |
| visual evidence | figure/table contracts, captions, provenance, accessibility, final-size QA |
| transparent tooling | 3 dependency-free CLI auditors and 35 deterministic tests |

The corpus informs judgment but supplies no text-generation template. The tools expose what they check and where they can fail.

## What it does

- Produces submission English from English or Chinese source drafts, with an optional Chinese decision and risk map.
- Revises Chinese and English scientific manuscripts, reviews, grants, and rebuttals.
- Separates computational prediction, experimental validation, and clinical/deployment evidence.
- Audits DOI existence, overclaiming, numeric claims, repeated templates, sentence rhythm, and citation proximity.
- Supports five modes: `audit`, `revise`, `deep-review`, `journal-ready`, and `CNS/top-venue`.
- Runs a 12-gate CNS editorial review covering the central claim, importance, novelty, evidence chain, alternative explanations, robustness, narrative, figures, accessibility, reproducibility, integrity, and venue fit.
- Adds venue-aware review paths for Cell, Nature, Science, AAAI, CVPR, NeurIPS, ICML, and ICLR while requiring current official instructions to be rechecked.
- Designs and audits figure stories, plots, evidence tables, captions, graphical abstracts, accessibility, provenance, and final-size rendering.
- Preserves the source and requires rendered-file QA for DOCX/PDF deliverables.
- Provides a dependency-free CLI for `.docx`, `.md`, and `.txt` triage.

## What it refuses to do

CNS does not fabricate evidence, invent DOIs, blur preprints into published articles, or promise a “0% AI score.” It also does not guarantee editorial triage, peer-review success, conference acceptance, or citation impact. AI-writing detectors are not a reliable scientific endpoint. CNS improves authentic authorial voice, argument quality, and evidential accountability; it does not help deceive editors or evade safeguards.

## CLI audit

No third-party Python packages are required.

```bash
python scripts/cns_audit.py manuscript.docx
python scripts/cns_audit.py manuscript.docx --json cns-report.json
python scripts/cns_audit.py manuscript.docx --verify-dois --shareable --json cns-report.json
python scripts/check_invariants.py chinese-source.docx english-revision.docx --shareable --json invariants.json
python scripts/check_crossrefs.py english-revision.docx --shareable --json crossrefs.json
```

Example output:

```text
CNS manuscript audit
Characters: 18422 | paragraphs: 97 | sentences: 286 | DOIs: 43
Sentence length mean/CV: 61.4 / 0.51
Stock phrase patterns: 4 pattern(s)
Repeated contrast patterns: 2 pattern(s)
DOI verification: verified=41, not_found=2
```

The tools report prose patterns, claim-risk language, DOI status, changes to numbers/units/statistics/citations, and broken figure/table references. They do not edit files, prove translation equivalence, assign a quality score, or act as AI detectors. Every flag must be interpreted in context. Full JSON reports can contain local paths and unpublished manuscript excerpts; treat them as confidential or use `--shareable` to redact those fields before sharing.

## Reproducible venue-language baseline

Version 0.3.0 introduced a dependency-free analyzer and an auditable **320-abstract** baseline, retained in v0.4.0: 40 sampled abstracts each from Cell, Nature, Science, AAAI, CVPR, NeurIPS, ICML, and ICLR.

```bash
python scripts/venue_corpus_analyzer.py --per-venue 40 --seed 20260830
```

The analyzer reconstructs abstracts only in memory. It stores aggregate metrics and a title/identifier manifest, not abstract text. The findings are descriptive—not a style-transfer corpus, acceptance model, or fixed length template. Conference-year coverage is disclosed in the [method note](references/venue-corpus-findings.md).

## The workflow

1. **Source lock** — establish the authoritative draft, intended audience, fixed terminology, and allowed scope.
2. **Claim ledger** — connect consequential claims to scope, evidence, wording strength, and action.
3. **Architecture** — organize the document around a scientific decision rather than a catalogue of topics.
4. **Paragraph function** — make each paragraph perform one primary intellectual move.
5. **Natural voice** — replace stock framing with the real logical relationship while preserving technical nouns.
6. **English-final bridge** — compose from the claim map, run field-native language QA, and back-audit against the source.
7. **Citation audit** — check existence, entailment, scope, and placement separately.
8. **Visual evidence** — make figures and tables carry auditable claims with honest uncertainty and complete captions.
9. **CNS Editorial Gate** — test the central claim, significance, novelty, evidence chain, alternative explanations, robustness, figure story, accessibility, reproducibility, integrity, and venue fit.
10. **Skeptical readers** — simulate a domain expert, methods reviewer, editor, and adjacent-field reader.
11. **Artifact QA** — render and inspect every page, table, figure, caption, and reference.

The full operating rules live in [SKILL.md](SKILL.md). Focused references cover the [English-first bilingual workflow](references/english-first-bilingual.md), [CNS Editorial Standard](references/cns-editorial-standard.md), [venue profiles](references/venue-profiles.md), [figures and tables](references/figures-tables.md), [scientific integrity](references/scientific-integrity.md), [natural academic style](references/natural-academic-style.md), [review articles](references/review-article-mode.md), [corpus findings](references/venue-corpus-findings.md), [license and provenance](references/license-and-provenance.md), and the [evaluation rubric](references/evaluation-rubric.md).

## 中文快速开始

CNS = **Cell · Nature · Science**。这个名字代表目标标准：用顶刊编辑和审稿人的视角，检查中心发现、广泛意义、证据闭环、图表叙事、可复现性与表达质量；面向顶会时，则进一步检查强基线、公平比较、消融、误差分析和复现条件。它不是简单的“降 AI 痕迹”工具。

推荐提示词：

```text
使用 $cns-skills 的 English-final + CNS/top-venue 模式完善这篇中文综述，目标为 Nature 系列期刊。
运行 12 项编辑门槛审查，保留原始文献编号，核验 DOI、发表状态与证据边界，
从主张—证据图重写英文稿，而不是逐句直译；重构摘要和图表叙事，
最后输出英文 DOCX、中文关键修改说明，并逐页检查成稿。
```

如果某一结论尚未被实验支持，CNS 会缩小表述或明确标注待核验，而不会用更漂亮的语言把不确定性藏起来。

## Design lineage

CNS was informed by several excellent open-source approaches: [`blader/humanizer`](https://github.com/blader/humanizer) and [`hannsxpeter/humanizer`](https://github.com/hannsxpeter/humanizer) for transparent prose-pattern editing; K-Dense's [`scientific-writing`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) and [`scientific-visualization`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md) for manifests, consistency gates, and visual provenance; [`research-paper-lifecycle-skills`](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills) for modular PASS/WARN/FAIL workflows; Anthropic's [`doc-coauthoring`](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md) for staged collaboration; John Kitchin's [`literature-review`](https://github.com/jkitchin/skillz/blob/main/skills/research/literature-review/SKILL.md) for citation-verification discipline; and the open [MQM framework](https://www.themqm.org/) for bilingual error taxonomy.

CNS is an independent implementation. It does not copy proprietary phrasebanks or publisher text. It combines these concerns around a claim-first architecture and adds English-first Chinese-to-English reconstruction, evidence-layer control, deterministic invariant and cross-reference checks, aggregate venue research, four-reader testing, and rendered-artifact QA.

## Roadmap

- [ ] CSL/BibTeX/RIS metadata adapters
- [ ] Claim-ledger export to CSV/JSON
- [x] English-first Chinese-to-English claim reconstruction
- [x] Cell/Nature/Science and AAAI/CVPR/NeurIPS/ICML/ICLR editorial profiles
- [x] Reproducible 320-abstract aggregate venue baseline
- [ ] Machine-checkable journal-specific formatting adapters
- [ ] Anonymous before/after benchmark corpus with expert ratings
- [ ] Reference-manager and word-processor integrations

Contributions, benchmark manuscripts, language-specific pattern reports, and peer-review feedback are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Name and affiliation

“CNS” in this project means **Cell, Nature, and Science** as an aspirational editorial benchmark. This independent project is not affiliated with or endorsed by those journals, their publishers, any conference, OpenAI, Anthropic, or the referenced open-source projects. The names are used descriptively; no acceptance or publication outcome is promised.

## License

[MIT](LICENSE) © 2026 niuyupeng.
