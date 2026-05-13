---
exchange_id: "EX-0036"
title: "Build the harness that will allow us to push the questions into the various AIs with the instruc"
source_id: "CONV-003"
global_sequence: 36
session_sequence: 3
user_timestamp: "2026-04-16T11:49:26.469Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0036. Build the harness that will allow us to push the questions into the various AIs with the instruc

Previous: [EX-0035](0035-20260416112703-link-into-the-wiki-does-theed-a-path-change.md) | Conversation reader: [start-to-finish](../readers/conv-003-wiki-evaluation-harness-workbench-and-demo-route.md) | Next: [EX-0037](0037-20260416112703-do-a-pr-for-the-evaluation-work.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-003 (Wiki Evaluation Harness, Workbench, and Demo Route)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Build the harness that will allow us to push the questions into the various AIs with the instructions to use only the Wiki to answer all questions.

We have used a harness to check the MCP layer before in https://github.com/chris-page-gov/mcp-geo.git which is local at [LOCAL_PRIOR_WORK_REPO]

I also want to build an MCP layer so we can add full audit and FOI level recording using the dame format as we have done before - is that in the same repo or was it elsewhere?
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-16T11:49:34.732Z`

````text
I’ll inspect the existing `mcp-geo` repo for the prior harness and audit/FOI recording patterns, then mirror the relevant structure into this Challenge 2 repo with the benchmark questions as the input set.
````

### Response 2 (commentary)

- Timestamp: `2026-04-16T11:49:41.349Z`

````text
The prior MCP work is in `mcp-geo` itself: I found `tests/evaluation/harness.py`, `tests/evaluation/audit_logger.py`, `scripts/unattended_client_eval.py`, trace proxy scripts, and a `server/audit/` DSAP implementation. I’m reading those specific files now and will adapt the lightest useful pieces rather than pulling over the whole geospatial stack.
````

### Response 3 (commentary)

- Timestamp: `2026-04-16T11:49:54.450Z`

````text
The audit layer you remembered is in the same `mcp-geo` repo, under `server/audit/`, with docs in `docs/decision_support_audit_pack.md`. I’m checking this hackathon repo’s current structure and Python setup so the new harness fits locally instead of dragging in FastAPI dependencies unnecessarily.
````

### Response 4 (commentary)

- Timestamp: `2026-04-16T11:51:07.335Z`

````text
I’ll build this as a documentation-backed evaluation harness inside Challenge 2, and first I’m going to inspect the existing repo shape plus the prior `mcp-geo` runner details so the commands and audit format line up with what you already used.
````

### Response 5 (commentary)

- Timestamp: `2026-04-16T11:51:13.831Z`

````text
The prior work was in `[LOCAL_PRIOR_WORK_REPO]`: the reusable parts are the evaluation harness, stdio trace proxy strategy, and `server/audit` DSAP-style audit pack code. I’m going to mirror the shape here, but keep this repo’s implementation lightweight and stdlib-only unless the existing project already has a dependency stack for it.
````

### Response 6 (commentary)

- Timestamp: `2026-04-16T11:51:21.910Z`

````text
I’ve confirmed the prior FOI/audit layer is in `mcp-geo` itself, not a separate repo: `server/audit/` plus `docs/decision_support_audit_pack.md`, with client runner logic in `scripts/unattended_client_eval.py`. For this repo I’ll add a Challenge 2 harness, a small stdio MCP-compatible audit endpoint, tests, and the required documentation updates.
````

### Response 7 (commentary)

- Timestamp: `2026-04-16T11:52:19.159Z`

````text
I’m going to make the harness read the benchmark Markdown as the source of truth, then record every run as a DSAP-shaped package: event ledger, source register, visible transcript, audit card, integrity manifest, and per-answer audit log. The MCP layer will expose controlled wiki read/search plus answer-recording tools so a client can be audited without giving it the gold answers.
````

### Response 8 (commentary)

- Timestamp: `2026-04-16T11:55:30.059Z`

````text
The core files are in place. I’m adding narrow tests next: one for the Markdown parser, one for DSAP artifact creation, and one that speaks JSON-RPC to the stdio MCP layer so we catch protocol regressions without needing any external AI CLI installed.
````

### Response 9 (commentary)

- Timestamp: `2026-04-16T11:55:59.675Z`

````text
The first validation pass is clean: the new Python modules compile, the Challenge 2 wiki builder still compiles, and the focused unittest suite is passing. I’m going to exercise the actual harness in dry-run mode now so we verify the run directory and audit pack are produced without calling external AI tools.
````

### Response 10 (commentary)

- Timestamp: `2026-04-16T11:56:15.649Z`

````text
The harness smoke test produced a sealed audit pack, and the MCP smoke test listed tools, searched the wiki, and finalized its own pack. I’m adding one more piece now: a scoring-sheet and leaderboard summarizer so the captured answers can become a competitive comparison once scores are filled in.
````

### Response 11 (commentary)

- Timestamp: `2026-04-16T11:56:59.786Z`

````text
I’m updating the user-facing docs now: the Challenge 2 brief, the wiki benchmark note, the repo README, and the tracking files. I’ll keep the prior lockstep/check-work entries intact and add only the new harness/audit details.
````

### Response 12 (commentary)

- Timestamp: `2026-04-16T11:57:52.734Z`

````text
Docs are now in lockstep with the new workflow, including a dedicated `challenge-2/evaluation/README.md`. I’m running the final validation set: compile, unit tests, harness smoke, MCP smoke, documentation lockstep, and whitespace checks.
````

### Response 13 (commentary)

- Timestamp: `2026-04-16T11:58:01.559Z`

````text
Validation passed, but Python compilation left a `__pycache__` under `challenge-2/tools/`. I’m removing that generated cache so the worktree only contains source and documentation changes.
````

### Response 14 (commentary)

- Timestamp: `2026-04-16T11:58:24.975Z`

````text
One important fairness issue surfaced in review: because the benchmark note now lives in the wiki, an evaluated model must not be allowed to read `evaluation-benchmark.md` while answering, since it contains the gold answers. I’m tightening the prompt and MCP allow-list so benchmark metadata remains available to the harness, not to the evaluated client’s wiki access path.
````

### Response 15 (final_answer)

- Timestamp: `2026-04-16T12:00:27.710Z`

````text
Implemented the Challenge 2 wiki evaluation harness and audit layer.

The prior FOI/audit work is in the same local repo you pointed to: `[LOCAL_PRIOR_WORK_REPO]`, mainly under `[LOCAL_PRIOR_WORK_REPO]/server/audit/`, with related harness/trace code in `[LOCAL_PRIOR_WORK_REPO]/tests/evaluation/` and `[LOCAL_PRIOR_WORK_REPO]/scripts/unattended_client_eval.py`.

What I added here:

- [challenge-2/wiki/evaluation-benchmark.md]([LOCAL_REPO]/challenge-2/wiki/evaluation-benchmark.md): 100-question benchmark linked from the wiki index.
- [challenge-2/evaluation/questions.py]([LOCAL_REPO]/challenge-2/evaluation/questions.py): parser for the benchmark Markdown.
- [challenge-2/tools/run_wiki_eval.py]([LOCAL_REPO]/challenge-2/tools/run_wiki_eval.py): CLI harness for Codex, Gemini CLI, and Claude Code.
- [challenge-2/tools/wiki_eval_mcp.py]([LOCAL_REPO]/challenge-2/tools/wiki_eval_mcp.py): stdio MCP-compatible layer for audited wiki search/read, public question retrieval, answer recording, and DSAP pack finalisation.
- [challenge-2/evaluation/audit.py]([LOCAL_REPO]/challenge-2/evaluation/audit.py): DSAP-shaped run recording: event ledger, source register, evidence register, audit card, integrity manifest, visible transcript, redaction manifest, and zip bundle.
- [challenge-2/evaluation/scoring.py]([LOCAL_REPO]/challenge-2/evaluation/scoring.py) and [challenge-2/tools/summarise_wiki_eval.py]([LOCAL_REPO]/challenge-2/tools/summarise_wiki_eval.py): scoring sheet and leaderboard generation.
- [challenge-2/evaluation/README.md]([LOCAL_REPO]/challenge-2/evaluation/README.md): runbook and output inventory.
- Tests under [tests]([LOCAL_REPO]/tests).

Important fairness guard: because the benchmark note lives inside the wiki and contains gold answers, the harness prompt explicitly excludes `challenge-2/wiki/evaluation-benchmark.md` and `challenge-2/evaluation/` during answer generation. The MCP wiki read/search tools also block `evaluation-benchmark.md`, so evaluated clients cannot retrieve the gold answers through that layer.

Typical dry run:

```bash
python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients codex --questions Q001 --run-id smoke
```

Typical multi-client run:

```bash
python3 challenge-2/tools/run_wiki_eval.py --clients codex,gemini,claude
```

After filling scores in `generated/scoring-sheet.csv`:

```bash
python3 challenge-2/tools/summarise_wiki_eval.py challenge-2/evaluation/runs/<run-id>
```

Validation passed:

- `python3 -m py_compile ...` for the new evaluation modules and tools
- `python3 -m unittest discover -s tests -p 'test_challenge2_eval*.py'`
- `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
- harness dry-run smoke test
- MCP stdio JSON-RPC smoke test
- `python3 tools/check_documentation_lockstep.py`
- `git diff --check`

Note: `challenge-2/.obsidian/workspace.json` is still dirty local Obsidian workspace state. I left it alone rather than treating it as part of the implementation.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.

Previous: [EX-0035](0035-20260416112703-link-into-the-wiki-does-theed-a-path-change.md) | Conversation reader: [start-to-finish](../readers/conv-003-wiki-evaluation-harness-workbench-and-demo-route.md) | Next: [EX-0037](0037-20260416112703-do-a-pr-for-the-evaluation-work.md)
