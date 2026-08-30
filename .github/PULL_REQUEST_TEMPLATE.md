## What this changes

Describe the manuscript decision, routing behavior, audit invariant, or distribution problem addressed by this pull request.

## Why the change belongs in CNS Skills

Explain the generalizable scientific-writing value. Do not include confidential manuscript text or turn a single paper-specific preference into a universal rule.

## Verification

- [ ] I added or updated a meaningful test when behavior changed.
- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] `python scripts/check_discovery_metadata.py` passes.
- [ ] `python scripts/build_plugin_bundle.py --check` passes.
- [ ] Standalone and generated plugin skills validate.
- [ ] Documentation links and installation commands were checked when changed.

## Evidence, privacy, and provenance

- [ ] This change does not fabricate evidence, acceptance outcomes, citations, or AI-detector claims.
- [ ] No confidential manuscript, reviewer, participant, credential, or unpublished source content is included.
- [ ] External text, code, data, and assets have compatible licenses and required attribution.
- [ ] Any new diagnostic states what it can and cannot establish.
