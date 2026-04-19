---
title: "Copilot Studio MCP Authentication Options"
note_type: "decision-support"
status: "accepted-options-evaluation"
tags:
  - "mcp"
  - "authentication"
  - "copilot-studio"
  - "streamable-http"
search_terms:
  - "Copilot Studio MCP authentication"
  - "OAuth 2.0 MCP"
  - "Entra SSO MCP"
  - "API key MCP caveat"
related:
  - "security-model.md"
  - "implementation-plan.md"
  - "sources/microsoft-copilot-mcp.md"
  - "decision-record.md"
---

# Copilot Studio MCP Authentication Options

This note evaluates authentication choices for a Copilot Studio-facing Streamable HTTP MCP endpoint. The endpoint is expected to expose a read-only Challenge 2 wiki surface, not the full repository.

## Option Evaluation

| Option | Fit | Benefits | Risks and Caveats | Use |
| --- | --- | --- | --- | --- |
| No authentication | Low for internet-facing use | Fastest local and tunnel smoke tests; simplest Copilot Studio proof of connection | Not suitable for a public or government-style endpoint; relies entirely on network controls and obscurity | Local-only or temporary proof of transport |
| Static bearer token | Medium for internal smoke tests | Simple to put behind a gateway or reverse proxy; matches some reference implementation patterns | Shared secret lifecycle, rotation, leakage, and limited user attribution; not ideal for Microsoft 365 plugin packaging | Short-lived internal smoke or private tunnel only |
| API key through Copilot Studio | Low-medium | Some Copilot Studio connection paths expose API-key-style choices | Microsoft guidance is inconsistent across Copilot Studio, custom connector, and Microsoft 365 Copilot plugin paths; weak principal-level audit | Avoid as default; use only if a specific host path requires it and the limitation is documented |
| OAuth 2.0 authorization-code flow | High | Standards-based, supports real principal identity, consent, expiry, revocation, and stronger audit | More setup effort; requires hosted auth configuration, redirect handling, and token validation | Preferred default for a remotely exposed endpoint |
| Microsoft Entra ID / SSO | High where tenant integration is available | Best alignment to Microsoft 365 identity, conditional access, tenant governance, and user attribution | Requires tenant/admin setup and careful validation with the selected Copilot host | Preferred government/enterprise production path |
| Reverse proxy with network allowlist plus upstream OAuth | Medium-high as a deployment control | Adds origin, rate, size, IP, WAF, and logging controls outside the MCP process | Not a replacement for user auth; must avoid hiding caller identity from audit logs | Use as defence-in-depth around OAuth/Entra |
| Mutual TLS | Medium for service-to-service use | Strong client authentication and good fit for controlled infrastructure | Poor fit for end-user Copilot Studio onboarding unless the host supports it directly | Consider only for internal gateway-to-server legs |

## Decision

Use OAuth 2.0 or Microsoft Entra ID / SSO as the target pattern for a Copilot Studio-facing production endpoint. Anonymous access and static bearer tokens remain allowed only for local development, smoke testing, or tightly controlled private tunnels.

API-key authentication should not be the default because Microsoft support varies by host and packaging path. If a specific Copilot Studio path requires API key support, record that as a host-specific exception in [the decision record](decision-record.md).

## Implementation Implications

- Keep the core MCP server stateless and read-only.
- Validate `Origin` and host headers for Streamable HTTP.
- Record principal identity, authentication mode, transport, and request ID in audit events.
- Return deterministic citations and source IDs regardless of authentication pattern.
- Keep benchmark and gold-answer denylist controls independent of identity.
- Treat auth failures and policy denials as audit events.

## Related

- [Security model](security-model.md)
- [Implementation plan](implementation-plan.md)
- [Microsoft Copilot MCP source note](sources/microsoft-copilot-mcp.md)
- [MCP specification sources](sources/mcp-specification.md)
