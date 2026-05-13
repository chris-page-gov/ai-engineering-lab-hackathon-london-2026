---
exchange_id: "EX-0080"
title: "The Wiki is also available over GitHub, would that solve the Can't access local paths problem?"
source_id: "CONV-005"
global_sequence: 80
session_sequence: 28
user_timestamp: "2026-04-19T16:53:02.423Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0080. The Wiki is also available over GitHub, would that solve the Can't access local paths problem?

Previous: [EX-0079](0079-20260418065216-allow-claude-to-use-the-local-settings-file-which-is-specifying-the-model-managed-by-dsit.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0081](0081-20260418065216-claude-says-mcp-failed-related.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
The Wiki is also available over GitHub, would that solve the Can't access local paths problem?
Claude, with no parameters, runs as we want it to
 ai-engineering-lab-hackathon-london-2026 git:(codex/evaluation-versioning) claude
╭─── Claude Code v2.1.114 ───────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                    │ Tips for getting started                                          │
│                 Welcome back Chris!                │ Run /init to create a CLAUDE.md file with instructions for Claude │
│                                                    │ ───────────────────────────────────────────────────────────────── │
│                       ▐▛███▜▌                      │ Recent activity                                                   │
│                      ▝▜█████▛▘                     │ No recent activity                                                │
│                        ▘▘ ▝▝                       │                                                                   │
│                                                    │                                                                   │
│ Opus 4.6 (1M context) with hi… · API Usage Billing │                                                                   │
│  ~/repos/ai-engineering-lab-hackathon-london-2026  │                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
❯
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  ? for shortcuts

So can we ask that the user sets this up and we run with it?
I left it open, do you need me to close it?
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T16:53:12.543Z`

````text
I’ll treat this as two changes to verify rather than guess: first, whether GitHub wiki URLs are enough for the Microsoft web UI; second, whether Claude can be run by the harness without CLI parameters while still producing capturable output. I do not need you to close the Claude window unless it is holding a file lock or consuming the same terminal.
````

### Response 2 (commentary)

- Timestamp: `2026-04-19T16:53:41.246Z`

````text
The remote is the public fork, so GitHub URLs can help Microsoft if the web UI is allowed to fetch GitHub pages. Claude is different: launching the interactive shell only proves the managed settings load; my non-interactive probes still fail at the first API request, so I’m checking whether a true TTY interactive Claude request behaves differently.
````

### Response 3 (commentary)

- Timestamp: `2026-04-19T16:54:52.644Z`

````text
The interactive Claude request is hanging rather than returning a quick “OK”. I’ll wait once more, then I’ll close that test session if it does not complete, because leaving extra interactive Claude processes around can interfere with diagnosis.
````

### Response 4 (commentary)

- Timestamp: `2026-04-19T16:55:48.428Z`

````text
The true TTY Claude test also did not complete a trivial prompt, so the welcome screen alone is not enough for the harness. I’m doing one direct Microsoft GitHub-URL smoke now, because that will tell us whether public GitHub links can replace local paths for the web UI.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0079](0079-20260418065216-allow-claude-to-use-the-local-settings-file-which-is-specifying-the-model-managed-by-dsit.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0081](0081-20260418065216-claude-says-mcp-failed-related.md)
