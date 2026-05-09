# Appendix A: Methods

## Purpose

This research pack prepares a 15-20 minute HMRC Beyond the Hype talk plus Q&A on the transition from AI coding assistants to coding agents. It combines external research with repo-local evidence from the AI Engineering Lab Challenge 2 Codex build.

## Scope

Included:

- 2021 to May 2026 evolution of coding assistants and agents
- empirical evidence on productivity, quality, and security risks
- capability and benchmark interpretation
- public-sector operating model and controls
- Challenge 2 repo case study

Excluded:

- procurement recommendation for any single tool
- claim that the repo is production-ready
- assurance for real HMRC data
- unverified transcript claims
- raw private conversation material

## Evidence Grades

| Grade | Meaning | Examples |
|---|---|---|
| A | Primary or high-reliability source for the claim | peer-reviewed or arXiv research papers, official government guidance, repo-local committed artefacts |
| B | Primary vendor or product source | official product announcements and documentation |
| C | Secondary source or weakly verified source | credible commentary, conference talk, or indirect summary |
| D | Excluded or not used for substantive claims | marketing-only material, unsourced comparison posts, unverifiable anecdotes |

## Repository Extraction Method

The repo-local evidence pass inspected:

- operating rules: `AGENTS.md`, `challenge-2/AGENTS.md`
- project tracking: `README.md`, `Context.md`, `Progress.md`, `Changelog.md`
- Challenge 2 wiki artefacts under `challenge-2/wiki/`
- workbench runbook and UI tests under `challenge-2/workbench/`
- evaluation runbooks and committed reports under `challenge-2/evaluation/`
- reports under `output/doc/`
- public postmortem under `postmortem-public/`

Local claims in the main outputs cite a local path and then a GitHub permalink to the exact line where possible.

## External Source Discovery Method

The external pass started from the prompt-kit seed list, then verified official product announcements, research papers, benchmark papers, government guidance, and security guidance using web search and direct page opens. The source register records date, evidence grade, supported claim, limitation, and use section.

## Validation Method

The pack is validated by:

- checking that all deliverables named in `research/hmrc-beyond-hype-prompt-kit/prompts/00_master_prompt.md` exist
- checking source-register CSV parsing
- checking repo-local claims have path-plus-permalink citations where practical
- updating lockstep repository docs
- running `python3 tools/check_documentation_lockstep.py`
- running `git diff --check`

## Limitations

- The research pack is a talk-preparation artefact, not an independent audit.
- Product capabilities can change quickly; current product statements were checked on 2026-05-09.
- Some vendor announcements are useful for timeline and capability framing but are not independent evidence of productivity or safety.
- Repo evidence is strong for what this prototype did, but does not prove production readiness.
- The Challenge 2 fixture data is synthetic, so real HMRC data would require separate data protection, security, and operational assurance.
