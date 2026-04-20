---
title: "MCP Wiki Optimization Log"
note_type: "decision-log"
status: "active"
tags:
  - "mcp"
  - "wiki-optimization"
  - "decision-log"
  - "lint"
search_terms:
  - "wiki optimisation"
  - "wiki optimization"
  - "cross linking"
  - "frontmatter"
  - "search tags"
related:
  - "index.md"
  - "decision-record.md"
  - "sources/bibliography.md"
  - "lint-report.md"
---

# MCP Wiki Optimization Log

This log records how the MCP research wiki is being shaped so humans and AI clients can navigate it predictably. It is deliberately separate from [the decision record](decision-record.md): the decision record captures durable choices, while this log captures the search, navigation, and validation changes used to make the wiki usable.

## 2026-04-20

| Change | Reason | Evaluation signal |
| --- | --- | --- |
| Added [the Codex MCP implementation and evaluation thread capture](sources/codex-thread-mcp-implementation-evaluation.md). | Preserve the contribution trace and publication recommendation for the thread that drove the MCP server, client-grounding strategy, and Codex-with-MCP comparison. | The thread is available as a summarized public source note and is linked from the index, decision record, implementation workspace, and source register without publishing raw transcripts. |

## 2026-04-19

| Change | Reason | Evaluation signal |
| --- | --- | --- |
| Added [the bibliography](sources/bibliography.md) and [machine-readable bibliography data](data/bibliography.json). | Resolve Deep Research citation markers into durable URLs and source IDs without copying third-party source bodies. | Lint can check bibliography JSON, source IDs, and internal links. |
| Preserved the raw Deep Research report and created a linked derivative. | Keep the original report as evidence while giving agents a citation-clean source. | Opaque Deep Research markers are allowed only in the raw report. |
| Added search-oriented frontmatter to wiki notes. | Make tags, related links, search terms, note type, and source IDs machine-readable. | Lint reports frontmatter coverage and cross-link density. |
| Added a wiki-specific lint gate. | Detect broken internal links, missing tags, duplicate source IDs, `.DS_Store` files, and leaked opaque citation markers. | `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report` must pass. |
| Cross-linked architecture, implementation, security, candidate, bibliography, research, and decision notes. | Make the wiki navigable from any major entry point and improve retrieval by link graph. | Lint reports internal-link totals and per-file coverage. |
| Added first-use reference submodules with local `SOURCE.md` metadata. | Preserve direct access to selected implementations while keeping upstream code separate and license-reviewed. | Lint excludes upstream submodule Markdown and checks local source metadata links. |
| Recorded authentication, semantic retrieval, and release-time URL validation decisions. | Convert open decisions into implementation constraints before building the server. | Decision record now closes the previous open questions and leaves only implementation-specific follow-ups. |
| Added semantic retrieval option evaluation. | Select embedding and vector-index technology by evidence without weakening licensing, provenance, or reproducibility. | The wiki now records a local permissive shortlist and exact NumPy baseline for v1 retrieval benchmarking. |
| Added implementation notes for the read-only Challenge 2 Wiki MCP server. | Keep the research wiki aligned with the actual server shape, including JSON-RPC core, stdio/local HTTP transports, Codex MCP validation, and semantic retrieval caveats. | Implementation docs now link to the plan, security model, decision record, and evaluation harness. |
| Added comparison-report generation for MCP evaluation runs. | Make Codex-with-MCP versus standard Codex comparison reproducible without committing raw prompts or answer transcripts. | Report metrics cover completion, JSON parseability, timings, citation-overlap proxy, model/version provenance, and MCP audit events. |

## Next Optimization Checks

- Add external-link verification once the source URLs are frozen for a release.
- Run the embedding shortlist benchmark and record the final model lock.
- Add Copilot Studio direct MCP validation notes once the Microsoft host smoke has been run.
