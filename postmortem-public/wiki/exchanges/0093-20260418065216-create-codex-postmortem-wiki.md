---
exchange_id: "EX-0093"
title: "Create Codex Postmortem Wiki"
source_id: "CONV-005"
global_sequence: 93
session_sequence: 41
user_timestamp: "2026-04-19T20:25:35.115Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0093. Create Codex Postmortem Wiki

Previous: [EX-0092](0092-20260418065216-update-deep-research-prompt.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0094](0094-20260418065216-agree-add-all-local-state-file-to-gitignore-note-that-you-have-two-other-equivalent-report.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Here is the Deep Research report '/challenge-2/MCP-Wiki/research/Challenge 2 Wiki MCP Server Research Report.md' and there are docx and pdf of the report
Consider whether this report should be incorporated into the postmortem Wiki to improve access for people and the AI, is this the right place? I'm thinking that the Category 2 Wiki is an alternative or in a new research Wiki but Karpathy may express a view on the need to separate and size
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T20:25:45.439Z`

````text
I’ll inspect the new research report and surrounding files, then I’ll check how the current Challenge 2 wiki and postmortem-public wiki are structured before recommending placement. I’ll keep this as an information-architecture decision first, unless the repo clearly needs a small index/link update.
````

### Response 2 (commentary)

- Timestamp: `2026-04-19T20:25:54.181Z`

````text
The research report is present as an untracked `challenge-2/MCP-Wiki/` folder, with Markdown, DOCX, and PDF versions. I’m checking the repo’s Karpathy-methodology notes next so the recommendation aligns with the LLM Wiki pattern rather than just file convenience.
````

### Response 3 (final_answer)

- Timestamp: `2026-04-19T20:26:12.559Z`

````text
Yes, this report should be made accessible to people and AI, but **not by folding it into the existing Challenge 2 generated wiki or the postmortem wiki as-is**.

My recommendation:

**Keep it as a new, separate MCP Research Wiki under `challenge-2/MCP-Wiki/`.**

That is the right boundary.

Why:

- `challenge-2/wiki/` is the **Challenge 2 knowledge base over the synthetic source corpus**. It is generated from the raw challenge documents and used for evaluation. Adding MCP implementation research there would mix product/source knowledge with meta-engineering research and risks confusing the benchmark surface.
- `postmortem-public/wiki/` is the **public evidence/postmortem wiki** explaining human/Codex collaboration and publication evidence. The MCP report is a forward-looking architecture/research artefact, not part of the original v1.1 delivery postmortem.
- `challenge-2/MCP-Wiki/` is already a good emerging boundary: it can become the “wiki about the wiki MCP server” without polluting either the Challenge 2 corpus or the postmortem archive.

This fits the Karpathy-style pattern already captured in the repo: keep raw/source evidence separate from the generated knowledge layer, give each wiki a clear purpose, and use explicit operating rules/index/log files so future agents know what corpus they are operating on.

**Suggested structure**
I would evolve the new folder into this:

```text
challenge-2/MCP-Wiki/
  AGENTS.md
  index.md
  architecture.md
  implementation-plan.md
  candidate-register.md
  decision-record.md
  security-model.md
  research/
    Challenge 2 Wiki MCP Server Research Report.md
    Challenge 2 Wiki MCP Server Research Report.docx
    Challenge 2 Wiki MCP Server Research Report.pdf
  sources/
    github-candidates.md
    academic-literature.md
    microsoft-copilot-mcp.md
  data/
    candidate-register.json
    source-register.json
```

**Important cleanup before treating it as publication-ready**

The Markdown report currently contains Deep Research citation markers like:

```text
citeturn17search0
```

Those are not useful GitHub citations. Before relying on this as a repo knowledge source, we should convert them into normal Markdown links, footnotes, or a source register with URLs. Otherwise both humans and AI will see opaque citation IDs.

There is also an untracked `[LOCAL_STATE_FILE]` under:

```text
challenge-2/MCP-Wiki/[LOCAL_STATE_FILE]
```

That should be deleted and not committed.

**How to connect it to the existing wikis**

I would link to it, but not merge it.

Add a small pointer from:

- `README.md`: “MCP Wiki research and implementation planning”
- `challenge-2/wiki/index.md`: under a new “Related Engineering Research” section
- maybe `postmortem-public/wiki/repository-evidence.md`: as later follow-on work, not as core postmortem evidence

I would not add it to the postmortem exchange/source structure unless we regenerate the postmortem for a later version, because that wiki is about the original collaboration timeline. For now, a link from the postmortem to “subsequent MCP research” is enough.

**Decision**
Use a **new MCP Research Wiki**. Keep the Challenge 2 wiki focused on the dark-data corpus. Keep the postmortem wiki focused on collaboration evidence. Link between them deliberately.

That gives people and AI better access without collapsing three different knowledge domains into one oversized, ambiguous wiki.
````

## Contribution Reading

- User contribution: Defined the evidence-preservation goal and requested a research wiki plus analysis.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.

Previous: [EX-0092](0092-20260418065216-update-deep-research-prompt.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0094](0094-20260418065216-agree-add-all-local-state-file-to-gitignore-note-that-you-have-two-other-equivalent-report.md)
