# Open-source skill and tooling review

Snapshot: 2026-08-30. This review documents design lineage; it does not imply endorsement, affiliation, or code reuse.

## Selection criteria

Projects were screened for transparent workflow design, scientific integrity, bilingual QA, figure/table provenance, deterministic checks, active or inspectable source, and a license that could be identified. GitHub visibility alone was not treated as permission to copy or redistribute.

| Project | License observed | Design lesson used by CNS Skills | Boundary |
|---|---|---|---|
| [Agent Skills specification](https://github.com/agentskills/agentskills) | Apache-2.0 code/specification; CC BY 4.0 documentation | lowercase portable naming, discriminating metadata, progressive disclosure, and explicit optional license/version metadata | compatibility does not transfer licenses from referenced skills or assets |
| [OpenAI skill-creator](https://github.com/openai/skills/tree/main/skills/.system/skill-creator) | Apache-2.0 in the skill directory | keep routing cheap, move conditional detail to references, and use deterministic scripts only where they improve reliability | design principles were independently implemented; no prompt or helper code was copied |
| [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Apache-2.0 | iterative creation, realistic evaluation, and progressive disclosure | Anthropic's document skills have different proprietary/source-available terms and are comparison-only |
| [K-Dense scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) | skill identifies MIT | separate source/claim/consistency manifests and reserve submission approval for humans | each skill and dependency still needs its own license check |
| [K-Dense scientific-visualization](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md) | skill identifies MIT | separate raw data, transformations, and display exports; inspect physical-size rendering | journal parameters remain live external rules |
| [research-paper-lifecycle-skills](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills) | Apache-2.0 with NOTICE | modular lifecycle, deterministic scripts, venue profiles, PASS/WARN/FAIL states | CNS independently implements its checks; Apache code was not copied |
| [Vale](https://github.com/vale-cli/vale) | MIT | markup-aware style lint can complement human review | style lint cannot determine scientific truth or authorship |
| [textlint](https://github.com/textlint/textlint) | MIT core; plugins vary | extensible Chinese/English diagnostics and machine-readable reports | every rule/plugin license must be checked separately |
| [Manubot](https://github.com/manubot/manubot) | BSD-2-Clause Plus Patent | persistent identifiers and versioned manuscript builds | optional surrounding workflow, not a CNS core dependency |
| [PaperQA2](https://github.com/Future-House/paper-qa) | Apache-2.0 | retrieve, rank, and retain source-linked evidence before synthesis | retrieval relevance is not claim entailment; access licenses for papers remain separate |
| [OpenScholar](https://github.com/AkariAsai/OpenScholar) | Apache-2.0 | evaluate multi-source synthesis with citation quality and completeness dimensions | benchmark answers and training data have their own terms and must not become style templates |
| [ScholarQABench](https://github.com/AkariAsai/ScholarQABench) | MIT evaluation code; aggregate data and reference answers ODC-BY with constituent-dataset terms | use held-out, rubric-based evaluation for literature synthesis rather than anecdotal demos | public ground truth can contaminate future models; keep a separate local held-out set |
| [LangChain Open Deep Research](https://github.com/langchain-ai/open_deep_research) | MIT | separate research planning, source gathering, synthesis, and artifact output | a generic research loop does not establish systematic-review completeness |
| [ai-peer-review](https://github.com/poldrack/ai-peer-review) | MIT | collect truly independent reader outputs before comparing consensus, unique concerns, and conflicts | multiple model calls are not independent evidence about the science and cannot replace human review |
| [Quarto](https://github.com/quarto-dev/quarto-cli) | version-dependent; current releases must be checked | single-source figures, tables, cross-references, and multi-format output | conversion never replaces DOCX/PDF visual QA |
| [showyourwork](https://github.com/showyourwork/showyourwork) | MIT | rebuild figures from data/code through a dependency graph | appropriate only when the project is code- and data-reproducible |
| [academic-figure-skill](https://github.com/TingxiYu/academic-figure-skill) | root license observed as Apache-2.0 | figure contract, reusable plotting scripts, multi-pass visual QA | conflicting README license text requires the root license to control |
| [ResearchFigureSkill](https://github.com/KaiyiHu/ResearchFigureSkill) | MIT | evidence-locked conceptual diagrams and deterministic text/arrows | a visual reference can guide grammar, never supply evidence |
| [SciencePlots](https://github.com/garrettj403/SciencePlots) | MIT | plotting styles are useful starting points | a style preset is not journal compliance |
| [Great Tables](https://github.com/posit-dev/great-tables) | MIT | generate presentation tables from structured data | submission tables should remain editable, not screenshots |
| [MQM](https://www.themqm.org/) | content identified as CC BY 4.0 | translation defects need typed categories and major/minor severity | CNS adds scientific invariants and evidence-scope checks |
| [Google WMT MQM evaluation](https://github.com/google/wmt-mqm-human-evaluation) | Apache-2.0 | context-aware segment annotation, including Chinese–English | evaluation examples are not a submission-writing corpus |

## Adopted architecture

CNS Skills combines independently implemented controls:

```text
source lock + protected tokens
  → argument-gap register + evidence-state transitions
  → claim/evidence/terminology registries
  → English argument reconstruction
  → bilingual accuracy + monolingual English edit
  → invariant and citation diff
  → visual claim/provenance manifests
  → venue-specific gate
  → rendered artifact QA + human sign-off
  → demonstrated defect + held-out test before a reusable rule is admitted
```

The design deliberately excludes proprietary phrasebanks, detector-evasion tactics, generic “Nature-style” certification, copied publisher instructions, and redistribution of paper abstracts or figures.

## Translation-specific conclusion

No mature, broadly licensed open-source skill was found that alone converts a Chinese scientific draft into defensible submission English. CNS therefore combines stable segment IDs, a bilingual termbase, protected-token diffs, MQM-style error categories, scientific claim/evidence checks, and a separate monolingual English pass. Back-translation is optional supporting evidence, never the sole accuracy test.

## Visual-specific conclusion

Strong open workflows converge on a figure contract, immutable raw inputs, a transformation log, honest statistical encoding, color-redundant accessibility, caption contracts, editable deliverables, and inspection at final physical size. CNS adopts those controls while keeping target-venue dimensions and generative-AI policies dynamically verified.

## Review-iteration and evaluation conclusion

Open research systems separate discovery from grounded synthesis, while strong skill-development systems separate development examples from forward evaluation. CNS combines those principles without turning them into a fixed prose template: literature expansion starts from a missing argumentative role; each source advances through metadata, full-text, entailment, and status checks; apparently repeated support is checked for independence; and manuscript failures enter the skill only after counterexamples and a locked held-out test. Naturalness is evaluated by blinded reader preference after evidence equivalence is confirmed, never by optimizing an AI-detector score.

## Reuse policy

No third-party prompt, instruction block, code, test, template, or asset was imported for the 0.6.0 review-iteration workflow. Any future import must record source, version/commit, license, modification, notice/attribution requirement, and whether linked assets carry a different license. Source-available is not synonymous with open source. See `references/license-and-provenance.md`.
