# Public Postmortem Operating Rules

This folder is intended to be committed to GitHub.

- Do not add raw Codex JSONL files or raw transcript sources here.
- Do not add full copied third-party methodology source bodies unless licensing or permission is recorded.
- Keep local filesystem paths, screenshot paths, and private reference repositories redacted.
- Preserve commit-specific GitHub permalinks for tracked repository artifacts.
- Add new conversation session IDs to the curated list in `tools/build_codex_postmortem.py` before regenerating public output.
- Regenerate with `python3 tools/build_codex_postmortem.py` rather than hand-editing generated exchange notes.
- Treat `wiki/readers/` as the standard GitHub-friendly route for following conversations from start to finish.
