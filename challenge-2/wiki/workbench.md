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
updated: "2026-05-12"
---

# Dark Data Workbench

Dark Data Workbench is the browser interface for the Challenge 2 knowledge base. It sits alongside the Obsidian vault and uses the generated source register and wiki notes as its data source.

The workbench is designed around the same useful pattern as SeeLinks: state the question, filter the visible material, explicitly build a context set, inspect the evidence, and then choose whether to use AI.

## How To Run

From the repository root:

```bash
cd challenge-2/workbench
pnpm install
pnpm dev
```

Open the local URL printed by Vite. The default Playwright/dev port is `5174`.

## Main Modes

- **No AI:** use the question box, search, dynamic facets, source cards, order-by stack, grid/outline/graph/timeline views, reader view, workbook table view, saved context sets, local collections, and deterministic demo checks.
- **Reader:** source notes open as rendered Markdown preview by default, with a Text toggle for exact Markdown/frontmatter inspection and a local source-note endpoint for opening the Markdown directly.
- **Browser AI:** copy or download the current context as JSON, copy a browser-AI prompt, or download a Markdown evidence bundle. The export includes the current question.
- **MCP:** run `python3 challenge-2/tools/workbench_mcp.py` so desktop AI clients can search, read, and build context from the same source set.

## SeeLinks-Style Controls

The workbench now mirrors the key SeeLinks/Micropedia control surfaces inside this repo:

- resizable left rail, dataset/import status, Order by stack, metadata toggle, facet open/pin/reorder controls, value ordering, Links, Collections, Printing, AI export, Tile Text, and browser-only Editing panels;
- click/right-click/double-click facet-value workflows for filter/mark, adjusted highlight sets, and view reductions;
- Choose highlighted, Choose unhighlighted, Undo view, Reset, history chips, drag-facet-to-grid colouring, and drag-value-to-grid rollups;
- a docked grid detail panel with tile strip, previous/next/close, Overview/Images tabs, source links, thumbnails, and metadata.

Collections are stored in browser IndexedDB through Dexie. Per-pack UI preferences are stored in `localStorage`. Editing operates only on the in-browser working copy and does not write Challenge 2 raw sources, HMRC narrative files, or generated pack JSON.

The parity matrix is [SeeLinks Micropedia parity matrix](../../research/hmrc-beyond-hype/narrative/notes/seelinks-micropedia-parity-matrix.md).

## Question Box

The question box records the user need before source selection. Typed questions are included in Browser AI JSON, browser prompts, and Markdown evidence bundles. Running a saved check fills the question box with that check's demo question so the exported context shows both the evidence and the question it was assembled to answer.

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
