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
  - "authentication-options.md"
  - "semantic-retrieval-options.md"
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
| MCP-DEC-011 | Use OAuth 2.0 or Microsoft Entra ID / SSO as the target authentication pattern for Copilot Studio-facing Streamable HTTP. | It gives principal identity, expiry, revocation, consent, and auditability. Anonymous and bearer-token modes are acceptable only for local or private smoke tests. | Accepted |
| MCP-DEC-012 | Add the first-use candidate repositories as submodules for study: ProfessionalWiki, olgasafonova, qmd, and mkdocs-mcp-plugin. | These were the candidates marked study-first or possible-submodule; they cover wiki surface design, remote HTTP deployment, Markdown retrieval, and Python/FastMCP retrieval. | Accepted |
| MCP-DEC-013 | Include semantic retrieval in v1 behind the same provenance-preserving `search_wiki` and `build_context_pack` contracts. | Semantic retrieval should improve recall, but deterministic lexical retrieval, source IDs, snippets, and citation objects must remain the audit baseline. | Accepted |
| MCP-DEC-014 | Keep external URL checking as release-time validation rather than a CI gate. | Publisher sites can rate-limit, block, redirect, or change availability unpredictably; CI should not fail because a third-party website is temporarily unavailable. | Accepted |
| MCP-DEC-015 | Evaluate v1 semantic retrieval using a local permissive embedding shortlist and exact local vector matrix before locking the final model. | This preserves licensing and reproducibility while allowing evidence-based choice. The provisional baseline is `BAAI/bge-small-en-v1.5` plus exact NumPy cosine search, with `all-MiniLM-L6-v2` and `e5-small-v2` as comparisons. | Accepted |
| MCP-DEC-016 | Validate Copilot Studio direct MCP connection first. | Copilot Studio direct MCP currently exposes tools and resources from a connected MCP server. Use Agents Toolkit plugin packaging or a custom connector only if direct connection cannot deliver the required tools, resources, authentication, or governance behaviour. | Accepted |
| MCP-DEC-017 | Exclude API-key authentication unless live Copilot Studio validation proves it is required for a specific host path. | OAuth 2.0 / Microsoft Entra ID remains the target production pattern; API keys weaken principal-level audit and have inconsistent Microsoft host support. | Accepted |

## Open Decisions

- Which embedding model from the evaluated shortlist should be locked after the v1 retrieval benchmark?
- Does Copilot Studio direct MCP validation expose enough of the server's tools and resources, or does the work need to move to Agents Toolkit packaging?

## Related

- [Wiki optimization log](wiki-optimization-log.md)
- [Authentication options](authentication-options.md)
- [Semantic retrieval options](semantic-retrieval-options.md)
- [Bibliography](sources/bibliography.md)
- [Implementation plan](implementation-plan.md)
- [External reference workspace](references/external/README.md)
- [Lint report](lint-report.md)
