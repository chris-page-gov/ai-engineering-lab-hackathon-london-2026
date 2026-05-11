## Research brief: ClawPilot / OpenClaw

**Headline:** ClawPilot is best understood as an early sign of the shift from “chatbot copilots” to **persistent workplace agents** that can observe work signals, propose actions, and execute approved tasks across email, calendar, Teams and files. The important point is that there are **two different things called ClawPilot/Clawpilot**: Microsoft’s internal ClawPilot, part of **Project Lobster**, and unrelated public/commercial Clawpilot services built around OpenClaw. GeekWire explicitly reports that Microsoft’s ClawPilot desktop environment has **no relation to clawpilot.ai**. ([GeekWire][1])

### 1. What it is

OpenClaw is the underlying open-source agent framework. Its own GitHub page describes it as a personal AI assistant that runs on a user’s own devices, answers through existing channels, and supports many messaging surfaces including WhatsApp, Telegram, Slack, Discord, Google Chat, Signal, iMessage and Microsoft Teams. ([GitHub][2])

ClawPilot, in the Microsoft context, is the **Mac and Windows desktop runtime** being used internally by Microsoft to experiment with “claw-like agentic workflows”. Omar Shahine, Corporate Vice President at Microsoft, says it is being built by a Microsoft team in Oslo and is used by him daily as his own personal assistant. ([LinkedIn][3])

There are also public “Clawpilot” products. One commercial site presents Clawpilot as “OpenClaw for the masses”, with products for Slack, managed OpenClaw Cloud, and a desktop app; another describes ClawPilot as managed hosting for OpenClaw where a private OpenClaw instance is provisioned in the cloud. ([Clawpilot][4])

### 2. The Microsoft initiative: Project Lobster and 3,000 staff

Microsoft’s internal initiative appears to be called **Project Lobster**. In Shahine’s Week 1 update, he said Microsoft had built an early experimental prototype in which an OpenClaw agent was “waking up inside Microsoft 365 Copilot”, with teams working on cloud runtime, Microsoft Teams integration, OpenClaw itself, identity, infrastructure, APIs, provenance and servicing. ([LinkedIn][5])

On **1 May 2026**, Shahine wrote that ClawPilot had grown from about **100 internal users** to **more than 3,000 daily users inside Microsoft** in seven days, without a broad internal push. GeekWire independently summarised the same initiative, reporting that as of 1 May Microsoft had more than 3,000 daily users testing ClawPilot, the OpenClaw-based desktop environment within Project Lobster. ([LinkedIn][3])

The core Microsoft design bet is to give agents their own **Microsoft 365 identity**: an Entra ID, mailbox, Teams presence and governance through Agent 365. Shahine says the prototype agents can read and write across Microsoft 365 using a similar security model to human employees: permissions, audit, conditional access and compliance. ([LinkedIn][3])

The strategic intent is broader than a desktop app. Microsoft is reportedly exploring OpenClaw-style features to make Microsoft 365 Copilot operate more like an always-on agent that can complete tasks on behalf of users; The Verge, citing The Information, reports that Microsoft is also considering role-specific agents for functions such as marketing, sales and accounting to limit the permissions each agent needs. ([The Verge][6])

### 3. What ClawPilot is trying to do differently

The key distinction from today’s Copilot pattern is **proactivity**. Instead of waiting for the user to ask “what can you help with?”, Shahine describes an onboarding flow where the agent notices recent work signals, such as stale drafts, overbooked Mondays or Teams replies waiting, and then offers to take specific habits off the user’s plate. ([LinkedIn][3])

That matters because the user experience shifts from “prompt-and-response” to “delegation-and-supervision”. GeekWire describes the Microsoft vision as an always-on agent team, including a Chief of Staff agent, an Executive Assistant agent and specialist agents, operating within the Microsoft 365 ecosystem. ([GeekWire][1])

The implied architecture is: persistent runtime, organisational identity, access to Microsoft Graph, continuous monitoring of signals, action proposals, user approval, audit trail and policy-governed execution. That is my synthesis from Shahine’s descriptions of Entra identity, Microsoft Graph, Teams presence, mailbox access, onboarding and pending-user-approval behaviour. ([LinkedIn][3])

### 4. Why Microsoft is interested

OpenClaw has moved quickly in the developer ecosystem. GitHub describes it as an open-source framework for building and running agentic systems, with orchestration, state management and long-running workflows; GitHub also says it had picked up more than **350,000 stars** by early May 2026. ([The GitHub Blog][7])

For Microsoft, the opportunity is to turn Microsoft 365 Copilot from a useful assistant into a governed, enterprise-grade **digital worker layer**. That would place agentic execution inside the Microsoft stack: Entra for identity, Graph for data and actions, Teams/Outlook/Office as work surfaces, Purview/Defender/Sentinel for governance, and Agent 365 as the agent control plane. The individual components are reported or described in Microsoft-related sources; the packaging into a digital worker layer is my interpretation. ([LinkedIn][3])

### 5. Why it is risky

Microsoft’s own Defender Security Research Team has been blunt about OpenClaw-style self-hosted agents. It says OpenClaw has limited built-in security controls, can ingest untrusted text, download and execute external “skills”, and act using assigned credentials. Microsoft’s guidance is that OpenClaw should be treated as **untrusted code execution with persistent credentials**, and should not be run on a standard personal or enterprise workstation. ([Microsoft][8])

The main risks are credential/data exposure, persistent memory manipulation, host compromise, indirect prompt injection and malicious skills. Microsoft recommends isolation, dedicated non-privileged credentials, non-sensitive data, monitoring for state or memory manipulation, and a rebuild plan for any evaluation. ([Microsoft][8])

This is why Microsoft’s internal approach is significant: Project Lobster is not merely adopting OpenClaw; it is trying to wrap an OpenClaw-like agent in enterprise identity, permissions, audit, conditional access and compliance controls. ([LinkedIn][3])

### 6. Enterprise/public-sector evaluation lens

For an organisation, the main decision is not “is the agent clever?” but **what authority it is allowed to exercise**. A safe pilot would need to answer these questions before any real deployment:

| Area                     | Question to test                                                                             |
| ------------------------ | -------------------------------------------------------------------------------------------- |
| Identity                 | Does each agent have its own identity, rather than borrowing a human’s credentials?          |
| Least privilege          | Can the agent’s permissions be scoped by role, data domain, time and task?                   |
| Human approval           | Which actions can be suggested, drafted, executed, reversed or never allowed?                |
| Auditability             | Can every agent observation, decision, tool call and data access be reconstructed?           |
| Data governance          | Are Purview labels, retention rules, DLP and information barriers respected?                 |
| Prompt-injection defence | What happens when the agent reads malicious content in email, Teams, web pages or documents? |
| Supply chain             | Are skills, plug-ins and extensions allowlisted, pinned, scanned and reviewed?               |
| Recovery                 | Can the agent’s identity, memory, credentials and runtime be revoked or rebuilt quickly?     |

### 7. Bottom line

ClawPilot is not just another Copilot feature. It points towards **AI agents as organisational actors**: persistent, identity-bearing, policy-governed entities that can work across business systems. Microsoft’s 3,000-staff internal test is therefore strategically important because it suggests the company is dogfooding this model at meaningful scale, not merely demonstrating a lab prototype. ([LinkedIn][3])

The opportunity is substantial: reduced administrative load, proactive work triage, delegated routine actions and new forms of personal/team productivity. The governance challenge is equally substantial: once an agent can read, decide and act, it becomes part of the organisation’s operational control surface, not just a user interface.

[1]: https://www.geekwire.com/2026/microsofts-openclaw-team-takes-on-the-personal-assistant-challenge/ "Microsoft's OpenClaw team takes on the personal assistant challenge – GeekWire"
[2]: https://github.com/openclaw/openclaw "GitHub - openclaw/openclaw: Your own personal AI assistant. Any OS. Any Platform. The lobster way.  · GitHub"
[3]: https://www.linkedin.com/pulse/project-lobster-week-3-update-ignition-identity-pipeline-shahine-j4wac "Project Lobster - Week 3 Update: Ignition, An identity, an ingestion pipeline, and an onboarding flow"
[4]: https://clawpilot.ai/ "OpenClaw for the Masses | Clawpilot"
[5]: https://www.linkedin.com/pulse/project-lobster-week-1-update-omar-shahine-hrwsc "Project Lobster - Week 1 Update"
[6]: https://www.theverge.com/tech/911080/microsoft-ai-openclaw-365-businesses "Microsoft is testing OpenClaw-like AI bots for Copilot | The Verge"
[7]: https://github.blog/open-source/register-now-for-openclaw-after-hours-github/ "Register now for OpenClaw: After Hours @ GitHub - The GitHub Blog"
[8]: https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/ "Running OpenClaw safely: identity, isolation, and runtime risk | Microsoft Security Blog"
