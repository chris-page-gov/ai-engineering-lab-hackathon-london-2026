---
exchange_id: "EX-0018"
title: "Add tracking files to the repo, Changelog.md (best practice change tracking showing dated change"
source_id: "CONV-002"
global_sequence: 18
session_sequence: 16
user_timestamp: "2026-04-16T11:26:49.500Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0018. Add tracking files to the repo, Changelog.md (best practice change tracking showing dated change

Previous: [EX-0017](0017-20260416084939-fix-obsidian-mermaid-architecture-diagram.md) | Conversation reader: [start-to-finish](../readers/conv-002-karpathy-wiki-planning-and-challenge-2-vault-build.md) | Next: [EX-0019](0019-20260416084939-commit-push-and-pr-to-the-fork.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-002 (Karpathy Wiki Planning and Challenge 2 Vault Build)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Add tracking files to the repo, Changelog.md (best practice change tracking showing dated changes, additions etc) Context.md, Progress.md and enforce keeping all documentation up to date in lockstep
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-16T11:27:02.460Z`

````text
I’ll add the tracking docs at the repo root and make the lockstep documentation rule explicit so future changes have to update the tracker files, not just code. I’ll also fold in the Mermaid fix that is already in the working tree, while leaving the Obsidian workspace drift alone.
````

### Response 2 (commentary)

- Timestamp: `2026-04-16T11:27:11.471Z`

````text
I found only `challenge-2/AGENTS.md`, so there is no repo-wide operating rule yet. I’ll add a root `AGENTS.md`, the three tracking files, and a PR checklist so the lockstep rule is visible to both agents and reviewers.
````

### Response 3 (commentary)

- Timestamp: `2026-04-16T11:27:59.922Z`

````text
The tracking files and PR checklist are in place. I’m checking the new docs for ASCII hygiene and the lockstep references, then I’ll run the narrow validation for the existing Challenge 2 generator change.
````

### Response 4 (commentary)

- Timestamp: `2026-04-16T11:28:17.170Z`

````text
The current lockstep rule is visible, but to make “enforce” concrete rather than only advisory I’m adding a small check script plus a GitHub Actions workflow. The check will fail a PR if meaningful repo changes don’t update `Changelog.md`, `Context.md`, and `Progress.md` together.
````

### Response 5 (commentary)

- Timestamp: `2026-04-16T11:28:56.908Z`

````text
The lockstep check now has both a local script and a PR workflow. I’m validating the script and checking that the new files are clean Markdown/text, then I’ll report exactly what changed and what remains unstaged from Obsidian.
````

### Response 6 (commentary)

- Timestamp: `2026-04-16T11:29:02.539Z`

````text
The new lockstep check exposed one bug in itself: local mode was not counting untracked files, so newly added tracking docs looked “missing.” I’m fixing that so it works for fresh files before first commit as well as normal edits.
````

### Response 7 (commentary)

- Timestamp: `2026-04-16T11:29:24.769Z`

````text
The checks pass now. I’m making one small documentation pass so `Progress.md` records the validation I actually ran, which is part of the new lockstep standard.
````

### Response 8 (final_answer)

- Timestamp: `2026-04-16T11:29:50.421Z`

````text
Added the tracking and enforcement layer.

Created:
- [AGENTS.md]([LOCAL_REPO]/AGENTS.md): repo-wide operating rules, including documentation lockstep requirements.
- [Changelog.md]([LOCAL_REPO]/Changelog.md): dated change tracking using Added, Changed, Fixed, Documentation, Validation style sections.
- [Context.md]([LOCAL_REPO]/Context.md): project context, assumptions, data policy, key paths, and documentation rules.
- [Progress.md]([LOCAL_REPO]/Progress.md): current status, completed work, validation, open items, and next steps.
- [.github/pull_request_template.md]([LOCAL_REPO]/.github/pull_request_template.md): PR checklist requiring Changelog, Context, Progress, and source-data checks.
- [.github/workflows/documentation-lockstep.yml]([LOCAL_REPO]/.github/workflows/documentation-lockstep.yml): CI check for PRs.
- [tools/check_documentation_lockstep.py]([LOCAL_REPO]/tools/check_documentation_lockstep.py): local/CI enforcement script.

Updated:
- [README.md]([LOCAL_REPO]/README.md) now lists the tracking files in the included materials.
- Kept the previous Mermaid fix in [challenge-2/wiki/architecture.md]([LOCAL_REPO]/challenge-2/wiki/architecture.md) and [challenge-2/tools/build_wiki.py]([LOCAL_REPO]/challenge-2/tools/build_wiki.py).

Validation passed:
- `python3 tools/check_documentation_lockstep.py`
- `python3 -m py_compile tools/check_documentation_lockstep.py`
- `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
- `git diff --check`

No raw challenge source files were changed, and nothing was redacted from synthetic data. The only unrelated dirty file remains local Obsidian workspace state: `challenge-2/.obsidian/workspace.json`.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0017](0017-20260416084939-fix-obsidian-mermaid-architecture-diagram.md) | Conversation reader: [start-to-finish](../readers/conv-002-karpathy-wiki-planning-and-challenge-2-vault-build.md) | Next: [EX-0019](0019-20260416084939-commit-push-and-pr-to-the-fork.md)
