# Empirical evidence: productivity, quality and developer experience

## Bottom line

AI coding support is best understood as a conditional capability amplifier, not a uniform productivity multiplier.

The best available evidence is mixed because studies measure different things: single lab tasks, experienced maintainers on mature repositories, public benchmark tasks, product telemetry and self-reported adoption. These are not interchangeable.

## HMRC Talk Navigation

This file is supporting evidence for the HMRC talk narrative:

- [Narrative entry point](narrative/index.md)
- [Navigation and scope](narrative/notes/navigation-and-scope.md)
- [AI Coding Assistants market briefing](narrative/notes/ai-coding-assistants-market-briefing.md)
- [Topic index](narrative/topics.md)

## Evidence table

| Study/source | Setting | Participants | Task type | Tool/model | Measured outcome | Result | Limitations | Relevance to public-sector engineering |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Peng et al., "The Impact of AI on Developer Productivity" [EXT-005] | Controlled online experiment | Recruited software developers | Implement a JavaScript HTTP server quickly | GitHub Copilot | Completion time | AI-assisted group completed the task faster. | One bounded task; speed over long-term maintainability; not a mature public-sector codebase. | Supports trying agents on low-risk, well-scoped tasks with measurable acceptance criteria. |
| METR early-2025 experienced developer RCT [EXT-020] | Real open-source repositories | 16 experienced developers on familiar mature repos | 246 real issues, bug fixes, features and refactors | Primarily Cursor with Claude 3.5/3.7 Sonnet-era tools | Self-reported implementation time with screen recording | AI-allowed tasks took 19 per cent longer in this setting. | Small and specific; tools evolve quickly; does not show AI never helps. | Closest warning for government legacy estates: mature codebases with implicit requirements can create review and rework drag. |
| SWE-bench [EXT-004] | Benchmark over open-source GitHub issues | Models/agents, not human developers | Repository issue resolution | Various models/agents | Automated test pass on issue tasks | Early models solved only a small share; later progress made it a central benchmark. | Public benchmark, Python-heavy, test-dependent and contamination-prone. | Useful for capability direction, not local adoption or procurement decisions. |
| OpenAI critique of SWE-bench Verified [EXT-021] | Audit/benchmark critique | Expert review and contamination probing | SWE-bench Verified tasks | Frontier models | Test validity and contamination indicators | Identified flawed tests and contamination as major problems. | Vendor-authored critique; still concrete and relevant. | Reinforces that public-sector pilots need local evaluations over representative tasks. |
| METR long-task autonomy [EXT-019] | Multi-step software/reasoning tasks | Models compared against human task times | Task-completion horizons | Frontier models/agents | Task duration solved at reliability thresholds | Task length is a useful capability lens; longer tasks remain harder. | Extrapolation depends on methodology and task mix. | Helps explain why short demos do not prove day-long autonomous delivery. |
| DORA State of AI-assisted Software Development 2025 [EXT-022] | Industry survey/report | Software delivery practitioners | AI-assisted development adoption and delivery outcomes | Various tools | Self-reported and organisational delivery measures | Useful for adoption and organisational context. | Survey/correlational; detailed findings need report-level review; not causal proof. | Helps frame developer experience, measurement and governance conversations. |
| Security code-generation studies [EXT-006; EXT-007] | Prompt studies and user study | Generated programs and human participants | Security-relevant code tasks | Copilot/Codex-era tools | Vulnerability presence and user confidence | Generated/AI-assisted code can be insecure; overconfidence is a risk. | Older tools and specific scenarios; not a modern benchmark of every product. | Supports mandatory review, scanning and secure-coding requirements before use in government services. |
| Repo-local Challenge 2 evaluation [REPO-014; REPO-015] | Synthetic local benchmark | Codex, Codex with MCP, Claude, Gemini, Microsoft Copilot UI | 100 source-backed wiki questions | Multiple AI coding/client tools | Rubric score, completions, citation overlap, MCP audit evidence | Codex and Claude scored highly on this synthetic wiki task; Gemini was quota-limited; Microsoft Copilot UI struggled in this harness. | Local benchmark; raw runs external; not official comparative evidence. | Shows how a team can build a source-backed local evaluation rather than relying on vendor leaderboards. |

## Why the evidence conflicts

The evidence conflicts because the studies measure different operating conditions.

**Greenfield versus brownfield.** Copilot-style lab tasks are closer to greenfield implementation. METR's experienced-developer RCT used mature repositories where hidden context, style, review standards and existing abstractions matter.

**Simple versus complex tasks.** Short, well-specified tasks fit autocomplete and agent delegation better. Multi-hour tasks require planning, context recovery, tests, iteration and judgement.

**Novice versus expert.** AI can help less experienced developers with syntax, scaffolding and unfamiliar libraries. Expert maintainers may already know the codebase and may spend more time correcting plausible but misaligned output.

**Familiar versus unfamiliar codebase.** Agents are useful for exploration, but they can miss implicit conventions and local history. Familiar human maintainers can be faster at selecting the right constraint.

**Quality bar.** Speed-to-first-solution is not the same as quality-adjusted delivery. Public-sector work often requires review evidence, security checks, accessibility, privacy, operational readiness and documentation.

**Review burden.** Generated code shifts effort from typing to reviewing. If the reviewer must inspect more code than they would have written, productivity may fall.

**Task decomposition.** Agents work best with bounded tasks, explicit files, acceptance criteria and tests. They are weaker when the prompt is broad, ambiguous or authority-laden.

**Hidden costs.** Rework, flaky tests, hallucinated APIs, dependency drift, CI failures, security review and audit packaging can erase apparent gains.

**Measurement effects.** Self-reported productivity can diverge from measured time. Developers may feel faster because the work is less effortful, even when elapsed time increases.

## Practical interpretation for HMRC/public-sector teams

Use AI coding assistants and agents first where the task is:

- low-risk;
- bounded;
- reversible;
- covered by tests or easy to inspect;
- based on synthetic or approved data;
- reviewable in a small diff;
- isolated from production credentials and live systems.

Avoid or escalate where the task involves:

- live citizen or tax data;
- secrets or privileged systems;
- safety-critical or legally significant decisions;
- production operations;
- unreviewed dependency introduction;
- unclear accountability;
- absent tests or absent owner.

## Talk-ready conclusion

The empirical story is not "AI makes developers 50 per cent faster" or "AI makes developers slower". Both are weak simplifications.

The evidence says AI coding support can amplify capability when the task, environment and controls fit. It can also add cost when the model output is plausible but wrong, when the codebase carries hidden context, or when assurance work outweighs typing time saved.

The public-sector adoption question is therefore:

> Have we built an engineering system in which faster code generation leads to better, safer services?
