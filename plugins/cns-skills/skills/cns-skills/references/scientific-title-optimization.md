# Scientific title optimization

Use this reference when the user asks to name, rename, shorten, translate, or
optimize a scientific manuscript title. A title is the manuscript's first
claim and first retrieval surface. Treat it as a manuscript-level decision, not
as isolated copywriting.

## Decide whether the recommendation can be final

- If the full relevant manuscript is supplied, read it before choosing the
  final title.
- If only an abstract is supplied, return an abstract-bounded recommendation
  and identify any contribution or evidence boundary that remains uncertain.
- If only a topic or draft title is supplied, label all outputs **provisional**.
  Do not invent a discovery, dataset, validation layer, or article type.

Never claim to have read papers when only title and bibliographic metadata were
examined.

## Lock the title source

Record these fields before generating candidates:

| Field | Required question |
|---|---|
| Article type | Research Article, Review/Perspective, Methods/Resource/Dataset, conference paper, or another named type? |
| Scientific object | Which material, population, model, process, endpoint, or problem must a reader see? |
| Contribution or organizing lens | What did the paper establish, or what new synthesis/decision does the review provide? |
| Evidence boundary | Which attractive wording would exceed the supplied experiments, corpus, validation, or scope? |
| Audience and venue | Which journal/conference family and which adjacent-field reader must understand it? |
| Retrieval terms | Which 1–3 phrases are essential for realistic search and indexing? |
| Protected terminology | Which names, acronyms, scale labels, and field terms may not drift? |

The title must agree with the abstract, introduction, conclusion, figures, and
article type. If those components make different claims, repair or disclose the
misalignment instead of selecting the strongest-sounding version.

## Match the title to the article type

### Research Article

Prefer the scientific object plus the central supported result, relationship,
or capability. A conclusion-led title is valid only when the reported evidence
supports that conclusion. Do not promote association to mechanism, retrospective
performance to prospective utility, or animal evidence to clinical translation.

### Review or Perspective

Expose the object and the review's distinguishing synthesis: an organizing
principle, decision problem, controversy, bottleneck, taxonomy, or research
agenda. A list of technologies is not a synthesis. Avoid `A review of...`,
`recent advances`, or `challenges and future perspectives` when those phrases
merely identify the genre. Never use `systematic`, `comprehensive`, or a
field-wide prevalence claim unless the documented protocol and corpus support it.

### Methods, Resource, or Dataset paper

Name what is provided, the task or domain it supports, and the validated
capability that distinguishes it. Do not use `benchmark`, `general`, `robust`,
or `community resource` without the corresponding task, split, comparator,
coverage, and availability evidence.

### Leading-conference paper

Make the task, contribution type, and technical distinction retrievable. A
memorable method name or acronym is useful only when it is already defined,
stable, pronounceable, and not carrying the title by itself. Do not make
state-of-the-art performance the title's premise when the paper's real value is
theory, analysis, data, feasibility, or a negative result.

## Use a comparison corpus without copying it

For a data-grounded title study, compare 20–100 verified titles that are as close
as possible in:

1. article type;
2. venue family;
3. scientific domain and audience;
4. publication period when conventions have changed.

Record title, journal/venue, year, DOI or stable identifier, article type when
verifiable, metadata source, and access date. Deduplicate DOI and normalized
title. Store title metadata only unless licensing and the research purpose
explicitly support more. Use `references/license-and-provenance.md` for external
metadata and publisher material.

Measure descriptive features such as word and character count, colon/question
frequency, acronym use, keyword position, and recurring structural families.
Then interpret the result. Do not turn a median into a target, a frequent phrase
into a template, or a selected corpus into an acceptance model. Research-paper
titles are a secondary comparator when optimizing a Review or Perspective.

The CNS Skills biomaterials case study uses two auditable layers and stores no
abstracts or full text: a core of 70 elite-journal plus 30 accepted
main-conference titles, and a separate 100-title field-journal comparison layer
that retains useful *ACS Nano*, *Advanced Functional Materials*,
*Acta Biomaterialia*, *Biomaterials*, and adjacent examples. Fifty DOI records
occur in both panels, so the two 100-record layers contain 150 distinct titles;
never report them as 200 unique titles or pool them into one prestige average.
Use the elite core for venue-family contrasts
and the field layer for domain terminology. In the core, conference titles use
colons and acronyms more often than journal titles; that observation is a reason
to preserve article-type distinctions, not a reason to imitate conference
branding in a Review. The reusable lesson is methodological: compact titles
usually expose one scientific object and one intellectual move, while generic
three-part inventories often describe a table of contents rather than a
distinct contribution. Test that hypothesis against each manuscript rather
than treating it as a universal venue law.

## Generate distinct candidate families

Create candidates from at least four genuinely different families when the
source permits them:

- **Compact object/lens:** the scientific object plus the unique decision or
  organizing principle.
- **Contribution-led:** the supported result or capability, mainly for research
  articles.
- **Decision-led:** the choice, comparison, or experimental question that the
  manuscript resolves.
- **Main title plus subtitle:** use a colon only when the subtitle adds
  nonredundant scope or contribution.

Do not create cosmetic variants by swapping synonyms. Keep technical nouns
stable. Generate one deliberately conservative candidate so that any gain from
stronger wording is visible and auditable.

## Apply the seven title gates

Score each candidate from 0–4 with a one-line reason. The scores organize
judgment; they do not predict editorial outcomes.

| Gate | 4/4 question |
|---|---|
| Scope fidelity | Does every word remain inside the documented manuscript scope? |
| Contribution visibility | Can a reader see the result or synthesis that distinguishes this paper? |
| Scientific-object clarity | Is the material, task, system, or problem concrete enough to identify the paper? |
| Retrievability | Are the essential field and object terms present without keyword stuffing? |
| Cross-field readability | Can an adjacent-field reader understand it without avoidable jargon or acronyms? |
| Economy and cadence | Is every noun doing work, with no redundant subtitle or ornamental list? |
| Venue/article-type fit | Does it follow the current verified rules and conventions for the exact target? |

Reject a candidate regardless of total score when scope fidelity is below 3, a
conclusion-like term lacks evidence, or the title misstates the article type.
Use the transparent `scripts/title_audit.py` checks for count, punctuation,
acronym, keyword, formula, and advisory venue-limit diagnostics. The script is
triage; it cannot judge the manuscript's contribution or evidence by itself.

## English-first bilingual titles

For SCI journals and international conferences, choose the English title first
from the English argument map. Then write a Chinese title with the same object,
contribution, and evidence boundary. Functional equivalence is required;
word-for-word order and identical punctuation are not.

Back-audit both directions:

- Does the Chinese title add `systematic`, `mechanism`, `clinical`, `general`,
  `智能`, `精准`, or another stronger claim absent from English?
- Does the English title drop a necessary material class, comparison, or
  validation boundary present in Chinese?
- Are `model`, `method`, `framework`, `system`, and `platform` used with the same
  meaning in both languages?

## Anti-patterns requiring a decision

- three or more abstract nouns joined as a symmetrical inventory;
- `from X to Y` when the paper does not establish a real progression;
- priority, novelty, clinical, mechanism, safety, efficacy, generality, or
  transformation claims unsupported by the manuscript;
- `comprehensive`, `definitive`, `ultimate`, `revolutionary`, or similar
  promotion in place of a scientific distinction;
- a generic `framework`, `landscape`, `evidence`, or `pipeline` with no named
  construct;
- a subtitle that repeats the main title in different words;
- unnecessary acronyms, model names, punctuation, or keyword chains;
- a Review title that promises exhaustive coverage when the corpus is a
  structured narrative or illustrative selection.

These are review triggers, not automatic word bans. Keep a conventional phrase
when it is the clearest accurate wording for the actual contribution.

## Required title handoff

Return:

1. one recommended English title and its Chinese equivalent when useful;
2. three materially different alternatives;
3. article type, target status, word/character counts, and required search terms;
4. one-line gate reasons for each candidate;
5. the strongest tempting title that was rejected and the evidence/scope reason;
6. any live venue rule or manuscript component still missing.

For a full manuscript, update the reader-visible title, core document title
metadata, running title if present, cover letter, submission fields, and any
supplement that repeats the old title. Re-render and inspect the final artifact.
