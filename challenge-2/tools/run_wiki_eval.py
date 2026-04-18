#!/usr/bin/env python3
"""Run Challenge 2 wiki evaluation questions through CLI AI clients."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


CHALLENGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = CHALLENGE_ROOT.parent
sys.path.insert(0, str(CHALLENGE_ROOT))

from evaluation.audit import ChallengeAuditRecorder, sha256_file  # noqa: E402
from evaluation.clients import (  # noqa: E402
    ClientCommandContext,
    DEFAULT_CLIENTS,
    FULL_COVERAGE_CLIENTS,
    SUPPORTED_CLIENTS,
    build_wiki_prompt,
    describe_client,
    describe_desktop_ai_apps,
    load_client_config,
    run_client,
)
from evaluation.questions import BENCHMARK_PATH, load_questions, select_questions  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", type=Path, default=BENCHMARK_PATH, help="Benchmark Markdown path.")
    parser.add_argument(
        "--clients",
        default=",".join(DEFAULT_CLIENTS),
        help=f"Comma-separated clients to run, or 'default'/'full'. Supported: {', '.join(SUPPORTED_CLIENTS)}.",
    )
    parser.add_argument("--questions", help="Comma-separated question IDs, for example Q001,Q002.")
    parser.add_argument("--category", help="Category substring filter.")
    parser.add_argument("--limit", type=int, help="Limit the number of selected questions.")
    parser.add_argument("--output-root", type=Path, default=CHALLENGE_ROOT / "evaluation" / "runs")
    parser.add_argument("--run-id", help="Explicit run id. Defaults to a UTC timestamp.")
    parser.add_argument("--timeout-sec", type=int, default=600)
    parser.add_argument("--dry-run", action="store_true", help="Write prompts and audit skeleton without invoking clients.")
    parser.add_argument("--client-config", type=Path, help="Optional JSON file overriding client argv templates.")
    parser.add_argument(
        "--model",
        action="append",
        default=[],
        metavar="CLIENT=MODEL",
        help="Override a client model. May be repeated.",
    )
    args = parser.parse_args(argv)

    clients = _parse_clients(args.clients)
    model_overrides = _parse_model_overrides(args.model)
    questions = load_questions(args.benchmark)
    selected = select_questions(
        questions,
        question_ids=_split_csv(args.questions),
        category=args.category,
        limit=args.limit,
    )
    if not selected:
        raise SystemExit("No questions selected.")

    run_id = args.run_id or f"wiki-eval-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    run_dir = args.output_root / run_id
    client_config = load_client_config(args.client_config)
    client_manifests = {
        client: describe_client(client, model_override=model_overrides.get(client), config=client_config)
        for client in clients
    }
    recorder = ChallengeAuditRecorder(
        run_dir,
        run_id=run_id,
        repo_root=REPO_ROOT,
        challenge_root=CHALLENGE_ROOT,
    )
    recorder.start_run(
        questions=selected,
        clients=clients,
        dry_run=args.dry_run,
        metadata={
            "benchmark": str(args.benchmark),
            "benchmark_sha256": sha256_file(args.benchmark),
            "timeout_sec": args.timeout_sec,
            "client_config": str(args.client_config) if args.client_config else None,
            "repo_state": _repo_state(REPO_ROOT),
            "client_manifests": client_manifests,
            "desktop_ai_apps": describe_desktop_ai_apps(),
        },
    )

    for question in selected:
        for client in clients:
            prompt = build_wiki_prompt(question, repo_root=REPO_ROOT, challenge_root=CHALLENGE_ROOT)
            prompt_path = recorder.write_prompt(client, question, prompt)
            assistant_response_path = run_dir / "raw" / client / f"{question.question_id}.assistant-response.txt"
            context = ClientCommandContext(
                client=client,
                model=model_overrides.get(client),
                prompt=prompt,
                question_id=question.question_id,
                run_dir=run_dir,
                repo_root=REPO_ROOT,
                challenge_root=CHALLENGE_ROOT,
                assistant_response_path=assistant_response_path,
                client_manifest=client_manifests.get(client),
            )
            result = run_client(
                context=context,
                prompt_path=prompt_path,
                config=client_config,
                timeout_sec=args.timeout_sec,
                dry_run=args.dry_run,
            )
            recorder.record_answer(question, result)
            print(
                json.dumps(
                    {
                        "run_id": run_id,
                        "client": client,
                        "question_id": question.question_id,
                        "model": result.model,
                        "status": result.status,
                        "exit_code": result.exit_code,
                    },
                    sort_keys=True,
                )
            )

    final = recorder.finalize()
    print(json.dumps({"run_dir": str(run_dir), "audit_card": final["audit_card"]}, sort_keys=True))
    return 0


def _parse_clients(raw: str) -> list[str]:
    if raw.strip().lower() == "default":
        return list(DEFAULT_CLIENTS)
    if raw.strip().lower() == "full":
        return list(FULL_COVERAGE_CLIENTS)
    clients = _split_csv(raw)
    if not clients:
        raise SystemExit("At least one client is required.")
    unsupported = sorted(set(clients) - set(SUPPORTED_CLIENTS))
    if unsupported:
        raise SystemExit(f"Unsupported client(s): {', '.join(unsupported)}")
    return clients


def _parse_model_overrides(values: list[str]) -> dict[str, str]:
    overrides: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Invalid --model value {value!r}; expected CLIENT=MODEL")
        client, model = value.split("=", 1)
        client = client.strip()
        if client not in SUPPORTED_CLIENTS:
            raise SystemExit(f"Unsupported --model client: {client}")
        if not model.strip():
            raise SystemExit(f"Invalid --model value {value!r}; model cannot be empty")
        overrides[client] = model.strip()
    return overrides


def _split_csv(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _repo_state(repo_root: Path) -> dict[str, object]:
    status = _git(repo_root, "status", "--short")
    return {
        "commit": _git(repo_root, "rev-parse", "HEAD"),
        "branch": _git(repo_root, "rev-parse", "--abbrev-ref", "HEAD"),
        "tags_at_head": _split_lines(_git(repo_root, "tag", "--points-at", "HEAD")),
        "dirty": bool(status.strip()),
        "status_short": status,
    }


def _git(repo_root: Path, *args: str) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        return "<timeout>"
    if proc.returncode != 0:
        return (proc.stderr or proc.stdout or "").strip()
    return proc.stdout.strip()


def _split_lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


if __name__ == "__main__":
    raise SystemExit(main())
