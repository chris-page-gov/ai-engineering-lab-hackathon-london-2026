---
title: "olgasafonova MediaWiki MCP Server Source Metadata"
source_id: "MCP-REF-OLGA-MW"
note_type: "external-reference-source"
status: "first-use-submodule"
tags:
  - "mcp"
  - "mediawiki"
  - "streamable-http"
  - "submodule"
search_terms:
  - "olgasafonova mediawiki mcp server"
  - "remote HTTP MCP reference"
  - "bearer token MCP"
related:
  - "../../../candidate-register.md"
  - "../../../sources/bibliography.md"
  - "../../../implementation-plan.md"
---

# olgasafonova MediaWiki MCP Server Source Metadata

| Field | Value |
| --- | --- |
| Source ID | `MCP-REF-OLGA-MW` |
| Bibliography ID | `MCP-BIB-OLGA-MW` |
| Upstream | [olgasafonova/mediawiki-mcp-server](https://github.com/olgasafonova/mediawiki-mcp-server) |
| Local submodule | [upstream](upstream) |
| Pinned commit | `a09173325bd21e7c35f17360c4ad3b62314c7063` |
| Upstream ref at add time | `v1.24.1-114-ga091733` |
| Latest commit date at add time | `2026-04-13` |
| License posture | MIT license file present in submodule |
| Local use | First-use reference for remote Streamable HTTP deployment ergonomics and practical client guidance |

## Use Constraints

- Study remote transport, deployment, and operational patterns.
- Do not adopt edit or private-wiki behaviours into Challenge 2 evaluation mode.
- Treat bearer-token patterns as smoke-test or internal options, not final government-facing authentication by default.
- Preserve the upstream `LICENSE` file inside the submodule.
