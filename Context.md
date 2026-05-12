# Context

## Repository Purpose

This fork is Team DSIT A's working Challenge 2 implementation and evidence pack from the AI Engineering Lab Hackathon London 2026. It keeps the original event briefs and starter material, but its primary purpose is now to document, demonstrate, evaluate, and critique the "Unlocking the dark data" prototype.

The original repository was an event pack for a one-day AI-assisted engineering hackathon. This fork is a worked example of how AI coding assistants can help build a source-backed LLM Wiki, browser workbench, MCP/evaluation harness, delivery report, public postmortem, and security assessment for a government-style dark-data problem.

The repository now also includes an HMRC Beyond the Hype talk research pack that uses this fork as a public-sector case study for the transition from coding assistants to coding agents. The pack is evidence-led and treats the Challenge 2 work as a bounded synthetic-data prototype, not as production assurance or a recommendation to use agents on real HMRC data without approved controls.

Repo-local GitHub permalinks in the HMRC talk pack are pinned to the clean talk-prep branch commit rather than to `main`, so cited line numbers remain stable before and after PR review.

The HMRC talk prep area also has a local import drop under `research/hmrc-beyond-hype/import/`. Large raw decks, images, PDFs, and audio files stay local by default; distilled Markdown inputs and generated transcript artefacts are the publishable Git materials unless a later review explicitly selects a binary source for publication. The 2026-05-12 HMRC Beyond the Hype demo release explicitly selects `research/hmrc-beyond-hype/import/beyond_hype_coding_assistants_public_sector_engineering.pptx` as the public presentation deck.

The HMRC narrative SeeLinks datapack is currently expected to expose 234 workbench cards. Dark Data Workbench unit and Playwright coverage use that count as a regression check for the committed narrative pack.

## Current Prototype Focus

The active build work has focused on Challenge 2: Unlocking the dark data.

Challenge 2 asks teams to turn messy government guidance, policy, procedural documents, PDFs, Word files, and spreadsheets into structured, findable, machine-usable content. The current prototype implements this as an Obsidian-friendly LLM Wiki:

- Raw Challenge 2 sources remain immutable.
- Generated Markdown notes live under `challenge-2/wiki/`.
- One source note is generated for each raw source document.
- Topic, entity, and map notes provide navigable synthesis.
- JSON and table exports provide machine-readable interfaces.
- Lint output checks coverage, metadata, links, and known challenge flags.
- The evaluation harness tests whether AI coding agents can answer source-backed questions using only the generated wiki, while producing DSAP-shaped audit artifacts for later scoring, FOI-style disclosure, and reconstruction.
- Dark Data Workbench provides a browser UI over the generated wiki so users can filter sources, build explicit context sets, inspect evidence without AI, or export the same context to browser AI and MCP clients.
- The Codex collaboration postmortem applies the same wiki pattern to the build conversations themselves so the human and Codex contributions can be traced from prompts, responses, repository artifacts, and external methodology sources.
- The MCP research wiki applies the same separation principle to follow-on engineering work: MCP research, source/license registers, candidate implementation reviews, specifications, and future server implementation notes live under `challenge-2/MCP-Wiki/` rather than being folded into the Challenge 2 corpus wiki or postmortem wiki.

## Data Assumptions

- Challenge starter data is synthetic unless the relevant challenge brief says otherwise.
- Challenge 2 staff-directory names, emails, phone-like values, roles, and identifiers are synthetic fixture data and should not be redacted for the demo.
- Real secrets, credentials, local filesystem paths, and provenance gaps remain review issues.
- Raw files under Challenge 2 source folders should not be edited, renamed, moved, or normalised as part of wiki generation.

## Important Paths

- `README.md`: fork overview, Challenge 2 value proposition, start points, repository map, validation summary, and original hackathon context.
- `START-HERE.md`: public reader guide for LinkedIn, event, time-based, and persona-based routes through the repository.
- `Changelog.md`: dated change history.
- `Context.md`: project context, architecture assumptions, and operating constraints.
- `Progress.md`: current status, validation, blockers, and next steps.
- `AGENTS.md`: repo-wide operating rules and documentation lockstep policy.
- `tools/check_documentation_lockstep.py`: local and CI check that required tracking docs exist and move with meaningful changes.
- `challenge-2/AGENTS.md`: Challenge 2 LLM Wiki operating schema.
- `challenge-2/tools/build_wiki.py`: repeatable Challenge 2 wiki builder.
- `challenge-2/evaluation/README.md`: Challenge 2 wiki evaluation harness runbook.
- `challenge-2/tools/run_wiki_eval.py`: CLI harness for sending benchmark questions to Codex, Gemini CLI, and Claude Code.
- `challenge-2/tools/compare_wiki_eval.py`: DSAP run comparison report generator for completion, JSON parseability, citation-overlap proxies, timings, and MCP tool-call evidence.
- `challenge-2/evaluation/reports/validated-full-20260419T2225Z-comparison.md`: full Challenge 2 wiki evaluation report comparing standard Codex with Codex using the Wiki MCP server and the other validated clients.
- `challenge-2/evaluation/reports/validated-full-20260419T2225Z-metrics.json`: sanitized machine-readable metrics for the same run, including rubric-score summary data; raw prompts, answers, and bundles remain outside Git.
- `challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-scores.csv`: public-safe per-question rubric scores, statuses, and scorer notes without raw answer text.
- `challenge-2/evaluation/reports/validated-full-20260419T2225Z-rubric-leaderboard.md`: human-rubric quality leaderboard for the validated full run.
- `challenge-2/tools/wiki_mcp_server.py`: read-only Challenge 2 Wiki MCP server entry point for stdio and local HTTP validation.
- `challenge-2/tools/wiki_eval_mcp.py`: stdio MCP-compatible audit layer for controlled wiki read/search and answer recording.
- `challenge-2/tools/summarise_wiki_eval.py`: leaderboard summariser for scored harness runs.
- `challenge-2/tools/workbench_mcp.py`: stdio MCP server for Dark Data Workbench source search, source read, and context export.
- `challenge-2/workbench/src/routes/api/corpus/[packId].json/+server.ts`: local JSON endpoint for alternate workbench packs, including the HMRC narrative datapack.
- `challenge-2/workbench/src/routes/api/narrative-asset/[...path]/+server.ts`: local asset endpoint for checked-in HMRC narrative thumbnails and generated note-card placeholders.
- `challenge-2/workbench/src/routes/api/source-note/[sourceId]/+server.ts`: local Markdown endpoint used by Dark Data Workbench reader links so source notes can be opened from the app.
- `challenge-2/MCP-Wiki/index.md`: MCP research wiki entry point for the planned purpose-built Wiki MCP server.
- `challenge-2/MCP-Wiki/implementation/`: implemented read-only Wiki MCP server package, transports, and validation notes.
- `challenge-2/MCP-Wiki/research/Challenge 2 Wiki MCP Server Research Report.md`: Deep Research report motivating the Wiki MCP server architecture.
- `challenge-2/MCP-Wiki/research/Challenge 2 Wiki MCP Server Research Report - linked.md`: citation-clean linked derivative for AI navigation, derived from the raw Deep Research report.
- `challenge-2/MCP-Wiki/sources/bibliography.md` and `challenge-2/MCP-Wiki/data/bibliography.json`: resolved source bibliography with source IDs, URLs, license posture, local treatment, and related wiki paths.
- `challenge-2/MCP-Wiki/sources/codex-thread-mcp-implementation-evaluation.md`: publication-safe capture and recommendation note for the Codex thread that drove the Wiki MCP server implementation, client-grounding strategy, and Codex-with-MCP comparison.
- `challenge-2/MCP-Wiki/authentication-options.md`: evaluated authentication options for Copilot Studio-facing Streamable HTTP and records OAuth 2.0 / Microsoft Entra ID as the target production pattern.
- `challenge-2/MCP-Wiki/semantic-retrieval-options.md`: evaluated embedding model and vector-index options for v1 semantic retrieval, including licensing, provenance, reproducibility, and release constraints.
- `challenge-2/MCP-Wiki/data/source-register.json`: MCP research wiki source register, including report variants and external source treatment.
- `challenge-2/MCP-Wiki/data/candidate-register.json`: candidate project register for reference implementations and licensing posture.
- `challenge-2/MCP-Wiki/references/external/`: first-use reference implementation submodules and local source metadata for the selected MCP candidates.
- `challenge-2/MCP-Wiki/tools/lint_mcp_wiki.py`: MCP research wiki lint gate for internal links, frontmatter, tags, search terms, source-register paths, duplicate IDs, `.DS_Store` tracking, and Deep Research citation-marker leakage.
- `challenge-2/MCP-Wiki/wiki-optimization-log.md`: decision trail for how the MCP research wiki is being cross-linked and tuned for AI retrieval experiments.
- `challenge-2/MCP-Wiki/lint-report.md` and `challenge-2/MCP-Wiki/data/lint-report.json`: generated MCP wiki quality reports.
- `challenge-2/wiki/index.md`: Obsidian knowledge-base entry point.
- `challenge-2/wiki/demonstration-guide.md`: end-to-end Challenge 2 demo route covering source construction, Obsidian validation, workbench usage, Browser AI export, evaluation, and audit/FOI tracking.
- `challenge-2/wiki/workbench.md`: Obsidian entry point for running and explaining Dark Data Workbench.
- `challenge-2/wiki/architecture.md`: plain-English architecture explanation with Mermaid diagrams.
- `challenge-2/wiki/evaluation-benchmark.md`: 100-question Challenge 2 wiki benchmark with gold answers, rubrics, and scoring regime.
- `challenge-2/wiki/lint-report.md`: generated quality report.
- `challenge-2/wiki/data/source-register.json`: machine-readable source register.
- `challenge-2/workbench/`: SvelteKit Dark Data Workbench app and its unit, component, Playwright, and optional coverage tests.
- `output/doc/challenge-2-realtime-delivery-report.md` and `.docx`: colleague-facing report reconstructing the Challenge 2 realtime delivery story from the supplied hackathon write-up, repo history, logs, and Codex thread evidence.
- `postmortem/`: private generated Codex collaboration evidence archive and wiki, ignored by Git.
- `postmortem-public/`: GitHub-safe public derivative of the Codex collaboration postmortem.
- `postmortem-public/wiki/index.md`: public postmortem navigation entry point.
- `postmortem-public/wiki/postmortem.md`: public postmortem of user and Codex contributions.
- `postmortem-public/wiki/decisions.md`: inclusion-forward publication decision register with questions for review.
- `postmortem-public/wiki/data/publication-lint-report.json`: machine-readable publication lint output.
- `tools/build_codex_postmortem.py`: repeatable builder for both the private postmortem archive and public derivative.
- `tests/test_build_codex_postmortem.py`: regression tests for postmortem contribution classification and public path sanitisation.
- `output/doc/contribution-modes-proposal.md`: Markdown conversion of the attached report used as the contribution-mode evaluation frame.
- `output/doc/codex-contribution-modes-security-assessment.md`: government-security and contribution-mode assessment of Codex's role in the project.
- `output/doc/linkedin-version-1-1-announcement.md`: LinkedIn announcement draft for the Version 1.1 public release.
- `research/hmrc-beyond-hype/00_research_brief.md`: HMRC Beyond the Hype talk research brief for "From Typing Code to Steering Agents".
- `research/hmrc-beyond-hype/01_source_register.csv`: external and repo-local evidence register, with repo-local claims mapped to GitHub permalinks where possible.
- `research/hmrc-beyond-hype/06_repo_case_study_codex_build.md`: evidence-led Challenge 2 Codex build case study.
- `research/hmrc-beyond-hype/07_operating_model_for_public_sector_engineering.md`: five-layer operating model for piloting coding agents in public-sector engineering.
- `research/hmrc-beyond-hype/import/`: local HMRC talk-prep resource drop; raw binary/audio resources are ignored by default, while lightweight Markdown such as `clawpilot.md` can be tracked as source input.
- `research/hmrc-beyond-hype/import/beyond_hype_coding_assistants_public_sector_engineering.pptx`: explicitly published presentation deck for the 2026-05-12 HMRC Beyond the Hype demo release.
- `research/hmrc-beyond-hype/narrative/index.md`: GitHub-browsable entry point for the HMRC talk narrative scaffold, linking the overview, narrative arc, topic index, source-material register, visual coverage report, structural validation report, semantic lint report, sidecars, and ClawPilot sidebar.
- `research/hmrc-beyond-hype/narrative/README.md`: durable goal brief for the GitHub-browsable HMRC talk narrative wiki, including acceptance criteria and the current sidecar coverage status.
- `research/hmrc-beyond-hype/narrative/notes/import-inventory.md`: generated inventory proving every current import file has an explicit narrative treatment.
- `research/hmrc-beyond-hype/narrative/notes/ai-coding-assistants-market-briefing.md`: source note for the imported AI Coding Assistants Markdown/DOCX briefing pair.
- `research/hmrc-beyond-hype/narrative/notes/ai-coding-assistants-*.md`: section-level narrative notes for the 9 May 2026 AI Coding Assistants briefing, covering the executive summary, market map, productivity evidence, failure modes, public-sector controls, repo case study, talk track, Q&A prep, and source-register limitations.
- `research/hmrc-beyond-hype/narrative/slides/ai-native-engineering-blueprint/narrative-guide.md`: curated route through the 15-slide AI-Native Engineering Blueprint deck, with related AI-native sources handled separately.
- `research/hmrc-beyond-hype/narrative/slides/`: generated Markdown sidecars for all current imported PPTX slides, PDF pages, and standalone PNG images.
- `research/hmrc-beyond-hype/narrative/assets/visuals/`: small derived image assets referenced by the generated sidecars; raw imported visual binaries remain local/ignored.
- `research/hmrc-beyond-hype/narrative/assets/infographics/`: generated SVG infographics documenting the original SeeLinks web UI anatomy, interactions, views, and data/state flow.
- `research/hmrc-beyond-hype/narrative/seelinks/pack.json`: generated SeeLinks-style datapack for loading the HMRC talk narrative in Dark Data Workbench as slide-thumbnail cards, bounded facets, graph edges, and source-note links.
- `research/hmrc-beyond-hype/narrative/seelinks/README.md`: generated coverage summary for the HMRC narrative datapack.
- `research/hmrc-beyond-hype/narrative/notes/seelinks-web-ui-reference.md`: generated visual specification of the original SeeLinks web UI for the HMRC workbench UI pass.
- `research/hmrc-beyond-hype/narrative/notes/seelinks-micropedia-parity-matrix.md`: side-by-side matrix recording implemented SeeLinks/Micropedia parity controls, unavailable external-service states, and regression coverage.
- `research/hmrc-beyond-hype/narrative/data/narrative_semantic_lint_report.md`: generated semantic lint report covering stale-sensitive claims, documented-count contradictions, required concept/page coverage, and live external-link checks.
- `research/hmrc-beyond-hype/transcripts/`: committed Whisper transcript text, SRT timings, pyannote diarization evidence, and `Trace` / `Query` review drafts for the imported audio. `Trace` and `Query` are invented AI voice names for the machine diarization clusters, not verified speaker identities.
- `research/hmrc-beyond-hype/tools/transcribe_audio.py`: reproducible local `ffmpeg` plus `whisper-cli` transcription helper.
- `research/hmrc-beyond-hype/tools/diarize_audio_transcripts.py`: local pyannote diarization helper that uses `mps` on Apple Silicon where available.
- `research/hmrc-beyond-hype/tools/build_narrative_sidecars.py`: reproducible sidecar and derived-asset builder for the current HMRC talk visual import inventory.
- `research/hmrc-beyond-hype/tools/build_narrative_seelinks_pack.py`: reproducible generator for the HMRC talk SeeLinks-style datapack consumed by Dark Data Workbench.
- `research/hmrc-beyond-hype/tools/build_seelinks_ui_infographics.py`: reproducible generator for the original SeeLinks web UI infographic pack.
- `research/hmrc-beyond-hype/tools/validate_narrative_sidecars.py`: validation gate for sidecar coverage, local Markdown links, orphan detection, inbound sidecar links, asset references, required sidecar metadata, and raw-import staging.
- `research/hmrc-beyond-hype/tools/lint_narrative_semantics.py`: semantic validation gate for stale-claim caveats, count contradictions, missing required concepts/pages, and live external-link revalidation, including GitHub blob line-anchor checks when GitHub links are present.
- `ruff.toml` and `.vscode/settings.json`: workspace Ruff configuration that avoids parsing nested external reference repositories such as the vendored mkdocs MCP plugin `pyproject.toml`.

Dark Data Workbench controls expose active visual state for users and pressed-state metadata for automation/accessibility. Playwright tests assert the active UI state for facet, saved-check, view-mode, pack-switch, and reader note-view controls because those controls drive the visible corpus, evidence, and export context. The workbench also carries a user-entered question through Browser AI JSON, copied prompts, and Markdown evidence bundles so exported evidence remains tied to the question it is meant to answer. When a context set has selected sources, exports use the selected corpus records even if the current search or filters hide those cards. Reader note links resolve through a local Markdown endpoint rather than assuming the generated wiki folder is served as app-static content. The reader defaults to a constrained rendered Markdown preview for source notes, while preserving a raw Text view for frontmatter, exact Markdown, and troubleshooting.

Dark Data Workbench can now load the HMRC Beyond the Hype narrative pack with `?pack=hmrc-narrative`. That pack reuses the SeeLinks-style browsing pattern for the talk narrative: thumbnail cards for visual sidecars, source cards for notes and transcripts, bounded facets inferred from topics/sources/conversations, keep-marked and dismiss-marked controls, and drag-a-facet-name-to-the-card-grid colouring. Pack switching is treated as route data, so the Challenge 2 and HMRC buttons update the loaded corpus and reset corpus-scoped filters, selections, highlights, dismissed cards, and reader state without requiring a manual browser reload. Category facets use high-contrast pastel fills; the `Screenfulls` readability measure uses a graded colour scale. The pack is generated from committed narrative material and selected postmortem conversation traces; it is a navigation layer, not a replacement for the underlying source evidence.

The original SeeLinks web UI is documented as a generated infographic-backed visual specification, and the implemented parity pass is recorded in `research/hmrc-beyond-hype/narrative/notes/seelinks-micropedia-parity-matrix.md`. Dark Data Workbench now carries the main SeeLinks/Micropedia surfaces in this repo: resizable control rail, dataset/import status, dynamic facets, metadata toggle, multi-facet order-by stack, facet/value ordering, link summaries, Dexie-backed collections, print/export panels, tile-text controls, browser-only editing, grid/outline/graph/timeline/reading/table/checks views, rollup cards, history reductions, and a docked detail panel. External MCP/API loading surfaces remain configuration states unless an endpoint is configured. Editing, collections, and preferences are browser state and do not write Challenge 2 raw sources, HMRC narrative files, or generated pack JSON.

The HMRC narrative wiki now has two validation layers. `validate_narrative_sidecars.py` proves structural completeness, links, reachability, sidecar metadata, assets, and raw-import staging. `lint_narrative_semantics.py` evaluates editorial risk by flagging stale-sensitive claims, checking documented counts against generated artifacts, verifying that required talk concepts have pages/topic routes, and live-validating external URLs. Live external-link validation is not intended for CI unless network access is available.

The Challenge 2 demonstration guide is the recommended walkthrough for showing the complete prototype. It ties the source corpus, Obsidian wiki, SeeLinks-style workbench, Browser AI export, evaluation benchmark, harness outputs, and audit/FOI record back to the `Unlocking_Dark_Data.pdf` slide narrative and benchmark scoring guide.

The MCP research wiki now preserves the raw Deep Research report as evidence and uses a linked derivative for everyday AI consumption. The linked derivative removes opaque Deep Research citation markers and points to a local bibliography rather than copying third-party source bodies. The MCP wiki lint gate treats the raw report as the only allowed location for opaque Deep Research markers and checks that navigation metadata is present across the curated wiki notes.

The current MCP implementation and evaluation thread is captured in the MCP research wiki as a public summary source note rather than a raw transcript. This keeps the current branch evidence-focused and publication-safe while leaving full prompt-response regeneration to the separate `postmortem-public/` workflow if the public postmortem conversation count needs to be updated.

The accepted MCP design decisions are now: target OAuth 2.0 or Microsoft Entra ID / SSO for Copilot Studio-facing Streamable HTTP; keep anonymous and bearer-token modes to local or private smoke tests; exclude API-key auth unless live Copilot Studio validation proves it is required; validate Copilot Studio direct MCP connection first; use Codex stdio MCP as the tightest local validation loop; include semantic retrieval in v1 while preserving deterministic provenance; add the first-use candidate repositories as submodules for study; and validate external URLs at release time rather than in CI. The first-use submodules are direct reference material only and are not production dependencies.

Semantic retrieval should start with local permissive options rather than an external embedding API. The preferred first evaluation candidates are `BAAI/bge-small-en-v1.5`, `sentence-transformers/all-MiniLM-L6-v2`, and `intfloat/e5-small-v2`. The implemented validation backend uses deterministic exact-cosine local hashing so MCP contracts can be tested without downloading models on a disk-constrained machine. The final model should be locked only after a retrieval benchmark over the Challenge 2 wiki.

The Codex postmortem source archive is evidence material, not automatically publication-ready content. Conversation transcripts may include local paths, screenshots, private workflow details, local assistant configuration references, and dynamic third-party source snapshots. The localized Karpathy X/gist copies have no explicit redistribution license recorded, so public releases should cite canonical URLs and publish metadata or short excerpts rather than full copied source bodies unless permission or an explicit license is obtained. The GitHub-safe `postmortem-public/` derivative redacts local paths, excludes raw transcripts, keeps `.claude/settings.local.json` visible as a conventional public path, and publishes citation-only external source notes. Repository artifact references in the postmortem use commit-specific GitHub fork permalinks where the source file was tracked at the tagged baseline; local-only sources are flagged as such. Postmortem conversation counts are local Codex session-source counts; finer-grained user/Codex turns are represented as sequenced exchanges.

The contribution-modes assessment treats Codex as strongest in Explorer, Builder, Refiner, and Verifier work; useful with human steering in Framer, Architect, and Experience Shaper work; assistant-only in Security Steward work; and not autonomous for Operator work. The security baseline for any production continuation is Secure by Design, GOV.UK Service Standard point 9, the Technology Code of Practice, NCSC secure development guidance, CAF outcomes, ICO data protection by design/default, NIST SSDF, and OWASP web/CI guidance.

The public sharing default is to link LinkedIn and event posts to the repository root, then use `START-HERE.md` as the reader guide for fast, time-based, and persona-based routes through the evidence pack.

The HMRC talk narrative pack is now partially built. Its import milestone represents all 13 sidecar/inventory files previously present in `research/hmrc-beyond-hype/import/`: 50 PowerPoint slides, 20 PDF pages, 3 standalone PNG files, the AI Coding Assistants Markdown/DOCX briefing pair, two audio sources represented through transcript notes, and the ClawPilot Markdown source. The generated sidecars use OCR or PDF text extraction with explicit caveats, so they are navigation and review aids rather than authoritative replacements for the imported sources. `AI-Native_Engineering_Blueprint.pptx` has 15 slides; the broader AI-native material also includes a 20-page PDF, a workflow PNG, and the AI Coding Assistants briefing. The 2026-05-12 demo release adds the selected presentation deck `beyond_hype_coding_assistants_public_sector_engineering.pptx` as an intentionally published raw PPTX, linked from the research and narrative entry points but not converted into sidecars in this pass. The AI Coding Assistants 9 May 2026 briefing is now decomposed into nine section-level notes and cross-linked from the talk arc, topic index, Q&A prep route, and SeeLinks datapack. The generated SeeLinks datapack currently adds 234 card items, 10 facets, 9 collections, 285 graph nodes, and 2984 graph edges over that narrative material, selected Challenge 2 evidence, relevant conversation traces, and the original SeeLinks UI reference. The ClawPilot / OpenClaw sidebar uses `research/hmrc-beyond-hype/import/clawpilot.md` as the local source-of-record and treats the shared ChatGPT thread as context, with current product/internal-adoption claims marked for rechecking before live use.

Obsidian `.obsidian/` directories are local browsing state by default and are ignored throughout the repository. Previously tracked Challenge 2 Obsidian settings remain tracked until explicitly removed from Git, but new Obsidian workspace folders should not create repository changes.

## Evaluation And Audit Assumptions

- The Challenge 2 benchmark Markdown is the scoring source of truth for questions, gold answers, and rubrics.
- Evaluation runs record the exact client invocation context: selected model or alias, reasoning effort where supported, model-selection source, model reference URL/date, executable paths, version-command output, repository commit/branch/tag/dirty state, benchmark SHA-256, and detected macOS Copilot desktop app versions.
- Current best-model policy is explicit `gpt-5.4` with `xhigh` effort for Codex, explicit `gpt-5.4` with the local Challenge 2 Wiki MCP server for Codex-with-MCP, explicit Gemini 3.1 Pro Preview where deterministic model selection is required, DSIT-managed local Claude Code settings expected to route to Opus 4.6 with `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` for gateway compatibility, staff-confirmed `gpt-5.4` with `xhigh` effort for GitHub Copilot CLI despite contradictory public docs, and Microsoft 365 Copilot Chat GPT-5 with optional visible `Think Deeper` UI mode selection for the Microsoft Copilot UI client.
- `--clients full` expands to Codex, Codex with MCP, Gemini CLI, Claude Code, GitHub Copilot CLI, and Microsoft Copilot UI coverage.
- GitHub Copilot CLI requires the standalone `copilot` binary, authentication, and organisation/subscription policy access before non-dry runs; the local `gh` wrapper alone is not treated as proof that Copilot CLI is installed, and policy denials are recorded as `policy_blocked`.
- Microsoft Copilot is included through a caveated Playwright web UI adapter because there is no stable headless local API for the installed desktop app. UI runs require an authenticated Playwright profile and may break when Microsoft changes selectors, loading states, tenant policies, or model routing. The adapter can attempt a visible GPT mode selection such as `Think Deeper`, but Microsoft Copilot still has no local filesystem tools in this harness; the Microsoft client config therefore uses public GitHub `v1.1` wiki permalinks and copied source excerpts for deterministic source grounding. A versioned OneDrive or SharePoint copy of the wiki remains a possible manual Microsoft-native fallback if GitHub access fails, but it must be validated with a smoke run because Microsoft file grounding depends on selected files, permissions, indexing, and product limits.
- Evaluated agents are instructed to use only `challenge-2/wiki/`, `challenge-2/wiki/data/`, and `challenge-2/AGENTS.md`.
- Evaluated agents are explicitly instructed not to inspect `challenge-2/wiki/evaluation-benchmark.md` or `challenge-2/evaluation/` while answering, because those paths contain gold answers or scoring material.
- Harness run artifacts are written under `challenge-2/evaluation/runs/<run-id>/` and ignored by git.
- The local MCP layer records source access when clients use its wiki search/read tools, but direct filesystem reads by a CLI client cannot be proven from the harness alone.
- The `codex-mcp` path records source access through `raw/codex-mcp/<question>.mcp-audit.jsonl`; noninteractive Codex requires approval bypass for MCP tool calls, but the MCP server itself remains read-only and path-scoped.
- `codex-mcp` prompt seeding and answer-time MCP tool calls must share the same server configuration. In particular, `semantic_model_id` is forwarded into the spawned `wiki_mcp_server.py` args as well as the precomputed context pack, and non-stdio server transport is rejected for Codex-spawned MCP because Codex expects a stdio MCP process.
- The completed `validated-full-20260419T2225Z` evaluation gives effective `100/100` completed rows for Codex, Codex with MCP, Claude, and Microsoft Copilot after applying the explicit `codex-mcp` Q057 correction run. Gemini CLI completed `36/100` rows before `gemini-3.1-pro-preview` returned quota exhaustion, and GitHub Copilot CLI remains `policy_blocked`.
- The same effective answer set now has a rubric-scored quality leaderboard using the benchmark's human-written rubrics. The score artifacts are public-safe summaries; raw prompts, raw answers, UI captures, and full generated scoring sheets remain external run evidence rather than committed repository content.
- MCP byte-budget fields are byte limits, not character limits. Context packs and source-note readers must truncate by UTF-8 bytes, especially for Welsh and other non-ASCII material. JSON-RPC notifications are no-response messages; HTTP transport returns `204 No Content` for them rather than a JSON result envelope. MCP request handlers must validate that incoming JSON-RPC requests are objects and that `params` / `arguments` envelopes are objects before reading fields, so malformed or batch-style client traffic returns a protocol error instead of terminating the session.
- Challenge 2 evaluation repo-state metadata should be best-effort: missing Git records `git_available: false` rather than aborting an evaluation run. Repository maintenance scripts that require Git should fail with a clear missing-Git message instead of an unhandled traceback.
- Evaluation runs can reuse a `run_id` while debugging, so live client execution must remove any pre-existing assistant-response artifact before invoking the client. Comparison/reporting tools should treat partially written MCP audit JSONL as degraded evidence by skipping and counting malformed lines, not by aborting the whole report.
- MCP servers that accept a configurable challenge root must use that root consistently for both tool calls and resource reads.
- Wiki MCP HTTP runs that specify `--bearer-token-env` must fail fast if the named environment variable is unset or empty. Anonymous local HTTP remains an explicit choice only when the bearer-token option is omitted.
- Public comparison metrics must not retain machine-local executable paths, app paths, run roots, repository roots, or home-relative paths. Sanitized metrics use placeholders while raw manifests remain in external run evidence.
- Wiki MCP retrieval modes are expected to be side-effect scoped: lexical mode does not build semantic vectors, semantic mode does not run lexical scoring, and hybrid mode is the only path that combines both engines.
- The audit format follows the same DSAP principles used in the related `mcp-geo` server audit work: event ledger, evidence register, source register, audit card, integrity manifest, redaction manifest, visible transcript, and zipped bundle.

## Documentation Lockstep

Documentation is part of the product. Any meaningful change should update the relevant tracking files:

- `Changelog.md` for what changed.
- `Context.md` for changed assumptions, architecture, or constraints.
- `Progress.md` for changed status, blockers, validation, or next steps.
- `README.md` or challenge briefs for user-facing changes.

The changelog keeps `Unreleased` for genuinely pending work only. Merged, tagged, or demo-published work should move into dated sections so repository readers are not left with a permanent backlog of already-published changes.

This rule is enforced through `AGENTS.md`, `.github/pull_request_template.md`, `tools/check_documentation_lockstep.py`, and the Documentation Lockstep GitHub Actions workflow. The check fails if required tracking files are missing or if meaningful changes omit a tracking-file update.
