---
title: "Public Codex Postmortem"
tags:
  - "index"
  - "codex-postmortem-public"
---

# Public Codex Postmortem

This folder is the GitHub-safe derivative of the private Codex postmortem evidence archive for Team DSIT A's Challenge 2 work.

## Start Here

- [Public Postmortem](postmortem.md)
- [Conversation Summary](conversation-summary.md)
- [Start-to-Finish Conversation Readers](#start-to-finish-conversation-readers)
- [Publication Decision Register](decisions.md)
- [Methodology Sources](methodology.md)
- [Repository Evidence](repository-evidence.md)
- [Public Postmortem Architecture](architecture.md)

## Start-to-Finish Conversation Readers

| Source | Conversation | Exchanges | Reader | Source Note |
|---|---|---:|---|---|
| CONV-001 | Deep Research Prompt and Copilot Review | 2 | [read](readers/conv-001-deep-research-prompt-and-copilot-review.md) | [source](sources/conv-001-deep-research-prompt-and-copilot-review.md) |
| CONV-002 | Karpathy Wiki Planning and Challenge 2 Vault Build | 31 | [read](readers/conv-002-karpathy-wiki-planning-and-challenge-2-vault-build.md) | [source](sources/conv-002-karpathy-wiki-planning-and-challenge-2-vault-build.md) |
| CONV-003 | Wiki Evaluation Harness, Workbench, and Demo Route | 15 | [read](readers/conv-003-wiki-evaluation-harness-workbench-and-demo-route.md) | [source](sources/conv-003-wiki-evaluation-harness-workbench-and-demo-route.md) |
| CONV-004 | SeeLinks Question Box, PR Hygiene, and Baseline Cleanup | 4 | [read](readers/conv-004-seelinks-question-box-pr-hygiene-and-baseline-cleanup.md) | [source](sources/conv-004-seelinks-question-box-pr-hygiene-and-baseline-cleanup.md) |
| CONV-005 | Codex Postmortem, Publication Assessment, and Version 1.1 PR | 61 | [read](readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | [source](sources/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) |

## Redacted Prompt-Response Exchanges

| Sequence | Exchange | Source |
|---:|---|---|
| 1 | [Update Deep Research Prompt](exchanges/0001-20260416024008-update-deep-research-prompt.md) | CONV-001 |
| 2 | [There are some claude artifacts in the [LOCAL_REFERENCE_REPO]/.claude/ folder,  s](exchanges/0002-20260416024008-there-are-some-claude-artifacts-in-the-local-reference-repo-claude-folder-s.md) | CONV-001 |
| 3 | [Plan Karpathy Wiki Translation](exchanges/0003-20260416084939-plan-karpathy-wiki-translation.md) | CONV-002 |
| 4 | [Implement Karpathy Wiki Vault](exchanges/0004-20260416084939-implement-karpathy-wiki-vault.md) | CONV-002 |
| 5 | [Which folder do I open in Obsidian to browse](exchanges/0005-20260416084939-which-folder-do-i-open-in-obsidian-to-browse.md) | CONV-002 |
| 6 | [Open Challenge 2 Obsidian Vault](exchanges/0006-20260416084939-open-challenge-2-obsidian-vault.md) | CONV-002 |
| 7 | [Commit and push](exchanges/0007-20260416084939-commit-and-push.md) | CONV-002 |
| 8 | [Include these](exchanges/0008-20260416084939-include-these.md) | CONV-002 |
| 9 | [Write the PR and trigger a code review](exchanges/0009-20260416084939-write-the-pr-and-trigger-a-code-review.md) | CONV-002 |
| 10 | [Along with the code, can you draft a io webpage for our architecture explaining it to a person w](exchanges/0010-20260416084939-along-with-the-code-can-you-draft-a-io-webpage-for-our-architecture-explaining-it-to-a-per.md) | CONV-002 |
| 11 | [Work exclusively on the Fork-Local PR.](exchanges/0011-20260416084939-work-exclusively-on-the-fork-local-pr.md) | CONV-002 |
| 12 | [Implement these fixes](exchanges/0012-20260416084939-implement-these-fixes.md) | CONV-002 |
| 13 | [With the comments, fix and reject so the ones you've addressed or rejected are not shown as left](exchanges/0013-20260416084939-with-the-comments-fix-and-reject-so-the-ones-you-ve-addressed-or-rejected-are-not-shown-as.md) | CONV-002 |
| 14 | [Review and fix the comments, make sure you don't change sources or redact anything from the synt](exchanges/0014-20260416084939-review-and-fix-the-comments-make-sure-you-don-t-change-sources-or-redact-anything-from-the.md) | CONV-002 |
| 15 | [Merge to the fork](exchanges/0015-20260416084939-merge-to-the-fork.md) | CONV-002 |
| 16 | [Do a review on how far we meet the evaluation/judging criteria?](exchanges/0016-20260416084939-do-a-review-on-how-far-we-meet-the-evaluation-judging-criteria.md) | CONV-002 |
| 17 | [Fix Obsidian Mermaid Architecture Diagram](exchanges/0017-20260416084939-fix-obsidian-mermaid-architecture-diagram.md) | CONV-002 |
| 18 | [Add tracking files to the repo, Changelog.md (best practice change tracking showing dated change](exchanges/0018-20260416084939-add-tracking-files-to-the-repo-changelog-md-best-practice-change-tracking-showing-dated-ch.md) | CONV-002 |
| 19 | [Commit, push and PR to the fork](exchanges/0019-20260416084939-commit-push-and-pr-to-the-fork.md) | CONV-002 |
| 20 | [fix comments](exchanges/0020-20260416084939-fix-comments.md) | CONV-002 |
| 21 | [I need to design a UI for this with options to use AI or not. I like the way that SeeLinks pulls](exchanges/0021-20260416084939-i-need-to-design-a-ui-for-this-with-options-to-use-ai-or-not-i-like-the-way-that-seelinks.md) | CONV-002 |
| 22 | [Dark Data Workbench is good, create a plan to implement this with a full test suite including pl](exchanges/0022-20260416084939-dark-data-workbench-is-good-create-a-plan-to-implement-this-with-a-full-test-suite-includi.md) | CONV-002 |
| 23 | [Implement this plan on a new branch codex/SeeLinks](exchanges/0023-20260416084939-implement-this-plan-on-a-new-branch-codex-seelinks.md) | CONV-002 |
| 24 | [Implement Karpathy Wiki Vault](exchanges/0024-20260416084939-implement-karpathy-wiki-vault.md) | CONV-002 |
| 25 | [can we test it](exchanges/0025-20260416084939-can-we-test-it.md) | CONV-002 |
| 26 | [Push and create PR](exchanges/0026-20260416084939-push-and-create-pr.md) | CONV-002 |
| 27 | [Add these as well](exchanges/0027-20260416084939-add-these-as-well.md) | CONV-002 |
| 28 | [Merge the PR](exchanges/0028-20260416084939-merge-the-pr.md) | CONV-002 |
| 29 | [Is the obsidian file changed every time I use Obsidian - can it be gitignored?](exchanges/0029-20260416084939-is-the-obsidian-file-changed-every-time-i-use-obsidian-can-it-be-gitignored.md) | CONV-002 |
| 30 | [fix it](exchanges/0030-20260416084939-fix-it.md) | CONV-002 |
| 31 | [Incomplete Update Request](exchanges/0031-20260416084939-incomplete-update-request.md) | CONV-002 |
| 32 | [Can we review and clean, include dropping the PR on the original repo that we forked](exchanges/0032-20260416084939-can-we-review-and-clean-include-dropping-the-pr-on-the-original-repo-that-we-forked.md) | CONV-002 |
| 33 | [Commit and push this too](exchanges/0033-20260416084939-commit-and-push-this-too.md) | CONV-002 |
| 34 | [Add Documentation Lockstep and Evaluation Notes](exchanges/0034-20260416112703-add-documentation-lockstep-and-evaluation-notes.md) | CONV-003 |
| 35 | [Link into the Wiki - does theed a path change?](exchanges/0035-20260416112703-link-into-the-wiki-does-theed-a-path-change.md) | CONV-003 |
| 36 | [Build the harness that will allow us to push the questions into the various AIs with the instruc](exchanges/0036-20260416112703-build-the-harness-that-will-allow-us-to-push-the-questions-into-the-various-ais-with-the-i.md) | CONV-003 |
| 37 | [Do a PR for the evaluation work](exchanges/0037-20260416112703-do-a-pr-for-the-evaluation-work.md) | CONV-003 |
| 38 | [Is their a PR on the fork?](exchanges/0038-20260416112703-is-their-a-pr-on-the-fork.md) | CONV-003 |
| 39 | [merge the outstanding PRs on the fork](exchanges/0039-20260416112703-merge-the-outstanding-prs-on-the-fork.md) | CONV-003 |
| 40 | [is this referring to the fork branch](exchanges/0040-20260416112703-is-this-referring-to-the-fork-branch.md) | CONV-003 |
| 41 | [so is this branch clean?](exchanges/0041-20260416112703-so-is-this-branch-clean.md) | CONV-003 |
| 42 | [Is this clean and up to date?](exchanges/0042-20260416112703-is-this-clean-and-up-to-date.md) | CONV-003 |
| 43 | [I think that challenge-2/.obsidian/workspace.json is on main now](exchanges/0043-20260416112703-i-think-that-challenge-2-obsidian-workspace-json-is-on-main-now.md) | CONV-003 |
| 44 | [We should be clean now](exchanges/0044-20260416112703-we-should-be-clean-now.md) | CONV-003 |
| 45 | [That's okay, we live on the fork](exchanges/0045-20260416112703-that-s-okay-we-live-on-the-fork.md) | CONV-003 |
| 46 | [Now I need you to create a page in the wiki which will demonstrate all functionality including h](exchanges/0046-20260416112703-now-i-need-you-to-create-a-page-in-the-wiki-which-will-demonstrate-all-functionality-inclu.md) | CONV-003 |
| 47 | [Commit all changes including all untracked files](exchanges/0047-20260416112703-commit-all-changes-including-all-untracked-files.md) | CONV-003 |
| 48 | [can you run seelinks UI again](exchanges/0048-20260416112703-can-you-run-seelinks-ui-again.md) | CONV-003 |
| 49 | [Add Workbench Question Box](exchanges/0049-20260416142455-add-workbench-question-box.md) | CONV-004 |
| 50 | [Check Publication Branch Status](exchanges/0050-20260416142455-check-publication-branch-status.md) | CONV-004 |
| 51 | [Excellent. I need to write this up in full detail as a report to colleagues: what we did, the or](exchanges/0051-20260416142455-excellent-i-need-to-write-this-up-in-full-detail-as-a-report-to-colleagues-what-we-did-the.md) | CONV-004 |
| 52 | [I've added a section to the md file # Challenge 2 Obsidian Knowledge Base Plan](exchanges/0052-20260416142455-i-ve-added-a-section-to-the-md-file-challenge-2-obsidian-knowledge-base-plan.md) | CONV-004 |
| 53 | [Create Codex Postmortem Wiki](exchanges/0053-20260418065216-create-codex-postmortem-wiki.md) | CONV-005 |
| 54 | [Create Codex Postmortem Wiki](exchanges/0054-20260418065216-create-codex-postmortem-wiki.md) | CONV-005 |
| 55 | [Check the licensing on the localised sources](exchanges/0055-20260418065216-check-the-licensing-on-the-localised-sources.md) | CONV-005 |
| 56 | [Create Codex Postmortem Wiki](exchanges/0056-20260418065216-create-codex-postmortem-wiki.md) | CONV-005 |
| 57 | [Create Contribution Modes and Security Assessment](exchanges/0057-20260418065216-create-contribution-modes-and-security-assessment.md) | CONV-005 |
| 58 | [Check Publication Branch Status](exchanges/0058-20260418065216-check-publication-branch-status.md) | CONV-005 |
| 59 | [Recast README for Challenge 2 Implementation](exchanges/0059-20260418065216-recast-readme-for-challenge-2-implementation.md) | CONV-005 |
| 60 | [Prepare Version 1.1 Publication PR](exchanges/0060-20260418065216-prepare-version-1-1-publication-pr.md) | CONV-005 |
| 61 | [<turn_aborted>](exchanges/0061-20260418065216-turn-aborted.md) | CONV-005 |
| 62 | [Status Check During Publication Work](exchanges/0062-20260418065216-status-check-during-publication-work.md) | CONV-005 |
| 63 | [The PR says 5 conversations, I thought we added this, which would be six?](exchanges/0063-20260418065216-the-pr-says-5-conversations-i-thought-we-added-this-which-would-be-six.md) | CONV-005 |
| 64 | [We now have a command line GitHub Copilot and a Microsoft Copilot app. Can you investigate addin](exchanges/0064-20260418065216-we-now-have-a-command-line-github-copilot-and-a-microsoft-copilot-app-can-you-investigate.md) | CONV-005 |
| 65 | [First, fix the current PR comments, ensuring that you consider each as indicating a class of err](exchanges/0065-20260418065216-first-fix-the-current-pr-comments-ensuring-that-you-consider-each-as-indicating-a-class-of.md) | CONV-005 |
| 66 | [Ensure you close the comments you address with apropriate comments](exchanges/0066-20260418065216-ensure-you-close-the-comments-you-address-with-apropriate-comments.md) | CONV-005 |
| 67 | [merge](exchanges/0067-20260418065216-merge.md) | CONV-005 |
| 68 | [Do we need a plan or are we ready to implement the evaluation on a new branch? I want to make su](exchanges/0068-20260418065216-do-we-need-a-plan-or-are-we-ready-to-implement-the-evaluation-on-a-new-branch-i-want-to-ma.md) | CONV-005 |
| 69 | [I want full coverage with the best models selected in each client so that includes GitHub Copilo](exchanges/0069-20260418065216-i-want-full-coverage-with-the-best-models-selected-in-each-client-so-that-includes-github.md) | CONV-005 |
| 70 | [override and use GPT-5.4 on Copilot as I found contradictory documentation and this was from a m](exchanges/0070-20260418065216-override-and-use-gpt-5-4-on-copilot-as-i-found-contradictory-documentation-and-this-was-fr.md) | CONV-005 |
| 71 | [If there is an authentication block and a policy issue, can I fix them? I want all to run succes](exchanges/0071-20260418065216-if-there-is-an-authentication-block-and-a-policy-issue-can-i-fix-them-i-want-all-to-run-su.md) | CONV-005 |
| 72 | [I see the issue, my account has a personal GitHub and an Org but I am working only with personal](exchanges/0072-20260418065216-i-see-the-issue-my-account-has-a-personal-github-and-an-org-but-i-am-working-only-with-per.md) | CONV-005 |
| 73 | [PS [LOCAL_REPO]> cd [LOCAL_USER_PATH]](exchanges/0073-20260418065216-ps-local-repo-cd-local-user-path.md) | CONV-005 |
| 74 | [python3 challenge-2/tools/run_wiki_eval.py --clients github-copilot --questions Q001 --timeout-s](exchanges/0074-20260418065216-python3-challenge-2-tools-run-wiki-eval-py-clients-github-copilot-questions-q001-timeout-s.md) | CONV-005 |
| 75 | [It shows ╭──────────────────────────────────────────────────────────────────────────────╮](exchanges/0075-20260418065216-it-shows.md) | CONV-005 |
| 76 | [Looks like it's blocked at policy level, I don't understand as this is a personal project and is](exchanges/0076-20260418065216-looks-like-it-s-blocked-at-policy-level-i-don-t-understand-as-this-is-a-personal-project-a.md) | CONV-005 |
| 77 | [Is there anything else I need to do before we run the evaluation](exchanges/0077-20260418065216-is-there-anything-else-i-need-to-do-before-we-run-the-evaluation.md) | CONV-005 |
| 78 | [There were a few "Can I trust this folder" prompts holding things up. I want all to use the best](exchanges/0078-20260418065216-there-were-a-few-can-i-trust-this-folder-prompts-holding-things-up-i-want-all-to-use-the-b.md) | CONV-005 |
| 79 | [Allow Claude to use the local settings file which is specifying the model (managed by DSIT) so t](exchanges/0079-20260418065216-allow-claude-to-use-the-local-settings-file-which-is-specifying-the-model-managed-by-dsit.md) | CONV-005 |
| 80 | [The Wiki is also available over GitHub, would that solve the Can't access local paths problem?](exchanges/0080-20260418065216-the-wiki-is-also-available-over-github-would-that-solve-the-can-t-access-local-paths-probl.md) | CONV-005 |
| 81 | [Claude says MCP Failed - related?](exchanges/0081-20260418065216-claude-says-mcp-failed-related.md) | CONV-005 |
| 82 | [I passed the claude CLI error to Claude Coworker (personal authentication) and had this:](exchanges/0082-20260418065216-i-passed-the-claude-cli-error-to-claude-coworker-personal-authentication-and-had-this.md) | CONV-005 |
| 83 | [It looked like the Microsoft 365 Copilot failed because the prompt specified:](exchanges/0083-20260418065216-it-looked-like-the-microsoft-365-copilot-failed-because-the-prompt-specified.md) | CONV-005 |
| 84 | [If GitHub access fails for the M365 Copilot, can we just have the Wiki replicated in OneDrive - ](exchanges/0084-20260418065216-if-github-access-fails-for-the-m365-copilot-can-we-just-have-the-wiki-replicated-in-onedri.md) | CONV-005 |
| 85 | [The idea is to allow the AI to use the Wiki as a knowledge base - what is the best strategy for ](exchanges/0085-20260418065216-the-idea-is-to-allow-the-ai-to-use-the-wiki-as-a-knowledge-base-what-is-the-best-strategy.md) | CONV-005 |
| 86 | [Another thought, there is now a Copilot desktop app on the Mac, what can this do? Should we cons](exchanges/0086-20260418065216-another-thought-there-is-now-a-copilot-desktop-app-on-the-mac-what-can-this-do-should-we-c.md) | CONV-005 |
| 87 | [Okay, I have a synced OneDrive here [LOCAL_USER_PATH]](exchanges/0087-20260418065216-okay-i-have-a-synced-onedrive-here-local-user-path.md) | CONV-005 |
| 88 | [Can you try a smoke test now](exchanges/0088-20260418065216-can-you-try-a-smoke-test-now.md) | CONV-005 |
| 89 | [just the Copilots](exchanges/0089-20260418065216-just-the-copilots.md) | CONV-005 |
| 90 | [We won't use SharePoint but check if we can use my personal OneDrive, it seems as though it has ](exchanges/0090-20260418065216-we-won-t-use-sharepoint-but-check-if-we-can-use-my-personal-onedrive-it-seems-as-though-it.md) | CONV-005 |
| 91 | [Any good giving the share link?](exchanges/0091-20260418065216-any-good-giving-the-share-link.md) | CONV-005 |
| 92 | [Update Deep Research Prompt](exchanges/0092-20260418065216-update-deep-research-prompt.md) | CONV-005 |
| 93 | [Create Codex Postmortem Wiki](exchanges/0093-20260418065216-create-codex-postmortem-wiki.md) | CONV-005 |
| 94 | [Agree, add all [LOCAL_STATE_FILE] to gitignore. Note that you have two other equivalent reports, the docx](exchanges/0094-20260418065216-agree-add-all-local-state-file-to-gitignore-note-that-you-have-two-other-equivalent-report.md) | CONV-005 |
| 95 | [Continue and include the lint check after the links have been resolved. Ensure extensive cross-l](exchanges/0095-20260418065216-continue-and-include-the-lint-check-after-the-links-have-been-resolved-ensure-extensive-cr.md) | CONV-005 |
| 96 | [Decisions](exchanges/0096-20260418065216-decisions.md) | CONV-005 |
| 97 | [Decisions:](exchanges/0097-20260418065216-decisions.md) | CONV-005 |
| 98 | [Decisions:](exchanges/0098-20260418065216-decisions.md) | CONV-005 |
| 99 | [I want to capture this thread as we did with previous ones but need to consider how this is best](exchanges/0099-20260418065216-i-want-to-capture-this-thread-as-we-did-with-previous-ones-but-need-to-consider-how-this-i.md) | CONV-005 |
| 100 | [Should we do both of these within the current PR or only the first, discuss](exchanges/0100-20260418065216-should-we-do-both-of-these-within-the-current-pr-or-only-the-first-discuss.md) | CONV-005 |
| 101 | [Do human rubric scoring in this PR](exchanges/0101-20260418065216-do-human-rubric-scoring-in-this-pr.md) | CONV-005 |
| 102 | [So, is this thread up to date in the PR? Should we wait till after the PR is reviewed and fully ](exchanges/0102-20260418065216-so-is-this-thread-up-to-date-in-the-pr-should-we-wait-till-after-the-pr-is-reviewed-and-fu.md) | CONV-005 |
| 103 | [Okay, more comments to fix as before](exchanges/0103-20260418065216-okay-more-comments-to-fix-as-before.md) | CONV-005 |
| 104 | [Okay, more comments to fix as before](exchanges/0104-20260418065216-okay-more-comments-to-fix-as-before.md) | CONV-005 |
| 105 | [More comments to fix as before, your being sloppy?](exchanges/0105-20260418065216-more-comments-to-fix-as-before-your-being-sloppy.md) | CONV-005 |
| 106 | [yet more comments to fix as before!!](exchanges/0106-20260418065216-yet-more-comments-to-fix-as-before.md) | CONV-005 |
| 107 | [You still have two comments not closed but I believe you fixed before they were "visible" and yo](exchanges/0107-20260418065216-you-still-have-two-comments-not-closed-but-i-believe-you-fixed-before-they-were-visible-an.md) | CONV-005 |
| 108 | [merge](exchanges/0108-20260418065216-merge.md) | CONV-005 |
| 109 | [Create Codex Postmortem Wiki](exchanges/0109-20260418065216-create-codex-postmortem-wiki.md) | CONV-005 |
| 110 | [Create Codex Postmortem Wiki](exchanges/0110-20260418065216-create-codex-postmortem-wiki.md) | CONV-005 |
| 111 | [Create Codex Postmortem Wiki](exchanges/0111-20260418065216-create-codex-postmortem-wiki.md) | CONV-005 |
| 112 | [Commit these changes, ensuring all the documentation is in lockstep](exchanges/0112-20260418065216-commit-these-changes-ensuring-all-the-documentation-is-in-lockstep.md) | CONV-005 |
| 113 | [status of this branch?](exchanges/0113-20260418065216-status-of-this-branch.md) | CONV-005 |

## Publication Counts

- Conversation summaries: 5
- Redacted prompt-response exchanges: 113
- External citations: 3
- Repository artifacts registered: 44

## Scope Notes

- Public conversations are restricted to the curated session IDs named in `tools/build_codex_postmortem.py`; evaluation runs and incidental local sessions are excluded unless deliberately promoted into that curated list.
