"""Client command helpers for the Challenge 2 wiki evaluation harness."""

from __future__ import annotations

import json
import os
import platform
import plistlib
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .audit import ClientRunResult, utc_now
from .questions import EvaluationQuestion


SUPPORTED_CLIENTS = ("codex", "gemini", "claude", "github-copilot")
DEFAULT_CLIENTS = ("codex", "gemini", "claude")

MODEL_ENV_VARS = {
    "codex": ("CODEX_MODEL",),
    "gemini": ("GEMINI_MODEL",),
    "claude": ("CLAUDE_MODEL", "ANTHROPIC_MODEL"),
    "github-copilot": ("COPILOT_MODEL",),
}

MODEL_POLICIES: dict[str, dict[str, Any]] = {
    "codex": {
        "default_model": "gpt-5.4",
        "default_source": "built_in_latest_explicit",
        "pass_default_model_arg": True,
        "latest_policy": "OpenAI model documentation recommends gpt-5.4 for complex reasoning and coding workflows.",
        "reference_url": "https://developers.openai.com/api/docs/models",
        "reference_checked_at": "2026-04-18",
    },
    "gemini": {
        "default_model": "auto",
        "default_source": "cli_default_auto_routing",
        "pass_default_model_arg": False,
        "latest_policy": "Gemini CLI defaults to Auto routing; current docs describe Gemini 3 Auto routing over Gemini 3 Pro/Flash where available.",
        "reference_url": "https://geminicli.com/docs/cli/model-routing/",
        "reference_checked_at": "2026-04-18",
    },
    "claude": {
        "default_model": "opus",
        "default_source": "built_in_latest_alias",
        "pass_default_model_arg": True,
        "latest_policy": "Claude Code's opus alias selects the most capable Opus model available to the account; record the CLI version because the alias floats.",
        "reference_url": "https://code.claude.com/docs/en/model-config",
        "reference_checked_at": "2026-04-18",
    },
    "github-copilot": {
        "default_model": "copilot-cli-default",
        "default_source": "cli_default_floating",
        "known_default_model_label": "Claude Sonnet 4.5",
        "pass_default_model_arg": False,
        "latest_policy": "GitHub documents the Copilot CLI default as Claude Sonnet 4.5 and reserves the right to change it; pass --model only when deliberately pinned.",
        "reference_url": "https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli",
        "reference_checked_at": "2026-04-18",
    },
}

CLIENT_VERSION_COMMANDS = {
    "codex": (("codex", "--version"),),
    "gemini": (("gemini", "--version"),),
    "claude": (("claude", "--version"),),
    "github-copilot": (
        ("copilot", "--version"),
        ("gh", "--version"),
        ("gh", "copilot", "--help"),
    ),
}

MACOS_AI_APP_PATHS = (
    "/Applications/Copilot.app",
    "/Applications/Microsoft 365 Copilot.app",
)


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


def build_wiki_prompt(question: EvaluationQuestion, *, repo_root: Path, challenge_root: Path) -> str:
    """Build the per-question prompt sent to each CLI client."""

    return "\n".join(
        [
            "You are answering a Challenge 2 wiki evaluation question.",
            "",
            "Use only these local repository sources as authority:",
            f"- {challenge_root / 'wiki'}",
            f"- {challenge_root / 'wiki' / 'data'}",
            f"- {challenge_root / 'AGENTS.md'}",
            "",
            "Do not use web search or outside knowledge. Do not inspect raw source files unless the question explicitly asks about provenance back to a raw file path.",
            "Do not inspect challenge-2/wiki/evaluation-benchmark.md or challenge-2/evaluation/ while answering; those are benchmark harness artifacts and contain gold-answer or scoring material.",
            "Cite the source IDs or wiki paths you used. Preserve any caveat the wiki flags, including draft, stale, superseded, synthetic, low OCR quality, past review, contradictory, or incomplete material.",
            "",
            "Return concise JSON with this shape:",
            '{"question_id":"Q000","answer":"...","cited_sources":["..."],"caveats":["..."]}',
            "",
            f"Repository root: {repo_root}",
            f"Question ID: {question.question_id}",
            f"Category: {question.category}",
            f"Question: {question.question}",
        ]
    )


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
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "model_environment": _capture_model_environment(client),
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
    elif str(client_config.get("model") or "").strip():
        model = str(client_config["model"]).strip()
        source = str(client_config.get("model_source") or "client_config")
        pass_model_arg = bool(client_config.get("pass_model_arg", True))
    else:
        env_model = _first_model_environment(client)
        if env_model is not None:
            model, env_var = env_model
            source = f"environment:{env_var}"
            pass_model_arg = True
        else:
            model = str(policy.get("default_model") or "")
            source = str(policy.get("default_source") or "unspecified")
            pass_model_arg = bool(policy.get("pass_default_model_arg", bool(model)))

    return {
        "selected_model": model or None,
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
            "--json",
            "-o",
            str(context.assistant_response_path),
            "-C",
            str(context.repo_root),
            context.prompt,
        ]
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
        command.extend(["-p", "--output-format", "json", context.prompt])
    elif context.client == "github-copilot":
        command = _github_copilot_command(context, command_model if pass_model_arg else None)
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
        )
        elapsed = time.monotonic() - started
        stdout_path.write_text(proc.stdout or "", encoding="utf-8")
        stderr_path.write_text(proc.stderr or "", encoding="utf-8")
        answer_text = _read_answer_text(context.assistant_response_path, proc.stdout)
        return ClientRunResult(
            run_id=context.run_dir.name,
            client=context.client,
            question_id=context.question_id,
            model=selected_model,
            command=command,
            status="completed" if proc.returncode == 0 else "failed",
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
    for name in MODEL_ENV_VARS.get(client, ()):
        value = os.environ.get(name)
        captured[name] = {"set": value is not None, "value": value if value else None}
    return captured


def _describe_executables(client: str, client_config: dict[str, Any]) -> list[dict[str, Any]]:
    names: list[str] = []
    if "argv" in client_config and client_config["argv"]:
        names.append(str(client_config["argv"][0]))
    elif client == "github-copilot":
        names.extend(["copilot", "gh"])
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


def _github_copilot_command(context: ClientCommandContext, model: str | None) -> list[str]:
    if shutil.which("copilot"):
        command = ["copilot"]
    else:
        command = ["gh", "copilot", "--"]
    if model:
        command.extend(["--model", model])
    command.extend(["-p", context.prompt])
    return command


def _public_client_config_metadata(client_config: dict[str, Any]) -> dict[str, Any]:
    allowed_keys = {
        "model",
        "model_source",
        "model_reference_url",
        "model_reference_checked_at",
        "latest_policy",
        "pass_model_arg",
        "notes",
    }
    return {key: client_config[key] for key in allowed_keys if key in client_config}


def _read_macos_app_info(path: Path) -> dict[str, Any]:
    info_plist = path / "Contents" / "Info.plist"
    if not info_plist.exists():
        return {}
    try:
        with info_plist.open("rb") as handle:
            return plistlib.load(handle)
    except (OSError, plistlib.InvalidFileException):
        return {}
