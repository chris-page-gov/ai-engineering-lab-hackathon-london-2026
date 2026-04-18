---
exchange_id: "EX-0016"
title: "Do a review on how far we meet the evaluation/judging criteria?"
source_id: "CONV-002"
global_sequence: 16
session_sequence: 14
user_timestamp: "2026-04-16T11:16:03.975Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0016. Do a review on how far we meet the evaluation/judging criteria?

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-002 (Karpathy Wiki Planning and Challenge 2 Vault Build)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Do a review on how far we meet the evaluation/judging criteria?
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-16T11:16:16.127Z`

````text
I’ll assess this against the actual criteria in the repo rather than guessing. I’m going to find the judging/evaluation notes first, then compare them to the Challenge 2 knowledge-base implementation and call out gaps.
````

### Response 2 (commentary)

- Timestamp: `2026-04-16T11:16:22.889Z`

````text
I found that the repository does not publish a detailed scoring rubric; the closest official criteria are in the README, the Challenge 2 brief, and the existing review note’s proposed public-sector prototype tests. I’m reading those now and will make the assessment explicit about what is official versus inferred.
````

### Response 3 (commentary)

- Timestamp: `2026-04-16T11:16:33.363Z`

````text
The official brief is light on a numeric rubric, so I’ll judge against the stated outcomes: working demo, user/problem clarity, extraction and schema, query/search, provenance, AI-tool evidence, safe data, and believable next steps. I’m checking the generated wiki artefacts and validation outputs before scoring.
````

### Response 4 (commentary)

- Timestamp: `2026-04-16T11:16:52.755Z`

````text
The rebuild still passes strictly: 43 sources, 81 notes, 0 lint issues. It may have refreshed generated timestamps/log locally during the check, so I’m checking the working tree and will keep the review separate from any accidental local churn.
````

### Response 5 (commentary)

- Timestamp: `2026-04-16T11:17:01.107Z`

````text
The strict rebuild only changed generated lint timestamps and appended a log entry. Since this was just part of the assessment, I’m going to remove that local churn and leave the pre-existing Obsidian workspace drift untouched.
````

### Response 6 (commentary)

- Timestamp: `2026-04-16T11:17:28.608Z`

````text
The only remaining local churn from my validation is exact newline/blank-line differences in generated files. I’m restoring those two generated files to HEAD, scoped only to the files I touched during the check.
````

### Response 7 (final_answer)

- Timestamp: `2026-04-16T11:17:58.755Z`

````text
**Overall Assessment**

Against the published Challenge 2 brief, this is a strong prototype: roughly **8/10 for the challenge outcome**, with the main weakness being that it is a navigable Obsidian knowledge base rather than a dedicated search/Q&A user interface.

The repo does not include a detailed judging rubric. The official criteria I found are: build a working prototype, show a complete user journey, explain how AI tools shaped the work, and for Challenge 2 specifically show extracted/structured documents, a way to query or search them, and a clear explanation of who benefits. See [README.md]([LOCAL_REPO]/README.md) and [challenge-02-unlocking-the-dark-data.md]([LOCAL_REPO]/challenge-02-unlocking-the-dark-data.md).

**Where We’re Strong**

| Criterion | Assessment |
|---|---:|
| Working prototype | Strong |
| Challenge 2 fit | Strong |
| Source coverage | Very strong |
| Metadata/provenance | Very strong |
| Findability/navigation | Strong |
| Query/search experience | Partial |
| Demo readiness | Strong |
| Responsible data handling | Good, but must be explained |
| Evidence of AI-assisted engineering | Partial |
| Next-step credibility | Good |

The strongest part is coverage and provenance. The wiki processes all **43 Challenge 2 sources**: 20 structured files and 23 unstructured files. It produces **43 source notes**, **14 topic pages**, **14 entity pages**, **5 maps**, workbook exports, a source register, and lint reports. The generated architecture page makes this easy to explain: [challenge-2/wiki/architecture.md]([LOCAL_REPO]/challenge-2/wiki/architecture.md).

The implementation also hits the brief’s “dark data” problem well. It handles HTML, Markdown, TXT, PDF, DOCX and XLSX; preserves raw source links; adds normalised metadata; captures tables; links related documents; and flags stale, superseded, draft and past-review material. The strict build currently reports **43 sources, 81 notes, 0 lint issues**.

**Best Judging Story**

The strongest story is:

> “We turned a messy departmental document dump into a repeatable, provenance-first knowledge base that humans can browse in Obsidian and machines can consume through JSON. It preserves the raw sources, adds structure and metadata, flags stale or risky documents, and gives citizens/advisers/developers a path to find the right content faster.”

That maps cleanly to the Challenge 2 users:
- Citizen: can be pointed to direct source-backed answers rather than a 60-page PDF.
- Frontline adviser: can find current/stale/draft guidance quickly.
- Developer/service team: gets structured Markdown/JSON outputs.
- Policy owner: gets source register, lint, versioning and flags.

**Main Gaps**

The biggest gap is **no dedicated query/search UI**. Obsidian search, graph, backlinks, maps and topic pages are a valid navigable knowledge layer, but the brief explicitly says a good outcome includes “a way to query or search that content.” Judges may expect a visible search box or Q&A workflow. Obsidian can do this manually, but a small `wiki/demo-answers.md` or simple search page would make it more judge-proof.

The second gap is that topic pages are mostly generated aggregation pages, not fully curated answer pages. For example, the demo question “Which Council Tax Reduction guidance is current?” is routed to the Council Tax Reduction topic, but the wiki does not yet give a crisp, top-level answer like “DOC-HB-009 is current; DOC-HB-003 is stale/conflicted.” The information is present, but the judge has to follow the trail.

The third gap is judging evidence. The product shows a lot of AI-assisted engineering discipline, but there is no concise evidence page saying: what AI helped with, what was human-reviewed, what was mocked, what checks were run, and what would happen next. That matters because the event judges also ask how AI tools shaped the work.

**Risk Notes**

The synthetic staff directory is now correctly marked as synthetic fixture data, with no redaction. That is aligned with your instruction and the Challenge 2 synthetic corpus. In the demo, say this explicitly before a judge raises it.

Some metadata remains `unknown` for unstructured files. That is acceptable because the source data is messy, but it should be framed as an honest finding: the system preserves raw metadata, normalises what it can, and flags what needs policy-owner review.

**What Would Improve The Score Fastest**

1. Add a prominent `wiki/demo-answers.md` answering the five official demo questions with source-backed links.
2. Add a tiny search/query interface, even a static HTML page or CLI script, that returns matching notes and source links.
3. Add `wiki/judging-evidence.md`: user, problem, prototype scope, AI-tool use, validation checks, limitations, 30/90/180-day next steps.
4. Tighten grammar in index counts: “1 source” rather than “1 sources” in topic/entity lists.
5. Add a few deterministic tests around `linkify`, metadata extraction, and source coverage so the build proof is not only `--strict`.

**Bottom Line**

This would likely score well for Challenge 2 because it solves the core problem in the right architectural direction: extraction, structure, provenance, versioning and navigability. It is weaker as a polished end-user product because it relies on Obsidian rather than a bespoke search/Q&A interface. For judging, I would present it as an **infrastructure-first prototype** with a credible path to search/chat, not as a finished citizen-facing service.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.
