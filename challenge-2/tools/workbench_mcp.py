#!/usr/bin/env python3
"""Minimal stdio MCP server for the Challenge 2 Dark Data Workbench."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHALLENGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = CHALLENGE_ROOT.parent
REGISTER_PATH = CHALLENGE_ROOT / "wiki" / "data" / "source-register.json"
SYNTHETIC_NOTICE = (
    "Challenge 2 corpus data is synthetic hackathon fixture data. Synthetic names and "
    "contact-like values are retained for demo fidelity and should not be redacted."
)


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    title: str
    source_path: str
    note_path: str
    status: str
    source_format: str
    department: str
    topics: list[str]
    flags: list[str]
    note_text: str

    @property
    def search_text(self) -> str:
        return " ".join(
            [
                self.source_id,
                self.title,
                self.status,
                self.source_format,
                self.department,
                *self.topics,
                *self.flags,
                self.note_text,
            ]
        ).casefold()

    def to_summary(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "title": self.title,
            "status": self.status,
            "format": self.source_format,
            "department": self.department,
            "topics": self.topics,
            "flags": self.flags,
            "note_path": self.note_path,
            "source_path": self.source_path,
            "summary": extract_summary(self.note_text, self.title),
        }


def load_sources(challenge_root: Path = CHALLENGE_ROOT) -> list[SourceRecord]:
    raw = json.loads((challenge_root / "wiki" / "data" / "source-register.json").read_text(encoding="utf-8"))
    sources: list[SourceRecord] = []
    for entry in raw:
        note_path = str(entry["note_path"])
        try:
            note_text = (challenge_root / note_path).read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            note_text = ""
        topics = sorted(set([*(entry.get("topics") or []), *(entry.get("matched_topics") or [])]))
        sources.append(
            SourceRecord(
                source_id=str(entry["source_id"]),
                title=str(entry["title"]),
                source_path=str(entry["source_path"]),
                note_path=note_path,
                status=str(entry.get("status") or "unknown"),
                source_format=str(entry.get("source_format") or "unknown"),
                department=str(entry.get("department") or "Unknown"),
                topics=topics,
                flags=sorted(set(entry.get("flags") or [])),
                note_text=note_text,
            )
        )
    return sources


def extract_summary(note_text: str, fallback: str) -> str:
    body = note_text
    if body.startswith("---"):
        parts = body.split("---", 2)
        if len(parts) == 3:
            body = parts[2]
    marker = "## Summary"
    if marker in body:
        body = body.split(marker, 1)[1].split("\n## ", 1)[0]
    lines = [
        line.strip().lstrip("-* ").strip()
        for line in body.splitlines()
        if line.strip() and not line.strip().startswith("|")
    ]
    summary = " ".join(lines).strip()
    return (summary or fallback)[:700]


def extract_excerpts(source: SourceRecord, query: str = "", limit: int = 3) -> list[str]:
    paragraphs = [
        paragraph.replace("\n", " ").strip()
        for paragraph in source.note_text.split("\n\n")
        if len(paragraph.strip()) > 80 and not paragraph.strip().startswith("|")
    ]
    needle = query.casefold().strip()
    if needle:
        matches = [paragraph for paragraph in paragraphs if needle in paragraph.casefold()]
    else:
        matches = paragraphs
    return [paragraph[:1200] for paragraph in (matches or paragraphs)[:limit]]


class WorkbenchMcpServer:
    def __init__(self, *, challenge_root: Path = CHALLENGE_ROOT) -> None:
        self.challenge_root = challenge_root
        self.sources = load_sources(challenge_root)

    def handle(self, request: dict[str, Any]) -> dict[str, Any] | None:
        method = request.get("method")
        request_id = request.get("id")
        try:
            if method in {"notifications/initialized", "notifications/cancelled"}:
                return None
            if method == "initialize":
                return self._response(request_id, self._initialize())
            if method == "tools/list":
                return self._response(request_id, {"tools": self._tools()})
            if method == "tools/call":
                params = request.get("params") or {}
                return self._response(request_id, self._tool_call(str(params.get("name") or ""), params.get("arguments") or {}))
            if method == "resources/list":
                return self._response(request_id, {"resources": self._resources()})
            if method == "resources/read":
                params = request.get("params") or {}
                return self._response(request_id, self._resource_read(str(params.get("uri") or "")))
            if method == "ping":
                return self._response(request_id, {})
            return self._error(request_id, -32601, f"Unsupported method: {method}")
        except Exception as exc:  # noqa: BLE001 - JSON-RPC surface should return errors.
            return self._error(request_id, -32000, str(exc))

    def _initialize(self) -> dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}, "resources": {}},
            "serverInfo": {"name": "challenge2-dark-data-workbench", "version": "0.1.0"},
        }

    def _tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "workbench.search_sources",
                "description": "Search Challenge 2 workbench sources by title, metadata, flags, topics, and note text.",
                "inputSchema": {
                    "type": "object",
                    "required": ["query"],
                    "properties": {
                        "query": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                    },
                },
            },
            {
                "name": "workbench.read_source",
                "description": "Read one source summary and optionally its generated wiki note text.",
                "inputSchema": {
                    "type": "object",
                    "required": ["source_id"],
                    "properties": {
                        "source_id": {"type": "string"},
                        "include_note": {"type": "boolean"},
                        "max_bytes": {"type": "integer", "minimum": 1},
                    },
                },
            },
            {
                "name": "workbench.build_context",
                "description": "Build an AI-ready context export from source IDs or a query.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "source_ids": {"type": "array", "items": {"type": "string"}},
                        "query": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                    },
                },
            },
        ]

    def _resources(self) -> list[dict[str, str]]:
        return [
            {
                "uri": "workbench://corpus",
                "name": "Dark Data Workbench corpus",
                "mimeType": "application/json",
            },
            {
                "uri": "workbench://source-register",
                "name": "Challenge 2 source register",
                "mimeType": "application/json",
            },
        ]

    def _tool_call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "workbench.search_sources":
            result = self.search_sources(str(arguments.get("query") or ""), int(arguments.get("limit") or 10))
        elif name == "workbench.read_source":
            result = self.read_source(
                str(arguments.get("source_id") or ""),
                include_note=bool(arguments.get("include_note")),
                max_bytes=int(arguments.get("max_bytes") or 30000),
            )
        elif name == "workbench.build_context":
            result = self.build_context(
                source_ids=[str(item) for item in arguments.get("source_ids") or []],
                query=str(arguments.get("query") or ""),
                limit=int(arguments.get("limit") or 10),
            )
        else:
            raise ValueError(f"Unknown tool: {name}")
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2, sort_keys=True)}]}

    def _resource_read(self, uri: str) -> dict[str, Any]:
        if uri == "workbench://corpus":
            text = json.dumps(self.build_context(source_ids=[], query="", limit=50), indent=2, sort_keys=True)
        elif uri == "workbench://source-register":
            text = REGISTER_PATH.read_text(encoding="utf-8")
        else:
            raise ValueError(f"Unknown resource: {uri}")
        return {"contents": [{"uri": uri, "mimeType": "application/json", "text": text}]}

    def search_sources(self, query: str, limit: int = 10) -> dict[str, Any]:
        needle = query.casefold().strip()
        matches = [source for source in self.sources if not needle or needle in source.search_text]
        matches.sort(key=lambda source: self._search_rank(source, needle))
        matches = matches[: min(limit, 50)]
        return {"query": query, "count": len(matches), "sources": [source.to_summary() for source in matches]}

    def read_source(self, source_id: str, *, include_note: bool = False, max_bytes: int = 30000) -> dict[str, Any]:
        source = self._find_source(source_id)
        payload = source.to_summary()
        payload["synthetic_data_notice"] = SYNTHETIC_NOTICE
        if include_note:
            payload["note_text"] = truncate_utf8(source.note_text, max_bytes)
            payload["truncated"] = len(source.note_text.encode("utf-8")) > max_bytes
        return payload

    def build_context(self, *, source_ids: list[str], query: str, limit: int = 10) -> dict[str, Any]:
        wanted = set(source_ids)
        if wanted:
            sources = [source for source in self.sources if source.source_id in wanted]
        else:
            sources = [source for source in self.sources if not query or query.casefold() in source.search_text][: min(limit, 50)]
        return {
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "mode": "mcp",
            "corpus": {
                "title": "Dark Data Workbench",
                "source_count": len(self.sources),
                "synthetic_data": True,
                "synthetic_data_notice": SYNTHETIC_NOTICE,
            },
            "instructions": {
                "answer_policy": "Use only the supplied context. If evidence is missing or ambiguous, say so.",
                "citation_policy": "Cite source_id for every factual claim.",
                "synthetic_data_notice": SYNTHETIC_NOTICE,
            },
            "sources": [
                {
                    **source.to_summary(),
                    "excerpts": extract_excerpts(source, query),
                    "selected": bool(wanted and source.source_id in wanted),
                    "highlighted": False,
                }
                for source in sources
            ],
        }

    def _find_source(self, source_id: str) -> SourceRecord:
        for source in self.sources:
            if source.source_id == source_id:
                return source
        raise ValueError(f"Unknown source_id: {source_id}")

    @staticmethod
    def _search_rank(source: SourceRecord, needle: str) -> tuple[int, str]:
        if not needle:
            return (0, source.source_id)
        if source.source_id.casefold() == needle:
            return (0, source.source_id)
        if needle in source.title.casefold():
            return (1, source.source_id)
        return (2, source.source_id)

    @staticmethod
    def _response(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    @staticmethod
    def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--challenge-root", type=Path, default=CHALLENGE_ROOT)
    args = parser.parse_args(argv)

    server = WorkbenchMcpServer(challenge_root=args.challenge_root.resolve())
    for line in sys.stdin:
        if not line.strip():
            continue
        response = server.handle(json.loads(line))
        if response is not None:
            print(json.dumps(response), flush=True)
    return 0


def truncate_utf8(text: str, max_bytes: int) -> str:
    if max_bytes <= 0:
        return ""
    data = text.encode("utf-8", errors="replace")
    if len(data) <= max_bytes:
        return text
    return data[:max_bytes].decode("utf-8", errors="ignore")


if __name__ == "__main__":
    raise SystemExit(main())
