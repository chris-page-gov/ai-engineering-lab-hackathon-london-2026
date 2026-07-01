---
okf_version: "0.1"
type: index
title: GOV.UK CKAN OKF Bundle
description: Metadata-first OKF bundle over the National Data Library CKAN directory.
timestamp: "2026-07-01T08:13:32Z"
---

# GOV.UK CKAN OKF Bundle

This bundle localises public metadata from the National Data Library directory into a static OKF-style corpus. It keeps dataset and resource metadata, source links, publisher information, facets, and graph relationships, but it does not download remote data files.

## Current Build

- CKAN API base: `https://data.gov.uk/api/action`
- Datasets harvested into this bundle: `200`
- Resources indexed: `16271`
- Publishers indexed: `9`
- Relationships indexed: `50052`
- Full CKAN dataset count reported by the API at harvest time: `58461`
- Viewer: [Open the static viewer](../viewer.html#overview)

## Source Boundaries

The CKAN directory is the spine. GOV.UK content metadata is included only when a dataset or resource URL points exactly to `www.gov.uk` content and the public Content API returns metadata.

Localising means preserving the conceptual framework that can be derived from the corpus: datasets, resources, publishers, tags, formats, licences, hosts, source links, exact GOV.UK content metadata, and graph relationships. It does not mean committing copies of remote documents or downloaded resource bodies. Future concept extraction should store derived concepts, provenance, and links back to the source resources rather than source-document copies.

## Official Source Anchors

- [data.gov.uk API documentation](https://guidance.data.gov.uk/get_data/api_documentation/)
- [Accepted CKAN fields](https://guidance.data.gov.uk/publish_and_manage_data/harvest_or_add_data/harvest_data/ckan/)
- [GOV.UK Content API docs](https://content-api.publishing.service.gov.uk/getting-started.html)
- [GOV.UK Content API reference](https://content-api.publishing.service.gov.uk/reference.html)
- [GOV.UK Search API docs](https://docs.publishing.service.gov.uk/repos/search-api.html)
