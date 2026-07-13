---
type: data-readme
title: GOV.UK CKAN data source report
description: Source, coverage, and extraction boundary report for the GOV.UK CKAN bundle.
timestamp: "2026-07-13T11:30:00Z"
---

# GOV.UK CKAN stratified evaluation bundle Data Source Report

## Extraction Boundary

The evaluation builder selects normalized records deterministically from the committed full CKAN bundle, then rebuilds facets, search indexes, analysis, and relationships for the selected reduction. It does not make network requests or download remote resource bodies. The selection rationale is published in `data/evaluation-selection.json`.

Remote resource bodies are not downloaded. URLs are retained as source links. Raw full API responses are intentionally not committed. The intended concept-localisation path is to analyse linked resources efficiently and persist derived concepts, evidence pointers, and relationship summaries, not copies of the original documents.

## Coverage

- Bundle mode: `stratified-evaluation`
- Harvested datasets: `300`
- Harvested resources: `747`
- Publishers: `86`
- GOV.UK content records enriched: `3`
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
