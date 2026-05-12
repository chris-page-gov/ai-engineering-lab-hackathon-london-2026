# HMRC Talk Narrative Wiki Goal

## Purpose

Create a navigable narrative pack for the HMRC Beyond the Hype talk that can be shared as a GitHub link during or after the session.

The pack should turn the current research material, imported AI-generated slides, imported images, imported PDFs, and transcripts into a short, focused, keyword-classified, highly interlinked Markdown corpus. The result should work like a small wiki: readers should be able to start from one obvious entry point, follow the narrative arc, inspect supporting material, and jump by topic.

This file is the durable replacement for the attempted `/goal` command. Future Codex work on the talk should treat this as the active goal until it is explicitly superseded.

## Table Of Contents

- [Purpose](#purpose)
- [Current Status](#current-status)
- [Source Inputs](#source-inputs)
- [Target Output](#target-output)
- [Narrative Arc](#narrative-arc)
- [Slide And Image Sidecars](#slide-and-image-sidecars)
- [SeeLinks Datapack](#seelinks-datapack)
- [SeeLinks UI Reference](#seelinks-ui-reference)
- [Navigation And Readability](#navigation-and-readability)
- [Scope](#scope)
- [Tagging](#tagging)
- [Definition Of Done](#definition-of-done)
- [Verification Plan](#verification-plan)
- [Publication Approach](#publication-approach)

## Current Status

Status: import-inventory, sidecar, SeeLinks datapack, original SeeLinks UI-reference, and semantic validation milestones complete; full editorial curation still in progress.

The narrative wiki now has a GitHub-browsable scaffold, visual sidecars, source notes, full import inventory, coverage reports, derived image assets, a SeeLinks-style datapack, original SeeLinks UI infographics, a structural validation report, and a semantic lint report. Large imported binary/audio/PDF/PPTX materials remain local by default unless explicitly selected for publication. The 2026-05-12 demo release explicitly selects [beyond_hype_coding_assistants_public_sector_engineering.pptx](../import/beyond_hype_coding_assistants_public_sector_engineering.pptx) as the public presentation deck.

## Source Inputs

Use the existing committed research pack:

- `research/hmrc-beyond-hype/00_research_brief.md`
- `research/hmrc-beyond-hype/01_source_register.csv`
- `research/hmrc-beyond-hype/02_timeline_ai_software_engineering.md`
- `research/hmrc-beyond-hype/03_empirical_evidence_productivity.md`
- `research/hmrc-beyond-hype/04_agentic_coding_capabilities.md`
- `research/hmrc-beyond-hype/05_security_governance_public_sector.md`
- `research/hmrc-beyond-hype/06_repo_case_study_codex_build.md`
- `research/hmrc-beyond-hype/07_operating_model_for_public_sector_engineering.md`
- `research/hmrc-beyond-hype/appendices/`
- `research/hmrc-beyond-hype/transcripts/`

Also inspect the local import drop in `research/hmrc-beyond-hype/import/`, including:

- `beyond_hype_coding_assistants_public_sector_engineering.pptx`, the selected 2026-05-12 presentation deck and explicit raw-binary publication exception
- `AI-Native_Engineering_Blueprint.pptx`
- `Challenge_2_Unlocking_Dark_Data.pptx`
- `Dark_Data_Blueprint.pptx`
- `Governing_AI_Engineering.pptx`
- `AI-Native-Engineering-Team-source_openAI.pdf`
- imported PNG images
- the imported AI-generated Markdown briefing
- the imported AI-generated DOCX briefing companion
- `clawpilot.md`, the local ClawPilot / OpenClaw research brief used for the current agentic-workplace sidebar
- imported audio sources, represented through committed transcripts and audio source notes

Do not commit raw imported binary/audio/PDF/PPTX material unless the user explicitly selects it for publication. Prefer committed derivatives that are small, reviewable, and useful on GitHub. The current explicit exception is the selected presentation deck linked above.

## Target Output

Build a committed folder of text and image artefacts under `research/hmrc-beyond-hype/narrative/`.

Expected structure:

- `index.md`: the obvious entry point for the talk link.
- `overview.md`: a one-page explanation of the whole story.
- `narrative-arc.md`: the coherent beginning-to-end argument for the talk.
- `topics.md`: topic list with links into all relevant notes.
- `source-materials.md`: publication-safe register of the imported source assets and derived artefacts.
- `notes/import-inventory.md`: one explicit narrative treatment for every file in the import folder.
- `slides/`: one Markdown sidecar per slide or major image, with publication-safe image derivatives where appropriate.
- `notes/`: short, focused wiki notes for concepts, claims, risks, tools, workflow patterns, and Q&A themes.
- `assets/`: checked-in image derivatives that are intentionally publishable on GitHub.
- `data/`: machine-readable navigation, topic, source, structural-validation, semantic-lint, and link-check outputs if useful.
- `seelinks/pack.json`: generated datapack for browsing the narrative through Dark Data Workbench as cards, facets, graph nodes, and source-note links.
- `notes/seelinks-web-ui-reference.md`: generated infographic-backed reference for the original SeeLinks web UI.

The exact structure may evolve, but the final result must preserve the entry point, overview, topic navigation, asset register, and coherent narrative path.

## Narrative Arc

The story should be complete and coherent:

1. Start with the public-sector dark-data problem: guidance exists, but it is hard to find, structure, trust, and reuse safely.
2. Explain the shift from typing code to steering agents: intent, context, constraints, review, and validation become the work.
3. Use the Challenge 2 Codex build as the concrete case study: generated wiki, Dark Data Workbench, provenance, evaluation harness, MCP tooling, and postmortem evidence.
4. Show what AI coding agents are good at: exploration, scaffolding, refactoring, test generation, documentation, evidence packaging, and validation support.
5. Draw the boundary: no autonomous security sign-off, no production operation, no policy ownership, no high-sensitivity data decisions without approved controls.
6. Give teams a safe first step: low-risk internal material, repo rules, immutable raw data, small changes, tests, diffs, decision records, and no trust in fluent output without evidence.
7. Close with the practical lesson: the productivity gain comes from disciplined workflow as much as model capability.

## Slide And Image Sidecars

Status: complete for the current `research/hmrc-beyond-hype/import/` visual inventory as of 2026-05-11.

Coverage achieved:

- The 13 top-level import files present at sidecar-generation time are represented in [notes/import-inventory.md](notes/import-inventory.md); the 2026-05-12 presentation deck is linked there as a raw-PPTX publication exception.
- 4 imported PowerPoint decks: 50 slide sidecars.
- 1 imported PDF: 20 page sidecars.
- 3 imported standalone PNG files: 3 image sidecars.
- Total: 73 visual items, 73 Markdown sidecars, and 73 small derived image assets.
- The AI Coding Assistants Markdown/DOCX pair is represented by [notes/ai-coding-assistants-market-briefing.md](notes/ai-coding-assistants-market-briefing.md) plus nine section-level notes.
- The two imported audio files are represented by [notes/engineering-accountability-audio.md](notes/engineering-accountability-audio.md) and [notes/governing-agentic-ai-audio.md](notes/governing-agentic-ai-audio.md), with transcript links.
- Coverage report: [data/visual_coverage.md](data/visual_coverage.md).
- Validation report: [data/narrative_validation_report.md](data/narrative_validation_report.md).
- Semantic lint report: [data/narrative_semantic_lint_report.md](data/narrative_semantic_lint_report.md).
- Obvious entry point: [index.md](index.md).
- Source-material register: [source-materials.md](source-materials.md).
- Topic navigation: [topics.md](topics.md).

The sidecars were generated with `research/hmrc-beyond-hype/tools/build_narrative_sidecars.py` and validated with `research/hmrc-beyond-hype/tools/validate_narrative_sidecars.py --write-report`. The structural validator checks item coverage against the actual PPTX/PDF/PNG counts, Markdown link integrity, orphaned narrative Markdown files, inbound links to sidecars, asset references, required sidecar metadata, and staged raw-import binaries. The semantic linter `research/hmrc-beyond-hype/tools/lint_narrative_semantics.py --check-external --write-report` adds stale-claim detection, count contradiction detection, missing concept/page detection, and live external-link revalidation.

The local `clawpilot.md` import has also been incorporated into [notes/clawpilot-project-lobster.md](notes/clawpilot-project-lobster.md), with the shared ChatGPT thread treated as context rather than final evidence.

Scope note: `AI-Native_Engineering_Blueprint.pptx` contains 15 slides. The broader import folder contains additional AI-native material, including the 20-page `AI-Native-Engineering-Team-source_openAI.pdf`, the `AI-Native Engineering Team Workflow.png` image, and the AI Coding Assistants Markdown/DOCX briefing; those are separate import files with their own narrative treatments.

For each material point illustrated by every imported PowerPoint slide, PDF page, and standalone image:

- create a Markdown sidecar file;
- describe the visual in enough detail that a reader can understand the point without opening the binary source;
- identify the claim or narrative function of the visual;
- link to the relevant research note, transcript excerpt, source-register item, or repo artefact;
- assign stable tags;
- record publication status and any caveat;
- include a small, publishable image derivative only when appropriate.

Do not silently alter source meaning while creating sidecars. If OCR, screenshot extraction, or AI image description is uncertain, mark the uncertainty in the sidecar.

## SeeLinks Datapack

Status: complete for the current narrative corpus as of 2026-05-11.

The narrative can also be loaded in Dark Data Workbench using the HMRC narrative pack link:

```text
challenge-2/workbench/?pack=hmrc-narrative
```

The generated pack is [seelinks/pack.json](seelinks/pack.json), with a short generated summary at [seelinks/README.md](seelinks/README.md). It contains 234 items, 10 facets, 9 collections, 285 graph nodes, and 2984 graph edges.

The pack casts the net across the whole talk-prep corpus: slide and image sidecars, curated narrative notes, HMRC research files, transcripts and diarization reports, selected Challenge 2 repo evidence, and relevant postmortem conversation traces. Each item includes a local source-note link where possible so cards open inside the workbench rather than becoming dead ends.

Primary bounded facets are:

- `Source Family`
- `Narrative Stage`
- `Talk Section`
- `Asset Type`
- `Evidence Role`
- `Governance Theme`
- `Topic Group`
- `Provenance Mode`
- `Screenfulls`
- `Tags`

Dark Data Workbench supports the SeeLinks-style card flow for this pack: slide thumbnails, source cards, keep marked, dismiss marked, restore dismissed, reader links, graph view, and drag-a-facet-name-to-the-card-grid colouring. Category facets use high-contrast pastel fills; `Screenfulls` is treated as a measure and uses a graded colour scale.

## SeeLinks UI Reference

Status: complete for the current original SeeLinks source snapshot as of 2026-05-11.

The original SeeLinks interface is documented in [notes/seelinks-web-ui-reference.md](notes/seelinks-web-ui-reference.md). That note links four generated SVG infographics:

- [Web UI anatomy](assets/infographics/seelinks-web-ui-anatomy.svg)
- [Facet and tile interaction model](assets/infographics/seelinks-facet-tile-interactions.svg)
- [Views, detail surfaces, and output tools](assets/infographics/seelinks-views-detail-output.svg)
- [Data, state, and export flow](assets/infographics/seelinks-data-state-flow.svg)

These infographics are generated by `research/hmrc-beyond-hype/tools/build_seelinks_ui_infographics.py` from the observed original SeeLinks documentation and Svelte UI source. They are intended as the visual specification for bringing the HMRC workbench UI closer to the original SeeLinks interaction model.

## Navigation And Readability

The narrative should be readable by screenfuls. Long index-like pages need a table of contents at the top and should offer high-level routes before dense item lists.

Backlinks should be applied selectively:

- curated HMRC talk research notes and transcript notes should link back to the narrative;
- imported source files should generally remain source evidence, not navigation pages;
- Challenge 2 source evidence should be reached through [notes/challenge-2-worked-example.md](notes/challenge-2-worked-example.md) rather than by turning every generated Challenge 2 wiki page into an HMRC talk page;
- the policy is recorded in [notes/navigation-and-scope.md](notes/navigation-and-scope.md).

## Scope

The narrative includes all current import-folder material at source-treatment level: every file is represented in the import inventory, and every imported visual has a sidecar.

The AI Coding Assistants 9 May 2026 briefing is included through [notes/ai-coding-assistants-market-briefing.md](notes/ai-coding-assistants-market-briefing.md), the tracked Markdown source, the DOCX extraction check, companion visuals, and nine short section-level notes:

- [Executive summary](notes/ai-coding-assistants-executive-summary.md)
- [Market map](notes/ai-coding-assistants-market-map.md)
- [Productivity evidence](notes/ai-coding-assistants-productivity-evidence.md)
- [Failure modes](notes/ai-coding-assistants-failure-modes.md)
- [Public-sector controls](notes/ai-coding-assistants-public-sector-controls.md)
- [Repo case study](notes/ai-coding-assistants-repo-case-study.md)
- [Talk track](notes/ai-coding-assistants-talk-track.md)
- [Q&A prep](notes/ai-coding-assistants-q-and-a.md)
- [Source register and validation limits](notes/ai-coding-assistants-source-register.md)

The Challenge 2 worked example is included as the concrete case-study route through [notes/challenge-2-worked-example.md](notes/challenge-2-worked-example.md), linked sidecar decks, and selected Challenge 2 wiki/workbench/evaluation evidence.

## Tagging

Use concise lowercase tags. Candidate tags:

- `agentic-coding`
- `ai-assistants`
- `auditability`
- `challenge-2`
- `codex`
- `dark-data`
- `evaluation`
- `governance`
- `hmrc`
- `mcp`
- `operating-model`
- `provenance`
- `public-sector`
- `risk-boundaries`
- `security`
- `source-backed-answers`
- `talk-demo`
- `traceability`
- `validation`
- `workflow`

Add new tags only when they improve navigation.

## Definition Of Done

This goal is complete only when all of the following are true:

- The narrative folder has an obvious entry point.
- There is an index, an overview, a topic list, and a coherent narrative arc.
- Every committed narrative note is reachable from `index.md` through normal Markdown links.
- There are no orphaned Markdown files in the narrative corpus.
- All internal Markdown links are valid.
- All local file references resolve.
- All GitHub links resolve, including line anchors where used.
- The semantic lint report has no hard errors for stale-claim caveating, documented-count contradictions, missing required concepts/pages, or live external-link validation.
- Every published image or slide derivative has a sidecar note.
- Every material point from each imported PPTX, PDF, and standalone image is described in text.
- Every file in `research/hmrc-beyond-hype/import/` has an explicit narrative treatment.
- Sidecars include tags, source attribution, publication status, and caveats.
- Raw imported binaries remain ignored unless explicitly selected for publication.
- The pack can be browsed directly on GitHub without requiring local tooling.
- `Changelog.md`, `Context.md`, and `Progress.md` are updated in lockstep.
- Validation output is recorded in `Progress.md`.

## Verification Plan

Before marking the goal complete, run or create validation that checks:

- Markdown link integrity across `research/hmrc-beyond-hype/narrative/`.
- Orphan detection for all narrative Markdown files.
- Required files exist: `index.md`, `overview.md`, `topics.md`, `narrative-arc.md`, and `source-materials.md`.
- Every sidecar has tags, source path, publication status, and at least one inbound link.
- Every checked-in asset is referenced by at least one sidecar.
- No ignored raw import files are accidentally staged.
- Semantic lint passes with `python3 research/hmrc-beyond-hype/tools/lint_narrative_semantics.py --check-external --write-report`.
- Documentation lockstep passes with `python3 tools/check_documentation_lockstep.py`.
- Whitespace validation passes with `git diff --check`.

If a validation helper is added, prefer a reproducible script under `research/hmrc-beyond-hype/tools/` and record its output in `Progress.md`.

## Publication Approach

The default publication route is GitHub Markdown, not a local-only slide deck. The narrative should be useful from a plain browser link and should avoid depending on proprietary local viewers.

Use small derived images only where they make the narrative clearer. Prefer text descriptions and links for claims. Do not publish raw binary sources, generated decks, audio, or PDFs unless the user explicitly approves that publication decision.
