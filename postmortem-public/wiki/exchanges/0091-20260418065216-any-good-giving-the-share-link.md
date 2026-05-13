---
exchange_id: "EX-0091"
title: "Any good giving the share link?"
source_id: "CONV-005"
global_sequence: 91
session_sequence: 39
user_timestamp: "2026-04-19T18:32:28.654Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0091. Any good giving the share link?

Previous: [EX-0090](0090-20260418065216-we-won-t-use-sharepoint-but-check-if-we-can-use-my-personal-onedrive-it-seems-as-though-it.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0092](0092-20260418065216-update-deep-research-prompt.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Any good giving the share link?
https://1drv.ms/f/c/3a8a1639d535209f/IgBISe9eQpbZSaIWNEca0Gu_AdxmmLShQ0txBkbstn3cmus?e=7UWXbX
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T18:32:45.548Z`

````text
A share link is worth testing because it changes the problem from “can M365 search my Personal OneDrive index?” to “can Copilot open this explicit cloud source?” I’ll run a strict Microsoft Copilot smoke with only that shared OneDrive folder link, and I’ll also check whether the link resolves publicly from the local machine.
````

### Response 2 (commentary)

- Timestamp: `2026-04-19T18:32:48.854Z`

````text
The link resolves to a OneDrive folder redirect, but unauthenticated curl gets `403`, so it is not a simple public fetch for the harness. I’m still testing it in the signed-in M365 Copilot session, because that may have access where curl does not.
````

### Response 3 (commentary)

- Timestamp: `2026-04-19T18:32:58.132Z`

````text
The shared-link smoke is running. If it succeeds, we’ll have a Personal OneDrive route that does not depend on folder-name indexing; if it fails, the share link alone is not enough for the M365 web UI client.
````

### Response 4 (final_answer)

- Timestamp: `2026-04-19T18:34:04.498Z`

````text
I tested the share link. It does not solve the M365 Copilot grounding problem.

Local link check:
- The `1drv.ms` link redirects to OneDrive.
- Unauthenticated `curl` gets `403`, so it is not a simple public folder fetch.

Microsoft Copilot smoke:
- Mode: `Think Deeper` selected successfully.
- Prompt used only the shared OneDrive folder link, with no GitHub links and no copied excerpts.
- Result: `cannot_access_onedrive_share_link`.

Copilot’s captured answer said it could not retrieve files or folder contents from the shared link, likely because the link is outside its Microsoft 365 data context, requires auth, is not indexed/visible to the connector, or cannot be opened by its file tools.

Artifact path:
`/tmp/challenge2-wiki-eval-versioning/copilot-onedrive-share-link-smoke`

So: useful experiment, but no for the benchmark. A Personal OneDrive share link is not a reliable knowledge-base strategy for M365 Copilot Chat in this setup.

Current viable options are:

1. Continue with the proven GitHub permalink plus copied excerpt strategy.
2. Attach a compact source pack directly in the Copilot UI, if the UI supports it in this session.
3. Use the Microsoft Copilot Mac app as a separate manually-attached-file client, clearly labelled as not the M365 knowledge-base route.
4. Build a hosted MCP/HTTP retrieval layer later if we need true controlled wiki access.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0090](0090-20260418065216-we-won-t-use-sharepoint-but-check-if-we-can-use-my-personal-onedrive-it-seems-as-though-it.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0092](0092-20260418065216-update-deep-research-prompt.md)
