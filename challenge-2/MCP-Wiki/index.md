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
---

# Challenge 2 MCP Research Wiki

This wiki is the research and implementation planning space for a purpose-built MCP server over the Challenge 2 generated wiki. It exists because Microsoft 365 Copilot could not reliably ground on local or Personal OneDrive wiki folders, while a proper MCP endpoint can expose the wiki as controlled, audited knowledge.

## Start Here

- [Architecture](architecture.md)
- [Implementation Plan](implementation-plan.md)
- [Security Model](security-model.md)
- [Decision Record](decision-record.md)
- [Candidate Register](candidate-register.md)
- [Research Report Index](research/index.md)
- [Source Register](data/source-register.json)
- [Candidate Register Data](data/candidate-register.json)

## Research Report

The Deep Research output is stored in three equivalent formats:

- [Markdown report](<research/Challenge 2 Wiki MCP Server Research Report.md>)
- [Word report](<research/Challenge 2 Wiki MCP Server Research Report.docx>)
- [PDF report](<research/Challenge 2 Wiki MCP Server Research Report.pdf>)

The Markdown report is the preferred source for agents. The DOCX and PDF variants are preserved for human review and publication workflows. Hashes and file sizes are recorded in [the source register](data/source-register.json).

## Why This Is A Separate Wiki

The Challenge 2 corpus wiki in `challenge-2/wiki/` is generated from the synthetic dark-data source corpus and is used for benchmark evaluation. The public postmortem wiki explains the human and Codex collaboration history. This MCP research wiki is different: it is a forward-looking engineering research and implementation space for the server that will expose the corpus wiki safely to AI clients.

Keeping those scopes separate follows the LLM Wiki pattern: each wiki has a clear source boundary, purpose, index, and operating contract.

## Current Direction

Build a purpose-built read-only Wiki MCP server rather than forking a broad Obsidian, MediaWiki, or Wiki.js server. Use the candidate projects as references, preserve their licenses, and keep the first implementation narrow:

- expose only generated wiki notes, metadata, and source-register data;
- deny benchmark and gold-answer artifacts;
- return deterministic citations to wiki paths and source IDs;
- log source access for audit;
- support local stdio and Microsoft-compatible Streamable HTTP;
- add reference implementations or MCP specifications as submodules only after license review.

## Related Source Notes

- [Karpathy LLM Wiki methodology](sources/karpathy-llm-wiki-methodology.md)
- [MCP specification sources](sources/mcp-specification.md)
- [GitHub candidate projects](sources/github-candidates.md)
- [Microsoft Copilot MCP sources](sources/microsoft-copilot-mcp.md)
- [Academic literature](sources/academic-literature.md)
