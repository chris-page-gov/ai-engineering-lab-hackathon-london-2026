---
okf_version: "0.1"
type: index
title: GOV.UK CKAN stratified evaluation bundle
description: Metadata-first OKF bundle over the National Data Library CKAN directory.
timestamp: "2026-07-13T11:30:00Z"
---

# GOV.UK CKAN stratified evaluation bundle

This bundle localises public metadata from the National Data Library directory into a static OKF-style corpus. It keeps dataset and resource metadata, source links, canonical publisher concepts, facets, quality/provenance signals, and graph relationships, but it does not download remote data files.

This repository preserves the historical development path from the original dark-data challenge into the GOV.UK CKAN large-corpus fixture. The generic OKF Explorer product, bundle conventions, and reusable Svelte viewer now live in [`ai-infrastructure-wiki`](https://github.com/chris-page-gov/ai-infrastructure-wiki). This CKAN bundle remains the largest fixture used to prove that generic Explorer at scale.

## Current Build

- CKAN API base: `https://data.gov.uk/api/action`
- Datasets harvested into this bundle: `300`
- Resources indexed: `747`
- Publishers indexed: `86`
- Relationships indexed: `6079`
- Builder version: `gov-ckan-builder-v2`
- Enrichment version: `gov-ckan-enrichment-v1`
- Transformation pipeline version: `gov-ckan-pipeline-v2`
- Full CKAN dataset count reported by the API at harvest time: `58461`
- Large-corpus entry point: [Open the OKF Explorer](../index.html)
- Viewer: [Open the static viewer](../viewer.html#overview)
- Performance guidance: [Large-corpus performance model](performance.md)

## Generated Enrichment Contract

The generated JSON records carry an additive enrichment contract for generic OKF Explorer consumers. The contract is generated from CKAN metadata and checked by `scripts/check_gov_ckan_bundle.py`.

| Area | Generated fields | Notes |
| --- | --- | --- |
| Stable concepts | `concept_id`, `route`, `publisher_concept_id`, `dataset_concept_id` | Datasets use `datasets/<publisher>/<package>.md`, publishers use `publishers/<publisher>.md`, and resources use `resources/<package>/<position>-<resource>.md` as logical OKF concept paths. |
| Canonical values | `license_id`, `license_source_id`, `format`, `source_format`, confidence fields | Common licence and format spelling variants collapse to controlled values while preserving source values for audit. |
| Publisher authority | publisher chunk records, `publisher authority` relationships | Each CKAN organization becomes one publisher concept; datasets reference the authority concept instead of duplicating publisher metadata. |
| Controlled topics | `controlled_topics`, `topic_confidence` | Topics are deterministic metadata classifications used for overview and facet discovery, not asserted semantic truth. |
| Explicit relationships | `published by`, `publisher authority`, `licence`, `download resource`, `classified as`, `temporal coverage`, plus format/tag/host/resource links | Relationship chunks keep graph exploration lazy while making the relationship type explicit for agents and viewers. |
| Quality signals | `quality.overall`, `quality.metrics` | Scores cover metadata completeness, licence confidence, update recency, resource availability, API/resource signals, and format confidence. Download success remains `null` because resource bodies are not fetched. |
| Provenance | `provenance.ckan_package_id`, `harvest_timestamp`, `source_url`, `generation_timestamp`, `enrichment_version`, `transformation_pipeline_version` | Every dataset/resource/publisher carries enough source and pipeline metadata to make regenerated bundles comparable. |

Changing any of these fields is a bundle-contract change. Update this generated note, the top-level tracking docs, the checker, and the generic Explorer documentation together.

## Source Boundaries

The CKAN directory is the spine. GOV.UK content metadata is included only when a dataset or resource URL points exactly to `www.gov.uk` content and the public Content API returns metadata.

Localising means preserving the conceptual framework that can be derived from the corpus: datasets, resources, publisher authority records, controlled topics, canonical formats/licences, tags, hosts, source links, exact GOV.UK content metadata, quality metrics, provenance, and graph relationships. Dataset records include stable logical concept identifiers such as `datasets/<publisher>/<package>.md`; publisher authority records use `publishers/<publisher>.md`; resources use `resources/<package>/<position>-<resource>.md`. These identifiers are logical OKF concept paths inside the large-corpus JSON model rather than thousands of generated Markdown stub files.

The normalisation layer collapses common licence variants such as `not specified`, `not-specified`, and `notspecified`, and maps OGL variants such as `uk-ogl`, `OGL-UK-3.0`, and `ogl` to the `uk-ogl` canonical value. Resource formats are similarly canonicalised so variants such as `CSV`, `.csv`, and `text/csv` resolve to `CSV`.

The enrichment layer adds controlled topics, richer relationship types, and deterministic quality metrics. Quality scores are metadata heuristics covering completeness, licence confidence, update recency, resource URL/state presence, API/resource-format signals, and format confidence. The static generator intentionally does not download resource bodies, so download success is recorded as not checked rather than inferred.

It does not mean committing copies of remote documents or downloaded resource bodies. Future concept extraction should store derived concepts, provenance, and links back to the source resources rather than source-document copies.

## Official Source Anchors

- [data.gov.uk API documentation](https://guidance.data.gov.uk/get_data/api_documentation/)
- [Accepted CKAN fields](https://guidance.data.gov.uk/publish_and_manage_data/harvest_or_add_data/harvest_data/ckan/)
- [GOV.UK Content API docs](https://content-api.publishing.service.gov.uk/getting-started.html)
- [GOV.UK Content API reference](https://content-api.publishing.service.gov.uk/reference.html)
- [GOV.UK Search API docs](https://docs.publishing.service.gov.uk/repos/search-api.html)
