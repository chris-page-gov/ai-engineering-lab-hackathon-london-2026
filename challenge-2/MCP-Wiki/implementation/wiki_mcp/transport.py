"""stdio and local HTTP transports for the Challenge 2 Wiki MCP server."""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .core import AuditLogger, WikiKnowledgeBase, WikiMcpServer


def build_server(
    *,
    repo_root: Path,
    challenge_root: Path,
    audit_path: Path | None = None,
    semantic_model_id: str = "challenge2-local-hash-v1",
) -> WikiMcpServer:
    audit = AuditLogger(audit_path)
    kb = WikiKnowledgeBase(
        repo_root=repo_root,
        challenge_root=challenge_root,
        audit=audit,
        semantic_model_id=semantic_model_id,
    )
    return WikiMcpServer(kb)


def run_stdio(server: WikiMcpServer) -> int:
    for raw_line in sys.stdin:
        if not raw_line.strip():
            continue
        try:
            request = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}
        else:
            response = server.handle(request)
        if response is not None:
            print(json.dumps(response, separators=(",", ":")), flush=True)
    return 0


def make_http_handler(
    server: WikiMcpServer,
    *,
    allowed_origins: set[str] | None = None,
    bearer_token: str | None = None,
) -> type[BaseHTTPRequestHandler]:
    origins = allowed_origins or set()

    class WikiMcpHttpHandler(BaseHTTPRequestHandler):
        server_version = "Challenge2WikiMCP/0.1"

        def do_OPTIONS(self) -> None:  # noqa: N802 - stdlib method name.
            if not self._origin_allowed():
                self._write_json(403, {"error": "origin_not_allowed"})
                return
            self.send_response(204)
            self._cors_headers()
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802 - stdlib method name.
            parsed = urlparse(self.path)
            if parsed.path == "/health":
                self._write_json(200, {"status": "ok", "server": server.initialize()["serverInfo"]})
                return
            if parsed.path == "/manifest":
                self._write_json(
                    200,
                    {
                        "server": server.initialize()["serverInfo"],
                        "tools": server.tools(),
                        "resources": server.resources(),
                        "prompts": server.prompts(),
                    },
                )
                return
            self._write_json(404, {"error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802 - stdlib method name.
            parsed = urlparse(self.path)
            if parsed.path != "/mcp":
                self._write_json(404, {"error": "not_found"})
                return
            if not self._origin_allowed():
                self._write_json(403, {"error": "origin_not_allowed"})
                return
            if not self._authorized():
                self._write_json(401, {"error": "unauthorized"})
                return
            try:
                length = int(self.headers.get("Content-Length") or "0")
            except ValueError:
                self._write_json(400, {"error": "bad_content_length"})
                return
            if length <= 0 or length > 2_000_000:
                self._write_json(413, {"error": "invalid_request_size"})
                return
            try:
                request = json.loads(self.rfile.read(length).decode("utf-8"))
            except json.JSONDecodeError as exc:
                self._write_json(400, {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}})
                return
            response = server.handle(request)
            self._write_json(200, response or {})

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - stdlib signature.
            return

        def _origin_allowed(self) -> bool:
            if not origins:
                return True
            origin = self.headers.get("Origin")
            return origin is None or origin in origins

        def _authorized(self) -> bool:
            if not bearer_token:
                return True
            return self.headers.get("Authorization") == f"Bearer {bearer_token}"

        def _cors_headers(self) -> None:
            origin = self.headers.get("Origin")
            if origin and (not origins or origin in origins):
                self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Headers", "authorization, content-type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

        def _write_json(self, status: int, payload: dict[str, Any]) -> None:
            data = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self._cors_headers()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    return WikiMcpHttpHandler


def run_http(
    server: WikiMcpServer,
    *,
    host: str,
    port: int,
    allowed_origins: set[str] | None = None,
    bearer_token: str | None = None,
) -> int:
    handler = make_http_handler(server, allowed_origins=allowed_origins, bearer_token=bearer_token)
    httpd = ThreadingHTTPServer((host, port), handler)
    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()
    return 0
