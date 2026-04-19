---
source_id: "MCP-SRC-BIBLIOGRAPHY"
title: "MCP Wiki Bibliography"
source_type: "source-register"
publication_status: "summary-and-links"
license_status: "mixed-citation-only-until-reviewed"
tags:
  - "source"
  - "bibliography"
  - "mcp"
  - "license-review"
search_terms:
  - "citation map"
  - "source bibliography"
  - "reference implementation"
  - "academic literature"
related:
  - "../index.md"
  - "../research/index.md"
  - "../candidate-register.md"
  - "../data/bibliography.json"
---

# MCP Wiki Bibliography

This bibliography resolves the Deep Research report's opaque citation markers into ordinary URLs, local source notes, and stable source IDs. It does not vendor third-party source bodies. Local copying, submodules, or specification snapshots require the license checks recorded in [the decision record](../decision-record.md) and [the source register](../data/source-register.json).

## Reference Implementations

| Source ID | Source | URL | License posture | Local treatment |
| --- | --- | --- | --- | --- |
| `MCP-BIB-OBS-MCP` | cyanheads/obsidian-mcp-server | [GitHub](https://github.com/cyanheads/obsidian-mcp-server) | Apache-2.0 signal; verify before reuse | Study only |
| `MCP-BIB-PROF-MW` | ProfessionalWiki/MediaWiki-MCP-Server | [GitHub](https://github.com/ProfessionalWiki/MediaWiki-MCP-Server) | MIT file present in submodule | First-use submodule for study |
| `MCP-BIB-OLGA-MW` | olgasafonova/mediawiki-mcp-server | [GitHub](https://github.com/olgasafonova/mediawiki-mcp-server) | MIT file present in submodule | First-use submodule for study |
| `MCP-BIB-SHIQUDA-MW` | shiquda/mediawiki-mcp-server | [GitHub](https://github.com/shiquda/mediawiki-mcp-server) | No clear license detected in the research pass | Avoid reuse |
| `MCP-BIB-WIKIJS` | heAdz0r/wikijs-mcp-server | [GitHub](https://github.com/heAdz0r/wikijs-mcp-server) | MIT signal; verify before reuse | Study only |
| `MCP-BIB-KB-MCP` | jeanibarz/knowledge-base-mcp-server | [GitHub](https://github.com/jeanibarz/knowledge-base-mcp-server) | Unlicense signal; verify before reuse | Study only |
| `MCP-BIB-QMD` | tobi/qmd | [GitHub](https://github.com/tobi/qmd) | MIT file present in submodule; dependency review needed | First-use submodule for study |
| `MCP-BIB-MKDOCS-MCP` | douinc/mkdocs-mcp-plugin | [GitHub](https://github.com/douinc/mkdocs-mcp-plugin) | MIT metadata in `pyproject.toml`; root license file missing in pinned checkout | First-use submodule for study with license caveat |
| `MCP-BIB-MINERU` | OpenDataLab/MinerU-Document-Explorer | [GitHub](https://github.com/OpenDataLab/MinerU-Document-Explorer) | MIT signal; service and model terms need review | Study only |

See [the candidate register](../candidate-register.md), [the candidate data](../data/candidate-register.json), and [the GitHub candidate source note](github-candidates.md) for reuse analysis.

## Specifications And Tooling

| Source ID | Source | URL | Local treatment |
| --- | --- | --- | --- |
| `MCP-BIB-MCP-SPEC` | Model Context Protocol specification | [modelcontextprotocol.io](https://modelcontextprotocol.io/specification) | Citation only until snapshot decision |
| `MCP-BIB-MCP-TRANSPORT` | MCP Streamable HTTP transport specification | [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) | Citation only until snapshot decision |
| `MCP-BIB-PY-SDK` | MCP Python SDK | [GitHub](https://github.com/modelcontextprotocol/python-sdk) | Likely dependency after license and dependency review |
| `MCP-BIB-INSPECTOR` | MCP Inspector | [GitHub](https://github.com/modelcontextprotocol/inspector) | Developer-tool citation |

See [the MCP specification source note](mcp-specification.md), [the architecture](../architecture.md), and [the implementation plan](../implementation-plan.md).

## Microsoft Copilot Sources

| Source ID | Source | URL | Local treatment |
| --- | --- | --- | --- |
| `MCP-BIB-MS-COPILOT-STUDIO` | Microsoft Copilot Studio MCP connection guidance | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp) | Citation only |
| `MCP-BIB-MS-AGENTS-MCP` | Microsoft 365 Copilot MCP plugin build guidance | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/build-mcp-plugins) | Citation only |
| `MCP-BIB-MS-AUTH` | Microsoft 365 Copilot authentication guidance | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-plugin-authentication) | Citation only |

See [the Microsoft Copilot source note](microsoft-copilot-mcp.md) and [the security model](../security-model.md).

## Semantic Retrieval Sources

| Source ID | Source | URL | Local treatment |
| --- | --- | --- | --- |
| `MCP-BIB-BGE-SMALL` | BAAI/bge-small-en-v1.5 | [Hugging Face](https://huggingface.co/BAAI/bge-small-en-v1.5) | Preferred first embedding candidate |
| `MCP-BIB-MINILM` | sentence-transformers/all-MiniLM-L6-v2 | [Hugging Face](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | Fallback embedding baseline |
| `MCP-BIB-E5-SMALL` | intfloat/e5-small-v2 | [Hugging Face](https://huggingface.co/intfloat/e5-small-v2) | Second local embedding candidate |
| `MCP-BIB-OPENAI-EMBEDDINGS` | OpenAI text-embedding-3 models | [OpenAI](https://openai.com/index/new-embedding-models-and-api-updates/) | Comparison only unless external embedding service use is approved |
| `MCP-BIB-NUMPY` | NumPy | [numpy.org](https://numpy.org/about) | Preferred exact vector-matrix baseline |
| `MCP-BIB-SCIKIT-LEARN` | scikit-learn | [Scientific Python](https://scientific-python.org/specs/core-projects/scikit-learn/) | Optional exact-search helper |
| `MCP-BIB-FAISS` | FAISS | [GitHub](https://github.com/facebookresearch/faiss) | Scale candidate if exact NumPy is too slow |
| `MCP-BIB-SQLITE-VEC` | sqlite-vec | [GitHub](https://github.com/asg017/sqlite-vec) | Study for later persistent local index |
| `MCP-BIB-HNSWLIB` | hnswlib | [GitHub](https://github.com/nmslib/hnswlib) | Approximate search option, not v1 default |
| `MCP-BIB-CHROMA` | Chroma open source docs | [Chroma](https://docs.trychroma.com/docs/overview/oss) | Defer until vector database scale is needed |

See [semantic retrieval options](../semantic-retrieval-options.md) for the evaluation.

## Academic And Security Sources

| Source ID | Source | URL | Design relevance |
| --- | --- | --- | --- |
| `MCP-BIB-RAG` | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) | Use retrieval over source evidence rather than model memory |
| `MCP-BIB-SEMANTIC-MEDIAWIKI` | Semantic MediaWiki | [DOI](https://doi.org/10.1007/11926078_68) | Treat wiki metadata and relationships as first-class |
| `MCP-BIB-WIKIDATA` | Wikidata: A Free Collaborative Knowledge Base | [Google Research](https://research.google/pubs/wikidata-a-free-collaborative-knowledge-base/) | Preserve structured source and entity identifiers |
| `MCP-BIB-DBPEDIA` | DBpedia: A Nucleus for a Web of Open Data | [DOI](https://doi.org/10.1007/978-3-540-76298-0_52) | Support linked-data style traceability |
| `MCP-BIB-YAGO` | YAGO: A Core of Semantic Knowledge | [Author PDF](https://suchanek.name/work/publications/www2007.pdf) | Support entity grounding and provenance |
| `MCP-BIB-GRAPHRAG` | From Local to Global: A Graph RAG Approach to Query-Focused Summarization | [arXiv](https://arxiv.org/abs/2404.16130) | Use existing topic/entity/map structure before adding a graph store |
| `MCP-BIB-ATTRIBUTED-QA` | Attributed Question Answering | [arXiv](https://arxiv.org/abs/2212.08037) | Evaluate answers against cited evidence |
| `MCP-BIB-ATTRIBUTION-EVAL` | Automatic Evaluation of Attribution by Large Language Models | [arXiv](https://arxiv.org/abs/2305.06311) | Measure whether claims are supported by evidence |
| `MCP-BIB-RARR` | RARR: Researching and Revising What Language Models Say | [arXiv](https://arxiv.org/abs/2210.08726) | Separate retrieval, checking, and final answer revision |
| `MCP-BIB-FACTSCORE` | FActScore | [arXiv](https://arxiv.org/abs/2305.14251) | Score factual support at claim level |
| `MCP-BIB-CONTAMINATION` | Benchmark Data Contamination of Large Language Models: A Survey | [arXiv](https://arxiv.org/abs/2406.04244) | Keep benchmark/gold-answer files out of the exposed MCP surface |
| `MCP-BIB-KNOWLEDGE-POISONING` | Exploring Knowledge Poisoning Attacks to Retrieval-Augmented Generation | [DOI](https://doi.org/10.1016/j.inffus.2025.103900) | Treat retrieved knowledge stores as attack surfaces |
| `MCP-BIB-NCSC-PROMPT-INJECTION` | NCSC: Prompt injection is not SQL injection | [NCSC](https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection) | Limit tool blast radius instead of relying on prompt wording |
| `MCP-BIB-NCSC-AI-CYBER` | NCSC: AI and cyber security | [NCSC](https://www.ncsc.gov.uk/guidance/ai-and-cyber-security-what-you-need-to-know) | Apply AI security controls to the tool surface |

See [the academic literature source note](academic-literature.md) and [the security model](../security-model.md).

## Methodology

| Source ID | Source | URL | Local treatment |
| --- | --- | --- | --- |
| `MCP-BIB-KARPATHY-LLM-WIKI` | Karpathy LLM Wiki methodology gist | [GitHub Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | Citation only because no explicit redistribution license is recorded |

See [the Karpathy methodology source note](karpathy-llm-wiki-methodology.md) and [the wiki index](../index.md).
