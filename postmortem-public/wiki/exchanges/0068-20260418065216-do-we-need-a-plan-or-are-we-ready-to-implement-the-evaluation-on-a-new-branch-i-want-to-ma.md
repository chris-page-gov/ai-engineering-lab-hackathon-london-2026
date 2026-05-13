---
exchange_id: "EX-0068"
title: "Do we need a plan or are we ready to implement the evaluation on a new branch? I want to make su"
source_id: "CONV-005"
global_sequence: 68
session_sequence: 16
user_timestamp: "2026-04-18T12:43:33.825Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0068. Do we need a plan or are we ready to implement the evaluation on a new branch? I want to make su

Previous: [EX-0067](0067-20260418065216-merge.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0069](0069-20260418065216-i-want-full-coverage-with-the-best-models-selected-in-each-client-so-that-includes-github.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Do we need a plan or are we ready to implement the evaluation on a new branch? I want to make sure we are using the very latest models and that all versioning information is recoded agains each client
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-18T12:43:49.300Z`

````text
We are ready to implement this on a new branch. I’ll branch from the merged `main`, then tighten the evaluation harness so each run records the exact client binary, command path, model setting, and source of model selection; I’ll also verify current/latest model choices from official sources where the CLI itself does not expose them.
````

### Response 2 (commentary)

- Timestamp: `2026-04-18T12:44:08.730Z`

````text
The installed CLIs are: Codex CLI `0.121.0`, Gemini CLI `0.38.0`, Claude Code `2.1.109`; Copilot CLI is not installed yet. I’m checking official model/version docs now, and then I’ll create the branch and make the harness record both the chosen model and the installed client/version facts per answer and per run.
````

### Response 3 (commentary)

- Timestamp: `2026-04-18T12:45:40.441Z`

````text
We’re already on a new branch from `v1.1`, so I’ll implement the harness changes now. I’m going to first finish the source checks for current model/version guidance, then make the repo changes so each evaluation run records the exact client, binary, CLI version, command, model setting, and source of that model choice.
````

### Response 4 (commentary)

- Timestamp: `2026-04-18T12:46:06.664Z`

````text
I’ve confirmed the current guidance from the vendor docs: OpenAI points at `gpt-5.4` for complex coding, Gemini CLI now defaults through Auto routing with Gemini 3 options available, Claude Code aliases/defaults have moved past the older Sonnet 4 references, and Copilot CLI exposes model selection but the installed `gh` wrapper does not prove the standalone agent is present. I’m checking the existing evaluator shape now so the change lands in the right layer.
````

### Response 5 (commentary)

- Timestamp: `2026-04-18T12:46:56.794Z`

````text
The installed command-line state is clear: Codex, Gemini CLI, Claude Code, and `gh` are present; the standalone `copilot` binary is not on `PATH`, but `gh copilot` can download/run it. I’ll add Copilot CLI as an optional client with wrapper metadata, while keeping the default batch to the three installed headless clients.
````

### Response 6 (commentary)

- Timestamp: `2026-04-18T12:47:54.223Z`

````text
I’m going to make the model choice explicit where “latest” is a stable documented selector, and record floating defaults where the client owns routing. That gives us reproducibility of the run inputs without pretending that aliases such as Gemini `auto`, Claude `opus`, or Copilot’s default are immutable model snapshots.
````

### Response 7 (commentary)

- Timestamp: `2026-04-18T12:49:56.294Z`

````text
The core harness code is now collecting client manifests and repo state at run start. I’m updating the runbook and tracking docs next so a reviewer can see exactly why each default model selector was chosen and where the current vendor guidance was checked.
````

### Response 8 (commentary)

- Timestamp: `2026-04-18T12:51:07.888Z`

````text
The first code pass is in place: the evaluator now resolves model selectors separately from command building, writes the resolved model into each answer, and records a manifest for each client at run start. I’ve added a focused regression test for the new default selectors and dry-run metadata.
````

### Response 9 (commentary)

- Timestamp: `2026-04-18T12:51:14.418Z`

````text
Validation is passing for the new client metadata tests and the Challenge 2 wiki builder compile check. I’m running the dry-run smoke now and inspecting its `run.json`, because that is the artifact we’ll rely on before the full 100-question evaluation.
````

### Response 10 (commentary)

- Timestamp: `2026-04-18T12:51:43.831Z`

````text
Both dry-runs produced the expected manifests. The default smoke captures Codex `0.121.0` with `gpt-5.4`, Gemini `0.38.0` with `auto`, Claude Code `2.1.109` with `opus`, plus the installed Microsoft Copilot desktop app versions; the optional Copilot CLI smoke correctly records that standalone `copilot` is missing while `gh 2.90.0` has the preview wrapper.
````

### Response 11 (commentary)

- Timestamp: `2026-04-18T12:52:41.900Z`

````text
The implementation is coherent and validation has passed, so I’m going to commit this branch as the evaluation-versioning baseline. That gives us a clean point to review before any full benchmark run consumes model quota.
````

### Response 12 (final_answer)

- Timestamp: `2026-04-18T12:53:17.340Z`

````text
Implemented on `codex/evaluation-versioning` and committed as `2b3b9c5 Add evaluation client version manifests`. The working tree is clean.

What changed:
- Added per-client manifests in `run.json`: selected model, model source, reference URL/date, executable path, CLI version output, command template source, repo state, benchmark SHA-256, and relevant model env vars.
- Updated defaults for the run:
  - Codex: `gpt-5.4`
  - Gemini CLI: `auto` routing, with no `--model` passed by default
  - Claude Code: `opus` latest alias
  - GitHub Copilot CLI: optional `github-copilot` client, not in the default batch
- Captures installed Microsoft Copilot desktop app versions as environment evidence, but does not treat them as headless harness clients.
- Updated docs and tracking files, including [challenge-2/evaluation/README.md]([LOCAL_REPO]/challenge-2/evaluation/README.md), [Context.md]([LOCAL_REPO]/Context.md), [Progress.md]([LOCAL_REPO]/Progress.md), and [Changelog.md]([LOCAL_REPO]/Changelog.md).

Current detected local client state from the dry-run smoke:
- Codex CLI: `0.121.0`, model `gpt-5.4`
- Gemini CLI: `0.38.0`, model selector `auto`
- Claude Code: `2.1.109`, model alias `opus`
- GitHub Copilot CLI: standalone `copilot` not on `PATH`; `gh 2.90.0` has the preview `gh copilot` wrapper
- Desktop apps: Copilot `25.6.440416001`, Microsoft 365 Copilot `1.2604`

Validation passed:
- `python3 -m unittest discover -s tests -p 'test_challenge2_eval*.py'`
- `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
- `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients codex,gemini,claude --questions Q001 ...`
- `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients github-copilot --questions Q001 ...`
- `python3 tools/check_documentation_lockstep.py`
- `git diff --check`

I checked the current vendor guidance while choosing the selectors: [OpenAI models](https://developers.openai.com/api/docs/models), [Gemini CLI model routing](https://geminicli.com/docs/cli/model-routing/), [Claude Code model config](https://code.claude.com/docs/en/model-config), and [GitHub Copilot CLI model usage](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli).

I did not run the full 100-question benchmark. The next clean step is to review/merge this harness branch first, then run the full evaluation from `main` so the results are anchored to a published baseline.

::git-create-branch{cwd="[LOCAL_REPO]" branch="codex/evaluation-versioning"}
::git-stage{cwd="[LOCAL_REPO]"}
::git-commit{cwd="[LOCAL_REPO]"}
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0067](0067-20260418065216-merge.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0069](0069-20260418065216-i-want-full-coverage-with-the-best-models-selected-in-each-client-so-that-includes-github.md)
