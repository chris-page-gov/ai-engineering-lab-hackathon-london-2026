#!/usr/bin/env python3
"""Lint the Challenge 2 MCP research wiki.

The checks stay dependency-free so the wiki can be validated on a clean
developer machine and in CI without adding another markdown toolchain.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
DATA_DIR = ROOT / "data"
RAW_REPORT = Path("research/Challenge 2 Wiki MCP Server Research Report.md")
FRONTMATTER_EXEMPTIONS = {
    RAW_REPORT,
    Path("AGENTS.md"),
}
OPAQUE_MARKER_EXEMPTIONS = {
    RAW_REPORT,
}
REQUIRED_NAV_FILES = [
    Path("index.md"),
    Path("architecture.md"),
    Path("implementation-plan.md"),
    Path("security-model.md"),
    Path("decision-record.md"),
    Path("wiki-optimization-log.md"),
    Path("candidate-register.md"),
    Path("sources/bibliography.md"),
    Path("research/index.md"),
    Path("data/source-register.json"),
    Path("data/bibliography.json"),
    Path("data/candidate-register.json"),
]


MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^]\n|#]+)(?:#[^]\n|]+)?(?:\|[^]\n]+)?\]\]")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def strip_quotes(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object] | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    raw = text[4:end].splitlines()
    data: dict[str, object] = {}
    current_key: str | None = None
    for line in raw:
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(strip_quotes(line[4:]))
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            data[key] = strip_quotes(value) if value else []
    return data, text[end + 5 :]


def is_external_target(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme in {"http", "https", "mailto", "wiki"}


def normalize_target(target: str) -> str:
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target and not target.startswith("<"):
        target = target.strip()
    target = target.split("#", 1)[0]
    target = target.split("?", 1)[0]
    return unquote(target)


def resolve_local_target(source_file: Path, target: str) -> Path | None:
    target = normalize_target(target)
    if not target or target.startswith("#") or is_external_target(target):
        return None
    candidate = (source_file.parent / target).resolve()
    return candidate


def collect_links(source_file: Path, text: str) -> list[tuple[str, Path | None]]:
    links: list[tuple[str, Path | None]] = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group(1)
        links.append((target, resolve_local_target(source_file, target)))
    for match in WIKILINK_RE.finditer(text):
        target = match.group(1)
        if not target.endswith(".md"):
            target = f"{target}.md"
        links.append((target, resolve_local_target(source_file, target)))
    return links


def related_links(frontmatter: dict[str, object] | None, source_file: Path) -> list[Path]:
    if not frontmatter:
        return []
    values = frontmatter.get("related")
    if not isinstance(values, list):
        return []
    paths: list[Path] = []
    for value in values:
        if not isinstance(value, str) or is_external_target(value):
            continue
        target = resolve_local_target(source_file, value)
        if target:
            paths.append(target)
    return paths


def has_required_frontmatter(frontmatter: dict[str, object]) -> tuple[bool, list[str]]:
    missing: list[str] = []
    if not frontmatter.get("title"):
        missing.append("title")
    if not any(frontmatter.get(key) for key in ("note_type", "source_type", "artifact_type")):
        missing.append("note_type/source_type/artifact_type")
    tags = frontmatter.get("tags")
    if not isinstance(tags, list) or not tags:
        missing.append("tags")
    return not missing, missing


def load_json(path: Path, errors: list[dict[str, object]]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - lint report should capture exact parser failure.
        errors.append({"type": "json_parse", "file": rel(path), "message": str(exc)})
        return None


def check_source_ids(
    name: str,
    values: object,
    id_field: str,
    errors: list[dict[str, object]],
) -> None:
    if not isinstance(values, list):
        errors.append({"type": "json_shape", "file": name, "message": "expected a list"})
        return
    seen: set[str] = set()
    for item in values:
        if not isinstance(item, dict):
            errors.append({"type": "json_shape", "file": name, "message": "list item is not an object"})
            continue
        source_id = item.get(id_field)
        if not isinstance(source_id, str) or not source_id:
            errors.append({"type": "missing_id", "file": name, "field": id_field, "item": item})
            continue
        if source_id in seen:
            errors.append({"type": "duplicate_id", "file": name, "field": id_field, "id": source_id})
        seen.add(source_id)


def tracked_files(paths: list[Path]) -> set[str]:
    if not paths:
        return set()
    repo_relative = [path.relative_to(REPO_ROOT).as_posix() for path in paths]
    try:
        result = subprocess.run(
            ["git", "ls-files", "--", *repo_relative],
            cwd=REPO_ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except OSError:
        return set()
    return set(result.stdout.splitlines())


def write_reports(report: dict[str, object]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "lint-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    summary = report["summary"]
    status = report["status"]
    errors = report["errors"]
    warnings = report["warnings"]
    lines = [
        "---",
        'title: "MCP Wiki Lint Report"',
        'note_type: "lint-report"',
        'generated_by: "tools/lint_mcp_wiki.py"',
        f'status: "{status}"',
        "tags:",
        '  - "mcp"',
        '  - "lint"',
        '  - "quality-gate"',
        "search_terms:",
        '  - "mcp wiki lint"',
        '  - "broken links"',
        '  - "frontmatter coverage"',
        "related:",
        '  - "index.md"',
        '  - "wiki-optimization-log.md"',
        '  - "data/lint-report.json"',
        "---",
        "",
        "# MCP Wiki Lint Report",
        "",
        f"Generated: `{report['created_at']}`",
        "",
        f"Status: **{status.upper()}**",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key, value in summary.items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Errors", ""])
    if errors:
        for item in errors:
            lines.append(f"- `{item.get('type')}` in `{item.get('file')}`: {item}")
    else:
        lines.append("- None.")
    lines.extend(["", "## Warnings", ""])
    if warnings:
        for item in warnings:
            lines.append(f"- `{item.get('type')}` in `{item.get('file')}`: {item}")
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Related",
            "",
            "- [Wiki index](index.md)",
            "- [Optimization log](wiki-optimization-log.md)",
            "- [Bibliography](sources/bibliography.md)",
            "- [Machine-readable lint report](data/lint-report.json)",
            "",
        ]
    )
    (ROOT / "lint-report.md").write_text("\n".join(lines), encoding="utf-8")


def run() -> dict[str, object]:
    errors: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []
    metrics: dict[str, dict[str, int | bool]] = {}

    for required in REQUIRED_NAV_FILES:
        if not (ROOT / required).exists():
            errors.append({"type": "missing_required_file", "file": required.as_posix()})

    markdown_files = sorted(ROOT.rglob("*.md"))
    total_internal_links = 0
    total_external_links = 0
    frontmatter_count = 0
    missing_search_terms = 0

    for path in markdown_files:
        relative = Path(rel(path))
        text = path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(text)
        links = collect_links(path, text)
        related = related_links(frontmatter, path)
        local_link_count = sum(1 for _, target in links if target is not None) + len(related)
        external_link_count = sum(
            1
            for target, resolved in links
            if resolved is None and is_external_target(normalize_target(target))
        )
        total_internal_links += local_link_count
        total_external_links += external_link_count

        if "" in text and relative not in OPAQUE_MARKER_EXEMPTIONS:
            errors.append(
                {
                    "type": "opaque_deep_research_marker",
                    "file": relative.as_posix(),
                    "message": "opaque Deep Research citation markers are only allowed in the raw report",
                }
            )

        if relative not in FRONTMATTER_EXEMPTIONS:
            if frontmatter is None:
                errors.append({"type": "missing_frontmatter", "file": relative.as_posix()})
            else:
                frontmatter_count += 1
                ok, missing = has_required_frontmatter(frontmatter)
                if not ok:
                    errors.append(
                        {
                            "type": "incomplete_frontmatter",
                            "file": relative.as_posix(),
                            "missing": missing,
                        }
                    )
                search_terms = frontmatter.get("search_terms")
                if not isinstance(search_terms, list) or not search_terms:
                    missing_search_terms += 1
                    warnings.append(
                        {
                            "type": "missing_search_terms",
                            "file": relative.as_posix(),
                            "message": "tags are present, but search_terms would improve retrieval experiments",
                        }
                    )

        for original, target in links:
            normalized = normalize_target(original)
            if not normalized or is_external_target(normalized):
                continue
            if not target or not target.exists():
                errors.append(
                    {
                        "type": "broken_internal_link",
                        "file": relative.as_posix(),
                        "target": original,
                    }
                )
        for target in related:
            if not target.exists():
                errors.append(
                    {
                        "type": "broken_related_link",
                        "file": relative.as_posix(),
                        "target": str(target),
                    }
                )

        if relative not in FRONTMATTER_EXEMPTIONS and local_link_count < 2:
            warnings.append(
                {
                    "type": "low_cross_link_count",
                    "file": relative.as_posix(),
                    "count": local_link_count,
                }
            )

        metrics[relative.as_posix()] = {
            "has_frontmatter": frontmatter is not None,
            "internal_link_count": local_link_count,
            "external_link_count": external_link_count,
            "opaque_marker_exempt": relative in OPAQUE_MARKER_EXEMPTIONS,
        }

    ds_store_files = list(ROOT.rglob(".DS_Store"))
    tracked_ds_store = tracked_files(ds_store_files)
    for ds_store in ds_store_files:
        repo_path = ds_store.relative_to(REPO_ROOT).as_posix()
        if repo_path in tracked_ds_store:
            errors.append({"type": "tracked_ds_store_present", "file": rel(ds_store)})

    source_register = load_json(DATA_DIR / "source-register.json", errors)
    bibliography = load_json(DATA_DIR / "bibliography.json", errors)
    candidates = load_json(DATA_DIR / "candidate-register.json", errors)
    check_source_ids("data/source-register.json", source_register, "source_id", errors)
    check_source_ids("data/bibliography.json", bibliography, "source_id", errors)
    check_source_ids("data/candidate-register.json", candidates, "name", errors)

    if isinstance(source_register, list):
        for item in source_register:
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                continue
            target = ROOT / item["path"]
            if not target.exists():
                errors.append(
                    {
                        "type": "source_register_path_missing",
                        "file": "data/source-register.json",
                        "source_id": item.get("source_id"),
                        "target": item["path"],
                    }
                )

    summary = {
        "markdown_files": len(markdown_files),
        "frontmatter_files": frontmatter_count,
        "internal_links": total_internal_links,
        "external_links": total_external_links,
        "errors": len(errors),
        "warnings": len(warnings),
        "missing_search_terms": missing_search_terms,
        "ignored_ds_store_files": len(ds_store_files) - len(tracked_ds_store),
    }
    return {
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": str(ROOT),
        "status": "pass" if not errors else "fail",
        "summary": summary,
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true", help="write lint-report.md and data/lint-report.json")
    args = parser.parse_args()

    report = run()
    if args.write_report:
        write_reports(report)
    print(json.dumps({"status": report["status"], "summary": report["summary"]}, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
