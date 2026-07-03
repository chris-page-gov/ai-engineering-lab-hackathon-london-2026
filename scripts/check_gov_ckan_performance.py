#!/usr/bin/env python3
"""Check the large-corpus performance budget for the GOV.UK CKAN viewer."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = ROOT / "gov-ckan"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def size(path: Path) -> int:
    return path.stat().st_size


def group_size(bundle: Path, names: list[str]) -> int:
    return sum(size(bundle / name) for name in names)


def main(argv: list[str] | None = None) -> int:
    bundle = Path(argv[0]) if argv else DEFAULT_BUNDLE
    if not bundle.is_absolute():
        bundle = ROOT / bundle
    errors: list[str] = []

    manifest_path = bundle / "data" / "manifest.json"
    overview_path = bundle / "data" / "overview.json"
    viewer_path = bundle / "viewer.html"
    descriptor_path = bundle / "okf-explorer.json"
    entry_path = bundle / "index.html"

    for path in (manifest_path, overview_path, viewer_path, descriptor_path, entry_path):
        if not path.exists():
            errors.append(f"{rel(path)} is missing")

    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    manifest = read_json(manifest_path)
    descriptor = read_json(descriptor_path)
    budgets = manifest.get("performance", {}).get("budgets", {})
    max_overview = int(budgets.get("max_overview_payload_bytes") or 0)
    max_requests = int(budgets.get("max_initial_requests") or 0)
    initial_files = [viewer_path, manifest_path, overview_path]
    overview_bytes = size(overview_path)
    initial_bytes = sum(size(path) for path in initial_files)

    if manifest.get("indexes", {}).get("overview") != "data/overview.json":
        errors.append("manifest indexes.overview must point to data/overview.json")
    if descriptor.get("schema") != "okf-explorer-large-corpus.v0":
        errors.append("okf-explorer.json must use schema okf-explorer-large-corpus.v0")
    if descriptor.get("entrypoints", {}).get("data_manifest") != "data/manifest.json":
        errors.append("okf-explorer.json must expose data/manifest.json")
    if max_overview and overview_bytes > max_overview:
        errors.append(
            f"{rel(overview_path)} is {overview_bytes} bytes, above budget {max_overview}"
        )
    if max_requests and len(initial_files) > max_requests:
        errors.append(f"default startup uses {len(initial_files)} files, above request budget {max_requests}")

    viewer_text = viewer_path.read_text(encoding="utf-8")
    if "overviewData=await loadJson(manifest.indexes.overview" not in viewer_text:
        errors.append("viewer.html no longer loads the overview index before full chunks")
    if "datasets=await loadChunks(manifest.chunks.datasets)" not in viewer_text:
        errors.append("viewer.html no longer has an explicit full-index hydration path")
    if "function requestRelationships()" not in viewer_text or "manifest.chunks.relationships" not in viewer_text:
        errors.append("viewer.html no longer lazy-loads relationship chunks")

    deferred_datasets = group_size(bundle, manifest.get("chunks", {}).get("datasets", []))
    deferred_resources = group_size(bundle, manifest.get("chunks", {}).get("resources", []))
    deferred_relationships = group_size(bundle, manifest.get("chunks", {}).get("relationships", []))

    if errors:
        print("GOV.UK CKAN performance budget errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "GOV.UK CKAN performance budget passed: "
        f"default startup {initial_bytes} bytes across {len(initial_files)} files; "
        f"overview {overview_bytes} bytes; "
        f"deferred datasets {deferred_datasets} bytes, "
        f"resources {deferred_resources} bytes, "
        f"relationships {deferred_relationships} bytes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
