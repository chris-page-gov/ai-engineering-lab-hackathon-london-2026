"""Core read-only Challenge 2 Wiki MCP implementation.

The package deliberately avoids a hard dependency on a specific MCP framework so
that stdio and HTTP transports can share the same tested logic.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4


PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "challenge2-wiki-mcp"
SERVER_VERSION = "0.1.0"
SYNTHETIC_NOTICE = (
    "Challenge 2 corpus data is synthetic hackathon fixture data. Synthetic names and "
    "contact-like values are retained for demo fidelity and should not be redacted."
)
DEFAULT_MAX_BYTES = 30000
DEFAULT_CONTEXT_BUDGET = 48000
TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")


class AccessDenied(ValueError):
    """Raised when a request tries to leave the read-only wiki source surface."""


@dataclass(frozen=True)
class SourceRecord:
    """One entry from `wiki/data/source-register.json`."""

    source_id: str
    title: str
    source_path: str
    note_path: str
    source_format: str = "unknown"
    document_type: str = "unknown"
    department: str = "Unknown"
    status: str = "unknown"
    topics: tuple[str, ...] = ()
    matched_topics: tuple[str, ...] = ()
    matched_entities: tuple[str, ...] = ()
    flags: tuple[str, ...] = ()
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def topics_all(self) -> tuple[str, ...]:
        return tuple(_dedupe([*self.topics, *self.matched_topics]))

    @property
    def searchable_text(self) -> str:
        return " ".join(
            [
                self.source_id,
                self.title,
                self.source_path,
                self.note_path,
                self.source_format,
                self.document_type,
                self.department,
                self.status,
                *self.topics_all,
                *self.matched_entities,
                *self.flags,
            ]
        )

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "title": self.title,
            "source_path": f"challenge-2/{self.source_path}",
            "note_path": f"challenge-2/{self.note_path}",
            "source_format": self.source_format,
            "document_type": self.document_type,
            "department": self.department,
            "status": self.status,
            "topics": list(self.topics_all),
            "matched_entities": list(self.matched_entities),
            "flags": list(self.flags),
            "synthetic_data_notice": SYNTHETIC_NOTICE,
        }


@dataclass(frozen=True)
class WikiNote:
    """A safely exposed wiki note or machine-readable wiki data file."""

    path: Path
    repo_rel_path: str
    challenge_rel_path: str
    title: str
    text: str
    sha256: str
    byte_size: int
    source_id: str | None = None
    source: SourceRecord | None = None
    frontmatter: dict[str, Any] = field(default_factory=dict)

    @property
    def searchable_text(self) -> str:
        source_text = self.source.searchable_text if self.source else ""
        return f"{self.title}\n{self.repo_rel_path}\n{source_text}\n{self.text}"

    def to_public_dict(self, *, include_frontmatter: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "path": self.repo_rel_path,
            "challenge_path": self.challenge_rel_path,
            "title": self.title,
            "source_id": self.source_id,
            "sha256": self.sha256,
            "byte_size": self.byte_size,
        }
        if self.source:
            payload["source"] = self.source.to_public_dict()
        if include_frontmatter:
            payload["frontmatter"] = self.frontmatter
        return payload


@dataclass(frozen=True)
class SearchResult:
    """One lexical, semantic, or hybrid retrieval result."""

    note: WikiNote
    score: float
    match_type: str
    snippets: tuple[dict[str, Any], ...]

    def to_public_dict(self) -> dict[str, Any]:
        payload = self.note.to_public_dict()
        payload.update(
            {
                "score": round(self.score, 6),
                "match_type": self.match_type,
                "snippets": list(self.snippets),
            }
        )
        return payload


class AuditLogger:
    """Append-only JSONL audit logger for MCP source access and denials."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, event_type: str, **payload: Any) -> None:
        if not self.path:
            return
        record = {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "timestamp": utc_now(),
            **payload,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    def summary(self) -> dict[str, Any]:
        if not self.path or not self.path.exists():
            return {"path": str(self.path) if self.path else None, "event_count": 0, "event_types": {}}
        counts: dict[str, int] = {}
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            event_type = str(json.loads(line).get("event_type") or "")
            counts[event_type] = counts.get(event_type, 0) + 1
        return {"path": str(self.path), "event_count": sum(counts.values()), "event_types": counts}


class PathPolicy:
    """Canonical allowlist/denylist policy for the exposed wiki surface."""

    def __init__(
        self,
        *,
        repo_root: Path,
        challenge_root: Path,
        max_file_bytes: int = 2_000_000,
        extensions: Iterable[str] = (".md", ".json", ".csv", ".txt"),
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.challenge_root = challenge_root.resolve()
        self.wiki_root = (self.challenge_root / "wiki").resolve()
        self.wiki_data_root = (self.wiki_root / "data").resolve()
        self.agents_path = (self.challenge_root / "AGENTS.md").resolve()
        self.benchmark_path = (self.wiki_root / "evaluation-benchmark.md").resolve()
        self.max_file_bytes = max_file_bytes
        self.extensions = {extension.lower() for extension in extensions}

    def iter_allowed_files(self) -> list[Path]:
        files = [self.agents_path]
        if self.wiki_root.exists():
            files.extend(sorted(path for path in self.wiki_root.rglob("*") if path.is_file()))
        allowed: list[Path] = []
        for path in files:
            try:
                allowed.append(self.resolve(path))
            except AccessDenied:
                continue
        return allowed

    def resolve(self, raw_path: str | Path) -> Path:
        candidate = Path(raw_path)
        if not candidate.is_absolute():
            candidate = self.repo_root / candidate
        resolved = candidate.resolve()
        if resolved == self.benchmark_path:
            raise AccessDenied("Benchmark file is not exposed because it contains gold-answer material.")
        if self._has_symlink(candidate):
            raise AccessDenied(f"Symlink paths are not exposed: {raw_path}")
        if resolved == self.agents_path:
            return self._validate_file(resolved)
        if resolved == self.wiki_root or self.wiki_root in resolved.parents:
            if self._is_denied_wiki_path(resolved):
                raise AccessDenied(f"Denied wiki path: {self._display_path(resolved)}")
            return self._validate_file(resolved)
        raise AccessDenied(f"Path is outside allowed Challenge 2 wiki scope: {raw_path}")

    def repo_rel(self, path: Path) -> str:
        return path.resolve().relative_to(self.repo_root).as_posix()

    def challenge_rel(self, path: Path) -> str:
        return path.resolve().relative_to(self.challenge_root).as_posix()

    def _validate_file(self, path: Path) -> Path:
        if not path.exists() or not path.is_file():
            raise AccessDenied(f"Allowed path is not a file: {self._display_path(path)}")
        if path.suffix.lower() not in self.extensions:
            raise AccessDenied(f"File extension is not exposed: {self._display_path(path)}")
        if path.stat().st_size > self.max_file_bytes:
            raise AccessDenied(f"File exceeds maximum exposed size: {self._display_path(path)}")
        return path

    def _is_denied_wiki_path(self, path: Path) -> bool:
        parts = set(path.relative_to(self.wiki_root).parts)
        if path == self.benchmark_path:
            return True
        denied_names = {
            ".DS_Store",
            "workspace.json",
        }
        if path.name in denied_names:
            return True
        denied_parts = {
            ".obsidian",
            "__pycache__",
            "evaluation",
            "runs",
            "postmortem",
            "postmortem-public",
        }
        return bool(parts & denied_parts)

    def _has_symlink(self, path: Path) -> bool:
        probe = path if path.is_absolute() else self.repo_root / path
        parts = probe.parts
        current = Path(parts[0])
        for part in parts[1:]:
            current = current / part
            try:
                if current.is_symlink():
                    return True
            except OSError:
                return True
        return False

    def _display_path(self, path: Path) -> str:
        try:
            return self.repo_rel(path)
        except ValueError:
            return str(path)


class WikiKnowledgeBase:
    """Read-only searchable view over the generated Challenge 2 wiki."""

    def __init__(
        self,
        *,
        repo_root: Path,
        challenge_root: Path,
        audit: AuditLogger | None = None,
        semantic_dimensions: int = 384,
        semantic_model_id: str = "challenge2-local-hash-v1",
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.challenge_root = challenge_root.resolve()
        self.audit = audit or AuditLogger()
        self.policy = PathPolicy(repo_root=self.repo_root, challenge_root=self.challenge_root)
        self.semantic_dimensions = semantic_dimensions
        self.semantic_model_id = semantic_model_id
        self.sources = self._load_sources()
        self.sources_by_id = {source.source_id: source for source in self.sources}
        self.sources_by_note_path = {
            f"challenge-2/{source.note_path}": source for source in self.sources if source.note_path
        }
        self.notes = self._load_notes()
        self.notes_by_repo_path = {note.repo_rel_path: note for note in self.notes}
        self.notes_by_source_id = {note.source_id: note for note in self.notes if note.source_id}
        self._semantic_vectors: dict[str, list[float]] | None = None

    def search(
        self,
        query: str,
        *,
        limit: int = 10,
        mode: str = "hybrid",
        source_ids: Iterable[str] | None = None,
        tags: Iterable[str] | None = None,
        max_snippet_chars: int = 500,
    ) -> dict[str, Any]:
        mode = _bounded_choice(mode, {"lexical", "semantic", "hybrid"}, "hybrid")
        selected_notes = self._filter_notes(source_ids=source_ids, tags=tags)
        lexical = self._lexical_search(query, selected_notes, max_snippet_chars=max_snippet_chars)
        semantic = self._semantic_search(query, selected_notes, max_snippet_chars=max_snippet_chars)
        if mode == "lexical":
            results = lexical
        elif mode == "semantic":
            results = semantic
        else:
            results = self._merge_results(lexical, semantic)
        results = results[: _bounded_int(limit, default=10, minimum=1, maximum=50)]
        self.audit.record(
            "wiki.search",
            query=query,
            mode=mode,
            result_count=len(results),
            source_ids=list(source_ids or []),
            tags=list(tags or []),
        )
        return {
            "query": query,
            "mode": mode,
            "count": len(results),
            "results": [result.to_public_dict() for result in results],
            "semantic_index": self.semantic_manifest(),
        }

    def read_note(
        self,
        raw_path: str,
        *,
        offset: int = 0,
        max_bytes: int = DEFAULT_MAX_BYTES,
        include_frontmatter: bool = False,
        include_backlinks: bool = False,
    ) -> dict[str, Any]:
        path = self.policy.resolve(raw_path)
        note = self.notes_by_repo_path.get(self.policy.repo_rel(path))
        if note is None:
            note = self._note_from_path(path)
        data = path.read_bytes()
        safe_offset = max(int(offset), 0)
        safe_max = _bounded_int(max_bytes, default=DEFAULT_MAX_BYTES, minimum=1, maximum=100000)
        chunk = data[safe_offset : safe_offset + safe_max]
        payload = note.to_public_dict(include_frontmatter=include_frontmatter)
        payload.update(
            {
                "offset": safe_offset,
                "next_offset": safe_offset + len(chunk) if safe_offset + len(chunk) < len(data) else None,
                "text": chunk.decode("utf-8", errors="replace"),
                "truncated": safe_offset + len(chunk) < len(data),
            }
        )
        if include_backlinks:
            payload["backlinks"] = self._backlinks(note.repo_rel_path)
        self.audit.record(
            "wiki.read",
            path=note.repo_rel_path,
            offset=safe_offset,
            max_bytes=safe_max,
            sha256=note.sha256,
        )
        return payload

    def list_sources(
        self,
        *,
        query: str = "",
        status: str | None = None,
        department: str | None = None,
        topic: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        needle = query.casefold().strip()
        results: list[SourceRecord] = []
        for source in self.sources:
            if needle and needle not in source.searchable_text.casefold():
                continue
            if status and status.casefold() != source.status.casefold():
                continue
            if department and department.casefold() not in source.department.casefold():
                continue
            if topic and topic.casefold() not in {item.casefold() for item in source.topics_all}:
                continue
            results.append(source)
        results.sort(key=lambda source: (source.status != "current", source.source_id))
        results = results[: _bounded_int(limit, default=50, minimum=1, maximum=100)]
        self.audit.record(
            "wiki.list_sources",
            query=query,
            status=status,
            department=department,
            topic=topic,
            result_count=len(results),
        )
        return {"count": len(results), "sources": [source.to_public_dict() for source in results]}

    def read_source(self, source_id: str, *, include_note: bool = False, max_bytes: int = DEFAULT_MAX_BYTES) -> dict[str, Any]:
        source = self.find_source(source_id)
        payload = source.to_public_dict()
        note = self.notes_by_source_id.get(source.source_id)
        if note:
            payload["note"] = note.to_public_dict()
        if include_note and note:
            payload["note_text"] = self.read_note(
                note.repo_rel_path,
                max_bytes=max_bytes,
                include_frontmatter=True,
            )["text"]
        self.audit.record("wiki.read_source", source_id=source.source_id, include_note=include_note)
        return payload

    def source_register(self) -> dict[str, Any]:
        note = self.read_note(f"challenge-2/wiki/data/source-register.json", max_bytes=100000)
        return {
            "path": note["path"],
            "sha256": note["sha256"],
            "source_count": len(self.sources),
            "sources": [source.to_public_dict() for source in self.sources],
            "raw_json_path": "challenge-2/wiki/data/source-register.json",
        }

    def find_source(self, source_id: str) -> SourceRecord:
        wanted = source_id.strip().upper()
        try:
            return self.sources_by_id[wanted]
        except KeyError as exc:
            raise ValueError(f"Unknown source_id: {source_id}") from exc

    def build_context_pack(
        self,
        *,
        query: str = "",
        paths: Iterable[str] | None = None,
        source_ids: Iterable[str] | None = None,
        limit: int = 8,
        budget_bytes: int = DEFAULT_CONTEXT_BUDGET,
        mode: str = "hybrid",
    ) -> dict[str, Any]:
        budget = _bounded_int(budget_bytes, default=DEFAULT_CONTEXT_BUDGET, minimum=1000, maximum=200000)
        selected: list[WikiNote] = []
        seen: set[str] = set()
        for source_id in source_ids or []:
            source = self.find_source(source_id)
            note = self.notes_by_source_id.get(source.source_id)
            if note and note.repo_rel_path not in seen:
                selected.append(note)
                seen.add(note.repo_rel_path)
        for raw_path in paths or []:
            note = self.notes_by_repo_path.get(self.policy.repo_rel(self.policy.resolve(raw_path)))
            if note and note.repo_rel_path not in seen:
                selected.append(note)
                seen.add(note.repo_rel_path)
        if query.strip():
            search_payload = self.search(query, limit=limit, mode=mode)
            for item in search_payload["results"]:
                note = self.notes_by_repo_path[item["path"]]
                if note.repo_rel_path not in seen:
                    selected.append(note)
                    seen.add(note.repo_rel_path)
        selected = selected[: _bounded_int(limit, default=8, minimum=1, maximum=50)]
        evidence: list[dict[str, Any]] = []
        remaining = budget
        for note in selected:
            if remaining <= 0:
                break
            text = _strip_frontmatter(note.text).strip()
            excerpt = text[:remaining]
            remaining -= len(excerpt.encode("utf-8", errors="replace"))
            evidence.append(
                {
                    **note.to_public_dict(),
                    "excerpt": excerpt,
                    "truncated": len(excerpt) < len(text),
                }
            )
        pack = {
            "created_at": utc_now(),
            "query": query,
            "mode": mode,
            "source_policy": {
                "allowed_sources": [
                    "challenge-2/wiki/",
                    "challenge-2/wiki/data/",
                    "challenge-2/AGENTS.md",
                ],
                "denied_sources": [
                    "challenge-2/wiki/evaluation-benchmark.md",
                    "challenge-2/evaluation/",
                    "generated run artifacts",
                    "local application state",
                ],
                "synthetic_data_notice": SYNTHETIC_NOTICE,
            },
            "answer_policy": {
                "instruction": "Answer only from this context pack. If evidence is missing or ambiguous, say so.",
                "citation_policy": "Cite `path` and `source_id` where available for each factual claim.",
            },
            "semantic_index": self.semantic_manifest(),
            "evidence_count": len(evidence),
            "evidence": evidence,
        }
        self.audit.record(
            "wiki.build_context_pack",
            query=query,
            mode=mode,
            evidence_count=len(evidence),
            budget_bytes=budget,
        )
        return pack

    def explain_provenance(self, *, path: str | None = None, source_id: str | None = None) -> dict[str, Any]:
        note: WikiNote | None = None
        source: SourceRecord | None = None
        if source_id:
            source = self.find_source(source_id)
            note = self.notes_by_source_id.get(source.source_id)
        if path:
            resolved = self.policy.resolve(path)
            note = self.notes_by_repo_path.get(self.policy.repo_rel(resolved))
            source = note.source if note else source
        if not note and not source:
            raise ValueError("Provide a known path or source_id")
        payload = {
            "note": note.to_public_dict(include_frontmatter=True) if note else None,
            "source": source.to_public_dict() if source else None,
            "raw_source_exposed": False,
            "raw_source_policy": "Raw structured_files and unstructured_files are not exposed through this MCP server.",
            "synthetic_data_notice": SYNTHETIC_NOTICE,
        }
        self.audit.record(
            "wiki.explain_provenance",
            path=note.repo_rel_path if note else path,
            source_id=source.source_id if source else source_id,
        )
        return payload

    def semantic_manifest(self) -> dict[str, Any]:
        if self._semantic_vectors is None:
            vector_count = 0
            index_hash = None
        else:
            vector_count = len(self._semantic_vectors)
            digest = hashlib.sha256()
            for path in sorted(self._semantic_vectors):
                digest.update(path.encode("utf-8"))
                digest.update(json.dumps(self._semantic_vectors[path], separators=(",", ":")).encode("utf-8"))
            index_hash = digest.hexdigest()
        return {
            "provider": "deterministic-local-hash",
            "requested_model_id": self.semantic_model_id,
            "effective_model_id": "challenge2-local-hash-v1",
            "dimensions": self.semantic_dimensions,
            "index_type": "exact-cosine",
            "vector_count": vector_count,
            "index_sha256": index_hash,
            "corpus_note_count": len(self.notes),
            "benchmark_excluded": True,
        }

    def audit_summary(self) -> dict[str, Any]:
        return self.audit.summary()

    def _load_sources(self) -> list[SourceRecord]:
        register_path = self.challenge_root / "wiki" / "data" / "source-register.json"
        raw_records = json.loads(register_path.read_text(encoding="utf-8"))
        sources = []
        for raw in raw_records:
            sources.append(
                SourceRecord(
                    source_id=str(raw.get("source_id") or "").upper(),
                    title=str(raw.get("title") or ""),
                    source_path=str(raw.get("source_path") or ""),
                    note_path=str(raw.get("note_path") or ""),
                    source_format=str(raw.get("source_format") or "unknown"),
                    document_type=str(raw.get("document_type") or "unknown"),
                    department=str(raw.get("department") or "Unknown"),
                    status=str(raw.get("status") or "unknown"),
                    topics=tuple(str(item) for item in raw.get("topics") or []),
                    matched_topics=tuple(str(item) for item in raw.get("matched_topics") or []),
                    matched_entities=tuple(str(item) for item in raw.get("matched_entities") or []),
                    flags=tuple(str(item) for item in raw.get("flags") or []),
                    raw=raw,
                )
            )
        return sources

    def _load_notes(self) -> list[WikiNote]:
        notes = [self._note_from_path(path) for path in self.policy.iter_allowed_files()]
        notes.sort(key=lambda note: note.repo_rel_path)
        return notes

    def _note_from_path(self, path: Path) -> WikiNote:
        text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter = _parse_frontmatter(text)
        repo_rel = self.policy.repo_rel(path)
        challenge_rel = self.policy.challenge_rel(path)
        source_id = str(frontmatter.get("source_id") or "").upper() or None
        source = self.sources_by_id.get(source_id or "") or self.sources_by_note_path.get(repo_rel)
        if source and not source_id:
            source_id = source.source_id
        title = str(frontmatter.get("title") or _first_heading(text) or path.stem)
        data = path.read_bytes()
        return WikiNote(
            path=path,
            repo_rel_path=repo_rel,
            challenge_rel_path=challenge_rel,
            title=title,
            text=text,
            sha256=hashlib.sha256(data).hexdigest(),
            byte_size=len(data),
            source_id=source_id,
            source=source,
            frontmatter=frontmatter,
        )

    def _filter_notes(
        self,
        *,
        source_ids: Iterable[str] | None,
        tags: Iterable[str] | None,
    ) -> list[WikiNote]:
        wanted_source_ids = {item.strip().upper() for item in source_ids or [] if item.strip()}
        wanted_tags = {item.casefold() for item in tags or [] if item.strip()}
        notes = []
        for note in self.notes:
            if wanted_source_ids and note.source_id not in wanted_source_ids:
                continue
            if wanted_tags:
                note_tags = {str(item).casefold() for item in note.frontmatter.get("tags") or []}
                note_topics = {str(item).casefold() for item in note.frontmatter.get("topics") or []}
                source_topics = {item.casefold() for item in (note.source.topics_all if note.source else ())}
                if not wanted_tags & (note_tags | note_topics | source_topics):
                    continue
            notes.append(note)
        return notes

    def _lexical_search(self, query: str, notes: list[WikiNote], *, max_snippet_chars: int) -> list[SearchResult]:
        query_tokens = _tokens(query)
        phrase = query.casefold().strip()
        results: list[SearchResult] = []
        for note in notes:
            searchable = note.searchable_text.casefold()
            if not query_tokens and not phrase:
                score = 0.1
            else:
                score = 0.0
                if phrase and phrase in searchable:
                    score += 20.0
                for token in query_tokens:
                    count = searchable.count(token)
                    if count:
                        score += 2.0 + min(count, 8) * 0.25
                if note.source_id and note.source_id.casefold() in query.casefold():
                    score += 25.0
                if phrase and phrase in note.title.casefold():
                    score += 10.0
            if score <= 0:
                continue
            snippets = tuple(_snippets(note.text, query_tokens, phrase, max_chars=max_snippet_chars))
            results.append(SearchResult(note=note, score=score, match_type="lexical", snippets=snippets))
        results.sort(key=lambda item: (-item.score, item.note.repo_rel_path))
        return results

    def _semantic_search(self, query: str, notes: list[WikiNote], *, max_snippet_chars: int) -> list[SearchResult]:
        query_vector = _hash_vector(query, dimensions=self.semantic_dimensions)
        if self._semantic_vectors is None:
            self._semantic_vectors = {
                note.repo_rel_path: _hash_vector(note.searchable_text, dimensions=self.semantic_dimensions)
                for note in self.notes
            }
        query_tokens = _tokens(query)
        phrase = query.casefold().strip()
        results: list[SearchResult] = []
        for note in notes:
            vector = self._semantic_vectors.get(note.repo_rel_path)
            if vector is None:
                continue
            score = _cosine(query_vector, vector)
            if score <= 0:
                continue
            snippets = tuple(_snippets(note.text, query_tokens, phrase, max_chars=max_snippet_chars))
            results.append(SearchResult(note=note, score=score, match_type="semantic", snippets=snippets))
        results.sort(key=lambda item: (-item.score, item.note.repo_rel_path))
        return results

    @staticmethod
    def _merge_results(lexical: list[SearchResult], semantic: list[SearchResult]) -> list[SearchResult]:
        merged: dict[str, SearchResult] = {}
        for result in semantic:
            merged[result.note.repo_rel_path] = SearchResult(
                note=result.note,
                score=result.score * 10.0,
                match_type="semantic",
                snippets=result.snippets,
            )
        for result in lexical:
            existing = merged.get(result.note.repo_rel_path)
            if existing:
                merged[result.note.repo_rel_path] = SearchResult(
                    note=result.note,
                    score=result.score + existing.score,
                    match_type="hybrid",
                    snippets=result.snippets or existing.snippets,
                )
            else:
                merged[result.note.repo_rel_path] = result
        results = list(merged.values())
        results.sort(key=lambda item: (-item.score, item.note.repo_rel_path))
        return results

    def _backlinks(self, repo_rel_path: str) -> list[dict[str, Any]]:
        filename = Path(repo_rel_path).name
        backlinks: list[dict[str, Any]] = []
        for note in self.notes:
            if note.repo_rel_path == repo_rel_path:
                continue
            if filename in note.text:
                backlinks.append({"path": note.repo_rel_path, "title": note.title})
        backlinks.sort(key=lambda item: item["path"])
        return backlinks


class WikiMcpServer:
    """JSON-RPC MCP protocol surface over the Challenge 2 wiki knowledge base."""

    def __init__(self, knowledge_base: WikiKnowledgeBase) -> None:
        self.kb = knowledge_base

    def handle(self, request: dict[str, Any]) -> dict[str, Any] | None:
        method = str(request.get("method") or "")
        request_id = request.get("id")
        try:
            if method in {"notifications/initialized", "notifications/cancelled"}:
                return None
            if method == "initialize":
                return self._response(request_id, self.initialize())
            if method == "ping":
                return self._response(request_id, {})
            if method == "tools/list":
                return self._response(request_id, {"tools": self.tools()})
            if method == "tools/call":
                params = request.get("params") or {}
                return self._response(
                    request_id,
                    self.call_tool(str(params.get("name") or ""), params.get("arguments") or {}),
                )
            if method == "resources/list":
                return self._response(request_id, {"resources": self.resources()})
            if method == "resources/read":
                params = request.get("params") or {}
                return self._response(request_id, self.read_resource(str(params.get("uri") or "")))
            if method == "prompts/list":
                return self._response(request_id, {"prompts": self.prompts()})
            if method == "prompts/get":
                params = request.get("params") or {}
                return self._response(request_id, self.get_prompt(str(params.get("name") or ""), params.get("arguments") or {}))
            return self._error(request_id, -32601, f"Unsupported method: {method}")
        except AccessDenied as exc:
            self.kb.audit.record("wiki.denied", method=method, message=str(exc))
            return self._error(request_id, -32001, str(exc))
        except Exception as exc:  # noqa: BLE001 - JSON-RPC errors are the protocol surface.
            return self._error(request_id, -32000, str(exc))

    def initialize(self) -> dict[str, Any]:
        return {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        }

    def tools(self) -> list[dict[str, Any]]:
        return [
            _tool_schema(
                "wiki.search",
                "Search the Challenge 2 generated wiki with lexical, semantic, or hybrid retrieval.",
                {
                    "query": {"type": "string"},
                    "mode": {"type": "string", "enum": ["lexical", "semantic", "hybrid"]},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                    "source_ids": {"type": "array", "items": {"type": "string"}},
                    "tags": {"type": "array", "items": {"type": "string"}},
                },
                required=["query"],
            ),
            _tool_schema(
                "wiki.read",
                "Read an allowlisted wiki note, wiki data file, or challenge-2/AGENTS.md.",
                {
                    "path": {"type": "string"},
                    "offset": {"type": "integer", "minimum": 0},
                    "max_bytes": {"type": "integer", "minimum": 1, "maximum": 100000},
                    "include_frontmatter": {"type": "boolean"},
                    "include_backlinks": {"type": "boolean"},
                },
                required=["path"],
            ),
            _tool_schema(
                "wiki.list_sources",
                "List source-register entries by query, status, department, or topic.",
                {
                    "query": {"type": "string"},
                    "status": {"type": "string"},
                    "department": {"type": "string"},
                    "topic": {"type": "string"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 100},
                },
            ),
            _tool_schema(
                "wiki.read_source",
                "Read one source-register entry and optionally its generated source note.",
                {
                    "source_id": {"type": "string"},
                    "include_note": {"type": "boolean"},
                    "max_bytes": {"type": "integer", "minimum": 1, "maximum": 100000},
                },
                required=["source_id"],
            ),
            _tool_schema(
                "wiki.source_register",
                "Return the source register in publication-safe structured form.",
                {},
            ),
            _tool_schema(
                "wiki.read_source_register",
                "Alias for wiki.source_register for clients that prefer read-style tool names.",
                {},
            ),
            _tool_schema(
                "wiki.find_by_source_id",
                "Find one source-register entry by source ID.",
                {
                    "source_id": {"type": "string"},
                    "include_note": {"type": "boolean"},
                    "max_bytes": {"type": "integer", "minimum": 1, "maximum": 100000},
                },
                required=["source_id"],
            ),
            _tool_schema(
                "wiki.build_context_pack",
                "Build a bounded, citation-ready context pack from query, paths, or source IDs.",
                {
                    "query": {"type": "string"},
                    "paths": {"type": "array", "items": {"type": "string"}},
                    "source_ids": {"type": "array", "items": {"type": "string"}},
                    "mode": {"type": "string", "enum": ["lexical", "semantic", "hybrid"]},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                    "budget_bytes": {"type": "integer", "minimum": 1000, "maximum": 200000},
                },
            ),
            _tool_schema(
                "wiki.explain_provenance",
                "Explain the provenance for a wiki path or source ID without exposing raw source files.",
                {
                    "path": {"type": "string"},
                    "source_id": {"type": "string"},
                },
            ),
            _tool_schema(
                "wiki.audit_summary",
                "Summarise the server audit log for this MCP session.",
                {},
            ),
        ]

    def resources(self) -> list[dict[str, str]]:
        resources = [
            {"uri": "wiki://index", "name": "Challenge 2 wiki index", "mimeType": "text/markdown"},
            {"uri": "wiki://source-register", "name": "Challenge 2 source register", "mimeType": "application/json"},
            {"uri": "wiki://agents", "name": "Challenge 2 AI operating rules", "mimeType": "text/markdown"},
            {"uri": "wiki://semantic-manifest", "name": "Semantic retrieval manifest", "mimeType": "application/json"},
        ]
        for source in self.kb.sources[:50]:
            resources.append(
                {
                    "uri": f"wiki://source/{source.source_id}",
                    "name": source.title,
                    "mimeType": "application/json",
                }
            )
        return resources

    def prompts(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "wiki.answer_question",
                "description": "Answer a Challenge 2 question using only a generated context pack.",
                "arguments": [
                    {"name": "question", "description": "Question to answer from the wiki", "required": True},
                    {"name": "mode", "description": "lexical, semantic, or hybrid retrieval", "required": False},
                ],
            }
        ]

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "wiki.search":
            result = self.kb.search(
                str(arguments.get("query") or ""),
                limit=int(arguments.get("limit") or 10),
                mode=str(arguments.get("mode") or "hybrid"),
                source_ids=[str(item) for item in arguments.get("source_ids") or []],
                tags=[str(item) for item in arguments.get("tags") or []],
            )
        elif name == "wiki.read":
            result = self.kb.read_note(
                str(arguments.get("path") or ""),
                offset=int(arguments.get("offset") or 0),
                max_bytes=int(arguments.get("max_bytes") or DEFAULT_MAX_BYTES),
                include_frontmatter=bool(arguments.get("include_frontmatter")),
                include_backlinks=bool(arguments.get("include_backlinks")),
            )
        elif name == "wiki.list_sources":
            result = self.kb.list_sources(
                query=str(arguments.get("query") or ""),
                status=_optional_str(arguments.get("status")),
                department=_optional_str(arguments.get("department")),
                topic=_optional_str(arguments.get("topic")),
                limit=int(arguments.get("limit") or 50),
            )
        elif name == "wiki.read_source":
            result = self.kb.read_source(
                str(arguments.get("source_id") or ""),
                include_note=bool(arguments.get("include_note")),
                max_bytes=int(arguments.get("max_bytes") or DEFAULT_MAX_BYTES),
            )
        elif name in {"wiki.source_register", "wiki.read_source_register"}:
            result = self.kb.source_register()
        elif name == "wiki.find_by_source_id":
            result = self.kb.read_source(
                str(arguments.get("source_id") or ""),
                include_note=bool(arguments.get("include_note")),
                max_bytes=int(arguments.get("max_bytes") or DEFAULT_MAX_BYTES),
            )
        elif name == "wiki.build_context_pack":
            result = self.kb.build_context_pack(
                query=str(arguments.get("query") or ""),
                paths=[str(item) for item in arguments.get("paths") or []],
                source_ids=[str(item) for item in arguments.get("source_ids") or []],
                limit=int(arguments.get("limit") or 8),
                budget_bytes=int(arguments.get("budget_bytes") or DEFAULT_CONTEXT_BUDGET),
                mode=str(arguments.get("mode") or "hybrid"),
            )
        elif name == "wiki.explain_provenance":
            result = self.kb.explain_provenance(
                path=_optional_str(arguments.get("path")),
                source_id=_optional_str(arguments.get("source_id")),
            )
        elif name == "wiki.audit_summary":
            result = self.kb.audit_summary()
        else:
            raise ValueError(f"Unknown tool: {name}")
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2, sort_keys=True)}]}

    def read_resource(self, uri: str) -> dict[str, Any]:
        if uri == "wiki://index":
            note = self.kb.read_note("challenge-2/wiki/index.md", max_bytes=100000)
            return _resource_text(uri, "text/markdown", note["text"])
        if uri == "wiki://source-register":
            text = json.dumps(self.kb.source_register(), indent=2, sort_keys=True)
            return _resource_text(uri, "application/json", text)
        if uri == "wiki://agents":
            note = self.kb.read_note("challenge-2/AGENTS.md", max_bytes=100000)
            return _resource_text(uri, "text/markdown", note["text"])
        if uri == "wiki://semantic-manifest":
            text = json.dumps(self.kb.semantic_manifest(), indent=2, sort_keys=True)
            return _resource_text(uri, "application/json", text)
        if uri.startswith("wiki://source/"):
            source_id = uri.rsplit("/", 1)[-1]
            text = json.dumps(self.kb.read_source(source_id, include_note=False), indent=2, sort_keys=True)
            return _resource_text(uri, "application/json", text)
        raise ValueError(f"Unknown resource URI: {uri}")

    def get_prompt(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name != "wiki.answer_question":
            raise ValueError(f"Unknown prompt: {name}")
        question = str(arguments.get("question") or "").strip()
        if not question:
            raise ValueError("Prompt argument 'question' is required")
        mode = str(arguments.get("mode") or "hybrid")
        pack = self.kb.build_context_pack(query=question, mode=mode)
        text = _format_context_prompt(question, pack)
        return {
            "description": "Answer from the Challenge 2 wiki MCP context pack.",
            "messages": [{"role": "user", "content": {"type": "text", "text": text}}],
        }

    @staticmethod
    def _response(request_id: Any, result: Any) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    @staticmethod
    def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def build_codex_mcp_prompt(
    question_id: str,
    category: str,
    question: str,
    context_pack: dict[str, Any],
    *,
    include_context_pack: bool = False,
) -> str:
    """Build the benchmark prompt for Codex when using the wiki MCP context path."""

    prompt_context = context_pack if include_context_pack else _context_pack_stub(context_pack)
    return "\n".join(
        [
            "You are answering a Challenge 2 wiki evaluation question using the Challenge 2 Wiki MCP server.",
            "",
            "Mandatory validation step: before answering, call at least one Challenge 2 Wiki MCP tool such as `wiki.search`, `wiki.read`, or `wiki.build_context_pack`.",
            "Use only the MCP-provided wiki tools as authority.",
            "Do not use web search or outside knowledge.",
            "Do not inspect challenge-2/wiki/evaluation-benchmark.md or challenge-2/evaluation/.",
            "Cite source IDs or wiki paths for every factual claim.",
            "Preserve caveats such as draft, stale, superseded, synthetic, low OCR quality, contradictory, or incomplete material.",
            "If the MCP tools are unavailable, return JSON with an empty answer and a caveat explaining that MCP validation failed.",
            "",
            "Return concise JSON with this shape:",
            '{"question_id":"Q000","answer":"...","cited_sources":["..."],"caveats":["..."]}',
            "",
            f"Question ID: {question_id}",
            f"Category: {category}",
            f"Question: {question}",
            "",
            "MCP context pack audit seed:",
            json.dumps(prompt_context, indent=2, sort_keys=True),
        ]
    )


def _context_pack_stub(context_pack: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at": context_pack.get("created_at"),
        "query": context_pack.get("query"),
        "mode": context_pack.get("mode"),
        "evidence_count": context_pack.get("evidence_count"),
        "source_policy": context_pack.get("source_policy"),
        "semantic_index": context_pack.get("semantic_index"),
        "evidence": "[withheld from prompt to require live MCP tool validation; full pack retained as run artifact]",
    }


def _format_context_prompt(question: str, context_pack: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Answer the question using only this Challenge 2 wiki context pack.",
            "Cite `path` and `source_id` values where available.",
            "",
            f"Question: {question}",
            "",
            json.dumps(context_pack, indent=2, sort_keys=True),
        ]
    )


def _tool_schema(
    name: str,
    description: str,
    properties: dict[str, Any],
    *,
    required: list[str] | None = None,
) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "object", "properties": properties}
    if required:
        schema["required"] = required
    return {"name": name, "description": description, "inputSchema": schema}


def _resource_text(uri: str, mime_type: str, text: str) -> dict[str, Any]:
    return {"contents": [{"uri": uri, "mimeType": mime_type, "text": text}]}


def _tokens(value: str) -> list[str]:
    return [match.group(0).casefold() for match in TOKEN_RE.finditer(value)]


def _hash_vector(value: str, *, dimensions: int) -> list[float]:
    vector = [0.0] * dimensions
    for token in _tokens(value):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign
    norm = math.sqrt(sum(item * item for item in vector))
    if norm == 0:
        return vector
    return [item / norm for item in vector]


def _cosine(left: list[float], right: list[float]) -> float:
    return sum(l_item * r_item for l_item, r_item in zip(left, right))


def _snippets(text: str, query_tokens: list[str], phrase: str, *, max_chars: int) -> list[dict[str, Any]]:
    body = _strip_frontmatter(text)
    folded = body.casefold()
    starts: list[int] = []
    if phrase:
        index = folded.find(phrase)
        if index >= 0:
            starts.append(index)
    for token in query_tokens:
        index = folded.find(token)
        if index >= 0:
            starts.append(index)
    if not starts:
        starts.append(0)
    snippets: list[dict[str, Any]] = []
    seen: set[int] = set()
    width = _bounded_int(max_chars, default=500, minimum=80, maximum=2000)
    for index in sorted(starts)[:3]:
        start = max(0, index - width // 3)
        end = min(len(body), start + width)
        start = max(0, end - width)
        if start in seen:
            continue
        seen.add(start)
        line_no = body.count("\n", 0, start) + 1
        snippets.append(
            {
                "line": line_no,
                "char_start": start,
                "char_end": end,
                "text": body[start:end].replace("\n", " ").strip(),
            }
        )
    return snippets


def _parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    frontmatter: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in parts[1].splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            frontmatter.setdefault(current_key, []).append(_clean_scalar(line[4:]))
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if value == "":
                frontmatter[key] = []
            elif value in {"[]", "null"}:
                frontmatter[key] = [] if value == "[]" else None
            else:
                frontmatter[key] = _clean_scalar(value)
    return frontmatter


def _strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    parts = text.split("---", 2)
    return parts[2].lstrip() if len(parts) == 3 else text


def _first_heading(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _clean_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def _bounded_int(value: Any, *, default: int, minimum: int, maximum: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = default
    return max(minimum, min(maximum, number))


def _bounded_choice(value: str, choices: set[str], default: str) -> str:
    return value if value in choices else default


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
