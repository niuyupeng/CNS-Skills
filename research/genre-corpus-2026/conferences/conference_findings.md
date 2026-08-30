# Top-conference writing corpus: findings from 200 papers

## What was actually analysed

This corpus contains **exactly 200 English accepted main-conference papers**: 40 each from AAAI, CVPR, NeurIPS, ICML, and ICLR. All records are from the 2025 conference year, the most recent common finalized year available from the five official proceedings at the time of access (2026-08-30). The design is a deterministic systematic sample, not a ranking-based or citation-based selection.

| Venue | Records | Title obtained | Abstract obtained | Official PDF text extracted | Median PDF pages | Eligible frame |
|---|---:|---:|---:|---:|---:|---:|
| AAAI | 40 | 40 | 40 | 40 | 9.0 | 2903 |
| CVPR | 40 | 40 | 40 | 40 | 11.0 | 2871 |
| NeurIPS | 40 | 40 | 40 | 38 | 32.0 | 5286 |
| ICML | 40 | 40 | 40 | 40 | 22.0 | 3330 |
| ICLR | 40 | 40 | 40 | 37 | 25.0 | 3703 |

Across the corpus, title-level analysis was possible for **200/200**, abstract-level analysis for **200/200**, and PDF-derived full-text structural analysis for **195/200**. “Full text” here means that an official PDF was downloaded, validated, and converted to at least 800 word tokens. It does **not** mean that every equation, citation, or supplementary appendix was manually read line by line. The five records without successful PDF extraction remain explicitly labelled `abstract_only` in the manifest.

## Descriptive writing patterns

### Titles and abstracts

- The median title length was **9.0 words** (interquartile range 7.75–11.0); the median abstract length was **181.0 words** (IQR 155.75–210.25). These are observations, not recommended quotas.
- Abstract move detection found context/problem language in **128/200**, a gap or contrast move in **127/200**, a method/resource introduction in **169/200**, an empirical/theoretical result move in **138/200**, and an implication or boundary cue in **121/200**. Strong abstracts usually compress a problem, a precise intervention, and an evidenced result; they do not merely announce a topic.
- The introduction contained an explicit contribution marker or list in **62/195** PDF-extracted papers. This is a useful conference navigation device under page and reviewer-time pressure, but it is not a universal requirement and should not be copied mechanically into a scholarly review.

### Positioning and method narrative

- Dedicated Related Work sections were often placed early or between method and experiments, but **165/195** papers had no separately detected Related Work heading. The latter may integrate positioning into the Introduction or method discussion. Therefore, “must have a Related Work section” is not supported as a universal rule.
- Method narration typically moved from preliminaries/problem formulation to an isolated method or approach, making the paper’s technical delta inspectable. The transferable mechanism is **claim → design choice → evidence**, not any fixed heading name.
- Conference papers repeatedly name the nearest strong comparator and the simple baseline. Comparator language appeared in **195/195** PDF-extracted papers. This is transferable to reviews as explicit comparison among methods, assumptions, datasets, and validation settings.

### Experiments, uncertainty, and failure boundaries

- Ablation terminology appeared in **126/195** papers; uncertainty/variance/statistical-testing language appeared in **100/195**. Presence does not prove adequacy, but it exposes what is supposed to cause an improvement and how stable the result is.
- A dedicated limitations section was detected in **6/195**, an ethics/impact section in **11/195**, and a checklist in **37/195**. The strong venue effect visible in the per-venue JSON confirms that some of this structure is induced by submission policy, not by a universal scientific prose law.
- A conclusion-like section was detected in **45/195** papers. Effective conclusions recapitulate the scoped contribution and decisive evidence, then state a real boundary or implication; generic “future work” inventories add little.

### Figures and tables

Caption identifiers were detected from PDF text as an approximate structural signal. The median was **5.0 figure captions** and **3.0 table captions** per successfully extracted paper. Because appendix displays and two-column extraction can affect counts, these should not be treated as exact display limits. The reusable editorial principle is that each display should support one auditable inferential step and remain legible at final column width.

## What can transfer to a review article

1. **First-page contract.** State the field-level problem, the unresolved decision, the review’s organizing contribution, and its evidence boundary early. A review needs a synthesis claim, not an algorithmic novelty claim.
2. **Explicit comparison.** Compare model families against the same dimensions—input, assumption, task, validation, failure mode, and decision role—just as conference papers compare methods under common datasets and metrics.
3. **Claim–evidence proximity.** Put the supporting study or table next to the claim it supports; distinguish computational prediction, retrospective analysis, wet-lab validation, and adaptive experimental feedback.
4. **Alternative explanations and robustness.** Translate “baselines and ablations” into a review-appropriate question: do reported gains survive dataset split, proxy choice, laboratory/batch variation, simpler models, and external or prospective validation?
5. **Visible limitations.** State where the sampled literature, data, and validation layers stop supporting a conclusion. A candid boundary is more credible than a generic limitations paragraph.
6. **Figure-led reasoning.** Design figures/tables around reader questions and comparison axes, not around a catalogue of studies.

## What must not be transferred mechanically

1. **Page-limit compression.** Seven-to-nine-page conference architectures and dense contribution bullets are responses to page limits and reviewer workflow. They are not a model for the pacing of a long-form review.
2. **“Our contributions are” boilerplate.** A review may identify its synthesis contribution, but numbered novelty claims can sound artificial when the real value is selection, comparison, and judgment.
3. **Standalone Related Work as a compulsory section.** Reviews *are* literature synthesis. Positioning should be distributed through the argument unless a dedicated historiographic section has a real function.
4. **Leaderboard logic.** Benchmark wins cannot be used as the sole comparison scale for biomaterials, where data provenance, experimental action, biological fidelity, and transfer conditions matter.
5. **Ablation as a literal review requirement.** A review cannot ablate other researchers’ studies. The transferable analogue is sensitivity to inclusion choices, evidence layers, proxy endpoints, and alternative interpretations.
6. **Venue checklists and impact statements.** NeurIPS checklists, ICML impact statements, anonymity conventions, and track-specific ethics forms are policy artefacts. Preserve their substantive questions, not their headings or boilerplate.
7. **Appendix dependence.** A conference supplement may house detail because of page limits. A review’s central search boundary and evidence qualifications must remain visible in the main narrative or a clearly linked methods/supplement record.

## Assessment of the supplied “2.1 Search approach and scope” passage

The passage is **methodologically legitimate for a structured narrative review**, and top journals do sometimes describe databases, search concepts, dates, and inclusion priorities. Prestige does not require hiding the search method. The problem is not that it lists search terms; the problem is that the current paragraph blurs several different operations and repeats its non-systematic boundary.

- `PubMed` is a discovery database, whereas publisher platforms and DOI landing pages are mainly retrieval or metadata-verification routes. “Author-organized full text” is a local corpus source, not an independently reproducible search source. Separate **discovery**, **deduplication/screening**, **metadata verification**, and **full-text retrieval**.
- Saying that two long term blocks “were combined” is only reproducible if the combinations, fields, filters, and date limits were actually logged. If no exact query log exists, call them *core concept blocks* and provide representative strings or a supplementary search log rather than implying a fully reproducible Boolean strategy.
- The first and final paragraphs both say that coverage was not estimated and the corpus is not exhaustive. Merge them once, close to the selection-purpose statement.
- “Representative” and “methodologically informative” are judgment-based criteria. Name who made the selection or at least state that selection was purposive and synthesis-oriented. Do not infer prevalence from the selected studies.
- The inclusion hierarchy is strong: AI must change candidate/experiment ordering, real fabrication or biological testing receives priority, and method-only or other-material autonomous cases are kept as capability analogies. Preserve this hierarchy because it prevents prediction-only work from being described as completed biomaterials discovery.
- Conference-paper habits cannot decide the form of this review Methods subsection. The appropriate benchmark is the target journal’s article type and reporting expectations. A compact main-text account plus an auditable supplementary search log is often cleaner than a long keyword inventory, but the exact choice is venue-specific.

A stronger underlying structure is:

> **Review type and purpose → discovery sources and date → concept blocks/query record → screening and purposive selection → metadata/full-text verification → use of adjacent-field examples → non-systematic limits and prohibited inferences.**

This preserves transparency without presenting the work as a systematic review or claiming an unknowable coverage rate.

## Interpretation limits

This is a writing-genre study, not a bibliometric estimate of all accepted papers. Equal allocation gives each venue the same voice despite different proceedings sizes. Regex-assisted structural signals were checked against extracted text but may miss unconventional headings or misread appendices. No causal claim is made that any observed feature increases acceptance probability. Official author guidelines and live submission forms remain authoritative for page limits, checklists, ethics statements, and AI-use disclosures.
