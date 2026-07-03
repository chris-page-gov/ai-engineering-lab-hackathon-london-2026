---
type: performance-guidance
title: GOV.UK CKAN large-corpus performance model
description: Startup, hydration, graph, and publication guidance for the large GOV.UK CKAN OKF bundle.
timestamp: "2026-07-01T14:55:30Z"
---

# GOV.UK CKAN Large-Corpus Performance Model

This is the largest OKF-style data source in the repository, so it deliberately uses the large-corpus path rather than the smaller single-bundle viewer pattern.

## Current Scale

- Datasets: `58461`
- Resources: `268241`
- Publishers: `1185`
- Relationships: `1178122`
- Chunked data manifest: [`../data/manifest.json`](../data/manifest.json)
- Lightweight overview index: [`../data/overview.json`](../data/overview.json)
- Large-corpus descriptor: [`../okf-explorer.json`](../okf-explorer.json)

## Startup Budget

The default `#overview` route must be overview-first. It should load only:

- `viewer.html`
- `data/manifest.json`
- `data/overview.json`

The full dataset/resource/publisher indexes are intentionally deferred until a user searches, filters, opens a detail route, or enters a non-overview view. Relationship chunks are deferred again until Graph mode is opened.

The generated overview payload budget is `524288` bytes. Keep `data/overview.json` small enough to be cache-friendly and safe for slow public networks.

## Design Rules

- Do not publish the full GOV.UK CKAN corpus as a single `okf-bundle.json`.
- Keep the root `gov-ckan/index.html` as the browser entry point and `okf-explorer.json` as the machine-readable large-corpus descriptor.
- Keep routes hash-addressable: `#overview`, `#dataset/<package-name>`, `#resource/<resource-id>`, and `#publisher/<organization-name>`.
- Keep heavy views opt-in. Graph mode may load relationship chunks; overview must not.
- Keep list views reduced. Render bounded slices of the visible corpus rather than thousands of DOM nodes.
- Store derived metadata, relationships, facets, and source links. Do not commit downloaded resource bodies.

## Validation

Run these checks after CKAN bundle or viewer changes:

```sh
python3 scripts/check_gov_ckan_bundle.py
python3 scripts/check_gov_ckan_performance.py
python3 scripts/check_okf_conformance.py
python3 scripts/build_site.py
```

For browser validation, serve the repo over HTTP and open `gov-ckan/index.html`; direct `file://` opens can block `fetch`.
