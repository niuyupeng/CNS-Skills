# CNS Skills release and distribution preflight checklist

Status: blocking checklist. Every unchecked blocker must remain unresolved in public claims.

Preparation note, 2026-08-30: the repository worktree contained unreleased modified and untracked files while this package was written. Do not submit or promote that moving state. Freeze, test, commit, tag, package, and verify one coherent release first.

## A. Immutable release

- [ ] FROZEN_RELEASE_TAG is a public tag on the intended commit.
- [ ] FROZEN_COMMIT_SHA is recorded and resolves in the public repository.
- [ ] The release source has no uncommitted or untracked files.
- [ ] SKILL.md metadata, root and packaged plugin manifests, marketplace metadata, CITATION.cff, README citation example, changelog, and package name use FROZEN_VERSION.
- [ ] The generated plugin payload matches the root skill and all referenced scripts, references, templates, and assets.
- [ ] The uploadable ZIP is built from FROZEN_COMMIT_SHA, opens successfully, and contains no secrets, local caches, private documents, or temporary files.
- [ ] FROZEN_ZIP_SHA256 is recomputed from the exact upload artifact and published beside it.
- [ ] All release CI jobs pass on the frozen commit and tag.
- [ ] Declared deterministic-test, routing-case, corpus, title-panel, venue-profile, editorial-gate, and auditor counts are regenerated from the frozen tag.
- [ ] FROZEN_PROOF_LINE is identical in the English and Chinese READMEs, release notes, directory copy, and launch posts; the social preview uses the same stable positioning, and any count it displays matches the frozen release.
- [ ] A clean installation from the release artifact works in every host claimed in public copy.
- [ ] Optional local auditors report their actual Python version requirement and dependency/network behavior accurately.

## B. Public identity and legal pages

- [ ] The exact public publisher name is chosen.
- [ ] The OpenAI Platform developer or business identity is verified under that same name.
- [ ] The submitting OpenAI organization grants Apps Management write access.
- [ ] GitHub author/manifests, CITATION.cff, support contact, privacy policy, terms, and directory listing do not present conflicting publisher identities.
- [ ] Website, support, privacy, terms, security, license, code of conduct, and contribution URLs are public without sign-in.
- [ ] The support process can receive both public bug reports and private security/privacy reports.
- [ ] The independent-project disclaimer is visible: CNS means Cell, Nature, and Science as an aspirational benchmark and does not imply affiliation or endorsement.
- [ ] The MIT license and no-warranty boundary are retained.
- [ ] No third-party logo, publisher mark, proprietary phrasebank, confidential corpus text, or unlicensed asset is included.

## C. Privacy and scientific integrity

- [ ] The listing accurately says there is no hosted CNS account, maintainer analytics service, or manuscript collection service.
- [ ] Optional Crossref DOI-string and OpenAlex public-metadata requests are disclosed.
- [ ] Local full reports that may contain paths or unpublished excerpts are distinguished from shareable output.
- [ ] Test fixtures and demos contain only synthetic or explicitly authorized public material.
- [ ] Public issues and posts warn users not to upload confidential manuscripts, personal data, credentials, or peer-review material.
- [ ] The skill refuses fabricated sources, results, sample sizes, p-values, mechanisms, publication status, or validation.
- [ ] The skill refuses acceptance guarantees, publisher/platform affiliation claims, plagiarism evasion, and AI-detector evasion.
- [ ] Automated DOI or text flags are described as diagnostics requiring expert review, not proof of entailment or correctness.
- [ ] Medical, legal, raw-statistical-analysis, generic-translation, and coursework boundaries remain accurate.

## D. OpenAI Skills-only submission

- [ ] Submission type is Skills only; no nonexistent MCP server or integration reference is entered.
- [ ] The final uploaded skill bundle is the same file tree tested locally.
- [ ] SKILL.md contains clear trigger conditions, non-target conditions, task instructions, and minimal scoped authority.
- [ ] Every referenced script, reference, template, and asset is present in the bundle.
- [ ] Listing name, short description, long description, logo, category, website, support, privacy, and terms are complete.
- [ ] At least five positive tests include prompt, expected skill/workflow behavior, expected result shape, and reproducible fixture details.
- [ ] At least three negative tests include prompt/scenario, expected refusal/clarification/safe fallback, and why CNS Skills should not complete it.
- [ ] Reviewer tests require no MFA, SMS, email confirmation, private network, unpublished context, or CNS account.
- [ ] Starter prompts show realistic high-value workflows and do not promise unavailable rendering, lookup, or file operations.
- [ ] Country and region availability is selected only after publisher, support, privacy, and terms readiness is confirmed.
- [ ] Initial release notes identify the frozen tag, commit, checksum, lack of required credentials, and optional network behavior.
- [ ] Policy attestations are completed only after the final portal draft is rechecked.
- [ ] Public copy says submitted, under review, approved, or published only when that exact state is true.

## E. Claude community marketplace

- [ ] The public repository commit contains plugins/cns-skills/.claude-plugin/plugin.json and the complete skills tree.
- [ ] `claude plugin validate ./plugins/cns-skills` passes against FROZEN_COMMIT_SHA (use only flags shown by the installed CLI's `--help`).
- [ ] A local session loaded from ./plugins/cns-skills invokes /cns-skills:cns-skills successfully.
- [ ] Positive, negative, mixed, privacy, and integrity cases are replayed against the frozen plugin.
- [ ] The submission uses the individual Console form unless a Team/Enterprise organization and directory-management access are intentionally used.
- [ ] Public copy distinguishes claude-community from the separately curated claude-plugins-official marketplace.
- [ ] No approval is announced until the public community catalog contains the pinned entry and installation works.

## F. Awesome-list and public promotion

- [ ] Each target list's live contribution rules, section, row format, ordering, license requirement, and star threshold are checked immediately before editing.
- [ ] The first pull request targets one high-fit list and contains a customized rationale.
- [ ] CURRENT_STAR_COUNT and all proof counts are refreshed at action time.
- [ ] Every social post identifies the author/project relationship and links to the canonical repository.
- [ ] Platform-specific self-promotion and moderation rules are checked at posting time.
- [ ] Reddit posts are limited to one relevant community unless moderators explicitly allow cross-posting.
- [ ] Hacker News copy is written by the owner in their own words; no generated comment or vote solicitation is used.
- [ ] No automated posting, mass direct messages, purchased engagement, reciprocal stars, or voting coordination is used.
- [ ] Real user quotes, logos, affiliations, and outcomes are published only with documented permission and evidence.

## G. Final human sign-off

| Decision | Owner | Date | Evidence link or note |
|---|---|---|---|
| Release frozen |  |  |  |
| CI and package verified |  |  |  |
| Identity and policies verified |  |  |  |
| OpenAI draft reviewed |  |  |  |
| Claude draft reviewed |  |  |  |
| Promotion copy facts checked |  |  |  |
| Public posting authorized |  |  |  |

An empty sign-off row is not approval.
