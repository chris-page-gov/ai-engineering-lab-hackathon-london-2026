---
exchange_id: "EX-0076"
title: "Looks like it's blocked at policy level, I don't understand as this is a personal project and is"
source_id: "CONV-005"
global_sequence: 76
session_sequence: 24
user_timestamp: "2026-04-19T15:25:50.904Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0076. Looks like it's blocked at policy level, I don't understand as this is a personal project and is

Previous: [EX-0075](0075-20260418065216-it-shows.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0077](0077-20260418065216-is-there-anything-else-i-need-to-do-before-we-run-the-evaluation.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
Looks like it's blocked at policy level, I don't understand as this is a personal project and is on my personal ID, I have not lgged in to the org
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T15:26:00.265Z`

````text
I’ll verify the GitHub policy mechanics against the current official docs, then explain what is probably happening in your account setup and what you can do next.
````

### Response 2 (final_answer)

- Timestamp: `2026-04-19T15:26:29.952Z`

````text
Yes, this can still happen even if the repo is personal and you have not explicitly “logged into the org”.

The key point is that GitHub auth is by **user account**, not by project context. `chris-page-gov` is one GitHub identity. If that identity is a member of an org, or if its Copilot entitlement comes from an org/enterprise seat, GitHub can apply org/enterprise Copilot policies when the CLI asks for available models.

Your CLI output confirms the sequence:

```text
Welcome chris-page-gov!
Failed to load models: access denied by Copilot policy.
```

So login is working. The denial happens when GitHub evaluates Copilot CLI/model access for that account.

GitHub’s docs describe this directly: if a user receives Copilot from an organization, the Copilot CLI policy must be enabled in that organization’s settings; users also need a valid Copilot seat, and available models can be controlled by enterprise/org policy. See GitHub’s docs on [administering Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/administer-copilot-cli-for-your-enterprise) and [troubleshooting Copilot CLI authentication](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/troubleshoot-copilot-cli-auth).

What is probably happening:

- `chris-page-gov` is the authenticated account.
- GitHub sees that account’s Copilot entitlement or model access as org/enterprise-managed.
- The CLI model-list call is blocked before it considers whether this local repo is personal.
- The local machine being “personal” and the repo being “personal” do not bypass the account-level Copilot policy.

Check this page while signed in as `chris-page-gov`:

[https://github.com/settings/copilot](https://github.com/settings/copilot)

Look for wording like:

- “Copilot is managed by your organization”
- “Your organization has disabled this feature”
- “Get Copilot from an organization”
- “Copilot Individual/Pro” or personal subscription status
- feature/model settings under Copilot

Also check:

[https://github.com/settings/copilot/features](https://github.com/settings/copilot/features)

If it says the feature is controlled by an organization, you cannot fix it locally. The org/enterprise admin must enable Copilot CLI/model access for your user or org.

Two practical ways forward:

1. **Use the current `chris-page-gov` account and ask the org/admin to enable Copilot CLI.**
   The admin ask is: “Copilot CLI v1.0.32 authenticates as `chris-page-gov`, but `/model` fails with `access denied by Copilot policy`. Please enable Copilot CLI and required model access for this user.”

2. **Use a GitHub account whose Copilot entitlement is purely personal.**
   If you have a separate personal GitHub account with Copilot Pro, log the CLI out and back in with that account:

```powershell
copilot
```

Then inside Copilot:

```text
/logout
/login
/user
/model
```

If the same account has both personal and org connections, GitHub may still resolve policy through the managed entitlement. A truly separate personal GitHub account is the cleanest way to isolate from org policy.

One more local thing worth checking: environment tokens can override the account the CLI uses. Run this, which only prints variable names, not secrets:

```powershell
Get-ChildItem Env:COPILOT_GITHUB_TOKEN,Env:GH_TOKEN,Env:GITHUB_TOKEN -ErrorAction SilentlyContinue | Select-Object Name
```

If any of those are set to an org-associated token, remove them for this shell and retry:

```powershell
Remove-Item Env:COPILOT_GITHUB_TOKEN -ErrorAction SilentlyContinue
Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue
Remove-Item Env:GITHUB_TOKEN -ErrorAction SilentlyContinue
```

Then:

```powershell
copilot
```

and check:

```text
/user
/model
```

For the benchmark, we should keep GitHub Copilot CLI as `policy_blocked` until `/model` loads successfully. Once `/model` works, the harness should run.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Inspected repository/GitHub state and adjusted branch or PR hygiene.

Previous: [EX-0075](0075-20260418065216-it-shows.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0077](0077-20260418065216-is-there-anything-else-i-need-to-do-before-we-run-the-evaluation.md)
