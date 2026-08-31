# Scientific visual production

Use this reference for file-level figure creation, three-line tables, visual prompts, and visual QA. Read `figures-tables.md` first for scientific integrity and evidence rules.

## Rule classes and official-source router

Last verified: **2026-08-31 (Asia/Shanghai)**. Publisher and conference rules are live external state. Recheck them for the exact venue, article type, track, and submission phase before every submission or camera-ready handoff.

- **Hard requirement (HR):** the official source explicitly requires or prohibits the item in the stated scope.
- **Official guidance (OG):** the official source recommends, illustrates, or describes a typical practice without making it universal.
- **Project default (PD):** a CNS production or evidence-integrity rule used when the venue is silent. It may be enforced by this workflow but must not be described as publisher policy.

Unless an exact venue record labels a rule HR or OG, the operational workflow in the rest of this file is PD. A more specific current HR always overrides a PD; an OG is recorded and followed unless the authors document a defensible reason not to. Never transfer a numeric rule across venues or between initial and final submission.

| Venue/scope | Current official route | Verified | Rule routing |
|---|---|---|---|
| *Nature*, initial/final figures and tables | [Initial submission](https://www.nature.com/nature/for-authors/initial-submission); [final submission](https://www.nature.com/nature/for-authors/final-submission); [figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/); [panel/export guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/); [Extended Data](https://research-figure-guide.nature.com/figures/extended-data-formatting-guidelines/); [image integrity](https://research-figure-guide.nature.com/figures/image-integrity/) | 2026-08-31 | Dimensions, final-file structure, type/stroke bounds, accessible palette, labelled axes/units, Extended Data table rules, and image-integrity prohibitions are HR in their stated phase/display class. Panel economy, RGB supply, rainbow-scale avoidance, and restrained complexity are OG. The three-line pattern is HR only for the cited Extended Data scope. Nature's 300/450 dpi wording is preserved as a source inconsistency; the 450 dpi CNS target is PD, never achieved by artificial upsampling. |
| *Nature Reviews Bioengineering*, Review displays | [Content types](https://www.nature.com/natrevbioeng/content); [preparing a submission](https://www.nature.com/natrevbioeng/for-authors/preparing-your-submission); [editorial process](https://www.nature.com/natrevbioeng/for-authors/editorial-process); [Review format guide](https://www.nature.com/documents/natrev-articleformatguide-review.pdf); [figure-design guide](https://www.nature.com/documents/natrev-artworkguide_PS.pdf) | 2026-08-31 | The current Review format guide states that no more than seven main-text display items (figures, tables, and boxes combined) are allowed; treat this as HR for that guide's scope. The content-type description of roughly 6,000 words and typically 5–7 display items is OG. Original display preference, ordered citation, logical flow, and reader-usefulness guidance are OG unless the exact linked language is mandatory. Non-primary-content and AI-policy boundaries are HR where the linked policy uses mandatory language. |
| Cell Press / Elsevier | [Current graphical-abstract route](https://www.elsevier.com/researcher/author/tools-and-resources/graphical-abstract); [generative-AI policy](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals); [Review planning](https://crosstalk.cell.com/blog/how-to-get-started-writing-a-review-article); [Review-figure principles](https://crosstalk.cell.com/blog/frankenfigures-alive-but-easily-misunderstood); [Review-figure classes](https://crosstalk.cell.com/blog/from-mad-scientist-to-artist) | 2026-08-31; AI policy states June 2026 update | Content-class permissions, reproducible data-figure derivation, disclosure, primary-image prohibition, and the ban on general-purpose generative-AI graphical abstracts are HR where the current policy uses mandatory language. Cell Press/Trends editorial advice to plan figures early, add insight, avoid disconnected source panels, and consider cross-source replotting, schematics, or conceptual diagrams is OG; it provides no universal figure-count rule. |
| *Science* flagship / AAAS | [Initial-manuscript route](https://www.science.org/content/page/instructions-preparing-initial-manuscript); [editorial policies](https://www.science.org/content/page/science-journals-editorial-policies) | 2026-08-31: both returned HTTP 403 in this audit | Status is `unverified`; assign no HR/OG from third-party summaries. Manually verify or contact the journal. Science Partner Journal instructions are not substitutes for flagship *Science*. |
| *ACS Nano* | [Author guidelines](https://researcher-resources.acs.org/publish/author_guidelines?coden=ancac3); [ACS AI Best Practices and Policies](https://researcher-resources.acs.org/publish/aipolicy) | accessed 2026-08-31; pages state 2026-07-03 and 2024-12-13 updates, respectively | Stated resolution, width/depth, minimum type/line, accessibility, and file rules are HR. Forward-looking Review storytelling is OG. The AI policy says use should be disclosed, permits disclosed AI cover art, and says AI images should not be used in TOC graphics; those modal statements are OG, with editor discretion. No blanket AI-figure ban or three-line mandate was found. |
| CVPR 2026 | [Author guidelines](https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines); [official author kit](https://github.com/cvpr-org/author-kit); [formatting source](https://github.com/cvpr-org/author-kit/blob/main/sec/2_formatting.tex) | 2026-08-31 | Page limit, current template, two-column geometry, body type, and submission policy are HR. The 9 pt caption/placement wording, print resolvability, redundant color encoding, and `booktabs` table example are OG. The example is not a universal three-line mandate. |
| AAAI-27 | [Submission instructions](https://aaai.org/conference/aaai/aaai-27/submission-instructions/); [Main Technical Track call](https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/); [policies for authors](https://aaai.org/conference/aaai/aaai-27/policies-for-aaai-27-authors/) | 2026-08-31 | Format/page rules are HR. The two official AI pages are not fully harmonized; treat any generative text/image use as `policy conflict`, record the exact track, and seek current clarification instead of inferring permission. No three-line mandate was found. |
| NeurIPS 2026 | [Call for Papers](https://neurips.cc/Conferences/2026/CallForPapers); [Main Track Handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook); [official style archive](https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip); [Paper Checklist](https://neurips.cc/public/guides/PaperChecklist) | 2026-08-31 | Current style, page limit, checklist completion, author responsibility for all figures, disclosure of important/non-standard methodological agent use, and the prompt-injection prohibition are HR. The Position Paper Track is stricter than the main track, so track identity is part of the rule key. Checklist prompts do not create a three-line-table rule. |

## Lock the display contract [PD]

Before drawing or restyling anything, state:

| Field | Required decision |
|---|---|
| Reader question | What should a reader be able to answer after seeing this item? |
| Supported claim | Which claim can the supplied data, studies, or manuscript actually support? |
| Prohibited inference | Which mechanism, ranking, causal arrow, clinical implication, or validation stage must not be added? |
| Display class | Quantitative data figure, experimental image, review schematic, evidence table, or conceptual art? |
| Source | Data/code, cited studies, author synthesis, or licensed asset? |
| Venue | Exact current specification or `pending`? |
| Deliverables | Editable source, submission export, caption, alt text, and provenance record? |

Use `assets/figure_brief.json` as a starting point and route it with:

```bash
python scripts/figure_brief.py figure-brief.json --json routed-brief.json
```

The routed brief is a production contract, not permission to create missing evidence.

## Route by scientific object [PD]

- **Quantitative or statistical figure:** generate from declared data and code. Do not use an image generator. Preserve independent units, denominators, uncertainty, and statistics.
- **Experimental image:** use authentic source observations and an auditable transformation history. Never generate or content-alter microscopy, gels/blots, pathology, spectra, clinical images, or other observations.
- **Review flow, comparison, taxonomy, or decision schematic:** default to editable SVG with real text and semantic groups. Do not imply causality, order, or maturity unless the cited evidence supports it.
- **Conceptual art or graphical abstract:** verify the exact venue's current AI-image and disclosure policy first. If permitted, label it as conceptual, retain the prompt/tool/version/output/human-edit history, and typeset final labels manually.

For deterministic concept figures, `render_concept_svg.py` supports `flow` and `independent_axes` layouts. Its output is an editable SVG, not a data figure:

```bash
python scripts/render_concept_svg.py figure-spec.json figure.svg
```

## Audit semantic coverage before styling [PD]

An axis or comparison-table heading must be a true parent category for every item beneath it. Before locking labels, enumerate the actual endpoint in each row or panel: acellular/manufacturing, physical/mechanical/process, in vitro, ex vivo, animal, human, retrospective, or prospective. If one dimension mixes these contexts, use **Testing / validation context** (`测试与验证情境`) rather than **Biological testing** (`生物学测试`); the latter misclassifies non-biological manufacturing and physical endpoints.

Keep **testing / validation context** and **generalization / boundary** as separate fields. The first records what was measured, where, and prospectively or retrospectively; the second records what population, material family, laboratory, species, scale, or task the conclusion has and has not transferred to. Do not put an animal assay in the generalization column, or “one formulation system” in the testing column.

Use auditable nouns instead of evaluative shorthand. Replace labels such as `strong validation`, `high fidelity`, or `extensive testing` with the exact assay or context—for example, `prospective rat pharmacokinetics`, `multispecies in vivo testing`, `compressive mechanical testing`, or `pilot-scale process yield`. If the manuscript does not report the assay or context, write `not reported` rather than infer strength.

## Publication-neutral three-line tables [PD]

When the user requests an ordinary SCI manuscript table and the exact venue does not prescribe another style, use this project default:

- a top rule, a rule below the header, and a bottom rule;
- no vertical rules, no cell-by-cell grid, and no decorative fill;
- additional horizontal rules only when they mark a real hierarchical group;
- table title above; abbreviation, source, statistical, and missing-value notes below;
- repeated header on continuation pages;
- no fixed row height that can clip content;
- explicit column widths based on content rather than equal columns;
- narrative columns left aligned; numeric columns aligned by magnitude, unit, or decimal;
- `NA`, `not reported`, `not tested`, and `not applicable` kept distinct;
- color retained only when it encodes scientific information, has a legend, and remains interpretable without color.

This is a clean default, not a claim that every SCI journal mandates three-line tables. The current venue template overrides it. Layout tables, formal boxes, and venue-required key-point blocks are not scientific comparison tables and must not be restyled mechanically.

For Word tables, a practical working range is 8.5–9 pt unless the verified venue specifies otherwise. Prefer better column design, concise headings, landscape or supplementary placement, and table splitting over shrinking below legibility. Preserve table text, citations, numbers, merged-cell semantics, repeated headers, and cross-references.

Audit the result with:

```bash
python scripts/visual_audit.py manuscript.docx --expect-three-line --strict
```

The auditor resolves inherited Word table styles, so a `Table Grid` style cannot pass merely because borders are absent from the table's direct properties.

Word border rendering follows a cascade of table styles, direct table/row/cell properties, and merged-cell behavior. If that cascade suppresses an intended three-line rule, set the top border on every cell in the first logical row, the bottom border on every cell in the last header row, and the bottom border on every cell in the last logical row. Do not rely on `w:tblBorders`, a named table style, or XML presence alone. Run the structural audit, render the DOCX through the standard document workflow, and visually inspect the rules on every continuation page at final size; XML-clean but visibly missing or doubled rules are failures.

## Figure production contract [PD]

For an editable review schematic:

1. remove a redundant title from inside the artwork when the caption already carries it;
2. give every panel or axis one scientific job;
3. use direct labels and an obvious reading path;
4. prefer shallow hierarchy, restrained color, and meaningful whitespace over decorative cards;
5. encode important distinctions with position, shape, line style, and text—not color alone;
6. keep lines, arrows, text, and panel labels editable;
7. include SVG `title` and `desc`, then add meaningful DOCX/PDF alt text;
8. export a high-resolution preview only after the vector source passes structural review;
9. inspect the standalone export and the rendered manuscript at final physical size.

Do not force independent dimensions into aligned columns when alignment implies a false one-to-one mapping. Do not use a single arrow as a generic signal of progress when the scientific categories are non-ordinal. Use feedback arrows only when results actually inform another decision round.

## Prompts are bounded specifications [PD]

A useful scientific-visual prompt has three layers:

1. **Scientific contract:** reader question, supported claim, evidence/source, and prohibited inference.
2. **Production instruction:** layout, reading order, language, final size, labels, typography, palette, editable layers, and export.
3. **Audit instruction:** no invented data or mechanisms; check arrows, labels, accessibility, final-size legibility, provenance, license, and venue policy.

Do not ask for a generic “Nature-style” or “top-journal-style” image. Describe the qualities needed—clarity, evidence boundary, restrained hierarchy, accessible encoding, and editable output—without imitating a publisher's visual identity or implying endorsement.

If a host exposes image generation, use the routed prompt only for venue-permitted conceptual artwork. For ordinary review schematics, tables, and data figures, deterministic vector or plotting workflows remain preferable.

## Visual gate [PD]

Run separate checks; do not collapse them into the clean-copy gate:

| Layer | Pass condition |
|---|---|
| Structure | correct table/figure class, borders, captions, dimensions, anchors, fonts, and cross-references |
| Evidence | every data point, arrow, rank, and category is traceable to supplied evidence or declared author synthesis |
| Provenance | editable source, export, tool/code, transformations, license, and disclosure are recorded |
| Venue | the current official instruction was checked for the exact venue and article type |
| Render | standalone final-size export and every manuscript page were visually inspected |

An unprovided manifest, unresolved venue, or unperformed render is `unverified`, not `pass`. A high-resolution PNG can pass resolution while still failing editable-source or provenance review.

## Handoff [PD]

For each changed display item, return:

- the editable source (`SVG`, plotting code and data, or native table);
- the manuscript export;
- the completed figure/table manifest;
- caption and alt text;
- the exact venue rule status and access date;
- final-size, grayscale/accessibility, cross-reference, and rendered-page results;
- unresolved evidence, license, disclosure, or production risk.
