# PROGRAMBUILD_PRODUCT.md

# Program Build Product

Use this version for a normal production product: customer-facing or operationally important, multi-feature, and maintained by a small or medium-sized team.
This is the recommended default for most real applications.

Authority:
- `PROGRAMBUILD_CANONICAL.md` defines source-of-truth rules
- `PROGRAMBUILD_FILE_INDEX.md` is the lookup table for critical files
- `PROGRAMBUILD_IDEA_INTAKE.md` runs before Stage 0 — challenge the idea before filling the inputs block
- `PROGRAMBUILD_CHALLENGE_GATE.md` runs at every stage transition — all 7 parts required; Part G required at Stages 4+
- `PROGRAMBUILD_GAMEPLAN.md` defines the execution order with full cross-stage validation

---

## When To Use

Use this file when:
- the team is 3 to 12 people
- the product is customer-facing, revenue-affecting, or operationally important
- multiple feature areas share contracts and infrastructure
- quality gates matter more than pure speed

This variant fits both interactive products and non-interactive systems such as APIs, internal services, and background automations that still need real release discipline.

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
| Post-launch review | `POST_LAUNCH_REVIEW.md` | lessons captured and follow-up owned |

---

## Required Guardrails

- contract layer with canonical, deprecated, and planned states for routes, endpoints, commands, jobs, or public APIs
- auth-aware API client, trusted caller helper, or equivalent boundary adapter
- auth matrix tests
- alignment and reverse-alignment tests for the dominant contract surface
- schema completeness checks
- no hardcoded contract identifier checks
- requirements-to-test traceability
- contract-to-test registry
- smoke suite for the dominant execution mode on PRs
- nightly regression and golden runs
- decision log updates for material changes
- critical planning files follow the `PROGRAMBUILD_*.md` naming convention

Attach `USERJOURNEY/` only when the product has real end-user onboarding, consent, activation, or first-run routing behavior to design.

---

## Suggested Subagents

See `PROGRAMBUILD_SUBAGENTS.md` for full prompts and workspace agent files.

| Agent | Use for | Output |
|---|---|---|
| Discovery & Scoping | domain research, scope, user stories, kill criteria, user flows | research + requirements draft |
| Architecture & Security | system boundaries, API contracts, auth model, threat model | architecture review + security findings |
| Quality & Release | test strategy, release readiness, launch gate | test strategy + readiness report |
| Risk Spike Agent | unknowns rated medium or high impact in RISK_SPIKES.md | spike report |
| Contract Auditor | route, auth, schema, and contract drift at Stage 9 | audit findings |

---

## Product Prompt Pattern

```text
Create a full product delivery plan for this application.

Inputs:
- project inputs block

Produce:
1. feasibility and kill criteria
2. decision log entries for each gate
3. research summary
4. requirements and workflows appropriate to the product shape
5. architecture and risk spikes
6. scaffold and structural tests
7. test strategy with smoke and regression split for the dominant execution mode
8. feature implementation loop
9. release readiness plan
10. post-build audit plan
11. post-launch review plan
```

---

## Product Definition Of Done

- every dominant contract surface is declared, registered, and covered by the registry
- auth, trust-boundary, schema, and contract behavior are verified structurally
- primary execution scenarios have smoke coverage
- release readiness includes rollback, monitoring, and ownership
- audit finds no unresolved critical issues
- post-launch review records actual outcomes against the success metric

---

Last updated: 2026-03-31
