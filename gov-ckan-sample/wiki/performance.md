---
type: performance-guidance
title: GOV.UK CKAN large-corpus performance model
description: Startup, hydration, graph, and publication guidance for the large GOV.UK CKAN OKF bundle.
timestamp: "2026-07-01T08:13:32Z"
---

# GOV.UK CKAN Large-Corpus Performance Model

This is the largest OKF-style data source in the repository, so it deliberately uses the large-corpus path rather than the smaller single-bundle viewer pattern.

## Current Scale

- Datasets: `200`
- Resources: `16271`
- Publishers: `9`
- Relationships: `81730`
- Chunked data manifest: [`../data/manifest.json`](../data/manifest.json)
- Lightweight overview index: [`../data/overview.json`](../data/overview.json)
- Static search manifest: [`../data/search/manifest.json`](../data/search/manifest.json)
- Generated overview analysis: [`../data/analysis/overview.json`](../data/analysis/overview.json)
- Large-corpus descriptor: [`../okf-explorer.json`](../okf-explorer.json)
- Canonical topics: `Business And Economy, Consultation, Education, Environment, Finance, Geospatial, Housing, Planning, Public Health, Transport, Unclassified`

## Startup Budget

The default `#overview` route must be overview-first. It should load only:

- `viewer.html`
- `data/manifest.json`
- `data/overview.json`

Search loads the static search manifest plus lexicon, postings, and result-doc chunks. It must not hydrate the full dataset/resource/publisher indexes. Those full indexes are intentionally deferred until a user applies full-record filters, opens a detail route, or enters a non-overview view that needs full records. Relationship chunks are deferred again until Graph mode is opened.

The generic OKF Explorer may also load `data/analysis/overview.json` before full hydration. That file contains generated aggregate context for overview Graph, Links, Timeline, Facets/Dimensions, Resources, Narrative views, controlled topics, quality overview, and provenance-aware hierarchy definitions. It is additive to the startup `data/overview.json`; the legacy static viewer keeps the minimal startup path.

The generated overview payload budget is `524288` bytes. Keep `data/overview.json` small enough to be cache-friendly and safe for slow public networks.

## Design Rules

- Do not publish the full GOV.UK CKAN corpus as a single `okf-bundle.json`.
- Keep the root `gov-ckan/index.html` as the browser entry point and `okf-explorer.json` as the machine-readable large-corpus descriptor.
- Keep `data/search/manifest.json` as the first search entrypoint; search implementations should resolve postings and compact result docs from there.
- Keep `data/analysis/overview.json` as the generated overview-context entrypoint for the generic OKF Explorer.
- Keep routes hash-addressable: `#overview`, `#dataset/<package-name>`, `#resource/<resource-id>`, and `#publisher/<organization-name>`.
- Keep heavy views opt-in. Graph mode may load relationship chunks; overview must not.
- Keep list views reduced. Render bounded slices of the visible corpus rather than thousands of DOM nodes.
- Store derived metadata, canonical concept identifiers, relationships, facets, quality/provenance signals, and source links. Do not commit downloaded resource bodies.
- Treat enrichment fields as a viewer contract. If `concept_id`, canonical licence/format fields, controlled topics, quality metrics, provenance, publisher authority records, or explicit relationship kinds change, update `wiki/index.md`, `wiki/data-source-report.md`, this performance note, top-level tracking docs, checker coverage, and Explorer-facing documentation together.

## Validation

Run these checks after CKAN bundle or viewer changes:

```sh
python3 -m unittest tests.test_gov_ckan_bundle
python3 scripts/check_gov_ckan_bundle.py
python3 scripts/check_gov_ckan_performance.py
python3 scripts/check_okf_conformance.py
python3 scripts/build_site.py
```

For browser validation, serve the repo over HTTP and open `gov-ckan/index.html`; direct `file://` opens can block `fetch`.
