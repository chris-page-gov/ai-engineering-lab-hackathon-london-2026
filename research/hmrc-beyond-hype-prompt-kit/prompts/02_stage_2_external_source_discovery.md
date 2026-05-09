# Stage 2 prompt: External source discovery

## Goal

Build a high-quality source base on AI support for software engineering from 2021 to May 2026.

## Inputs

Use:

```text
research/hmrc-beyond-hype-prompt-kit/context/seed_source_list.md
research/hmrc-beyond-hype-prompt-kit/context/research_method_and_evidence_rules.md
```

## Source categories

Find and record sources in these categories.

### A. Product and capability timeline

Cover, where reliable sources are available:

- OpenAI Codex, ChatGPT coding, Codex CLI, and cloud Codex agent.
- GitHub Copilot, Copilot Chat, and Copilot coding agent.
- Anthropic Claude Code.
- Cognition Devin.
- Google Jules.
- Amazon CodeWhisperer and Amazon Q Developer.
- Cursor, Windsurf, and other agentic coding environments where reliable sources exist.

### B. Empirical productivity evidence

Find evidence on:

- Copilot productivity experiments.
- Field experiments in industry.
- METR or equivalent studies on real-world developer productivity.
- DORA or Google Cloud State of DevOps findings on AI adoption and software delivery.
- Developer-experience studies or surveys, clearly distinguishing self-report from measured outcomes.

### C. Benchmarks and capability evaluation

Find sources on:

- HumanEval.
- SWE-bench.
- SWE-bench Verified.
- SWE-bench Live or other contamination-resistant benchmarks.
- Time-horizon or long-task autonomy evaluations.
- Any credible critique of benchmark validity.

### D. Security and quality evidence

Find sources on:

- vulnerable AI-generated code;
- user overconfidence;
- hallucinated APIs and dependencies;
- supply-chain risk;
- CI/CD risk;
- prompt injection;
- agent sandboxing;
- approval policies;
- network access controls;
- secret handling;
- audit logs.

### E. Public-sector and government guidance

Find current public sources on:

- UK Government AI Playbook;
- NCSC secure AI development guidance;
- UK Secure by Design policy;
- Government Service Standard;
- relevant CDDO, DSIT, Cabinet Office, or HMRC-aligned public guidance.

## Output

Create or update:

```text
research/hmrc-beyond-hype/01_source_register.csv
research/hmrc-beyond-hype/appendices/b_search_queries.md
research/hmrc-beyond-hype/appendices/c_excluded_sources.md
```

For every source, record:

```text
source_id,title,author_or_org,publication_date,source_type,url,accessed_date,evidence_grade,claim_supported,relevant_quote_short,limitations_or_bias,used_in_sections,verification_status
```

## Rules

- Prefer primary sources.
- Use vendor documentation for release dates, capabilities, product architecture, and stated controls.
- Do not use vendor sources as independent evidence of productivity or safety.
- Use journalism only for market context or when no primary source exists.
- If a source is weak, record it in excluded sources or mark it as evidence grade D.
- If web access is unavailable, write exact search queries and mark the missing evidence clearly.
