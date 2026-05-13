---
exchange_id: "EX-0111"
title: "Create Codex Postmortem Wiki"
source_id: "CONV-005"
global_sequence: 111
session_sequence: 59
user_timestamp: "2026-05-09T10:04:55.561Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0111. Create Codex Postmortem Wiki

Previous: [EX-0110](0110-20260418065216-create-codex-postmortem-wiki.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0112](0112-20260418065216-commit-these-changes-ensuring-all-the-documentation-is-in-lockstep.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Can you confirm that the full postmortem is Audit level tracing rather than summarising any conversations and responses
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-05-09T10:05:06.984Z`

````text
I’m going to verify this against the actual builder and the generated folder structure, because the distinction between full audit tracing and public summarisation is exactly the kind of thing that should be stated from the implementation, not from memory.
````

### Response 2 (final_answer)

- Timestamp: `2026-05-09T10:05:17.011Z`

````text
Yes. I updated the skill to make that the default contract.

It now says:
- produce a full private `postmortem/`
- produce a redacted public `public-postmortem/`
- keep the full `postmortem/` out of GitHub by default

Files:
- [SKILL.md]([LOCAL_REPO]/skills/assistant-postmortem-wiki/SKILL.md)
- [reference-implementation.md]([LOCAL_REPO]/skills/assistant-postmortem-wiki/references/reference-implementation.md)

I also kept the reference note explicit that this repo’s concrete implementation used `postmortem-public/`, while the skill’s portable default is `public-postmortem/`.

These changes are local only at the moment and not committed.
````

## Contribution Reading

- User contribution: Defined the evidence-preservation goal and requested a research wiki plus analysis.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.

Previous: [EX-0110](0110-20260418065216-create-codex-postmortem-wiki.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0112](0112-20260418065216-commit-these-changes-ensuring-all-the-documentation-is-in-lockstep.md)
