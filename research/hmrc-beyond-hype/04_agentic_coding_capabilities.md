# Agentic coding capabilities and benchmark limits

## What benchmarks show

Benchmarks show that model capability has moved beyond isolated function generation towards repository-level issue resolution and longer-horizon agent tasks.

They do not show that a tool is ready for public-sector production work.

## HMRC Talk Navigation

This file is supporting evidence for the HMRC talk narrative:

- [Narrative entry point](narrative/index.md)
- [Navigation and scope](narrative/notes/navigation-and-scope.md)
- [AI-Native Engineering Blueprint narrative guide](narrative/slides/ai-native-engineering-blueprint/narrative-guide.md)
- [AI Coding Assistants market briefing](narrative/notes/ai-coding-assistants-market-briefing.md)
- [Topic index](narrative/topics.md)

## HumanEval and early code-generation benchmarks

HumanEval, introduced with the Codex paper, measured whether a model could generate Python function bodies from prompt/docstring-style tasks and pass tests [EXT-001]. It was valuable because it gave a concrete functional-correctness measure for code synthesis.

Its limitations are important:

- it is small and narrow;
- it largely evaluates isolated functions;
- it does not evaluate repository navigation, architecture, data handling, review, CI/CD, accessibility, privacy or operational ownership;
- it can encourage benchmark-driven overclaiming.

For the talk, HumanEval is useful as the "line/function" era of the timeline, not as evidence about modern coding-agent readiness.

## SWE-bench and repository-level issue resolution

SWE-bench changed the task shape. Instead of generating isolated functions, a model receives a real GitHub issue and a repository state, then must edit the codebase so tests pass [EXT-004].

This matters because the task resembles maintenance work more closely:

- finding relevant files;
- understanding an issue;
- modifying multiple files;
- interacting with a repository;
- relying on test outcomes.

But SWE-bench is still not production readiness. It is a benchmark over selected open-source repositories with automated tests. It does not ask whether a service owner should accept the operational risk of a change.

## SWE-bench Verified and human validation

SWE-bench Verified attempted to improve SWE-bench by filtering tasks through expert review. It became a common reported score for frontier coding agents.

By February 2026, OpenAI argued that SWE-bench Verified no longer measured frontier coding capabilities well because of test-design problems and contamination [EXT-021]. The important public-sector lesson is not that SWE-bench is useless. The lesson is that public benchmarks age, leak and narrow.

## SWE-bench Live and contamination-resistant approaches

This pack did not verify a primary SWE-bench Live source cleanly enough to rely on it as a main evidence row. The limitation is recorded in [appendix C](appendices/c_excluded_sources.md), and exact follow-up search queries are recorded in [appendix B](appendices/b_search_queries.md).

Equivalent contamination-resistant principles are still clear from the verified sources:

- use fresh or privately authored tasks where possible;
- avoid tasks and solutions likely to be in model training data;
- review whether tests accept functionally correct solutions;
- use human review where tests are incomplete;
- evaluate on local representative work, not only public leaderboards [EXT-019; EXT-021].

## Long-task autonomy and time horizons

METR's long-task research frames capability by the length of tasks agents can complete at given reliability thresholds [EXT-019]. This is useful because software engineering is often not a single answer. It is a sequence of exploration, editing, testing, debugging and revision.

The public-sector implication is straightforward:

- short task success is not enough evidence for day-long delegated work;
- high benchmark performance does not imply reliable production operation;
- teams should measure elapsed time, interventions, rework and review burden, not only pass/fail.

## Why benchmark scores should not be treated as procurement evidence

Benchmark scores should not be treated as procurement evidence because they usually miss the conditions that make government engineering hard.

| Benchmark issue | Why it matters |
| --- | --- |
| Contamination | Public tasks, solutions and discussions may appear in training data, inflating scores. |
| Stale tasks | Benchmarks age while tools adapt to them. |
| Flawed or incomplete tests | Automated tests can reject valid fixes or accept incomplete ones. |
| Narrow language and repository coverage | Public-sector estates include legacy systems, data pipelines, low-code tools, casework systems and policy constraints. |
| Hidden scaffolding | Reported scores may depend on retrieval, retries, ranking, test-time compute or human-crafted prompts. |
| Model-specific tool environments | A benchmark result may rely on a shell, browser, file editor or CI setup unavailable in a target organisation. |
| Lack of data-governance evaluation | Benchmarks rarely assess data classification, retention, processor assurance or DPIA requirements. |
| Lack of security evaluation | Passing tests does not prove secure code. |
| Lack of accessibility evaluation | Web/UI changes may pass tests but fail users. |
| Mismatch with legacy estates | Government codebases often have implicit rules, old dependencies and operational constraints. |
| Mismatch with service ownership | Benchmarks do not assign risk accountability to an SRO, service owner or security owner. |

## Capabilities that matter locally

For public-sector engineering, the useful capabilities are not just "can write code".

Teams should evaluate whether an agent can:

- understand repository rules and local docs;
- preserve raw-source immutability;
- make small reviewable changes;
- run the right tests;
- update documentation in lockstep;
- cite evidence and explain uncertainty;
- avoid secrets and local-path leaks;
- respect sandbox and network restrictions;
- avoid introducing unapproved dependencies;
- produce audit logs or reconstruction evidence;
- handle accessibility and content constraints;
- stop and escalate when a task is outside policy.

## Local evaluation protocol

A responsible local pilot should include:

1. Representative backlog tasks selected by developers and product owners.
2. Fixed acceptance criteria before the agent starts.
3. Human-blind review where possible, so reviewers judge output quality rather than tool identity.
4. Required tests, linters, static analysis and security checks.
5. Accessibility checks for user-facing changes.
6. Dependency and secret scanning.
7. CI/CD checks under normal branch protection.
8. Cost, elapsed time and intervention measurement.
9. Defect and rework tracking.
10. Audit logs: prompt, files changed, commands run, tests run and review outcome.
11. Comparison against a non-agent baseline or previous team norms.
12. Explicit decision criteria: adopt, restrict, retrain, redesign or reject.

## Talk-ready synthesis

Benchmarks tell us that coding agents are becoming more capable. They do not tell us whether a government team should trust a given change in a live service.

The safe path is local evidence over representative tasks, with human review and assurance gates that match the risk of the work.
