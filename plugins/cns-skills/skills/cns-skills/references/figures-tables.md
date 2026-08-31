# Figures, tables, captions, and visual evidence

Use this reference when designing, revising, or auditing display items. A top-venue figure is part of the evidence chain, not decoration.

For file-level figure production, three-line-table implementation, safe figure prompts, deterministic SVG output, and visual-gate commands, also read `visual-production.md`.

## Start with a visual claim ledger

For every proposed display item, record:

| Item | Reader question | Supported claim | Data/source | Evidence layer | Main uncertainty | Action |
|---|---|---|---|---|---|---|

Delete, merge, or move an item to supplementary material when it does not change the reader's understanding. Do not repeat the same evidence in prose, a table, and a figure without a clear reason.

## Build a figure-first story

Before polishing paragraphs, test whether the display sequence can carry the paper's logic:

1. define the system, cohort, material, task, or design space;
2. establish the primary result against the correct comparator;
3. test mechanism, robustness, or alternative explanations;
4. show generalization, prospective validation, or boundary conditions;
5. close with the evidence-calibrated model or implication.

This is a reasoning sequence, not a mandatory five-figure template. Review articles may instead use a conceptual map, evidence landscape, comparison matrix, workflow, and gap/roadmap figure.

Give each figure one governing question. Give each panel one job. Order panels in the reading direction and make the panel logic explicit in the caption.

## Honest quantitative graphics

- Show the experimental or sampling unit, not only the number of technical measurements.
- Define `n`, biological/technical replicates, exclusions, error bars, interval type, and statistical test.
- Report exact or appropriately bounded p-values and multiple-comparison adjustment where relevant.
- Show distributions and individual observations when sample size and privacy allow; do not hide them behind bars alone.
- Use the same axes, scales, denominators, normalization, and baseline across panels that invite comparison.
- Do not truncate an axis, smooth a curve, bin values, or change aspect ratio in a way that exaggerates an effect.
- Separate training, internal validation, external validation, prospective testing, and deployment evidence visually and textually.
- For ML comparisons, identify splits, leakage controls, seeds, uncertainty, compute budget, data access, and whether baselines were retuned fairly.

Choose the display by the reader's question:

| Question | Usually suitable | Common failure |
|---|---|---|
| distribution or variability | dot/strip, box, violin, interval plot | bar chart hiding observations |
| change over time | line plus uncertainty/individual trajectories | connecting unrelated groups |
| paired change | paired points/lines | treating pairs as independent |
| method comparison | aligned dot/interval plot or compact table | ranking without uncertainty or fair conditions |
| association | scatter with model and uncertainty | causal wording from correlation |
| composition | normalized bars/area only when denominators are stable | unreadable pie charts or changing denominators |
| workflow or mechanism | editable schematic with evidence labels | decorative arrows implying untested causality |

## Images and scientific integrity

- Keep original image data and an auditable transformation history.
- Apply global adjustments consistently unless a local operation is scientifically justified, disclosed, and permitted.
- Do not splice, duplicate, erase, selectively enhance, or generate experimental observations.
- Mark boundaries between fields, samples, time points, or conditions.
- Include scale bars, acquisition conditions, channel definitions, and representative-image selection rules.
- Distinguish raw images, processed images, segmentations, reconstructions, and conceptual illustrations.
- Use generative image tools only for clearly labeled conceptual artwork when the venue permits it; never use them to create or alter evidence.

## Visual accessibility and production

- Use a colorblind-safe palette and ensure meaning survives grayscale and common color-vision deficiencies.
- Encode important distinctions with position, shape, line style, or labels as well as color.
- Keep typefaces, font sizes, line weights, symbols, significant digits, abbreviations, and panel labels consistent.
- Check final-size legibility; a figure that works only when zoomed is not finished.
- Prefer editable vector output (`SVG`, `PDF`, or venue-supported equivalent) for diagrams and plots; use sufficient-resolution raster formats for images.
- Embed fonts when required and verify exports for missing glyphs, clipping, transparency errors, and shifted layers.
- Supply the plotting data and code where policy, consent, and licensing allow.

Always verify current venue dimensions, resolution, color mode, file type, and supplementary-file limits before submission.

## Captions that make figures auditable

A caption should let a reader understand the display without searching the main text. Include, as applicable:

1. a declarative title or the question answered;
2. what each panel shows, in panel order;
3. samples, conditions, comparators, and units;
4. what points, lines, boxes, bands, and colors represent;
5. `n`, the independent unit, replicate structure, and exclusions;
6. summary statistics, error bars/intervals, tests, and multiplicity handling;
7. definitions of abbreviations and symbols;
8. source, adaptation, or licensing information.

Do not put unsupported interpretation in the caption. Do not use “representative” without stating how the image was selected.

## Tables as comparison instruments

Every table should answer one comparison question. Put the comparison dimensions in columns and the evaluated entities in rows unless another orientation is clearly easier to scan.

When no exact venue style is supplied and the user requests an ordinary SCI manuscript table, default to the publication-neutral three-line profile in `visual-production.md`: top, header-bottom, and bottom rules; no vertical rules, cell grid, or decorative fill. Treat this as a project default rather than a universal journal mandate, and do not apply it to layout tables or formal boxes.

- Define cohort, denominator, unit, precision, missingness, and statistical summaries.
- Align decimals and keep meaningful precision; do not manufacture precision from rounded source data.
- Use `NA`, `not reported`, `not tested`, and `not applicable` distinctly.
- Preserve citation proximity for every externally sourced row or claim.
- For literature reviews, include evidence layer, validation setting, sample size, comparator, endpoint, and key limitation—not only method and claimed advantage.
- Avoid color-only judgments such as green = good and red = bad; give the criterion and value.
- Move exhaustive parameter grids or raw catalogues to supplementary material when they obstruct the main inference.

## Review-article visuals

For a review, distinguish:

- conceptual synthesis created by the authors;
- quantitative evidence extracted from studies;
- adapted or reproduced third-party content;
- illustrative examples that are not systematic evidence.

Do not draw arrow direction, hierarchy, readiness, or causal mechanism more strongly than the cited evidence permits. If studies are heterogeneous, show the source of heterogeneity instead of forcing a single ranking.

A strong evidence table records the validation ladder explicitly—for example, computational-only, retrospective/in vitro, prospective/in vivo, and clinical/deployment evidence—using definitions appropriate to the field.

## Graphical abstracts and overview figures

Use a graphical abstract only when it compresses the paper's governing question, method/evidence route, and bounded takeaway. It must not add uncited mechanisms, decorative clinical promises, or visual certainty absent from the data.

Keep the reading path obvious, labels short, and visual grammar consistent with the main figures. Verify whether the exact venue requests, permits, or forbids a graphical abstract and whether it is peer-reviewed content.

## Required visual QA handoff

For each final figure or table created or edited at file level, provide:

- editable source and submission export;
- underlying data or provenance record where permitted;
- caption and abbreviation key;
- a note on `n`, uncertainty, and statistical encoding;
- source/licensing status;
- final-size and rendered-page inspection status;
- any unresolved integrity, accessibility, or venue-compliance issue.

For a read-only audit or a table revised only in chat, report export and rendering as `not performed / outside scope`; do not create files without authorization. Markdown, CSV, or a native document table may serve as the editable source when appropriate to the task.

Never call a manuscript submission-ready when a consequential figure cannot be traced to its data/source or when a caption leaves the evidence unit ambiguous.
