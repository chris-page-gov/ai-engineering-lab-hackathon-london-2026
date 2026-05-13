from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.build_codex_postmortem import (  # noqa: E402
    Exchange,
    Message,
    Session,
    conversation_reader_path,
    exchange_anchor,
    infer_codex_contribution,
    infer_user_contribution,
    public_conversation_reader_path,
    public_sanitize_text,
    strip_fenced_blocks,
)


def make_exchange(user_text: str, assistant_text: str = "") -> Exchange:
    session = Session(
        source_id="CONV-TEST",
        session_id="test-session",
        thread_name="Test Thread",
        title="Test Thread",
        start_timestamp="2026-04-18T00:00:00Z",
        updated_at="2026-04-18T00:00:00Z",
        cwd=str(REPO_ROOT),
        source_path=Path("session.jsonl"),
        source_sha256="0" * 64,
    )
    assistant_messages = []
    if assistant_text:
        assistant_messages.append(
            Message(role="assistant", timestamp="2026-04-18T00:00:01Z", text=assistant_text)
        )
    return Exchange(
        exchange_id="EX-TEST",
        global_sequence=1,
        session=session,
        session_sequence=1,
        title="Test",
        slug="test",
        user_message=Message(role="user", timestamp="2026-04-18T00:00:00Z", text=user_text),
        assistant_messages=assistant_messages,
    )


class BuildCodexPostmortemContributionInferenceTest(unittest.TestCase):
    def test_exchange_anchor_is_stable_for_reader_links(self) -> None:
        self.assertEqual(exchange_anchor(make_exchange("Review")), "ex-0001")

    def test_private_reader_path_lives_under_readers(self) -> None:
        path = conversation_reader_path(make_exchange("Review").session)

        self.assertEqual(path.relative_to(REPO_ROOT).as_posix(), "postmortem/wiki/readers/conv-test-test-thread.md")

    def test_public_reader_path_lives_under_public_readers(self) -> None:
        path = public_conversation_reader_path(make_exchange("Review").session)

        self.assertEqual(
            path.relative_to(REPO_ROOT).as_posix(),
            "postmortem-public/wiki/readers/conv-test-test-thread.md",
        )

    def test_fence_stripper_handles_nested_triple_fences_inside_quad_fence(self) -> None:
        text = "before\n````text\n[not a link](missing.md)\n```python\nprint('inside')\n```\n````\nafter"

        stripped = strip_fenced_blocks(text)

        self.assertNotIn("missing.md", stripped)
        self.assertIn("before", stripped)
        self.assertIn("after", stripped)

    def test_fence_stripper_handles_closing_fence_at_eof(self) -> None:
        text = "before\n```text\n[not a link](missing.md)\n```"

        stripped = strip_fenced_blocks(text)

        self.assertNotIn("missing.md", stripped)
        self.assertIn("before", stripped)

    def test_prompt_substring_does_not_infer_pr_workflow(self) -> None:
        contribution = infer_user_contribution(make_exchange("Update the deep research prompt"))

        self.assertEqual(contribution, "Supplied task direction, constraints, or review feedback.")

    def test_pr_word_infers_repository_workflow(self) -> None:
        contribution = infer_user_contribution(make_exchange("Write the PR and trigger a code review"))

        self.assertEqual(contribution, "Asked Codex to inspect GitHub state and unblock the repository workflow.")

    def test_legitimate_substring_does_not_infer_git_workflow(self) -> None:
        contribution = infer_codex_contribution(make_exchange("Review", "This is a legitimate publication artifact."))

        self.assertEqual(contribution, "Performed repo analysis, implementation, validation, or synthesis in response.")

    def test_git_word_infers_repository_workflow(self) -> None:
        contribution = infer_codex_contribution(make_exchange("Review", "I checked git status and the branch."))

        self.assertEqual(contribution, "Inspected repository/GitHub state and adjusted branch or PR hygiene.")

    def test_public_sanitizer_removes_bare_users_path_marker(self) -> None:
        sanitized = public_sanitize_text("Publication scan found no `/Users/` paths.")

        self.assertNotIn("/Users/", sanitized)
        self.assertIn("[LOCAL_USER_PATH]", sanitized)

    def test_public_sanitizer_handles_username_agnostic_repo_paths(self) -> None:
        sanitized = public_sanitize_text(
            "See /Users/example/repos/seelinks/README.md and /Users/example/Downloads/Hackathon 20260416.docx"
        )

        self.assertIn("[PRIVATE_REFERENCE_REPO]/README.md", sanitized)
        self.assertIn("[LOCAL_SOURCE_WRITEUP]", sanitized)
        self.assertNotIn("/Users/", sanitized)
        self.assertNotIn("example", sanitized)

    def test_public_sanitizer_handles_current_home_repo_paths(self) -> None:
        sanitized = public_sanitize_text(f"Check {Path.home()}/repos/mcp-geo/README.md")

        self.assertIn("[LOCAL_PRIOR_WORK_REPO]/README.md", sanitized)
        self.assertNotIn(str(Path.home()), sanitized)

    def test_public_sanitizer_removes_local_state_filename(self) -> None:
        sanitized = public_sanitize_text("Remove .DS_Store before committing.")

        self.assertNotIn(".DS_Store", sanitized)
        self.assertIn("[LOCAL_STATE_FILE]", sanitized)


if __name__ == "__main__":
    unittest.main()
