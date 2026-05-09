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
