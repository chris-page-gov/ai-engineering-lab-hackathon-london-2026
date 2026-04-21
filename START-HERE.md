# Start Here

This guide is for people arriving from LinkedIn, event write-ups, or shared links who want to know which part of the repository to read first.

Use the repository root as the canonical public link. GitHub renders the README there, and this guide gives shorter routes for different readers.

## Fast Routes

| Time available | Read this | Why |
| --- | --- | --- |
| 2 minutes | [README](README.md) | Understand what Team DSIT A built and why the fork exists. |
| 10 minutes | [Demonstration guide](challenge-2/wiki/demonstration-guide.md) | Follow the end-to-end dark-data prototype route. |
| 30 minutes | [Challenge 2 wiki index](challenge-2/wiki/index.md), [Workbench guide](challenge-2/wiki/workbench.md), and [evaluation leaderboard](challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-leaderboard.md) | See the knowledge base, browser UI, and benchmark result together. |
| Deep dive | [Realtime delivery report](output/doc/challenge-2-realtime-delivery-report.md), [public postmortem](postmortem-public/wiki/index.md), and [MCP research wiki](challenge-2/MCP-Wiki/index.md) | Inspect the implementation story, collaboration evidence, and follow-on MCP work. |

## Routes By Reader

| Reader | Start with | Then read |
| --- | --- | --- |
| Event attendee or organiser | [README](README.md) | [Original event material](README.md#original-hackathon-context), [setup guide](SETUP-GUIDE.md), [open brief](open-brief.md) |
| Public-sector digital or service leader | [Challenge 2 brief](challenge-02-unlocking-the-dark-data.md) | [Demonstration guide](challenge-2/wiki/demonstration-guide.md), [realtime delivery report](output/doc/challenge-2-realtime-delivery-report.md) |
| Engineer | [Dark Data Workbench guide](challenge-2/wiki/workbench.md) | [Workbench README](challenge-2/workbench/README.md), [wiki builder](challenge-2/tools/build_wiki.py), [evaluation harness](challenge-2/evaluation/README.md) |
| Data or knowledge management reader | [Challenge 2 wiki index](challenge-2/wiki/index.md) | [Architecture overview](challenge-2/wiki/architecture.md), [maps of content](challenge-2/wiki/index.md#maps-of-content), [source register](challenge-2/wiki/data/source-register.json) |
| AI evaluation or benchmarking reader | [Evaluation benchmark](challenge-2/wiki/evaluation-benchmark.md) | [Evaluation README](challenge-2/evaluation/README.md), [comparison report](challenge-2/evaluation/reports/validated-full-20260419T2225Z-comparison.md), [rubric leaderboard](challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-leaderboard.md) |
| Security or assurance reader | [Contribution modes and security assessment](output/doc/codex-contribution-modes-security-assessment.md) | [Context](Context.md), [public postmortem decisions](postmortem-public/wiki/decisions.md), [repository evidence](postmortem-public/wiki/repository-evidence.md) |
| MCP or agent-tooling reader | [MCP research wiki](challenge-2/MCP-Wiki/index.md) | [MCP architecture](challenge-2/MCP-Wiki/architecture.md), [implementation workspace](challenge-2/MCP-Wiki/implementation/README.md), [semantic retrieval options](challenge-2/MCP-Wiki/semantic-retrieval-options.md) |
| AI-assisted delivery or collaboration reader | [Public Codex postmortem](postmortem-public/wiki/index.md) | [Contribution modes proposal](output/doc/contribution-modes-proposal.md), [realtime delivery report](output/doc/challenge-2-realtime-delivery-report.md) |

## Suggested Public Link

For LinkedIn and other event posts, link to:

```text
https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026
```

That keeps one stable entry point while letting readers choose a route once they arrive.

## What This Repository Is

This is a synthetic Challenge 2 implementation and evidence pack from the AI Engineering Lab Hackathon London 2026. It shows how government-style documents can be converted into a source-backed knowledge base, inspected through a browser workbench, exported to AI tools with evidence, evaluated through a benchmark, and reviewed through public postmortem material.

## What This Repository Is Not

This is not a production government service, a live data system, or a recommendation to use real personal or sensitive data in a hackathon prototype. The security and contribution-mode material is included so limitations and production gaps are visible alongside the implementation.

---

Version: 1.0
Last updated: April 2026
