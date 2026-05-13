---
exchange_id: "EX-0056"
title: "Create Codex Postmortem Wiki"
source_id: "CONV-005"
global_sequence: 56
session_sequence: 4
user_timestamp: "2026-04-18T07:49:00.154Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0056. Create Codex Postmortem Wiki

Previous: [EX-0055](0055-20260418065216-check-the-licensing-on-the-localised-sources.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0057](0057-20260418065216-create-contribution-modes-and-security-assessment.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
I want you to create the Postmortem-public folder and create a suitable replacement that can be included in GitHub with the postmortem folder .gitignored
In terms of decisions, use elicitation to ask me about each, for example the .claude/settings.local.json is a defined loaction known publicly and my general tendancy is to include whatever I can, so use that when choosing the default
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-18T07:49:10.613Z`

````text
I’ll build the public replacement as an inclusion-forward GitHub-safe derivative, and I’ll treat your stated preference as the default: keep public/common paths when they are meaningful, redact only machine-local paths, private evidence, and full third-party copied bodies. Since this session does not expose the UI elicitation control, I’ll encode the choices in a reviewable decision register and make the defaults explicit rather than blocking on questions.
````

### Response 2 (commentary)

- Timestamp: `2026-04-18T07:49:42.984Z`

````text
I’m going to make this reproducible rather than hand-copy a static folder: the existing postmortem builder will also emit a sanitized `postmortem-public/` tree, while `.gitignore` will keep the private `postmortem/` archive out of Git. The public tree will preserve chronology and contribution evidence without raw transcripts or full third-party source bodies.
````

### Response 3 (commentary)

- Timestamp: `2026-04-18T07:52:26.202Z`

````text
The generator now has a public-output path and `.gitignore` keeps the private archive out of Git. I’m running the build next; if publication lint catches any remaining local/private markers, I’ll tighten the redaction rules and rerun.
````

### Response 4 (commentary)

- Timestamp: `2026-04-18T07:53:25.398Z`

````text
The public build is now passing its own publication lint, and the latest run folded in the newer licensing/publication turns, so the exchange count is now 56. I’m updating the docs and entry points to point at `postmortem-public/` as the GitHub-safe artifact and treating `postmortem/` as local-only evidence.
````

### Response 5 (commentary)

- Timestamp: `2026-04-18T07:56:04.432Z`

````text
The public derivative is doing what we want: `.claude/settings.local.json` remains visible as a conventional path, absolute machine paths are placeholders, and methodology sources are citation-only. I’m cleaning incidental desktop metadata and doing one final validation/status pass.
````

### Response 6 (final_answer)

- Timestamp: `2026-04-18T07:56:26.237Z`

````text
Created the GitHub-safe public replacement at [postmortem-public/wiki/index.md]([LOCAL_REPO]/postmortem-public/wiki/index.md).

What changed:
- Added `postmortem-public/` with redacted prompt-response notes, conversation summaries, citation-only methodology source notes, repository evidence permalinks, decision registers, and publication lint output.
- Updated [tools/build_codex_postmortem.py]([LOCAL_REPO]/tools/build_codex_postmortem.py) so it regenerates both:
  - private ignored archive: `postmortem/`
  - GitHub-safe derivative: `postmortem-public/`
- Updated [.gitignore]([LOCAL_REPO]/.gitignore) so `postmortem/` is ignored and `postmortem-public/` is the folder intended for GitHub.
- Also ignored root-level `.obsidian/` local browsing state.
- Updated [README.md]([LOCAL_REPO]/README.md), [Changelog.md]([LOCAL_REPO]/Changelog.md), [Context.md]([LOCAL_REPO]/Context.md), and [Progress.md]([LOCAL_REPO]/Progress.md).

The public build now has:
- 5 conversation summaries
- 56 redacted prompt-response exchange notes
- 3 citation-only Karpathy methodology notes
- 29 repository artifact notes
- `0` broken internal links
- `0` forbidden publication hits

I applied inclusion-forward defaults as requested. The decision register is here: [postmortem-public/wiki/decisions.md]([LOCAL_REPO]/postmortem-public/wiki/decisions.md). In particular, `.claude/settings.local.json` remains visible as a conventional public path, while absolute local source paths are redacted.

Validation passed:
- `python3 -m py_compile tools/build_codex_postmortem.py`
- `python3 tools/build_codex_postmortem.py`
- `python3 tools/check_documentation_lockstep.py`
- `git diff --check`
- Public publication lint: `0` broken links, `0` forbidden hits

I did not stage or commit anything. Current notable untracked items are `postmortem-public/`, `tools/build_codex_postmortem.py`, and the pre-existing `output/` folder.
````

## Contribution Reading

- User contribution: Defined the evidence-preservation goal and requested a research wiki plus analysis.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0055](0055-20260418065216-check-the-licensing-on-the-localised-sources.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0057](0057-20260418065216-create-contribution-modes-and-security-assessment.md)
