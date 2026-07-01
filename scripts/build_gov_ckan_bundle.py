#!/usr/bin/env python3
"""Build a metadata-first GOV.UK/data.gov.uk CKAN OKF bundle."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from html import escape
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "gov-ckan"
DEFAULT_API_BASE = "https://data.gov.uk/api/action"
VIEWER_VERSION = "gov-ckan-viewer-v1"
BUILDER_VERSION = "gov-ckan-builder-v1"
DEFAULT_ROWS = 1000
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_ENRICH_LIMIT = 200
LOCAL_PATH_RE = re.compile(r"(/Users/|/private/|/tmp/|[A-Za-z]:\\\\)")


@dataclass(frozen=True)
class HarvestConfig:
    api_base: str = DEFAULT_API_BASE
    sample: int | None = None
    rows: int = DEFAULT_ROWS
    chunk_size: int = DEFAULT_CHUNK_SIZE
    enrich_govuk_limit: int = DEFAULT_ENRICH_LIMIT
    generated_at: str = ""


def slug(value: str, fallback: str = "item") -> str:
    text = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return text or fallback


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact_text(value: Any, limit: int = 900) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) <= limit:
        return text
    return f"{text[: limit - 3].rstrip()}..."


def clean_value(value: Any) -> Any:
    if isinstance(value, str):
        return compact_text(value, 1600)
    if isinstance(value, list):
        return [clean_value(item) for item in value]
    if isinstance(value, dict):
        return {str(k): clean_value(v) for k, v in sorted(value.items()) if v not in (None, "", [], {})}
    return value


def extras_to_dict(extras: Any) -> dict[str, str]:
    result: dict[str, str] = {}
    if not isinstance(extras, list):
        return result
    for item in extras:
        if not isinstance(item, dict):
            continue
        key = str(item.get("key") or "").strip()
        if not key:
            continue
        result[key] = compact_text(item.get("value"), 900)
    return result


def host_for_url(url: str) -> str:
    parsed = urlparse(str(url or "").strip())
    return parsed.netloc.lower().removeprefix("www.")


def govuk_content_path_for_url(url: str) -> str | None:
    parsed = urlparse(str(url or "").strip())
    host = parsed.netloc.lower()
    if host not in {"www.gov.uk", "gov.uk"}:
        return None
    path = parsed.path.strip("/")
    if not path or path.startswith(("api/", "assets/", "government/uploads/")):
        return None
    return path


def stable_timestamp(package: dict[str, Any], extras: dict[str, str]) -> str:
    for key in ("dcat_modified", "modified", "metadata_modified", "dcat_issued", "issued", "metadata_created"):
        value = extras.get(key) or package.get(key)
        if value:
            return str(value)
    return ""


def normalize_resource(resource: dict[str, Any], dataset_name: str) -> dict[str, Any]:
    url = str(resource.get("url") or "").strip()
    resource_id = str(resource.get("id") or slug(f"{dataset_name}-{resource.get('position', 0)}", "resource"))
    govuk_path = govuk_content_path_for_url(url)
    return {
        "id": resource_id,
        "dataset": dataset_name,
        "name": compact_text(resource.get("name") or resource.get("description") or resource_id, 220),
        "description": compact_text(resource.get("description"), 500),
        "url": url,
        "host": host_for_url(url),
        "format": compact_text(resource.get("format") or resource.get("mimetype") or "unknown", 120),
        "resource_type": compact_text(resource.get("resource_type") or "unknown", 80),
        "schema_url": compact_text(resource.get("schema_url"), 360),
        "schema_type": compact_text(resource.get("schema_type"), 120),
        "position": int(resource.get("position") or 0),
        "created": str(resource.get("created") or ""),
        "last_modified": str(resource.get("last_modified") or ""),
        "metadata_modified": str(resource.get("metadata_modified") or ""),
        "size": resource.get("size"),
        "hash": compact_text(resource.get("hash"), 160),
        "state": compact_text(resource.get("state") or "unknown", 80),
        "govuk_content_path": govuk_path or "",
    }


def normalize_publisher(org: dict[str, Any]) -> dict[str, Any]:
    name = str(org.get("name") or org.get("id") or "unknown").strip()
    return {
        "id": str(org.get("id") or name),
        "name": name,
        "title": compact_text(org.get("title") or name.replace("-", " ").title(), 220),
        "type": compact_text(org.get("type") or "organization", 80),
        "description": compact_text(org.get("description"), 700),
        "state": compact_text(org.get("state") or "unknown", 80),
        "approval_status": compact_text(org.get("approval_status") or "", 80),
        "dataset_count": 0,
        "resource_count": 0,
    }


def normalize_dataset(
    package: dict[str, Any],
    api_base: str = DEFAULT_API_BASE,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    name = str(package.get("name") or package.get("id") or "").strip()
    if not name:
        name = slug(package.get("title") or package.get("id") or "dataset")
    extras = extras_to_dict(package.get("extras"))
    org = package.get("organization") if isinstance(package.get("organization"), dict) else {}
    publisher = normalize_publisher(org)
    resources = [normalize_resource(r, name) for r in package.get("resources", []) if isinstance(r, dict)]
    tags = sorted(
        {
            compact_text(tag.get("name") or tag.get("display_name"), 120)
            for tag in package.get("tags", [])
            if isinstance(tag, dict) and (tag.get("name") or tag.get("display_name"))
        }
    )
    groups = sorted(
        {
            compact_text(group.get("name") or group.get("display_name"), 120)
            for group in package.get("groups", [])
            if isinstance(group, dict) and (group.get("name") or group.get("display_name"))
        }
    )
    dataset = {
        "id": str(package.get("id") or name),
        "name": name,
        "title": compact_text(package.get("title") or name.replace("-", " ").title(), 240),
        "notes": compact_text(package.get("notes"), 900),
        "url": str(package.get("url") or ""),
        "host": host_for_url(str(package.get("url") or "")),
        "isopen": bool(package.get("isopen")),
        "license_id": compact_text(package.get("license_id") or "not-specified", 120),
        "license_title": compact_text(package.get("license_title") or package.get("license_id") or "Not specified", 180),
        "state": compact_text(package.get("state") or "unknown", 80),
        "type": compact_text(package.get("type") or "dataset", 80),
        "private": bool(package.get("private")),
        "metadata_created": str(package.get("metadata_created") or ""),
        "metadata_modified": str(package.get("metadata_modified") or ""),
        "timestamp": stable_timestamp(package, extras),
        "publisher": publisher["name"],
        "publisher_title": publisher["title"],
        "tags": tags,
        "groups": groups,
        "resource_ids": [resource["id"] for resource in resources],
        "resource_count": len(resources),
        "formats": sorted({resource["format"] for resource in resources if resource["format"]}),
        "resource_hosts": sorted({resource["host"] for resource in resources if resource["host"]}),
        "govuk_content_paths": sorted(
            {path for path in [govuk_content_path_for_url(str(package.get("url") or ""))] if path}
            | {resource["govuk_content_path"] for resource in resources if resource["govuk_content_path"]}
        ),
        "extras": extras,
        "source_api_url": f"{api_base.rstrip('/')}/package_show?id={quote(name)}",
    }
    return dataset, resources, publisher


def fetch_json(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "ai-engineering-lab-gov-ckan-builder/1.0"})
    with urlopen(request, timeout=60) as response:  # noqa: S310 - controlled public metadata URL
        return json.loads(response.read().decode("utf-8"))


def ckan_get(api_base: str, action: str, params: dict[str, Any]) -> dict[str, Any]:
    url = f"{api_base.rstrip('/')}/{action}?{urlencode(params)}"
    payload = fetch_json(url)
    if not payload.get("success"):
        raise RuntimeError(f"CKAN action {action} failed: {payload.get('error')}")
    result = payload.get("result")
    if not isinstance(result, dict):
        raise RuntimeError(f"CKAN action {action} returned unexpected result")
    return result


def iter_packages(config: HarvestConfig) -> tuple[list[dict[str, Any]], int]:
    packages: list[dict[str, Any]] = []
    total_count = 0
    start = 0
    while True:
        wanted = config.rows
        if config.sample is not None:
            remaining = config.sample - len(packages)
            if remaining <= 0:
                break
            wanted = min(wanted, remaining)
        result = ckan_get(config.api_base, "package_search", {"rows": wanted, "start": start, "sort": "metadata_modified desc"})
        total_count = int(result.get("count") or total_count)
        batch = [item for item in result.get("results", []) if isinstance(item, dict)]
        if not batch:
            break
        packages.extend(batch)
        start += len(batch)
        if config.sample is None and start >= total_count:
            break
    return packages, total_count


def classify_content_api_result(status: int, headers: dict[str, str], body: str, requested_path: str) -> dict[str, Any]:
    if status == 303:
        return {
            "path": requested_path,
            "status": 303,
            "redirect": headers.get("location") or headers.get("Location") or "",
        }
    if status in {404, 410}:
        return {"path": requested_path, "status": status}
    if status != 200:
        return {"path": requested_path, "status": status}
    data = json.loads(body)
    return {
        "path": requested_path,
        "status": 200,
        "content_id": data.get("content_id") or "",
        "base_path": data.get("base_path") or "",
        "title": compact_text(data.get("title"), 240),
        "description": compact_text(data.get("description"), 500),
        "document_type": data.get("document_type") or "",
        "schema_name": data.get("schema_name") or "",
        "public_updated_at": data.get("public_updated_at") or "",
        "web_url": f"https://www.gov.uk{data.get('base_path') or ''}",
        "link_types": sorted((data.get("links") or {}).keys()) if isinstance(data.get("links"), dict) else [],
    }


def fetch_govuk_content(path: str) -> dict[str, Any]:
    url = f"https://www.gov.uk/api/content/{quote(path)}"
    request = Request(url, headers={"User-Agent": "ai-engineering-lab-gov-ckan-builder/1.0"})
    try:
        with urlopen(request, timeout=30) as response:  # noqa: S310 - controlled public metadata URL
            body = response.read().decode("utf-8")
            return classify_content_api_result(response.status, dict(response.headers.items()), body, path)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return classify_content_api_result(exc.code, dict(exc.headers.items()), body, path)
    except (TimeoutError, URLError) as exc:
        return {"path": path, "status": "error", "error": compact_text(str(exc), 300)}


def build_relationships(
    datasets: list[dict[str, Any]],
    resources: list[dict[str, Any]],
    govuk_content: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    relationships: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    def add(source: str, target: str, kind: str) -> None:
        if not source or not target:
            return
        key = (source, target, kind)
        if key not in seen:
            relationships.append({"source": source, "target": target, "kind": kind})
            seen.add(key)

    for dataset in datasets:
        did = f"dataset/{dataset['name']}"
        add(did, f"publisher/{dataset['publisher']}", "published by")
        add(did, f"license/{dataset['license_id']}", "licensed as")
        if dataset.get("host"):
            add(did, f"host/{dataset['host']}", "landing host")
        for tag in dataset.get("tags", []):
            add(did, f"tag/{tag}", "tagged")
        for group in dataset.get("groups", []):
            add(did, f"group/{group}", "grouped")
        for fmt in dataset.get("formats", []):
            add(did, f"format/{fmt}", "has format")
        for path in dataset.get("govuk_content_paths", []):
            add(did, f"govuk/{path}", "references GOV.UK content")
    for resource in resources:
        rid = f"resource/{resource['id']}"
        add(f"dataset/{resource['dataset']}", rid, "has resource")
        add(rid, f"format/{resource['format']}", "resource format")
        if resource.get("host"):
            add(rid, f"host/{resource['host']}", "resource host")
        path = resource.get("govuk_content_path")
        if path:
            add(rid, f"govuk/{path}", "resource GOV.UK content")
    for path, content in govuk_content.items():
        if content.get("status") == 200 and content.get("content_id"):
            add(f"govuk/{path}", f"govuk-content-id/{content['content_id']}", "content id")
            if content.get("document_type"):
                add(f"govuk/{path}", f"govuk-document-type/{content['document_type']}", "document type")
    return sorted(relationships, key=lambda item: (item["source"], item["kind"], item["target"]))


def chunked(values: list[dict[str, Any]], chunk_size: int) -> list[list[dict[str, Any]]]:
    return [values[index : index + chunk_size] for index in range(0, len(values), chunk_size)]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_chunks(data_dir: Path, prefix: str, records: list[dict[str, Any]], chunk_size: int) -> list[str]:
    paths: list[str] = []
    for index, group in enumerate(chunked(records, chunk_size), start=1):
        name = f"{prefix}-{index:04d}.json"
        write_json(data_dir / name, group)
        paths.append(f"data/{name}")
    if not paths:
        name = f"{prefix}-0001.json"
        write_json(data_dir / name, [])
        paths.append(f"data/{name}")
    return paths


def clean_generated_outputs(out_dir: Path) -> None:
    data_dir = out_dir / "data"
    if data_dir.exists():
        for path in data_dir.glob("*.json"):
            path.unlink()
    for path in [
        out_dir / "viewer.html",
        out_dir / "wiki" / "index.md",
        out_dir / "wiki" / "data-source-report.md",
        out_dir / "wiki" / "ui-design.md",
    ]:
        path.unlink(missing_ok=True)
    remove_local_metadata(out_dir)


def remove_local_metadata(out_dir: Path) -> None:
    for path in out_dir.rglob(".DS_Store") if out_dir.exists() else []:
        path.unlink(missing_ok=True)


def count_by(values: list[str], limit: int = 100) -> list[dict[str, Any]]:
    counter = Counter(value or "Unknown" for value in values)
    return [{"value": key, "count": count} for key, count in counter.most_common(limit)]


def build_facets(datasets: list[dict[str, Any]], resources: list[dict[str, Any]], publishers: dict[str, dict[str, Any]]) -> dict[str, Any]:
    years = [str(item.get("timestamp", ""))[:4] for item in datasets if str(item.get("timestamp", ""))[:4].isdigit()]
    return {
        "publisher": count_by([dataset["publisher"] for dataset in datasets], 250),
        "publisher_family": count_by([publisher_family(dataset["publisher"]) for dataset in datasets], 100),
        "format": count_by([resource["format"] for resource in resources], 150),
        "license": count_by([dataset["license_id"] for dataset in datasets], 80),
        "tag": count_by([tag for dataset in datasets for tag in dataset.get("tags", [])], 250),
        "update_year": count_by(years, 80),
        "host": count_by([resource["host"] for resource in resources if resource.get("host")], 250),
        "govuk_linked": count_by(["yes" if dataset.get("govuk_content_paths") else "no" for dataset in datasets], 2),
        "resource_type": count_by([resource["resource_type"] for resource in resources], 80),
        "publisher_state": count_by([publisher.get("state", "unknown") for publisher in publishers.values()], 20),
    }


def publisher_family(publisher: str) -> str:
    if publisher.endswith("-council") or "borough-council" in publisher or "county-council" in publisher:
        return "local government"
    if "nhs" in publisher or "health" in publisher:
        return "health"
    if publisher.startswith("department-") or publisher in {"cabinet-office", "home-office", "hm-treasury"}:
        return "central government"
    if "environment" in publisher or "natural" in publisher or "geological" in publisher:
        return "environment and science"
    return "other public body"


def build_graph(
    datasets: list[dict[str, Any]],
    resources: list[dict[str, Any]],
    publishers: dict[str, dict[str, Any]],
    relationships: list[dict[str, str]],
) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    for dataset in datasets:
        nodes[f"dataset/{dataset['name']}"] = {
            "id": f"dataset/{dataset['name']}",
            "kind": "dataset",
            "label": dataset["title"],
            "count": dataset["resource_count"],
        }
    for resource in resources:
        nodes[f"resource/{resource['id']}"] = {
            "id": f"resource/{resource['id']}",
            "kind": "resource",
            "label": resource["name"],
            "format": resource["format"],
        }
    for publisher in publishers.values():
        nodes[f"publisher/{publisher['name']}"] = {
            "id": f"publisher/{publisher['name']}",
            "kind": "publisher",
            "label": publisher["title"],
            "count": publisher["dataset_count"],
        }
    return {"nodes": sorted(nodes.values(), key=lambda item: item["id"]), "edges": relationships}


def render_wiki(out_dir: Path, manifest: dict[str, Any], official_sources: list[dict[str, str]]) -> None:
    wiki = out_dir / "wiki"
    timestamp = manifest["generated_at"]
    source_rows = "\n".join(f"- [{item['title']}]({item['url']})" for item in official_sources)
    index = f"""---
okf_version: "0.1"
type: index
title: GOV.UK CKAN OKF Bundle
description: Metadata-first OKF bundle over the National Data Library CKAN directory.
timestamp: "{timestamp}"
---

# GOV.UK CKAN OKF Bundle

This bundle localises public metadata from the National Data Library directory into a static OKF-style corpus. It keeps dataset and resource metadata, source links, publisher information, facets, and graph relationships, but it does not download remote data files.

## Current Build

- CKAN API base: `{manifest['source']['api_base']}`
- Datasets harvested into this bundle: `{manifest['counts']['datasets']}`
- Resources indexed: `{manifest['counts']['resources']}`
- Publishers indexed: `{manifest['counts']['publishers']}`
- Relationships indexed: `{manifest['counts']['relationships']}`
- Full CKAN dataset count reported by the API at harvest time: `{manifest['source']['ckan_reported_count']}`
- Viewer: [Open the static viewer](../viewer.html#overview)

## Source Boundaries

The CKAN directory is the spine. GOV.UK content metadata is included only when a dataset or resource URL points exactly to `www.gov.uk` content and the public Content API returns metadata.

Localising means preserving the conceptual framework that can be derived from the corpus: datasets, resources, publishers, tags, formats, licences, hosts, source links, exact GOV.UK content metadata, and graph relationships. It does not mean committing copies of remote documents or downloaded resource bodies. Future concept extraction should store derived concepts, provenance, and links back to the source resources rather than source-document copies.

## Official Source Anchors

{source_rows}
"""
    report = f"""---
type: data-readme
title: GOV.UK CKAN data source report
description: Source, coverage, and extraction boundary report for the GOV.UK CKAN bundle.
timestamp: "{timestamp}"
---

# GOV.UK CKAN Data Source Report

## Extraction Boundary

The builder calls the unauthenticated CKAN API under `{manifest['source']['api_base']}`. It harvests `package_search` pages, normalises dataset and resource metadata, derives facets and graph relationships, and stores compact JSON chunks under `gov-ckan/data/`.

Remote resource bodies are not downloaded. URLs are retained as source links. Raw full API responses are intentionally not committed. The intended concept-localisation path is to analyse linked resources efficiently and persist derived concepts, evidence pointers, and relationship summaries, not copies of the original documents.

## Coverage

- Bundle mode: `{manifest['source']['mode']}`
- Harvested datasets: `{manifest['counts']['datasets']}`
- Harvested resources: `{manifest['counts']['resources']}`
- Publishers: `{manifest['counts']['publishers']}`
- GOV.UK content records enriched: `{manifest['counts']['govuk_content']}`
- Enrichment limit: `{manifest['source']['govuk_enrichment_limit']}`

## Caveats

- The CKAN directory contains records of mixed quality, age, and link health.
- Publisher and format names are normalised only lightly so the bundle remains faithful to source metadata.
- GOV.UK Content API enrichment is metadata-only and stores no rendered GOV.UK body HTML.
- The current sample is metadata-first. Document-content concept extraction is a follow-on enrichment layer and should keep the no-copied-documents boundary.
"""
    ui = f"""---
type: interface
title: GOV.UK CKAN viewer UI design
description: Three-panel interaction design, accessibility standard, and screenshot checklist for the GOV.UK CKAN viewer.
timestamp: "{timestamp}"
---

# GOV.UK CKAN Viewer UI Design

## Three-panel Standard

The left panel reduces the corpus through search and folded facets. Facets are derived from source structure: publisher, publisher family, format, licence, tag, update year, URL host, GOV.UK-linked status, and resource type.

The centre canvas never defaults to a hairball. `#overview` opens with a screen-sized bundle info-card. Dataset, publisher, resource-stack, timeline, matrix, and force views are available after selection or filtering.

The right panel is a scannable data card for the selected dataset, resource, or publisher. It exposes metadata, source links, related records, provenance, a copyable route, and pin controls.

## Hover, Touch, And Accessibility

All hover behaviour is backed by one `spotlight` state. Pointer hover, keyboard focus, Enter, Space, and touch tap all activate the same state. Escape clears it. The viewer announces spotlight changes through an aria-live region, and every visual hover action has a button equivalent.

## Comparison

Pinned cards are stored locally and can be spread from a compact stack into a comparison strip. The comparison strip is intentionally below the canvas controls so it does not cover graph relationships.

## Screenshot Examples

The sample bundle has deterministic screenshot examples for the viewer states that matter most:

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
"""
    (wiki / "assets" / "ui-examples").mkdir(parents=True, exist_ok=True)
    (wiki / "index.md").write_text(index, encoding="utf-8")
    (wiki / "data-source-report.md").write_text(report, encoding="utf-8")
    (wiki / "ui-design.md").write_text(ui, encoding="utf-8")


def render_viewer() -> str:
    return VIEWER_TEMPLATE.replace("__VIEWER_VERSION__", VIEWER_VERSION)


def build_bundle(config: HarvestConfig, out_dir: Path) -> dict[str, Any]:
    clean_generated_outputs(out_dir)
    packages, total_count = iter_packages(config)
    datasets: list[dict[str, Any]] = []
    resources: list[dict[str, Any]] = []
    publishers: dict[str, dict[str, Any]] = {}

    for package in packages:
        dataset, package_resources, publisher = normalize_dataset(package, config.api_base)
        datasets.append(dataset)
        resources.extend(package_resources)
        current = publishers.get(publisher["name"], publisher)
        current["dataset_count"] += 1
        current["resource_count"] += len(package_resources)
        publishers[publisher["name"]] = current

    datasets.sort(key=lambda item: item["name"])
    resources.sort(key=lambda item: (item["dataset"], item["position"], item["id"]))
    publisher_records = sorted(publishers.values(), key=lambda item: item["name"])

    govuk_paths = sorted({path for dataset in datasets for path in dataset.get("govuk_content_paths", [])})
    govuk_content: dict[str, dict[str, Any]] = {}
    for path in govuk_paths[: config.enrich_govuk_limit]:
        govuk_content[path] = fetch_govuk_content(path)

    relationships = build_relationships(datasets, resources, govuk_content)
    facets = build_facets(datasets, resources, publishers)
    graph = build_graph(datasets, resources, publishers, relationships)
    generated_at = config.generated_at or now_iso()

    data_dir = out_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    chunks = {
        "datasets": write_chunks(data_dir, "datasets", datasets, config.chunk_size),
        "resources": write_chunks(data_dir, "resources", resources, config.chunk_size),
        "publishers": write_chunks(data_dir, "publishers", publisher_records, config.chunk_size),
        "relationships": write_chunks(data_dir, "relationships", relationships, config.chunk_size),
    }
    write_json(data_dir / "facets.json", facets)
    write_json(data_dir / "graph.json", graph)
    write_json(data_dir / "govuk-content.json", govuk_content)

    official_sources = [
        {
            "title": "data.gov.uk API documentation",
            "url": "https://guidance.data.gov.uk/get_data/api_documentation/",
        },
        {
            "title": "Accepted CKAN fields",
            "url": "https://guidance.data.gov.uk/publish_and_manage_data/harvest_or_add_data/harvest_data/ckan/",
        },
        {
            "title": "GOV.UK Content API docs",
            "url": "https://content-api.publishing.service.gov.uk/getting-started.html",
        },
        {
            "title": "GOV.UK Content API reference",
            "url": "https://content-api.publishing.service.gov.uk/reference.html",
        },
        {
            "title": "GOV.UK Search API docs",
            "url": "https://docs.publishing.service.gov.uk/repos/search-api.html",
        },
    ]
    manifest = {
        "title": "GOV.UK CKAN OKF Bundle",
        "generated_at": generated_at,
        "generated_by": "scripts/build_gov_ckan_bundle.py",
        "builder_version": BUILDER_VERSION,
        "viewer_version": VIEWER_VERSION,
        "source": {
            "api_base": config.api_base,
            "mode": "sample" if config.sample is not None else "full",
            "sample": config.sample,
            "ckan_reported_count": total_count,
            "govuk_enrichment_limit": config.enrich_govuk_limit,
        },
        "counts": {
            "datasets": len(datasets),
            "resources": len(resources),
            "publishers": len(publisher_records),
            "relationships": len(relationships),
            "govuk_content": len(govuk_content),
        },
        "chunks": chunks,
        "indexes": {
            "facets": "data/facets.json",
            "graph": "data/graph.json",
            "govuk_content": "data/govuk-content.json",
        },
        "official_sources": official_sources,
        "routes": ["#overview", "#dataset/<package-name>", "#resource/<resource-id>", "#publisher/<organization-name>"],
        "commit_policy": "metadata-first; remote resource bodies are not downloaded",
    }
    write_json(data_dir / "manifest.json", manifest)
    render_wiki(out_dir, manifest, official_sources)
    (out_dir / "viewer.html").write_text(render_viewer(), encoding="utf-8")
    remove_local_metadata(out_dir)
    return manifest


VIEWER_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GOV.UK CKAN OKF Viewer</title>
<style>
:root{color-scheme:light;--bg:#f5f7fa;--ink:#101820;--muted:#5d6b78;--panel:#fff;--line:#d7dee8;--line2:#bbc7d6;--blue:#1d70b8;--green:#00703c;--yellow:#ffdd00;--red:#d4351c;--card:#eef3f8}
*{box-sizing:border-box}html,body{height:100%;margin:0}body{font:14px/1.45 Arial,sans-serif;background:var(--bg);color:var(--ink);overflow:hidden}.app{height:100dvh;display:grid;grid-template-rows:auto 1fr;min-width:0}.top{display:flex;gap:12px;align-items:center;padding:12px 16px;background:#0b0c0c;color:#fff}.top h1{font-size:19px;margin:0}.top small{color:#d5dee7}.top a{color:#fff}.shell{min-height:0;display:grid;grid-template-columns:minmax(280px,350px) minmax(420px,1fr) minmax(360px,480px)}aside,.stage{min-height:0;overflow:hidden}.left,.right{background:var(--panel);border-right:1px solid var(--line);display:flex;flex-direction:column}.right{border-right:0;border-left:1px solid var(--line)}.scroll{overflow:auto;min-height:0;padding:14px}.search{display:grid;gap:8px;padding:14px;border-bottom:1px solid var(--line)}input,select,button{font:inherit}input[type=search]{width:100%;padding:10px;border:2px solid var(--line2);border-radius:4px}.facet{border-bottom:1px solid var(--line);padding:10px 14px}.facet h2{font-size:13px;margin:0 0 8px;display:flex;justify-content:space-between}.facet button,.pill,.mode button,.action{border:1px solid var(--line2);background:#fff;color:var(--ink);border-radius:4px;padding:6px 8px;cursor:pointer}.facet button{margin:0 4px 5px 0;font-size:12px}.facet button.active,.mode button.active,.action.primary{background:var(--blue);border-color:var(--blue);color:#fff}.stage{position:relative;background:linear-gradient(180deg,#e9f1f8,#f8fafc);display:grid;grid-template-rows:auto 1fr auto}.mode{display:flex;gap:7px;align-items:center;padding:10px 12px;border-bottom:1px solid var(--line);background:rgba(255,255,255,.92);z-index:2}.canvas{min-height:0;overflow:auto;position:relative;padding:18px}.overview{max-width:980px;margin:0 auto;display:grid;gap:14px}.hero{background:#0b0c0c;color:#fff;padding:22px;border-radius:6px}.hero h2{font-size:30px;margin:0 0 8px}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.metric,.card{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px}.metric strong{display:block;font-size:24px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}.list{display:grid;gap:8px}.row{border:1px solid var(--line);background:#fff;border-radius:6px;padding:10px;text-align:left;cursor:pointer}.row:hover,.row.spotlight{outline:3px solid #ffdd00}.row h3{font-size:15px;margin:0 0 4px}.meta{color:var(--muted);font-size:12px}.graph{width:100%;height:100%;min-height:520px}.node{cursor:pointer}.node circle{stroke:#fff;stroke-width:2}.node text{font-size:11px;paint-order:stroke;stroke:#fff;stroke-width:4px}.edge{stroke:#8da0b4;stroke-width:1.2;opacity:.55}.edge.spotlight{stroke:var(--blue);stroke-width:3;opacity:1}.detail h2{font-size:24px;margin:0 0 8px}.kv{display:grid;grid-template-columns:120px minmax(0,1fr);gap:5px;border-top:1px solid var(--line);padding-top:10px;margin-top:10px}.kv dt{font-weight:700}.kv dd{margin:0;word-break:break-word}.chips{display:flex;gap:5px;flex-wrap:wrap}.chip{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:3px 8px;font-size:12px}.pins{border-top:1px solid var(--line);padding:10px 12px;background:#fff}.pinStack{display:flex;gap:6px;flex-wrap:wrap}.pin{border:1px solid var(--line2);background:#fff;border-radius:5px;padding:6px 8px;max-width:220px}.pin.spread{min-width:220px}.sr{position:absolute;left:-9999px}.notice{border-left:5px solid var(--yellow);background:#fff8cc;padding:10px;margin:10px 0}.resourceList{display:grid;gap:6px}.resourceList button{text-align:left}.hidden{display:none}@media(max-width:1050px){body{overflow:auto}.app{height:auto}.shell{display:block}.left,.right{max-height:none}.stage{height:72vh}.metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>
</head>
<body>
<div class="app">
<header class="top"><div><h1>GOV.UK CKAN OKF Viewer</h1><small id="subtitle">Loading bundle metadata</small></div><a href="wiki/index.md">OKF bundle notes</a></header>
<main class="shell">
<aside class="left"><div class="search"><input id="query" type="search" placeholder="Search datasets, resources, publishers, tags"><button class="action" id="clearFilters">Clear filters</button></div><div id="facets" class="scroll"></div></aside>
<section class="stage"><div class="mode"><button data-mode="overview" class="active">Overview</button><button data-mode="force">Force</button><button data-mode="timeline">Timeline</button><button data-mode="matrix">Publisher x Format</button><button data-mode="resources">Resource stack</button><span class="meta" id="count"></span></div><div class="canvas" id="canvas"></div><div class="pins"><button class="action" id="spreadPins">Spread pins</button> <button class="action" id="exportPins">Export pins</button><div class="pinStack" id="pins"></div></div></section>
<aside class="right"><article class="scroll detail" id="detail"></article></aside>
</main>
<div class="sr" aria-live="polite" id="live"></div>
</div>
<script>
const VIEWER_VERSION="__VIEWER_VERSION__";
let manifest,datasets=[],resources=[],publishers=[],relationships=[],facets={},graph={},govukContent={};
let byDataset=new Map(),byResource=new Map(),byPublisher=new Map(),filters={},query="",mode="overview",selected=null,spotlight=null,pins=JSON.parse(localStorage.getItem("govCkanPins")||"[]"),spread=false;
const $=id=>document.getElementById(id),canvas=$("canvas"),detail=$("detail"),live=$("live");
function esc(v){return String(v??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]));}
function attr(v){return esc(v).replace(/"/g,"&quot;");}
async function loadJson(path){const res=await fetch(path);if(!res.ok)throw new Error(`${path}: ${res.status}`);return res.json();}
async function load(){manifest=await loadJson("data/manifest.json");if(manifest.viewer_version!==VIEWER_VERSION)throw new Error("viewer/data version mismatch");const loadChunks=async names=>(await Promise.all(names.map(loadJson))).flat();datasets=await loadChunks(manifest.chunks.datasets);resources=await loadChunks(manifest.chunks.resources);publishers=await loadChunks(manifest.chunks.publishers);relationships=await loadChunks(manifest.chunks.relationships);facets=await loadJson(manifest.indexes.facets);graph=await loadJson(manifest.indexes.graph);govukContent=await loadJson(manifest.indexes.govuk_content);datasets.forEach(d=>byDataset.set(d.name,d));resources.forEach(r=>byResource.set(r.id,r));publishers.forEach(p=>byPublisher.set(p.name,p));$("subtitle").textContent=`${manifest.counts.datasets.toLocaleString()} datasets, ${manifest.counts.resources.toLocaleString()} resources, ${manifest.counts.publishers.toLocaleString()} publishers`;applyUrl();render();}
function routeFor(item){if(!item)return"#overview";if(item.kind==="resource")return`#resource/${encodeURIComponent(item.id)}`;if(item.kind==="publisher")return`#publisher/${encodeURIComponent(item.name)}`;return`#dataset/${encodeURIComponent(item.name)}`;}
function applyUrl(){const params=new URLSearchParams(location.search);query=params.get("q")||"";$("query").value=query;["publisher","format","license","tag","update_year","host","govuk_linked","resource_type","publisher_family"].forEach(k=>{if(params.get(k))filters[k]=new Set(params.getAll(k));});if(["overview","force","timeline","matrix","resources"].includes(params.get("mode")))mode=params.get("mode");if(params.getAll("pin").length){pins=params.getAll("pin");localStorage.setItem("govCkanPins",JSON.stringify(pins));}spread=params.get("spread")==="1";const hash=decodeURIComponent(location.hash||"#overview");if(hash.startsWith("#resource/"))selected={kind:"resource",...byResource.get(hash.slice(10))};else if(hash.startsWith("#publisher/"))selected={kind:"publisher",...byPublisher.get(hash.slice(11))};else if(hash.startsWith("#dataset/"))selected={kind:"dataset",...byDataset.get(hash.slice(9))};}
function pushUrl(){const params=new URLSearchParams();if(query)params.set("q",query);if(mode&&mode!=="overview")params.set("mode",mode);Object.entries(filters).forEach(([k,set])=>[...set].sort().forEach(v=>params.append(k,v)));history.replaceState(null,"",`${params.toString()?`?${params}`:""}${routeFor(selected)}`);}
function valuesFor(dataset,key){if(key==="publisher")return[dataset.publisher];if(key==="publisher_family")return[publisherFamily(dataset.publisher)];if(key==="format")return dataset.formats||[];if(key==="license")return[dataset.license_id];if(key==="tag")return dataset.tags||[];if(key==="update_year")return dataset.timestamp?[String(dataset.timestamp).slice(0,4)]:[];if(key==="host")return dataset.resource_hosts||[];if(key==="govuk_linked")return[dataset.govuk_content_paths?.length?"yes":"no"];if(key==="resource_type")return dataset.resource_ids.flatMap(id=>[(byResource.get(id)||{}).resource_type||"unknown"]);return[];}
function publisherFamily(name){if(name.endsWith("-council")||name.includes("borough-council")||name.includes("county-council"))return"local government";if(name.includes("nhs")||name.includes("health"))return"health";if(name.startsWith("department-")||["cabinet-office","home-office","hm-treasury"].includes(name))return"central government";if(name.includes("environment")||name.includes("natural")||name.includes("geological"))return"environment and science";return"other public body";}
function filteredDatasets(){const q=query.toLowerCase().trim();return datasets.filter(d=>{if(q&&!`${d.name} ${d.title} ${d.notes} ${d.publisher_title} ${(d.tags||[]).join(" ")} ${(d.formats||[]).join(" ")}`.toLowerCase().includes(q))return false;for(const[k,set]of Object.entries(filters)){if(set.size&&!valuesFor(d,k).some(v=>set.has(String(v))))return false;}return true;});}
function renderFacets(visible){const counts={};Object.keys(facets).forEach(k=>counts[k]=new Map());visible.forEach(d=>Object.keys(counts).forEach(k=>valuesFor(d,k).forEach(v=>counts[k].set(v,(counts[k].get(v)||0)+1))));$("facets").innerHTML=Object.entries(facets).map(([key,items])=>`<section class="facet"><h2><span>${esc(key.replaceAll("_"," "))}</span><span>${(filters[key]?.size)||0}</span></h2>${items.slice(0,24).map(item=>{const active=filters[key]?.has(item.value);const count=counts[key].get(item.value)||0;return`<button class="${active?"active":""}" data-facet="${attr(key)}" data-value="${attr(item.value)}">${esc(item.value)} <small>${count}</small></button>`;}).join("")}</section>`).join("");document.querySelectorAll("[data-facet]").forEach(b=>b.onclick=()=>{const k=b.dataset.facet,v=b.dataset.value;filters[k]=filters[k]||new Set();filters[k].has(v)?filters[k].delete(v):filters[k].add(v);pushUrl();render();});}
function setSpotlight(id){spotlight=id;live.textContent=id?`Highlighted ${id}`:"Highlight cleared";document.querySelectorAll("[data-spot-id]").forEach(el=>el.classList.toggle("spotlight",el.dataset.spotId===id));}
function bindRows(root=document){root.querySelectorAll("[data-open]").forEach(el=>{el.onclick=()=>openId(el.dataset.open);el.onmouseenter=()=>setSpotlight(el.dataset.open);el.onfocus=()=>setSpotlight(el.dataset.open);el.ontouchstart=()=>setSpotlight(el.dataset.open);el.onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();openId(el.dataset.open);}};});}
function openId(id){if(id==="overview"){selected=null;mode="overview";}else if(id.startsWith("dataset/"))selected={kind:"dataset",...byDataset.get(id.slice(8))};else if(id.startsWith("resource/"))selected={kind:"resource",...byResource.get(id.slice(9))};else if(id.startsWith("publisher/"))selected={kind:"publisher",...byPublisher.get(id.slice(10))};pushUrl();render();}
function topList(title,items){return`<section class="card"><h3>${esc(title)}</h3><div class="list">${items.map(item=>`<button class="row" data-open="${attr(item.open)}" data-spot-id="${attr(item.open)}"><strong>${esc(item.label)}</strong><div class="meta">${esc(item.meta||"")}</div></button>`).join("")}</div></section>`;}
function renderOverview(visible){const topPub=[...new Map(visible.map(d=>[d.publisher,d])).values()].slice(0,8).map(d=>({label:d.publisher_title,meta:d.publisher,open:`publisher/${d.publisher}`}));const topDatasets=visible.slice(0,10).map(d=>({label:d.title,meta:`${d.publisher_title} - ${d.resource_count} resources`,open:`dataset/${d.name}`}));const formatCounts=new Map();visible.forEach(d=>(d.formats||[]).forEach(f=>formatCounts.set(f,(formatCounts.get(f)||0)+1)));canvas.innerHTML=`<div class="overview"><section class="hero"><h2>Metadata-first map of UK public data</h2><p>This static OKF bundle indexes CKAN datasets, resources, publishers, formats, licences, tags, hosts, and exact GOV.UK content links without downloading remote resource bodies.</p></section><div class="metrics"><div class="metric"><strong>${visible.length.toLocaleString()}</strong>shown datasets</div><div class="metric"><strong>${manifest.counts.resources.toLocaleString()}</strong>resources</div><div class="metric"><strong>${manifest.counts.publishers.toLocaleString()}</strong>publishers</div><div class="metric"><strong>${manifest.counts.govuk_content.toLocaleString()}</strong>GOV.UK enrichments</div></div><div class="grid">${topList("Top visible publishers",topPub)}${topList("Recently modified datasets",topDatasets)}${topList("Dominant formats",[...formatCounts.entries()].sort((a,b)=>b[1]-a[1]).slice(0,10).map(([k,v])=>({label:k,meta:`${v} visible datasets`,open:"overview"})))}</div><p class="notice">Use filters and search to reduce the corpus before entering graph views. The viewer intentionally avoids opening on a full hairball.</p></div>`;bindRows(canvas);}
function renderListView(visible,title){canvas.innerHTML=`<div class="overview"><h2>${esc(title)}</h2><div class="list">${visible.slice(0,180).map(d=>`<button class="row" data-open="dataset/${attr(d.name)}" data-spot-id="dataset/${attr(d.name)}"><h3>${esc(d.title)}</h3><div class="meta">${esc(d.publisher_title)} - ${(d.formats||[]).join(", ")} - ${d.resource_count} resources</div><p>${esc(d.notes)}</p></button>`).join("")}</div></div>`;bindRows(canvas);}
function renderMatrix(visible){const pubs=[...new Set(visible.map(d=>d.publisher_title))].slice(0,18);const fmts=[...new Set(visible.flatMap(d=>d.formats||[]))].slice(0,12);const counts=new Map();visible.forEach(d=>d.formats.forEach(f=>counts.set(`${d.publisher_title}|${f}`,(counts.get(`${d.publisher_title}|${f}`)||0)+1)));canvas.innerHTML=`<div class="overview"><h2>Publisher x Format Matrix</h2><div class="card" style="overflow:auto"><table><thead><tr><th>Publisher</th>${fmts.map(f=>`<th>${esc(f)}</th>`).join("")}</tr></thead><tbody>${pubs.map(p=>`<tr><th>${esc(p)}</th>${fmts.map(f=>`<td>${counts.get(`${p}|${f}`)||""}</td>`).join("")}</tr>`).join("")}</tbody></table></div></div>`;}
function renderForce(visible){const reduced=visible.slice(0,80);const selectedNode=selected?routeFor(selected).slice(1):"";const selectedIds=new Set(reduced.map(d=>`dataset/${d.name}`));const pubIds=new Set(reduced.map(d=>`publisher/${d.publisher}`));const nodes=[...reduced.map((d,i)=>({id:`dataset/${d.name}`,label:d.title,kind:"dataset",x:260+Math.cos(i*.7)*190,y:260+Math.sin(i*.7)*190})),...[...pubIds].map((id,i)=>({id,label:(byPublisher.get(id.slice(10))||{}).title||id,kind:"publisher",x:260+Math.cos(i*(Math.PI*2/pubIds.size))*245,y:260+Math.sin(i*(Math.PI*2/pubIds.size))*245}))];const map=new Map(nodes.map(n=>[n.id,n]));const edges=relationships.filter(e=>selectedIds.has(e.source)&&pubIds.has(e.target));canvas.innerHTML=`<svg class="graph" viewBox="0 0 540 540" role="img" aria-label="Reduced dataset publisher graph">${edges.map(e=>{const a=map.get(e.source),b=map.get(e.target);return a&&b?`<line class="edge" data-spot-id="${attr(e.source)}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"></line>`:"";}).join("")}${nodes.map(n=>{const label=n.kind==="publisher"||n.id===selectedNode,tx=n.x>420?n.x-10:n.x+10,anchor=n.x>420?"end":"start";return`<g class="node" tabindex="0" data-open="${attr(n.id)}" data-spot-id="${attr(n.id)}"><title>${esc(n.label)}</title><circle cx="${n.x}" cy="${n.y}" r="${n.kind==="publisher"?9:6}" fill="${n.kind==="publisher"?"#00703c":"#1d70b8"}"></circle>${label?`<text x="${tx}" y="${n.y+4}" text-anchor="${anchor}">${esc(n.label).slice(0,42)}</text>`:""}</g>`;}).join("")}</svg><p class="meta">Showing ${reduced.length} datasets plus their publishers. Filter or search to reduce the graph further.</p>`;bindRows(canvas);}
function renderDetail(){if(!selected){detail.innerHTML=`<h2>Bundle overview</h2><p>${esc(manifest.title)}</p><dl class="kv"><dt>Generated</dt><dd>${esc(manifest.generated_at)}</dd><dt>Mode</dt><dd>${esc(manifest.source.mode)}</dd><dt>CKAN count</dt><dd>${manifest.source.ckan_reported_count.toLocaleString()}</dd></dl>`;return;}if(selected.kind==="resource"){detail.innerHTML=resourceDetail(selected);return;}if(selected.kind==="publisher"){detail.innerHTML=publisherDetail(selected);return;}detail.innerHTML=datasetDetail(selected);bindRows(detail);}
function datasetDetail(d){const res=d.resource_ids.map(id=>byResource.get(id)).filter(Boolean);return`<h2>${esc(d.title)}</h2><p>${esc(d.notes)}</p><div class="chips">${(d.tags||[]).slice(0,10).map(t=>`<span class="chip">${esc(t)}</span>`).join("")}</div><p><button class="action primary" onclick='pinCurrent()'>Pin</button> <button class="action" onclick='copyRoute()'>Copy route</button></p><dl class="kv"><dt>Publisher</dt><dd><button class="pill" data-open="publisher/${attr(d.publisher)}">${esc(d.publisher_title)}</button></dd><dt>Licence</dt><dd>${esc(d.license_title)}</dd><dt>Modified</dt><dd>${esc(d.metadata_modified)}</dd><dt>Landing URL</dt><dd>${d.url?`<a href="${attr(d.url)}">${esc(d.url)}</a>`:""}</dd><dt>API</dt><dd><a href="${attr(d.source_api_url)}">${esc(d.source_api_url)}</a></dd></dl><h3>Resources</h3><div class="resourceList">${res.map(r=>`<button class="row" data-open="resource/${attr(r.id)}" data-spot-id="resource/${attr(r.id)}"><strong>${esc(r.name)}</strong><div class="meta">${esc(r.format)} - ${esc(r.host)}</div></button>`).join("")}</div>`;}
function resourceDetail(r){return`<h2>${esc(r.name)}</h2><p>${esc(r.description)}</p><p><button class="action primary" onclick='pinCurrent()'>Pin</button> <button class="action" onclick='copyRoute()'>Copy route</button></p><dl class="kv"><dt>Dataset</dt><dd><button class="pill" data-open="dataset/${attr(r.dataset)}">${esc((byDataset.get(r.dataset)||{}).title||r.dataset)}</button></dd><dt>Format</dt><dd>${esc(r.format)}</dd><dt>Type</dt><dd>${esc(r.resource_type)}</dd><dt>Host</dt><dd>${esc(r.host)}</dd><dt>URL</dt><dd><a href="${attr(r.url)}">${esc(r.url)}</a></dd><dt>GOV.UK path</dt><dd>${r.govuk_content_path?esc(r.govuk_content_path):"None"}</dd></dl>`;}
function publisherDetail(p){const ds=datasets.filter(d=>d.publisher===p.name).slice(0,40);return`<h2>${esc(p.title)}</h2><p>${esc(p.description)}</p><p><button class="action primary" onclick='pinCurrent()'>Pin</button> <button class="action" onclick='copyRoute()'>Copy route</button></p><dl class="kv"><dt>Name</dt><dd>${esc(p.name)}</dd><dt>State</dt><dd>${esc(p.state)}</dd><dt>Datasets</dt><dd>${p.dataset_count}</dd><dt>Resources</dt><dd>${p.resource_count}</dd></dl><h3>Datasets</h3><div class="resourceList">${ds.map(d=>`<button class="row" data-open="dataset/${attr(d.name)}" data-spot-id="dataset/${attr(d.name)}">${esc(d.title)}<div class="meta">${d.resource_count} resources</div></button>`).join("")}</div>`;}
function renderPins(){const root=$("pins");root.innerHTML=pins.map(id=>`<div class="pin ${spread?"spread":""}">${esc(id)} <button onclick="removePin('${attr(id)}')">x</button></div>`).join("");}
function pinCurrent(){if(!selected)return;const id=routeFor(selected).slice(1);if(!pins.includes(id))pins.push(id);localStorage.setItem("govCkanPins",JSON.stringify(pins));renderPins();}
function removePin(id){pins=pins.filter(p=>p!==id);localStorage.setItem("govCkanPins",JSON.stringify(pins));renderPins();}
function copyRoute(){navigator.clipboard?.writeText(location.href);}
function render(){const visible=filteredDatasets();$("count").textContent=`${visible.length.toLocaleString()} of ${datasets.length.toLocaleString()} datasets`;renderFacets(visible);document.querySelectorAll(".mode button").forEach(b=>b.classList.toggle("active",b.dataset.mode===mode));if(mode==="overview"||!selected)renderOverview(visible);else if(mode==="matrix")renderMatrix(visible);else if(mode==="force")renderForce(visible);else renderListView(visible,mode==="timeline"?"Timeline reduction":"Resource stack");renderDetail();renderPins();}
document.querySelectorAll(".mode button").forEach(b=>b.onclick=()=>{mode=b.dataset.mode;render();});
$("query").oninput=e=>{query=e.target.value;pushUrl();render();};
$("clearFilters").onclick=()=>{filters={};query="";$("query").value="";pushUrl();render();};
$("spreadPins").onclick=()=>{spread=!spread;renderPins();};
$("exportPins").onclick=()=>{navigator.clipboard?.writeText(JSON.stringify({exported_at:new Date().toISOString(),pins},null,2));};
document.addEventListener("keydown",e=>{if(e.key==="Escape")setSpotlight(null);});
load().catch(error=>{canvas.innerHTML=`<div class="overview"><section class="hero"><h2>Could not load bundle data</h2><p>${esc(error.message)}</p></section></div>`;});
</script>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output bundle directory.")
    parser.add_argument("--sample", type=int, help="Limit harvest to the first N CKAN datasets.")
    parser.add_argument("--api-base", default=DEFAULT_API_BASE, help="CKAN action API base URL.")
    parser.add_argument("--rows", type=int, default=DEFAULT_ROWS, help="CKAN package_search page size.")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help="Records per JSON chunk.")
    parser.add_argument("--enrich-govuk-limit", type=int, default=DEFAULT_ENRICH_LIMIT, help="Max exact GOV.UK paths to enrich.")
    parser.add_argument("--generated-at", default="", help="Override generated timestamp for reproducible tests.")
    args = parser.parse_args(argv)

    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    config = HarvestConfig(
        api_base=args.api_base,
        sample=args.sample,
        rows=args.rows,
        chunk_size=args.chunk_size,
        enrich_govuk_limit=max(0, args.enrich_govuk_limit),
        generated_at=args.generated_at,
    )
    try:
        manifest = build_bundle(config, out_dir)
    except (RuntimeError, HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"gov-ckan bundle build failed: {exc}", file=sys.stderr)
        return 1
    print(
        "built gov-ckan bundle: "
        f"{manifest['counts']['datasets']} datasets, "
        f"{manifest['counts']['resources']} resources, "
        f"{manifest['counts']['publishers']} publishers"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
