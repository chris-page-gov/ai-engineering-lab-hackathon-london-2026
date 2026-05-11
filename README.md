# Challenge 2 Dark Data Implementation

This fork is Team DSIT A's working Challenge 2 implementation and evidence pack from the AI Engineering Lab Hackathon London 2026.

It demonstrates how a messy collection of government-style guidance, policy, procedure, PDF, Word, and spreadsheet material can be turned into a source-backed knowledge base, inspected without AI, exported to AI tools with explicit evidence, evaluated through a repeatable benchmark, and preserved as an auditable postmortem of human and Codex contributions.

The original repository was an event pack for a one-day AI-assisted engineering hackathon. This fork now serves a different purpose: it is the implementation record for the "Unlocking the dark data" challenge and a worked example of how AI coding assistants can help build, test, document, and critique a government-style prototype.

## Value Proposition

Challenge 2 asks what it would take to make large volumes of government documentation findable, source-backed, and usable by people and AI systems. This fork provides a concrete answer:

- A generated LLM Wiki over 43 synthetic source documents, with one source note per raw document.
- Topic, entity, map, table, source-register, and lint outputs for transparent navigation.
- A browser workbench for searching, filtering, reading, selecting, and exporting evidence without requiring AI.
- Browser AI and MCP export paths that carry the user's question and selected sources together.
- A 100-question evaluation benchmark for testing whether AI coding agents can answer from the generated wiki.
- Audit and postmortem artifacts showing how the implementation was produced, validated, reviewed, and packaged for publication.
- A government-security assessment of the repo and of Codex's suitability across contribution modes.

The result is not a production government service. It is a tested prototype and evidence trail showing how dark-data engineering could work, what controls helped, and what would still be required before real government data or production use.

## Start Here

New to the repo or arriving from LinkedIn? Start with the [reader guide](START-HERE.md) for routes by role, interest, and time available.

For the Challenge 2 implementation:

- [Challenge 2 brief](challenge-02-unlocking-the-dark-data.md): the original problem statement.
- [Challenge 2 wiki index](challenge-2/wiki/index.md): generated Obsidian-friendly knowledge base.
- [Demonstration guide](challenge-2/wiki/demonstration-guide.md): end-to-end walkthrough of the prototype.
- [Dark Data Workbench guide](challenge-2/wiki/workbench.md): how to run and use the browser workbench.
- [Evaluation benchmark](challenge-2/wiki/evaluation-benchmark.md): 100 source-backed questions with scoring guidance.
- [Realtime delivery report](output/doc/challenge-2-realtime-delivery-report.md): narrative reconstruction of the build.
- [Codex postmortem](postmortem-public/wiki/index.md): GitHub-safe collaboration postmortem.
- [Contribution modes and security assessment](output/doc/codex-contribution-modes-security-assessment.md): assessment of Codex, contribution modes, and security findings.
- [MCP research wiki](challenge-2/MCP-Wiki/index.md): research, candidates, licensing posture, and implementation planning for a purpose-built Wiki MCP server.
- [HMRC Beyond the Hype talk research pack](research/hmrc-beyond-hype/00_research_brief.md): evidence-backed preparation for a mixed-audience talk on moving from coding assistants to coding agents.
- [HMRC talk narrative wiki](research/hmrc-beyond-hype/narrative/index.md): GitHub-browsable narrative scaffold, visual sidecars, topic navigation, source-material register, and validation output for the HMRC talk.
- [HMRC talk import inventory](research/hmrc-beyond-hype/narrative/notes/import-inventory.md): publication-safe treatment for every current file in the local talk-prep import folder.
- [AI Coding Assistants market briefing](research/hmrc-beyond-hype/narrative/notes/ai-coding-assistants-market-briefing.md): narrative note for the imported Markdown/DOCX briefing pair and the companion evolution visual.
- [HMRC talk narrative wiki goal](research/hmrc-beyond-hype/narrative/README.md): durable definition of done and sidecar coverage status for the GitHub-browsable narrative pack.
- [HMRC talk audio transcripts](research/hmrc-beyond-hype/transcripts/README.md): local Whisper transcripts and pyannote `Trace` / `Query` voice-name diarization drafts for the imported prep audio.
- [LinkedIn announcement draft](output/doc/linkedin-version-1-1-announcement.md): publication post for Version 1.1.

## What Was Built

### Generated LLM Wiki

The Challenge 2 wiki turns raw source material into structured Markdown and machine-readable outputs:

- raw Challenge 2 sources remain immutable
- generated notes live under `challenge-2/wiki/`
- source notes preserve provenance and caveats
- topic, entity, and map notes make the corpus navigable
- JSON and table exports support tool use
- lint output checks generated coverage, links, metadata, and known challenge flags

The repeatable builder is [challenge-2/tools/build_wiki.py](challenge-2/tools/build_wiki.py).

### Dark Data Workbench

The workbench in [challenge-2/workbench/](challenge-2/workbench/) is a SvelteKit browser UI over the generated corpus. It supports:

- searching and filtering sources
- reading source metadata and extracted content
- building explicit context sets
- saving source-context selections locally
- exporting evidence bundles
- copying Browser AI prompts
- generating MCP-ready context
- running saved source-backed checks

The workbench is deliberately useful without AI. AI export is optional and evidence-led.

### Evaluation Harness

The evaluation harness tests whether AI coding agents can answer benchmark questions using only the generated wiki and approved local context. It includes:

- [challenge-2/wiki/evaluation-benchmark.md](challenge-2/wiki/evaluation-benchmark.md): 100 questions, gold answers, rubrics, and scoring.
- [challenge-2/tools/run_wiki_eval.py](challenge-2/tools/run_wiki_eval.py): CLI runner for Codex, Gemini CLI, Claude Code, GitHub Copilot CLI, and Microsoft Copilot UI coverage, with per-client model/version manifests for auditable runs.
- [challenge-2/tools/wiki_eval_mcp.py](challenge-2/tools/wiki_eval_mcp.py): stdio MCP audit layer.
- [challenge-2/tools/summarise_wiki_eval.py](challenge-2/tools/summarise_wiki_eval.py): scoring-sheet and leaderboard summariser.
- [challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-leaderboard.md](challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-leaderboard.md): rubric-scored leaderboard for the validated full run, with raw answers kept outside Git.

### Postmortem and Publication Pack

This branch also contains a public postmortem derivative:

- `postmortem/` is the private local evidence archive and is gitignored.
- [postmortem-public/](postmortem-public/) is the GitHub-safe derivative.
- [tools/build_codex_postmortem.py](tools/build_codex_postmortem.py) regenerates both the private archive and the public derivative.

The public postmortem preserves sequence, decisions, artifact links, and contribution evidence while excluding raw transcripts, local-only paths, and unlicensed copied third-party source bodies.

## Original Hackathon Context

The upstream repository was created for the AI Engineering Lab Hackathon London 2026: a one-day event where teams used AI coding tools to build prototypes against cross-government challenge briefs.

Challenge 2, "Unlocking the dark data", focused on a common government problem: guidance and policy material exists, but is hard to find, structure, evaluate, and use safely. This fork keeps the original briefs and starter material, but the README now documents the fork as the Challenge 2 implementation rather than as an invitation to attend the event.

The original event material remains available:

- [Open brief guidance](open-brief.md)
- [Challenge 1: From PDF to digital service](challenge-01-from-pdf-to-digital-service.md)
- [Challenge 2: Unlocking the dark data](challenge-02-unlocking-the-dark-data.md)
- [Challenge 3: Supporting casework decisions](challenge-03-supporting-casework-decisions.md)
- [Challenge 4: Knowing your own organisation](challenge-04-knowing-your-own-organisation.md)
- [Setup guide](SETUP-GUIDE.md)

## Repository Map

Core tracking and governance:

- `README.md`: this fork overview.
- `START-HERE.md`: reader guide for LinkedIn, event, and role-based routes through the repository.
- `Changelog.md`: dated change history.
- `Context.md`: project purpose, architecture assumptions, data policy, and operating constraints.
- `Progress.md`: implementation status, validation, blockers, and next steps.
- `AGENTS.md`: repo-wide operating rules, including documentation lockstep.
- `tools/check_documentation_lockstep.py`: local and CI check for tracking-document updates.

Challenge 2 implementation:

- `challenge-2/structured_files/`: synthetic text-based starter documents.
- `challenge-2/unstructured_files/`: synthetic binary-format starter documents.
- `challenge-2/tools/build_wiki.py`: repeatable wiki builder.
- `challenge-2/wiki/`: generated Obsidian-friendly knowledge base.
- `challenge-2/wiki/demonstration-guide.md`: end-to-end demo route.
- `challenge-2/wiki/evaluation-benchmark.md`: 100-question benchmark.
- `challenge-2/workbench/`: SvelteKit Dark Data Workbench.
- `challenge-2/tools/workbench_mcp.py`: MCP source search/read/context export server.
- `challenge-2/evaluation/`: evaluation harness support code.
- `challenge-2/tools/run_wiki_eval.py`: benchmark runner.
- `challenge-2/tools/wiki_eval_mcp.py`: audited MCP layer for wiki evaluation.
- `challenge-2/tools/summarise_wiki_eval.py`: leaderboard summariser.
- `challenge-2/MCP-Wiki/`: MCP research wiki for the planned read-only Wiki MCP server, including the Deep Research report, candidate register, source register, licensing posture, and implementation workspace.

Reports and publication artifacts:

- `output/doc/challenge-2-realtime-delivery-report.md`: colleague-facing delivery report.
- `output/doc/challenge-2-realtime-delivery-report.docx`: Word version of the delivery report.
- `output/doc/contribution-modes-proposal.md`: Markdown conversion of the attached contribution-modes proposal.
- `output/doc/codex-contribution-modes-security-assessment.md`: contribution-mode and security assessment.
- `output/doc/linkedin-version-1-1-announcement.md`: LinkedIn announcement draft for Version 1.1.
- `research/hmrc-beyond-hype/`: HMRC Beyond the Hype talk research pack, source register, case study, operating model, and appendices.
- `research/hmrc-beyond-hype/import/`: local talk-prep source drop; lightweight Markdown is trackable, while large binary/audio resources are ignored unless explicitly selected for publication.
- `research/hmrc-beyond-hype/narrative/index.md`: GitHub-browsable entry point for the HMRC talk narrative scaffold, including links to sidecars, topics, source materials, and validation reports.
- `research/hmrc-beyond-hype/narrative/notes/import-inventory.md`: generated coverage inventory showing the narrative treatment for every current import file.
- `research/hmrc-beyond-hype/narrative/notes/ai-coding-assistants-market-briefing.md`: source note for the imported AI Coding Assistants Markdown/DOCX briefing.
- `research/hmrc-beyond-hype/narrative/README.md`: active goal brief, acceptance criteria, and sidecar completion status for the GitHub-browsable talk narrative wiki.
- `research/hmrc-beyond-hype/transcripts/`: committed machine transcripts, SRT files, diarization evidence, and `Trace` / `Query` voice-name review drafts derived from the local audio import.
- `research/hmrc-beyond-hype/tools/`: local reproducibility scripts for audio transcription, pyannote diarization, visual sidecar generation, and narrative validation.
- `postmortem-public/wiki/index.md`: public Codex collaboration postmortem entry point.
- `postmortem-public/wiki/decisions.md`: publication decision register.
- `postmortem-public/wiki/data/publication-lint-report.json`: machine-readable publication lint output.

## Validation Summary

Recent local validation for this branch includes:

- Challenge 2 workbench typecheck, unit/component tests, production build, and Playwright tests.
- Python compile checks for the wiki builder, MCP tools, evaluation client, postmortem builder, and documentation lockstep tool.
- MCP unit tests for the workbench and evaluation layer.
- Documentation lockstep validation.
- `git diff --check` / staged whitespace validation.
- Credential-pattern scan, unsafe-code-pattern scan, `pnpm audit`, and Bandit security scan.

Known security and production-readiness gaps are recorded in [output/doc/codex-contribution-modes-security-assessment.md](output/doc/codex-contribution-modes-security-assessment.md). The most important point is that this is a synthetic prototype and research artifact, not a production service.

## Version

Version: 1.0
Last updated: May 2026
