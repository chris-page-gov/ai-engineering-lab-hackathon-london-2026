# Progress

## Current Status

The Challenge 2 Obsidian knowledge-base prototype is implemented and merged into the fork's `main` branch via fork-local PR #1.

The current local working branch also contains the Challenge 2 wiki evaluation benchmark, CLI harness, MCP-compatible audit layer, and scoring-sheet/leaderboard tooling for comparing Codex, Gemini CLI, and Claude Code against the generated wiki.

The current local working branch now also includes an end-to-end Challenge 2 demonstration guide that links the source corpus, Obsidian validation, SeeLinks-style workbench, Browser AI export, evaluation matrix/harness, and audit/FOI tracking into one walkthrough.

Dark Data Workbench now includes a question box so saved checks and Browser AI exports preserve the user question alongside the selected evidence.

The current local working branch also includes a linked and illustrated colleague report in Markdown and Word format that reconstructs the Challenge 2 realtime delivery sequence from the supplied hackathon write-up, repo history, logs, and Codex thread evidence.

Version 1.1 has been published from `main` and tagged as `v1.1`. The current local branch is `codex/wiki-mcp-research`, which extends the Challenge 2 evaluation harness with a purpose-built Wiki MCP server and a full comparison report for standard Codex versus Codex using MCP.

The current MCP research branch adds a separate `challenge-2/MCP-Wiki/` research wiki and now includes the implemented read-only Wiki MCP server. It preserves the Deep Research report variants, candidate and source registers, licensing posture, security model, implementation trace, and evaluation evidence without polluting the Challenge 2 corpus wiki or the public postmortem wiki.

The current MCP implementation and evaluation thread is now captured as a publication-safe summary note in the MCP research wiki. The branch recommendation is to include that summary in the current MCP pull request, while leaving any raw transcript or full public postmortem regeneration to the separate postmortem workflow.

The full Challenge 2 wiki evaluation report now lives at `challenge-2/evaluation/reports/validated-full-20260419T2225Z-comparison.md`, with sanitized metrics in the adjacent JSON file and a rubric-scored leaderboard in `challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-leaderboard.md`. Raw prompts, answers, audit bundles, screenshots, and UI captures remain outside Git in external run directories.

The postmortem release includes a private generated Codex collaboration postmortem archive under ignored `postmortem/` and a GitHub-safe public derivative under `postmortem-public/`. The publication line now treats the public derivative and reports as part of the Version 1.1 baseline, with the full 100-question AI comparison still outstanding.

The postmortem artifacts have been reviewed for publication readiness. The review found no obvious credential-shaped secrets or email-address pattern hits in the postmortem scan, but it blocks public release until local paths, local assistant configuration references, copied third-party source bodies, private workflow references, and local-only evidence are redacted or repackaged. A follow-up license check found no explicit redistribution license in the localized Karpathy X/gist copies, so public releases should use citation metadata and short excerpts unless permission or an explicit license is obtained.

The attached contribution-modes proposal has been converted to Markdown under `output/doc/`, and a government-security assessment has been added. The assessment concludes that Codex was strongest for Explorer, Builder, Refiner, and Verifier work; useful with human steering for Framer, Architect, and Experience Shaper work; assistant-only for Security Steward work; and not suitable as an autonomous Operator for production government services.

`README.md` now presents this fork as Team DSIT A's Challenge 2 dark-data implementation and evidence pack, rather than as the original one-day event invitation.

`START-HERE.md` now provides a public reader guide for LinkedIn and event traffic, with short routes by available time and by reader type while keeping the repository root as the canonical shared URL.

`output/doc/linkedin-version-1-1-announcement.md` now contains copy-ready LinkedIn publication text plus a shorter comment suitable for replying on other event posts.

`.gitignore` now ignores all `.obsidian/` directories so local Obsidian browsing state does not appear as untracked repo content.

The current local branch is `codex/workbench-review`, focused on Dark Data Workbench review and fixes. Initial validation found the existing typecheck, unit/component suite, production build, and Playwright UI suite passing before changes.

The current local branch now also includes `research/hmrc-beyond-hype/`, a complete talk-preparation research pack for an HMRC Beyond the Hype session on moving from coding assistants to coding agents. The pack covers the research brief, source register, timeline, productivity evidence, agentic capability analysis, public-sector governance, repo case study, operating model, and appendices required by `research/hmrc-beyond-hype-prompt-kit/prompts/00_master_prompt.md`.

The current local branch is `codex/hmrc-talk-transcripts`, continuing the HMRC talk preparation work. It adds a local import-resource review, tracks the lightweight imported Markdown briefing, keeps large raw media ignored by default, fixes the VS Code Ruff workspace configuration, and commits machine transcripts plus pyannote `Trace` / `Query` diarization drafts for the two imported prep-audio files. The latest update keeps the transcript words and timings unchanged while replacing only the generic diarization labels with AI voice names.

The current local branch is `codex/hmrc-narrative-navigation`, building the HMRC talk narrative wiki and SeeLinks-style workbench datapack from the research pack, imported material, transcripts, Challenge 2 evidence, relevant conversation traces, and original SeeLinks UI reference material. The import and visual sidecar milestone is complete for the 13-file import inventory present at sidecar-generation time, and the visual subset has 50 PowerPoint slide sidecars, 20 PDF page sidecars, and 3 standalone PNG sidecars with small derived image assets, topic/source navigation, coverage output, validation output, a 234-item workbench datapack, and four SeeLinks UI infographics. The 9 May 2026 AI Coding Assistants briefing is now split into section-level notes and linked from the talk arc, topic index, Q&A prep route, and datapack. Full editorial curation of the broader narrative remains open.

The current HMRC narrative pull request now includes a Dark Data Workbench UI fix: pack-switch links refresh the loaded corpus without a manual browser reload, and reader cards default to rendered Markdown preview while retaining raw Text view access.

The current HMRC demo publication pass explicitly includes `research/hmrc-beyond-hype/import/beyond_hype_coding_assistants_public_sector_engineering.pptx` as the selected presentation deck for the 2026-05-12 release, linked from the repository README and HMRC narrative entry points as a deliberate exception to the default raw-import ignore policy.

The current workbench parity pass brings the visible SeeLinks/Micropedia web controls into `challenge-2/workbench` against the HMRC narrative and Challenge 2 packs. The parity matrix is `research/hmrc-beyond-hype/narrative/notes/seelinks-micropedia-parity-matrix.md`; it records implemented controls, local/configuration-only external-service surfaces, and regression coverage. The latest fix restores the intended facet accordion behaviour: facets default folded, inactive unpinned facets close when another opens, active selected/highlighted facets remain visible, pinned facets remain visible, and double-click value reduction keeps the chosen value active.

## Completed

- Built a repeatable Challenge 2 wiki generator.
- Generated source notes for all 43 Challenge 2 documents.
- Generated topic pages, entity pages, maps of content, architecture notes, source-register JSON, workbook exports, and lint reports.
- Preserved raw Challenge 2 sources as immutable source material.
- Added synthetic fixture metadata for staff-directory content without redacting the synthetic data.
- Fixed generated link integrity issues and removed local filesystem path leakage from generated metadata.
- Merged the fork-local Challenge 2 PR into the fork's `main` branch.
- Resolved all fork-local PR review threads.
- Fixed the architecture Mermaid diagram labels that Obsidian rendered as unsupported Markdown lists.
- Added repo-wide tracking files and a documentation lockstep check for local and pull-request validation.
- Fixed review feedback on the documentation lockstep check so deleted tracking files cannot pass as updated files.
- Added the 100-question Challenge 2 wiki evaluation benchmark and linked it from the wiki index.
- Added a CLI evaluation harness that builds wiki-only prompts, captures client outputs, and emits DSAP-shaped audit packs.
- Added a stdio MCP-compatible layer for audited Challenge 2 wiki search/read, public question retrieval, answer recording, and run finalisation.
- Added scoring-sheet and leaderboard tooling for competitive evaluation once per-answer scores are entered.
- Added Dark Data Workbench under `challenge-2/workbench/` with source filtering, context-set building, source reader, graph/table/check views, browser-AI context export, and MCP setup guidance.
- Added `challenge-2/tools/workbench_mcp.py` for local MCP source search/read/context export.
- Added Dark Data Workbench unit, component, Playwright, MCP, and optional coverage test paths.
- Hardened Dark Data Workbench Playwright control interactions after the PR check exposed CI-only click/state flakiness.
- Removed Obsidian workspace session state from Git tracking while preserving useful vault configuration files.
- Added `challenge-2/wiki/demonstration-guide.md` and linked it from the wiki index, README, and Challenge 2 brief.
- Added the Dark Data Workbench question box and included question text in Browser AI JSON, copied prompts, Markdown evidence bundles, and saved-check setup.
- Added `output/doc/challenge-2-realtime-delivery-report.md` and `output/doc/challenge-2-realtime-delivery-report.docx`.
- Added `tools/build_codex_postmortem.py` and generated the Codex collaboration postmortem source archive/wiki under `postmortem/`.
- Added `postmortem/publication-readiness-report.md` with required redaction and packaging changes before public postmortem release.
- Added localized-source licensing findings to the publication-readiness report.
- Added `postmortem-public/` as the GitHub-safe postmortem replacement, with redacted exchange notes, conversation summaries, citation-only external source notes, public repository evidence links, decision registers, and publication lint output.
- Added `.gitignore` coverage for the private `postmortem/` archive so the public derivative is the only postmortem folder intended for GitHub.
- Created the local `v1-challenge-2` tag at commit `326a82a8f17440d49471dab6a11d2b725b879359` before starting postmortem work on `codex/postmortem-wiki`.
- Converted the attached `Contribution Modes Proposal.docx` to `output/doc/contribution-modes-proposal.md` with extracted media.
- Added `output/doc/codex-contribution-modes-security-assessment.md` with contribution-mode analysis, Codex suitability conclusions, and security findings against government Secure by Design and secure-development expectations.
- Recast `README.md` around the Challenge 2 implementation, value proposition, start points, repository map, validation summary, and original hackathon context.
- Added Team DSIT A attribution across the README, delivery report, security assessment, public postmortem generation, and LinkedIn announcement draft.
- Replaced non-GitHub-renderable contribution-modes EMF references with SVG diagram assets.
- Added `output/doc/linkedin-version-1-1-announcement.md` for public Version 1.1 announcement copy.
- Addressed PR review comments by fixing whole-word contribution classification, single-pass Jina Reader source URLs, and public sanitisation for bare local path markers.
- Added `tests/test_build_codex_postmortem.py` to guard postmortem contribution inference and public sanitisation regressions.
- Added the HMRC Beyond the Hype talk research pack under `research/hmrc-beyond-hype/`, including all Stage 1-8 outputs and appendices from the prompt kit.
- Added line-level GitHub permalinks after repo-local paths in the source register, repo case study, operating model, and claims matrix where practical.
- Added the HMRC talk import resource review, raw-media ignore policy, lightweight imported Markdown source input, audio transcription tooling, pyannote diarization tooling, base transcripts, SRT files, diarization CSV/report, and `Trace` / `Query` speaker-attributed transcript drafts.
- Renamed the generated HMRC talk diarization labels to `Trace` and `Query` across speaker-attributed transcript files, diarization metadata, reports, and reproduction tooling without editing the base Whisper transcripts or SRT timings.
- Added `research/hmrc-beyond-hype/narrative/README.md` as the durable active goal brief for the planned HMRC talk narrative wiki, replacing the unavailable `/goal` slash-command workflow with a committed definition of done and verification plan.
- Added `research/hmrc-beyond-hype/import/clawpilot.md` as a lightweight local source input for the ClawPilot / OpenClaw sidebar and incorporated it into the HMRC narrative pack.
- Added the HMRC narrative scaffold under `research/hmrc-beyond-hype/narrative/`, including `index.md`, `overview.md`, `narrative-arc.md`, `topics.md`, `source-materials.md`, `notes/clawpilot-project-lobster.md`, sidecar indexes, visual coverage data, and validation reports.
- Added generated Markdown sidecars and small derived image assets for all `73` current imported visual items: `15` slides from `AI-Native_Engineering_Blueprint.pptx`, `10` slides from `Challenge_2_Unlocking_Dark_Data.pptx`, `13` slides from `Dark_Data_Blueprint.pptx`, `12` slides from `Governing_AI_Engineering.pptx`, `20` pages from `AI-Native-Engineering-Team-source_openAI.pdf`, and `3` standalone PNG files.
- Added `research/hmrc-beyond-hype/narrative/notes/import-inventory.md` and `data/import_inventory.csv`, proving every current file in `research/hmrc-beyond-hype/import/` has an explicit narrative treatment.
- Added `research/hmrc-beyond-hype/narrative/notes/ai-coding-assistants-market-briefing.md` for the imported AI Coding Assistants Markdown/DOCX briefing pair, with links to the companion evolution and benchmark visuals.
- Added transcript-backed narrative source notes for the two imported audio files under `research/hmrc-beyond-hype/narrative/notes/`.
- Curated `research/hmrc-beyond-hype/narrative/slides/ai-native-engineering-blueprint/narrative-guide.md` as the preferred route through the 15-slide AI-Native Engineering Blueprint deck.
- Added `research/hmrc-beyond-hype/tools/build_narrative_sidecars.py` and `research/hmrc-beyond-hype/tools/validate_narrative_sidecars.py` so the sidecar pack can be regenerated and checked.
- Added `research/hmrc-beyond-hype/tools/build_narrative_seelinks_pack.py` and generated `research/hmrc-beyond-hype/narrative/seelinks/pack.json` for browsing the HMRC talk narrative through Dark Data Workbench.
- Extended Dark Data Workbench so `/?pack=hmrc-narrative` loads the HMRC narrative pack with slide thumbnails, source-note links, bounded facets, keep/dismiss marked cards, restore, graph data, and drag-facet-to-grid colouring.
- Fixed Dark Data Workbench pack-switch route handling so Challenge 2 and HMRC narrative buttons update route data and reset corpus-scoped UI state without a manual reload.
- Added a reader Markdown preview/Text toggle so source notes are readable as rendered Markdown by default while preserving exact raw note text.
- Added the selected HMRC Beyond the Hype presentation deck `research/hmrc-beyond-hype/import/beyond_hype_coding_assistants_public_sector_engineering.pptx` to the demo publication set and linked it from the README, research brief, narrative index, source-material register, import inventory, and narrative goal brief.
- Added `research/hmrc-beyond-hype/tools/build_seelinks_ui_infographics.py`, four generated SVG infographics, and `research/hmrc-beyond-hype/narrative/notes/seelinks-web-ui-reference.md` to document the original SeeLinks web UI before the HMRC workbench UI alignment pass.
- Added `research/hmrc-beyond-hype/narrative/notes/seelinks-micropedia-parity-matrix.md` and implemented the Dark Data Workbench SeeLinks/Micropedia parity pass: dynamic facets, metadata toggle, order-by stack, facet/value ordering, link summaries, Dexie-backed collections, print/export/tile-text/edit panels, grid/outline/graph/timeline/reading/table/checks views, rollups, history reductions, and docked detail.
- Split `research/hmrc-beyond-hype/import/AI coding assistants on 9 May 2026 for the HMRC Data Science Academy talk.md` into nine generated section-level narrative notes covering the executive summary, market map, productivity evidence, failure modes, public-sector controls, repo case study, talk track, Q&A prep, and source-register limitations.
- Added repository-level Ruff configuration and VS Code settings so the workspace Ruff extension uses the repo config instead of parsing nested external reference `pyproject.toml` files.
- Published Version 1.1 from `main` with a GitHub tag and release.
- Created `codex/evaluation-versioning` from the clean `v1.1` baseline for the next evaluation run.
- Added Challenge 2 evaluation model/version capture for Codex, Gemini CLI, Claude Code, GitHub Copilot CLI, Microsoft Copilot UI runs, and detected Microsoft Copilot desktop apps.
- Added staff-confirmed `gpt-5.4` selection for GitHub Copilot CLI after contradictory public model guidance was identified.
- Added distinct `policy_blocked` classification for GitHub Copilot CLI live requests denied by organisation, subscription, or policy controls.
- Added a Playwright-based Microsoft Copilot UI adapter for full coverage, with caveats for authenticated profile requirements and selector/UI fragility.
- Adjusted Microsoft Copilot UI adapter metadata to record the Playwright profile source rather than a default local profile path.
- Added an optional Microsoft Copilot UI `preferred_mode` path and smoke-tested `Think Deeper` mode selection.
- Added a client-config path for Claude Code to defer model and effort selection to DSIT-managed local Claude settings.
- Added per-client environment overrides so Claude Code can run with `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` and avoid DSIT gateway rejection of beta request fields such as `context_management`.
- Added a Microsoft Copilot prompt-source path that cites public `v1.1` GitHub wiki permalinks and injects copied excerpts from key wiki files so the Microsoft web UI is not asked to read local filesystem paths.
- Added the MCP research wiki under `challenge-2/MCP-Wiki/`, including an index, operating rules, architecture, implementation plan, security model, decision record, candidate register, source notes, report index, machine-readable source register, machine-readable candidate register, and reserved folders for implementation, specifications, and external reference submodules.
- Added a resolved MCP bibliography, linked Deep Research report derivative, search-oriented frontmatter, cross-link graph, wiki optimization log, and MCP wiki lint gate.
- Resolved the MCP wiki open decisions: OAuth 2.0 / Microsoft Entra ID target authentication, first-use reference submodules, semantic retrieval in v1, and release-time external URL validation.
- Resolved additional MCP validation/auth decisions: Copilot Studio direct MCP connection is first, and API-key authentication is excluded unless live host validation proves it is required.
- Added semantic retrieval option evaluation, with a provisional local baseline of `BAAI/bge-small-en-v1.5` plus exact NumPy cosine search and comparison runs for `all-MiniLM-L6-v2` and `e5-small-v2`.
- Added first-use reference implementation submodules for ProfessionalWiki, olgasafonova, qmd, and mkdocs-mcp-plugin, with local `SOURCE.md` metadata and license/reuse caveats.
- Added repository ignore coverage for nested `.DS_Store` and AppleDouble metadata files.
- Implemented the read-only Challenge 2 Wiki MCP server under `challenge-2/MCP-Wiki/implementation/wiki_mcp/`, with stdio and local HTTP transports, path allowlists, benchmark denylists, source-register tools, context-pack tools, provenance explanations, deterministic semantic retrieval, and append-only audit logging.
- Added `challenge-2/tools/wiki_mcp_server.py` as the MCP server CLI entry point.
- Added `codex-mcp` as an evaluation client so Codex can answer through the local Wiki MCP server and record live MCP tool-call evidence.
- Added `challenge-2/tools/compare_wiki_eval.py` and `tests/test_challenge2_compare_wiki_eval.py` for correction-aware comparison reporting.
- Completed the `validated-full-20260419T2225Z` 100-question evaluation run for the validated clients. Codex, Codex with MCP, Claude, and Microsoft Copilot have effective `100/100` completed rows; Gemini completed `36/100` before model quota exhaustion; GitHub Copilot CLI remains `policy_blocked` by smoke test.
- Added the sanitized comparison report and metrics under `challenge-2/evaluation/reports/`.
- Added `challenge-2/MCP-Wiki/sources/codex-thread-mcp-implementation-evaluation.md` to capture the current MCP implementation/evaluation thread as a public summary and to recommend including it in the current MCP pull request rather than publishing a raw transcript.
- Added public-safe rubric scoring artifacts for the same effective run: `validated-full-20260419T2225Z-rubric-scores.csv`, `validated-full-20260419T2225Z-rubric-leaderboard.md`, and `validated-full-20260419T2225Z-rubric-leaderboard.json`.
- Added `START-HERE.md`, a public reader guide with LinkedIn, event, time-based, and persona-based routes through the repository.
- Expanded `output/doc/linkedin-version-1-1-announcement.md` with a polished main LinkedIn post and a short comment for other event posts.
- Updated `.gitignore` to ignore all `.obsidian/` directories as local Obsidian browsing state.
- Updated the comparison report to include the rubric-scored quality leaderboard: Codex `484/500`, Claude `480/500`, Codex with MCP `471/500`, Gemini `171/500`, and Microsoft Copilot `58/500`.
- Added a Dark Data Workbench source-note Markdown endpoint and updated reader links so `Open note` resolves inside the local app.
- Fixed Dark Data Workbench context export selection so selected sources remain exported even when the active search or filters hide them.
- Added pnpm workspace build-approval config for the workbench `esbuild` dependency.
- Addressed the current PR review comments as bug classes: all byte-budgeted MCP excerpts now truncate by UTF-8 bytes, including the Workbench MCP reader, and Wiki MCP HTTP notifications now return no content instead of `{}`.
- Addressed the follow-up PR review comments as bug classes: all local MCP handlers now validate non-object JSON-RPC requests and invalid `params` / `arguments` envelopes, Workbench MCP stdio now returns parse errors without terminating, and Challenge 2 evaluation repo-state capture no longer aborts if Git is missing from `PATH`.
- Addressed the latest PR review comment as a reproducibility bug class: the `codex-mcp` spawned Wiki MCP server now receives configured server args, including `semantic_model_id`, so live MCP retrieval uses the same semantic model recorded for the prompt context-pack seed.
- Addressed the newest PR review comments as evidence-integrity classes: live evaluation runs now remove stale assistant-response files before invocation, Workbench MCP resources use the configured challenge root, and comparison metrics skip/count malformed MCP audit JSONL lines instead of failing the report.
- Addressed the latest PR review comments as security/publication classes: Wiki MCP HTTP startup now rejects a missing or empty configured bearer-token environment variable, and public comparison metrics now sanitize arbitrary local executable/app paths and home-relative paths.
- Addressed the latest PR review comment as a retrieval-performance class: Wiki MCP search now runs only the retrieval engine required by the selected mode, so lexical-only calls do not build/query the semantic index.

## Validation

- Current SeeLinks/Micropedia parity validation passed locally:
  - ran `cd challenge-2/workbench && pnpm check`;
  - ran `cd challenge-2/workbench && pnpm test` with `22` passing Vitest tests;
  - ran `cd challenge-2/workbench && pnpm build`;
  - ran `cd challenge-2/workbench && pnpm test:ui` outside the sandbox after local server binding was blocked; Playwright reported `14` passing browser tests, including folded-by-default facet accordion behaviour, active/pinned facet retention, double-click value reduction, order-by, metadata, facet pin/order, highlight reduction, rollup, collection, detail dock, tile text, outline, timeline, existing pack switching, reader Markdown preview/text, graph/table/checks, and mobile layout coverage.
  - ran `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`;
  - ran `python3 tools/check_documentation_lockstep.py`;
  - ran `git diff --check`.
- Current Dark Data Workbench pack-switch and Markdown preview validation passed locally:
  - ran `cd challenge-2/workbench && pnpm check`;
  - ran `cd challenge-2/workbench && pnpm test` with `19` passing Vitest tests;
  - ran `cd challenge-2/workbench && pnpm build`;
  - ran `cd challenge-2/workbench && pnpm test:ui` outside the sandbox after the sandbox blocked Chromium launch; Playwright reported `10` passing browser tests;
  - ran `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`;
  - ran `python3 tools/check_documentation_lockstep.py`;
  - ran `git diff --check`;
  - live in-app browser verification confirmed Challenge 2/HMRC pack switching updates URL, heading, and card counts, and confirmed reader Preview/Text mode on `DOC-HB-002`.
- Current HMRC Beyond the Hype talk research pack validation passed locally:
  - confirmed all `12` master-prompt deliverables exist under `research/hmrc-beyond-hype/`;
  - parsed `research/hmrc-beyond-hype/01_source_register.csv` as `50` source rows from `EXT-001` through `REPO-022`;
  - checked for stale repo-local pseudo-links, placeholder markers, and transcript processing remnants in the talk pack and lockstep docs;
  - retested all `69` repo-local GitHub blob links in `research/hmrc-beyond-hype/` against the pinned clean-branch commit and found `0` missing paths or invalid line references;
  - ran `python3 tools/check_documentation_lockstep.py`;
  - ran `git diff --check`.
- Current HMRC talk import/transcript validation passed locally:
  - generated two base transcripts from local `.m4a` files with `whisper-cli`, English `ggml-base.en.bin`, CPU/no-flash flags, and SRT output;
  - generated pyannote diarization with `pyannote-community/speaker-diarization-community-1` on `mps`, processing `40.0` minutes of audio in `83.8` seconds;
  - wrote `Trace` / `Query` Markdown and TXT drafts for both audio files, plus diarization segment CSV and report;
  - confirmed the `Trace` / `Query` rename is label-only: the base `.txt` and `.srt` transcript files are unchanged, `236` speaker-attributed turns retain the same timestamps and words after the label mapping, and `439` diarization CSV rows changed only the normalized voice-name field;
  - ran `python3 -m py_compile research/hmrc-beyond-hype/tools/transcribe_audio.py research/hmrc-beyond-hype/tools/diarize_audio_transcripts.py`;
  - ran `python3 -m json.tool research/hmrc-beyond-hype/transcripts/manifest.json`;
  - ran `uv run --with ruff ruff check --config ruff.toml research/hmrc-beyond-hype/tools`;
  - previously ran `uv run --with ruff ruff check --config ruff.toml --show-files .` and confirmed nested external reference repositories are excluded from the workspace Ruff file set.
- Current HMRC narrative goal validation passed locally:
  - added `research/hmrc-beyond-hype/narrative/README.md` as the active goal brief and checked its local Markdown links resolve;
  - ran `python3 tools/check_documentation_lockstep.py`;
  - ran `git diff --check`.
- Current HMRC narrative sidecar validation passed locally:
  - ran `python3 research/hmrc-beyond-hype/tools/build_narrative_seelinks_pack.py`;
  - ran `python3 research/hmrc-beyond-hype/tools/build_seelinks_ui_infographics.py`;
  - generated four original SeeLinks web UI infographics covering anatomy, facet/tile interactions, view/detail/output surfaces, and data/state/export flow;
  - generated a SeeLinks-style datapack with `234` items, `10` facets, `9` collections, `285` graph nodes, and `2984` graph edges;
  - ran `uv run --with python-pptx --with pillow --with pypdf python research/hmrc-beyond-hype/tools/build_narrative_sidecars.py`;
  - generated `73` sidecars and `73` derived image assets from the current visual import inventory;
  - ran `uv run --with python-pptx --with pillow --with pypdf python research/hmrc-beyond-hype/tools/validate_narrative_sidecars.py --write-report`;
  - validation reported all `13` current import files represented, `73` covered visual items, `109` reachable narrative Markdown files, `77` referenced assets, `0` orphaned narrative Markdown files, and `0` errors;
  - added and ran `python3 research/hmrc-beyond-hype/tools/lint_narrative_semantics.py --check-external --write-report`;
  - semantic lint reported `0` errors, `0` warnings, no contradictory tracked counts, all required concepts and indexed tags represented, and `5` unique external links passing live validation;
  - confirmed `AI-Native_Engineering_Blueprint.pptx` contains `15` slides, with related AI-native PDF/image/briefing material covered as separate import files;
  - ran `python3 -m py_compile research/hmrc-beyond-hype/tools/lint_narrative_semantics.py research/hmrc-beyond-hype/tools/build_narrative_sidecars.py research/hmrc-beyond-hype/tools/build_seelinks_ui_infographics.py research/hmrc-beyond-hype/tools/build_narrative_seelinks_pack.py research/hmrc-beyond-hype/tools/validate_narrative_sidecars.py`;
  - previously ran `uv run --with python-pptx --with pillow --with pypdf python -m py_compile research/hmrc-beyond-hype/tools/build_narrative_sidecars.py research/hmrc-beyond-hype/tools/build_narrative_seelinks_pack.py research/hmrc-beyond-hype/tools/build_seelinks_ui_infographics.py research/hmrc-beyond-hype/tools/validate_narrative_sidecars.py research/hmrc-beyond-hype/tools/transcribe_audio.py research/hmrc-beyond-hype/tools/diarize_audio_transcripts.py`;
  - ran `uv run --with ruff ruff check --config ruff.toml research/hmrc-beyond-hype/tools`;
  - ran `cd challenge-2/workbench && pnpm check`;
  - ran `cd challenge-2/workbench && pnpm test`;
  - ran `cd challenge-2/workbench && pnpm build`;
  - ran `cd challenge-2/workbench && pnpm test:ui`;
  - reran the same workbench check sequence after the PR-check fix, including 16 passing Vitest tests and 9 passing Playwright tests;
  - ran `python3 tools/check_documentation_lockstep.py`;
  - ran `git diff --check`.
- Challenge 2 strict build previously passed with `43 sources, 81 notes, 0 lint issues`.
- Current lightweight validation for the Mermaid fix passed:
  - `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
  - Checked that the architecture Mermaid labels no longer start with ordered-list syntax.
- Documentation lockstep validation passed locally:
  - `python3 tools/check_documentation_lockstep.py`
  - `python3 -m py_compile tools/check_documentation_lockstep.py`
  - `git diff --check`
  - temporary missing-file check confirmed the script fails when `Changelog.md` is absent.
- Current lightweight validation for the Challenge 2 evaluation harness passed:
  - `python3 -m py_compile challenge-2/evaluation/__init__.py challenge-2/evaluation/questions.py challenge-2/evaluation/audit.py challenge-2/evaluation/clients.py challenge-2/evaluation/scoring.py challenge-2/tools/run_wiki_eval.py challenge-2/tools/wiki_eval_mcp.py challenge-2/tools/summarise_wiki_eval.py`
  - `python3 -m unittest discover -s tests -p 'test_challenge2_eval*.py'`
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients codex --questions Q001 --output-root /tmp/challenge2-wiki-eval-test --run-id smoke`
  - `python3 challenge-2/tools/summarise_wiki_eval.py /tmp/challenge2-wiki-eval-test/smoke`
  - stdio JSON-RPC smoke test for `challenge-2/tools/wiki_eval_mcp.py`
- Current Dark Data Workbench validation passed locally:
  - `cd challenge-2/workbench && pnpm check`
  - `cd challenge-2/workbench && pnpm test`
  - `cd challenge-2/workbench && pnpm build`
  - `cd challenge-2/workbench && pnpm test:ui`
  - `python3 -m unittest tests/test_challenge2_workbench_mcp.py`
- Current Dark Data Workbench review baseline on `codex/workbench-review` passed locally:
  - `cd challenge-2/workbench && pnpm check`
  - `cd challenge-2/workbench && pnpm test`
  - `cd challenge-2/workbench && pnpm build`
  - `cd challenge-2/workbench && pnpm test:ui`
  - `cd challenge-2/workbench && pnpm test:coverage`
  - `python3 -m unittest tests/test_challenge2_workbench_mcp.py`
  - `python3 tools/check_documentation_lockstep.py`
  - `git diff --check`
  - Live Playwright interaction pass confirmed 43 initial source cards, exact source search narrowing to one card, Browser AI controls, graph rendering, and no console/page/request errors.
  - Local `curl` smoke test confirmed `/api/source-note/DOC-HB-002` returns Markdown with HTTP `200`, and the static build emitted source-note endpoint files.
- Current documentation validation for the Challenge 2 demonstration guide passed locally:
  - `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
  - `python3 tools/check_documentation_lockstep.py`
  - `git diff --check`
- Current report generation validation passed locally:
  - `pandoc -f markdown-smart output/doc/challenge-2-realtime-delivery-report.md --toc --number-sections --resource-path=output/doc:output/doc/assets:. -o output/doc/challenge-2-realtime-delivery-report.docx`
  - `unzip -l output/doc/challenge-2-realtime-delivery-report.docx`
  - `textutil -convert txt -stdout output/doc/challenge-2-realtime-delivery-report.docx`
- Current Codex postmortem wiki validation passed locally:
  - `python3 -m py_compile tools/build_codex_postmortem.py`
  - `python3 tools/build_codex_postmortem.py`
  - `python3 -m unittest tests/test_build_codex_postmortem.py`
  - Generated private lint reports `5` conversation sources, `66` exchanges, `3` external sources, `44` repository artifact sources, and `0` broken internal links.
  - Generated public publication lint report with `0` broken internal links and `0` forbidden publication hits.
- Current postmortem publication-readiness review used targeted scans for local paths, account/workspace identifiers, credential-shaped strings, email-address patterns, copied external-source material, read-only source permissions, and untracked publication-adjacent artifacts.
- Current localized-source license review checked the external source copies for license notices and compared them against X Terms of Service, GitHub Terms of Service, GitHub licensing guidance, the Karpathy gist page, and Jina AI legal terms.
- Current contribution-modes/security assessment validation passed locally:
  - Converted the attached DOCX to Markdown with Pandoc and normalised local media paths.
  - `rg` credential-pattern scan found no live secrets in the intended publication material; hits were documentation, synthetic fixture policy content, generated discussion, lockfile token strings, and Git sample hook text.
  - Unsafe-pattern scan found no direct dynamic HTML or shell execution pattern; it identified expected subprocess usage in local tools/tests and `localStorage` use for saved workbench context metadata.
  - `cd challenge-2/workbench && pnpm audit --audit-level moderate` passed for moderate and higher severities; `pnpm audit --json` reported one low `cookie` transitive advisory, CVE-2024-47764 / GHSA-pxg6-pf52-xh8x.
  - `uv run --with bandit bandit -r challenge-2 tools tests -x challenge-2/workbench,node_modules,postmortem,postmortem-public,output` reported 17 low, 1 medium, and 0 high findings after hardening the postmortem external-source fetcher.
  - `python3 -m unittest tests/test_challenge2_workbench_mcp.py tests/test_challenge2_eval_mcp.py`
  - `python3 -m py_compile tools/build_codex_postmortem.py tools/check_documentation_lockstep.py challenge-2/tools/build_wiki.py challenge-2/tools/workbench_mcp.py challenge-2/evaluation/clients.py`
  - `cd challenge-2/workbench && pnpm check`
  - `cd challenge-2/workbench && pnpm test`
  - `cd challenge-2/workbench && pnpm build`
  - `cd challenge-2/workbench && pnpm test:ui`
- Current evaluation-versioning validation passed locally:
  - `python3 -m py_compile challenge-2/evaluation/clients.py challenge-2/evaluation/audit.py challenge-2/tools/run_wiki_eval.py tests/test_challenge2_eval_clients.py`
  - `python3 -m json.tool challenge-2/evaluation/client-config.example.json`
  - `node --check challenge-2/tools/microsoft_copilot_playwright.mjs`
  - `python3 -m unittest discover -s tests -p 'test_challenge2_eval*.py'`
  - `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients codex,gemini,claude --questions Q001 --output-root /tmp/challenge2-wiki-eval-versioning --run-id versioning-smoke`
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients github-copilot --questions Q001 --output-root /tmp/challenge2-wiki-eval-versioning --run-id copilot-smoke`
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients full --questions Q001 --output-root /tmp/challenge2-wiki-eval-versioning --run-id full-coverage-smoke`
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients full --questions Q001 --client-config challenge-2/evaluation/client-config.example.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id full-config-smoke`
  - `copilot version` returned `GitHub Copilot CLI 1.0.32` and reported it was the latest installed version.
- Current MCP PR review-hardening validation passed locally:
  - `python3 -m py_compile challenge-2/MCP-Wiki/implementation/wiki_mcp/core.py challenge-2/MCP-Wiki/implementation/wiki_mcp/transport.py challenge-2/tools/workbench_mcp.py challenge-2/tools/wiki_eval_mcp.py challenge-2/tools/run_wiki_eval.py challenge-2/evaluation/clients.py tools/check_documentation_lockstep.py tools/build_codex_postmortem.py`
  - `python3 -m unittest tests.test_challenge2_wiki_mcp_server tests.test_challenge2_workbench_mcp tests.test_challenge2_eval_mcp tests.test_challenge2_run_wiki_eval tests.test_challenge2_eval_clients tests.test_challenge2_compare_wiki_eval`
  - `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report`
  - `python3 tools/check_documentation_lockstep.py`
  - `git diff --check`
- Current `codex-mcp` reproducibility validation passed locally:
  - `python3 -m py_compile challenge-2/evaluation/clients.py`
  - `python3 -m unittest tests.test_challenge2_eval_clients`
  - `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report`
  - `python3 tools/check_documentation_lockstep.py`
  - `git diff --check`
- Current evidence-integrity review validation passed locally:
  - `python3 -m py_compile challenge-2/evaluation/clients.py challenge-2/tools/workbench_mcp.py challenge-2/tools/compare_wiki_eval.py`
  - `python3 -m unittest tests.test_challenge2_eval_clients tests.test_challenge2_workbench_mcp tests.test_challenge2_compare_wiki_eval`
  - `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report`
  - `python3 tools/check_documentation_lockstep.py`
  - `git diff --check`
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients full --questions Q001 --output-root /tmp/challenge2-wiki-eval-versioning --run-id full-coverage-smoke-xhigh`
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients full --questions Q001 --client-config challenge-2/evaluation/client-config.example.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id full-config-smoke-xhigh`
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients full --questions Q001 --client-config challenge-2/evaluation/client-config.example.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id full-config-smoke-sanitized`
  - Inspected `full-config-smoke-sanitized/run.json`; Microsoft Copilot UI metadata records `profile_dir_source: default` rather than a local profile path, and GitHub Copilot records `gpt-5.4` with `xhigh` effort from the staff-confirmed override.
  - `python3 challenge-2/tools/run_wiki_eval.py --clients microsoft-copilot --questions Q001 --timeout-sec 90 --output-root /tmp/challenge2-wiki-eval-versioning --run-id microsoft-live-smoke-3` returned `auth_required`, proving the adapter runs and captures sign-in evidence but still needs an authenticated Playwright profile.
  - `python3 challenge-2/tools/run_wiki_eval.py --clients microsoft-copilot --questions Q001 --timeout-sec 90 --output-root /tmp/challenge2-wiki-eval-versioning --run-id microsoft-live-smoke-sanitized` returned `auth_required`; the captured JSON records `profileDirSource: default` and no local profile path.
  - `python3 challenge-2/tools/run_wiki_eval.py --clients github-copilot --questions Q001 --timeout-sec 120 --output-root /tmp/challenge2-wiki-eval-versioning --run-id github-copilot-live-smoke-policy` returned `policy_blocked`, proving the installed CLI is callable but the account or organisation policy blocks live requests.
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients full --questions Q001 --timeout-sec 180 --client-config /tmp/challenge2-explicit-smoke.XXXXXX.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id managed-claude-thinking-dry-smoke`
  - `python3 challenge-2/tools/run_wiki_eval.py --clients full --questions Q001 --timeout-sec 180 --client-config /tmp/challenge2-explicit-smoke.XXXXXX.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id managed-claude-thinking-live-smoke` completed for Codex, Gemini, and Microsoft Copilot with `Think Deeper` selected; Claude still failed against the DSIT-managed license portal with `context_management: Extra inputs are not permitted`, and GitHub Copilot CLI remained `policy_blocked`.
  - `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 claude -p --output-format json "Reply with OK only."` completed.
  - `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 claude -p --model opus --output-format json "Reply with OK only."` completed and resolved to the DSIT-managed `eu.anthropic.claude-opus-4-6-v1` model group.
  - `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 python3 challenge-2/tools/run_wiki_eval.py --clients full --questions Q001 --timeout-sec 180 --client-config /tmp/challenge2-explicit-smoke.XXXXXX.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id managed-claude-beta-disabled-live-smoke` completed for Codex, Gemini, Claude, and Microsoft Copilot; GitHub Copilot CLI remained `policy_blocked`.
  - `python3 challenge-2/tools/run_wiki_eval.py --clients claude --questions Q001 --timeout-sec 120 --client-config challenge-2/evaluation/client-config.example.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id claude-config-env-smoke` completed, proving the client config can inject the Claude beta-disable compatibility flag without a shell-level export.
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients full --questions Q001 --client-config challenge-2/evaluation/client-config.example.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id full-config-env-dry-smoke`
  - `python3 challenge-2/tools/run_wiki_eval.py --dry-run --clients full --questions Q001 --client-config challenge-2/evaluation/client-config.example.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id full-explicit-config-dry-smoke` recorded explicit selectable models for Codex, Gemini, GitHub Copilot, and Microsoft Copilot, with Claude delegated to DSIT-managed local settings.
  - `python3 challenge-2/tools/run_wiki_eval.py --clients full --questions Q001 --timeout-sec 180 --client-config challenge-2/evaluation/client-config.example.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id full-explicit-config-live-smoke` completed for Codex, Gemini, Claude, and Microsoft Copilot; GitHub Copilot CLI remained `policy_blocked`.
  - A direct Microsoft Copilot `Think Deeper` smoke with public GitHub wiki URLs selected the mode successfully but did not yield usable scored JSON, so GitHub URLs alone are not sufficient; Microsoft scoring still needs explicit source-context injection or attachment strategy.
  - `python3 challenge-2/tools/run_wiki_eval.py --clients microsoft-copilot --questions Q001 --timeout-sec 180 --client-config challenge-2/evaluation/client-config.example.json --output-root /tmp/challenge2-wiki-eval-versioning --run-id microsoft-github-context-live-smoke` completed and returned usable JSON from the Microsoft UI client with `Think Deeper` selected, using public GitHub permalinks plus copied source excerpts instead of local paths.
  - `python3 tools/check_documentation_lockstep.py`
  - `git diff --check`
- Current MCP research wiki validation passed locally:
  - `python3 -m json.tool challenge-2/MCP-Wiki/data/source-register.json`
  - `python3 -m json.tool challenge-2/MCP-Wiki/data/candidate-register.json`
  - `python3 -m json.tool challenge-2/MCP-Wiki/data/bibliography.json`
  - `python3 -m py_compile challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py`
  - `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report` reported `22` Markdown files, `222` internal links, `67` external links, complete search-term coverage, `0` errors, and `0` warnings.
  - Live bibliography URL check returned HTTP success responses for all `31` entries after replacing stale Microsoft/NCSC URLs and ACM DOI targets that blocked automated checks.
  - After adding first-use submodule metadata, `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report` reported `27` Markdown files, `270` internal links, `75` external links, complete search-term coverage, `0` errors, and `0` warnings.
  - After adding semantic retrieval options, `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report` reported `28` Markdown files, `286` internal links, `85` external links, complete search-term coverage, `0` errors, and `0` warnings.
  - `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
  - `python3 tools/check_documentation_lockstep.py`
  - `git diff --check`
  - Removed the previously tracked `challenge-2/.DS_Store`; MCP wiki lint treats ignored `.DS_Store` files as local state and fails only if they are tracked.
- Current Wiki MCP implementation and evaluation validation passed locally:
  - `python3 -m py_compile challenge-2/MCP-Wiki/implementation/wiki_mcp/__init__.py challenge-2/MCP-Wiki/implementation/wiki_mcp/core.py challenge-2/MCP-Wiki/implementation/wiki_mcp/transport.py challenge-2/tools/wiki_mcp_server.py challenge-2/tools/compare_wiki_eval.py challenge-2/evaluation/clients.py challenge-2/tools/run_wiki_eval.py`
  - `python3 -m unittest tests.test_challenge2_eval_clients tests.test_challenge2_compare_wiki_eval tests.test_challenge2_wiki_mcp_server`
  - `uv run --with coverage python -m coverage run --source=challenge-2/MCP-Wiki/implementation/wiki_mcp -m unittest tests.test_challenge2_wiki_mcp_server`
  - `uv run --with coverage python -m coverage report` reported `91%` package coverage for the MCP server implementation.
  - `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report` reported `28` Markdown files, `287` internal links, `85` external links, complete search-term coverage, `0` errors, and `0` warnings.
  - `python3 challenge-2/tools/run_wiki_eval.py --clients codex-mcp --questions Q057 --timeout-sec 900 --output-root /tmp/challenge2-wiki-eval-corrections --run-id codex-mcp-q057-correction-20260420T0320Z --client-config challenge-2/evaluation/client-config.example.json` completed the single Codex-MCP correction row.
  - `python3 challenge-2/tools/compare_wiki_eval.py /tmp/challenge2-wiki-eval-full/validated-full-20260419T2225Z --correction-run codex-mcp=/tmp/challenge2-wiki-eval-corrections/codex-mcp-q057-correction-20260420T0320Z --smoke-run github-copilot=/tmp/challenge2-wiki-eval-mcp/github-copilot-q001-smoke --output challenge-2/evaluation/reports/validated-full-20260419T2225Z-comparison.md --json-output challenge-2/evaluation/reports/validated-full-20260419T2225Z-metrics.json`
  - The comparison report records `100/100` completed answers for Codex, Codex with MCP, Claude, and Microsoft Copilot; Gemini is recorded as `completed:36, quota_exhausted:64`; GitHub Copilot CLI is recorded through a `policy_blocked` smoke run.
- Current MCP thread-capture validation passed locally:
  - `python3 -m json.tool challenge-2/MCP-Wiki/data/source-register.json`
  - `python3 -m py_compile challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py`
  - `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report` reported `29` Markdown files, `311` internal links, `85` external links, complete search-term coverage, `0` errors, and `0` warnings.
- Current rubric-scoring validation passed locally:
  - Rubric scoring batches produced `500` unique score rows, one per effective client/question pair.
  - `python3 challenge-2/tools/compare_wiki_eval.py /tmp/challenge2-wiki-eval-full/validated-full-20260419T2225Z --correction-run codex-mcp=/tmp/challenge2-wiki-eval-corrections/codex-mcp-q057-correction-20260420T0320Z --smoke-run github-copilot=/tmp/challenge2-wiki-eval-mcp/github-copilot-q001-smoke --score-path challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-scores.csv --output challenge-2/evaluation/reports/validated-full-20260419T2225Z-comparison.md --json-output challenge-2/evaluation/reports/validated-full-20260419T2225Z-metrics.json`
  - `python3 -m json.tool challenge-2/evaluation/reports/validated-full-20260419T2225Z-metrics.json`
  - `python3 -m json.tool challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-leaderboard.json`
  - `python3 -m py_compile challenge-2/tools/compare_wiki_eval.py challenge-2/evaluation/scoring.py`
  - `python3 -m unittest tests.test_challenge2_compare_wiki_eval`
  - `python3 -m unittest tests.test_challenge2_eval_clients tests.test_challenge2_compare_wiki_eval tests.test_challenge2_wiki_mcp_server`
  - `python3 tools/check_documentation_lockstep.py`
  - `git diff --check`
  - Targeted publication scan found no raw answer/gold-answer columns, local run paths, UI session IDs, or Playwright profile metadata in the committed rubric report artifacts.
- Current PR review-fix validation passed locally:
  - `python3 -m py_compile challenge-2/MCP-Wiki/implementation/wiki_mcp/core.py challenge-2/MCP-Wiki/implementation/wiki_mcp/transport.py challenge-2/tools/workbench_mcp.py`
  - `python3 -m unittest tests.test_challenge2_wiki_mcp_server tests.test_challenge2_workbench_mcp`
  - `python3 -m unittest tests.test_challenge2_wiki_mcp_server tests.test_challenge2_workbench_mcp tests.test_challenge2_eval_clients tests.test_challenge2_compare_wiki_eval`
  - `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report` reported `29` Markdown files, `311` internal links, `85` external links, complete search-term coverage, `0` errors, and `0` warnings.
  - Searched for remaining `text[:remaining]`, `[:max_bytes]`, and `response or {}` style instances in MCP implementation paths; remaining byte slices are inside the UTF-8 truncation helpers.
- Current security/publication PR review validation passed locally:
  - `python3 -m py_compile challenge-2/tools/wiki_mcp_server.py challenge-2/tools/compare_wiki_eval.py`
  - `python3 -m unittest tests.test_challenge2_wiki_mcp_server tests.test_challenge2_compare_wiki_eval`
  - `python3 -m unittest tests.test_challenge2_wiki_mcp_server tests.test_challenge2_workbench_mcp tests.test_challenge2_eval_mcp tests.test_challenge2_run_wiki_eval tests.test_challenge2_eval_clients tests.test_challenge2_compare_wiki_eval`
  - `uv run --with coverage python -m coverage run --source=challenge-2/MCP-Wiki/implementation/wiki_mcp -m unittest tests.test_challenge2_wiki_mcp_server`
  - `uv run --with coverage python -m coverage report` reported `91%` package coverage for the MCP server implementation.
  - `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report` reported `29` Markdown files, `311` internal links, `85` external links, complete search-term coverage, `0` errors, and `0` warnings.
  - `python3 -m json.tool challenge-2/evaluation/reports/validated-full-20260419T2225Z-metrics.json`
  - `python3 -m json.tool challenge-2/MCP-Wiki/data/source-register.json`
  - `python3 -m json.tool challenge-2/MCP-Wiki/data/lint-report.json`
  - `python3 tools/check_documentation_lockstep.py`
  - `git diff --check`
  - Targeted path scans found no `/opt/homebrew`, `/Applications`, local user home, home-relative, `/usr/local`, or `/tmp/challenge2` paths remaining in committed evaluation report JSON/Markdown artifacts.
- Current retrieval-mode PR review validation passed locally:
  - `python3 -m py_compile challenge-2/MCP-Wiki/implementation/wiki_mcp/core.py`
  - `python3 -m unittest tests.test_challenge2_wiki_mcp_server`
  - `python3 -m py_compile challenge-2/MCP-Wiki/implementation/wiki_mcp/core.py challenge-2/MCP-Wiki/implementation/wiki_mcp/transport.py challenge-2/tools/wiki_mcp_server.py challenge-2/tools/compare_wiki_eval.py`
  - `python3 -m unittest tests.test_challenge2_wiki_mcp_server tests.test_challenge2_workbench_mcp tests.test_challenge2_eval_mcp tests.test_challenge2_run_wiki_eval tests.test_challenge2_eval_clients tests.test_challenge2_compare_wiki_eval`
  - `uv run --with coverage python -m coverage run --source=challenge-2/MCP-Wiki/implementation/wiki_mcp -m unittest tests.test_challenge2_wiki_mcp_server`
  - `uv run --with coverage python -m coverage report` reported `91%` package coverage for the MCP server implementation.
  - `python3 challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py --write-report` reported `29` Markdown files, `311` internal links, `85` external links, complete search-term coverage, `0` errors, and `0` warnings.
  - `python3 -m json.tool challenge-2/MCP-Wiki/data/source-register.json`
  - `python3 -m json.tool challenge-2/MCP-Wiki/data/lint-report.json`
  - `python3 tools/check_documentation_lockstep.py`
  - `git diff --check`

## Open Items

- Review the `postmortem-public/wiki/decisions.md` defaults before publishing externally.
- Address the security assessment findings before making any production-readiness claim: harden GitHub Actions permissions/action pinning, upgrade the low `cookie` advisory path, replace unsafe XML parsing for untrusted documents, add response-size and redirect controls to postmortem URL fetching, and define Secure by Design/DPIA/operational controls for real data.
- Add `challenge-2/wiki/demo-answers.md` with source-backed answers to the official demo questions.
- Enable/authenticate GitHub Copilot CLI policy access for live runs; the standalone `copilot` binary is installed locally, but live evaluation currently returns `policy_blocked`.
- Use `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` for Claude Code runs through the DSIT-managed gateway; the full validated run completed with that compatibility flag injected through client config.
- Keep Microsoft Copilot source grounding explicit for scored runs: the GitHub permalink plus copied-excerpt prompt path has passed a `Q001` smoke, while a versioned OneDrive or SharePoint wiki copy is a plausible manual fallback if GitHub access fails and should be smoke-tested before use.
- Rerun Gemini CLI on `Q037` through `Q100` after `gemini-3.1-pro-preview` quota resets, or record a decision to exclude Gemini from the full validated set for this publication cycle.
- Run the v1 semantic retrieval benchmark to lock the final embedding model from the evaluated shortlist.
- Validate the Copilot Studio direct MCP connection and only escalate to Agents Toolkit packaging or a custom connector if direct connection cannot deliver the required server functionality.

## Next Recommended Steps

1. Review the rubric-scored leaderboard and decide whether independent moderation is needed before making an external comparative quality claim.
2. Rerun Gemini CLI after quota reset if a complete Gemini row set is required for the public comparison.
3. Enable GitHub Copilot CLI policy access if GitHub Copilot must be included beyond the current `policy_blocked` smoke evidence.
4. Run the embedding shortlist benchmark and lock the v1 semantic retrieval model.
5. Validate the server through Copilot Studio direct MCP connection.
6. Add source-backed demo answers for the five Challenge 2 demo questions.
