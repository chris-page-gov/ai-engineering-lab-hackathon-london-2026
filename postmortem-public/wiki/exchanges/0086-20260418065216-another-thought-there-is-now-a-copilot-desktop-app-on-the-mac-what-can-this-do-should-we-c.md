---
exchange_id: "EX-0086"
title: "Another thought, there is now a Copilot desktop app on the Mac, what can this do? Should we cons"
source_id: "CONV-005"
global_sequence: 86
session_sequence: 34
user_timestamp: "2026-04-19T17:31:19.057Z"
publication_status: "redacted-public-derivative"
tags:
  - "exchange"
  - "codex-postmortem-public"
---

# 0086. Another thought, there is now a Copilot desktop app on the Mac, what can this do? Should we cons

Previous: [EX-0085](0085-20260418065216-the-idea-is-to-allow-the-ai-to-use-the-wiki-as-a-knowledge-base-what-is-the-best-strategy.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0087](0087-20260418065216-okay-i-have-a-synced-onedrive-here-local-user-path.md)

## Publication Boundary

This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.

## Source

- Conversation: CONV-005 (Codex Postmortem, Publication Assessment, and Version 1.1 PR)
- Raw transcript: retained only in the private local evidence archive.

## User Prompt

````text
# Files mentioned by the user:

## Screenshot 2026-04-19 at 18.30.42.png: [TEMP_SCREENSHOT]

## My request for Codex:
Another thought, there is now a Copilot desktop app on the Mac, what can this do? Should we consider this as a solution for the M365 test?


<image name=[Image #1]>
[image attachment omitted: data:image/png;base64; base64 omitted]
</image>
````

## Codex Response

### Response 1 (commentary)

- Timestamp: `2026-04-19T17:31:31.190Z`

````text
I’ll separate two things that look similar but matter for the test: the Mac “Copilot” desktop app, and Microsoft 365 Copilot Chat/agents. I’ll verify the installed app identity locally and check current Microsoft docs so we don’t accidentally test the consumer app when we mean M365 grounding.
````

### Response 2 (final_answer)

- Timestamp: `2026-04-19T17:32:18.263Z`

````text
Short answer: the Mac desktop app is useful, but it should not replace the M365 Copilot web/agent test unless we are deliberately testing the desktop app as its own client.

I inspected the installed apps locally and there are two separate Microsoft apps on this Mac:

- `/Applications/Copilot.app`
  - Bundle: `com.microsoft.copilot-mac`
  - Version: `25.6.440416001`
  - This matches the screenshot.
  - This is the standalone Microsoft Copilot Mac app.

- `/Applications/Microsoft 365 Copilot.app`
  - Bundle: `com.microsoft.m365copilot`
  - Version: `1.2604`
  - This is the Microsoft 365 Copilot app.

**What the screenshot app can do**
The app in the screenshot is the standalone `Copilot.app`, not the `Microsoft 365 Copilot.app`.

Microsoft says Copilot for macOS generally has the same features as `copilot.com`, plus macOS shortcut support, light/dark mode, and some device-context help. It does not currently support Copilot Pages or Deep Research on macOS. Microsoft also documents file upload for Microsoft Copilot, including PDF, DOCX, XLSX, PPTX, TXT, JSON, CSV, and MD, up to 20 files per conversation and 50 MB per file.

So it could upload a small wiki source pack manually. That is useful for a smoke test, especially because Markdown is supported. But it is not a durable knowledge-base integration.

**Why it is not the best M365 test target**
For our evaluation, the key requirement is: “Can the AI use the Challenge 2 wiki as a knowledge base?”

The standalone Mac Copilot app is weaker for that because:

- it is primarily a conversational app, not a managed M365 knowledge source;
- uploaded files are per-chat context, not a reusable scoped agent knowledge base;
- it does not prove SharePoint/Graph/M365 grounding;
- automating the native Mac UI would be more brittle than Playwright against the web UI;
- it may test a different product surface from Microsoft 365 Copilot Chat.

Microsoft’s own distinction is that the Microsoft 365 Copilot app is for Microsoft 365 apps/files and productivity chat, while the standalone Microsoft Copilot app is a conversational AI companion.

**Best strategy**
Use the desktop apps as evidence and fallback, but not as the primary M365 evaluation route.

Recommended ranking:

1. **Best M365 knowledge-base path**
   Create a SharePoint/OneDrive source pack from the wiki, then create a SharePoint Agent or Microsoft 365 declarative agent scoped to that library/folder/site.

2. **Best automation path**
   Keep using the web route at `m365.cloud.microsoft` with Playwright, because it is easier to automate, screenshot, inspect, and reproduce than a native Mac webview.

3. **Useful fallback**
   Use `Microsoft 365 Copilot.app` if the browser path is blocked but the desktop app is signed in and can access the same agent/source pack.

4. **Separate client, not substitute**
   Treat `Copilot.app` as a separate “Microsoft Copilot Mac app” client only if we want to compare the consumer/standalone Copilot experience. It should not be scored as the M365 knowledge-base test unless clearly labelled with caveats.

**What I would do for the repo**
I would keep the current `microsoft-copilot` client pointed at the web UI, and extend the manifest to record both installed Mac apps, which it already largely does. Then add a separate optional client later only if needed:

- `microsoft-365-copilot-desktop`: native Mac app, M365 account, SharePoint/agent grounding, brittle accessibility automation.
- `microsoft-copilot-mac`: standalone Copilot app, manual/uploaded-file grounding, not equivalent to M365.

For the full benchmark, I would not route the primary M365 test through the screenshot app. The better test is: SharePoint-backed wiki agent, exercised via M365 Copilot web or the Microsoft 365 Copilot app, with the app version captured as environment evidence.

Sources:
- [Getting started with Copilot on macOS](https://support.microsoft.com/en-us/topic/getting-started-with-copilot-on-macos-e69021ae-3592-4a0b-b2b6-df7b7f9eeb30)
- [File upload in Microsoft Copilot](https://support.microsoft.com/en-us/topic/file-upload-in-microsoft-copilot-8b7bf432-9576-4b16-9dee-6c19a4169e62)
- [Download the Microsoft 365 Copilot app](https://www.microsoft.com/en-US/microsoft-365-copilot/download-copilot-app)
- [Use Copilot Chat in Microsoft 365 apps](https://support.microsoft.com/en-au/topic/use-copilot-chat-in-microsoft-365-apps-676db5e8-9568-4bdb-bf0b-e207e29e056b)
````

## Contribution Reading

- User contribution: Supplied task direction, constraints, or review feedback.
- Codex contribution: Implemented and validated user-facing workbench behavior.

Previous: [EX-0085](0085-20260418065216-the-idea-is-to-allow-the-ai-to-use-the-wiki-as-a-knowledge-base-what-is-the-best-strategy.md) | Conversation reader: [start-to-finish](../readers/conv-005-codex-postmortem-publication-assessment-and-version-1-1-pr.md) | Next: [EX-0087](0087-20260418065216-okay-i-have-a-synced-onedrive-here-local-user-path.md)
