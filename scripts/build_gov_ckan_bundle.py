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

The left panel reduces the corpus through search and folded facets. Facets are derived from source structure: publisher, publisher family, format, licence, tag, update year, URL host, GOV.UK-linked status, and resource type. Facets start folded; opening one facet folds the previous inactive facet while selected values remain visible as compact chips.

The centre canvas never defaults to a hairball. `#overview` opens with a screen-sized bundle info-card. Dataset, publisher, resource-stack, timeline, matrix, and Graph views are available after selection or filtering. Graph view includes a colour key, visible relationship list, edge labels for selected-item graphs, drag-to-pan, zoom controls, and clickable concept nodes for facets such as format, tag, host, and licence.

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
*{box-sizing:border-box}html,body{height:100%;margin:0}body{font:14px/1.45 Arial,sans-serif;background:var(--bg);color:var(--ink);overflow:hidden}.app{height:100dvh;display:grid;grid-template-rows:auto 1fr;min-width:0}.top{display:flex;gap:12px;align-items:center;padding:12px 16px;background:#0b0c0c;color:#fff}.top h1{font-size:19px;margin:0}.top small{color:#d5dee7}.top a{color:#fff}.shell{min-height:0;display:grid;grid-template-columns:minmax(280px,350px) minmax(420px,1fr) minmax(360px,480px)}aside,.stage{min-height:0;overflow:hidden}.left,.right{background:var(--panel);border-right:1px solid var(--line);display:flex;flex-direction:column}.right{border-right:0;border-left:1px solid var(--line)}.scroll{overflow:auto;min-height:0;padding:14px}.search{display:grid;gap:8px;padding:14px;border-bottom:1px solid var(--line)}input,select,button{font:inherit}input[type=search]{width:100%;padding:10px;border:2px solid var(--line2);border-radius:4px}.facet{border-bottom:1px solid var(--line);padding:10px 14px}.facet h2{font-size:13px;margin:0 0 8px;display:flex;justify-content:space-between}.facet button,.pill,.mode button,.action{border:1px solid var(--line2);background:#fff;color:var(--ink);border-radius:4px;padding:6px 8px;cursor:pointer}.facet button{margin:0 4px 5px 0;font-size:12px}.facet button.active,.mode button.active,.action.primary{background:var(--blue);border-color:var(--blue);color:#fff}.stage{position:relative;background:linear-gradient(180deg,#e9f1f8,#f8fafc);display:grid;grid-template-rows:auto 1fr auto}.mode{display:flex;gap:7px;align-items:center;padding:10px 12px;border-bottom:1px solid var(--line);background:rgba(255,255,255,.92);z-index:2;flex-wrap:wrap}.navBtn{min-width:34px}.crumbs{min-width:180px;flex:1;color:var(--muted);font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.canvas{min-height:0;overflow:auto;position:relative;padding:18px}.overview{max-width:980px;margin:0 auto;display:grid;gap:14px}.hero{background:#0b0c0c;color:#fff;padding:22px;border-radius:6px}.hero h2{font-size:30px;margin:0 0 8px}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.metric,.card{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px}.metric strong{display:block;font-size:24px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}.list{display:grid;gap:8px}.row{border:1px solid var(--line);background:#fff;border-radius:6px;padding:10px;text-align:left;cursor:pointer}.row:hover,.row.spotlight{outline:3px solid #ffdd00}.row h3{font-size:15px;margin:0 0 4px}.meta{color:var(--muted);font-size:12px}.graph{width:100%;height:100%;min-height:560px}.node{cursor:pointer}.node circle,.node rect{stroke:#fff;stroke-width:2}.node.active circle,.node.active rect{stroke:#0b0c0c;stroke-width:3}.node text{font-size:11px;paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round}.node .cardLine{stroke:#fff;stroke-width:1;opacity:.9}.edge{stroke:#8da0b4;stroke-width:1.2;opacity:.55}.edge.active,.edge.spotlight{stroke:var(--blue);stroke-width:3;opacity:1}.graphCaption{position:sticky;left:0;bottom:0;background:rgba(255,255,255,.9);border:1px solid var(--line);border-radius:5px;padding:6px 8px;display:inline-block}.detail h2{font-size:24px;margin:0 0 8px}.kv{display:grid;grid-template-columns:120px minmax(0,1fr);gap:5px;border-top:1px solid var(--line);padding-top:10px;margin-top:10px}.kv dt{font-weight:700}.kv dd{margin:0;word-break:break-word}.chips{display:flex;gap:5px;flex-wrap:wrap}.chip{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:3px 8px;font-size:12px}.pins{border-top:1px solid var(--line);padding:10px 12px;background:#fff}.pinStack{display:flex;gap:6px;flex-wrap:wrap}.pin{border:1px solid var(--line2);background:#fff;border-radius:5px;padding:6px 8px;max-width:220px}.pin.spread{min-width:220px}.sr{position:absolute;left:-9999px}.notice{border-left:5px solid var(--yellow);background:#fff8cc;padding:10px;margin:10px 0}.resourceList{display:grid;gap:6px}.resourceList button{text-align:left}.hidden{display:none}@media(max-width:1050px){body{overflow:auto}.app{height:auto}.shell{display:block}.left,.right{max-height:none}.stage{height:72vh}.metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>
<style>
.mode{align-content:center}.navGroup,.modeGroup{display:flex;gap:6px;align-items:center}.navGroup{padding-right:10px;margin-right:2px;border-right:1px solid var(--line)}.modeGroup{flex-wrap:wrap}.mode button.navBtn{width:32px;height:32px;min-width:0;border-radius:999px;background:var(--card);font-weight:700;padding:0;line-height:1}.mode button.navBtn:hover{background:#dbe7f2}.mode button.modeBtn{border:1px solid var(--line2);background:#fff;color:var(--ink);border-radius:4px;padding:6px 8px;cursor:pointer}.mode button.modeBtn.active{background:var(--blue);border-color:var(--blue);color:#fff}.facet{padding:0}.facet h2{margin:0}.facet button.facetHeader{width:100%;display:flex;align-items:center;justify-content:space-between;border:0;border-radius:0;background:#fff;color:var(--ink);padding:10px 14px;margin:0;font-size:13px;font-weight:700;text-align:left;cursor:pointer}.facet button.facetHeader:hover{background:var(--card)}.facetToggleIcon{display:inline-block;width:18px;color:var(--muted)}.facetCount{color:var(--muted);font-weight:700}.facetBody{padding:0 14px 10px}.facetActive{display:flex;flex-wrap:wrap;gap:4px;padding:0 14px 10px}.facet.collapsed .facetBody{display:none}.facet.open .facetActive{display:none}
.graph{cursor:grab;touch-action:none;user-select:none}.graph.dragging{cursor:grabbing}.nodeHit{fill:transparent;stroke:transparent;pointer-events:all}.graphShell{min-height:620px;display:grid;grid-template-rows:auto minmax(560px,1fr) auto;gap:8px}.graphShell .graphCaption{position:static;pointer-events:none}.graphControls{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;background:rgba(255,255,255,.82);border:1px solid var(--line);border-radius:6px;padding:8px}.graphButtons{display:flex;align-items:center;gap:5px;flex-wrap:wrap}.graphButtons .action{min-width:34px}.legend{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.legendItem{display:inline-flex;align-items:center;gap:4px;color:var(--muted);font-size:12px}.swatch{width:11px;height:11px;border-radius:50%;border:1px solid #fff;box-shadow:0 0 0 1px var(--line2)}.edgeLabel{font-size:9px;fill:var(--ink);paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round;pointer-events:none}.edgePanel{background:rgba(255,255,255,.92);border:1px solid var(--line);border-radius:6px;padding:8px}.edgePanel summary{cursor:pointer;font-weight:700}.edgePanel ul{margin:6px 0 0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:4px;max-height:138px;overflow:auto}.edgePanel button{width:100%;border:0;background:transparent;text-align:left;color:var(--ink);padding:4px;border-radius:4px;cursor:pointer}.edgePanel button:hover,.edgePanel button:focus{background:var(--card);outline:2px solid var(--yellow)}
</style>
</head>
<body>
<div class="app">
<header class="top"><div><h1>GOV.UK CKAN OKF Viewer</h1><small id="subtitle">Loading bundle metadata</small></div><a href="wiki/index.md">OKF bundle notes</a></header>
<main class="shell">
<aside class="left"><div class="search"><input id="query" type="search" placeholder="Search datasets, resources, publishers, tags"><button class="action" id="clearFilters">Clear filters</button></div><div id="facets" class="scroll"></div></aside>
<section class="stage"><div class="mode"><div class="navGroup" aria-label="Navigation"><button class="navBtn" id="backBtn" title="Back" aria-label="Back">&#8592;</button><button class="navBtn" id="forwardBtn" title="Forward" aria-label="Forward">&#8594;</button></div><div class="modeGroup" aria-label="Canvas views"><button class="modeBtn active" data-mode="overview">Overview</button><button class="modeBtn" data-mode="force">Graph</button><button class="modeBtn" data-mode="timeline">Timeline</button><button class="modeBtn" data-mode="matrix">Publisher x Format</button><button class="modeBtn" data-mode="resources">Resource stack</button></div><span class="meta" id="count"></span><span class="crumbs" id="crumbs"></span></div><div class="canvas" id="canvas"></div><div class="pins"><button class="action" id="spreadPins">Spread pins</button> <button class="action" id="exportPins">Export pins</button><div class="pinStack" id="pins"></div></div></section>
<aside class="right"><article class="scroll detail" id="detail"></article></aside>
</main>
<div class="sr" aria-live="polite" id="live"></div>
</div>
<script>
const VIEWER_VERSION="__VIEWER_VERSION__";
let manifest,datasets=[],resources=[],publishers=[],relationships=[],facets={},graph={},govukContent={};
let byDataset=new Map(),byResource=new Map(),byPublisher=new Map(),filters={},query="",mode="overview",selected=null,spotlight=null,pins=JSON.parse(localStorage.getItem("govCkanPins")||"[]"),spread=false,labelPhase=0,labelLayerCount=1,openFacet="",graphKey="",graphZoom=1,graphBox={x:0,y:0,w:720,h:560,baseW:720,baseH:560},graphDrag=null,graphSuppressClick=false;
const $=id=>document.getElementById(id),canvas=$("canvas"),detail=$("detail"),live=$("live");
const FILTER_KEYS=["publisher","format","license","tag","update_year","host","govuk_linked","resource_type","publisher_family","publisher_state"];
function esc(v){return String(v??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]));}
function attr(v){return esc(v).replace(/"/g,"&quot;");}
function formatList(values){return(values||[]).map(v=>esc(v)).join(", ");}
function cleanText(v){const raw=String(v??"").replace(/<\\/?(p|div|li|br|ul|ol|h[1-6])\\b[^>]*>/gi," $& ");const t=document.createElement("template");t.innerHTML=raw;return(t.content.textContent||raw).replace(/\\s+/g," ").trim();}
async function loadJson(path){const res=await fetch(path);if(!res.ok)throw new Error(`${path}: ${res.status}`);return res.json();}
async function load(){manifest=await loadJson("data/manifest.json");if(manifest.viewer_version!==VIEWER_VERSION)throw new Error("viewer/data version mismatch");const loadChunks=async names=>(await Promise.all(names.map(loadJson))).flat();datasets=await loadChunks(manifest.chunks.datasets);resources=await loadChunks(manifest.chunks.resources);publishers=await loadChunks(manifest.chunks.publishers);relationships=await loadChunks(manifest.chunks.relationships);facets=await loadJson(manifest.indexes.facets);graph=await loadJson(manifest.indexes.graph);govukContent=await loadJson(manifest.indexes.govuk_content);datasets.forEach(d=>byDataset.set(d.name,d));resources.forEach(r=>byResource.set(r.id,r));publishers.forEach(p=>byPublisher.set(p.name,p));$("subtitle").textContent=`${manifest.counts.datasets.toLocaleString()} datasets, ${manifest.counts.resources.toLocaleString()} resources, ${manifest.counts.publishers.toLocaleString()} publishers`;applyUrl();render();}
function routeFor(item){if(!item)return"#overview";if(item.kind==="resource")return`#resource/${encodeURIComponent(item.id)}`;if(item.kind==="publisher")return`#publisher/${encodeURIComponent(item.name)}`;return`#dataset/${encodeURIComponent(item.name)}`;}
function applyUrl(){const params=new URLSearchParams(location.search);query=params.get("q")||"";$("query").value=query;filters={};FILTER_KEYS.forEach(k=>{if(params.get(k))filters[k]=new Set(params.getAll(k));});mode=["overview","force","timeline","matrix","resources"].includes(params.get("mode"))?params.get("mode"):"overview";if(params.getAll("pin").length){pins=params.getAll("pin");localStorage.setItem("govCkanPins",JSON.stringify(pins));}spread=params.get("spread")==="1";selected=null;const hash=decodeURIComponent(location.hash||"#overview");if(hash.startsWith("#resource/"))selected={kind:"resource",...byResource.get(hash.slice(10))};else if(hash.startsWith("#publisher/"))selected={kind:"publisher",...byPublisher.get(hash.slice(11))};else if(hash.startsWith("#dataset/"))selected={kind:"dataset",...byDataset.get(hash.slice(9))};}
function pushUrl(replace=false){const params=new URLSearchParams();if(query)params.set("q",query);if(mode&&mode!=="overview")params.set("mode",mode);Object.entries(filters).forEach(([k,set])=>[...set].sort().forEach(v=>params.append(k,v)));const next=`${params.toString()?`?${params}`:""}${routeFor(selected)}`;if(next===`${location.search}${location.hash}`)return;(replace?history.replaceState:history.pushState).call(history,null,"",next);}
function valuesFor(dataset,key){if(key==="publisher")return[dataset.publisher];if(key==="publisher_family")return[publisherFamily(dataset.publisher)];if(key==="publisher_state")return[(byPublisher.get(dataset.publisher)||{}).state||"unknown"];if(key==="format")return dataset.formats||[];if(key==="license")return[dataset.license_id];if(key==="tag")return dataset.tags||[];if(key==="update_year")return dataset.timestamp?[String(dataset.timestamp).slice(0,4)]:[];if(key==="host")return dataset.resource_hosts||[];if(key==="govuk_linked")return[dataset.govuk_content_paths?.length?"yes":"no"];if(key==="resource_type")return dataset.resource_ids.flatMap(id=>[(byResource.get(id)||{}).resource_type||"unknown"]);return[];}
function publisherFamily(name){if(name.endsWith("-council")||name.includes("borough-council")||name.includes("county-council"))return"local government";if(name.includes("nhs")||name.includes("health"))return"health";if(name.startsWith("department-")||["cabinet-office","home-office","hm-treasury"].includes(name))return"central government";if(name.includes("environment")||name.includes("natural")||name.includes("geological"))return"environment and science";return"other public body";}
function filteredDatasets(skipKey=null){const q=query.toLowerCase().trim();return datasets.filter(d=>{if(q&&!`${d.name} ${d.title} ${cleanText(d.notes)} ${d.publisher_title} ${(d.tags||[]).join(" ")} ${(d.formats||[]).join(" ")}`.toLowerCase().includes(q))return false;for(const[k,set]of Object.entries(filters)){if(k===skipKey)continue;if(set.size&&!valuesFor(d,k).some(v=>set.has(String(v))))return false;}return true;});}
function selectionMatchesVisible(visible){if(!selected)return true;if(selected.kind==="dataset")return visible.some(d=>d.name===selected.name);if(selected.kind==="resource")return visible.some(d=>(d.resource_ids||[]).includes(selected.id));if(selected.kind==="publisher")return visible.some(d=>d.publisher===selected.name);return true;}
function applyFacet(k,v,additive=false){const current=filters[k]||new Set();if(additive){current.has(v)?current.delete(v):current.add(v);filters[k]=current;}else if(current.size===1&&current.has(v)){filters[k]=new Set();}else{filters[k]=new Set([v]);}if(!filters[k].size)delete filters[k];openFacet=k;graphKey="";const visible=filteredDatasets();if(!selectionMatchesVisible(visible))selected=null;pushUrl();render();}
function toggleFacet(k){openFacet=openFacet===k?"":k;render();}
function facetButtons(key,items,counts,activeOnly=false){return items.filter(item=>!activeOnly||filters[key]?.has(item.value)).slice(0,24).map(item=>{const active=filters[key]?.has(item.value),count=counts.get(item.value)||0;return`<button class="${active?"active":""}" data-facet="${attr(key)}" data-value="${attr(item.value)}" title="Click to switch this facet; Ctrl or Command click to add/remove">${esc(item.value)} <small>${count}</small></button>`;}).join("");}
function renderFacets(visible){$("facets").innerHTML=Object.entries(facets).map(([key,items])=>{const base=filteredDatasets(key),counts=new Map();base.forEach(d=>valuesFor(d,key).forEach(v=>counts.set(v,(counts.get(v)||0)+1)));const isOpen=openFacet===key,selectedCount=(filters[key]?.size)||0,label=key.replaceAll("_"," "),activeHtml=selectedCount?`<div class="facetActive">${facetButtons(key,items,counts,true)}</div>`:"";return`<section class="facet ${isOpen?"open":"collapsed"}"><h2><button class="facetHeader" data-facet-toggle="${attr(key)}" aria-expanded="${isOpen?"true":"false"}"><span><span class="facetToggleIcon">${isOpen?"-":"+"}</span>${esc(label)}</span><span class="facetCount">${selectedCount}</span></button></h2>${activeHtml}<div class="facetBody">${facetButtons(key,items,counts,false)}</div></section>`;}).join("");document.querySelectorAll("[data-facet-toggle]").forEach(b=>b.onclick=()=>toggleFacet(b.dataset.facetToggle));document.querySelectorAll("[data-facet]").forEach(b=>b.onclick=e=>applyFacet(b.dataset.facet,b.dataset.value,e.ctrlKey||e.metaKey));}
function setSpotlight(id){spotlight=id;live.textContent=id?`Highlighted ${id}`:"Highlight cleared";document.querySelectorAll("[data-spot-id]").forEach(el=>el.classList.toggle("spotlight",el.dataset.spotId===id));}
function bindRows(root=document){root.querySelectorAll("[data-open]").forEach(el=>{el.onclick=()=>{if(graphSuppressClick){graphSuppressClick=false;return;}openId(el.dataset.open);};el.onmouseenter=()=>setSpotlight(el.dataset.open);el.onfocus=()=>setSpotlight(el.dataset.open);el.ontouchstart=()=>setSpotlight(el.dataset.open);el.onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();openId(el.dataset.open);}};});}
function openId(id){if(id==="overview"){selected=null;mode="overview";}else if(id.startsWith("dataset/"))selected={kind:"dataset",...byDataset.get(id.slice(8))};else if(id.startsWith("resource/"))selected={kind:"resource",...byResource.get(id.slice(9))};else if(id.startsWith("publisher/"))selected={kind:"publisher",...byPublisher.get(id.slice(10))};labelPhase=0;labelLayerCount=1;graphKey="";pushUrl();render();}
function topList(title,items){return`<section class="card"><h3>${esc(title)}</h3><div class="list">${items.map(item=>`<button class="row" data-open="${attr(item.open)}" data-spot-id="${attr(item.open)}"><strong>${esc(item.label)}</strong><div class="meta">${esc(item.meta||"")}</div></button>`).join("")}</div></section>`;}
function summaryFor(visible){const resourcesShown=new Set(),publishersShown=new Set(),govukShown=new Set();visible.forEach(d=>{(d.resource_ids||[]).forEach(id=>resourcesShown.add(id));if(d.publisher)publishersShown.add(d.publisher);(d.govuk_content_paths||[]).forEach(path=>{if(govukContent[path]?.status===200)govukShown.add(path);});});return{resources:resourcesShown.size,publishers:publishersShown.size,govuk:govukShown.size};}
function renderOverview(visible){const summary=summaryFor(visible);const topPub=[...new Map(visible.map(d=>[d.publisher,d])).values()].slice(0,8).map(d=>({label:d.publisher_title,meta:d.publisher,open:`publisher/${d.publisher}`}));const topDatasets=visible.slice(0,10).map(d=>({label:d.title,meta:`${d.publisher_title} - ${d.resource_count} resources`,open:`dataset/${d.name}`}));const formatCounts=new Map();visible.forEach(d=>(d.formats||[]).forEach(f=>formatCounts.set(f,(formatCounts.get(f)||0)+1)));canvas.innerHTML=`<div class="overview"><section class="hero"><h2>Metadata-first map of UK public data</h2><p>This static OKF bundle indexes CKAN datasets, resources, publishers, formats, licences, tags, hosts, and exact GOV.UK content links without downloading remote resource bodies.</p></section><div class="metrics"><div class="metric"><strong>${visible.length.toLocaleString()}</strong>shown datasets</div><div class="metric"><strong>${summary.resources.toLocaleString()}</strong>shown resources</div><div class="metric"><strong>${summary.publishers.toLocaleString()}</strong>shown publishers</div><div class="metric"><strong>${summary.govuk.toLocaleString()}</strong>shown GOV.UK enrichments</div></div><div class="grid">${topList("Top visible publishers",topPub)}${topList("Recently modified datasets",topDatasets)}${topList("Dominant formats",[...formatCounts.entries()].sort((a,b)=>b[1]-a[1]).slice(0,10).map(([k,v])=>({label:k,meta:`${v} visible datasets`,open:"overview"})))}</div><p class="notice">Use filters and search to reduce the corpus before entering graph views. The viewer intentionally avoids opening on a full hairball.</p></div>`;bindRows(canvas);}
function renderListView(visible,title){canvas.innerHTML=`<div class="overview"><h2>${esc(title)}</h2><div class="list">${visible.slice(0,180).map(d=>`<button class="row" data-open="dataset/${attr(d.name)}" data-spot-id="dataset/${attr(d.name)}"><h3>${esc(d.title)}</h3><div class="meta">${esc(d.publisher_title)} - ${formatList(d.formats)} - ${d.resource_count} resources</div><p>${esc(cleanText(d.notes))}</p></button>`).join("")}</div></div>`;bindRows(canvas);}
function renderMatrix(visible){const pubs=[...new Set(visible.map(d=>d.publisher_title))].slice(0,18);const fmts=[...new Set(visible.flatMap(d=>d.formats||[]))].slice(0,12);const counts=new Map();visible.forEach(d=>d.formats.forEach(f=>counts.set(`${d.publisher_title}|${f}`,(counts.get(`${d.publisher_title}|${f}`)||0)+1)));canvas.innerHTML=`<div class="overview"><h2>Publisher x Format Matrix</h2><div class="card" style="overflow:auto"><table><thead><tr><th>Publisher</th>${fmts.map(f=>`<th>${esc(f)}</th>`).join("")}</tr></thead><tbody>${pubs.map(p=>`<tr><th>${esc(p)}</th>${fmts.map(f=>`<td>${counts.get(`${p}|${f}`)||""}</td>`).join("")}</tr>`).join("")}</tbody></table></div></div>`;}
function nodeForId(id){if(id.startsWith("dataset/")){const d=byDataset.get(id.slice(8));return d&&{id,label:d.title,kind:"dataset",open:id};}if(id.startsWith("resource/")){const r=byResource.get(id.slice(9));return r&&{id,label:r.name||r.id,kind:"resource",open:id};}if(id.startsWith("publisher/")){const p=byPublisher.get(id.slice(10));return{id,label:(p&&p.title)||id.slice(10),kind:"publisher",open:id};}const [kind,...rest]=id.split("/");const value=decodeURIComponent(rest.join("/")||kind);return{id,label:value,value,kind,open:null};}
function shortLabel(text,max=42){const clean=cleanText(text);return clean.length>max?`${clean.slice(0,max-1)}...`:clean;}
function colourFor(kind){return kind==="publisher"?"#00703c":kind==="resource"?"#5694ca":kind==="dataset"?"#1d70b8":kind==="format"?"#4c2c92":kind==="license"?"#b58800":kind==="tag"?"#d4351c":"#5d6b78";}
function facetKeyForKind(kind){return kind==="format"?"format":kind==="license"?"license":kind==="tag"?"tag":kind==="host"?"host":kind==="resource_type"?"resource_type":"";}
function nodeActionAttrs(n){if(n.open)return`data-open="${attr(n.open)}"`;const facet=facetKeyForKind(n.kind);return facet?`data-graph-facet="${attr(facet)}" data-value="${attr(n.value||n.label)}"`:"";}
function placeArc(pos,nodes,cx,cy,r,start,end){const step=nodes.length>1?(end-start)/(nodes.length-1):0;nodes.forEach((n,i)=>{const a=nodes.length>1?start+i*step:(start+end)/2;pos[n.id]={x:cx+Math.cos(a)*r,y:cy+Math.sin(a)*r};});}
function graphNodesAndEdges(visible){const centre=selected?routeFor(selected).slice(1):"";let edges=[];if(centre){edges=relationships.filter(e=>e.source===centre||e.target===centre);if(selected.kind==="publisher"){const visibleDatasetIds=new Set(visible.filter(d=>d.publisher===selected.name).slice(0,40).map(d=>`dataset/${d.name}`));edges=relationships.filter(e=>e.target===centre&&visibleDatasetIds.has(e.source));}const priority={publisher:0,dataset:1,format:2,license:3,govuk_content:4,tag:5,host:6,resource:7};edges=edges.sort((a,b)=>{const ak=(nodeForId(a.source===centre?a.target:a.source)||{}).kind,bk=(nodeForId(b.source===centre?b.target:b.source)||{}).kind;return(priority[ak]??9)-(priority[bk]??9);}).slice(0,52);}else{const reduced=visible.slice(0,60);const datasetIds=new Set(reduced.map(d=>`dataset/${d.name}`));const publisherIds=new Set(reduced.map(d=>`publisher/${d.publisher}`));edges=relationships.filter(e=>datasetIds.has(e.source)&&publisherIds.has(e.target));}const ids=new Set(centre?[centre]:[]);edges.forEach(e=>{ids.add(e.source);ids.add(e.target);});if(!centre){visible.slice(0,60).forEach(d=>{ids.add(`dataset/${d.name}`);ids.add(`publisher/${d.publisher}`);});}const nodes=[...ids].map(nodeForId).filter(Boolean);return{centre,nodes,edges:edges.filter(e=>ids.has(e.source)&&ids.has(e.target))};}
function graphPositions(model,w,h){const cx=w/2,cy=h/2,pos={};if(model.centre){pos[model.centre]={x:cx,y:cy};const groups={publisher:[],dataset:[],format:[],license:[],tag:[],resource:[],govuk_content:[],host:[],other:[]};model.nodes.filter(n=>n.id!==model.centre).forEach(n=>(groups[n.kind]||groups.other).push(n));Object.values(groups).forEach(list=>list.sort((a,b)=>a.label.localeCompare(b.label)));const r=Math.min(w,h)*.33;placeArc(pos,groups.publisher,cx,cy,r,-.2,.25);placeArc(pos,groups.format.concat(groups.license),cx,cy,r,-2.2,-1.25);placeArc(pos,groups.tag,cx,cy,r,2.35,3.8);placeArc(pos,groups.resource,cx,cy,r,.75,2.15);placeArc(pos,groups.dataset.concat(groups.govuk_content,groups.host,groups.other),cx,cy,r,-.95,-.45);return pos;}const publishers=model.nodes.filter(n=>n.kind==="publisher").sort((a,b)=>a.label.localeCompare(b.label)),datasetsOnly=model.nodes.filter(n=>n.kind==="dataset").sort((a,b)=>a.label.localeCompare(b.label));placeArc(pos,publishers,cx,cy,Math.min(w,h)*.34,-Math.PI*.9,Math.PI*.9);datasetsOnly.forEach((n,i)=>{pos[n.id]={x:cx+Math.cos(i*.72)*Math.min(w,h)*.23,y:cy+Math.sin(i*.72)*Math.min(w,h)*.23};});return pos;}
function labelBox(n,p){const w=Math.min(260,shortLabel(n.label,52).length*6.5+16),h=18;return{x:p.x+18,y:p.y-11,w,h};}
function boxOverlap(a,b){return a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;}
function labelLayers(nodes,pos,alwaysId){const always=nodes.filter(n=>n.id===alwaysId||n.kind==="publisher").map(n=>({n,box:labelBox(n,pos[n.id])})).filter(item=>item.box);const alwaysBoxes=always.map(item=>item.box);const candidates=nodes.filter(n=>!always.some(item=>item.n.id===n.id)&&pos[n.id]).map(n=>({n,box:labelBox(n,pos[n.id])})).filter(item=>!alwaysBoxes.some(box=>boxOverlap(item.box,box)));const layers=[];candidates.forEach(item=>{let placed=false;for(const layer of layers){if(!layer.some(other=>boxOverlap(item.box,other.box))){layer.push(item);placed=true;break;}}if(!placed)layers.push([item]);});labelLayerCount=Math.max(1,layers.length);const active=layers.length?layers[labelPhase%labelLayerCount]:[];return new Set([...always.map(item=>item.n.id),...active.map(item=>item.n.id)]);}
function renderNode(n,p,active,labelled){const label=labelled?`<text x="${p.x+20}" y="${p.y+4}">${esc(shortLabel(n.label,50))}</text>`:"",attrs=nodeActionAttrs(n);if(n.kind==="resource")return`<g class="node ${active?"active":""}" tabindex="0" ${attrs} data-spot-id="${attr(n.id)}"><title>${esc(n.label)}</title><rect class="nodeHit" x="${p.x-24}" y="${p.y-18}" width="48" height="36" rx="5"></rect><rect x="${p.x-14}" y="${p.y-10}" width="28" height="20" rx="3" fill="${colourFor(n.kind)}"></rect><line class="cardLine" x1="${p.x-9}" y1="${p.y-3}" x2="${p.x+9}" y2="${p.y-3}"></line><line class="cardLine" x1="${p.x-9}" y1="${p.y+3}" x2="${p.x+6}" y2="${p.y+3}"></line>${label}</g>`;if(n.kind==="dataset")return`<g class="node ${active?"active":""}" tabindex="0" ${attrs} data-spot-id="${attr(n.id)}"><title>${esc(n.label)}</title><rect class="nodeHit" x="${p.x-25}" y="${p.y-20}" width="50" height="40" rx="6"></rect><rect x="${p.x-17}" y="${p.y-12}" width="34" height="24" rx="5" fill="${colourFor(n.kind)}"></rect>${label}</g>`;return`<g class="node ${active?"active":""}" tabindex="0" ${attrs} data-spot-id="${attr(n.id)}"><title>${esc(n.label)}</title><circle class="nodeHit" cx="${p.x}" cy="${p.y}" r="20"></circle><circle cx="${p.x}" cy="${p.y}" r="${active?11:8}" fill="${colourFor(n.kind)}"></circle>${label}</g>`;}
function graphLegend(){return`<div class="legend" aria-label="Graph colour key">${[["dataset","dataset"],["publisher","publisher"],["resource","resource"],["format","format"],["license","licence"],["tag","tag"],["host","host/other"]].map(([kind,label])=>`<span class="legendItem"><span class="swatch" style="background:${colourFor(kind)}"></span>${esc(label)}</span>`).join("")}</div>`;}
function relationshipText(e,map){return`${e.kind}: ${((map.get(e.source)||{}).label||e.source)} -> ${((map.get(e.target)||{}).label||e.target)}`;}
function graphRelationshipPanel(model,map){return`<details class="edgePanel" open><summary>Relationships (${model.edges.length})</summary><ul>${model.edges.slice(0,80).map((e,i)=>`<li><button data-edge-source="${attr(e.source)}" data-edge-target="${attr(e.target)}">${esc(relationshipText(e,map))}</button></li>`).join("")||"<li>No relationships in this reduction.</li>"}</ul></details>`;}
function graphSignature(model){return`${model.centre}|${model.nodes.map(n=>n.id).sort().join("|")}|${model.edges.map(e=>`${e.source}>${e.target}:${e.kind}`).sort().join("|")}`;}
function resetGraphViewState(w=720,h=560){graphZoom=1;graphBox={x:0,y:0,w,h,baseW:w,baseH:h};}
function graphViewBox(){return`${graphBox.x} ${graphBox.y} ${graphBox.w} ${graphBox.h}`;}
function updateGraphViewBox(){const svg=document.querySelector("svg.graph");if(svg)svg.setAttribute("viewBox",graphViewBox());const z=$("graphZoomLevel");if(z)z.textContent=`${Math.round(graphZoom*100)}%`;}
function setGraphZoom(value){const cx=graphBox.x+graphBox.w/2,cy=graphBox.y+graphBox.h/2;graphZoom=Math.max(.5,Math.min(4,value));graphBox.w=graphBox.baseW/graphZoom;graphBox.h=graphBox.baseH/graphZoom;graphBox.x=cx-graphBox.w/2;graphBox.y=cy-graphBox.h/2;updateGraphViewBox();}
function resetGraphView(){resetGraphViewState(graphBox.baseW,graphBox.baseH);updateGraphViewBox();}
function beginGraphPan(e){if(e.button!==undefined&&e.button!==0)return;graphDrag={x:e.clientX,y:e.clientY,box:{...graphBox},moved:false,captured:false};e.currentTarget.classList.add("dragging");}
function moveGraphPan(e){if(!graphDrag)return;const svg=e.currentTarget,dx=e.clientX-graphDrag.x,dy=e.clientY-graphDrag.y;if(Math.hypot(dx,dy)>3){graphDrag.moved=true;graphSuppressClick=true;if(!graphDrag.captured&&svg.setPointerCapture){svg.setPointerCapture(e.pointerId);graphDrag.captured=true;}}if(!graphDrag.moved)return;e.preventDefault();graphBox.x=graphDrag.box.x-dx*(graphBox.w/(svg.clientWidth||graphBox.baseW));graphBox.y=graphDrag.box.y-dy*(graphBox.h/(svg.clientHeight||graphBox.baseH));updateGraphViewBox();}
function endGraphPan(e){if(!graphDrag)return;const moved=graphDrag.moved;e.currentTarget.classList.remove("dragging");graphDrag=null;if(moved)setTimeout(()=>{graphSuppressClick=false;},80);}
function graphNodeAction(e){const target=e.target.closest("[data-graph-facet],[data-open]");if(!target)return;if(graphSuppressClick){graphSuppressClick=false;return;}if(target.dataset.graphFacet){applyFacet(target.dataset.graphFacet,target.dataset.value,e.ctrlKey||e.metaKey);return;}if(target.dataset.open)openId(target.dataset.open);}
function bindGraphControls(){const svg=document.querySelector("svg.graph");if(svg){svg.addEventListener("pointerdown",beginGraphPan);svg.addEventListener("pointermove",moveGraphPan);svg.addEventListener("pointerup",endGraphPan);svg.addEventListener("pointercancel",endGraphPan);svg.addEventListener("dragstart",e=>e.preventDefault());svg.addEventListener("click",graphNodeAction);svg.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();graphNodeAction(e);}});svg.addEventListener("wheel",e=>{e.preventDefault();setGraphZoom(graphZoom*(e.deltaY<0?1.12:.89));},{passive:false});}const zi=$("graphZoomIn"),zo=$("graphZoomOut"),zr=$("graphZoomReset");if(zi)zi.onclick=()=>setGraphZoom(graphZoom*1.2);if(zo)zo.onclick=()=>setGraphZoom(graphZoom/1.2);if(zr)zr.onclick=resetGraphView;document.querySelectorAll("[data-edge-source]").forEach(el=>{el.onclick=()=>setSpotlight(el.dataset.edgeSource);});updateGraphViewBox();}
function renderForce(visible){const model=graphNodesAndEdges(visible),w=720,h=560,pos=graphPositions(model,w,h),map=new Map(model.nodes.map(n=>[n.id,n])),labels=labelLayers(model.nodes,pos,model.centre),sig=graphSignature(model);if(sig!==graphKey){graphKey=sig;resetGraphViewState(w,h);}const edgeSvg=model.edges.map(e=>{const a=pos[e.source],b=pos[e.target],active=model.centre&&(e.source===model.centre||e.target===model.centre);return a&&b?`<line class="edge ${active?"active":""}" data-spot-id="${attr(e.source)}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"><title>${esc(relationshipText(e,map))}</title></line>`:"";}).join("");const edgeLabels=model.centre?model.edges.map(e=>{const a=pos[e.source],b=pos[e.target];return a&&b?`<text class="edgeLabel" x="${(a.x+b.x)/2+5}" y="${(a.y+b.y)/2-5}">${esc(e.kind)}</text>`:"";}).join(""):"";const nodeSvg=model.nodes.map(n=>renderNode(n,pos[n.id]||{x:w/2,y:h/2},n.id===model.centre,labels.has(n.id))).join("");canvas.innerHTML=`<div class="graphShell"><div class="graphControls"><div class="graphButtons" aria-label="Graph controls"><button class="action" id="graphZoomOut" title="Zoom out" aria-label="Zoom out">-</button><button class="action" id="graphZoomReset" title="Reset zoom" aria-label="Reset zoom"><span id="graphZoomLevel">${Math.round(graphZoom*100)}%</span></button><button class="action" id="graphZoomIn" title="Zoom in" aria-label="Zoom in">+</button></div>${graphLegend()}</div><svg class="graph" viewBox="${graphViewBox()}" role="img" aria-label="${model.centre?"Selected item relationship graph":"Reduced dataset publisher graph"}">${edgeSvg}${edgeLabels}${nodeSvg}</svg>${graphRelationshipPanel(model,map)}<p class="graphCaption">${model.centre?`Showing ${model.nodes.length} graph nodes directly related to ${esc(shortLabel((map.get(model.centre)||{}).label||model.centre,70))}.`:`Showing ${visible.slice(0,60).length} datasets plus their publishers. Select a dataset, resource, or publisher for a relationship graph.`} Drag the graph to pan, use +/- to zoom, and click concept nodes such as formats, tags, hosts, or licences to filter.</p></div>`;bindRows(canvas);bindGraphControls();}
function renderDetail(){if(!selected){detail.innerHTML=`<h2>Bundle overview</h2><p>${esc(manifest.title)}</p><dl class="kv"><dt>Generated</dt><dd>${esc(manifest.generated_at)}</dd><dt>Mode</dt><dd>${esc(manifest.source.mode)}</dd><dt>CKAN count</dt><dd>${manifest.source.ckan_reported_count.toLocaleString()}</dd></dl>`;return;}if(selected.kind==="resource"){detail.innerHTML=resourceDetail(selected);return;}if(selected.kind==="publisher"){detail.innerHTML=publisherDetail(selected);return;}detail.innerHTML=datasetDetail(selected);bindRows(detail);}
function datasetDetail(d){const res=d.resource_ids.map(id=>byResource.get(id)).filter(Boolean);return`<h2>${esc(d.title)}</h2><p>${esc(cleanText(d.notes))}</p><div class="chips">${(d.tags||[]).slice(0,10).map(t=>`<span class="chip">${esc(t)}</span>`).join("")}</div><p><button class="action primary" onclick='pinCurrent()'>Pin</button> <button class="action" onclick='copyRoute()'>Copy route</button></p><dl class="kv"><dt>Publisher</dt><dd><button class="pill" data-open="publisher/${attr(d.publisher)}">${esc(d.publisher_title)}</button></dd><dt>Licence</dt><dd>${esc(d.license_title)}</dd><dt>Modified</dt><dd>${esc(d.metadata_modified)}</dd><dt>Landing URL</dt><dd>${d.url?`<a href="${attr(d.url)}">${esc(d.url)}</a>`:""}</dd><dt>API</dt><dd><a href="${attr(d.source_api_url)}">${esc(d.source_api_url)}</a></dd></dl><h3>Resources</h3><div class="resourceList">${res.map(r=>`<button class="row" data-open="resource/${attr(r.id)}" data-spot-id="resource/${attr(r.id)}"><strong>${esc(r.name)}</strong><div class="meta">${esc(r.format)} - ${esc(r.host)}</div></button>`).join("")}</div>`;}
function resourceDetail(r){return`<h2>${esc(r.name)}</h2><p>${esc(cleanText(r.description))}</p><p><button class="action primary" onclick='pinCurrent()'>Pin</button> <button class="action" onclick='copyRoute()'>Copy route</button></p><dl class="kv"><dt>Dataset</dt><dd><button class="pill" data-open="dataset/${attr(r.dataset)}">${esc((byDataset.get(r.dataset)||{}).title||r.dataset)}</button></dd><dt>Format</dt><dd>${esc(r.format)}</dd><dt>Type</dt><dd>${esc(r.resource_type)}</dd><dt>Host</dt><dd>${esc(r.host)}</dd><dt>URL</dt><dd><a href="${attr(r.url)}">${esc(r.url)}</a></dd><dt>GOV.UK path</dt><dd>${r.govuk_content_path?esc(r.govuk_content_path):"None"}</dd></dl>`;}
function publisherDetail(p){const ds=datasets.filter(d=>d.publisher===p.name).slice(0,40);return`<h2>${esc(p.title)}</h2><p>${esc(cleanText(p.description))}</p><p><button class="action primary" onclick='pinCurrent()'>Pin</button> <button class="action" onclick='copyRoute()'>Copy route</button></p><dl class="kv"><dt>Name</dt><dd>${esc(p.name)}</dd><dt>State</dt><dd>${esc(p.state)}</dd><dt>Datasets</dt><dd>${p.dataset_count}</dd><dt>Resources</dt><dd>${p.resource_count}</dd></dl><h3>Datasets</h3><div class="resourceList">${ds.map(d=>`<button class="row" data-open="dataset/${attr(d.name)}" data-spot-id="dataset/${attr(d.name)}">${esc(d.title)}<div class="meta">${d.resource_count} resources</div></button>`).join("")}</div>`;}
function renderPins(){const root=$("pins");root.innerHTML=pins.map(id=>`<div class="pin ${spread?"spread":""}">${esc(id)} <button onclick="removePin('${attr(id)}')">x</button></div>`).join("");}
function pinCurrent(){if(!selected)return;const id=routeFor(selected).slice(1);if(!pins.includes(id))pins.push(id);localStorage.setItem("govCkanPins",JSON.stringify(pins));renderPins();}
function removePin(id){pins=pins.filter(p=>p!==id);localStorage.setItem("govCkanPins",JSON.stringify(pins));renderPins();}
function copyRoute(){navigator.clipboard?.writeText(location.href);}
function modeLabel(){return mode==="force"?"Graph":mode==="matrix"?"Publisher x Format":mode==="resources"?"Resource stack":mode[0].toUpperCase()+mode.slice(1);}
function selectedLabel(){if(!selected)return"";return selected.kind==="resource"?selected.name||selected.id:selected.kind==="publisher"?selected.title:selected.title;}
function filterLabel(){const parts=[];if(query)parts.push(`Search: ${query}`);Object.entries(filters).forEach(([k,set])=>[...set].forEach(v=>parts.push(`${k.replaceAll("_"," ")}: ${v}`)));return parts;}
function breadcrumbText(){const parts=["GOV.UK CKAN",modeLabel(),...filterLabel().slice(0,3)];if(selected)parts.push(shortLabel(selectedLabel(),54));return parts.join(" / ");}
function updateChrome(visible){$("count").textContent=`${visible.length.toLocaleString()} of ${datasets.length.toLocaleString()} datasets`;$("crumbs").textContent=breadcrumbText();document.title=`${selected?shortLabel(selectedLabel(),58):modeLabel()} - GOV.UK CKAN OKF Viewer`;}
function render(){let visible=filteredDatasets();if(selected&&!selectionMatchesVisible(visible)){selected=null;graphKey="";pushUrl(true);}updateChrome(visible);renderFacets(visible);document.querySelectorAll(".mode button[data-mode]").forEach(b=>b.classList.toggle("active",b.dataset.mode===mode));if(mode==="overview")renderOverview(visible);else if(mode==="matrix")renderMatrix(visible);else if(mode==="force")renderForce(visible);else renderListView(visible,mode==="timeline"?"Timeline reduction":"Resource stack");renderDetail();renderPins();}
document.querySelectorAll(".mode button[data-mode]").forEach(b=>b.onclick=()=>{mode=b.dataset.mode;labelPhase=0;labelLayerCount=1;graphKey="";pushUrl();render();});
$("query").oninput=e=>{query=e.target.value;graphKey="";const visible=filteredDatasets();if(!selectionMatchesVisible(visible))selected=null;pushUrl(true);render();};
$("clearFilters").onclick=()=>{filters={};query="";openFacet="";graphKey="";$("query").value="";pushUrl();render();};
$("backBtn").onclick=()=>history.back();
$("forwardBtn").onclick=()=>history.forward();
$("spreadPins").onclick=()=>{spread=!spread;renderPins();};
$("exportPins").onclick=()=>{navigator.clipboard?.writeText(JSON.stringify({exported_at:new Date().toISOString(),pins},null,2));};
document.addEventListener("keydown",e=>{if(e.key==="Escape")setSpotlight(null);});
window.addEventListener("popstate",()=>{applyUrl();render();});
setInterval(()=>{if(mode==="force"&&labelLayerCount>1){labelPhase=(labelPhase+1)%labelLayerCount;renderForce(filteredDatasets());}},2000);
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
