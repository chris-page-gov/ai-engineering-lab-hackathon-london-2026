# Operating Model For Public-Sector Engineering With Coding Agents

This operating model is designed for public-sector teams that want to try coding agents without pretending they are autonomous engineers, security authorities, or policy owners. It combines the repo-local Challenge 2 evidence with government AI, security, service, and data-protection guidance.

Repo-local citations use the format `path:line` followed by a GitHub permalink to that exact line where available.

## HMRC Talk Navigation

This file is supporting evidence for the HMRC talk narrative:

- [Narrative entry point](narrative/index.md)
- [Navigation and scope](narrative/notes/navigation-and-scope.md)
- [AI-Native Engineering Blueprint narrative guide](narrative/slides/ai-native-engineering-blueprint/narrative-guide.md)
- [Challenge 2 worked example](narrative/notes/challenge-2-worked-example.md)
- [Topic index](narrative/topics.md)

## The Five-Layer Model

### 1. Task Selection

Use coding agents first where the blast radius is small, the source material is approved for the tool, and the result can be checked quickly.

Good early tasks:

- internal prototypes over synthetic or already-public data
- test generation and test repair
- documentation cleanup
- codebase exploration and impact mapping
- migration scaffolds with human review
- repeatable build or lint automation

Avoid or escalate:

- live taxpayer, claimant, health, law-enforcement, or classified data
- secrets, credentials, private keys, or privileged operational logs
- safety-critical or payment-affecting logic without formal controls
- production operation, incident response, access-control changes, or irreversible actions
- policy interpretation where a named policy owner must decide the answer

Repo pattern: Challenge 2 used synthetic material and treated source data as immutable. Local evidence: `challenge-2/wiki/architecture.md:112` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/126f9f0df4a6d4c3993e28df52b609e26316070f/challenge-2/wiki/architecture.md#L112)); `challenge-2/AGENTS.md:7` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/126f9f0df4a6d4c3993e28df52b609e26316070f/challenge-2/AGENTS.md#L7)).

### 2. Agent Environment

The agent environment should make the safe path the easy path:

- work on a branch or disposable workspace
- default to least-privilege file and tool access
- restrict or review network access
- keep raw data read-only
- block secrets from prompts, files, logs, and exports
- make generated artefacts reproducible from scripts where possible
- record commands, validation, and decisions
- separate public artefacts from private working evidence

Repo pattern: the repository rules require documentation lockstep and validation, while Challenge 2 rules keep raw source folders read-only. Local evidence: `AGENTS.md:9` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/126f9f0df4a6d4c3993e28df52b609e26316070f/AGENTS.md#L9)); `AGENTS.md:34` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/126f9f0df4a6d4c3993e28df52b609e26316070f/AGENTS.md#L34)).

### 3. Prompting And Steering

Prompts should give context, constraints, acceptance criteria, and validation expectations. They should also tell the agent what not to do.

Reusable task pattern:

```text
Goal:
Context:
Allowed data and tools:
Files or modules in scope:
Files or data not to edit:
Expected outputs:
Validation required:
Evidence required for claims:
Review boundaries:
```

Repo pattern: the build worked because operating files kept context, progress, and change history visible to the agent and reviewers. Local evidence: `Context.md:137` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/126f9f0df4a6d4c3993e28df52b609e26316070f/Context.md#L137)); `Progress.md:121` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/126f9f0df4a6d4c3993e28df52b609e26316070f/Progress.md#L121)).

### 4. Review And Assurance

Review should focus on evidence, not polish:

- inspect the diff, including generated artefacts
- run the narrowest relevant tests
- check source-data handling
- check whether claims cite evidence
- check for secrets, local paths, copied third-party material, and policy-sensitive assertions
- require human sign-off for security, privacy, architecture, operational, and policy decisions
- keep benchmark and model claims scoped to the evidence that produced them

Repo pattern: the contribution-mode assessment explicitly treats Codex as strong for Explorer, Builder, Refiner, and Verifier work, but not as an autonomous Security Steward or Operator. Local evidence: `output/doc/codex-contribution-modes-security-assessment.md:163` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/126f9f0df4a6d4c3993e28df52b609e26316070f/output/doc/codex-contribution-modes-security-assessment.md#L163)); `output/doc/codex-contribution-modes-security-assessment.md:170` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/126f9f0df4a6d4c3993e28df52b609e26316070f/output/doc/codex-contribution-modes-security-assessment.md#L170)).

### 5. Learning Loop

Every pilot should leave behind reusable learning:

- what task was attempted
- what data class was used
- what the agent was allowed to do
- what tests and reviews were run
- what failed or had to be corrected
- which prompts, rules, and checks should become standard
- which tasks should stay out of scope

Repo pattern: this project used `Changelog.md`, `Context.md`, and `Progress.md` as living memory for decisions, validation, and next steps. Local evidence: `Changelog.md:5` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/126f9f0df4a6d4c3993e28df52b609e26316070f/Changelog.md#L5)); `Context.md:146` ([GitHub](https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026/blob/126f9f0df4a6d4c3993e28df52b609e26316070f/Context.md#L146)).

## RACI-Style Responsibilities

| Activity | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Choose pilot task and data class | Delivery lead, technical lead | Service or product owner | Security, data protection, policy owner | Team and governance forum |
| Configure agent environment | Technical lead, platform engineer | Engineering manager | Security, architecture | Developers, testers |
| Write repo rules and task prompts | Technical lead, senior developer | Engineering manager | Delivery lead, policy owner where relevant | Team |
| Implement bounded changes | Developer with agent support | Engineering manager | Domain expert, tester | Product owner |
| Review code and generated artefacts | Human reviewer, tester | Engineering manager | Security for risk-bearing changes | Team |
| Approve data handling | Data protection lead or delegated owner | Information asset owner / SIRO route as applicable | Security, legal, policy | Delivery team |
| Approve security posture | Security owner | Senior risk owner / service owner | Architecture, platform, DPO where relevant | Delivery team |
| Approve production release | Service owner | Appropriate operational owner | Security, architecture, delivery, support | Users and stakeholders |
| Capture learning and reusable controls | Delivery lead, technical lead | Engineering manager | Team, governance forum | Wider practice/community |

## Control Checklist

Before using a coding agent on public-sector work, confirm:

- The task has a named human owner.
- The data class is approved for the tool and environment.
- The prompt excludes secrets, credentials, and unapproved personal data.
- The agent has least-privilege access.
- Raw source material is read-only where it is evidence.
- The work happens on a branch or disposable workspace.
- Network/tool access is approved or disabled.
- Outputs can be reviewed as diffs.
- Validation is defined before implementation.
- Security, privacy, policy, and operational decisions remain human-owned.
- Logs and generated evidence are retained where appropriate.
- Public artefacts are checked for local paths, secrets, and private context.

## Minimum Safe Pilot For A Government Engineering Team

Pilot scope:

- one internal repository
- synthetic, open, or explicitly approved low-risk data
- no production credentials
- no live service operation
- one small user-facing improvement or test/documentation workflow
- branch-based work with human code review
- documented prompts, decisions, and validation

Pilot outputs:

- a short problem statement
- a local `AGENTS.md` or equivalent repo rule file
- an evidence register for claims
- a validation log
- a before/after diff
- a short retrospective covering speed, quality, review burden, failures, and controls

Success criteria:

- the change is useful without bypassing normal review
- reviewers can understand and test it
- no source data, secrets, or local state leaks into committed artefacts
- the team can explain which decisions the agent made and which decisions humans retained
- the pilot produces at least one reusable rule, test, or checklist for the next task

## How To Present The Operating Model In The Talk

The simplest line is:

> Treat coding agents as force multipliers inside an engineering control system, not as free-floating authorities.

For the HMRC audience, translate that into five takeaways:

1. Pick low-risk work first.
2. Put the agent in a bounded environment.
3. Write down the rules and acceptance criteria.
4. Review evidence, tests, and diffs.
5. Keep security, privacy, policy, and operational accountability with named people.
