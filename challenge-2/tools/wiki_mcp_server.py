#!/usr/bin/env python3
"""Run the Challenge 2 read-only Wiki MCP server."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


CHALLENGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = CHALLENGE_ROOT.parent
IMPLEMENTATION_ROOT = CHALLENGE_ROOT / "MCP-Wiki" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from wiki_mcp.transport import build_server, run_http, run_stdio  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--challenge-root", type=Path, default=CHALLENGE_ROOT)
    parser.add_argument("--audit-path", type=Path, default=Path("/tmp/challenge2-wiki-mcp-audit/events.jsonl"))
    parser.add_argument("--semantic-model-id", default="challenge2-local-hash-v1")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--allowed-origin",
        action="append",
        default=[],
        help="Allowed HTTP Origin. May be repeated. Omit for local unrestricted HTTP.",
    )
    parser.add_argument(
        "--bearer-token-env",
        help="Optional environment variable containing a private smoke-test bearer token.",
    )
    args = parser.parse_args(argv)

    bearer_token = os.environ.get(args.bearer_token_env) if args.bearer_token_env else None
    server = build_server(
        repo_root=args.repo_root.resolve(),
        challenge_root=args.challenge_root.resolve(),
        audit_path=args.audit_path,
        semantic_model_id=args.semantic_model_id,
    )
    if args.transport == "stdio":
        return run_stdio(server)
    return run_http(
        server,
        host=args.host,
        port=args.port,
        allowed_origins=set(args.allowed_origin),
        bearer_token=bearer_token,
    )


if __name__ == "__main__":
    raise SystemExit(main())
