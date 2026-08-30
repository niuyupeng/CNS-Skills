# Install and verify CNS Skills

CNS Skills is a skills-only plugin. It does not require an API key or an
external account. Python 3.9+ is needed only when you run the optional local
auditors.

## ChatGPT desktop / Codex

1. Add the repository marketplace:

   ```bash
   codex plugin marketplace add niuyupeng/CNS-Skills
   ```

2. Restart the ChatGPT desktop app.
3. Open **Plugins Directory**, choose the **CNS Skills** source, and install
   **CNS Skills**.
4. Start a new task and try:

   ```text
   Use $cns-skills to audit this synthetic sentence against the supplied evidence.
   Evidence: one in-vitro experiment. Sentence: "This platform enables clinical translation."
   ```

Expected behavior: the skill should narrow the sentence to the observed
in-vitro result and mark in-vivo performance and clinical utility as untested.

Check that the marketplace is configured:

```bash
codex plugin marketplace list
```

Refresh the repository marketplace after a new CNS Skills release:

```bash
codex plugin marketplace upgrade cns-skills
```

Then restart the desktop app and update or reinstall the plugin from its
directory page. To remove the source, first uninstall or disable CNS Skills in
the app, then run:

```bash
codex plugin marketplace remove cns-skills
```

These repository-marketplace instructions are for direct distribution. Public
listing in the universal Plugins Directory is a separate platform review.

## Claude Code

Add the marketplace and install the plugin:

```bash
claude plugin marketplace add niuyupeng/CNS-Skills
claude plugin install cns-skills@cns-skills
```

Reload active plugins and invoke the skill explicitly:

```text
/reload-plugins
/cns-skills:cns-skills
```

Refresh the marketplace after a release:

```bash
claude plugin marketplace update cns-skills
```

Uninstall the plugin or remove the marketplace:

```bash
claude plugin uninstall cns-skills@cns-skills
claude plugin marketplace remove cns-skills
```

## Standalone Agent Skill

Clone the repository into the skill directory used by your host:

```bash
# ChatGPT desktop / Codex
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.agents/skills/cns-skills

# Claude Code
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.claude/skills/cns-skills
```

If you cloned the repository, update it with `git pull --ff-only` from inside
that directory.

## Verify the optional local auditors

From the repository root:

```bash
python scripts/cns_audit.py --version
python scripts/review_citation_audit.py --version
python scripts/review_search_audit.py --version
python scripts/title_audit.py --version
python scripts/check_invariants.py --version
python scripts/check_crossrefs.py --version
```

Run auditors only on files you are authorized to process. Add `--shareable` to
JSON-producing commands before sharing a report; otherwise a report can retain
local paths or manuscript excerpts.

## Troubleshooting

- **Marketplace added but plugin not visible:** restart the desktop app, open
  the Plugins Directory, and select the CNS Skills source.
- **Claude reports plugin not found:** run
  `claude plugin marketplace update cns-skills`, then install again.
- **Skill does not activate automatically:** invoke `$cns-skills` in ChatGPT or
  Codex, or `/cns-skills:cns-skills` in Claude Code.
- **An auditor rejects a file:** run the command without a strict flag first and
  inspect the diagnostic report. A diagnostic is triage, not proof of scientific
  correctness.

Report reproducible installation problems through the
[bug report form](https://github.com/niuyupeng/CNS-Skills/issues/new?template=bug_report.yml).
