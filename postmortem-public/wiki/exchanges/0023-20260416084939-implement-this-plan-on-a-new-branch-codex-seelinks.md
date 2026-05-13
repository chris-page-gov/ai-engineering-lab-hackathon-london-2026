---
exchange_id: "EX-0023"
title: "Implement this plan on a new branch codex/SeeLinks"
source_id: "CONV-002"
global_sequence: 23
session_sequence: 21
user_timestamp: "2026-04-16T12:35:14.997Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0023. Implement this plan on a new branch codex/SeeLinks

Previous: [EX-0022](0022-20260416084939-dark-data-workbench-is-good-create-a-plan-to-implement-this-with-a-full-test-suite-includi.md) | Conversation reader: [start-to-finish](../readers/conv-002-karpathy-wiki-planning-and-challenge-2-vault-build.md) | Next: [EX-0024](0024-20260416084939-implement-karpathy-wiki-vault.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-002 (Karpathy Wiki Planning and Challenge 2 Vault Build)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Implement this plan on a new branch codex/SeeLinks
````

## Codex Response

### Response 1 (final_answer)

- Timestamp: `2026-04-16T12:35:33.347Z`

````text
<proposed_plan>
# Dark Data Workbench Execution Plan On `codex/SeeLinks`

## Summary

Implement the approved **Dark Data Workbench** plan on a new branch named `codex/SeeLinks`. The branch will add a self-contained SvelteKit workbench under `challenge-2/workbench/`, expose optional browser-AI and MCP context flows, and add a test suite with Playwright coverage at least comparable to SeeLinks. Coverage enforcement will be available through an explicit optional command, not the default test path.

## Key Changes

- Create branch `codex/SeeLinks` from the current fork-local working branch after preserving unrelated local work.
- Add `challenge-2/workbench/` with SvelteKit, TypeScript, Vite, Vitest, Playwright, and static build support.
- Build a corpus loader that reads `challenge-2/wiki/data/source-register.json` and generated wiki notes, then exposes normalized source, topic, entity, flag, and provenance data to the UI.
- Implement the three-panel workbench:
  - Left: maps, facets, saved context sets.
  - Centre: source grid, reader, graph, table, and saved-query results.
  - Right: context basket, evidence panel, and `No AI / Browser AI / MCP` mode switch.
- Implement Browser AI export:
  - Copy JSON context.
  - Download JSON context.
  - Copy browser-AI prompt.
  - Download Markdown evidence bundle.
- Implement local MCP support with `challenge-2/tools/workbench_mcp.py`:
  - list resources
  - read source/wiki files within allowed Challenge 2 paths
  - search sources
  - build context exports
- Add `challenge-2/wiki/workbench.md` and link it prominently from `wiki/index.md` and `wiki/architecture.md`.
- Update `Changelog.md`, `Context.md`, and `Progress.md` in lockstep.

## Test Plan

- Add Vitest unit tests for:
  - corpus normalization
  - source counts and facets
  - search
  - saved demo queries
  - context export shape
  - synthetic-data notice preservation
  - prompt generation
  - MCP handler behavior
- Add component tests for:
  - source cards
  - filter panel
  - context basket
  - mode switch
  - evidence panel
- Add Playwright tests for:
  - app loads and displays all 43 sources
  - search by source ID narrows results
  - department/topic/status filters update counts
  - context add/remove/save/reopen flow
  - reader opens metadata, provenance, and raw-source links
  - five no-AI saved demo questions return source-backed evidence
  - Browser AI export produces valid JSON with selected source IDs
  - MCP panel renders local setup and tool list
  - graph/table views render
  - mobile viewport does not overlap controls
- Add scripts:
  - `pnpm test` for normal unit/component tests
  - `pnpm test:ui` for Playwright
  - `pnpm build` for production build
  - `pnpm test:coverage` for optional >90% coverage enforcement
- CI should run install, typecheck, unit tests, build, and Playwright. Coverage remains manual or optional.

## Assumptions

- The implementation branch is exactly `codex/SeeLinks`.
- The app lives in the Challenge repo, not the private SeeLinks repo.
- SeeLinks is used as the interaction reference, but code is only copied if licensing and repo ownership make that acceptable.
- Raw Challenge 2 sources remain unchanged.
- Synthetic staff/contact-like data remains visible and labelled as synthetic, with no redaction.
- No runtime model API is added in v1.
</proposed_plan>
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.

Previous: [EX-0022](0022-20260416084939-dark-data-workbench-is-good-create-a-plan-to-implement-this-with-a-full-test-suite-includi.md) | Conversation reader: [start-to-finish](../readers/conv-002-karpathy-wiki-planning-and-challenge-2-vault-build.md) | Next: [EX-0024](0024-20260416084939-implement-karpathy-wiki-vault.md)
