# From repeated manuscript failures to an author-led development workflow

## Purpose and evidence boundary

This note records the qualitative defect analysis used to add upstream
manuscript development to CNS Skills v0.12.0. Two complete, longitudinal project
transcripts and their continuity records were reviewed from beginning to end.
The raw conversations and unpublished manuscript content are not redistributed.
Only generalizable failure classes, rejected assumptions, and resulting public
rules are reported here.

This is a design-defect study, not a prevalence survey, a user benchmark, or
evidence that the workflow improves acceptance. A defect could recur many times
in one project and still count as one rule-design problem. The study is useful
because it follows decisions across positioning, outline, evidence collection,
drafting, figures, revision and file delivery rather than judging isolated
prompts.

## Main finding

The largest source of avoidable rework was upstream of sentence editing. A
polishing workflow can preserve claims in an existing draft yet still produce
the wrong paper when it does not know:

1. which source is allowed to decide the architecture;
2. which earlier decision has been superseded;
3. whether the requested artifact is a positioning memo, one-page outline,
   detailed outline, evidence matrix, first draft or clean submission copy;
4. what evidence is sufficiently verified for that stage; and
5. which analytical scaffolds must never enter reader-visible prose.

Accordingly, v0.12 adds a staged, author-led development route rather than
stretching the existing “Revise” mode to cover everything.

## Defect-to-rule matrix

| Observed failure class | General rule adopted | Public implementation or regression target |
|---|---|---|
| project history was not read before a new framework was proposed | read the continuity record and identify active, pending and superseded decisions before redesign | decision-provenance and continuity fields in `manuscript_plan.py` |
| an assistant inference was later described as a meeting decision | label decisions as author-confirmed, source-explicit, inferred, proposed, pending or superseded | authority-mismatch and superseded-decision tests |
| a file supplied for formatting introduced its obsolete scientific content | classify every input as content, evidence, format, visual or background | format-reference decision and evidence counterexamples |
| a title changed during an unrelated structure revision | preserve the source title; a new title remains a proposal until approved | title-lock regression |
| a narrative Review silently became a Perspective or quasi-systematic Review | lock article type; propose genre changes and obtain approval rather than applying them silently | manuscript-development and genre-specific references |
| several taxonomies competed for control of the main headings | declare one ownership or hierarchy rule; allow nested axes, but resolve competing parallel taxonomies | competing-primary-axis regression |
| an outline was a list of methods, materials or fashionable terms | make every section answer a reader question, advance a claim/comparison, map evidence and expose a boundary | section-contract schema |
| a brief meeting outline expanded into a long explanatory document | treat format and length as an artifact contract | exact budget and approval-state fields |
| the author asked to approve text before a DOCX was built, but production skipped that checkpoint | record and obey approval state before advancing stages | staged route in `manuscript-development.md` |
| a renamed or reformatted document was called a new architecture | require a delta in governing question, primary axis, section function, reader decision or evidence placement | no-substantive-delta regression |
| a one-sentence explanation became a long multi-part answer | separate one sentence, short message, one page and expert brief | exact one-sentence contract regression |
| identical section shells made the prose look generated | use common internal comparison fields without repeating visible headings, openings or paragraph choreography | backstage-scaffolding and natural-style rules |
| `central judgment`, evidence grades, prompts and author TODOs appeared in a clean manuscript | keep editorial instruments in a separate author-side log | reader-visible internal-label regression |
| abstract labels such as framework, evidence chain and pipeline displaced the material, experiment and result | rewrite at the scientific-object level instead of renaming the scaffold | Review prose and author-led drafting rules |
| a large bibliography was equated with a strong evidence base | count direct primary evidence, independent validation, counterexamples and methodological context separately | evidence-matrix contract |
| discovered records or vague placeholders were presented as a verified core library | require a unique record, source locator, verification state and exact support location | source/evidence state regressions |
| DOI resolution was treated as proof that a citation supported a claim | separate existence, metadata/status, entailment, scope, placement and independence | six-axis citation audit |
| a Review article was used as the sole support for a specific experiment or mechanism | use Reviews for orientation and primary studies for specific experimental claims | scientific-integrity and evidence-matrix rules |
| a Perspective was treated as original evidence or an in-vitro result was described as near-clinical | lock article type and validation setting before drafting the claim | genre and evidence-boundary gates |
| automation, robotic execution, feedback learning and autonomy were collapsed into one label | record AI decision, execution, test setting and feedback as distinct constructs | Review evidence profile rules |
| several evidence dimensions were compressed into one universal maturity score | keep validation, setting, generalization and autonomy orthogonal | no-universal-rank rule |
| “no large dataset means experiments cannot begin” was used as a blanket conclusion | require reliable structured feedback, while allowing a small standardized seed set when its provenance and iteration are strong | data-readiness gate |
| an author-proposed data schema was called a community standard or established benchmark | record whether a standard is official, community-used, author-proposed or pending | benchmark-status regression |
| the independent experimental unit, batch, process, failures or version were missing from a dataset claim | audit unit, identity, process/site, measurement/time, missingness, provenance and split/feedback eligibility | data-readiness completeness regression |
| a title made a causal, clinical, priority or completeness claim beyond the evidence | optimize only after article type, contribution and evidence boundary are locked | scientific-title workflow |
| a target reference count or display count was treated as a quality target | search and display plans follow argument gaps, scientific roles and verified venue constraints | Review development and visual architecture rules |
| decorative coloured grid tables were delivered as SCI-ready | use the verified venue style or a neutral three-line default; audit inherited borders and fills | visual audit and table rules |
| biomedical Review figures were stacks of interchangeable boxes | require scientific objects, experimental actions, tests, decisions/feedback and boundaries | object-based scene grammar |
| several workflows were used where the Review needed a cross-study synthesis | require genuine traceable study comparison when the argument depends on it | Review visual-plan audit |
| a commercial illustration style was treated as a template to copy | transfer general clarity principles, not proprietary assets, templates or visual identity | licence/provenance and visual-production rules |
| “top-journal style” was interpreted as reusable phrases or a fixed layout | transfer argumentative and evidential functions, not prose templates or publisher identity | genre-aware top-venue rule |
| multiple expert or agent passes surfaced as a committee transcript | share one source lock and merge feedback into one consistent authorial voice | author-led drafting rule |
| future-tense promises replaced the requested search, draft or file | completion requires the corresponding record, artifact or explicit incomplete status | completion-contract regression |
| successful file generation was reported as completion without rendering | verify existence, exact budget, editability, cross-references and every rendered page | completion-check regression and artifact QA |
| “humanization” was interpreted as AI-detector evasion | optimize authentic authorship, evidence fidelity and reader experience; refuse detector gaming | explicit negative boundary |

## Stage and sufficiency model

The study yielded two independent ladders. The artifact ladder prevents the
system from delivering the wrong kind of product; the sufficiency ladder
prevents it from writing beyond the supplied science.

| Available material | Highest honest default product |
|---|---|
| topic only | positioning proposal, provisional outline, evidence-acquisition plan |
| author notes or meeting record | decision-locked outline and bounded prose |
| verified literature or author results | supported sections plus unresolved-evidence log |
| approved outline plus traceable evidence | author-led, author-approved first draft |
| complete source package | complete draft followed by genre, citation, visual and artifact QA |

The ladders are deliberately not a promise of automatic progression. A complete
source package can still contain an unsupported central claim, and a concise
outline can be the correct final artifact for a meeting.

## Rules intentionally not generalized

Longitudinal work creates tempting but invalid “best practices.” The following
project decisions were rejected as public defaults:

- any particular seven-category, material-category or capability-level chapter
  taxonomy;
- a fixed number of figures, tables, boxes, pages, words or references;
- a project-specific compact evidence scale or record count;
- a universal percentage split between current evidence, limitations and
  outlook;
- a requirement that every biomedical Review use clinical translation,
  autonomous laboratories or data infrastructure as its main narrative;
- a claim that every SCI journal requires a three-line table;
- a claim that a large public dataset is necessary before useful wet-lab
  iteration can begin.

The transferable rule is to preserve the project's current authorized decision,
keep comparison constructs separate, and derive length and display choices from
the artifact contract, scientific argument and verified venue instructions.

## Public implementation

The public workflow is split across:

- `references/manuscript-development.md` for positioning, authority, outline,
  evidence, drafting, data readiness, naturalness and handoff;
- `assets/manuscript_development_plan.json` as a safe, synthetic plan contract;
- `scripts/manuscript_plan.py` as a dependency-free deterministic auditor; and
- `tests/test_manuscript_plan.py` for failure-focused regressions.

The plan audit is intentionally backstage. Passing it means that the declared
development contract is internally coherent; it does not verify source truth,
read the literature, judge citation entailment, assess unpublished data, or
certify a manuscript as publishable.
