# PROGRAMBUILD_PRODUCT.md

# Program Build Product

Use this version for a normal production product: customer-facing, multi-feature, and maintained by a small or medium-sized team.
This is the recommended default for most real applications.

Authority:
- `PROGRAMBUILD_CANONICAL.md` defines source-of-truth rules
- `PROGRAMBUILD_FILE_INDEX.md` is the lookup table for critical files

---

## When To Use

Use this file when:
- the team is 3 to 12 people
- the product is customer-facing or revenue-affecting
- multiple feature areas share contracts and infrastructure
- quality gates matter more than pure speed

---

## Required Stages

| Stage | Output | Gate |
|---|---|---|
| Feasibility | `FEASIBILITY.md` | go or limited spike |
| Research | `RESEARCH_SUMMARY.md` | decisions reviewed |
| Requirements and UX | `REQUIREMENTS.md`, `USER_FLOWS.md` | scope approved |
| Architecture and risk spikes | `ARCHITECTURE.md`, `RISK_SPIKES.md` | contracts approved |
| Scaffold and guardrails | repo skeleton and CI | structural tests green |
| Test strategy | `TEST_STRATEGY.md` | coverage approved |
| Implementation loop | feature code | feature DoD |
| Release readiness | `RELEASE_READINESS.md` | go / no-go |
| Audit | `AUDIT_REPORT.md` | critical issues resolved |

---

## Required Guardrails

- route constants with canonical, deprecated, and planned states
- auth-aware API and streaming clients
- auth matrix tests
- route alignment and reverse alignment tests
- schema completeness checks
- no hardcoded URL checks
- endpoint-to-test registry
- Playwright smoke suite on PRs
- nightly regression and golden runs
- critical planning files follow the `PROGRAMBUILD_*.md` naming convention

---

## Suggested Subagents

| Subagent | Use for | Output |
|---|---|---|
| Research Scout | stack and market validation | research summary |
| Product Analyst | requirements and acceptance criteria | requirements draft |
| UX Flow Designer | user journeys and failure states | user flows |
| Architecture Reviewer | contracts, auth, and boundaries | architecture review |
| Risk Spike Agent | unknowns around integrations, AI, streaming, or auth | spike report |
| Test Planner | full pyramid, registry, and fixture strategy | test strategy |
| Contract Auditor | route, auth, and schema alignment checks | audit findings |
| Release Readiness Reviewer | launch, rollback, monitoring, and runbook review | readiness report |

---

## Product Prompt Pattern

```text
Create a full product delivery plan for this application.

Inputs:
- project inputs block

Produce:
1. feasibility and kill criteria
2. research summary
3. requirements and user flows
4. architecture and risk spikes
5. scaffold and structural tests
6. test strategy with smoke and regression split
7. feature implementation loop
8. release readiness plan
9. post-build audit plan
```

---

## Product Definition Of Done

- every endpoint is declared, registered, and covered by the registry
- auth, schema, and route behavior are verified structurally
- primary user journeys have Playwright smoke coverage
- release readiness includes rollback, monitoring, and ownership
- audit finds no unresolved critical issues

---

Last updated: 2026-03-27