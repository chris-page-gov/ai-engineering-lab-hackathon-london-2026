---
title: "MCP Wiki Implementation"
note_type: "implementation-workspace"
status: "implemented"
tags:
  - "mcp"
  - "implementation"
  - "json-rpc"
  - "stdio"
  - "streamable-http"
  - "workspace"
search_terms:
  - "MCP server implementation workspace"
  - "Challenge 2 Wiki MCP implementation"
  - "Challenge 2 Wiki MCP code"
  - "Codex MCP evaluation client"
related:
  - "../implementation-plan.md"
  - "../architecture.md"
  - "../security-model.md"
  - "../references/README.md"
---

# Implementation

This folder contains the first read-only Challenge 2 Wiki MCP server implementation.

Implemented surfaces:

- `wiki_mcp/`: dependency-light Python package for the knowledge base, retrieval, JSON-RPC MCP handlers, stdio transport, and local HTTP transport.
- `../../tools/wiki_mcp_server.py`: CLI entry point for stdio and HTTP modes.
- `../../tools/compare_wiki_eval.py`: comparison report generator for DSAP evaluation runs.
- `../../evaluation/clients.py`: includes the `codex-mcp` evaluation client that configures Codex with the local stdio MCP server.

Implemented tools:

- `wiki.search`
- `wiki.read`
- `wiki.list_sources`
- `wiki.read_source`
- `wiki.source_register`
- `wiki.read_source_register`
- `wiki.find_by_source_id`
- `wiki.build_context_pack`
- `wiki.explain_provenance`
- `wiki.audit_summary`

Implemented resources:

- `wiki://index`
- `wiki://source-register`
- `wiki://agents`
- `wiki://semantic-manifest`
- `wiki://source/<SOURCE_ID>`

Implemented prompt:

- `wiki.answer_question`

## Security Posture

The server exposes only `challenge-2/wiki/`, `challenge-2/wiki/data/`, and `challenge-2/AGENTS.md`. It denies `challenge-2/wiki/evaluation-benchmark.md`, evaluation harness directories, generated run artifacts, local state, symlinks, unsupported extensions, oversized files, and raw Challenge 2 source directories. Every allowed and denied access can be recorded to an append-only JSONL audit file.

Semantic retrieval is available through a deterministic local exact-cosine hashing backend for the current validation loop. The production embedding model remains unpinned until the shortlisted permissive local models are benchmarked.

## Codex Validation

The `codex-mcp` evaluation client configures Codex with the local stdio server and requires live MCP tool validation before answering. Noninteractive Codex otherwise cancels MCP tool calls, so the harness uses Codex's approval-bypass mode for this client only. The MCP server remains read-only and path-scoped.

## Validation

Current validation includes:

- `python3 -m unittest tests.test_challenge2_wiki_mcp_server`
- `uv run --with coverage python -m coverage run --source=challenge-2/MCP-Wiki/implementation/wiki_mcp -m unittest tests.test_challenge2_wiki_mcp_server`
- `uv run --with coverage python -m coverage report`
- Coverage result: `91%` across the MCP implementation package.
- Live Q001 smoke for `codex-mcp`, with recorded `wiki.search` and `wiki.read` MCP audit events.
- Full Challenge 2 wiki evaluation report: `../../evaluation/reports/validated-full-20260419T2225Z-comparison.md`.
- Effective `codex-mcp` coverage: `100/100` benchmark questions after a correction rerun for the single base-run Q057 timeout.

## Related

- [Implementation plan](../implementation-plan.md)
- [Architecture](../architecture.md)
- [Security model](../security-model.md)
- [Specifications workspace](../specifications/README.md)
