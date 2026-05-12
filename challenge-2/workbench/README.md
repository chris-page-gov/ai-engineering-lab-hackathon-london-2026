# Dark Data Workbench

Browser interface for the Challenge 2 Obsidian/wiki corpus. It loads `../wiki/data/source-register.json` plus generated source notes, then lets users enter the question they need to answer, filter documents, build a context set, inspect evidence, preview rendered Markdown notes or raw note text, and optionally export that same context for browser AI or MCP clients.

The same app can also load the HMRC Beyond the Hype narrative datapack:

```text
/?pack=hmrc-narrative
```

That pack is generated at `../../research/hmrc-beyond-hype/narrative/seelinks/pack.json` and presents the talk narrative as slide-thumbnail source cards, narrative notes, transcripts, Challenge 2 evidence, and conversation traces.

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
- **Reader:** open source notes as rendered Markdown preview by default, switch to raw Text when exact Markdown/frontmatter matters, or open the local `/api/source-note/<source-id>` Markdown endpoint.
- **Browser AI:** copy/download JSON context, copy a browser prompt, or download Markdown evidence. Exports include the current question box text and selected sources even when filters or search terms currently hide them.
- **MCP:** run `python3 ../tools/workbench_mcp.py` from this directory or `python3 challenge-2/tools/workbench_mcp.py` from the repository root.

## Narrative Pack Controls

The HMRC narrative pack uses bounded facets for source family, narrative stage, talk section, asset type, evidence role, governance theme, topic group, provenance mode, screenfulls, and tags. Source cards can be marked, narrowed with **Keep marked**, removed with **Dismiss marked**, and restored with **Restore**.

The header pack buttons switch between the Challenge 2 corpus and the HMRC narrative pack through SvelteKit route data, so the URL and visible corpus stay in sync without a manual browser reload.

Facet headings are draggable. Drag a facet name such as `Talk Section` onto the card grid to colour the visible cards by that facet. Category facets use high-contrast pastel fills; the `Screenfulls` measure uses a graded colour scale.
