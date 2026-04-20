from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MCP_SCRIPT = REPO_ROOT / "challenge-2" / "tools" / "workbench_mcp.py"


class Challenge2WorkbenchMcpTest(unittest.TestCase):
    def test_stdio_server_searches_reads_and_builds_context(self) -> None:
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "workbench.search_sources",
                    "arguments": {"query": "DOC-HB-002", "limit": 5},
                },
            },
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "workbench.read_source",
                    "arguments": {"source_id": "DOC-HB-002", "include_note": True, "max_bytes": 1000},
                },
            },
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "workbench.build_context",
                    "arguments": {"source_ids": ["DOC-HB-002"]},
                },
            },
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "workbench.read_source",
                    "arguments": {
                        "source_id": "UF-WELSH-LANGUAGE-STANDARDS-COMPLIANCE-REPORT-2023",
                        "include_note": True,
                        "max_bytes": 1000,
                    },
                },
            },
        ]
        proc = subprocess.run(
            [sys.executable, str(MCP_SCRIPT)],
            input="\n".join(json.dumps(request) for request in requests) + "\n",
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=False,
            timeout=10,
        )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        responses = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
        self.assertEqual(len(responses), 5)

        search_payload = json.loads(responses[1]["result"]["content"][0]["text"])
        self.assertEqual(search_payload["sources"][0]["source_id"], "DOC-HB-002")

        read_payload = json.loads(responses[2]["result"]["content"][0]["text"])
        self.assertIn("synthetic", read_payload["synthetic_data_notice"])
        self.assertIn("note_text", read_payload)

        context_payload = json.loads(responses[3]["result"]["content"][0]["text"])
        self.assertEqual(context_payload["sources"][0]["source_id"], "DOC-HB-002")
        self.assertIn("source_id", context_payload["instructions"]["citation_policy"])

        welsh_payload = json.loads(responses[4]["result"]["content"][0]["text"])
        self.assertLessEqual(len(welsh_payload["note_text"].encode("utf-8")), 1000)
        self.assertTrue(welsh_payload["truncated"])


if __name__ == "__main__":
    unittest.main()
