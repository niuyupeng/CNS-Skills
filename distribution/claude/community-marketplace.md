# Claude community marketplace submission pack

Status: draft, not submitted or approved.

Official process checked 2026-08-30:

https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace

Anthropic distinguishes the curated claude-plugins-official marketplace from the reviewed third-party claude-community marketplace. The public submission form feeds the community marketplace, not the separately curated official marketplace.

## Immutable submission values

| Field | Value |
|---|---|
| Plugin name | cns-skills |
| Display name | CNS Skills |
| Repository | https://github.com/niuyupeng/CNS-Skills |
| Plugin directory | plugins/cns-skills |
| Release tag | FROZEN_RELEASE_TAG |
| Commit SHA | FROZEN_COMMIT_SHA |
| Version | FROZEN_VERSION |
| License | MIT |
| Maintainer | Yupeng Niu |
| Support | https://github.com/niuyupeng/CNS-Skills/blob/main/SUPPORT.md |
| Privacy | https://github.com/niuyupeng/CNS-Skills/blob/main/PRIVACY.md |
| Terms | https://github.com/niuyupeng/CNS-Skills/blob/main/TERMS.md |

Replace the frozen placeholders with public immutable values. The submitted commit must contain the same version in the root skill, Claude manifest, Codex manifest, marketplace metadata, citation file, and generated plugin payload.

## Submission description

CNS Skills is an independent, MIT-licensed Agent Skill for evidence-bounded scientific manuscript revision. It supports English-first bilingual rewriting, scientific-title optimization, peer review and rebuttals, claim-citation and overclaiming audits, figure/table/caption QA, and clean-submission-file checks. It preserves supplied scientific claims and invariants, reports unresolved evidence limits, and refuses fabricated evidence, acceptance guarantees, and AI-detector evasion.

It is a local, skills-only plugin with no hosted CNS account or MCP server. Optional scripts can query Crossref with DOI strings and OpenAlex for public scholarly metadata, as disclosed in the repository privacy policy.

## Why it belongs in the community marketplace

- It addresses recurring research-writing workflows rather than generic text rewriting.
- It provides explicit positive and negative routing boundaries.
- Its instructions, references, local auditors, tests, privacy terms, and license are inspectable.
- It supports both Claude Code plugin installation and the open Agent Skills layout.
- It does not depend on a proprietary CNS backend.

These are verifiable repository characteristics, not a claim of marketplace endorsement or external adoption.

## Local validation

Run from the repository root against the exact frozen commit:

~~~bash
claude plugin validate ./plugins/cns-skills
claude --plugin-dir ./plugins/cns-skills
~~~

Inside the local test session:

~~~text
/cns-skills:cns-skills
~~~

Then run representative positive and negative prompts from ../openai/submission-tests.jsonl. Confirm that legitimate manuscript tasks invoke the skill, close non-target requests do not, mixed requests preserve the legitimate work while refusing the prohibited clause, and every reported capability exists in the frozen bundle.

## Console-form copy source

Use the individual-author Console form:

https://platform.claude.com/plugins/submit

Map its current labels to the following:

- Repository URL: https://github.com/niuyupeng/CNS-Skills
- Plugin path: plugins/cns-skills
- Commit or release reference: FROZEN_COMMIT_SHA and FROZEN_RELEASE_TAG
- Plugin name: cns-skills
- One-line summary: Evidence-bounded scientific manuscript revision, bilingual rewriting, peer review, citation audits, and clean-copy QA.
- Maintainer: Yupeng Niu, matching the repository and submission account.
- License: MIT.
- Runtime or service dependencies: no hosted CNS service; Python 3.9+ is needed only for optional local auditors.
- Network behavior: optional DOI-string requests to Crossref and public scholarly-metadata requests to OpenAlex; no manuscript upload to the maintainer.
- Safety boundary: no fabricated evidence, acceptance guarantees, publisher affiliation, or detector evasion.

If the form asks for additional information, answer from the frozen public repository. Do not infer user counts, production adoption, review status, or compatibility that has not been tested.

## Submission and publication checks

- The repository and referenced commit are public.
- The commit is immutable and contains the validated plugin directory.
- The strict validation command passes without warnings.
- A clean local install can invoke /cns-skills:cns-skills.
- All version strings and public proof counts describe the same release.
- README, support, privacy, terms, security, and license links resolve without sign-in.
- No private manuscript, path, credential, unpublished excerpt, or unredacted audit report is bundled.
- The community submission is not described as official marketplace inclusion.

If approved, Anthropic pins the accepted plugin to a commit SHA and the community catalog sync may occur later. Do not announce availability until the entry is visible in the public community catalog.

After visibility is confirmed, the community-marketplace install path can be documented as:

~~~text
/plugin marketplace add anthropics/claude-plugins-community
/plugin install cns-skills@claude-community
~~~

Keep the repository-marketplace installation instructions available until the community entry is actually installable.
