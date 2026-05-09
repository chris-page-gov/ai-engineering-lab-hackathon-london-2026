# HMRC Beyond the Hype research prompt kit

This folder is designed to be expanded directly into the source repository:

`https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026.git`

It contains a Codex-ready research brief, context files, Stage 1-8 prompts, and templates for the evidence register and claims matrix.

## Intended use

1. Clone the source repository.
2. Expand this folder into the repository root.
3. Open `research/hmrc-beyond-hype-prompt-kit/prompts/00_master_prompt.md`.
4. Give the master prompt to Codex.
5. Then either:
   - give Codex each stage prompt in order; or
   - give Codex `prompts/99_all_prompts_combined.md` as a single long unattended research handoff.

The research outputs should be written by Codex to:

`research/hmrc-beyond-hype/`

The prompt kit itself should remain in:

`research/hmrc-beyond-hype-prompt-kit/`

## Included files

```text
research/hmrc-beyond-hype-prompt-kit/
  README.md
  context/
    project_context.md
    research_method_and_evidence_rules.md
    seed_source_list.md
  prompts/
    00_master_prompt.md
    01_stage_1_repository_forensic_extraction.md
    02_stage_2_external_source_discovery.md
    03_stage_3_timeline_reconstruction.md
    04_stage_4_empirical_evidence_synthesis.md
    05_stage_5_capability_and_benchmark_analysis.md
    06_stage_6_security_governance_public_sector.md
    07_stage_7_case_study_synthesis.md
    08_stage_8_public_sector_operating_model.md
    99_all_prompts_combined.md
  templates/
    source_register_template.csv
    claims_matrix_template.md
```

## Boundary

This kit is for research planning and evidence collection. It does not ask Codex to change the product or application code. It tells Codex to inspect the repository, extract evidence, build a source register, and prepare an evidence-led research pack.
