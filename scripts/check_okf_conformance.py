#!/usr/bin/env python3
"""Check published Markdown wiki bundles against the local OKF v0.1 profile."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLES = [ROOT / "challenge-2" / "wiki", ROOT / "postmortem-public" / "wiki"]
REQUIRED_FIELDS = ("type", "title", "description", "timestamp")
KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*:\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s{2}-\s+.+$")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def split_frontmatter(text: str) -> tuple[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return text[4:end], text[end + 4 :].lstrip("\n")


def frontmatter_value(block: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", block, re.MULTILINE)
    return match.group(1).strip() if match else None


def non_empty(value: str | None) -> bool:
    if value is None:
        return False
    normalized = value.strip().strip("\"'")
    return bool(normalized and normalized not in {"[]", "{}"})


def frontmatter_syntax_errors(block: str) -> list[str]:
    errors: list[str] = []
    current_key_accepts_list = False
    for line_number, line in enumerate(block.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key_match = KEY_RE.match(line)
        if key_match:
            current_key_accepts_list = not key_match.group(1).strip()
            continue
        if LIST_ITEM_RE.match(line) and current_key_accepts_list:
            continue
        if line.startswith(" ") and (":" in stripped or stripped.startswith("-")):
            continue
        errors.append(f"line {line_number}: {line}")
    return errors


def check_bundle(bundle: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    if not bundle.exists():
        return count, errors

    root_index = bundle / "index.md"
    for path in sorted(bundle.rglob("*.md")):
        count += 1
        text = path.read_text(encoding="utf-8")
        frontmatter = split_frontmatter(text)
        if frontmatter is None:
            errors.append(f"{rel(path)}: missing or unterminated YAML frontmatter")
            continue

        block, body = frontmatter
        errors.extend(f"{rel(path)}: invalid frontmatter {error}" for error in frontmatter_syntax_errors(block))
        for field in REQUIRED_FIELDS:
            if not non_empty(frontmatter_value(block, field)):
                errors.append(f"{rel(path)}: missing required OKF frontmatter field {field}")

        if path == root_index and not non_empty(frontmatter_value(block, "okf_version")):
            errors.append(f"{rel(path)}: bundle root must declare okf_version")
        if path.name == "index.md" and "# " not in body:
            errors.append(f"{rel(path)}: index page should contain Markdown section content")

    return count, errors


def main() -> int:
    errors: list[str] = []
    checked = 0
    for bundle in BUNDLES:
        count, bundle_errors = check_bundle(bundle)
        checked += count
        errors.extend(bundle_errors)

    print(f"OKF markdown documents checked: {checked}")
    if errors:
        print("OKF conformance errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
