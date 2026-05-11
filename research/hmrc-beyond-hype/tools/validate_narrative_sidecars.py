#!/usr/bin/env python3
"""Validate HMRC narrative sidecar coverage and Markdown navigation."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import deque
from pathlib import Path
from urllib.parse import unquote

from build_narrative_sidecars import (
    ASSETS_DIR,
    DATA_DIR,
    GENERATED_MARKER,
    IMPORT_DIR,
    NARRATIVE_DIR,
    REPO_ROOT,
    VISUAL_SOURCES,
)
from pptx import Presentation
from pypdf import PdfReader


MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REQUIRED_SIDECAR_FIELDS = (
    "source_file:",
    "item_type:",
    "publication_status:",
    "tags:",
    "asset:",
)
RAW_IMPORT_SUFFIXES = {".pptx", ".pdf", ".png", ".m4a", ".wav", ".docx"}


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def expected_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for source in VISUAL_SOURCES:
        source_path = IMPORT_DIR / source.filename
        if source.kind == "pptx":
            counts[source.source_id] = len(Presentation(source_path).slides)
        elif source.kind == "pdf":
            counts[source.source_id] = len(PdfReader(str(source_path)).pages)
        elif source.kind == "png":
            counts[source.source_id] = 1
        else:
            raise ValueError(f"Unhandled source kind: {source.kind}")
    return counts


def load_coverage() -> list[dict[str, str]]:
    coverage_path = DATA_DIR / "visual_coverage.csv"
    if not coverage_path.exists():
        raise AssertionError(f"Missing coverage CSV: {repo_relative(coverage_path)}")
    with coverage_path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [match.group(1).split()[0].strip("<>") for match in MARKDOWN_LINK_RE.finditer(text)]


def resolve_link(source_file: Path, target: str) -> Path | None:
    if target.startswith(("http://", "https://", "mailto:")):
        return None
    if target.startswith("#"):
        return None
    path_part = unquote(target.split("#", 1)[0])
    if not path_part:
        return None
    return (source_file.parent / path_part).resolve()


def validate_links() -> tuple[list[str], dict[Path, set[Path]], set[Path]]:
    errors: list[str] = []
    inbound: dict[Path, set[Path]] = {}
    referenced_assets: set[Path] = set()
    for markdown_file in sorted(NARRATIVE_DIR.rglob("*.md")):
        for target in markdown_links(markdown_file):
            resolved = resolve_link(markdown_file, target)
            if resolved is None:
                continue
            if not resolved.exists():
                errors.append(
                    f"Broken local link in {repo_relative(markdown_file)}: {target}"
                )
                continue
            if resolved.suffix == ".md":
                inbound.setdefault(resolved, set()).add(markdown_file)
            if ASSETS_DIR in resolved.parents:
                referenced_assets.add(resolved)
    return errors, inbound, referenced_assets


def reachable_markdown() -> set[Path]:
    start = NARRATIVE_DIR / "index.md"
    seen: set[Path] = set()
    queue: deque[Path] = deque([start])
    while queue:
        current = queue.popleft().resolve()
        if current in seen or not current.exists():
            continue
        seen.add(current)
        for target in markdown_links(current):
            resolved = resolve_link(current, target)
            if resolved is None or resolved.suffix != ".md":
                continue
            if NARRATIVE_DIR in resolved.parents or resolved == NARRATIVE_DIR:
                queue.append(resolved)
    return seen


def staged_raw_imports() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return [f"Unable to inspect staged files: {result.stderr.strip()}"]
    staged = []
    for line in result.stdout.splitlines():
        path = Path(line)
        if (
            line.startswith("research/hmrc-beyond-hype/import/")
            and path.suffix.lower() in RAW_IMPORT_SUFFIXES
        ):
            staged.append(line)
    return staged


def validate() -> dict[str, object]:
    errors: list[str] = []
    required_files = [
        NARRATIVE_DIR / "index.md",
        NARRATIVE_DIR / "overview.md",
        NARRATIVE_DIR / "topics.md",
        NARRATIVE_DIR / "narrative-arc.md",
        NARRATIVE_DIR / "source-materials.md",
        DATA_DIR / "visual_coverage.md",
        DATA_DIR / "visual_coverage.csv",
    ]
    for path in required_files:
        if not path.exists():
            errors.append(f"Missing required narrative file: {repo_relative(path)}")

    expected = expected_counts()
    coverage = load_coverage()
    by_source: dict[str, list[dict[str, str]]] = {}
    for row in coverage:
        by_source.setdefault(row["source_id"], []).append(row)

    for source_id, expected_count in expected.items():
        actual = len(by_source.get(source_id, []))
        if actual != expected_count:
            errors.append(
                f"Coverage mismatch for {source_id}: expected {expected_count}, got {actual}"
            )

    sidecar_paths: set[Path] = set()
    asset_paths: set[Path] = set()
    for row in coverage:
        sidecar = REPO_ROOT / row["sidecar_path"]
        asset = REPO_ROOT / row["asset_path"]
        sidecar_paths.add(sidecar)
        asset_paths.add(asset)
        if not sidecar.exists():
            errors.append(f"Missing sidecar: {row['sidecar_path']}")
            continue
        if not asset.exists():
            errors.append(f"Missing derived asset: {row['asset_path']}")
        text = sidecar.read_text(encoding="utf-8")
        for field in REQUIRED_SIDECAR_FIELDS:
            if field not in text:
                errors.append(f"{row['sidecar_path']} missing required field {field}")
        if "## Material Points Illustrated" not in text:
            errors.append(f"{row['sidecar_path']} missing material-points section")
        if "## Caveats" not in text:
            errors.append(f"{row['sidecar_path']} missing caveats section")

    link_errors, inbound, referenced_assets = validate_links()
    errors.extend(link_errors)

    all_markdown = {path.resolve() for path in NARRATIVE_DIR.rglob("*.md")}
    reachable = reachable_markdown()
    orphans = sorted(all_markdown - reachable)
    for orphan in orphans:
        errors.append(f"Orphaned narrative Markdown file: {repo_relative(orphan)}")

    for sidecar in sorted(sidecar_paths):
        inbound_sources = inbound.get(sidecar.resolve(), set())
        if not inbound_sources:
            errors.append(f"Sidecar has no inbound Markdown link: {repo_relative(sidecar)}")

    actual_assets = {path.resolve() for path in ASSETS_DIR.rglob("*") if path.is_file()}
    missing_asset_refs = sorted(actual_assets - {path.resolve() for path in referenced_assets})
    for asset in missing_asset_refs:
        errors.append(f"Derived asset is not referenced by Markdown: {repo_relative(asset)}")

    staged = staged_raw_imports()
    for path in staged:
        errors.append(f"Raw imported binary/media file is staged: {path}")

    return {
        "ok": not errors,
        "errors": errors,
        "expected_counts": expected,
        "covered_items": len(coverage),
        "markdown_files": len(all_markdown),
        "asset_files": len(actual_assets),
        "orphan_count": len(orphans),
        "sidecar_count": len(sidecar_paths),
    }


def write_report(result: dict[str, object]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    json_path = DATA_DIR / "narrative_validation_report.json"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    status = "passed" if result["ok"] else "failed"
    expected_rows = "\n".join(
        f"- `{source_id}`: {count} item(s)"
        for source_id, count in sorted(result["expected_counts"].items())
    )
    errors = result["errors"]
    if errors:
        error_block = "\n".join(f"- {error}" for error in errors)
    else:
        error_block = "- None"
    md_path = DATA_DIR / "narrative_validation_report.md"
    md_path.write_text(
        f"""{GENERATED_MARKER}
# Narrative Validation Report

Status: {status}.

## Counts

- Covered visual items: {result["covered_items"]}
- Sidecar files: {result["sidecar_count"]}
- Narrative Markdown files: {result["markdown_files"]}
- Derived asset files: {result["asset_files"]}
- Orphaned Markdown files: {result["orphan_count"]}

## Expected Coverage By Source

{expected_rows}

## Errors

{error_block}
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    if args.write_report:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        placeholder = DATA_DIR / "narrative_validation_report.md"
        if not placeholder.exists():
            placeholder.write_text(
                f"{GENERATED_MARKER}\n# Narrative Validation Report\n\nStatus: pending.\n",
                encoding="utf-8",
            )
    result = validate()
    if args.write_report:
        write_report(result)
    if result["ok"]:
        print(
            "Narrative sidecar validation passed: "
            f"{result['covered_items']} items, "
            f"{result['markdown_files']} Markdown files, "
            f"{result['asset_files']} assets."
        )
        return 0
    print("Narrative sidecar validation failed.", file=sys.stderr)
    for error in result["errors"]:
        print(f"- {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
