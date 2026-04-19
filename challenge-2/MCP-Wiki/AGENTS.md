# Challenge 2 MCP Research Wiki Operating Rules

This folder is a research, design, and implementation wiki for the Challenge 2 Wiki MCP server. It is separate from the generated Challenge 2 corpus wiki in `challenge-2/wiki/` and from the public Codex postmortem in `postmortem-public/`.

## Purpose

- Preserve the research basis for a purpose-built, source-grounded Wiki MCP server.
- Keep implementation decisions, candidate assessments, specifications, and security constraints in one navigable place.
- Support future agents building the MCP server without mixing engineering research into the Challenge 2 evaluation corpus.

## Boundaries

- Do not add this folder to the Challenge 2 evaluation source surface unless the evaluation explicitly asks about MCP implementation research.
- Do not place benchmark gold answers or evaluation run outputs in the MCP server's exposed knowledge surface.
- Do not copy full third-party source bodies unless the license permits redistribution and the source register records the license.
- Treat external specifications, reference implementations, and academic papers as cited sources first. Vendor or submodule them only after license and update policy are recorded.

## Source And License Rules

- Every external source note must record canonical URL, license status, publication status, retrieval or update method, and whether full text is stored locally.
- Preserve upstream license files when adding submodules, vendored examples, or specification snapshots.
- If a source has no explicit redistribution license, cite it and summarize it; do not publish a full local copy.
- The Karpathy LLM Wiki gist remains citation-only in public materials unless an explicit license or permission is obtained.

## Folder Contract

- `index.md` is the navigation entry point.
- `architecture.md` explains how the research wiki, future server, source corpus, and external references fit together.
- `implementation/` is reserved for implementation notes and, later, server design docs.
- `references/external/` is reserved for git submodules or vendored reference implementations after licensing review.
- `specifications/` is reserved for updateable MCP specification notes or snapshots.
- `research/` stores human-readable research report variants and report index notes.
- `sources/` stores source notes for specifications, candidate projects, methodology sources, and academic work.
- `data/` stores machine-readable registers.

## Implementation Bias

Build the first server as read-only, evaluation-safe, and auditable. Mutation tools, raw source access, vector stores, and external service calls require explicit decisions before implementation.
