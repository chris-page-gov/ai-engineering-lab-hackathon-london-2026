---
type: data-readme
title: GOV.UK CKAN data source report
description: Source, coverage, and extraction boundary report for the GOV.UK CKAN bundle.
timestamp: "2026-07-01T08:13:32Z"
---

# GOV.UK CKAN Data Source Report

## Extraction Boundary

The builder calls the unauthenticated CKAN API under `https://data.gov.uk/api/action`. It harvests `package_search` pages, normalises dataset and resource metadata, derives facets and graph relationships, and stores compact JSON chunks under `gov-ckan/data/`.

Remote resource bodies are not downloaded. URLs are retained as source links. Raw full API responses are intentionally not committed. The intended concept-localisation path is to analyse linked resources efficiently and persist derived concepts, evidence pointers, and relationship summaries, not copies of the original documents.

## Coverage

- Bundle mode: `sample`
- Harvested datasets: `200`
- Harvested resources: `16271`
- Publishers: `9`
- GOV.UK content records enriched: `3`
- Enrichment limit: `200`

## Caveats

- The CKAN directory contains records of mixed quality, age, and link health.
- Publisher records are canonical authority concepts keyed by CKAN organization name.
- Licence and format values are canonicalised while source values are preserved as `license_source_*` and `source_format`.
- Quality scores are deterministic metadata heuristics, not a substitute for checking resource contents.
- GOV.UK Content API enrichment is metadata-only and stores no rendered GOV.UK body HTML.
- The current bundle is metadata-first. Document-content concept extraction is a follow-on enrichment layer and should keep the no-copied-documents boundary.
