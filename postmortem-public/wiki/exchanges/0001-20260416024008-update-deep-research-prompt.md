---
exchange_id: "EX-0001"
title: "Update Deep Research Prompt"
source_id: "CONV-001"
global_sequence: 1
session_sequence: 1
user_timestamp: "2026-04-16T02:44:37.378Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0001. Update Deep Research Prompt

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-001 (Deep Research Prompt and Copilot Review)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
# Files mentioned by the user:

## Deep-Research-Prompt.md: [LOCAL_REFERENCE_REPO]/20260416-AILabHack/Deep-Research-Prompt.md

## My request for Codex:
When the innitial hackathon repo was produced I used this deep research prompt - but it now needs modifying as we have the published repo.

Update the prompt, save to the repo so that it now can be used to create the new research report.
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-16T02:44:42.085Z`

````text
I’ll update the prompt in the current repo, using the original prompt as source material and adapting it to the published repository context. First I’ll inspect the repo structure and read the existing prompt so the edited version lands in the right place and matches the current project.
````

### Response 2 (commentary)

- Timestamp: `2026-04-16T02:44:48.875Z`

````text
The current published repo has separate challenge briefs and data folders, so the old prompt’s “README-only” hypothesis is stale. I’m reading the repo docs now and will rewrite the prompt around the published challenge pack rather than the earlier exploratory state.
````

### Response 3 (commentary)

- Timestamp: `2026-04-16T02:45:03.451Z`

````text
I have enough of the published challenge pack to make the substantive update. I’m checking the repository metadata now so the prompt can tell the future researcher exactly what to verify, including commit history and the published source of truth.
````

### Response 4 (commentary)

- Timestamp: `2026-04-16T02:45:12.777Z`

````text
I’m going to add a new root-level `Deep-Research-Prompt.md`. The edit will replace the obsolete “initial findings” framing with a published-repo baseline, and it will keep the research output requirements for the report, Obsidian knowledge base, diagrams, attendee analysis, and facilitator/training recommendations.
````

### Response 5 (commentary)

- Timestamp: `2026-04-16T02:46:20.405Z`

````text
The new prompt has been added. I’m doing a quick verification pass now: checking the file content, Git diff, and whether the repository only contains the intended change.
````

### Response 6 (commentary)

- Timestamp: `2026-04-16T02:46:35.733Z`

````text
One detail I’m tightening before finishing: the new file inherited some typographic punctuation from the original prompt. I’m normalising the new prompt to plain ASCII so it is easier to diff and safer across Markdown tooling.
````

### Response 7 (final_answer)

- Timestamp: `2026-04-16T02:46:53.101Z`

````text
Created the updated prompt at [Deep-Research-Prompt.md]([LOCAL_REPO]/Deep-Research-Prompt.md:1).

It now reflects the published repository state: detailed challenge briefs, open brief, setup guide, starter data, judging model, FDE support, mocked/live AI model guidance, attendee-data handling, standards lens, output structure, diagrams, and repository gap analysis. I also made the prompt explicit that earlier README-only assumptions are obsolete and must be re-verified against the current repo.

Verification done:
- Read the published README, setup guide, open brief, and all four challenge briefs.
- Checked repo remotes and recent commit history.
- Confirmed the only working tree change is the new `Deep-Research-Prompt.md`.
- Normalised the new file to ASCII punctuation for cleaner diffs.

No tests were run; this was a documentation-only change.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.
