---
title: "ProfessionalWiki MediaWiki MCP Server Source Metadata"
source_id: "MCP-REF-PROF-MW"
note_type: "external-reference-source"
status: "first-use-submodule"
tags:
  - "mcp"
  - "mediawiki"
  - "reference-implementation"
  - "submodule"
search_terms:
  - "ProfessionalWiki MediaWiki MCP Server"
  - "wiki MCP design reference"
  - "MIT submodule"
related:
  - "../../../candidate-register.md"
  - "../../../sources/bibliography.md"
  - "../../../implementation-plan.md"
---

# ProfessionalWiki MediaWiki MCP Server Source Metadata

| Field | Value |
| --- | --- |
| Source ID | `MCP-REF-PROF-MW` |
| Bibliography ID | `MCP-BIB-PROF-MW` |
| Upstream | [ProfessionalWiki/MediaWiki-MCP-Server](https://github.com/ProfessionalWiki/MediaWiki-MCP-Server) |
| Local submodule | [upstream](upstream) |
| Pinned commit | `6521ebfc1c5e6460a4964de17d90d212b4f872da` |
| Upstream ref at add time | `v0.6.5-46-g6521ebf` |
| Latest commit date at add time | `2026-04-13` |
| License posture | MIT license file present in submodule |
| Local use | First-use reference for wiki MCP surface design, resources/tools shape, and read/write separation |

## Use Constraints

- Study patterns only unless a later decision approves direct code reuse.
- Do not import mutable operations into the Challenge 2 server's evaluation mode.
- Preserve the upstream `LICENSE` file inside the submodule.
- Re-check dependencies before using code beyond design reference.
