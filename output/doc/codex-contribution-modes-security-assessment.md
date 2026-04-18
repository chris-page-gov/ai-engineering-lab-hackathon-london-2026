# Codex Contribution Modes and Government Security Assessment

Date: 18 April 2026
Team: Team DSIT A
Repository branch: `codex/postmortem-wiki`
Primary local input: `output/doc/contribution-modes-proposal.md`
Related evidence: `postmortem-public/`, `output/doc/challenge-2-realtime-delivery-report.md`, Challenge 2 wiki/workbench code and validation outputs

## Executive summary

Team DSIT A used more than one mode of programming. It was not a simple "developer writes code" exercise. The strongest pattern was a human-led framing and governance loop with Codex doing broad repo exploration, implementation, refactoring, verification, report generation, publication packaging, and security review. That maps closely to the contribution modes in the attached proposal: Explorer, Framer, Architect, Builder, Refiner, Experience Shaper, Verifier, Security Steward, and Operator.

Codex was highly suitable for Explorer, Builder, Refiner, and Verifier work in this project. It was also useful in Architect and Framer modes when the user supplied intent, constraints, and corrections. It was weaker as a final Security Steward and should not be treated as an autonomous Operator for government production services. The evidence from this repo is that Codex can produce a coherent, tested, traceable prototype quickly, but production-level security still requires explicit government assurance controls, human security ownership, hardened CI/CD, dependency governance, threat modelling, privacy assessment, and operational readiness.

Security scan conclusion: no live credentials or obvious secret material were found in the files intended for publication. The candidate GitHub material is still not production-grade software. The main security findings are CI/CD hardening gaps, one low npm advisory, one medium Bandit finding in local tooling, missing production deployment security controls, and the need for formal Secure by Design, privacy, and AI-tool governance before using this pattern with real government data.

## Scope and standards

This is a repository-level security and production-readiness scan. It is not a formal penetration test, CHECK assessment, GovAssure assessment, independent architecture review, DPIA, or accreditation decision.

The scan was evaluated against the standards and guidance that would normally matter for a government software delivery context:

| Standard or guidance | Why it applies here | Assessment use |
|---|---|---|
| [UK Government Secure by Design](https://www.security.gov.uk/policy-and-guidance/secure-by-design/about/) | Secure by Design is mandatory for central government departments, ALBs, and executive agencies whose services are subject to digital and technology spend control. | Used as the main lens for early security, roles, risk-driven controls, and continuous security ownership. |
| [GOV.UK Service Standard point 9](https://www.gov.uk/service-manual/service-standard/point-9-create-a-secure-service) | Government services must be secure and protect privacy. | Used to judge whether a prototype has enough evidence to become a service. |
| [GOV.UK Technology Code of Practice](https://www.gov.uk/guidance/the-technology-code-of-practice) and [Make things secure](https://www.gov.uk/guidance/make-things-secure) | Government technology projects should address security, privacy, accessibility, open standards, lifecycle, and assurance. | Used to check whether security and privacy are built into programme planning, not just code. |
| [NCSC Secure Development and Deployment](https://www.ncsc.gov.uk/collection/developers-collection) | NCSC frames secure development as a whole-lifecycle concern covering code, repositories, build pipeline, testing, and flaw response. | Used to evaluate repo, CI, build, testing, and vulnerability response posture. |
| [NCSC Cyber Assessment Framework](https://www.ncsc.gov.uk/collection/cyber-assessment-framework/introduction-to-caf) | CAF provides outcome-focused objectives for managing risk, protection, detection, and response. | Used as a production-readiness check, especially for operational controls that are absent from a prototype. |
| [NCSC Guidelines for Secure AI System Development](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development) | This project studies AI-assisted software delivery and agentic tooling. | Used to evaluate AI-tool security, data exposure, transparency, and ownership. |
| [Government Security Classifications Policy](https://www.gov.uk/government/publications/government-security-classifications/government-security-classifications-policy-html) | Challenge 2 contains synthetic government-style material with OFFICIAL, SECRET, and TOP SECRET language. | Used to separate synthetic fixture content from real classification handling requirements. |
| [ICO Data Protection by Design and Default](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/guide-to-accountability-and-governance/data-protection-by-design-and-default/) | A real dark-data service could process personal data or sensitive operational data. | Used to test whether data minimisation, DPIA, privacy defaults, and processor assurance would be needed. |
| [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | The attached contribution-modes proposal cites SSDF and its emphasis on defined roles and secure SDLC practices. | Used as a secure software lifecycle vocabulary for roles, provenance, testing, and vulnerability response. |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), [OWASP SAMM](https://owasp.org/www-project-samm/), and [OWASP CI/CD Security](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html) | The workbench is a web application and the repo uses CI. | Used for web-app verification expectations, maturity planning, secrets handling, CI/CD integrity, and supply-chain controls. |

## Contribution modes observed

| Mode | How it appeared in the project | Codex suitability | Required control |
|---|---|---|---|
| Explorer | Reading the repo, inferring the existing wiki pattern, finding Codex session material, checking publication risks, and trying conversion/security tooling. | Strong. Codex is well suited to broad inspection and quick synthesis when the repo is local and tools are available. | Keep exploration in a sandbox and prevent accidental publication of local state, transcripts, credentials, or copied third-party material. |
| Framer | Turning broad user intent into a postmortem/publication structure, security review scope, and contribution-mode evaluation. | Strong when the user supplies purpose and acceptance criteria. | Human owner must validate the framing because it defines what evidence counts and what risks are acceptable. |
| Architect | Choosing the private `postmortem/` plus public `postmortem-public/` split, preserving `v1-challenge-2`, and using generated wiki structures. | Good for bounded architectural decisions that reuse existing patterns. | Architecture decisions touching trust boundaries, retention, AI tooling, and publication need explicit human/security review. |
| Builder | Creating the postmortem builder, public derivative, Markdown reports, workbench UI, MCP tooling, tests, and documentation updates. | Strong. Codex can produce useful implementation across multiple files when repo conventions are clear. | CI, review, dependency scanning, and narrow validation must gate the output. |
| Refiner | Redaction tuning, link cleanup, doc lockstep updates, report formatting, and publication packaging. | Strong. Codex is effective at applying consistent mechanical changes and local style. | Avoid unrelated rewrites and keep generated artifacts reproducible. |
| Experience Shaper | Building and testing the Dark Data Workbench UI and evidence export flows. | Good for prototypes and internal tools. | Accessibility testing, content design, assisted-digital considerations, and service-design review are still needed for public services. |
| Verifier | Running unit tests, Playwright tests, py_compile, documentation lockstep, publication lint, secrets grep, Bandit, and npm audit. | Strong as a test runner and coverage-expander. | Codex cannot prove absence of vulnerabilities; formal SAST/SCA/DAST, threat modelling, and independent review remain necessary. |
| Security Steward | Identifying publication risks, local path leakage, licensing gaps, CI/CD issues, and production hardening requirements. | Useful as a first-pass reviewer, not sufficient as final authority. | A named security owner must approve risk treatment, threat model, DPIA, AI-tool use, and operational controls. |
| Operator | Local branch/tag setup, builds, and validation. No live service operation occurred. | Weak for unsupervised production operation. | Production operation needs runbooks, monitoring, incident response, least privilege, approvals, and audit trails outside Codex. |

The attached contribution-modes proposal is a good fit for what happened here. The project worked because the human set direction and policy preference, while Codex filled in many implementation and evidence details. That is exactly the distinction the proposal makes: authority should depend on mode, environment, and task, not on a generic "developer" label.

## Security scan commands and results

The following checks were run locally on 18 April 2026.

| Check | Result |
|---|---|
| Credential-pattern scan with ripgrep across repo content, excluding build output, node modules, ignored private `postmortem/`, and binary assets | No live credentials found. Hits were documentation text, synthetic Challenge 2 policy material, generated postmortem discussion, lockfile token strings, and Git sample hook text. |
| Unsafe-code-pattern scan for `eval`, `new Function`, `{@html`, `innerHTML`, `shell=True`, subprocess calls, local/session storage, and similar patterns | No direct dynamic HTML or shell execution pattern found. Legitimate subprocess use appears in local tools/tests. `localStorage` is used for saved source-context names and source IDs in the browser prototype. |
| `pnpm audit --audit-level moderate` in `challenge-2/workbench` | Passed for moderate and above. Reported 1 low vulnerability. |
| `pnpm audit --json` in `challenge-2/workbench` | Low advisory: `cookie` 0.6.0 via `@sveltejs/kit`, CVE-2024-47764 / GHSA-pxg6-pf52-xh8x. Recommendation: upgrade to `cookie` 0.7.0 or later through dependency update. |
| `uv run --with bandit bandit -r challenge-2 tools tests -x challenge-2/workbench,node_modules,postmortem,postmortem-public,output` | 18 findings: 17 low, 1 medium, 0 high after hardening the postmortem external-source fetcher. The remaining medium finding is ElementTree parsing of DOCX metadata in `challenge-2/tools/build_wiki.py`. |
| `python3 -m unittest tests/test_challenge2_workbench_mcp.py tests/test_challenge2_eval_mcp.py` | Passed, 2 tests. |
| Python compile check for postmortem builder, doc lockstep, wiki builder, workbench MCP, and evaluation clients | Passed. |
| `pnpm check` | Passed, 0 Svelte errors or warnings. |
| `pnpm test` | Passed, 2 test files and 14 tests. |
| `pnpm build` | Passed; static site written to `challenge-2/workbench/build`. |
| `pnpm test:ui` | Passed, 8 Playwright tests across desktop and mobile Chromium. |

No Python dependency audit was run because the repository has no Python dependency manifest such as `requirements.txt`, `pyproject.toml`, or a lock file. The Python tooling currently relies on the standard library plus ephemeral validation tools invoked through `uv --with`.

## Security findings

### F-01: Production security case is not yet present

Severity: High for production use; acceptable for a synthetic hackathon prototype.

The repository contains a strong prototype, generated evidence, tests, and documentation, but it does not contain a full production security case. There is no deployment architecture, IAM model, data-flow diagram for real data, threat model, DPIA, service owner risk acceptance, operational monitoring design, incident response plan, vulnerability disclosure route, or GovAssure/Secure by Design self-assessment.

Required before production: complete Secure by Design activities, define a named security owner, produce a threat model, document data flows, run a DPIA where personal data may be processed, define hosting/security headers, and record risk treatment decisions.

### F-02: CI/CD hardening is incomplete

Severity: Medium.

The GitHub Actions workflows use tag-pinned actions such as `actions/checkout@v4`, `actions/setup-node@v4`, `pnpm/action-setup@v4`, and `actions/setup-python@v5`, but not immutable commit SHA pins. The workflows also do not define least-privilege `permissions`, dependency review, CodeQL, secret scanning, SBOM generation, artifact signing, or provenance.

Required before production: add explicit workflow permissions, pin third-party actions to commit SHAs where appropriate, add automated SCA/SAST/secret scanning, protect branches, require review, and define artifact provenance. This aligns with OWASP CI/CD risks around dependency chain abuse, credential hygiene, artifact integrity, and logging.

### F-03: Low npm advisory in SvelteKit transitive dependency

Severity: Low.

`pnpm audit` reports CVE-2024-47764 / GHSA-pxg6-pf52-xh8x in `cookie` 0.6.0 through `@sveltejs/kit`. The reported issue concerns out-of-bounds characters in cookie name/path/domain handling. The current static workbench does not implement user-controlled cookie serialization, which reduces immediate risk, but government production policy should not carry known vulnerable dependencies without documented risk acceptance.

Required before production: update SvelteKit or override the transitive `cookie` package to a patched version, then rerun `pnpm audit`.

### F-04: XML metadata parsing should use a hardened parser if inputs become untrusted

Severity: Medium if user-supplied documents are accepted; low for the current synthetic corpus.

Bandit flagged `xml.etree.ElementTree.fromstring` in `challenge-2/tools/build_wiki.py` when reading `docProps/core.xml` from DOCX files. The current challenge data is local synthetic fixture data, so the risk is bounded. If the wiki builder is reused for arbitrary uploaded documents, XML parsing should use `defusedxml` and explicit size limits.

Required before production: switch DOCX metadata parsing to `defusedxml.ElementTree`, add archive-size and member-size limits, and reject unexpected paths/content types.

### F-05: URL fetching in the postmortem builder has scheme and domain controls

Severity: Remediated publication-tooling finding.

Bandit initially flagged `urllib.request.urlopen` in `tools/build_codex_postmortem.py`. The builder now rejects non-HTTPS URLs and blocks hosts outside the explicit Karpathy/X/GitHub/Jina source allowlist before fetching known methodology references for local evidence packaging.

Residual action before shared automation: reject redirects outside the allowlist, cap response size, and keep recording fetch hashes.

### F-06: Browser local storage is acceptable for this prototype, but not for sensitive contexts

Severity: Low now; medium if used with real data.

The workbench stores saved context names and source IDs in `localStorage`. It does not store raw document text or model responses. In a real government deployment, saved contexts could reveal sensitive user work patterns or case material if source IDs map to protected records.

Required before production: classify saved-context metadata, minimise retention, provide clear deletion, avoid storing sensitive content client-side, and consider server-side storage protected by user identity and audit controls.

### F-07: Contribution-modes Markdown image rendering has been remediated

Severity: Publication quality issue, not security. Status: remediated in the publication artifact.

The Markdown conversion of `Contribution Modes Proposal.docx` initially extracted three embedded diagrams as `.emf` files, which GitHub does not render consistently. The public Markdown now references GitHub-renderable SVG replacements under `output/doc/assets/contribution-modes-proposal/`.

Residual action: review the regenerated SVG diagrams against the original Word artwork if exact visual fidelity is required. The publication issue is resolved for GitHub rendering.

### F-08: Static prototype lacks deployment security headers

Severity: Medium for a public deployment.

The SvelteKit workbench is a static build. The repository does not define production hosting headers such as Content Security Policy, Referrer-Policy, X-Content-Type-Options, Permissions-Policy, or HSTS. For a static prototype this is expected; for a public government service it is incomplete.

Required before production: define host-level security headers, CSP compatible with SvelteKit assets, HTTPS-only hosting, access logging, dependency update process, and cache policy.

### F-09: AI coding assistant use needs explicit government data-handling controls

Severity: High if real government data, secrets, or classified material are used.

This project used synthetic data and local repository content. That is an appropriate learning context. The same workflow over live case data, unpublished policy, credentials, or classified information would require explicit approval, data classification handling, processor assurance, logging, tool configuration, and human review. NCSC secure AI guidance stresses ownership, transparency, and secure-by-default operation for AI systems; those principles also apply to AI-assisted delivery tooling.

Required before real-data use: define allowed data classes for Codex and similar tools, prohibit secrets and classified material unless the tool environment is approved for them, capture tool permissions, retain audit evidence, and make a human accountable for security and privacy decisions.

## Positive security evidence

- Challenge 2 raw source material is treated as immutable source data.
- Challenge 2 fixture data is explicitly synthetic, and repository rules distinguish synthetic identifiers from real secrets or local path leaks.
- The workbench does not make live model API calls and does not require model credentials.
- The workbench can be used without AI and exports explicit evidence bundles when AI is used externally.
- Validation is broad for a prototype: Svelte typecheck, unit/component tests, Playwright desktop/mobile tests, Python compile checks, MCP tests, documentation lockstep, publication lint, Bandit, and npm audit.
- `postmortem/` is ignored as a private evidence archive, while `postmortem-public/` is the intended GitHub-safe derivative.
- The public postmortem excludes raw transcripts and full third-party source copies, using citation-style references for unlicensed external material.
- Documentation lockstep reduces the chance that implementation, assumptions, validation, and user-facing instructions drift apart.

## Suitability of Codex for secure production-level code

Codex was effective at producing secure-by-default prototype behaviours when the repo already encoded the right expectations. It followed the documentation lockstep policy, preserved synthetic source data, generated tests, ran validations, used a public/private publication split, found false-positive secret hits, and identified meaningful production gaps once asked to scan for them.

Codex was not sufficient on its own to guarantee production-level security. The strongest evidence is what had to be made explicit: government security standards, Secure by Design expectations, source licensing, publication redaction, dependency scanning, Bandit scanning, and CI/CD hardening. Codex can execute and document those controls, but it should not be the authority that decides the risk appetite or signs off a government service.

The appropriate role for Codex in this context is:

- Strong: Explorer, Builder, Refiner, Verifier.
- Useful with human steering: Framer, Architect, Experience Shaper.
- Assistant only: Security Steward.
- Not autonomous: Operator.

For government production work, Codex should be used inside a controlled engineering system: approved data classes, least-privilege tool access, branch protections, human code review, automated tests, SCA/SAST/secret scanning, threat modelling, DPIA where relevant, signed-off deployment architecture, and operational monitoring. Under those conditions it is a strong accelerator. Without those controls it can create plausible, well-written code and documentation faster than the surrounding assurance process can absorb safely.

## Recommended publication actions

1. Publish `postmortem-public/`, not ignored `postmortem/`.
2. Publish `output/doc/contribution-modes-proposal.md` as the Markdown conversion of the attached proposal; the former EMF diagram references have been replaced with GitHub-renderable SVG diagrams.
3. Publish this assessment with the security findings intact; do not present the repo as production-ready.
4. Add CI hardening work before any production claim: explicit workflow permissions, pinned actions, dependency review, CodeQL or equivalent SAST, secret scanning, SBOM/provenance, and protected branches.
5. Upgrade the `cookie` transitive dependency path and rerun `pnpm audit`.
6. Replace ElementTree parsing with `defusedxml` before processing user-supplied documents.
7. Add scheme/domain allowlisting to postmortem external-source fetching.
8. Produce a real Secure by Design pack before processing real government data: threat model, DPIA screening, classification handling, security owner, operational model, incident process, and risk acceptance.

## References

- Local: `output/doc/contribution-modes-proposal.md`
- Local: `output/doc/challenge-2-realtime-delivery-report.md`
- Local: `postmortem-public/wiki/index.md`
- [UK Government Secure by Design](https://www.security.gov.uk/policy-and-guidance/secure-by-design/about/)
- [GOV.UK Service Standard point 9](https://www.gov.uk/service-manual/service-standard/point-9-create-a-secure-service)
- [GOV.UK Technology Code of Practice](https://www.gov.uk/guidance/the-technology-code-of-practice)
- [GOV.UK Make things secure](https://www.gov.uk/guidance/make-things-secure)
- [NCSC Secure development and deployment guidance](https://www.ncsc.gov.uk/collection/developers-collection)
- [NCSC Cyber Assessment Framework](https://www.ncsc.gov.uk/collection/cyber-assessment-framework/introduction-to-caf)
- [NCSC Guidelines for secure AI system development](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development)
- [Government Security Classifications Policy](https://www.gov.uk/government/publications/government-security-classifications/government-security-classifications-policy-html)
- [ICO Data protection by design and default](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/guide-to-accountability-and-governance/data-protection-by-design-and-default/)
- [NIST SP 800-218 Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP SAMM](https://owasp.org/www-project-samm/)
- [OWASP CI/CD Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html)
