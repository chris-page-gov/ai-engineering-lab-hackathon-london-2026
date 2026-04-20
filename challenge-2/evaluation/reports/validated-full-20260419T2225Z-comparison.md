# Challenge 2 Wiki Evaluation: MCP Comparison

## Scope

- Run ID: `validated-full-20260419T2225Z`
- Raw artifact location: external run directory `validated-full-20260419T2225Z`; raw prompts and answers are not committed to Git.
- Questions: `100`
- Clients: `claude, codex, codex-mcp, gemini, microsoft-copilot`
- Repository state: `codex/wiki-mcp-research` at `f775aec3d689`, dirty=`True`
- Scoring posture: rubric-scored quality leaderboard added from the benchmark's human-written rubrics; automated proxy metrics are retained as secondary operational signals.
- Source policy: Challenge 2 wiki, `wiki/data`, and `challenge-2/AGENTS.md`; benchmark and gold-answer artifacts remain excluded from prompts and MCP tools.

## Model And Version Provenance

| Client | Selected model | Selection source | Reasoning | Primary version check |
| --- | --- | --- | --- | --- |
| claude | `local-settings-managed` | dsit_managed_local_settings | not recorded | `2.1.114 (Claude Code)` |
| codex | `gpt-5.4` | explicit_latest_openai_docs | xhigh | `codex-cli 0.121.0` |
| codex-mcp | `gpt-5.4` | explicit_latest_openai_docs_with_challenge2_wiki_mcp | xhigh | `codex-cli 0.121.0` |
| gemini | `gemini-3.1-pro-preview` | explicit_gemini_cli_docs | not recorded | `0.38.2` |
| microsoft-copilot | `gpt-5-thinking-ui-selected` | microsoft_365_copilot_ui_preferred_mode | not recorded | `v25.9.0` |

## Client Summary

| Client | Answers | Completed | JSON % | Avg completed seconds | Gold-ref recall proxy | MCP audited questions | Statuses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| claude | 100 | 100 | 100.0 | 21.667 | 89.5 | 0 | completed:100 |
| codex | 100 | 100 | 100.0 | 45.213 | 92.5 | 0 | completed:100 |
| codex-mcp | 100 | 100 | 100.0 | 33.748 | 94.0 | 100 | completed:100 |
| gemini | 100 | 36 | 36.0 | 24.693 | 32.3 | 0 | completed:36, quota_exhausted:64 |
| microsoft-copilot | 100 | 100 | 100.0 | 57.078 | 69.9 | 0 | completed:100 |

## Rubric-Scored Quality Leaderboard

| Rank | Client | Scored answers | Raw points | Final % | Scored subset % | Hallucinations | Missed source risks |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | codex | 100 | 484.0/500 | 96.8 | 96.8 | 2 | 2 |
| 2 | claude | 100 | 480.0/500 | 96.0 | 96.0 | 9 | 7 |
| 3 | codex-mcp | 100 | 471.0/500 | 94.2 | 94.2 | 5 | 6 |
| 4 | gemini | 100 | 171.0/500 | 34.2 | 34.2 | 1 | 59 |
| 5 | microsoft-copilot | 100 | 58.0/500 | 11.6 | 11.6 | 19 | 92 |

### Rubric Scoring Method

- Scores use the benchmark's human-written `specific_rubric` and gold answer for each question.
- The effective answer set applies the explicit Q057 Codex-with-MCP correction before scoring.
- Each client is scored against the full 500-point benchmark denominator; non-completed, failed, and quota-exhausted rows receive `0`.
- The committed score CSV records per-question scores and notes without committing raw prompts or answer text.

## Partial Or Blocked Clients

- `gemini` became quota-limited during the run (`quota_exhausted`=64); completed rows before quota remain retained as evidence, but the client needs a rerun after quota reset for full coverage.

## Correction Evidence

| Client | Question | Base status | Correction status | Correction run |
| --- | --- | --- | --- | --- |
| codex-mcp | Q057 | timeout | completed | `codex-mcp-q057-correction-20260420T0320Z` |

## Codex Versus Codex With MCP

- `codex` completed `100` answers; `codex-mcp` completed `100`.
- `codex` average elapsed time was `45.213` seconds; `codex-mcp` average elapsed time was `33.748` seconds.
- `codex` JSON parseability was `100.0`%; `codex-mcp` JSON parseability was `100.0`%.
- `codex` gold-reference recall proxy was `92.5`%; `codex-mcp` was `94.0`%.
- `codex-mcp` recorded MCP audit events for `100` questions, with events `{'wiki.build_context_pack': 56, 'wiki.explain_provenance': 1, 'wiki.list_sources': 3, 'wiki.read': 89, 'wiki.read_source': 9, 'wiki.search': 134}`.
- Rubric score: `codex` scored `484.0/500` (`96.8`%); `codex-mcp` scored `471.0/500` (`94.2`%).
- Rubric risks: `codex` recorded `2` missed-source risks and `2` hallucination flags; `codex-mcp` recorded `6` missed-source risks and `5` hallucination flags.

### Per-Question Difference Flags

| Question | Baseline status | MCP status | Baseline gold refs | MCP gold refs | MCP tool events |
| --- | --- | --- | ---: | ---: | ---: |
| Q001 | completed | completed | 2/2 | 2/2 | 3 |
| Q002 | completed | completed | 1/1 | 1/1 | 2 |
| Q003 | completed | completed | 1/2 | 1/2 | 2 |
| Q004 | completed | completed | 1/1 | 1/1 | 2 |
| Q005 | completed | completed | 8/8 | 8/8 | 2 |
| Q006 | completed | completed | 0/2 | 1/2 | 9 |
| Q007 | completed | completed | 1/1 | 1/1 | 3 |
| Q008 | completed | completed | 2/2 | 2/2 | 8 |
| Q009 | completed | completed | 1/1 | 1/1 | 2 |
| Q010 | completed | completed | 1/1 | 1/1 | 2 |
| Q011 | completed | completed | 1/1 | 1/1 | 3 |
| Q012 | completed | completed | 1/1 | 1/1 | 2 |
| Q013 | completed | completed | 1/2 | 2/2 | 5 |
| Q014 | completed | completed | 1/1 | 1/1 | 2 |
| Q015 | completed | completed | 1/1 | 1/1 | 2 |
| Q016 | completed | completed | 1/1 | 1/1 | 2 |
| Q017 | completed | completed | 1/1 | 1/1 | 2 |
| Q018 | completed | completed | 1/1 | 1/1 | 2 |
| Q019 | completed | completed | 1/1 | 1/1 | 2 |
| Q020 | completed | completed | 1/1 | 1/1 | 2 |
| Q021 | completed | completed | 1/1 | 1/1 | 4 |
| Q022 | completed | completed | 1/1 | 1/1 | 2 |
| Q023 | completed | completed | 1/1 | 1/1 | 2 |
| Q024 | completed | completed | 1/1 | 1/1 | 2 |
| Q025 | completed | completed | 1/1 | 1/1 | 2 |
| ... | First 25 of 100 questions shown |  |  |  |  |

## Smoke-Test Evidence

| Client | Run directory | Statuses |
| --- | --- | --- |
| github-copilot | `github-copilot-q001-smoke` | policy_blocked:1 |

## Caveats

- The citation metric remains a recall proxy over source IDs and wiki paths; the rubric-scored leaderboard is the quality signal for answer correctness.
- Microsoft Copilot uses browser UI automation and may include UI chrome or previous chat text in raw captured output; parsed JSON is extracted from visible text where possible.
- GitHub Copilot CLI was excluded from the full validated run if the smoke run remained `policy_blocked`.
- Codex with MCP uses noninteractive approval bypass for the Codex process so MCP tool calls are not cancelled; the MCP server itself is read-only, allowlisted, and benchmark-safe.
- Semantic retrieval is implemented with deterministic exact-cosine local hashing in this run. The production embedding model remains to be locked after a dedicated retrieval benchmark over the shortlisted permissive local models.

## Next Steps

- Use independent moderation if this rubric-scored leaderboard is promoted from project evidence to an official comparative claim.
- Run the embedding shortlist benchmark and lock the v1 model only after comparing retrieval quality, disk impact, license posture, and reproducibility.
- Validate the same MCP server through Copilot Studio direct MCP connection; move to Agents Toolkit packaging only if direct connection cannot expose the required tools, resources, or governance controls.
- Improve the Microsoft Copilot adapter by starting a fresh conversation per question and extracting only the final assistant JSON block.
