#!/usr/bin/env python3
"""Build a deterministic, stratified GOV.UK CKAN evaluation bundle."""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import tempfile
from typing import Any

import build_gov_ckan_bundle as builder


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "gov-ckan"
DEFAULT_OUT = ROOT / "gov-ckan-sample"
DEFAULT_CONFIG = ROOT / "scripts" / "config" / "gov-ckan-evaluation.json"
DEFAULT_OPERATIONAL_METADATA = ROOT / "scripts" / "config" / "gov-ckan-operational-metadata.json"
SELECTION_SCHEMA = "gov-ckan-stratified-evaluation.v1"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_chunks(bundle: Path, paths: list[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for relative in paths:
        payload = load_json(bundle / relative)
        if not isinstance(payload, list):
            raise ValueError(f"{bundle / relative}: expected a JSON array")
        records.extend(item for item in payload if isinstance(item, dict))
    return records


def normalized_text(dataset: dict[str, Any]) -> str:
    values = [
        dataset.get("name"),
        dataset.get("title"),
        dataset.get("notes"),
        dataset.get("publisher"),
        dataset.get("publisher_title"),
        *(dataset.get("tags") or []),
        *(dataset.get("topics") or []),
        *(dataset.get("formats") or []),
    ]
    return " ".join(str(value or "") for value in values).casefold()


def stable_order(dataset: dict[str, Any]) -> tuple[int, str]:
    name = str(dataset.get("name") or "")
    return (int(dataset.get("resource_count") or 0), sha256(name.encode("utf-8")).hexdigest())


def query_score(dataset: dict[str, Any], query: str) -> int:
    tokens = [token for token in builder.search_tokens(query) if token not in builder.STOP_WORDS]
    if not tokens:
        return 0
    title = str(dataset.get("title") or "").casefold()
    name = str(dataset.get("name") or "").casefold()
    publisher = f"{dataset.get('publisher') or ''} {dataset.get('publisher_title') or ''}".casefold()
    tags = " ".join(dataset.get("tags") or []).casefold()
    notes = str(dataset.get("notes") or "").casefold()
    score = 0
    for token in tokens:
        score += 8 if token in title else 0
        score += 6 if token in name else 0
        score += 5 if token in tags else 0
        score += 4 if token in publisher else 0
        score += 1 if token in notes else 0
    return score


def select_datasets(
    datasets: list[dict[str, Any]],
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, list[str]], dict[str, int]]:
    if config.get("schema") != SELECTION_SCHEMA:
        raise ValueError(f"evaluation config must use {SELECTION_SCHEMA}")
    target = int(config.get("target_count") or 300)
    resource_cap = int(config.get("max_resource_count") or 40)
    selected: dict[str, dict[str, Any]] = {}
    reasons: dict[str, set[str]] = defaultdict(set)
    cohort_counts: dict[str, int] = defaultdict(int)

    def add(rows: list[dict[str, Any]], limit: int, reason: str, required: bool = False) -> None:
        before = len(selected)
        added = 0
        for dataset in rows:
            name = str(dataset.get("name") or "")
            if not name:
                continue
            if name not in selected and len(selected) >= target and not required:
                break
            if name not in selected and added >= limit:
                break
            if name not in selected:
                selected[name] = dataset
                added += 1
            reasons[f"dataset/{name}"].add(reason)
        cohort_counts[reason] += len(selected) - before

    publisher_config = config.get("publisher_cohorts") or {}
    target_publishers = set(publisher_config)
    for publisher, requested in publisher_config.items():
        rows = [dataset for dataset in datasets if dataset.get("publisher") == publisher]
        required = requested == "all"
        if not required:
            rows = [dataset for dataset in rows if int(dataset.get("resource_count") or 0) <= resource_cap]
        rows.sort(key=stable_order)
        limit = len(rows) if required else int(requested)
        add(rows, limit, f"publisher:{publisher}", required=required)

    for term, limit in (config.get("lexical_cohorts") or {}).items():
        rows = [
            dataset
            for dataset in datasets
            if dataset.get("publisher") not in target_publishers
            and term.casefold() in normalized_text(dataset)
            and int(dataset.get("resource_count") or 0) <= resource_cap
        ]
        rows.sort(key=stable_order)
        add(rows, int(limit), f"lexical-decoy:{term}")

    for query in config.get("query_cohorts") or []:
        rows = [
            dataset
            for dataset in datasets
            if int(dataset.get("resource_count") or 0) <= resource_cap and query_score(dataset, query) > 0
        ]
        rows.sort(key=lambda dataset: (-query_score(dataset, query), *stable_order(dataset)))
        add(rows, 1, f"query:{query}")

    for fmt, limit in (config.get("format_cohorts") or {}).items():
        rows = [
            dataset
            for dataset in datasets
            if fmt in (dataset.get("formats") or []) and int(dataset.get("resource_count") or 0) <= resource_cap
        ]
        rows.sort(key=stable_order)
        add(rows, int(limit), f"format:{fmt}")

    missing_cohorts = {
        "missing:licence": [dataset for dataset in datasets if dataset.get("license_id") == "not-specified"],
        "missing:format": [dataset for dataset in datasets if not dataset.get("formats") or dataset.get("formats") == ["unknown"]],
    }
    for reason, rows in missing_cohorts.items():
        rows = [dataset for dataset in rows if int(dataset.get("resource_count") or 0) <= resource_cap]
        rows.sort(key=stable_order)
        add(rows, 10, reason)

    remaining = [
        dataset
        for dataset in datasets
        if dataset.get("name") not in selected and int(dataset.get("resource_count") or 0) <= resource_cap
    ]
    remaining.sort(key=lambda dataset: sha256(str(dataset.get("name") or "").encode("utf-8")).hexdigest())
    add(remaining, max(0, target - len(selected)), "deterministic-diversity-fill")

    rows = sorted(selected.values(), key=lambda dataset: str(dataset["name"]))
    return rows, {route: sorted(values) for route, values in sorted(reasons.items())}, dict(sorted(cohort_counts.items()))


def build_evaluation_bundle(
    source_bundle: Path,
    out_dir: Path,
    config_path: Path,
    operational_metadata_path: Path,
) -> dict[str, Any]:
    config = load_json(config_path)
    source_manifest = load_json(source_bundle / "data" / "manifest.json")
    datasets = load_chunks(source_bundle, source_manifest["chunks"]["datasets"])
    resources = load_chunks(source_bundle, source_manifest["chunks"]["resources"])
    publisher_rows = load_chunks(source_bundle, source_manifest["chunks"]["publishers"])
    selected_datasets, selection_reasons, cohort_counts = select_datasets(datasets, config)
    selected_names = {dataset["name"] for dataset in selected_datasets}
    selected_resources = sorted(
        [resource for resource in resources if resource.get("dataset") in selected_names],
        key=lambda resource: (str(resource.get("dataset") or ""), int(resource.get("position") or 0), str(resource.get("id") or "")),
    )
    publisher_names = {dataset.get("publisher") for dataset in selected_datasets}
    publishers: dict[str, dict[str, Any]] = {}
    for source_publisher in publisher_rows:
        name = source_publisher.get("name")
        if name not in publisher_names:
            continue
        publisher = dict(source_publisher)
        publisher["dataset_count"] = sum(1 for dataset in selected_datasets if dataset.get("publisher") == name)
        publisher["resource_count"] = sum(
            len(dataset.get("resource_ids") or []) for dataset in selected_datasets if dataset.get("publisher") == name
        )
        publishers[name] = publisher
    publisher_records = sorted(publishers.values(), key=lambda publisher: str(publisher.get("name") or ""))

    source_govuk = load_json(source_bundle / source_manifest["indexes"]["govuk_content"])
    selected_paths = {path for dataset in selected_datasets for path in dataset.get("govuk_content_paths") or []}
    govuk_content = {path: value for path, value in source_govuk.items() if path in selected_paths}
    relationships = builder.build_relationships(selected_datasets, selected_resources, govuk_content)
    facets = builder.build_facets(selected_datasets, selected_resources, publishers)
    graph = builder.build_graph(selected_datasets, selected_resources, publishers, relationships)

    builder.clean_generated_outputs(out_dir)
    data_dir = out_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    chunks = {
        "datasets": builder.write_chunks(data_dir, "datasets", selected_datasets, 500),
        "resources": builder.write_chunks(data_dir, "resources", selected_resources, 500),
        "publishers": builder.write_chunks(data_dir, "publishers", publisher_records, 500),
        "relationships": builder.write_chunks(data_dir, "relationships", relationships, 500),
    }
    original_shard_length = builder.SEARCH_LEXICON_SHARD_LENGTH
    try:
        builder.SEARCH_LEXICON_SHARD_LENGTH = int(config.get("lexicon_shard_length") or original_shard_length)
        search = builder.build_search_index(out_dir, selected_datasets, selected_resources, 500)
    finally:
        builder.SEARCH_LEXICON_SHARD_LENGTH = original_shard_length
    builder.write_json(data_dir / "facets.json", facets)
    builder.write_json(data_dir / "graph.json", graph)
    builder.write_json(data_dir / "govuk-content.json", govuk_content)

    operational_metadata = builder.operational_metadata_for_datasets(
        builder.load_operational_metadata(operational_metadata_path), selected_datasets
    )
    if operational_metadata["records"]:
        builder.write_json(data_dir / "operational-metadata.json", operational_metadata)
    selection = {
        "schema": SELECTION_SCHEMA,
        "generated_at": config["generated_at"],
        "source_bundle": source_bundle.name,
        "target_count": config["target_count"],
        "selected_count": len(selected_datasets),
        "cohort_counts": cohort_counts,
        "records": selection_reasons,
    }
    builder.write_json(data_dir / "evaluation-selection.json", selection)

    official_sources = source_manifest.get("official_sources") or []
    manifest = {
        "title": "GOV.UK CKAN stratified evaluation bundle",
        "generated_at": config["generated_at"],
        "generated_by": "scripts/build_gov_ckan_evaluation_sample.py",
        "builder_version": builder.BUILDER_VERSION,
        "enrichment_version": builder.ENRICHMENT_VERSION,
        "transformation_pipeline_version": builder.TRANSFORMATION_PIPELINE_VERSION,
        "viewer_version": builder.VIEWER_VERSION,
        "source": {
            "api_base": source_manifest["source"]["api_base"],
            "mode": "stratified-evaluation",
            "source_bundle": f"{source_bundle.name}/okf-explorer.json",
            "source_generated_at": source_manifest["generated_at"],
            "ckan_reported_count": source_manifest["source"].get("ckan_reported_count"),
            "selection_schema": SELECTION_SCHEMA,
            "selection_target": config["target_count"],
            "harvest_timestamp": source_manifest["source"].get("harvest_timestamp"),
            "govuk_enrichment_limit": source_manifest["source"].get("govuk_enrichment_limit", 0),
        },
        "counts": {
            "datasets": len(selected_datasets),
            "resources": len(selected_resources),
            "publishers": len(publisher_records),
            "relationships": len(relationships),
            "govuk_content": len(govuk_content),
        },
        "chunks": chunks,
        "indexes": {
            "overview": "data/overview.json",
            "analysis": "data/analysis/overview.json",
            "search": "data/search/manifest.json",
            "facets": "data/facets.json",
            "graph": "data/graph.json",
            "govuk_content": "data/govuk-content.json",
            "evaluation_selection": "data/evaluation-selection.json",
        },
        "search": {
            "schema": search["schema"],
            "documents": search["counts"]["documents"],
            "tokens": search["counts"]["tokens"],
            "result_limit": search["result_limit"],
        },
        "official_sources": official_sources,
        "normalisation": source_manifest.get("normalisation") or {},
        "routes": ["#overview", "#dataset/<package-name>", "#resource/<resource-id>", "#publisher/<organization-name>"],
        "commit_policy": "derived metadata-only evaluation corpus; remote resource bodies are not downloaded",
    }
    if operational_metadata["records"]:
        manifest["indexes"]["operational_metadata"] = "data/operational-metadata.json"
    manifest["performance"] = builder.performance_model(manifest)
    overview = builder.build_overview(manifest, selected_datasets, facets, graph)
    analysis = builder.build_analysis_overview(
        manifest, selected_datasets, selected_resources, publishers, facets, relationships
    )
    (data_dir / "analysis").mkdir(parents=True, exist_ok=True)
    builder.write_json(data_dir / "overview.json", overview)
    builder.write_json(data_dir / "analysis" / "overview.json", analysis)
    builder.write_json(data_dir / "manifest.json", manifest)
    builder.write_json(out_dir / "okf-explorer.json", builder.build_explorer_descriptor(manifest))
    builder.render_wiki(out_dir, manifest, official_sources)
    (out_dir / "index.html").write_text(builder.render_index(), encoding="utf-8")
    (out_dir / "viewer.html").write_text(builder.render_viewer(), encoding="utf-8")
    builder.remove_local_metadata(out_dir)
    return manifest


def generated_files(bundle: Path) -> dict[str, bytes]:
    paths = [bundle / "index.html", bundle / "okf-explorer.json", bundle / "viewer.html"]
    paths.extend((bundle / "data").rglob("*"))
    paths.extend((bundle / "wiki").glob("*.md"))
    return {
        path.relative_to(bundle).as_posix(): path.read_bytes()
        for path in paths
        if path.is_file()
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Existing normalized full bundle.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output evaluation bundle.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Stratified selection configuration.")
    parser.add_argument(
        "--operational-metadata",
        type=Path,
        default=DEFAULT_OPERATIONAL_METADATA,
        help="Source-backed operational metadata registry.",
    )
    parser.add_argument("--check", action="store_true", help="Verify the committed output is reproducible.")
    args = parser.parse_args(argv)
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            check_dir = Path(tmp) / "gov-ckan-sample"
            build_evaluation_bundle(args.source, check_dir, args.config, args.operational_metadata)
            expected = generated_files(check_dir)
            actual = generated_files(args.out)
            if expected != actual:
                missing = sorted(set(expected) - set(actual))
                extra = sorted(set(actual) - set(expected))
                changed = sorted(path for path in set(expected) & set(actual) if expected[path] != actual[path])
                details = [
                    *(f"missing {path}" for path in missing),
                    *(f"extra {path}" for path in extra),
                    *(f"changed {path}" for path in changed),
                ]
                raise SystemExit("stratified evaluation bundle is out of date:\n" + "\n".join(details[:50]))
        print(f"stratified GOV.UK CKAN evaluation bundle is synchronized: {len(actual)} generated files")
        return 0
    manifest = build_evaluation_bundle(args.source, args.out, args.config, args.operational_metadata)
    print(
        "built stratified GOV.UK CKAN evaluation bundle: "
        f"{manifest['counts']['datasets']} datasets, "
        f"{manifest['counts']['resources']} resources, "
        f"{manifest['counts']['publishers']} publishers"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
