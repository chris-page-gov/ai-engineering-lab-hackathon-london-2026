# Stage 6 prompt: Security, governance, and public-sector controls

## Goal

Create a public-sector safe-use framework for AI coding agents.

## Output

Create or update:

```text
research/hmrc-beyond-hype/05_security_governance_public_sector.md
```

## Risk taxonomy

Include at least:

- insecure generated code;
- hallucinated APIs or dependencies;
- vulnerable dependency introduction;
- supply-chain risk;
- prompt injection;
- data leakage;
- secret exposure;
- excessive permissions;
- unsafe network access;
- unsafe shell command execution;
- weak CI/CD;
- lack of auditability;
- unclear accountability;
- accessibility and equality impacts;
- privacy and data-protection risks;
- policy drift where teams rely on generated output without adequate review.

## Controls

Include at least:

- sandboxing;
- least privilege;
- no production secrets in agent environments;
- network access off by default or tightly approved;
- approval for external access and privileged commands;
- branch protections;
- mandatory human review;
- generated-code scanning;
- dependency scanning;
- static analysis;
- threat modelling;
- tests and coverage expectations;
- accessibility checks;
- provenance and audit logs;
- clear owner for final decisions;
- incident response and rollback;
- procurement and supplier assurance questions.

## Map controls to public-sector guidance

Map controls to, where sources are found and verified:

- UK Government AI Playbook;
- NCSC secure AI development guidance;
- UK Secure by Design policy;
- Government Service Standard;
- repo-specific security assessment.

## Practical checklist

Create a checklist titled:

```text
Before using a coding agent on public-sector work, have we...?
```

Make it usable by a delivery team, not only a security team.

## Rules

- Do not present AI-generated code as inherently safe.
- Do not imply that agent sandboxing alone solves security risk.
- Make accountability explicit.
- Use official guidance where possible.
- Separate what is mandatory under cited guidance from recommended local practice.
