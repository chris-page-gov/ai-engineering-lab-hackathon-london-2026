---
exchange_id: "EX-0092"
title: "Update Deep Research Prompt"
source_id: "CONV-005"
global_sequence: 92
session_sequence: 40
user_timestamp: "2026-04-19T18:50:08.115Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0092. Update Deep Research Prompt

Previous: [EX-0091](0091-20260418065216-any-good-giving-the-share-link.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0093](0093-20260418065216-create-codex-postmortem-wiki.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
So I think we are now at the point where what we need is a Wiki MCP Server. Is this branch clean? I think the MCP server should be on a new branch and we should start by researching what Open Source Wiki MCPs there are and what licenses they have as well as a scan of related academic work including the use of Wikis in AI and knowledge base work. Hence, do preliminary research to create a Deep Research Prompt - I will run (I'm assuming you can't from here) and will add the research to the repo. Then you can review this with a thorough search of GitHub for suitable candidates that we can learn from or base our implementation on
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T18:50:20.190Z`

````text
I’ll first verify the branch state, then I’ll create a separate research branch if it is clean. After that I’ll do a preliminary web/GitHub literature scan and draft a Deep Research prompt you can run, with enough structure that the results can be added to the repo and reviewed against implementation options.
````

### Response 2 (commentary)

- Timestamp: `2026-04-19T18:50:29.864Z`

````text
The working tree is clean. This branch is not merged into `origin/main` yet; I’m going to create the MCP research branch from the current clean HEAD so it includes the evaluation context we just proved, while keeping the next work isolated.
````

### Response 3 (commentary)

- Timestamp: `2026-04-19T18:50:43.942Z`

````text
I’ll now do the preliminary scan in two lanes: GitHub repository discovery for open-source MCP/wiki candidates and web/scholar-facing discovery for academic/technical themes. This is not the final candidate review yet; it is to shape the Deep Research prompt so your run comes back with useful, comparable evidence.
````

### Response 4 (commentary)

- Timestamp: `2026-04-19T18:51:52.702Z`

````text
The first GitHub pass found several relevant families: Obsidian vault MCP servers, MediaWiki/Wiki.js MCP servers, Wikipedia/online-wiki MCP servers, and Confluence-style enterprise wiki MCP servers. I’m checking a few top candidates more closely for language, license, activity, and whether they are read-only/search-oriented versus full CRUD.
````

### Response 5 (final_answer)

- Timestamp: `2026-04-19T18:53:41.247Z`

````text
Branch status: clean.

I created a new branch for this work:

`codex/wiki-mcp-research`

It is based on the current clean `codex/evaluation-versioning` HEAD, so it includes the evaluation/Microsoft Copilot context we just proved. No repo files were changed.

**Preliminary Findings**
The direction is right: for M365 Copilot, a Wiki MCP server is a better long-term answer than Personal OneDrive discovery or share links.

Key implication: Microsoft Copilot Studio currently supports MCP via **Streamable HTTP**, not local stdio. Our existing `challenge-2/tools/wiki_eval_mcp.py` is useful as a local/audit prototype, but an M365-compatible server needs an HTTP MCP endpoint, likely with OAuth/API-key auth and a constrained tool/resource surface.

Initial open-source candidates worth researching:

| Candidate | Type | Language | License signal | Notes |
| --- | --- | ---: | --- | --- |
| [cyanheads/obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server) | Obsidian MCP | TypeScript | Apache-2.0 signal | Mature, broad Obsidian CRUD/search via Obsidian Local REST API. Good patterns, too broad for our read-only benchmark unless constrained. |
| [ProfessionalWiki/MediaWiki-MCP-Server](https://github.com/ProfessionalWiki/MediaWiki-MCP-Server) | MediaWiki MCP | TypeScript | MIT signal | Strong candidate for multi-wiki resource/tool design, Streamable HTTP support, read/write separation. |
| [olgasafonova/mediawiki-mcp-server](https://github.com/olgasafonova/mediawiki-mcp-server) | MediaWiki MCP | Go | MIT signal | Search/read/edit patterns, good docs/security materials. |
| [heAdz0r/wikijs-mcp-server](https://github.com/heAdz0r/wikijs-mcp-server) | Wiki.js MCP | TypeScript | MIT signal | GraphQL-backed wiki MCP; useful if comparing API-backed wiki design. |
| [jeanibarz/knowledge-base-mcp-server](https://github.com/jeanibarz/knowledge-base-mcp-server) | Generic KB MCP | Unknown stack from quick pass | Unlicense | Useful for generic KB abstraction, but needs quality review. |
| [shiquda/mediawiki-mcp-server](https://github.com/shiquda/mediawiki-mcp-server) | MediaWiki MCP | Python | no license detected | Interesting Python candidate, but license absence means avoid basing implementation on it unless clarified. |

License note: GitHub search/readme badges gave the license signals above. The next review should verify each actual `LICENSE` file and dependency tree before reuse.

**Deep Research Prompt**
```text
You are conducting deep technical and literature research for an open-source government-style software prototype.

Context:
We have a repository implementing a Challenge 2 “LLM Wiki” / Obsidian-style Markdown knowledge base for synthetic government dark-data documents. The wiki is generated from immutable raw sources and contains Markdown notes, source notes, topic pages, entity pages, maps of content, source-register JSON, lint reports, and operating rules in AGENTS.md. We need a Wiki MCP Server so AI clients, especially Microsoft 365 Copilot via Copilot Studio, can use the wiki as a controlled knowledge base. Personal OneDrive folder discovery and OneDrive share links did not work reliably for M365 Copilot. GitHub permalink plus copied excerpts works, but is not a proper knowledge-base integration.

Research objective:
Recommend whether to build, adapt, or learn from existing open-source Wiki/knowledge-base MCP servers, and define the best architecture for a secure, auditable, source-grounded MCP server over a local Markdown/Obsidian wiki.

Questions to answer:
1. Survey open-source MCP servers related to wikis, Markdown knowledge bases, Obsidian, MediaWiki, Wiki.js, Wikipedia, Confluence, Outline, generic knowledge bases, RAG, and document retrieval.
2. For each relevant repository, report:
   - GitHub URL
   - owner/project
   - description and intended wiki/KB backend
   - language/runtime
   - MCP SDK/library used
   - supported transports: stdio, SSE, Streamable HTTP, custom HTTP
   - tools/resources/prompts exposed
   - read-only vs write/delete capabilities
   - search features: full text, semantic/vector, graph/backlinks, frontmatter, tags
   - authentication model
   - license SPDX ID, actual LICENSE-file text, and dependency-license concerns
   - stars/activity/recent commits/releases/tests/CI
   - security posture and risks
   - suitability for reuse, adaptation, or just design reference
3. Include at least these seed candidates:
   - cyanheads/obsidian-mcp-server
   - ProfessionalWiki/MediaWiki-MCP-Server
   - olgasafonova/mediawiki-mcp-server
   - heAdz0r/wikijs-mcp-server
   - shiquda/mediawiki-mcp-server
   - jeanibarz/knowledge-base-mcp-server
   - any strong Markdown/Obsidian/RAG MCP candidates discovered during research
4. Research Microsoft 365 Copilot/Copilot Studio MCP requirements:
   - current supported MCP transports
   - Streamable HTTP requirements
   - OAuth/API-key options
   - whether stdio is usable in M365 Copilot contexts
   - connector/custom connector implications
   - known limits or caveats
5. Research academic and technical work relevant to wiki-backed AI knowledge bases:
   - Retrieval-Augmented Generation and provenance
   - semantic wikis and Semantic MediaWiki
   - Wikipedia/Wikidata/YAGO/DBpedia-style knowledge bases
   - GraphRAG and graph-enhanced retrieval
   - knowledge-base construction from documents
   - citation, provenance, evidence, and evaluation for knowledge-intensive QA
   - risks: hallucination, stale data, prompt injection, data poisoning, benchmark leakage, over-broad tools
6. Recommend a target architecture for our Challenge 2 Wiki MCP server:
   - read-only by default
   - explicit allowlist rooted at challenge-2/wiki, challenge-2/wiki/data, and challenge-2/AGENTS.md
   - explicit denylist for evaluation-benchmark.md and evaluation harness/gold-answer artifacts
   - tools such as search_wiki, read_note, list_sources, read_source_register, find_by_source_id, build_context_pack, explain_provenance
   - resources for index, source register, individual notes, topic/entity/map collections
   - prompts for “answer from wiki with citations” and “build context pack”
   - audit logging of source access
   - deterministic citations to wiki paths/source IDs
   - optional stdio for local clients and Streamable HTTP for M365/Copilot Studio
   - security controls: path traversal prevention, no raw source access unless explicitly allowed, max response sizes, rate limits, auth, no write/delete tools in evaluation mode
7. Provide an implementation recommendation:
   - build from scratch vs fork/adapt a candidate
   - preferred language for this repo, considering existing Python tools
   - whether Python FastMCP is sufficient
   - how to test with MCP Inspector
   - how to integrate with Microsoft Copilot Studio
   - minimal viable implementation plan and acceptance criteria
8. Output format:
   - Executive summary
   - Candidate matrix
   - License and reuse-risk table
   - Academic/technical literature review
   - Microsoft Copilot/MCP compatibility section
   - Recommended architecture
   - Implementation plan
   - Security and publication risks
   - Bibliography with URLs, DOIs/arXiv IDs where available
   - Open questions requiring hands-on validation
```

Useful sources already checked:
- [MCP Python SDK](https://py.sdk.modelcontextprotocol.io/) documents tools, resources, prompts, stdio/SSE/Streamable HTTP.
- [MCP authorization spec](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) covers OAuth expectations for HTTP transports.
- [Microsoft Copilot Studio MCP docs](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent) say Copilot Studio supports Streamable transport and no longer supports SSE after August 2025.
- [M365 declarative agent knowledge docs](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/build-declarative-agents-add-knowledge) cover OneDrive/SharePoint knowledge sources for agents.
- [RAG paper](https://arxiv.org/abs/2005.11401) is the baseline for knowledge-intensive QA with non-parametric memory/provenance.
- [Microsoft GraphRAG](https://microsoft.github.io/graphrag/) is relevant for graph/hierarchy retrieval over private data.
- [YAGO paper](https://www.coli.uni-saarland.de/courses/WebAsCorpus-12/papers/Yago07.pdf) is a classic Wikipedia-derived knowledge-base reference.
- [Semantic Wikipedia paper](https://www.sciencedirect.com/science/article/abs/pii/S1570826807000339) is a key semantic-wiki reference.

Next after you add the Deep Research output to the repo: I’ll do the thorough GitHub candidate review, verify licenses from source files, and turn the research into an implementation plan for the MCP server branch.

::git-create-branch{cwd="[LOCAL_REPO]" branch="codex/wiki-mcp-research"}
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.

Previous: [EX-0091](0091-20260418065216-any-good-giving-the-share-link.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0093](0093-20260418065216-create-codex-postmortem-wiki.md)
