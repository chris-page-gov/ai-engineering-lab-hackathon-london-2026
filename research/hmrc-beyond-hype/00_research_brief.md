# Research brief: From Typing Code to Steering Agents

## Purpose

This pack supports a 15-minute HMRC "Beyond the Hype" talk with a 15-minute Q&A:

**From Typing Code to Steering Agents: Lessons from the AI Engineering Lab Codex Build**

**Subtitle:** What coding assistants change, what they don't, and how to use them safely in public-sector engineering.

The pack answers four questions:

1. What changed between early AI coding assistants and coding agents?
2. What does the evidence say about productivity, quality, safety, developer experience and governance?
3. What does this repository show as a case study?
4. What operating model should public-sector engineering teams use before adopting coding agents?

The source register is [01_source_register.csv](01_source_register.csv). Methods and limitations are in [appendix A](appendices/a_methods.md). Search queries are in [appendix B](appendices/b_search_queries.md). Exclusions are in [appendix C](appendices/c_excluded_sources.md). The claims matrix is in [appendix D](appendices/d_claims_matrix.md).

## 2026-05-11 Import Note

The local `research/hmrc-beyond-hype/import/` drop adds a richer market briefing, a ClawPilot / OpenClaw research brief, slide-source files, image assets, a PDF on AI-native engineering teams, and two audio files. The immediate talk implication is to strengthen the category-first framing: IDE assistant, terminal/repo agent, PR/review assistant, autonomous issue-to-PR agent, and enterprise control layer.

Treat the imported material as source input, not finished evidence. The Markdown briefing is useful enough to track, but the larger binary/audio resources remain local by default until there is a clear publication decision. The two audio files have been transcribed under `research/hmrc-beyond-hype/transcripts/`, including pyannote `Trace` / `Query` voice-name diarization drafts. Promote individual claims into the main source register only after their external links, dates, and audio quotations have been revalidated.

The active follow-on goal is recorded in [narrative/README.md](narrative/README.md): build a GitHub-browsable narrative wiki with slide/image sidecars, topic navigation, valid links, no orphaned notes, and a coherent talk arc. The current import milestone is browseable from [narrative/index.md](narrative/index.md), with the 13-file sidecar-generation inventory represented in [narrative/notes/import-inventory.md](narrative/notes/import-inventory.md), 73 visual sidecars, and validation output under [narrative/data/](narrative/data/). `AI-Native_Engineering_Blueprint.pptx` itself has 15 slides; the additional AI-native material is covered separately through the AI-native PDF, workflow PNG, and AI Coding Assistants briefing notes.

## 2026-05-12 Demo Deck Publication Note

The selected slides for the 2026-05-12 presentation are [beyond_hype_coding_assistants_public_sector_engineering.pptx](import/beyond_hype_coding_assistants_public_sector_engineering.pptx). This is an explicit publication exception to the default raw-import rule: the deck is intentionally included so the public fork and release can point to the same presentation material used in the demo.

## One-page synthesis

By May 2026, AI support for software engineering has moved from autocomplete and chat towards bounded task delegation. The important change is not only model quality. It is the workflow boundary: token to line, line to function, function to conversation, conversation to file, file to repository, repository to issue, branch, pull request and bounded task.

The evidence does not support a single productivity multiplier. Controlled lab evidence shows large gains on bounded tasks [EXT-005]. Realistic experienced-developer evidence can show slowdown in mature repositories [EXT-020]. Benchmark evidence shows genuine progress on repository-level issue resolution [EXT-004], but also substantial benchmark validity problems, including contamination and flawed tests [EXT-021]. Security studies show that generated code can be vulnerable and that users can over-trust AI-assisted code [EXT-006; EXT-007].

The safest practical claim is:

> AI coding support is best understood as a conditional capability amplifier, not a uniform productivity multiplier.

For the public sector, this matters because faster implementation only helps if the surrounding engineering system can keep up. The relevant controls are task selection, sandboxing, least privilege, no secrets in agent environments, branch protection, human review, testing, dependency and security scanning, accessibility review, data-protection review, audit logs and named service-owner accountability [EXT-023; EXT-024; EXT-025; EXT-026; EXT-027].

## Repo case-study thesis

This repository is useful because it shows the shift from typing code to steering agents without pretending that the agent became accountable.

The Challenge 2 problem is public-sector dark data: guidance, policy and procedural material exists, but it is trapped in PDFs, Word files, spreadsheets and shared-drive-style material [REPO-002]. The repo implements a source-backed prototype with 43 synthetic documents, a generated wiki, topic/entity/map notes, a browser Dark Data Workbench, Browser AI and MCP export paths, a 100-question evaluation benchmark, audit artefacts, postmortem evidence and a government-security assessment [REPO-001; REPO-008; REPO-010; REPO-012; REPO-017].

The strongest talk line is:

> Provenance is the product.

The demo is not "watch AI answer a question". It is "show how a team makes source-backed answers possible". The workbench records the user's question, filters sources, builds an evidence set, exposes source cards and exports the question plus evidence bundle for AI use [REPO-010; REPO-011].

## Claims safe to use in the public talk

| Claim | Source support | Caveat |
| --- | --- | --- |
| The workflow has shifted from autocomplete towards bounded task delegation. | Product timeline from GitHub, Anthropic, OpenAI, Google and AWS [EXT-002; EXT-010; EXT-011; EXT-014; EXT-016]. | Product capabilities are vendor-described; do not treat them as independent proof of effectiveness. |
| Productivity evidence is conditional, not uniform. | Copilot lab task speedup [EXT-005] conflicts with METR experienced-developer slowdown [EXT-020]. | Different tasks, users, quality bars and codebases explain much of the conflict. |
| Benchmark scores are not production-readiness evidence. | SWE-bench paper [EXT-004], METR time-horizon framing [EXT-019], OpenAI benchmark critique [EXT-021]. | Benchmarks are still useful when interpreted narrowly. |
| Generated code must be treated as untrusted until reviewed, tested and accepted. | Security studies and NCSC/GOV.UK guidance [EXT-006; EXT-007; EXT-024; EXT-025]. | Modern tools may improve, but the control principle remains. |
| The Challenge 2 repo is a synthetic prototype and evidence pack, not a production government service. | README and security assessment [REPO-001; REPO-017]. | Do not imply operational readiness. |
| Codex was strongest in Explorer, Builder, Refiner and Verifier modes in this repo. | Contribution/security assessment [REPO-017]. | This is a repo-local assessment, not a general benchmark of Codex. |
| Real HMRC or government data would need approved handling, assurance, audit, DPIA/security controls and accountable ownership. | UK AI Playbook, NCSC, Service Standard, Secure by Design and ICO guidance [EXT-023; EXT-024; EXT-025; EXT-026; EXT-027]. | Specific approval routes depend on HMRC policy and data classification. |

## Claims not yet safe to use

| Claim | Why not safe |
| --- | --- |
| "Coding agents make teams X per cent faster." | Evidence varies by task, codebase, developer experience, tool, quality bar and review burden [EXT-005; EXT-020]. |
| "Codex proved the repo is production-ready." | The repo is a synthetic prototype; the security assessment explicitly rejects production-readiness claims [REPO-017]. |
| "Benchmark leaderboards prove procurement value." | Benchmarks can be contaminated, narrow, scaffolded and disconnected from local security/accessibility/privacy needs [EXT-004; EXT-021]. |
| "Agent sandboxing solves the security problem." | Sandboxing is one control. It does not replace review, least privilege, scanning, data handling and accountable risk acceptance [EXT-013; EXT-024]. |
| "AI can replace junior developers." | This pack does not provide labour-market evidence for replacement. The repo case shows human framing, review and accountability remained central [REPO-018]. |

## Q&A-ready short answers

**Can we use this with real HMRC data?**
Only inside an approved data-handling and security model. This repo used synthetic data. Real HMRC data would need classification, approved tooling, processor assurance, no secret leakage, audit logs, DPIA screening where relevant and named accountability.

**How much faster was it really?**
This repo shows rapid implementation, but it is not a controlled productivity study. The evidence base says speedups are conditional: bounded lab tasks can be faster, while experienced developers in mature codebases can be slower.

**Which tool should we start with?**
Start with the approved tool your organisation can govern. The first pilot should be low-risk, repository-local, testable and reviewable. Tool choice matters less than data handling, permissions, review and evidence capture.

**How do you know the output is right?**
You do not know from fluency. You inspect diffs, run tests, check source citations, scan dependencies and generated code, review security/privacy/accessibility implications and record evidence.

**Will this replace junior developers?**
The safer framing is that tasks shift. People still need to understand the problem, set constraints, review output, learn judgement and own risk. Junior development may need more deliberate mentoring because typing small pieces of code is no longer the only learning path.

**What setup is needed?**
Repo rules, a clean dev environment, test commands, documentation lockstep, source-data rules, secret handling, branch protection, CI, review expectations and an escalation path for security/data questions.

**What are the biggest failure modes?**
Over-trust, weak context, broad permissions, secret exposure, hallucinated dependencies, vulnerable code, unsupported claims, stale sources, inaccessible UI, poor auditability and unclear ownership.
