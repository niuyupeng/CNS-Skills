# Genre-separated top-venue writing corpus (2026)

This public research asset contains exactly 600 records in three separate 200-record
strata. It was built to compare writing functions across top Reviews, original
research Articles, and leading AI conference papers without treating the genres
as interchangeable.

## What was actually analysed

| Stratum | Records | Verified text levels | Main use |
|---|---:|---|---|
| [Reviews](reviews/reviews_findings.md) | 200 | 42 full-text XML, 157 abstract, 1 title-only | Review architecture, abstract moves, and search-disclosure practice within the accessible full-text subset |
| [Original Articles](articles/articles_findings.md) | 200 | 200 title + PubMed abstract + parseable PMC JATS full text | Claim alignment, inference-led Results, auditable Methods, and bounded Discussion |
| [Leading conferences](conferences/conference_findings.md) | 200 | 200 titles, 200 abstracts, 195 official-PDF-derived full texts, and 5 abstract-only records | Problem/contribution framing, benchmark and ablation logic, reproducibility, and limitations |

`600 records studied` does **not** mean 600 expert line-by-line close readings.
Every manifest exposes the actual analysis level. Failed or unavailable full-text
retrieval remains title- or abstract-level and is never upgraded by inference.

## Files

Each stratum contains four primary deliverables:

- a 200-row CSV manifest with persistent identifiers, provenance, and actual
  analysis level;
- a JSON metrics file with denominators and deterministic feature definitions;
- a Markdown findings report that separates transferable functions from
  non-transferable surface conventions; and
- a provenance report with sampling, verification, legal-access, missingness,
  and non-inference boundaries.

The public, Git-tracked corpus stores metadata and derived indicators, not
article abstracts, publisher prose, figures, or full text. The conference
directory intentionally retains only the same four public deliverables; its
one-off builders and local download/extraction cache were removed after the
final quality-controlled snapshot.

## Design boundary

- The Review stratum is a relevance-weighted, venue-quota sample across 20
  review sources. Full-text findings are heavily shaped by PMC availability.
- The Article stratum is stratified across Cell, Nature, Science, Nature
  Materials, Nature Biomedical Engineering, Advanced Materials, Biomaterials,
  and Science Translational Medicine; requiring parseable PMC JATS creates an
  OA/deposit/version selection effect.
- The conference stratum uses deterministic equal-interval sampling from the
  official 2025 main-track proceedings of AAAI, CVPR, NeurIPS, ICML, and ICLR.

All frequencies describe these records only. They do not estimate journal- or
field-wide prevalence, explain editorial acceptance, provide an imitation
template, or override current official venue instructions. The durable transfer
rules are summarized in
[`references/genre-aware-top-venue-writing.md`](../../references/genre-aware-top-venue-writing.md).
