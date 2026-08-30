# Provenance and sampling record

## Corpus identity

- Corpus: 200 English review/review-type records used for genre analysis.
- Publication window: 2021-01-01 through 2026-08-30.
- Access and update date: 2026-08-30.
- Design: purposive, stratified venue-quota sample; not a systematic review, random sample, journal ranking, citation ranking or estimate of all top-journal reviews.
- Exact-count gate: 200 rows, 200 unique persistent IDs, 200 unique DOI values and zero duplicate persistent IDs.
- Metadata gate: all 200 DOI records resolved through Crossref; all normalized Crossref/Europe PMC titles exceeded the predefined similarity threshold, with zero title records left for manual mismatch review.

## Authoritative and legal sources

- Candidate discovery and PubMed-derived metadata: [Europe PMC REST API](https://europepmc.org/RestfulWebService), whose `MED` records expose PubMed identifiers, publication types, abstracts and links.
- Persistent identifier and title verification: [Crossref REST API](https://api.crossref.org/).
- Open full text: [Europe PMC](https://europepmc.org/), accessed only when a PMCID full-text XML endpoint was legally available.
- Reporting interpretation: [PRISMA 2020 expanded checklist](https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-yc78.pdf), [Nature clinical research policy](https://www.nature.com/nature/editorial-policies/clinical-research) and [Nature Reviews Materials author guidance](https://www.nature.com/natrevmats/for-authors/preparing-your-submission), all accessed on 2026-08-30.

No publisher PDF, abstract or article body was stored in this directory. Abstracts and Europe PMC JATS XML were processed transiently in memory. The manifest contains bibliographic metadata and derived codes only. It does not reproduce article prose, full search strings or figures.

## Candidate query and venue strata

For every venue, the candidate query was:

```text
JOURNAL:"<Europe PMC journal name>" AND PUB_TYPE:"Review" AND LANG:eng AND FIRST_PDATE:[2021-01-01 TO 2026-08-30]
```

The 20 searches returned 7,245 candidate records before quotas. Candidate counts are an API snapshot, not deduplicated field-wide literature counts.

| Stratum | Venue | Candidate records | Final quota | Selection rationale |
|---|---|---:|---:|---|
| CNS flagship | Nature | 163 | 10 | Broad-selective, cross-disciplinary review genre |
| CNS flagship | Science | 243 | 10 | Broad-selective, cross-disciplinary review genre |
| CNS flagship | Cell | 208 | 10 | Broad-selective life-science review and synthesis genre |
| Nature Reviews | Nature Reviews Materials | 16 | 10 | Materials and biomaterials specialist review title |
| Nature Reviews | Nature Reviews Bioengineering | 12 | 10 | Bioengineering specialist review title |
| Nature Reviews | Nature Reviews Chemistry | 267 | 10 | Chemistry and materials specialist review title |
| Nature Reviews | Nature Reviews Drug Discovery | 208 | 10 | Discovery and translation specialist review title |
| Nature Reviews | Nature Reviews Molecular Cell Biology | 272 | 10 | Mechanistic life-science specialist review title |
| Nature Reviews | Nature Reviews Cancer | 258 | 10 | Disease biology and translation specialist review title |
| Nature Reviews | Nature Reviews Microbiology | 283 | 10 | Microbiology and biotechnology specialist review title |
| Nature specialist | Nature Materials | 79 | 10 | Selective primary journal with review/perspective content |
| Nature specialist | Nature Nanotechnology | 74 | 10 | Selective nano/bio-interface journal |
| Nature specialist | Nature Biomedical Engineering | 52 | 10 | Selective interdisciplinary bioengineering journal |
| Nature specialist | Nature Biotechnology | 45 | 10 | Selective biotechnology journal |
| Nature specialist | Nature Methods | 81 | 10 | Selective methods journal |
| Materials/chemistry reviews | Chemical Reviews | 1,206 | 10 | Field-leading chemistry review journal |
| Materials/chemistry reviews | Advanced Materials | 2,037 | 10 | Selective materials journal with review/progress-report genres |
| Specialist review leaders | Advanced Drug Delivery Reviews | 1,063 | 10 | Field-leading drug-delivery review journal |
| Specialist review leaders | Trends in Biotechnology | 569 | 10 | High-selectivity trends/opinion/review venue |
| Specialist review leaders | Annual Review of Biomedical Engineering | 109 | 10 | Field-leading annual review series |

## Inclusion, exclusion and selection

Included records had to be English, fall inside the declared date window, be tagged as a Review in the Europe PMC/PubMed metadata, have a title, and have a stable DOI or PMID. Corrections, errata, retractions and withdrawn notices were excluded. DOI was the primary deduplication key; PMID or normalized title was the fallback.

Each venue contributed exactly 10 records. Selection was relevance-weighted toward life science, materials, biomaterials, bioengineering, nanomedicine, drug delivery, AI, computation, automation and adjacent method topics. Citation count provided a small secondary signal; year coverage was spread across 2021-2026 where available. A disclosed bonus favored legally accessible Europe PMC full text because the task required structural analysis. Where metadata explicitly indicated systematic, scoping or meta-analytic subtypes, these labels were retained; where it did not, records were coded `review_narrative_or_unspecified` rather than being silently declared narrative.

This process deliberately favors relevant and legally analyzable examples. It is not a probability sample and cannot estimate the frequency of any feature across a journal, publisher or field.

## Actual analysis levels

| Level | Records | Fraction | Coding authority |
|---|---:|---:|---|
| Full text XML | 42 | 21.0% | Title, abstract and body structure; review-search reporting fields assessed |
| Abstract | 157 | 78.5% | Title and abstract moves only; body-level search reporting marked not assessed |
| Title | 1 | 0.5% | Metadata and title indicators only |

The full-text subset consisted of 40 `review_narrative_or_unspecified` and 2 `perspective_review_type` records. The systematic/scoping/meta-labelled records did not have Europe PMC full text in this snapshot, so this corpus cannot compare their body-level reporting with narrative reviews.

The 42 full texts were strongly concentrated in a few Europe PMC-accessible venues:

| Venue | Full texts |
|---|---:|
| Nature Reviews Materials | 10 |
| Nature Reviews Bioengineering | 9 |
| Chemical Reviews | 6 |
| Nature Reviews Microbiology | 5 |
| Nature Reviews Molecular Cell Biology | 4 |
| Nature Reviews Drug Discovery | 3 |
| Annual Review of Biomedical Engineering | 2 |
| Advanced Materials | 1 |
| Nature Reviews Cancer | 1 |
| Nature Reviews Chemistry | 1 |

This distribution reflects PMC/Europe PMC deposit and embargo availability, not editorial prevalence. It is a major access bias and is why full-text findings are always reported with `n=42`.

## Coding rules

- `actual_analysis_text_level` records the deepest text layer actually obtained and machine-analysed: title, abstract or full-text XML.
- Abstract silence never became a body-level negative. Abstract/title-only records use `not_assessed_without_full_text` for explicit review-search methods and `not_assessed` for component fields.
- A full-text record was coded as having an explicit review search only when the article's own literature-search context contained a search statement plus a database, search-term, eligibility or study-selection signal.
- A generic `Methods` heading about experiments, computational methods, materials fabrication or high-throughput screening did not count as a review-search method.
- Database, date-limit, keyword/search-term, Boolean/full-string, supplementary-string, inclusion/exclusion, screening, deduplication, PRISMA and literature-flow fields were coded separately.
- Flow diagrams counted only in literature-selection/PRISMA context. The initial false positive for the high-throughput biomaterials workflow was manually rejected.
- Title and abstract HTML/entities were normalized before tokenization. Escaped subscript/superscript tags were removed from display titles and did not count as words.
- Title words, abstract words/sentences, first-person use and abstract rhetorical moves were deterministic indicators. They are descriptive and may miss synonymous or implicit moves.
- Body structure used JATS top-level section, figure, table-wrap and boxed-text counts. A nested `table-wrap`/`table` double count found during QA was corrected.
- Article subtype combines PubMed publication type with conservative title/abstract self-description. Indexing labels can be imperfect and should not be treated as an editor-assigned genre without checking the publisher page.

## Search-reporting denominator and uncertainty boundary

An independent second pass examined all 42 accessible bodies for review-search headings; first-person search statements; PubMed/MEDLINE, Embase, Scopus, Web of Science, Cochrane and related database names; and PRISMA/selection-flow context. It found 0/42 explicit review-search strategies. One body mentioned a PubMed search to quantify use of a public resource; that was not the review's literature-selection method and remained negative.

For each body-level search field:

- observed full-text result: 0/42;
- descriptive Wilson 95% interval within this purposive full-text subset: 0-8.38%;
- unassessed records: 158/200;
- body-level unassessed fraction: 158/200 (79%);
- whole-corpus feature-prevalence bounds under the two extreme assumptions for those unassessed records: 0-79%.

The Wilson interval is supplied only as a finite-subset uncertainty description. Because venue selection and OA availability were purposive, it is not a population confidence interval. The wide feature-prevalence bounds induced by the 79% unassessed body texts are more important: they prevent abstract-only access from being misreported as evidence that the body lacks a search method.

## Quality-control checks

- Exact row count: 200.
- Unique persistent IDs: 200.
- Unique DOI values: 200.
- Duplicate persistent IDs: 0.
- Crossref DOI resolution: 200/200.
- Crossref normalized-title mismatches requiring review: 0.
- Stored titles containing residual HTML/entity markup after normalization: 0.
- Full-text body audit: 42/42 accessible JATS records.
- PRISMA/literature-flow positives after manual context review: 0/42.
- Copyrighted abstracts or full-text bodies retained: 0.

## Biases and missingness

- Venue bias: a deliberately selected set of high-profile and specialist review venues; it omits many excellent journals.
- Indexing bias: Europe PMC/PubMed publication-type indexing is uneven across fields and article types.
- Topic bias: relevance weighting favors AI, biomaterials, nanomedicine, bioengineering and adjacent methods.
- Citation bias: citation count was a secondary selection signal and favors older records.
- OA/embargo bias: full-text weighting and Europe PMC availability favor deposited, funded or embargo-expired records.
- Partial-year bias: 2026 stops on 30 August and is not a full publication year.
- Text-level missingness: 158 body texts were unavailable for body-level search-method coding.
- Heuristic-coding bias: structural and rhetorical indicators can miss implicit or synonymous expressions.
- Version/status limit: Crossref and Europe PMC status were checked at the access date; later corrections, retractions or version changes require a fresh query.

These limits prohibit claims of completeness, field-wide prevalence, journal-level rates or a verified relationship between any writing feature and editorial acceptance.
