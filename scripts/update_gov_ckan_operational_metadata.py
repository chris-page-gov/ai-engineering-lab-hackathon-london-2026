#!/usr/bin/env python3
"""Refresh an existing GOV.UK CKAN bundle's operational metadata sidecar."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import build_gov_ckan_bundle as builder


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = ROOT / "gov-ckan"
DEFAULT_SOURCE = ROOT / "scripts" / "config" / "gov-ckan-operational-metadata.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def refresh(bundle: Path, source: Path) -> int:
    manifest_path = bundle / "data" / "manifest.json"
    manifest = load_json(manifest_path)
    datasets: list[dict[str, Any]] = []
    for relative in manifest.get("chunks", {}).get("datasets", []):
        payload = load_json(bundle / relative)
        datasets.extend(item for item in payload if isinstance(item, dict))
    operational = builder.operational_metadata_for_datasets(builder.load_operational_metadata(source), datasets)
    if not operational["records"]:
        raise ValueError(f"{source}: none of the declared routes exist in {bundle}")
    relative = "data/operational-metadata.json"
    builder.write_json(bundle / relative, operational)
    manifest.setdefault("indexes", {})["operational_metadata"] = relative
    builder.write_json(manifest_path, manifest)
    builder.write_json(bundle / "okf-explorer.json", builder.build_explorer_descriptor(manifest))
    builder.remove_local_metadata(bundle)
    return len(operational["records"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args(argv)
    count = refresh(args.bundle, args.source)
    print(f"updated {args.bundle}: {count} operational metadata record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
