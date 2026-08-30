# Contributing to CNS Skills

Thank you for helping improve evidence-first scientific writing.

## Useful contributions

- Reproducible false-positive or false-negative cases from `cns_audit.py`.
- Bilingual academic-style patterns with a clear explanation of context.
- Claim–citation audit cases using open or anonymized text.
- Improvements to review workflows, validation ladders, or artifact QA.
- Tests that demonstrate the proposed behavior.

Do not submit confidential manuscripts, personal data, copyrighted full text without permission, or features designed to evade AI detectors.

## Development

The audit script has no runtime dependencies. Run:

```bash
python -m unittest discover -s tests -v
python scripts/check_discovery_metadata.py
python scripts/build_plugin_bundle.py --check
python scripts/package_plugin.py --output-dir /tmp/cns-plugin
python scripts/cns_audit.py README.md --json /tmp/cns-report.json
```

Keep heuristics transparent. A new flag should have a name, rationale, example, and test. Avoid opaque aggregate “human scores.”

The repository root is the canonical standalone skill. After changing `SKILL.md`, `agents/`, `assets/`, `references/`, or a bundled runtime script, regenerate the marketplace payload and verify it:

```bash
python scripts/build_plugin_bundle.py --write
python scripts/build_plugin_bundle.py --check
```

Do not edit generated files under `plugins/cns-skills/skills/cns-skills/` directly.

## Pull requests

1. Open an issue for substantial workflow or schema changes.
2. Keep each pull request focused.
3. Add or update tests.
4. Explain likely false positives and language/domain limitations.
5. Confirm that no evidence or bibliographic metadata was generated without verification.

By contributing, you agree that your contribution is licensed under the MIT License.
