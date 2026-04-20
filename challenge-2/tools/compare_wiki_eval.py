#!/usr/bin/env python3
"""Compare Challenge 2 wiki evaluation runs and write a reproducible report."""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


CHALLENGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = CHALLENGE_ROOT.parent
sys.path.insert(0, str(CHALLENGE_ROOT))

from evaluation.scoring import summarise_scores  # noqa: E402


SOURCE_ID_RE = re.compile(r"\b(?:DOC-[A-Z0-9-]+|UF-[A-Z0-9-]+)\b")
WIKI_PATH_RE = re.compile(r"\bchallenge-2/(?:AGENTS\.md|wiki/[^\s\]\)\"'<>`,;:]*)")
LOCAL_ABSOLUTE_PATH_ROOTS = (
    "Applications",
    "Library",
    "System",
    "Users",
    "Volumes",
    "bin",
    "dev",
    "etc",
    "home",
    "mnt",
    "nix",
    "opt",
    "private",
    "run",
    "sbin",
    "tmp",
    "usr",
    "var",
)
LOCAL_ABSOLUTE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9+.-]:)"
    r"(?<![A-Za-z0-9_~<>./-])"
    r"/(?:" + "|".join(re.escape(root) for root in LOCAL_ABSOLUTE_PATH_ROOTS) + r")"
    r"(?=/|$)"
    r"(?:/[^\s\]\)\"'<>`,;]*)*"
)
HOME_RELATIVE_PATH_RE = re.compile(r"~/(?:[^\s\]\)\"'<>`,;]*)+")


@dataclass
class ParsedAnswer:
    raw: dict[str, Any]
    visible_json: dict[str, Any] | None
    run_dir: Path

    @property
    def client(self) -> str:
        return str(self.raw.get("client") or "")

    @property
    def question_id(self) -> str:
        return str(self.raw.get("question_id") or "")

    @property
    def status(self) -> str:
        return str(self.raw.get("status") or "")

    @property
    def elapsed(self) -> float:
        return float(self.raw.get("elapsed_seconds") or 0.0)

    @property
    def answer_text(self) -> str:
        if self.visible_json:
            return str(self.visible_json.get("answer") or "")
        return str(self.raw.get("answer_text") or "")

    @property
    def cited_sources(self) -> list[str]:
        if self.visible_json and isinstance(self.visible_json.get("cited_sources"), list):
            return [str(item) for item in self.visible_json["cited_sources"]]
        return [str(item) for item in self.raw.get("cited_sources") or []]

    @property
    def caveats(self) -> list[str]:
        if self.visible_json and isinstance(self.visible_json.get("caveats"), list):
            return [str(item) for item in self.visible_json["caveats"]]
        return []

    @property
    def gold_refs(self) -> list[str]:
        return [str(item) for item in self.raw.get("gold_source_refs") or []]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Evaluation run directory.")
    parser.add_argument("--output", type=Path, required=True, help="Markdown report path.")
    parser.add_argument("--json-output", type=Path, help="Optional machine-readable metrics path.")
    parser.add_argument(
        "--baseline-client",
        default="codex",
        help="Client used as the baseline for focused comparison.",
    )
    parser.add_argument(
        "--comparison-client",
        default="codex-mcp",
        help="Client compared with the baseline.",
    )
    parser.add_argument(
        "--smoke-run",
        action="append",
        default=[],
        help="Optional CLIENT=RUN_DIR smoke run evidence, may be repeated.",
    )
    parser.add_argument(
        "--correction-run",
        action="append",
        default=[],
        help="Optional CLIENT=RUN_DIR correction run used to replace a non-completed base row.",
    )
    parser.add_argument(
        "--score-path",
        type=Path,
        help="Optional rubric-scored CSV used to add a quality leaderboard to the report.",
    )
    args = parser.parse_args(argv)

    answers = load_answers(args.run_dir)
    correction_runs = load_correction_runs(args.correction_run)
    answers, applied_corrections = apply_corrections(answers, correction_runs)
    metrics = build_metrics(args.run_dir, answers)
    metrics["corrections"] = applied_corrections
    if args.score_path:
        metrics["rubric_scores"] = summarise_scores(args.score_path)
    public_metrics = sanitize_public_value(metrics, run_dir=args.run_dir)
    smoke = load_smoke_runs(args.smoke_run)
    report = format_report(
        args.run_dir,
        public_metrics,
        answers,
        baseline_client=args.baseline_client,
        comparison_client=args.comparison_client,
        smoke=smoke,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(public_metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(args.output), "json": str(args.json_output) if args.json_output else None}, sort_keys=True))
    return 0


def load_answers(run_dir: Path) -> list[ParsedAnswer]:
    answers_path = run_dir / "answers.jsonl"
    rows: list[ParsedAnswer] = []
    for line in answers_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        rows.append(
            ParsedAnswer(
                raw=raw,
                visible_json=extract_visible_json(str(raw.get("answer_text") or "")),
                run_dir=run_dir,
            )
        )
    return rows


def extract_visible_json(text: str) -> dict[str, Any] | None:
    """Extract the last visible benchmark JSON object from messy client output."""

    candidates: list[dict[str, Any]] = []
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            obj, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            if "question_id" in obj and ("answer" in obj or "cited_sources" in obj):
                candidates.append(obj)
            for key in ("answer", "result", "response", "text", "content"):
                if isinstance(obj.get(key), str):
                    nested = extract_visible_json(obj[key])
                    if nested:
                        candidates.append(nested)
    return candidates[-1] if candidates else None


def build_metrics(run_dir: Path, answers: list[ParsedAnswer]) -> dict[str, Any]:
    by_client: dict[str, list[ParsedAnswer]] = defaultdict(list)
    for answer in answers:
        by_client[answer.client].append(answer)
    clients: dict[str, Any] = {}
    for client, rows in sorted(by_client.items()):
        effective_statuses = [classified_status(row) for row in rows]
        status_counts = Counter(effective_statuses)
        parseable = [row for row in rows if row.visible_json]
        completed = [row for row, status in zip(rows, effective_statuses, strict=True) if status == "completed"]
        elapsed = [
            row.elapsed
            for row, status in zip(rows, effective_statuses, strict=True)
            if status == "completed" and row.elapsed > 0
        ]
        overlap = [citation_overlap(row) for row in rows]
        clients[client] = {
            "answer_count": len(rows),
            "completed": len(completed),
            "status_counts": dict(sorted(status_counts.items())),
            "parseable_json": len(parseable),
            "parseable_json_percent": pct(len(parseable), len(rows)),
            "avg_elapsed_seconds": round(statistics.mean(elapsed), 3) if elapsed else 0.0,
            "median_elapsed_seconds": round(statistics.median(elapsed), 3) if elapsed else 0.0,
            "avg_answer_chars": round(statistics.mean(len(row.answer_text) for row in rows), 1) if rows else 0.0,
            "citation_overlap": {
                "gold_ref_mentions": sum(item["gold_ref_mentions"] for item in overlap),
                "gold_ref_total": sum(item["gold_ref_total"] for item in overlap),
                "gold_ref_recall_percent": pct(
                    sum(item["gold_ref_mentions"] for item in overlap),
                    sum(item["gold_ref_total"] for item in overlap),
                ),
                "questions_with_any_gold_ref": sum(1 for item in overlap if item["gold_ref_mentions"] > 0),
            },
            "mcp_tool_evidence": mcp_tool_evidence(run_dir, client, rows),
        }
    return {
        "run_dir": str(run_dir),
        "run": read_json(run_dir / "run.json"),
        "audit_card": read_json(run_dir / "audit-card.json"),
        "clients": clients,
    }


def citation_overlap(answer: ParsedAnswer) -> dict[str, int]:
    cited = normalise_refs(answer.cited_sources + [answer.answer_text])
    gold = normalise_refs(answer.gold_refs)
    mentions = sum(1 for ref in gold if ref in cited or any(ref in item or item in ref for item in cited))
    return {"gold_ref_mentions": mentions, "gold_ref_total": len(gold)}


def normalise_refs(values: Iterable[str]) -> set[str]:
    refs: set[str] = set()
    for value in values:
        text = str(value)
        refs.update(match.group(0).upper() for match in SOURCE_ID_RE.finditer(text.upper()))
        refs.update(match.group(0).rstrip(".,;:").casefold() for match in WIKI_PATH_RE.finditer(text))
        if text.startswith("challenge-2/"):
            refs.add(text.rstrip(".,;:").casefold())
    return refs


def classified_status(answer: ParsedAnswer) -> str:
    if answer.status == "failed":
        stderr_path = answer.run_dir / "raw" / answer.client / f"{answer.question_id}.stderr.txt"
        if stderr_path.exists():
            stderr = stderr_path.read_text(encoding="utf-8", errors="replace")
            if answer.client == "gemini" and ("QUOTA_EXHAUSTED" in stderr or "exhausted your capacity" in stderr):
                return "quota_exhausted"
    return answer.status


def mcp_tool_evidence(run_dir: Path, client: str, rows: list[ParsedAnswer]) -> dict[str, Any]:
    raw_dir = run_dir / "raw" / client
    event_counts: Counter[str] = Counter()
    malformed_audit_lines = 0
    stdout_tool_calls = 0
    questions_with_mcp_audit = 0
    for row in rows:
        raw_dir = row.run_dir / "raw" / client
        audit_path = raw_dir / f"{row.question_id}.mcp-audit.jsonl"
        if audit_path.exists() and audit_path.stat().st_size:
            questions_with_mcp_audit += 1
            for line in audit_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    malformed_audit_lines += 1
                    continue
                if isinstance(event, dict):
                    event_counts[str(event.get("event_type") or "")] += 1
                else:
                    malformed_audit_lines += 1
        stdout_path = raw_dir / f"{row.question_id}.stdout.txt"
        if stdout_path.exists():
            stdout_tool_calls += stdout_path.read_text(encoding="utf-8", errors="replace").count('"type":"mcp_tool_call"')
    return {
        "questions_with_mcp_audit": questions_with_mcp_audit,
        "audit_event_counts": dict(sorted(event_counts.items())),
        "malformed_audit_lines": malformed_audit_lines,
        "stdout_mcp_tool_call_events": stdout_tool_calls,
    }


def load_smoke_runs(values: list[str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for value in values:
        if "=" not in value:
            continue
        client, path = value.split("=", 1)
        run_dir = Path(path)
        card = read_json(run_dir / "audit-card.json")
        answers = load_answers(run_dir) if (run_dir / "answers.jsonl").exists() else []
        result[client] = {
            "run_dir": str(run_dir),
            "status_counts": dict(Counter(answer.status for answer in answers)),
            "audit_card": card,
        }
    return result


def load_correction_runs(values: list[str]) -> list[ParsedAnswer]:
    corrections: list[ParsedAnswer] = []
    for value in values:
        if "=" not in value:
            continue
        expected_client, path = value.split("=", 1)
        for answer in load_answers(Path(path)):
            if answer.client == expected_client:
                corrections.append(answer)
    return corrections


def apply_corrections(
    answers: list[ParsedAnswer],
    corrections: list[ParsedAnswer],
) -> tuple[list[ParsedAnswer], list[dict[str, Any]]]:
    by_key = {(answer.client, answer.question_id): index for index, answer in enumerate(answers)}
    effective = list(answers)
    applied: list[dict[str, Any]] = []
    for correction in corrections:
        key = (correction.client, correction.question_id)
        index = by_key.get(key)
        if index is None:
            continue
        original = effective[index]
        if classified_status(original) == "completed" or classified_status(correction) != "completed":
            continue
        effective[index] = correction
        applied.append(
            {
                "client": correction.client,
                "question_id": correction.question_id,
                "base_status": classified_status(original),
                "correction_status": classified_status(correction),
                "correction_run_dir": str(correction.run_dir),
            }
        )
    return effective, applied


def format_report(
    run_dir: Path,
    metrics: dict[str, Any],
    answers: list[ParsedAnswer],
    *,
    baseline_client: str,
    comparison_client: str,
    smoke: dict[str, dict[str, Any]],
) -> str:
    run = metrics.get("run") or {}
    clients = metrics["clients"]
    lines = [
        "# Challenge 2 Wiki Evaluation: MCP Comparison",
        "",
        "## Scope",
        "",
        f"- Run ID: `{run.get('run_id', run_dir.name)}`",
        f"- Raw artifact location: external run directory `{run_dir.name}`; raw prompts and answers are not committed to Git.",
        f"- Questions: `{run.get('question_count', len({answer.question_id for answer in answers}))}`",
        f"- Clients: `{', '.join(clients)}`",
        f"- Repository state: {repo_state_summary(run)}",
        scoring_posture(metrics),
        "- Source policy: Challenge 2 wiki, `wiki/data`, and `challenge-2/AGENTS.md`; benchmark and gold-answer artifacts remain excluded from prompts and MCP tools.",
        "",
        "## Model And Version Provenance",
        "",
    ]
    lines.extend(client_provenance_table(metrics))
    lines.extend(
        [
            "",
            "## Client Summary",
            "",
            "| Client | Answers | Completed | JSON % | Avg completed seconds | Gold-ref recall proxy | MCP audited questions | Statuses |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for client, item in clients.items():
        overlap = item["citation_overlap"]
        mcp = item["mcp_tool_evidence"]
        lines.append(
            "| {client} | {answers} | {completed} | {json_pct} | {avg} | {recall} | {mcp_q} | {statuses} |".format(
                client=client,
                answers=item["answer_count"],
                completed=item["completed"],
                json_pct=item["parseable_json_percent"],
                avg=item["avg_elapsed_seconds"],
                recall=overlap["gold_ref_recall_percent"],
                mcp_q=mcp["questions_with_mcp_audit"],
                statuses=", ".join(f"{key}:{value}" for key, value in item["status_counts"].items()),
            )
        )
    rubric_scores = metrics.get("rubric_scores")
    if isinstance(rubric_scores, dict):
        lines.extend(["", "## Rubric-Scored Quality Leaderboard", ""])
        lines.extend(rubric_leaderboard_table(rubric_scores))
        lines.extend(["", "### Rubric Scoring Method", ""])
        lines.extend(
            [
                "- Scores use the benchmark's human-written `specific_rubric` and gold answer for each question.",
                "- The effective answer set applies the explicit Q057 Codex-with-MCP correction before scoring.",
                "- Each client is scored against the full 500-point benchmark denominator; non-completed, failed, and quota-exhausted rows receive `0`.",
                "- The committed score CSV records per-question scores and notes without committing raw prompts or answer text.",
            ]
        )
    partial = partial_client_notes(clients)
    if partial:
        lines.extend(["", "## Partial Or Blocked Clients", ""])
        lines.extend(partial)
    corrections = metrics.get("corrections") or []
    if corrections:
        lines.extend(["", "## Correction Evidence", ""])
        lines.append("| Client | Question | Base status | Correction status | Correction run |")
        lines.append("| --- | --- | --- | --- | --- |")
        for correction in corrections:
            run_name = str(correction.get("correction_run_dir") or "").rstrip("/").split("/")[-1]
            lines.append(
                "| {client} | {question} | {base} | {status} | `{run}` |".format(
                    client=correction.get("client"),
                    question=correction.get("question_id"),
                    base=correction.get("base_status"),
                    status=correction.get("correction_status"),
                    run=run_name,
                )
            )
    lines.extend(["", "## Codex Versus Codex With MCP", ""])
    baseline = clients.get(baseline_client)
    comparison = clients.get(comparison_client)
    if baseline and comparison:
        lines.extend(compare_clients_text(baseline_client, comparison_client, baseline, comparison))
        if isinstance(rubric_scores, dict):
            lines.extend(rubric_comparison_text(baseline_client, comparison_client, rubric_scores))
        lines.extend(["", "### Per-Question Difference Flags", ""])
        lines.extend(question_delta_table(run_dir, answers, baseline_client, comparison_client))
    else:
        lines.append(f"One or both comparison clients are missing: `{baseline_client}`, `{comparison_client}`.")
    if smoke:
        lines.extend(["", "## Smoke-Test Evidence", ""])
        lines.append("| Client | Run directory | Statuses |")
        lines.append("| --- | --- | --- |")
        for client, item in sorted(smoke.items()):
            statuses = ", ".join(f"{key}:{value}" for key, value in item["status_counts"].items()) or "not recorded"
            lines.append(f"| {client} | `{Path(item['run_dir']).name}` | {statuses} |")
    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- The citation metric remains a recall proxy over source IDs and wiki paths; the rubric-scored leaderboard is the quality signal for answer correctness.",
            "- Microsoft Copilot uses browser UI automation and may include UI chrome or previous chat text in raw captured output; parsed JSON is extracted from visible text where possible.",
            "- GitHub Copilot CLI was excluded from the full validated run if the smoke run remained `policy_blocked`.",
            "- Codex with MCP uses noninteractive approval bypass for the Codex process so MCP tool calls are not cancelled; the MCP server itself is read-only, allowlisted, and benchmark-safe.",
            "- Semantic retrieval is implemented with deterministic exact-cosine local hashing in this run. The production embedding model remains to be locked after a dedicated retrieval benchmark over the shortlisted permissive local models.",
            "",
            "## Next Steps",
            "",
            "- Use independent moderation if this rubric-scored leaderboard is promoted from project evidence to an official comparative claim.",
            "- Run the embedding shortlist benchmark and lock the v1 model only after comparing retrieval quality, disk impact, license posture, and reproducibility.",
            "- Validate the same MCP server through Copilot Studio direct MCP connection; move to Agents Toolkit packaging only if direct connection cannot expose the required tools, resources, or governance controls.",
            "- Improve the Microsoft Copilot adapter by starting a fresh conversation per question and extracting only the final assistant JSON block.",
        ]
    )
    return "\n".join(lines) + "\n"


def scoring_posture(metrics: dict[str, Any]) -> str:
    if isinstance(metrics.get("rubric_scores"), dict):
        return "- Scoring posture: rubric-scored quality leaderboard added from the benchmark's human-written rubrics; automated proxy metrics are retained as secondary operational signals."
    return "- Scoring posture: automated proxy metrics only; no human rubric scores are asserted in this report."


def rubric_leaderboard_table(rubric_scores: dict[str, Any]) -> list[str]:
    leaderboard = rubric_scores.get("leaderboard") or []
    if not isinstance(leaderboard, list) or not leaderboard:
        return ["No rubric score rows were supplied."]
    lines = [
        "| Rank | Client | Scored answers | Raw points | Final % | Scored subset % | Hallucinations | Missed source risks |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for rank, item in enumerate(leaderboard, start=1):
        subset = "" if item.get("scored_subset_percent") is None else item.get("scored_subset_percent")
        lines.append(
            "| {rank} | {client} | {scored} | {points}/{max_points} | {final} | {subset} | {hallucinations} | {risks} |".format(
                rank=rank,
                client=item.get("client"),
                scored=item.get("scored_answers"),
                points=item.get("raw_points"),
                max_points=item.get("benchmark_max_points"),
                final=item.get("final_score_percent"),
                subset=subset,
                hallucinations=item.get("hallucination_count"),
                risks=item.get("missed_source_risk_count"),
            )
        )
    return lines


def rubric_comparison_text(
    baseline_client: str,
    comparison_client: str,
    rubric_scores: dict[str, Any],
) -> list[str]:
    by_client = {
        str(item.get("client")): item
        for item in rubric_scores.get("leaderboard", [])
        if isinstance(item, dict)
    }
    baseline = by_client.get(baseline_client)
    comparison = by_client.get(comparison_client)
    if not baseline or not comparison:
        return []
    return [
        f"- Rubric score: `{baseline_client}` scored `{baseline['raw_points']}/{baseline['benchmark_max_points']}` (`{baseline['final_score_percent']}`%); `{comparison_client}` scored `{comparison['raw_points']}/{comparison['benchmark_max_points']}` (`{comparison['final_score_percent']}`%).",
        f"- Rubric risks: `{baseline_client}` recorded `{baseline['missed_source_risk_count']}` missed-source risks and `{baseline['hallucination_count']}` hallucination flags; `{comparison_client}` recorded `{comparison['missed_source_risk_count']}` missed-source risks and `{comparison['hallucination_count']}` hallucination flags.",
    ]


def sanitize_public_value(value: Any, *, run_dir: Path) -> Any:
    """Remove machine-local absolute paths from committed comparison metrics."""

    if isinstance(value, dict):
        return {str(key): sanitize_public_value(item, run_dir=run_dir) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_public_value(item, run_dir=run_dir) for item in value]
    if not isinstance(value, str):
        return value
    replacements = [
        (str(REPO_ROOT), "<repo-root>"),
        (str(CHALLENGE_ROOT), "<challenge-root>"),
        (str(run_dir), f"<external-run-root>/{run_dir.name}"),
        (str(run_dir.parent), "<external-run-root>"),
        ("/tmp/challenge2-", "<external-tmp>/challenge2-"),
        (str(Path.home()), "~"),
    ]
    result = value
    for raw, replacement in replacements:
        if raw:
            result = result.replace(raw, replacement)
    if is_local_absolute_path(result):
        return "<absolute-path>"
    if result.startswith("~/"):
        return "<home-path>"
    result = LOCAL_ABSOLUTE_PATH_RE.sub("<absolute-path>", result)
    result = HOME_RELATIVE_PATH_RE.sub("<home-path>", result)
    return result


def is_local_absolute_path(value: str) -> bool:
    return any(value == f"/{root}" or value.startswith(f"/{root}/") for root in LOCAL_ABSOLUTE_PATH_ROOTS)


def client_provenance_table(metrics: dict[str, Any]) -> list[str]:
    run = metrics.get("run") or {}
    metadata = run.get("metadata") or {}
    manifests = metadata.get("client_manifests") or {}
    if not manifests:
        return ["No client manifest metadata was recorded for this run."]
    lines = [
        "| Client | Selected model | Selection source | Reasoning | Primary version check |",
        "| --- | --- | --- | --- | --- |",
    ]
    for client, manifest in sorted(manifests.items()):
        model = manifest.get("model") or {}
        version = first_version_check(manifest.get("version_checks") or [])
        lines.append(
            "| {client} | `{model}` | {source} | {effort} | {version} |".format(
                client=client,
                model=model.get("selected_model") or "not recorded",
                source=str(model.get("source") or "not recorded"),
                effort=str(model.get("reasoning_effort") or "not recorded"),
                version=version,
            )
        )
    return lines


def partial_client_notes(clients: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    for client, item in clients.items():
        statuses = item.get("status_counts") or {}
        non_completed = {key: value for key, value in statuses.items() if key != "completed"}
        if not non_completed:
            continue
        detail = ", ".join(f"`{key}`={value}" for key, value in sorted(non_completed.items()))
        if "quota_exhausted" in non_completed:
            notes.append(
                f"- `{client}` became quota-limited during the run ({detail}); completed rows before quota remain retained as evidence, but the client needs a rerun after quota reset for full coverage."
            )
        else:
            notes.append(
                f"- `{client}` did not complete all selected questions ({detail}); inspect raw stderr/stdout in the external run artifacts before treating it as validated."
            )
    return notes


def repo_state_summary(run: dict[str, Any]) -> str:
    repo_state = ((run.get("metadata") or {}).get("repo_state") or {})
    commit = str(repo_state.get("commit") or "not recorded")
    branch = str(repo_state.get("branch") or "not recorded")
    dirty = repo_state.get("dirty")
    if commit and commit != "not recorded":
        commit = commit[:12]
    return f"`{branch}` at `{commit}`, dirty=`{dirty}`"


def first_version_check(version_checks: list[dict[str, Any]]) -> str:
    for check in version_checks:
        if check.get("detected_version"):
            return f"`{check['detected_version']}`"
    for check in version_checks:
        command = " ".join(str(part) for part in check.get("command") or [])
        status = check.get("status") or ("available" if check.get("available") else "missing")
        if command:
            return f"`{command}`: {status}"
    return "not recorded"


def compare_clients_text(
    baseline_name: str,
    comparison_name: str,
    baseline: dict[str, Any],
    comparison: dict[str, Any],
) -> list[str]:
    return [
        f"- `{baseline_name}` completed `{baseline['completed']}` answers; `{comparison_name}` completed `{comparison['completed']}`.",
        f"- `{baseline_name}` average elapsed time was `{baseline['avg_elapsed_seconds']}` seconds; `{comparison_name}` average elapsed time was `{comparison['avg_elapsed_seconds']}` seconds.",
        f"- `{baseline_name}` JSON parseability was `{baseline['parseable_json_percent']}`%; `{comparison_name}` JSON parseability was `{comparison['parseable_json_percent']}`%.",
        f"- `{baseline_name}` gold-reference recall proxy was `{baseline['citation_overlap']['gold_ref_recall_percent']}`%; `{comparison_name}` was `{comparison['citation_overlap']['gold_ref_recall_percent']}`%.",
        f"- `{comparison_name}` recorded MCP audit events for `{comparison['mcp_tool_evidence']['questions_with_mcp_audit']}` questions, with events `{comparison['mcp_tool_evidence']['audit_event_counts']}`.",
    ]


def question_delta_table(
    run_dir: Path,
    answers: list[ParsedAnswer],
    baseline_client: str,
    comparison_client: str,
) -> list[str]:
    by_key = {(answer.client, answer.question_id): answer for answer in answers}
    question_ids = sorted({answer.question_id for answer in answers})
    lines = [
        "| Question | Baseline status | MCP status | Baseline gold refs | MCP gold refs | MCP tool events |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    for question_id in question_ids[:25]:
        baseline = by_key.get((baseline_client, question_id))
        comparison = by_key.get((comparison_client, question_id))
        if not baseline or not comparison:
            continue
        base_overlap = citation_overlap(baseline)
        mcp_overlap = citation_overlap(comparison)
        mcp_events = mcp_event_count(comparison)
        baseline_status = classified_status(baseline)
        comparison_status = classified_status(comparison)
        lines.append(
            f"| {question_id} | {baseline_status} | {comparison_status} | {base_overlap['gold_ref_mentions']}/{base_overlap['gold_ref_total']} | {mcp_overlap['gold_ref_mentions']}/{mcp_overlap['gold_ref_total']} | {mcp_events} |"
        )
    if len(question_ids) > 25:
        lines.append(f"| ... | First 25 of {len(question_ids)} questions shown |  |  |  |  |")
    return lines


def mcp_event_count(answer: ParsedAnswer) -> int:
    path = answer.run_dir / "raw" / answer.client / f"{answer.question_id}.mcp-audit.jsonl"
    if not path.exists():
        return 0
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        count += 1
    return count


def pct(numerator: int, denominator: int) -> float:
    return round((numerator / denominator) * 100, 1) if denominator else 0.0


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
