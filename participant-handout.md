# AI Engineering Lab Hackathon: participant reference

Keep this open throughout the day.

---

## The day at a glance

| Time | What happens |
|------|--------------|
| 08:30 | Arrive, register, breakfast, meet your pre-assigned team |
| 09:00 | Welcome and kick-off |
| 09:15 | Pick your challenge, plan with your team, FDE helps with setup |
| 09:45 | Lightning talk: Version 1 (theme TBC) |
| 09:55 | Build phase |
| 11:00 | Morning break |
| 11:30 | Lightning talk: AWS (theme TBC) |
| 11:40 | Build phase (continued) |
| 12:30 | Lunch break (optional working break) |
| 13:45 | Lightning talk: Anthropic (theme TBC) |
| 13:55 | Build phase (resumed) |
| 14:30 | Afternoon break |
| 14:45 | Lightning talk: Google (theme TBC) |
| 14:55 | Build phase (final stretch) |
| 15:30 | Final review — judges return to your team |
| 16:15 | Lightning talk: Microsoft (theme TBC; during results tabulation) |
| 16:30 | Winners announced and wrap-up |
| 16:40 | Hard finish |

---

## The challenges

Choose one of the four challenges below, or propose an open brief during the morning session. Open brief teams must pitch to a facilitator for approval before the build phase begins (09:55).

You are using AI coding tools to build your prototype. The event does not provide access to AI models for use within your application. If you have your own model access or want to mock AI capabilities, that is fine.

Challenge 1: From PDF to digital service — pick a real or realistic government PDF form and turn it into a working digital service following GOV.UK design patterns and WCAG 2.2 accessibility standards. A good starting point if your team is newer to AI coding tools.

Challenge 2: Unlocking the dark data — build a solution that makes unstructured government documents (Word files, PDFs, spreadsheets) searchable, extractable, and usable without manual migration. Bonus: define a standard format for a GOV.UK app or chat interface to consume the output.

Challenge 3: The intelligent case worker — build reusable capabilities that work across caseworking systems to summarise cases, automate routine workflows, and surface relevant policy to support human decision-making. You can integrate AI models if you have access, or mock AI endpoints to demonstrate the approach.

Challenge 4: Knowing your own organisation — build a tool that takes workforce and allocation data and gives a department a clear picture of how its resources are deployed. Focus on answering one or two questions a department head would actually ask.

You may change your challenge before 11:00. Speak to your FDE.

---

## Judging

Scoring runs throughout the day via a live dashboard. Your team earns points for reaching milestones during the build phase, such as setting up your repository, producing a first working prototype, and demonstrating a complete user journey.

When the final build stretch ends at 15:30, judges return to their assigned teams for final review until 16:15. Each pair asks a consistent set of questions about what you built, how you used AI tools, and what you would do next. They score against a simple rubric.

Your final score combines your milestone points with the judge review. There are no stage presentations. Judges want honesty. A clear explanation of what you tried and what failed scores better than a polished story that glosses over the hard parts.

---

## Getting the most from your AI tool

### Prompting for planning

Before writing any code, use your AI tool to help scope the problem:

- `We are building [description]. What are the core components we need to build in one day?`
- `What is the simplest version of this that would work as a demo?`
- `What open data sources could we use for [problem area]?`

### Prompting for building

Give your tool context before asking it to write code:

- `We are building a [description] using [language/framework]. Here is the structure so far: [paste relevant code or file list]. Now help me implement [specific feature].`
- `Write a function that [specific behaviour]. It should handle the case where [edge case].`
- `Explain what this code does and suggest how to simplify it.`

### Prompting for testing

Use prompts such as:

- `Write a test for this function that covers the happy path and the case where [input is invalid].`
- `What could go wrong with this code? What would you test?`

### Prompting for your judge review

Use prompts such as:

- `Summarise what this prototype does in two sentences for a non-technical audience.`
- `What are the limitations of this approach that I should be honest about?`

### When your tool gives you something wrong

Refine rather than restart:

- `That is not quite right. The issue is [specific problem]. Try again with [constraint].`
- `This uses [pattern I do not want]. Rewrite it using [preferred approach] instead.`

---

## During the build phase

Your assigned FDE checks in with your team regularly throughout the day. There is an optional informal check-in at lunch to surface blockers. If you are stuck at any point, speak to your FDE — they are your first point of contact.

---

## Build phase closes at 15:30

At 15:30, stop building. Share your work with your FDE — send a zip file by email or Microsoft Teams, or share a GitHub repository URL if you have access to github.com. GitHub access is not required. Prepare a brief summary of what you have built.

You will not be able to update your submission after 15:30. Final review with judges begins at 15:30.

---

## If you get stuck

Your assigned FDE is your first point of contact. You can also ask at the support desk.

Common situations:

- stuck on a technical problem — describe what you are trying to do and what is not working. An FDE can help you unblock or rescope
- AI tool not working — go to the support desk. Vendors are present and can help
- team disagreement on direction — speak to your FDE. Rescoping by 14:30 is better than presenting something half-finished
- running out of time — cut scope, not quality. A small thing that works is better than a large thing that does not

---

## Useful data sources

Some starting points:

- GOV.UK open data — https://data.gov.uk
- Office for National Statistics — https://www.ons.gov.uk
- local authority open data portals
- synthetic data is acceptable if real data raises security concerns

---
Version: 1.0
Last updated: April 2026
