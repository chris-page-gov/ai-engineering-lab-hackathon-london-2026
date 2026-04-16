---
title: "Challenge 2 Demonstration Guide"
aliases:
  - "Demo Guide"
  - "Challenge 2 Functionality Showcase"
note_type: "demo-guide"
tags:
  - "challenge-2"
  - "demo"
  - "llm-wiki"
  - "dark-data-workbench"
updated: "2026-04-16"
---

# Challenge 2 Demonstration Guide

This page is the end-to-end demonstration route for Challenge 2. It shows how the wiki, Obsidian vault, SeeLinks-style workbench, browser AI export, benchmark, harness, and audit trail fit the challenge brief: make government "dark data" findable, structured, source-backed, and reviewable.

The slide deck frames the main principle clearly: provenance is the product. A useful AI answer is not just fluent text; it is an answer that can be traced to the exact source, version, status, supersession relationship, and extraction route that produced it.

## Demo Narrative

1. Start with the problem shown in [Unlocking Dark Data](../Unlocking_Dark_Data.pdf): government guidance is often published, but not genuinely findable.
2. Show the raw corpus: a mixed departmental drive with structured documents, binary documents, inconsistent statuses, draft material, stale material, spreadsheets, and PDFs.
3. Open the generated wiki in Obsidian and validate that it has topic pages, source pages, maps, search, backlinks, and machine-readable data.
4. Open the SeeLinks-style [Dark Data Workbench](workbench.md) and demonstrate filtered discovery, source inspection, saved checks, context-set construction, and graph/table views.
5. Export a selected evidence set to Browser AI with a "use only this context" prompt and source-ID citation policy.
6. Show the [Evaluation Benchmark](evaluation-benchmark.md), its 100 questions, 0-5 point rubrics, scoring caps, and comparative scoring design.
7. Run the evaluation harness and show that prompts, answers, source access, scoring sheets, audit cards, manifests, and FOI-ready bundles are recorded.

## Sources Used To Build The Wiki

The wiki is generated from the synthetic Challenge 2 source corpus. Raw sources stay immutable; generated notes and data live under `wiki/`.

| Source family | Count | Formats | What it represents | Links |
| --- | ---: | --- | --- | --- |
| Structured corpus | 20 | HTML, Markdown, plain text | Published-style guidance with metadata, policy pages, cross-domain references, and deliberate consistency traps. | [structured_files](../structured_files/) |
| Unstructured corpus | 23 | Word, PDF, Excel | Shared-drive material: policies, briefing packs, staff directories, performance frameworks, procurement tables, meeting minutes, and compliance reports. | [unstructured_files](../unstructured_files/) |
| Generated source notes | 43 | Markdown | One auditable note per raw source, with source ID, status, format, department, topics, provenance, extraction quality, warnings, and source path. | [Source corpus index](index.md#source-corpus) |
| Machine-readable register | 43 records | JSON | The queryable source inventory used by the workbench, MCP tools, and evaluation harness. | [source-register.json](data/source-register.json) |
| Tables and exports | Multiple | CSV, JSON | Extracted workbook/table views used for review and scoring. | [data](data/) |

Useful source examples:

| Demo point | Source note | Why it matters |
| --- | --- | --- |
| Current Council Tax Reduction guidance | [DOC-HB-009](sources/doc-hb-009-council-tax-reduction-schemes-prescribed-requirements-e.md) | Demonstrates a current source that replaces an older March 2024 version. |
| Stale status trap | [DOC-HB-003](sources/doc-hb-003-council-tax-reduction-schemes-regulatory-framework-and.md) | Marked current in its own metadata, but flagged as stale/conflicted because DOC-HB-009 replaces it. |
| Discretionary Housing Payments | [DOC-HB-002](sources/doc-hb-002-discretionary-housing-payments-guidance-for-local-autho.md) | Good source for showing exact policy answers with source-backed citations. |
| Superseded operational form guidance | [DOC-HB-006](sources/doc-hb-006-housing-benefit-claim-form-hb1-completion-instructions.md) | Demonstrates superseded-source handling. |
| Draft policy | [UF-INFORMATION-SECURITY-POLICY-DRAFT-V0-8](sources/uf-information-security-policy-draf-draft-not-for-distribution.md) | Demonstrates draft caveats and risk flags. |
| Synthetic staff directory | [UF-STAFF-DIRECTORY-EXTRACT-Q4-2023](sources/uf-staff-directory-extract-q4-2023-staff-directory-extract-q4-2023.md) | Demonstrates synthetic fixture identifiers and FOI/audit sensitivity handling. |
| IT hardware approval | [UF-SPENDING-CONTROLS-GUIDANCE](sources/uf-spending-controls-guidance-dwp-spending-controls-guidance.md) and [UF-PROCUREMENT-THRESHOLDS-2024-25](sources/uf-procurement-thresholds-2024-25-procurement-thresholds-2024-25.md) | Demonstrates multi-source evidence and spreadsheet/PDF extraction. |
| FOI response workflow | [UF-FOI-RESPONSE-TEMPLATE](sources/uf-foi-response-template-template-freedom-of-information-act-2000-response.md) | Demonstrates how audit packs support disclosure and reconstruction. |

The build logic is documented in [Architecture Overview](architecture.md). In short, `build_wiki.py` extracts metadata and text from the raw corpus, preserves the raw source path, generates source notes, derives topic/entity/map notes, writes machine-readable registers, then runs lint checks for metadata coverage, broken links, stale/draft/superseded flags, and known challenge traps.

## Obsidian Validation

Open `challenge-2/` as the Obsidian vault root, then start at [index.md](index.md). Obsidian gives basic human validation before any AI layer is involved.

What to show:

| Obsidian capability | Demo action | What it proves |
| --- | --- | --- |
| Vault navigation | Open [index.md](index.md), then [Architecture Overview](architecture.md), [Dark Data Workbench](workbench.md), and [Evaluation Benchmark](evaluation-benchmark.md). | The knowledge base has a human-readable entrypoint, not only machine data. |
| Topic selection | Open [Housing Benefit](topics/housing-benefit.md), [Council Tax Reduction](topics/council-tax-reduction.md), [Discretionary Housing Payments](topics/discretionary-housing-payments.md), and [FOI And Transparency](topics/foi-and-transparency.md). | Topics are built from source metadata and source-note links, so users can inspect the document set behind a theme. |
| Source validation | Open [DOC-HB-003](sources/doc-hb-003-council-tax-reduction-schemes-regulatory-framework-and.md) and [DOC-HB-009](sources/doc-hb-009-council-tax-reduction-schemes-prescribed-requirements-e.md) side by side. | The wiki exposes conflicting status and supersession evidence rather than hiding it. |
| Search | Search for `DHP`, `Council Tax Reduction`, `draft`, `past review`, `DOC-HB-009`, and `FOI`. | Plain search finds source notes, topic pages, and flags without requiring a bespoke app. |
| Graph and backlinks | Use Obsidian graph/backlinks from topic and source notes. | Relationships are visible as navigable evidence, not just opaque retrieval results. |
| Machine-readable validation | Open [source-register.json](data/source-register.json). | The same corpus can power Obsidian, UI filtering, MCP tools, and benchmark prompts. |

How topics were built:

1. Each source note carries normalised fields such as `source_id`, `status`, `source_format`, `department`, `topics`, `supersedes`, `related_sources`, and extraction warnings.
2. The builder groups source notes into topic pages, entity pages, maps of content, and the source corpus table in [index.md](index.md).
3. Topic pages link back to the exact source notes so a human can verify the synthesis in Obsidian.
4. The lint report checks whether known traps are visible, including stale/conflicted, draft, superseded, synthetic, and past-review records.

## SeeLinks UI: Dark Data Workbench

The [Dark Data Workbench](workbench.md) is the SeeLinks-style UI for the wiki. It lets a user state a question, move from broad search to a deliberate evidence set, and keep the question with the exported context before any AI answer is generated.

Run it with:

```bash
cd challenge-2/workbench
pnpm install
pnpm dev
```

Then open the local URL printed by Vite. The [workbench README](../workbench/README.md) lists the validation commands and the [Playwright tests](../workbench/tests/ui/workbench.spec.ts) capture the intended demo flows.

Start by entering a question in the question box. Saved checks also fill the box with their demo question, and Browser AI exports include that question in the JSON, copied prompt, and Markdown evidence bundle.

### Search Compared With Facets

Use this sequence to show why search alone is not enough:

| Check | Expected behaviour | Demo value |
| --- | --- | --- |
| Search `house` | Returns 10 broad matches, including housing guidance and unrelated occurrences where the substring appears in source text or metadata. | Shows that keyword search can be noisy and needs structured facets. |
| Search `housing` | Returns 19 broader matches across Housing Benefit, homelessness, Right to Buy, social housing, cross-domain notes, and internal documents. | Shows recall, but also why a user needs topic/status filters. |
| Facet `Topic: housing-benefit` | Narrows to 15 topic-backed Housing Benefit sources. | Shows curated classification rather than raw string matching. |
| Facet `Status: current` | Shows 17 current sources across the corpus. | Shows lifecycle filtering. |
| Combine topic/status and saved checks | Use the saved Council Tax Reduction check. It should include DOC-HB-009 and exclude DOC-HB-003. | Shows that provenance logic beats title matching when sources conflict. |
| Search `DHP` | Finds 2 direct text matches. | Shows exact acronym search. |
| Saved check `DHP mentions` | Returns 5 topic-backed DHP-related sources. | Shows how semantic/topic enrichment catches related evidence that direct acronym search misses. |
| Search `IT hardware` | Finds the spending-controls source. | Shows direct discovery. |
| Saved check `IT hardware over GBP 5,000` | Brings in procurement threshold evidence as well as spending-control evidence. | Shows cross-source answer construction. |

### Saved Checks To Demonstrate

The workbench includes saved checks in [model.ts](../workbench/src/lib/workbench/model.ts):

| Saved check | Good demo question | Expected evidence behaviour |
| --- | --- | --- |
| Current Council Tax Reduction guidance | Which CTR guidance is current? | `DOC-HB-009` should be visible; `DOC-HB-003` should be excluded because it is stale/conflicted. |
| Self-employed Housing Benefit | Can a self-employed person claim Housing Benefit? | Brings together self-employment and Housing Benefit sources including `DOC-SB-006`, `DOC-HB-001`, and `DOC-SB-002`. |
| Staff policy risks | Which staff policies are draft, stale, superseded, or past review? | Surfaces draft, superseded, synthetic, and past-review flags. |
| IT hardware over GBP 5,000 | What approvals are needed for IT hardware above GBP 5,000? | Uses procurement and spending-control evidence rather than a single free-text hit. |
| DHP mentions | Which documents mention Discretionary Housing Payments? | Uses topic tags and text search together. |

### Workbench Views

| View | Use it for |
| --- | --- |
| Grid | Quick triage of source cards, flags, formats, topics, and departments. |
| Reader | Inspect one source note, raw source path, status, department, format, topics, warnings, and related links. |
| Graph | Explain relationships between visible sources and topics. |
| Table | Compare source metadata in a compact review format. |
| Checks | Replay saved evidence checks for known challenge scenarios. |

## Browser AI With SeeLinks

The Browser AI mode deliberately separates evidence selection from answer generation.

Demo route:

1. In the workbench, enter "What are the gateway conditions for Discretionary Housing Payments?" in the question box.
2. Run the saved `DHP mentions` check or search for `DOC-HB-002`.
3. Add [DOC-HB-002](sources/doc-hb-002-discretionary-housing-payments-guidance-for-local-autho.md) to the context set.
4. Open the Browser AI panel.
5. Use `Copy JSON`, `Download JSON`, `Copy Prompt`, or `Evidence MD`.
6. Paste the prompt and JSON into a browser AI assistant.

The expected answer should cite `DOC-HB-002`, stay within the supplied context, and include any caveats from the selected source. The prompt tells the model to use only the exported context, cite `source_id` values, and respect the synthetic-data notice. This is the practical version of the slide-deck warning against a confident chat interface with weak provenance.

Browser AI is useful when teams do not have a backend model API during the hackathon. The workbench gives them a controlled evidence pack and a copyable prompt so the browser model can be used without pretending that retrieval, citation, and source selection are solved by the chat interface itself.

## MCP Use With SeeLinks

The workbench also includes a small local MCP-compatible server:

```bash
python3 challenge-2/tools/workbench_mcp.py
```

It exposes:

| Tool | Purpose |
| --- | --- |
| `workbench.search_sources` | Search and filter the same source register used by the UI. |
| `workbench.read_source` | Return one source note by source ID. |
| `workbench.build_context` | Build a Browser AI style evidence pack for selected source IDs. |

This makes the same source-selection discipline available to MCP clients, not just the browser UI.

## Evaluation Matrix

The [Evaluation Benchmark](evaluation-benchmark.md) is the scoring source of truth. It contains 100 source-backed questions, gold answers, per-question rubrics, and a summative regime for comparing Codex, Gemini CLI, and Claude Code on the same wiki-only task.

The design follows the scoring-guide image: [AI Benchmark Mastery Scoring Guide](../AI%20Benchmark%20Mastery%20Scoring%20Guide.png).

![AI Benchmark Mastery scoring guide](../AI%20Benchmark%20Mastery%20Scoring%20Guide.png)

Core scoring model:

| Element | Rule |
| --- | --- |
| Question count | 100 questions. |
| Per-question score | 0 to 5 points. |
| Maximum score | 500 points. |
| Perfect answer | Complete, source-backed, cites specific source IDs, and includes required caveats such as stale, draft, superseded, synthetic, or past-review status. |
| Automatic deductions | Missing citations or ignored risk flags should lose credit. |
| Hallucination cap | If an answer invents facts not supported by the wiki, the score is capped. |
| Tie-breakers | Risk flag accuracy, provenance matching, and hallucination count. |

Question families:

| Family | What it tests |
| --- | --- |
| Source inventory | Whether the model can identify counts, formats, source IDs, departments, and raw/source-note links. |
| Policy facts | Whether the model can answer domain questions from exact wiki sources. |
| Status and versioning | Whether stale, superseded, draft, and current records are handled correctly. |
| Cross-source synthesis | Whether the model can combine multiple source notes without inventing connecting facts. |
| Tables and spreadsheets | Whether workbook-derived evidence is used accurately. |
| Provenance and audit | Whether answers preserve source IDs, caveats, and reconstruction paths. |
| Negative controls | Whether the model refuses or limits answers when the wiki does not contain enough evidence. |

The 100 questions are intentionally visible to harness designers, but evaluated agents must be prevented from reading [evaluation-benchmark.md](evaluation-benchmark.md) while answering because it contains gold answers and rubrics.

## Evaluation Harness And Comparative Evaluation

The harness is documented in [challenge-2/evaluation/README.md](../evaluation/README.md). It sends the same wiki-only prompt to Codex, Gemini CLI, and Claude Code, records each answer, and emits scoring/audit artifacts.

Dry run:

```bash
python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients codex --questions Q001 --run-id smoke
```

Representative comparative run:

```bash
python3 challenge-2/tools/run_wiki_eval.py --clients codex,gemini,claude --run-id challenge2-full
```

After manual or assisted scoring, generate the leaderboard:

```bash
python3 challenge-2/tools/summarise_wiki_eval.py challenge-2/evaluation/runs/challenge2-full
```

Run outputs:

| Output | Purpose |
| --- | --- |
| `prompts/` | Exact prompt supplied to each client/question. |
| `answers/` | Raw captured model responses. |
| `generated/scoring-sheet.csv` | Human scoring sheet with question, client, score, citation, and comments fields. |
| `generated/leaderboard.json` and `generated/leaderboard.md` | Comparative score summary once scoring is filled in. |
| `audit/event-ledger.jsonl` | Event timeline for run setup, prompt dispatch, answer capture, tool activity, and finalisation. |
| `audit/source-register.json` | Sources and wiki files available to the run. |
| `audit/audit-card.json` | Run metadata, scope, client list, and summary. |
| `audit/integrity-manifest.json` | Hashes and integrity metadata for reconstruction. |
| `audit/redaction-manifest.json` | Redaction/disclosure decisions. |
| `audit/visible-transcript.md` | Human-readable reconstruction of prompts and answers. |
| `audit/*.zip` | DSAP-style audit bundle for sharing or FOI-style disclosure. |

The comparative evaluation is not only a leaderboard. It is also a way to test whether an AI agent actually uses the wiki as the source of truth, preserves caveats, and avoids making a polished answer out of unsupported memory.

## Audit And FOI Tracking

Audit and FOI tracking are built into both user-facing and evaluator-facing flows.

| Layer | What is recorded | FOI/audit value |
| --- | --- | --- |
| Source notes | Source ID, title, status, version, department, raw source path, extraction method, warnings, sensitivity flags, topics, related sources. | Lets a reviewer trace a claim back to an exact synthetic fixture document. |
| Source register | Machine-readable source metadata and flags. | Lets tools reconstruct the evidence universe used by a UI or harness run. |
| Workbench context export | Selected source IDs, note text, synthetic-data notice, answer policy, citation policy, and evidence markdown. | Shows what evidence a browser AI was allowed to use. |
| Workbench MCP | Search/read/context tool calls over the source register. | Makes source access explicit for MCP clients. |
| Evaluation harness | Prompts, answers, scoring sheet, event ledger, source register, audit card, integrity manifest, visible transcript, and zip bundle. | Supports replay, disclosure, and challenge scoring. |
| Wiki evaluation MCP | Controlled wiki search/read, public question retrieval, answer recording, and run finalisation. | Provides a fuller audit trail when clients use MCP rather than direct filesystem reads. |

Important limitation: direct filesystem reads by a CLI client cannot be proven by the harness alone. The MCP audit layer records access when clients use its tools, but a tool that reads files outside MCP must be controlled by prompt instructions, run isolation, and output review.

FOI examples to show:

- [UF-FOI-RESPONSE-TEMPLATE](sources/uf-foi-response-template-template-freedom-of-information-act-2000-response.md) as a source in the corpus.
- [FOI And Transparency](topics/foi-and-transparency.md) as a generated topic page.
- The evaluation audit bundle as the answer to "what did the model see, what did it say, and which sources support that answer?"

## Slide And Scoring Guide Evidence

The slide deck [Unlocking Dark Data](../Unlocking_Dark_Data.pdf) gives the policy and product framing for this demo:

| Slide theme | How the implementation responds |
| --- | --- |
| Published is not the same as findable | Obsidian wiki, source register, workbench search, facets, topic pages, and saved checks make the corpus navigable. |
| AI chat fails without machine-readable foundations | The wiki and source register create structured inputs before Browser AI or MCP answers are attempted. |
| Messy departmental drive | The corpus includes 20 structured files and 23 unstructured files across HTML, Markdown, text, Word, PDF, and Excel. |
| Use AI to build the pipeline | The repo shows an extraction/wiki pipeline, schema choices, UI layer, tests, and evaluation harness. |
| Anti-pattern: confident answer, weak provenance | Browser AI export and the benchmark require source IDs and caveats. |
| Three pathways | The prototype includes extraction pipeline, provenance-first index, and verified Q&A evaluation. |
| Anatomy of provenance-first response | Source notes and harness prompts require source citation, version/status, and caveats. |
| January 2026 AI-ready datasets | Metadata, governance, reproducibility, and audit are first-class outputs. |
| Provenance is the product | The demo centres on exact source, status, supersession, and reconstruction rather than generated prose alone. |

The scoring-guide image adds the evaluation framing:

- 100 questions.
- 0-5 points per question.
- 500-point maximum.
- Perfect answers need complete source-backed responses with citations and caveats.
- Missing citations, ignored flags, and hallucinations reduce or cap scores.
- Tie-breakers prioritise risk flag accuracy, provenance matching, and hallucination count.

## Recommended Live Demo Route

1. Open [index.md](index.md) in Obsidian and show the source corpus table.
2. Open [Council Tax Reduction](topics/council-tax-reduction.md), then compare [DOC-HB-003](sources/doc-hb-003-council-tax-reduction-schemes-regulatory-framework-and.md) with [DOC-HB-009](sources/doc-hb-009-council-tax-reduction-schemes-prescribed-requirements-e.md).
3. Open the workbench and run the saved Council Tax Reduction check.
4. Search `house`, then show how facets and saved checks improve the evidence set.
5. Add [DOC-HB-002](sources/doc-hb-002-discretionary-housing-payments-guidance-for-local-autho.md) to context and export Browser AI prompt/JSON.
6. Open [Evaluation Benchmark](evaluation-benchmark.md) and show the 100-question matrix, gold answers, rubrics, and scoring rules.
7. Run the dry-run harness command and point to the generated prompt, answer, scoring, and audit directories.
8. Close by showing the audit outputs and explaining how an FOI-style reconstruction would identify the prompt, answer, evidence set, and source files.

## Related Notes

- [Architecture Overview](architecture.md)
- [Dark Data Workbench](workbench.md)
- [Evaluation Benchmark](evaluation-benchmark.md)
- [Lint Report](lint-report.md)
- [Challenge 2 evaluation README](../evaluation/README.md)
- [Workbench README](../workbench/README.md)
