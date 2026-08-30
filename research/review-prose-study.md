# Review-prose study: keeping editorial scaffolding out of the manuscript

## Scope and method

This study examined 24 English review or perspective articles in machine learning, materials science, biomaterials, drug discovery, and autonomous experimentation. It was designed to answer a narrow editorial question: how do published reviews synthesize studies without repeatedly describing their own prose as an "evidence chain", "framework", "landscape", or similar abstraction?

Two complementary sets were used:

1. **Full-text lexical set:** 12 open-access articles available through PMC and Europe PMC. Approximately 137,000 words of body paragraphs were searched for the exact terms `evidence`, `framework`, `dataset`/`data set`, `pipeline`, `paradigm`, and `landscape`. Reference lists were excluded.
2. **Editorial calibration set:** 12 reviews and perspectives from *Nature*, *Nature Reviews*, *Science*, *Trends*, and Cell Press journals. Their abstracts, available sections, and paragraph-level rhetorical choices were read qualitatively.

This is a prose study, not a systematic literature review or a ranking of venues. The conclusions below are cross-article observations, not rules inferred from any single paper. No article text is redistributed here; examples are paraphrases or newly written schematic revisions.

## Main quantitative observation

Across the 12 full-text articles:

| Exact term | Body-text occurrences |
|---|---:|
| `evidence` | 2 |
| `framework` / `frameworks` | 99 |
| `dataset` / `data set` and plurals | 439 |
| `pipeline` / `pipelines` | 18 |
| `paradigm` / `paradigms` | 16 |
| `landscape` / `landscapes` | 21 |

The exact word `evidence` appeared only twice in roughly 137,000 words, both in one article. The other 11 full-text reviews did not use it in their body paragraphs.

This does **not** mean that scientific reviews avoid reasoning from evidence. Rather, they usually name the study, material, measurement, result, comparison, or limitation directly. `Framework` and `dataset` remain common because they often denote real computational structures or bounded data collections.

## Full-text lexical corpus

| Article | Venue and year | Role in analysis |
|---|---|---|
| [Applied machine learning as a driver for polymeric biomaterials design](https://pmc.ncbi.nlm.nih.gov/articles/PMC10415291/) | *Nature Communications*, 2023 | Biomaterials synthesis and concrete data limitations |
| [A User's Guide to Machine Learning for Polymeric Biomaterials](https://pmc.ncbi.nlm.nih.gov/articles/PMC10103193/) | *ACS Polymers Au*, 2023 | Tutorial-style paragraph organization |
| [Emerging Trends in Machine Learning: A Polymer Perspective](https://pmc.ncbi.nlm.nih.gov/articles/PMC10273415/) | *ACS Polymers Au*, 2023 | Workflow terms used with explicit components |
| [Machine Learning in Polymer Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC11923530/) | *Advanced Materials*, 2025 | Broad polymer review and study-level synthesis |
| [Biomaterials by design: Harnessing data for future development](https://pmc.ncbi.nlm.nih.gov/articles/PMC8628044/) | *Materials Today Bio*, 2021 | Cross-material synthesis |
| [Machine-Learning-Assisted De Novo Design of Organic Molecules and Polymers](https://pmc.ncbi.nlm.nih.gov/articles/PMC7023065/) | *Polymers*, 2020 | Generative-design terminology |
| [Machine Learning of Coarse-Grained Models for Organic Molecules and Polymers](https://pmc.ncbi.nlm.nih.gov/articles/PMC7841771/) | *ACS Omega*, 2021 | Model and representation language |
| [Big data and machine learning for materials science](https://pmc.ncbi.nlm.nih.gov/articles/PMC8054236/) | *Discover Materials*, 2021 | Data-resource terminology |
| [Artificial Intelligence-Powered Materials Science](https://pmc.ncbi.nlm.nih.gov/articles/PMC11803041/) | *Nano-Micro Letters*, 2025 | Recent broad materials review |
| [Machine Learning-Enhanced Nanoparticle Design for Precision Cancer Drug Delivery](https://pmc.ncbi.nlm.nih.gov/articles/PMC12376635/) | *Advanced Science*, 2025 | Nanoparticle and translational language |
| [A Review of Performance Prediction Based on Machine Learning in Materials Science](https://pmc.ncbi.nlm.nih.gov/articles/PMC9457802/) | *Nanomaterials*, 2022 | Prediction-focused review |
| [The Role of Machine Learning and Design of Experiments in Biomaterial and Tissue Engineering Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC9598592/) | *Bioengineering*, 2022 | The only two body-text occurrences of `evidence` |

## Editorial calibration corpus

| Article | Venue and year |
|---|---|
| [Machine learning for biomaterials design](https://doi.org/10.1038/s44222-026-00476-w) | *Nature Reviews Bioengineering*, 2026 |
| [Machine learning for molecular and materials science](https://doi.org/10.1038/s41586-018-0337-2) | *Nature*, 2018 |
| [Emerging materials intelligence ecosystems propelled by machine learning](https://doi.org/10.1038/s41578-020-00255-y) | *Nature Reviews Materials*, 2021 |
| [Nanoparticle synthesis assisted by machine learning](https://doi.org/10.1038/s41578-021-00337-5) | *Nature Reviews Materials*, 2021 |
| [Machine learning methods to model multicellular complexity and tissue specificity](https://doi.org/10.1038/s41578-021-00339-3) | *Nature Reviews Materials*, 2021 |
| [Applications of machine learning in drug discovery and development](https://doi.org/10.1038/s41573-019-0024-5) | *Nature Reviews Drug Discovery*, 2019 |
| [Rethinking drug design in the artificial intelligence era](https://doi.org/10.1038/s41573-019-0050-3) | *Nature Reviews Drug Discovery*, 2020 |
| [Inverse molecular design using machine learning](https://doi.org/10.1126/science.aat2663) | *Science*, 2018 |
| [Next-Generation Experimentation with Self-Driving Laboratories](https://doi.org/10.1016/j.trechm.2019.02.007) | *Trends in Chemistry*, 2019 |
| [Autonomous experimentation systems for materials development](https://doi.org/10.1016/j.matt.2021.06.036) | *Matter*, 2021 |
| [Redefining biomaterial biocompatibility](https://doi.org/10.1016/j.tibtech.2023.09.015) | *Trends in Biotechnology*, 2024 |
| [Advancements and prospects of deep learning in biomaterials evolution](https://doi.org/10.1016/j.xcrp.2024.102116) | *Cell Reports Physical Science*, 2024 |

## Cross-article prose findings

### 1. Strong paragraphs discuss scientific objects, not the manuscript's machinery

Common paragraph subjects include:

- experimental measurements and datasets;
- polymer structures and processing conditions;
- degradation rates and biological endpoints;
- transfer learning and model representations;
- scaffold fabrication and candidate selection;
- active-learning acquisition functions;
- disagreement between in vitro and in vivo behavior;
- named databases, models, or studies.

The prose rarely makes `the evidence`, `the framework`, or `the landscape` the grammatical actor unless one of those words denotes a real technical object.

### 2. Paragraph openings usually perform one of four moves

- Name the local scientific problem.
- Introduce a material, model, or measurement.
- State a concrete limitation.
- Position a named approach or study against an earlier one.

Meta-openings such as "This evidence demonstrates...", "From an evidence perspective...", and "Within this framework..." hide the object under discussion and give the sentence less information to carry forward.

### 3. Synthesis is organized around a comparison axis

Effective review paragraphs compare studies by an explicit axis, such as:

- experimental versus simulated labels;
- retrospective prediction versus prospective candidate testing;
- chemical composition versus processing history;
- in vitro versus in vivo degradation;
- interpolation versus extrapolation;
- manual execution versus model-selected experiments.

Citation density alone is not synthesis. Several citations placed together may show recurrence, disagreement, or merely topic coverage; the prose must state which relation applies.

### 4. Citations stay close to the supported clause

When a paragraph introduces several studies, references generally appear beside the corresponding method, material, result, or limitation. A citation cluster at the end of a broad paragraph cannot show which source supports which assertion.

### 5. Limitations are expressed through the source of failure

The more informative prose specifies that:

- measurements are few;
- protocols differ across laboratories;
- molecular structures are incompletely recorded;
- processing conditions are absent;
- labels come from simulations rather than experiments;
- biological endpoints are indirect;
- external or prospective validation is missing.

"Evidence remains limited" is weaker because it does not tell the reader what is missing or which conclusion is affected.

## Vocabulary gates

### `Evidence`

Use only when it denotes a recognizable evidentiary basis, preferably with a modifier:

- experimental evidence;
- clinical evidence;
- genetic evidence;
- visual evidence;
- causal evidence.

Avoid using it as generic connective tissue:

- evidence chain;
- evidence stitching;
- evidence layer;
- evidence landscape;
- evidence-generating narrative;
- multidimensional evidence profile.

Claim ledgers and evidence chains are useful editorial tools, but their labels should normally remain in internal notes.

### `Dataset`

Use when referring to a bounded collection whose contents can be described:

- an experimental dataset of measured degradation times;
- a microscopy-image dataset;
- training, validation, or external-test datasets;
- a named public database.

Do not call the literature as a whole `the dataset` unless a formal corpus was actually constructed. Depending on the referent, use `studies`, `reports`, `measurements`, `images`, `sequences`, `records`, `formulations`, or `screening results`.

### `Framework`

Use for a named architecture, theory, evaluation scheme, or explicitly defined set of components. If the reader cannot answer "which components, and how are they connected?", replace the word with those components.

### `Pipeline`

Use only when a real ordered sequence is being described, for example data collection → featurization → training → validation. Do not use `pipeline` as a prestige synonym for research activity.

### `Landscape` and `paradigm`

Use sparingly and only with a concrete referent: a chemical search landscape, phase landscape, or defined design-build-test-learn regime. Avoid generic phrases such as "the evolving evidence landscape" or "a transformative paradigm" when a direct description is possible.

## Executable editing rules for CNS Skills

1. **Keep editorial scaffolding internal.** Claim ledgers, source locks, evidence chains, and paragraph-function labels guide revision; they are not default manuscript vocabulary.
2. **Replace meta-nouns with scientific referents.** Ask what was measured, predicted, compared, synthesized, validated, or omitted.
3. **Give each paragraph one scientific question or comparison axis.**
4. **Put the finding before its editorial interpretation.**
5. **Attach citations to the smallest supportable claim.**
6. **Name the source and consequence of every important limitation.**
7. **Run a concordance, not a blacklist.** Review every occurrence of `evidence`, `framework`, `dataset`, `pipeline`, `landscape`, `paradigm`, `bridge`, `loop`, and `closure`; retain technically necessary uses.
8. **Require a referent test.** If the noun cannot be replaced by a named object, method, measurement, or study, it is probably rhetorical filler.
9. **Do not force symmetrical paragraphs.** Paragraph length and syntax should follow the inferential load.
10. **Use `we review`, `we survey`, and `we discuss` mainly for scope-setting.** Once scope is established, return to the studies and scientific problem.
11. **Do not infer strength from citation count.** Multiple citations do not by themselves establish agreement, validation, or generality.
12. **Do not optimize for detector scores.** Naturalness should come from defensible selection, concrete judgment, and author-controlled reasoning.

## Schematic rewrites

| Meta-language | Object-level revision |
|---|---|
| "The evidence chain demonstrates that data quality is the main bottleneck." | "Available measurements are few, use incompatible protocols, and often omit processing history; models trained on them therefore generalize poorly across laboratories." |
| "This framework bridges prediction and experimentation." | "The model ranks candidate formulations, the instrument prepares the next batch, and assay results update the acquisition function." |
| "The evidence remains limited." | "Most reports evaluate held-out historical data; prospective synthesis and external biological testing remain uncommon." |
| "The dataset landscape is fragmented." | "Polymer measurements are distributed across incompatible databases, and many records lack molecular weight, processing conditions, or assay metadata." |
| "These studies form a robust evidence base." | "The studies agree on the direction of the association, but they use different endpoints and none tests transfer to an independent laboratory." |

These rewrites are schematic. Counts, study coverage, and scientific details must be replaced with verified manuscript-specific information before use.
