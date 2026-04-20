---
title: "External MCP Reference Workspace"
note_type: "reference-workspace"
status: "reserved"
tags:
  - "mcp"
  - "external-references"
  - "submodules"
  - "licensing"
search_terms:
  - "external MCP references"
  - "MCP reference submodules"
  - "licensed source snapshots"
related:
  - "../README.md"
  - "../../candidate-register.md"
  - "../../sources/bibliography.md"
  - "../../decision-record.md"
---

# External References

Future git submodules or licensed snapshots should live here.

Expected naming pattern:

```text
<source-id>-<owner>-<repo>/
```

Do not add external reference code here until the decision record and source register have been updated.

## First-Use Submodules

| Source ID | Upstream | Local path | Pinned commit | License posture | Use |
| --- | --- | --- | --- | --- | --- |
| `MCP-REF-PROF-MW` | [ProfessionalWiki/MediaWiki-MCP-Server](https://github.com/ProfessionalWiki/MediaWiki-MCP-Server) | [MCP-BIB-PROF-MW-ProfessionalWiki-MediaWiki-MCP-Server](MCP-BIB-PROF-MW-ProfessionalWiki-MediaWiki-MCP-Server/SOURCE.md) | `6521ebfc1c5e6460a4964de17d90d212b4f872da` | MIT file present | Wiki MCP surface design |
| `MCP-REF-OLGA-MW` | [olgasafonova/mediawiki-mcp-server](https://github.com/olgasafonova/mediawiki-mcp-server) | [MCP-BIB-OLGA-MW-olgasafonova-mediawiki-mcp-server](MCP-BIB-OLGA-MW-olgasafonova-mediawiki-mcp-server/SOURCE.md) | `a09173325bd21e7c35f17360c4ad3b62314c7063` | MIT file present | Remote Streamable HTTP deployment |
| `MCP-REF-QMD` | [tobi/qmd](https://github.com/tobi/qmd) | [MCP-BIB-QMD-tobi-qmd](MCP-BIB-QMD-tobi-qmd/SOURCE.md) | `cfd640ed3499769b3ee41a7118119ff884dbe8c5` | MIT file present | Markdown and hybrid retrieval |
| `MCP-REF-MKDOCS-MCP` | [douinc/mkdocs-mcp-plugin](https://github.com/douinc/mkdocs-mcp-plugin) | [MCP-BIB-MKDOCS-MCP-douinc-mkdocs-mcp-plugin](MCP-BIB-MKDOCS-MCP-douinc-mkdocs-mcp-plugin/SOURCE.md) | `1bb15d124295bb3344e1b2991d05f6485dd1d1de` | MIT metadata; no root license file present | Python/FastMCP retrieval shape |

Initialize these references after cloning the repo with:

```bash
git submodule update --init --recursive
```

## Related

- [Reference material policy](../README.md)
- [Candidate register](../../candidate-register.md)
- [Bibliography](../../sources/bibliography.md)
- [Decision record](../../decision-record.md)
