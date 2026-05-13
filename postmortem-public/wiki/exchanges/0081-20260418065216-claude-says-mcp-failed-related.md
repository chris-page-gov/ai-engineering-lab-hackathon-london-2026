---
exchange_id: "EX-0081"
title: "Claude says MCP Failed - related?"
source_id: "CONV-005"
global_sequence: 81
session_sequence: 29
user_timestamp: "2026-04-19T16:56:32.081Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0081. Claude says MCP Failed - related?

Previous: [EX-0080](0080-20260418065216-the-wiki-is-also-available-over-github-would-that-solve-the-can-t-access-local-paths-probl.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0082](0082-20260418065216-i-passed-the-claude-cli-error-to-claude-coworker-personal-authentication-and-had-this.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Claude says MCP Failed - related?
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T16:56:35.710Z`

````text
It may be related to the interactive Claude session, but it is not the main failure I’m seeing from the harness. The harness failure is an API/provider error after model resolution; the “MCP failed” notice is likely a separate local tool-server startup issue unless Claude depends on that MCP for the request.
````

### Response 2 (commentary)

- Timestamp: `2026-04-19T16:57:15.506Z`

````text
The GitHub URL smoke for Microsoft finished, and it selected Think Deeper, but the captured page text did not contain a usable JSON answer. It appears Copilot tried web-search/navigation against the GitHub tree and got stuck in “Exploring web search options,” so GitHub URLs help in principle but are not reliable enough by themselves for scoring.
````

### Response 3 (final_answer)

- Timestamp: `2026-04-19T16:57:29.182Z`

````text
The Claude **“MCP failed”** notice is probably not the main issue. It may mean one configured local MCP server failed to start, but the harness failure I see is different:

```text
context_management: Extra inputs are not permitted
Received Model Group=eu.anthropic.claude-opus-4-6-v1
```

That is an API/provider request-shape error from the DSIT-managed Claude endpoint. It is not obviously caused by MCP.

The important distinction: the Claude welcome screen proves the local settings load and identify **Opus 4.6**, but it does not prove an API request succeeds. I also started Claude in a real TTY and sent `Reply with OK only.`; it hung rather than returning. So before we can include Claude as “successful”, please try this in the Claude window you already have open:

```text
Reply with OK only.
```

If it returns `OK`, then interactive Claude works and the problem is specifically non-interactive automation. If it hangs or errors, the DSIT-managed provider needs fixing before the benchmark.

You do **not** need to close the Claude window for me unless you want a clean manual retest. Leaving it open is fine.

On Microsoft Copilot and GitHub URLs: they help in principle, but they do not fully solve the problem alone. I tested a prompt pointing Microsoft Copilot at the public GitHub wiki URLs. It selected **Think Deeper**, but the captured answer did not produce usable JSON; it appeared to get stuck trying to browse/search the GitHub tree.

So for Microsoft, the reliable path is:

1. Use **commit-pinned GitHub URLs** for provenance.
2. Also inject the relevant wiki context into the prompt, or generate a small per-question source bundle.
3. Record that Microsoft answered from provided context plus GitHub permalinks, not from local filesystem access.

Using only GitHub tree URLs is too brittle for scoring because Microsoft may fail to browse, search, or parse the repository pages consistently.

Current readiness:

```text
Codex              OK
Gemini             OK
Microsoft Copilot  UI OK, Think Deeper selectable, needs context injection
Claude             needs manual OK test / provider fix
GitHub Copilot     still policy_blocked
```

Next thing I need from you: in the open Claude window, send `Reply with OK only.` and tell me whether it responds, hangs, or errors.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0080](0080-20260418065216-the-wiki-is-also-available-over-github-would-that-solve-the-can-t-access-local-paths-probl.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0082](0082-20260418065216-i-passed-the-claude-cli-error-to-claude-coworker-personal-authentication-and-had-this.md)
