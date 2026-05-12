---
tags:
  - seelinks
  - micropedia
  - dark-data-workbench
  - ui-parity
publication_status: "published parity matrix for the HMRC workbench UI pass"
---

# SeeLinks Micropedia Parity Matrix

This note compares the running SeeLinks Micropedia UI with the Dark Data Workbench implementation in `challenge-2/workbench`. The target is not a copy of the Micropedia app; it is SeeLinks-style behaviour adapted to the Challenge 2 and HMRC narrative packs while keeping raw source data immutable.

| SeeLinks / Micropedia surface | Dark Data Workbench behaviour | Status |
| --- | --- | --- |
| Resizable left rail | Left control rail width is adjustable and persisted per pack. | Implemented |
| Dataset picker and import controls | Challenge 2/HMRC pack switchers refresh route data; JSON/JSONL import control is present with a local-only status message. | Implemented; file ingestion remains browser-local/config-state only |
| Intro/status messages | Pack/import/print/export status messages are surfaced in the relevant panels and toolbar. | Implemented |
| Order by rail | Multi-facet sort stack, direction toggle, drag/drop facet add, per-value include/exclude legend, and per-pack persistence. | Implemented |
| Metadata toggle | Metadata facets are hidden by default and can be shown from the facet rail. | Implemented |
| Facet open/pin/reorder | Facets default folded; clicking opens one facet and folds inactive unpinned siblings; selected/highlighted facets and pinned facets remain open; facet headers support pin/unpin and drag-reorder. | Implemented |
| Facet value ordering | Values can be auto-ordered, cleared, and drag-reordered. | Implemented |
| Click/right-click/double-click values | Click filters and marks, right-click adjusts highlight values, double-click reduces through the highlighted set. | Implemented, with Challenge 2 click-filter compatibility retained |
| Highlight reductions | Choose highlighted, Choose unhighlighted, Undo view, Reset, and history chips reduce or restore the current view. | Implemented |
| Drag facet to grid | Dropping a facet header onto the grid colours cards by that facet. | Implemented |
| Drag value to grid | Dropping a facet value onto the grid creates a rollup card and applies the related colour legend. | Implemented |
| Links panel | Summarises current-view facet links and lets users mark linked values. | Implemented |
| Collections panel | Save/open/analyse local collections as first-class source sets. | Implemented with Dexie/IndexedDB |
| Printing panel | Print selected records or the current visible set. | Implemented |
| AI export panel | Copy/download AI context from the current view, selected set, active reductions, sort stack, collection name, and highlight filters. | Implemented |
| Tile Text panel | Choose card title/subtitle fields and toggle the small ID badge. | Implemented |
| Editing panel | Apply browser-only working-copy topic/flag/source-family edits to selected cards. | Implemented; no source or generated pack files are written |
| Grid view | Source cards, thumbnails, state badges, colour reasons, rollups, selection, mark, and open actions. | Implemented |
| Outline view | Current view grouped by the active sort/legend facet or first visible facet. | Implemented |
| Graph view | Topic/source graph remains available for Challenge 2 and HMRC packs. | Implemented |
| Timeline view | Current view grouped by narrative stage, talk section, or available date. | Implemented |
| Reading view | Source metadata, links, image, Markdown Preview/Text toggle, and direct note link. | Implemented |
| Table view | Workbook/Markdown table inspection remains available. | Implemented |
| Checks view | Deterministic saved checks remain available for Challenge 2. | Implemented |
| Docked detail panel | Grid detail dock has tile strip, Previous/Next/Close, Overview/Images tabs, links, thumbnails, and metadata. | Implemented |
| Image/gallery metadata | Sources can carry thumbnail and gallery metadata; detail Images tab renders available images. | Implemented |
| Pack graph/meta/extensions | Workbench types now carry dynamic properties, pack metadata, graph nodes/edges, category path, tile subtitle, collections, and gallery metadata. | Implemented |
| MCP/API external-service panels | External MCP/API service loading is represented as configuration/local-only state when no endpoint is configured. | Documented unavailable unless service is configured |

## Regression Contract

- Challenge 2 raw and generated source data remains immutable.
- HMRC narrative pack loading still uses `/?pack=hmrc-narrative`.
- Existing Browser AI and MCP exports remain backwards-compatible, with added view-reduction, sort-stack, collection, and highlight metadata.
- Local collections and UI preferences are browser state: Dexie for collections and `localStorage` for per-pack UI preferences.
- Playwright coverage exercises pack switching, Markdown Preview/Text, folded-by-default facet accordion behaviour, active/pinned facet retention, double-click value reduction, order-by controls, metadata toggle, facet pin/order, highlight reductions, rollups, collections, detail tabs/links, tile text, graph/table/checks, and mobile layout.
