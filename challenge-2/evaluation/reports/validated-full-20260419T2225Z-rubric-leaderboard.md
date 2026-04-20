# Challenge 2 Wiki Evaluation Rubric Leaderboard

This leaderboard scores the effective `validated-full-20260419T2225Z` answer set against the benchmark human-written rubrics. It uses the base full run plus the explicit Codex-MCP Q057 correction run. Raw prompts and answer text remain outside Git; the committed score CSV contains only per-question scores, status, and short scoring notes.

Scores use the full 500-point benchmark denominator for every client. Non-completed, failed, and quota-exhausted rows receive zero.

## Leaderboard

| Rank | Client | Scored answers | Raw points | Final % | Hallucinations | Missed source risks |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | codex | 100 | 484.0/500 | 96.8 | 2 | 2 |
| 2 | claude | 100 | 480.0/500 | 96.0 | 9 | 7 |
| 3 | codex-mcp | 100 | 471.0/500 | 94.2 | 5 | 6 |
| 4 | gemini | 100 | 171.0/500 | 34.2 | 1 | 59 |
| 5 | microsoft-copilot | 100 | 58.0/500 | 11.6 | 19 | 92 |

## Related

- [Comparison report](validated-full-20260419T2225Z-comparison.md)
- [Per-question rubric scores](validated-full-20260419T2225Z-rubric-scores.csv)
- [Machine-readable metrics](validated-full-20260419T2225Z-metrics.json)

