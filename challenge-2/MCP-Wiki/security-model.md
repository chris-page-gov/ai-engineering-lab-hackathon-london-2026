---
title: "Wiki MCP Security Model"
note_type: "security-model"
tags:
  - "security"
  - "mcp"
  - "evaluation-safety"
search_terms:
  - "Wiki MCP security model"
  - "prompt injection mitigation"
  - "benchmark leakage"
  - "evaluation-safe MCP"
related:
  - "architecture.md"
  - "implementation-plan.md"
  - "authentication-options.md"
  - "semantic-retrieval-options.md"
  - "sources/academic-literature.md"
  - "sources/bibliography.md"
---

# Wiki MCP Security Model

## Baseline Position

The first Challenge 2 Wiki MCP server should be read-only, scoped, auditable, and benchmark-safe. It should expose the generated wiki as evidence, not the whole repository as a filesystem.

This posture follows [the architecture](architecture.md), [the implementation plan](implementation-plan.md), and the security sources catalogued in [the bibliography](sources/bibliography.md).

## Required Controls

- Canonical path resolution before every read.
- Allowlist roots for generated wiki notes, wiki data, and `challenge-2/AGENTS.md`.
- Denylist for `evaluation-benchmark.md`, `challenge-2/evaluation/`, generated run artifacts, raw postmortem archives, local state, and secrets.
- Symlink refusal unless explicitly reviewed.
- File extension allowlist.
- Maximum bytes per result and per request.
- No write, delete, shell, network, or raw repository read tools in evaluation mode.
- Structured audit events for every allowed and denied request.
- Deterministic citations from server-side metadata, not model-generated path guesses.
- OAuth 2.0 or Microsoft Entra ID / SSO for remote Copilot-facing production endpoints.
- Semantic retrieval must preserve path allowlists, denylists, source IDs, index hashes, and bounded response sizes.

## Prompt Injection Posture

Retrieved wiki text is untrusted data. The server should not execute instructions embedded in retrieved content, and downstream prompts should separate retrieved evidence from task instructions.

## Benchmark Leakage Posture

The benchmark and gold answers must never be indexed or exposed to evaluated clients. This is a hard test requirement, not only documentation.

## External Source Licensing

External source material can only be exposed through the server if the license allows redistribution. Citation-only sources should remain summarized and linked, not served in full.

## Authentication Posture

For local development, anonymous stdio and local-only HTTP are acceptable. For Copilot Studio-facing Streamable HTTP, use OAuth 2.0 or Microsoft Entra ID / SSO as the target production pattern. Static bearer tokens are acceptable only for private smoke tests or gateway-to-server controls. API-key support should be treated as a host-specific exception because Microsoft support differs across Copilot Studio and Microsoft 365 plugin paths.

See [authentication options](authentication-options.md) for the full evaluation.

API-key authentication is excluded from the v1 implementation unless live Copilot Studio validation proves it is required for a specific host path.

## Semantic Retrieval Posture

Semantic retrieval must be additive to deterministic lexical retrieval, not a replacement for provenance. The v1 implementation should start with local embeddings, an exact local vector matrix, and a manifest that records model revision, index type, corpus hashes, source IDs, and denylist proof. External embedding APIs are comparison-only unless project policy explicitly permits sending corpus text outside the local environment.

## Related

- [Academic literature and security sources](sources/academic-literature.md)
- [Authentication options](authentication-options.md)
- [Semantic retrieval options](semantic-retrieval-options.md)
- [Bibliography](sources/bibliography.md)
- [MCP specification sources](sources/mcp-specification.md)
- [Microsoft Copilot sources](sources/microsoft-copilot-mcp.md)
- [Decision record](decision-record.md)
