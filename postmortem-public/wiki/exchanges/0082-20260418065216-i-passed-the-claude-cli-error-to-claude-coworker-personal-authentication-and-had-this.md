---
exchange_id: "EX-0082"
title: "I passed the claude CLI error to Claude Coworker (personal authentication) and had this:"
source_id: "CONV-005"
global_sequence: 82
session_sequence: 30
user_timestamp: "2026-04-19T17:09:20.530Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0082. I passed the claude CLI error to Claude Coworker (personal authentication) and had this:

Previous: [EX-0081](0081-20260418065216-claude-says-mcp-failed-related.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0083](0083-20260418065216-it-looked-like-the-microsoft-365-copilot-failed-because-the-prompt-specified.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
I passed the claude CLI error to Claude Coworker (personal authentication) and had this:
(Do we need to use export CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 )
What's happening: Claude Code v2.1.114 automatically adds a `context_management` field to every API request (a beta feature for auto-pruning the context window). Your `licenseportal.aiengineeringlab.co.uk` proxy is a LiteLLM-style gateway that doesn't know about that field, so it rejects the request with "Extra inputs are not permitted" — and the fallback to Sonnet and then Haiku fails for the same reason. It's not about your model choice; `/model` can't help.

There isn't (yet) an official flag to turn off just `context_management`. A couple of things to try, in order:

1. Disable experimental beta features before launching Claude Code:

```
export CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1
claude
```

That stops Claude Code from sending experimental beta parameters, which should include `context_management`.

2. If that doesn't clear it, downgrade to a slightly older Claude Code that predates this feature being on by default:

```
npm install -g @anthropic-ai/claude-code@2.0
```

…then `claude --version` to confirm, and try again.

3. The real fix is on the proxy side — this is the AI Engineering Lab's own gateway, so ping whoever runs `licenseportal.aiengineeringlab.co.uk` and ask them to either (a) strip `context_management` from the request body before forwarding to Bedrock, or (b) update their LiteLLM/gateway version so it passes the field through. Other hackathon attendees will hit the exact same wall.

Open GitHub issues tracking this: [anthropics/claude-code#21612](https://github.com/anthropics/claude-code/issues/21612) and [#44219](https://github.com/anthropics/claude-code/issues/44219) (a `--no-context-management` flag is requested but not shipped).
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T17:09:31.337Z`

````text
That explanation is plausible and testable. I’ll run Claude with `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` first on a trivial prompt, then through the evaluation harness; if it fixes the proxy error, I’ll make the harness/documentation capture that environment requirement so the eventual run is reproducible.
````

### Response 2 (commentary)

- Timestamp: `2026-04-19T17:10:12.315Z`

````text
The proposed environment variable fixes the Claude proxy issue in this environment. With `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`, a trivial non-interactive Claude request succeeds, including an explicit Opus request resolving to the DSIT-managed `eu.anthropic.claude-opus-4-6-v1` model group.
````

### Response 3 (commentary)

- Timestamp: `2026-04-19T17:10:53.458Z`

````text
I’m rerunning the full smoke with that environment variable exported for the child processes. It is still running, so I’m waiting for the batch result rather than interrupting it.
````

### Response 4 (commentary)

- Timestamp: `2026-04-19T17:12:00.214Z`

````text
Still no final output at 90 seconds. This is within the Microsoft UI path’s normal runtime, so I’m letting the smoke finish.
````

### Response 5 (commentary)

- Timestamp: `2026-04-19T17:12:35.857Z`

````text
The smoke with `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` has now completed for Claude. The only remaining live-client failure in that run is GitHub Copilot’s existing `policy_blocked` status.
````

### Response 6 (commentary)

- Timestamp: `2026-04-19T17:12:52.427Z`

````text
The smoke confirmed the env var is the right fix: Claude completed when `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` was inherited. I’m adding first-class client-config support for that env override so the run does not depend on whoever launched the shell remembering to export it manually.
````

### Response 7 (commentary)

- Timestamp: `2026-04-19T17:14:08.969Z`

````text
The code now supports per-client environment overrides and the example config carries the Claude beta-disable flag. I’m validating that the config alone is enough by running a Claude-only smoke without relying on an exported shell variable.
````

### Response 8 (commentary)

- Timestamp: `2026-04-19T17:15:02.094Z`

````text
The config smoke also proved the harness can inject the Claude compatibility flag itself. I noticed the example config still left Gemini and Microsoft labelled as auto/router defaults, so I’m tightening that config to match your “no AUTO where selectable” requirement before rerunning the dry/live smoke.
````

### Response 9 (commentary)

- Timestamp: `2026-04-19T17:15:51.707Z`

````text
The dry-run now has no Auto-labelled selectable clients: Gemini is pinned to `gemini-3.1-pro-preview`, Claude is DSIT local-settings managed with the compatibility env flag, Microsoft is `gpt-5-thinking-ui-selected`, and GitHub remains `gpt-5.4`. I’m running one live smoke with that checked-in config.
````

### Response 10 (commentary)

- Timestamp: `2026-04-19T17:16:35.416Z`

````text
The live smoke with the checked-in config is running. Claude has already proven the config-level env path works, so I’m mainly waiting to confirm all client statuses in one batch.
````

### Response 11 (commentary)

- Timestamp: `2026-04-19T17:18:03.082Z`

````text
The checked-in config live smoke completed for Codex, Gemini, Claude, and Microsoft. GitHub Copilot is still the only failed client, and the failure remains the known policy block rather than authentication or model selection.
````

### Response 12 (commentary)

- Timestamp: `2026-04-19T17:18:16.646Z`

````text
I’ve recorded the successful checked-in-config smoke and the GitHub-URL limitation for Microsoft. I’m running the final validation pass and then I’ll commit the environment/config changes.
````

### Response 13 (commentary)

- Timestamp: `2026-04-19T17:18:34.539Z`

````text
The final diff is limited to client-config env support, the explicit model config, tests, and tracking docs. I’m staging and committing this now.
````

### Response 14 (commentary)

- Timestamp: `2026-04-19T17:19:04.616Z`

````text
One nuance before I close this out: the config-level Claude run completed, but its captured `modelUsage` showed a Sonnet fallback in one run, while an explicit `--model opus` with the beta-disable flag resolved to the DSIT Opus 4.6 group. I’m running a Claude-only harness smoke with `--model claude=opus` and the checked-in environment config so the evaluation uses Opus rather than merely “whatever local default resolves to”.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0081](0081-20260418065216-claude-says-mcp-failed-related.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0083](0083-20260418065216-it-looked-like-the-microsoft-365-copilot-failed-because-the-prompt-specified.md)
