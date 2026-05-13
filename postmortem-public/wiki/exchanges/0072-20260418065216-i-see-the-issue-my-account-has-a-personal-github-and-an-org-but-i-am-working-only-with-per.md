---
exchange_id: "EX-0072"
title: "I see the issue, my account has a personal GitHub and an Org but I am working only with personal"
source_id: "CONV-005"
global_sequence: 72
session_sequence: 20
user_timestamp: "2026-04-18T13:25:19.469Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0072. I see the issue, my account has a personal GitHub and an Org but I am working only with personal

Previous: [EX-0071](0071-20260418065216-if-there-is-an-authentication-block-and-a-policy-issue-can-i-fix-them-i-want-all-to-run-su.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0073](0073-20260418065216-ps-local-repo-cd-local-user-path.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
# Files mentioned by the user:

## Screenshot 2026-04-18 at 14.23.54.png: [TEMP_SCREENSHOT]

## My request for Codex:
I see the issue, my account has a personal GitHub and an Org but I am working only with personal on this machine so the auth to the org is not required

<image name=[Image #1]>
[image attachment omitted: data:image/png;base64; base64 omitted]
</image>
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-18T13:25:29.226Z`

````text
That screenshot is the right Copilot CLI device activation flow. I’ll treat this as a local account-selection problem first, not an org-admin blocker, and I’ll check the repo-side harness only after you finish the browser authorization.
````

### Response 2 (final_answer)

- Timestamp: `2026-04-18T13:25:33.478Z`

````text
Yes. In that screenshot, click **Continue** for `chris-page-gov` if that is the personal GitHub account that has the Copilot entitlement you want to use.

A small but important distinction: GitHub Copilot CLI is authenticating a **GitHub user account**, not “the org” as a separate login. If that same user account receives Copilot through an org seat, org policy can still affect CLI access. But if `chris-page-gov` has a personal Copilot plan, completing this device activation should make the CLI use that account directly.

After you click **Continue** and approve the device activation, run:

```bash
cd [LOCAL_REPO]

python3 challenge-2/tools/run_wiki_eval.py \
  --clients github-copilot \
  --questions Q001 \
  --timeout-sec 120 \
  --output-root /tmp/challenge2-wiki-eval-versioning \
  --run-id github-copilot-after-personal-login
```

Expected good result:

```json
"status": "completed"
```

If it still returns `policy_blocked`, then one of these is true:

- `chris-page-gov` does not have an active personal Copilot entitlement;
- the CLI is still resolving entitlement through the org seat;
- GPT-5.4 or Copilot CLI is disabled for that account/seat;
- a previous Copilot CLI token is still being preferred.

If that happens, the next local fix is to force a clean Copilot CLI login:

```bash
copilot
```

Then in the Copilot prompt:

```text
/logout
/login
/user
/model
```

Use `/user` to confirm it is using the expected personal account, and `/model` to confirm whether `gpt-5.4` is available to that account.

Once GitHub Copilot returns `completed`, we only need to warm the Microsoft Copilot Playwright profile and then all clients should be able to run.
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Implemented and validated user-facing workbench behavior.

Previous: [EX-0071](0071-20260418065216-if-there-is-an-authentication-block-and-a-policy-issue-can-i-fix-them-i-want-all-to-run-su.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0073](0073-20260418065216-ps-local-repo-cd-local-user-path.md)
