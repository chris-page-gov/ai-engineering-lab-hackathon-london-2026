# Context

## Repository Purpose

This fork is Team DSIT A's working Challenge 2 implementation and evidence pack from the AI Engineering Lab Hackathon London 2026. It keeps the original event briefs and starter material, but its primary purpose is now to document, demonstrate, evaluate, and critique the "Unlocking the dark data" prototype.

The original repository was an event pack for a one-day AI-assisted engineering hackathon. This fork is a worked example of how AI coding assistants can help build a source-backed LLM Wiki, browser workbench, MCP/evaluation harness, delivery report, public postmortem, and security assessment for a government-style dark-data problem.

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

## Data Assumptions

- Challenge starter data is synthetic unless the relevant challenge brief says otherwise.
- Challenge 2 staff-directory names, emails, phone-like values, roles, and identifiers are synthetic fixture data and should not be redacted for the demo.
- Real secrets, credentials, local filesystem paths, and provenance gaps remain review issues.
- Raw files under Challenge 2 source folders should not be edited, renamed, moved, or normalised as part of wiki generation.

## Important Paths

- `README.md`: fork overview, Challenge 2 value proposition, start points, repository map, validation summary, and original hackathon context.
- `Changelog.md`: dated change history.
- `Context.md`: project context, architecture assumptions, and operating constraints.
- `Progress.md`: current status, validation, blockers, and next steps.
- `AGENTS.md`: repo-wide operating rules and documentation lockstep policy.
- `tools/check_documentation_lockstep.py`: local and CI check that required tracking docs exist and move with meaningful changes.
- `challenge-2/AGENTS.md`: Challenge 2 LLM Wiki operating schema.
- `challenge-2/tools/build_wiki.py`: repeatable Challenge 2 wiki builder.
- `challenge-2/evaluation/README.md`: Challenge 2 wiki evaluation harness runbook.
- `challenge-2/tools/run_wiki_eval.py`: CLI harness for sending benchmark questions to Codex, Gemini CLI, and Claude Code.
- `challenge-2/tools/wiki_eval_mcp.py`: stdio MCP-compatible audit layer for controlled wiki read/search and answer recording.
- `challenge-2/tools/summarise_wiki_eval.py`: leaderboard summariser for scored harness runs.
- `challenge-2/tools/workbench_mcp.py`: stdio MCP server for Dark Data Workbench source search, source read, and context export.
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

Dark Data Workbench controls expose active visual state for users and pressed-state metadata for automation/accessibility. Playwright tests assert the active UI state for facet, saved-check, and view-mode controls because those controls drive the visible corpus, evidence, and export context. The workbench also carries a user-entered question through Browser AI JSON, copied prompts, and Markdown evidence bundles so exported evidence remains tied to the question it is meant to answer.

The Challenge 2 demonstration guide is the recommended walkthrough for showing the complete prototype. It ties the source corpus, Obsidian wiki, SeeLinks-style workbench, Browser AI export, evaluation benchmark, harness outputs, and audit/FOI record back to the `Unlocking_Dark_Data.pdf` slide narrative and benchmark scoring guide.

The Codex postmortem source archive is evidence material, not automatically publication-ready content. Conversation transcripts may include local paths, screenshots, private workflow details, local assistant configuration references, and dynamic third-party source snapshots. The localized Karpathy X/gist copies have no explicit redistribution license recorded, so public releases should cite canonical URLs and publish metadata or short excerpts rather than full copied source bodies unless permission or an explicit license is obtained. The GitHub-safe `postmortem-public/` derivative redacts local paths, excludes raw transcripts, keeps `.claude/settings.local.json` visible as a conventional public path, and publishes citation-only external source notes. Repository artifact references in the postmortem use commit-specific GitHub fork permalinks where the source file was tracked at the tagged baseline; local-only sources are flagged as such. Postmortem conversation counts are local Codex session-source counts; finer-grained user/Codex turns are represented as sequenced exchanges.

The contribution-modes assessment treats Codex as strongest in Explorer, Builder, Refiner, and Verifier work; useful with human steering in Framer, Architect, and Experience Shaper work; assistant-only in Security Steward work; and not autonomous for Operator work. The security baseline for any production continuation is Secure by Design, GOV.UK Service Standard point 9, the Technology Code of Practice, NCSC secure development guidance, CAF outcomes, ICO data protection by design/default, NIST SSDF, and OWASP web/CI guidance.

Obsidian workspace files such as `challenge-2/.obsidian/workspace.json` are local session state, not shared vault configuration. They are ignored and left on disk locally so using Obsidian does not repeatedly create repository changes.

## Evaluation And Audit Assumptions

- The Challenge 2 benchmark Markdown is the scoring source of truth for questions, gold answers, and rubrics.
- Evaluation runs record the exact client invocation context: selected model or alias, reasoning effort where supported, model-selection source, model reference URL/date, executable paths, version-command output, repository commit/branch/tag/dirty state, benchmark SHA-256, and detected macOS Copilot desktop app versions.
- Current best-model policy is explicit `gpt-5.4` with `xhigh` effort for Codex, Gemini CLI `auto` routing without passing `--model`, Claude Code `best` with `max` effort, staff-confirmed `gpt-5.4` with `xhigh` effort for GitHub Copilot CLI despite contradictory public docs, and Microsoft 365 Copilot Chat GPT-5 automatic routing for the Microsoft Copilot UI client.
- `--clients full` expands to Codex, Gemini CLI, Claude Code, GitHub Copilot CLI, and Microsoft Copilot UI coverage.
- GitHub Copilot CLI requires the standalone `copilot` binary, authentication, and organisation/subscription policy access before non-dry runs; the local `gh` wrapper alone is not treated as proof that Copilot CLI is installed, and policy denials are recorded as `policy_blocked`.
- Microsoft Copilot is included through a caveated Playwright web UI adapter because there is no stable headless local API for the installed desktop app. UI runs require an authenticated Playwright profile and may break when Microsoft changes selectors, loading states, tenant policies, or model routing. The adapter can attempt a visible GPT mode selection such as `Think Deeper`, but Microsoft Copilot still has no local filesystem tools in this harness; scored runs require explicit context injection if answers must be grounded in local wiki content.
- Evaluated agents are instructed to use only `challenge-2/wiki/`, `challenge-2/wiki/data/`, and `challenge-2/AGENTS.md`.
- Evaluated agents are explicitly instructed not to inspect `challenge-2/wiki/evaluation-benchmark.md` or `challenge-2/evaluation/` while answering, because those paths contain gold answers or scoring material.
- Harness run artifacts are written under `challenge-2/evaluation/runs/<run-id>/` and ignored by git.
- The local MCP layer records source access when clients use its wiki search/read tools, but direct filesystem reads by a CLI client cannot be proven from the harness alone.
- The audit format follows the same DSAP principles used in the related `mcp-geo` server audit work: event ledger, evidence register, source register, audit card, integrity manifest, redaction manifest, visible transcript, and zipped bundle.

## Documentation Lockstep

Documentation is part of the product. Any meaningful change should update the relevant tracking files:

- `Changelog.md` for what changed.
- `Context.md` for changed assumptions, architecture, or constraints.
- `Progress.md` for changed status, blockers, validation, or next steps.
- `README.md` or challenge briefs for user-facing changes.

This rule is enforced through `AGENTS.md`, `.github/pull_request_template.md`, `tools/check_documentation_lockstep.py`, and the Documentation Lockstep GitHub Actions workflow. The check fails if required tracking files are missing or if meaningful changes omit a tracking-file update.
