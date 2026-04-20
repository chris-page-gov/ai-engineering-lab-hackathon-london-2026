from __future__ import annotations

import json
import io
import os
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHALLENGE_ROOT = REPO_ROOT / "challenge-2"
IMPLEMENTATION_ROOT = CHALLENGE_ROOT / "MCP-Wiki" / "implementation"
MCP_SCRIPT = CHALLENGE_ROOT / "tools" / "wiki_mcp_server.py"
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from wiki_mcp import AccessDenied, AuditLogger, PathPolicy, WikiKnowledgeBase, WikiMcpServer, build_codex_mcp_prompt  # noqa: E402
from wiki_mcp.transport import build_server, make_http_handler, run_stdio  # noqa: E402
from http.server import ThreadingHTTPServer  # noqa: E402


class Challenge2WikiMcpCoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.audit_path = Path(self.tmp.name) / "audit.jsonl"
        self.kb = WikiKnowledgeBase(
            repo_root=REPO_ROOT,
            challenge_root=CHALLENGE_ROOT,
            audit=AuditLogger(self.audit_path),
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_loads_wiki_surface_and_excludes_benchmark(self) -> None:
        paths = {note.repo_rel_path for note in self.kb.notes}

        self.assertEqual(len(self.kb.sources), 43)
        self.assertIn("challenge-2/AGENTS.md", paths)
        self.assertIn("challenge-2/wiki/index.md", paths)
        self.assertIn("challenge-2/wiki/data/source-register.json", paths)
        self.assertNotIn("challenge-2/wiki/evaluation-benchmark.md", paths)

    def test_path_policy_denies_unsafe_reads(self) -> None:
        policy = PathPolicy(repo_root=REPO_ROOT, challenge_root=CHALLENGE_ROOT)

        with self.assertRaisesRegex(AccessDenied, "gold-answer"):
            policy.resolve("challenge-2/wiki/evaluation-benchmark.md")
        with self.assertRaisesRegex(AccessDenied, "outside allowed"):
            policy.resolve("README.md")
        with self.assertRaisesRegex(AccessDenied, "outside allowed"):
            policy.resolve("challenge-2/MCP-Wiki/research/Challenge 2 Wiki MCP Server Research Report.pdf")

    def test_path_policy_denies_symlink_and_oversized_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            challenge = repo / "challenge-2"
            wiki = challenge / "wiki"
            wiki.mkdir(parents=True)
            (challenge / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
            (wiki / "evaluation-benchmark.md").write_text("gold", encoding="utf-8")
            (wiki / "data").mkdir()
            (wiki / "data" / "source-register.json").write_text("[]", encoding="utf-8")
            target = wiki / "ok.md"
            target.write_text("ok", encoding="utf-8")
            unsupported = wiki / "attachment.pdf"
            unsupported.write_text("pdf", encoding="utf-8")
            link = wiki / "link.md"
            link.symlink_to(target)

            with self.assertRaisesRegex(AccessDenied, "Symlink"):
                PathPolicy(repo_root=repo, challenge_root=challenge).resolve(link)
            with self.assertRaisesRegex(AccessDenied, "extension"):
                PathPolicy(repo_root=repo, challenge_root=challenge).resolve(unsupported)
            with self.assertRaisesRegex(AccessDenied, "maximum"):
                PathPolicy(repo_root=repo, challenge_root=challenge, max_file_bytes=1).resolve(target)

    def test_search_supports_lexical_semantic_hybrid_and_filters(self) -> None:
        lexical = self.kb.search("Housing Benefit", mode="lexical", limit=5)
        semantic = self.kb.search("Housing Benefit", mode="semantic", limit=5)
        hybrid = self.kb.search("Housing Benefit", mode="hybrid", limit=5, tags=["housing-benefit"])
        source_filtered = self.kb.search("self employment", source_ids=["DOC-SB-006"], limit=3)

        self.assertEqual(lexical["mode"], "lexical")
        self.assertGreater(lexical["count"], 0)
        self.assertGreater(semantic["count"], 0)
        self.assertEqual(semantic["semantic_index"]["provider"], "deterministic-local-hash")
        self.assertGreater(hybrid["count"], 0)
        self.assertEqual(source_filtered["results"][0]["source_id"], "DOC-SB-006")
        self.assertTrue(all("evaluation-benchmark" not in item["path"] for item in hybrid["results"]))

    def test_read_note_offsets_frontmatter_and_backlinks(self) -> None:
        payload = self.kb.read_note(
            "challenge-2/wiki/sources/doc-hb-001-housing-benefit-check-if-you-re-eligible-gov-uk.md",
            max_bytes=200,
            include_frontmatter=True,
            include_backlinks=True,
        )

        self.assertEqual(payload["source_id"], "DOC-HB-001")
        self.assertTrue(payload["truncated"])
        self.assertIn("title", payload["frontmatter"])
        self.assertIsInstance(payload["backlinks"], list)
        self.assertEqual(payload["next_offset"], 200)

    def test_source_tools_return_public_provenance_without_raw_reads(self) -> None:
        listed = self.kb.list_sources(query="housing benefit", status="current", topic="housing-benefit", limit=5)
        source = self.kb.read_source("DOC-HB-001", include_note=True, max_bytes=500)
        register = self.kb.source_register()
        provenance = self.kb.explain_provenance(source_id="DOC-HB-001")

        self.assertGreater(listed["count"], 0)
        self.assertEqual(source["source_id"], "DOC-HB-001")
        self.assertIn("note_text", source)
        self.assertEqual(register["source_count"], 43)
        self.assertEqual(register["raw_json_path"], "challenge-2/wiki/data/source-register.json")
        self.assertFalse(provenance["raw_source_exposed"])
        self.assertIn("synthetic", provenance["synthetic_data_notice"])

    def test_context_pack_is_bounded_and_citable(self) -> None:
        pack = self.kb.build_context_pack(
            query="What are the housing benefit eligibility criteria?",
            source_ids=["DOC-HB-001"],
            limit=4,
            budget_bytes=2500,
        )

        self.assertEqual(pack["source_policy"]["denied_sources"][0], "challenge-2/wiki/evaluation-benchmark.md")
        self.assertGreater(pack["evidence_count"], 0)
        self.assertLessEqual(sum(len(item["excerpt"].encode("utf-8")) for item in pack["evidence"]), 2500)
        self.assertTrue(any(item["source_id"] == "DOC-HB-001" for item in pack["evidence"]))

    def test_context_pack_budget_is_enforced_in_utf8_bytes(self) -> None:
        pack = self.kb.build_context_pack(
            source_ids=["UF-WELSH-LANGUAGE-STANDARDS-COMPLIANCE-REPORT-2023"],
            limit=1,
            budget_bytes=1000,
        )

        self.assertEqual(pack["evidence_count"], 1)
        excerpt = pack["evidence"][0]["excerpt"]
        self.assertLessEqual(len(excerpt.encode("utf-8")), 1000)
        self.assertTrue(pack["evidence"][0]["truncated"])

    def test_audit_log_records_allowed_and_denied_events(self) -> None:
        self.kb.search("procurement", limit=1)
        server = WikiMcpServer(self.kb)
        denied = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "wiki.read", "arguments": {"path": "challenge-2/wiki/evaluation-benchmark.md"}},
            }
        )
        summary = self.kb.audit_summary()

        self.assertIn("error", denied)
        self.assertGreaterEqual(summary["event_types"]["wiki.search"], 1)
        self.assertGreaterEqual(summary["event_types"]["wiki.denied"], 1)

    def test_codex_mcp_prompt_includes_context_pack_and_schema(self) -> None:
        pack = self.kb.build_context_pack(query="right to buy", limit=2, budget_bytes=2000)
        prompt = build_codex_mcp_prompt("Q999", "Smoke", "What is right to buy?", pack)

        self.assertIn("Challenge 2 Wiki MCP server", prompt)
        self.assertIn('"question_id":"Q000"', prompt)
        self.assertIn("MCP context pack audit seed", prompt)
        self.assertIn("Mandatory validation step", prompt)
        self.assertIn("withheld from prompt", prompt)
        self.assertIn("right to buy", prompt.casefold())


class Challenge2WikiMcpProtocolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.kb = WikiKnowledgeBase(
            repo_root=REPO_ROOT,
            challenge_root=CHALLENGE_ROOT,
            audit=AuditLogger(Path(self.tmp.name) / "audit.jsonl"),
        )
        self.server = WikiMcpServer(self.kb)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_json_rpc_tools_resources_and_prompts(self) -> None:
        initialize = self.server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        tools = self.server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        resource = self.server.handle(
            {"jsonrpc": "2.0", "id": 3, "method": "resources/read", "params": {"uri": "wiki://index"}}
        )
        prompt = self.server.handle(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "prompts/get",
                "params": {"name": "wiki.answer_question", "arguments": {"question": "What is DHP?"}},
            }
        )
        notification = self.server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"})

        self.assertEqual(initialize["result"]["serverInfo"]["name"], "challenge2-wiki-mcp")
        tool_names = {tool["name"] for tool in tools["result"]["tools"]}
        self.assertIn("wiki.find_by_source_id", tool_names)
        self.assertIn("Challenge 2 Knowledge Base Index", resource["result"]["contents"][0]["text"])
        self.assertIn("context pack", prompt["result"]["messages"][0]["content"]["text"])
        self.assertIsNone(notification)

    def test_json_rpc_call_aliases_and_errors(self) -> None:
        register = self.server.handle(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "wiki.read_source_register", "arguments": {}},
            }
        )
        source = self.server.handle(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "wiki.find_by_source_id", "arguments": {"source_id": "DOC-HB-001"}},
            }
        )
        missing_method = self.server.handle({"jsonrpc": "2.0", "id": 3, "method": "missing", "params": {}})
        missing_tool = self.server.handle(
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "missing", "arguments": {}}}
        )

        self.assertEqual(json.loads(register["result"]["content"][0]["text"])["source_count"], 43)
        self.assertEqual(json.loads(source["result"]["content"][0]["text"])["source_id"], "DOC-HB-001")
        self.assertEqual(missing_method["error"]["code"], -32601)
        self.assertIn("Unknown tool", missing_tool["error"]["message"])

    def test_json_rpc_rejects_non_object_requests_and_invalid_params(self) -> None:
        non_object = self.server.handle([])
        missing_method = self.server.handle({"jsonrpc": "2.0", "id": 1, "params": {}})
        invalid_params = self.server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": []})
        invalid_arguments = self.server.handle(
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "wiki.search", "arguments": []}}
        )

        self.assertEqual(non_object["error"]["code"], -32600)
        self.assertEqual(missing_method["error"]["code"], -32600)
        self.assertEqual(invalid_params["error"]["code"], -32602)
        self.assertEqual(invalid_arguments["error"]["code"], -32602)

    def test_stdio_script_smoke(self) -> None:
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "wiki.read", "arguments": {"path": "challenge-2/wiki/evaluation-benchmark.md"}},
            },
        ]
        proc = subprocess.run(
            [
                sys.executable,
                str(MCP_SCRIPT),
                "--transport",
                "stdio",
                "--audit-path",
                str(Path(self.tmp.name) / "stdio-audit.jsonl"),
            ],
            input="\n".join(json.dumps(item) for item in requests) + "\n",
            text=True,
            capture_output=True,
            cwd=REPO_ROOT,
            check=False,
            timeout=10,
        )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        responses = [json.loads(line) for line in proc.stdout.splitlines()]
        self.assertEqual(responses[0]["result"]["serverInfo"]["name"], "challenge2-wiki-mcp")
        self.assertEqual(responses[1]["error"]["code"], -32001)

    def test_http_script_rejects_missing_bearer_token_env(self) -> None:
        env = dict(os.environ)
        env.pop("CHALLENGE2_MISSING_TOKEN", None)
        proc = subprocess.run(
            [
                sys.executable,
                str(MCP_SCRIPT),
                "--transport",
                "http",
                "--bearer-token-env",
                "CHALLENGE2_MISSING_TOKEN",
                "--port",
                "0",
            ],
            text=True,
            capture_output=True,
            cwd=REPO_ROOT,
            check=False,
            timeout=10,
            env=env,
        )

        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("--bearer-token-env 'CHALLENGE2_MISSING_TOKEN' is unset or empty", proc.stderr)

    def test_http_transport_health_manifest_post_and_guards(self) -> None:
        handler = make_http_handler(
            self.server,
            allowed_origins={"https://allowed.example"},
            bearer_token="test-token",
        )
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{httpd.server_address[1]}"
        try:
            health = self._get_json(f"{base}/health")
            manifest = self._get_json(f"{base}/manifest")
            post = self._post_json(
                f"{base}/mcp",
                {"jsonrpc": "2.0", "id": 1, "method": "resources/read", "params": {"uri": "wiki://agents"}},
                headers={"Origin": "https://allowed.example", "Authorization": "Bearer test-token"},
            )
            notification_status, notification_body = self._post_json_status(
                f"{base}/mcp",
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                headers={"Origin": "https://allowed.example", "Authorization": "Bearer test-token"},
            )

            self.assertEqual(health["status"], "ok")
            self.assertTrue(any(tool["name"] == "wiki.search" for tool in manifest["tools"]))
            self.assertIn("Challenge 2 LLM Wiki Operating Rules", post["result"]["contents"][0]["text"])
            self.assertEqual(notification_status, 204)
            self.assertEqual(notification_body, b"")
            with self.assertRaises(urllib.error.HTTPError) as origin_error:
                self._post_json(
                    f"{base}/mcp",
                    {"jsonrpc": "2.0", "id": 2, "method": "ping"},
                    headers={"Origin": "https://blocked.example", "Authorization": "Bearer test-token"},
                )
            self.assertEqual(origin_error.exception.code, 403)
            origin_error.exception.close()
            with self.assertRaises(urllib.error.HTTPError) as auth_error:
                self._post_json(
                    f"{base}/mcp",
                    {"jsonrpc": "2.0", "id": 3, "method": "ping"},
                    headers={"Origin": "https://allowed.example"},
                )
            self.assertEqual(auth_error.exception.code, 401)
            auth_error.exception.close()
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=5)

    def test_stdio_transport_loop_handles_parse_errors_and_notifications(self) -> None:
        server = build_server(
            repo_root=REPO_ROOT,
            challenge_root=CHALLENGE_ROOT,
            audit_path=Path(self.tmp.name) / "transport-audit.jsonl",
        )
        stdin = io.StringIO(
            "\n".join(
                [
                    "{not-json}",
                    json.dumps({"jsonrpc": "2.0", "id": 1, "method": "ping"}),
                    json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}),
                ]
            )
            + "\n"
        )
        stdout = io.StringIO()
        old_stdin, old_stdout = sys.stdin, sys.stdout
        try:
            sys.stdin, sys.stdout = stdin, stdout
            exit_code = run_stdio(server)
        finally:
            sys.stdin, sys.stdout = old_stdin, old_stdout

        responses = [json.loads(line) for line in stdout.getvalue().splitlines()]
        self.assertEqual(exit_code, 0)
        self.assertEqual(responses[0]["error"]["code"], -32700)
        self.assertEqual(responses[1]["result"], {})
        self.assertEqual(len(responses), 2)

    def test_http_transport_options_and_invalid_requests(self) -> None:
        handler = make_http_handler(self.server)
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{httpd.server_address[1]}"
        try:
            options_request = urllib.request.Request(f"{base}/mcp", method="OPTIONS")
            with urllib.request.urlopen(options_request, timeout=5) as response:
                self.assertEqual(response.status, 204)

            with self.assertRaises(urllib.error.HTTPError) as get_error:
                self._get_json(f"{base}/missing")
            self.assertEqual(get_error.exception.code, 404)
            get_error.exception.close()

            with self.assertRaises(urllib.error.HTTPError) as path_error:
                self._post_json(f"{base}/missing", {"jsonrpc": "2.0", "id": 1, "method": "ping"}, headers={})
            self.assertEqual(path_error.exception.code, 404)
            path_error.exception.close()

            empty_request = urllib.request.Request(
                f"{base}/mcp",
                data=b"",
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(urllib.error.HTTPError) as size_error:
                urllib.request.urlopen(empty_request, timeout=5)
            self.assertEqual(size_error.exception.code, 413)
            size_error.exception.close()

            bad_json_request = urllib.request.Request(
                f"{base}/mcp",
                data=b"{",
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(urllib.error.HTTPError) as json_error:
                urllib.request.urlopen(bad_json_request, timeout=5)
            self.assertEqual(json_error.exception.code, 400)
            json_error.exception.close()
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=5)

    @staticmethod
    def _get_json(url: str) -> dict:
        with urllib.request.urlopen(url, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))

    @staticmethod
    def _post_json(url: str, payload: dict, *, headers: dict[str, str]) -> dict:
        _, body = Challenge2WikiMcpProtocolTest._post_json_status(url, payload, headers=headers)
        return json.loads(body.decode("utf-8"))

    @staticmethod
    def _post_json_status(url: str, payload: dict, *, headers: dict[str, str]) -> tuple[int, bytes]:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json", **headers},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, response.read()


if __name__ == "__main__":
    unittest.main()
