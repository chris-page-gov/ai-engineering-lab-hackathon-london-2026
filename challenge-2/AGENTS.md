# Challenge 2 LLM Wiki Operating Rules

This folder is an Obsidian vault for Challenge 2. It follows the Karpathy LLM Wiki pattern: raw documents are immutable sources, `wiki/` is the generated knowledge layer, and this file is the operating schema for future agents.

## Source Of Truth

- Treat `structured_files/` and `unstructured_files/` as read-only.
- Do not edit, rename, move, or normalise raw source files.
- Every generated claim must remain traceable to a source note and raw source path.
- Keep raw metadata exactly as found. Add normalised metadata separately for navigation and filtering.

## Synthetic Fixture Data

- All Challenge 2 raw and generated data is synthetic hackathon fixture data.
- Do not redact names, email-like values, phone-like values, roles, departments, or staff-directory entries solely because they resemble personal data.
- Preserve synthetic identifiers in generated notes, tables, CSV, and JSON so the demo remains navigable and auditable.
- Continue to flag real secrets, credentials, local filesystem paths, malformed links, bad provenance, and any data copied from outside the Challenge 2 synthetic corpus.

## Generated Wiki Contract

- Generated notes live under `wiki/`.
- Every note must have YAML frontmatter.
- Source notes live in `wiki/sources/`, one note per raw source file.
- Topic synthesis notes live in `wiki/topics/`.
- Entity notes live in `wiki/entities/`.
- Maps of content live in `wiki/maps/`.
- Machine-readable outputs live in `wiki/data/`.
- `wiki/index.md` is the content catalogue and primary navigation entrypoint.
- `wiki/architecture.md` is the plain-English architecture page for first-time readers and must stay prominent in `wiki/index.md`.
- `wiki/log.md` is an append-only chronological record of ingest, query, and lint events.

## Source Note Frontmatter

Use this shape for source notes:

```yaml
source_id: DOC-HB-002
title: "Discretionary Housing Payments: Guidance for Local Authority Administration"
source_path: "../../structured_files/DOC-HB-002-discretionary-housing-payments.md"
source_format: "md"
document_type: "procedural-manual"
department: "DLUHC"
owner: null
status: "current"
version: "2.1"
publication_date: "2025-03-01"
last_updated: "2025-09-15"
audience: ["Local authority housing officers"]
topics: ["housing-benefit", "discretionary-housing-payments"]
supersedes: ["DOC-HB-002 v1.4"]
related_sources: ["DOC-HB-001", "DOC-HB-008"]
tags: ["source", "challenge-2", "housing-benefit"]
data_origin: "synthetic_fixture"
extraction:
  method: "markdown-frontmatter"
  quality: "high"
  warnings: []
sensitivity:
  contains_real_personal_data: false
  contains_synthetic_identifiers: false
  classification: null
```

## Maintenance Workflow

1. Run `uv run challenge-2/tools/build_wiki.py` from the repository root.
2. Review `wiki/lint-report.md`.
3. Open `challenge-2/` as an Obsidian vault and start from `wiki/index.md`.
4. When adding new source documents, rerun the builder and check that `wiki/log.md` records the ingest.

## Linking And Provenance

- Use relative Markdown links so notes work in Obsidian, VS Code, and GitHub.
- Prefer stable descriptive filenames.
- Link source IDs, departments, legislation, forms, policies, and named programmes.
- Long notes should end with a "Related Notes" section.
- Flag stale, draft, superseded, contradictory, and low-confidence records rather than hiding them.
- Flag synthetic fixture identifiers as synthetic fixtures, not as real personal data.
