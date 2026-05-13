---
exchange_id: "EX-0090"
title: "We won't use SharePoint but check if we can use my personal OneDrive, it seems as though it has "
source_id: "CONV-005"
global_sequence: 90
session_sequence: 38
user_timestamp: "2026-04-19T18:06:39.953Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0090. We won't use SharePoint but check if we can use my personal OneDrive, it seems as though it has

Previous: [EX-0089](0089-20260418065216-just-the-copilots.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0091](0091-20260418065216-any-good-giving-the-share-link.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
We won't use SharePoint but check if we can use my personal OneDrive, it seems as though it has only just completed uploading from the synced folder
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T18:06:43.264Z`

````text
I’ll re-run the strict OneDrive-only Microsoft Copilot smoke now that upload has completed, still without GitHub links or injected wiki excerpts. If it remains invisible, the next distinction is whether M365 Copilot can see Personal OneDrive at all from the signed-in account.
````

### Response 2 (commentary)

- Timestamp: `2026-04-19T18:06:51.980Z`

````text
The retry is running against the Microsoft web UI. I’m keeping this one as a direct Personal OneDrive discovery test so the result tells us whether upload/indexing fixed the issue, not whether prompt injection can paper over it.
````

### Response 3 (final_answer)

- Timestamp: `2026-04-19T18:08:03.084Z`

````text
I retried after the upload completed, using a strict Microsoft Copilot prompt with no GitHub links and no copied wiki excerpts.

Result: still not usable directly from Personal OneDrive.

Microsoft Copilot completed the run and selected `Think Deeper`, but returned:

```json
{
  "question_id": "Q001",
  "status": "cannot_access_onedrive_folder",
  "answer": "I can’t locate or open any files/folder named \"Challenge 2 Wiki v1.1 - M365 Grounding\" under Obsidian in your personal OneDrive from this Copilot session...",
  "cited_sources": [],
  "caveats": "Searches for the exact folder name and close variants returned no matching vault files/folder..."
}
```

Artifact path:
`/tmp/challenge2-wiki-eval-versioning/copilot-onedrive-direct-smoke-after-upload`

So the conclusion is sharper now: even after sync/upload, the M365 Copilot session we are automating cannot discover that Personal OneDrive folder by name. That likely means the signed-in M365 Copilot work/chat context is not indexing or authorized against your Personal OneDrive content.

What still works:
- Microsoft Copilot via M365 web works with the current GitHub permalink + copied excerpt strategy.
- Personal OneDrive may still work if files are explicitly attached through the Copilot file picker, but it is not reliable as an automatically searchable knowledge base from this session.

For the benchmark, I would not use Personal OneDrive discovery as the grounding mechanism. The next personal-OneDrive-only option would be to create a compact source pack, attach the key files directly in Copilot, and smoke test whether the UI accepts those attachments.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0089](0089-20260418065216-just-the-copilots.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0091](0091-20260418065216-any-good-giving-the-share-link.md)
