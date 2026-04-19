---
title: "MCP Wiki Reference Material Policy"
note_type: "reference-policy"
status: "active"
tags:
  - "mcp"
  - "references"
  - "licensing"
  - "submodules"
search_terms:
  - "reference implementation policy"
  - "MCP submodule policy"
  - "license review before vendoring"
related:
  - "../candidate-register.md"
  - "../sources/bibliography.md"
  - "external/README.md"
  - "../decision-record.md"
---

# Reference Material Policy

This folder is for local access to external reference implementations or specifications only after a licensing and update decision is recorded.

Do not copy third-party code or documentation into this folder casually. Prefer citation notes in `../sources/` until we know:

- the upstream license;
- dependency license implications;
- whether full local redistribution is allowed;
- whether we need code, docs, or just a stable citation;
- how updates will be applied.

If a source is added as a git submodule or snapshot, include a sibling `SOURCE.md`, preserve upstream `LICENSE` and `NOTICE` files, and record the source in `../data/source-register.json`.

## Related

- [Candidate register](../candidate-register.md)
- [Bibliography](../sources/bibliography.md)
- [Decision record](../decision-record.md)
- [External reference workspace](external/README.md)
