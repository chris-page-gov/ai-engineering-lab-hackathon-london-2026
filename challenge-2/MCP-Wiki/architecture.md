---
title: "MCP Research Wiki Architecture"
note_type: "architecture"
tags:
  - "architecture"
  - "mcp"
  - "research-wiki"
---

# MCP Research Wiki Architecture

This wiki separates MCP research and implementation planning from the Challenge 2 evaluation corpus. It gives humans and agents one place to understand candidate projects, specifications, licensing, security controls, and the future server implementation.

## Knowledge Boundaries

```mermaid
flowchart LR
  Corpus["Challenge 2 raw corpus\nstructured_files and unstructured_files"] --> Generated["Generated corpus wiki\nchallenge-2/wiki"]
  Generated --> Workbench["Dark Data Workbench\nhuman and browser AI export"]
  Generated --> FutureServer["Future Wiki MCP server\nread-only audited tools"]
  Research["MCP Research Wiki\nchallenge-2/MCP-Wiki"] --> FutureServer
  Specs["MCP specs and exemplars\nlicensed sources or submodules"] --> Research
  Postmortem["Public postmortem wiki\ncollaboration evidence"] --> Research
```

## Server Target

```mermaid
flowchart TD
  Client["MCP client\nCodex, Claude, Copilot Studio"] --> Transport["stdio locally\nStreamable HTTP remotely"]
  Transport --> Auth["Auth, origin validation,\nrate limits"]
  Auth --> Tools["MCP tools and resources"]
  Tools --> Guard["Path allowlist and denylist"]
  Guard --> Index["Wiki metadata and search index"]
  Index --> Notes["challenge-2/wiki notes"]
  Index --> Register["wiki/data/source-register.json"]
  Tools --> Audit["Append-only access audit"]
```

## Research Source Model

The research wiki stores four classes of source material:

| Class | Local treatment | License posture |
| --- | --- | --- |
| Project-generated reports | Full Markdown, DOCX, and PDF variants | Project artifact; record hashes and provenance |
| External specifications | Citation notes first; optional snapshots later | Preserve upstream license and update method |
| Reference implementations | Citation notes first; optional git submodules after review | Preserve upstream license files and dependency notices |
| Academic or web literature | Citation notes and summaries | Use canonical URLs, DOIs, arXiv IDs, or publisher links |

## Future Submodule Layout

Reference implementations and specifications should not be copied casually. If we decide to vendor or submodule them, use this layout:

```text
challenge-2/MCP-Wiki/references/external/<source-id>/
  upstream-submodule-or-snapshot
  SOURCE.md
  LICENSE
  NOTICE.md
```

Each `SOURCE.md` should record canonical URL, commit or version, license, retrieval command, purpose of inclusion, and whether code is used directly or only studied.
