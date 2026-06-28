#!/usr/bin/env python3
"""Build the GitHub Pages static site into _site/."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"

PUBLIC_ROOT_FILES = [
    "viewer.html",
    "README.md",
    "START-HERE.md",
    "Changelog.md",
    "Context.md",
    "Progress.md",
    "challenge-01-from-pdf-to-digital-service.md",
    "challenge-02-unlocking-the-dark-data.md",
    "challenge-03-supporting-casework-decisions.md",
    "challenge-04-knowing-your-own-organisation.md",
    "open-brief.md",
    "SETUP-GUIDE.md",
]
PUBLIC_TREES = [
    "challenge-2/wiki",
    "challenge-2/structured_files",
    "challenge-2/unstructured_files",
    "output/doc/assets",
    "postmortem-public",
]
FORBIDDEN_NAMES = {".DS_Store"}
FORBIDDEN_PREFIXES = ("._", "~$")
FORBIDDEN_PARTS = {".git", ".obsidian", "__pycache__"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


def is_forbidden(path: Path) -> bool:
    return (
        path.name in FORBIDDEN_NAMES
        or path.name.startswith(FORBIDDEN_PREFIXES)
        or any(part in FORBIDDEN_PARTS for part in path.parts)
        or path.suffix.lower() in FORBIDDEN_SUFFIXES
    )


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def copy_public_tree(source_dir: Path, target_dir: Path) -> None:
    for source in source_dir.rglob("*"):
        if source.is_dir() or is_forbidden(source):
            continue
        copy_file(source, target_dir / source.relative_to(source_dir))


def assert_no_forbidden_files() -> None:
    errors: list[str] = []
    for path in OUT.rglob("*"):
        if path.is_file() and is_forbidden(path):
            errors.append(path.relative_to(OUT).as_posix())
    if errors:
        joined = "\n".join(f"- {error}" for error in errors)
        raise RuntimeError(f"forbidden files in site build:\n{joined}")


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for name in PUBLIC_ROOT_FILES:
        source = ROOT / name
        if source.exists():
            copy_file(source, OUT / name)

    copy_file(ROOT / "viewer.html", OUT / "index.html")

    for dirname in PUBLIC_TREES:
        copy_public_tree(ROOT / dirname, OUT / dirname)

    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "404.html").write_text(
        "<!doctype html><meta charset=\"utf-8\"><title>Challenge 2 Wiki</title>"
        "<meta http-equiv=\"refresh\" content=\"0; url=./\">"
        "<p>Return to <a href=\"./\">Challenge 2 Wiki</a>.</p>\n",
        encoding="utf-8",
    )

    assert_no_forbidden_files()
    file_count = sum(1 for path in OUT.rglob("*") if path.is_file())
    print(f"built {OUT.relative_to(ROOT)} with {file_count} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
