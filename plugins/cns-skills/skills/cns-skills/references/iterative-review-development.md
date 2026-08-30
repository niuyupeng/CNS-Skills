# Iterative review development

Use this reference when expanding a review article, auditing its literature base, or turning a demonstrated manuscript failure into a reusable CNS Skills rule. The aim is a better argument with traceable support, not a larger bibliography for its own sake.

## Declare the review boundary

Distinguish the product before searching:

- A **structured narrative review** may disclose databases, dates, query concepts, inclusion logic, and known coverage limits, but study selection remains interpretive.
- A **systematic or scoping review** requires the protocol, reproducible search strings, deduplication, explicit eligibility criteria, documented independent/duplicate screening or a justified alternative, flow accounting, and the reporting standard appropriate to that review type.

Do not use “systematic”, “comprehensive”, or “all studies” when the corresponding search and screening record does not exist. A structured search can strengthen a narrative review without changing its article type.

## Expand from argument gaps

Search from a missing inferential role, not from a target reference count. Maintain a small gap register:

| Section decision | Claim or comparison at risk | Missing evidence role | Candidate search concepts | Stop decision |
|---|---|---|---|---|
| retain / narrow / remove | exact claim and scope | definition, representative primary study, independent replication, counterexample, boundary, or current status | entities, intervention/model, endpoint, validation setting, and date/status terms | sufficient / unresolved / out of scope |

Prefer a source when it changes the synthesis: it supports a necessary claim, supplies an independent test, reveals a boundary, resolves a contradiction, or updates publication status. Do not add several papers that repeat the same dataset, laboratory, benchmark, or conclusion and then describe them as independent confirmation.

## Track evidence state

Advance each candidate through explicit states:

```text
discovered
  -> metadata verified
  -> full text located
  -> entailment verified
  -> publication/status checked
  -> author approved
```

- **Discovered** means only that a record may be relevant.
- **Metadata verified** locks title, authors, venue, year, DOI or other persistent identifier.
- **Full text located** records the version actually read; an abstract alone cannot settle detailed methods or limitations.
- **Entailment verified** identifies the exact result, population/material/model, endpoint, and validation setting that license the proposed sentence.
- **Publication/status checked** keeps preprints, corrections, retractions, and online-first records visible.
- **Author approved** records acceptance of a substantive addition, claim change, or unresolved risk when author judgment is required.

Do not cite a candidate as verified while it remains in an earlier state. Preserve unresolved items rather than polishing uncertainty out of view.

## Audit citations on six axes

Evaluate each consequential citation separately:

1. **Existence** — the item and persistent identifier resolve.
2. **Metadata and status** — authorship, title, venue, year, version, correction, and retraction state match the reference.
3. **Entailment** — the source supports the nearby proposition, not merely the topic.
4. **Scope** — wording stays within the tested material, population, model, endpoint, comparator, and validation layer.
5. **Placement** — the reader can tell which clause or quantitative statement the citation supports.
6. **Independence** — apparent corroboration is not only a review citing the same primary study, a derivative analysis of the same data, or repeated work from one tightly coupled experimental lineage.

Run `scripts/review_citation_audit.py` for bracketed numeric-reference structure and section coverage. It parses forms such as `[1]` and `[1, 2–4]`; it does not currently parse author–year or superscript Vancouver citations. Use authoritative metadata services and, where appropriate, `cns_audit.py --verify-dois` for axes 1–2; read the relevant source version for axes 3–6. Citation density is a diagnostic, not a quality score.

## Keep action, autonomy, and validation distinct

When a manuscript compares AI-guided workflows, record four different facts:

- what the model predicts or generates;
- which decision it is allowed to make;
- whether the next action is executed manually or automatically;
- which assay or biological level validates the output.

Infer labels from methods and the actual action sequence, not from the title, “autonomous” branding, or the presence of animal experiments. Extensive in vivo validation can coexist with a low-autonomy design workflow. If a project defines `C4` as an in-vivo closed loop, use `C4` only when an in vivo endpoint is fed back to select a subsequent autonomous round; animal validation performed after the loop does not satisfy that definition. Preserve any project-specific axis instead of silently replacing it with this example.

## Admit manuscript lessons into the skill cautiously

Use a defect-to-rule gate:

```text
observed defect -> defect class -> candidate rule -> counterexample check
                -> held-out forward test -> adopt, narrow, or reject
```

Record the defect without confidential manuscript text. Add a rule only when it generalizes beyond one paper, changes a real decision, survives plausible counterexamples, and improves a held-out task without harming evidence fidelity or scope. Prefer a narrow reference or deterministic check over enlarging the routing description. Version the accepted rule and keep a rollback path.

## Evaluate without optimizing to the test

- Keep routing development prompts separate from a locked, append-only held-out split. Do not add trigger keywords merely to fit known prompts.
- For prose naturalness, use blinded A/B comparison by qualified readers after confirming that claims, numbers, and citations remain equivalent. Ask which version is clearer, more field-native, less formulaic, and easier to audit, and collect the reason for the judgment.
- Never use an AI-detector score as the target or claim detector evasion. Naturalness remains subordinate to evidence and meaning preservation.

Finish an iteration with a compact record of added, narrowed, rejected, and unresolved claims; citation-state changes; structural-audit results; and any skill rule admitted or rejected by the defect-to-rule gate.
