# Changelog

All notable changes to this repository are tracked here.

This file follows the spirit of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/): dated entries, human-readable summaries, and clear categories for additions, changes, fixes, removals, security notes, and documentation updates.

## Unreleased

### Added

- 2026-05-12: Added nine section-level HMRC narrative notes that decompose the 9 May 2026 AI Coding Assistants briefing into executive summary, market map, productivity evidence, failure modes, public-sector controls, repo case study, talk track, Q&A prep, and source-register/validation-limit pages.
- 2026-05-12: Added `research/hmrc-beyond-hype/tools/lint_narrative_semantics.py` and generated semantic lint reports for stale-claim detection, documented-count contradiction checks, required concept/page coverage, and live external-link revalidation.
- 2026-05-11: Added a generated HMRC talk narrative scaffold under `research/hmrc-beyond-hype/narrative/`, including an entry point, overview, narrative arc, topic index, source-material register, ClawPilot sidebar note, coverage reports, validation reports, and 73 visual sidecars with 73 small derived image assets for the current imported PPTX/PDF/PNG inventory.
- 2026-05-11: Added a generated HMRC talk import inventory and non-visual source notes so all 13 current files in `research/hmrc-beyond-hype/import/` have an explicit narrative treatment, including the AI Coding Assistants Markdown/DOCX briefing pair and the two imported audio sources.
- 2026-05-11: Added `research/hmrc-beyond-hype/tools/build_narrative_sidecars.py` and `research/hmrc-beyond-hype/tools/validate_narrative_sidecars.py` to make the HMRC visual sidecar pack reproducible and validate coverage, local links, orphaned narrative Markdown, sidecar metadata, asset references, and raw-import staging.
- 2026-05-11: Added `research/hmrc-beyond-hype/tools/build_narrative_seelinks_pack.py` and the generated HMRC narrative SeeLinks datapack under `research/hmrc-beyond-hype/narrative/seelinks/`, now covering 234 cards, 10 facets, 9 collections, 285 graph nodes, and 2984 graph edges.
- 2026-05-11: Added `research/hmrc-beyond-hype/tools/build_seelinks_ui_infographics.py`, four generated SVG infographics, and `research/hmrc-beyond-hype/narrative/notes/seelinks-web-ui-reference.md` to document the original SeeLinks web UI as the target interaction model for the HMRC workbench UI pass.
- 2026-05-11: Added `research/hmrc-beyond-hype/import/clawpilot.md` as a lightweight imported source brief for the ClawPilot / OpenClaw sidebar in the HMRC talk narrative.
- 2026-05-11: Added `research/hmrc-beyond-hype/narrative/README.md` as the durable active goal brief for a GitHub-browsable HMRC talk narrative wiki, including source inputs, expected structure, slide/image sidecar requirements, tags, definition of done, and verification plan.
- 2026-05-11: Added HMRC talk import-resource handling under `research/hmrc-beyond-hype/`, including an import review appendix, lightweight imported Markdown source tracking, local audio transcription tooling, pyannote diarization tooling, base transcripts, SRT files, diarization evidence, and `Trace` / `Query` speaker-attributed transcript drafts for the two imported prep-audio files.
- 2026-05-09: Added `research/hmrc-beyond-hype/`, a complete HMRC Beyond the Hype talk research pack covering the research brief, source register, AI software-engineering timeline, empirical productivity evidence, agentic capability analysis, public-sector governance, Codex build case study, operating model, and appendices required by the local prompt kit.
- 2026-05-09: Added line-level GitHub permalinks after repo-local evidence paths in the HMRC talk source register, case study, operating model, and claims matrix where practical, pinned to the clean talk-prep branch commit for line stability.
- 2026-04-29: Added a Dark Data Workbench source-note Markdown endpoint so reader note links resolve under the local dev/static app.
- 2026-04-29: Added `challenge-2/workbench/pnpm-workspace.yaml` to record the approved pnpm build dependency for `esbuild`.
- 2026-04-21: Added `START-HERE.md`, a public reader guide with LinkedIn, event, time-based, and persona-based routes through the repository.
- 2026-04-21: Expanded `output/doc/linkedin-version-1-1-announcement.md` with copy-ready main LinkedIn post text and a shorter comment for other event posts.
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
- Added per-client model/version manifests to Challenge 2 evaluation runs, including selected model source, reasoning effort where supported, model-reference URL/date, executable paths, version-command outputs, repo state, benchmark hash, and detected macOS Copilot desktop app versions.
- Added full-coverage Challenge 2 evaluation support for GitHub Copilot CLI and Microsoft Copilot UI runs, including a caveated Playwright adapter for Microsoft 365 Copilot Chat.
- Added a `full` client alias for running Codex, Gemini CLI, Claude Code, GitHub Copilot CLI, and Microsoft Copilot together.
- Added a distinct `policy_blocked` status for GitHub Copilot CLI live runs denied by organisation, subscription, or policy controls.
- Added optional Microsoft Copilot UI GPT mode selection so the Playwright adapter can attempt to select a visible mode such as `Think Deeper` before submitting benchmark prompts.
- Added per-client environment overrides in the evaluation config so Claude Code can run with `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` for DSIT managed gateway compatibility.
- Added a Microsoft Copilot prompt-source mode that replaces inaccessible local wiki paths with public GitHub permalinks plus copied source excerpts for deterministic UI-client grounding.
- Added `challenge-2/MCP-Wiki/`, a separate MCP research wiki with the Deep Research report in Markdown/DOCX/PDF, source and candidate registers, security model, implementation plan, and license-aware reference/specification policy for a purpose-built Wiki MCP server.
- Added `challenge-2/MCP-Wiki/sources/bibliography.md` and `data/bibliography.json` to resolve Deep Research citation markers into durable source IDs, URLs, license posture, and local treatment.
- Added a citation-clean linked derivative of the MCP Deep Research report for AI and human navigation while preserving the raw report unchanged as evidence.
- Added `challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py`, plus generated Markdown and JSON lint reports for frontmatter, tags, source paths, duplicate IDs, internal links, and citation-marker leakage checks.
- Added `challenge-2/MCP-Wiki/wiki-optimization-log.md` to record wiki navigation, metadata, and lint decisions as part of the MCP research evidence.
- Added `challenge-2/MCP-Wiki/authentication-options.md` to evaluate Copilot Studio-facing Streamable HTTP authentication options and record OAuth 2.0 / Microsoft Entra ID as the target production pattern.
- Added `challenge-2/MCP-Wiki/semantic-retrieval-options.md` to evaluate v1 embedding models and vector-index choices against licensing, provenance, reproducibility, and government-fit criteria.
- Added first-use MCP reference implementation submodules under `challenge-2/MCP-Wiki/references/external/` for ProfessionalWiki, olgasafonova, qmd, and mkdocs-mcp-plugin, each with local `SOURCE.md` metadata.
- Added `challenge-2/tools/wiki_eval_mcp.py`, a stdio MCP-compatible audit layer for controlled wiki search/read, answer recording, and DSAP-shaped audit pack finalisation.
- Added `challenge-2/tools/summarise_wiki_eval.py` to turn completed scoring sheets into leaderboard JSON and Markdown.
- Added `challenge-2/MCP-Wiki/implementation/wiki_mcp/`, a read-only Challenge 2 Wiki MCP server with stdio and local HTTP transports, source allowlists, benchmark denylists, source-register tools, context-pack tools, provenance explanations, deterministic semantic retrieval, and append-only audit logging.
- Added `challenge-2/tools/wiki_mcp_server.py` as the CLI entry point for the Challenge 2 Wiki MCP server.
- Added `codex-mcp` as a Challenge 2 evaluation client that configures Codex with the local Wiki MCP server and records live MCP tool-call evidence.
- Added `challenge-2/tools/compare_wiki_eval.py` to generate reproducible comparison reports from DSAP evaluation runs.
- Added `challenge-2/evaluation/reports/validated-full-20260419T2225Z-comparison.md` and matching sanitized metrics JSON for the full Challenge 2 wiki evaluation report.
- Added `challenge-2/MCP-Wiki/sources/codex-thread-mcp-implementation-evaluation.md`, a publication-safe capture and recommendation note for the Codex thread that drove the MCP implementation and evaluation work.
- Added public-safe rubric score artifacts for the validated full run: per-question scores, a Markdown leaderboard, and a JSON leaderboard, without committing raw answer text.

### Changed

- 2026-05-12: Cross-linked the AI Coding Assistants section notes from the narrative entry point, overview, narrative arc, source-material register, topic index, Q&A prep route, and SeeLinks datapack so the briefing is navigable by section instead of only through one long source note.
- 2026-05-12: Promoted SeeLinks, ClawPilot, transcripts, and semantic lint outputs into the HMRC narrative topic/index routes so generated report pages and evidence sidebars are discoverable from the wiki entry point.
- 2026-05-11: Updated the HMRC narrative goal status from planned to sidecar milestone complete, while keeping full narrative curation open.
- 2026-05-11: Extended Dark Data Workbench so `/?pack=hmrc-narrative` loads the HMRC talk narrative datapack with slide-thumbnail cards, narrative/repo/transcript/conversation evidence, source-note links, bounded facets, keep/dismiss marked-card controls, and drag-facet-to-grid card colouring.
- 2026-05-11: Curated `AI-Native_Engineering_Blueprint.pptx` into a 15-slide narrative route with slide-by-slide talk paths, while clarifying that the broader AI-native import material is covered separately through the PDF, workflow image, and AI Coding Assistants briefing.
- 2026-05-11: Renamed the HMRC talk pyannote diarization labels from generic speaker numbers to the AI voice names `Trace` and `Query`, while preserving the base Whisper transcript text and SRT outputs.
- 2026-04-22: Updated `.gitignore` to ignore all `.obsidian/` directories as local Obsidian browsing state.
- Updated Challenge 2 evaluation best-model policy to use `gpt-5.4` with `xhigh` effort for Codex, Gemini CLI Auto routing, Claude Code `best` with `max` effort, staff-confirmed `gpt-5.4` for GitHub Copilot CLI, and Microsoft 365 Copilot Chat GPT-5 automatic routing for Microsoft Copilot.
- Allowed client config to suppress a default reasoning-effort argument with JSON `null`, enabling Claude Code runs that defer model and effort selection to DSIT-managed local Claude settings.
- Updated the Microsoft Copilot example config to prefer `Think Deeper`, cite the public `v1.1` GitHub wiki, and inject key wiki excerpts because the Microsoft web UI cannot read local repository paths.
- Expanded the MCP research wiki frontmatter, search terms, related-link properties, and cross-links so the wiki can be navigated and linted as an AI-usable knowledge base.
- Resolved MCP research wiki open decisions for authentication, first-use submodules, semantic retrieval in v1, and release-time external URL validation.
- Updated the MCP implementation plan so semantic retrieval is included in v1 behind deterministic provenance and context-pack contracts.
- Recorded Copilot Studio direct MCP connection as the first Microsoft validation path, with Agents Toolkit or custom connector routes reserved for gaps in direct delivery.
- Excluded API-key authentication from v1 unless live Copilot Studio validation proves a host-specific need.
- Added a provisional semantic retrieval baseline: local `BAAI/bge-small-en-v1.5` embeddings with exact NumPy cosine search, compared against `all-MiniLM-L6-v2` and `e5-small-v2` before final lock.
- Updated the Claude example config to defer model and effort selection to DSIT-managed local settings while keeping `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.
- Recorded Codex stdio MCP as the tightest local validation loop and kept Copilot Studio direct MCP validation as the first Microsoft-host path.
- Kept the production embedding lock open while using deterministic local exact-cosine hashing for server contract tests and live MCP validation on the disk-constrained machine.
- Classified Gemini CLI quota exhaustion separately from generic client failures and taught the comparison report to apply explicit correction runs without committing raw prompts or answer transcripts.
- Updated the comparison report generator to accept a rubric score CSV and include a quality leaderboard alongside operational proxy metrics.

### Fixed

- 2026-05-11: Added a repository Ruff configuration and VS Code Ruff setting so the workspace stops parsing nested external reference `pyproject.toml` files that contain unsupported Ruff rule selectors such as `W503`.
- 2026-04-29: Fixed Dark Data Workbench Browser AI/MCP context exports so selected sources remain in the exported context even when current filters or search terms hide them.
- 2026-04-29: Fixed Dark Data Workbench reader `Open note` links that previously resolved to missing `/wiki/...` paths in the app.
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
- Ignored nested `.DS_Store` and AppleDouble metadata files throughout the repository.
- Removed the previously tracked `challenge-2/.DS_Store` local Finder state file.
- Changed the MCP wiki lint report to record the repository-relative wiki root instead of a local absolute path.
- Fixed UTF-8 byte-budget enforcement for Wiki MCP context packs and Workbench MCP source-note reads so non-ASCII text cannot exceed requested byte caps.
- Fixed Wiki MCP HTTP notification handling so JSON-RPC notifications return `204 No Content` instead of an invalid empty JSON object response.
- Hardened Wiki MCP, Workbench MCP, and evaluation MCP JSON-RPC handlers so non-object requests and malformed `params` envelopes return protocol errors instead of terminating stdio or HTTP sessions.
- Made Challenge 2 evaluation repo-state metadata tolerate a missing `git` executable, and changed repository maintenance helpers to report missing Git with clear failures instead of raw tracebacks.
- Fixed the `codex-mcp` invocation so spawned Wiki MCP server arguments use the same configured semantic model as the prompt context-pack seed, preventing recorded config from diverging from live MCP tool-call behavior.
- Fixed evaluation reruns so stale assistant-response artifacts are removed before live client invocation and cannot contaminate failed-run audit evidence.
- Fixed Workbench MCP `workbench://source-register` reads so they use the configured challenge root instead of the repository default root.
- Fixed comparison-report MCP audit parsing so malformed or truncated JSONL lines are skipped and counted instead of aborting metrics generation.
- Fixed Wiki MCP HTTP startup so a configured `--bearer-token-env` must resolve to a non-empty environment variable instead of silently starting without bearer-token checks.
- Broadened comparison metrics sanitisation and refreshed the committed metrics JSON so arbitrary local executable paths, app paths, and home-relative paths are replaced before publication.
- Fixed Wiki MCP search mode selection so lexical-only searches do not build/query the semantic index and semantic-only searches do not run lexical scoring.

### Security

- Avoided recording default local Microsoft Copilot Playwright profile paths in generated UI-adapter metadata; runs now record the profile source instead.

### Documentation

- 2026-05-11: Linked the HMRC talk narrative wiki entry point from the repository README and research brief, and recorded the sidecar coverage status in the narrative goal brief.
- 2026-05-11: Documented the HMRC narrative SeeLinks datapack, workbench load path, facet set, card controls, and validation state across the narrative README, workbench README, Context, and Progress.
- 2026-05-11: Linked the original SeeLinks UI reference and infographics from the HMRC narrative entry point, overview, narrative arc, source-material register, README, Context, and Progress.
- 2026-05-11: Linked the HMRC talk import inventory, AI Coding Assistants market briefing note, audio source notes, and AI-Native deck guide from the narrative entry points, topic index, source-material register, README, research brief, Context, and Progress.
- 2026-05-11: Documented the HMRC talk import drop, transcript caveats, raw-media publication policy, transcript reproduction commands, and current validation state across the research brief, import review appendix, README, Context, and Progress.
- 2026-05-09: Linked the HMRC Beyond the Hype research pack from `README.md` and recorded its purpose, evidence boundaries, and important paths in `Context.md` and `Progress.md`.
- 2026-04-21: Linked the new public reader guide from `README.md` and recorded it in the repository map and tracking docs.
- Recast `README.md` from the original event-invitation framing into a fork-specific Challenge 2 implementation overview with the value proposition, start points, repository map, validation summary, and original hackathon context.
- Added Team DSIT A attribution to the README, delivery report, security assessment, LinkedIn draft, and public postmortem generation.
- Linked the Challenge 2 demonstration guide from the wiki index, README, and Challenge 2 brief.
- Linked the public Codex collaboration postmortem from `README.md` and recorded its evidence, publication, and validation constraints in `Context.md` and `Progress.md`.
- Recorded postmortem publication-readiness and licensing decisions in the private archive and public decision register.
- Recorded the contribution-modes and government security assessment in the public materials list.
- Linked the new tracking files from `README.md`.
- Linked the Challenge 2 benchmark into the wiki index and documented the evaluation harness in the Challenge 2 brief and README.
- Recorded the MCP wiki citation-linking and optimization decisions in the MCP decision record and source register.
- Linked the MCP implementation/evaluation thread capture from the MCP wiki index, implementation workspace, decision record, optimization log, and source register.
- Documented the committed rubric-scored leaderboard and the rule that raw scoring sheets with answer text stay outside Git.

### Validation

- 2026-05-12: Verified the updated HMRC narrative section-note and semantic-lint route with the reproducible sidecar builder, SeeLinks datapack builder, narrative validator (`73` imported visual items, `109` reachable narrative Markdown files, `77` referenced assets, `0` orphaned narrative Markdown files), semantic lint (`0` errors, `0` warnings, `5` live external links OK), tool py_compile, and whitespace checks.
- 2026-05-11: Verified the HMRC talk narrative sidecar pack with the reproducible builder and validator: `73` imported visual items covered, `90` reachable narrative Markdown files, `73` referenced assets, `0` orphaned narrative Markdown files, and no validation errors.
- 2026-05-11: Verified the expanded HMRC talk narrative import pack with all `13` current import files represented, `73` imported visual items covered, `95` reachable narrative Markdown files, `73` referenced assets, `0` orphaned narrative Markdown files, and no validation errors.
- 2026-05-11: Verified the HMRC narrative SeeLinks datapack, original SeeLinks UI infographics, and workbench integration with the datapack/infographic builders, narrative validator (`99` reachable narrative Markdown files, `77` assets), tool py_compile, Ruff, Svelte typecheck, unit tests, production build, Playwright UI tests, documentation lockstep, and whitespace checks.
- 2026-05-11: Verified the HMRC talk audio workflow with `whisper-cli` transcript/SRT generation, pyannote diarization on `mps` for `40.0` minutes of audio in `83.8` seconds, py_compile for the transcript tools, workspace Ruff file-set validation, and documentation lockstep updates.
- 2026-05-09: Verified the HMRC Beyond the Hype talk research pack has all `12` master-prompt deliverables, a parseable `50`-row source register, no stale repo-local pseudo-links or transcript processing remnants, `69` valid repo-local GitHub blob links, passing documentation lockstep, and clean `git diff --check`.
- Verified the MCP research wiki lint: `22` Markdown files, `222` internal links, `67` external links, complete search-term coverage, `0` errors, and `0` warnings.
- Verified all `31` MCP bibliography URLs returned HTTP success responses and replaced stale Microsoft/NCSC citation targets with current URLs.
- Verified the MCP research wiki lint after submodule metadata: `27` Markdown files, `270` internal links, `75` external links, complete search-term coverage, `0` errors, and `0` warnings.
- Verified the MCP research wiki lint after semantic retrieval options: `28` Markdown files, `286` internal links, `85` external links, complete search-term coverage, `0` errors, and `0` warnings.
- Verified the final MCP research wiki lint after implementation/report updates: `28` Markdown files, `287` internal links, `85` external links, complete search-term coverage, `0` errors, and `0` warnings.
- Verified the MCP research wiki lint after adding the Codex thread capture: `29` Markdown files, `311` internal links, `85` external links, complete search-term coverage, `0` errors, and `0` warnings.
- Verified PR review hardening for malformed JSON-RPC request handling and missing-Git metadata with targeted unit tests, py_compile, MCP wiki lint, documentation lockstep, and whitespace checks.
- Verified the `codex-mcp` server-argument reproducibility fix with targeted client-invocation tests, py_compile, MCP wiki lint, documentation lockstep, and whitespace checks.
- Verified stale-output cleanup, configured-root Workbench resources, and malformed MCP audit-line tolerance with targeted regression tests, py_compile, MCP wiki lint, documentation lockstep, and whitespace checks.
- Verified the Challenge 2 Wiki MCP server with unit and transport tests at `91%` package coverage using `uv run --with coverage`.
- Verified live `Q001` smoke tests for `codex`, `codex-mcp`, `gemini`, `claude`, and `microsoft-copilot`; `github-copilot` remains `policy_blocked`.
- Completed a 100-question benchmark run for `codex,codex-mcp,gemini,claude,microsoft-copilot`, writing raw audit evidence outside the repository under an external run directory and sealing DSAP audit pack `DSAP-validated-full-20260419T2225Z`.
- Completed a correction run for the single `codex-mcp` timeout on `Q057`, giving Codex with MCP effective completed coverage for all `100` benchmark questions.
- Recorded that Gemini CLI completed `36` questions before `gemini-3.1-pro-preview` quota exhaustion blocked the remaining `64` questions; the report keeps those rows as `quota_exhausted`.
- Generated the comparison report showing `100/100` completed answers for Codex, Codex with MCP, Claude, and Microsoft Copilot; GitHub Copilot CLI remains represented by a `policy_blocked` smoke run.
- Generated the rubric-scored leaderboard from the effective full run: Codex `484/500`, Claude `480/500`, Codex with MCP `471/500`, Gemini `171/500`, and Microsoft Copilot `58/500`.
- Verified the rubric score CSV contains `500` unique client/question score rows with no raw answer or gold-answer columns, and no local path or UI-session metadata hits in the committed report artifacts.
- Verified `python3 -m unittest tests.test_challenge2_compare_wiki_eval` after adding rubric-score report support.
- Verified the broader MCP evaluation test set with `python3 -m unittest tests.test_challenge2_eval_clients tests.test_challenge2_compare_wiki_eval tests.test_challenge2_wiki_mcp_server`.
- Verified the PR review fixes with `python3 -m unittest tests.test_challenge2_wiki_mcp_server tests.test_challenge2_workbench_mcp`, covering non-ASCII byte caps and HTTP notification no-response behavior.
- Verified the MCP wiki lint after updating the thread capture for PR review status: `29` Markdown files, `311` internal links, `85` external links, complete search-term coverage, `0` errors, and `0` warnings.

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
