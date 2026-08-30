# English-first bilingual scientific writing

Use this reference when the source is Chinese, the target venue publishes in English, or the user requests a Chinese–English workflow.

## Default output contract

For SCI journals and international conferences, the default final deliverable is **submission English**. Chinese is the author-facing reasoning layer, not the language from which sentences are translated one by one.

Unless the user asks for a different package, return:

1. a clean English manuscript or revised passage;
2. a short Chinese change map explaining consequential scientific and structural decisions;
3. a bilingual terminology table when terminology is specialized or unstable;
4. an unresolved-risk list in the language most useful to the author.

Do not force a side-by-side bilingual manuscript unless requested. Parallel text doubles the opportunity for version drift.

## Translate the argument, not the syntax

Lock these elements before drafting English:

- the central claim and its evidence boundary;
- the population, material, model, comparator, endpoint, and validation layer;
- the distinction between observation, association, prediction, mechanism, and causation;
- quantitative values, units, uncertainty, and citation locations;
- field-specific terms that must remain stable.

Then rebuild each English paragraph from its intellectual function. Do not preserve Chinese word order, topic chains, omitted subjects, or four-part rhetorical symmetry merely because they appear in the source.

A safe bridge is:

```text
Chinese source → claim/evidence/logic map → English paragraph → back-audit against source
```

The map is authoritative. The literal Chinese sentence is not.

## Four-pass workflow

Assign stable segment IDs when the manuscript is long, collaborative, or likely to undergo several revision rounds. Keep a protected-token list for numbers, units, sample sizes, intervals, p/q values, chemical formulas, gene/material names, equations, citations, DOI strings, and figure/table identifiers. Run an invariant diff before and after translation and again after copy-editing.

### Pass 1 — Chinese evidence lock

In Chinese, state for each consequential sentence:

- what is known;
- how it is known;
- how strong the evidence is;
- what remains unknown;
- which term or number may not change.

Resolve ambiguous pronouns, hidden comparators, missing agents, and vague words such as “效果”“性能”“显著”“机制” before English drafting.

### Pass 2 — English argument reconstruction

Draft directly from the claim map. Give each paragraph one primary function and place evidence beside the clause it supports. Prefer concrete scientific subjects over empty framing.

Use first person when it makes agency or a contribution clearer and the venue permits it. Do not overuse passive voice to sound formal. Do not replace precise ordinary words with rare synonyms.

### Pass 3 — Field-native language pass

Check at least:

- articles and countability;
- singular/plural agreement and subject–verb agreement;
- tense by function: established knowledge, methods, observed results, and interpretation;
- collocations used in the target discipline;
- stable terminology across title, abstract, figures, and main text;
- explicit antecedents for `this`, `these`, `it`, and `which`;
- logical relations expressed by meaning, not stock transitions;
- calibrated modal verbs and evidential verbs;
- citation placement at the supported clause;
- sentence and paragraph rhythm across the whole section.

Reserve `significant` for statistical significance when that is what the text means. Do not use `prove`, `cause`, `safe`, `effective`, `generalizable`, or `clinically applicable` beyond the demonstrated evidence.

### Pass 4 — Back-audit

Map every consequential English claim back to the source and evidence ledger. Flag:

- new claims introduced during rewriting;
- narrower or broader scope;
- changed comparison direction;
- lost uncertainty or limitations;
- altered numbers, units, or citation entailment;
- English sentences that are fluent but scientifically less precise.

Run the audit after structural revision and again after final copy-editing.

Classify bilingual defects rather than saying only “awkward translation”:

| Dimension | Scientific examples |
|---|---|
| Accuracy | omission/addition, changed polarity, wrong number or comparison, association upgraded to causation |
| Terminology | wrong field term, unstable abbreviation, model/method/framework conflation |
| Linguistic convention | grammar, articles, countability, collocation, punctuation |
| Style | genre-inappropriate voice, repetitive scaffolding, inflated or vague wording |
| Audience | undefined specialist term, missing cross-disciplinary context |
| Design/markup | broken equation, citation, cross-reference, symbol, or DOCX structure |

Mark a defect **major** when it changes a scientific decision, claim, evidence boundary, quantitative value, or interpretation; otherwise mark it **minor**. Do not use back-translation as the only accuracy test because it can reproduce the same error.

## Common Chinese-to-English failure modes

Replace the missing reasoning, not merely the phrase:

| Weak transfer | Required repair |
|---|---|
| `With the rapid development of...` | Name the technical change that created the present problem or opportunity. |
| `has important significance` | State the decision, mechanism, capability, or interpretation that changes. |
| `provides a theoretical basis for...` | Specify the supported inference and its evidence boundary. |
| `lays a solid foundation / opens a new avenue` | Name the concrete next capability; remove it if none is demonstrated. |
| `the experimental results show that` repeated | Put the result or comparison in subject position when agency is already clear. |
| `on the one hand / on the other hand` | Use the actual contrast, trade-off, or conditional relationship. |
| many sentences beginning with `This` | Name the result, method, constraint, or inference. |
| `performance was greatly improved` | Give the endpoint, comparator, magnitude, uncertainty, and test conditions. |

These are diagnosis prompts, not banned phrases. Keep a conventional phrase when it is the clearest accurate choice.

## Title and abstract in English-final mode

For title naming or optimization, use `references/scientific-title-optimization.md`. Choose the English title from the English argument map, then write a Chinese title with the same scientific object, contribution, article type, and evidence boundary. Do not strengthen one language to make it sound more impressive. Match the exact venue's current length and style requirements, and avoid unnecessary acronyms, priority claims, and decorative punctuation.

The abstract should normally make these moves, in an order suited to the work:

1. establish the problem with minimal background;
2. define the unresolved gap or decision;
3. state what was done;
4. report the strongest evidence, preferably with scale or uncertainty where useful;
5. state the interpretation within the evidence boundary.

Do not force one sentence per move. Do not import limitations or numeric density from a corpus mechanically. Use `references/venue-corpus-findings.md` only as descriptive context.

## Terminology control

Create a termbase when the draft crosses languages or disciplines:

| Chinese source term | Canonical English | Meaning/scope | Avoid | First definition |
|---|---|---|---|---|

Do not treat near-synonyms as interchangeable. In particular, distinguish model, method, framework, system, platform, strategy, algorithm, workflow, and pipeline according to what was actually built.

If a field has competing translations, select one using recent primary literature and the target venue, record the choice, and keep it stable. Mark unresolved terms instead of silently improvising.

## Authentic voice

Human-sounding scientific English comes from visible judgment: what the author chose to compare, what the evidence licenses, and where the boundary lies. It does not come from random sentence variation or synonym substitution.

Preserve the author's characteristic directness, technical vocabulary, and legitimate uncertainty. Remove empty framing and repetitive templates, but retain necessary disciplinary conventions. Never optimize for an AI-detector score or promise detector evasion.

## Completion standard

An English-final deliverable passes only when:

- no consequential meaning changed without disclosure;
- terminology is stable across text and visuals;
- grammar, collocation, and reference chains were checked in context;
- claims remain proportional to evidence;
- the English reads as an argument composed in English rather than a polished literal translation;
- the author can identify every unresolved scientific or citation decision.
