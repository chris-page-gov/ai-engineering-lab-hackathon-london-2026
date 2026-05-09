# Repo Case Study: Codex Build

This case study turns the AI Engineering Lab Challenge 2 build into talk material for a mixed HMRC audience. It is not a claim that Codex built or assured a production government service. It is evidence that a coding agent can accelerate a bounded, synthetic-data engineering prototype when the human owner supplies intent, constraints, review, and validation.

Repo-local citations use the format `path:line` followed by a GitHub permalink to that exact line where available.

## Case Study Thesis

The useful shift was not "AI writes code instead of a developer". The useful shift was "the human steers a bounded engineering system". In this repo, Codex moved between exploration, implementation, refinement, and verification while the repository rules, tracking documents, tests, generated artefacts, and human judgement constrained the work.

The talk should frame the project as a concrete example of moving from typing code to steering agents:

- The problem was not a lack of government guidance; it was guidance buried across messy documents and hard to reconstruct safely. Local evidence: `challenge-2/wiki/demonstration-guide.md:17` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/wiki/demonstration-guide.md#L17)).
- The repo became a worked Challenge 2 implementation and evidence pack rather than only a hackathon starter. Local evidence: `README.md:3` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/README.md#L3)).
- The prototype made the source layer visible through a generated wiki, workbench, evaluation harness, MCP tooling, and postmortem evidence. Local evidence: `README.md:11` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/README.md#L11)).
- The public-sector engineering lesson is that provenance, review, and validation are part of the product, not paperwork added later. Local evidence: `challenge-2/wiki/demonstration-guide.md:278` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/wiki/demonstration-guide.md#L278)).

## Evidence-Led Story

| Talk claim | Repo evidence | What it supports | Caveat |
|---|---|---|---|
| Challenge 2 was a realistic "dark data" problem. | `challenge-2/wiki/architecture.md:23` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/wiki/architecture.md#L23)) | The corpus spans HTML, Markdown, text, PDFs, Word, and spreadsheets. | The dataset is synthetic, not HMRC operational data. |
| Raw source material was kept immutable. | `README.md:46` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/README.md#L46)); `challenge-2/AGENTS.md:7` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/AGENTS.md#L7)) | The build separated source material from generated wiki and app layers. | Rule compliance still depends on review and validation. |
| The wiki converted messy source documents into traceable knowledge objects. | `challenge-2/wiki/architecture.md:79` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/wiki/architecture.md#L79)) | The generated layer includes one source note for each of 43 documents. | Generated notes are only as reliable as the extraction logic and review. |
| The demo made provenance inspectable, not hidden behind generated answers. | `challenge-2/wiki/demonstration-guide.md:39` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/wiki/demonstration-guide.md#L39)) | Source notes expose ID, status, format, department, topics, provenance, extraction quality, warnings, and source path. | It is a demo workflow, not a certified records-management system. |
| The workbench was built around the user question, filters, source cards, and exportable evidence. | `challenge-2/workbench/README.md:3` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/workbench/README.md#L3)); `challenge-2/workbench/README.md:23` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/workbench/README.md#L23)) | The UI supports source inspection and Browser AI export from a selected evidence set. | Browser AI export is only appropriate for approved data classes and approved tools. |
| The repo included a measurable evaluation harness, not just a demo. | `challenge-2/evaluation/README.md:147` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/evaluation/README.md#L147)); `challenge-2/wiki/evaluation-benchmark.md:80` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/wiki/evaluation-benchmark.md#L80)) | The benchmark has 100 questions and a 500-point scoring structure. | Local synthetic benchmark scores are not procurement or production-readiness evidence. |
| The local leaderboard showed strong Codex performance on this narrow task. | `challenge-2/evaluation/reports/validated-full-20260419T2225Z-comparison.md:37` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/challenge-2/evaluation/reports/validated-full-20260419T2225Z-comparison.md#L37)) | Codex scored 484/500 on the committed local benchmark summary. | This is repo-local evidence only; official comparative claims need independent moderation. |
| The work was recorded as a continuous build with validation evidence. | `output/doc/challenge-2-realtime-delivery-report.md:16` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/output/doc/challenge-2-realtime-delivery-report.md#L16)); `output/doc/challenge-2-realtime-delivery-report.md:255` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/output/doc/challenge-2-realtime-delivery-report.md#L255)) | The repo has a dated delivery narrative and validation section. | The report is a reconstruction from project evidence, not an independent audit. |
| Human direction remained central. | `postmortem-public/wiki/postmortem.md:12` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/postmortem-public/wiki/postmortem.md#L12)) | The public postmortem separates human goal-setting from Codex implementation work. | Raw transcripts are deliberately not published. |

## Codex Contribution Mode Assessment

| Codex contribution mode | Repo evidence | Value created | Human control or review required | Production-readiness caveat |
|---|---|---|---|---|
| Explorer | `output/doc/codex-contribution-modes-security-assessment.md:40` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/output/doc/codex-contribution-modes-security-assessment.md#L40)) | Rapidly inspected the repo, inferred patterns, and found relevant evidence. | Human owner must decide what evidence matters and what can be published. | Exploration can surface sensitive paths, transcripts, or secrets unless sandboxed and reviewed. |
| Framer | `output/doc/codex-contribution-modes-security-assessment.md:41` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/output/doc/codex-contribution-modes-security-assessment.md#L41)) | Helped convert broad intent into research structure, postmortem structure, and review scope. | Human owner must approve the framing because it defines the claims and constraints. | Framing mistakes can send the agent down the wrong path quickly. |
| Builder | `output/doc/codex-contribution-modes-security-assessment.md:43` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/output/doc/codex-contribution-modes-security-assessment.md#L43)) | Implemented multi-file prototype features, reports, MCP tooling, tests, and documentation updates. | Code review, CI, dependency scanning, and narrow task boundaries are required. | Generated code can be plausible but wrong, insecure, or inconsistent with policy. |
| Refiner | `output/doc/codex-contribution-modes-security-assessment.md:44` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/output/doc/codex-contribution-modes-security-assessment.md#L44)) | Cleaned links, redactions, documentation, formatting, and publication packaging. | Review needs to catch unrelated rewrites and accidental meaning changes. | Refactoring and publication cleanup can silently change assurance evidence. |
| Verifier | `output/doc/codex-contribution-modes-security-assessment.md:46` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/output/doc/codex-contribution-modes-security-assessment.md#L46)) | Ran and extended checks such as tests, compile checks, lockstep checks, scans, and publication lint. | Humans must judge whether the validation set is sufficient for the risk. | Passing tests does not prove absence of security or data-protection issues. |
| Security Steward | `output/doc/codex-contribution-modes-security-assessment.md:47` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/output/doc/codex-contribution-modes-security-assessment.md#L47)) | Identified risk areas, local path leakage, licensing gaps, and production hardening needs. | Named security, privacy, and service owners must approve risk treatment. | The agent is a reviewer aid, not the authority for HMRC or government security sign-off. |
| Operator | `output/doc/codex-contribution-modes-security-assessment.md:48` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/d5aa7c9688f2a703cc6665344a37d5e7cb0fe50f/output/doc/codex-contribution-modes-security-assessment.md#L48)) | Helped with local validation and branch/package workflow only. | Production operation needs runbooks, monitoring, approvals, incident response, and accountable humans. | This repo contains no evidence that Codex should autonomously operate a live public service. |

## Demo Flow For The Talk

1. Open with the user problem: published material exists, but users cannot easily find the right source-backed answer.
2. Show the repo README as the "what this is" slide: a Challenge 2 implementation and evidence pack.
3. Show `AGENTS.md`, `Context.md`, `Progress.md`, and `Changelog.md` as the steering rails.
4. Show the wiki index and architecture page: raw documents stay put, generated knowledge becomes navigable.
5. Show the Dark Data Workbench: question box, filters, source cards, context set, Browser AI export.
6. Show the evaluation harness and leaderboard with the caveat that it is a local synthetic benchmark.
7. Close the demo by returning to the boundary: this is a disciplined prototype pattern, not production approval.

## Talk-Safe Claims

Safe:

- "Codex helped build across code, docs, tests, reports, and validation in this repo."
- "The value came from the workflow: clear goal, repo rules, source immutability, review, tests, and evidence."
- "The prototype shows how coding agents can make source-backed answers easier to build and evaluate."
- "The local benchmark is useful project evidence, not a procurement ranking."
- "For real HMRC data, the operating model must add approved tooling, data controls, DPIA/security review, and named ownership."

Not safe:

- "Codex can safely work on any government data."
- "The model output is correct because it sounds confident."
- "The benchmark proves one tool is best."
- "Agents replace junior developers."
- "This repo is production-ready for HMRC."

## Practical Lessons For HMRC Teams

- Start with low-risk, internal, non-live material.
- Give the agent repo-level rules before asking for implementation.
- Keep raw source data immutable.
- Ask for small, reviewable changes.
- Require evidence for claims and tests for behaviours.
- Inspect diffs, not just the final answer.
- Treat fluent output as a draft until the source, test, and assurance evidence agree.
