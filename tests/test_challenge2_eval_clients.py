from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
CHALLENGE_ROOT = REPO_ROOT / "challenge-2"
sys.path.insert(0, str(CHALLENGE_ROOT))

from evaluation.clients import ClientCommandContext, build_client_invocation, run_client  # noqa: E402
from evaluation.clients import _client_status  # noqa: E402


class Challenge2EvalClientsTest(unittest.TestCase):
    def test_default_model_selectors_are_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {}, clear=True):
            run_dir = Path(tmp) / "run"
            run_dir.mkdir()

            codex_command, codex_metadata = build_client_invocation(self._context(run_dir, "codex"), {})
            self.assertIn("gpt-5.4", codex_command)
            self.assertEqual(codex_metadata["model"]["selected_model"], "gpt-5.4")
            self.assertEqual(codex_metadata["model"]["source"], "built_in_latest_explicit")
            self.assertEqual(codex_metadata["model"]["reasoning_effort"], "xhigh")

            gemini_command, gemini_metadata = build_client_invocation(self._context(run_dir, "gemini"), {})
            self.assertNotIn("--model", gemini_command)
            self.assertEqual(gemini_metadata["model"]["selected_model"], "auto")
            self.assertEqual(gemini_metadata["model"]["source"], "cli_default_auto_routing")

            claude_command, claude_metadata = build_client_invocation(self._context(run_dir, "claude"), {})
            self.assertIn("--model", claude_command)
            self.assertIn("best", claude_command)
            self.assertIn("--effort", claude_command)
            self.assertIn("max", claude_command)
            self.assertEqual(claude_metadata["model"]["selected_model"], "best")

            copilot_command, copilot_metadata = build_client_invocation(
                self._context(run_dir, "github-copilot"), {}
            )
            self.assertIn("gpt-5.4", copilot_command)
            self.assertIn("--reasoning-effort=xhigh", copilot_command)
            self.assertEqual(copilot_metadata["model"]["source"], "staff_confirmed_best_override")
            self.assertEqual(copilot_metadata["model"]["reasoning_effort"], "xhigh")

            microsoft_command, microsoft_metadata = build_client_invocation(
                self._context(run_dir, "microsoft-copilot"), {}
            )
            self.assertIn("microsoft_copilot_playwright.mjs", " ".join(microsoft_command))
            self.assertEqual(microsoft_metadata["model"]["selected_model"], "gpt-5-auto-routed")

            thinking_command, thinking_metadata = build_client_invocation(
                self._context(run_dir, "microsoft-copilot"),
                {"microsoft-copilot": {"preferred_mode": "Think Deeper"}},
            )
            self.assertIn("--preferred-mode", thinking_command)
            self.assertIn("Think Deeper", thinking_command)
            self.assertEqual(thinking_metadata["command_config"]["preferred_mode"], "Think Deeper")

    def test_dry_run_records_resolved_model_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {}, clear=True):
            run_dir = Path(tmp) / "run"
            run_dir.mkdir()
            context = self._context(
                run_dir,
                "gemini",
                client_manifest={"client": "gemini", "version_checks": [{"detected_version": "0.0.test"}]},
            )
            prompt_path = run_dir / "prompts" / "gemini" / "Q001.txt"
            prompt_path.parent.mkdir(parents=True)
            prompt_path.write_text("prompt", encoding="utf-8")

            result = run_client(
                context=context,
                prompt_path=prompt_path,
                config={},
                timeout_sec=1,
                dry_run=True,
            )

            self.assertEqual(result.status, "dry_run")
            self.assertEqual(result.model, "auto")
            self.assertEqual(result.metadata["invocation"]["model"]["source"], "cli_default_auto_routing")
            self.assertEqual(result.metadata["client_manifest"]["client"], "gemini")

    def test_github_copilot_policy_denial_is_classified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            assistant_response_path = Path(tmp) / "missing.txt"
            status = _client_status(
                "github-copilot",
                1,
                assistant_response_path,
                "Error: Access denied by policy settings",
            )

            self.assertEqual(status, "policy_blocked")

    def test_claude_can_defer_model_and_effort_to_local_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {}, clear=True):
            run_dir = Path(tmp) / "run"
            run_dir.mkdir()
            command, metadata = build_client_invocation(
                self._context(run_dir, "claude"),
                {
                    "claude": {
                        "model": "local-settings-managed",
                        "model_source": "local_settings_managed",
                        "pass_model_arg": False,
                        "reasoning_effort": None,
                    }
                },
            )

            self.assertNotIn("--model", command)
            self.assertNotIn("--effort", command)
            self.assertEqual(metadata["model"]["selected_model"], "local-settings-managed")
            self.assertIsNone(metadata["model"]["reasoning_effort"])

    def _context(
        self,
        run_dir: Path,
        client: str,
        *,
        client_manifest: dict | None = None,
    ) -> ClientCommandContext:
        return ClientCommandContext(
            client=client,
            model=None,
            prompt="Answer from the wiki",
            question_id="Q001",
            run_dir=run_dir,
            repo_root=REPO_ROOT,
            challenge_root=CHALLENGE_ROOT,
            assistant_response_path=run_dir / "raw" / client / "Q001.assistant-response.txt",
            client_manifest=client_manifest,
        )


if __name__ == "__main__":
    unittest.main()
