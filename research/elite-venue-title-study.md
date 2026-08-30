# Elite-venue scientific title study: 70 top-journal and 30 top-conference titles

## Purpose and evidence boundary

This is the core title benchmark for CNS Skills v0.8.0. It contains **100
verified titles and bibliographic metadata—not 100 full papers**—selected from
an explicit elite-venue panel. It is descriptive evidence about title practice,
not a style-transfer dataset, ranking exercise, acceptance model, or substitute
for reading the manuscript being titled.

The public records are in
[`elite-venue-title-corpus-100.csv`](elite-venue-title-corpus-100.csv); the
generated duplicate and feature checks are in
[`elite-venue-title-corpus-100-summary.json`](elite-venue-title-corpus-100-summary.json).

## Predeclared venue panel

The core has **70 journal titles** and **30 accepted main-conference titles**.

| Layer | Included venues | Records |
|---|---|---:|
| CNS flagships | *Cell*, *Nature*, *Science* | 11 |
| CNS-family elite specialties | *Nature Reviews Materials*, *Nature Reviews Bioengineering*, *Nature Materials*, *Nature Biomedical Engineering*, *Nature Machine Intelligence*, *Nature Biotechnology*, *Nature Nanotechnology*, *Nature Chemistry*, *Nature Methods*, *Science Advances*, *Science Robotics*, *Matter* | 46 |
| Field flagships | *Chemical Reviews*, *Journal of the American Chemical Society*, *Advanced Materials* | 13 |
| Flagship conferences | AAAI, CVPR, NeurIPS, ICML, ICLR | 30 |

General selective journals were not used to fill the elite core. Stronger
domain-adjacent journals remain available in the separate
[`field-journal-title-study.md`](field-journal-title-study.md) comparison layer.

## Selection and verification

Titles had to match AI-guided materials or biomaterials design, molecular or
protein design, scientific machine learning, inverse/generative design,
active/Bayesian optimization, autonomous experimentation, multimodal
scientific data, or biomedical image analysis.

- All 70 journal records have DOI values and were re-fetched from the Crossref
  DOI endpoint on **30 August 2026**. The DOI, title, venue, and year are stored
  in the frozen release snapshot.
- All 30 conference records are accepted **2025 main-conference papers** from
  official AAAI, CVF, NeurIPS, PMLR, or ICLR proceedings. Workshops, withdrawn
  papers, and submission-only records were excluded.
- Conference papers without DOI values use the official proceedings article
  ID, hash, or slug as the stable identifier. An absent DOI is not replaced by
  a guessed identifier.
- Normalized titles and stable identifiers are unique 100/100. The CSV stores
  no abstract or full text.

The genre field is deliberately conservative: 21 journal records are Reviews
verified through PubMed or the journal's review-only scope; 49 remain “journal
article, genre not verified”; the other 30 are conference papers. Unknown
records are not silently relabelled as research articles.

## Descriptive results, kept by genre family

| Observable feature | All 100 | Journals (70) | Conferences (30) |
|---|---:|---:|---:|
| Median title words | 9 | 9 | 10 |
| Interquartile range, words | 7–11.25 | 7–11 | 8–12.75 |
| Median title characters | 78.5 | 76 | 82.5 |
| Interquartile range, characters | 64.75–92.75 | 61.25–88.75 | 69.5–100.5 |
| Titles with a colon | 23% | 15.7% | 40% |
| Titles phrased as a question | 1% | 1.4% | 0% |
| Titles with a detected acronym | 11% | 7.1% | 20% |

The mixed 100-title median is not a target. Conference papers use branded
`acronym: subtitle` structures much more often than journals, so conference
punctuation and naming habits must not be imported mechanically into a Review.
The only question title in the corpus is a *Matter* perspective-style title;
its rarity does not ban questions, but it makes them a deliberate exception.

## Reusable editorial findings

1. **One scientific action is stronger than a contents list.** The title should
   expose the object and the paper's result, design decision, or organizing
   lens rather than enumerate data, models, experiments, and validation.
2. **Article type precedes frequency.** Review/Perspective titles should reveal
   the synthesis or decision problem. Research and conference titles are
   secondary comparators, not templates.
3. **Conference branding does not transfer automatically.** Method acronyms and
   colons are common enough in conference titles to be venue-specific evidence,
   not a universal prestige signal.
4. **Retrieval terms stay selective.** Keep the scientific object and one
   distinguishing action; do not reproduce the abstract or keyword list.
5. **Evidence limits attractive wording.** `Mechanism`, `clinical`, `robust`,
   `general`, or priority language requires corresponding manuscript evidence.

For the accompanying biomaterials Review, the corpus supports a concise
decision-led family such as **Choosing Models for AI-Guided Biomaterials
Design**. The recommendation still comes from the manuscript's seven-model
comparison and evidence boundary, not from copying corpus phrases or optimizing
to a frequency.

## Reproduce the checks

```bash
python scripts/title_audit.py \
  --corpus research/elite-venue-title-corpus-100.csv \
  --strict \
  --json research/elite-venue-title-corpus-100-summary.json
```

The Crossref metadata guide is available from
[Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/).
Conference records link directly to their official proceedings pages in the
CSV. Live metadata can change; the checked CSV and verification date define the
v0.8.0 snapshot.

## Non-inferences

The study does not establish that any title caused acceptance, citation, or
editorial interest; that 9 words or 78.5 characters is optimal; that punctuation
frequency is a venue rule; that every journal shares a house style; or that a
strong title can compensate for unsupported science.
