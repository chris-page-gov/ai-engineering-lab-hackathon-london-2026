# Master prompt for Codex

You are an AI research engineer working inside this repository:

`https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026.git`

Create a rigorous, evidence-based research pack for a 15-minute HMRC “Beyond the Hype” talk titled:

**From Typing Code to Steering Agents: Lessons from the AI Engineering Lab Codex Build**

Subtitle:

**What coding assistants change, what they don’t, and how to use them safely in public-sector engineering.**

Use the context and rules in:

```text
research/hmrc-beyond-hype-prompt-kit/context/project_context.md
research/hmrc-beyond-hype-prompt-kit/context/research_method_and_evidence_rules.md
research/hmrc-beyond-hype-prompt-kit/context/seed_source_list.md
```

Write all research outputs under:

```text
research/hmrc-beyond-hype/
```

Do not modify product or application files unless explicitly required for safe inspection. Do not use or request secrets. Do not include private data. Use British English.

## Research questions

The research must answer:

1. What has happened, and when, in the advance from AI coding assistants to agentic AI systems that can write, test, and modify code across a repository?
2. What does the best available evidence say about productivity, quality, safety, security, developer experience, governance, and public-sector use?
3. What does this repository show about the AI Engineering Lab Codex Build as a case study in moving from typing code to steering agents?
4. What operating model should public-sector engineering teams use to adopt coding agents safely?

## Working rules

- Distinguish facts, empirical findings, benchmark results, vendor claims, interpretations, and recommendations.
- Prefer primary sources, credible research papers, official documentation, official government guidance, NCSC guidance, and reproducible benchmark papers.
- Vendor claims may be used for product release dates and documented capabilities, but label them as vendor claims.
- Do not over-claim benchmark results.
- Discuss contamination, staleness, task selection, hidden scaffolding, ecological validity, and the difference between benchmark performance and production readiness.
- Treat generated code as untrusted until reviewed, tested, scanned, and accepted by an accountable human owner.
- For repo-specific claims, use repository-local evidence.
- For public-sector recommendations, consider secure-by-design, auditability, privacy, accessibility, procurement, and operational ownership.
- If web access is unavailable, complete all repo-local work and write exact search queries and missing-source notes.

## Deliverables for this Stage 1-8 research pack

Create:

```text
research/hmrc-beyond-hype/
  00_research_brief.md
  01_source_register.csv
  02_timeline_ai_software_engineering.md
  03_empirical_evidence_productivity.md
  04_agentic_coding_capabilities.md
  05_security_governance_public_sector.md
  06_repo_case_study_codex_build.md
  07_operating_model_for_public_sector_engineering.md
  appendices/
    a_methods.md
    b_search_queries.md
    c_excluded_sources.md
    d_claims_matrix.md
```

## Minimum quality bar

Before finishing:

1. Ensure every major claim is traceable to a source-register entry.
2. Mark unverified or weak claims clearly.
3. Include URLs for all external sources.
4. Include limitations for each source.
5. Include repo-local file paths for repository evidence.
6. Include a list of claims safe to use in a public talk and claims not yet safe to use.
7. Do not present tool marketing claims as independent evidence of effectiveness.

## Execution order

Run the stage prompts in order:

1. Repository forensic extraction.
2. External source discovery.
3. Timeline reconstruction.
4. Empirical evidence synthesis.
5. Capability and benchmark analysis.
6. Security, governance, and public-sector controls.
7. Case-study synthesis.
8. Public-sector operating model.

Work unattended. Make reasonable progress with available evidence. Where evidence is missing, state what is missing and how to verify it.
