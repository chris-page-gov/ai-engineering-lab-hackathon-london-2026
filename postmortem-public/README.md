# Public Codex Collaboration Postmortem

This folder is the GitHub-safe replacement for the private `postmortem/` evidence archive for Team DSIT A's Challenge 2 work.

It includes:

- redacted prompt-response exchange notes that preserve sequence and contribution evidence;
- start-to-finish Markdown conversation readers for efficient GitHub browsing;
- conversation summaries instead of raw Codex transcripts;
- citation-only external methodology notes instead of full copied third-party source bodies;
- repository artifact notes with commit-specific GitHub permalinks where available;
- a publication decision register showing inclusion-forward defaults and questions for review.

Start at `wiki/index.md`.

Regenerate both the private and public postmortem folders with:

```bash
python3 tools/build_codex_postmortem.py
```

The standard build uses the curated session IDs in `tools/build_codex_postmortem.py`; add a session there before regenerating if a new conversation should become part of the public postmortem corpus.
