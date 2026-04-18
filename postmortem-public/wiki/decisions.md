---
title: "Publication Decision Register"
tags:
  - "decisions"
  - "codex-postmortem-public"
---

# Publication Decision Register

These decisions use inclusion-forward defaults. Each row includes the question to revisit if a stricter publication posture is needed.

| ID | Default Applied | Decision | Elicitation Question | Status |
|---|---|---|---|---|
| PUB-DEC-001 | Apply | Keep the private postmortem evidence archive out of Git. | Should the raw `postmortem/` evidence archive remain local-only and ignored by Git? | default_applied_pending_user_review |
| PUB-DEC-002 | Include path, redact local machine provenance | Keep `.claude/settings.local.json` as a visible conventional path, but redact absolute local source locations. | Should `.claude/settings.local.json` remain visible in the public exchange notes? | default_applied_pending_user_review |
| PUB-DEC-003 | Include public GitHub evidence links | Keep public GitHub fork permalinks and PR links where they support evidence. | Should public GitHub account, commit, and PR links remain visible where they evidence the timeline? | default_applied_pending_user_review |
| PUB-DEC-004 | Citation metadata and short excerpts only | Do not publish full localized Karpathy X/gist source bodies. | Should full third-party source copies remain private unless permission or an explicit license is obtained? | default_applied_pending_user_review |
| PUB-DEC-005 | Redact private repo URL and local prior-work paths | Redact private/local reference repositories while preserving the design influence. | Should private repo names/URLs and local prior-work paths be replaced with neutral labels? | default_applied_pending_user_review |
| PUB-DEC-006 | Do not claim a GitHub permalink until tracked | Reference the realtime delivery report as local-only until it is intentionally committed. | Should the realtime delivery report be committed later so it can become public permalink evidence? | default_applied_pending_user_review |
| PUB-DEC-007 | Omit image payloads, redact paths | Do not publish screenshot image payloads or local screenshot paths. | Should screenshots stay out of the public package unless individually reviewed? | default_applied_pending_user_review |
| PUB-DEC-008 | Include synthetic fixture references | Do not redact Challenge 2 synthetic fixture values solely because they resemble personal data. | Should synthetic Challenge 2 names/contact-like values remain publishable when context makes them synthetic? | default_applied_pending_user_review |
| PUB-DEC-009 | Include redacted prompt-response files | Preserve the prompt-response sequence in redacted exchange notes. | Should the public package keep one sanitized note per prompt-response exchange? | default_applied_pending_user_review |
