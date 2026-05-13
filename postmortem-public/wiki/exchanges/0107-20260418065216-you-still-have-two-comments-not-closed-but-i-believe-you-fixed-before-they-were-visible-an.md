---
exchange_id: "EX-0107"
title: "You still have two comments not closed but I believe you fixed before they were \"visible\" and yo"
source_id: "CONV-005"
global_sequence: 107
session_sequence: 55
user_timestamp: "2026-04-20T10:06:07.506Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0107. You still have two comments not closed but I believe you fixed before they were "visible" and yo

Previous: [EX-0106](0106-20260418065216-yet-more-comments-to-fix-as-before.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0108](0108-20260418065216-merge.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
You still have two comments not closed but I believe you fixed before they were "visible" and you have yet more bugs
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-20T10:06:22.941Z`

````text
I’ll re-open the PR state from GitHub rather than relying on the previous check. I’m going to pull both thread-aware review data and the flat review bodies, because some Codex findings have been showing up outside normal resolvable threads.
````

### Response 2 (commentary)

- Timestamp: `2026-04-20T10:06:31.642Z`

````text
GitHub now shows one new active unresolved thread on `WikiKnowledgeBase.search`: lexical searches are still building/querying the semantic index. The two older “stale output” and “source-register root” items are review-body findings, not resolvable review threads; I already fixed and commented on them, but I’ll include that explicitly again after this new fix so the PR trail is unambiguous.
````

### Response 3 (commentary)

- Timestamp: `2026-04-20T10:06:49.734Z`

````text
I’ve read the search path. The right fix is broader than the exact line: `search()` should only run the retrieval engines required by the selected mode, so lexical-only does not touch semantic state and semantic-only does not spend time on lexical scoring.
````

### Response 4 (commentary)

- Timestamp: `2026-04-20T10:07:06.169Z`

````text
The implementation and regression test are patched. I’m running the targeted test now, then I’ll update the tracking docs and MCP source-register/lint artifacts for this new review class.
````

### Response 5 (commentary)

- Timestamp: `2026-04-20T10:07:33.955Z`

````text
I’ve updated the tracking docs to record this as the eleventh review bug class. Now I’m refreshing the MCP source-register hash and lint reports, then I’ll run the full validation set again.
````

### Response 6 (commentary)

- Timestamp: `2026-04-20T10:07:46.705Z`

````text
The MCP wiki lint is clean after the source-register refresh. I’m running the full local gate now, including coverage, because this is another behavior fix in the MCP package.
````

### Response 7 (commentary)

- Timestamp: `2026-04-20T10:08:14.850Z`

````text
The broader validation results are now recorded in `Progress.md`. I’m doing a final lockstep/whitespace check, then I’ll commit and push this review fix.
````

### Response 8 (commentary)

- Timestamp: `2026-04-20T10:08:24.859Z`

````text
Committed the retrieval-mode fix as `e57c845`. I’m pushing it and then closing the new active review thread with a specific note.
````

### Response 9 (commentary)

- Timestamp: `2026-04-20T10:08:50.188Z`

````text
The new semantic/lexical review thread is replied to and resolved. I’m adding a short PR-level clarification for the two older review-body findings that GitHub does not expose as closable threads, then I’ll request another review.
````

### Response 10 (commentary)

- Timestamp: `2026-04-20T10:09:04.656Z`

````text
There are zero active unresolved review threads now. CI is running again from the push; documentation-lockstep and mcp are already green, with workbench still in progress. I’ll wait for that check and then re-check for the new Codex review result.
````

### Response 11 (commentary)

- Timestamp: `2026-04-20T10:09:47.147Z`

````text
CI is green after the latest push. I’m checking the review threads and latest review body now.
````

### Response 12 (commentary)

- Timestamp: `2026-04-20T10:09:56.920Z`

````text
PR state is clean and CI is green. The new `@codex review` comment has been acknowledged with an eyes reaction but has not posted its new automated review yet, so I’ll give it another short wait before closing this out.
````

### Response 13 (final_answer)

- Timestamp: `2026-04-20T10:11:50.941Z`

````text
You were right. A new Codex review arrived after my last check, and one active thread was open.

I fixed it in `e57c845`:
- [core.py]([LOCAL_REPO]/challenge-2/MCP-Wiki/implementation/wiki_mcp/core.py): `WikiKnowledgeBase.search()` now only runs the retrieval engine needed by the selected mode.
- Lexical mode no longer builds or queries semantic vectors.
- Semantic mode no longer runs lexical scoring.
- Hybrid still runs both.
- Added regression coverage in [test_challenge2_wiki_mcp_server.py]([LOCAL_REPO]/tests/test_challenge2_wiki_mcp_server.py) that fails if the unused retrieval path is called.

On the “two comments not closed”: those were Codex review-body findings, not GitHub review threads, so GitHub does not expose them as closable/resolvable thread IDs. I added a PR-level clarification linking them to the fixing commit `a6169b9`, and also noted the new retrieval fix in `e57c845`.

Current PR state:
- Active unresolved review threads: `0`
- CI: green (`documentation-lockstep`, `mcp`, `workbench`)
- Branch: clean and pushed
- Latest `@codex review` request is acknowledged with an eyes reaction, but no new automated review has posted yet.

Validation run:
- `python3 -m unittest tests.test_challenge2_wiki_mcp_server tests.test_challenge2_workbench_mcp tests.test_challenge2_eval_mcp tests.test_challenge2_run_wiki_eval tests.test_challenge2_eval_clients tests.test_challenge2_compare_wiki_eval`
- MCP package coverage remains `91%`
- `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report`
- `python3 tools/check_documentation_lockstep.py`
- `git diff --check`

::git-stage{cwd="[LOCAL_REPO]"}
::git-commit{cwd="[LOCAL_REPO]"}
::git-push{cwd="[LOCAL_REPO]" branch="codex/wiki-mcp-research"}
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0106](0106-20260418065216-yet-more-comments-to-fix-as-before.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0108](0108-20260418065216-merge.md)
