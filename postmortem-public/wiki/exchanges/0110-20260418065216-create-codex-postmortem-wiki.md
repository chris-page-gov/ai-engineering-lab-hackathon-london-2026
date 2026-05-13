---
exchange_id: "EX-0110"
title: "Create Codex Postmortem Wiki"
source_id: "CONV-005"
global_sequence: 110
session_sequence: 58
user_timestamp: "2026-05-09T10:02:05.842Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0110. Create Codex Postmortem Wiki

Previous: [EX-0109](0109-20260418065216-create-codex-postmortem-wiki.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0111](0111-20260418065216-create-codex-postmortem-wiki.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
We will need the postmortem (full) and the redacted public-postmortem, with the first excluded from github
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-05-09T10:02:26.219Z`

````text
Understood. I’ll encode that split explicitly in the skill as a default rule: always produce both a full local postmortem and a redacted `public-postmortem`, with the full archive kept out of GitHub by default. I’m checking the current tracking-file structure so I can add the skill cleanly on `main`.
````

### Response 2 (commentary)

- Timestamp: `2026-05-09T10:02:35.395Z`

````text
I’ve confirmed the tracking-file layout. I’m adding the skill as a repo-local portable artifact now, with the private-full vs public-redacted split made explicit in both the trigger description and the workflow steps.
````

### Response 3 (commentary)

- Timestamp: `2026-05-09T10:03:17.933Z`

````text
The skill and tracking docs are in place. I’m running the lockstep and whitespace checks now, then I’ll give you the exact path and the portability note for using it in another project.
````

### Response 4 (final_answer)

- Timestamp: `2026-05-09T10:03:33.063Z`

````text
Yes. I created a reusable repo-local skill at [skills/assistant-postmortem-wiki/SKILL.md]([LOCAL_REPO]/skills/assistant-postmortem-wiki/SKILL.md) with a concrete reference note at [skills/assistant-postmortem-wiki/references/reference-implementation.md]([LOCAL_REPO]/skills/assistant-postmortem-wiki/references/reference-implementation.md).

The skill now encodes the rule you just clarified as the default:
- always build a full private postmortem archive
- always build a redacted public postmortem
- keep the full archive out of GitHub by default

It also captures the working pattern from this repo:
- read-only conversation sources
- sequenced prompt/response exchange notes
- artifact and citation registers
- commit-specific GitHub permalinks
- publication decisions and linting
- conservative handling of localized third-party methodology sources

I also updated [Changelog.md]([LOCAL_REPO]/Changelog.md), [Context.md]([LOCAL_REPO]/Context.md), and [Progress.md]([LOCAL_REPO]/Progress.md). `python3 tools/check_documentation_lockstep.py` and `git diff --check` both pass.

I kept it repo-local so it is portable. To use it in another project, copy or symlink the `skills/assistant-postmortem-wiki/` folder into that project, or install it into `[LOCAL_ASSISTANT_HOME]/skills/` as a global skill. I have not committed these changes yet.
````

## Contribution Reading

- User contribution: Defined the evidence-preservation goal and requested a research wiki plus analysis.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0109](0109-20260418065216-create-codex-postmortem-wiki.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0111](0111-20260418065216-create-codex-postmortem-wiki.md)
