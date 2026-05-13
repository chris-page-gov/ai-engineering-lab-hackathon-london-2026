---
exchange_id: "EX-0077"
title: "Is there anything else I need to do before we run the evaluation"
source_id: "CONV-005"
global_sequence: 77
session_sequence: 25
user_timestamp: "2026-04-19T15:54:09.219Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0077. Is there anything else I need to do before we run the evaluation

Previous: [EX-0076](0076-20260418065216-looks-like-it-s-blocked-at-policy-level-i-don-t-understand-as-this-is-a-personal-project-a.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0078](0078-20260418065216-there-were-a-few-can-i-trust-this-folder-prompts-holding-things-up-i-want-all-to-use-the-b.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Is there anything else I need to do before we run the evaluation
````

## Codex Response

### Response 1 (final_answer)

- Timestamp: `2026-04-19T15:54:25.968Z`

````text
Yes. Before running the **full** evaluation successfully across all clients, there are two things to resolve.

**1. GitHub Copilot CLI must pass `/model`**

Right now this is still blocked at GitHub policy level. The evaluation cannot complete for `github-copilot` until this works inside the CLI:

```text
/model
```

Success means it loads a model list, ideally including `gpt-5.4`. If it still says `access denied by Copilot policy`, the full run will record `policy_blocked`.

One local check worth doing first in `zsh`:

```bash
env | grep -E '^(COPILOT_GITHUB_TOKEN|GH_TOKEN|GITHUB_TOKEN)='
```

If any are set and may belong to the wrong account, clear them for this shell:

```bash
unset COPILOT_GITHUB_TOKEN GH_TOKEN GITHUB_TOKEN
```

Then retry:

```bash
copilot
```

Inside Copilot:

```text
/logout
/login
/user
/model
```

If `/model` is still blocked after that, it needs GitHub account/org/support action.

**2. Microsoft Copilot needs a warmed Playwright profile**

Run this once and sign in interactively:

```bash
cd [LOCAL_REPO]/challenge-2/workbench
pnpm exec playwright open --user-data-dir "$HOME/.cache/challenge2-microsoft-copilot-playwright" https://m365.cloud.microsoft/chat
```

In the browser:

1. Sign in.
2. Confirm Microsoft 365 Copilot Chat loads.
3. Send a tiny prompt like `Reply with ok.`
4. Close the browser.

Then smoke test it:

```bash
cd [LOCAL_REPO]
python3 challenge-2/tools/run_wiki_eval.py --clients microsoft-copilot --questions Q001 --timeout-sec 180 --output-root /tmp/challenge2-wiki-eval-versioning --run-id microsoft-after-login
```

We want `status: "completed"`.

**Before the full run**

Run one final smoke for all clients:

```bash
python3 challenge-2/tools/run_wiki_eval.py --clients full --questions Q001 --timeout-sec 180 --output-root /tmp/challenge2-wiki-eval-versioning --run-id full-live-smoke
```

Only start the 100-question evaluation when every client returns `completed`.

Then run:

```bash
python3 challenge-2/tools/run_wiki_eval.py --clients full --timeout-sec 180 --output-root output/evaluation --run-id full-100-question-evaluation
```

At the moment, the main thing blocking “all successful” is GitHub Copilot CLI policy access. Microsoft is likely fixable locally by signing into the Playwright profile.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Implemented and validated user-facing workbench behavior.

Previous: [EX-0076](0076-20260418065216-looks-like-it-s-blocked-at-policy-level-i-don-t-understand-as-this-is-a-personal-project-a.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0078](0078-20260418065216-there-were-a-few-can-i-trust-this-folder-prompts-holding-things-up-i-want-all-to-use-the-b.md)
