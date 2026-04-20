from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPARE_SCRIPT = REPO_ROOT / "challenge-2" / "tools" / "compare_wiki_eval.py"

spec = importlib.util.spec_from_file_location("compare_wiki_eval", COMPARE_SCRIPT)
assert spec and spec.loader
compare_wiki_eval = importlib.util.module_from_spec(spec)
sys.modules["compare_wiki_eval"] = compare_wiki_eval
spec.loader.exec_module(compare_wiki_eval)


class Challenge2CompareWikiEvalTest(unittest.TestCase):
    def test_extract_visible_json_unwraps_cli_envelopes(self) -> None:
        answer = {
            "question_id": "Q001",
            "answer": "Use the generated wiki.",
            "cited_sources": ["challenge-2/wiki/architecture.md"],
            "caveats": [],
        }
        gemini_envelope = json.dumps({"session_id": "abc", "response": "```json\n" + json.dumps(answer) + "\n```"})
        claude_envelope = json.dumps({"type": "result", "result": "```json\n" + json.dumps(answer) + "\n```"})

        self.assertEqual(compare_wiki_eval.extract_visible_json(gemini_envelope), answer)
        self.assertEqual(compare_wiki_eval.extract_visible_json(claude_envelope), answer)

    def test_normalise_refs_extracts_embedded_wiki_paths(self) -> None:
        refs = compare_wiki_eval.normalise_refs(
            [
                "The evidence is in challenge-2/wiki/architecture.md and DOC-HB-001.",
                "Also cite challenge-2/AGENTS.md.",
            ]
        )

        self.assertIn("doc-hb-001".upper(), refs)
        self.assertIn("challenge-2/wiki/architecture.md", refs)
        self.assertIn("challenge-2/agents.md", refs)

    def test_classified_status_identifies_gemini_quota_exhaustion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            stderr = run_dir / "raw" / "gemini" / "Q037.stderr.txt"
            stderr.parent.mkdir(parents=True)
            stderr.write_text("reason: QUOTA_EXHAUSTED", encoding="utf-8")
            answer = compare_wiki_eval.ParsedAnswer(
                raw={"client": "gemini", "question_id": "Q037", "status": "failed"},
                visible_json=None,
                run_dir=run_dir,
            )

            self.assertEqual(compare_wiki_eval.classified_status(answer), "quota_exhausted")

    def test_mcp_tool_evidence_tolerates_malformed_audit_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            audit_path = run_dir / "raw" / "codex-mcp" / "Q001.mcp-audit.jsonl"
            audit_path.parent.mkdir(parents=True)
            audit_path.write_text(
                "\n".join(
                    [
                        json.dumps({"event_type": "wiki.search"}),
                        "{truncated",
                        json.dumps(["not", "an", "event"]),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            answer = compare_wiki_eval.ParsedAnswer(
                raw={"client": "codex-mcp", "question_id": "Q001", "status": "completed"},
                visible_json=None,
                run_dir=run_dir,
            )

            evidence = compare_wiki_eval.mcp_tool_evidence(run_dir, "codex-mcp", [answer])

            self.assertEqual(evidence["questions_with_mcp_audit"], 1)
            self.assertEqual(evidence["audit_event_counts"], {"wiki.search": 1})
            self.assertEqual(evidence["malformed_audit_lines"], 2)
            self.assertEqual(compare_wiki_eval.mcp_event_count(answer), 1)

    def test_apply_corrections_replaces_non_completed_base_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp) / "base"
            correction_dir = Path(tmp) / "correction"
            base_dir.mkdir()
            correction_dir.mkdir()
            base = compare_wiki_eval.ParsedAnswer(
                raw={"client": "codex-mcp", "question_id": "Q057", "status": "timeout"},
                visible_json=None,
                run_dir=base_dir,
            )
            correction = compare_wiki_eval.ParsedAnswer(
                raw={"client": "codex-mcp", "question_id": "Q057", "status": "completed"},
                visible_json={"question_id": "Q057", "answer": "Corrected", "cited_sources": []},
                run_dir=correction_dir,
            )

            effective, applied = compare_wiki_eval.apply_corrections([base], [correction])

            self.assertEqual(effective[0].status, "completed")
            self.assertEqual(applied[0]["base_status"], "timeout")
            self.assertEqual(applied[0]["correction_status"], "completed")

    def test_format_report_includes_rubric_leaderboard_when_scores_supplied(self) -> None:
        metrics = {
            "run": {"run_id": "test-run", "question_count": 1, "metadata": {}},
            "clients": {
                "codex": {
                    "answer_count": 1,
                    "completed": 1,
                    "parseable_json_percent": 100.0,
                    "avg_elapsed_seconds": 1.0,
                    "status_counts": {"completed": 1},
                    "citation_overlap": {"gold_ref_recall_percent": 100.0},
                    "mcp_tool_evidence": {
                        "questions_with_mcp_audit": 0,
                        "audit_event_counts": {},
                    },
                },
                "codex-mcp": {
                    "answer_count": 1,
                    "completed": 1,
                    "parseable_json_percent": 100.0,
                    "avg_elapsed_seconds": 1.0,
                    "status_counts": {"completed": 1},
                    "citation_overlap": {"gold_ref_recall_percent": 100.0},
                    "mcp_tool_evidence": {
                        "questions_with_mcp_audit": 1,
                        "audit_event_counts": {"wiki.search": 1},
                    },
                },
            },
            "rubric_scores": {
                "leaderboard": [
                    {
                        "client": "codex",
                        "scored_answers": 1,
                        "raw_points": 5.0,
                        "benchmark_max_points": 5,
                        "final_score_percent": 100.0,
                        "scored_subset_percent": 100.0,
                        "hallucination_count": 0,
                        "missed_source_risk_count": 0,
                    },
                    {
                        "client": "codex-mcp",
                        "scored_answers": 1,
                        "raw_points": 4.0,
                        "benchmark_max_points": 5,
                        "final_score_percent": 80.0,
                        "scored_subset_percent": 80.0,
                        "hallucination_count": 0,
                        "missed_source_risk_count": 1,
                    },
                ]
            },
        }

        report = compare_wiki_eval.format_report(
            Path("run"),
            metrics,
            [],
            baseline_client="codex",
            comparison_client="codex-mcp",
            smoke={},
        )

        self.assertIn("## Rubric-Scored Quality Leaderboard", report)
        self.assertIn("Rubric score: `codex` scored `5.0/5`", report)


if __name__ == "__main__":
    unittest.main()
