---
type: interface
title: GOV.UK CKAN viewer UI design
description: Three-panel interaction design, accessibility standard, and screenshot checklist for the GOV.UK CKAN viewer.
timestamp: "2026-07-01T08:13:32Z"
---

# GOV.UK CKAN Viewer UI Design

## Three-panel Standard

The left panel reduces the corpus through search and folded facets. Facets are derived from source structure: publisher, publisher family, format, licence, tag, update year, URL host, GOV.UK-linked status, and resource type. Facets start folded; opening one facet folds the previous inactive facet while selected values remain visible as compact chips.

The centre canvas never defaults to a hairball. `#overview` opens with a screen-sized bundle info-card. Dataset, publisher, resource-stack, timeline, matrix, and Graph views are available after selection or filtering. Graph relationships lazy-load in batches when Graph is opened so the full corpus can still open on the overview quickly. Graph view includes a colour key, visible relationship list, grouped edge labels for selected-item graphs, drag-to-pan, zoom controls, clickable concept nodes for facets such as format, tag, host, and licence, and bounded label placement so dense publisher graphs stay readable.

The right panel is a scannable data card for the selected dataset, resource, or publisher. It exposes metadata, CKAN extras, source links, related records, provenance, a copyable route, pin controls, local normalized JSON, and package-shaped static bundle JSON. Live CKAN `package_show` JSON is attempted opportunistically, but the static JSON remains available when browser CORS or offline use blocks the live API fetch.

Single-click and double-click are deliberately separated. A single click inspects an item without rebuilding the current canvas: dataset/resource/publisher nodes update the right data card, while concept nodes open and highlight the relevant left facet. A double click navigates: records become the graph centre and concept nodes apply their facet reduction. Empty graph-background double click folds or shows both side panels, and each panel has its own window-style fold control.

Resource review is a first-class path. The Resource stack view renders resource rows directly, dataset cards expose resource rows, single click highlights the resource and updates the data card, and the in-app back button clears the current inspection before using browser history.

The top bar renders the generated OKF Markdown notes in-app and includes a light/dark theme toggle stored in local browser state.

## Hover, Touch, And Accessibility

All hover behaviour is backed by one `spotlight` state. Pointer hover, keyboard focus, Enter, Space, and touch tap all activate the same state. Escape clears it. The viewer announces spotlight changes through an aria-live region, and every visual hover action has a button equivalent.

## Comparison

Pinned cards are stored locally and can be spread from a compact stack into a comparison strip. The comparison strip is intentionally below the canvas controls so it does not cover graph relationships.

## Screenshot Examples

The checked-in screenshot examples cover the viewer states that matter most:

![Overview info-card](assets/ui-examples/overview.png)

The overview route opens at `viewer.html#overview` and presents counts, top publishers, dominant formats, and caveats before any graph is shown.

![Selected dataset graph/card](assets/ui-examples/dataset.png)

The selected dataset route uses `mode=force` to show a reduced publisher/dataset relationship graph with the selected data card visible on the right.

![Resource stack](assets/ui-examples/resource-stack.png)

The resource stack route uses the same active reduction model as the graph views, but renders scannable dataset rows as a step before deeper exploration.

![Pinned comparison spread](assets/ui-examples/comparison.png)

Pinned items can be kept as a compact stack or spread into a comparison strip. The screenshot restores pins from URL state for deterministic documentation; normal use persists pins in localStorage.

![Mobile/touch layout](assets/ui-examples/mobile.png)

The mobile route stacks the panels and preserves touch access to the same spotlight state used by pointer hover and keyboard focus.
