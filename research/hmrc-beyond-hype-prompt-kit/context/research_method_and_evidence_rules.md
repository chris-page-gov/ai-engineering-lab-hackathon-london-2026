# Research method and evidence rules

## General standards

Use British English.

Distinguish clearly between:

- fact;
- empirical finding;
- benchmark result;
- vendor claim;
- interpretation;
- recommendation.

Do not use hype language. Avoid claims such as “AI replaces developers” unless quoting or critiquing a source that makes that claim.

Treat generated code as untrusted code until reviewed, tested, scanned, and accepted by an accountable human owner.

## Evidence grades

Use the following evidence grades in the source register.

```text
A = primary source, peer-reviewed article, credible preprint with methods, official government guidance, official security guidance, or reproducible benchmark paper.
B = vendor documentation or official product announcement, used only for product capability, release date, architecture, or stated controls.
C = reputable industry analysis, developer survey, or journalism, used for market context or triangulation.
D = weak, unclear, or unverifiable source; do not use in the main argument unless marked as unverified or illustrative.
```

## Source-register requirement

Every substantive claim in the final research pack should map to a row in:

`research/hmrc-beyond-hype/01_source_register.csv`

Suggested fields:

```text
source_id,title,author_or_org,publication_date,source_type,url,accessed_date,evidence_grade,claim_supported,relevant_quote_short,limitations_or_bias,used_in_sections,verification_status
```

## Claims matrix requirement

For important claims, especially claims that will appear in the talk, create a claims matrix in:

`research/hmrc-beyond-hype/appendices/d_claims_matrix.md`

Suggested columns:

```text
claim | evidence source | supporting quotation or paraphrase | confidence | limitation | safe for talk?
```

## Citation validation rules

For each citation, verify:

1. URL opens.
2. Title matches the cited source.
3. Author or organisation matches.
4. Publication date is correct.
5. The cited claim is actually supported.
6. Source type and evidence grade are recorded.
7. Limitations or bias are recorded.

If a source cannot be verified, mark the claim as unverified and do not rely on it for the main argument.

## Vendor sources

Vendor sources are useful for:

- release dates;
- documented product capabilities;
- product architecture;
- permissions and security controls;
- official claims about intended use.

Vendor sources are not sufficient for independent claims about productivity, safety, quality, reliability, or organisational value. Label vendor claims explicitly.

## Benchmarks

Do not over-claim benchmark results. Discuss:

- task selection;
- benchmark contamination;
- stale benchmark tasks;
- hidden scaffolding;
- test quality;
- ecological validity;
- mismatch with legacy or public-sector estates;
- whether the benchmark measures code generation, issue resolution, long-horizon autonomy, or production readiness.

Benchmark scores should not be treated as procurement evidence unless they are supplemented by local evaluation on representative tasks.

## Productivity evidence

Do not collapse incompatible productivity studies into one headline number. Compare:

- lab tasks versus field tasks;
- novice versus experienced developers;
- greenfield versus brownfield work;
- familiar versus unfamiliar codebases;
- simple implementation versus complex maintenance;
- time-to-first-solution versus quality-adjusted delivery;
- generated code volume versus accepted, reviewed, maintainable code.

A safe synthesis is:

“AI coding support is best understood as a conditional capability amplifier, not a uniform productivity multiplier.”

## Public-sector safety rules

For public-sector engineering, the research should address:

- data leakage;
- secret exposure;
- prompt injection;
- supply-chain risk;
- hallucinated dependencies;
- insecure generated code;
- excessive permissions;
- unsafe network access;
- weak CI/CD controls;
- lack of auditability;
- unclear accountability;
- accessibility and equality impacts;
- human review and service-owner accountability.

## Repo handling rules

When working inside the source repository:

- Do not modify product or application files unless explicitly required for inspection and only if safe.
- Do not request or use secrets.
- Do not use private data.
- Use repo-local evidence for repo-specific claims.
- Record limitations.
- If web access is unavailable, complete the repo-local extraction and produce exact search queries for the missing external evidence.
