# Security, governance and public-sector controls

## Core position

Treat generated code as untrusted until it has been reviewed, tested, scanned and accepted by an accountable human owner.

This is not anti-AI. It is normal engineering discipline applied to a faster code producer.

## Risk taxonomy

| Risk | What can go wrong | Relevant evidence |
| --- | --- | --- |
| Insecure generated code | The agent produces vulnerable code that passes superficial review. | EXT-006; EXT-007 |
| Hallucinated APIs or dependencies | The agent invents package names, API methods or usage patterns. | EXT-006; EXT-007 |
| Vulnerable dependency introduction | A plausible dependency brings known CVEs, weak maintenance or licence issues. | REPO-017 |
| Supply-chain risk | Agent-generated changes alter build scripts, workflow permissions or package sources. | EXT-024; EXT-026 |
| Prompt injection | Malicious repository content or external material steers an agent into unsafe behaviour. | EXT-024 |
| Data leakage | Prompts, logs or tool calls expose protected data to unauthorised systems. | EXT-023; EXT-027 |
| Secret exposure | Secrets are copied into prompts, logs, generated files or external tools. | EXT-024; REPO-017 |
| Excessive permissions | The agent acts with the user's broad repository, shell or cloud permissions. | EXT-013; EXT-016 |
| Unsafe network access | The agent downloads untrusted code, posts data externally or changes behaviour based on uncontrolled web content. | EXT-013; EXT-024 |
| Unsafe shell command execution | Commands mutate files, systems or dependencies beyond the intended task. | EXT-013 |
| Weak CI/CD | Generated changes bypass tests, reviews or deployment protections. | EXT-025; EXT-026; REPO-017 |
| Lack of auditability | Teams cannot reconstruct prompt, context, source evidence, commands, diffs and validation. | REPO-013; REPO-014 |
| Unclear accountability | The tool is blamed or credited, but no human owns the risk decision. | EXT-023; REPO-017 |
| Accessibility and equality impacts | UI/content changes work for the demo but fail disabled users or excluded groups. | EXT-023; EXT-025 |
| Privacy and data-protection risk | Personal data is used without lawful basis, minimisation, retention controls or DPIA screening. | EXT-027 |
| Policy drift | Teams accept fluent output as proof, skip review or quietly move prototype patterns into live services. | REPO-017 |

## Control set

| Control | Minimum local practice | Public-sector rationale |
| --- | --- | --- |
| Sandboxing | Run agents in isolated dev/test environments. | Limits blast radius but does not remove assurance duties [EXT-013; EXT-024]. |
| Least privilege | Scope repository, filesystem, network and cloud permissions to the task. | Aligns with secure design and secure operation [EXT-024; EXT-026]. |
| No production secrets | Do not expose production credentials, tokens or live citizen data to coding agents unless specifically approved. | Prevents data leakage and unauthorised access [EXT-023; EXT-027]. |
| Network off or approved | Keep network access disabled by default or require explicit approval per task. | Reduces exfiltration and supply-chain risk [EXT-013]. |
| Privileged command approval | Require approval for package installs, external fetches, shell scripts, destructive commands and deployment actions. | Keeps humans in control of high-risk actions. |
| Branch protections | Agents work on branches or draft PRs; no direct main or production changes. | GitHub's own coding-agent posture uses draft PR/review control concepts [EXT-016]. |
| Mandatory human review | A named developer/tech lead reviews the diff and evidence. | Required because generated code can be insecure or wrong [EXT-006; EXT-007]. |
| Generated-code scanning | Run SAST, secret scanning and unsafe-pattern checks. | Finds classes of defects humans miss at speed. |
| Dependency scanning | SCA/audit before accepting new packages or lockfile changes. | Controls supply-chain and known-CVE risk. |
| Static analysis and tests | Require typecheck, unit tests, integration tests and relevant UI tests. | Prevents fluency substituting for correctness. |
| Threat modelling | Update threat model when the agent changes trust boundaries, auth, data flows or deployment. | Secure by Design requires risk-informed security from the start [EXT-026]. |
| Accessibility checks | Run automated and human accessibility checks for UI/content changes. | Government services must be usable and inclusive [EXT-025]. |
| Provenance and audit logs | Capture prompt, selected context, files changed, commands, tests and review outcome. | Supports audit, FOI-style reconstruction and assurance [REPO-013]. |
| Clear owner | The tool does not sign off risk; a human service owner/security owner does. | AI Playbook principle: meaningful human control and assurance [EXT-023]. |
| Incident response and rollback | Define how to revert agent-generated changes and report issues. | Production readiness requires operation and maintenance controls [EXT-024]. |
| Procurement/supplier assurance | Ask about data use, retention, training, sub-processors, regional hosting, logging and admin controls. | Required before real public-sector use, especially with protected data [EXT-023; EXT-027]. |

## Mapping to public-sector guidance

| Guidance | Relevant requirement or principle | Coding-agent implication |
| --- | --- | --- |
| UK Government AI Playbook [EXT-023] | Lawful, ethical, secure and responsible use; meaningful human control; lifecycle management; assurance. | Coding agents need approved use cases, human review, lifecycle evidence, escalation and assurance. |
| NCSC secure AI system development [EXT-024] | Secure design, development, deployment, operation and maintenance. | Agent environments, prompts, tool permissions, data flows and generated code all need lifecycle controls. |
| GOV.UK Service Standard point 9 [EXT-025] | Create a secure service that protects privacy. | A coding-agent prototype cannot become a service without security and privacy evidence. |
| Secure by Design policy [EXT-026] | Build security into digital delivery and manage risk through ownership and assurance. | Do not bolt security onto generated output at the end; make it part of task framing and review. |
| ICO data protection by design/default [EXT-027] | Data protection should be designed in from the start. | Do not feed real personal data into tools before lawful basis, minimisation, retention and processor questions are answered. |
| Repo-local security assessment [REPO-017] | Strong prototype, not production-grade; Codex useful for first-pass security review but not final sign-off. | Use Codex as assistant, not security owner or operator. |

## Before using a coding agent on public-sector work, have we...?

- Chosen a low-risk task with clear acceptance criteria?
- Confirmed the data classification and whether real personal, tax, casework or classified data is involved?
- Confirmed the tool is approved for that data and environment?
- Removed production secrets from the agent environment?
- Scoped filesystem, repository, network and cloud permissions?
- Written the prompt with relevant files, constraints, tests and stop conditions?
- Defined who reviews the diff and who owns the final decision?
- Required tests, type checks, linters and security scans?
- Checked dependency and licence changes?
- Checked accessibility for user-facing output?
- Recorded prompt, context, commands, diffs, test evidence and review notes?
- Updated documentation, ADRs, runbooks or tracking docs where needed?
- Defined rollback, incident and escalation routes?
- Kept raw source data immutable unless explicitly approved?
- Avoided treating a polished answer as proof?

## Setup questions for teams

Ask these before procurement or a wider pilot:

- What data is sent to the tool provider?
- Is prompt/output content used for training or service improvement?
- Where is data processed and retained?
- What logs are available to administrators and auditors?
- Can network access be disabled or approved per action?
- Can shell commands and external fetches require approval?
- How are secrets detected and blocked?
- Can the tool operate on branches only?
- Are PRs/diffs human-reviewable before CI or deployment?
- How are model/version/tool changes announced?
- Can the organisation enforce policy centrally?
- What happens when the tool is unavailable?

## Boundary for the HMRC talk

The repository used synthetic fixture data [REPO-003; REPO-004]. That makes it suitable for a talk and learning exercise.

Real HMRC data would be a different case. It would require approved handling, security assurance, auditability, DPIA screening where relevant, supplier/processor assurance, accessibility review, operational readiness and named accountable owners.
