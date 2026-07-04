#!/usr/bin/env python3
"""Validate the generated GOV.UK CKAN OKF bundle."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import build_gov_ckan_bundle

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = ROOT / "gov-ckan"
LOCAL_PATH_RE = re.compile(r"(?<![A-Za-z0-9._-])/(?:Users|private|tmp)/|(?<![A-Za-z0-9])[A-Za-z]:\\")
FORBIDDEN_REMOTE_BODY_DIRS = {
    "download",
    "downloads",
    "raw",
    "raw-harvest",
    "resource-bodies",
    "resource-files",
    "snapshots",
}
REMOTE_BODY_SUFFIXES = {
    ".csv",
    ".ods",
    ".xls",
    ".xlsx",
    ".zip",
    ".gz",
    ".bz2",
    ".7z",
    ".pdf",
    ".doc",
    ".docx",
    ".geojson",
    ".gpkg",
    ".shp",
}
ALLOWED_SUFFIXES = {".html", ".json", ".md", ".png", ".jpg", ".jpeg", ".webp", ".svg"}


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_chunk_records(bundle: Path, manifest: dict[str, Any], key: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    chunk_names = manifest.get("chunks", {}).get(key, [])
    if not isinstance(chunk_names, list) or not chunk_names:
        raise ValueError(f"manifest chunks.{key} must list at least one chunk")
    for chunk_name in chunk_names:
        chunk_path = bundle / chunk_name
        if not chunk_path.exists():
            raise ValueError(f"missing chunk {rel(chunk_path)}")
        data = read_json(chunk_path)
        if not isinstance(data, list):
            raise ValueError(f"{rel(chunk_path)} is not a JSON list")
        for item in data:
            if not isinstance(item, dict):
                raise ValueError(f"{rel(chunk_path)} contains a non-object record")
        records.extend(data)
    return records


def require_unique(records: list[dict[str, Any]], key: str, label: str, errors: list[str]) -> None:
    seen: set[str] = set()
    for index, record in enumerate(records, start=1):
        value = str(record.get(key) or "").strip()
        if not value:
            errors.append(f"{label} record {index}: missing {key}")
            continue
        if value in seen:
            errors.append(f"{label}: duplicate {key} {value}")
        seen.add(value)


def contains_local_path(value: Any) -> bool:
    if isinstance(value, str):
        return bool(LOCAL_PATH_RE.search(value))
    if isinstance(value, list):
        return any(contains_local_path(item) for item in value)
    if isinstance(value, dict):
        return any(contains_local_path(key) or contains_local_path(item) for key, item in value.items())
    return False


def check_file_boundary(bundle: Path, errors: list[str]) -> None:
    for path in sorted(bundle.rglob("*")):
        relative_parts = set(path.relative_to(bundle).parts)
        if path.is_dir():
            if path.name in FORBIDDEN_REMOTE_BODY_DIRS:
                errors.append(f"{rel(path)}: generated bundle must not contain raw/downloaded resource bodies")
            continue
        if path.name == ".DS_Store":
            continue
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            errors.append(f"{rel(path)}: unexpected generated file suffix")
        if relative_parts & FORBIDDEN_REMOTE_BODY_DIRS:
            errors.append(f"{rel(path)}: raw/downloaded resource body path is not allowed")
        if path.suffix.lower() in REMOTE_BODY_SUFFIXES and "wiki" not in relative_parts:
            errors.append(f"{rel(path)}: remote resource body suffix is not allowed in bundle data")
        if path.suffix.lower() in {".html", ".json", ".md", ".svg"}:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"{rel(path)}: text artefact is not UTF-8")
                continue
            if LOCAL_PATH_RE.search(text):
                errors.append(f"{rel(path)}: local filesystem path leaked into generated artefact")


def check_manifest(bundle: Path, errors: list[str]) -> dict[str, Any] | None:
    manifest_path = bundle / "data" / "manifest.json"
    if not manifest_path.exists():
        errors.append(f"{rel(manifest_path)}: missing manifest")
        return None
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict):
        errors.append(f"{rel(manifest_path)}: manifest must be a JSON object")
        return None
    if manifest.get("viewer_version") != build_gov_ckan_bundle.VIEWER_VERSION:
        errors.append("manifest viewer_version does not match builder viewer version")
    if manifest.get("builder_version") != build_gov_ckan_bundle.BUILDER_VERSION:
        errors.append("manifest builder_version does not match builder version")
    for key in ("overview", "facets", "graph", "govuk_content"):
        index_path = manifest.get("indexes", {}).get(key)
        if not index_path or not (bundle / index_path).exists():
            errors.append(f"manifest indexes.{key} is missing or points to a missing file")
    index_path = bundle / "index.html"
    if not index_path.exists():
        errors.append(f"{rel(index_path)}: missing large-corpus entry point")
    elif index_path.read_text(encoding="utf-8") != build_gov_ckan_bundle.render_index():
        errors.append(f"{rel(index_path)}: index is not synchronized with scripts/build_gov_ckan_bundle.py")
    descriptor_path = bundle / "okf-explorer.json"
    if not descriptor_path.exists():
        errors.append(f"{rel(descriptor_path)}: missing large-corpus descriptor")
    else:
        descriptor = read_json(descriptor_path)
        if descriptor.get("schema") != "okf-explorer-large-corpus.v0":
            errors.append(f"{rel(descriptor_path)}: unexpected descriptor schema")
        if descriptor.get("entrypoints", {}).get("overview") != "viewer.html#overview":
            errors.append(f"{rel(descriptor_path)}: overview entrypoint should target viewer.html#overview")
    viewer_path = bundle / "viewer.html"
    if not viewer_path.exists():
        errors.append(f"{rel(viewer_path)}: missing static viewer")
    elif viewer_path.read_text(encoding="utf-8") != build_gov_ckan_bundle.render_viewer():
        errors.append(f"{rel(viewer_path)}: viewer is not synchronized with scripts/build_gov_ckan_bundle.py")
    return manifest


def check_records(bundle: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    datasets = load_chunk_records(bundle, manifest, "datasets")
    resources = load_chunk_records(bundle, manifest, "resources")
    publishers = load_chunk_records(bundle, manifest, "publishers")
    relationships = load_chunk_records(bundle, manifest, "relationships")
    counts = manifest.get("counts", {})
    expected = {
        "datasets": len(datasets),
        "resources": len(resources),
        "publishers": len(publishers),
        "relationships": len(relationships),
    }
    for key, actual in expected.items():
        if counts.get(key) != actual:
            errors.append(f"manifest counts.{key}={counts.get(key)!r} but chunks contain {actual}")
    require_unique(datasets, "name", "dataset", errors)
    require_unique(resources, "id", "resource", errors)
    require_unique(publishers, "name", "publisher", errors)

    dataset_names = {str(item.get("name")) for item in datasets}
    resource_ids = {str(item.get("id")) for item in resources}
    publisher_names = {str(item.get("name")) for item in publishers}
    for dataset in datasets:
        if "/" in str(dataset.get("name", "")):
            errors.append(f"dataset/{dataset.get('name')}: route ids must not contain slashes")
        if contains_local_path(dataset):
            errors.append(f"dataset/{dataset.get('name')}: local path leaked into record")
        for resource_id in dataset.get("resource_ids", []):
            if resource_id not in resource_ids:
                errors.append(f"dataset/{dataset.get('name')}: missing resource {resource_id}")
        if dataset.get("publisher") not in publisher_names:
            errors.append(f"dataset/{dataset.get('name')}: missing publisher {dataset.get('publisher')}")
    for resource in resources:
        if "/" in str(resource.get("id", "")):
            errors.append(f"resource/{resource.get('id')}: route ids must not contain slashes")
        if resource.get("dataset") not in dataset_names:
            errors.append(f"resource/{resource.get('id')}: missing dataset {resource.get('dataset')}")
        if contains_local_path(resource):
            errors.append(f"resource/{resource.get('id')}: local path leaked into record")
    for publisher in publishers:
        if "/" in str(publisher.get("name", "")):
            errors.append(f"publisher/{publisher.get('name')}: route ids must not contain slashes")
        if contains_local_path(publisher):
            errors.append(f"publisher/{publisher.get('name')}: local path leaked into record")
    for relationship in relationships:
        if not {"source", "target", "kind"} <= relationship.keys():
            errors.append(f"relationship is missing required fields: {relationship}")
        if contains_local_path(relationship):
            errors.append(f"relationship leaked local path: {relationship}")


def check_wiki(bundle: Path, errors: list[str]) -> None:
    for name in ("index.md", "data-source-report.md", "performance.md", "ui-design.md"):
        path = bundle / "wiki" / name
        if not path.exists():
            errors.append(f"{rel(path)}: missing wiki page")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"{rel(path)}: missing OKF frontmatter")
        if "\n# " not in text:
            errors.append(f"{rel(path)}: missing Markdown heading")


def main(argv: list[str] | None = None) -> int:
    bundle = Path(argv[0]) if argv else DEFAULT_BUNDLE
    if not bundle.is_absolute():
        bundle = ROOT / bundle
    errors: list[str] = []
    if not bundle.exists():
        errors.append(f"{rel(bundle)}: bundle directory does not exist")
    else:
        manifest = check_manifest(bundle, errors)
        if manifest is not None:
            try:
                check_records(bundle, manifest, errors)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                errors.append(str(exc))
        check_wiki(bundle, errors)
        check_file_boundary(bundle, errors)
    if errors:
        print("GOV.UK CKAN bundle validation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    manifest = read_json(bundle / "data" / "manifest.json")
    print(
        "GOV.UK CKAN bundle validated: "
        f"{manifest['counts']['datasets']} datasets, "
        f"{manifest['counts']['resources']} resources, "
        f"{manifest['counts']['publishers']} publishers"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
