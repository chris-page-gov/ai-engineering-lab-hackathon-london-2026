---
source_id: "MCP-SRC-SPEC"
title: "Model Context Protocol Specification Sources"
source_type: "external_specification"
license_status: "to_verify_before_snapshot"
publication_status: "citation-first"
tags:
  - "source"
  - "mcp"
  - "specification"
---

# Model Context Protocol Specification Sources

Use these sources to guide implementation. Do not copy specification bodies into this repository until license and update policy are recorded.

| Source | URL | Local Treatment | Notes |
| --- | --- | --- | --- |
| MCP specification | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) | Citation note | Source for protocol semantics and transport requirements. |
| MCP Streamable HTTP transport | [modelcontextprotocol.io/specification/2025-06-18/basic/transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) | Citation note | Important for Microsoft-compatible HTTP endpoint design. |
| MCP authorization | [modelcontextprotocol.io/specification/2025-06-18/basic/authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) | Citation note | Important for OAuth and remote server posture. |
| MCP Python SDK | [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | Candidate submodule after license review | Likely implementation dependency or reference. |
| MCP TypeScript SDK | [github.com/modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) | Reference only unless needed | Useful for comparing server/resource/tool patterns. |

## Update Policy

If we add a local snapshot or submodule, record:

- upstream URL;
- version, tag, or commit;
- license file;
- retrieval command;
- reason for local inclusion;
- update cadence.
