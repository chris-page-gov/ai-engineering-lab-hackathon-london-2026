---
title: "Wiki MCP Security Model"
note_type: "security-model"
tags:
  - "security"
  - "mcp"
  - "evaluation-safety"
---

# Wiki MCP Security Model

## Baseline Position

The first Challenge 2 Wiki MCP server should be read-only, scoped, auditable, and benchmark-safe. It should expose the generated wiki as evidence, not the whole repository as a filesystem.

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

## Prompt Injection Posture

Retrieved wiki text is untrusted data. The server should not execute instructions embedded in retrieved content, and downstream prompts should separate retrieved evidence from task instructions.

## Benchmark Leakage Posture

The benchmark and gold answers must never be indexed or exposed to evaluated clients. This is a hard test requirement, not only documentation.

## External Source Licensing

External source material can only be exposed through the server if the license allows redistribution. Citation-only sources should remain summarized and linked, not served in full.
