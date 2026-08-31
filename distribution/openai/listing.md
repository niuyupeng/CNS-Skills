# OpenAI universal Plugins Directory submission copy

Status: draft, not submitted.

Official basis checked 2026-08-30:

- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/guides/optimize-metadata

## Submission identity

| Portal field | Prepared value |
|---|---|
| Submission type | Skills only |
| Plugin name | CNS Skills |
| Publisher | Yupeng Niu, only if this exactly matches the verified OpenAI Platform developer identity |
| Proposed category | Productivity; use the closest available portal category if labels differ |
| Website | https://github.com/niuyupeng/CNS-Skills |
| Support URL | https://github.com/niuyupeng/CNS-Skills/blob/main/SUPPORT.md |
| Privacy policy URL | https://github.com/niuyupeng/CNS-Skills/blob/main/PRIVACY.md |
| Terms URL | https://github.com/niuyupeng/CNS-Skills/blob/main/TERMS.md |
| Logo source | assets/cns-icon.svg; confirm the portal's accepted format and export a square production PNG if required |
| Authentication | None |
| MCP server | None |
| Hosted account or analytics service | None |

The publisher value is a proposal, not a verification claim. The exact verified Platform identity, repository author, support contact, privacy policy, terms, and public listing must agree before submission.

## Short description

Author-led scientific positioning, outlines, evidence-bounded drafting, English revision, and submission-file QA.

## Long description

CNS Skills is an independent, open-source workflow for developing scientific manuscripts without outrunning the evidence. It distinguishes author decisions, verified evidence, format-only references, proposals, and superseded directions; builds argument-led outlines and evidence matrices; drafts only from approved sources; reconstructs Chinese manuscripts into natural submission English; audits consequential claims and citations; and checks figures, tables, responses, and clean submission files.

The skill supports research papers, reviews, theses, grants, rebuttals, and journal cover letters. It preserves supplied claims, numbers, terminology, citations, and project-defined scales; identifies unsupported or over-broad statements; and returns unresolved risks instead of inventing evidence. When the host provides document rendering, it can include rendered DOCX or PDF quality assurance.

CNS means Cell, Nature, and Science as an aspirational editorial benchmark. CNS Skills is not affiliated with or endorsed by those journals, their publishers, any conference, OpenAI, or Anthropic. It does not guarantee acceptance, fabricate evidence or references, or optimize writing to evade AI detectors.

## Privacy summary for reviewer context

CNS Skills is an instruction-first package and does not operate a hosted service, create user accounts, collect analytics, or send manuscripts to the maintainer. Included audit scripts read only user-supplied files and run locally by default. Optional DOI verification sends DOI strings to Crossref, and optional venue-corpus reconstruction requests public scholarly metadata from OpenAlex. Full local audit reports can contain paths or unpublished excerpts; the package documents a shareable-output mode and warns users not to disclose confidential material.

The public privacy policy remains authoritative:

https://github.com/niuyupeng/CNS-Skills/blob/main/PRIVACY.md

## Recommended starter prompts

Use the first four prompts from starter-prompts.md in the initial listing unless the portal permits more. They cover source-to-outline development, evidence-bounded first drafting, full-manuscript revision, and bilingual reconstruction. Additional prompts cover peer review, claim-citation auditing, titles, rebuttals, visual evidence, and review-method boundaries.

## Test-case source

Use openai/submission-tests.jsonl.

- Core minimum set: pos-01 through pos-05 and neg-01 through neg-03.
- Extended regression set: pos-06 through pos-08 and neg-04 through neg-06.
- Every case is self-contained and requires no private account, internal network, or unpublished fixture.

## Initial-submission release notes

CNS Skills is being submitted for the first time as a Skills-only plugin. It provides author-led positioning, scientific outlines, evidence matrices, evidence-bounded first drafts, English-first rewriting, title optimization, peer review, citation audits, figure/table QA, and clean-submission-file checks. The submitted bundle is open source under the MIT License and requires no hosted CNS account or MCP server.

Reviewer note: this submission uses FROZEN_RELEASE_TAG at FROZEN_COMMIT_SHA. The exact uploaded bundle checksum is FROZEN_ZIP_SHA256. Optional DOI and venue-metadata checks use the public Crossref and OpenAlex services as disclosed in the privacy policy. No test credentials are required.

Replace every frozen placeholder before submission.

## Availability decision

Do not select countries or regions by default. Select only locations where:

- the publisher is legally and operationally prepared to support users;
- the public privacy policy and terms are suitable;
- the repository and support channel are accessible;
- any optional Crossref or OpenAlex workflow is accurately disclosed; and
- the publisher can respond to support and safety reports.

Record the final selection and reason in compliance/preflight-checklist.md.

## Portal mapping

1. Confirm the submitting organization grants Apps Management write access.
2. Confirm the exact publisher identity is verified in the same OpenAI Platform organization.
3. Create a Skills only draft.
4. Complete the Info fields with the copy and URLs above.
5. Upload the exact final skill bundle built from FROZEN_COMMIT_SHA.
6. Confirm the bundle contains the tested SKILL.md plus every referenced script, reference, template, and asset.
7. Add the selected starter prompts.
8. Enter at least the five core positive and three core negative tests.
9. Select only the approved availability regions.
10. Paste the finalized release notes, complete policy attestations only after rechecking the whole draft, and submit for review.

Submission starts review; it does not establish approval or public availability. Do not say that CNS Skills is listed until OpenAI has approved it, the publisher has published it, and the public directory entry is visible.

## Claims that must not appear in the listing

- Approved, verified, certified, official, or endorsed by OpenAI, Anthropic, Cell, Nature, Science, or a conference.
- Guaranteed activation, guaranteed acceptance, acceptance-rate improvement, or editorial fast track.
- Real user counts, testimonials, institutional adoption, or successful submissions without documented permission and evidence.
- AI-detector evasion, zero-AI-score, plagiarism-evasion, or fabricated-reference capability.
- Test, routing, corpus, title, or auditor counts taken from a different release.
