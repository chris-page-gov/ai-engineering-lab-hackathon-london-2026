---
exchange_id: "EX-0084"
title: "If GitHub access fails for the M365 Copilot, can we just have the Wiki replicated in OneDrive - "
source_id: "CONV-005"
global_sequence: 84
session_sequence: 32
user_timestamp: "2026-04-19T17:21:56.612Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0084. If GitHub access fails for the M365 Copilot, can we just have the Wiki replicated in OneDrive -

Previous: [EX-0083](0083-20260418065216-it-looked-like-the-microsoft-365-copilot-failed-because-the-prompt-specified.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0085](0085-20260418065216-the-idea-is-to-allow-the-ai-to-use-the-wiki-as-a-knowledge-base-what-is-the-best-strategy.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
If GitHub access fails for the M365 Copilot, can we just have the Wiki replicated in OneDrive - could it access that correctly
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T17:22:03.341Z`

````text
OneDrive is a better fit for Microsoft 365 Copilot than local paths or raw GitHub tree pages, because it can ground on Microsoft 365 content the signed-in account can access. I’m checking the current Microsoft smoke result and then I’ll map the practical OneDrive setup.
````

### Response 2 (commentary)

- Timestamp: `2026-04-19T17:22:24.450Z`

````text
Yes, OneDrive or SharePoint is likely the more reliable Microsoft-native grounding route than GitHub, especially if we reference files through Microsoft 365’s file picker/Context IQ or a Copilot Notebook. The caveat is that Copilot usually grounds on accessible files you select/reference, not “a folder” as an arbitrary local corpus.
````

### Response 3 (commentary)

- Timestamp: `2026-04-19T17:23:31.260Z`

````text
I’ll turn that OneDrive question into a concrete repo update, then validate the evaluation harness so the published docs match what we actually tested. The latest Microsoft smoke gave us a useful signal: GitHub permalinks plus embedded source excerpts worked, so OneDrive is an optional Microsoft-native fallback rather than the only path.
````

### Response 4 (commentary)

- Timestamp: `2026-04-19T17:23:53.546Z`

````text
I’m checking the touched files now and will keep the repo changes narrow: the harness should record the Microsoft access strategy, not just rely on a hand-run workaround. After that I’ll run the focused tests and documentation lockstep check.
````

### Response 5 (commentary)

- Timestamp: `2026-04-19T17:23:59.580Z`

````text
The working tree currently has only the harness/config edits unstaged; the tracking docs have not yet been updated for the GitHub-context Microsoft smoke. I’m going to add a small test around that prompt mode and then update the runbook/progress notes so the fallback decision is captured.
````

### Response 6 (commentary)

- Timestamp: `2026-04-19T17:24:27.640Z`

````text
I’m making two small implementation adjustments: the Microsoft prompt source text will not promise copied excerpts unless they are configured, and the tests will cover the permalink-plus-excerpt path. The docs will then describe OneDrive/SharePoint as a manual fallback with limits rather than a magic replacement for local filesystem access.
````

### Response 7 (commentary)

- Timestamp: `2026-04-19T17:25:37.073Z`

````text
The docs now record the practical answer: OneDrive/SharePoint can be used, but the evaluated path is GitHub permalinks plus explicit context excerpts because that is reproducible and already smoke-tested. I’m running the focused validation set next.
````

### Response 8 (commentary)

- Timestamp: `2026-04-19T17:25:47.487Z`

````text
The unit and lockstep checks passed. I’m doing one dry-run through the Microsoft configured path as a final sanity check, because the important part here is the exact prompt artifact that will be sent to the web UI.
````

### Response 9 (commentary)

- Timestamp: `2026-04-19T17:25:58.057Z`

````text
The dry-run prompt exposed one more class issue: even with GitHub sources, it still printed the local repository root as metadata. That is harmless for CLI clients but wrong for Microsoft Copilot, so I’m removing that local path from non-local prompt modes and adding a regression assertion.
````

### Response 10 (commentary)

- Timestamp: `2026-04-19T17:26:30.578Z`

````text
The regenerated Microsoft dry-run prompt now names the GitHub baseline instead of leaking the local repository root. I’m running the remaining final checks, then I’ll review the diff and commit the branch changes.
````

### Response 11 (commentary)

- Timestamp: `2026-04-19T17:26:44.957Z`

````text
The diff is scoped to the evaluation harness, Microsoft/Claude config, tests, and the required tracking docs. I’m staging and committing it now so the branch has a clean checkpoint before the full benchmark run.
````

### Response 12 (final_answer)

- Timestamp: `2026-04-19T17:27:16.093Z`

````text
Yes, but with constraints. Replicating the wiki into OneDrive/SharePoint is a better Microsoft-native fallback than giving Microsoft 365 Copilot local paths, but I would not treat a copied folder as automatically reliable evidence access.

Microsoft’s current docs say Copilot can ground on selected OneDrive/SharePoint files through Context IQ, and Copilot Notebooks can use curated references rather than the whole OneDrive. The caveats matter for our benchmark: OneDrive Q&A is file-selection based, folder Q&A has limits, and supported file formats are more Office/PDF/TXT-oriented than arbitrary Markdown trees. So the reliable pattern would be a versioned OneDrive/SharePoint source pack or Copilot Notebook, not just “copy `challenge-2/wiki/` and hope it finds everything.”

For this branch I implemented the safer immediate path: Microsoft Copilot now gets public `v1.1` GitHub wiki permalinks plus copied source excerpts from key wiki files, avoiding local filesystem paths. I also removed the local repo root from the Microsoft prompt mode after the dry-run exposed it.

Committed as `dac157e` on `codex/evaluation-versioning`.

Validated:
- `python3 -m py_compile challenge-2/evaluation/clients.py challenge-2/tools/run_wiki_eval.py tests/test_challenge2_eval_clients.py`
- `python3 -m unittest discover -s tests -p 'test_challenge2_eval*.py'`
- `python3 -m json.tool challenge-2/evaluation/client-config.example.json`
- `node --check challenge-2/tools/microsoft_copilot_playwright.mjs`
- `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
- `python3 tools/check_documentation_lockstep.py`
- `git diff --check`
- Microsoft configured dry-run prompt smoke confirmed no `[LOCAL_USER_PATH]` path in the prompt.

Relevant Microsoft references checked:
- [Context IQ file references in Microsoft 365 Copilot](https://support.microsoft.com/en-us/topic/using-context-iq-to-refer-to-specific-files-people-and-more-in-microsoft-365-copilot-and-copilot-chat-272ac2c1-c5f7-49c9-8a42-2a8a87846fa0)
- [How Microsoft 365 Copilot Notebooks works](https://support.microsoft.com/en-us/topic/how-microsoft-365-copilot-notebooks-works-4071d73d-8bdd-478f-8968-8dc1d7c3d43e)
- [FAQ about Copilot in OneDrive](https://support.microsoft.com/en-us/office/frequently-asked-questions-about-copilot-in-onedrive-1bd55d10-7c46-417c-ab3d-e9c7be346947)

Working tree is clean. GitHub Copilot CLI is still the remaining blocked client because of policy access; Microsoft Copilot is now ready to use the explicit GitHub/context path, with OneDrive as the documented fallback.

::git-stage{cwd="[LOCAL_REPO]"}
::git-commit{cwd="[LOCAL_REPO]"}
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Implemented and validated user-facing workbench behavior.

Previous: [EX-0083](0083-20260418065216-it-looked-like-the-microsoft-365-copilot-failed-because-the-prompt-specified.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0085](0085-20260418065216-the-idea-is-to-allow-the-ai-to-use-the-wiki-as-a-knowledge-base-what-is-the-best-strategy.md)
