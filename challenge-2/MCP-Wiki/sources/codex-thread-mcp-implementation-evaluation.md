---
source_id: "MCP-SRC-CODEX-THREAD-IMPLEMENTATION-EVAL"
title: "Codex Thread Capture: MCP Implementation And Evaluation"
source_type: "codex-thread-summary"
publication_status: "public-summary-not-raw-transcript"
license_status: "project-artifact"
status: "captured"
tags:
  - "source"
  - "codex-thread"
  - "mcp"
  - "evaluation"
  - "postmortem"
search_terms:
  - "Codex MCP implementation evaluation thread"
  - "Challenge 2 Wiki MCP conversation capture"
  - "Codex with MCP comparison evidence"
  - "M365 Copilot OneDrive MCP grounding"
related:
  - "../index.md"
  - "../implementation/README.md"
  - "../decision-record.md"
  - "../wiki-optimization-log.md"
  - "../../evaluation/reports/validated-full-20260419T2225Z-comparison.md"
---

# Codex Thread Capture: MCP Implementation And Evaluation

This note captures the current Codex thread as a public, publication-safe evidence summary. It is not a raw transcript. The raw conversation remains local application evidence unless the postmortem builder is rerun and a redacted public derivative is intentionally produced.

The thread is directly relevant to the current MCP research and evaluation branch because it records the transition from "Microsoft Copilot cannot reliably use the local or OneDrive wiki as a knowledge base" to "build and validate a purpose-built read-only Wiki MCP server, then compare Codex with MCP against the standard Codex path and other validated clients."

## Scope Captured

The thread covered:

- GitHub Copilot CLI authentication and policy blocking, including the distinction between personal GitHub authentication and organisation-level Copilot policy controls.
- PowerShell command-line continuation issues during smoke testing and the corrected single-line harness invocation.
- Best-model selection across clients, including explicit `gpt-5.4` selection for Codex and GitHub Copilot CLI, DSIT-managed Claude settings, Gemini preview selection, and Microsoft Copilot GPT-5 / Think Deeper caveats.
- Claude Code gateway failure analysis and the `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` compatibility setting for the DSIT-managed proxy.
- Microsoft Copilot grounding problems with local repository paths, public GitHub permalinks, OneDrive sync, shared OneDrive links, and the limits of the Copilot desktop app as an evaluation host.
- The conclusion that a Wiki MCP server is the right strategy for exposing the Challenge 2 wiki as controlled, audited knowledge.
- Deep Research incorporation, reference implementation review, license-aware submodule choices, MCP specification and Microsoft host-path decisions, and semantic retrieval decisions.
- Implementation of the read-only Challenge 2 Wiki MCP server, including path allowlists, benchmark denylists, source-register tools, context-pack tools, provenance explanations, deterministic semantic retrieval, and audit logging.
- Validation through unit tests, coverage, MCP wiki linting, live Codex-MCP smoke evidence, full benchmark comparison, rubric scoring, and sanitized report generation.
- The need to capture this thread as evidence for how the implementation and evaluation decisions were made.

## Contribution Analysis

Human contribution in this thread:

- Set the research and evaluation goal: compare all available AI clients with best-model settings and add Codex with MCP as a new path.
- Identified practical blockers from live use: GitHub Copilot policy denial, Claude proxy incompatibility, Microsoft Copilot local-path failure, OneDrive upload timing, and desktop-app limitations.
- Made design decisions where policy and intent mattered: include semantic retrieval in v1, prefer Copilot Studio direct MCP validation, exclude API-key auth unless live validation proves it necessary, and treat Claude local settings as authoritative.
- Raised publication and evidence questions, including whether the thread belongs in the postmortem, the MCP research wiki, or a separate record.
- Required a high validation bar: coverage over 90 percent for non-Copilot-specific functionality, comprehensive tests, full comparison reporting, and GitHub publication readiness.

Codex contribution in this thread:

- Diagnosed harness and shell-invocation failures and converted them into reusable evaluation behavior.
- Researched and structured the MCP research wiki, including source registers, candidate registers, bibliography, decision log, and lint checks.
- Implemented the Wiki MCP server and integrated it with the Challenge 2 evaluation harness as `codex-mcp`.
- Added deterministic semantic retrieval for validation while leaving the production embedding-model lock open pending benchmark evidence.
- Generated the comparison report and rubric-scored leaderboard showing the effect of Codex with MCP against standard Codex and other validated clients.
- Preserved source-boundary and publication constraints so research material, corpus wiki content, evaluation gold answers, and public postmortem material remain separated.

## Placement Options

| Option | Description | Strengths | Weaknesses | Recommendation |
| --- | --- | --- | --- | --- |
| Add this thread to `postmortem-public/` now | Rerun the Codex postmortem builder and publish it as another public conversation source. | Consistent with the earlier postmortem workflow and would increase the public conversation count. | It risks expanding a focused MCP implementation PR with regenerated postmortem material and may require another redaction pass over authentication, policy, local path, and UI details. | Defer unless the PR scope is explicitly widened to update the whole public postmortem. |
| Capture this thread in `challenge-2/MCP-Wiki/` | Add a summarized source note linked from the MCP wiki, decision record, and optimization log. | Best matches the thread's content because it explains MCP design, implementation, validation, and evaluation choices. Keeps raw transcript out of Git. | It is a summary rather than a full prompt-response transcript. | Use this now. |
| Keep only private/local evidence | Leave the raw thread in local Codex application history and mention it only in final PR notes. | Lowest publication risk. | Weakens the repo's evidence trail for why the MCP server and comparison report were created. | Not sufficient for this branch. |
| Create a separate follow-on postmortem branch | Finish the MCP implementation PR, then create a dedicated postmortem update branch that regenerates public conversation artifacts. | Cleanest separation if the full conversation count and public postmortem need updating. | Delays public traceability for MCP-specific decisions. | Use only if a full prompt-response postmortem update is needed after this PR. |

## Recommendation

This thread should form part of the current MCP pull request as a summarized public evidence note in the MCP research wiki. It explains the design pressure behind the Wiki MCP server, records the human/Codex split of contribution, and provides reviewers with the rationale for the evaluation artifacts already in the branch.

The raw transcript should not be included in this PR. A full postmortem-public regeneration should be handled separately, after a redaction and rendering pass, if the goal is to update the public postmortem conversation count from the previous five sources to include this sixth thread.

## Current PR Review Status

The PR review cycle after rubric scoring raised five implementation bug classes. The first pass found UTF-8 byte budgets being applied as character counts in context excerpts and HTTP JSON-RPC notifications being serialized as `{}` rather than treated as no-response messages. The follow-up pass found JSON-RPC handlers reading fields before validating request shape and an evaluation repo-state probe that aborted if Git was missing from `PATH`. The latest pass found that `codex-mcp` recorded configurable MCP server options for the prompt context-pack seed without forwarding them to the spawned answer-time server process. The PR now fixes those classes across the Wiki MCP, Workbench MCP, and evaluation MCP surfaces, adds regression tests for non-ASCII byte caps, HTTP notification `204 No Content` behavior, malformed request envelopes, missing-Git metadata, and `codex-mcp` server-argument reproducibility, and keeps raw transcript publication separate from this summary note.

## Publication Treatment

Publish:

- This summary note.
- Links to implementation and evaluation artifacts.
- Sanitized comparison metrics and reports.
- Public-safe rubric score summaries that omit raw prompts and answer text.
- Decision-log entries that explain branch scope and source boundaries.

Do not publish without another review:

- Raw local Codex transcripts.
- Screenshots or UI captures that reveal local account, policy, or tenant state.
- Local filesystem paths beyond already-approved conventional public paths.
- Run directories containing raw prompts, raw answers, audit bundles, or client screenshots.

## Evidence Links

- [MCP implementation workspace](../implementation/README.md)
- [MCP decision record](../decision-record.md)
- [MCP wiki optimization log](../wiki-optimization-log.md)
- [Security model](../security-model.md)
- [Semantic retrieval options](../semantic-retrieval-options.md)
- [Validated full comparison report](../../evaluation/reports/validated-full-20260419T2225Z-comparison.md)
- [MCP server CLI](../../tools/wiki_mcp_server.py)
- [Evaluation comparison generator](../../tools/compare_wiki_eval.py)
- [Evaluation clients](../../evaluation/clients.py)
- [Public postmortem conversation summary](../../../postmortem-public/wiki/conversation-summary.md)
