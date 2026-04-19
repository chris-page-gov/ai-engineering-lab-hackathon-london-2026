---
title: "MCP Wiki Decision Record"
note_type: "decision-register"
tags:
  - "decisions"
  - "mcp"
search_terms:
  - "MCP wiki decisions"
  - "wiki optimisation decisions"
  - "citation-linked report"
  - "submodule license review"
related:
  - "index.md"
  - "wiki-optimization-log.md"
  - "sources/bibliography.md"
  - "implementation-plan.md"
---

# MCP Wiki Decision Record

| ID | Decision | Rationale | Status |
| --- | --- | --- | --- |
| MCP-DEC-001 | Keep MCP research in `challenge-2/MCP-Wiki/` rather than merging it into `challenge-2/wiki/` or `postmortem-public/wiki/`. | The generated corpus wiki, public postmortem wiki, and MCP engineering research have different source boundaries and audiences. | Accepted |
| MCP-DEC-002 | Preserve Markdown, DOCX, and PDF variants of the Deep Research report. | Markdown is best for agents; DOCX and PDF support human review and publication workflows. | Accepted |
| MCP-DEC-003 | Treat Karpathy methodology sources as citation-only in public wiki notes. | The localized gist/X copies have no explicit redistribution license in the public record. | Accepted |
| MCP-DEC-004 | Build a purpose-built read-only Wiki MCP server first. | Existing wiki MCP servers are useful references but are too broad, mutable, or backend-specific for this evaluation-safe use case. | Proposed |
| MCP-DEC-005 | Add external specifications and reference implementations as citation notes first, submodules only after license review. | This preserves licensing and keeps the repo updateable without copying third-party code prematurely. | Accepted |
| MCP-DEC-006 | Prefer Python/FastMCP for the first implementation. | The repo already uses Python for wiki/evaluation tooling, and FastMCP supports local and HTTP MCP server surfaces. | Proposed |
| MCP-DEC-007 | Preserve the raw Deep Research report and maintain a linked derivative. | The raw report is evidence of the Deep Research output; the linked derivative is easier for humans and AI clients to navigate because citations resolve through the bibliography. | Accepted |
| MCP-DEC-008 | Make frontmatter, tags, search terms, and related links part of the wiki quality bar. | Search quality and AI retrievability should be measurable rather than implicit. | Accepted |
| MCP-DEC-009 | Add a local lint gate for links, metadata, source-register paths, duplicate IDs, `.DS_Store`, and opaque citation markers. | The wiki is becoming an implementation input, so broken navigation and stale source metadata should fail before publication. | Accepted |
| MCP-DEC-010 | Keep lint and optimization records inside the MCP Wiki. | The build strategy for the wiki is itself research evidence for how to create AI-usable knowledge bases. | Accepted |

## Open Decisions

- Which authentication pattern should be used for a Copilot Studio-facing Streamable HTTP endpoint?
- Which candidate implementations should be added as git submodules, if any?
- Should semantic retrieval be added in v1, or deferred until deterministic lexical retrieval and provenance are proven?
- Should external URLs be actively checked in CI, or kept as a release-time validation because publisher sites can rate-limit or redirect unpredictably?

## Related

- [Wiki optimization log](wiki-optimization-log.md)
- [Bibliography](sources/bibliography.md)
- [Implementation plan](implementation-plan.md)
- [Lint report](lint-report.md)
