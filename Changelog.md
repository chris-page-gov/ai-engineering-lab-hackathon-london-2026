# Changelog

All notable changes to this repository are tracked here.

This file follows the spirit of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/): dated entries, human-readable summaries, and clear categories for additions, changes, fixes, removals, security notes, and documentation updates.

## Unreleased

### Added

- Added `challenge-2/wiki/demonstration-guide.md`, an end-to-end Challenge 2 demo route covering source construction, Obsidian validation, SeeLinks-style workbench flows, Browser AI export, the evaluation matrix/harness, and audit/FOI tracking.
- Added `postmortem/`, a generated Codex collaboration postmortem wiki with read-only conversation sources, prompt-response exchange notes, external methodology snapshots, repository artifact permalinks, source registers, and a detailed postmortem.
- Added `postmortem/publication-readiness-report.md` to record redaction and packaging changes required before public release of the Codex postmortem artifacts.
- Added `postmortem-public/`, a GitHub-safe public derivative of the Codex postmortem with redacted prompt-response notes, conversation summaries, citation-only external source notes, repository evidence permalinks, publication decisions, and publication lint output.
- Added licensing findings for the localized Karpathy X/gist source copies, including a recommendation to publish citation metadata and short excerpts rather than full third-party source bodies.
- Added `tools/build_codex_postmortem.py` to regenerate the private Codex postmortem archive and the public `postmortem-public/` derivative from local Codex rollout JSONL files, verified Karpathy LLM Wiki references, and GitHub fork permalinks.
- Added `output/doc/contribution-modes-proposal.md`, a Markdown conversion of the attached contribution-modes proposal with extracted media.
- Added `output/doc/codex-contribution-modes-security-assessment.md`, evaluating project contribution modes, Codex suitability, and security scan findings against government Secure by Design, NCSC, GOV.UK, ICO, NIST SSDF, and OWASP expectations.
- Added `output/doc/linkedin-version-1-1-announcement.md`, a LinkedIn announcement draft for the public Version 1.1 publication.
- Added GitHub-renderable SVG replacements for the contribution-modes proposal diagrams so the Markdown renders without EMF support.
- Added regression coverage for postmortem contribution inference and public local-path sanitisation.
- Added a Dark Data Workbench question box that carries the user's question into Browser AI JSON, copied prompts, Markdown evidence bundles, and saved-check flows.
- Added `output/doc/challenge-2-realtime-delivery-report.md` and `.docx`, a linked and illustrated colleague report reconstructing the Challenge 2 build timeline from the source write-up, repo history, logs, and Codex thread evidence.
- Added Dark Data Workbench, a SvelteKit browser UI under `challenge-2/workbench/` for filtering the Challenge 2 wiki corpus, building context sets, browsing evidence, and exporting optional AI/MCP context.
- Added `challenge-2/tools/workbench_mcp.py` to expose Dark Data Workbench search, source read, and context-building flows to local MCP clients.
- Added unit, component, Playwright, and MCP tests for Dark Data Workbench, with optional coverage enforcement via `pnpm test:coverage`.
- Added a GitHub Actions workflow for Dark Data Workbench typecheck, tests, build, Playwright, and MCP validation.
- Added repo-wide tracking files: `Changelog.md`, `Context.md`, and `Progress.md`.
- Added repo-wide operating rules in `AGENTS.md` requiring documentation updates in lockstep with implementation changes.
- Added a GitHub pull request template with explicit documentation lockstep checks.
- Added `tools/check_documentation_lockstep.py` and a GitHub Actions workflow to enforce tracking-file updates on pull requests.
- Added `challenge-2/wiki/evaluation-benchmark.md` with 100 source-backed questions, gold answers, per-question rubrics, and a 500-point summative scoring regime for Challenge 2 wiki evaluation.
- Added a Challenge 2 wiki evaluation harness under `challenge-2/evaluation/` and `challenge-2/tools/run_wiki_eval.py` for Codex, Gemini CLI, and Claude Code prompt runs.
- Added per-client model/version manifests to Challenge 2 evaluation runs, including selected model source, model-reference URL/date, executable paths, version-command outputs, repo state, benchmark hash, and detected macOS Copilot desktop app versions.
- Added optional GitHub Copilot CLI support to the Challenge 2 evaluation harness, gated behind explicit `--clients github-copilot` selection or client configuration.
- Added `challenge-2/tools/wiki_eval_mcp.py`, a stdio MCP-compatible audit layer for controlled wiki search/read, answer recording, and DSAP-shaped audit pack finalisation.
- Added `challenge-2/tools/summarise_wiki_eval.py` to turn completed scoring sheets into leaderboard JSON and Markdown.

### Changed

- Updated Challenge 2 evaluation default model policy to use explicit `gpt-5.4` for Codex, Gemini CLI Auto routing, and Claude Code's `opus` latest-model alias, with floating selectors recorded as aliases rather than immutable model snapshots.

### Fixed

- Updated the Challenge 2 architecture Mermaid labels from `1.`, `2.`, etc. to `Step 1:`, `Step 2:`, etc. so Obsidian does not render them as unsupported Markdown lists.
- Fixed the documentation lockstep check so it fails if required tracking files are deleted, even when their deleted paths appear in the diff.
- Hardened Dark Data Workbench Playwright interactions for facet and view controls, and exposed explicit pressed-state metadata for those controls.
- Stopped tracking Obsidian workspace session state so local vault browsing no longer dirties the repository.
- Ignored the private `postmortem/` evidence archive so only `postmortem-public/` is intended for GitHub publication.
- Ignored root-level Obsidian state so local browsing metadata is not included with the public postmortem.
- Ignored Python bytecode caches created by local validation runs.
- Hardened the postmortem external-source fetcher with HTTPS and host allowlisting.
- Fixed postmortem contribution inference so `pr` and `git` are matched as whole words instead of substrings inside words such as `prompt` or `legitimate`.
- Fixed Karpathy X source snapshot URLs to use a single Jina Reader prefix instead of proxying an already proxied URL.
- Fixed public postmortem sanitisation for bare local user-path markers and local state-file mentions in explanatory text.

### Documentation

- Recast `README.md` from the original event-invitation framing into a fork-specific Challenge 2 implementation overview with the value proposition, start points, repository map, validation summary, and original hackathon context.
- Added Team DSIT A attribution to the README, delivery report, security assessment, LinkedIn draft, and public postmortem generation.
- Linked the Challenge 2 demonstration guide from the wiki index, README, and Challenge 2 brief.
- Linked the public Codex collaboration postmortem from `README.md` and recorded its evidence, publication, and validation constraints in `Context.md` and `Progress.md`.
- Recorded postmortem publication-readiness and licensing decisions in the private archive and public decision register.
- Recorded the contribution-modes and government security assessment in the public materials list.
- Linked the new tracking files from `README.md`.
- Linked the Challenge 2 benchmark into the wiki index and documented the evaluation harness in the Challenge 2 brief and README.

## 2026-04-16

### Added

- Added the Challenge 2 Obsidian knowledge base under `challenge-2/wiki/`.
- Added `challenge-2/tools/build_wiki.py` to generate source notes, topic pages, entity pages, maps of content, table exports, source register data, architecture documentation, and lint output.
- Added Challenge 2 Obsidian vault configuration under `challenge-2/.obsidian/`.
- Added `challenge-2/AGENTS.md` with operating rules for the generated LLM Wiki.
- Added `challenge-2/wiki/architecture.md` with Mermaid diagrams and a glossary explaining the knowledge-base architecture.
- Added GitHub Copilot custom instructions for Challenge 2 synthetic fixture data.

### Changed

- Treated `challenge-2/` as the Obsidian vault root so raw source files, generated notes, and links live together.
- Preserved synthetic staff-directory fixture data while marking it as synthetic and not real personal data.
- Generated source notes for all 43 Challenge 2 documents.

### Fixed

- Fixed malformed generated Markdown links caused by rewriting document IDs inside existing links.
- Fixed `/guidance/DOC-*` pseudo-links by rewriting them to relative source-note links.
- Removed ExifTool local-environment fields from generated raw metadata and source-register output.
- Fixed Social Fund version extraction to capture `March 2018`.
- Added a corrected HMT Green Book link while preserving the raw extracted PDF text.
- Fixed singular wording for topic pages with exactly one source document.

### Validation

- Verified the Challenge 2 strict build: `43 sources, 81 notes, 0 lint issues`.
- Resolved all fork-local PR review threads for the Challenge 2 work.
