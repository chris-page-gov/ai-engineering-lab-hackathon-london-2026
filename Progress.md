# Progress

## Current Status

The Challenge 2 Obsidian knowledge-base prototype is implemented and merged into the fork's `main` branch via fork-local PR #1.

The current local working branch also contains the Challenge 2 wiki evaluation benchmark, CLI harness, MCP-compatible audit layer, and scoring-sheet/leaderboard tooling for comparing Codex, Gemini CLI, and Claude Code against the generated wiki.

## Completed

- Built a repeatable Challenge 2 wiki generator.
- Generated source notes for all 43 Challenge 2 documents.
- Generated topic pages, entity pages, maps of content, architecture notes, source-register JSON, workbook exports, and lint reports.
- Preserved raw Challenge 2 sources as immutable source material.
- Added synthetic fixture metadata for staff-directory content without redacting the synthetic data.
- Fixed generated link integrity issues and removed local filesystem path leakage from generated metadata.
- Merged the fork-local Challenge 2 PR into the fork's `main` branch.
- Resolved all fork-local PR review threads.
- Fixed the architecture Mermaid diagram labels that Obsidian rendered as unsupported Markdown lists.
- Added repo-wide tracking files and a documentation lockstep check for local and pull-request validation.
- Fixed review feedback on the documentation lockstep check so deleted tracking files cannot pass as updated files.
- Added the 100-question Challenge 2 wiki evaluation benchmark and linked it from the wiki index.
- Added a CLI evaluation harness that builds wiki-only prompts, captures client outputs, and emits DSAP-shaped audit packs.
- Added a stdio MCP-compatible layer for audited Challenge 2 wiki search/read, public question retrieval, answer recording, and run finalisation.
- Added scoring-sheet and leaderboard tooling for competitive evaluation once per-answer scores are entered.
- Added Dark Data Workbench under `challenge-2/workbench/` with source filtering, context-set building, source reader, graph/table/check views, browser-AI context export, and MCP setup guidance.
- Added `challenge-2/tools/workbench_mcp.py` for local MCP source search/read/context export.
- Added Dark Data Workbench unit, component, Playwright, MCP, and optional coverage test paths.
- Hardened Dark Data Workbench Playwright control interactions after the PR check exposed CI-only click/state flakiness.
- Removed Obsidian workspace session state from Git tracking while preserving useful vault configuration files.

## Validation

- Challenge 2 strict build previously passed with `43 sources, 81 notes, 0 lint issues`.
- Current lightweight validation for the Mermaid fix passed:
  - `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
  - Checked that the architecture Mermaid labels no longer start with ordered-list syntax.
- Documentation lockstep validation passed locally:
  - `python3 tools/check_documentation_lockstep.py`
  - `python3 -m py_compile tools/check_documentation_lockstep.py`
  - `git diff --check`
  - temporary missing-file check confirmed the script fails when `Changelog.md` is absent.
- Current lightweight validation for the Challenge 2 evaluation harness passed:
  - `python3 -m py_compile challenge-2/evaluation/__init__.py challenge-2/evaluation/questions.py challenge-2/evaluation/audit.py challenge-2/evaluation/clients.py challenge-2/evaluation/scoring.py challenge-2/tools/run_wiki_eval.py challenge-2/tools/wiki_eval_mcp.py challenge-2/tools/summarise_wiki_eval.py`
  - `python3 -m unittest discover -s tests -p 'test_challenge2_eval*.py'`
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients codex --questions Q001 --output-root /tmp/challenge2-wiki-eval-test --run-id smoke`
  - `python3 challenge-2/tools/summarise_wiki_eval.py /tmp/challenge2-wiki-eval-test/smoke`
  - stdio JSON-RPC smoke test for `challenge-2/tools/wiki_eval_mcp.py`
- Current Dark Data Workbench validation passed locally:
  - `cd challenge-2/workbench && pnpm check`
  - `cd challenge-2/workbench && pnpm test`
  - `cd challenge-2/workbench && pnpm build`
  - `cd challenge-2/workbench && pnpm test:ui`
  - `python3 -m unittest tests/test_challenge2_workbench_mcp.py`

## Open Items

- Add `challenge-2/wiki/demo-answers.md` with source-backed answers to the official demo questions.
- Add a concise judging evidence page covering user need, prototype scope, AI-tool usage, validation, limitations, and next steps.
- Run the full 100-question benchmark through the available Codex, Gemini CLI, and Claude Code installations, then fill the scoring sheet and publish the generated leaderboard.

## Next Recommended Steps

1. Run the full benchmark against Codex, Gemini CLI, and Claude Code using `challenge-2/tools/run_wiki_eval.py`.
2. Score `generated/scoring-sheet.csv` and generate `generated/leaderboard.md`.
3. Add source-backed demo answers for the five Challenge 2 demo questions.
4. Use Dark Data Workbench during the demo to show search, context export, and source-backed checks over the generated knowledge base.
