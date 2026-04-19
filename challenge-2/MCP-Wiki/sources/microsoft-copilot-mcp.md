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
search_terms:
  - "Microsoft Copilot MCP"
  - "Copilot Studio Streamable HTTP"
  - "Microsoft 365 Copilot MCP plugin"
  - "MCP authentication"
related:
  - "bibliography.md"
  - "../implementation-plan.md"
  - "../security-model.md"
  - "../architecture.md"
---

# Microsoft Copilot MCP Integration Sources

The research report concludes that Microsoft 365 Copilot and Copilot Studio need a remote Streamable HTTP MCP endpoint, not a local stdio server.

The accepted target authentication pattern is OAuth 2.0 or Microsoft Entra ID / SSO. See [authentication options](../authentication-options.md) for the evaluated alternatives and caveats around API keys, bearer tokens, and anonymous smoke tests.

The first validation path is Copilot Studio direct MCP connection. Move to Agents Toolkit packaging or a custom connector only if direct connection cannot deliver the required tools, resources, authentication, or governance behaviour.

| Source | URL | Relevance |
| --- | --- | --- |
| Copilot Studio MCP connection guidance | [learn.microsoft.com](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp) | Target host integration path. |
| Microsoft 365 Copilot MCP plugin guidance | [learn.microsoft.com](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/build-mcp-plugins) | Packaging and validation route for Microsoft hosts. |
| Microsoft 365 Copilot authentication guidance | [learn.microsoft.com](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api-plugin-authentication) | Authentication caveats for agents and MCP/API plugins. |

## Local Validation Context

Personal OneDrive folder discovery and OneDrive share links did not provide reliable M365 Copilot grounding for this repo. The current working workaround is GitHub permalinks plus copied context excerpts, but the proper target is an MCP endpoint that exposes controlled wiki tools.

## Related

- [Bibliography](bibliography.md)
- [Authentication options](../authentication-options.md)
- [Implementation plan](../implementation-plan.md)
- [Security model](../security-model.md)
- [MCP specification sources](mcp-specification.md)
