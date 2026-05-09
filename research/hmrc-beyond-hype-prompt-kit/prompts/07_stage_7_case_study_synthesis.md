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
