# A 100-title field-journal comparison corpus

## Purpose and boundary

This companion corpus preserves a topic-matched set of strong materials,
chemistry, bioengineering, and biomaterials journals, including *ACS Nano*,
*Advanced Functional Materials*, *Acta Biomaterialia*, *Biomaterials*,
*Materials Today*, and the *Trends* family. It is useful for domain vocabulary
and field-specific title conventions, but it is **not** the elite benchmark used
to define top-venue title practice.

It contains **100 titles and bibliographic metadata, not 100 full papers**. The
records are in
[`field-journal-title-corpus-100.csv`](field-journal-title-corpus-100.csv), and
the generated aggregate is in
[`field-journal-title-corpus-100-summary.json`](field-journal-title-corpus-100-summary.json).

The separate [`elite-venue-title-study.md`](elite-venue-title-study.md) defines
the 70-journal + 30-conference core benchmark. Results from the two layers are
reported separately rather than pooled into one prescriptive average.

This panel predates the reconstructed elite core. **Fifty DOI records overlap
the core**, so the two 100-record panels contain 150 distinct titles, not 200.
The overlap is retained transparently rather than replaced post hoc; do not sum
the panel sizes when reporting the number of distinct titles.

## Retrieval and selection protocol

Metadata were retrieved on **30 August 2026** through the Crossref REST API.
The search window was 2010–30 August 2026. Queries combined AI/model or
automation language with biomaterials, drug delivery, polymers, peptides,
hydrogels, tissue engineering, bioprinting, materials discovery, inverse
design, active learning, Bayesian optimization, autonomous laboratories, or
high-throughput experimentation.

Candidate records required a DOI, title, journal, year, topical match, and no
correction/reprint or normalized-title/DOI duplicate. Venue and topic caps
prevented one high-volume journal from dominating. The resulting corpus spans
2018–2026 and 25 journals. It is purposive rather than random or exhaustive.

## Verification and genre status

Every row was fetched again from the Crossref DOI endpoint. DOI, normalized
title, normalized journal, and publication year matched for all **100/100**
records. PubMed publication-type metadata were available for 76 records and
were used only as an additional genre check.

- 24 records are verified Reviews;
- 3 are verified comments, editorials, or letters;
- 73 are journal articles whose more specific publisher genre was not reliably
  exposed and therefore remains unknown.

No abstract or full-text field is stored. See the
[Crossref REST API documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/).

## Descriptive results

| Observable feature | Field-journal layer |
|---|---:|
| Titles | 100 |
| Unique normalized titles / stable IDs | 100 / 100 |
| Publication years | 2018–2026 |
| Median title words | 10 |
| Interquartile range, words | 8–12 |
| Median title characters | 80 |
| Interquartile range, characters | 62.75–99.25 |
| Titles with a colon | 13% |
| Titles phrased as a question | 1% |
| Titles with a detected acronym | 7% |

These values describe this selected comparison set; they are not title targets,
journal rankings, or acceptance predictors.

## How this layer is used

1. Check whether a proposed title uses domain-native biomaterials terminology.
2. Compare topic wording in field journals against the stricter elite core.
3. Retain useful adjacent examples without allowing their frequency to set a
   single “top-journal formula.”
4. Weight verified Reviews more heavily for a review-article title; use research
   articles only as a secondary comparator.

Reproduce the aggregate checks with:

```bash
python scripts/title_audit.py \
  --corpus research/field-journal-title-corpus-100.csv \
  --strict \
  --json research/field-journal-title-corpus-100-summary.json
```

## Non-inferences

This corpus does not establish that any title caused acceptance or citation,
that a median length is optimal, that all included journals share one tier or
house style, or that title metadata can replace reading a manuscript.
