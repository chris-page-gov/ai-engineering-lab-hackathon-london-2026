# Appendix E: Import Resource Review

Review date: 2026-05-11.

The folder `research/hmrc-beyond-hype/import/` is a local source drop for the HMRC AI Agents talk. It contains useful briefing material, generated visual assets, slide decks, a PDF source deck, and audio files. The raw folder is large, so this review distinguishes tracked text sources and generated transcript outputs from local-only media.

## Inventory

| File | Type | Size | Extracted signal | Current treatment |
|---|---:|---:|---|---|
| `AI coding assistants on 9 May 2026 for the HMRC Data Science Academy talk.md` | Markdown briefing | 40 KB | Strong market map, tool-category framing, evidence tables, Q&A material, source links. | Track as lightweight source input. |
| `AI coding assistants on 9 May 2026 for the HMRC Data Science Academy talk.docx` | Word document | 27 KB | Same briefing content in DOCX form. | Keep local unless formatted DOCX is needed. |
| `AI-Native-Engineering-Team-source_openAI.pdf` | PDF | 7.8 MB | 20-page deck on AI-native engineering across plan, design, build, test, review, document, deploy, maintain. | Keep local; cite only after source/provenance decision. |
| `Governing_AI_Engineering.pptx` | PowerPoint | 15 MB | 12-slide generated/source deck; simple OOXML text extraction found no text, likely image-heavy. | Keep local; visual review needed before reuse. |
| `Dark_Data_Blueprint.pptx` | PowerPoint | 13 MB | 13-slide generated/source deck; simple OOXML text extraction found no text, likely image-heavy. | Keep local; visual review needed before reuse. |
| `AI-Native_Engineering_Blueprint.pptx` | PowerPoint | 17 MB | 15-slide generated/source deck; simple OOXML text extraction found no text, likely image-heavy. | Keep local; visual review needed before reuse. |
| `Challenge_2_Unlocking_Dark_Data.pptx` | PowerPoint | 15 MB | 10-slide generated/source deck; simple OOXML text extraction found no text, likely image-heavy. | Keep local; visual review needed before reuse. |
| `AI Coding Assistants 2026 Evolution.png` | PNG | 4.3 MB | 2752 x 1536 visual asset. | Keep local; use only after visual and licence/provenance review. |
| `AI Benchmark Mastery Scoring Guide.png` | PNG | 4.5 MB | 2752 x 1536 visual asset. | Keep local; use only after visual and licence/provenance review. |
| `AI-Native Engineering Team Workflow.png` | PNG | 4.8 MB | 2752 x 1536 visual asset. | Keep local; use only after visual and licence/provenance review. |
| `Governing_agentic_AI_in_software_engineering.m4a` | Audio | 37 MB | 20.2-minute audio. | Keep raw audio local; commit generated transcript, SRT, and speaker-attributed draft. |
| `Engineering_Accountability_in_Public_Sector_AI.m4a` | Audio | 36 MB | 19.8-minute audio. | Keep raw audio local; commit generated transcript, SRT, and speaker-attributed draft. |

## Usable Additions To The Talk Spine

- Use a category-first market map rather than a vendor-first comparison.
- Explain the workflow shift as `assistant + agent + review + controls`.
- Treat enterprise/government control layers as a distinct adoption category.
- Add a clearer failure-mode section: unsafe commands, context drift, over-editing, brittle tool use, noisy review, and false reassurance.
- Strengthen the pilot design question: which task types, for which users, in which repos, under which controls, improve cycle time without increasing review burden or risk?
- Consider CodeScaleBench as a candidate benchmark source for large-codebase and multi-repo evaluation, but verify it before adding it to the formal source register.

## Publication Decision

Raw media in `research/hmrc-beyond-hype/import/` is intentionally ignored by default. The repository should commit distilled Markdown notes, validated source references, and final deliverables rather than large generated decks, screenshots, audio, or duplicate DOCX/PDF inputs unless they are explicitly selected for publication.

The committed transcript set under `research/hmrc-beyond-hype/transcripts/` includes base Whisper text, SRT timings, pyannote diarization segment CSV, a diarization report, and `Trace` / `Query` voice-name Markdown/TXT drafts. The raw `.m4a` files remain local import sources.

## Follow-Up Work

1. Validate the imported Markdown briefing's external links and dates.
2. Promote verified new sources into `01_source_register.csv`, especially Microsoft developer workflows, Gemini Code Assist, Cursor, Windsurf, Sourcegraph Cody, JetBrains AI/Junie/Air, Devin Enterprise, and CodeScaleBench where evidence is strong enough.
3. Visually review the PPTX/PNG assets before using them in slides.
4. Review the two machine-generated speaker-attributed transcripts against the source audio before quoting them publicly.
5. Decide whether the final HMRC deliverable should be a slide deck, speaker notes pack, or both.
