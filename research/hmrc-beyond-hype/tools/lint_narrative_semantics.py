#!/usr/bin/env python3
"""Semantic lint checks for the HMRC talk narrative wiki.

The structural validator proves that the wiki is linked and complete. This
script covers softer editorial risks that still need automation: stale-looking
claims, count contradictions, missing concept pages, and live external links.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[3]
NARRATIVE_DIR = REPO_ROOT / "research" / "hmrc-beyond-hype" / "narrative"
IMPORT_DIR = REPO_ROOT / "research" / "hmrc-beyond-hype" / "import"
REPORT_JSON = NARRATIVE_DIR / "data" / "narrative_semantic_lint_report.json"
REPORT_MD = NARRATIVE_DIR / "data" / "narrative_semantic_lint_report.md"
SEMANTIC_REPORT_NAMES = {REPORT_JSON.name, REPORT_MD.name}
STALE_EXCLUDED_REL_PATHS = {
    "topics.md",
    "data/visual_coverage.md",
    "data/narrative_validation_report.md",
}

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"""href=["']([^"']+)["']""")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
TAG_HEADING_RE = re.compile(r"^##\s+`([^`]+)`\s*$", re.MULTILINE)

STALE_PATTERN = re.compile(
    r"\b("
    r"latest|current(?:ly)?|today|now|recent(?:ly)?|new|emerging|"
    r"preview|beta|roadmap|pricing|generally available|GA|"
    r"as of|last month|this month|next year|fast-changing|fast moving"
    r")\b|"
    r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|"
    r"Dec(?:ember)?)\s+\d{1,2},?\s+20\d{2}\b|"
    r"\b\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|"
    r"May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|"
    r"Nov(?:ember)?|Dec(?:ember)?)\s+20\d{2}\b",
    re.IGNORECASE,
)
STALE_CAVEAT_RE = re.compile(
    r"\b("
    r"snapshot|point-in-time|source status|recheck|re-check|verify|validated|"
    r"before live use|access date|as of|dated|caveat|not yet safe|"
    r"secondary claims|publication status|confidence"
    r")\b",
    re.IGNORECASE,
)
CLAIM_STRIP_RE = re.compile(
    r"^[-*]\s+|^\|.*\|$|^#{1,6}\s+|^tags:\s*$|^\s+-\s+\w[\w-]*\s*$",
    re.MULTILINE,
)

FINDING_LEVELS = ("error", "warning", "info")


@dataclass(frozen=True)
class Finding:
    check: str
    level: str
    message: str
    path: str | None = None
    line: int | None = None
    detail: str | None = None

    def to_json(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "check": self.check,
            "level": self.level,
            "message": self.message,
        }
        if self.path:
            payload["path"] = self.path
        if self.line is not None:
            payload["line"] = self.line
        if self.detail:
            payload["detail"] = self.detail
        return payload


@dataclass(frozen=True)
class ExternalLink:
    source_path: Path
    line: int
    url: str


@dataclass
class LinkResult:
    url: str
    status: str
    status_code: int | None
    source_count: int
    sample_sources: list[str] = field(default_factory=list)
    detail: str | None = None


@dataclass(frozen=True)
class ConceptRequirement:
    concept: str
    paths: tuple[str, ...] = ()
    topic_terms: tuple[str, ...] = ()
    body_terms: tuple[str, ...] = ()


CONCEPT_REQUIREMENTS: tuple[ConceptRequirement, ...] = (
    ConceptRequirement(
        "AI coding assistants market context",
        paths=("notes/ai-coding-assistants-market-briefing.md",),
        topic_terms=("ai-assistants",),
        body_terms=("AI Coding Assistants",),
    ),
    ConceptRequirement(
        "productivity evidence",
        paths=("notes/ai-coding-assistants-productivity-evidence.md",),
        topic_terms=("productivity",),
        body_terms=("productivity",),
    ),
    ConceptRequirement(
        "failure modes",
        paths=("notes/ai-coding-assistants-failure-modes.md",),
        topic_terms=("risk-boundaries",),
        body_terms=("failure",),
    ),
    ConceptRequirement(
        "public-sector controls",
        paths=("notes/ai-coding-assistants-public-sector-controls.md",),
        topic_terms=("public-sector", "governance"),
        body_terms=("public-sector", "controls"),
    ),
    ConceptRequirement(
        "Challenge 2 worked example",
        paths=("notes/challenge-2-worked-example.md",),
        topic_terms=("challenge-2", "dark-data"),
        body_terms=("Challenge 2",),
    ),
    ConceptRequirement(
        "source-backed answers and provenance",
        paths=("notes/challenge-2-worked-example.md",),
        topic_terms=("provenance", "source-backed-answers"),
        body_terms=("source-backed", "provenance"),
    ),
    ConceptRequirement(
        "validation and evaluation",
        paths=("notes/ai-coding-assistants-source-register.md",),
        topic_terms=("validation", "evaluation"),
        body_terms=("validation", "evaluation"),
    ),
    ConceptRequirement(
        "talk arc",
        paths=("narrative-arc.md", "notes/ai-coding-assistants-talk-track.md"),
        topic_terms=("talk-demo",),
        body_terms=("talk",),
    ),
    ConceptRequirement(
        "Q&A prep",
        paths=("notes/ai-coding-assistants-q-and-a.md",),
        topic_terms=("q-and-a",),
        body_terms=("Q&A",),
    ),
    ConceptRequirement(
        "SeeLinks navigation datapack",
        paths=("seelinks/README.md", "notes/seelinks-web-ui-reference.md"),
        topic_terms=("seelinks",),
        body_terms=("SeeLinks",),
    ),
    ConceptRequirement(
        "MCP tooling",
        paths=("notes/challenge-2-worked-example.md",),
        topic_terms=("mcp", "tooling"),
        body_terms=("MCP",),
    ),
    ConceptRequirement(
        "ClawPilot and agentic workplace signal",
        paths=("notes/clawpilot-project-lobster.md",),
        topic_terms=("clawpilot",),
        body_terms=("ClawPilot", "Project Lobster"),
    ),
    ConceptRequirement(
        "audio transcript inputs",
        paths=("notes/engineering-accountability-audio.md", "notes/governing-agentic-ai-audio.md"),
        topic_terms=("transcripts",),
        body_terms=("transcript",),
    ),
    ConceptRequirement(
        "navigation scope and dead-end policy",
        paths=("notes/navigation-and-scope.md",),
        topic_terms=("navigation",),
        body_terms=("dead end", "navigation"),
    ),
)


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def narrative_rel(path: Path) -> str:
    return path.resolve().relative_to(NARRATIVE_DIR).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_files() -> list[Path]:
    files = sorted(NARRATIVE_DIR.rglob("*.md"))
    return [path for path in files if path.name not in SEMANTIC_REPORT_NAMES]


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def strip_code_blocks(text: str) -> str:
    return CODE_BLOCK_RE.sub("", text)


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def extract_frontmatter_tags(text: str) -> set[str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return set()
    tags: set[str] = set()
    in_tags = False
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped == "tags:":
            in_tags = True
            continue
        if in_tags:
            if stripped.startswith("- "):
                tags.add(stripped[2:].strip().strip('"').strip("'"))
                continue
            if stripped and not line.startswith(" "):
                in_tags = False
    return {tag for tag in tags if tag}


def extract_external_links(path: Path, text: str) -> list[ExternalLink]:
    links: list[ExternalLink] = []
    for regex in (MARKDOWN_LINK_RE, HTML_LINK_RE):
        for match in regex.finditer(text):
            target = match.group(1).strip()
            target = target.split()[0].strip("<>")
            if target.startswith(("http://", "https://")):
                links.append(ExternalLink(path, line_number(text, match.start(1)), target))
    return links


def split_paragraphs(text: str) -> list[tuple[int, str]]:
    paragraphs: list[tuple[int, str]] = []
    current: list[str] = []
    start_line = 1
    for index, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            if current:
                paragraphs.append((start_line, "\n".join(current)))
                current = []
            start_line = index + 1
            continue
        if not current:
            start_line = index
        current.append(line)
    if current:
        paragraphs.append((start_line, "\n".join(current)))
    return paragraphs


def paragraph_window_has_caveat(paragraphs: list[tuple[int, str]], index: int, file_has_caveat: bool) -> bool:
    if file_has_caveat:
        return True
    start = max(0, index - 1)
    end = min(len(paragraphs), index + 2)
    window = "\n".join(text for _, text in paragraphs[start:end])
    return bool(STALE_CAVEAT_RE.search(window))


def extract_stale_claim_findings(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[str, int, str]] = set()
    for path in files:
        if narrative_rel(path) in STALE_EXCLUDED_REL_PATHS:
            continue
        text = read_text(path)
        body = strip_code_blocks(strip_frontmatter(text))
        file_has_caveat = bool(STALE_CAVEAT_RE.search(body)) or "## Caveats" in body
        paragraphs = split_paragraphs(body)
        for index, (start_line, paragraph) in enumerate(paragraphs):
            if not STALE_PATTERN.search(paragraph):
                continue
            cleaned = " ".join(CLAIM_STRIP_RE.sub("", paragraph).split())
            if len(cleaned) < 36:
                continue
            snippet = cleaned[:260]
            key = (rel(path), start_line, snippet)
            if key in seen:
                continue
            seen.add(key)
            has_caveat = paragraph_window_has_caveat(paragraphs, index, file_has_caveat)
            level = "info" if has_caveat else "warning"
            message = (
                "Stale-sensitive claim has an explicit caveat or source-status marker"
                if has_caveat
                else "Stale-sensitive claim should get an explicit source date or recheck caveat"
            )
            findings.append(
                Finding(
                    check="stale_claim",
                    level=level,
                    message=message,
                    path=rel(path),
                    line=start_line,
                    detail=snippet,
                )
            )
    return findings


def parse_pack_counts() -> dict[str, int]:
    pack_path = NARRATIVE_DIR / "seelinks" / "pack.json"
    if not pack_path.exists():
        return {}
    data = json.loads(read_text(pack_path))
    graph = data.get("graph", {})
    nodes = graph.get("nodes", []) if isinstance(graph, dict) else data.get("nodes", [])
    edges = graph.get("edges", []) if isinstance(graph, dict) else data.get("edges", [])
    return {
        "items": len(data.get("items", [])),
        "facets": len(data.get("facets", data.get("properties", []))),
        "collections": len(data.get("collections", [])),
        "graph_nodes": len(nodes),
        "graph_edges": len(edges),
    }


def parse_report_counts() -> dict[str, int]:
    report_path = NARRATIVE_DIR / "data" / "narrative_validation_report.json"
    if not report_path.exists():
        return {}
    data = json.loads(read_text(report_path))
    counts = data.get("counts", {})
    return {key: int(value) for key, value in counts.items() if isinstance(value, int)}


def extract_counts_from_text(files: list[Path]) -> dict[str, list[tuple[Path, int, int]]]:
    patterns: tuple[tuple[str, re.Pattern[str]], ...] = (
        (
            "ai_native_blueprint_slides",
            re.compile(r"AI-Native_Engineering_Blueprint\.pptx`?\s+contains\s+(\d+)\s+slides", re.I),
        ),
        ("visual_items", re.compile(r"\b(?:Total|Covered)\s*:\s*(\d+)\s+visual items\b", re.I)),
        ("sidecar_count", re.compile(r"\b(\d+)\s+Markdown sidecars\b", re.I)),
        ("asset_count", re.compile(r"\b(\d+)\s+(?:small )?derived image assets\b", re.I)),
        ("import_files", re.compile(r"\bAll\s+(\d+)\s+current top-level import files\b", re.I)),
        (
            "seelinks_summary",
            re.compile(
                r"contains\s+(\d+)\s+items,\s+(\d+)\s+facets,\s+(\d+)\s+collections,\s+"
                r"(\d+)\s+graph nodes,\s+and\s+(\d+)\s+graph edges",
                re.I,
            ),
        ),
    )
    counts: dict[str, list[tuple[Path, int, int]]] = {}
    for path in files:
        text = read_text(path)
        for key, pattern in patterns:
            for match in pattern.finditer(text):
                if key == "seelinks_summary":
                    keys = ("items", "facets", "collections", "graph_nodes", "graph_edges")
                    for offset, subkey in enumerate(keys, start=1):
                        counts.setdefault(f"seelinks_{subkey}", []).append(
                            (path, line_number(text, match.start(offset)), int(match.group(offset)))
                        )
                    continue
                counts.setdefault(key, []).append(
                    (path, line_number(text, match.start(1)), int(match.group(1)))
                )
    return counts


def actual_import_count() -> int:
    if not IMPORT_DIR.exists():
        return 0
    return len(
        [
            path
            for path in IMPORT_DIR.iterdir()
            if not path.name.startswith(".") and not path.name.startswith("~$")
        ]
    )


def actual_markdown_count() -> int:
    return len(sorted(NARRATIVE_DIR.rglob("*.md")))


def actual_visual_sidecar_count() -> int:
    return len(
        [
            path
            for path in (NARRATIVE_DIR / "slides").rglob("*.md")
            if path.name != "index.md" and path.name != "narrative-guide.md"
        ]
    )


def actual_asset_count() -> int:
    return len([path for path in (NARRATIVE_DIR / "assets" / "visuals").rglob("*") if path.is_file()])


def contradiction_findings(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    observed = extract_counts_from_text(files)
    validation_counts = parse_report_counts()
    pack_counts = parse_pack_counts()

    expected: dict[str, int] = {
        "ai_native_blueprint_slides": len(
            list((NARRATIVE_DIR / "slides" / "ai-native-engineering-blueprint").glob("slide-*.md"))
        ),
        "import_files": actual_import_count(),
        "sidecar_count": actual_visual_sidecar_count(),
        "asset_count": actual_asset_count(),
    }
    if "visual_items" in validation_counts:
        expected["visual_items"] = validation_counts["visual_items"]
    for key, value in pack_counts.items():
        expected[f"seelinks_{key}"] = value

    for key, entries in observed.items():
        observed_values = {value for _, _, value in entries}
        if len(observed_values) > 1:
            sample = "; ".join(f"{rel(path)}:{line}={value}" for path, line, value in entries[:8])
            findings.append(
                Finding(
                    check="contradiction",
                    level="error",
                    message=f"Conflicting documented counts for {key}",
                    detail=sample,
                )
            )
        if key in expected:
            expected_value = expected[key]
            for path, line, value in entries:
                if value != expected_value:
                    findings.append(
                        Finding(
                            check="contradiction",
                            level="error",
                            message=f"Documented {key} count is {value}, expected {expected_value}",
                            path=rel(path),
                            line=line,
                        )
                    )

    report_markdown_count = validation_counts.get("markdown_files")
    if report_markdown_count is not None and report_markdown_count != actual_markdown_count():
        findings.append(
            Finding(
                check="contradiction",
                level="warning",
                message=(
                    "Structural validation report Markdown count is stale after semantic report generation; "
                    "rerun validate_narrative_sidecars.py --write-report"
                ),
                path=rel(NARRATIVE_DIR / "data" / "narrative_validation_report.json"),
                detail=f"report={report_markdown_count}; actual={actual_markdown_count()}",
            )
        )

    if not findings:
        findings.append(
            Finding(
                check="contradiction",
                level="info",
                message="No contradictory tracked counts found",
            )
        )
    return findings


def topic_tags() -> set[str]:
    topics_path = NARRATIVE_DIR / "topics.md"
    if not topics_path.exists():
        return set()
    return set(TAG_HEADING_RE.findall(read_text(topics_path)))


def missing_concept_findings(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    all_text = "\n".join(read_text(path) for path in files)
    topics = topic_tags()
    existing_rel_paths = {narrative_rel(path) for path in files}

    for requirement in CONCEPT_REQUIREMENTS:
        missing_paths = [path for path in requirement.paths if path not in existing_rel_paths]
        missing_topics = [tag for tag in requirement.topic_terms if tag not in topics]
        missing_terms = [
            term for term in requirement.body_terms if not re.search(re.escape(term), all_text, re.IGNORECASE)
        ]
        if missing_paths or missing_topics or missing_terms:
            findings.append(
                Finding(
                    check="missing_concept",
                    level="error",
                    message=f"Required concept is not fully represented: {requirement.concept}",
                    detail=(
                        f"missing_paths={missing_paths}; "
                        f"missing_topic_tags={missing_topics}; missing_terms={missing_terms}"
                    ),
                )
            )

    orphan_tags: list[str] = []
    for path in files:
        tags = extract_frontmatter_tags(read_text(path))
        for tag in tags:
            if tag not in topics:
                orphan_tags.append(f"{tag} ({rel(path)})")
    if orphan_tags:
        findings.append(
            Finding(
                check="missing_concept",
                level="warning",
                message="Some frontmatter tags are not listed as topic headings",
                detail="; ".join(orphan_tags[:30]),
            )
        )

    if not findings:
        findings.append(
            Finding(
                check="missing_concept",
                level="info",
                message="All required narrative concepts and indexed tags are represented",
            )
        )
    return findings


def request_url(url: str, method: str, timeout: float) -> tuple[int | None, bytes, str | None]:
    request = urllib.request.Request(
        url,
        method=method,
        headers={
            "User-Agent": "hmrc-narrative-link-check/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml,text/plain,*/*",
        },
    )
    context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            body = response.read(2_000_000) if method == "GET" else b""
            return response.status, body, None
    except urllib.error.HTTPError as exc:
        if method == "HEAD" and exc.code in {403, 405, 429}:
            return exc.code, b"", None
        try:
            body = exc.read(2_000_000) if method == "GET" else b""
        except Exception:
            body = b""
        return exc.code, body, str(exc.reason)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, b"", str(exc)


def fetch_url(url: str, timeout: float) -> tuple[int | None, bytes, str | None]:
    status, body, detail = request_url(url, "HEAD", timeout)
    if status is not None and status not in {403, 405, 429}:
        return status, body, detail
    return request_url(url, "GET", timeout)


def github_raw_url(url: str) -> tuple[str, int | None] | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.lower() != "github.com":
        return None
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 5 or parts[2] != "blob":
        return None
    owner, repo, _, ref, *file_parts = parts
    raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{'/'.join(file_parts)}"
    line = None
    line_match = re.match(r"L(\d+)(?:-L(\d+))?$", parsed.fragment)
    if line_match:
        line = int(line_match.group(2) or line_match.group(1))
    return raw, line


def classify_link_status(status_code: int | None, detail: str | None) -> str:
    if status_code is None:
        return "warning"
    if 200 <= status_code < 400:
        return "ok"
    if status_code in {401, 403, 405, 429}:
        return "warning"
    if status_code in {404, 410}:
        return "error"
    if status_code >= 500:
        return "warning"
    if detail:
        return "warning"
    return "error"


def validate_github_line(url: str, timeout: float) -> tuple[str, int | None, str | None]:
    raw = github_raw_url(url)
    if raw is None:
        status_code, _, detail = fetch_url(url, timeout)
        return classify_link_status(status_code, detail), status_code, detail

    raw_url, expected_line = raw
    status_code, body, detail = fetch_url(raw_url, timeout)
    status = classify_link_status(status_code, detail)
    if status != "ok" or expected_line is None:
        return status, status_code, detail
    line_count = len(body.decode("utf-8", errors="replace").splitlines())
    if expected_line > line_count:
        return "error", status_code, f"line anchor L{expected_line} exceeds {line_count} lines"
    return "ok", status_code, f"GitHub blob and L{expected_line} line anchor resolved"


def external_link_results(files: list[Path], *, check_external: bool, timeout: float) -> list[LinkResult]:
    links: list[ExternalLink] = []
    for path in files:
        links.extend(extract_external_links(path, read_text(path)))

    by_url: dict[str, list[ExternalLink]] = {}
    for link in links:
        by_url.setdefault(link.url, []).append(link)

    results: list[LinkResult] = []
    for url, occurrences in sorted(by_url.items()):
        samples = [f"{rel(link.source_path)}:{link.line}" for link in occurrences[:5]]
        if not check_external:
            results.append(
                LinkResult(
                    url=url,
                    status="skipped",
                    status_code=None,
                    source_count=len(occurrences),
                    sample_sources=samples,
                    detail="run with --check-external for live validation",
                )
            )
            continue
        status, status_code, detail = validate_github_line(url, timeout)
        results.append(
            LinkResult(
                url=url,
                status=status,
                status_code=status_code,
                source_count=len(occurrences),
                sample_sources=samples,
                detail=detail,
            )
        )
    return results


def external_link_findings(results: list[LinkResult]) -> list[Finding]:
    findings: list[Finding] = []
    for result in results:
        if result.status == "error":
            findings.append(
                Finding(
                    check="external_link",
                    level="error",
                    message=f"External link failed live validation: {result.url}",
                    detail=f"status={result.status_code}; sources={result.sample_sources}; {result.detail or ''}",
                )
            )
        elif result.status == "warning":
            findings.append(
                Finding(
                    check="external_link",
                    level="warning",
                    message=f"External link could not be fully confirmed: {result.url}",
                    detail=f"status={result.status_code}; sources={result.sample_sources}; {result.detail or ''}",
                )
            )
    if not findings:
        checked = len([result for result in results if result.status != "skipped"])
        skipped = len([result for result in results if result.status == "skipped"])
        if checked:
            message = f"All {checked} unique external links passed live validation"
        else:
            message = f"External link validation skipped for {skipped} unique links"
        findings.append(Finding(check="external_link", level="info", message=message))
    return findings


def report_summary(findings: list[Finding], link_results: list[LinkResult]) -> dict[str, Any]:
    counts = {level: 0 for level in FINDING_LEVELS}
    by_check: dict[str, dict[str, int]] = {}
    for finding in findings:
        counts[finding.level] = counts.get(finding.level, 0) + 1
        by_check.setdefault(finding.check, {level: 0 for level in FINDING_LEVELS})
        by_check[finding.check][finding.level] = by_check[finding.check].get(finding.level, 0) + 1
    link_counts: dict[str, int] = {}
    for result in link_results:
        link_counts[result.status] = link_counts.get(result.status, 0) + 1
    return {
        "status": "failed" if counts.get("error", 0) else "passed",
        "counts": counts,
        "by_check": by_check,
        "external_link_status_counts": link_counts,
    }


def write_json_report(payload: dict[str, Any]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def md_path_link(path: str | None, line: int | None = None) -> str:
    if not path:
        return ""
    target = os.path.relpath(REPO_ROOT / path, REPORT_MD.parent)
    suffix = f"#L{line}" if line is not None else ""
    return f"[{path}{':' + str(line) if line is not None else ''}]({target}{suffix})"


def escape_report_detail(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("[", "&#91;")
        .replace("]", "&#93;")
        .replace("|", "\\|")
    )


def write_markdown_report(payload: dict[str, Any]) -> None:
    findings = [Finding(**finding) for finding in payload["findings"]]
    link_results = [LinkResult(**result) for result in payload["external_links"]]
    summary = payload["summary"]
    lines = [
        "# Narrative Semantic Lint Report",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        f"Status: **{summary['status']}**",
        "",
        "## Summary",
        "",
        f"- Errors: `{summary['counts'].get('error', 0)}`",
        f"- Warnings: `{summary['counts'].get('warning', 0)}`",
        f"- Info findings: `{summary['counts'].get('info', 0)}`",
        f"- Unique external links: `{len(link_results)}`",
        f"- External link statuses: `{summary['external_link_status_counts']}`",
        "",
        "## Checks",
        "",
        "- Stale-claim detection flags temporal, product-state, pricing, roadmap, preview, and date-sensitive claims; source-status caveats downgrade findings to informational review items.",
        "- Contradiction detection compares documented counts for visual items, sidecars, imports, Markdown files, and SeeLinks datapack counts against generated artifacts.",
        "- Missing-concept detection checks the required talk concepts, topic tags, and section-level narrative pages.",
        "- External-link revalidation performs live HTTP checks and verifies GitHub blob line anchors where applicable.",
        "",
        "## Findings",
        "",
    ]
    for finding in findings:
        location = md_path_link(finding.path, finding.line)
        detail = f" Detail: {escape_report_detail(finding.detail)}" if finding.detail else ""
        location_text = f" {location}" if location else ""
        lines.append(
            f"- `{finding.level}` `{finding.check}`: {finding.message}{location_text}.{detail}".rstrip()
        )

    lines.extend(["", "## External Links", ""])
    if link_results:
        lines.extend(["| Status | Code | URL | Sources | Detail |", "| --- | ---: | --- | --- | --- |"])
        for result in link_results:
            code = "" if result.status_code is None else str(result.status_code)
            sources = "<br>".join(result.sample_sources)
            detail = (result.detail or "").replace("|", "\\|")
            url = result.url.replace("|", "%7C")
            lines.append(f"| {result.status} | {code} | {url} | {sources} | {detail} |")
    else:
        lines.append("No external links found in the narrative Markdown scope.")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def build_payload(*, check_external: bool, timeout: float) -> dict[str, Any]:
    files = markdown_files()
    stale_findings = extract_stale_claim_findings(files)
    count_findings = contradiction_findings(files)
    concept_findings = missing_concept_findings(files)
    link_results = external_link_results(files, check_external=check_external, timeout=timeout)
    link_findings = external_link_findings(link_results)
    findings = stale_findings + count_findings + concept_findings + link_findings
    payload = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "scope": rel(NARRATIVE_DIR),
        "markdown_files_checked": len(files),
        "external_checks_live": check_external,
        "summary": report_summary(findings, link_results),
        "findings": [finding.to_json() for finding in findings],
        "external_links": [
            {
                "url": result.url,
                "status": result.status,
                "status_code": result.status_code,
                "source_count": result.source_count,
                "sample_sources": result.sample_sources,
                "detail": result.detail,
            }
            for result in link_results
        ],
    }
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true", help="Write JSON and Markdown reports.")
    parser.add_argument("--check-external", action="store_true", help="Perform live external URL checks.")
    parser.add_argument("--timeout", type=float, default=12.0, help="HTTP timeout per request in seconds.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_payload(check_external=args.check_external, timeout=args.timeout)
    if args.write_report:
        write_json_report(payload)
        write_markdown_report(payload)
    summary = payload["summary"]
    print(
        "Narrative semantic lint "
        f"{summary['status']}: "
        f"{summary['counts'].get('error', 0)} error(s), "
        f"{summary['counts'].get('warning', 0)} warning(s), "
        f"{summary['counts'].get('info', 0)} info finding(s); "
        f"external links {summary['external_link_status_counts']}"
    )
    return 1 if summary["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
