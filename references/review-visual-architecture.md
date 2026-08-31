# Review visual architecture

Use this reference for narrative, structured-narrative, scoping, systematic,
and meta-analytic Reviews. Read the exact article-type guide first. A display
count is a page-budget constraint, not a scientific target.

## Evidence basis and rule classes

Last verified: **2026-08-31 (Asia/Shanghai)**.

- **HR — Nature Reviews Review format guide:** no more than seven main-text
  display items (figures, tables, and boxes combined) are allowed. The same
  guide prefers original display items, requires ordered citation, and asks
  that every display explain a specific point or background science. This is a
  Nature Reviews rule, not a universal rule for Reviews.
- **OG — Nature Reviews content-type pages:** a roughly 6,000-word Review
  typically uses five to seven display items. Treat this as a venue-specific
  norm and confirm the target journal and invitation.
- **OG — Nature Reviews figure guide:** figures should complement and follow
  the narrative, use a logical reading path, and contain the scientific detail
  needed for peer review.
- **OG — Cell Press/Trends editorial guidance:** effective Review figures add
  new insight rather than reproduce disconnected primary-source panels.
  Useful classes include cross-source data collection and replotting,
  schematics, and conceptual diagrams. No universal figure count is stated.
- **Descriptive corpus observation:** in the CNS Skills 2026 Review stratum,
  only 42/200 records had parseable full-text XML. Within that availability-
  selected subset, the median counts were four figures, two tables, and one
  box. The subset is shaped by PMC availability and JATS tagging; these values
  are diagnostics, not publisher rules or acceptance predictors.
- **Purposive visual audit:** a separate [14-paper aggregate
  audit](https://github.com/niuyupeng/CNS-Skills/blob/v0.10.0/research/top-review-visual-architecture-study.md) found a median of
  seven independent main-text display containers and four main figures; the
  *Nature Reviews* subset (n=8) had a main-figure median of five. Topic and
  venue selection were purposive, so these values calibrate a functional audit
  only; they are not display quotas or acceptance predictors.

Official routes are maintained in visual-production.md. Recheck them before a
submission because article formats change.

## Plan a visual argument, not a quota

Before drawing, write one sentence for each display:

> After seeing this item, the reader can decide or explain **what** that prose
> alone, another display, or an inventory cannot show as clearly.

A strong long-form Review often needs several distinct visual functions, but
not every manuscript needs every function:

1. **Scope or system map** — defines the object, boundaries, and organizing
   lens.
2. **Taxonomy or mechanism** — shows relationships that prose would force the
   reader to hold in working memory.
3. **Cross-study evidence synthesis** — aligns studies on common variables,
   exposes contrasts, or replots comparable data with provenance.
4. **Decision aid** — turns the synthesis into a model-selection, diagnostic,
   or experimental choice.
5. **Boundary or roadmap** — shows where evidence stops and which observation
   would change the decision.

The sequence should carry the Review's governing question. Two workflow
schematics do not become a strong visual story merely because the total number
of tables reaches a venue range. Conversely, five decorative diagrams do not
replace one auditable evidence comparison.

## Assign the right job to figures, tables, and boxes

Use a **figure** when spatial relation, process, mechanism, contrast, or a
multivariable evidence pattern is the point. Use a **table** when readers need
exact lookup across stable fields. Use a **box** for prerequisite background,
definitions, or a peripheral method that would interrupt the main argument.

For every item record:

| Field | Decision |
|---|---|
| Reader question | One question only |
| Review function | scope, taxonomy, mechanism, evidence, decision, or boundary |
| Evidence class | author synthesis, extracted quantitative data, adapted content, or illustrative example |
| Provenance | cited studies, extraction table, data/code, and licence |
| Main or supplement | whether the governing argument still works if the item is not read |
| Non-duplication | what this item contributes that no other display contributes |
| Prohibited inference | causal, ordinal, translational, or generalization claim the display must not imply |

## Main text versus supplement

Keep in the main text the displays needed to understand the central synthesis
and make its main decision. Move exhaustive study inventories, extraction
fields, sensitivity tables, and audit trails to a supplement when they obscure
the comparison. The main text must still state the selection boundary and cite
the supplement honestly.

When converting an evidence table into a figure:

1. preserve the complete machine-readable or tabular record in the supplement;
2. state whether displayed examples are exhaustive, systematic, or deliberately
   selected contrasts;
3. retain citations next to study-derived claims;
4. keep incompatible endpoints or independent axes separate; and
5. do not turn missing or unreported information into a negative result.

## Review-specific failure modes

- **Inventory dominance:** most display area is spent listing papers, while no
  figure performs cross-study synthesis.
- **Frankenfigure:** many borrowed panels are assembled without a single reader
  question, consistent scale, or sufficient context.
- **Workflow duplication:** several figures redraw the same linear pipeline in
  different words.
- **False maturity ladder:** automation, biological setting, external transfer,
  and reporting completeness are compressed into one ordered score.
- **Decorative roadmap:** arrows and clinical endpoints imply causality or
  readiness that the cited studies did not test.
- **Count compliance without narrative coverage:** the manuscript reaches a
  nominal display range, but its decisive comparison or bottleneck remains only
  in prose.

## Stop rule

Do not add another display only to meet a count. Add, replace, merge, or move an
item only when the visual claim ledger shows an uncovered reader question or a
duplicated/overloaded item. Record exact venue compliance separately from this
editorial judgment.
