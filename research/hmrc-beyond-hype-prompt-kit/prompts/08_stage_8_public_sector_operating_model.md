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
