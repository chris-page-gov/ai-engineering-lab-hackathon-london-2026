#!/usr/bin/env python3
"""Build the Codex conversation postmortem wiki.

The builder reads local Codex rollout JSONL files for this repository, fetches
the external methodology references used during the build, and regenerates a
Markdown source archive plus a navigable postmortem wiki with start-to-finish
conversation reader pages.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
TARGET_CWD = str(REPO_ROOT)
POSTMORTEM_ROOT = REPO_ROOT / "postmortem"
POSTMORTEM_PUBLIC_ROOT = REPO_ROOT / "postmortem-public"
SOURCES_DIR = POSTMORTEM_ROOT / "sources"
CONVERSATION_SOURCES_DIR = SOURCES_DIR / "conversations"
EXTERNAL_SOURCES_DIR = SOURCES_DIR / "external"
WIKI_DIR = POSTMORTEM_ROOT / "wiki"
EXCHANGES_DIR = WIKI_DIR / "exchanges"
READERS_DIR = WIKI_DIR / "readers"
WIKI_SOURCES_DIR = WIKI_DIR / "sources"
TOPICS_DIR = WIKI_DIR / "topics"
ENTITIES_DIR = WIKI_DIR / "entities"
MAPS_DIR = WIKI_DIR / "maps"
DATA_DIR = WIKI_DIR / "data"
PUBLIC_WIKI_DIR = POSTMORTEM_PUBLIC_ROOT / "wiki"
PUBLIC_EXCHANGES_DIR = PUBLIC_WIKI_DIR / "exchanges"
PUBLIC_READERS_DIR = PUBLIC_WIKI_DIR / "readers"
PUBLIC_SOURCES_DIR = PUBLIC_WIKI_DIR / "sources"
PUBLIC_TOPICS_DIR = PUBLIC_WIKI_DIR / "topics"
PUBLIC_MAPS_DIR = PUBLIC_WIKI_DIR / "maps"
PUBLIC_DATA_DIR = PUBLIC_WIKI_DIR / "data"

ORIGIN_REPO = "https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026"
BASELINE_TAG = "v1-challenge-2"
PUBLICATION_VERSION = "1.1"
PUBLICATION_BRANCH = "codex/postmortem-wiki"
TEAM_NAME = "Team DSIT A"
ALLOWED_EXTERNAL_SOURCE_HOSTS = {
    "gist.github.com",
    "gist.githubusercontent.com",
    "r.jina.ai",
    "x.com",
}

TITLE_OVERRIDES = {
    "019d9429-01c4-7d32-a161-35c10aabcde4": "Deep Research Prompt and Copilot Review",
    "019d957b-4f68-7ee2-b295-86f448adfbb2": "Karpathy Wiki Planning and Challenge 2 Vault Build",
    "019d960b-6b2c-7260-ad4d-c3f9f308e173": "Wiki Evaluation Harness, Workbench, and Demo Route",
    "019d96ae-4082-79d2-bb12-74ea871e8c5e": "SeeLinks Question Box, PR Hygiene, and Baseline Cleanup",
    "019d9f5c-8f1e-72c1-88a7-7a777db6d3e3": "Codex Postmortem, Publication Assessment, and Version 1.1 PR",
}
CURATED_SESSION_IDS = set(TITLE_OVERRIDES)

ARTIFACT_PATHS = [
    "AGENTS.md",
    "Changelog.md",
    "Context.md",
    "Progress.md",
    "README.md",
    "challenge-02-unlocking-the-dark-data.md",
    "challenge-2/AGENTS.md",
    "challenge-2/tools/build_wiki.py",
    "challenge-2/wiki/index.md",
    "challenge-2/wiki/architecture.md",
    "challenge-2/wiki/demonstration-guide.md",
    "challenge-2/wiki/workbench.md",
    "challenge-2/wiki/evaluation-benchmark.md",
    "challenge-2/wiki/data/source-register.json",
    "challenge-2/evaluation/README.md",
    "challenge-2/evaluation/clients.py",
    "challenge-2/tools/run_wiki_eval.py",
    "challenge-2/tools/wiki_eval_mcp.py",
    "challenge-2/tools/summarise_wiki_eval.py",
    "challenge-2/workbench/README.md",
    "challenge-2/workbench/src/routes/+page.svelte",
    "challenge-2/workbench/src/lib/workbench/model.ts",
    "challenge-2/workbench/src/lib/workbench/types.ts",
    "challenge-2/workbench/src/lib/components/EvidencePanel.svelte",
    "challenge-2/workbench/src/lib/components/SourceCard.svelte",
    "tests/test_challenge2_eval_questions.py",
    "tests/test_challenge2_eval_mcp.py",
    "tests/test_challenge2_workbench_mcp.py",
    "tests/test_build_codex_postmortem.py",
    "output/doc/challenge-2-realtime-delivery-report.md",
    "output/doc/challenge-2-realtime-delivery-report.docx",
    "output/doc/contribution-modes-proposal.md",
    "output/doc/codex-contribution-modes-security-assessment.md",
    "output/doc/linkedin-version-1-1-announcement.md",
    "output/doc/Dark_Data_Engineering_Playbook.pdf",
    "output/doc/Real-Time Dark Data Engineering Timeline.png",
    "output/doc/assets/ai-benchmark-mastery-scoring-guide.png",
    "output/doc/assets/dark-data-workbench-question-box.png",
    "output/doc/assets/knowledge-architecture.png",
    "output/doc/assets/realtime-delivery-timeline.png",
    "output/doc/assets/contribution-modes-proposal/media/image1.png",
    "output/doc/assets/contribution-modes-proposal/mode-authority.svg",
    "output/doc/assets/contribution-modes-proposal/mode-anatomy.svg",
    "output/doc/assets/contribution-modes-proposal/hackathon-stages.svg",
]

EXTERNAL_REFERENCES = [
    {
        "source_id": "EXT-KARPATHY-X-LLM-KNOWLEDGE-BASES",
        "title": "Karpathy X Post: LLM Knowledge Bases",
        "canonical_url": "https://x.com/karpathy/status/2039805659525644595",
        "fetch_url": "https://r.jina.ai/https://x.com/karpathy/status/2039805659525644595",
        "direct_url": "https://x.com/karpathy/status/2039805659525644595",
        "filename": "karpathy-x-2039805659525644595-llm-knowledge-bases.md",
        "kind": "x_post_readable_snapshot",
        "citation_note": "Readable Markdown snapshot from Jina AI over the public X URL; direct X URL is verified separately.",
    },
    {
        "source_id": "EXT-KARPATHY-X-IDEA-FILE",
        "title": "Karpathy X Post: LLM Wiki Idea File",
        "canonical_url": "https://x.com/karpathy/status/2040470801506541998",
        "fetch_url": "https://r.jina.ai/https://x.com/karpathy/status/2040470801506541998",
        "direct_url": "https://x.com/karpathy/status/2040470801506541998",
        "filename": "karpathy-x-2040470801506541998-idea-file.md",
        "kind": "x_post_readable_snapshot",
        "citation_note": "Readable Markdown snapshot from Jina AI over the public X URL; direct X URL is verified separately.",
    },
    {
        "source_id": "EXT-KARPATHY-GIST-LLM-WIKI",
        "title": "Karpathy Gist: LLM Wiki",
        "canonical_url": "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f",
        "fetch_url": "https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw",
        "direct_url": "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f",
        "filename": "karpathy-llm-wiki-gist.raw.md",
        "kind": "gist_raw_markdown",
        "citation_note": "Raw GitHub gist content fetched directly from gist.githubusercontent.com.",
    },
]

FENCED_BLOCK_PATTERN = re.compile(r"(^|\n)(`{3,}|~{3,})[^\n]*\n.*?\n\2[ \t]*(?=\n|$)", re.DOTALL)


@dataclass
class Message:
    role: str
    timestamp: str
    text: str
    phase: str | None = None


@dataclass
class Session:
    source_id: str
    session_id: str
    thread_name: str
    title: str
    start_timestamp: str
    updated_at: str
    cwd: str
    source_path: Path
    source_sha256: str
    messages: list[Message] = field(default_factory=list)
    event_counts: dict[str, int] = field(default_factory=dict)
    tool_counts: dict[str, int] = field(default_factory=dict)
    output_path: Path | None = None


@dataclass
class Exchange:
    exchange_id: str
    global_sequence: int
    session: Session
    session_sequence: int
    title: str
    slug: str
    user_message: Message
    assistant_messages: list[Message]
    output_path: Path | None = None


def run_git(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()
    except FileNotFoundError as exc:
        raise SystemExit("Postmortem build failed: git executable is unavailable on PATH.") from exc


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def slugify(value: str, fallback: str = "item") -> str:
    value = value.lower()
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    value = re.sub(r"-{2,}", "-", value)
    return value[:90].strip("-") or fallback


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def rel_link(from_path: Path, target: Path, label: str) -> str:
    rel = os.path.relpath(target, from_path.parent)
    return f"[{label}]({rel})"


def strip_fenced_blocks(text: str) -> str:
    return FENCED_BLOCK_PATTERN.sub("\n", text)


def write_text(path: Path, text: str, *, read_only: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.chmod(0o644)
    if path.suffix == ".md":
        text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
        text = text.rstrip() + "\n"
    path.write_text(text, encoding="utf-8")
    if read_only:
        path.chmod(0o444)


def reset_generated_dirs() -> None:
    for directory in [CONVERSATION_SOURCES_DIR, EXTERNAL_SOURCES_DIR, WIKI_DIR]:
        if directory.exists():
            for path in directory.rglob("*"):
                if path.is_file():
                    path.chmod(0o644)
            shutil.rmtree(directory)
    for directory in [
        CONVERSATION_SOURCES_DIR,
        EXTERNAL_SOURCES_DIR,
        EXCHANGES_DIR,
        READERS_DIR,
        WIKI_SOURCES_DIR,
        TOPICS_DIR,
        ENTITIES_DIR,
        MAPS_DIR,
        DATA_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)
    if POSTMORTEM_ROOT.exists():
        remove_state_files()


def reset_public_dirs() -> None:
    if POSTMORTEM_PUBLIC_ROOT.exists():
        shutil.rmtree(POSTMORTEM_PUBLIC_ROOT)
    for directory in [
        PUBLIC_EXCHANGES_DIR,
        PUBLIC_READERS_DIR,
        PUBLIC_SOURCES_DIR,
        PUBLIC_TOPICS_DIR,
        PUBLIC_MAPS_DIR,
        PUBLIC_DATA_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)


def remove_state_files() -> None:
    if not POSTMORTEM_ROOT.exists():
        return
    for state_file in POSTMORTEM_ROOT.rglob(".DS_Store"):
        state_file.unlink()


def load_session_index() -> dict[str, dict[str, Any]]:
    index_path = CODEX_HOME / "session_index.jsonl"
    index: dict[str, dict[str, Any]] = {}
    if not index_path.exists():
        return index
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        index[record["id"]] = record
    return index


def session_paths() -> list[Path]:
    paths: list[Path] = []
    sessions_root = CODEX_HOME / "sessions"
    archived_root = CODEX_HOME / "archived_sessions"
    if sessions_root.exists():
        paths.extend(sessions_root.glob("**/*.jsonl"))
    if archived_root.exists():
        paths.extend(archived_root.glob("*.jsonl"))
    return sorted(paths)


def normalise_content_item(item: dict[str, Any]) -> str:
    item_type = item.get("type", "unknown")
    if item_type in {"input_text", "output_text", "text"}:
        return item.get("text", "")
    if item_type in {"input_image", "image"}:
        image_url = item.get("image_url", "")
        if image_url.startswith("data:"):
            header, _, payload = image_url.partition(",")
            digest = sha256_bytes(payload.encode("utf-8"))
            return f"[image attachment omitted: {header}; base64_chars={len(payload)}; sha256={digest}]"
        return f"[image attachment: {image_url}]"
    return f"[non-text content omitted: type={item_type}]"


def message_text(content: Any) -> str:
    if isinstance(content, list):
        parts = [normalise_content_item(item) for item in content if isinstance(item, dict)]
        return "\n".join(part for part in parts if part).strip()
    if isinstance(content, str):
        return content.strip()
    return ""


def is_environment_only(text: str) -> bool:
    stripped = text.strip()
    return stripped.startswith("<environment_context>") and stripped.endswith("</environment_context>")


def is_context_only(text: str) -> bool:
    stripped = text.strip()
    return stripped.startswith("# AGENTS.md instructions for ")


def parse_session(path: Path, index: dict[str, dict[str, Any]]) -> Session | None:
    session_meta: dict[str, Any] | None = None
    messages: list[Message] = []
    event_counts: dict[str, int] = {}
    tool_counts: dict[str, int] = {}

    with path.open(encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            payload = record.get("payload", {})
            record_type = record.get("type", "")
            event_counts[record_type] = event_counts.get(record_type, 0) + 1
            if record_type == "session_meta":
                session_meta = payload
            elif record_type == "response_item" and payload.get("type") == "message":
                role = payload.get("role", "")
                if role not in {"user", "assistant"}:
                    continue
                text = message_text(payload.get("content", []))
                if not text or is_environment_only(text):
                    continue
                messages.append(
                    Message(
                        role=role,
                        timestamp=record.get("timestamp", ""),
                        text=text,
                        phase=payload.get("phase"),
                    )
                )
            elif record_type == "response_item" and payload.get("type") == "function_call":
                name = payload.get("name", "function_call")
                tool_counts[name] = tool_counts.get(name, 0) + 1
            elif record_type == "response_item" and payload.get("type") in {"web_search_call", "tool_search_call"}:
                name = payload.get("type", "tool_call")
                tool_counts[name] = tool_counts.get(name, 0) + 1

    if not session_meta or session_meta.get("cwd") != TARGET_CWD:
        return None

    session_id = session_meta["id"]
    start = session_meta.get("timestamp", "")
    record = index.get(session_id, {})
    thread_name = record.get("thread_name") or f"Codex session {session_id[:8]}"
    title = TITLE_OVERRIDES.get(session_id, thread_name)
    return Session(
        source_id="",
        session_id=session_id,
        thread_name=thread_name,
        title=title,
        start_timestamp=start,
        updated_at=record.get("updated_at", ""),
        cwd=session_meta.get("cwd", ""),
        source_path=path,
        source_sha256=sha256_file(path),
        messages=messages,
        event_counts=event_counts,
        tool_counts=tool_counts,
    )


def discover_sessions() -> list[Session]:
    index = load_session_index()
    sessions = [
        session
        for path in session_paths()
        if (session := parse_session(path, index)) and session.session_id in CURATED_SESSION_IDS
    ]
    sessions.sort(key=lambda item: (item.start_timestamp, item.session_id))
    for number, session in enumerate(sessions, start=1):
        session.source_id = f"CONV-{number:03d}"
    return sessions


def prompt_title(text: str) -> str:
    lower = text.lower()
    if "# files mentioned by the user" in lower and "some of the mermaid is failing" in lower:
        return "Fix Obsidian Mermaid Architecture Diagram"
    if "# files mentioned by the user" in lower and "i'm using" in lower:
        return "Open Challenge 2 Obsidian Vault"
    if lower.strip() == "update the":
        return "Incomplete Update Request"
    if "karpathy wiki method" in lower and "give us a plan" in lower:
        return "Plan Karpathy Wiki Translation"
    if lower.startswith("please implement this plan"):
        return "Implement Karpathy Wiki Vault"
    if "documentation only" in lower:
        return "Add Documentation Lockstep and Evaluation Notes"
    if "deep research prompt" in lower:
        return "Update Deep Research Prompt"
    if "contribution modes proposal" in lower or "full security scan" in lower:
        return "Create Contribution Modes and Security Assessment"
    if "tone of the readme" in lower or "recast it as what this fork actually is" in lower:
        return "Recast README for Challenge 2 Implementation"
    if "version 1.1" in lower or "linkedin post" in lower:
        return "Prepare Version 1.1 Publication PR"
    if "question box" in lower:
        return "Add Workbench Question Box"
    if "latest open pr" in lower or "unblock my most recent open pr" in lower:
        return "Unblock Latest Pull Request"
    if "postmortem" in lower or "writeup the conversations" in lower:
        return "Create Codex Postmortem Wiki"
    if "are we clean" in lower:
        return "Check Publication Branch Status"
    if "are you finished" in lower:
        return "Status Check During Publication Work"
    if "## My request for Codex:" in text:
        text = text.split("## My request for Codex:", 1)[1]
    lines = [line.strip("# ").strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        if line.startswith("## "):
            continue
        if line.startswith("# Files mentioned by the user"):
            continue
        if line.startswith("My request for Codex:"):
            continue
        if line.startswith("Screenshot "):
            continue
        if line.startswith("<image") or line.startswith("</image>") or line.startswith("[image attachment omitted"):
            continue
        cleaned = re.sub(r"^#+\s*", "", line)
        if cleaned:
            return cleaned[:96]
    return "User Prompt"


def build_exchanges(sessions: list[Session]) -> list[Exchange]:
    exchanges: list[Exchange] = []
    global_sequence = 1
    for session in sessions:
        current_user: Message | None = None
        assistant_messages: list[Message] = []
        session_sequence = 0

        def flush() -> None:
            nonlocal current_user, assistant_messages, session_sequence, global_sequence
            if not current_user:
                assistant_messages = []
                return
            if is_context_only(current_user.text):
                current_user = None
                assistant_messages = []
                return
            session_sequence += 1
            title = prompt_title(current_user.text)
            exchange = Exchange(
                exchange_id=f"EX-{global_sequence:04d}",
                global_sequence=global_sequence,
                session=session,
                session_sequence=session_sequence,
                title=title,
                slug=slugify(title),
                user_message=current_user,
                assistant_messages=assistant_messages.copy(),
            )
            exchanges.append(exchange)
            global_sequence += 1
            current_user = None
            assistant_messages = []

        for message in session.messages:
            if message.role == "user":
                flush()
                current_user = message
            elif message.role == "assistant" and current_user:
                assistant_messages.append(message)
        flush()
    return exchanges


def frontmatter(fields: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {yaml_string(str(item))}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif value is None:
            lines.append(f"{key}: null")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {yaml_string(str(value))}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def write_conversation_sources(sessions: list[Session]) -> None:
    for session in sessions:
        date = compact_date(session.start_timestamp)
        slug = slugify(session.title)
        path = CONVERSATION_SOURCES_DIR / f"{session.source_id.lower()}-{date}-{slug}.md"
        session.output_path = path
        message_count = len(session.messages)
        user_count = sum(1 for message in session.messages if message.role == "user")
        assistant_count = sum(1 for message in session.messages if message.role == "assistant")
        parts = [
            frontmatter(
                {
                    "source_id": session.source_id,
                    "title": session.title,
                    "source_type": "codex_conversation_transcript",
                    "session_id": session.session_id,
                    "thread_name": session.thread_name,
                    "start_timestamp": session.start_timestamp,
                    "updated_at": session.updated_at,
                    "cwd": session.cwd,
                    "source_jsonl_path": str(session.source_path),
                    "source_jsonl_sha256": session.source_sha256,
                    "read_only_intent": True,
                    "message_count": message_count,
                    "user_message_count": user_count,
                    "assistant_message_count": assistant_count,
                    "tags": ["source", "conversation", "codex-postmortem"],
                }
            ),
            f"# {session.title}\n\n",
            "This read-only source note preserves the visible user and Codex messages extracted from the local Codex rollout JSONL. Tool calls and private chain-of-thought are not reproduced; event and tool counts are captured for audit context.\n\n",
            "## Session Metadata\n\n",
            f"- Session ID: `{session.session_id}`\n",
            f"- Original thread name: {session.thread_name}\n",
            f"- Local JSONL: `{session.source_path}`\n",
            f"- JSONL SHA-256 at extraction: `{session.source_sha256}`\n",
            f"- User messages: {user_count}\n",
            f"- Codex messages: {assistant_count}\n\n",
            "## Tool Activity Summary\n\n",
        ]
        if session.tool_counts:
            for name, count in sorted(session.tool_counts.items()):
                parts.append(f"- `{name}`: {count}\n")
        else:
            parts.append("- No tool calls recorded in the visible rollout.\n")
        parts.append("\n## Transcript\n\n")
        for index, message in enumerate(session.messages, start=1):
            role = "User" if message.role == "user" else "Codex"
            phase = f" ({message.phase})" if message.phase else ""
            parts.append(f"### {index:03d}. {role}{phase}\n\n")
            parts.append(f"- Timestamp: `{message.timestamp}`\n\n")
            parts.append("```text\n")
            parts.append(message.text.rstrip())
            parts.append("\n```\n\n")
        write_text(path, "".join(parts), read_only=True)


def compact_date(timestamp: str) -> str:
    if not timestamp:
        return "unknown-date"
    return re.sub(r"[^0-9]", "", timestamp[:19])


def exchange_path(exchange: Exchange) -> Path:
    session_date = compact_date(exchange.session.start_timestamp)
    return EXCHANGES_DIR / f"{exchange.global_sequence:04d}-{session_date}-{exchange.slug}.md"


def conversation_reader_path(session: Session) -> Path:
    return READERS_DIR / f"{session.source_id.lower()}-{slugify(session.title)}.md"


def public_conversation_reader_path(session: Session) -> Path:
    return PUBLIC_READERS_DIR / f"{session.source_id.lower()}-{slugify(session.title)}.md"


def exchange_anchor(exchange: Exchange) -> str:
    return f"ex-{exchange.global_sequence:04d}"


def grouped_exchanges_by_session(sessions: list[Session], exchanges: list[Exchange]) -> dict[str, list[Exchange]]:
    return {
        session.session_id: sorted(
            [exchange for exchange in exchanges if exchange.session.session_id == session.session_id],
            key=lambda exchange: exchange.session_sequence,
        )
        for session in sessions
    }


def neighboring_exchanges(exchange: Exchange, exchanges: list[Exchange]) -> tuple[Exchange | None, Exchange | None]:
    session_exchanges = sorted(
        [candidate for candidate in exchanges if candidate.session.session_id == exchange.session.session_id],
        key=lambda candidate: candidate.session_sequence,
    )
    try:
        position = session_exchanges.index(exchange)
    except ValueError:
        return None, None
    previous_exchange = session_exchanges[position - 1] if position > 0 else None
    next_exchange = session_exchanges[position + 1] if position + 1 < len(session_exchanges) else None
    return previous_exchange, next_exchange


def exchange_navigation(
    current_path: Path,
    reader_path: Path,
    previous_exchange: Exchange | None,
    next_exchange: Exchange | None,
    *,
    public: bool = False,
) -> str:
    path_for_exchange = public_exchange_path if public else exchange_path
    links = []
    if previous_exchange:
        links.append(f"Previous: {rel_link(current_path, path_for_exchange(previous_exchange), previous_exchange.exchange_id)}")
    links.append(f"Conversation reader: {rel_link(current_path, reader_path, 'start-to-finish')}")
    if next_exchange:
        links.append(f"Next: {rel_link(current_path, path_for_exchange(next_exchange), next_exchange.exchange_id)}")
    return " | ".join(links) + "\n\n"


def fetch_url(url: str) -> tuple[int | None, dict[str, str], bytes, str | None]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_EXTERNAL_SOURCE_HOSTS:
        return None, {}, b"", f"Blocked external source URL: unsupported scheme or host for {parsed.scheme}://{parsed.hostname or ''}"
    request = urllib.request.Request(url, headers={"User-Agent": "codex-postmortem-builder/1.0"})
    try:
        # External references are HTTPS-only and host allowlisted above.
        with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310
            return response.status, dict(response.headers.items()), response.read(), None
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers.items()), exc.read(), str(exc)
    except urllib.error.URLError as exc:
        return None, {}, b"", str(exc)


def write_external_sources(captured_at: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for ref in EXTERNAL_REFERENCES:
        status, headers, data, error = fetch_url(ref["fetch_url"])
        local_path = EXTERNAL_SOURCES_DIR / ref["filename"]
        if data:
            write_text(local_path, data.decode("utf-8", errors="replace"), read_only=True)
        direct_status, direct_headers, direct_data, direct_error = fetch_url(ref["direct_url"])
        record = {
            **ref,
            "captured_at": captured_at,
            "fetch_status": status,
            "fetch_error": error,
            "fetch_content_type": headers.get("Content-Type") or headers.get("content-type"),
            "fetch_etag": headers.get("ETag") or headers.get("etag"),
            "fetch_last_modified": headers.get("Last-Modified") or headers.get("last-modified"),
            "byte_count": len(data),
            "sha256": sha256_bytes(data),
            "local_path": str(local_path.relative_to(REPO_ROOT)),
            "direct_status": direct_status,
            "direct_error": direct_error,
            "direct_content_type": direct_headers.get("Content-Type") or direct_headers.get("content-type"),
            "direct_byte_count": len(direct_data),
            "direct_sha256": sha256_bytes(direct_data),
            "verified": bool(data) and status == 200 and direct_status == 200,
        }
        records.append(record)
    write_text(
        DATA_DIR / "external-source-verification.json",
        json.dumps(records, indent=2, ensure_ascii=False),
    )
    return records


def artifact_permalink(path: str, commit: str) -> str:
    quoted_path = urllib.parse.quote(path, safe="/+._-")
    return f"{ORIGIN_REPO}/blob/{commit}/{quoted_path}"


def artifact_branch_link(path: str) -> str:
    quoted_path = urllib.parse.quote(path, safe="/+._-")
    quoted_branch = urllib.parse.quote(PUBLICATION_BRANCH, safe="")
    return f"{ORIGIN_REPO}/blob/{quoted_branch}/{quoted_path}"


def git_path_exists_at_ref(ref: str, path: str) -> bool:
    try:
        subprocess.check_output(["git", "cat-file", "-e", f"{ref}:{path}"], cwd=REPO_ROOT, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError as exc:
        raise SystemExit("Postmortem build failed: git executable is unavailable on PATH.") from exc
    except subprocess.CalledProcessError:
        return False


def build_artifact_register(commit: str) -> list[dict[str, Any]]:
    tracked = set(run_git(["ls-files"]).splitlines())
    records: list[dict[str, Any]] = []
    for path in ARTIFACT_PATHS:
        local_path = REPO_ROOT / path
        tracked_now = path in tracked
        tracked_at_baseline = git_path_exists_at_ref(commit, path)
        records.append(
            {
                "path": path,
                "exists": local_path.exists(),
                "tracked_at_baseline": tracked_at_baseline,
                "tracked_in_publication_branch": tracked_now,
                "baseline_commit": commit,
                "github_permalink": artifact_permalink(path, commit) if tracked_at_baseline else None,
                "publication_branch": PUBLICATION_BRANCH,
                "publication_branch_url": artifact_branch_link(path) if tracked_now else None,
                "sha256": sha256_file(local_path) if local_path.exists() and local_path.is_file() else None,
            }
        )
    write_text(DATA_DIR / "artifact-register.json", json.dumps(records, indent=2, ensure_ascii=False))
    return records


def write_exchange_files(exchanges: list[Exchange]) -> None:
    for exchange in exchanges:
        path = exchange_path(exchange)
        exchange.output_path = path
        previous_exchange, next_exchange = neighboring_exchanges(exchange, exchanges)
        response_count = len(exchange.assistant_messages)
        fields = {
            "exchange_id": exchange.exchange_id,
            "title": exchange.title,
            "source_id": exchange.session.source_id,
            "session_id": exchange.session.session_id,
            "global_sequence": exchange.global_sequence,
            "session_sequence": exchange.session_sequence,
            "user_timestamp": exchange.user_message.timestamp,
            "assistant_message_count": response_count,
            "tags": ["exchange", "codex-postmortem"],
        }
        parts = [
            frontmatter(fields),
            f"# {exchange.global_sequence:04d}. {exchange.title}\n\n",
            exchange_navigation(path, conversation_reader_path(exchange.session), previous_exchange, next_exchange),
            "## Source\n\n",
            f"- Conversation source: {rel_link(path, exchange.session.output_path or path, exchange.session.source_id)}\n",
            f"- Original thread: {exchange.session.title}\n\n",
            "## User Prompt\n\n",
            fenced_text(exchange.user_message.text),
            "\n",
            "## Codex Response\n\n",
        ]
        if exchange.assistant_messages:
            for number, message in enumerate(exchange.assistant_messages, start=1):
                phase = f" ({message.phase})" if message.phase else ""
                parts.append(f"### Response {number}{phase}\n\n")
                parts.append(f"- Timestamp: `{message.timestamp}`\n\n")
                parts.append(fenced_text(message.text))
                parts.append("\n")
        else:
            parts.append("No Codex response was recorded before the next user message.\n\n")
        parts.extend(
            [
                "## Contribution Reading\n\n",
                "- User contribution: supplied intent, constraints, acceptance criteria, source context, or review direction.\n",
                "- Codex contribution: translated that prompt into repo inspection, implementation choices, file edits, validation, or written analysis.\n",
                "\n",
                exchange_navigation(path, conversation_reader_path(exchange.session), previous_exchange, next_exchange),
            ]
        )
        write_text(path, "".join(parts))


def write_conversation_readers(sessions: list[Session], exchanges: list[Exchange]) -> None:
    grouped = grouped_exchanges_by_session(sessions, exchanges)
    for session in sessions:
        path = conversation_reader_path(session)
        session_exchanges = grouped.get(session.session_id, [])
        source_note = WIKI_SOURCES_DIR / f"{session.source_id.lower()}-{slugify(session.title)}.md"
        fields = {
            "source_id": session.source_id,
            "title": f"{session.title} Reader",
            "reader_type": "start_to_finish_conversation",
            "session_id": session.session_id,
            "exchange_count": len(session_exchanges),
            "tags": ["reader", "conversation", "codex-postmortem"],
        }
        parts = [
            frontmatter(fields),
            f"# {session.source_id}: {session.title}\n\n",
            "This reader inlines the prompt-response exchanges for one conversation in chronological order. Use it when you want to follow the conversation from start to finish without opening each exchange note separately.\n\n",
            "## Navigation\n\n",
            f"- Index: {rel_link(path, WIKI_DIR / 'index.md', 'Codex Postmortem Wiki')}\n",
            f"- Conversation source note: {rel_link(path, source_note, session.source_id)}\n",
            f"- Read-only transcript: {rel_link(path, session.output_path or source_note, 'source transcript')}\n\n",
            "## Exchange Map\n\n",
            "| Exchange | Prompt | Standalone Note |\n",
            "|---|---|---|\n",
        ]
        for exchange in session_exchanges:
            parts.append(
                f"| [{exchange.exchange_id}](#{exchange_anchor(exchange)}) | {exchange.title} | {rel_link(path, exchange.output_path or exchange_path(exchange), 'note')} |\n"
            )
        parts.append("\n## Conversation\n\n")
        for exchange in session_exchanges:
            parts.extend(
                [
                    f'<a id="{exchange_anchor(exchange)}"></a>\n\n',
                    f"### {exchange.exchange_id}: {exchange.title}\n\n",
                    f"- User timestamp: `{exchange.user_message.timestamp}`\n",
                    f"- Standalone note: {rel_link(path, exchange.output_path or exchange_path(exchange), exchange.exchange_id)}\n\n",
                    "#### User Prompt\n\n",
                    fenced_text(exchange.user_message.text),
                    "\n#### Codex Response\n\n",
                ]
            )
            if exchange.assistant_messages:
                for number, message in enumerate(exchange.assistant_messages, start=1):
                    phase = f" ({message.phase})" if message.phase else ""
                    parts.append(f"##### Response {number}{phase}\n\n")
                    parts.append(f"- Timestamp: `{message.timestamp}`\n\n")
                    parts.append(fenced_text(message.text))
                    parts.append("\n")
            else:
                parts.append("No Codex response was recorded before the next user message.\n\n")
            parts.append(f"[Back to exchange map](#exchange-map)\n\n")
        write_text(path, "".join(parts))


def write_source_notes(sessions: list[Session], external_records: list[dict[str, Any]], artifacts: list[dict[str, Any]]) -> None:
    for session in sessions:
        path = WIKI_SOURCES_DIR / f"{session.source_id.lower()}-{slugify(session.title)}.md"
        conversation_path = session.output_path or path
        exchanges = [exchange for exchange in build_exchanges([session]) if not is_context_only(exchange.user_message.text)]
        exchange_links = []
        for exchange in exchanges:
            global_match = next(
                (candidate for candidate in ALL_EXCHANGES if candidate.session.session_id == session.session_id and candidate.session_sequence == exchange.session_sequence),
                None,
            )
            if global_match and global_match.output_path:
                exchange_links.append(f"- {rel_link(path, global_match.output_path, f'{global_match.exchange_id}: {global_match.title}')}\n")
        parts = [
            frontmatter(
                {
                    "source_id": session.source_id,
                    "title": session.title,
                    "source_type": "codex_conversation",
                    "session_id": session.session_id,
                    "tags": ["source", "conversation", "codex-postmortem"],
                }
            ),
            f"# {session.title}\n\n",
            f"- Read-only transcript: {rel_link(path, conversation_path, conversation_path.name)}\n",
            f"- Start-to-finish reader: {rel_link(path, conversation_reader_path(session), 'conversation reader')}\n",
            f"- Local JSONL hash at extraction: `{session.source_sha256}`\n",
            f"- User visible messages: {sum(1 for item in session.messages if item.role == 'user')}\n",
            f"- Codex visible messages: {sum(1 for item in session.messages if item.role == 'assistant')}\n\n",
            "## Exchange Notes\n\n",
        ]
        parts.extend(exchange_links or ["No prompt-response exchange files were generated for this source.\n"])
        write_text(path, "".join(parts))

    for record in external_records:
        path = WIKI_SOURCES_DIR / f"{record['source_id'].lower()}.md"
        local = REPO_ROOT / record["local_path"]
        parts = [
            frontmatter(
                {
                    "source_id": record["source_id"],
                    "title": record["title"],
                    "source_type": record["kind"],
                    "canonical_url": record["canonical_url"],
                    "fetch_url": record["fetch_url"],
                    "verified": bool(record["verified"]),
                    "tags": ["source", "external", "methodology", "codex-postmortem"],
                }
            ),
            f"# {record['title']}\n\n",
            f"- Canonical URL: [{record['canonical_url']}]({record['canonical_url']})\n",
            f"- Fetch URL: [{record['fetch_url']}]({record['fetch_url']})\n",
            f"- Local copy: {rel_link(path, local, local.name)}\n",
            f"- Fetch status: `{record['fetch_status']}`; direct status: `{record['direct_status']}`\n",
            f"- Local SHA-256: `{record['sha256']}`\n",
            f"- Verification note: {record['citation_note']}\n\n",
            "## Use In Postmortem\n\n",
            "This source anchors the method used for the Challenge 2 wiki: raw sources stay immutable, the generated wiki is maintained by the LLM, and schema/log/index files make the work auditable.\n",
        ]
        write_text(path, "".join(parts))

    for record in artifacts:
        source_slug = slugify(record["path"])
        path = WIKI_SOURCES_DIR / f"artifact-{source_slug}.md"
        parts = [
            frontmatter(
                {
                    "source_id": f"ART-{source_slug[:48]}",
                    "title": record["path"],
                    "source_type": "repository_artifact",
                    "baseline_commit": record["baseline_commit"],
                    "tracked_at_baseline": bool(record["tracked_at_baseline"]),
                    "tags": ["source", "repository-artifact", "codex-postmortem"],
                }
            ),
            f"# {record['path']}\n\n",
            f"- Exists locally: `{record['exists']}`\n",
            f"- Tracked at `{record['baseline_commit']}`: `{record['tracked_at_baseline']}`\n",
            f"- Tracked on publication branch `{record.get('publication_branch')}`: `{record.get('tracked_in_publication_branch')}`\n",
            f"- SHA-256: `{record.get('sha256')}`\n",
        ]
        if record.get("github_permalink"):
            parts.append(f"- GitHub permalink: [{record['path']}]({record['github_permalink']})\n")
        else:
            parts.append("- GitHub permalink: not available for this source at the tagged baseline.\n")
        if record.get("publication_branch_url"):
            parts.append(f"- Publication branch link: [{record['path']}]({record['publication_branch_url']})\n")
        if record.get("note"):
            parts.append(f"- Note: {record['note']}\n")
        write_text(path, "".join(parts))


def infer_user_contribution(exchange: Exchange) -> str:
    text = exchange.user_message.text.lower()
    if _has_phrase(text, "give us a plan"):
        return "Set the strategic goal and named the Karpathy Wiki method as the design frame."
    if _has_phrase(text, "please implement"):
        return "Approved implementation and supplied a detailed acceptance plan."
    if _has_phrase(text, "documentation only"):
        return "Constrained the task to documentation and evaluation design."
    if _has_phrase(text, "question box"):
        return "Identified a user-facing gap in the workbench export flow."
    if _has_word(text, "postmortem"):
        return "Defined the evidence-preservation goal and requested a research wiki plus analysis."
    if _has_any_phrase(text, ["pull request", "pull requests"]) or _has_any_word(text, ["pr", "prs"]):
        return "Asked Codex to inspect GitHub state and unblock the repository workflow."
    return "Supplied task direction, constraints, or review feedback."


def infer_codex_contribution(exchange: Exchange) -> str:
    response_text = "\n".join(message.text for message in exchange.assistant_messages).lower()
    if _has_phrase(response_text, "strict build") or (
        _has_word(response_text, "generated") and _has_word(response_text, "wiki")
    ):
        return "Mapped the request into repeatable generation, linting, and source-backed wiki artifacts."
    if _has_any_word(response_text, ["playwright", "svelte"]):
        return "Implemented and validated user-facing workbench behavior."
    if (
        _has_any_phrase(response_text, ["pull request", "pull requests"])
        or _has_any_word(response_text, ["git", "github", "pr", "prs", "commit", "branch", "merge"])
    ):
        return "Inspected repository/GitHub state and adjusted branch or PR hygiene."
    if _has_word(response_text, "plan"):
        return "Translated the user intent into a concrete implementation plan."
    if not response_text:
        return "No visible response before the next user message."
    return "Performed repo analysis, implementation, validation, or synthesis in response."


def _has_phrase(text: str, phrase: str) -> bool:
    return phrase in text


def _has_any_phrase(text: str, phrases: list[str]) -> bool:
    return any(_has_phrase(text, phrase) for phrase in phrases)


def _has_word(text: str, word: str) -> bool:
    return re.search(rf"(?<![a-z0-9]){re.escape(word.lower())}(?![a-z0-9])", text.lower()) is not None


def _has_any_word(text: str, words: list[str]) -> bool:
    return any(_has_word(text, word) for word in words)


def write_data_registers(
    sessions: list[Session],
    exchanges: list[Exchange],
    external_records: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
) -> None:
    session_records = []
    for session in sessions:
        session_records.append(
            {
                "source_id": session.source_id,
                "session_id": session.session_id,
                "title": session.title,
                "thread_name": session.thread_name,
                "start_timestamp": session.start_timestamp,
                "updated_at": session.updated_at,
                "cwd": session.cwd,
                "source_jsonl_path": str(session.source_path),
                "source_jsonl_sha256": session.source_sha256,
                "source_markdown_path": str((session.output_path or Path()).relative_to(REPO_ROOT)),
                "reader_path": str(conversation_reader_path(session).relative_to(REPO_ROOT)),
                "user_message_count": sum(1 for message in session.messages if message.role == "user"),
                "assistant_message_count": sum(1 for message in session.messages if message.role == "assistant"),
                "tool_counts": session.tool_counts,
            }
        )
    exchange_records = []
    for exchange in exchanges:
        exchange_records.append(
            {
                "exchange_id": exchange.exchange_id,
                "global_sequence": exchange.global_sequence,
                "session_source_id": exchange.session.source_id,
                "session_id": exchange.session.session_id,
                "session_sequence": exchange.session_sequence,
                "title": exchange.title,
                "user_timestamp": exchange.user_message.timestamp,
                "assistant_message_count": len(exchange.assistant_messages),
                "path": str((exchange.output_path or Path()).relative_to(REPO_ROOT)),
                "user_contribution": infer_user_contribution(exchange),
                "codex_contribution": infer_codex_contribution(exchange),
            }
        )
    write_text(DATA_DIR / "session-register.json", json.dumps(session_records, indent=2, ensure_ascii=False))
    write_text(DATA_DIR / "exchange-register.json", json.dumps(exchange_records, indent=2, ensure_ascii=False))
    write_text(DATA_DIR / "source-register.json", json.dumps({"sessions": session_records, "external_sources": external_records, "artifacts": artifacts}, indent=2, ensure_ascii=False))


def write_topic_pages(exchanges: list[Exchange], artifacts: list[dict[str, Any]]) -> None:
    contribution_rows = []
    for exchange in exchanges:
        contribution_rows.append(
            f"| {exchange.exchange_id} | {exchange.title} | {infer_user_contribution(exchange)} | {infer_codex_contribution(exchange)} |"
        )
    write_text(
        TOPICS_DIR / "human-codex-contribution-patterns.md",
        frontmatter(
            {
                "title": "Human and Codex Contribution Patterns",
                "tags": ["topic", "contribution-analysis", "codex-postmortem"],
            }
        )
        + "# Human and Codex Contribution Patterns\n\n"
        + "The conversations show a consistent split: the user supplied goals, constraints, source context, and quality bars; Codex supplied repository discovery, detailed implementation, tool orchestration, validation, and synthesis.\n\n"
        + "| Exchange | Prompt | User Contribution | Codex Contribution |\n"
        + "|---|---|---|---|\n"
        + "\n".join(contribution_rows)
        + "\n",
    )

    methodology = textwrap.dedent(
        """\
        # Methodology Translation

        Karpathy's LLM Wiki pattern was translated into Challenge 2 as a local, auditable build pipeline rather than a live RAG or chat product. The key method decisions were:

        - Raw Challenge 2 source files remain immutable.
        - Generated Markdown source notes, topic pages, entity pages, maps, indexes, logs, and machine-readable registers form the maintained wiki layer.
        - `AGENTS.md` files act as schema and operating rules for future Codex runs.
        - Linting, tests, and documentation lockstep make the wiki more than a one-off demo artifact.
        - The postmortem applies the same pattern to the Codex conversations themselves.
        """
    )
    write_text(
        TOPICS_DIR / "methodology-translation.md",
        frontmatter({"title": "Methodology Translation", "tags": ["topic", "methodology", "codex-postmortem"]}) + methodology,
    )

    tracked = [record for record in artifacts if record.get("tracked_at_baseline")]
    local_only = [record for record in artifacts if not record.get("tracked_at_baseline")]
    parts = [
        frontmatter({"title": "Repository Evidence and Permalinks", "tags": ["topic", "evidence", "codex-postmortem"]}),
        "# Repository Evidence and Permalinks\n\n",
        f"The baseline commit is `{tracked[0]['baseline_commit'] if tracked else 'unknown'}`. Tracked artifacts below use GitHub permalinks to the fork so their state can be reconstructed independently of later branch edits.\n\n",
        "## Tracked Baseline Artifacts\n\n",
        "| Path | Permalink |\n|---|---|\n",
    ]
    for record in tracked:
        parts.append(f"| `{record['path']}` | [open]({record['github_permalink']}) |\n")
    parts.append("\n## Local-Only Sources\n\n")
    for record in local_only:
        parts.append(f"- `{record['path']}`: {record.get('note') or 'not tracked at the baseline'}\n")
    write_text(TOPICS_DIR / "repository-evidence-and-permalinks.md", "".join(parts))


def write_entities() -> None:
    entities = {
        "user": "The human project owner. The user supplied goals, constraints, judgement calls, and postmortem framing.",
        "codex": "The AI coding assistant. Codex inferred implementation details, edited files, ran tools, validated changes, and produced synthesis.",
        "challenge-2": "The selected hackathon problem: unlocking dark data by converting synthetic government documents into a structured, navigable knowledge base.",
        "karpathy-llm-wiki": "The methodology source: raw sources, generated wiki, schema, index, log, ingest/query/lint operations.",
    }
    for slug, body in entities.items():
        title = slug.replace("-", " ").title()
        write_text(
            ENTITIES_DIR / f"{slug}.md",
            frontmatter({"title": title, "tags": ["entity", "codex-postmortem"]}) + f"# {title}\n\n{body}\n",
        )


def write_maps(sessions: list[Session], exchanges: list[Exchange]) -> None:
    parts = [
        frontmatter({"title": "Conversation Map", "tags": ["map", "conversation", "codex-postmortem"]}),
        "# Conversation Map\n\n",
        "| Source | Conversation | Reader | Exchange Count | Transcript |\n",
        "|---|---|---|---:|---|\n",
    ]
    for session in sessions:
        count = sum(1 for exchange in exchanges if exchange.session.session_id == session.session_id)
        source_note = WIKI_SOURCES_DIR / f"{session.source_id.lower()}-{slugify(session.title)}.md"
        parts.append(
            f"| {session.source_id} | {rel_link(MAPS_DIR / 'conversation-map.md', source_note, session.title)} | {rel_link(MAPS_DIR / 'conversation-map.md', conversation_reader_path(session), 'read')} | {count} | {rel_link(MAPS_DIR / 'conversation-map.md', session.output_path or source_note, 'source')} |\n"
        )
    write_text(MAPS_DIR / "conversation-map.md", "".join(parts))

    chronology = [
        frontmatter({"title": "Build Chronology", "tags": ["map", "timeline", "codex-postmortem"]}),
        "# Build Chronology\n\n",
        "| Time | Event | Evidence |\n",
        "|---|---|---|\n",
    ]
    for session in sessions:
        source_note = WIKI_SOURCES_DIR / f"{session.source_id.lower()}-{slugify(session.title)}.md"
        chronology.append(f"| `{session.start_timestamp}` | {session.title} | {rel_link(MAPS_DIR / 'build-chronology.md', source_note, session.source_id)} |\n")
    write_text(MAPS_DIR / "build-chronology.md", "".join(chronology))


def write_architecture() -> None:
    text = textwrap.dedent(
        """\
        # Postmortem Wiki Architecture

        This folder mirrors the Challenge 2 wiki pattern. Local Codex conversations and external methodology references are immutable source material. The generated wiki then separates prompt-response exchanges, start-to-finish conversation readers, topic synthesis, entity pages, maps, and machine-readable registers.

        ```mermaid
        flowchart LR
          Raw["Read-only sources\\nconversations and external snapshots"] --> Builder["tools/build_codex_postmortem.py"]
          Builder --> Wiki["postmortem/wiki\\nexchange notes, topics, maps"]
          Wiki --> Readers["conversation readers\\nstart-to-finish Markdown"]
          Builder --> Data["postmortem/wiki/data\\nregisters and verification"]
          Wiki --> Postmortem["Detailed postmortem"]
          Data --> Postmortem
        ```

        The read-only source files are marked read-only on the local filesystem after generation. Git does not preserve that bit, so the frontmatter also records `read_only_intent: true`.
        """
    )
    write_text(WIKI_DIR / "architecture.md", frontmatter({"title": "Architecture", "tags": ["architecture", "codex-postmortem"]}) + text)


def write_methodology_page(external_records: list[dict[str, Any]]) -> None:
    parts = [
        frontmatter({"title": "Methodology Sources", "tags": ["methodology", "external-sources", "codex-postmortem"]}),
        "# Methodology Sources\n\n",
        "The postmortem localises and cites the sources that shaped the Challenge 2 approach.\n\n",
        "| Source | Canonical URL | Local Copy | Verification |\n",
        "|---|---|---|---|\n",
    ]
    for record in external_records:
        local = REPO_ROOT / record["local_path"]
        source_note = WIKI_SOURCES_DIR / f"{record['source_id'].lower()}.md"
        parts.append(
            f"| {rel_link(WIKI_DIR / 'methodology.md', source_note, record['title'])} | [open]({record['canonical_url']}) | {rel_link(WIKI_DIR / 'methodology.md', local, local.name)} | status `{record['fetch_status']}`, sha `{record['sha256'][:12]}` |\n"
        )
    parts.append(
        "\nThe X source pages are localised through a readable snapshot fetch while the canonical X URLs are checked separately. The GitHub gist is fetched from the raw gist endpoint and has an ETag recorded in the verification register.\n"
    )
    write_text(WIKI_DIR / "methodology.md", "".join(parts))


def write_postmortem(sessions: list[Session], exchanges: list[Exchange], artifacts: list[dict[str, Any]]) -> None:
    baseline = artifacts[0]["baseline_commit"] if artifacts else "unknown"
    report = next((record for record in artifacts if record["path"] == "output/doc/challenge-2-realtime-delivery-report.md"), None)
    parts = [
        frontmatter({"title": "Detailed Postmortem", "tags": ["postmortem", "analysis", "codex-postmortem"]}),
        "# Detailed Postmortem\n\n",
        "## Executive Summary\n\n",
        "The Challenge 2 build is a strong example of AI-assisted engineering where the human supplied the intent, constraints, and quality bar, while Codex inferred most implementation details and carried them through to code, documentation, tests, and evidence. The collaboration worked because the prompts were outcome-focused but bounded by repository rules: raw data could not be altered, documentation had to move in lockstep, and validation had to be run before claiming completion.\n\n",
        f"The current committed baseline is `{baseline}`, tagged locally as `{BASELINE_TAG}`. The postmortem work is isolated on `codex/postmortem-wiki`.\n\n",
        "## What The User Contributed\n\n",
        "- Selected Challenge 2 and framed the problem as making government dark data findable and structured.\n",
        "- Named the Karpathy LLM Wiki method and asked Codex to translate it into a Challenge 2 Obsidian knowledge base.\n",
        "- Approved implementation after the plan and supplied acceptance criteria for metadata, source coverage, linting, and demo questions.\n",
        "- Constrained later work to documentation, evaluation, and evidence rather than uncontrolled feature expansion.\n",
        "- Identified user-facing gaps, including preserving a question through Browser AI exports and saved checks.\n",
        "- Asked for this postmortem so the learning objective of the day, how AI coding assistants contribute, is explicit rather than implicit in the commits.\n\n",
        "## What Codex Contributed\n\n",
        "- Inspected the repository and discovered the real source corpus, existing docs, available CLI tools, and validation constraints.\n",
        "- Verified the external LLM Wiki pattern, then converted it into a concrete vault schema and generator design.\n",
        "- Implemented the Challenge 2 wiki builder, source notes, topic/entity/map pages, source register, lint report, and operating rules.\n",
        "- Built the evaluation benchmark and harness so multiple agents could be compared against the same wiki-only task.\n",
        "- Built the Dark Data Workbench UI and MCP surfaces, including tests and docs for the demo route.\n",
        "- Ran validation commands, fixed failures, updated documentation, and managed GitHub/PR hygiene.\n",
        "- Generated this postmortem wiki from the conversation evidence rather than relying on memory.\n\n",
        "## Timeline Reading\n\n",
    ]
    for session in sessions:
        source_note = WIKI_SOURCES_DIR / f"{session.source_id.lower()}-{slugify(session.title)}.md"
        parts.append(f"- `{session.start_timestamp}`: {rel_link(WIKI_DIR / 'postmortem.md', source_note, session.title)}.\n")
    parts.extend(
        [
            "\n## Evidence Quality\n\n",
            "The strongest evidence is the Git history and GitHub permalinks because they capture committed state. The conversation transcripts show the decision path and division of labour, but they are local operational evidence and may include local paths or sensitive workflow context. The external methodology snapshots are useful for reconstructing why the wiki pattern was chosen, with the gist serving as the clearest source and the X posts serving as origin/context evidence.\n\n",
            "The local report `output/doc/challenge-2-realtime-delivery-report.md` is included in the artifact register as a source requested by the user.",
        ]
    )
    if report and not report.get("tracked_at_baseline"):
        parts.append(" It was not tracked at the tagged baseline, so this wiki marks it as local-only until it is committed.\n\n")
    else:
        parts.append("\n\n")
    parts.extend(
        [
            "## What Worked\n\n",
            "- The user did not need to specify every file or class. Codex could infer the implementation surface by reading the repo and the challenge brief.\n",
            "- Documentation lockstep kept the work explainable as the implementation grew.\n",
            "- The wiki pattern fitted the problem because it made source provenance, metadata, contradictions, and review status visible.\n",
            "- Tests and linting converted a one-day prototype into an auditable artifact.\n\n",
            "## What Was Risky\n\n",
            "- The broad prompts gave Codex latitude to create a large surface area quickly; this increases review burden.\n",
            "- Local conversation transcripts contain evidence but are not automatically suitable for publication.\n",
            "- Some sources, including the realtime delivery report, were local-only at the time of this postmortem build.\n",
            "- External social media pages are dynamic and hard to archive perfectly; verification records must be kept with the local snapshots.\n\n",
            "## Lessons For AI Code Assistant Use\n\n",
            "1. A good AI coding assistant can turn intent into architecture, but the human still has to set the purpose and constraints.\n",
            "2. Repository operating rules materially improve agent behaviour because they make quality gates explicit.\n",
            "3. AI-generated implementation should leave evidence: commits, docs, validation logs, source registers, and reproducible scripts.\n",
            "4. The most useful collaboration pattern was not prompt-and-answer; it was prompt, inspect, infer, implement, validate, document, and then preserve the reasoning trail.\n\n",
            "## Next Decisions\n\n",
            "- Decide whether to commit and push the postmortem branch.\n",
            "- Decide whether conversation sources need redaction before any public publication.\n",
            "- Decide whether to add the local realtime delivery report to Git so it can receive a GitHub permalink.\n",
            "- Turn this wiki into a colleague-facing report or slide deck if the audience needs a shorter narrative.\n",
        ]
    )
    write_text(WIKI_DIR / "postmortem.md", "".join(parts))


def write_index(sessions: list[Session], exchanges: list[Exchange], external_records: list[dict[str, Any]], artifacts: list[dict[str, Any]]) -> None:
    parts = [
        frontmatter({"title": "Codex Postmortem Wiki", "tags": ["index", "codex-postmortem"]}),
        "# Codex Postmortem Wiki\n\n",
        "This wiki reconstructs the Challenge 2 Codex collaboration from local conversation evidence, repository artifacts, and verified external methodology sources.\n\n",
        "## Start Here\n\n",
        f"- {rel_link(WIKI_DIR / 'index.md', WIKI_DIR / 'postmortem.md', 'Detailed Postmortem')}\n",
        f"- {rel_link(WIKI_DIR / 'index.md', POSTMORTEM_ROOT / 'publication-readiness-report.md', 'Publication Readiness Report')}\n",
        f"- {rel_link(WIKI_DIR / 'index.md', WIKI_DIR / 'architecture.md', 'Postmortem Wiki Architecture')}\n",
        f"- {rel_link(WIKI_DIR / 'index.md', WIKI_DIR / 'methodology.md', 'Methodology Sources')}\n",
        f"- {rel_link(WIKI_DIR / 'index.md', MAPS_DIR / 'conversation-map.md', 'Conversation Map')}\n",
        f"- {rel_link(WIKI_DIR / 'index.md', MAPS_DIR / 'build-chronology.md', 'Build Chronology')}\n\n",
        "## Conversation Sources\n\n",
        "| Source | Conversation | Reader | Exchanges | Read-only Transcript |\n",
        "|---|---|---|---:|---|\n",
    ]
    for session in sessions:
        count = sum(1 for exchange in exchanges if exchange.session.session_id == session.session_id)
        source_note = WIKI_SOURCES_DIR / f"{session.source_id.lower()}-{slugify(session.title)}.md"
        parts.append(
            f"| {session.source_id} | {rel_link(WIKI_DIR / 'index.md', source_note, session.title)} | {rel_link(WIKI_DIR / 'index.md', conversation_reader_path(session), 'read')} | {count} | {rel_link(WIKI_DIR / 'index.md', session.output_path or source_note, 'source')} |\n"
        )
    parts.extend(
        [
            "\n## Prompt-Response Exchanges\n\n",
            "| Sequence | Exchange | Source |\n",
            "|---:|---|---|\n",
        ]
    )
    for exchange in exchanges:
        parts.append(f"| {exchange.global_sequence} | {rel_link(WIKI_DIR / 'index.md', exchange.output_path or WIKI_DIR, exchange.title)} | {exchange.session.source_id} |\n")
    parts.extend(
        [
            "\n## External Methodology Sources\n\n",
            "| Source | Localised Copy | Verified |\n",
            "|---|---|---|\n",
        ]
    )
    for record in external_records:
        source_note = WIKI_SOURCES_DIR / f"{record['source_id'].lower()}.md"
        parts.append(f"| {rel_link(WIKI_DIR / 'index.md', source_note, record['title'])} | `{record['local_path']}` | `{record['verified']}` |\n")
    parts.extend(
        [
            "\n## Data Registers\n\n",
            f"- {rel_link(WIKI_DIR / 'index.md', DATA_DIR / 'session-register.json', 'Session register')}\n",
            f"- {rel_link(WIKI_DIR / 'index.md', DATA_DIR / 'exchange-register.json', 'Exchange register')}\n",
            f"- {rel_link(WIKI_DIR / 'index.md', DATA_DIR / 'artifact-register.json', 'Artifact register')}\n",
            f"- {rel_link(WIKI_DIR / 'index.md', DATA_DIR / 'external-source-verification.json', 'External source verification')}\n",
            f"- {rel_link(WIKI_DIR / 'index.md', DATA_DIR / 'source-register.json', 'Combined source register')}\n\n",
            "## Scope Notes\n\n",
            f"- Candidate conversations must match Codex session `cwd`: `{TARGET_CWD}`.\n",
            "- Published postmortem conversations are restricted to the curated session IDs named in `tools/build_codex_postmortem.py`; evaluation runs and incidental local sessions are excluded unless deliberately promoted into that curated list.\n",
            f"- Baseline repository permalinks use commit `{artifacts[0]['baseline_commit'] if artifacts else 'unknown'}` in the `chris-page-gov` fork.\n",
            "- The active postmortem thread is captured as of the builder run; later messages can be incorporated by rerunning the builder.\n",
        ]
    )
    write_text(WIKI_DIR / "index.md", "".join(parts))


def write_log(captured_at: str, sessions: list[Session], exchanges: list[Exchange], external_records: list[dict[str, Any]]) -> None:
    lines = [
        frontmatter({"title": "Postmortem Log", "tags": ["log", "codex-postmortem"]}),
        "# Postmortem Log\n\n",
        f"## [{captured_at}] build | Codex postmortem wiki\n\n",
        f"- Conversation sources: {len(sessions)}\n",
        f"- Start-to-finish readers: {len(sessions)}\n",
        f"- Prompt-response exchanges: {len(exchanges)}\n",
        f"- External sources localised: {len(external_records)}\n",
        f"- Builder: `tools/build_codex_postmortem.py`\n",
    ]
    write_text(WIKI_DIR / "log.md", "".join(lines))


def write_readme() -> None:
    text = textwrap.dedent(
        f"""\
        # Codex Collaboration Postmortem

        This folder contains the generated source archive and wiki for reconstructing how the Challenge 2 solution was built with Codex.

        - `sources/conversations/` contains read-only Markdown transcripts extracted from local Codex rollout JSONL files for this repository.
        - `sources/external/` contains localised methodology references and verification metadata.
        - `wiki/` contains exchange-level prompt/response notes, start-to-finish conversation readers, source notes, topic/entity/map pages, data registers, and the detailed postmortem.
        - `publication-readiness-report.md` records redaction and packaging changes required before public release.

        Start at `wiki/index.md`.

        Regenerate with:

        ```bash
        python3 tools/build_codex_postmortem.py
        ```

        The standard build uses the curated session IDs in `tools/build_codex_postmortem.py`; add a session there before regenerating if a new conversation should become part of the postmortem corpus.

        The committed Challenge 2 baseline is tagged locally as `{BASELINE_TAG}`. Git does not preserve the read-only bit for source Markdown files, so the files also carry `read_only_intent: true` in frontmatter.
        """
    )
    write_text(POSTMORTEM_ROOT / "README.md", text)


def write_agents() -> None:
    text = textwrap.dedent(
        """\
        # Codex Postmortem Operating Rules

        This folder is a generated research wiki for the Challenge 2 Codex collaboration.

        ## Source Of Truth

        - Treat `sources/conversations/` and `sources/external/` as read-only evidence.
        - Do not edit generated source files by hand. Regenerate them with `python3 tools/build_codex_postmortem.py`.
        - Add new conversation session IDs to the curated list in `tools/build_codex_postmortem.py` before regenerating; do not publish incidental local sessions or evaluation-question runs by accident.
        - Keep conversation source notes tied to local Codex JSONL hashes.
        - Keep repository artifact links as commit-specific GitHub permalinks whenever the file was tracked at the baseline commit.

        ## Generated Wiki Contract

        - `wiki/index.md` is the entry point.
        - `wiki/exchanges/` contains one note per user prompt and Codex response sequence.
        - `wiki/readers/` contains one start-to-finish Markdown reader per conversation and is the standard route for following a conversation end to end.
        - `wiki/sources/` contains source notes for conversations, external references, and repository artifacts.
        - `wiki/topics/`, `wiki/entities/`, and `wiki/maps/` contain synthesis pages.
        - `wiki/data/` contains machine-readable registers.
        - `wiki/log.md` records generation events.

        ## Publication Caution

        Conversation transcripts may contain local paths, workflow details, or material that should be reviewed before public release.
        """
    )
    write_text(POSTMORTEM_ROOT / "AGENTS.md", text)


def validate_internal_links() -> list[str]:
    issues: list[str] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in WIKI_DIR.rglob("*.md"):
        text = strip_fenced_blocks(path.read_text(encoding="utf-8"))
        for raw in link_pattern.findall(text):
            if raw.startswith(("http://", "https://", "#", "mailto:", "/")):
                continue
            target = raw.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / urllib.parse.unquote(target)).resolve()
            if not resolved.exists():
                issues.append(f"{path.relative_to(REPO_ROOT)} -> {raw}")
    return issues


def public_exchange_path(exchange: Exchange) -> Path:
    session_date = compact_date(exchange.session.start_timestamp)
    title = public_sanitize_text(exchange.title)
    return PUBLIC_EXCHANGES_DIR / f"{exchange.global_sequence:04d}-{session_date}-{slugify(title)}.md"


def public_conversation_source_path(session: Session) -> Path:
    return PUBLIC_SOURCES_DIR / f"{session.source_id.lower()}-{slugify(session.title)}.md"


def public_external_source_path(record: dict[str, Any]) -> Path:
    return PUBLIC_SOURCES_DIR / f"{record['source_id'].lower()}.md"


def public_artifact_source_path(record: dict[str, Any]) -> Path:
    return PUBLIC_SOURCES_DIR / f"artifact-{slugify(record['path'])}.md"


def public_sanitize_text(text: str) -> str:
    """Remove local/private details while preserving useful public evidence."""
    text = text.replace("https://github.com/chris-page-gov/seelinks.git", "[PRIVATE_REFERENCE_REPO_URL]")
    text = text.replace("https://github.com/chris-page-gov/seelinks", "[PRIVATE_REFERENCE_REPO_URL]")
    replacements = [
        ("/Users/crpage/repos/ai-engineering-lab-hackathon-london-2026", "[LOCAL_REPO]"),
        ("/Users/crpage/repos/AI-Lab-Hackathons", "[LOCAL_REFERENCE_REPO]"),
        ("/Users/crpage/repos/seelinks", "[PRIVATE_REFERENCE_REPO]"),
        ("/Users/crpage/repos/mcp-geo", "[LOCAL_PRIOR_WORK_REPO]"),
        ("/Users/crpage/Downloads/Hackathon 20260416.docx", "[LOCAL_SOURCE_WRITEUP]"),
        ("/Users/crpage/Downloads", "[LOCAL_DOWNLOADS]"),
    ]
    for before, after in replacements:
        text = text.replace(before, after)
    text = text.replace("~/.codex/sessions", "[CODEX_SESSION_JSONL_DIR]")
    text = text.replace("~/.codex", "[LOCAL_ASSISTANT_HOME]")
    text = re.sub(r"/Users/crpage/\.codex/sessions/[^\s`)]+", "[CODEX_SESSION_JSONL]", text)
    text = re.sub(r"/Users/crpage/\.codex/[^\s`)]+", "[LOCAL_ASSISTANT_HOME]", text)
    text = re.sub(r"/Users/crpage/Desktop/[^\n`)]+", "[DESKTOP_SCREENSHOT]", text)
    text = re.sub(r"file:///Users/(?:[^\s`)]+)?", "[LOCAL_FILE_URL]", text)
    text = re.sub(r"/Users/(?:[^\s`)]+)?", "[LOCAL_USER_PATH]", text)
    text = re.sub(r"/var/folders/[^\n`)]+", "[TEMP_SCREENSHOT]", text)
    text = text.replace(".DS_Store", "[LOCAL_STATE_FILE]")
    text = text.replace("/Users/crpage", "[LOCAL_HOME]")
    text = re.sub(r"base64_chars=\d+; sha256=[a-f0-9]+", "base64 omitted", text)
    text = text.replace("only has `READ` permission", "did not have enough upstream permission")
    return text


def fenced_text(text: str) -> str:
    return "````text\n" + text.rstrip() + "\n````\n"


def external_license_status(record: dict[str, Any]) -> str:
    if record["kind"].startswith("x_post"):
        return "terms-only-platform-use"
    if record["kind"] == "gist_raw_markdown":
        return "no-explicit-license"
    return "permission-required"


def external_public_disposition(record: dict[str, Any]) -> str:
    if record["kind"].startswith("x_post"):
        return "Citation metadata only; do not publish the full localized readable snapshot."
    if record["kind"] == "gist_raw_markdown":
        return "Citation metadata only unless the author grants permission or adds an explicit license."
    return "Citation metadata only unless rights are cleared."


def publication_decisions() -> list[dict[str, str]]:
    return [
        {
            "id": "PUB-DEC-001",
            "decision": "Keep the private postmortem evidence archive out of Git.",
            "default": "Apply",
            "rationale": "The private archive contains raw transcripts, local paths, and full third-party source copies. The public folder preserves the useful evidence without those risks.",
            "elicitation_question": "Should the raw `postmortem/` evidence archive remain local-only and ignored by Git?",
            "status": "default_applied_pending_user_review",
        },
        {
            "id": "PUB-DEC-002",
            "decision": "Keep `.claude/settings.local.json` as a visible conventional path, but redact absolute local source locations.",
            "default": "Include path, redact local machine provenance",
            "rationale": "The path is a recognizable assistant configuration location. The sensitive part is the local filesystem topology, not the conventional file name.",
            "elicitation_question": "Should `.claude/settings.local.json` remain visible in the public exchange notes?",
            "status": "default_applied_pending_user_review",
        },
        {
            "id": "PUB-DEC-003",
            "decision": "Keep public GitHub fork permalinks and PR links where they support evidence.",
            "default": "Include public GitHub evidence links",
            "rationale": "The user preference is to include what can be included. Commit-specific GitHub links are the strongest public evidence.",
            "elicitation_question": "Should public GitHub account, commit, and PR links remain visible where they evidence the timeline?",
            "status": "default_applied_pending_user_review",
        },
        {
            "id": "PUB-DEC-004",
            "decision": "Do not publish full localized Karpathy X/gist source bodies.",
            "default": "Citation metadata and short excerpts only",
            "rationale": "No explicit redistribution license was found. Platform terms do not create a general off-platform redistribution license.",
            "elicitation_question": "Should full third-party source copies remain private unless permission or an explicit license is obtained?",
            "status": "default_applied_pending_user_review",
        },
        {
            "id": "PUB-DEC-005",
            "decision": "Redact private/local reference repositories while preserving the design influence.",
            "default": "Redact private repo URL and local prior-work paths",
            "rationale": "The public narrative only needs the reusable interaction pattern and audit-harness influence.",
            "elicitation_question": "Should private repo names/URLs and local prior-work paths be replaced with neutral labels?",
            "status": "default_applied_pending_user_review",
        },
        {
            "id": "PUB-DEC-006",
            "decision": "Reference the realtime delivery report as local-only until it is intentionally committed.",
            "default": "Do not claim a GitHub permalink until tracked",
            "rationale": "The report is useful evidence, but public traceability requires a committed file and commit-specific URL.",
            "elicitation_question": "Should the realtime delivery report be committed later so it can become public permalink evidence?",
            "status": "default_applied_pending_user_review",
        },
        {
            "id": "PUB-DEC-007",
            "decision": "Do not publish screenshot image payloads or local screenshot paths.",
            "default": "Omit image payloads, redact paths",
            "rationale": "The screenshots are not required to understand the engineering timeline and may expose desktop context.",
            "elicitation_question": "Should screenshots stay out of the public package unless individually reviewed?",
            "status": "default_applied_pending_user_review",
        },
        {
            "id": "PUB-DEC-008",
            "decision": "Do not redact Challenge 2 synthetic fixture values solely because they resemble personal data.",
            "default": "Include synthetic fixture references",
            "rationale": "Repository operating rules explicitly state that Challenge 2 fixture data is synthetic unless a brief says otherwise.",
            "elicitation_question": "Should synthetic Challenge 2 names/contact-like values remain publishable when context makes them synthetic?",
            "status": "default_applied_pending_user_review",
        },
        {
            "id": "PUB-DEC-009",
            "decision": "Preserve the prompt-response sequence in redacted exchange notes.",
            "default": "Include redacted prompt-response files",
            "rationale": "The sequence is the core evidence for the human/Codex contribution split.",
            "elicitation_question": "Should the public package keep one sanitized note per prompt-response exchange?",
            "status": "default_applied_pending_user_review",
        },
    ]


def write_public_exchange_files(exchanges: list[Exchange]) -> None:
    for exchange in exchanges:
        path = public_exchange_path(exchange)
        title = public_sanitize_text(exchange.title)
        previous_exchange, next_exchange = neighboring_exchanges(exchange, exchanges)
        fields = {
            "exchange_id": exchange.exchange_id,
            "title": title,
            "source_id": exchange.session.source_id,
            "global_sequence": exchange.global_sequence,
            "session_sequence": exchange.session_sequence,
            "user_timestamp": exchange.user_message.timestamp,
            "publication_status": "redacted-public-derivative",
            "tags": ["exchange", "codex-postmortem-public"],
        }
        parts = [
            frontmatter(fields),
            f"# {exchange.global_sequence:04d}. {title}\n\n",
            exchange_navigation(
                path,
                public_conversation_reader_path(exchange.session),
                previous_exchange,
                next_exchange,
                public=True,
            ),
            "## Publication Boundary\n\n",
            "This is a redacted public derivative. It preserves sequence and contribution evidence, but it is not the raw Codex transcript.\n\n",
            "## Source\n\n",
            f"- Conversation: {exchange.session.source_id} ({exchange.session.title})\n",
            "- Raw transcript: retained only in the private local evidence archive.\n\n",
            "## User Prompt\n\n",
            fenced_text(public_sanitize_text(exchange.user_message.text)),
            "\n## Codex Response\n\n",
        ]
        if exchange.assistant_messages:
            for number, message in enumerate(exchange.assistant_messages, start=1):
                phase = f" ({message.phase})" if message.phase else ""
                parts.append(f"### Response {number}{phase}\n\n")
                parts.append(f"- Timestamp: `{message.timestamp}`\n\n")
                parts.append(fenced_text(public_sanitize_text(message.text)))
                parts.append("\n")
        else:
            parts.append("No Codex response was recorded before the next user message.\n\n")
        parts.extend(
            [
                "## Contribution Reading\n\n",
                f"- User contribution: {infer_user_contribution(exchange)}\n",
                f"- Codex contribution: {infer_codex_contribution(exchange)}\n",
                "\n",
                exchange_navigation(
                    path,
                    public_conversation_reader_path(exchange.session),
                    previous_exchange,
                    next_exchange,
                    public=True,
                ),
            ]
        )
        write_text(path, "".join(parts))


def write_public_conversation_readers(sessions: list[Session], exchanges: list[Exchange]) -> None:
    grouped = grouped_exchanges_by_session(sessions, exchanges)
    for session in sessions:
        path = public_conversation_reader_path(session)
        session_exchanges = grouped.get(session.session_id, [])
        source_note = public_conversation_source_path(session)
        fields = {
            "source_id": session.source_id,
            "title": f"{public_sanitize_text(session.title)} Reader",
            "reader_type": "redacted_start_to_finish_conversation",
            "publication_status": "redacted-public-derivative",
            "exchange_count": len(session_exchanges),
            "tags": ["reader", "conversation", "codex-postmortem-public"],
        }
        parts = [
            frontmatter(fields),
            f"# {session.source_id}: {public_sanitize_text(session.title)}\n\n",
            "This redacted public reader inlines the prompt-response exchanges for one conversation in chronological order. It is the standard GitHub-friendly route for reading the conversation from start to finish without opening each exchange note separately.\n\n",
            "## Navigation\n\n",
            f"- Index: {rel_link(path, PUBLIC_WIKI_DIR / 'index.md', 'Public Codex Postmortem')}\n",
            f"- Conversation source note: {rel_link(path, source_note, session.source_id)}\n",
            "- Raw transcript: retained only in the private local evidence archive.\n\n",
            "## Exchange Map\n\n",
            "| Exchange | Prompt | Standalone Note |\n",
            "|---|---|---|\n",
        ]
        for exchange in session_exchanges:
            title = public_sanitize_text(exchange.title)
            parts.append(
                f"| [{exchange.exchange_id}](#{exchange_anchor(exchange)}) | {title} | {rel_link(path, public_exchange_path(exchange), 'note')} |\n"
            )
        parts.append("\n## Conversation\n\n")
        for exchange in session_exchanges:
            title = public_sanitize_text(exchange.title)
            parts.extend(
                [
                    f'<a id="{exchange_anchor(exchange)}"></a>\n\n',
                    f"### {exchange.exchange_id}: {title}\n\n",
                    f"- User timestamp: `{exchange.user_message.timestamp}`\n",
                    f"- Standalone note: {rel_link(path, public_exchange_path(exchange), exchange.exchange_id)}\n\n",
                    "#### User Prompt\n\n",
                    fenced_text(public_sanitize_text(exchange.user_message.text)),
                    "\n#### Codex Response\n\n",
                ]
            )
            if exchange.assistant_messages:
                for number, message in enumerate(exchange.assistant_messages, start=1):
                    phase = f" ({message.phase})" if message.phase else ""
                    parts.append(f"##### Response {number}{phase}\n\n")
                    parts.append(f"- Timestamp: `{message.timestamp}`\n\n")
                    parts.append(fenced_text(public_sanitize_text(message.text)))
                    parts.append("\n")
            else:
                parts.append("No Codex response was recorded before the next user message.\n\n")
            parts.append(f"[Back to exchange map](#exchange-map)\n\n")
        write_text(path, "".join(parts))


def write_public_sources(
    sessions: list[Session],
    exchanges: list[Exchange],
    external_records: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
) -> None:
    for session in sessions:
        path = public_conversation_source_path(session)
        session_exchanges = [exchange for exchange in exchanges if exchange.session.session_id == session.session_id]
        parts = [
            frontmatter(
                {
                    "source_id": session.source_id,
                    "title": session.title,
                    "source_type": "redacted_conversation_summary",
                    "publication_status": "raw-transcript-private",
                    "tags": ["source", "conversation", "codex-postmortem-public"],
                }
            ),
            f"# {session.title}\n\n",
            "This source note summarizes a local Codex conversation without publishing the raw transcript or local JSONL path.\n\n",
            f"- Conversation source ID: `{session.source_id}`\n",
            f"- Start timestamp: `{session.start_timestamp}`\n",
            f"- Updated at: `{session.updated_at}`\n",
            f"- Start-to-finish reader: {rel_link(path, public_conversation_reader_path(session), 'conversation reader')}\n",
            f"- User visible messages: {sum(1 for item in session.messages if item.role == 'user')}\n",
            f"- Codex visible messages: {sum(1 for item in session.messages if item.role == 'assistant')}\n",
            f"- Private evidence hash: `{session.source_sha256}`\n",
            "- Raw transcript: private/local evidence archive only.\n\n",
            "## Public Exchange Notes\n\n",
        ]
        for exchange in session_exchanges:
            parts.append(f"- {rel_link(path, public_exchange_path(exchange), f'{exchange.exchange_id}: {public_sanitize_text(exchange.title)}')}\n")
        write_text(path, "".join(parts))

    for record in external_records:
        path = public_external_source_path(record)
        parts = [
            frontmatter(
                {
                    "source_id": record["source_id"],
                    "title": record["title"],
                    "source_type": "external_citation",
                    "canonical_url": record["canonical_url"],
                    "license_status": external_license_status(record),
                    "publication_status": "citation-only",
                    "tags": ["source", "external", "methodology", "codex-postmortem-public"],
                }
            ),
            f"# {record['title']}\n\n",
            "This public source note intentionally does not include the localized full-text copy.\n\n",
            f"- Canonical URL: [{record['canonical_url']}]({record['canonical_url']})\n",
            f"- Source kind: `{record['kind']}`\n",
            f"- Captured at: `{record['captured_at']}`\n",
            f"- Fetch status: `{record['fetch_status']}`; direct status: `{record['direct_status']}`\n",
            f"- Private archive SHA-256: `{record['sha256']}`\n",
            f"- License status: `{external_license_status(record)}`\n",
            f"- Publication disposition: {external_public_disposition(record)}\n",
        ]
        if record.get("fetch_etag"):
            parts.append(f"- ETag: `{record['fetch_etag']}`\n")
        write_text(path, "".join(parts))

    for record in artifacts:
        path = public_artifact_source_path(record)
        parts = [
            frontmatter(
                {
                    "title": record["path"],
                    "source_type": "repository_artifact",
                    "tracked_at_baseline": bool(record["tracked_at_baseline"]),
                    "publication_status": "baseline-permalink" if record.get("github_permalink") else ("publication-branch-link" if record.get("publication_branch_url") else "local-only-reference"),
                    "tags": ["source", "repository-artifact", "codex-postmortem-public"],
                }
            ),
            f"# {record['path']}\n\n",
            f"- Tracked at baseline: `{record['tracked_at_baseline']}`\n",
            f"- Tracked on publication branch `{record.get('publication_branch')}`: `{record.get('tracked_in_publication_branch')}`\n",
            f"- Baseline commit: `{record['baseline_commit']}`\n",
        ]
        if record.get("github_permalink"):
            parts.append(f"- GitHub permalink: [{record['path']}]({record['github_permalink']})\n")
        else:
            parts.append("- GitHub permalink: not available at the tagged baseline.\n")
        if record.get("publication_branch_url"):
            parts.append(f"- Publication branch link: [{record['path']}]({record['publication_branch_url']})\n")
        if record.get("note"):
            parts.append(f"- Note: {record['note']}\n")
        write_text(path, "".join(parts))


def write_public_data_registers(
    sessions: list[Session],
    exchanges: list[Exchange],
    external_records: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
) -> None:
    session_records = [
        {
            "source_id": session.source_id,
            "title": session.title,
            "start_timestamp": session.start_timestamp,
            "updated_at": session.updated_at,
            "private_evidence_sha256": session.source_sha256,
            "user_message_count": sum(1 for message in session.messages if message.role == "user"),
            "assistant_message_count": sum(1 for message in session.messages if message.role == "assistant"),
            "public_source_path": str(public_conversation_source_path(session).relative_to(REPO_ROOT)),
            "public_reader_path": str(public_conversation_reader_path(session).relative_to(REPO_ROOT)),
        }
        for session in sessions
    ]
    exchange_records = [
        {
            "exchange_id": exchange.exchange_id,
            "global_sequence": exchange.global_sequence,
            "session_source_id": exchange.session.source_id,
            "title": public_sanitize_text(exchange.title),
            "user_timestamp": exchange.user_message.timestamp,
            "assistant_message_count": len(exchange.assistant_messages),
            "public_path": str(public_exchange_path(exchange).relative_to(REPO_ROOT)),
            "user_contribution": infer_user_contribution(exchange),
            "codex_contribution": infer_codex_contribution(exchange),
        }
        for exchange in exchanges
    ]
    external_citations = [
        {
            "source_id": record["source_id"],
            "title": record["title"],
            "canonical_url": record["canonical_url"],
            "kind": record["kind"],
            "captured_at": record["captured_at"],
            "fetch_status": record["fetch_status"],
            "direct_status": record["direct_status"],
            "private_archive_sha256": record["sha256"],
            "license_status": external_license_status(record),
            "publication_disposition": external_public_disposition(record),
            "public_source_path": str(public_external_source_path(record).relative_to(REPO_ROOT)),
        }
        for record in external_records
    ]
    artifact_records = [
        {
            "path": record["path"],
            "tracked_at_baseline": record["tracked_at_baseline"],
            "tracked_in_publication_branch": record.get("tracked_in_publication_branch"),
            "baseline_commit": record["baseline_commit"],
            "github_permalink": record.get("github_permalink"),
            "publication_branch": record.get("publication_branch"),
            "publication_branch_url": record.get("publication_branch_url"),
            "publication_status": "baseline-permalink" if record.get("github_permalink") else ("publication-branch-link" if record.get("publication_branch_url") else "local-only-reference"),
        }
        for record in artifacts
    ]
    write_text(PUBLIC_DATA_DIR / "session-register-public.json", json.dumps(session_records, indent=2, ensure_ascii=False))
    write_text(PUBLIC_DATA_DIR / "exchange-register-public.json", json.dumps(exchange_records, indent=2, ensure_ascii=False))
    write_text(PUBLIC_DATA_DIR / "external-source-citations.json", json.dumps(external_citations, indent=2, ensure_ascii=False))
    write_text(PUBLIC_DATA_DIR / "artifact-register-public.json", json.dumps(artifact_records, indent=2, ensure_ascii=False))
    write_text(PUBLIC_DATA_DIR / "publication-decision-register.json", json.dumps(publication_decisions(), indent=2, ensure_ascii=False))


def write_public_decisions() -> None:
    decisions = publication_decisions()
    parts = [
        frontmatter({"title": "Publication Decision Register", "tags": ["decisions", "codex-postmortem-public"]}),
        "# Publication Decision Register\n\n",
        "These decisions use inclusion-forward defaults. Each row includes the question to revisit if a stricter publication posture is needed.\n\n",
        "| ID | Default Applied | Decision | Elicitation Question | Status |\n",
        "|---|---|---|---|---|\n",
    ]
    for decision in decisions:
        parts.append(
            f"| {decision['id']} | {decision['default']} | {decision['decision']} | {decision['elicitation_question']} | {decision['status']} |\n"
        )
    write_text(PUBLIC_WIKI_DIR / "decisions.md", "".join(parts))


def write_public_methodology(external_records: list[dict[str, Any]]) -> None:
    parts = [
        frontmatter({"title": "Methodology Sources", "tags": ["methodology", "codex-postmortem-public"]}),
        "# Methodology Sources\n\n",
        "The public package cites the methodology sources without redistributing full copied third-party source bodies.\n\n",
        "| Source | Canonical URL | License Status | Public Treatment |\n",
        "|---|---|---|---|\n",
    ]
    for record in external_records:
        source_note = public_external_source_path(record)
        parts.append(
            f"| {rel_link(PUBLIC_WIKI_DIR / 'methodology.md', source_note, record['title'])} | [open]({record['canonical_url']}) | `{external_license_status(record)}` | {external_public_disposition(record)} |\n"
        )
    parts.append(
        "\nThe implementation translated the cited LLM Wiki pattern into a reproducible Challenge 2 wiki builder: raw sources stay immutable, generated notes carry provenance, indexes and logs make navigation explicit, and linting catches broken links or missing coverage.\n"
    )
    write_text(PUBLIC_WIKI_DIR / "methodology.md", "".join(parts))


def write_public_conversation_summary(sessions: list[Session], exchanges: list[Exchange]) -> None:
    parts = [
        frontmatter({"title": "Conversation Summary", "tags": ["conversation", "codex-postmortem-public"]}),
        "# Conversation Summary\n\n",
        "Raw transcripts are retained in the private local evidence archive. Public evidence is published as redacted exchange notes.\n\n",
        "| Source | Conversation | Start | Exchanges | Reader | Public Source Note |\n",
        "|---|---|---|---:|---|---|\n",
    ]
    for session in sessions:
        count = sum(1 for exchange in exchanges if exchange.session.session_id == session.session_id)
        source_note = public_conversation_source_path(session)
        parts.append(
            f"| {session.source_id} | {session.title} | `{session.start_timestamp}` | {count} | {rel_link(PUBLIC_WIKI_DIR / 'conversation-summary.md', public_conversation_reader_path(session), 'read')} | {rel_link(PUBLIC_WIKI_DIR / 'conversation-summary.md', source_note, 'open')} |\n"
        )
    write_text(PUBLIC_WIKI_DIR / "conversation-summary.md", "".join(parts))


def write_public_evidence_page(artifacts: list[dict[str, Any]]) -> None:
    tracked = [record for record in artifacts if record.get("github_permalink")]
    branch_tracked = [record for record in artifacts if not record.get("github_permalink") and record.get("publication_branch_url")]
    local_only = [record for record in artifacts if not record.get("github_permalink") and not record.get("publication_branch_url")]
    parts = [
        frontmatter({"title": "Repository Evidence", "tags": ["evidence", "codex-postmortem-public"]}),
        "# Repository Evidence\n\n",
        f"Commit-specific GitHub permalinks are used where files were tracked at the tagged Challenge 2 baseline. Version {PUBLICATION_VERSION} publication artifacts that did not exist at that baseline use publication-branch links until the PR is merged and they can be replaced with permanent commit links.\n\n",
        "## Baseline Permalinks\n\n",
        "| Artifact | Permalink |\n",
        "|---|---|\n",
    ]
    for record in tracked:
        source_note = public_artifact_source_path(record)
        parts.append(f"| {rel_link(PUBLIC_WIKI_DIR / 'repository-evidence.md', source_note, record['path'])} | [open]({record['github_permalink']}) |\n")
    parts.append(f"\n## Version {PUBLICATION_VERSION} Publication Branch Evidence\n\n")
    for record in branch_tracked:
        source_note = public_artifact_source_path(record)
        parts.append(f"- {rel_link(PUBLIC_WIKI_DIR / 'repository-evidence.md', source_note, record['path'])}: [publication branch]({record['publication_branch_url']})\n")
    if local_only:
        parts.append("\n## Local-Only Evidence\n\n")
        for record in local_only:
            parts.append(f"- `{record['path']}`: {record.get('note') or 'not tracked at the tagged baseline'}\n")
    write_text(PUBLIC_WIKI_DIR / "repository-evidence.md", "".join(parts))


def write_public_postmortem(sessions: list[Session], artifacts: list[dict[str, Any]]) -> None:
    baseline = artifacts[0]["baseline_commit"] if artifacts else "unknown"
    parts = [
        frontmatter({"title": "Public Codex Collaboration Postmortem", "tags": ["postmortem", "codex-postmortem-public"]}),
        "# Public Codex Collaboration Postmortem\n\n",
        "## Executive Summary\n\n",
        f"This public postmortem explains how {TEAM_NAME} built the Challenge 2 prototype with Codex while keeping the raw local evidence archive out of Git. The human team supplied the goal, constraints, review direction, and quality bar. Codex inferred much of the implementation detail by inspecting the repository, then produced code, documentation, tests, validation evidence, and synthesis.\n\n",
        f"The Challenge 2 committed baseline is `{baseline}`. Public repository evidence uses commit-specific GitHub permalinks where possible.\n\n",
        "## Publication Boundary\n\n",
        "- Raw Codex transcripts stay in the ignored private `postmortem/` folder.\n",
        "- This `postmortem-public/` folder preserves sequence and contribution evidence in redacted form.\n",
        "- Third-party methodology sources are cited by URL and private archive hash; full copied bodies are not redistributed here.\n",
        "- Local machine paths, local Codex session paths, private reference repositories, and screenshot paths are replaced with placeholders.\n\n",
        "## What The User Contributed\n\n",
        "- Selected Challenge 2 and framed the outcome as making government dark data findable and structured.\n",
        "- Named the Karpathy LLM Wiki pattern as the methodology to adapt.\n",
        "- Set repository constraints: raw challenge data should remain immutable, documentation should move in lockstep, and validation should be run before completion claims.\n",
        "- Identified product gaps, including the need for a question field that travels with Browser AI exports and saved checks.\n",
        "- Requested a postmortem so the AI-assistant learning objective was explicit rather than hidden in commit history.\n\n",
        f"Team attribution: the Challenge 2 implementation work was done by {TEAM_NAME}.\n\n",
        "## What Codex Contributed\n\n",
        "- Inspected the repository structure, challenge corpus, docs, Git state, validation tools, and external methodology sources.\n",
        "- Converted the LLM Wiki idea into a Challenge 2 Obsidian-style generated wiki with source notes, topic/entity/map pages, registers, and linting.\n",
        "- Built evaluation harnesses and workbench surfaces around the generated wiki.\n",
        "- Managed PR hygiene, documentation lockstep, and validation runs.\n",
        "- Generated the private postmortem archive and this public derivative from conversation evidence.\n\n",
        "## Timeline\n\n",
    ]
    for session in sessions:
        parts.append(f"- `{session.start_timestamp}`: {rel_link(PUBLIC_WIKI_DIR / 'postmortem.md', public_conversation_reader_path(session), session.title)}\n")
    parts.extend(
        [
            "\n## Lessons\n\n",
            "1. Outcome-focused prompts worked because repository rules bounded Codex's freedom.\n",
            "2. The useful collaboration pattern was prompt, inspect, infer, implement, validate, document, and preserve evidence.\n",
            "3. Commit-specific links, generated registers, and lint reports are more reliable public evidence than memory or narrative alone.\n",
            "4. A public postmortem needs a separate publication layer; raw assistant transcripts are valuable evidence but poor public artifacts.\n\n",
            "## Start Points\n\n",
            f"- {rel_link(PUBLIC_WIKI_DIR / 'postmortem.md', PUBLIC_WIKI_DIR / 'conversation-summary.md', 'Conversation Summary')}\n",
            f"- {rel_link(PUBLIC_WIKI_DIR / 'postmortem.md', PUBLIC_WIKI_DIR / 'index.md', 'Start-to-Finish Conversation Readers')}\n",
            f"- {rel_link(PUBLIC_WIKI_DIR / 'postmortem.md', PUBLIC_WIKI_DIR / 'decisions.md', 'Publication Decision Register')}\n",
            f"- {rel_link(PUBLIC_WIKI_DIR / 'postmortem.md', PUBLIC_WIKI_DIR / 'methodology.md', 'Methodology Sources')}\n",
            f"- {rel_link(PUBLIC_WIKI_DIR / 'postmortem.md', PUBLIC_WIKI_DIR / 'repository-evidence.md', 'Repository Evidence')}\n",
        ]
    )
    write_text(PUBLIC_WIKI_DIR / "postmortem.md", "".join(parts))


def write_public_architecture() -> None:
    text = textwrap.dedent(
        """\
        # Public Postmortem Architecture

        ```mermaid
        flowchart LR
          Private["Ignored private postmortem archive"] --> Builder["tools/build_codex_postmortem.py"]
          Builder --> Public["postmortem-public"]
          Public --> Exchanges["Redacted exchange notes"]
          Public --> Readers["Markdown conversation readers"]
          Public --> Citations["Citation-only external sources"]
          Public --> Evidence["GitHub permalinks and registers"]
        ```

        The public folder is intentionally a derivative. It keeps the useful timeline, contribution analysis, start-to-finish Markdown readers, and repository evidence while excluding raw local transcripts and full third-party copied source bodies.
        """
    )
    write_text(PUBLIC_WIKI_DIR / "architecture.md", frontmatter({"title": "Architecture", "tags": ["architecture", "codex-postmortem-public"]}) + text)


def write_public_index(
    sessions: list[Session],
    exchanges: list[Exchange],
    external_records: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
) -> None:
    parts = [
        frontmatter({"title": "Public Codex Postmortem", "tags": ["index", "codex-postmortem-public"]}),
        "# Public Codex Postmortem\n\n",
        f"This folder is the GitHub-safe derivative of the private Codex postmortem evidence archive for {TEAM_NAME}'s Challenge 2 work.\n\n",
        "## Start Here\n\n",
        f"- {rel_link(PUBLIC_WIKI_DIR / 'index.md', PUBLIC_WIKI_DIR / 'postmortem.md', 'Public Postmortem')}\n",
        f"- {rel_link(PUBLIC_WIKI_DIR / 'index.md', PUBLIC_WIKI_DIR / 'conversation-summary.md', 'Conversation Summary')}\n",
        "- [Start-to-Finish Conversation Readers](#start-to-finish-conversation-readers)\n",
        f"- {rel_link(PUBLIC_WIKI_DIR / 'index.md', PUBLIC_WIKI_DIR / 'decisions.md', 'Publication Decision Register')}\n",
        f"- {rel_link(PUBLIC_WIKI_DIR / 'index.md', PUBLIC_WIKI_DIR / 'methodology.md', 'Methodology Sources')}\n",
        f"- {rel_link(PUBLIC_WIKI_DIR / 'index.md', PUBLIC_WIKI_DIR / 'repository-evidence.md', 'Repository Evidence')}\n",
        f"- {rel_link(PUBLIC_WIKI_DIR / 'index.md', PUBLIC_WIKI_DIR / 'architecture.md', 'Public Postmortem Architecture')}\n\n",
        "## Start-to-Finish Conversation Readers\n\n",
        "| Source | Conversation | Exchanges | Reader | Source Note |\n",
        "|---|---|---:|---|---|\n",
    ]
    for session in sessions:
        count = sum(1 for exchange in exchanges if exchange.session.session_id == session.session_id)
        source_note = public_conversation_source_path(session)
        parts.append(
            f"| {session.source_id} | {public_sanitize_text(session.title)} | {count} | {rel_link(PUBLIC_WIKI_DIR / 'index.md', public_conversation_reader_path(session), 'read')} | {rel_link(PUBLIC_WIKI_DIR / 'index.md', source_note, 'source')} |\n"
        )
    parts.extend(
        [
            "\n",
            "## Redacted Prompt-Response Exchanges\n\n",
            "| Sequence | Exchange | Source |\n",
            "|---:|---|---|\n",
        ]
    )
    for exchange in exchanges:
        parts.append(f"| {exchange.global_sequence} | {rel_link(PUBLIC_WIKI_DIR / 'index.md', public_exchange_path(exchange), public_sanitize_text(exchange.title))} | {exchange.session.source_id} |\n")
    parts.extend(
        [
            "\n## Publication Counts\n\n",
            f"- Conversation summaries: {len(sessions)}\n",
            f"- Redacted prompt-response exchanges: {len(exchanges)}\n",
            f"- External citations: {len(external_records)}\n",
            f"- Repository artifacts registered: {len(artifacts)}\n",
            "\n## Scope Notes\n\n",
            "- Public conversations are restricted to the curated session IDs named in `tools/build_codex_postmortem.py`; evaluation runs and incidental local sessions are excluded unless deliberately promoted into that curated list.\n",
        ]
    )
    write_text(PUBLIC_WIKI_DIR / "index.md", "".join(parts))


def write_public_readme() -> None:
    text = textwrap.dedent(
        """\
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
        """
    )
    write_text(POSTMORTEM_PUBLIC_ROOT / "README.md", text)


def write_public_agents() -> None:
    text = textwrap.dedent(
        """\
        # Public Postmortem Operating Rules

        This folder is intended to be committed to GitHub.

        - Do not add raw Codex JSONL files or raw transcript sources here.
        - Do not add full copied third-party methodology source bodies unless licensing or permission is recorded.
        - Keep local filesystem paths, screenshot paths, and private reference repositories redacted.
        - Preserve commit-specific GitHub permalinks for tracked repository artifacts.
        - Add new conversation session IDs to the curated list in `tools/build_codex_postmortem.py` before regenerating public output.
        - Regenerate with `python3 tools/build_codex_postmortem.py` rather than hand-editing generated exchange notes.
        - Treat `wiki/readers/` as the standard GitHub-friendly route for following conversations from start to finish.
        """
    )
    write_text(POSTMORTEM_PUBLIC_ROOT / "AGENTS.md", text)


def write_public_log(captured_at: str, sessions: list[Session], exchanges: list[Exchange], external_records: list[dict[str, Any]]) -> None:
    lines = [
        frontmatter({"title": "Public Postmortem Log", "tags": ["log", "codex-postmortem-public"]}),
        "# Public Postmortem Log\n\n",
        f"## [{captured_at}] build | Public Codex postmortem\n\n",
        f"- Conversation summaries: {len(sessions)}\n",
        f"- Start-to-finish readers: {len(sessions)}\n",
        f"- Redacted prompt-response exchanges: {len(exchanges)}\n",
        f"- Citation-only external sources: {len(external_records)}\n",
        "- Private source archive: ignored `postmortem/` folder.\n",
    ]
    write_text(PUBLIC_WIKI_DIR / "log.md", "".join(lines))


def validate_public_internal_links() -> list[str]:
    issues: list[str] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in PUBLIC_WIKI_DIR.rglob("*.md"):
        text = strip_fenced_blocks(path.read_text(encoding="utf-8"))
        for raw in link_pattern.findall(text):
            if raw.startswith(("http://", "https://", "#", "mailto:", "/")):
                continue
            target = raw.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / urllib.parse.unquote(target)).resolve()
            if not resolved.exists():
                issues.append(f"{path.relative_to(REPO_ROOT)} -> {raw}")
    return issues


def public_forbidden_hits() -> list[dict[str, str]]:
    checks = [
        ("absolute-user-path", re.compile(r"/Users/")),
        ("codex-session-path", re.compile(r"\.codex/sessions|CODEX_HOME")),
        ("desktop-screenshot-path", re.compile(r"Desktop/Screenshot")),
        ("temporary-screenshot-path", re.compile(r"TemporaryItems")),
        ("downloads-path", re.compile(r"/Downloads/")),
        ("private-seelinks-url", re.compile(r"github\.com/chris-page-gov/seelinks")),
        ("image-base64-metadata", re.compile(r"base64_chars=")),
        ("x-post-full-body-marker", re.compile(r"Something I'm finding very useful recently: using LLMs")),
        ("gist-full-body-marker", re.compile(r"Most people's experience with LLMs and documents looks like RAG")),
    ]
    hits: list[dict[str, str]] = []
    for path in POSTMORTEM_PUBLIC_ROOT.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in checks:
            match = pattern.search(text)
            if match:
                hits.append({"check": name, "path": str(path.relative_to(REPO_ROOT)), "match": match.group(0)})
    return hits


def write_public_lint_report(captured_at: str) -> list[str]:
    broken_links = validate_public_internal_links()
    forbidden_hits = public_forbidden_hits()
    lint = {
        "captured_at": captured_at,
        "broken_internal_links": broken_links,
        "forbidden_publication_hits": forbidden_hits,
    }
    write_text(PUBLIC_DATA_DIR / "publication-lint-report.json", json.dumps(lint, indent=2, ensure_ascii=False))
    lines = [
        frontmatter({"title": "Publication Lint Report", "tags": ["lint", "codex-postmortem-public"]}),
        "# Publication Lint Report\n\n",
        f"- Broken internal links: {len(broken_links)}\n",
        f"- Forbidden publication hits: {len(forbidden_hits)}\n",
    ]
    if forbidden_hits:
        lines.append("\n## Forbidden Hits\n\n")
        for hit in forbidden_hits:
            lines.append(f"- `{hit['check']}` in `{hit['path']}` matched `{hit['match']}`\n")
    if broken_links:
        lines.append("\n## Broken Links\n\n")
        for issue in broken_links:
            lines.append(f"- {issue}\n")
    write_text(PUBLIC_WIKI_DIR / "publication-lint-report.md", "".join(lines))
    return broken_links + [f"{hit['check']}: {hit['path']}" for hit in forbidden_hits]


def build_public_postmortem(
    captured_at: str,
    sessions: list[Session],
    exchanges: list[Exchange],
    external_records: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
) -> None:
    reset_public_dirs()
    write_public_exchange_files(exchanges)
    write_public_conversation_readers(sessions, exchanges)
    write_public_sources(sessions, exchanges, external_records, artifacts)
    write_public_data_registers(sessions, exchanges, external_records, artifacts)
    write_public_decisions()
    write_public_conversation_summary(sessions, exchanges)
    write_public_methodology(external_records)
    write_public_evidence_page(artifacts)
    write_public_postmortem(sessions, artifacts)
    write_public_architecture()
    write_public_index(sessions, exchanges, external_records, artifacts)
    write_public_log(captured_at, sessions, exchanges, external_records)
    write_public_readme()
    write_public_agents()
    public_issues = write_public_lint_report(captured_at)
    if public_issues:
        raise RuntimeError("Public postmortem publication lint failed:\n" + "\n".join(public_issues))


ALL_EXCHANGES: list[Exchange] = []


def build() -> None:
    global ALL_EXCHANGES
    captured_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    reset_generated_dirs()
    sessions = discover_sessions()
    if not sessions:
        raise RuntimeError(f"No Codex sessions found for cwd {TARGET_CWD}")
    write_conversation_sources(sessions)
    ALL_EXCHANGES = build_exchanges(sessions)
    write_exchange_files(ALL_EXCHANGES)
    write_conversation_readers(sessions, ALL_EXCHANGES)
    external_records = write_external_sources(captured_at)
    try:
        baseline_commit = run_git(["rev-parse", f"{BASELINE_TAG}^{{}}"])
    except subprocess.CalledProcessError:
        baseline_commit = run_git(["rev-parse", "HEAD"])
    artifacts = build_artifact_register(baseline_commit)
    write_source_notes(sessions, external_records, artifacts)
    write_data_registers(sessions, ALL_EXCHANGES, external_records, artifacts)
    write_topic_pages(ALL_EXCHANGES, artifacts)
    write_entities()
    write_maps(sessions, ALL_EXCHANGES)
    write_architecture()
    write_methodology_page(external_records)
    write_postmortem(sessions, ALL_EXCHANGES, artifacts)
    write_index(sessions, ALL_EXCHANGES, external_records, artifacts)
    write_log(captured_at, sessions, ALL_EXCHANGES, external_records)
    write_readme()
    write_agents()
    build_public_postmortem(captured_at, sessions, ALL_EXCHANGES, external_records, artifacts)
    issues = validate_internal_links()
    lint = {
        "captured_at": captured_at,
        "conversation_sources": len(sessions),
        "exchanges": len(ALL_EXCHANGES),
        "external_sources": len(external_records),
        "artifact_sources": len(artifacts),
        "broken_internal_links": issues,
    }
    write_text(DATA_DIR / "lint-report.json", json.dumps(lint, indent=2, ensure_ascii=False))
    write_text(
        WIKI_DIR / "lint-report.md",
        frontmatter({"title": "Postmortem Lint Report", "tags": ["lint", "codex-postmortem"]})
        + "# Postmortem Lint Report\n\n"
        + f"- Conversation sources: {len(sessions)}\n"
        + f"- Prompt-response exchanges: {len(ALL_EXCHANGES)}\n"
        + f"- External sources: {len(external_records)}\n"
        + f"- Repository artifact sources: {len(artifacts)}\n"
        + f"- Broken internal links: {len(issues)}\n",
    )
    remove_state_files()
    if issues:
        raise RuntimeError("Broken internal links:\n" + "\n".join(issues))
    print(
        f"Built Codex postmortem wiki: {len(sessions)} conversations, "
        f"{len(ALL_EXCHANGES)} exchanges, {len(external_records)} external sources."
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build the Codex collaboration postmortem wiki.")
    parser.parse_args(argv)
    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
