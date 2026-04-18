---
exchange_id: "EX-0004"
title: "Implement Karpathy Wiki Vault"
source_id: "CONV-002"
global_sequence: 4
session_sequence: 2
user_timestamp: "2026-04-16T08:57:43.861Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0004. Implement Karpathy Wiki Vault

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-002 (Karpathy Wiki Planning and Challenge 2 Vault Build)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
PLEASE IMPLEMENT THIS PLAN:
# Challenge 2 Obsidian Knowledge Base Plan

## Summary
Build Challenge 2 as a Karpathy-style LLM Wiki: raw source documents stay immutable, an LLM-maintained Markdown wiki becomes the navigable knowledge layer, and schema/index/log files keep the system disciplined. This follows the pattern in Karpathy’s [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): raw sources, generated wiki, and explicit operating rules.

Use all Challenge 2 documents: 20 structured files and 23 unstructured files from [challenge-2]([LOCAL_REPO]/challenge-2). “Translate” means format translation into Obsidian-friendly Markdown, not natural-language translation.

## Key Changes
- Treat `challenge-2/` as the Obsidian vault root so source files, generated notes, and links live together.
- Add a generated wiki layer under `challenge-2/wiki/`:
  - `index.md`: content catalogue and primary navigation.
  - `log.md`: append-only ingest/query/lint history.
  - `sources/`: one note per original document.
  - `topics/`: synthesized policy/topic pages such as Housing Benefit, DHPs, Flexible Working, Procurement, Data Protection, FOI, HR Policies.
  - `entities/`: departments, teams, roles, legislation, forms, and named programmes.
  - `maps/`: maps of content for Housing and Benefits, Small Business and Employment, Corporate Operations, People Policies, and Risk/Assurance.
- Add `challenge-2/AGENTS.md` as the wiki operating schema: raw sources are read-only, every generated note needs YAML frontmatter, every claim needs source provenance, and every ingest updates `index.md` and `log.md`.
- Add lightweight extraction tooling under `challenge-2/tools/`:
  - Inventory every source file with path, format, size, SHA-256, technical metadata, and extraction status.
  - Extract Markdown/HTML/TXT directly.
  - Extract PDFs with `pdftotext`, `pdfinfo`, and `exiftool`.
  - Extract DOCX with `pandoc` plus DOCX core-property metadata.
  - Extract XLSX with `openpyxl` via `uv`, converting each worksheet to Markdown tables plus structured JSON.

## Metadata And Interfaces
- Preserve metadata in three places:
  - YAML frontmatter for Obsidian navigation and Dataview-style filtering.
  - A visible “Metadata” section inside each source note.
  - A machine-readable source register, `challenge-2/wiki/data/source-register.json`.
- Use this canonical frontmatter shape for source notes:

```yaml
source_id: DOC-HB-002
title: "Discretionary Housing Payments: Guidance for Local Authority Administration"
source_path: "../structured_files/DOC-HB-002-discretionary-housing-payments.md"
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
extraction:
  method: "markdown-frontmatter"
  quality: "high"
  warnings: []
sensitivity:
  contains_personal_data: false
  classification: null
```

- Keep raw metadata exactly as found, even when inconsistent. Normalised fields support navigation; raw fields support audit.
- Use relative Markdown links throughout so the wiki works in Obsidian, VS Code, and GitHub.
- Use Obsidian aliases and tags, but avoid Obsidian-only syntax where a normal Markdown fallback is needed.

## Build Flow
1. Inventory: scan all 43 files, fingerprint them, capture technical metadata, and create the source register.
2. Extract: convert each document into Markdown-like content while retaining headings, pages, sections, tables, and worksheets.
3. Generate source notes: one note per document with summary, extracted structure, metadata, tables, provenance, and related links.
4. Generate synthesis notes: create topic/entity pages that compile repeated concepts once, instead of rediscovering them on every query.
5. Link: auto-link document IDs, titles, departments, legislation, “see also” references, supersession relationships, stale-review dates, and draft/current conflicts.
6. Lint: report broken links, missing metadata, orphan notes, unrepresented sources, stale policies, contradictions, and low-quality extraction.
7. Demo: open the vault at `challenge-2/`, show `wiki/index.md`, graph navigation, maps of content, source provenance, and a few policy questions answered from linked notes.

## Test Plan
- Source coverage: all 43 Challenge 2 files have one source note and one source-register entry.
- Metadata coverage: every note has valid YAML frontmatter, source path, source format, extraction method, and provenance.
- Link integrity: all internal Markdown links resolve; no source note is orphaned.
- Known challenge checks:
  - Flag `DOC-HB-003` as stale/conflicted because `DOC-HB-009` says it replaces the March 2024 version.
  - Flag `DOC-HB-006` as superseded.
  - Flag `Information Security Policy - DRAFT v0.8.docx` as draft.
  - Flag `travel-and-subsistence-policy-v2.0.docx` as past review because it says next review was April 2022.
  - Capture the spending-controls PDF table into a navigable Markdown table.
  - Capture all three XLSX workbooks by sheet, including Procurement Thresholds and Staff Directory.
- Demo questions:
  - “Which Council Tax Reduction guidance is current?”
  - “Can a self-employed person claim Housing Benefit?”
  - “Which staff policies are draft, stale, or past review?”
  - “What approvals are needed for IT hardware over £5,000?”
  - “Which documents mention Discretionary Housing Payments?”

## Assumptions
- The prototype does not require a runtime LLM API. The coding agent can build and maintain the wiki, while deterministic scripts provide repeatable extraction and linting.
- Raw files under `structured_files/` and `unstructured_files/` are never modified.
- Synthetic personal data in the staff directory can be included for the demo, but it must be tagged as personal-data-like content and handled as sensitive in the metadata.
- The first demo prioritises provenance, versioning, findability, and contradiction detection over a polished chat UI.
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-16T08:57:47.471Z`

````text
I’ll implement the vault artifacts and repeatable tooling now. I’ll first inspect the source document structures a bit more and then add a generator/linter that produces the wiki without modifying the raw files.
````

### Response 2 (commentary)

- Timestamp: `2026-04-16T08:58:04.608Z`

````text
I’m going to use `uv` with `openpyxl` for the spreadsheet path, and otherwise rely on the tools already present here: `pandoc` for DOCX/HTML, `pdftotext`/`pdfinfo` for PDFs, and `exiftool` for file metadata. The generator will own only `challenge-2/wiki/` and will leave the raw source folders untouched.
````

### Response 3 (commentary)

- Timestamp: `2026-04-16T08:58:39.076Z`

````text
I’ve got enough context to make the code changes. I’m adding a single repeatable builder/linter script plus the vault operating instructions, then I’ll run the generator to materialise the wiki and validate coverage/linking.
````

### Response 4 (commentary)

- Timestamp: `2026-04-16T09:01:39.098Z`

````text
The initial script and operating rules are in place. I’m going to compile and run the builder now, expecting a first pass to expose any extraction edge cases from the mixed PDF/DOCX/XLSX corpus.
````

### Response 5 (commentary)

- Timestamp: `2026-04-16T09:01:45.894Z`

````text
The first run found a path bug in the script root calculation: it was looking for `structured_files/` at the repository root instead of inside `challenge-2/`. I’m correcting that and rerunning.
````

### Response 6 (commentary)

- Timestamp: `2026-04-16T09:02:01.864Z`

````text
The builder now processes all 43 files and generates 78 notes, but strict lint is catching broken internal links. I’m reading the lint output and generated samples, then I’ll tighten link generation and rerun.
````

### Response 7 (commentary)

- Timestamp: `2026-04-16T09:02:41.620Z`

````text
The broken-link set is all generator hygiene: generated `lint-report` links were checked before the report file existed, source HTML root links like `/benefits` were treated as local files, and short summaries were preserving raw Markdown links from source snippets. I also found two source-ID normalisation bugs where cross-references were mistaken for document IDs; I’m fixing those before the next strict run.
````

### Response 8 (commentary)

- Timestamp: `2026-04-16T09:03:11.184Z`

````text
The strict build now passes: 43 sources, 79 Markdown notes, and zero lint issues. I’m doing a quality pass over the generated index, source register, known flags, XLSX table outputs, and representative extracted notes before I call it done.
````

### Response 9 (commentary)

- Timestamp: `2026-04-16T09:03:35.014Z`

````text
The generated vault is valid, but I’m tightening quality before the final pass: PDF titles were inheriting placeholder metadata like `(anonymous)`, XLSX notes were named after their first worksheet, and a few topic keywords were too broad, pulling documents into unrelated topic pages. These are generator fixes, not raw-data changes.
````

### Response 10 (commentary)

- Timestamp: `2026-04-16T09:04:11.154Z`

````text
One more polish pass: I’m making protective markings behave as classification rather than titles, preserving year ranges in spreadsheet titles, and narrowing the small-business topic so National Insurance mentions in unrelated guidance do not over-link.
````

### Response 11 (commentary)

- Timestamp: `2026-04-16T09:04:47.165Z`

````text
The remaining gap against the test plan is the spending-controls PDF table: text extraction preserved the table visually, but not as a Markdown table. I’m adding a fixed-width table detector so PDF tables get an explicit `Extracted Tables` section while keeping the original extracted text intact for provenance.
````

### Response 12 (commentary)

- Timestamp: `2026-04-16T09:05:49.433Z`

````text
The spending-controls table is now present as a real Markdown table, with the original PDF extraction still below it. I’m checking the final file set and repository status now so I can give you a clean handover.
````

### Response 13 (final_answer)

- Timestamp: `2026-04-16T09:06:50.815Z`

````text
Implemented the Challenge 2 Obsidian knowledge base.

Key entry points:
- Operating schema: [AGENTS.md]([LOCAL_REPO]/challenge-2/AGENTS.md:1)
- Repeatable builder/linter: [build_wiki.py]([LOCAL_REPO]/challenge-2/tools/build_wiki.py:1)
- Obsidian start page: [index.md]([LOCAL_REPO]/challenge-2/wiki/index.md:1)
- Lint report: [lint-report.md]([LOCAL_REPO]/challenge-2/wiki/lint-report.md:1)
- Source register: [source-register.json]([LOCAL_REPO]/challenge-2/wiki/data/source-register.json:1)

What was built:
- `challenge-2/` now works as the Obsidian vault root.
- `challenge-2/wiki/` contains 79 Markdown notes: 43 source notes, topic notes, entity notes, maps of content, index, log, and lint report.
- All 43 Challenge 2 source files are represented with unique source IDs.
- XLSX workbooks are converted to Markdown tables and exported as JSON/CSV under `wiki/data/tables/`.
- The spending-controls PDF now has an explicit Markdown table for the internal controls table, including `IT hardware | Over £5,000 | IT Asset Board`.
- Known challenge flags are surfaced: stale `DOC-HB-003`, superseded `DOC-HB-006`, draft information security policy, staff directory sensitivity, and stale travel policy review date.

Validation passed:
```text
uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py
uv run --with openpyxl challenge-2/tools/build_wiki.py --strict
Built Challenge 2 wiki: 43 sources, 79 notes, 0 lint issues.
```

The raw `structured_files/` and `unstructured_files/` folders were not modified. I also left the pre-existing untracked `Review-*.md` files untouched.
````

## Contribution Reading

- User contribution: Approved implementation and supplied a detailed acceptance plan.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.
