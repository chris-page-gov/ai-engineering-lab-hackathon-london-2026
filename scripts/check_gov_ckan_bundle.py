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
    for key in ("overview", "analysis", "facets", "graph", "govuk_content"):
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
        if descriptor.get("schema") != build_gov_ckan_bundle.LARGE_CORPUS_SCHEMA:
            errors.append(f"{rel(descriptor_path)}: unexpected descriptor schema")
        if descriptor.get("entrypoints", {}).get("overview") != "viewer.html#overview":
            errors.append(f"{rel(descriptor_path)}: overview entrypoint should target viewer.html#overview")
        if descriptor.get("entrypoints", {}).get("analysis_overview") != "data/analysis/overview.json":
            errors.append(f"{rel(descriptor_path)}: analysis_overview should target data/analysis/overview.json")
        if descriptor.get("entrypoints", {}).get("search_manifest") != "data/search/manifest.json":
            errors.append(f"{rel(descriptor_path)}: search_manifest should target data/search/manifest.json")
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
        if not str(dataset.get("concept_id", "")).startswith("datasets/"):
            errors.append(f"dataset/{dataset.get('name')}: missing stable dataset concept_id")
        if dataset.get("route") != f"dataset/{dataset.get('name')}":
            errors.append(f"dataset/{dataset.get('name')}: route should match dataset/<name>")
        if not dataset.get("topics"):
            errors.append(f"dataset/{dataset.get('name')}: controlled topics must not be empty")
        if not isinstance(dataset.get("quality"), dict) or "overall" not in dataset.get("quality", {}):
            errors.append(f"dataset/{dataset.get('name')}: missing quality score")
        provenance = dataset.get("provenance")
        if not isinstance(provenance, dict) or not provenance.get("ckan_package_id") or not provenance.get("transformation_pipeline_version"):
            errors.append(f"dataset/{dataset.get('name')}: missing provenance")
        if str(dataset.get("license_id", "")).lower() in {"not specified", "notspecified", "ogl", "ogl-uk-3.0"}:
            errors.append(f"dataset/{dataset.get('name')}: licence was not canonicalised")
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
        if not str(resource.get("concept_id", "")).startswith("resources/"):
            errors.append(f"resource/{resource.get('id')}: missing stable resource concept_id")
        if resource.get("route") != f"resource/{resource.get('id')}":
            errors.append(f"resource/{resource.get('id')}: route should match resource/<id>")
        if "source_format" not in resource or "format_confidence" not in resource:
            errors.append(f"resource/{resource.get('id')}: missing source/canonical format metadata")
        resource_format = str(resource.get("format", "")).strip().lower()
        if resource_format.startswith(".") or resource_format.startswith(("http://", "https://")):
            errors.append(f"resource/{resource.get('id')}: format was not canonicalised")
        provenance = resource.get("provenance")
        if not isinstance(provenance, dict) or not provenance.get("transformation_pipeline_version"):
            errors.append(f"resource/{resource.get('id')}: missing provenance")
        if resource.get("dataset") not in dataset_names:
            errors.append(f"resource/{resource.get('id')}: missing dataset {resource.get('dataset')}")
        if contains_local_path(resource):
            errors.append(f"resource/{resource.get('id')}: local path leaked into record")
    for publisher in publishers:
        if "/" in str(publisher.get("name", "")):
            errors.append(f"publisher/{publisher.get('name')}: route ids must not contain slashes")
        if publisher.get("concept_id") != f"publishers/{publisher.get('name')}.md":
            errors.append(f"publisher/{publisher.get('name')}: missing publisher authority concept_id")
        if publisher.get("route") != f"publisher/{publisher.get('name')}":
            errors.append(f"publisher/{publisher.get('name')}: route should match publisher/<name>")
        if not isinstance(publisher.get("provenance"), dict):
            errors.append(f"publisher/{publisher.get('name')}: missing provenance")
        if contains_local_path(publisher):
            errors.append(f"publisher/{publisher.get('name')}: local path leaked into record")
    for relationship in relationships:
        if not {"source", "target", "kind"} <= relationship.keys():
            errors.append(f"relationship is missing required fields: {relationship}")
        if contains_local_path(relationship):
            errors.append(f"relationship leaked local path: {relationship}")
    relationship_kinds = {str(relationship.get("kind")) for relationship in relationships}
    for required_kind in ("published by", "publisher authority", "licence", "download resource", "classified as", "temporal coverage"):
        if required_kind not in relationship_kinds:
            errors.append(f"relationships: missing required enriched relationship kind {required_kind!r}")


def check_search_index(bundle: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    search_path_name = manifest.get("indexes", {}).get("search")
    if search_path_name != "data/search/manifest.json":
        errors.append("manifest indexes.search must point to data/search/manifest.json")
        return
    search_path = bundle / search_path_name
    if not search_path.exists():
        errors.append(f"{rel(search_path)}: missing search manifest")
        return
    search = read_json(search_path)
    if search.get("schema") != build_gov_ckan_bundle.SEARCH_SCHEMA:
        errors.append(f"{rel(search_path)}: unexpected search schema")
    if search.get("counts", {}).get("documents") != manifest.get("counts", {}).get("datasets"):
        errors.append("search counts.documents must match manifest counts.datasets")
    entrypoints = search.get("entrypoints", {})
    for key in ("postings", "result_docs"):
        values = entrypoints.get(key)
        if not isinstance(values, list) or not values:
            errors.append(f"search entrypoints.{key} must list at least one chunk")
            continue
        for name in values:
            path = bundle / name
            if not path.exists():
                errors.append(f"{rel(path)}: missing search {key} chunk")
    for key in ("lexicon", "prefixes"):
        values = entrypoints.get(key)
        if not isinstance(values, dict) or not values:
            errors.append(f"search entrypoints.{key} must map shards to chunks")
            continue
        for name in values.values():
            path = bundle / name
            if not path.exists():
                errors.append(f"{rel(path)}: missing search {key} chunk")
    for key in ("facets", "doc_map"):
        name = entrypoints.get(key)
        path = bundle / str(name or "")
        if not name or not path.exists():
            errors.append(f"search entrypoints.{key} is missing or points to a missing file")

    doc_map_path = bundle / str(entrypoints.get("doc_map") or "")
    if doc_map_path.exists():
        doc_map = read_json(doc_map_path)
        if not isinstance(doc_map, dict):
            errors.append(f"{rel(doc_map_path)}: doc map must be an object")
        elif len(doc_map) != manifest.get("counts", {}).get("datasets"):
            errors.append(f"{rel(doc_map_path)}: doc map count must match dataset count")

    result_docs = entrypoints.get("result_docs") or []
    if result_docs:
        first_docs_path = bundle / result_docs[0]
        if first_docs_path.exists():
            docs = read_json(first_docs_path)
            if not isinstance(docs, list):
                errors.append(f"{rel(first_docs_path)}: result docs chunk must be a list")
            for doc in docs[:5]:
                if not isinstance(doc, dict) or not {"ordinal", "name", "title", "open"} <= set(doc):
                    errors.append(f"{rel(first_docs_path)}: result doc is missing required keys")

    lexicon_chunks = list((entrypoints.get("lexicon") or {}).values())
    postings_by_path = set(entrypoints.get("postings") or [])
    if lexicon_chunks:
        lexicon_path = bundle / lexicon_chunks[0]
        if lexicon_path.exists():
            lexicon = read_json(lexicon_path)
            if not isinstance(lexicon, list):
                errors.append(f"{rel(lexicon_path)}: lexicon chunk must be a list")
            for entry in lexicon[:25]:
                if not isinstance(entry, dict) or not {"token", "df", "postings"} <= set(entry):
                    errors.append(f"{rel(lexicon_path)}: lexicon entry is missing required keys")
                    continue
                if entry.get("postings") not in postings_by_path:
                    errors.append(f"{rel(lexicon_path)}: lexicon entry points at missing postings chunk")

    postings_chunks = entrypoints.get("postings") or []
    if postings_chunks:
        postings_path = bundle / postings_chunks[0]
        if postings_path.exists():
            postings = read_json(postings_path)
            if postings.get("schema") != "gov-ckan-search-postings.v1":
                errors.append(f"{rel(postings_path)}: unexpected postings schema")
            if not isinstance(postings.get("tokens"), dict):
                errors.append(f"{rel(postings_path)}: postings tokens must be an object")


def check_analysis_overview(bundle: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    analysis_path_name = manifest.get("indexes", {}).get("analysis")
    if analysis_path_name != "data/analysis/overview.json":
        errors.append("manifest indexes.analysis must point to data/analysis/overview.json")
        return
    analysis_path = bundle / analysis_path_name
    if not analysis_path.exists():
        errors.append(f"{rel(analysis_path)} is missing")
        return
    analysis = read_json(analysis_path)
    if analysis.get("schema") != build_gov_ckan_bundle.ANALYSIS_SCHEMA:
        errors.append(f"{rel(analysis_path)}: unexpected analysis schema")
    for key in (
        "summary",
        "graph_overview",
        "timeline_overview",
        "relationship_overview",
        "resource_overview",
        "quality_overview",
        "facet_analysis",
        "hierarchies",
        "ontology_candidates",
    ):
        if key not in analysis:
            errors.append(f"{rel(analysis_path)}: missing {key}")
    if not analysis.get("graph_overview", {}).get("nodes"):
        errors.append(f"{rel(analysis_path)}: graph_overview.nodes must not be empty")
    if not analysis.get("timeline_overview", {}).get("buckets"):
        errors.append(f"{rel(analysis_path)}: timeline_overview.buckets must not be empty")
    if not analysis.get("facet_analysis"):
        errors.append(f"{rel(analysis_path)}: facet_analysis must not be empty")


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
                check_search_index(bundle, manifest, errors)
                check_analysis_overview(bundle, manifest, errors)
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
