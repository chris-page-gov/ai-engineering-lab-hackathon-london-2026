# Progress

## Current Status

The Challenge 2 Obsidian knowledge-base prototype is implemented and merged into the fork's `main` branch via fork-local PR #1.

The current local working branch also contains the Challenge 2 wiki evaluation benchmark, CLI harness, MCP-compatible audit layer, and scoring-sheet/leaderboard tooling for comparing Codex, Gemini CLI, and Claude Code against the generated wiki.

The current local working branch now also includes an end-to-end Challenge 2 demonstration guide that links the source corpus, Obsidian validation, SeeLinks-style workbench, Browser AI export, evaluation matrix/harness, and audit/FOI tracking into one walkthrough.

Dark Data Workbench now includes a question box so saved checks and Browser AI exports preserve the user question alongside the selected evidence.

The current local working branch also includes a linked and illustrated colleague report in Markdown and Word format that reconstructs the Challenge 2 realtime delivery sequence from the supplied hackathon write-up, repo history, logs, and Codex thread evidence.

The current local branch is `codex/postmortem-wiki`, with the committed Challenge 2 baseline tagged locally as `v1-challenge-2`. It now includes a private generated Codex collaboration postmortem archive under ignored `postmortem/` and a GitHub-safe public derivative under `postmortem-public/`. The latest generation covers five project conversations, 56 redacted prompt-response exchanges, three citation-only Karpathy methodology source notes, and repository artifacts linked to GitHub fork permalinks at the tagged baseline.

The postmortem artifacts have been reviewed for publication readiness. The review found no obvious credential-shaped secrets or email-address pattern hits in the postmortem scan, but it blocks public release until local paths, local assistant configuration references, copied third-party source bodies, private workflow references, and local-only evidence are redacted or repackaged. A follow-up license check found no explicit redistribution license in the localized Karpathy X/gist copies, so public releases should use citation metadata and short excerpts unless permission or an explicit license is obtained.

The attached contribution-modes proposal has been converted to Markdown under `output/doc/`, and a government-security assessment has been added. The assessment concludes that Codex was strongest for Explorer, Builder, Refiner, and Verifier work; useful with human steering for Framer, Architect, and Experience Shaper work; assistant-only for Security Steward work; and not suitable as an autonomous Operator for production government services.

`README.md` now presents this fork as Team DSIT A's Challenge 2 dark-data implementation and evidence pack, rather than as the original one-day event invitation.

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

## Validation

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
  - Generated private lint reports `5` conversation sources, `56` exchanges, `3` external sources, `29` repository artifact sources, and `0` broken internal links.
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

## Open Items

- Review the `postmortem-public/wiki/decisions.md` defaults before publishing externally.
- Address the security assessment findings before making any production-readiness claim: harden GitHub Actions permissions/action pinning, upgrade the low `cookie` advisory path, replace unsafe XML parsing for untrusted documents, constrain postmortem URL fetching, and define Secure by Design/DPIA/operational controls for real data.
- Add `challenge-2/wiki/demo-answers.md` with source-backed answers to the official demo questions.
- Run the full 100-question benchmark through the available Codex, Gemini CLI, and Claude Code installations, then fill the scoring sheet and publish the generated leaderboard.

## Next Recommended Steps

1. Run the full benchmark against Codex, Gemini CLI, and Claude Code using `challenge-2/tools/run_wiki_eval.py`.
2. Score `generated/scoring-sheet.csv` and generate `generated/leaderboard.md`.
3. Add source-backed demo answers for the five Challenge 2 demo questions.
4. Use Dark Data Workbench during the demo to show search, context export, and source-backed checks over the generated knowledge base.
