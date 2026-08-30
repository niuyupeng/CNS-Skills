# Open-source skill and tooling review

Snapshot: 2026-08-30. This review documents design lineage; it does not imply endorsement, affiliation, or code reuse.

## Selection criteria

Projects were screened for transparent workflow design, scientific integrity, bilingual QA, figure/table provenance, deterministic checks, active or inspectable source, and a license that could be identified. GitHub visibility alone was not treated as permission to copy or redistribute.

| Project | License observed | Design lesson used by CNS Skills | Boundary |
|---|---|---|---|
| [K-Dense scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) | skill identifies MIT | separate source/claim/consistency manifests and reserve submission approval for humans | each skill and dependency still needs its own license check |
| [K-Dense scientific-visualization](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md) | skill identifies MIT | separate raw data, transformations, and display exports; inspect physical-size rendering | journal parameters remain live external rules |
| [research-paper-lifecycle-skills](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills) | Apache-2.0 with NOTICE | modular lifecycle, deterministic scripts, venue profiles, PASS/WARN/FAIL states | CNS independently implements its checks; Apache code was not copied |
| [Vale](https://github.com/vale-cli/vale) | MIT | markup-aware style lint can complement human review | style lint cannot determine scientific truth or authorship |
| [textlint](https://github.com/textlint/textlint) | MIT core; plugins vary | extensible Chinese/English diagnostics and machine-readable reports | every rule/plugin license must be checked separately |
| [Manubot](https://github.com/manubot/manubot) | BSD-2-Clause Plus Patent | persistent identifiers and versioned manuscript builds | optional surrounding workflow, not a CNS core dependency |
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
  → claim/evidence/terminology registries
  → English argument reconstruction
  → bilingual accuracy + monolingual English edit
  → invariant and citation diff
  → visual claim/provenance manifests
  → venue-specific gate
  → rendered artifact QA + human sign-off
```

The design deliberately excludes proprietary phrasebanks, detector-evasion tactics, generic “Nature-style” certification, copied publisher instructions, and redistribution of paper abstracts or figures.

## Translation-specific conclusion

No mature, broadly licensed open-source skill was found that alone converts a Chinese scientific draft into defensible submission English. CNS therefore combines stable segment IDs, a bilingual termbase, protected-token diffs, MQM-style error categories, scientific claim/evidence checks, and a separate monolingual English pass. Back-translation is optional supporting evidence, never the sole accuracy test.

## Visual-specific conclusion

Strong open workflows converge on a figure contract, immutable raw inputs, a transformation log, honest statistical encoding, color-redundant accessibility, caption contracts, editable deliverables, and inspection at final physical size. CNS adopts those controls while keeping target-venue dimensions and generative-AI policies dynamically verified.

## Reuse policy

Any future code or content import must record source, version/commit, license, modification, notice/attribution requirement, and whether linked assets carry a different license. See `references/license-and-provenance.md`.
