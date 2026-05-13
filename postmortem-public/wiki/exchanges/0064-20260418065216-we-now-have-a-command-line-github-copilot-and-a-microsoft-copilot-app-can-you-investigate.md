---
exchange_id: "EX-0064"
title: "We now have a command line GitHub Copilot and a Microsoft Copilot app. Can you investigate addin"
source_id: "CONV-005"
global_sequence: 64
session_sequence: 12
user_timestamp: "2026-04-18T12:09:12.119Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0064. We now have a command line GitHub Copilot and a Microsoft Copilot app. Can you investigate addin

Previous: [EX-0063](0063-20260418065216-the-pr-says-5-conversations-i-thought-we-added-this-which-would-be-six.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0065](0065-20260418065216-first-fix-the-current-pr-comments-ensuring-that-you-consider-each-as-indicating-a-class-of.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
We now have a command line GitHub Copilot and a Microsoft Copilot app. Can you investigate adding these, I've installed the Copilot app on this Mac and I think the GitHub Copilot CLI may come with the update of gh so maybe there as well
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-18T12:09:14.365Z`

````text
I’ll inspect what is installed locally first: `gh` extensions/commands, any Copilot binaries, and the macOS app registration. Then I’ll map that against the existing evaluation harness so we can see what would be needed to add GitHub Copilot CLI and Microsoft Copilot as evaluation targets.
````

### Response 2 (commentary)

- Timestamp: `2026-04-18T12:09:37.589Z`

````text
The repo already has an evaluation harness, and it currently knows about `codex`, `gemini`, and `claude`. Locally, `gh copilot` is present as a GitHub CLI preview wrapper; I’m checking whether the actual Copilot CLI is installed/downloadable and what non-interactive interface it exposes.
````

### Response 3 (commentary)

- Timestamp: `2026-04-18T12:09:52.211Z`

````text
There are two separate local app bundles: `/Applications/Copilot.app` and `/Applications/Microsoft 365 Copilot.app`. The AppleScript name I tried for “Microsoft Copilot” is not the registered app name, so I’m checking their bundle IDs and whether either exposes URL schemes or scriptability that a harness could use.
````

### Response 4 (commentary)

- Timestamp: `2026-04-18T12:09:56.309Z`

````text
`gh` is new enough for the Copilot preview wrapper, but the actual Copilot CLI payload is not installed yet, so `gh copilot -p ...` currently fails before reaching a prompt. I’m going to trigger the wrapper once to see whether it downloads the payload or requires an interactive setup step.
````

### Response 5 (commentary)

- Timestamp: `2026-04-18T12:10:15.273Z`

````text
The native Copilot app appears to expose a URL scheme (`copilotn`) and a macOS service, but no obvious AppleScript dictionary from the plist. I’m reading the evaluation harness now to see the smallest clean integration point for CLI-style clients versus GUI-only clients.
````

### Response 6 (commentary)

- Timestamp: `2026-04-18T12:10:40.261Z`

````text
Official GitHub docs now describe a separate GitHub Copilot CLI install path, and the old `gh-copilot` extension is deprecated. I’m checking whether Homebrew/npm install routes are viable on this Mac without installing anything yet.
````

### Response 7 (final_answer)

- Timestamp: `2026-04-18T12:11:49.928Z`

````text
I investigated both.

**GitHub Copilot CLI**
Local state:

- `gh` is current enough: `gh version 2.90.0`.
- `gh copilot --help` exists, but the actual Copilot CLI payload is not installed.
- `gh copilot`, `gh copilot -- --help`, and `gh copilot -p ...` all currently fail with:
  - `! Copilot CLI not installed`
- `~/.local/share/gh` does not exist, so the `gh` wrapper has not downloaded it.
- Homebrew can see `copilot-cli` but it is not installed:
  - available as `copilot-cli` version `1.0.31`
- npm can see `@github/copilot` version `1.0.32`.
- Local Node is `v25.9.0`, which is compatible with GitHub’s documented Node 22+ requirement.

Official docs now describe GitHub Copilot CLI as a separate CLI install, with Homebrew or npm as valid install paths: [Install Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli). The `gh copilot` manual still says `gh` can run/download it, but that path is not working on this Mac right now: [gh copilot manual](https://cli.github.com/manual/gh_copilot).

Recommended integration: after the PR is merged, install with either:

```bash
brew install copilot-cli
```

or:

```bash
npm install -g @github/copilot
```

Then add `github-copilot` as a normal CLI client in `challenge-2/tools/run_wiki_eval.py` and `challenge-2/evaluation/clients.py`, using the programmatic interface:

```bash
copilot -p "{prompt}"
```

GitHub documents `-p` / `--prompt` as the programmatic mode: [About Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli). We will need a smoke test first because Copilot CLI asks about trusted directories and tool approvals. For the benchmark, I’d start read-only and avoid write permissions.

**Microsoft Copilot Apps**
There are actually two installed app bundles:

- `/Applications/Copilot.app`
  - bundle id: `com.microsoft.copilot-mac`
  - version: `25.6.440416001`
  - URL schemes: `copilotn`, `mscopilotmac`
- `/Applications/Microsoft 365 Copilot.app`
  - bundle id: `com.microsoft.m365copilot`
  - version: `1.2604.0601`
  - URL scheme: `msauth.com.microsoft.m365copilot`

Microsoft’s support pages distinguish the standalone Microsoft Copilot app from the Microsoft 365 Copilot app: [Microsoft 365 Copilot app transition](https://support.microsoft.com/en-us/office/the-microsoft-365-app-transition-to-the-microsoft-365-copilot-app-22eac811-08d6-4df3-92dd-77f193e354a5). The macOS Copilot app is primarily an interactive app with shortcut/device-context features, not a documented headless CLI/API target: [Getting started with Copilot on macOS](https://support.microsoft.com/en-us/topic/getting-started-with-copilot-on-macos-e69021ae-3592-4a0b-b2b6-df7b7f9eeb30).

Recommended integration: do not treat the Microsoft Copilot app as an automated benchmark client yet. It is better as a manual or semi-manual target:

- harness writes prompt files for `microsoft-copilot-manual`
- optionally copies the prompt to clipboard or opens `Copilot.app`
- human pastes prompt and records response into the run folder
- scorer treats it as a manually captured client with provenance notes

A fully automated GUI path via AppleScript/Accessibility or browser automation would be brittle and harder to defend as evidence.

**Harness Impact**
The current harness is close. It already supports custom argv templates in `challenge-2/evaluation/client-config.example.json`, but `run_wiki_eval.py` hard-codes supported clients as:

```python
SUPPORTED_CLIENTS = ("codex", "gemini", "claude")
```

After merge, I’d make a small follow-up PR that adds:

- `github-copilot` as an automated CLI client once `copilot` is installed and smoke-tested.
- `microsoft-copilot-manual` as a manual capture client, not an automated CLI.
- docs explaining that Microsoft Copilot app results are manually captured unless/until Microsoft exposes a stable automation interface.
- dry-run and one-question smoke tests before any 100-question run.

No repo files were changed in this investigation.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0063](0063-20260418065216-the-pr-says-5-conversations-i-thought-we-added-this-which-would-be-six.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0065](0065-20260418065216-first-fix-the-current-pr-comments-ensuring-that-you-consider-each-as-indicating-a-class-of.md)
