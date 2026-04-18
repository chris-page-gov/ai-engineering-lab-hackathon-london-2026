---
title: "Architecture"
tags:
  - "architecture"
  - "codex-postmortem-public"
---

# Public Postmortem Architecture

```mermaid
flowchart LR
  Private["Ignored private postmortem archive"] --> Builder["tools/build_codex_postmortem.py"]
  Builder --> Public["postmortem-public"]
  Public --> Exchanges["Redacted exchange notes"]
  Public --> Citations["Citation-only external sources"]
  Public --> Evidence["GitHub permalinks and registers"]
```

The public folder is intentionally a derivative. It keeps the useful timeline, contribution analysis, and repository evidence while excluding raw local transcripts and full third-party copied source bodies.
