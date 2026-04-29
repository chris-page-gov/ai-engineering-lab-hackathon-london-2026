# Dark Data Workbench

Browser interface for the Challenge 2 Obsidian/wiki corpus. It loads `../wiki/data/source-register.json` plus generated source notes, then lets users enter the question they need to answer, filter documents, build a context set, inspect evidence, and optionally export that same context for browser AI or MCP clients.

## Commands

```bash
pnpm install
pnpm dev
pnpm check
pnpm test
pnpm build
pnpm test:ui
pnpm test:coverage
```

`pnpm test:coverage` enforces the >90% coverage target. It is intentionally separate from the default test command.

## AI Modes

- **No AI:** deterministic search, facets, saved checks, reader, graph, workbook table view, and evidence bundles.
- **Reader:** open rendered note text in the workbench or via the local `/api/source-note/<source-id>` Markdown endpoint.
- **Browser AI:** copy/download JSON context, copy a browser prompt, or download Markdown evidence. Exports include the current question box text and selected sources even when filters or search terms currently hide them.
- **MCP:** run `python3 ../tools/workbench_mcp.py` from this directory or `python3 challenge-2/tools/workbench_mcp.py` from the repository root.
