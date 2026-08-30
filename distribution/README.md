# CNS Skills distribution and directory submission pack

Status: internal draft; no directory approval, public post, form submission, or pull request is implied.

This folder turns the current CNS Skills repository into an action-ready distribution package. It was prepared on 2026-08-30 against the current repository content and the current official submission documentation:

- OpenAI plugin submission: https://developers.openai.com/plugins/deploy/submission
- OpenAI metadata guidance: https://developers.openai.com/plugins/guides/optimize-metadata
- Claude Code community marketplace: https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace

## Freeze these values before using any public copy

| Variable | Required value |
|---|---|
| FROZEN_RELEASE_TAG | Replace with the public release tag being submitted |
| FROZEN_VERSION | Replace with the version embedded in the final skill and manifests |
| FROZEN_COMMIT_SHA | Replace with the immutable public commit used by reviewers |
| FROZEN_ZIP_SHA256 | Replace with the checksum of the exact uploaded bundle |
| FROZEN_PROOF_LINE | Replace with test, routing, corpus, and auditor counts from that exact release only |
| SUBMISSION_DATE | Replace with the actual date of submission |

Do not resolve these placeholders from memory. Read them from the frozen tag, release assets, CI run, and package checksum. If a public page, social card, manifest, citation file, or post reports a number, it must describe the same frozen release.

## Package map

| File | Use |
|---|---|
| openai/listing.md | Copy source and field mapping for an OpenAI Skills-only submission |
| openai/starter-prompts.md | Highest-value user-facing starter prompts |
| openai/submission-tests.jsonl | Eight positive and six negative reviewer-reproducible cases |
| claude/community-marketplace.md | Claude community marketplace validation and form copy |
| awesome-lists/submission-pack.md | Targeted list entry and pull-request copy |
| social/platform-matrix.md | Channel order, audience, copy, CTA, and anti-spam constraints |
| compliance/preflight-checklist.md | Release, identity, privacy, claim, and platform gates |
| metrics/launch-metrics.md | Measurement definitions and 24-hour, 7-day, and 30-day review |
| metrics/launch-metrics-template.csv | Fillable measurement sheet |

## Recommended execution order

1. Freeze one release and one commit. Do not promote an unreleased or internally inconsistent worktree.
2. Complete every blocking item in compliance/preflight-checklist.md.
3. Run the OpenAI and Claude validation cases against the exact final bundle.
4. Submit to the OpenAI universal Plugins Directory and Claude community marketplace.
5. Create one targeted awesome-list pull request at a time.
6. Publish channel-specific posts only after the listing facts, proof line, and links are stable.
7. Record the baseline before posting, then fill the 24-hour, 7-day, and 30-day measurements.

The materials deliberately avoid fabricated users, testimonials, acceptance rates, external endorsements, directory approvals, or guaranteed routing claims.
