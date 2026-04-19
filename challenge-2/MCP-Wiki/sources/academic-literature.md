---
source_id: "MCP-SRC-ACADEMIC-LITERATURE"
title: "Academic Literature For Wiki MCP Design"
source_type: "literature-summary"
publication_status: "citation-and-summary"
tags:
  - "source"
  - "literature"
  - "rag"
  - "provenance"
---

# Academic Literature For Wiki MCP Design

The research report identifies several literature streams relevant to a state-of-the-art Wiki MCP server.

| Theme | Representative Work | Design Implication |
| --- | --- | --- |
| Retrieval-Augmented Generation | Lewis et al., RAG for knowledge-intensive NLP | Use retrieval over external evidence rather than model memory. |
| Attribution and evidence | Attributed QA, RARR, FActScore | Return citations and support data as server-side evidence objects. |
| Semantic wikis | Semantic MediaWiki, Wikidata, DBpedia, YAGO | Preserve source IDs, entity links, topic pages, metadata, and relationships. |
| Graph-enhanced retrieval | GraphRAG | Use existing topic/entity/map structure before adding a new graph stack. |
| Security and contamination | Prompt injection guidance, benchmark contamination surveys, retrieval poisoning work | Keep the server narrow, audited, and deny benchmark/gold-answer artifacts. |

Full bibliographic detail is in the Deep Research report.
