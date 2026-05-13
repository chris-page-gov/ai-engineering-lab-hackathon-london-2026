---
exchange_id: "EX-0070"
title: "override and use GPT-5.4 on Copilot as I found contradictory documentation and this was from a m"
source_id: "CONV-005"
global_sequence: 70
session_sequence: 18
user_timestamp: "2026-04-18T13:01:31.481Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0070. override and use GPT-5.4 on Copilot as I found contradictory documentation and this was from a m

Previous: [EX-0069](0069-20260418065216-i-want-full-coverage-with-the-best-models-selected-in-each-client-so-that-includes-github.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0071](0071-20260418065216-if-there-is-an-authentication-block-and-a-policy-issue-can-i-fix-them-i-want-all-to-run-su.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
override and use GPT-5.4 on Copilot as I found contradictory documentation and this was from a member of staff
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-18T13:01:37.544Z`

````text
I’ll override the GitHub Copilot CLI selector to `gpt-5.4` and record the source as a staff-confirmed override, because that is a decision input separate from the public docs. I’ll keep the public documentation references in the manifest as context, but the actual command will pass `--model gpt-5.4`.
````

### Response 2 (commentary)

- Timestamp: `2026-04-18T13:04:28.875Z`

````text
The new code compiles and the example config validates. I’m running the focused evaluation tests and a dry-run with the full client set now; this should prove the harness records all five clients without spending requests or requiring UI login yet.
````

### Response 3 (commentary)

- Timestamp: `2026-04-18T13:04:56.649Z`

````text
The dry-run proves the full set is now represented and the commands are selecting the intended models, including the staff-confirmed `gpt-5.4` override for GitHub Copilot CLI. I’m going to do one bounded Microsoft Copilot smoke attempt so we know whether the Playwright path can actually reach a prompt box on this Mac, and I’ll keep it to a single question with a short timeout.
````

### Response 4 (commentary)

- Timestamp: `2026-04-18T13:05:18.900Z`

````text
The first Microsoft smoke failed before opening Copilot because the local workbench install has `@playwright/test` but not the bare `playwright` package at that resolution path. I’ve patched the adapter to fall back to `@playwright/test` and I’m rerunning the same single-question smoke.
````

### Response 5 (commentary)

- Timestamp: `2026-04-18T13:06:35.393Z`

````text
The Microsoft live smoke now reaches the adapter and returns `auth_required`, with screenshot/HTML evidence captured, which is the correct caveated failure mode until the Playwright profile is signed in. I’m checking the GitHub Copilot CLI path in the same bounded way; because the standalone binary is absent, it should record an unavailable/fail state without making a model request.
````

### Response 6 (commentary)

- Timestamp: `2026-04-18T13:07:05.752Z`

````text
The full harness is now in place. The remaining live blockers are environmental: GitHub Copilot CLI is not actually installed as `copilot`, and Microsoft Copilot needs an authenticated Playwright profile. Since you asked for full coverage, I’m going to install the standalone GitHub Copilot CLI via Homebrew so the next live run can at least reach that client.
````

### Response 7 (commentary)

- Timestamp: `2026-04-18T13:07:32.650Z`

````text
GitHub Copilot CLI is now installed as `copilot` version 1.0.32. Its local help supports `xhigh`, so I’m tightening the Copilot selector to `gpt-5.4` with `xhigh` effort rather than the conservative `high` effort from the public command-reference excerpt.
````

### Response 8 (commentary)

- Timestamp: `2026-04-18T13:09:08.572Z`

````text
I’ll apply your override consistently: GitHub Copilot CLI should be treated as GPT-5.4 with xhigh effort, with the contradiction documented as a staff-confirmed decision. I’m going to tighten the tests and rerun the relevant dry-runs and validation so the branch records that choice cleanly.
````

### Response 9 (commentary)

- Timestamp: `2026-04-18T13:09:17.383Z`

````text
The local changes already reflect the override in the harness and docs. One test still expects the older Copilot effort value, so I’m patching that and then I’ll rerun the validation set.
````

### Response 10 (commentary)

- Timestamp: `2026-04-18T13:09:27.633Z`

````text
I’ve corrected the test expectation to the staff-confirmed GPT-5.4/xhigh policy. Next I’m running the syntax and schema checks first, then the eval-specific tests and dry-runs.
````

### Response 11 (commentary)

- Timestamp: `2026-04-18T13:09:34.534Z`

````text
The unit tests are passing with the new Copilot policy. I’m now refreshing the dry-run manifests so the generated audit metadata captures the installed Copilot CLI and the full client set.
````

### Response 12 (commentary)

- Timestamp: `2026-04-18T13:09:45.542Z`

````text
The full dry-run now expands to all five clients and records GitHub Copilot as GPT-5.4/xhigh. I’m doing one bounded GitHub Copilot CLI live smoke next; that will tell us whether the installed CLI is actually authenticated and runnable before the later full 100-question evaluation.
````

### Response 13 (commentary)

- Timestamp: `2026-04-18T13:10:00.741Z`

````text
The GitHub Copilot CLI is installed, but the live smoke is blocked by GitHub policy settings, not by the harness. I’m going to classify that distinctly as `policy_blocked` in the run output so the eventual benchmark can separate client access problems from model failures.
````

### Response 14 (commentary)

- Timestamp: `2026-04-18T13:10:19.526Z`

````text
I’ve added a distinct `policy_blocked` result for Copilot CLI access denials and covered it with a test. I’m rerunning that one smoke so the observed result matches the new status taxonomy.
````

### Response 15 (commentary)

- Timestamp: `2026-04-18T13:10:37.359Z`

````text
The live Copilot smoke now records `policy_blocked`, which is exactly the kind of caveat we need for publication-quality evaluation evidence. I’m updating the tracking docs and config notes so this is recorded as an access-control constraint, not a harness failure.
````

### Response 16 (commentary)

- Timestamp: `2026-04-18T13:11:16.192Z`

````text
The tracking docs now record both access constraints: Copilot CLI policy blocking and Microsoft Copilot profile authentication. I’m running the final validation pass, including documentation lockstep and whitespace checks.
````

### Response 17 (commentary)

- Timestamp: `2026-04-18T13:11:55.673Z`

````text
One more publication hygiene issue surfaced while reviewing the UI adapter: the Microsoft run metadata should not leak a local profile path by default. I’m changing it to record the profile source instead, while still allowing the adapter to use the path internally.
````

### Response 18 (commentary)

- Timestamp: `2026-04-18T13:12:19.597Z`

````text
The adapter no longer records the default local profile directory in its output. I’m rerunning the affected checks and a fresh full dry-run so the manifest shape is validated after that hygiene change.
````

### Response 19 (commentary)

- Timestamp: `2026-04-18T13:13:00.716Z`

````text
The refreshed dry-run manifest now shows the sanitized Microsoft profile metadata and the Copilot GPT-5.4/xhigh selector. I’m doing one more Microsoft UI smoke to verify the live adapter still exits cleanly at the authentication gate after the metadata change.
````

### Response 20 (commentary)

- Timestamp: `2026-04-18T13:13:24.328Z`

````text
All checks are green after the sanitized live smoke. I’m staging the evaluation harness, docs, tests, and the Microsoft Copilot adapter now, then I’ll commit this branch update.
````

### Response 21 (final_answer)

- Timestamp: `2026-04-18T13:13:56.164Z`

````text
Applied the override: GitHub Copilot CLI is now recorded as `gpt-5.4` with `xhigh` reasoning effort, with the source marked as `staff_confirmed_best_override`.

Implemented and committed on `codex/evaluation-versioning`:

- Commit: `e8aa864 Add full coverage Copilot evaluation clients`
- Working tree: clean
- Full coverage clients now expand to Codex, Gemini CLI, Claude Code, GitHub Copilot CLI, and Microsoft Copilot UI.
- Added Microsoft Copilot UI automation at [microsoft_copilot_playwright.mjs]([LOCAL_REPO]/challenge-2/tools/microsoft_copilot_playwright.mjs:1), with explicit caveats and sanitized profile metadata.
- Updated model/version capture in [clients.py]([LOCAL_REPO]/challenge-2/evaluation/clients.py:1), [client-config.example.json]([LOCAL_REPO]/challenge-2/evaluation/client-config.example.json:1), docs, and tests.
- Added `policy_blocked` classification for GitHub Copilot CLI policy/access denials.

Validation passed:

- `python3 -m py_compile ...`
- `python3 -m json.tool challenge-2/evaluation/client-config.example.json`
- `node --check challenge-2/tools/microsoft_copilot_playwright.mjs`
- `python3 -m unittest discover -s tests -p 'test_challenge2_eval*.py'` ran 8 tests OK
- `uv run --with openpyxl python -m py_compile challenge-2/tools/build_wiki.py`
- `python3 tools/check_documentation_lockstep.py`
- `git diff --check`
- Full dry-run with config: `full-config-smoke-sanitized`

Observed client state:

- GitHub Copilot CLI is installed: `GitHub Copilot CLI 1.0.32`, reported latest.
- GitHub Copilot live smoke is callable but returns `policy_blocked`, so live answers need account/org policy access enabled.
- Microsoft Copilot UI smoke runs and returns `auth_required`; it needs an authenticated Playwright profile before the full benchmark.

Reference links recorded in the repo docs/config include [OpenAI GPT-5.4](https://developers.openai.com/api/docs/models/gpt-5.4), [Gemini CLI Gemini 3 routing](https://geminicli.com/docs/get-started/gemini-3/), [Claude Code model config](https://code.claude.com/docs/en/model-config), [GitHub Copilot model comparison](https://docs.github.com/en/copilot/reference/ai-models/model-comparison), and [Microsoft 365 Copilot release notes](https://learn.microsoft.com/en-us/microsoft-365/copilot/release-notes).

Next blocker before the full 100-question run is access, not implementation: enable GitHub Copilot CLI policy access and warm/authenticate the Microsoft Copilot Playwright profile.

::git-stage{cwd="[LOCAL_REPO]"}
::git-commit{cwd="[LOCAL_REPO]"}
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Mapped the request into repeatable generation, linting, and source-backed wiki artifacts.

Previous: [EX-0069](0069-20260418065216-i-want-full-coverage-with-the-best-models-selected-in-each-client-so-that-includes-github.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0071](0071-20260418065216-if-there-is-an-authentication-block-and-a-policy-issue-can-i-fix-them-i-want-all-to-run-su.md)
