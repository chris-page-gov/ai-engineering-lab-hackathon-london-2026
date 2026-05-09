# Project context: HMRC Beyond the Hype research pack

## Speaking context

The research is background material for a 15-minute talk, followed by 15 minutes of questions, at an HMRC Beyond the Hype event.

**Talk title:** From Typing Code to Steering Agents: Lessons from the AI Engineering Lab Codex Build

**Subtitle:** What coding assistants change, what they don’t, and how to use them safely in public-sector engineering.

**Source repository:** https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026.git

**Time horizon:** The review should cover the development of AI support for software engineering from 2021 to May 2026.

## Purpose of the paper

The paper is intended to provide:

1. A quick reference on what has happened, and when, in the advance from AI coding assistants to agentic AI systems that can write, test, and modify code across a repository.
2. An academically rigorous, evidence-based review with validated citations and URLs for follow-up.
3. A practical public-sector framing: what coding assistants and agents change, what they do not change, and how they can be used safely in government engineering.

## Core research questions

1. What changed between early AI coding assistants and agentic software-engineering tools?
2. What can the best available evidence tell us about productivity, quality, safety, security, developer experience, and organisational effects?
3. What does the AI Engineering Lab Codex Build show about human steering, agent contribution, assurance, and production-readiness limits?
4. What operating model would allow public-sector engineering teams to use coding agents safely and responsibly?

## Working thesis

By May 2026, AI support for software engineering has shifted from completion inside the editor to delegation of bounded engineering work to agents. The human role is moving from typing most of the code towards framing the task, constraining the environment, judging trade-offs, testing, reviewing, and owning the risk.

The central claim is not that engineering judgement disappears. The stronger claim is that implementation can become faster and more parallel, while assurance, context-setting, and accountability become more important.

## Public-sector framing

The research should be written for readers who care about reliable public services, not only software productivity. In this context, coding agents may help with prototypes, backlog reduction, documentation, tests, migration support, refactoring, evaluation harnesses, and evidence-pack generation. They do not remove the need for:

- secure-by-design delivery;
- accountable service ownership;
- human code review;
- testing and CI/CD controls;
- dependency and supply-chain governance;
- privacy and data-protection assessment;
- accessibility;
- procurement discipline;
- operational readiness;
- clear audit trails.

## Important distinction

Use these definitions consistently unless a source uses different terminology.

**Coding assistant:** A tool that helps a developer by suggesting code, answering questions, explaining code, or assisting with small edits while the developer remains the direct operator.

**Coding agent:** A system that can take a higher-level task, inspect a repository, plan changes, edit multiple files, run commands or tests, use a sandbox or terminal, and produce a branch, patch, pull request, or other work product for human review.

## Narrative spine for the talk

The unit of interaction has shifted:

```text
token -> line -> function -> conversation -> file -> repository -> issue -> branch -> pull request -> bounded task
```

The safe question is not simply: “Can AI write the code?”

A better public-sector question is: “Have we built an engineering system in which faster code generation leads to better, safer services?”

## Repo-specific caution

Do not infer facts about the AI Engineering Lab Codex Build that are not supported by repository evidence. Use repository-local documents for repo-specific claims. Use external sources only to contextualise the repo case study.
