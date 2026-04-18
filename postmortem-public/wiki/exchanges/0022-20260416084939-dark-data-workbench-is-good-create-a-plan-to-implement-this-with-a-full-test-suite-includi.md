---
exchange_id: "EX-0022"
title: "Dark Data Workbench is good, create a plan to implement this with a full test suite including pl"
source_id: "CONV-002"
global_sequence: 22
session_sequence: 20
user_timestamp: "2026-04-16T12:06:52.509Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0022. Dark Data Workbench is good, create a plan to implement this with a full test suite including pl

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-002 (Karpathy Wiki Planning and Challenge 2 Vault Build)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Dark Data Workbench is good, create a plan to implement this with a full test suite including playwright, at least as good as SeeLinks one. Coverage target is >90% but make this coverage test optional so we can easily test features without the coverage failure each time
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-16T12:07:07.010Z`

````text
I’ll ground this against both repos before locking the implementation plan: current Challenge 2 has the wiki/output model, and SeeLinks has the interaction and test patterns we can match or exceed.
````

### Response 2 (commentary)

- Timestamp: `2026-04-16T12:07:16.350Z`

````text
The hackathon repo does not currently have a frontend package or Playwright setup; SeeLinks does. I’m checking the source-register shape and SeeLinks’ UI tests next so the plan includes concrete data interfaces and realistic test depth.
````

### Response 3 (commentary)

- Timestamp: `2026-04-16T12:07:25.097Z`

````text
I’ve confirmed the Challenge repo has the wiki data and Python evaluation pieces but no frontend/test harness yet, while SeeLinks already has SvelteKit plus Vitest and Playwright patterns. Two choices materially affect the implementation plan, so I’m going to lock those before writing the final plan.
````

### Response 4 (final_answer)

- Timestamp: `2026-04-16T12:11:10.526Z`

````text
<proposed_plan>
# Dark Data Workbench Implementation Plan

## Summary

Build **Dark Data Workbench** as a self-contained SvelteKit app inside the Challenge 2 repo. It will let users browse the generated Obsidian/wiki corpus with or without AI: deterministic search/filter/context-building first, then optional browser-AI export and local MCP access to the same selected evidence set.

The v1 implementation will not require a model API. It will preserve synthetic data as-is, keep raw Challenge 2 source files read-only, and make the workbench prominent from the Obsidian knowledge base index.

## Key Changes

- Add a new app at `challenge-2/workbench/` using SvelteKit, TypeScript, Vite, Vitest, and Playwright.
- Load corpus data from `challenge-2/wiki/data/source-register.json` and generated wiki notes, then normalize it into:
  - `WorkbenchCorpus`
  - `WorkbenchSource`
  - `WorkbenchTopic`
  - `WorkbenchEntity`
  - `ContextExport`
- Implement a three-panel UI:
  - Left: maps, filters, facets, saved context sets.
  - Centre: source grid, reader, graph, timeline/table views.
  - Right: current context set, evidence details, AI/no-AI mode controls.
- Add mode switch:
  - **No AI:** deterministic search, filters, saved demo queries, evidence bundles, provenance.
  - **Browser AI:** copy/download current context as JSON/Markdown plus a safe prompt.
  - **MCP:** show local MCP setup and expose corpus/context tools for desktop AI clients.
- Include saved no-AI checks for the demo questions:
  - Current Council Tax Reduction guidance.
  - Self-employed Housing Benefit eligibility.
  - Draft/stale/past-review staff policies.
  - IT hardware approvals over GBP 5,000.
  - Documents mentioning Discretionary Housing Payments.
- Add `challenge-2/tools/workbench_mcp.py` exposing:
  - `resources/list`
  - `resources/read`
  - `tools/list`
  - `workbench.search_sources`
  - `workbench.read_source`
  - `workbench.build_context`
- Add `challenge-2/wiki/workbench.md` and link it prominently from `challenge-2/wiki/index.md` and `challenge-2/wiki/architecture.md`.
- Update `Changelog.md`, `Context.md`, and `Progress.md` in lockstep with the repo documentation policy.

## Public Interfaces

- `GET /api/corpus.json`
  - Returns normalized corpus metadata, source summaries, filter facets, topic/entity links, and lint flags.
- `ContextExport`
  - Includes export timestamp, corpus metadata, synthetic-data notice, active filters, selected source IDs, source summaries, provenance, flags, and extracted excerpts.
- Browser AI actions:
  - `Copy AI context`
  - `Download AI context JSON`
  - `Copy browser-AI prompt`
  - `Download evidence bundle Markdown`
- MCP tools:
  - `workbench.search_sources({ query, filters, limit })`
  - `workbench.read_source({ source_id, include_note, max_bytes })`
  - `workbench.build_context({ source_ids, query, filters })`
- Default local commands:
  - `cd challenge-2/workbench && pnpm dev`
  - `cd challenge-2/workbench && pnpm test`
  - `cd challenge-2/workbench && pnpm test:ui`
  - `cd challenge-2/workbench && pnpm test:coverage`

## Test Plan

- Unit tests with Vitest:
  - Corpus loader reads all 43 sources.
  - Facets/counts match the source register.
  - Search matches titles, source IDs, topics, departments, flags, and note text.
  - Saved demo queries return the expected source IDs.
  - Context export includes selected/highlighted flags, provenance, synthetic-data notice, and no redactions.
  - Browser-AI prompt requires answers from supplied context and cited source IDs.
  - MCP request handlers list, search, read, and build context without exposing raw files outside Challenge 2.
- Component tests:
  - Filter panel state.
  - Source card flags.
  - Context basket add/remove/clear/save.
  - Mode switch behavior.
  - Evidence panel rendering.
- Playwright tests at least matching SeeLinks coverage depth:
  - App loads and shows `43 sources`.
  - Search by `DOC-HB-002` narrows to one source.
  - Topic/status/department filters update grid counts.
  - Add selected sources to context, save a context set, reopen it.
  - Reader opens a source note with metadata, provenance, flags, and raw-source link.
  - No-AI saved query answers the five demo questions with source-backed results.
  - Browser AI export copies/downloads valid JSON with selected source IDs.
  - MCP panel shows correct local command and available tools.
  - Graph/table views render useful content, including procurement threshold table access.
  - Mobile viewport smoke test verifies the panels collapse without overlapping controls.
- Coverage:
  - Add optional `pnpm test:coverage`.
  - Enforce >90% lines/statements/functions/branches for workbench source logic and component-testable code.
  - Do not run coverage in the default `pnpm test`, Playwright run, or normal CI path, so feature testing is not blocked by coverage during rapid iteration.
- CI:
  - Add a normal workbench test workflow for install, typecheck, unit tests, build, and Playwright.
  - Keep coverage as a manually run script or separate optional workflow/job.

## Assumptions

- V1 lives in the Challenge repo under `challenge-2/workbench/`.
- V1 supports **Export + MCP**, with no in-app model API dependency.
- Raw files under `challenge-2/structured_files/` and `challenge-2/unstructured_files/` remain immutable.
- Synthetic staff/contact-like data is retained and labelled as synthetic fixture data, not redacted.
- The UI is optimized for demo clarity, provenance, and current-context questioning rather than a polished chat product.
- Playwright runs Chromium by default, with one mobile viewport smoke test for responsive coverage.
</proposed_plan>
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.
