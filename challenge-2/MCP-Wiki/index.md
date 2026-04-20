---
title: "Challenge 2 MCP Research Wiki"
aliases:
  - "MCP Research Wiki"
  - "Wiki MCP Research"
note_type: "index"
tags:
  - "index"
  - "challenge-2"
  - "mcp"
  - "research-wiki"
search_terms:
  - "Challenge 2 MCP research wiki"
  - "Wiki MCP server"
  - "M365 Copilot grounding"
  - "source-backed wiki server"
related:
  - "architecture.md"
  - "implementation-plan.md"
  - "authentication-options.md"
  - "sources/bibliography.md"
  - "sources/codex-thread-mcp-implementation-evaluation.md"
  - "wiki-optimization-log.md"
---

# Challenge 2 MCP Research Wiki

This wiki is the research, implementation, and validation space for a purpose-built MCP server over the Challenge 2 generated wiki. It exists because Microsoft 365 Copilot could not reliably ground on local or Personal OneDrive wiki folders, while a proper MCP endpoint can expose the wiki as controlled, audited knowledge.

## Start Here

- [Architecture](architecture.md)
- [Implementation Plan](implementation-plan.md)
- [Implementation](implementation/README.md)
- [Security Model](security-model.md)
- [Authentication Options](authentication-options.md)
- [Semantic Retrieval Options](semantic-retrieval-options.md)
- [Decision Record](decision-record.md)
- [Wiki Optimization Log](wiki-optimization-log.md)
- [Codex Thread Capture And Publication Recommendation](sources/codex-thread-mcp-implementation-evaluation.md)
- [Candidate Register](candidate-register.md)
- [External Reference Submodules](references/external/README.md)
- [Bibliography](sources/bibliography.md)
- [Research Report Index](research/index.md)
- [MCP Wiki Lint Report](lint-report.md)
- [Source Register](data/source-register.json)
- [Bibliography Data](data/bibliography.json)
- [Candidate Register Data](data/candidate-register.json)

## Research Report

The raw Deep Research output is preserved in three equivalent formats, and a linked derivative is maintained for AI navigation:

- [Linked Markdown report](<research/Challenge 2 Wiki MCP Server Research Report - linked.md>)
- [Markdown report](<research/Challenge 2 Wiki MCP Server Research Report.md>)
- [Word report](<research/Challenge 2 Wiki MCP Server Research Report.docx>)
- [PDF report](<research/Challenge 2 Wiki MCP Server Research Report.pdf>)

The linked Markdown report is the preferred source for agents because it removes Deep Research internal markers and points to [the bibliography](sources/bibliography.md). The raw Markdown, DOCX, and PDF variants are preserved for evidence and human review. Hashes and file sizes are recorded in [the source register](data/source-register.json).

## Why This Is A Separate Wiki

The Challenge 2 corpus wiki in `challenge-2/wiki/` is generated from the synthetic dark-data source corpus and is used for benchmark evaluation. The public postmortem wiki explains the human and Codex collaboration history. This MCP research wiki is different: it is a forward-looking engineering research and implementation space for the server that will expose the corpus wiki safely to AI clients.

Keeping those scopes separate follows the LLM Wiki pattern: each wiki has a clear source boundary, purpose, index, and operating contract.

See [the Karpathy methodology note](sources/karpathy-llm-wiki-methodology.md) for the source-boundary rationale and [the wiki optimization log](wiki-optimization-log.md) for how this wiki is being tuned for navigation and AI retrieval.

## Current Direction

The first purpose-built read-only Wiki MCP server is now implemented under [the implementation workspace](implementation/README.md) rather than forked from a broad Obsidian, MediaWiki, or Wiki.js server. The candidate projects remain references with preserved licenses. The current implementation:

- expose only generated wiki notes, metadata, and source-register data;
- deny benchmark and gold-answer artifacts;
- return deterministic citations to wiki paths and source IDs;
- log source access for audit;
- support local stdio and Microsoft-compatible Streamable HTTP;
- uses first-use reference implementation submodules only for study, not as runtime dependencies;
- use OAuth 2.0 or Microsoft Entra ID / SSO for a production Copilot Studio-facing endpoint;
- includes semantic retrieval behind deterministic provenance and context-pack contracts, currently using a local deterministic exact-cosine hashing backend for validation while the embedding shortlist remains under benchmark;
- validate Copilot Studio direct MCP connection first;
- exclude API-key authentication unless live host validation proves it is required;
- validate external URLs at release time rather than in CI.

The `codex-mcp` evaluation client has completed live Q001 smoke validation with recorded `wiki.search` and `wiki.read` MCP audit events. Full validated-client benchmark evidence is generated through the Challenge 2 evaluation harness rather than stored directly in this research wiki.

The current MCP implementation and evaluation thread is captured as a public summary note at [Codex Thread Capture: MCP Implementation And Evaluation](sources/codex-thread-mcp-implementation-evaluation.md). The note records why this thread should be included in the current MCP pull request as summarized evidence, while leaving any raw transcript regeneration to the separate postmortem-public workflow.

## Quality Gate

Run [the MCP Wiki lint tool](tools/lint_mcp_wiki.py) after changing links, source registers, or metadata:

```bash
python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report
```

The generated [lint report](lint-report.md) and [machine-readable lint output](data/lint-report.json) check frontmatter, tags, local links, source-register paths, duplicate IDs, `.DS_Store` files, and Deep Research citation-marker leakage outside the raw report.

## Related Source Notes

- [Bibliography](sources/bibliography.md)
- [Karpathy LLM Wiki methodology](sources/karpathy-llm-wiki-methodology.md)
- [MCP specification sources](sources/mcp-specification.md)
- [GitHub candidate projects](sources/github-candidates.md)
- [Microsoft Copilot MCP sources](sources/microsoft-copilot-mcp.md)
- [Academic literature](sources/academic-literature.md)
- [Codex MCP implementation and evaluation thread capture](sources/codex-thread-mcp-implementation-evaluation.md)
