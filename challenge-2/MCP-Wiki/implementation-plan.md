---
title: "Wiki MCP Server Implementation Plan"
note_type: "plan"
tags:
  - "implementation"
  - "mcp"
  - "plan"
---

# Wiki MCP Server Implementation Plan

## Decision

Create the research wiki first, then implement the server inside this folder structure. The wiki now carries the research report, candidate matrix, source and license registers, architecture, and future implementation notes. That avoids a loose plan document and keeps the implementation traceable from the start.

## Target Implementation

The first implementation should be purpose-built for the generated Challenge 2 wiki:

- Python and FastMCP unless later research proves a better fit.
- Read-only by default.
- Local stdio for development and MCP Inspector.
- Streamable HTTP for Microsoft Copilot Studio and remote clients.
- Explicit allowlist for `challenge-2/wiki`, `challenge-2/wiki/data`, and `challenge-2/AGENTS.md`.
- Explicit denylist for `evaluation-benchmark.md`, `challenge-2/evaluation/`, and generated run artifacts.
- Deterministic citations to wiki-relative paths and source IDs.
- Append-only audit logging for source access.

## Phase 1: Research Wiki And Registers

- Preserve the Deep Research report in Markdown, DOCX, and PDF.
- Add source and candidate registers.
- Record license posture for all external candidates and specifications.
- Define update policy for submodules and snapshots.

## Phase 2: Minimal Local MCP Server

- Add a server package under `implementation/`.
- Implement `search_wiki`, `read_note`, `list_sources`, `read_source_register`, and `find_by_source_id`.
- Add traversal, symlink, extension, size, and denylist tests.
- Validate with the MCP Inspector over stdio.

## Phase 3: Provenance And Context Packs

- Add `build_context_pack` and `explain_provenance`.
- Return structured evidence objects with note path, source ID, title, snippet, and offsets where practical.
- Add tests proving benchmark artifacts never surface.

## Phase 4: Streamable HTTP

- Mount the same core server behind a Streamable HTTP endpoint.
- Add authentication, origin validation, rate limits, and response-size controls.
- Validate against a local HTTP MCP client before trying Copilot Studio.

## Phase 5: Microsoft Copilot Studio Validation

- Connect the HTTP MCP endpoint to Copilot Studio.
- Validate which parts of MCP are consumed by the Microsoft host: tools, resources, prompts, or tools only.
- Run Q001 and a small representative smoke set against the Challenge 2 wiki.

## Phase 6: Reference Implementations

Only after the first implementation shape is stable, decide whether to add reference implementations as git submodules under `references/external/`. Do this for study and comparison, not as production dependencies, unless a later decision record says otherwise.
