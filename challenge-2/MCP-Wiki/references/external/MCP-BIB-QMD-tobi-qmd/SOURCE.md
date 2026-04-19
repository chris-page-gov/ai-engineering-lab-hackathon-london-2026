---
title: "qmd Source Metadata"
source_id: "MCP-REF-QMD"
note_type: "external-reference-source"
status: "first-use-submodule"
tags:
  - "mcp"
  - "markdown"
  - "hybrid-search"
  - "submodule"
search_terms:
  - "qmd markdown retrieval"
  - "hybrid search MCP"
  - "semantic retrieval reference"
related:
  - "../../../candidate-register.md"
  - "../../../sources/bibliography.md"
  - "../../../implementation-plan.md"
---

# qmd Source Metadata

| Field | Value |
| --- | --- |
| Source ID | `MCP-REF-QMD` |
| Bibliography ID | `MCP-BIB-QMD` |
| Upstream | [tobi/qmd](https://github.com/tobi/qmd) |
| Local submodule | [upstream](upstream) |
| Pinned commit | `cfd640ed3499769b3ee41a7118119ff884dbe8c5` |
| Upstream ref at add time | `v2.1.0-26-gcfd640e` |
| Latest commit date at add time | `2026-04-11` |
| License posture | MIT license file present in submodule |
| Local use | First-use reference for Markdown retrieval, BM25, vector search, hybrid search, reranking, and MCP HTTP surface |

## Use Constraints

- Use as a retrieval design reference before adopting dependencies.
- Do not broaden the Challenge 2 MCP tool surface to generic corpus search without provenance controls.
- Review model, native, and optional dependency licences before reusing implementation code.
- Preserve the upstream `LICENSE` file inside the submodule.
