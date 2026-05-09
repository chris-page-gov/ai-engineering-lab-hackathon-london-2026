# All prompts combined: HMRC Beyond the Hype research pack

Use this file when you want to give Codex one long unattended research handoff.

-----

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


-----

# Stage 1 prompt: Repository forensic extraction

## Goal

Extract the evidence already present in this repository about the AI Engineering Lab Codex Build.

## Inputs

Use the repository and the context files in:

```text
research/hmrc-beyond-hype-prompt-kit/context/
```

## Tasks

1. Inspect README files, AGENTS files, reports, evaluation documents, security assessments, postmortems, test files, and evaluation harness documentation.
2. Identify what the repository claims was built, when, by whom or by what workflow, and with what checks.
3. Extract evidence for:
   - the challenge or problem addressed;
   - source documents and knowledge-base construction;
   - evaluation harness and benchmark design;
   - user interface or workbench;
   - security assessment;
   - known gaps;
   - examples of Codex contribution modes;
   - evidence of human steering, review, constraints, and quality gates.
4. Create or update:

```text
research/hmrc-beyond-hype/06_repo_case_study_codex_build.md
research/hmrc-beyond-hype/appendices/d_claims_matrix.md
research/hmrc-beyond-hype/01_source_register.csv
```

5. Add every repo document used to `01_source_register.csv` as a repo-local source.
6. Create a clear repo-local evidence table with:
   - claim;
   - evidence file path;
   - supporting quotation or paraphrase;
   - confidence;
   - limitation.

## Rules

- Do not invent chronology.
- Use only repository evidence for repo-specific claims.
- Do not modify product or application code.
- Do not use secrets or private data.
- If a file looks generated, still record it, but note that it is generated or inferred if the repo indicates that.
- Preserve uncertainty.


-----

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


-----

# Stage 3 prompt: Timeline reconstruction

## Goal

Create a dated timeline showing the evolution from AI coding assistants to agentic software-engineering systems.

## Output

Create or update:

```text
research/hmrc-beyond-hype/02_timeline_ai_software_engineering.md
```

## Structure

Use this structure:

1. 2021-2022: code generation and autocomplete.
2. 2023: chat, repository context, pull-request support, documentation support, and SWE-bench.
3. 2024: agent framing and real-world issue-resolution benchmarks.
4. 2025: cloud, terminal, and asynchronous coding agents.
5. January-May 2026: multi-agent workflows, long-task autonomy, governance, benchmark contamination, and public-sector implications.

## For each milestone

Include:

- date;
- event;
- source;
- source type;
- what changed technically;
- why it matters;
- caveat or limitation.

## Required synthesis

End with a short synthesis using this idea:

“What changed is not merely model quality; it is the workflow boundary. The unit of interaction moved from token, to line, to function, to conversation, to issue, branch, pull request, and bounded task.”

## Rules

- Do not invent release dates.
- Use primary or official sources wherever possible.
- If a date is uncertain, say so and explain how to verify it.
- Label vendor claims as vendor claims.
- Keep public-sector relevance visible: explain why each shift matters to delivery teams, assurance teams, and service owners.


-----

# Stage 4 prompt: Empirical evidence synthesis

## Goal

Assess what is actually known about productivity, quality, and developer experience.

## Output

Create or update:

```text
research/hmrc-beyond-hype/03_empirical_evidence_productivity.md
```

## Required evidence table

Include a table with:

```text
study/source | setting | participants | task type | tool/model | measured outcome | result | limitations | relevance to public-sector engineering
```

## Compare at least

- bounded lab tasks;
- professional field experiments;
- experienced developers on mature codebases;
- self-reported adoption surveys;
- benchmark task performance;
- developer-experience evidence.

## Analysis requirements

Identify where the evidence conflicts.

Explain why findings may differ, including:

- greenfield versus brownfield work;
- simple versus complex tasks;
- novice versus expert;
- familiar versus unfamiliar codebase;
- quality bar;
- review burden;
- task decomposition;
- hidden costs from rework and assurance;
- incentives and measurement effects.

## Required conclusion

Produce a conclusion suitable for the paper:

“AI coding support is best understood as a conditional capability amplifier, not a uniform productivity multiplier.”

## Rules

- Do not average incompatible studies into one headline productivity number.
- Distinguish measured productivity from self-reported productivity.
- Distinguish speed of completion from quality-adjusted delivery.
- Distinguish benchmark performance from real-world delivery.
- Record source limitations in the source register.


-----

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


-----

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


-----

# Stage 7 prompt: Case-study synthesis

## Goal

Turn the AI Engineering Lab Codex Build into an evidence-led case study.

## Output

Create or update:

```text
research/hmrc-beyond-hype/06_repo_case_study_codex_build.md
```

This file may already exist from Stage 1. Refine it into a coherent case study.

## Use

Use only repo-local evidence for facts about the build, unless explicitly comparing the repo to external evidence.

## Suggested structure

1. Context: what the challenge was.
2. Build narrative: what was produced.
3. Human role:
   - intent;
   - constraints;
   - evidence standards;
   - review;
   - quality bar;
   - final accountability.
4. Agent role:
   - exploration;
   - implementation;
   - refactoring;
   - tests;
   - documentation;
   - evidence-pack generation.
5. Verification:
   - tests;
   - evaluation harness;
   - security checks;
   - known gaps.
6. Lessons:
   - what accelerated;
   - what still required human judgement;
   - what would be unsafe to generalise;
   - what would be needed for production.
7. Pull quotes:
   - short, cited quotations from repo reports.
8. “From typing to steering” interpretation:
   - explain how the case supports the talk title.

## Required table

Include a table:

```text
Codex contribution mode | repo evidence | value created | human control or review required | production-readiness caveat
```

## Rules

- Do not overstate the case study.
- Distinguish prototype evidence from production evidence.
- Make known gaps visible.
- Explain why a demo or hackathon success should not be treated as operational proof.


-----

# Stage 8 prompt: Public-sector operating model

## Goal

Create a practical model for using coding agents safely in government engineering teams.

## Output

Create or update:

```text
research/hmrc-beyond-hype/07_operating_model_for_public_sector_engineering.md
```

## Model structure

Create a five-layer model.

### 1. Task selection

Include:

- suitable tasks;
- unsuitable tasks;
- escalation triggers;
- examples from the repo case study;
- examples from typical public-sector software estates.

### 2. Agent environment

Include:

- sandbox;
- repository access;
- branch strategy;
- network access;
- secrets;
- dependency controls;
- logging;
- auditability;
- environment reset;
- isolation from production.

### 3. Prompting and steering

Include a reusable task prompt pattern with:

- problem statement;
- relevant files;
- constraints;
- acceptance criteria;
- tests to run;
- documentation to update;
- security requirements;
- accessibility requirements;
- data-protection constraints;
- expected output format;
- stop conditions.

### 4. Review and assurance

Include:

- diff review;
- tests;
- static analysis;
- dependency scanning;
- secret scanning;
- threat modelling;
- accessibility review;
- data protection review;
- operational readiness;
- service owner sign-off.

### 5. Learning loop

Include:

- measure time saved;
- measure defects and rework;
- track rejected agent output;
- maintain prompt patterns;
- update coding standards;
- maintain local evaluation set;
- compare results across teams;
- feed lessons into governance and procurement.

## RACI-style table

Include a RACI-style table for:

- developer;
- tech lead;
- security architect;
- product owner;
- delivery manager;
- SRO or service owner;
- data protection lead;
- accessibility lead;
- procurement or commercial role where relevant.

## Required closing section

Create a closing section titled:

```text
Minimum safe pilot for a government engineering team
```

Define a small, measurable, low-risk pilot that could be run before scaling adoption.

## Rules

- Keep this practical.
- Do not imply that every team should immediately adopt coding agents.
- Make adoption conditional on controls, evidence, and local evaluation.
- Make human accountability explicit.
-----
