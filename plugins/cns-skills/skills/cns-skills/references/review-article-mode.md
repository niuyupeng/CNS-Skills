# Review article mode

## Lock the review corpus

Before using literature counts or claiming coverage, classify the review as narrative, scoping, systematic, or meta-analytic and record:

- search cutoff date and update date;
- databases, registries, archives, and other sources;
- full query strings or a reproducible search strategy;
- inclusion/exclusion criteria and article-type rules;
- deduplication and version handling;
- title/abstract and full-text screening process;
- extraction fields, evidence cards, and reviewer agreement process;
- treatment of preprints, corrections, retractions, and publication linkage.

For systematic or scoping work, follow the applicable reporting framework and retain a study-flow record. For a narrative review, distinguish systematic retrieval from purposive examples.

If this protocol is missing or incomplete, label the corpus as a **non-systematic illustrative selection**. Do not claim completeness, representativeness, prevalence, field-wide proportions, or a verified paper count. Keep provisional counts and classification statistics marked `pending verification` until identifiers, publication status, duplicates, and evidence cards are audited.

## Build the review around a decision problem

A high-value review does more than enumerate papers. It gives readers a map for deciding among methods, interpreting evidence, and locating the next useful experiment.

Choose a primary organizing axis such as mechanism, model class, decision stage, evidence layer, or translational bottleneck. Use secondary axes for comparison rather than letting them compete for chapter ownership.

## Section contract

For every major section, write a one-sentence internal contract:

> This section explains **which problem**, compares **which evidence**, and ends with **which decision consequence**.

Remove or relocate paragraphs that do not serve the contract.

## Synthesis unit

Prefer a synthesis unit of 2–5 related studies:

1. common question;
2. relevant methodological difference;
3. comparable outcome or evidence layer;
4. reason the difference matters;
5. remaining boundary.

Avoid one-study-per-paragraph catalogues unless chronology or provenance is the point.

Write the synthesis at the level of the scientific objects. Use
`review-prose-naturalness.md` when a draft repeatedly announces its framework,
evidence chain, landscape, axes, or pipeline. Those labels may remain in the
internal section contract or extraction table, but the reader usually needs to
know which material was tested, what the model changed, which result transferred,
and what remained untested.

## Cross-cutting comparison dimensions

- representation and input data;
- prediction/design objective;
- data scale and provenance;
- validation design and leakage control;
- uncertainty and calibration;
- interpretability or mechanistic constraint;
- experimental validation layer;
- transferability and deployment cost.

## Abstract contract

The abstract should state:

- the field-level problem;
- the review's organizing logic;
- the central synthesis or decision framework;
- the main evidence boundary;
- the practical implication.

Do not reproduce the table of contents. Avoid unexplained literature counts unless the search protocol makes those counts meaningful.

## Conclusion contract

A conclusion should not replay every section. It should identify:

1. what the literature now supports;
2. what remains an inference;
3. which validation or infrastructure bottleneck dominates;
4. what research design would resolve it.

Keep forecasts conditional and time-bounded when appropriate.

## Evidence grading

When heterogeneous studies are compared, keep distinct constructs in separate fields. A reusable evidence profile may include:

- validation design: none, retrospective, held-out, prospective, or deployed;
- biological/physical setting: in silico, in vitro, ex vivo, in vivo, human, or field/production;
- generalization: internal, temporal, cross-site, cross-domain, or independent external;
- AI decision role or loop autonomy, using a project-defined scheme;
- reporting completeness and reproducibility status.

Do not collapse these fields into a universal ordinal “maturity” score: a prospective in vitro study and a retrospective external in vivo study are not naturally ordered on one axis.

If a compact code is necessary, give each construct its own namespace and state every definition beside the table. Never reuse labels already defined by the project, source literature, or target field. If a project already uses `C0–C4` or another named scale, preserve those definitions exactly.

Verify every assignment. Do not let polished tables conceal uncertain classifications or silently collapse several axes into one.
