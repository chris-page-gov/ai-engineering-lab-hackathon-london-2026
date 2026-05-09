# Stage 5 prompt: Capability and benchmark analysis

## Goal

Explain what coding benchmarks show, what they miss, and why local evaluation matters.

## Output

Create or update:

```text
research/hmrc-beyond-hype/04_agentic_coding_capabilities.md
```

## Cover

1. HumanEval and early code-generation benchmarks.
2. SWE-bench and repository-level issue resolution.
3. SWE-bench Verified and human validation.
4. SWE-bench Live or equivalent contamination-resistant approaches.
5. Long-task autonomy and time-horizon measures.
6. Why benchmark performance is not the same as safe production readiness.
7. What capabilities matter for public-sector engineering but are usually absent from benchmarks.

## Create a section titled

```text
Why benchmark scores should not be treated as procurement evidence
```

Include:

- benchmark contamination;
- stale tasks;
- flawed or incomplete tests;
- narrow language and repository coverage;
- hidden scaffolding;
- model-specific tool environments;
- lack of data-governance evaluation;
- lack of security evaluation;
- lack of accessibility evaluation;
- mismatch with public-sector legacy estates;
- mismatch with operational service ownership.

## Local evaluation recommendations

End with recommendations for a local evaluation protocol:

- representative backlog tasks;
- fixed acceptance criteria;
- human-blind review where possible;
- security checks;
- accessibility checks;
- CI/CD checks;
- cost and time measurement;
- defect and rework tracking;
- audit logs;
- comparison to non-agent baseline;
- explicit decision criteria for adoption, restriction, or rejection.

## Rules

- Do not use benchmark ranking as proof of production readiness.
- Do not rely on vendor benchmark claims without independent context.
- Explain benchmark limitations in plain English.
