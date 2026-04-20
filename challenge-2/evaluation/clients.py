"""Client command helpers for the Challenge 2 wiki evaluation harness."""

from __future__ import annotations

import json
import os
import platform
import plistlib
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .audit import ClientRunResult, utc_now
from .questions import EvaluationQuestion


SUPPORTED_CLIENTS = ("codex", "codex-mcp", "gemini", "claude", "github-copilot", "microsoft-copilot")
DEFAULT_CLIENTS = ("codex", "gemini", "claude")
FULL_COVERAGE_CLIENTS = SUPPORTED_CLIENTS

MODEL_ENV_VARS = {
    "codex": ("CODEX_MODEL",),
    "codex-mcp": ("CODEX_MODEL",),
    "gemini": ("GEMINI_MODEL",),
    "claude": ("CLAUDE_MODEL", "ANTHROPIC_MODEL"),
    "github-copilot": ("COPILOT_MODEL",),
    "microsoft-copilot": (),
}

MODEL_EFFORT_ENV_VARS = {
    "codex": ("CODEX_REASONING_EFFORT",),
    "codex-mcp": ("CODEX_REASONING_EFFORT",),
    "claude": ("CLAUDE_CODE_EFFORT_LEVEL",),
    "github-copilot": (),
    "gemini": (),
    "microsoft-copilot": (),
}

CLIENT_RUNTIME_ENV_VARS = {
    "claude": ("CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS",),
}

MODEL_POLICIES: dict[str, dict[str, Any]] = {
    "codex": {
        "default_model": "gpt-5.4",
        "default_source": "built_in_latest_explicit",
        "default_effort": "xhigh",
        "pass_default_model_arg": True,
        "latest_policy": "OpenAI model documentation describes gpt-5.4 as the frontier model for complex professional work; the harness sets xhigh reasoning effort for best-model runs.",
        "reference_url": "https://developers.openai.com/api/docs/models/gpt-5.4",
        "reference_checked_at": "2026-04-18",
    },
    "codex-mcp": {
        "default_model": "gpt-5.4",
        "default_source": "built_in_latest_explicit_with_challenge2_wiki_mcp",
        "default_effort": "xhigh",
        "pass_default_model_arg": True,
        "latest_policy": "Codex uses gpt-5.4 with xhigh reasoning effort and a configured local Challenge 2 Wiki MCP server for source retrieval.",
        "reference_url": "https://developers.openai.com/api/docs/models/gpt-5.4",
        "reference_checked_at": "2026-04-18",
    },
    "gemini": {
        "default_model": "auto",
        "default_source": "cli_default_auto_routing",
        "pass_default_model_arg": False,
        "known_default_model_label": "Auto routing over Gemini 3 and available Gemini 3.1 models",
        "latest_policy": "Gemini CLI docs recommend Auto routing; Gemini 3.1 Pro Preview is included in routing where available, so the harness leaves routing to the installed client.",
        "reference_url": "https://geminicli.com/docs/get-started/gemini-3/",
        "reference_checked_at": "2026-04-18",
    },
    "claude": {
        "default_model": "best",
        "default_source": "built_in_best_alias",
        "default_effort": "max",
        "pass_default_model_arg": True,
        "latest_policy": "Claude Code documents best as the most capable available model and currently equivalent to opus; the harness uses max effort for best-model runs.",
        "reference_url": "https://code.claude.com/docs/en/model-config",
        "reference_checked_at": "2026-04-18",
    },
    "github-copilot": {
        "default_model": "gpt-5.4",
        "default_source": "staff_confirmed_best_override",
        "default_effort": "xhigh",
        "pass_default_model_arg": True,
        "latest_policy": "Staff-confirmed override after contradictory Copilot documentation: use gpt-5.4 with xhigh effort for GitHub Copilot CLI best-model coverage; public Copilot docs are retained as context.",
        "reference_url": "https://docs.github.com/en/copilot/reference/ai-models/model-comparison",
        "reference_checked_at": "2026-04-18",
    },
    "microsoft-copilot": {
        "default_model": "gpt-5-auto-routed",
        "default_source": "microsoft_365_copilot_default_gpt5",
        "known_default_model_label": "Microsoft 365 Copilot Chat GPT-5 with automatic routing",
        "pass_default_model_arg": False,
        "latest_policy": "Microsoft 365 Copilot release notes state Copilot Chat uses GPT-5 by default and routes prompts to the best-performing models for each task.",
        "reference_url": "https://learn.microsoft.com/en-us/microsoft-365/copilot/release-notes",
        "reference_checked_at": "2026-04-18",
    },
}

CLIENT_VERSION_COMMANDS = {
    "codex": (("codex", "--version"),),
    "codex-mcp": (("codex", "--version"), (sys.executable, "--version")),
    "gemini": (("gemini", "--version"),),
    "claude": (("claude", "--version"),),
    "github-copilot": (
        ("copilot", "version"),
        ("copilot", "--version"),
        ("gh", "--version"),
        ("gh", "copilot", "--help"),
    ),
    "microsoft-copilot": (("node", "--version"),),
}

MACOS_AI_APP_PATHS = (
    "/Applications/Copilot.app",
    "/Applications/Microsoft 365 Copilot.app",
)

MICROSOFT_COPILOT_URL = "https://m365.cloud.microsoft/chat"


@dataclass(frozen=True)
class ClientCommandContext:
    client: str
    model: str | None
    prompt: str
    question_id: str
    run_dir: Path
    repo_root: Path
    challenge_root: Path
    assistant_response_path: Path
    client_manifest: dict[str, Any] | None = None


def build_wiki_prompt(
    question: EvaluationQuestion,
    *,
    repo_root: Path,
    challenge_root: Path,
    client_config: dict[str, Any] | None = None,
) -> str:
    """Build the per-question prompt sent to each CLI client."""

    client_config = client_config or {}
    source_lines = _prompt_source_lines(
        repo_root=repo_root,
        challenge_root=challenge_root,
        client_config=client_config,
    )
    context_lines = _prompt_context_lines(repo_root=repo_root, client_config=client_config)
    repository_context = _prompt_repository_context(repo_root=repo_root, client_config=client_config)

    return "\n".join(
        [
            "You are answering a Challenge 2 wiki evaluation question.",
            "",
            *source_lines,
            "",
            "Do not use web search or outside knowledge. Do not inspect raw source files unless the question explicitly asks about provenance back to a raw file path.",
            "Do not inspect challenge-2/wiki/evaluation-benchmark.md or challenge-2/evaluation/ while answering; those are benchmark harness artifacts and contain gold-answer or scoring material.",
            "Cite the source IDs or wiki paths you used. Preserve any caveat the wiki flags, including draft, stale, superseded, synthetic, low OCR quality, past review, contradictory, or incomplete material.",
            "",
            "Return concise JSON with this shape:",
            '{"question_id":"Q000","answer":"...","cited_sources":["..."],"caveats":["..."]}',
            "",
            repository_context,
            f"Question ID: {question.question_id}",
            f"Category: {question.category}",
            f"Question: {question.question}",
            *context_lines,
        ]
    )


def build_client_prompt(
    client: str,
    question: EvaluationQuestion,
    *,
    repo_root: Path,
    challenge_root: Path,
    run_dir: Path,
    client_config: dict[str, Any] | None = None,
) -> str:
    """Build the per-client prompt, including MCP context generation where required."""

    client_config = client_config or {}
    if client == "codex-mcp":
        return build_codex_mcp_prompt(
            question,
            repo_root=repo_root,
            challenge_root=challenge_root,
            run_dir=run_dir,
            client_config=client_config,
        )
    return build_wiki_prompt(
        question,
        repo_root=repo_root,
        challenge_root=challenge_root,
        client_config=client_config,
    )


def build_codex_mcp_prompt(
    question: EvaluationQuestion,
    *,
    repo_root: Path,
    challenge_root: Path,
    run_dir: Path,
    client_config: dict[str, Any] | None = None,
) -> str:
    """Build a Codex prompt backed by a context pack from the local wiki MCP implementation."""

    client_config = client_config or {}
    implementation_root = challenge_root / "MCP-Wiki" / "implementation"
    if str(implementation_root) not in sys.path:
        sys.path.insert(0, str(implementation_root))
    from wiki_mcp import AuditLogger, WikiKnowledgeBase, build_codex_mcp_prompt as format_mcp_prompt  # noqa: PLC0415

    artifact_dir = run_dir / "raw" / "codex-mcp"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    audit_path = artifact_dir / f"{question.question_id}.context-pack-audit.jsonl"
    semantic_model_id = str(client_config.get("semantic_model_id") or "challenge2-local-hash-v1")
    kb = WikiKnowledgeBase(
        repo_root=repo_root,
        challenge_root=challenge_root,
        audit=AuditLogger(audit_path),
        semantic_model_id=semantic_model_id,
    )
    context_pack = kb.build_context_pack(
        query=question.question,
        limit=int(client_config.get("mcp_context_limit") or 8),
        budget_bytes=int(client_config.get("mcp_context_budget_bytes") or 48000),
        mode=str(client_config.get("mcp_retrieval_mode") or "hybrid"),
    )
    context_pack_path = artifact_dir / f"{question.question_id}.context-pack.json"
    context_pack_path.write_text(json.dumps(context_pack, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    prompt = format_mcp_prompt(
        question.question_id,
        question.category,
        question.question,
        context_pack,
        include_context_pack=bool(client_config.get("mcp_prompt_include_context_pack")),
    )
    return "\n".join(
        [
            prompt,
            "",
            "The local MCP server is configured for Codex as `challenge2_wiki`.",
            "Use the MCP server tools directly if you need to verify, expand, or cross-check the supplied context pack.",
            f"Context pack audit artifact: {context_pack_path}",
        ]
    )


def _prompt_repository_context(*, repo_root: Path, client_config: dict[str, Any]) -> str:
    mode = str(client_config.get("prompt_source_mode") or "local_paths")
    if mode == "github_permalinks":
        return "Repository baseline: public GitHub permalink sources listed above"
    return f"Repository root: {repo_root}"


def load_client_config(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def describe_client(
    client: str,
    *,
    model_override: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Capture run-time client, model, and executable metadata without invoking an LLM."""

    client_config = _client_config(config, client)
    model = resolve_model(client, model_override=model_override, client_config=client_config)
    command_source = "client_config.argv" if "argv" in client_config else "built_in"
    return {
        "client": client,
        "captured_at": utc_now(),
        "supported_by_harness": client in SUPPORTED_CLIENTS,
        "model": model,
        "command_source": command_source,
        "command_config": _public_client_config_metadata(client_config),
        "executables": _describe_executables(client, client_config),
        "version_checks": [_run_version_check(command) for command in CLIENT_VERSION_COMMANDS.get(client, ())],
        "ui_automation": _describe_ui_automation(client, client_config),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "model_environment": _capture_model_environment(client),
        "runtime_environment": _capture_runtime_environment(client, client_config),
    }


def describe_desktop_ai_apps() -> list[dict[str, Any]]:
    """Capture installed desktop AI app versions that are not headless harness clients."""

    if platform.system() != "Darwin":
        return []
    apps: list[dict[str, Any]] = []
    for raw_path in MACOS_AI_APP_PATHS:
        path = Path(raw_path)
        if not path.exists():
            continue
        info = _read_macos_app_info(path)
        apps.append(
            {
                "path": str(path),
                "name": info.get("CFBundleDisplayName") or info.get("CFBundleName") or path.stem,
                "bundle_identifier": info.get("CFBundleIdentifier"),
                "version": info.get("CFBundleShortVersionString") or info.get("CFBundleVersion"),
                "build": info.get("CFBundleVersion"),
                "headless_harness_client": False,
            }
        )
    return apps


def _prompt_source_lines(*, repo_root: Path, challenge_root: Path, client_config: dict[str, Any]) -> list[str]:
    mode = str(client_config.get("prompt_source_mode") or "local_paths")
    if mode == "github_permalinks":
        tree_base = str(client_config.get("github_tree_base_url") or "").rstrip("/")
        blob_base = str(client_config.get("github_blob_base_url") or "").rstrip("/")
        has_context = bool(client_config.get("prompt_context_paths"))
        if not tree_base:
            tree_base = "https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/tree/v1.1"
        if not blob_base:
            blob_base = tree_base.replace("/tree/", "/blob/")
        source_intro = "Use only these public GitHub permalink sources"
        if has_context:
            source_intro += " and the copied source excerpts below"
        return [
            f"{source_intro} as authority:",
            f"- {tree_base}/challenge-2/wiki",
            f"- {tree_base}/challenge-2/wiki/data",
            f"- {blob_base}/challenge-2/AGENTS.md",
        ]
    return [
        "Use only these local repository sources as authority:",
        f"- {challenge_root / 'wiki'}",
        f"- {challenge_root / 'wiki' / 'data'}",
        f"- {challenge_root / 'AGENTS.md'}",
    ]


def _prompt_context_lines(*, repo_root: Path, client_config: dict[str, Any]) -> list[str]:
    raw_paths = client_config.get("prompt_context_paths")
    if not isinstance(raw_paths, list) or not raw_paths:
        return []
    max_chars = int(client_config.get("prompt_context_max_chars") or 24000)
    remaining = max(max_chars, 0)
    lines = [
        "",
        "Copied source excerpts for clients without local filesystem access:",
    ]
    for raw_path in raw_paths:
        rel_path = Path(str(raw_path))
        if rel_path.is_absolute() or ".." in rel_path.parts:
            continue
        if "evaluation-benchmark.md" in rel_path.parts or "evaluation" in rel_path.parts:
            continue
        path = repo_root / rel_path
        if not path.exists() or not path.is_file() or remaining <= 0:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        excerpt = text[:remaining]
        remaining -= len(excerpt)
        suffix = "\n[truncated]" if len(excerpt) < len(text) else ""
        lines.extend(
            [
                "",
                f"--- {rel_path.as_posix()} ---",
                f"{excerpt}{suffix}",
            ]
        )
    return lines


def resolve_model(
    client: str,
    *,
    model_override: str | None = None,
    client_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve the model selector and record why that selector was chosen."""

    policy = MODEL_POLICIES.get(client, {})
    client_config = client_config or {}
    if model_override is not None and model_override.strip():
        model = model_override.strip()
        source = "run_argument"
        pass_model_arg = True
        effort = _configured_effort(client, client_config, policy)
    elif str(client_config.get("model") or "").strip():
        model = str(client_config["model"]).strip()
        source = str(client_config.get("model_source") or "client_config")
        pass_model_arg = bool(client_config.get("pass_model_arg", True))
        effort = _configured_effort(client, client_config, policy)
    else:
        env_model = _first_model_environment(client)
        if env_model is not None:
            model, env_var = env_model
            source = f"environment:{env_var}"
            pass_model_arg = True
            effort = _configured_effort(client, client_config, policy)
        else:
            model = str(policy.get("default_model") or "")
            source = str(policy.get("default_source") or "unspecified")
            pass_model_arg = bool(policy.get("pass_default_model_arg", bool(model)))
            effort = _configured_effort(client, client_config, policy)

    return {
        "selected_model": model or None,
        "reasoning_effort": effort,
        "source": source,
        "pass_model_arg": pass_model_arg and bool(model),
        "known_default_model_label": policy.get("known_default_model_label"),
        "latest_policy": client_config.get("latest_policy") or policy.get("latest_policy"),
        "reference_url": client_config.get("model_reference_url") or policy.get("reference_url"),
        "reference_checked_at": client_config.get("model_reference_checked_at")
        or policy.get("reference_checked_at"),
    }


def build_client_invocation(
    context: ClientCommandContext, config: dict[str, Any] | None = None
) -> tuple[list[str], dict[str, Any]]:
    """Build a client command and metadata describing model/command selection."""

    client_config = _client_config(config, context.client)
    model = resolve_model(context.client, model_override=context.model, client_config=client_config)
    if "argv" in client_config:
        command = []
        for raw_token in client_config["argv"]:
            expanded = _expand_token(str(raw_token), context, model=model)
            if expanded != "":
                command.append(expanded)
        return command, {
            "model": model,
            "command_source": "client_config.argv",
            "command_config": _public_client_config_metadata(client_config),
        }

    command_model = str(model.get("selected_model") or "")
    pass_model_arg = bool(model.get("pass_model_arg") and command_model)
    if context.client == "codex":
        command = [
            "codex",
            "exec",
            "-m",
            command_model or "gpt-5.4",
        ]
        if model.get("reasoning_effort"):
            command.extend(["-c", f"model_reasoning_effort=\"{model['reasoning_effort']}\""])
        command.extend(
            [
                "--json",
                "-o",
                str(context.assistant_response_path),
                "-C",
                str(context.repo_root),
                context.prompt,
            ]
        )
    elif context.client == "codex-mcp":
        command = _codex_mcp_command(context, command_model or "gpt-5.4", str(model.get("reasoning_effort") or "xhigh"))
    elif context.client == "gemini":
        command = [
            "gemini",
            "--approval-mode",
            "yolo",
            "--output-format",
            "json",
            "--include-directories",
            str(context.challenge_root),
        ]
        if pass_model_arg:
            command.extend(["--model", command_model])
        command.extend(["--prompt", context.prompt])
    elif context.client == "claude":
        command = ["claude"]
        if pass_model_arg:
            command.extend(["--model", command_model])
        if model.get("reasoning_effort"):
            command.extend(["--effort", str(model["reasoning_effort"])])
        command.extend(["-p", "--output-format", "json", context.prompt])
    elif context.client == "github-copilot":
        command = _github_copilot_command(
            context,
            command_model if pass_model_arg else None,
            str(model.get("reasoning_effort") or "") or None,
        )
    elif context.client == "microsoft-copilot":
        command = _microsoft_copilot_command(context, client_config)
    else:
        raise ValueError(f"Unsupported client: {context.client}")

    return command, {
        "model": model,
        "command_source": "built_in",
        "command_config": _public_client_config_metadata(client_config),
    }


def build_command(context: ClientCommandContext, config: dict[str, Any] | None = None) -> list[str]:
    """Build a client command, using optional JSON config overrides."""

    return build_client_invocation(context, config)[0]


def run_client(
    *,
    context: ClientCommandContext,
    prompt_path: Path,
    config: dict[str, Any] | None,
    timeout_sec: int,
    dry_run: bool,
) -> ClientRunResult:
    """Run a client command and capture visible output."""

    client_config = _client_config(config, context.client)
    command, invocation_metadata = build_client_invocation(context, config)
    selected_model = invocation_metadata["model"].get("selected_model")
    metadata = {
        "invocation": invocation_metadata,
        "client_manifest": context.client_manifest or {},
    }
    stdout_path = context.run_dir / "raw" / context.client / f"{context.question_id}.stdout.txt"
    stderr_path = context.run_dir / "raw" / context.client / f"{context.question_id}.stderr.txt"
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    started = time.monotonic()
    if dry_run:
        finished_at = utc_now()
        return ClientRunResult(
            run_id=context.run_dir.name,
            client=context.client,
            question_id=context.question_id,
            model=selected_model,
            command=command,
            status="dry_run",
            answer_text="",
            elapsed_seconds=0.0,
            started_at=started_at,
            finished_at=finished_at,
            prompt_path=str(prompt_path),
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            metadata=metadata,
        )
    try:
        proc = subprocess.run(
            command,
            cwd=context.repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=max(timeout_sec, 1),
            env=_subprocess_environment(client_config),
        )
        elapsed = time.monotonic() - started
        stdout_path.write_text(proc.stdout or "", encoding="utf-8")
        stderr_path.write_text(proc.stderr or "", encoding="utf-8")
        answer_text = _read_answer_text(context.assistant_response_path, proc.stdout)
        status = _client_status(context.client, proc.returncode, context.assistant_response_path, proc.stderr)
        return ClientRunResult(
            run_id=context.run_dir.name,
            client=context.client,
            question_id=context.question_id,
            model=selected_model,
            command=command,
            status=status,
            answer_text=answer_text,
            elapsed_seconds=elapsed,
            started_at=started_at,
            finished_at=utc_now(),
            exit_code=proc.returncode,
            prompt_path=str(prompt_path),
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            error=None if proc.returncode == 0 else f"{context.client} exited with {proc.returncode}",
            metadata=metadata,
        )
    except FileNotFoundError as exc:
        elapsed = time.monotonic() - started
        stderr_path.write_text(str(exc), encoding="utf-8")
        return ClientRunResult(
            run_id=context.run_dir.name,
            client=context.client,
            question_id=context.question_id,
            model=selected_model,
            command=command,
            status="unavailable",
            answer_text="",
            elapsed_seconds=elapsed,
            started_at=started_at,
            finished_at=utc_now(),
            exit_code=127,
            prompt_path=str(prompt_path),
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            error=f"{context.client} executable unavailable: {exc}",
            metadata=metadata,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - started
        stdout_path.write_text(_coerce_output(exc.stdout), encoding="utf-8")
        stderr_path.write_text(_coerce_output(exc.stderr), encoding="utf-8")
        return ClientRunResult(
            run_id=context.run_dir.name,
            client=context.client,
            question_id=context.question_id,
            model=selected_model,
            command=command,
            status="timeout",
            answer_text=_coerce_output(exc.stdout),
            elapsed_seconds=elapsed,
            started_at=started_at,
            finished_at=utc_now(),
            exit_code=124,
            timed_out=True,
            prompt_path=str(prompt_path),
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            error=f"{context.client} timed out after {timeout_sec}s",
            metadata=metadata,
        )


def _read_answer_text(assistant_response_path: Path, stdout: str) -> str:
    if assistant_response_path.exists() and assistant_response_path.stat().st_size:
        return assistant_response_path.read_text(encoding="utf-8", errors="replace")
    return stdout or ""


def _client_status(client: str, returncode: int, assistant_response_path: Path, stderr: str = "") -> str:
    if returncode == 0:
        return "completed"
    if client == "github-copilot" and "Copilot CLI not installed" in stderr:
        return "unavailable"
    if client == "github-copilot" and "Access denied by policy settings" in stderr:
        return "policy_blocked"
    if client == "gemini" and ("QUOTA_EXHAUSTED" in stderr or "exhausted your capacity" in stderr):
        return "quota_exhausted"
    if client == "microsoft-copilot" and assistant_response_path.exists():
        try:
            payload = json.loads(assistant_response_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return "failed"
        status = str(payload.get("status") or "").strip()
        if status:
            return status
    return "failed"


def _coerce_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _expand_token(token: str, context: ClientCommandContext, *, model: dict[str, Any]) -> str:
    selected_model = str(model.get("selected_model") or "")
    values = {
        "client": context.client,
        "model": selected_model,
        "prompt": context.prompt,
        "question_id": context.question_id,
        "run_dir": str(context.run_dir),
        "repo_root": str(context.repo_root),
        "challenge_root": str(context.challenge_root),
        "wiki_root": str(context.challenge_root / "wiki"),
        "assistant_response_path": str(context.assistant_response_path),
    }
    return token.format(**values)


def _client_config(config: dict[str, Any] | None, client: str) -> dict[str, Any]:
    if not isinstance(config, dict):
        return {}
    value = config.get(client, {})
    return value if isinstance(value, dict) else {}


def _first_model_environment(client: str) -> tuple[str, str] | None:
    for name in MODEL_ENV_VARS.get(client, ()):
        value = os.environ.get(name)
        if value:
            return value, name
    return None


def _capture_model_environment(client: str) -> dict[str, dict[str, Any]]:
    captured: dict[str, dict[str, Any]] = {}
    for name in MODEL_ENV_VARS.get(client, ()) + MODEL_EFFORT_ENV_VARS.get(client, ()):
        value = os.environ.get(name)
        captured[name] = {"set": value is not None, "value": value if value else None}
    return captured


def _capture_runtime_environment(client: str, client_config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    names = set(CLIENT_RUNTIME_ENV_VARS.get(client, ()))
    names.update(_configured_environment(client_config).keys())
    captured: dict[str, dict[str, Any]] = {}
    configured = _configured_environment(client_config)
    for name in sorted(names):
        value = configured.get(name, os.environ.get(name))
        captured[name] = {
            "set": value is not None,
            "source": "client_config" if name in configured else "environment",
            "value": _public_env_value(name, value),
        }
    return captured


def _configured_environment(client_config: dict[str, Any]) -> dict[str, str | None]:
    raw = client_config.get("environment", client_config.get("env", {}))
    if not isinstance(raw, dict):
        return {}
    return {str(name): (None if value is None else str(value)) for name, value in raw.items()}


def _subprocess_environment(client_config: dict[str, Any]) -> dict[str, str]:
    env = os.environ.copy()
    for name, value in _configured_environment(client_config).items():
        if value is None:
            env.pop(name, None)
        else:
            env[name] = value
    return env


def _configured_effort(client: str, client_config: dict[str, Any], policy: dict[str, Any]) -> str | None:
    for key in ("reasoning_effort", "effort"):
        if key in client_config and client_config[key] is None:
            return None
        if str(client_config.get(key) or "").strip():
            return str(client_config[key]).strip()
    for name in MODEL_EFFORT_ENV_VARS.get(client, ()):
        value = os.environ.get(name)
        if value:
            return value
    value = policy.get("default_effort")
    return str(value) if value else None


def _describe_executables(client: str, client_config: dict[str, Any]) -> list[dict[str, Any]]:
    names: list[str] = []
    if "argv" in client_config and client_config["argv"]:
        names.append(str(client_config["argv"][0]))
    elif client == "codex-mcp":
        names.extend(["codex", Path(sys.executable).name])
    elif client == "github-copilot":
        names.extend(["copilot", "gh"])
    elif client == "microsoft-copilot":
        names.append("node")
    else:
        names.append({"codex": "codex", "gemini": "gemini", "claude": "claude"}.get(client, client))
    seen: set[str] = set()
    executables: list[dict[str, Any]] = []
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        executables.append({"name": name, "path": shutil.which(name), "available": shutil.which(name) is not None})
    return executables


def _describe_ui_automation(client: str, client_config: dict[str, Any]) -> dict[str, Any] | None:
    if client != "microsoft-copilot":
        return None
    profile_dir_source = "client_config" if client_config.get("profile_dir") else "environment"
    if not client_config.get("profile_dir") and not os.environ.get("MICROSOFT_COPILOT_PROFILE_DIR"):
        profile_dir_source = "default"
    return {
        "method": client_config.get("automation_method") or "playwright_web_ui",
        "url": client_config.get("url") or MICROSOFT_COPILOT_URL,
        "app_name": client_config.get("app_name") or "Microsoft 365 Copilot",
        "profile_dir_source": profile_dir_source,
        "profile_dir_configured": profile_dir_source != "default",
        "headless": bool(client_config.get("headless", False)),
        "preferred_mode": client_config.get("preferred_mode"),
        "caveats": [
            "Microsoft Copilot is evaluated through a browser UI adapter rather than a stable headless API.",
            "The adapter requires an authenticated Microsoft session in the Playwright profile.",
            "Selectors, loading states, tenant policies, and model routing can change outside this repository.",
        ],
    }


def _run_version_check(command: tuple[str, ...]) -> dict[str, Any]:
    executable_path = shutil.which(command[0])
    record: dict[str, Any] = {
        "command": list(command),
        "executable_path": executable_path,
        "available": executable_path is not None,
    }
    if executable_path is None:
        record["status"] = "missing"
        return record
    try:
        proc = subprocess.run(
            list(command),
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except subprocess.TimeoutExpired as exc:
        record.update(
            {
                "status": "timeout",
                "exit_code": 124,
                "stdout": _trim_output(_coerce_output(exc.stdout)),
                "stderr": _trim_output(_coerce_output(exc.stderr)),
            }
        )
        return record
    record.update(
        {
            "status": "completed" if proc.returncode == 0 else "failed",
            "exit_code": proc.returncode,
            "stdout": _trim_output(proc.stdout),
            "stderr": _trim_output(proc.stderr),
            "detected_version": _first_output_line(proc.stdout or proc.stderr),
        }
    )
    return record


def _first_output_line(value: str | None) -> str | None:
    if not value:
        return None
    for line in value.splitlines():
        if line.strip():
            return line.strip()
    return None


def _trim_output(value: str | None, limit: int = 4000) -> str:
    if not value:
        return ""
    if len(value) <= limit:
        return value
    return value[:limit] + "\n[truncated]\n"


def _github_copilot_command(
    context: ClientCommandContext, model: str | None, reasoning_effort: str | None
) -> list[str]:
    if shutil.which("copilot"):
        command = ["copilot"]
    else:
        command = ["gh", "copilot", "--"]
    command.extend(
        [
            f"--add-dir={context.challenge_root}",
            "--available-tools=read",
            "--allow-tool=read",
        ]
    )
    if model:
        command.extend(["--model", model])
    if reasoning_effort:
        command.append(f"--reasoning-effort={reasoning_effort}")
    command.extend(["-p", context.prompt])
    return command


def _codex_mcp_command(context: ClientCommandContext, model: str, reasoning_effort: str | None) -> list[str]:
    script_path = context.challenge_root / "tools" / "wiki_mcp_server.py"
    audit_path = context.run_dir / "raw" / context.client / f"{context.question_id}.mcp-audit.jsonl"
    mcp_args = [
        str(script_path),
        "--transport",
        "stdio",
        "--repo-root",
        str(context.repo_root),
        "--challenge-root",
        str(context.challenge_root),
        "--audit-path",
        str(audit_path),
    ]
    command = [
        "codex",
        "exec",
        "-m",
        model,
    ]
    if reasoning_effort:
        command.extend(["-c", f"model_reasoning_effort=\"{reasoning_effort}\""])
    command.extend(
        [
            "-c",
            f"mcp_servers.challenge2_wiki.command={json.dumps(sys.executable)}",
            "-c",
            f"mcp_servers.challenge2_wiki.args={json.dumps(mcp_args)}",
            "--dangerously-bypass-approvals-and-sandbox",
            "--json",
            "-o",
            str(context.assistant_response_path),
            "-C",
            str(context.repo_root),
            context.prompt,
        ]
    )
    return command


def _microsoft_copilot_command(context: ClientCommandContext, client_config: dict[str, Any]) -> list[str]:
    script_path = context.challenge_root / "tools" / "microsoft_copilot_playwright.mjs"
    command = [
        "node",
        str(script_path),
        "--client",
        context.client,
        "--url",
        str(client_config.get("url") or MICROSOFT_COPILOT_URL),
        "--output",
        str(context.assistant_response_path),
        "--artifact-dir",
        str(context.run_dir / "raw" / context.client / f"{context.question_id}.ui"),
        "--prompt",
        context.prompt,
    ]
    preferred_mode = client_config.get("preferred_mode")
    if preferred_mode:
        command.extend(["--preferred-mode", str(preferred_mode)])
    profile_dir = client_config.get("profile_dir")
    if profile_dir:
        command.extend(["--profile-dir", str(profile_dir)])
    if client_config.get("headless"):
        command.append("--headless")
    return command


def _public_client_config_metadata(client_config: dict[str, Any]) -> dict[str, Any]:
    allowed_keys = {
        "model",
        "model_source",
        "model_reference_url",
        "model_reference_checked_at",
        "reasoning_effort",
        "effort",
        "latest_policy",
        "pass_model_arg",
        "automation_method",
        "url",
        "app_name",
        "profile_dir",
        "headless",
        "preferred_mode",
        "prompt_source_mode",
        "github_tree_base_url",
        "github_blob_base_url",
        "prompt_context_paths",
        "prompt_context_max_chars",
        "environment",
        "env",
        "mcp_context_limit",
        "mcp_context_budget_bytes",
        "mcp_retrieval_mode",
        "mcp_server_transport",
        "mcp_prompt_include_context_pack",
        "semantic_model_id",
        "notes",
    }
    record: dict[str, Any] = {}
    for key in allowed_keys:
        if key not in client_config:
            continue
        if key in {"environment", "env"} and isinstance(client_config[key], dict):
            record[key] = {
                str(name): _public_env_value(str(name), None if value is None else str(value))
                for name, value in client_config[key].items()
            }
        else:
            record[key] = client_config[key]
    return record


def _public_env_value(name: str, value: str | None) -> str | None:
    if value is None:
        return None
    if any(marker in name.upper() for marker in ("TOKEN", "KEY", "SECRET", "PASSWORD", "AUTH", "CREDENTIAL")):
        return "[redacted]"
    return value


def _read_macos_app_info(path: Path) -> dict[str, Any]:
    info_plist = path / "Contents" / "Info.plist"
    if not info_plist.exists():
        return {}
    try:
        with info_plist.open("rb") as handle:
            return plistlib.load(handle)
    except (OSError, plistlib.InvalidFileException):
        return {}
