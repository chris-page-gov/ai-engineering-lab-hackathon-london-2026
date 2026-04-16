---
title: "Dark Data Workbench"
aliases:
  - "Challenge 2 Workbench"
  - "Knowledge Explorer"
note_type: "interface"
tags:
  - "challenge-2"
  - "dark-data-workbench"
  - "start-here"
updated: "2026-04-16"
---

# Dark Data Workbench

Dark Data Workbench is the browser interface for the Challenge 2 knowledge base. It sits alongside the Obsidian vault and uses the generated source register and wiki notes as its data source.

The workbench is designed around the same useful pattern as SeeLinks: filter the visible material, explicitly build a context set, inspect the evidence, and then choose whether to use AI.

## How To Run

From the repository root:

```bash
cd challenge-2/workbench
pnpm install
pnpm dev
```

Open the local URL printed by Vite. The default Playwright/dev port is `5174`.

## Main Modes

- **No AI:** use search, facets, source cards, reader view, graph view, workbook table view, saved context sets, and deterministic demo checks.
- **Browser AI:** copy or download the current context as JSON, copy a browser-AI prompt, or download a Markdown evidence bundle.
- **MCP:** run `python3 challenge-2/tools/workbench_mcp.py` so desktop AI clients can search, read, and build context from the same source set.

## What It Uses

- [Source register](data/source-register.json)
- [Source notes](sources/doc-hb-001-housing-benefit-check-if-you-re-eligible-gov-uk.md)
- [Lint report](lint-report.md)
- [Architecture overview](architecture.md)

## Validation

The workbench includes unit, component, MCP, and Playwright tests:

```bash
cd challenge-2/workbench
pnpm test
pnpm test:ui
pnpm build
pnpm test:coverage
```

Coverage enforcement is intentionally optional through `pnpm test:coverage` so feature tests can run quickly during iteration.
