# Genre-aware transfer from top-venue writing

Use this reference when a request compares Reviews, original research Articles,
and leading-conference papers or asks CNS Skills to learn from top-venue writing.
The goal is **functional transfer**, not surface imitation. Article type and the
current official venue instructions remain authoritative.

## Evidence ledger

The 2026 genre study is stored under `research/genre-corpus-2026/`. Its three
200-record strata are deliberately separate:

- **Reviews:** 200 DOI-identified records from 20 high-selectivity review venues.
  The actual text levels are 42 full-text XML, 157 abstract, and 1 title-only.
  The full-text subset is strongly shaped by PMC availability and cannot estimate
  how often all top Reviews report a search method.
- **Original Articles:** 200 DOI/PMID/PMCID-identified research Articles from
  Cell, Nature, Science, and five selective field journals; all 200 supplied
  parseable PMC JATS full text. This is structured heuristic analysis, not 200
  expert line-by-line annotations.
- **Leading conferences:** 200 accepted main-track papers sampled from the
  official 2025 proceedings of AAAI, CVPR, NeurIPS, ICML, and ICLR. Use the
  manifest's per-record `analysis_text_level` and the metrics' exact
  denominators: 200 titles, 200 abstracts, and 195 official-PDF-derived full
  texts. Never turn an abstract-only record or failed PDF retrieval into a
  claimed full read.

The corpus records metadata and derived features, not source prose. Its
frequencies are descriptive observations under selection and parsing bias. They
are not acceptance predictors, house-style rules, or permission to reproduce
publisher text.

## Transfer by article type

| Function | Review | Original research Article | Leading-conference paper |
|---|---|---|---|
| Central promise | a distinctive synthesis, decision framework, controversy resolution, or field map | a supported discovery or capability | a precise technical contribution and why it matters |
| Opening | why this synthesis is needed now; what existing reviews leave unresolved | scientific problem, unresolved question, study action | problem, gap, contribution, and evaluation setting quickly |
| Body logic | questions, comparisons, mechanisms, evidence levels, or decisions | inference and figure sequence | method plus experiments that test contribution claims |
| Evidence | cross-study comparison with provenance and incompatibilities visible | newly generated data and controls | benchmarks, baselines, ablations, robustness, and error analysis |
| Author action verbs | `we synthesize`, `compare`, `distinguish`, `propose` | `we tested`, `show`, `found`, `measured` when supported | `we propose`, `derive`, `evaluate`, `ablate` when supported |
| Boundary | selection scope, evidence heterogeneity, unresolved mechanisms, transfer limits | limitations and alternative explanations near the affected claim | assumptions, dataset/benchmark limits, compute and generalization limits |

Do not transplant IMRaD headings, contribution bullets, `state-of-the-art`
language, or a benchmark-first argument into a narrative Review. Do transfer the
underlying discipline: every major claim should have a visible comparison,
evidence basis, and boundary.

## Search disclosure in a Review

First classify the product: narrative, structured narrative, scoping,
systematic, or meta-analytic. Then ask what the selected corpus is being used to
support.

For a narrative or structured narrative Review, a concise main-text disclosure
can be rigorous when it states:

1. the purpose of retrieval;
2. the primary bibliographic source or sources;
3. the search cutoff;
4. the scientific concept blocks or selection questions;
5. the reason studies were prioritized; and
6. the limit on coverage, prevalence, or exhaustiveness claims.

Separate source roles. A bibliographic database identifies records; publisher
pages or repositories retrieve full text; DOI/Crossref pages verify metadata and
status; an author-held collection supplements access or citation chasing. Do not
present these as interchangeable databases.

Avoid a long slash- or comma-separated keyword inventory unless it is merely a
short set of concept blocks. Such prose looks like a query but cannot be rerun.
If a defined corpus drives counts, evidence-grade distributions, or comparative
tables, keep the main text short and provide a **real** supplementary record with
database-specific executable strings, run dates, deduplication and version
rules, eligibility logic, and an included-record manifest.

Do not infer from the 42 accessible narrative-or-Perspective full texts that search
reporting is absent from all top Reviews. In that assessed subset, no explicit
review-search strategy was detected, but the denominator is small, selective,
and contains no full-text systematic/scoping/meta-analytic item. Official
article-type guidance and the manuscript's actual protocol outrank that
observation.

## Architecture of a strong narrative Review

Lock four statements before editing:

1. the field-level decision or unresolved question;
2. why a new synthesis is needed now;
3. the organizing lens that differs from prior reviews; and
4. what evidence the Review will not claim to cover.

Build each major section around an intellectual move, not a repeated template.
A section may explain a mechanism, compare model choices, expose a disagreement,
map evidence maturity, or derive a decision. Cases serve as evidence for that
move; they are not a serial catalogue of papers.

Use figures and tables to perform cross-study synthesis. A useful display makes
at least one relationship easier to judge: method × action, evidence level ×
claim, context × model choice, or capability × validation boundary. Move large
record inventories and audit fields to a supplement when they obscure the main
comparison.

For a Review, read `review-visual-architecture.md`; for an original research
paper, read `original-research-article-mode.md`; for a leading-conference paper,
read `leading-conference-paper-mode.md`. The same visual object has different
jobs across genres: a Review figure synthesizes relationships across studies,
an Article figure carries a new inference, and a conference display tests a
technical contribution within a page budget. Never copy a figure-count median
or page-budget convention across those modes.

End by resolving the governing question, identifying the highest-leverage
uncertainties, and specifying what evidence would change the field's decisions.
Do not end every section with an interchangeable advantages–limitations–future
work paragraph.

## What to learn from original Articles

Transfer these functions without copying their genre shell:

- one scope-controlled central claim should align the title, abstract,
  introduction close, evidence sequence, and discussion opening;
- results should be ordered by inference, not experimental chronology;
- numbers should specify scale, comparison, or uncertainty rather than decorate
  an abstract;
- Methods should be judged by auditability, not a prescribed first-person or
  passive-voice rate; and
- limitations should identify the claim, condition, or inference they restrict.

The Article corpus's medians and phrase frequencies are diagnostics only. A
Review does not become stronger by adopting an 11-word title, seven-sentence
abstract, or Article-like density of numbers.

## What to learn from leading conferences

Transfer the insistence on an explicit problem, contribution–evidence mapping,
credible baselines, ablations or alternative explanations, error analysis,
assumptions, and reproducibility details. For AI-heavy Reviews, these checks help
separate algorithmic novelty from a genuinely decision-changing biomaterials
result.

Do not copy conference compression blindly. A Review should not open with a
generic three-bullet contribution list, equate benchmark gain with scientific
importance, or let method acronyms replace biological and material context.

## Editorial stop rules

- Never say that 600 papers were fully read unless the per-record analysis levels
  support that claim; say `600 records studied` and report the text levels.
- Never convert corpus frequency into a venue requirement or acceptance cause.
- Never fill a missing Methods/search record from an abstract or title.
- Never copy source sentences, phrasebanks, figures, or tables into a manuscript.
- Never upgrade a narrative Review to systematic/scoping language without the
  real protocol and screening record.
- Recheck current official author instructions before submission.
