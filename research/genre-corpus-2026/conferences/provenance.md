# Provenance and sampling record

## Scope lock

- **Object studied:** writing and reporting structure in accepted English main-conference papers.
- **Venues:** AAAI, CVPR, NeurIPS, ICML, and ICLR.
- **Conference year:** 2025 for all five venues.
- **Access date:** 2026-08-30 (Asia/Shanghai project date).
- **Allocation:** exactly 40 papers per venue; exactly 200 unique records overall.
- **Why 2025:** it was the most recent common completed year with final official proceedings pages for all five venues. Using a common year avoids mixing a finalized 2025 corpus with incomplete 2026 proceedings.

## Official sampling frames

| Venue | Eligible frame | Official source | Main-track rule |
|---|---:|---|---|
| AAAI | 2903 | [AAAI OJS archive](https://ojs.aaai.org/index.php/AAAI/issue/archive/2) and numbered issues 624–648 | Included only sections whose OJS heading begins `AAAI Technical Track on`; excluded special tracks, IAAI, EAAI, journal track, demos, and student abstracts. |
| CVPR | 2871 | [CVF Open Access, CVPR 2025 all papers](https://openaccess.thecvf.com/CVPR2025?day=all) | The base `CVPR2025` proceedings page was used; `CVPR2025W` workshop pages were not eligible. |
| NeurIPS | 5286 | [NeurIPS 2025 Main Conference proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/vol38-main-conference) | Included only URLs ending `-Abstract-Conference.html`; excluded Position Paper and Datasets and Benchmarks tracks. |
| ICML | 3330 | [PMLR volume 267](https://proceedings.mlr.press/v267/) | The archival proceedings volume for the 42nd ICML was used; no workshop volumes were included. |
| ICLR | 3703 | [ICLR 2025 official proceedings](https://proceedings.iclr.cc/paper_files/paper/2025) | Included `Conference` records from the archival proceedings; rejected, withdrawn, and workshop submissions were not in the frame. |

Frame sizes are page-derived counts at access time, not claims about submissions or acceptance rates.

## Sampling procedure

Within each eligible frame, records were sorted by the stable native identifier embedded in the official canonical URL (AAAI numeric article ID; CVPR proceedings slug; NeurIPS/ICLR proceedings hash; ICML PMLR article slug). Forty equal-interval positions were then selected at `floor((i + 0.5) × N / 40)` for `i = 0…39`. The manifest records the one-based `sampling_rank`, frame size, and within-venue sample order. This provides deterministic spread over each proceedings frame without hand-picking famous, highly cited, or easy-to-download papers.

## Metadata and text acquisition

For every selected record, the official article/abstract page was requested. Title, authors, DOI when exposed, publication-date metadata, abstract, canonical URL, and PDF URL were parsed from publisher/proceedings HTML. DOI availability was: `{"AAAI": 40, "NeurIPS": 40}`. A blank DOI means the official proceedings page did not expose one; it is not a fabricated identifier.

PDF processing had three explicit gates:

1. the URL had to come from the official article/abstract page;
2. the downloaded response had to begin with PDF magic bytes (`%PDF-`);
3. `pdftotext -enc UTF-8 -layout` had to yield at least 800 English-word tokens.

Only records passing all three gates are labelled `full_text_extracted`. The PDF SHA-256, bytes, page count, text word count, and extraction status are retained in the manifest. The final public corpus does not redistribute paper PDFs or extracted full text; only bibliographic metadata, URLs, hashes, and independently computed structural descriptors are retained.

For runtime safety, structural pattern detection used the complete extracted text up to 450,000 characters. Longer texts used the first 300,000 and final 150,000 characters, preserving the opening/main-paper narrative and end-matter regions while bounding appendix-driven regex cost. PDF hashes, page counts, and full-text word counts always refer to the complete artifact. An earlier analysis pass revealed cross-line whitespace backtracking on long appendices; the final pass restricts heading whitespace to a single line and records this bounded window explicitly.

## Analysis levels

- **Title-level:** title length and topic cues from a non-empty official title.
- **Abstract-level:** move cues from an abstract actually present on the official article page.
- **Full-text structural level:** headings, contribution markers, related-work placement, method/experiment sections, baseline/ablation/uncertainty language, limitations/ethics/checklist headings, caption identifiers, and conclusion moves from successfully extracted PDF text.

Full-text extraction is not represented as human line-by-line close reading. It supports structural measurement and targeted spot checks. Abstract-only records are not described as fully read.

## Reproducibility and quality checks

Construction used Python with `requests` and `lxml`, plus Poppler's `pdftotext`
and `pdfinfo`. The final four-file research deposit intentionally excludes the
one-off builder, downloaded PDFs, extracted text, and network cache; it can be
reconstructed from the recorded official frame URLs, stable-ID sort rule,
equal-interval formula, manifest ranks, and access date. Live proceedings or
server responses can change after that date, so a later reconstruction may not
be byte-identical.

An initial quality audit identified 17 records below the full-text gate. Only
those 17 official PDF URLs entered a bounded sequential recovery pass. A
candidate replacement had to pass PDF magic-byte and end-of-file checks,
plausible file length, `pdfinfo` parsing with at least two pages, and
`pdftotext` extraction with at least 800 English-word tokens before atomic
replacement. Finite connection/read retries were used; an incomplete slow
transfer that exceeded the per-item wall allowance was stopped and its `.tmp`
file was not accepted. A single cache-only final analysis then produced the
coherent snapshot below. Five records still failed the stated gate and remain
explicitly `abstract_only`; none is counted as full text.

- Total records: 200
- Per venue: {"AAAI": 40, "CVPR": 40, "ICLR": 40, "ICML": 40, "NeurIPS": 40}
- Per year: {"2025": 200}
- Unique paper IDs: 200
- Unique canonical URLs: 200
- Title-level available: 200
- Abstract-level available: 200
- Full-text extracted: 195
- Records below full-text level: 5

The CSV is encoded as UTF-8 with BOM for reliable opening in spreadsheet software. The JSON records feature definitions and denominators. Boolean feature counts use successfully extracted full texts as their denominator.

## Bias and validity limits

1. **Venue weighting:** equal 40-paper allocation overrepresents smaller proceedings relative to a population-weighted design but enables venue comparison.
2. **Single-year cross-section:** findings may reflect 2025 policies and fashions; they do not establish temporal trends.
3. **Systematic-ID sampling:** stable identifiers are reproducible but may retain latent ordering by proceedings production, authors, or track.
4. **Accepted-paper conditioning:** the corpus cannot determine which writing features caused acceptance and contains no rejected-paper control.
5. **PDF extraction:** multi-column order, equations, headers, supplements, and appendix headings can create false negatives or positives. Caption counts are approximate.
6. **Presence is not adequacy:** detecting “ablation,” “standard deviation,” or “limitations” does not show that the analysis was well designed.
7. **Topic classification:** the primary topic is keyword-assisted and coarse; it is not an official conference subject code.
8. **Policy dependence:** checklists, impact statements, page density, and section placement can be induced by venue forms and page limits. They must not be universalized into scholarly-review rules.

## Licensing and redistribution

Proceedings pages and PDFs remain owned or licensed by their respective authors and publishers. The corpus stores short bibliographic facts, links, cryptographic hashes, and independently derived structural measurements; it does not reproduce abstracts in the CSV or redistribute full text, figures, tables, or templates. Users must follow each source’s terms for any subsequent PDF use. The findings paraphrase patterns and do not copy passages from individual papers.

## Policy sources used only to separate genre constraints

Conference format/checklist statements should be verified against the live official year and track before submission. Useful official entry points include [AAAI main-track calls](https://aaai.org/conference/aaai/), [CVPR author guidelines](https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines), [NeurIPS main-track handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook), [ICML author instructions](https://icml.cc/Conferences/2026/AuthorInstructions), and [ICLR author guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines). Journal comparison used only official genre-level guidance—[Nature for authors](https://www.nature.com/nature/for-authors), [Cell information for authors](https://www.cell.com/cell/information-for-authors), and [Science information for authors](https://www.science.org/content/page/science-information-authors)—and did not infer journal-article frequencies from this conference-only corpus.
