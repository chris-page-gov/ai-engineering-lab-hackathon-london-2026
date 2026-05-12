# Timeline: AI software engineering from assistants to agents

This timeline covers the movement from code completion towards agentic software-engineering systems from 2021 to May 2026. Dates are taken from verified sources in [01_source_register.csv](01_source_register.csv). Vendor sources are used for release dates and documented capabilities, not independent proof of productivity or safety.

## HMRC Talk Navigation

This file is supporting evidence for the HMRC talk narrative:

- [Narrative entry point](narrative/index.md)
- [Navigation and scope](narrative/notes/navigation-and-scope.md)
- [AI Coding Assistants market briefing](narrative/notes/ai-coding-assistants-market-briefing.md)
- [Topic index](narrative/topics.md)

## 2021-2022: code generation and autocomplete

| Date | Event | Source | Source type | What changed technically | Why it matters | Caveat |
| --- | --- | --- | --- | --- | --- | --- |
| 2021-07-07 | OpenAI published the Codex/HumanEval paper. | EXT-001 | Research paper | Code generation was evaluated as synthesising Python functions from prompts/docstrings using functional tests. | Established an early public benchmark and made code generation a visible frontier capability. | HumanEval is narrow and does not evaluate repository context, review, operations or public-sector assurance. |
| 2021-08-20 | "Asleep at the Keyboard?" examined security of Copilot-generated code. | EXT-006 | Security research | Security researchers systematically prompted an AI coding assistant across weakness scenarios. | Put insecure generated code on the adoption agenda early. | Study used early Copilot-era capabilities and prompt scenarios; modern tools may differ. |
| 2022-06-21 | GitHub Copilot became generally available to individual developers. | EXT-002 | Vendor announcement | AI assistance moved into the editor as suggestions and completions in everyday development environments. | This normalised AI pair-programming as a coding workflow rather than only a research demo. | Vendor source; adoption and productivity claims are not independent evidence. |
| 2022-11-07 | "Do Users Write More Insecure Code with AI Assistants?" was submitted. | EXT-007 | Security user study | Researchers studied how users with and without a Codex-era assistant handled security tasks. | Highlighted overconfidence: AI-assisted users could both write less secure code and believe it was secure. | Task set and model generation are specific; use as risk evidence, not as a blanket claim about all tools. |

## 2023: chat, repository context, pull-request support, documentation support and SWE-bench

| Date | Event | Source | Source type | What changed technically | Why it matters | Caveat |
| --- | --- | --- | --- | --- | --- | --- |
| 2023-02-13 | Copilot productivity experiment reported faster completion on a bounded JavaScript task. | EXT-005 | Controlled experiment | Developers with Copilot completed a single HTTP-server task faster than controls. | Shows that AI coding support can materially help on bounded, well-specified work. | Lab task, speed-focused outcome and limited quality horizon. |
| 2023-03-22 | GitHub announced Copilot X. | EXT-003 | Vendor announcement | Copilot expanded from autocomplete towards chat, pull requests, docs and CLI interaction. | The interaction boundary began moving from lines of code towards conversations and repository-adjacent work. | Product announcement; not independent evidence of effectiveness. |
| 2023-10-10 | SWE-bench was released. | EXT-004 | Benchmark paper | Models were evaluated on resolving real GitHub issues by editing repositories. | Moved evaluation from function synthesis to repository-level software-maintenance tasks. | Open-source benchmark tasks can become contaminated; tests may not capture full correctness. |

## 2024: agent framing and real-world issue-resolution benchmarks

| Date | Event | Source | Source type | What changed technically | Why it matters | Caveat |
| --- | --- | --- | --- | --- | --- | --- |
| 2024-03-12 | Cognition introduced Devin. | EXT-008 | Vendor announcement | Devin was presented as an autonomous software-engineering agent with shell, code editor and browser in a sandbox. | The market narrative shifted from assistant to AI software engineer or teammate. | Strongly vendor-framed; benchmark and job-completion claims require independent verification. |
| 2024-04-30 | Amazon Q Developer became generally available. | EXT-009; EXT-028 | Vendor announcement/docs | AWS consolidated coding suggestions, chat, security scanning, troubleshooting and transformation into Q Developer. | Enterprise developer assistants began spanning more of the SDLC than code completion alone. | Vendor capability source, not independent productivity proof. |
| 2024-2025 | SWE-bench became the standard public reference point for agentic software-engineering progress. | EXT-004; EXT-021 | Benchmark and critique | Repository-level issue resolution became a common model-release metric. | It gave teams a shared vocabulary for issue-level coding performance. | Later evidence shows benchmark validity and contamination problems at frontier levels. |

## 2025: cloud, terminal and asynchronous coding agents

| Date | Event | Source | Source type | What changed technically | Why it matters | Caveat |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-02-24 | Anthropic announced Claude Code in limited research preview. | EXT-010 | Vendor announcement | Claude Code could search/read code, edit files, write/run tests, commit/push and use command-line tools. | Terminal-based agentic coding became a mainstream tool category. | Vendor source; claims about time saved require independent evidence. |
| 2025-03-19 | METR published long-task autonomy research. | EXT-019 | Evaluation research | Capability was framed by the length of tasks agents can complete reliably. | Helps explain why short benchmark success does not equal autonomous project delivery. | Extrapolation is sensitive to task mix, human baselines and future trend changes. |
| 2025-05-16 | OpenAI introduced Codex as a cloud software-engineering agent. | EXT-011 | Vendor announcement | Codex could run isolated cloud tasks, inspect repositories, edit files, run commands and provide logs/test evidence. | This is the clearest example of the "steering agents" workflow: assign bounded work, review output, iterate. | Vendor release; safe use still requires human review and validation. |
| 2025-05-19 | GitHub introduced Copilot coding agent. | EXT-016; EXT-017 | Vendor announcement/docs | Copilot could work from issues or prompts, create branches/draft PRs and run in GitHub Actions environments. | Coding agents were integrated into normal GitHub issue/PR workflows. | Availability and controls depend on plan, repository policy and organisation settings. |
| 2025-05-20 | Google Jules entered public beta. | EXT-014 | Vendor announcement | Jules cloned repositories into cloud VMs and worked asynchronously on tests, features, bugs and dependencies. | Multiple major vendors converged on asynchronous repo-level agent patterns. | Vendor capability source; not independent evidence of quality. |
| 2025-07-10 | METR reported a slowdown for experienced open-source developers using early-2025 AI tools. | EXT-020 | Randomised controlled trial | Real maintainers worked on their own repository issues with or without AI tools. | A useful counterweight to hype: experienced developers on mature codebases may incur review/prompt/wait costs. | Small, specific setting; should not be generalised to all developers or all future tools. |
| 2025-08-06 | Google Jules moved out of beta. | EXT-015 | Vendor announcement | Jules added structured access tiers and a more mature asynchronous agent product surface. | Reinforced that cloud agent workflows were becoming products, not only previews. | Vendor source; usage numbers are not independent evidence. |

## January-May 2026: multi-agent workflows, long-task autonomy, governance and benchmark limits

| Date | Event | Source | Source type | What changed technically | Why it matters | Caveat |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-02-23 | OpenAI argued SWE-bench Verified no longer measured frontier coding capability well. | EXT-021 | Vendor benchmark critique | The critique identified flawed tests and contamination as key benchmark problems. | Public-sector buyers should not treat public benchmark scores as procurement evidence. | Vendor analysis; still useful because it documents concrete failure modes. |
| 2026-05-08 | OpenAI Codex changelog showed continuing CLI/product updates through May 2026. | EXT-012 | Vendor documentation | Coding-agent tooling continued to change quickly, including CLI releases and model/API availability changes. | Governance and training material can go stale quickly. | Changelog records product movement, not real-world adoption value. |
| 2026-05-09 | Current tool documentation describes coding agents across terminal, cloud, IDE, GitHub and browser surfaces. | EXT-013; EXT-017; EXT-018 | Vendor documentation | Agents can use sandboxes, approvals, repository tools, MCP and pull-request workflows. | The operating model must cover tool permissions, auditability, human approval and environment isolation. | Documentation changes rapidly and must be rechecked before operational decisions. |

## Synthesis

What changed is not merely model quality. It is the workflow boundary. The unit of interaction moved from token, to line, to function, to conversation, to file, to repository, to issue, branch, pull request and bounded task.

That shift changes public-sector engineering practice. A team no longer asks only whether AI can write code. It asks whether the delivery system can safely absorb faster code generation: source-data controls, branch strategy, tests, security scanning, accessibility review, data protection, audit logs, human review and accountable ownership.
