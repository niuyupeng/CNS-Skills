# Leading-conference paper mode

Use this reference for original papers targeting AAAI, CVPR, NeurIPS, ICML,
ICLR, or another named selective conference. Lock the year, track, submission
phase, template, anonymity policy, and page limit before editing; the conference
name alone is not a complete rule key.

## First-page contract

Within the first page, make four elements inspectable:

1. the concrete problem and why the present setting is difficult;
2. the closest unresolved gap, assumption, or failure mode;
3. the exact technical or empirical contribution; and
4. the evaluation that would falsify or support that contribution.

A contribution list is optional. Use one only when it improves navigation under
the page budget; do not manufacture three bullets from one contribution or use
“state of the art” as a substitute for significance.

## Contribution–evidence map

For each claimed contribution, require a nearby test:

| Contribution type | Minimum evidence question |
|---|---|
| New method | Does it beat simple and strong comparators under a fair protocol, and which component causes the gain? |
| New representation | What information is added, what shortcut is possible, and what happens under distribution shift? |
| New dataset or benchmark | What population/design space is represented, how were splits and labels created, and which uses are unsupported? |
| New system | What end-to-end task succeeds, at what cost/latency/resource level, and where does the system fail? |
| Theory | Are assumptions explicit, is the result complete, and do experiments test the regime in which it matters? |
| Analysis or negative result | Is the stress test controlled, reproducible, and broad enough to change a community belief or practice? |

Baselines, ablations, robustness tests, and error analysis are not decorative
sections. Each should answer a named alternative explanation. Report seeds,
uncertainty, data access, tuning/computation budgets, and evaluation leakage as
required by the claim and current checklist.

## Conference visual architecture

The main paper is page-budgeted, so a display must earn its area. Common roles
include:

- problem/setup or method overview;
- main comparison on the task that matches the contribution;
- ablation or controlled alternative-explanation test;
- robustness, distribution shift, efficiency, or scaling evidence;
- qualitative/error analysis with selection criteria; and
- dataset/system documentation when the resource itself is a contribution.

Do not assign a universal figure or table count. The CNS Skills 2025 conference
sample detected a median of five figure captions and three table captions in
195 official-PDF-derived full texts, but extraction can include appendix
displays and column-order artefacts. These counts are descriptive, not page
targets or acceptance predictors.

Prioritize main-paper evidence that a reviewer must read to assess the central
claim. Supplementary material may contain proofs, more examples, secondary
ablations, and implementation detail, but official guidance commonly states
that reviewers are not required to read it.

## Current official page-budget examples

Last verified: **2026-08-31 (Asia/Shanghai)**. Recheck the exact track.

- CVPR 2026: eight pages including figures and tables, plus references.
- AAAI-27 main submission: seven pages of non-reference content within a
  nine-page main PDF; current author kit and reproducibility checklist apply.
- ICML 2026 main track: eight main-body pages at submission, with references
  and appendices outside that body limit; accepted papers receive one extra
  main-body page.
- ICLR 2026: nine main-text pages at submission and ten during discussion/
  camera-ready; references and appendices are outside the main-text limit, and
  reviewers are not required to read appendices.
- NeurIPS 2026: use the current style, track-specific call, main-track handbook,
  and mandatory paper checklist. Track rules differ.

These are hard requirements only in their stated year/track/phase. They do not
define an ideal scientific structure and may change in the next cycle.

## Cross-domain AI for science and biomedicine

When a conference paper applies AI to materials, biology, or medicine, evaluate
both layers:

- **algorithmic layer:** split integrity, baselines, ablations, calibration,
  robustness, compute, and reproducibility;
- **scientific layer:** independent sample unit, real experimental action,
  proxy validity, biological/physical testing context, and transfer boundary.

A benchmark gain does not by itself establish a better experiment, mechanism,
or translational outcome. Conversely, animal testing does not repair a leaked
split or unfair baseline.

## Conference-specific stop rules

- Do not import a Review's broad literature tour into a page-limited technical
  paper.
- Do not hide a central baseline, ablation, limitation, or data-split decision
  in an appendix that reviewers may skip.
- Do not copy page limits, checklists, anonymity rules, or AI-use policies from
  another year, venue, or track.
- Do not equate more tables with rigor; a dense leaderboard without uncertainty,
  protocol equivalence, or failure analysis is weak evidence.
- Do not compress captions below final-column legibility merely to fit another
  experiment.
