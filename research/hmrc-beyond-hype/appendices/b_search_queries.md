# Appendix B: Search Queries

Searches were run on 2026-05-09. Queries were used to verify dates, titles, capability claims, empirical evidence, and public-sector controls.

## Product Timeline

| Query | Purpose | Outcome |
|---|---|---|
| `OpenAI Codex HumanEval paper 2021` | Verify Codex and HumanEval paper metadata. | Used EXT-001. |
| `GitHub Copilot generally available June 2022` | Verify Copilot GA date and framing. | Used EXT-002. |
| `GitHub Copilot X March 2023 pull requests docs chat CLI` | Verify shift from autocomplete to broader developer workflow. | Used EXT-003. |
| `Cognition Devin AI software engineer March 2024` | Verify Devin announcement. | Used EXT-008. |
| `Amazon Q Developer generally available April 2024 CodeWhisperer` | Verify Q Developer GA and rename context. | Used EXT-009 and EXT-028. |
| `Anthropic Claude Code Claude 3.7 February 2025` | Verify Claude Code public positioning. | Used EXT-010 and EXT-018. |
| `OpenAI Introducing Codex May 2025 coding agent` | Verify OpenAI Codex cloud agent announcement. | Used EXT-011. |
| `OpenAI Codex changelog CLI IDE cloud tasks May 2026` | Check current Codex product state. | Used EXT-012. |
| `Google Jules public beta May 2025` | Verify Jules beta date. | Used EXT-014. |
| `Google Jules now available August 2025` | Verify Jules out-of-beta date. | Used EXT-015. |
| `GitHub Copilot coding agent May 2025 press release` | Verify Copilot coding agent announcement. | Used EXT-016. |

## Empirical Evidence And Benchmarks

| Query | Purpose | Outcome |
|---|---|---|
| `Peng Kalliamvakou Cihon Demirer impact of AI on developer productivity GitHub Copilot 2023 arxiv` | Verify controlled Copilot productivity study. | Used EXT-005. |
| `METR early 2025 AI experienced open source developers productivity study` | Verify experienced-developer RCT. | Used EXT-020. |
| `DORA 2025 AI software development report AI adoption throughput stability` | Verify DORA findings. | Used EXT-022. |
| `SWE-bench real world GitHub issues arxiv 2023` | Verify SWE-bench paper. | Used EXT-004. |
| `OpenAI why we no longer evaluate SWE-bench Verified February 2026` | Verify frontier benchmark caveat. | Used EXT-021. |
| `METR measuring AI ability to complete long tasks March 2025` | Verify long-task autonomy measurement. | Used EXT-019. |
| `SWE-bench Live contamination benchmark AI coding agents` | Look for contamination-resistant benchmark evidence. | Not used as a primary source because a sufficiently stable primary source was not verified in this pass. |

## Security And Governance

| Query | Purpose | Outcome |
|---|---|---|
| `Asleep at the Keyboard Copilot vulnerable code arxiv` | Verify AI code-suggestion security paper. | Used EXT-006. |
| `Do Users Write More Insecure Code with AI Assistants arxiv` | Verify user-overconfidence and security study. | Used EXT-007. |
| `AI Playbook for the UK Government principles human control security` | Verify UK government AI playbook. | Used EXT-023. |
| `NCSC guidelines secure AI system development` | Verify NCSC secure AI lifecycle guidance. | Used EXT-024. |
| `GOV.UK Service Standard point 9 secure service privacy` | Verify service security and privacy requirement. | Used EXT-025. |
| `Secure by Design policy government security UK` | Verify Secure by Design policy. | Used EXT-026. |
| `ICO data protection by design and by default UK GDPR` | Verify ICO privacy-by-design guidance. | Used EXT-027. |

## Repository Evidence Queries

Local `rg` searches were used to locate line-level evidence:

| Query | Purpose |
|---|---|
| `rg -n "worked Challenge 2 implementation|43 sources|Provenance is the product" README.md challenge-2/wiki/*.md` | Find talk case-study claims. |
| `rg -n "Codex 484|500|leaderboard" challenge-2/evaluation` | Find benchmark score evidence. |
| `rg -n "Explorer|Builder|Refiner|Verifier|Operator" output/doc/codex-contribution-modes-security-assessment.md` | Find contribution-mode assessment lines. |
| `rg -n "Documentation Lockstep|raw sources|read-only" AGENTS.md challenge-2/AGENTS.md` | Find repo-rule evidence. |
