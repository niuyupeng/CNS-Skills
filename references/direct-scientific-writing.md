# Direct scientific writing

Use this pass when otherwise accurate writing spends more space defending its
scope than explaining the science. It supplements `natural-academic-style.md`
and `review-prose-naturalness.md`; it does not require a new manuscript section.
Keep the author's requested language and degree of formality.

## Identify the job of the qualification

Read the surrounding paragraph and its supporting source before deciding to
keep, compress, relocate, or rewrite. These are editorial decisions, not labels
to insert into the paper.

| Function in context | Treatment |
|---|---|
| An experimental condition, uncertainty, negative result, causal limitation, or untested population changes the interpretation | Preserve its meaning and attachment to the relevant claim. A direct negative result is not defensive prose. |
| A repeated disclaimer adds no new information after the actual condition is already stated | Compress or remove the repetition; lead with the observation, comparison, or consequence. |
| A phrase only announces caution or importance | Start with the scientific point that follows it, if that point is supported. |
| A missing source or unresolved author choice is concealed by vague caution | Resolve it or put a specific query in the author log. Do not replace it with confidence. |
| A limitation motivates a possible experiment or design choice | Distinguish the reported result from the proposed next action. Do not imply that the source performed the proposal. |

The same phrase can serve different functions. `May`, `not`, `only`, `不能`,
`可能`, a dash, or a parallel sentence is not sufficient evidence of a defect.
Do not count hedges or remove all sentences that begin with a qualification.

## Make the scientific point earn the paragraph

1. Recover the factual core: object, intervention or comparison, measurement,
   result, conditions, and citation. Preserve numbers, units, denominators,
   direction of effect, negation, and the distinction between association and
   causation. Source ambiguity requires a query, not an inferred stronger claim.
2. Decide what the reader should learn. In a Review this can be a comparison,
   explanation, unresolved disagreement, or justified choice; not every paragraph
   needs an experimental prescription. In a Methods section, exact reproducible
   description may be the entire job.
3. State that point using the material, model, measurement, or experiment as the
   subject where useful. Keep an informative qualification beside the claim it
   limits rather than adding a generic warning at every paragraph end.
4. If the author asks for an actionable design discussion, connect the stated
   objective to controllable variables, constraints, the model's role, and the
   next measurement or choice. Fill only the links supported by sources or
   explicitly identified as author recommendations. Do not invent target values,
   search bounds, assay thresholds, or successful optimization runs.
5. Compare the revision with the source. Check whether every consequential
   assertion is still supported, uncertainty still has the same scope, and a
   proposed action remains a proposal. Read the result for natural cadence;
   directness does not require short sentences everywhere.

A design discussion should distinguish prediction, candidate ranking,
generation, parameter search, and experimental feedback when that distinction
changes the choice. A high prediction score alone does not establish a working
optimization policy. Keep representations, model architectures, and task or
optimization strategies conceptually distinct without imposing one taxonomy on
every manuscript. Preserve useful conventional baselines; algorithm age or a
journal's prestige is not evidence that a comparator is irrelevant.

## Small synthetic examples

The following are invented editing examples, not experimental findings or
quotations. Bracketed references are fixture labels, not real citations.

**Redundant defense, same scientific boundary**

Before: “It must be stressed that these results cannot be taken to prove
universal performance. The classifier was evaluated only on measurements from
one laboratory [4].”

After: “The classifier's performance was evaluated on measurements from one
laboratory [4]; transfer to other laboratories remains untested.”

The revised sentence says exactly which transfer was untested; it does not
promise that an external test will succeed.

**Uncertainty that must survive**

Before: “需要指出的是，涂层可能通过降低蛋白吸附减少细胞黏附，但实验未区分这一路径与表面粗糙度的作用[7]。”

After: “涂层可能通过降低蛋白吸附减少细胞黏附；现有实验尚未区分蛋白吸附与表面粗糙度的作用[7]。”

Removing `可能` would turn a proposed mechanism into an established mechanism.
Removing the second clause would hide the unresolved alternative explanation.

**Actionable does not mean already accomplished**

Source note: a study predicts coating thickness from deposition time and current;
it reports no prospective optimization experiment.

Supported synthesis: “The predictor estimates coating thickness from deposition
time and current. A prospective design study could rank feasible parameter
combinations and test the selected coating thicknesses.”

Unsupported rewrite: “The model optimized deposition time and current to produce
the target coating thickness.” This invents both an action and its success.

## Check the outcome, not a prose score

Use `scripts/check_invariants.py` on source and revision for token-level triage.
Protect exact phrases when the author requires them. Numerical invariants cannot
detect every change in causality, negation, attribution, or evidential status;
complete the semantic comparison even when the report is clean.

Use `evals/direct-scientific-writing-cases.json` for forward evaluation. Give an
independent evaluator each case's request, passage, and source notes, plus the
skill. Withhold the case's acceptance criteria until the response is complete.
Judge the actual prose against those criteria; a valid response need not match
any particular wording. Report failures and missing inputs separately. These
synthetic cases are regression probes, not a validated real-world benchmark.

Do not insert human quirks, anecdotes, errors, invented opinions, or random
synonyms. Do not use AI-detector outputs, human-likeness percentages, or claims
of undetectability as editing targets. Deliver the revised prose and concise
substantive changes; keep the editing checklist outside the manuscript.
Keep instructions about agreed sections or the revision process in the author
note too; the replacement paragraph should discuss the scientific subject.

## Open-source comparison and provenance

Compared with [blader/humanizer at commit
9862685f575c65a8247f90369951df1b3416e3d6](https://github.com/blader/humanizer/tree/9862685f575c65a8247f90369951df1b3416e3d6),
accessed 2026-09-15. The repository's MIT licence was checked at that revision.
Its general emphasis on contextual rewriting and specificity informed this
comparison. This reference, its examples, and the forward cases were authored
independently; no upstream prompt, code, examples, Wikipedia-derived text, or
other assets are redistributed. CNS Skills adds scientific claim and source
controls and does not import rules for impersonating authors or manipulating
detectors. Linked external content retains its own terms.
