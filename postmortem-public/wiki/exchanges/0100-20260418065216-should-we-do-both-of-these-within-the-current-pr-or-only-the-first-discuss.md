---
exchange_id: "EX-0100"
title: "Should we do both of these within the current PR or only the first, discuss"
source_id: "CONV-005"
global_sequence: 100
session_sequence: 48
user_timestamp: "2026-04-20T06:22:10.217Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0100. Should we do both of these within the current PR or only the first, discuss

Previous: [EX-0099](0099-20260418065216-i-want-to-capture-this-thread-as-we-did-with-previous-ones-but-need-to-consider-how-this-i.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0101](0101-20260418065216-do-human-rubric-scoring-in-this-pr.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
# Selected text:

## Selection 1
Add human rubric scoring before presenting the report as a quality leaderboard.

## Selection 2
Run the embedding shortlist benchmark and lock the v1 semantic retrieval model.

## My request for Codex:
Should we do both of these within the current PR or only the first, discuss
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-20T06:22:14.465Z`

````text
I’ll look at the current PR scope, report wording, and the open TODOs around scoring and semantic retrieval so the recommendation is grounded in the branch rather than just project instincts.
````

### Response 2 (final_answer)

- Timestamp: `2026-04-20T06:22:41.506Z`

````text
I would not do both in the current PR.

My recommendation:

1. **Do human rubric scoring in this PR only if we intend the report to read as a quality leaderboard.**
2. **Defer the embedding shortlist benchmark and final model lock to a follow-up PR.**

Reasoning:

The current PR is already large: `63` changed files, about `8.7k` additions, and it introduces the MCP research wiki, the read-only Wiki MCP server, `codex-mcp`, evaluation integration, and the comparison report. Adding the thread capture was still within scope because it explains why this PR exists. Locking the semantic retrieval model is a different kind of work: it changes the retrieval implementation baseline, introduces model/dependency/licensing/reproducibility decisions, and may require disk/model artifact handling. That should be a clean follow-on branch.

For the **human rubric scoring**, the key question is presentation. The current report is carefully caveated:

> “automated proxy metrics only; no human rubric scores are asserted”

So it is publishable as a **completion/provenance/MCP-effect comparison**, but not as a true quality leaderboard. If we want this PR to claim “Codex with MCP performed better” in a qualitative way, then yes, we should add human scoring before merge. That is within the evaluation-report scope.

For the **embedding benchmark**, I would keep the current PR’s position:

- semantic retrieval exists behind the same provenance-preserving contract;
- the current backend is deterministic local hashing for validation;
- the real embedding model remains deliberately unlocked;
- the shortlist and benchmark criteria are documented.

That is defensible. Locking `BAAI/bge-small-en-v1.5` or another model now would blur two claims: “the MCP server works and improves auditability” versus “this is the selected production semantic retrieval model.” Those should be reviewed separately.

So the clean path is:

- **Current PR:** optionally add human rubric scoring, or keep the report explicitly labelled as proxy-metric comparison.
- **Next PR:** run the embedding shortlist benchmark, record model revisions/licenses/hashes, update the semantic manifest, and lock the v1 model based on evidence.

If time is limited, I would merge the current PR with the existing caveat intact and open two follow-up issues/tasks: one for human scoring, one for embedding model lock. If the public narrative needs a leaderboard now, do the human scoring before merging and still defer the embedding work.
````

## Contribution Reading

- User contribution: Asked Codex to inspect GitHub state and unblock the repository workflow.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0099](0099-20260418065216-i-want-to-capture-this-thread-as-we-did-with-previous-ones-but-need-to-consider-how-this-i.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0101](0101-20260418065216-do-human-rubric-scoring-in-this-pr.md)
