# Top-review visual architecture calibration (14-paper audit)

Version: 1.0  
Audit date: 2026-08-31 (Asia/Shanghai)  
Scope: aggregate design calibration for Review figures, tables, and boxes

## Question and boundary

This audit asks how published selective Reviews distribute their main-text
display items and what jobs those displays perform. It does **not** estimate a
field-wide prevalence, define an ideal figure count, predict acceptance, or
create a transferable quota. No unpublished manuscript, project-specific
classification, or manuscript-level diagnosis is included.

Publisher instructions and published-paper observations are kept separate:

- a current rule or typical range applies only to its named journal, article
  type, and submission phase;
- the 14-paper counts below are descriptive observations from a purposive
  sample; and
- CNS Skills uses those observations only to prompt a functional visual audit.

## Sample and counting method

The sample contains 14 English-language Reviews published from 2021 through
2026: eight in *Nature Reviews* journals, four in Cell Press journals, and two
in *Science*. Papers were purposively selected to cover biomaterials,
bioengineering, therapeutic delivery, machine learning, immunotherapy, and
related methods. This is not a random or systematic sample of those publishers.

Counts were taken from the article-body region of available PMC or Europe PMC
JATS XML and checked against the published article. Supplementary displays,
cover or web artwork, table-of-contents graphics, and reference-section content
were excluded. A figure nested inside a Box was counted as a graphic element
but not as a second independent display container. Display roles were manually
coded from the item, title, caption, and its position in the narrative; the
coding is a functional classification, not an aesthetic score.

## Aggregate results

| Measure | All Reviews (n=14) | *Nature Reviews* subset (n=8) |
|---|---:|---:|
| Independent main-text display items | median 7; mean 6.86; range 4–11 | median 7; mean 7.50; range 6–11 |
| Main figures | median 4; mean 4.43; range 2–7 | median 5; mean 4.75; range 3–7 |
| Tables | median 1; mean 1.21; range 0–4 | median 1; mean 1.38; range 0–4 |
| Boxes | median 1; mean 1.21; range 0–3 | median 1.5; mean 1.38; range 0–3 |

Across the 14 papers, the audit counted 96 independent display containers:
62 main figures, 17 tables, and 17 Boxes. These totals explain the reported
means but do not imply that another Review should reproduce the same mix.

The current [*Nature Reviews Bioengineering* content-type
page](https://www.nature.com/natrevbioeng/content) describes a roughly
6,000-word Review as typically containing 5–7 figures, tables, and/or boxes.
That is official venue guidance for that article type, not a universal rule.
The separate [Nature Reviews Review format
guide](https://www.nature.com/documents/natrev-articleformatguide-review.pdf)'s
stated maximum must likewise be applied only within that guide's scope. Cell
Press editorial guidance emphasizes [early figure
planning](https://crosstalk.cell.com/blog/how-to-get-started-writing-a-review-article),
[coherent visual flow](https://crosstalk.cell.com/blog/frankenfigures-alive-but-easily-misunderstood),
and [synthesis that adds
insight](https://crosstalk.cell.com/blog/from-mad-scientist-to-artist) rather
than a fixed cross-journal count.

## Observed display functions

Five recurring functions explained more of the visual architecture than the
raw count:

1. **Scope and navigation** — a field map, timeline, global taxonomy, or
   end-to-end process that establishes the Review's organizing lens.
2. **Mechanism and relation** — a spatial account of interactions, pathways,
   dependencies, or multi-scale links that prose would make difficult to hold
   in working memory.
3. **Cross-study comparison** — aligned categories, values, methods, or
   outcomes that reveal similarities and non-equivalences across studies.
4. **Design and decision** — variables, selection logic, design rules, or a
   validation route that converts synthesis into an inspectable choice.
5. **Boundary and outlook** — unresolved conditions, failure points, or the
   observation that would change the current interpretation.

Figures most often carried spatial relations, mechanisms, or high-level
synthesis. Tables preserved exact lookup fields, study identifiers, values,
and provenance-rich comparison. Boxes isolated definitions, enabling methods,
or peripheral context. Several tables therefore cannot be assumed to replace
a missing synthesis figure, while several decorative diagrams cannot replace
one auditable comparison.

## Design calibration for CNS Skills

The audit supports a two-part Review-visual check:

- **quantity gate:** verify the current venue's combined or separate limits for
  figures, tables, and boxes; and
- **function gate:** ask whether the display sequence covers the reader
  questions necessary for scope, synthesis, decision, and evidence boundary.

The operational consequence is a visual claim ledger, not a target number. Each
candidate display should record its reader question, supported claim, evidence
class, provenance, prohibited inference, main-versus-supplement decision, and
non-duplication role. An item is added, merged, replaced, or moved only when
that ledger exposes an uncovered question, an overloaded display, or redundant
visual work.

## Stable sample identifiers

The aggregate was calculated from the following published records. Identifiers
are listed for auditability; no article text, caption, or artwork is
redistributed here.

- `10.1038/s44222-023-00055-3`
- `10.1038/s44222-023-00052-6`
- `10.1038/s44222-023-00039-3`
- `10.1038/s44222-023-00063-3`
- `10.1038/s41578-021-00279-y`
- `10.1038/s41578-022-00426-z`
- `10.1038/s41578-022-00490-5`
- `10.1038/s41578-021-00358-0`
- `10.1016/j.cell.2021.05.005`
- `10.1016/j.cell.2023.08.030`
- `10.1016/j.tibtech.2022.03.011`
- `10.1016/j.tibtech.2023.05.007`
- `10.1126/science.abq7248`
- `10.1126/science.adx5362`

## Limitations and non-inferences

- Purposeful topic and venue selection prevents population-level inference.
- JATS availability and tagging can change which displays are machine
  countable; nested figures and Boxes require manual reconciliation.
- Published articles reflect editorial development and production, not only
  the authors' submitted architecture.
- A median is not a minimum, maximum, quality score, acceptance predictor, or
  recommendation for a specific manuscript.
- Exact venue instructions remain authoritative and must be rechecked before
  submission.

The corresponding operational rules are maintained in
[`references/review-visual-architecture.md`](../references/review-visual-architecture.md)
and the official-source rule record in
[`references/visual-production.md`](../references/visual-production.md).
