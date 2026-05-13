---
source_id: "CONV-001"
title: "Deep Research Prompt and Copilot Review Reader"
reader_type: "redacted_start_to_finish_conversation"
publication_status: "redacted-public-derivative"
exchange_count: 2
tags:
  - "reader"
  - "conversation"
  - "codex-postmortem-public"
---

# CONV-001: Deep Research Prompt and Copilot Review

This redacted public reader inlines the prompt-response exchanges for one conversation in chronological order. It is the standard GitHub-friendly route for reading the conversation from start to finish without opening each exchange note separately.

## Navigation

- Index: [Public Codex Postmortem](../index.md)
- Conversation source note: [CONV-001](../sources/conv-001-deep-research-prompt-and-copilot-review.md)
- Raw transcript: retained only in the private local evidence archive.

## Exchange Map

| Exchange | Prompt | Standalone Note |
|---|---|---|
| [EX-0001](#ex-0001) | Update Deep Research Prompt | [note](../exchanges/0001-20260416024008-update-deep-research-prompt.md) |
| [EX-0002](#ex-0002) | There are some claude artifacts in the [LOCAL_REFERENCE_REPO]/.claude/ folder,  s | [note](../exchanges/0002-20260416024008-there-are-some-claude-artifacts-in-the-local-reference-repo-claude-folder-s.md) |

## Conversation

<a id="ex-0001"></a>

### EX-0001: Update Deep Research Prompt

- User timestamp: `2026-04-16T02:44:37.378Z`
- Standalone note: [EX-0001](../exchanges/0001-20260416024008-update-deep-research-prompt.md)

#### User Prompt

````text
# Files mentioned by the user:

## Deep-Research-Prompt.md: [LOCAL_REFERENCE_REPO]/20260416-AILabHack/Deep-Research-Prompt.md

## My request for Codex:
When the innitial hackathon repo was produced I used this deep research prompt - but it now needs modifying as we have the published repo.

Update the prompt, save to the repo so that it now can be used to create the new research report.
````

#### Codex Response

##### Response 1 (commentary)

- Timestamp: `2026-04-16T02:44:42.085Z`

````text
I’ll update the prompt in the current repo, using the original prompt as source material and adapting it to the published repository context. First I’ll inspect the repo structure and read the existing prompt so the edited version lands in the right place and matches the current project.
````

##### Response 2 (commentary)

- Timestamp: `2026-04-16T02:44:48.875Z`

````text
The current published repo has separate challenge briefs and data folders, so the old prompt’s “README-only” hypothesis is stale. I’m reading the repo docs now and will rewrite the prompt around the published challenge pack rather than the earlier exploratory state.
````

##### Response 3 (commentary)

- Timestamp: `2026-04-16T02:45:03.451Z`

````text
I have enough of the published challenge pack to make the substantive update. I’m checking the repository metadata now so the prompt can tell the future researcher exactly what to verify, including commit history and the published source of truth.
````

##### Response 4 (commentary)

- Timestamp: `2026-04-16T02:45:12.777Z`

````text
I’m going to add a new root-level `Deep-Research-Prompt.md`. The edit will replace the obsolete “initial findings” framing with a published-repo baseline, and it will keep the research output requirements for the report, Obsidian knowledge base, diagrams, attendee analysis, and facilitator/training recommendations.
````

##### Response 5 (commentary)

- Timestamp: `2026-04-16T02:46:20.405Z`

````text
The new prompt has been added. I’m doing a quick verification pass now: checking the file content, Git diff, and whether the repository only contains the intended change.
````

##### Response 6 (commentary)

- Timestamp: `2026-04-16T02:46:35.733Z`

````text
One detail I’m tightening before finishing: the new file inherited some typographic punctuation from the original prompt. I’m normalising the new prompt to plain ASCII so it is easier to diff and safer across Markdown tooling.
````

##### Response 7 (final_answer)

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

[Back to exchange map](#exchange-map)

<a id="ex-0002"></a>

### EX-0002: There are some claude artifacts in the [LOCAL_REFERENCE_REPO]/.claude/ folder,  s

- User timestamp: `2026-04-16T06:55:53.282Z`
- Standalone note: [EX-0002](../exchanges/0002-20260416024008-there-are-some-claude-artifacts-in-the-local-reference-repo-claude-folder-s.md)

#### User Prompt

````text
There are some claude artifacts in the [LOCAL_REFERENCE_REPO]/.claude/ folder,  settings.local.json I think, that I need duplicated in a similar folder in this repo - can you do that
````

#### Codex Response

##### Response 1 (commentary)

- Timestamp: `2026-04-16T06:56:25.523Z`

````text
I’ll copy the Claude configuration artifacts into this repo, preserving the same `.claude/` layout. First I’ll inspect the source folder and confirm what files are there so I only duplicate the relevant artifacts.
````

##### Response 2 (commentary)

- Timestamp: `2026-04-16T06:56:35.969Z`

````text
The source `.claude` folder only contains `settings.local.json`, and this repo does not currently have a `.claude` folder. I’m creating the matching folder here and copying that file across unchanged.
````

##### Response 3 (commentary)

- Timestamp: `2026-04-16T06:56:45.788Z`

````text
The copy completed and `cmp` confirms the new file is byte-identical to the original. I’m checking whether Git is intentionally ignoring it, since local Claude settings often are not meant to be committed.
````

##### Response 4 (final_answer)

- Timestamp: `2026-04-16T06:56:48.492Z`

````text
Copied the Claude artifact into this repo:

[settings.local.json]([LOCAL_REPO]/.claude/settings.local.json)

I verified it is byte-identical to `[LOCAL_REFERENCE_REPO]/.claude/settings.local.json`.

Git is not showing it because `.claude/` is ignored via `[LOCAL_REPO]/.git/info/exclude`. Existing untracked review files were left untouched.
````

[Back to exchange map](#exchange-map)
