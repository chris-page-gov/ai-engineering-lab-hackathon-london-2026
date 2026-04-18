# Challenge 2 Wiki Evaluation Harness

This folder contains the local harness for comparing how AI coding agents answer the Challenge 2 wiki benchmark.

The benchmark source of truth is `challenge-2/wiki/evaluation-benchmark.md`. The harness parses that Markdown file, sends selected questions to CLI clients, captures visible answers, and writes a DSAP-shaped audit pack for FOI, internal audit, and later scoring.

## Run A Dry-Run Smoke Test

```bash
python3 challenge-2/tools/run_wiki_eval.py \
  --dry-run \
  --clients codex \
  --questions Q001 \
  --run-id smoke
```

Dry-run mode writes prompts and audit artifacts without invoking external AI CLIs.

## Run Clients

```bash
python3 challenge-2/tools/run_wiki_eval.py \
  --clients codex,gemini,claude \
  --questions Q001,Q002,Q003
```

By default, each prompt instructs the client to use only:

- `challenge-2/wiki/`
- `challenge-2/wiki/data/`
- `challenge-2/AGENTS.md`

The prompt also explicitly excludes `challenge-2/wiki/evaluation-benchmark.md` and `challenge-2/evaluation/` from answer-time evidence because those files contain benchmark and scoring material.

Use `--client-config challenge-2/evaluation/client-config.example.json` as a starting point if local CLI arguments need to be adjusted for installed versions of Codex, Gemini CLI, Claude Code, or the optional GitHub Copilot CLI client.

## Model And Version Capture

Each run now writes a client manifest into `run.json` under `metadata.client_manifests`. The manifest records:

- selected model or alias;
- source of the model choice, such as `--model`, client config, environment variable, or harness default;
- whether the model selector is passed as a command argument or left to the client default;
- model-reference URL and the date checked;
- executable path and version-command output;
- selected command template source; and
- relevant model environment variables without API keys.

The default batch remains `codex,gemini,claude`. Current model policy, checked on 2026-04-18:

| Client | Harness default | Why |
| --- | --- | --- |
| Codex | `gpt-5.4` | OpenAI model documentation recommends `gpt-5.4` for complex reasoning and coding. |
| Gemini CLI | `auto` | Gemini CLI documentation says the default model is Auto routing; the built-in command deliberately omits `--model` so the installed CLI owns routing to the latest available Gemini models. |
| Claude Code | `opus` | Claude Code documents `opus` as a floating alias for the most capable Opus model available to the account. |
| GitHub Copilot CLI | `copilot-cli-default` | Optional client. GitHub documents the default as Claude Sonnet 4.5 and reserves the right to change it; pin with `--model github-copilot=<model>` only after confirming the installed Copilot CLI model list. |

The runner also records Git commit, branch, tags-at-HEAD, dirty status, benchmark SHA-256, and detected macOS Copilot desktop app versions. Desktop Copilot apps are captured as environment evidence only; they are not headless clients for the current harness.

For an auditable smoke test of version capture:

```bash
python3 challenge-2/tools/run_wiki_eval.py \
  --dry-run \
  --clients codex,gemini,claude \
  --questions Q001 \
  --run-id versioning-smoke
```

Inspect `challenge-2/evaluation/runs/versioning-smoke/run.json` before running the full 100-question benchmark.

## Outputs

Each run is written under `challenge-2/evaluation/runs/<run-id>/`. Generated runs are ignored by git.

Key outputs:

- `run.json`: run metadata, selected clients, repo state, benchmark hash, desktop AI app evidence, and per-client model/version manifests.
- `questions.jsonl`: parsed benchmark questions, including gold answers for scoring.
- `answers.jsonl`: captured client answers with gold answers and rubrics for downstream scoring.
- `prompts/<client>/<question>.txt`: exact prompt sent to each client.
- `raw/<client>/`: captured stdout, stderr, and assistant-response files.
- `audit/<client>-<question>.txt`: LLM-readable per-answer audit log.
- `event-ledger.jsonl`: append-only audit event ledger.
- `source-register.json`: observed wiki/source access records.
- `audit-card.json` and `audit-card.md`: DSAP front sheet.
- `decision-record.json`, `conversation-record.json`, `evidence-register.json`, `redaction-manifest.json`, and `integrity-manifest.json`: DSAP-style audit records.
- `generated/scoring-sheet.csv`: scoring worksheet with blank score columns.
- `bundle/DSAP-<run-id>.zip`: sealed audit bundle plus SHA-256 sidecar.

## Score And Rank

Fill `score_0_to_5`, `scorer_notes`, `hallucination_count`, and `missed_source_risk` in `generated/scoring-sheet.csv`, then run:

```bash
python3 challenge-2/tools/summarise_wiki_eval.py challenge-2/evaluation/runs/<run-id>
```

The summariser writes:

- `generated/leaderboard.json`
- `generated/leaderboard.md`

The final percentage uses the benchmark regime in `challenge-2/wiki/evaluation-benchmark.md`: 100 questions, 5 points each, 500 points total.

## MCP Audit Layer

`challenge-2/tools/wiki_eval_mcp.py` is a small stdio MCP-compatible layer for audited wiki access and answer recording. It exposes tools to list questions, get the public prompt, search/read allowed wiki files, record answers, and finalize the DSAP pack. Its wiki read/search tools deliberately exclude `challenge-2/wiki/evaluation-benchmark.md`.

Smoke test:

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | python3 challenge-2/tools/wiki_eval_mcp.py --run-id smoke-mcp
```

The MCP layer deliberately does not expose gold answers through question-listing, question-reading, or wiki-file tools. Gold answers remain in harness artifacts for scoring.
