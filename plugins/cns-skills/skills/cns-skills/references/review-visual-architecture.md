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
  audit](https://github.com/niuyupeng/CNS-Skills/blob/v0.11.0/research/top-review-visual-architecture-study.md) found a median of
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

## Keep six commonly confused roles distinct

Assign one **primary** role to every display. A display may have a secondary
function, but it may not claim several roles merely to make the plan look
complete.

| Role | Reader question | Required content | Does not become this role merely by... |
|---|---|---|---|
| Graphical abstract | What is the paper's governing question, route, and bounded takeaway at a glance? | A self-contained compression that follows the exact venue's policy and submission role | shrinking the overview figure or adding a clinical endpoint |
| Overview | What belongs to the system and how is the Review organized? | Scope, scientific objects, boundaries, and the organizing lens | placing section headings in connected boxes |
| Workflow | What happens in which evidenced sequence? | Ordered actions, inputs/outputs, measurements, and conditional feedback where it actually occurs | drawing arrows between nouns or implying a closed loop without feedback |
| Framework | Which relationships or decision rules organize the synthesis? | Non-temporal structure, constructs, alternatives, and decision logic | renaming a workflow or adding a central circle |
| Evidence synthesis | What changes when studies are aligned on common variables? | At least two traceable studies, explicit comparison dimensions, missingness, and a non-ranking interpretation unless ranking is justified | adding citations to a workflow, showing isolated examples, or recolouring a literature table |
| Roadmap | Which observation, resource, or validation would change the next decision? | Evidence gaps, contingencies, responsible actors, and stopping or success conditions | pointing a decorative arrow toward patients, deployment, or the future |

A graphical abstract is not automatically a main-text figure and does not
replace an evidence-bearing display unless the current venue counts and reviews
it that way and the main argument remains auditable. An overview and a
framework may share objects, but the overview defines the territory whereas the
framework makes a relation or decision structure explicit.

## Use object-based biomedical scene grammar

For a biomedical overview, workflow, framework, or graphical abstract whose
reader question follows an experimental path, build the scene from five
semantic layers:

1. **Scientific object** — the material, formulation, molecule, cell, tissue,
   organism, device, data source, or model under discussion.
2. **Experimental action** — what is done to that object: synthesize, formulate,
   perturb, culture, expose, image, screen, manufacture, or administer.
3. **Measurement or test** — the actual readout and context: physicochemical or
   mechanical characterization, process yield, in vitro assay, ex vivo test,
   animal endpoint, human evidence, or another declared measurement.
4. **Decision or feedback** — select, reject, prioritize, update, or trigger the
   next round. Draw feedback only when a measured result really changes a later
   decision.
5. **Evidence boundary** — what remains unmeasured, untransferred, unvalidated,
   or outside the represented studies.

This is a semantic grammar, not a compulsory five-column layout. A figure may
compress, branch, or separate the layers, and an evidence landscape may use a
matrix instead of a scene. Omit a layer only when it is irrelevant to the
reader question or is explicitly recorded as a boundary. Do not convert the
grammar into another decorative pipeline.

Use object glyphs and icons only when they carry scientific work. Each one must
identify a specific object, action, readout, decision, or limitation, remain
distinguishable without colour, and be defined by a direct label, legend, or
caption. Remove an icon that could be exchanged for an unrelated icon without
changing the scientific interpretation.

The **static card/box-stack failure mode** occurs when most of the scientific
content lives as prose inside repeated rectangles, arrows merely indicate
reading order, and the artwork shows no material, intervention, test, decision,
or boundary. Repair it by replacing cards with original object geometry,
experimental actions, readout forms, and evidence-bounded connections. Cards
remain legitimate for a compact categorical comparison or definition set when
their alignment itself answers the reader question; they are not a default
biomedical illustration language.

## Require genuine cross-study evidence synthesis when the argument needs it

If a central inference depends on comparing studies, include at least one main-
text display whose primary role is **evidence synthesis**. It must:

- identify or cite the compared studies or point to a complete provenance-rich
  supplementary record;
- align them on explicit, scientifically compatible dimensions;
- show missing, unreported, or inapplicable information without recoding it as
  a negative result;
- separate testing context, decision role, generalization, and other
  independent constructs rather than forcing a maturity ladder; and
- state whether the studies are exhaustive, systematically selected, or
  deliberately selected contrasts.

Two workflows remain two workflows. A second process diagram, even one with
more icons or citations, cannot replace this comparison. A table can preserve
the full extraction record, but the main-text evidence-synthesis figure should
make the Review's cross-study inference perceptible when that inference is
central to the article.

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

For a multi-display Review plan, route `assets/review_visual_plan.json` through
`scripts/figure_brief.py`. The audit checks role coverage, genuine cross-study
synthesis, biomedical scene semantics, icon meaning, count-as-quota language,
and third-party visual provenance. It is a planning gate, not an assessment of
scientific truth or visual quality.

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
- **Static card/box stack:** repeated rectangles carry nearly all meaning while
  scientific objects, experimental actions, readouts, and boundaries remain
  invisible.
- **Decorative iconography:** icons signal that a figure is "biomedical" but do
  not encode an object, action, measurement, decision, or limitation.
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

A layout such as **six figures plus one table** can be a defensible solution for
one manuscript and a poor solution for another. It is not a CNS Skills default,
benchmark, or Review requirement. Derive the final number from distinct
narrative roles, evidence needs, main-versus-supplement decisions, available
page space, and the current article-type rules.
