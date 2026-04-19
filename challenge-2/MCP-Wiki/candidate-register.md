---
title: "Wiki MCP Candidate Register"
note_type: "register"
tags:
  - "candidate-register"
  - "mcp"
  - "licensing"
search_terms:
  - "MCP candidate projects"
  - "wiki MCP reference implementations"
  - "FastMCP candidates"
  - "MediaWiki MCP"
related:
  - "sources/github-candidates.md"
  - "sources/bibliography.md"
  - "data/candidate-register.json"
  - "implementation-plan.md"
  - "references/external/README.md"
---

# Wiki MCP Candidate Register

This register tracks candidate projects we can learn from while building a purpose-built Challenge 2 Wiki MCP server. It is not a dependency list.

| Candidate | Role | License Signal | Current Treatment | Notes |
| --- | --- | --- | --- | --- |
| `cyanheads/obsidian-mcp-server` | Obsidian vault MCP reference | Apache-2.0 signal | Study only | Mature Obsidian integration, but broad CRUD surface is too permissive for evaluation mode. |
| `ProfessionalWiki/MediaWiki-MCP-Server` | Wiki MCP design reference | MIT file present | First-use submodule | Strong wiki tools/resources shape and read/write separation. Backend model differs from local Markdown. |
| `olgasafonova/mediawiki-mcp-server` | Remote deployment and HTTP reference | MIT file present | First-use submodule | Useful Streamable HTTP and bearer-token deployment patterns. |
| `heAdz0r/wikijs-mcp-server` | Wiki.js GraphQL reference | MIT signal | Study only | Useful API-backed wiki bridge, but write/admin surface is too broad. |
| `tobi/qmd` | Markdown retrieval reference | MIT file present | First-use submodule | Strong local Markdown search and HTTP MCP pattern; heavier retrieval stack. |
| `douinc/mkdocs-mcp-plugin` | Python/FastMCP docs retrieval reference | MIT metadata; root license file missing in pinned checkout | First-use submodule with license caveat | Useful Python retrieval shape; dependency/model licensing must be reviewed before reuse. |
| `OpenDataLab/MinerU-Document-Explorer` | Future-state document/wiki retrieval reference | MIT signal | Study only | Broad ingest/deep-reading system; too large for MVP. |
| `jeanibarz/knowledge-base-mcp-server` | Generic semantic KB reference | Unlicense signal | Study only | Interesting semantic retrieval; weaker provenance/audit posture for this use case. |
| `shiquda/mediawiki-mcp-server` | Historical Python MediaWiki MCP | No clear license detected | Avoid reuse | Marked outdated in research; no-license posture is unsuitable for reuse. |

Machine-readable details are in [data/candidate-register.json](data/candidate-register.json). Resolved URLs and source IDs are in [the bibliography](sources/bibliography.md), and the summarized source note is [GitHub MCP candidate projects](sources/github-candidates.md).

First-use submodules are listed in [the external reference workspace](references/external/README.md). Each selected repository has a sibling `SOURCE.md` recording upstream URL, pinned commit, license posture, local use, and reuse constraints.

## Selection Principle

Use existing projects to learn MCP surface design, transport handling, retrieval ergonomics, and packaging patterns. Build the Challenge 2 server from scratch unless a later decision record justifies reuse.

## Related

- [Implementation plan](implementation-plan.md)
- [Decision record](decision-record.md)
- [Reference material policy](references/README.md)
- [External reference workspace](references/external/README.md)
