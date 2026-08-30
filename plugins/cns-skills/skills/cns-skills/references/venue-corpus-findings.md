# Descriptive venue-corpus findings

This note records a reproducible language baseline for CNS Skills v0.3.0. It is descriptive, not a recipe for acceptance or a source of text to imitate.

## Corpus and method

The included analyzer sampled **320 English abstracts**: 40 each from Cell, Nature, Science, AAAI, CVPR, NeurIPS, ICML, and ICLR. It used source-and-date-filtered OpenAlex random samples with seed `20260830`. Abstracts were reconstructed in memory from inverted indexes; the repository stores only aggregate statistics and a metadata manifest, never abstract text.

Records under 80 English tokens were treated as metadata stubs and excluded. Journal and AAAI samples cover 2024–30 August 2026. The specific OpenAlex source records available for CVPR, NeurIPS, ICML, and ICLR cover 2022 or 2021 snapshots; current submission rules must therefore come from official venue guidance, not this corpus.

Reproduce the analysis with:

```bash
python scripts/venue_corpus_analyzer.py --per-venue 40 --seed 20260830
```

Machine-readable results are in `research/venue-corpus-aggregate.json`; the title/identifier manifest is in `research/venue-corpus-manifest.csv`. The manifest also stores the non-text features needed to audit the aggregate, sentence-length vectors, and an abstract SHA-256 hash, but not the abstract itself.

## Selected aggregate results

| Venue | Sample years | Median title words | Median abstract words | Median sentences | Abstracts using we/our | Abstracts with a number |
|---|---:|---:|---:|---:|---:|---:|
| Cell | 2024–2026 | 11.0 | 151.5 | 7.0 | 97.5% | 60.0% |
| Nature | 2024–2026 | 8.0 | 217.5 | 8.5 | 100.0% | 95.0% |
| Science | 2024–2026 | 10.0 | 126.0 | 5.5 | 92.5% | 62.5% |
| AAAI | 2024–2026 | 10.0 | 174.5 | 8.0 | 97.5% | 37.5% |
| CVPR | 2022 | 9.0 | 186.5 | 8.0 | 97.5% | 45.0% |
| NeurIPS | 2021 | 8.0 | 182.5 | 7.0 | 100.0% | 50.0% |
| ICML | 2021 | 8.0 | 166.0 | 7.0 | 95.0% | 32.5% |
| ICLR | 2021 | 9.5 | 167.5 | 7.0 | 92.5% | 57.5% |

Across these samples, direct first-person authorship was normal rather than exceptional. Median titles were compact, and abstracts usually fit a small number of information-dense sentences. Numeric evidence appeared often but not universally; whether a number belongs in an abstract depends on the claim and venue, not a target percentage.

The heuristic move detector found explicit contribution language in 77.5–92.5% of Cell, Nature, AAAI, CVPR, NeurIPS, ICML, and ICLR abstracts, but only 40% of the shorter Science sample. Explicit limitation phrases appeared in only 0–5% of sampled abstracts. This does **not** license hiding limitations: the detector uses narrow phrase lists, analyzes abstracts rather than full papers, and cannot recognize every boundary statement.

## What CNS Skills may infer

- Strong venue writing is generally direct about author action and contribution.
- Compact titles and abstracts coexist with technical specificity; compression should remove setup, not evidence.
- Journal and conference abstracts differ in emphasis, but neither supports a universal sentence template.
- Numeric results are useful when they identify the scale, comparison, or uncertainty of the central claim.
- Surface frequency should never override exact venue instructions or the manuscript's evidence needs.

## What CNS Skills must not infer

- that these papers were accepted because of any measured phrase or length;
- that a median is a target, minimum, or maximum;
- that historical conference abstracts represent current policy;
- that abstract style describes methods, results, captions, or full-paper argument quality;
- that copying rhetorical sequences or vocabulary creates a top-venue contribution;
- that first-person language, numbers, strong verbs, or low hedging are always preferable.

## Measurement limits

OpenAlex source assignment and abstract availability can be incomplete. Random samples can vary with index updates even under a fixed seed. The sentence splitter and rhetorical-move detector are transparent heuristics, not trained discourse classifiers. Corpus years are uneven across venues, fields are not matched, and abstract genre conventions vary.

Use the aggregate as a sanity check and hypothesis generator. Current official author instructions, the evidence ledger, and expert judgment remain authoritative.
