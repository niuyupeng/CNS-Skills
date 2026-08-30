# Privacy

Effective date: 2026-08-30

CNS Skills is an open-source, instruction-first scientific-writing package. The package itself does not operate a hosted service, create user accounts, collect analytics, or send manuscript content to its maintainer.

The included local audit scripts read only the files a user explicitly supplies. By default, they run locally. Two optional network workflows make narrowly scoped requests:

- `cns_audit.py --verify-dois` sends DOI strings to the Crossref public API for metadata checks.
- `venue_corpus_analyzer.py` requests public scholarly metadata from the OpenAlex API.

Those services process requests under their own policies. Full audit JSON may contain local paths or unpublished excerpts; users should keep it confidential or use the documented `--shareable` option before external sharing. Host applications, models, connectors, document tools, and repositories used with CNS Skills have their own privacy terms. Users should not upload confidential or unpublished material to any external service unless they have authority to do so.

Questions or vulnerability reports may be opened through the repository's [support channels](SUPPORT.md).
