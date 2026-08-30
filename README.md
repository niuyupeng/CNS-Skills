<div align="center">
  <img src="assets/cns-icon.svg" width="128" alt="CNS Skills logo">
  <h1>CNS Skills</h1>
  <p><strong>Claim-grounded · Natural · Scholarly</strong></p>
  <p>An evidence-first skill for scientific writing that sounds like a researcher because it reasons like one.</p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-0B6E69.svg)](LICENSE)
  [![CI](https://github.com/niuyupeng/cns-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/niuyupeng/cns-skills/actions/workflows/ci.yml)
  [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-123B5D.svg)](https://www.python.org/)
</div>

## Why CNS

Most “humanizers” work at the surface. Most academic-writing agents focus on search and citation formatting. Scientific revision needs both—and a strict order of operations.

CNS locks claims and evidence before it touches style. It then repairs the argument, gives each paragraph a job, removes formulaic language without flattening disciplinary meaning, audits claim–citation alignment, tests the manuscript through four skeptical readers, and verifies the final file as a rendered artifact.

```text
source lock → claim ledger → argument architecture → paragraph function
            → natural academic voice → citation audit → reader test → file QA
```

The priority is explicit:

> evidence integrity > meaning preservation > logic > voice > elegance

## What it does

- Revises Chinese and English scientific manuscripts, reviews, grants, and rebuttals.
- Separates computational prediction, experimental validation, and clinical/deployment evidence.
- Audits DOI existence, overclaiming, numeric claims, repeated templates, sentence rhythm, and citation proximity.
- Supports four modes: `audit`, `revise`, `deep-review`, and `journal-ready`.
- Preserves the source and requires rendered-file QA for DOCX/PDF deliverables.
- Provides a dependency-free CLI for `.docx`, `.md`, and `.txt` triage.

## What it refuses to do

CNS does not fabricate evidence, invent DOIs, blur preprints into published articles, or promise a “0% AI score.” AI-writing detectors are not a reliable scientific endpoint. CNS improves authentic authorial voice, argument quality, and evidential accountability; it does not help deceive editors or evade safeguards.

## Install

### Codex / skills-compatible agents

Clone the repository into your personal skills directory:

```bash
git clone https://github.com/niuyupeng/cns-skills.git ~/.codex/skills/cns-skills
```

Then invoke it explicitly:

```text
Use $cns-skills in deep-review mode on this review article.
Preserve all claims, audit every DOI, and return a clean DOCX plus unresolved evidence risks.
```

The `SKILL.md` workflow is portable to agents that support instruction skills. The included `agents/openai.yaml` provides Codex UI metadata.

## CLI audit

No third-party Python packages are required.

```bash
python scripts/cns_audit.py manuscript.docx
python scripts/cns_audit.py manuscript.docx --json cns-report.json
python scripts/cns_audit.py manuscript.docx --verify-dois --json cns-report.json
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

The report is triage, not a quality score or AI detector. Every flag must be interpreted in context.

## The workflow

1. **Source lock** — establish the authoritative draft, intended audience, fixed terminology, and allowed scope.
2. **Claim ledger** — connect consequential claims to scope, evidence, wording strength, and action.
3. **Architecture** — organize the document around a scientific decision rather than a catalogue of topics.
4. **Paragraph function** — make each paragraph perform one primary intellectual move.
5. **Natural voice** — replace stock framing with the real logical relationship while preserving technical nouns.
6. **Citation audit** — check existence, entailment, scope, and placement separately.
7. **Skeptical readers** — simulate a domain expert, methods reviewer, editor, and adjacent-field reader.
8. **Artifact QA** — render and inspect every page, table, figure, caption, and reference.

The full operating rules live in [SKILL.md](SKILL.md). Focused references cover [scientific integrity](references/scientific-integrity.md), [natural academic style](references/natural-academic-style.md), [review articles](references/review-article-mode.md), and the [evaluation rubric](references/evaluation-rubric.md).

## 中文快速开始

CNS = **Claim-grounded, Natural, Scholarly**，即“主张有据、表达自然、符合学术规范”。它不是简单的“降 AI 痕迹”工具，而是一套先核对事实与证据、再处理结构和语言的深度修订流程。

推荐提示词：

```text
使用 $cns-skills 的 deep-review 模式完善这篇中文综述。
以证据完整性为最高优先级，保留原始文献编号，核验 DOI 和发表状态，
减少模板化句式但不要口语化，最后逐页检查输出的 DOCX。
```

如果某一结论尚未被实验支持，CNS 会缩小表述或明确标注待核验，而不会用更漂亮的语言把不确定性藏起来。

## Design lineage

CNS was informed by several excellent open-source approaches: [`blader/humanizer`](https://github.com/blader/humanizer) and [`hannsxpeter/humanizer`](https://github.com/hannsxpeter/humanizer) for transparent prose-pattern editing; [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills) and [`claude-scientific-writer`](https://github.com/K-Dense-AI/claude-scientific-writer) for scientific workflows; Anthropic's [`doc-coauthoring`](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md) for staged collaboration; and John Kitchin's [`literature-review`](https://github.com/jkitchin/skillz/blob/main/skills/research/literature-review/SKILL.md) for citation-verification discipline.

CNS is an independent implementation. It combines these concerns around a claim-first architecture and adds bilingual naturalization, evidence-layer control, transparent CLI diagnostics, four-reader testing, and rendered-artifact QA.

## Roadmap

- [ ] CSL/BibTeX/RIS metadata adapters
- [ ] Claim-ledger export to CSV/JSON
- [ ] Journal-specific abstract and reporting checklists
- [ ] Anonymous before/after benchmark corpus with expert ratings
- [ ] Reference-manager and word-processor integrations

Contributions, benchmark manuscripts, language-specific pattern reports, and peer-review feedback are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Name and affiliation

“CNS” in this project means **Claim-grounded, Natural, Scholarly**. This project is not affiliated with or endorsed by *Cell*, *Nature*, *Science*, their publishers, OpenAI, Anthropic, or the referenced open-source projects.

## License

[MIT](LICENSE) © 2026 niuyupeng.
