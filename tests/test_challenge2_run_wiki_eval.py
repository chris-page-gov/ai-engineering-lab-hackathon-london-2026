from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_WIKI_EVAL_SCRIPT = REPO_ROOT / "challenge-2" / "tools" / "run_wiki_eval.py"

spec = importlib.util.spec_from_file_location("run_wiki_eval", RUN_WIKI_EVAL_SCRIPT)
assert spec and spec.loader
run_wiki_eval = importlib.util.module_from_spec(spec)
sys.modules["run_wiki_eval"] = run_wiki_eval
spec.loader.exec_module(run_wiki_eval)


class Challenge2RunWikiEvalTest(unittest.TestCase):
    def test_repo_state_records_missing_git_as_non_fatal_metadata(self) -> None:
        with mock.patch.object(run_wiki_eval.subprocess, "run", side_effect=FileNotFoundError("git")):
            state = run_wiki_eval._repo_state(REPO_ROOT)

        self.assertFalse(state["git_available"])
        self.assertEqual(state["commit"], run_wiki_eval.GIT_UNAVAILABLE)
        self.assertEqual(state["branch"], run_wiki_eval.GIT_UNAVAILABLE)
        self.assertIsNone(state["dirty"])


if __name__ == "__main__":
    unittest.main()
