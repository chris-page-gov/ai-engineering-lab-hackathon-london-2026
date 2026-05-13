---
exchange_id: "EX-0069"
title: "I want full coverage with the best models selected in each client so that includes GitHub Copilo"
source_id: "CONV-005"
global_sequence: 69
session_sequence: 17
user_timestamp: "2026-04-18T12:58:44.898Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0069. I want full coverage with the best models selected in each client so that includes GitHub Copilo

Previous: [EX-0068](0068-20260418065216-do-we-need-a-plan-or-are-we-ready-to-implement-the-evaluation-on-a-new-branch-i-want-to-ma.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0070](0070-20260418065216-override-and-use-gpt-5-4-on-copilot-as-i-found-contradictory-documentation-and-this-was-fr.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
I want full coverage with the best models selected in each client so that includes GitHub Copilot CLI and running Microsoft Copliot - which may need a brittle accessibility and/or playwright but needs to be included with appropriate caveats
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-18T12:58:55.364Z`

````text
Understood. I’ll extend the evaluator so the full coverage set includes GitHub Copilot CLI and a Microsoft Copilot desktop/web adapter, with the strongest practical model selector recorded for each and explicit caveats where the client cannot be made as deterministic as the headless CLIs. I’ll first verify current vendor/model guidance and the local Copilot CLI/app capabilities, then update the harness and docs on the existing evaluation branch.
````

### Response 2 (commentary)

- Timestamp: `2026-04-18T12:59:18.544Z`

````text
The documentation check confirms a few important choices: Copilot CLI’s programmatic docs now recommend pinning `gpt-5.3-codex` for complex coding, Claude Code exposes a `best` alias and Opus 4.7 effort settings, Gemini’s best practical non-interactive choice is still Auto routing for Gemini 3/3.1 availability, and Microsoft 365 Copilot Chat is documented as GPT-5 with automatic routing. I’m going to encode those choices and add Microsoft Copilot as an explicit caveated client rather than just passive app evidence.
````

### Response 3 (commentary)

- Timestamp: `2026-04-18T13:01:15.368Z`

````text
I’m updating the runner to support a named `full` client set instead of overloading the safer default. That will let us run `codex, gemini, claude, github-copilot, microsoft-copilot` together, while still making unavailable or UI-dependent clients show up explicitly in the audit rather than silently dropping out.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0068](0068-20260418065216-do-we-need-a-plan-or-are-we-ready-to-implement-the-evaluation-on-a-new-branch-i-want-to-ma.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0070](0070-20260418065216-override-and-use-gpt-5-4-on-copilot-as-i-found-contradictory-documentation-and-this-was-fr.md)
