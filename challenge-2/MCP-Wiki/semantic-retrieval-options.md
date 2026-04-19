---
title: "Semantic Retrieval Options"
note_type: "decision-support"
status: "options-evaluated"
tags:
  - "mcp"
  - "semantic-retrieval"
  - "embeddings"
  - "vector-index"
search_terms:
  - "semantic retrieval options"
  - "embedding model selection"
  - "vector index selection"
  - "provenance preserving retrieval"
related:
  - "implementation-plan.md"
  - "decision-record.md"
  - "sources/bibliography.md"
  - "data/bibliography.json"
---

# Semantic Retrieval Options

This note evaluates embedding models and vector-index options for v1 semantic retrieval. The goal is to improve recall without weakening licensing, provenance, or reproducibility.

## Selection Criteria

| Criterion | Requirement |
| --- | --- |
| Licensing | Prefer explicit permissive licenses and local operation. Record model, dependency, and index licenses. |
| Provenance | Every vector must map back to note path, source ID, chunk offsets, source-note hash, and generated index manifest. |
| Reproducibility | Pin model ID, model revision, index code version, chunking policy, normalization, and corpus hash. |
| Security | Keep the same allowlist and denylist as lexical retrieval. Do not index benchmark, gold-answer, run, or local-state artifacts. |
| Government fit | Avoid sending source text to third-party APIs by default; keep external APIs as comparison baselines only. |
| Simplicity | Prefer exact deterministic search for the small Challenge 2 wiki before adding approximate indexes or vector databases. |

## Embedding Model Options

| Option | License posture | Strengths | Risks and caveats | v1 judgement |
| --- | --- | --- | --- | --- |
| `BAAI/bge-small-en-v1.5` | MIT model/license signal; model card says released models can be used commercially | Small, retrieval-oriented, local, 384-dimensional, strong current baseline for English search | English-only; record exact Hugging Face revision and model files before use | Preferred first evaluation candidate |
| `sentence-transformers/all-MiniLM-L6-v2` | Apache-2.0 license file present in Hugging Face repository | Very common, small, fast, local, 384-dimensional, easy to reproduce | Older model; truncates longer input; may underperform newer retrieval-specific models | Fallback baseline and regression comparison |
| `intfloat/e5-small-v2` | MIT license signal | Small, local, 512-token English model; strong retrieval family | Requires query/document prefix discipline; English-only | Good second candidate if BGE underperforms |
| `text-embedding-3-small` / `text-embedding-3-large` | Proprietary API service; OpenAI docs state API data is not used for training by default | Strong managed baseline, high quality, no local model-management burden | Sends corpus text to external API, cost, network dependency, weaker reproducibility than pinned local model files | Comparison-only unless project policy allows external embedding service |
| Larger or multilingual local models, for example BGE-M3 | Varies by model | Better multilingual or long-context coverage | More compute, larger artifacts, more dependency and license review | Defer until corpus need is proven |

## Vector Index Options

| Option | License posture | Strengths | Risks and caveats | v1 judgement |
| --- | --- | --- | --- | --- |
| Exact normalized matrix search with NumPy | NumPy uses a modified BSD license | Deterministic, simple, inspectable, no database service, ideal for small corpus; manifest and `.npz` artifact are easy to hash | Linear scan does not scale indefinitely | Preferred v1 baseline |
| scikit-learn `NearestNeighbors` with brute/cosine | 3-clause BSD | Familiar API and deterministic exact search | Extra dependency when NumPy is enough | Acceptable if it simplifies implementation |
| FAISS `IndexFlatIP` / exact indexes | MIT | Fast, mature, good growth path from exact to approximate search | Native binary dependency and index-format versioning; more operational surface | Use if NumPy exact search is too slow |
| `sqlite-vec` | MIT/Apache-2.0 dual-license signal; pre-v1 project | Keeps vectors and metadata close to SQLite, portable, useful local packaging story | Pre-v1 breaking-change risk and SQLite extension packaging | Study for later persistent local index |
| hnswlib | Apache-2.0 | Fast approximate search, small dependency | Approximate results and construction parameters add reproducibility burden | Not a v1 default |
| Chroma or Milvus | Apache-2.0 | Full vector database features, metadata filters, larger-scale operations | Overkill for v1; service lifecycle, telemetry/privacy, deployment, and upgrade management | Defer until scale requires a vector DB |

## Provisional V1 Baseline

Use a local, pinned, permissively licensed embedding model and an exact local vector matrix first:

- Primary candidate: `BAAI/bge-small-en-v1.5`.
- Fallback/comparison: `sentence-transformers/all-MiniLM-L6-v2`.
- Optional second retrieval candidate: `intfloat/e5-small-v2`.
- Index baseline: normalized vectors in a `.npz` file plus JSON metadata and exact cosine similarity with NumPy.

This is not the final model choice. It is the evaluation plan for the v1 implementation spike. The final model should be selected after running a small retrieval benchmark over the Challenge 2 wiki, including source-backed questions that require topic, entity, and source-note recall.

## Required Index Manifest

Every generated semantic index must include:

- model ID, model revision, model license, and local model file hashes;
- embedding library and version;
- vector index type and version;
- chunking policy, token/character limits, overlap, and normalization;
- corpus root, allowlist, denylist, source-register hash, and input note hashes;
- vector matrix hash and metadata hash;
- generated timestamp, git commit, dirty-state flag, and build command;
- benchmark/gold-answer exclusion proof.

## Related Sources

- [MCP Wiki bibliography](sources/bibliography.md)
- [Implementation plan](implementation-plan.md)
- [Security model](security-model.md)
- [Decision record](decision-record.md)
