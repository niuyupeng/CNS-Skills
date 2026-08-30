# Venue corpus artifacts

This directory contains the reproducible aggregate output used by CNS Skills v0.3.0.

- `review-prose-study.md`: a 24-article study of how scientific reviews synthesize studies with object-level prose while keeping editorial scaffolding such as claim ledgers and evidence chains out of the manuscript.
- `venue-corpus-aggregate.json`: method, limitations, request URLs, and per-venue aggregate metrics.
- `venue-corpus-manifest.csv`: titles, identifiers, years, non-text per-record features, sentence-length vectors, and abstract SHA-256 hashes for auditing the aggregate.

No abstract or full-paper text is stored. Formula-leading metadata are prefixed with an apostrophe in the CSV export to prevent spreadsheet execution. Rebuild the artifacts with:

```bash
python scripts/venue_corpus_analyzer.py --output-dir research --per-venue 40 --seed 20260830
```

Set `SOURCE_DATE_EPOCH` to make the report timestamp deterministic in a release build. The hash records the exact abstract representation used without redistributing its text; live OpenAlex index changes can still alter a future sample and are disclosed in the aggregate limitations.

OpenAlex metadata are provided under OpenAlex's published terms. Paper titles and identifiers are retained only to make the sample auditable; users remain responsible for publisher and venue terms when reading source content.
