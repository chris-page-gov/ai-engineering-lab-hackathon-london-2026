---
exchange_id: "EX-0034"
title: "Add Documentation Lockstep and Evaluation Notes"
source_id: "CONV-003"
global_sequence: 34
session_sequence: 1
user_timestamp: "2026-04-16T11:31:37.948Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0034. Add Documentation Lockstep and Evaluation Notes

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-003 (Wiki Evaluation Harness, Workbench, and Demo Route)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
This is documentation only
Fully understand the Wiki for Challenge 2, design 100 questions that can be answered correctly by the wiki. Give the Gold answer for each, an evaluation rubric, a summative scoring regime so that we can design a harness to feed each AI on this system (Gemini CLI, Claude Code and Codex) with questions, record answers and do a compatitive evaluation on how well each uses the Wiki
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-16T11:31:39.809Z`

````text
I’ll inspect the repo for the Challenge 2 wiki/docs first, then I’ll turn that content into a documentation-only benchmark: questions, gold answers, per-question rubrics, and an aggregate scoring scheme suitable for a harness.
````

### Response 2 (commentary)

- Timestamp: `2026-04-16T11:31:51.718Z`

````text
I found the Challenge 2 vault under `challenge-2/wiki/`: generated source notes, topic pages, entity pages, content maps, table exports, and a source register. I’m going to read the wiki layer rather than the raw binary files, because the benchmark should evaluate whether agents can use the wiki as the authority.
````

### Response 3 (commentary)

- Timestamp: `2026-04-16T11:32:06.803Z`

````text
The high-level wiki confirms the benchmark should test not just factual lookup, but also source status, stale/superseded flags, topic-to-source navigation, table exports, and provenance. I’m drilling into the generated source notes and exported tables now so the gold answers use exact values rather than broad summaries.
````

### Response 4 (commentary)

- Timestamp: `2026-04-16T11:33:01.077Z`

````text
I’ve covered the structured housing, business, and employment notes, including the deliberate version conflicts. The remaining pass is on the “dark data” side: DWP policies, scanned/OCR-like notes, staff directory, and the spreadsheet exports.
````

### Response 5 (commentary)

- Timestamp: `2026-04-16T11:35:32.109Z`

````text
I have enough source coverage now. I’m adding a standalone documentation file under `challenge-2/` with the benchmark spec, 100 question records, gold answers, per-question rubrics, and a total scoring regime; I’m leaving the raw corpus and generator untouched.
````

### Response 6 (commentary)

- Timestamp: `2026-04-16T11:39:49.872Z`

````text
The benchmark draft is in place. I’m doing a quick structural check now: question count, frontmatter, and a scan for obvious formatting problems before I hand it back.
````

### Response 7 (final_answer)

- Timestamp: `2026-04-16T11:40:36.808Z`

````text
Created the documentation-only benchmark at [challenge-2/evaluation-benchmark.md]([LOCAL_REPO]/challenge-2/evaluation-benchmark.md:1).

It includes:

- A common harness prompt for Gemini CLI, Claude Code, and Codex.
- Recommended captured fields for answer recording.
- A default 0-5 per-question rubric with source/caveat penalties.
- A 500-point summative scoring regime with category subscores and tie-breakers.
- 100 wiki-answerable questions, each with a gold answer, sources, and a question-specific rubric.

Verification done:

- Confirmed exactly `100` question headings.
- Confirmed question IDs are sequential `Q001` through `Q100`.
- Left the unrelated modified file `challenge-2/.obsidian/workspace.json` untouched.
````

## Contribution Reading

- User contribution: Constrained the task to documentation and evaluation design.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.
