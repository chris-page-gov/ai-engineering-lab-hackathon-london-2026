---
title: "Public Codex Collaboration Postmortem"
tags:
  - "postmortem"
  - "codex-postmortem-public"
---

# Public Codex Collaboration Postmortem

## Executive Summary

This public postmortem explains how Team DSIT A built the Challenge 2 prototype with Codex while keeping the raw local evidence archive out of Git. The human team supplied the goal, constraints, review direction, and quality bar. Codex inferred much of the implementation detail by inspecting the repository, then produced code, documentation, tests, validation evidence, and synthesis.

The Challenge 2 committed baseline is `326a82a8f17440d49471dab6a11d2b725b879359`. Public repository evidence uses commit-specific GitHub permalinks where possible.

## Publication Boundary

- Raw Codex transcripts stay in the ignored private `postmortem/` folder.
- This `postmortem-public/` folder preserves sequence and contribution evidence in redacted form.
- Third-party methodology sources are cited by URL and private archive hash; full copied bodies are not redistributed here.
- Local machine paths, local Codex session paths, private reference repositories, and screenshot paths are replaced with placeholders.

## What The User Contributed

- Selected Challenge 2 and framed the outcome as making government dark data findable and structured.
- Named the Karpathy LLM Wiki pattern as the methodology to adapt.
- Set repository constraints: raw challenge data should remain immutable, documentation should move in lockstep, and validation should be run before completion claims.
- Identified product gaps, including the need for a question field that travels with Browser AI exports and saved checks.
- Requested a postmortem so the AI-assistant learning objective was explicit rather than hidden in commit history.

Team attribution: the Challenge 2 implementation work was done by Team DSIT A.

## What Codex Contributed

- Inspected the repository structure, challenge corpus, docs, Git state, validation tools, and external methodology sources.
- Converted the LLM Wiki idea into a Challenge 2 Obsidian-style generated wiki with source notes, topic/entity/map pages, registers, and linting.
- Built evaluation harnesses and workbench surfaces around the generated wiki.
- Managed PR hygiene, documentation lockstep, and validation runs.
- Generated the private postmortem archive and this public derivative from conversation evidence.

## Timeline

- `2026-04-16T02:40:08.652Z`: [Deep Research Prompt and Copilot Review](sources/conv-001-deep-research-prompt-and-copilot-review.md)
- `2026-04-16T08:49:39.697Z`: [Karpathy Wiki Planning and Challenge 2 Vault Build](sources/conv-002-karpathy-wiki-planning-and-challenge-2-vault-build.md)
- `2026-04-16T11:27:03.987Z`: [Wiki Evaluation Harness, Workbench, and Demo Route](sources/conv-003-wiki-evaluation-harness-workbench-and-demo-route.md)
- `2026-04-16T14:24:55.443Z`: [SeeLinks Question Box, PR Hygiene, and Baseline Cleanup](sources/conv-004-seelinks-question-box-pr-hygiene-and-baseline-cleanup.md)
- `2026-04-18T06:52:16.557Z`: [Codex Postmortem, Publication Assessment, and Version 1.1 PR](sources/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md)

## Lessons

1. Outcome-focused prompts worked because repository rules bounded Codex's freedom.
2. The useful collaboration pattern was prompt, inspect, infer, implement, validate, document, and preserve evidence.
3. Commit-specific links, generated registers, and lint reports are more reliable public evidence than memory or narrative alone.
4. A public postmortem needs a separate publication layer; raw assistant transcripts are valuable evidence but poor public artifacts.

## Start Points

- [Conversation Summary](conversation-summary.md)
- [Publication Decision Register](decisions.md)
- [Methodology Sources](methodology.md)
- [Repository Evidence](repository-evidence.md)
