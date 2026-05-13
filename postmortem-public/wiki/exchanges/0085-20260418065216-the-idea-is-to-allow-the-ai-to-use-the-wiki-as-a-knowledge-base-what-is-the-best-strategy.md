---
exchange_id: "EX-0085"
title: "The idea is to allow the AI to use the Wiki as a knowledge base - what is the best strategy for "
source_id: "CONV-005"
global_sequence: 85
session_sequence: 33
user_timestamp: "2026-04-19T17:27:16.134Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0085. The idea is to allow the AI to use the Wiki as a knowledge base - what is the best strategy for

Previous: [EX-0084](0084-20260418065216-if-github-access-fails-for-the-m365-copilot-can-we-just-have-the-wiki-replicated-in-onedri.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0086](0086-20260418065216-another-thought-there-is-now-a-copilot-desktop-app-on-the-mac-what-can-this-do-should-we-c.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
The idea is to allow the AI to use the Wiki as a knowledge base - what is the best strategy for this on the M365 Copilot? Is there a Wiki M365 MCP server for example?
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T17:27:25.313Z`

````text
I’ll check the current Microsoft documentation rather than rely on memory here, because Copilot grounding and MCP support have been changing quickly. I’ll focus on official Microsoft sources and then map the options back to our Challenge 2 wiki/evaluation needs.
````

### Response 2 (final_answer)

- Timestamp: `2026-04-19T17:28:23.264Z`

````text
Best strategy: use SharePoint-backed Copilot agents first, and use MCP only if we need deterministic, auditable retrieval beyond what SharePoint grounding gives us.

For this project, I would do it in this order.

**1. Publish an M365 source pack to SharePoint**
Create a versioned SharePoint site/library, for example:

`Challenge 2 Wiki Evaluation v1.1`

Put a Copilot-friendly copy of the wiki there. I would not rely on raw Markdown alone. Microsoft’s supported file lists are strongest around Office docs, PDF, TXT, HTML, RTF, and similar web/document formats, so generate a parallel pack from `challenge-2/wiki/`:

- `index.html` or `index.txt`
- `architecture.html`
- `source-register.txt` or `.xlsx`
- one HTML/TXT file per source/topic/entity note
- optionally a consolidated PDF/DOCX source pack for the core navigation and operating schema

Keep the pack versioned and hash it so we can prove which wiki state Copilot was grounded on.

**2. Create a SharePoint Agent or Microsoft 365 declarative agent**
For quick, Microsoft-native grounding, create an agent from the SharePoint document library or folder. Microsoft says SharePoint agents are scoped to selected sites/pages/files and respect user permissions. They can also be used from Microsoft 365 Copilot Chat and Teams once shared.

This is the best fit for “let M365 Copilot use the wiki as a knowledge base” because it uses the Microsoft 365 semantic index, permissions, labels, and file grounding. Microsoft’s own guidance says SharePoint is ideal for static or structured knowledge bases.

Important constraints:

- SharePoint agents currently have source-count limits, so source at folder/library/site level where possible.
- Agent Builder supports SharePoint files/folders/sites and up to 100 SharePoint files for some agent configurations.
- New files can take several minutes to become ready.
- Agent Builder can prioritize specified sources, but Microsoft says it does not fully block general AI knowledge; for stricter control, use Copilot Studio.

**3. Use Copilot Studio if we need stricter control**
If the benchmark must be closer to “wiki-only,” Copilot Studio is the better authoring surface than the basic M365 Agent Builder. It supports knowledge sources, authentication, and stricter orchestration. It also supports tools, including MCP.

This matters because our evaluation needs source discipline, not just helpful answers.

**4. MCP is possible, but not the first move**
There is not, from the Microsoft docs I found, a generic first-party “M365 Wiki MCP server” that you point at a Markdown folder.

But Copilot Studio can connect an agent to an existing MCP server. Current Microsoft docs say Copilot Studio supports MCP via Streamable transport, with API key or OAuth options. It does not mean our existing local `challenge-2/tools/wiki_eval_mcp.py` can be plugged in directly, because that script is stdio-style local MCP. For M365 we would need to wrap or rebuild it as a hosted HTTPS Streamable MCP server.

That MCP server could expose tools like:

- `search_wiki(query, filters)`
- `read_wiki_note(path_or_source_id)`
- `get_source_register()`
- `build_context_pack(question)`
- `record_evidence(question_id, cited_sources)`

This would be valuable for audited retrieval and DSAP evidence, but it is heavier: hosting, auth, tenant configuration, tool descriptions, and smoke tests. I would treat it as phase 2.

**Recommended Path**
For the benchmark:

1. Generate an M365 source pack from the wiki into supported formats.
2. Upload it to a versioned SharePoint library.
3. Create a SharePoint/M365 Copilot agent scoped to that library or folder.
4. Give it instructions: answer only from the Challenge 2 wiki pack, cite source filenames/source IDs, say when the answer is not found.
5. Run Q001 smoke test manually and through the Playwright adapter.
6. If grounding or citation quality is not adequate, build the hosted MCP wrapper around our wiki search/read layer.

So yes, MCP is available in the M365/Copilot Studio ecosystem, but for this use case the most Microsoft-native knowledge-base strategy is SharePoint plus a scoped agent. MCP becomes the right answer when we need controlled retrieval, richer audit logs, or a source-access protocol that behaves like our local wiki evaluation harness.

Sources checked:
- [Copilot Studio MCP server connection](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent)
- [Declarative agent best practices](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-best-practices)
- [Add knowledge sources to M365 Copilot declarative agents](https://learn.microsoft.com/ko-kr/microsoft-365/copilot/extensibility/agent-builder-add-knowledge)
- [Declarative agent manifest knowledge capabilities](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-manifest-1.0)
- [Create an agent in SharePoint](https://support.microsoft.com/en-us/office/create-an-agent-in-sharepoint-d16c6ca1-a8e3-4096-af49-67e1cfdddd42)
- [SharePoint agent FAQ](https://support.microsoft.com/en-us/office/frequently-asked-questions-about-copilot-in-sharepoint-eb1b7668-3d98-4a93-98ef-f0c6dfc694f0)
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Implemented and validated user-facing workbench behavior.

Previous: [EX-0084](0084-20260418065216-if-github-access-fails-for-the-m365-copilot-can-we-just-have-the-wiki-replicated-in-onedri.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0086](0086-20260418065216-another-thought-there-is-now-a-copilot-desktop-app-on-the-mac-what-can-this-do-should-we-c.md)
