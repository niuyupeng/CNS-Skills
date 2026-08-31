# Open-source skill and tooling review

Snapshot updated: 2026-08-31. The visual-production additions and license-sensitive rows changed in this update were checked through primary repository pages, license files, per-skill metadata, or notices on this date. Other rows remain comparative design research and are not a reuse clearance. This review does not imply endorsement, affiliation, or code reuse. A license recorded as "observed" is an audit result rather than legal advice, and a moving `main`-branch link is not a reproducible version pin.

## Selection criteria

Projects were screened for transparent workflow design, scientific integrity, bilingual QA, figure/table provenance, deterministic checks, active or inspectable source, and a license that could be identified. GitHub visibility alone was not treated as permission to copy or redistribute. "Design lesson" below means a principle independently re-expressed and tested in CNS Skills; it does not mean that upstream prompt wording, examples, code, templates, or assets were imported.

| Project | License observed | Design lesson used by CNS Skills | Boundary |
|---|---|---|---|
| [Agent Skills specification](https://github.com/agentskills/agentskills) | Apache-2.0 code/specification; CC BY 4.0 documentation | lowercase portable naming, discriminating metadata, progressive disclosure, and explicit optional license/version metadata | compatibility does not transfer licenses from referenced skills or assets |
| [OpenAI skill-creator](https://github.com/openai/skills/tree/main/skills/.system/skill-creator) | Apache-2.0 in the skill directory | keep routing cheap, move conditional detail to references, and use deterministic scripts only where they improve reliability | design principles were independently implemented; no prompt or helper code was copied |
| [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Apache-2.0 | iterative creation, realistic evaluation, and progressive disclosure | Anthropic's document skills have different proprietary/source-available terms and are comparison-only |
| [K-Dense scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) | repository and skill identified as MIT at review time | separate source/claim/consistency manifests and reserve submission approval for humans | each skill, dependency, service, dataset, and bundled asset still needs its own terms check |
| [K-Dense scientific-visualization](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md) | repository and skill identified as MIT at review time | separate raw data, transformations, and display exports; inspect physical-size rendering | journal parameters remain live external rules; no upstream prompt text was copied |
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
| [academic-figure-skill](https://github.com/TingxiYu/academic-figure-skill) | root `LICENSE` is Apache-2.0; README also labels the license inconsistently as MIT in one place | figure contract, reusable plotting scripts, multi-pass visual QA | the contradiction is a provenance warning; do not rely on a README label or import assets without file-level review |
| [ResearchFigureSkill](https://github.com/KaiyiHu/ResearchFigureSkill) | MIT | evidence-locked conceptual diagrams and deterministic text/arrows | a visual reference can guide grammar, never supply evidence |
| [SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | CC BY 4.0 for original repository content; underlying tools retain separate licenses | registry-based discovery, typed skill templates, and explicit validation | copied or adapted prose would require attribution; CNS used only independently expressed architecture |
| [paper-figures / StatMate](https://github.com/DRZ-hang/paper-figures) | the former URL redirected to `DRZ-hang/StatMate` on 2026-08-31; current root license observed as MIT | data-first routing from raw values to statistics, plots, and editable tables | repository identity is volatile and example/data terms may differ; pin a commit and re-audit before reuse |
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

The audit also found a recurring failure mode: a repository-level license, a `SKILL.md` metadata field, a README claim, dependencies, example data, templates, and published-paper figures can all have different terms. CNS therefore learns methods at the level of abstract design unless an exact file is deliberately imported under a recorded commit, license, notice, and modification history.

## Review-iteration and evaluation conclusion

Open research systems separate discovery from grounded synthesis, while strong skill-development systems separate development examples from forward evaluation. CNS combines those principles without turning them into a fixed prose template: literature expansion starts from a missing argumentative role; each source advances through metadata, full-text, entailment, and status checks; apparently repeated support is checked for independence; and manuscript failures enter the skill only after counterexamples and a locked held-out test. Naturalness is evaluated by blinded reader preference after evidence equivalence is confirmed, never by optimizing an AI-detector score.

## Reuse policy

No third-party prompt, instruction block, code, test, template, or asset was imported for the current review-iteration or visual-production workflow. Any future import must record source, immutable version/commit, file path, license, modification, notice/attribution requirement, and whether dependencies or linked assets carry different terms. Source-available is not synonymous with open source. See `references/license-and-provenance.md`.

Before admitting an external artifact, the release audit must answer all of the following:

1. Is there an explicit license for the exact file or directory, not merely a GitHub badge or repository description?
2. Does a per-skill license override or qualify the root license, and are `NOTICE`, attribution, share-alike, or modification-marking duties present?
3. Are prompts, examples, datasets, fonts, icons, journal templates, and paper figures covered by the same grant?
4. Is the source pinned to a release or commit so the reviewed terms and content can be reconstructed?
5. Can the principle be implemented independently instead of copying protected expression?

If any answer is unresolved, CNS may cite the project as comparative research but must not redistribute or silently adapt its content.
