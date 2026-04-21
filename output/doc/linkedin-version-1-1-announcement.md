# LinkedIn Copy: Version 1.1 Public Release

## Main Post

Team DSIT A has published our AI Engineering Lab Hackathon Challenge 2 work: a dark-data implementation and evidence pack showing how messy government-style guidance, policy, procedure, PDF, Word and spreadsheet material can become a source-backed knowledge base.

Repository:
https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026

We built this during and after the hackathon as a worked example of AI-assisted engineering with an evidence trail, not just a polished demo.

What is in the repo:

- a generated LLM Wiki over 43 synthetic source documents
- an inspectable Dark Data Workbench for search, filtering, source review and evidence export
- Browser AI and MCP context export paths that keep the user's question attached to selected evidence
- a 100-question benchmark for testing whether AI coding agents can answer from the generated wiki
- a public Codex collaboration postmortem showing the split between human direction and AI-assisted implementation
- a contribution-modes and security assessment covering where Codex helped, where it needed human steering, and what would still be required for production government use

The main lesson was not "AI writes the code".

The useful pattern was: human framing and quality bar; Codex repo inspection, implementation, validation and synthesis; then repeatable evidence so the work can be reviewed later.

For me, the most important design principle was that provenance is the product. A useful AI answer is not just fluent text; it needs to be traceable to source, status, version, caveat and extraction route.

This is a synthetic prototype and research artifact, not a production government service. The security assessment is deliberately included so the limitations are visible alongside the implementation.

If you are arriving from the event posts, start with the reader guide in the repo. It gives routes for service leaders, engineers, data and knowledge-management readers, security reviewers, MCP/agent-tooling readers, and people interested in AI-assisted delivery.

Built by Team DSIT A.

#AICoding #GovTech #DigitalGovernment #SoftwareEngineering #ResponsibleAI #SecureByDesign #KnowledgeManagement #MCP #LLM #AIEngineering #Hackathon #PublicSectorInnovation

## Comment For Other Event Posts

Great to see the AI Engineering Lab Hackathon work being shared.

Team DSIT A has published our Challenge 2 dark-data implementation and evidence pack here:
https://github.com/chris-page-gov/ai-engineering-lab-hackathon-london-2026

It includes the generated knowledge base, Dark Data Workbench, Browser AI and MCP evidence-export paths, a 100-question evaluation benchmark, a public Codex collaboration postmortem, and a security/contribution-modes assessment.

The short version: we treated provenance as the product. The prototype is synthetic and not production-ready, but the repo shows how AI-assisted engineering can leave behind reviewable evidence rather than just a demo.

There is a `START-HERE.md` reader guide in the repo for different routes through the material.
