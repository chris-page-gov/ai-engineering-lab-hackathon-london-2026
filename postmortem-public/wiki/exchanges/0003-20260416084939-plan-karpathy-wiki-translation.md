---
exchange_id: "EX-0003"
title: "Plan Karpathy Wiki Translation"
source_id: "CONV-002"
global_sequence: 3
session_sequence: 1
user_timestamp: "2026-04-16T08:51:25.593Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0003. Plan Karpathy Wiki Translation

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-002 (Karpathy Wiki Planning and Challenge 2 Vault Build)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
We are going to do Challenge 2, the aim is to use the Karpathy Wiki method to translate the documents, including all metadata, into a knowledge base which Obsidian can navigate well.

Give us a plan
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-16T08:51:30.633Z`

````text
I’ll inspect the repo first so the plan matches the actual challenge materials, document formats, and any existing Obsidian or ingestion structure. Then I’ll ask only for the choices that are genuinely product-level, such as translation target languages or how strict you want metadata preservation to be.
````

### Response 2 (commentary)

- Timestamp: `2026-04-16T08:51:38.159Z`

````text
I found Challenge 2 materials split into structured and unstructured source sets, with PDFs, DOCX, XLSX, HTML, Markdown, and text. Next I’m reading the challenge brief and sampling source files to understand required outputs, metadata already present, and the likely shape of an Obsidian vault.
````

### Response 3 (commentary)

- Timestamp: `2026-04-16T08:51:51.823Z`

````text
I’m going to check whether the repo already mentions Karpathy/Obsidian, then I’ll verify the method externally because the name is specific and easy to misinterpret. After that I can turn the plan into a concrete vault-and-pipeline design rather than a generic extraction plan.
````

### Response 4 (commentary)

- Timestamp: `2026-04-16T08:52:15.243Z`

````text
I confirmed the local brief and the live Karpathy gist. The important fit is strong: raw sources stay immutable, the LLM-maintained layer becomes interlinked Markdown, `index.md` and `log.md` act as navigation and audit spine, and lint passes find stale claims, contradictions, orphan pages, and missing links.
````

### Response 5 (commentary)

- Timestamp: `2026-04-16T08:53:06.245Z`

````text
I’ll base the plan on all 43 Challenge 2 documents, treating “translate” as conversion into a maintained Markdown wiki rather than language translation. I’m checking available local extraction tooling now, so the plan can name a realistic pipeline instead of assuming tools that may not exist.
````

### Response 6 (commentary)

- Timestamp: `2026-04-16T08:53:15.745Z`

````text
The environment has `pdftotext`, `pdfinfo`, `pandoc`, and `exiftool`, but not the Python document libraries preinstalled. That pushes the plan toward a low-friction MVP using existing CLI tools plus small Python standard-library glue, with optional package installation only if the team wants richer DOCX/XLSX parsing.
````

### Response 7 (final_answer)

- Timestamp: `2026-04-16T08:54:26.468Z`

````text
<proposed_plan>
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
</proposed_plan>
````

## Contribution Reading

- User contribution: Set the strategic goal and named the Karpathy Wiki method as the design frame.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.
