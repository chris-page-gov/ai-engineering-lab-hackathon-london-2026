---
title: "Challenge 2 Wiki MCP Server Research Report - Linked"
source_id: "MCP-REPORT-LINKED-MD"
note_type: "linked-research-report"
derived_from: "MCP-REPORT-MD"
status: "citation-linked-derivative"
tags:
  - "mcp"
  - "research-report"
  - "linked-citations"
  - "wiki-mcp"
search_terms:
  - "MCP wiki server research"
  - "linked research report"
  - "challenge 2 wiki mcp"
related:
  - "index.md"
  - "../sources/bibliography.md"
  - "../data/bibliography.json"
  - "../implementation-plan.md"
---

# Challenge 2 Wiki MCP Server Research Report


> This linked derivative preserves the report body while removing Deep Research internal citation markers. Use [the MCP Wiki Bibliography](../sources/bibliography.md) and [bibliography data](../data/bibliography.json) for resolved source IDs, URLs, and license treatment. The raw report remains preserved unchanged as [Challenge 2 Wiki MCP Server Research Report.md](<Challenge 2 Wiki MCP Server Research Report.md>).

## Executive summary

The strongest recommendation is to **build a purpose-built Wiki MCP server for the generated local Markdown wiki, while learning selectively from existing open-source servers rather than forking one wholesale**. The main reason is architectural fit: the best existing servers are mostly designed either for **live wiki backends with write/delete capabilities** such as MediaWiki or Wiki.js, or for **general-purpose retrieval over Markdown/document corpora**. Your Challenge 2 requirement is narrower and more security-sensitive: an **immutable, source-grounded, auditable, evaluation-safe knowledge surface** over a generated wiki tree, with explicit path allowlists and denylists, deterministic citations, and strong controls around benchmark leakage and prompt-injection blast radius. The available open-source servers contain useful patterns, but none is already aligned to that exact trust model.

For reuse and design reference, the best projects are split across three roles. **ProfessionalWiki/MediaWiki-MCP-Server** is the best reference for a mature MCP surface over a wiki-style backend, including tools, resources, configuration, release discipline, and clear separation between read and privileged operations. **olgasafonova/mediawiki-mcp-server** is the best reference for remote deployment ergonomics, Streamable HTTP exposure, bearer-token style protection, and practical client guidance for SaaS MCP consumers. **qmd**, **mkdocs-mcp-plugin**, and **MinerU Document Explorer** are the best references for retrieval patterns over Markdown and document collections, especially hybrid search, deep reading, and context-building.

For implementation language and framework, **Python with the official MCP Python SDK’s FastMCP interface is sufficient and well-aligned to the repo context**. The official SDK supports tools, resources, prompts, local and remote transports, and explicitly recommends Streamable HTTP for production; it can also be mounted into an ASGI application, which is ideal for adding authentication, rate limiting, origin validation, request logging, and response-size controls. That makes it a good technical fit for a secure government-style prototype.

For Microsoft 365 Copilot and Copilot Studio, the architecture should treat **Streamable HTTP over a remote HTTPS endpoint as mandatory**, with **stdio kept only for local developer clients and the MCP Inspector**. Copilot Studio’s current MCP guidance says it supports the **Streamable** transport and no longer supports SSE after August 2025. The Microsoft 365 Agents Toolkit flow is also URL-based, which implies a remote MCP endpoint rather than a spawned local subprocess.

## Candidate matrix

| Candidate | GitHub URL | Backend and scope | Runtime and MCP library | Transport | Surface and mutability | Retrieval features | Authentication | Activity and delivery signals | Reuse judgement | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| cyanheads/obsidian-mcp-server | [`github.com/cyanheads/obsidian-mcp-server`](https://github.com/cyanheads/obsidian-mcp-server) | Obsidian vault via Local REST API plugin | TypeScript/Node; uses `@modelcontextprotocol/sdk` | Documented via scripts as stdio and HTTP | Broad note CRUD: read, update, search/replace, global search, list notes, frontmatter, tags, delete | Full-text and regex-style vault search; frontmatter and tag operations; no semantic/vector index documented | Auth model is tied to the local Obsidian REST/plugin boundary rather than enterprise identity in the surfaced docs | 459 stars, 187 commits, 28 tags, Actions present | Strong **Obsidian integration reference**; poor direct fit for a read-only generated government wiki because it is vault-management oriented and delete-capable | |
| ProfessionalWiki/MediaWiki-MCP-Server | [`github.com/ProfessionalWiki/MediaWiki-MCP-Server`](https://github.com/ProfessionalWiki/MediaWiki-MCP-Server) | Any MediaWiki wiki; public or private | TypeScript/Node; uses `@modelcontextprotocol/sdk` | stdio by default; HTTP via `MCP_TRANSPORT=http` | Large tool surface with read and privileged operations: create, update, delete, undelete, upload; also resources for wiki definitions | Search page titles and contents, prefix search, category/file/page/revision access | OAuth2 token preferred; username/password fallback for private or authenticated operations | 76 stars, 12 releases, Node package version `0.6.5`, test and lint scripts, release workflow discipline | Best **wiki-server design reference**; only a fork candidate if you decide to target MediaWiki itself rather than local Markdown | |
| olgasafonova/mediawiki-mcp-server | [`github.com/olgasafonova/mediawiki-mcp-server`](https://github.com/olgasafonova/mediawiki-mcp-server) | Any MediaWiki wiki; also file and PDF search workflows | Go; README credits the Go MCP SDK | stdio and HTTP; HTTP intended for ChatGPT, n8n and remote access | Read, search, revision history, broken-link checks, file search, Markdown→MediaWiki conversion; authenticated editing supported | Full-text search across wiki, related content/sections, file search, PDF search via `pdftotext`; no vector layer | Bot password for editing/private read; HTTP bearer token for remote exposure | 8 stars, 205 commits, 33 releases, latest visible release April 2026, CI and SECURITY docs | Excellent **remote transport and deployment reference**; backend still wrong for your immutable local wiki | |
| shiquda/mediawiki-mcp-server | [`github.com/shiquda/mediawiki-mcp-server`](https://github.com/shiquda/mediawiki-mcp-server) | Early MediaWiki/Wikipedia API server | Python/uv; SDK not obvious from surfaced docs | stdio, Streamable HTTP, and SSE | Small read-only tool set: search and get page; README explicitly says it is outdated in favour of ProfessionalWiki | Page search and retrieval only | No substantial auth model documented in the surfaced README | 24 stars, 18 commits; repo has workflows and Dockerfile, but project is explicitly marked outdated | **Historical reference only**; not a reuse candidate | |
| heAdz0r/wikijs-mcp-server | [`github.com/heAdz0r/wikijs-mcp-server`](https://github.com/heAdz0r/wikijs-mcp-server) | Wiki.js over GraphQL API | TypeScript/Node; package metadata suggests a custom MCP implementation rather than the official TS SDK | HTTP server and stdio mode | Very broad mutable surface: page CRUD, unpublished page management, user CRUD, group listing | Multi-method page search using GraphQL plus HTTP fallback; metadata and content search | Wiki.js API token | 8 stars, 3 tags, test scripts, Actions present | Useful **live wiki API bridge reference**; too write-heavy and admin-heavy for an evaluation-safe local wiki | |
| jeanibarz/knowledge-base-mcp-server | [`github.com/jeanibarz/knowledge-base-mcp-server`](https://github.com/jeanibarz/knowledge-base-mcp-server) | Generic local knowledge-base folders of `.txt` and `.md` files | Node/TypeScript; exact MCP SDK not obvious from surfaced docs | stdio-oriented in the surfaced configuration examples | Read-only; exposes `list_knowledge_bases` and `retrieve_knowledge` | Semantic retrieval using chunking plus FAISS; embeddings from local Ollama or Hugging Face | Local Ollama or Hugging Face API key depending on embedding provider | 43 stars, no releases, Actions tab present, Jest config and tests documented | Good **semantic retrieval reference**, but weaker on provenance, audit, and deterministic source-grounding | |
| tobi/qmd | [`github.com/tobi/qmd`](https://github.com/tobi/qmd) | Local Markdown collections, docs, notes, meeting transcripts | Node/TypeScript; uses `@modelcontextprotocol/sdk` | stdio by default; HTTP Streamable endpoint at `/mcp` | Read-only retrieval tools: `query`, `get`, `multi_get`, `status` | BM25 full-text, vector search, hybrid search, query expansion, reranking | Local-first; no auth model documented in surfaced README for local use | Package version `2.1.0`; changelog active in March 2026; repository shows heavy issue/PR activity | Best **search-engine reference** if you later add hybrid retrieval behind your own domain-specific tools | |
| douinc/mkdocs-mcp-plugin | [`github.com/douinc/mkdocs-mcp-plugin`](https://github.com/douinc/mkdocs-mcp-plugin) | MkDocs documentation trees | Python 3.12; FastMCP | Transport not clearly surfaced in the README excerpt, but FastMCP-based architecture is explicit | Tools, resources, and prompts for document retrieval; primarily read-only docs access | Keyword search, vector search, hybrid search, real-time indexing; metadata extraction | Auth model not clearly documented in surfaced material | 10 stars; package version `0.4.1`; pytest and coverage tooling in project metadata | Best **Python retrieval-and-MCP shape reference** for a clean FastMCP build | |
| OpenDataLab/MinerU-Document-Explorer | [`github.com/OpenDataLab/MinerU-Document-Explorer`](https://github.com/OpenDataLab/MinerU-Document-Explorer) | Multi-format local corpora with wiki ingestion: Markdown, PDF, DOCX, PPTX | npm package built around QMD; optional Python tooling for document extraction | stdio and HTTP via QMD MCP | 15 tools across retrieval, deep reading, and knowledge ingestion | BM25, vector, reranking, query expansion; “build and maintain an LLM wiki” from raw docs | No auth model surfaced in the README excerpt | Current v1 visible in April 2026; README shows CI badge and active changelog | Strong **future-state design reference** for ingest plus deep reading; too broad and moving too fast for an MVP | |

The matrix points to a clear pattern. The existing “real wiki” servers are mainly **API proxies over mutable live systems**, whereas the best Markdown/document candidates are mainly **retrieval engines**. Your target server needs a narrower, more controlled shape than either class currently offers.

## Licence and reuse-risk table

| Candidate | SPDX or declared licence | Actual licence-file text observed in this pass | Dependency or service-term concerns | Reuse risk |
|---|---|---|---|---|
| cyanheads/obsidian-mcp-server | Apache-2.0 | LICENSE file is the canonical Apache 2.0 text beginning “Apache License Version 2.0, January 2004” | Normal Node dependency stack; operationally tied to the Obsidian REST plugin and local vault semantics | Low legal risk, higher architectural mismatch risk | |
| ProfessionalWiki/MediaWiki-MCP-Server | MIT | LICENSE file is the canonical MIT grant beginning “Permission is hereby granted…” | Standard Node dependencies; no obvious copyleft concern in surfaced metadata | Low legal risk; medium adaptation cost because backend model differs | |
| olgasafonova/mediawiki-mcp-server | MIT | Repo and README declare MIT; the actual file text was not separately rendered in this pass, so verify before vendoring | Optional external dependency on `pdftotext`/poppler-utils; remote deployment guidance implies further infra hardening work | Low-medium legal risk; medium operational risk | |
| shiquda/mediawiki-mcp-server | No clear root SPDX surfaced | No root `LICENSE` file was visible in the surfaced repo root listing | Even apart from legal ambiguity, the project is obsolete and superseded | **High** reuse risk | |
| heAdz0r/wikijs-mcp-server | MIT | Repo declares MIT; actual file text was not separately rendered in this pass | Dependency stack is permissive-looking, but the server exposes high-risk admin and write operations | Low legal risk; high security-hardening cost | |
| jeanibarz/knowledge-base-mcp-server | Unlicense | Repo declares “Unlicense”; actual file text was not separately rendered here | External embedding providers introduce separate service and model terms; semantic retrieval can weaken provenance guarantees | Medium legal and governance risk for government-style reuse | |
| tobi/qmd | MIT | Package metadata declares MIT; actual file text not rendered separately in this pass | Native and model-related dependencies, including `node-llama-cpp` and platform-specific optional binaries, need supply-chain review | Medium reuse risk; technically strong but heavier operational footprint | |
| douinc/mkdocs-mcp-plugin | MIT | `pyproject.toml` declares MIT | Python stack includes `sentence-transformers` and `pymilvus[model]`; downloaded model artefacts may carry separate terms | Medium reuse risk if you enable semantic features | |
| OpenDataLab/MinerU-Document-Explorer | MIT | Repo declares MIT | Optional MinerU Cloud API and downloaded model artefacts add service-term and model-term review requirements | Medium reuse risk; broad capability surface raises governance burden | |

The practical reuse conclusion is straightforward. **ProfessionalWiki** is the cleanest legal/design reference if you want to borrow code ideas or interface shape. **Shiquda** should not be reused because the project is obsolete and the surfaced repo root did not expose a licence file. **Semantic-search servers** such as QMD, mkdocs-mcp-plugin, and MinerU are legally usable in principle, but they introduce extra supply-chain and model-governance review that you do not need for an MVP.

## Academic and technical literature review

### Retrieval, provenance, and answer support

The core RAG literature still matters here because it frames the trade-off that your server must solve. Lewis et al. introduced Retrieval-Augmented Generation as a way to combine parametric generation with retrieved external documents for knowledge-intensive tasks, specifically to improve factual access and external knowledge refresh. That foundational point still holds: even if the assistant does the final synthesis, the system needs a reliable retrieval layer over external evidence rather than relying on model memory.

But your use case needs more than retrieval. The more relevant follow-on literature is the attribution and evidence literature. The Attributed QA work from Google argues that attribution is not a cosmetic add-on but a central evaluation dimension for knowledge-seeking systems, and shows that both human and automatic evaluation are needed to judge whether an answer is actually supported by cited evidence. Work on automatic attribution evaluation and FActScore pushes the same direction by measuring whether individual statements are supported by cited sources rather than merely sounding plausible. RARR adds a practical lesson: it is useful to separate **retrieval**, **support checking**, and **final answer revision** rather than treating them as one opaque step.

For your Wiki MCP server, the implication is that the server should not simply expose a generic “search everything” tool. It should expose tools that make **support auditable**: a search tool that returns bounded snippets and note paths; a provenance tool that explains which wiki note and source IDs support a claim; and a context-pack builder that preserves the path from answerable excerpt back to source register and note. That design choice follows directly from the literature’s finding that attribution quality is a first-class property, not a post-hoc formatting exercise.

### Semantic wikis and structured knowledge bases

The semantic-wiki tradition anticipated much of what modern AI systems now need. The original Semantic MediaWiki paper framed the problem as integrating semantic structure into ordinary wiki workflows so that a wiki could be both human-readable and machine-queryable. Later systems scaled that idea differently: Wikimedia Foundation’s Wikidata centralised structured facts for reuse across wikis and external applications, while DBpedia and YAGO extracted linked datasets from Wikipedia and related resources.

The architectural lesson is not that you should build a full knowledge graph first. It is that **wiki content becomes much more useful to machines when metadata, entity identity, source identifiers, and relationships are first-class artefacts**. Your generated Challenge 2 wiki already has much of this shape: topic pages, entity pages, maps of content, source notes, source-register JSON, lint reports, and operating rules. That is closer to a semantic wiki than to an ordinary folder of Markdown. The MCP surface should therefore expose those artefacts as structured resources, not flatten them into bag-of-words text retrieval only.

### Graph-enhanced retrieval and corpus-level questions

GraphRAG is relevant, but selectively. The GraphRAG paper argues that conventional chunk-level RAG struggles on “global” corpus questions, such as asking for major themes across the whole collection, because those are really corpus-level summarisation tasks rather than ordinary retrieval problems. It improves performance by deriving an entity graph and community summaries that can support broader sensemaking queries.

That is useful for your roadmap, but not for your MVP. Your Challenge 2 wiki already contains **entity pages**, **topic pages**, and **maps of content**, which are lighter-weight graph artefacts already produced by your generation pipeline. The best near-term move is therefore not to add a new opaque graph database, but to let the MCP server exploit the graph-like structure you already have: backlinks where present, topic/entity cross-links, source-note relationships, and map-of-content hierarchy. In other words, do “graph-aware retrieval” before doing “GraphRAG as infrastructure”.

### Security, contamination, and evaluation leakage

The security literature is unusually aligned with your requirements. The UK National Cyber Security Centre argues that prompt injection should not be treated like SQL injection because current LLMs do not enforce a true boundary between data and instructions; the emphasis should therefore be on **limiting impact via deterministic safeguards**, not pretending the problem can be fully eliminated. That is directly relevant to MCP tools because every exposed tool turns the model into a possible “confusable deputy”.

The evaluation literature makes the denylist requirement equally clear. Benchmark contamination surveys show that leaked benchmark content can distort evaluation and make reported performance unreliable. Separately, recent work on poisoning attacks against retrieval systems, including KG-RAG variants, shows that external knowledge sources can themselves become attack surfaces. For a government-style prototype, this means two concrete controls are non-negotiable: **exclude benchmark and gold-answer artefacts from the exposed knowledge surface**, and **treat retrieved content as untrusted input when it flows into tool-calling models**.

## Microsoft Copilot and MCP compatibility

The current Microsoft position is sufficiently clear for architecture: **Copilot Studio presently supports Streamable transport for MCP, not stdio, and no longer supports SSE after August 2025**. That alone means your server should expose a proper remote Streamable HTTP endpoint if Microsoft 365 Copilot or Copilot Studio is a target host. Local stdio remains useful for desktop clients and developer tooling, but it is not the transport to optimise for in Microsoft-hosted scenarios.

The Streamable HTTP specification matters in implementation detail. The MCP spec requires a **single MCP endpoint** supporting **POST and GET**, with the client sending JSON-RPC messages by POST and advertising support for both `application/json` and `text/event-stream`. The spec also warns that servers must validate the `Origin` header to mitigate DNS rebinding, should bind to localhost when local, and should implement proper authentication. If you use session IDs, they travel in the `Mcp-Session-Id` header.

Microsoft’s product guidance introduces one important caveat: the documentation is **not perfectly consistent across hosts and packaging paths**. The Copilot Studio MCP onboarding wizard currently offers **None**, **API key**, and **OAuth 2.0**, with OAuth dynamic-discovery, dynamic, and manual modes. But the Microsoft 365 Copilot plugin-authentication documentation says **MCP plugins do not support API key authentication**, while OAuth 2.0 authorisation-code flow, Microsoft Entra SSO, and anonymous access are supported for agents. The safest interpretation is that **API keys may work in some Copilot Studio connection paths, but should not be assumed as the long-term cross-host Microsoft 365 Copilot strategy**. For a government-style production path, choose **OAuth 2.0** if at all possible.

The connection model also affects tooling choices. Microsoft’s “build plugins from an MCP server” flow in the Microsoft 365 Agents Toolkit is URL-led: you provide an MCP server URL, fetch actions, and package them into a declarative agent. Copilot Studio also supports a **custom connector** path through Power Apps, using an OpenAPI schema that declares `x-ms-agentic-protocol: mcp-streamable-1.0`. That means your server should be designed as a remote HTTPS service first, with local stdio retained as a local-development convenience only.

## Recommended architecture

### Core shape

I recommend a **read-only, file-backed, domain-specific MCP server** over the generated wiki artefacts rooted at `challenge-2/wiki`, `challenge-2/wiki/data`, and `challenge-2/AGENTS.md`, with explicit denials for `evaluation-benchmark.md` and any evaluation harness or gold-answer artefacts. The server should be designed around the generated wiki as the authoritative knowledge surface, **not** around the raw immutable sources, except where you later choose to allow a tightly bounded raw-source read path behind a feature flag. This follows both the provenance literature and the security guidance: keep the surfaced corpus narrow, explicit, and supportable.

The internal architecture should have five layers. First, a **path-governed filesystem adapter** performs canonicalisation, allowlist and denylist checks, symlink refusal, extension filtering, and size bounds. Secondly, an **index and metadata layer** ingests note paths, frontmatter, tags, entity/topic/map classifications, and the source-register JSON into a small local index. Thirdly, a **retrieval layer** provides deterministic lexical retrieval first, with optional semantic reranking later. Fourthly, a **provenance layer** maps every returned excerpt back to wiki note paths and source IDs. Finally, an **MCP surface layer** exposes the tools, resources, and prompts. This separation is what makes auditability and verification tractable.

For the index, the most conservative starting point is **metadata plus lexical search** over the generated wiki and source register. That is more explainable, easier to test, and easier to keep benchmark-safe than immediately introducing embeddings. If later search quality needs improvement, add an optional semantic reranker behind the same tool contract, taking design cues from **QMD** or **mkdocs-mcp-plugin** rather than changing the outward protocol.

### MCP surface

The tool surface should be narrower than the generic wiki servers and more structured than a raw filesystem server:

| Surface | Purpose | Why it fits this repo |
|---|---|---|
| `search_wiki(query, kind?, tags?, source_id?, top_k?, max_bytes?)` | Search notes, topic pages, entity pages, maps of content, and source notes | Keeps search scoped to generated artefacts rather than arbitrary files |
| `read_note(path, include_frontmatter?, include_backlinks?)` | Read a single note by canonical wiki-relative path | Deterministic and auditable |
| `list_sources(filter?)` | Enumerate source IDs and key metadata from the source register | Makes source provenance first-class |
| `read_source_register()` | Return the source-register JSON or a structured projection of it | Gives the model a safe overview of corpus provenance |
| `find_by_source_id(source_id)` | Jump from source ID to notes that cite or derive from it | Supports traceability and evidence-chasing |
| `build_context_pack(query, notes?, budget_bytes?, include_provenance=true)` | Return a bounded context bundle with snippets, note paths, source IDs, and confidence metadata | Aligns to attributed QA and evidence-first answering |
| `explain_provenance(path_or_excerpt)` | Explain how a note or excerpt maps to source notes and source IDs | Turns provenance into a callable capability rather than informal text |

These tools should be paired with resources for durable, browseable artefacts such as a wiki index, the source register, and grouped note collections. I would expose resources like `wiki://index`, `wiki://source-register`, `wiki://notes/{path}`, `wiki://topics`, `wiki://entities`, `wiki://maps`, and `wiki://agents`. I would also expose two prompts for non-Microsoft clients: one for **answer from wiki with citations**, and one for **build context pack**. Microsoft integrations should still be designed so that **tools alone are sufficient**, because Microsoft’s current MCP consumption paths are clearly tool-led.

### Transport, auth, and audit

Run the same core server in two modes. For local engineering workflows, support **stdio** so that the server can be used through the MCP Inspector and local clients. For Microsoft-hosted scenarios, run **Streamable HTTP** at a single `/mcp` endpoint. The Python SDK guidance explicitly recommends Streamable HTTP for production and shows `stateless_http=True` plus `json_response=True` as the scalable default, which is a good fit here because your knowledge base is mostly read-only and session state is unnecessary.

Every tool call and resource read should produce an **append-only audit event** containing at minimum timestamp, principal or connection identity, transport, client origin, tool/resource name, canonical path, source IDs returned, bytes returned, and whether access was allowed or denied. For privacy and minimisation reasons, I would log hashes or metadata for returned content rather than full note bodies by default. The literature and NCSC guidance support this stance: once a model is treated as a possibly confusable deputy, deterministic control and observability become the main lines of defence.

Citations should be **deterministic and non-generative**. Rather than asking the model to invent citation formatting, the server should emit note-relative citations in a stable machine-readable form, for example `{path, title, source_ids, snippet_offsets}`. The prompt layer can then render those into answer text, but the evidence object should come from the server, not the model. That is the cleanest way to honour the attribution literature and to make regression tests possible.

## Implementation plan

### Build choice and framework

The right implementation choice is **build from scratch, but borrow patterns**. Forking an existing Obsidian, MediaWiki, or Wiki.js server would mean removing large amounts of irrelevant surface area, especially write/delete operations, live-backend assumptions, and external authentication semantics. That is usually more work, and more risk, than building a smaller server that matches the repo’s actual knowledge model from day one.

The preferred language is **Python**, because your repository context already points that way and because the official MCP Python SDK with FastMCP is now mature enough for this use case. It supports tools, resources, prompts, and Streamable HTTP; it can also be mounted into Starlette or another ASGI application, which is ideal for Copilot-facing deployment. In practice, FastMCP is sufficient for an MVP and probably for the first production-capable prototype as well. Only drop to lower-level primitives if you later need custom auth delegation, resumability, or protocol features that the higher-level server wrapper obstructs.

### Minimal viable plan

| Phase | Deliverable | Acceptance criterion |
|---|---|---|
| Foundation | Python project using the official MCP SDK/FastMCP, mounted into ASGI for HTTP mode | Server initialises cleanly in stdio and Streamable HTTP modes |
| Safe corpus adapter | Canonical path resolver with allowlist, denylist, extension filter, size limits, and traversal protection | Attempts to escape the challenge root or read benchmark artefacts are denied and logged |
| Core tools | `search_wiki`, `read_note`, `list_sources`, `read_source_register`, `find_by_source_id` | MCP Inspector can discover and call all read-only tools successfully |
| Provenance and context | `build_context_pack` and `explain_provenance` with deterministic evidence objects | Every returned snippet includes note path and source ID data suitable for downstream citation rendering |
| Microsoft transport | HTTPS `/mcp` endpoint with Origin validation, auth, and rate limiting | Copilot Studio can connect over Streamable HTTP and invoke the core tools |
| Evaluation safety | “Evaluation mode” disables any future mutation tools and hides evaluation/gold artefacts from indexing and retrieval | Regression tests prove benchmark artefacts never surface in tool outputs |

The first retrieval implementation should be **lexical and metadata-first**, with deterministic scoring and bounded snippet extraction. After that is stable, add an optional semantic reranker behind the same `search_wiki` interface, rather than exposing a second public search semantics to clients. This keeps the protocol stable while letting you improve relevance later.

### Testing and validation

Use the official MCP Inspector in both modes. The Inspector supports stdio, SSE, and Streamable HTTP, can export configuration stanzas, and is explicitly intended for testing and debugging MCP servers. That makes it suitable for your local acceptance loop even though the target Microsoft integration will be HTTP-only.

For Microsoft integration, validate two paths. The first is the **Copilot Studio onboarding wizard**, pointed directly at your HTTPS `/mcp` endpoint. The second is a **custom connector** path through Power Apps if you need enterprise packaging or connector governance. If you choose authentication, prefer OAuth 2.0 rather than API keys because the Microsoft documentation is inconsistent on API-key support for MCP once you move beyond the simple connection wizard into Microsoft 365 Copilot plugin packaging.

## Security and publication risks

The biggest technical risk is **prompt injection through retrieved wiki content**. The NCSC’s current guidance is blunt: this is not a problem you “solve” once, because LLMs do not maintain a true boundary between instructions and data. That means your mitigation strategy must be architectural: narrow tools, no arbitrary file reads, no mutation tools in evaluation mode, deterministic parsing and citation generation outside the model, and strong audit logs. In other words, do not give the model a tool that behaves like a shell over the repo.

The biggest publication and governance risk is **evaluation leakage**. If benchmark artefacts, gold answers, or harness outputs are indexed by the same server used for QA evaluation, the system can appear to perform better than it really does, and you lose trust in the entire exercise. The contamination literature makes this a real concern, not a theoretical nicety. Your denylist requirement is therefore correct and should be tested continuously, not left as policy prose.

The next risk is **knowledge poisoning and silent provenance drift**. Because the wiki is generated from raw sources, corruption can happen either upstream in source ingestion or downstream in generated note/index artefacts. Recent work on poisoning attacks against retrieval systems shows that external knowledge stores can become attack surfaces. The answer is not to stop using retrieval; it is to make the generation pipeline and indexed corpus **immutable per build**, to record build provenance, and to keep the surfaced knowledge base smaller than the full repository.

A final risk is **over-building the retrieval stack too early**. GraphRAG, hybrid search, and document-deep-reading are valuable, but each added layer increases the burden of explanation, testing, and accreditation. For this prototype, the safest route is to keep the public MCP contract stable and conservative, while letting the internal retrieval engine evolve only after deterministic provenance and benchmark safety are already proven.

## Bibliography

The following sources were the most decision-relevant. Repository links are given as code-form URLs; the citations point to the exact source pages used.

- [`github.com/cyanheads/obsidian-mcp-server`](https://github.com/cyanheads/obsidian-mcp-server) — Obsidian MCP server, package metadata, Apache-2.0 licence.
- [`github.com/ProfessionalWiki/MediaWiki-MCP-Server`](https://github.com/ProfessionalWiki/MediaWiki-MCP-Server) — MediaWiki MCP server, package metadata, MIT licence.
- [`github.com/olgasafonova/mediawiki-mcp-server`](https://github.com/olgasafonova/mediawiki-mcp-server) — MediaWiki MCP server, remote HTTP deployment, bearer-token setup, MIT declaration.
- [`github.com/shiquda/mediawiki-mcp-server`](https://github.com/shiquda/mediawiki-mcp-server) — early Python MediaWiki MCP server, now marked outdated.
- [`github.com/heAdz0r/wikijs-mcp-server`](https://github.com/heAdz0r/wikijs-mcp-server) — Wiki.js MCP server with page/user/group tools and HTTP/stdio modes.
- [`github.com/jeanibarz/knowledge-base-mcp-server`](https://github.com/jeanibarz/knowledge-base-mcp-server) — FAISS-based semantic retrieval MCP server for local knowledge bases.
- [`github.com/tobi/qmd`](https://github.com/tobi/qmd) — local Markdown search engine and MCP server; package metadata and active changelog.
- [`github.com/douinc/mkdocs-mcp-plugin`](https://github.com/douinc/mkdocs-mcp-plugin) — FastMCP-based MkDocs retrieval server in Python.
- [`github.com/OpenDataLab/MinerU-Document-Explorer`](https://github.com/OpenDataLab/MinerU-Document-Explorer) — agent-native retrieval/deep-read/wiki-ingest system.
- Model Context Protocol transports specification, including Streamable HTTP and security requirements.
- Official MCP Python SDK and FastMCP guidance.
- MCP Inspector.
- Microsoft Copilot Studio MCP connection guidance and Streamable transport support.
- Microsoft 365 Copilot MCP plugin build guidance via Agents Toolkit.
- Microsoft 365 Copilot authentication guidance for agents and MCP/API plugins.
- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, arXiv:2005.11401.
- Krötzsch, Vrandečić, Völkel, *Semantic MediaWiki*, DOI: 10.1007/11926078_68.
- Vrandečić and Krötzsch, *Wikidata: A Free Collaborative Knowledge Base*, DOI: 10.1145/2629489.
- Auer et al., *DBpedia: A Nucleus for a Web of Open Data*, DOI: 10.1007/978-3-540-76298-0_52.
- Suchanek, Kasneci, Weikum, *YAGO: A Core of Semantic Knowledge*, DOI: 10.1145/1242572.1242667.
- Edge et al., *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*, arXiv:2404.16130.
- Bohnet et al., *Attributed Question Answering*, arXiv:2212.08037.
- Yue et al., *Automatic Evaluation of Attribution by Large Language Models*, arXiv:2305.06311.
- Gao et al., *RARR: Researching and Revising What Language Models Say*, arXiv:2210.08726.
- Min et al., *FActScore*, arXiv:2305.14251.
- Xu et al., *Benchmark Data Contamination of Large Language Models: A Survey*, arXiv:2406.04244.
- Zhao et al., *Exploring Knowledge Poisoning Attacks to Retrieval-Augmented Generation*, DOI: 10.1016/j.inffus.2025.103900.
- NCSC, *Prompt injection is not SQL injection*.
- NCSC, *AI and cyber security: what you need to know*.

## Open questions requiring hands-on validation

A few points still need live validation before you lock the architecture.

First, **Microsoft host behaviour should be tested directly**. The documentation is clear that Copilot Studio supports Streamable transport, but the authentication story for MCP is not fully harmonised across wizard-based connections, custom connectors, and Microsoft 365 Copilot plugin packaging. A short proof-of-connection exercise with both anonymous and OAuth 2.0 modes is worth doing before you commit to a deployment wrapper.

Secondly, you should validate whether **resources and prompts are actually consumed** by your target Microsoft hosts, even though the server should expose them for other MCP clients. The safest design is still to make the tool surface sufficient on its own.

Thirdly, you should test whether the generated wiki can meet your relevance targets with **lexical-plus-metadata retrieval only**. If it can, do not add vector retrieval until later. If it cannot, the best next step is an internal reranking layer, not a broader public tool surface.

Finally, if Confluence or Outline ever become target backends rather than mere comparators, they should be treated as **separate research items**. No mature open-source MCP candidate for those backends emerged strongly enough from this pass to change the recommendation for a Challenge 2 local Markdown wiki server.
