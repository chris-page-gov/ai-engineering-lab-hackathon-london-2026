---
exchange_id: "EX-0103"
title: "Okay, more comments to fix as before"
source_id: "CONV-005"
global_sequence: 103
session_sequence: 51
user_timestamp: "2026-04-20T08:22:11.824Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0103. Okay, more comments to fix as before

Previous: [EX-0102](0102-20260418065216-so-is-this-thread-up-to-date-in-the-pr-should-we-wait-till-after-the-pr-is-reviewed-and-fu.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0104](0104-20260418065216-okay-more-comments-to-fix-as-before.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Okay, more comments to fix as before
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-20T08:22:16.361Z`

````text
I’ll pull the new PR review threads, group them by bug class, then patch every matching instance across the repo before resolving the comments and requesting another review.
````

### Response 2 (commentary)

- Timestamp: `2026-04-20T08:22:25.586Z`

````text
The follow-up Codex review has returned against `f2b955a`. I’m fetching the thread-aware comments now so I can see which unresolved items are new and whether they point to a broader pattern.
````

### Response 3 (commentary)

- Timestamp: `2026-04-20T08:22:36.734Z`

````text
There are two new unresolved classes: JSON-RPC request-shape validation in the MCP server, and missing-executable handling around subprocess metadata probes. I’m going to inspect the implementation and search for equivalent subprocess wrappers before editing.
````

### Response 4 (commentary)

- Timestamp: `2026-04-20T08:23:35.616Z`

````text
I found the same request-shape assumption in the Wiki MCP, Workbench MCP, and evaluation MCP servers. I also found the only live repo-state probe that should be non-fatal when `git` is missing; other Git subprocess calls are repository maintenance checks or generated-postmortem helpers, so I’ll make those fail cleanly rather than pretending metadata exists.
````

### Response 5 (commentary)

- Timestamp: `2026-04-20T08:23:36.937Z`

````text
I’m making the protocol-surface edits now: reject non-object or invalid JSON-RPC request shapes before accessing fields, validate `params` and tool arguments as objects, and keep notification handling unchanged.
````

### Response 6 (commentary)

- Timestamp: `2026-04-20T08:24:13.671Z`

````text
I’m tightening that edit so only malformed JSON-RPC parameter envelopes map to `-32602`; existing tool-level `ValueError`s, such as unknown tool names, keep their prior generic error path.
````

### Response 7 (commentary)

- Timestamp: `2026-04-20T08:24:47.526Z`

````text
I’m addressing the missing-Git class next. The evaluation runner should keep going with explicit `git_available: false` metadata, while repository-maintenance scripts should fail with a clear message instead of a traceback.
````

### Response 8 (commentary)

- Timestamp: `2026-04-20T08:25:21.600Z`

````text
I’m adding regression coverage on each affected surface: Wiki MCP directly, the two stdio MCP helpers through their CLI loops, and the evaluation runner’s Git metadata probe.
````

### Response 9 (commentary)

- Timestamp: `2026-04-20T08:25:56.712Z`

````text
While applying the same resilience rule, I also found the Workbench MCP stdio loop did not catch JSON parse errors. I’m bringing it into line with the other MCP loops so malformed input returns a protocol error instead of killing the process.
````

### Response 10 (commentary)

- Timestamp: `2026-04-20T08:26:11.825Z`

````text
I noticed one subtle issue in my first parameter helper: `params: []` is falsy, so `or {}` would hide the invalid shape. I’m correcting the helpers to distinguish missing/null from the wrong JSON type.
````

### Response 11 (commentary)

- Timestamp: `2026-04-20T08:26:32.878Z`

````text
The code changes are in place. I’m updating the repository tracking docs and the MCP research note so the PR evidence records this second review cycle instead of leaving the postmortem trail stale.
````

### Response 12 (commentary)

- Timestamp: `2026-04-20T08:27:29.768Z`

````text
The docs and source register are updated. I’m going to run the targeted tests first, including the new regression tests, then I’ll run lint and lockstep checks.
````

### Response 13 (commentary)

- Timestamp: `2026-04-20T08:27:40.770Z`

````text
The targeted py_compile and unit suite passed: 32 tests. The remaining search hits are expected request-field reads after type checks and subprocess timeout handlers with missing-executable handling now in place; I’m running the wiki lint and lockstep gates now.
````

### Response 14 (commentary)

- Timestamp: `2026-04-20T08:27:48.753Z`

````text
All local gates have passed. I’m reviewing the final diff and checking for generated report churn before committing and pushing the fix.
````

### Response 15 (commentary)

- Timestamp: `2026-04-20T08:27:54.411Z`

````text
The final diff matches the two requested bug classes plus documentation and regression tests. I’m staging, committing, and pushing this review-fix pass now.
````

### Response 16 (commentary)

- Timestamp: `2026-04-20T08:28:05.078Z`

````text
The fix commit `fd93a2d` is pushed. I’m replying to the two review threads with what changed, resolving them, then I’ll ask Codex for another review.
````

### Response 17 (commentary)

- Timestamp: `2026-04-20T08:28:20.272Z`

````text
Both new review threads are replied to and resolved. I’m triggering another review and then I’ll verify PR status and checks.
````

### Response 18 (commentary)

- Timestamp: `2026-04-20T08:28:36.448Z`

````text
The new review request has been picked up. The PR threads are resolved; GitHub shows `documentation-lockstep` and `mcp` passed, with `workbench` still running, so I’ll wait briefly for that check before finalizing.
````

### Response 19 (commentary)

- Timestamp: `2026-04-20T08:29:27.681Z`

````text
All GitHub checks are now green and the PR is merge-clean. The new Codex review trigger is still in progress, so I’ll give it a little longer to return before I stop.
````

### Response 20 (commentary)

- Timestamp: `2026-04-20T08:30:01.459Z`

````text
The PR checks are stable; I’m still waiting on the asynchronous Codex review response to the latest trigger.
````

### Response 21 (commentary)

- Timestamp: `2026-04-20T08:30:35.271Z`

````text
No new review result yet; the trigger remains acknowledged by Codex. I’ll do one more poll at the end of this wait window, then I’ll report the state plainly.
````

### Response 22 (final_answer)

- Timestamp: `2026-04-20T08:31:44.497Z`

````text
Fixed the new PR comments and treated them as repo-wide bug classes.

Changes pushed in `fd93a2d Harden MCP request validation`:

- Hardened JSON-RPC request validation across `WikiMcpServer`, `workbench_mcp.py`, and `wiki_eval_mcp.py`.
- Non-object requests now return `-32600` instead of crashing.
- Invalid `params` / `arguments` envelopes now return `-32602`.
- Workbench MCP stdio now returns parse errors instead of terminating on invalid JSON.
- `run_wiki_eval.py` now records missing Git as non-fatal repo-state metadata with `git_available: false`.
- Related Git subprocess helpers now fail clearly if Git is unavailable, rather than throwing raw tracebacks.
- Added regression coverage for all of the above.
- Updated the MCP thread note, implementation note, source register, lint reports, and tracking docs.

Validation passed locally:

- `py_compile` for changed Python entry points and helpers
- `python3 -m unittest ...` across 32 targeted tests
- `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report`
- `python3 tools/check_documentation_lockstep.py`
- `git diff --check`
- JSON validation for updated MCP data files

On GitHub, all checks are green: `documentation-lockstep`, `mcp`, and `workbench`. I replied to and resolved both new PR review threads, then posted another `@codex review`. Codex has acknowledged the trigger with an eyes reaction, but it has not yet posted the next completed review.

The branch is clean and pushed to `origin/codex/wiki-mcp-research`.

::git-stage{cwd="[LOCAL_REPO]"}
::git-commit{cwd="[LOCAL_REPO]"}
::git-push{cwd="[LOCAL_REPO]" branch="codex/wiki-mcp-research"}
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.

Previous: [EX-0102](0102-20260418065216-so-is-this-thread-up-to-date-in-the-pr-should-we-wait-till-after-the-pr-is-reviewed-and-fu.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0104](0104-20260418065216-okay-more-comments-to-fix-as-before.md)
