---
exchange_id: "EX-0083"
title: "It looked like the Microsoft 365 Copilot failed because the prompt specified:"
source_id: "CONV-005"
global_sequence: 83
session_sequence: 31
user_timestamp: "2026-04-19T17:19:06.583Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0083. It looked like the Microsoft 365 Copilot failed because the prompt specified:

Previous: [EX-0082](0082-20260418065216-i-passed-the-claude-cli-error-to-claude-coworker-personal-authentication-and-had-this.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0084](0084-20260418065216-if-github-access-fails-for-the-m365-copilot-can-we-just-have-the-wiki-replicated-in-onedri.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
It looked like the Microsoft 365 Copilot failed because the prompt specified:
Use only these local repository sources as authority:
- [LOCAL_REPO]/challenge-2/wiki
- [LOCAL_REPO]/challenge-2/wiki/data
- [LOCAL_REPO]/challenge-2/AGENTS.md
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T17:19:11.321Z`

````text
Yes, that is the main Microsoft issue. The web UI has no local filesystem access, so that prompt is correct for CLI clients but wrong for Microsoft Copilot unless we either replace local paths with public permalinks or inject the relevant source text into the prompt. I’m also waiting on the Claude Opus smoke I just started.
````

### Response 2 (commentary)

- Timestamp: `2026-04-19T17:19:42.657Z`

````text
The Claude Opus smoke confirms the best setup is `--model opus` plus the beta-disable flag: it completed and the captured usage shows `eu.anthropic.claude-opus-4-6-v1`. I’m going to adjust the checked-in config to use that Opus alias instead of the placeholder local-settings label.
````

### Response 3 (commentary)

- Timestamp: `2026-04-19T17:20:01.006Z`

````text
You’re right: the prompt builder is client-neutral today, so Microsoft receives local filesystem paths that only the CLI clients can use. I’m adding a Microsoft-specific prompt mode that replaces those with GitHub permalinks and, for smoke/scoring viability, can inject selected wiki source excerpts directly into the prompt.
````

### Response 4 (commentary)

- Timestamp: `2026-04-19T17:21:20.437Z`

````text
The dry-run prompt now gives Microsoft GitHub permalinks and copied source excerpts instead of local-only paths. I’m running a Microsoft-only live smoke with that prompt so we can see whether the answer becomes scoreable.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0082](0082-20260418065216-i-passed-the-claude-cli-error-to-claude-coworker-personal-authentication-and-had-this.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0084](0084-20260418065216-if-github-access-fails-for-the-m365-copilot-can-we-just-have-the-wiki-replicated-in-onedri.md)
