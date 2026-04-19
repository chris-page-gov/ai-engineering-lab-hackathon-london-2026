---
title: "MCP Wiki Decision Record"
note_type: "decision-register"
tags:
  - "decisions"
  - "mcp"
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

## Open Decisions

- Which authentication pattern should be used for a Copilot Studio-facing Streamable HTTP endpoint?
- Which candidate implementations should be added as git submodules, if any?
- Should semantic retrieval be added in v1, or deferred until deterministic lexical retrieval and provenance are proven?
