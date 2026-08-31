# License, provenance, confidentiality, and external-tool gate

Use this reference when incorporating third-party text, code, data, figures, fonts, icons, models, templates, or cloud services.

## Provenance register

For every external component, record:

| Component | Type | Source/identifier | Author/owner | License/terms | Modification | Required credit | Redistribution allowed? | Status |
|---|---|---|---|---|---|---|---|---|

Check each layer separately. A repository license may not cover model weights, datasets, fonts, icons, screenshots, paper figures, or linked assets.

## Rules

- Publicly visible is not the same as open source or reusable.
- Verify the license at a pinned version or commit. A repository-wide license may contain per-directory exceptions, and a later revision may change the terms.
- Retain copyright and license notices required by MIT/BSD licenses.
- For Apache-2.0 material, retain the license, mark modifications, and preserve any applicable `NOTICE` content.
- Attribute CC BY content; respect share-alike, non-commercial, and no-derivatives restrictions.
- Do not redistribute publisher guides, phrasebanks, or paper figures merely because they are accessible online. Paraphrase short operational rules and link to the authoritative page.
- “Nature-style” or similar wording is descriptive, not certification or endorsement. State the access date and require final official-policy verification.
- Record permission for adapted/reproduced figures and the exact caption credit line.
- Verify that icon, stock-art, diagram, and graphical-abstract licenses permit publication, modification, and the intended distribution model.
- Treat source-available or proprietary skills as inspectable comparison material only. Do not import their prompts, instructions, code, templates, or assets without permission that covers modification and redistribution. For example, Anthropic's public `docx`, `pdf`, `pptx`, and `xlsx` skill directories have repository-specific proprietary terms even though other directories in the same repository are Apache-2.0.

Learning a general principle is not a license shortcut. Record the problem observed, derive an implementation independently, and keep the sources that informed the principle in the design review. If wording, code, examples, tests, or assets are adapted rather than independently implemented, treat them as a third-party component in the provenance register and satisfy the exact attribution and notice terms.

## Confidentiality gate

Before sending unpublished text, peer reviews, patient information, proprietary data, or figures to an external service, confirm:

- the author has authority to disclose it;
- consent, data-use agreements, embargoes, and reviewer confidentiality permit the transfer;
- the service's retention, training, location, and deletion terms are acceptable;
- sensitive identifiers are removed or protected;
- the target venue's AI/tool disclosure policy is satisfied.

If these conditions are unknown, keep the work local or stop and request authorization. Convenience is not permission.

## AI-assisted content

Verify the exact journal, article type, submission phase, and current policy. Text assistance, conceptual illustrations, data visualizations, graphical abstracts, and original research images may be governed differently.

Never use generative tools to create or alter experimental evidence. For permitted conceptual material, keep prompts/inputs, output provenance, human edits, disclosure text, and a statement that the graphic is illustrative rather than observed data.

Treat a visual-generation prompt as part of the provenance record when it materially determines scientific content or appearance. Record the figure brief, tool/model and version, date, policy clearance, generated output, human corrections, final labels, and the exact disclosure decision. Do not publish an unpublished manuscript-derived prompt when it would expose confidential claims or data; keep a private record and share only a redacted production description.

## Handoff

Do not call an artifact reusable or submission-ready while a material license, permission, confidentiality, or disclosure status is unresolved. Return the provenance register and label each entry `cleared`, `restricted`, `permission needed`, or `unknown`.
