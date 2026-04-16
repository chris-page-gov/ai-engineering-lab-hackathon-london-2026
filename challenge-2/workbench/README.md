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
- **Browser AI:** copy/download JSON context, copy a browser prompt, or download Markdown evidence. Exports include the current question box text.
- **MCP:** run `python3 ../tools/workbench_mcp.py` from this directory or `python3 challenge-2/tools/workbench_mcp.py` from the repository root.
