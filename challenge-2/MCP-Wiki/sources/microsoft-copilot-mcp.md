---
source_id: "MCP-SRC-MICROSOFT-COPILOT"
title: "Microsoft Copilot MCP Integration Sources"
source_type: "external_documentation"
license_status: "microsoft-docs-terms"
publication_status: "citation-only"
tags:
  - "source"
  - "microsoft-copilot"
  - "mcp"
---

# Microsoft Copilot MCP Integration Sources

The research report concludes that Microsoft 365 Copilot and Copilot Studio need a remote Streamable HTTP MCP endpoint, not a local stdio server.

| Source | URL | Relevance |
| --- | --- | --- |
| Copilot Studio MCP connection guidance | [learn.microsoft.com](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent) | Target host integration path. |
| Microsoft 365 Copilot extensibility | [learn.microsoft.com](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/) | Broader agent/plugin context. |
| Microsoft 365 Agents Toolkit | [learn.microsoft.com](https://learn.microsoft.com/en-us/microsoft-365/agents-toolkit/) | Packaging and validation route for Microsoft hosts. |

## Local Validation Context

Personal OneDrive folder discovery and OneDrive share links did not provide reliable M365 Copilot grounding for this repo. The current working workaround is GitHub permalinks plus copied context excerpts, but the proper target is an MCP endpoint that exposes controlled wiki tools.
