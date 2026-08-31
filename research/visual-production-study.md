# Visual-production research note

Snapshot: 2026-08-31. Official pages and primary GitHub repositories were accessed on this date unless a row states otherwise. This note records operational conclusions rather than copying publisher prose, prompts, templates, or paper figures. Rules are phase- and article-type-specific; the live target-venue instructions remain controlling.

## Rule classes

- **Hard requirement (HR):** explicit mandatory or prohibited language for the exact venue, article type, track, and submission phase. A mismatch can block review, production, or publication.
- **Official guidance (OG):** an official recommendation, typical value, design example, or non-mandatory preference. It is evidence of good practice, not a universal submission rule.
- **Project default (PD):** a CNS evidence-integrity control or production choice used when the target venue is silent. It must never be represented as publisher policy and is displaced by a verified venue rule.

An official example is not automatically an HR. In particular, a `booktabs` example does not prove that a venue mandates three-line tables. Numeric specifications are not transferred between publishers, between a flagship and its portfolio, or between initial and final submission.

## Official-source audit

| Venue and scope | Class | Official source | Auditable conclusion |
|---|---|---|---|
| *Nature*, final main figures | HR + PD; source inconsistency noted | [Final submission](https://www.nature.com/nature/for-authors/final-submission); [figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/); [panel export](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/) | Final artwork uses standard widths of 89 mm or 183 mm, 5–7 pt editable type, 8 pt bold lower-case panel labels, and 0.25–1 pt strokes; the research-figure guide caps ordinary figure height at 170 mm and requires editable vector layers for main figures (**HR**). Its image section calls 300 dpi the photographic minimum and 450 dpi the highest useful online-proof resolution, while its export checklist says images should be at least 450 dpi. Retaining authentic pixels and supplying 450 dpi when available, never artificial upsampling, is the conservative CNS resolution rule (**PD**) while both source statements remain in the venue record. The initial page rounds widths to 90/180 mm, so phase must also be recorded. |
| *Nature*, initial review file | HR + OG | [Initial submission](https://www.nature.com/nature/for-authors/initial-submission) | The review copy must remain assessable. The page recommends preparing near 90/180 mm, no more than 170 mm high, with 5–7 pt type; publication-quality files are requested later. Error bars, exact `n`, replicates, and statistical definitions must be reported when applicable. |
| *Nature*, color and accessibility | HR + OG | [Figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/); [panel/export guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/); [formatting guide](https://www.nature.com/nature/for-authors/formatting-guide) | An accessible palette, labelled axes/units, legible editable type, and standard fonts are stated as required (**HR**). Compact logical panel order, RGB supply, restrained color, avoidance of rainbow scales, color-only cues, colored text, unnecessary panels, and decorative complexity are official directions (**OG**). They are not a transferable “Nature style.” |
| *Nature* Extended Data tables | HR | [Extended Data formatting](https://research-figure-guide.nature.com/figures/extended-data-formatting-guidelines/) | For this exact display class, tables use a rule above and below the column headings and a bottom rule, normally 89 or 180 mm wide, with 7 pt sans-serif text; whitespace should separate data blocks and color should be scientifically necessary. This is direct support for a three-line table only within the stated scope. |
| *Nature*, research-image integrity | HR | [Image integrity](https://research-figure-guide.nature.com/figures/image-integrity/) | The final image must represent the original data; cloning, healing, content-aware manipulation, and generative AI in figures are prohibited by this flagship guide. Whole-image, equal adjustments and original-data retention remain necessary. |
| *Nature Reviews Bioengineering*, Review narrative | OG | [Content types](https://www.nature.com/natrevbioeng/content); [preparing a submission](https://www.nature.com/natrevbioeng/for-authors/preparing-your-submission); [editorial process](https://www.nature.com/natrevbioeng/for-authors/editorial-process); [Review format guide](https://www.nature.com/documents/natrev-articleformatguide-review.pdf) | A Review is balanced, authoritative, accessible, and selective rather than a paper-by-paper catalogue. Approximately 5–7 display items are typical, not guaranteed. Display items should explain specific points or background science; non-primary Review articles do not introduce unpublished research findings, and re-analysis or collated trends require editorial agreement. |
| Cell Press graphical abstract | OG | [Cell Press graphical-abstract article](https://crosstalk.cell.com/blog/attract-readers-at-a-glance-with-your-Graphical-Abstract?hs_amp=true); [current Elsevier graphical-abstract page](https://www.elsevier.com/researcher/author/tools-and-resources/graphical-abstract) | The older Cell Press article supports a single-panel, sparse-text, obvious-reading-path composition. It is historical general guidance, not a current journal-specific specification. The current Elsevier page requires an original representation and routes authors to the individual journal guide. |
| Cell Press/Elsevier, generative visual policy | HR | [Elsevier journal generative-AI policy](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals), policy updated June 2026 | Explanatory schematics may receive AI support only with human oversight and both caption-level and article-level disclosure. Data visualizations must be directly and reproducibly derived from underlying data; primary research images must not be created or altered with generative AI. General-purpose generative-image tools must not create graphical abstracts. Cover-art use requires the publisher/editor route stated by the policy. |
| *ACS Nano*, production graphics | HR | [ACS Nano author guidelines](https://researcher-resources.acs.org/publish/author_guidelines?coden=ancac3), page last updated 2026-07-03 | Minimum raster resolutions are 1200 dpi for line art, 600 dpi for grayscale, and 300 dpi for color. Single-column width is at most 3.33 in; double-column width is 4.167–7 in; maximum depth is 9.167 in including caption allowance. Final lettering is at least 4.5 pt and lines at least 0.5 pt. The guide cites WCAG contrast targets of 4.5:1 for text and 3:1 for non-text elements and warns against color-only distinctions. |
| *ACS Nano*, Reviews and AI-image policy | OG | [ACS Nano author guidelines](https://researcher-resources.acs.org/publish/author_guidelines?coden=ancac3); [ACS AI Best Practices and Policies](https://researcher-resources.acs.org/publish/aipolicy), policy page last updated 2024-12-13 | Reviews should be forward-looking, critically evaluate work from multiple groups, and use clear graphics for key concepts. ACS says AI-assisted text/image generation should be disclosed in Acknowledgments and, for graphics, briefly in the caption; cover AI is permitted with disclosure and tool-use-rights checks, while AI-generated images should not be used in Table of Contents graphics. These are recorded as OG because the cited operative sentences use “should”; editor discretion remains explicit. No universal three-line-table rule or blanket AI-figure ban was found. |
| CVPR 2026, format | HR + OG | [Author guidelines](https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines); [official author kit](https://github.com/cvpr-org/author-kit); [formatting source](https://github.com/cvpr-org/author-kit/blob/main/sec/2_formatting.tex) | The review paper is limited to eight content pages including figures and tables and must use the current template; the kit fixes two 3.25-in columns and 10 pt Times body text (**HR**). It says captions should use 9 pt Roman, with table captions above and figure captions below (**OG**). Page-limit/template noncompliance can cause rejection without review. |
| CVPR 2026, table/figure design | OG | [Official formatting source](https://github.com/cvpr-org/author-kit/blob/main/sec/2_formatting.tex) | The official example uses `toprule`/`midrule`/`bottomrule`, but this is an example rather than an explicit mandate. The guide asks that claims remain resolvable in print, figure type be comparable with body type, and color carry a redundant discriminator. The repository exposes no clear top-level general reuse license; use it as the submission template, but do not redistribute it inside CNS without permission analysis. |
| CVPR 2026, author AI use | HR + PD | [Author guidelines and FAQ route](https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines) | The official FAQ allows authors to use tools they find productive but makes them responsible for misrepresentation, factual error, and plagiarism; prompt injection is prohibited (**HR**). Requiring authentic data inputs, a transformation log, and provenance review for every generated visual is the stricter CNS control (**PD**), not a separate CVPR image-generation rule. |
| AAAI-27, format | HR | [Submission instructions](https://aaai.org/conference/aaai/aaai-27/submission-instructions/) | Use the AAAI-27 two-column author kit and a high-resolution US-Letter PDF with embedded Type 1 or TrueType fonts. The main PDF permits seven non-reference pages plus two reference-only pages. No three-line-table mandate was found. |
| AAAI-27, AI policy | HR, unresolved official conflict | [Main Technical Track call](https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/); [policies for authors](https://aaai.org/conference/aaai/aaai-27/policies-for-aaai-27-authors/) | The current track call says authors may judiciously use LLMs and image generators while retaining responsibility. A separate AAAI-27 author-policy page prohibits LLM-generated manuscript text except as experimental material but permits editing/polishing of author-written text. Do not infer a single blanket rule or assume image generation is accepted; record the exact track and obtain current conference clarification if the intended use falls in the gap. |
| NeurIPS 2026, format, checklist, and author AI use | HR | [Call for Papers](https://neurips.cc/Conferences/2026/CallForPapers); [Main Track Handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook); [official 2026 style archive](https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip); [Paper Checklist](https://neurips.cc/public/guides/PaperChecklist) | Use the current LaTeX style and keep main content, including figures and tables, within nine pages; complete the checklist. Its questions require transparent uncertainty and provenance reporting when applicable, not a three-line table. Main-track authors may use preparation tools but remain responsible for every figure and must disclose important/non-standard methodological agent or LLM use; prompt injection is prohibited. The Position Paper Track has a stricter substantially-human-written rule, so the track must be recorded. |
| *Science* flagship | Unverified; no rule class assigned | [Initial-manuscript route](https://www.science.org/content/page/instructions-preparing-initial-manuscript); [editorial-policy route](https://www.science.org/content/page/science-journals-editorial-policies) | Both flagship routes returned HTTP 403 during the 2026-08-31 audit. No third-party dimensions, fonts, resolutions, or AI-image claims were promoted to HR/OG. The author must verify the live official pages or contact the journal before submission; Science Partner Journal pages are not substitutes for flagship *Science*. |

## Three-line-table conclusion

| Situation | Class | CNS action |
|---|---|---|
| *Nature* Extended Data table | HR | Apply the specified top/header/bottom rule logic and its size/type constraints. |
| CVPR official example | OG | A sparse `booktabs` table is supported as an example, but do not describe it as mandatory. |
| ACS Nano, AAAI-27, or NeurIPS 2026 | PD only if a fresh venue check remains silent | No explicit three-line mandate was found in the audited official sources; recheck the exact current template before applying the default. |
| Venue silent | PD | Use top, header, and bottom rules; omit vertical gridlines and decorative fill; add internal rules only for real hierarchy; keep title, notes, abbreviations, and statistical definitions outside the data body. |

The practical 8.5–9 pt Word-table range used by CNS is PD, not a publisher specification. Legibility should be recovered by editing headings, widths, orientation, splitting, or supplementary placement before shrinking type.

## Applied bilingual-review feedback [PD]

The 2026-08-31 bilingual-review production pass exposed three reusable failure modes. These are manuscript-derived CNS controls, not publisher requirements:

| Observed failure | Generalizable CNS decision |
|---|---|
| A figure axis and table column were labelled `Biological testing`, but their rows also contained acellular/manufacturing and physical/mechanical/process endpoints. | Audit every row against its parent label. For mixed endpoint classes, use `Testing / validation context` / `测试与验证情境`; reserve `Biological testing` for a genuinely biological-only set. |
| Testing context and transfer scope were combined, allowing assays and system boundaries to migrate between columns. | Keep `testing / validation context` separate from `generalization / boundary`. State the exact assay/context and the exact untested or transferred domain; do not replace either with `strong validation`, `high fidelity`, or similar ordinal shorthand. |
| Table-level OOXML contained the intended three-rule pattern, but style precedence suppressed visible rules in the rendered document. | When needed, apply cell-level borders across the first logical row (top), final header row (bottom), and last logical row (bottom). Passing XML inspection is insufficient: render the DOCX and inspect every initial and continuation page at final size. |

## Review-article visual narrative

The following are PD synthesized from the official Review guidance above; they are not venue mandates:

1. Give each display item one reader question, one supported takeaway, and an explicit prohibited inference.
2. Make the display sequence carry the review's argument: scope or taxonomy, comparative evidence, mechanism or workflow, translational/validation bottlenecks, and actionable outlook. Do not allocate one figure mechanically to every section.
3. Use tables when readers must compare repeated fields across many studies; use diagrams for relationships, workflows, taxonomies, or decision logic; use data plots only when values can be regenerated from a declared dataset and method.
4. A Review figure may synthesize cited work but must distinguish literature-derived content from author interpretation. An arrow is a claim, not decoration.
5. Keep all labels, categories, ranks, maturity levels, and causal links traceable to citations or an explicitly declared author synthesis. Do not reconstruct a published figure merely by changing colors or layout.
6. Budget display items against the target article type. The 5–7 figure/table/box range is typical for a *Nature Reviews Bioengineering* Review, not a universal quota.

## Open-source design lineage and license audit

| Project | License observed on 2026-08-31 | Principle learned | Reuse boundary |
|---|---|---|---|
| [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) and its [scientific-visualization skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md) | root repository and relevant skill identified as MIT; individual skills and dependencies can differ | problem-first display design, raw-input/transformation/export separation, physical-size QA, and live venue verification | independently re-expressed; no prompt, code, template, or asset copied |
| [academic-figure-skill](https://github.com/TingxiYu/academic-figure-skill) | root `LICENSE` is Apache-2.0; README also calls the license MIT in one internal description | figure contracts, vector-first output, reusable plotting, and multi-pass visual QA | license inconsistency is a release risk; no content imported |
| [ResearchFigureSkill](https://github.com/KaiyiHu/ResearchFigureSkill) | MIT | evidence-locked conceptual diagrams and deterministic text/arrows | visual grammar may be studied; examples cannot supply manuscript evidence |
| [SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | CC BY 4.0 for original content; underlying tools remain separately licensed | registry-based discovery, typed task templates, and validation | copied/adapted prose would require attribution; CNS implementation is independent |
| [paper-figures / StatMate](https://github.com/DRZ-hang/paper-figures) | former URL redirected to `DRZ-hang/StatMate`; current root license observed as MIT | reproducible raw-data → statistics → figure/table routing | identity is moving and examples/data may have separate terms; pin and re-audit before reuse |
| [SciencePlots](https://github.com/garrettj403/SciencePlots) | MIT | plotting presets can improve consistency | a preset does not establish accuracy, accessibility, or venue compliance |
| [Great Tables](https://github.com/posit-dev/great-tables) | MIT | generate tables from structured values rather than raster screenshots | manuscript tables must remain editable and semantically intact |
| [Anthropic skills](https://github.com/anthropics/skills) | mixed: many examples are Apache-2.0, while `docx`, `pdf`, `pptx`, and `xlsx` are explicitly source-available rather than open source | progressive disclosure and render-and-inspect architecture | restricted document-skill content is comparison-only and was not copied |

License conclusions are deliberately file-specific:

- MIT or Apache-2.0 can permit reuse only after exact-file scope and applicable notice/attribution duties are checked; Apache-derived modified files also require the license's modification notices.
- CC BY 4.0 requires attribution for copied or adapted expression; citing a high-level design influence is not a license shortcut.
- Source-available content is not treated as open source.
- A public repository with no explicit license grants no general redistribution right.
- Publisher author kits may be used to format the intended submission, but that purpose does not automatically authorize repackaging them in a skill repository.
- A paper's open-access license, the license on its data, and rights in individual figures or third-party assets must be checked separately.

No restricted prompt, long instruction block, code, template, dataset, icon, font, or figure was copied into CNS Skills.

## Resulting CNS decision

The reusable unit is a bounded, classified production loop rather than a universal aesthetic:

```text
reader question + supported claim + prohibited inference
  → display-class routing
  → data/code, authentic image, editable vector, or policy-cleared conceptual art
  → evidence + provenance + accessibility + venue-phase + render checks
  → HR/OG/PD record with source and access date
```

Three-line tables, vector-first review schematics, color-redundant encodings, editable deliverables, and final-size inspection are PD when the venue is silent. Exact dimensions, fonts, resolutions, file formats, disclosure, and generative-image permission are never guessed: they must be attached to the current official venue, article type, track, and submission phase.
