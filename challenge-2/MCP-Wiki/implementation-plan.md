---
title: "Wiki MCP Server Implementation Plan"
note_type: "plan"
tags:
  - "implementation"
  - "mcp"
  - "plan"
search_terms:
  - "Wiki MCP implementation plan"
  - "FastMCP Challenge 2"
  - "MCP context pack"
  - "Copilot Studio Streamable HTTP"
related:
  - "architecture.md"
  - "security-model.md"
  - "authentication-options.md"
  - "semantic-retrieval-options.md"
  - "candidate-register.md"
  - "sources/bibliography.md"
---

# Wiki MCP Server Implementation Plan

## Decision

Create the research wiki first, then implement the server inside this folder structure. The wiki now carries the research report, candidate matrix, source and license registers, architecture, and future implementation notes. That avoids a loose plan document and keeps the implementation traceable from the start.

The plan is grounded in [the architecture](architecture.md), [the security model](security-model.md), [the candidate register](candidate-register.md), and [the linked research report](<research/Challenge 2 Wiki MCP Server Research Report - linked.md>).

## Target Implementation

The first implementation is purpose-built for the generated Challenge 2 wiki:

- Python with a dependency-light JSON-RPC MCP surface so stdio and local HTTP share the same tested core.
- Read-only by default.
- Local stdio for development, Codex, and MCP Inspector-style clients.
- Local Streamable HTTP-compatible JSON-RPC endpoint for Microsoft Copilot Studio and remote-host validation.
- OAuth 2.0 or Microsoft Entra ID / SSO for the target remote authentication pattern.
- Explicit allowlist for `challenge-2/wiki`, `challenge-2/wiki/data`, and `challenge-2/AGENTS.md`.
- Explicit denylist for `evaluation-benchmark.md`, `challenge-2/evaluation/`, and generated run artifacts.
- Deterministic citations to wiki-relative paths and source IDs.
- Append-only audit logging for source access.
- Semantic retrieval behind deterministic provenance objects and bounded context packs.
- Copilot Studio direct MCP connection as the first Microsoft host validation path.
- No API-key authentication unless direct live validation proves a host-specific need.

## Phase 1: Research Wiki And Registers

- Preserve the Deep Research report in Markdown, DOCX, and PDF.
- Maintain a linked Markdown derivative and [bibliography](sources/bibliography.md).
- Add source and candidate registers.
- Record license posture for all external candidates and specifications.
- Define update policy for submodules and snapshots.
- Keep [the optimization log](wiki-optimization-log.md) and [lint report](lint-report.md) current when navigation or metadata changes.
- Add first-use reference implementation submodules under [external references](references/external/README.md), each with a local `SOURCE.md`.

## Phase 2: Minimal Local MCP Server

- Status: complete.
- Added a server package under `implementation/wiki_mcp/`.
- Implemented `wiki.search`, `wiki.read`, `wiki.list_sources`, `wiki.read_source`, `wiki.source_register`, `wiki.read_source_register`, and `wiki.find_by_source_id`.
- Added traversal, symlink, extension, size, denylist, stdio, and HTTP tests.
- Validated with Codex over stdio.

## Phase 3: Provenance And Context Packs

- Status: complete.
- Add `build_context_pack` and `explain_provenance`.
- Return structured evidence objects with note path, source ID, title, snippet, and offsets where practical.
- Add tests proving benchmark artifacts never surface.

## Phase 4: Semantic Retrieval

- Status: implemented with deterministic local hashing for the current validation loop; embedding model lock remains open pending benchmark.
- Add semantic retrieval in v1 after lexical search and provenance tests are stable.
- Keep semantic scoring behind the same `search_wiki` and `build_context_pack` tool contracts.
- Evaluate [semantic retrieval options](semantic-retrieval-options.md), starting with local `BAAI/bge-small-en-v1.5` embeddings, exact NumPy cosine search, and `all-MiniLM-L6-v2` / `e5-small-v2` comparison runs.
- Record embedding model, vector index, chunking strategy, source note path, source IDs, and generated index hash.
- Ensure semantic matches cannot surface benchmark or gold-answer artifacts.

## Phase 5: Streamable HTTP

- Status: local endpoint implemented; Copilot Studio live validation remains next.
- Mount the same core server behind a Streamable HTTP endpoint.
- Add authentication, origin validation, rate limits, and response-size controls.
- Validate against a local HTTP MCP client before trying Copilot Studio.

## Phase 6: Microsoft Copilot Studio Validation

- Status: not yet live-validated.
- Connect the HTTP MCP endpoint to Copilot Studio.
- Validate which parts of MCP are consumed by the Microsoft host: tools, resources, prompts, or tools only.
- Stay with direct MCP connection unless it cannot expose the required tool/resource surface or governance controls.
- Run Q001 and a small representative smoke set against the Challenge 2 wiki.

## Phase 7: Reference Implementations

The first-use reference implementation submodules are now added under [references/external](references/external/README.md). Use them for study and comparison, not as production dependencies, unless a later decision record says otherwise.

## Related

- [Architecture](architecture.md)
- [Security model](security-model.md)
- [Authentication options](authentication-options.md)
- [Semantic retrieval options](semantic-retrieval-options.md)
- [Implementation workspace](implementation/README.md)
- [Specifications workspace](specifications/README.md)
- [Decision record](decision-record.md)
