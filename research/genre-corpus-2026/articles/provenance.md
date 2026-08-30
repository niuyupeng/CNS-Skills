# Provenance: 200 top-journal research Articles

## Purpose and corpus lock

This directory supports a writing-mechanism study, not a bibliometric estimate of all accepted papers. The frozen corpus contains exactly 200 unique English original research Articles first published between 2021-01-01 and 2026-08-30. The final allocation was frozen before record selection as eight journals × 25 records, with 2021–2024 contributing four records per journal-year, 2025 contributing five, and 2026 (through 30 August) contributing four. An initial feasibility allocation placed five records in 2026; it was changed before the sample was frozen because five of the nine Biomaterials 2026 PMCID-indexed candidates returned HTTP 404 at the JATS endpoint on the access date. Those records were not counted as full text.

Venue strata:

- broad flagships: Cell, Nature, Science (75 total);
- field-selective journals: Nature Materials, Nature Biomedical Engineering, Advanced Materials, Biomaterials, Science Translational Medicine (125 total).

The labels are sampling strata, not claims that all journals use the same house style or editorial standard.

## Sources, identifiers, and access date

Access date for every API and landing-page identifier: **2026-08-30**.

- Europe PMC REST search: candidate discovery, ISSN/date/publication-type filters, DOI/PMID/PMCID, first-publication date, OA flag, and PMC availability. Base URL: <https://www.ebi.ac.uk/europepmc/webservices/rest/search>.
- PMC JATS XML through Europe PMC: actual full-text structure and transient text analysis. Endpoint pattern: `https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML`.
- NCBI PubMed E-utilities `efetch`: independent check of title, DOI, English language, abstract presence, and publication types. Endpoint: <https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi>.
- Crossref REST `/works/{doi}`: exact DOI, title-similarity, and `journal-article` type check. Endpoint: <https://api.crossref.org/works/>.
- DOI landing links in the manifest use the persistent resolver <https://doi.org/>; PMC links use <https://pmc.ncbi.nlm.nih.gov/articles/>.

OpenAlex was tested but its unauthenticated daily budget was exhausted at access time. No OpenAlex identifier or OpenAlex-derived field is claimed in the final manifest. The final corpus is independently auditable through DOI, PMID, PMCID, PubMed/PMC, Europe PMC, and Crossref.

## Inclusion rules

All conditions were required:

1. exact journal ISSN and first-publication date within the locked window;
2. Europe PMC `PUB_TYPE:"Research Article"` and JATS root `article-type="research-article"`;
3. English PubMed record with a non-empty abstract;
4. DOI, PMID, and PMCID all present and unique;
5. PMC JATS XML successfully retrieved and parsed, with at least 1,000 words in the body;
6. no PubMed type or title signal for Review, Systematic Review, Meta-analysis, Editorial, Letter, Comment, Protocol, Correction, Expression of Concern, or Retraction;
7. DOI and title checked against Crossref, and title/DOI checked against PubMed.

The candidate list in every journal-year cell was sorted by PMID/DOI and independently shuffled with fixed seed **20260830**. A record occupied a quota only after JATS retrieval and the checks above succeeded; failed candidates were replaced by the next item in that cell's frozen shuffled order.

## Actual text layer

- title/metadata analyzed: 200;
- PubMed abstract analyzed: 200;
- PMC JATS full text successfully parsed and analyzed: 200;
- records described as full-text reads without a parsed full text: **0**.

The JATS XML was held only in memory long enough to derive counts and hashes. No abstract or article body is stored in this directory, and no copyrighted full text or long excerpt is reproduced. `pmc_xml_sha256` fingerprints the analyzed XML version without redistributing it.

`isOpenAccess=Y` in Europe PMC is recorded as `oa`. A PMC-retrievable item not flagged OA is recorded as `not_flagged_oa`; this does not assert that the publisher version is open, nor does it identify the PMC file as a publisher Version of Record.

## Candidate-frame audit

- Cell, 2021: API hitCount=263, eligible after metadata filter=262; query=`ISSN:0092-8674 AND FIRST_PDATE:[2021-01-01 TO 2021-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Cell, 2022: API hitCount=208, eligible after metadata filter=208; query=`ISSN:0092-8674 AND FIRST_PDATE:[2022-01-01 TO 2022-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Cell, 2023: API hitCount=208, eligible after metadata filter=208; query=`ISSN:0092-8674 AND FIRST_PDATE:[2023-01-01 TO 2023-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Cell, 2024: API hitCount=247, eligible after metadata filter=245; query=`ISSN:0092-8674 AND FIRST_PDATE:[2024-01-01 TO 2024-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Cell, 2025: API hitCount=176, eligible after metadata filter=176; query=`ISSN:0092-8674 AND FIRST_PDATE:[2025-01-01 TO 2025-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Cell, 2026: API hitCount=49, eligible after metadata filter=49; query=`ISSN:0092-8674 AND FIRST_PDATE:[2026-01-01 TO 2026-08-30] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature, 2021: API hitCount=479, eligible after metadata filter=478; query=`ISSN:0028-0836 AND FIRST_PDATE:[2021-01-01 TO 2021-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature, 2022: API hitCount=642, eligible after metadata filter=641; query=`ISSN:0028-0836 AND FIRST_PDATE:[2022-01-01 TO 2022-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature, 2023: API hitCount=746, eligible after metadata filter=743; query=`ISSN:0028-0836 AND FIRST_PDATE:[2023-01-01 TO 2023-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature, 2024: API hitCount=865, eligible after metadata filter=864; query=`ISSN:0028-0836 AND FIRST_PDATE:[2024-01-01 TO 2024-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature, 2025: API hitCount=929, eligible after metadata filter=926; query=`ISSN:0028-0836 AND FIRST_PDATE:[2025-01-01 TO 2025-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature, 2026: API hitCount=359, eligible after metadata filter=358; query=`ISSN:0028-0836 AND FIRST_PDATE:[2026-01-01 TO 2026-08-30] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science, 2021: API hitCount=290, eligible after metadata filter=290; query=`ISSN:0036-8075 AND FIRST_PDATE:[2021-01-01 TO 2021-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science, 2022: API hitCount=249, eligible after metadata filter=249; query=`ISSN:0036-8075 AND FIRST_PDATE:[2022-01-01 TO 2022-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science, 2023: API hitCount=208, eligible after metadata filter=207; query=`ISSN:0036-8075 AND FIRST_PDATE:[2023-01-01 TO 2023-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science, 2024: API hitCount=233, eligible after metadata filter=232; query=`ISSN:0036-8075 AND FIRST_PDATE:[2024-01-01 TO 2024-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science, 2025: API hitCount=199, eligible after metadata filter=199; query=`ISSN:0036-8075 AND FIRST_PDATE:[2025-01-01 TO 2025-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science, 2026: API hitCount=58, eligible after metadata filter=58; query=`ISSN:0036-8075 AND FIRST_PDATE:[2026-01-01 TO 2026-08-30] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Materials, 2021: API hitCount=17, eligible after metadata filter=17; query=`ISSN:1476-1122 AND FIRST_PDATE:[2021-01-01 TO 2021-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Materials, 2022: API hitCount=29, eligible after metadata filter=29; query=`ISSN:1476-1122 AND FIRST_PDATE:[2022-01-01 TO 2022-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Materials, 2023: API hitCount=38, eligible after metadata filter=38; query=`ISSN:1476-1122 AND FIRST_PDATE:[2023-01-01 TO 2023-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Materials, 2024: API hitCount=50, eligible after metadata filter=50; query=`ISSN:1476-1122 AND FIRST_PDATE:[2024-01-01 TO 2024-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Materials, 2025: API hitCount=59, eligible after metadata filter=59; query=`ISSN:1476-1122 AND FIRST_PDATE:[2025-01-01 TO 2025-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Materials, 2026: API hitCount=18, eligible after metadata filter=18; query=`ISSN:1476-1122 AND FIRST_PDATE:[2026-01-01 TO 2026-08-30] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Biomedical Engineering, 2021: API hitCount=54, eligible after metadata filter=54; query=`ISSN:2157-846X AND FIRST_PDATE:[2021-01-01 TO 2021-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Biomedical Engineering, 2022: API hitCount=64, eligible after metadata filter=64; query=`ISSN:2157-846X AND FIRST_PDATE:[2022-01-01 TO 2022-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Biomedical Engineering, 2023: API hitCount=67, eligible after metadata filter=66; query=`ISSN:2157-846X AND FIRST_PDATE:[2023-01-01 TO 2023-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Biomedical Engineering, 2024: API hitCount=48, eligible after metadata filter=46; query=`ISSN:2157-846X AND FIRST_PDATE:[2024-01-01 TO 2024-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Biomedical Engineering, 2025: API hitCount=84, eligible after metadata filter=84; query=`ISSN:2157-846X AND FIRST_PDATE:[2025-01-01 TO 2025-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Nature Biomedical Engineering, 2026: API hitCount=15, eligible after metadata filter=15; query=`ISSN:2157-846X AND FIRST_PDATE:[2026-01-01 TO 2026-08-30] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Advanced Materials, 2021: API hitCount=234, eligible after metadata filter=234; query=`ISSN:0935-9648 AND FIRST_PDATE:[2021-01-01 TO 2021-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Advanced Materials, 2022: API hitCount=56, eligible after metadata filter=56; query=`ISSN:0935-9648 AND FIRST_PDATE:[2022-01-01 TO 2022-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Advanced Materials, 2023: API hitCount=63, eligible after metadata filter=63; query=`ISSN:0935-9648 AND FIRST_PDATE:[2023-01-01 TO 2023-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Advanced Materials, 2024: API hitCount=215, eligible after metadata filter=215; query=`ISSN:0935-9648 AND FIRST_PDATE:[2024-01-01 TO 2024-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Advanced Materials, 2025: API hitCount=723, eligible after metadata filter=722; query=`ISSN:0935-9648 AND FIRST_PDATE:[2025-01-01 TO 2025-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Advanced Materials, 2026: API hitCount=213, eligible after metadata filter=213; query=`ISSN:0935-9648 AND FIRST_PDATE:[2026-01-01 TO 2026-08-30] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Biomaterials, 2021: API hitCount=98, eligible after metadata filter=98; query=`ISSN:0142-9612 AND FIRST_PDATE:[2021-01-01 TO 2021-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Biomaterials, 2022: API hitCount=64, eligible after metadata filter=64; query=`ISSN:0142-9612 AND FIRST_PDATE:[2022-01-01 TO 2022-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Biomaterials, 2023: API hitCount=66, eligible after metadata filter=66; query=`ISSN:0142-9612 AND FIRST_PDATE:[2023-01-01 TO 2023-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Biomaterials, 2024: API hitCount=40, eligible after metadata filter=40; query=`ISSN:0142-9612 AND FIRST_PDATE:[2024-01-01 TO 2024-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Biomaterials, 2025: API hitCount=29, eligible after metadata filter=29; query=`ISSN:0142-9612 AND FIRST_PDATE:[2025-01-01 TO 2025-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Biomaterials, 2026: API hitCount=9, eligible after metadata filter=9; query=`ISSN:0142-9612 AND FIRST_PDATE:[2026-01-01 TO 2026-08-30] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science Translational Medicine, 2021: API hitCount=194, eligible after metadata filter=193; query=`ISSN:1946-6234 AND FIRST_PDATE:[2021-01-01 TO 2021-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science Translational Medicine, 2022: API hitCount=166, eligible after metadata filter=166; query=`ISSN:1946-6234 AND FIRST_PDATE:[2022-01-01 TO 2022-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science Translational Medicine, 2023: API hitCount=136, eligible after metadata filter=136; query=`ISSN:1946-6234 AND FIRST_PDATE:[2023-01-01 TO 2023-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science Translational Medicine, 2024: API hitCount=124, eligible after metadata filter=124; query=`ISSN:1946-6234 AND FIRST_PDATE:[2024-01-01 TO 2024-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science Translational Medicine, 2025: API hitCount=108, eligible after metadata filter=108; query=`ISSN:1946-6234 AND FIRST_PDATE:[2025-01-01 TO 2025-12-31] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`
- Science Translational Medicine, 2026: API hitCount=22, eligible after metadata filter=22; query=`ISSN:1946-6234 AND FIRST_PDATE:[2026-01-01 TO 2026-08-30] AND HAS_ABSTRACT:Y AND PUB_TYPE:"Research Article" AND NOT PUB_TYPE:"Review"`

## Verification results

- corpus rows: 200; unique DOI: 200; unique PMID: 200; unique PMCID: 200;
- PubMed metadata/title/DOI/type/language verification passed: 200;
- Crossref exact DOI and title-match verification passed: 200;
- parsed PMC JATS research articles: 200.

## Derived features

The analysis uses transparent regular expressions and section-title heuristics for title length/punctuation, abstract information moves, introduction-final-paragraph actions, figure/numeric/statistical references in Results, reproducibility markers in Methods, claim/limitation/implication markers in Discussion-like closings, and first-person/passive-voice proxies. Results/body prose counts exclude JATS figure and table captions, table content, supplementary-material containers, reference lists, and footnote groups. Methods-marker percentages search identified Methods prose only; they do not count a standalone Data or Code Availability section. The rules and metric scopes are summarized in `articles_metrics.json`; they are not trained discourse classifiers and are not suitable as acceptance predictors.

When a journal did not expose an explicit Introduction, Results, Methods, or Discussion heading in JATS, the manifest records the actual inference mode (for example, `inferred_opening_paragraphs` or `conclusion_section_used`). The analysis never relabels an inferred section as an explicit section.

## Missingness and bias

1. **PMC selection bias.** Requiring parseable JATS favors OA articles, NIH-funded manuscripts, and publishers/workflows represented in PMC. It is not a random sample of every article published by these journals.
2. **Version bias.** A PMC author manuscript can differ in wording, section labels, layout, captions, and copy-editing from the publisher Version of Record. The manifest therefore distinguishes OA flag from full-text availability.
3. **Disciplinary composition.** Cell, Nature, and Science are multidisciplinary or biology-heavy, whereas the five field journals have different scientific objects and reporting conventions. Between-stratum differences are descriptive, not pure venue effects.
4. **JATS structure.** Some journals use a `Main` section or omit explicit IMRaD headings. Inferred opening/closing segments are reported as inferred and should not be treated as manual rhetorical annotation.
5. **Heuristic text analysis.** Sentence splitting, passive-voice proxies, figure references, statistical markers, and rhetorical moves have false positives and false negatives. Frequencies are diagnostics, not norms.
6. **Incomplete 2026.** The 2026 stratum ends on 30 August and cannot represent the complete publication year.
7. **Index drift.** Europe PMC, PubMed, PMC, and Crossref records can be corrected or updated. The manifest freezes identifiers and an XML SHA-256, but rerunning the candidate query later can change the candidate frame.
8. **No causal inference about acceptance.** The study observes published articles only. It has no rejected-paper control group and cannot show that a phrase, length, voice, or structure caused acceptance.
9. **Genre boundary.** This corpus contains original research Articles, not Reviews. It cannot by itself decide whether a top narrative review should list full search strings or adopt a systematic-review Methods section.

## Reproducible integrity checks

The following invariants were enforced before files were written:

- exactly 200 rows;
- 25 rows per journal;
- annual first-publication totals 32, 32, 32, 32, 40, and 32 for 2021–2026;
- 200 unique DOI, PMID, and PMCID values;
- every record has a PubMed abstract and a parsed PMC JATS research-article body;
- every Crossref DOI is exact and every Crossref title similarity is at least 0.85.

Only aggregate statistics and metadata are redistributed. Users should follow DOI/PMC links to inspect the source under the applicable access terms.
