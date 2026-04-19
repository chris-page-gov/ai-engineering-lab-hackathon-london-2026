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
  - "candidate-register.md"
  - "sources/bibliography.md"
---

# Wiki MCP Server Implementation Plan

## Decision

Create the research wiki first, then implement the server inside this folder structure. The wiki now carries the research report, candidate matrix, source and license registers, architecture, and future implementation notes. That avoids a loose plan document and keeps the implementation traceable from the start.

The plan is grounded in [the architecture](architecture.md), [the security model](security-model.md), [the candidate register](candidate-register.md), and [the linked research report](<research/Challenge 2 Wiki MCP Server Research Report - linked.md>).

## Target Implementation

The first implementation should be purpose-built for the generated Challenge 2 wiki:

- Python and FastMCP unless later research proves a better fit.
- Read-only by default.
- Local stdio for development and MCP Inspector.
- Streamable HTTP for Microsoft Copilot Studio and remote clients.
- OAuth 2.0 or Microsoft Entra ID / SSO for the target remote authentication pattern.
- Explicit allowlist for `challenge-2/wiki`, `challenge-2/wiki/data`, and `challenge-2/AGENTS.md`.
- Explicit denylist for `evaluation-benchmark.md`, `challenge-2/evaluation/`, and generated run artifacts.
- Deterministic citations to wiki-relative paths and source IDs.
- Append-only audit logging for source access.
- Semantic retrieval in v1, behind deterministic provenance objects and bounded context packs.

## Phase 1: Research Wiki And Registers

- Preserve the Deep Research report in Markdown, DOCX, and PDF.
- Maintain a linked Markdown derivative and [bibliography](sources/bibliography.md).
- Add source and candidate registers.
- Record license posture for all external candidates and specifications.
- Define update policy for submodules and snapshots.
- Keep [the optimization log](wiki-optimization-log.md) and [lint report](lint-report.md) current when navigation or metadata changes.
- Add first-use reference implementation submodules under [external references](references/external/README.md), each with a local `SOURCE.md`.

## Phase 2: Minimal Local MCP Server

- Add a server package under `implementation/`.
- Implement `search_wiki`, `read_note`, `list_sources`, `read_source_register`, and `find_by_source_id`.
- Add traversal, symlink, extension, size, and denylist tests.
- Validate with the MCP Inspector over stdio.

## Phase 3: Provenance And Context Packs

- Add `build_context_pack` and `explain_provenance`.
- Return structured evidence objects with note path, source ID, title, snippet, and offsets where practical.
- Add tests proving benchmark artifacts never surface.

## Phase 4: Semantic Retrieval

- Add semantic retrieval in v1 after lexical search and provenance tests are stable.
- Keep semantic scoring behind the same `search_wiki` and `build_context_pack` tool contracts.
- Record embedding model, vector index, chunking strategy, source note path, source IDs, and generated index hash.
- Ensure semantic matches cannot surface benchmark or gold-answer artifacts.

## Phase 5: Streamable HTTP

- Mount the same core server behind a Streamable HTTP endpoint.
- Add authentication, origin validation, rate limits, and response-size controls.
- Validate against a local HTTP MCP client before trying Copilot Studio.

## Phase 6: Microsoft Copilot Studio Validation

- Connect the HTTP MCP endpoint to Copilot Studio.
- Validate which parts of MCP are consumed by the Microsoft host: tools, resources, prompts, or tools only.
- Run Q001 and a small representative smoke set against the Challenge 2 wiki.

## Phase 7: Reference Implementations

The first-use reference implementation submodules are now added under [references/external](references/external/README.md). Use them for study and comparison, not as production dependencies, unless a later decision record says otherwise.

## Related

- [Architecture](architecture.md)
- [Security model](security-model.md)
- [Authentication options](authentication-options.md)
- [Implementation workspace](implementation/README.md)
- [Specifications workspace](specifications/README.md)
- [Decision record](decision-record.md)
