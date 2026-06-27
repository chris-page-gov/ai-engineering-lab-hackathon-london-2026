# Repository Operating Rules

These rules apply to the whole repository. More specific `AGENTS.md` files, such as `challenge-2/AGENTS.md`, add rules for their own folders.

## Documentation Lockstep

Keep repository documentation in lockstep with implementation changes.

- Update `Changelog.md` for every meaningful repo change. Use dated entries and group work under Added, Changed, Fixed, Removed, Security, or Documentation.
- Update `Context.md` when project purpose, architecture, data assumptions, operating constraints, or important decisions change.
- Update `Progress.md` when task status, completed work, current blockers, validation results, or next steps change.
- Update `README.md` or challenge briefs when a user-facing workflow, setup step, demo path, or included material changes.
- If a change genuinely does not need one of these updates, say why in the PR or final response.
- Run `python3 tools/check_documentation_lockstep.py` before submitting changes that touch code, generated artefacts, challenge docs, or repository operations.
- For published wiki Markdown changes, keep OKF frontmatter in place and run `python3 scripts/check_okf_conformance.py`.
- If `challenge-2/wiki/**/*.md` or `postmortem-public/wiki/**/*.md` changes, run `python3 scripts/update_viewer.py` and `python3 scripts/check_wiki_viewer.py` so root `viewer.html` stays synchronized for GitHub publication.
- Before publishing the wiki site, run `python3 scripts/build_site.py`; `_site/` is generated output and should not be committed.

## Source Data

- Treat challenge starter data as source material. Do not edit, rename, move, redact, or normalise files in `challenge-*/structured_files/`, `challenge-*/unstructured_files/`, or other raw-data folders unless the user explicitly requests it.
- Challenge fixture data is synthetic unless a brief says otherwise. Do not redact synthetic names, contact-like values, roles, or identifiers just because they resemble personal data.
- Do still flag real secrets, credentials, local filesystem paths, broken links, malformed generated content, and provenance gaps.

## Change Hygiene

- Prefer small, reviewable changes.
- Keep generated artefacts reproducible from their source scripts.
- Do not commit local application state, screenshots, caches, or `.DS_Store` files unless they are intentionally part of the demo.
- Treat `challenge-2/.obsidian/workspace.json` as local workspace state unless intentionally updating default vault layout.

## Validation

- Run the narrowest relevant validation before finishing.
- For Challenge 2 wiki changes, run `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`.
- Run the full Challenge 2 strict build only when generated wiki output should be refreshed, because it appends to `wiki/log.md` and updates generated timestamps.
- For OKF/publication changes, run `python3 scripts/check_okf_conformance.py` and `python3 scripts/check_wiki_viewer.py`.
- For GitHub Pages publication changes, run `python3 scripts/build_site.py` and leave `_site/` ignored.
- Run `python3 tools/check_documentation_lockstep.py` to verify that `Changelog.md`, `Context.md`, and `Progress.md` were updated with meaningful repo changes.
