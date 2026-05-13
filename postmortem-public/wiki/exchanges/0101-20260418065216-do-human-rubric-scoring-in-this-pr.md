---
exchange_id: "EX-0101"
title: "Do human rubric scoring in this PR"
source_id: "CONV-005"
global_sequence: 101
session_sequence: 49
user_timestamp: "2026-04-20T06:25:05.228Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0101. Do human rubric scoring in this PR

Previous: [EX-0100](0100-20260418065216-should-we-do-both-of-these-within-the-current-pr-or-only-the-first-discuss.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0102](0102-20260418065216-so-is-this-thread-up-to-date-in-the-pr-should-we-wait-till-after-the-pr-is-reviewed-and-fu.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Do human rubric scoring in this PR
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-20T06:25:19.309Z`

````text
I’ll add this within the current PR by using the published Challenge 2 rubrics as the scoring basis, then update the report so it distinguishes rubric-scored quality from the existing proxy metrics. First I’m going to inspect the run artifacts and scoring tooling so I don’t invent a parallel format.
````

### Response 2 (commentary)

- Timestamp: `2026-04-20T06:25:33.126Z`

````text
The report and tooling already support a scoring sheet, but the raw run directory isn’t at the expected `/tmp` location anymore. I’m checking the ignored run folder and the committed metrics to see whether enough answer data remains locally; if not, I’ll need to regenerate or recover the scoring inputs before I can score honestly.
````

### Response 3 (commentary)

- Timestamp: `2026-04-20T06:26:33.342Z`

````text
The full run directory is still available under `/tmp/challenge2-wiki-eval-full/validated-full-20260419T2225Z`, including `answers.jsonl` and the generated scoring sheet. I’m going to add committed aggregate/per-question scoring outputs without committing raw answers, and I’ll keep the report wording precise about the scoring basis.
````

### Response 4 (commentary)

- Timestamp: `2026-04-20T06:28:03.927Z`

````text
I’m going to run a rubric-scoring pass over the effective answers: the base full run plus the Q057 Codex-MCP correction. Failed/quota-exhausted rows will score zero against the 500-point benchmark denominator; completed rows will be scored against the benchmark’s gold answer and specific rubric, with the committed artifact containing scores and notes but not raw answer text.
````

### Response 5 (commentary)

- Timestamp: `2026-04-20T06:30:33.782Z`

````text
The first scoring batch completed and produced structured JSON scores. I’m running the remaining batches now; this is slow because each batch includes the gold answer, rubric, and compacted answers for five clients, but it avoids committing raw answer text.
````

### Response 6 (commentary)

- Timestamp: `2026-04-20T06:31:14.881Z`

````text
The scoring loop is still on batch 2. I’m letting it run rather than interrupting, because restarting would risk inconsistent scoring inputs.
````

### Response 7 (commentary)

- Timestamp: `2026-04-20T06:33:21.649Z`

````text
Batches 2 and 3 have completed cleanly. The remaining prompts are similar in size, so I expect this to continue steadily; I’ll check the parsed score coverage once all batches finish.
````

### Response 8 (commentary)

- Timestamp: `2026-04-20T06:35:29.415Z`

````text
Half the scoring batches have completed. I’m still keeping the output outside the repo until I can parse it, validate all 500 score rows, and strip the committed artifacts down to aggregate/per-question score data only.
````

### Response 9 (commentary)

- Timestamp: `2026-04-20T06:38:39.477Z`

````text
Batch 7 took longer but completed. I’m monitoring the last three; after that I’ll do coverage checks, regenerate the comparison report with a rubric leaderboard section, and update docs/tests.
````

### Response 10 (commentary)

- Timestamp: `2026-04-20T06:41:42.459Z`

````text
All scoring batches completed. I’m now parsing the batch outputs, checking for one score per effective client/question row, and looking for any anomalies before I write committed score artifacts.
````

### Response 11 (commentary)

- Timestamp: `2026-04-20T06:42:21.167Z`

````text
The parsed rubric scores cover all 500 effective rows. The result is not just a proxy metric: it materially changes the quality story, especially for Microsoft Copilot, which completed UI turns but often lacked enough source context to answer the actual question. I’m now adding report support for a committed score CSV and regenerating the comparison report from that score file.
````

### Response 12 (commentary)

- Timestamp: `2026-04-20T06:45:27.134Z`

````text
The documentation now reflects that the PR has a rubric-scored leaderboard, not just proxy metrics. I’m doing validation next: score CSV integrity, JSON validity, unit tests for the report generator, MCP wiki lint, docs lockstep, and whitespace checks.
````

### Response 13 (commentary)

- Timestamp: `2026-04-20T06:46:22.731Z`

````text
The report now treats rubric scores as the quality leaderboard and keeps proxy metrics as operational signals. I’m running the broader relevant test set now because `compare_wiki_eval.py` is shared by the MCP evaluation workflow.
````

### Response 14 (commentary)

- Timestamp: `2026-04-20T06:46:37.102Z`

````text
The broader unit test set passed. I’m doing final repo publication checks now: documentation lockstep, JSON validity, targeted no-raw-artifact scan, and whitespace.
````

### Response 15 (commentary)

- Timestamp: `2026-04-20T06:47:10.536Z`

````text
Validation is clean, and the only publication scan hit earlier was an absolute score path in the standalone leaderboard JSON; I rewrote that to a repo-relative path and reran the scan. I’m staging and committing the rubric-scoring update now.
````

### Response 16 (commentary)

- Timestamp: `2026-04-20T06:47:39.738Z`

````text
The rubric-scoring commit is made locally and the branch is one commit ahead. I’m pushing it to the PR branch now.
````

### Response 17 (final_answer)

- Timestamp: `2026-04-20T06:48:02.881Z`

````text
Done. I added rubric scoring to the current PR and pushed it to [PR #6](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/pull/6) at commit `41e72d8`.

The main updated artifacts are:

- [validated-full-20260419T2225Z-comparison.md]([LOCAL_REPO]/challenge-2/evaluation/reports/validated-full-20260419T2225Z-comparison.md)
- [validated-full-20260419T2225Z-rubric-leaderboard.md]([LOCAL_REPO]/challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-leaderboard.md)
- [validated-full-20260419T2225Z-rubric-scores.csv]([LOCAL_REPO]/challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-scores.csv)
- [validated-full-20260419T2225Z-rubric-leaderboard.json]([LOCAL_REPO]/challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-leaderboard.json)

The leaderboard now scores the effective full run against the benchmark’s human-written rubrics, using the Q057 Codex-MCP correction and the full 500-point denominator for every client:

| Rank | Client | Score |
| ---: | --- | ---: |
| 1 | Codex | `484/500` |
| 2 | Claude | `480/500` |
| 3 | Codex with MCP | `471/500` |
| 4 | Gemini | `171/500` |
| 5 | Microsoft Copilot | `58/500` |

The report now makes the distinction explicit: rubric scoring is the quality signal; completion, JSON parseability, citation overlap, timings, and MCP audit events remain operational/provenance signals. The committed score CSV contains only per-question scores, statuses, and short notes, not raw prompts or raw answer text.

I also updated [compare_wiki_eval.py]([LOCAL_REPO]/challenge-2/tools/compare_wiki_eval.py) so future reports can include a leaderboard with `--score-path`, and added regression coverage in [test_challenge2_compare_wiki_eval.py]([LOCAL_REPO]/tests/test_challenge2_compare_wiki_eval.py).

Validation passed:

- `python3 -m py_compile challenge-2/tools/compare_wiki_eval.py challenge-2/evaluation/scoring.py`
- `python3 -m unittest tests.test_challenge2_compare_wiki_eval`
- `python3 -m unittest tests.test_challenge2_eval_clients tests.test_challenge2_compare_wiki_eval tests.test_challenge2_wiki_mcp_server`
- `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report`
- `python3 tools/check_documentation_lockstep.py`
- `git diff --check`
- JSON validation for metrics, leaderboard, MCP lint, and MCP source register
- targeted scan found no local run paths, raw answer/gold-answer columns, UI session IDs, or Playwright profile metadata in the committed rubric artifacts

Working tree is clean and PR #6 is updated.

::git-stage{cwd="[LOCAL_REPO]"}
::git-commit{cwd="[LOCAL_REPO]"}
::git-push{cwd="[LOCAL_REPO]" branch="codex/wiki-mcp-research"}
````

## Contribution Reading

- User contribution: Asked Codex to inspect GitHub state and unblock the repository workflow.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.

Previous: [EX-0100](0100-20260418065216-should-we-do-both-of-these-within-the-current-pr-or-only-the-first-discuss.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0102](0102-20260418065216-so-is-this-thread-up-to-date-in-the-pr-should-we-wait-till-after-the-pr-is-reviewed-and-fu.md)
