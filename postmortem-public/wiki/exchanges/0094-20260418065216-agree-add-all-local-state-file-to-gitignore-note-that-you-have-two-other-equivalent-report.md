---
exchange_id: "EX-0094"
title: "Agree, add all [LOCAL_STATE_FILE] to gitignore. Note that you have two other equivalent reports, the docx"
source_id: "CONV-005"
global_sequence: 94
session_sequence: 42
user_timestamp: "2026-04-19T20:37:01.069Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0094. Agree, add all [LOCAL_STATE_FILE] to gitignore. Note that you have two other equivalent reports, the docx

Previous: [EX-0093](0093-20260418065216-create-codex-postmortem-wiki.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0095](0095-20260418065216-continue-and-include-the-lint-check-after-the-links-have-been-resolved-ensure-extensive-cr.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Agree, add all [LOCAL_STATE_FILE] to gitignore. Note that you have two other equivalent reports, the docx and pdf. Consider the Karpathy Gist, which is localised, as this has a proposed structure specifically for research.

We also need to accomodate the implementation within this folder structure after deciding on an implementation and any reference implementations or specifications as submodules to simplify access. We should also consider adding things like the MCP specification and exemplars onto the wiki in an updateable way. Preserve licensing of all these sources. Do we need a plan at this stage or shall we create this wiki first, for example, with all the candidates chosen to support our SOTA Wiki implementation
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T20:37:11.524Z`

````text
I’ll inspect the Karpathy gist citation note and the current ignore/docs rules, then I’ll create the first MCP Research Wiki scaffold with source/register structure, license-aware placeholders, and links to the existing report variants. I’ll avoid vendoring specs or candidate repos yet; the scaffold can define how we add them safely as submodules or snapshots once licenses are verified.
````

### Response 2 (commentary)

- Timestamp: `2026-04-19T20:37:33.850Z`

````text
I agree we should create the wiki scaffold now rather than wait for a longer plan. The scaffold itself will hold the plan, source/register rules, licensing posture, and future implementation/submodule layout, so the next implementation decision has a clear home.
````

### Response 3 (commentary)

- Timestamp: `2026-04-19T20:37:42.755Z`

````text
I found the existing public Karpathy gist note is citation-only with a private archive hash, which is exactly the licensing posture we should reuse here: cite specs and exemplars, preserve license metadata, and do not copy bodies unless the license and update mechanism are clear. I’m going to add the MCP research wiki skeleton, source/candidate registers, and cleanup rules now.
````

### Response 4 (commentary)

- Timestamp: `2026-04-19T20:39:53.346Z`

````text
The MCP research wiki scaffold is now in place with a separate source boundary, report index, candidate register, future implementation area, and reference/specification policy. I’m updating the repo overview and tracking docs next so documentation lockstep reflects the new wiki and [LOCAL_STATE_FILE] policy.
````

### Response 5 (commentary)

- Timestamp: `2026-04-19T20:40:34.943Z`

````text
The local `[LOCAL_STATE_FILE]` files outside `.git` are removed and the ignore rule now covers nested Finder metadata going forward. I’m validating the new JSON registers, documentation lockstep, and whitespace now, then I’ll record those validation results in `Progress.md`.
````

### Response 6 (commentary)

- Timestamp: `2026-04-19T20:41:02.193Z`

````text
The scaffold and validation are complete. I’m doing a quick diff review now, then I’ll commit this as the first checkpoint on the MCP research branch.
````

### Response 7 (final_answer)

- Timestamp: `2026-04-19T20:41:33.978Z`

````text
Created the MCP research wiki first, which I think is the right move. It now carries the plan, source/register rules, candidate set, licensing posture, and reserved implementation structure so we can build from a controlled information architecture rather than a loose plan.

Committed on `codex/wiki-mcp-research`:

`b62a1cd Add MCP research wiki scaffold`

Key additions:
- [MCP research wiki index]([LOCAL_REPO]/challenge-2/MCP-Wiki/index.md)
- [Operating rules]([LOCAL_REPO]/challenge-2/MCP-Wiki/AGENTS.md)
- [Implementation plan]([LOCAL_REPO]/challenge-2/MCP-Wiki/implementation-plan.md)
- [Security model]([LOCAL_REPO]/challenge-2/MCP-Wiki/security-model.md)
- [Candidate register]([LOCAL_REPO]/challenge-2/MCP-Wiki/candidate-register.md)
- Source notes for Karpathy methodology, MCP specs, GitHub candidates, Microsoft Copilot MCP, and academic literature
- Machine-readable source and candidate registers
- Reserved folders for `implementation/`, `specifications/`, and `references/external/`

I preserved all three report variants:
- Markdown
- DOCX
- PDF

The source register records their hashes and sizes. The Karpathy gist is handled as citation-only, matching the prior licensing posture: no full public copy unless permission or an explicit license appears.

I also updated `.gitignore` for nested `[LOCAL_STATE_FILE]` and AppleDouble metadata, and removed `[LOCAL_STATE_FILE]` files outside `.git`.

Validation passed:
- `python3 -m json.tool challenge-2/MCP-Wiki/data/source-register.json`
- `python3 -m json.tool challenge-2/MCP-Wiki/data/candidate-register.json`
- `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
- `python3 tools/check_documentation_lockstep.py`
- `git diff --check`
- Confirmed no `[LOCAL_STATE_FILE]` files remain outside `.git`

Next sensible steps are to normalize the Deep Research citation markers into durable links/source-register entries, then choose which MCP specs or candidate repos should become licensed submodules under `challenge-2/MCP-Wiki/references/external/`.

Working tree is clean.

::git-stage{cwd="[LOCAL_REPO]"}
::git-commit{cwd="[LOCAL_REPO]"}
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0093](0093-20260418065216-create-codex-postmortem-wiki.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0095](0095-20260418065216-continue-and-include-the-lint-check-after-the-links-have-been-resolved-ensure-extensive-cr.md)
