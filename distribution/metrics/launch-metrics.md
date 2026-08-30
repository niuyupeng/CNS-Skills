# CNS Skills launch measurement template

The launch question is not only how many stars appeared. Measure discovery, conversion, activation, quality, and community contribution separately.

Record an exact T0 baseline immediately before the first directory submission or public post. GitHub traffic data can lag and is retained for a limited period, so capture it on schedule and label the measurement timestamp.

## Measurement table

| Metric | Definition | T0 | 24 hours | 7 days | 30 days | Source |
|---|---|---:|---:|---:|---:|---|
| Repository views | Total GitHub repository views in the reported window |  |  |  |  | GitHub Traffic |
| Unique visitors | Unique repository visitors in the reported window |  |  |  |  | GitHub Traffic |
| Clones | Total clones in the reported window |  |  |  |  | GitHub Traffic |
| Unique cloners | Unique cloners in the reported window |  |  |  |  | GitHub Traffic |
| Stars | Current stargazer count |  |  |  |  | GitHub API |
| Forks | Current fork count; treat as contribution intent, not normal installation |  |  |  |  | GitHub API |
| Release downloads | Sum of assets for the frozen release, reported per asset as well |  |  |  |  | GitHub Releases API |
| Referring domains | Count and names of external referrers |  |  |  |  | GitHub Traffic |
| Qualified issues | Reproducible install, routing, audit, or output-quality issues |  |  |  |  | GitHub Issues |
| Discussions | Substantive workflow questions or reports |  |  |  |  | GitHub Discussions |
| External contributors | Distinct non-maintainer contributors |  |  |  |  | GitHub contributors/PRs |
| OpenAI directory state | not submitted, draft, under review, changes requested, approved, published |  |  |  |  | OpenAI Platform |
| Claude directory state | not submitted, under review, changes requested, approved, catalog visible |  |  |  |  | Claude Console/catalog |
| Awesome-list state | target, PR URL, review state, merged entry |  |  |  |  | Target repository |
| Public post clicks | Link clicks where the platform exposes them |  |  |  |  | Platform analytics |
| Clean install confirmations | Fresh installs confirmed by maintainer or external tester |  |  |  |  | Test log/issues |
| Successful workflow reports | Reports with a concrete input class and expected output, excluding vague praise |  |  |  |  | Discussions/issues |
| False-positive routes | Non-target prompts that invoked CNS Skills |  |  |  |  | Issues/eval log |
| False-negative routes | In-scope prompts that failed to invoke CNS Skills |  |  |  |  | Issues/eval log |
| Safety/integrity defects | Unsupported expansion, fabricated evidence, privacy leak, or evasion behavior |  |  |  |  | Issues/private reports |
| Median first response time | Median time to first maintainer response on qualified reports |  |  |  |  | Issue timestamps |

Use not available rather than zero when a platform does not expose a metric.

## Channel log

| Channel | Post/submission URL | Published at | Copy variant | Impressions | Clicks | GitHub referrer visible? | Qualified feedback | Action |
|---|---|---|---|---:|---:|---|---:|---|
| OpenAI directory |  |  | listing |  |  |  |  |  |
| Claude community |  |  | listing |  |  |  |  |  |
| OpenAI Developer Forum |  |  | technical |  |  |  |  |  |
| X |  |  | concise |  |  |  |  |  |
| LinkedIn |  |  | research-software |  |  |  |  |  |
| V2EX |  |  | Chinese technical |  |  |  |  |  |
| 掘金 |  |  | tutorial |  |  |  |  |  |
| 知乎 |  |  | educational |  |  |  |  |  |
| Reddit |  |  | community-specific |  |  |  |  |  |
| Research groups | private or permission note |  | concise Chinese |  |  | no |  |  |

## Review cadence

### 24-hour review

- Capture GitHub views, unique visitors, clones, referrers, stars, forks, and release-asset downloads.
- Confirm every public link, install command, image, privacy page, and checksum works.
- Respond to reproducible installation failures or safety issues first.
- Record which channel produced actual repository traffic.
- Do not change positioning solely because stars remain low in the first day.

### 7-day review

- Compare traffic by channel and stop repeating posts with impressions but no relevant clicks.
- Check OpenAI, Claude, and awesome-list review states.
- Group feedback into install friction, routing, manuscript quality, citation audit, visual QA, privacy, and documentation.
- Convert reproducible failures into issues and regression tests.
- Ask willing testers for a privacy-safe, permissioned workflow description; do not solicit praise.
- Update documentation only from verified recurring confusion.

### 30-day review

- Separate one-time launch traffic from organic search, directory, and referral traffic.
- Review successful installs, repeated use, external contributors, and substantive issues alongside stars.
- Identify the highest-converting use case and the most common false route.
- Decide whether to improve landing-page proof, installation, metadata, workflow quality, or support capacity.
- Publish only aggregated, verifiable numbers with an as-of date and source.

## Diagnostic interpretation

| Observed pattern | Likely bottleneck | Next experiment |
|---|---|---|
| Low unique visitors and low stars | Distribution or indexing | Complete directory submissions and one high-fit community post |
| High visitors but low installs/downloads | Landing-page or install friction | Shorten first-run path and test a fresh installation |
| Downloads or clones but few successful workflows | Activation or documentation | Add one synthetic end-to-end demo and clearer expected output |
| Successful workflows but few public signals | CTA or privacy constraints | Invite a star or privacy-safe issue after value is delivered, without incentives |
| Many false-positive routes | Metadata precision | Strengthen non-target clauses and replay negative cases |
| Many false-negative routes | Metadata recall | Add outcome language from real in-scope prompts and replay held-out cases |
| Safety or unsupported-claim defect | Product integrity | Pause promotion for the affected workflow, fix, test, and disclose if material |

## Useful read-only collection commands

Run with an authenticated GitHub CLI account that can view repository traffic:

~~~powershell
gh api repos/niuyupeng/CNS-Skills/traffic/views
gh api repos/niuyupeng/CNS-Skills/traffic/clones
gh api repos/niuyupeng/CNS-Skills/traffic/popular/referrers
gh api repos/niuyupeng/CNS-Skills
gh api repos/niuyupeng/CNS-Skills/releases
~~~

Preserve the raw measurement timestamp. Do not describe delayed traffic data as real-time.
