---
type: data-readme
title: GOV.UK CKAN data source report
description: Source, coverage, and extraction boundary report for the GOV.UK CKAN bundle.
timestamp: "2026-07-01T14:55:30Z"
---

# GOV.UK CKAN Data Source Report

## Extraction Boundary

The builder calls the unauthenticated CKAN API under `https://data.gov.uk/api/action`. It harvests `package_search` pages, normalises dataset and resource metadata, derives facets and graph relationships, and stores compact JSON chunks under `gov-ckan/data/`.

Remote resource bodies are not downloaded. URLs are retained as source links. Raw full API responses are intentionally not committed. The intended concept-localisation path is to analyse linked resources efficiently and persist derived concepts, evidence pointers, and relationship summaries, not copies of the original documents.

## Coverage

- Bundle mode: `full`
- Harvested datasets: `58461`
- Harvested resources: `268241`
- Publishers: `1185`
- GOV.UK content records enriched: `200`
- Enrichment limit: `200`

## Derived Record Model

The committed bundle is a derived metadata model, not a mirror of CKAN JSON. The builder preserves CKAN identifiers and source URLs, then adds stable OKF concept paths, publisher authority references, canonical licence and format values, controlled topics, explicit relationship types, quality scores, and provenance. Source values remain available where normalisation occurs, for example `license_source_id`, `license_source_title`, and `source_format`.

The generated relationship model is intentionally richer than `published by`. It includes publisher authority, licence, download resource, classified-as topic/tag, temporal coverage, resource host, format, and GOV.UK content relationships where the metadata supports them. These are metadata-derived relationship assertions; they should not be treated as proof that remote resource contents were downloaded or inspected.

Regeneration lockstep is part of the source boundary. If the enrichment vocabulary, quality metrics, provenance shape, or relationship kinds change, update the builder, generated wiki notes, checker assertions, tests, and top-level repository documentation in the same pull request.

## Caveats

- The CKAN directory contains records of mixed quality, age, and link health.
- Publisher records are canonical authority concepts keyed by CKAN organization name.
- Licence and format values are canonicalised while source values are preserved as `license_source_*` and `source_format`.
- Quality scores are deterministic metadata heuristics, not a substitute for checking resource contents.
- GOV.UK Content API enrichment is metadata-only and stores no rendered GOV.UK body HTML.
- The current bundle is metadata-first. Document-content concept extraction is a follow-on enrichment layer and should keep the no-copied-documents boundary.
