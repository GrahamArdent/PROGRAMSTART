# PROGRAMBUILD.md

# Master Program Build Playbook

This is the default playbook for building a new software product with strong engineering discipline and low rework.
It is organized around decision gates, not just task lists.
The point is to prevent the predictable failures that usually appear later as silent bugs, auth gaps, schema drift, route drift, weak test coverage, and launch surprises.

Use this file when you want a balanced process: strong enough for a real production system, lighter than a full enterprise program.

Companion variants:
- `PROGRAMBUILD_LITE.md` for solo, prototype, or very small product work
- `PROGRAMBUILD_PRODUCT.md` for standard production product teams
- `PROGRAMBUILD_ENTERPRISE.md` for regulated, multi-team, audit-heavy delivery

Control files:
- `PROGRAMBUILD_CANONICAL.md` is the source of truth for document authority, naming, and stage ownership
- `PROGRAMBUILD_FILE_INDEX.md` is the index of all critical planning files and their roles
- `PROGRAMBUILD_KICKOFF_PACKET.md` is the standardized starter pack for new projects
- `PROGRAMBUILD_SUBAGENTS.md` is the subagent catalog with reusable prompts
- `PROGRAMBUILD_CHECKLIST.md` is the execution checklist version of this system

---

## 1. How To Use This File

1. Fill in the Inputs block.
2. Pick the correct variant if this default playbook is too heavy or too light.
3. Read `PROGRAMBUILD_CANONICAL.md` first and treat it as authoritative when documents disagree.
4. Use `PROGRAMBUILD_FILE_INDEX.md` to locate the right planning artifact.
5. Complete each stage in order.
6. Do not start the next stage until the current stage output is reviewed.
7. Treat every interface between layers as a contract that must be explicit and tested in both directions.

---

## 2. Inputs

Fill these in once. Reuse them in every stage.

```text
PROJECT_NAME:
ONE_LINE_DESCRIPTION:
PRIMARY_USER:
SECONDARY_USER:
CORE_PROBLEM:
SUCCESS_METRIC:
FRONTEND_STACK:
BACKEND_STACK:
AUTH_MECHANISM:
HTTP_CLIENT:
DATABASE:
DEPLOYMENT_TARGET:
INTEGRATIONS:
KNOWN_CONSTRAINTS:
OUT_OF_SCOPE:
COMPLIANCE_OR_SECURITY_NEEDS:
TEAM_SIZE:
DELIVERY_TARGET:
```

---

## 3. Core Rules

- No hardcoded API paths outside the route contract layer.
- No raw network calls for authenticated endpoints outside the approved auth-aware client.
- No endpoint is considered done until auth behavior, schema shape, and route registration are tested.
- No feature is considered done until it has loading, success, empty, and error behavior where applicable.
- No release is considered ready without rollback, observability, and support ownership.
- `PROGRAMBUILD_CANONICAL.md` defines which document is authoritative for each concern.
- No document claim survives conflict with validated code, tests, or the canonical authority map.

---

## 4. Naming Convention For Critical Files

Critical planning and control files use one prefix: `PROGRAMBUILD_`.

Rules:
- Use uppercase snake case for all critical markdown control files.
- Use singular names when the file defines one authority, standard, or checklist.
- Use plural names only for registers or catalogs.
- Do not create alternative names for the same purpose.

Required critical files:
- `PROGRAMBUILD_CANONICAL.md`
- `PROGRAMBUILD_FILE_INDEX.md`
- `PROGRAMBUILD_KICKOFF_PACKET.md`
- `PROGRAMBUILD_SUBAGENTS.md`
- `PROGRAMBUILD_CHECKLIST.md`

Recommended stage outputs for each project:
- `FEASIBILITY.md`
- `RESEARCH_SUMMARY.md`
- `REQUIREMENTS.md`
- `USER_FLOWS.md`
- `ARCHITECTURE.md`
- `RISK_SPIKES.md`
- `TEST_STRATEGY.md`
- `RELEASE_READINESS.md`
- `AUDIT_REPORT.md`

---

## 5. Suggested Subagents

If you are using an AI workflow with subagents, assign specialized work instead of asking one agent to do everything.

Recommended subagents:

| Subagent | Use for | Deliverable |
|---|---|---|
| Research Scout | competitor scan, stack validation, compliance scan, tooling survey | research summary with sources |
| Product Analyst | user stories, acceptance criteria, scope boundaries, kill criteria | requirements draft |
| UX Flow Designer | primary user workflows, empty/error states, navigation, accessibility flow | workflow map and UX notes |
| Architecture Reviewer | topology, boundaries, data ownership, API contracts, auth model | architecture review |
| Risk Spike Agent | prototype risky integrations, auth flow, streaming, file processing, AI cost assumptions | spike report |
| Contract Auditor | compare frontend route constants, backend handlers, schemas, and auth enforcement | alignment report |
| Test Planner | test matrix, fixture strategy, smoke/regression split, golden baseline policy | test strategy |
| Security Reviewer | threat modeling, auth matrix, secret handling, tenancy rules, abuse cases | security findings |
| Release Readiness Reviewer | rollback, monitoring, SLOs, deployment gates, operational gaps | launch readiness report |

Guidance:
- Use subagents for parallel research and review work.
- Use the main agent for synthesis, decisions, and code edits.
- Require each subagent to return findings, risks, and unresolved assumptions.

---

## 6. Stage Overview

| Stage | Purpose | Main output | Gate |
|---|---|---|---|
| 0 | Inputs and mode selection | completed inputs block | human review |
| 1 | Feasibility and kill criteria | `FEASIBILITY.md` | clear go / no-go |
| 2 | Research | `RESEARCH_SUMMARY.md` | stack and market confidence |
| 3 | Requirements and UX | `REQUIREMENTS.md` and `USER_FLOWS.md` | approved scope and workflows |
| 4 | Architecture and risk spikes | `ARCHITECTURE.md` and `RISK_SPIKES.md` | approved contracts and resolved unknowns |
| 5 | Scaffold and guardrails | working skeleton and CI gates | structural tests green |
| 6 | Test strategy | `TEST_STRATEGY.md` | coverage plan approved |
| 7 | Implementation loop | feature code and tests | feature DoD complete |
| 8 | Release readiness | `RELEASE_READINESS.md` | deploy gate passed |
| 9 | Audit and drift control | `AUDIT_REPORT.md` | critical gaps resolved |

---

## 7. Stage 1: Feasibility And Kill Criteria

Purpose:
Decide whether the product is worth building before substantial design or implementation effort.

Output:
`FEASIBILITY.md`

Must answer:
- Is the problem real and specific?
- Is the proposed solution materially better than current alternatives?
- What would cause us to stop or reshape the project early?
- What are the top 3 business and technical risks?

Prompt template:

```text
Create FEASIBILITY.md for this product.

Inputs:
- Project inputs block

Produce:
1. Problem statement
2. Primary user pain and evidence
3. Existing alternatives and why they are insufficient
4. Business viability assumptions
5. Technical feasibility assumptions
6. Top 3 risks
7. Kill criteria: what evidence would stop or materially redirect this project
8. Recommendation: go, limited spike, or no-go
```

Gate:
Do not proceed without an explicit go or limited-spike decision.

---

## 8. Stage 2: Research

Purpose:
Validate stack choices, understand the market, identify constraints, and find avoidable failure patterns before architecture is locked.

Output:
`RESEARCH_SUMMARY.md`

Must answer:
- What already exists?
- Which stack choices are mature and supportable?
- Which compliance, AI, or integration concerns matter?
- Which pitfalls are expensive if discovered late?

Prompt template:

```text
Create RESEARCH_SUMMARY.md for this product.

Inputs:
- Project inputs block
- Feasibility outcome

Produce sections for:
1. Existing solutions and competitors
2. Technology validation
3. AI and automation opportunities
4. Compliance and regulatory considerations
5. Tooling recommendations
6. Known failure patterns and how to prevent them

End with a decisions table:
| Decision | Proposed choice | Alternatives | Confidence | Open question |
```

Gate:
Any low-confidence decision must be explicitly approved or deferred into a risk spike.

---

## 9. Stage 3: Requirements And UX

Purpose:
Define what gets built, for whom, and how success is measured. This stage closes the gap between product intent and engineering work.

Outputs:
- `REQUIREMENTS.md`
- `USER_FLOWS.md`

Must answer:
- What are the P0, P1, and P2 outcomes?
- What does the user do step by step?
- What is out of scope?
- What assumptions still need confirmation?

Prompt template:

```text
Create REQUIREMENTS.md and USER_FLOWS.md.

Inputs:
- Project inputs block
- Feasibility outcome
- Research summary

REQUIREMENTS.md must include:
1. Functional requirements with IDs
2. Non-functional requirements with measurable targets
3. User stories for all P0 and P1 items
4. Out-of-scope register
5. Assumption register

USER_FLOWS.md must include:
1. Primary user journeys
2. Entry points and exits
3. Loading, empty, error, and retry states
4. Permissions and role-sensitive flows
5. Accessibility-sensitive interactions
```

Gate:
No architecture work begins until scope, user stories, and workflows are approved.

---

## 10. Stage 4: Architecture And Risk Spikes

Purpose:
Define the system contract and reduce uncertainty before scaffolding or implementation.

Outputs:
- `ARCHITECTURE.md`
- `RISK_SPIKES.md`

Must answer:
- What are the services, boundaries, data owners, and auth rules?
- What are the exact endpoint contracts?
- What technical unknowns need proof before committing to the design?

Prompt template:

```text
Create ARCHITECTURE.md and RISK_SPIKES.md.

Inputs:
- Project inputs block
- Requirements
- User flows
- Research summary

ARCHITECTURE.md must include:
1. System topology
2. Technology decision table
3. API contract table
4. Data model and ownership
5. Route contract plan
6. Auth matrix
7. Error contract
8. Environment strategy
9. Observability plan

RISK_SPIKES.md must include:
1. Top 3 to 5 technical unknowns
2. Small prototype or investigation plan for each
3. Success and failure criteria
4. Result summary
5. Decision taken after each spike
```

Mandatory spike candidates:
- authentication and session lifecycle
- streaming or long-lived connection behavior
- external integrations
- AI or model cost/latency assumptions
- file handling or document processing

Gate:
Do not scaffold until the architecture is approved and the high-risk unknowns have been resolved or explicitly accepted.

---

## 11. Stage 5: Scaffold And Guardrails

Purpose:
Set the rules of the system before feature work begins.

Output:
Working repo skeleton with CI and structural tests.

Required guardrails:
- route contract layer with canonical, deprecated, and planned route states
- auth-aware HTTP client and a separate authenticated streaming helper
- backend registration pattern for all routes
- CI with lint, types, tests, build, and timeouts
- local bootstrap command with no tribal knowledge

Required structural tests:
- route alignment: frontend declared routes resolve to live backend handlers
- reverse alignment: live backend handlers are either used or explicitly documented
- auth client discipline: authenticated endpoints do not use raw network calls
- auth matrix: 401, 403, and cross-tenant expectations are enforced
- schema completeness: frontend interfaces map to backend schema contracts
- no hardcoded URLs outside the route contract layer
- planned-route safety: stubs are documented and not accidentally called from live UI

Prompt template:

```text
Create the project scaffold only.
Do not implement product features.

Inputs:
- Architecture
- User flows

Produce:
1. Repo structure
2. Route contract layer
3. Auth-aware client layer
4. Structural test suite
5. CI pipeline with explicit timeouts
6. PR checklist and conventions
7. One-command local setup
8. Deprecation pattern
```

Gate:
Feature work starts only after every structural test is green.

---

## 12. Stage 6: Test Strategy

Purpose:
Decide the testing model before writing features so coverage is designed, not improvised.

Output:
`TEST_STRATEGY.md`

Must answer:
- What belongs in unit, component, purpose, golden, and E2E tests?
- What fixtures exist and who owns them?
- Which tests block PRs, nightly runs, and releases?

Prompt template:

```text
Create TEST_STRATEGY.md.

Inputs:
- Requirements
- User flows
- Architecture

Include:
1. Test pyramid targets
2. Unit test rules
3. Component test rules
4. Backend purpose and auth test rules
5. Golden baseline policy
6. Playwright and Chromium smoke/regression strategy
7. Test data and fixture strategy
8. Endpoint-to-test registry
9. Gap analysis
```

Non-negotiables:
- golden tests use the exact production code path
- mocked shapes match real contract shapes
- auth behavior is tested explicitly, not assumed
- every endpoint appears in a registry that points to its tests

Gate:
No feature implementation starts until the test model is approved.

---

## 13. Stage 7: Implementation Loop

Purpose:
Build one feature at a time with a repeatable definition of done.

Output:
Working feature code with complete coverage for its risk profile.

Implementation loop:
1. Write purpose and auth tests first.
2. Implement backend contract and validation.
3. Register route and keep alignment tests green.
4. Implement typed frontend API client using route constants and auth-aware client helpers.
5. Build UI with loading, success, empty, and error states.
6. Add component tests.
7. Add Playwright coverage for P0 behavior.
8. Add or update golden baseline if the feature produces complex or AI-driven output.
9. Update the endpoint-to-test registry.
10. Re-run the relevant structural tests.

Definition of done:
- contract shape matches in frontend and backend
- auth behavior is verified
- route registration is verified
- user-visible states are covered
- logging and error handling are in place
- release notes or ADR updated if the design changed

Prompt template:

```text
Implement one feature using the approved contracts and test strategy.

Inputs:
- Feature user story
- Relevant API contract rows
- Relevant user flow
- Relevant test strategy rows

Follow the implementation loop exactly and stop if any gate cannot be met.
```

---

## 14. Stage 8: Release Readiness

Purpose:
Prevent “it passed tests” from being mistaken for “it is safe to launch.”

Output:
`RELEASE_READINESS.md`

Must answer:
- Can we deploy and roll back safely?
- Do we have visibility into failures?
- Are support, ownership, and operational procedures defined?

Prompt template:

```text
Create RELEASE_READINESS.md.

Inputs:
- Architecture
- Test strategy
- Current implementation status

Include:
1. Launch scope and excluded items
2. Environment readiness
3. Migration and rollback plan
4. SLOs and monitoring
5. Alert thresholds and escalation path
6. Security checklist
7. Support runbook ownership
8. Smoke test list for release day
9. Go / no-go recommendation with risks
```

Minimum gate:
- deployment path validated
- rollback path validated
- secrets and config verified
- critical smoke tests pass
- monitoring and alerts active

---

## 15. Stage 9: Audit And Drift Control

Purpose:
Catch silent breakage and contract drift after features have accumulated.

Output:
`AUDIT_REPORT.md`

Audit checklist:
- route and endpoint alignment in both directions
- response schema consistency
- auth wrapper consistency, especially for streaming and admin paths
- test coverage blind spots
- planned and deprecated route safety
- invalid-input behavior and error quality
- multi-user and cross-tenant isolation behavior
- release-readiness drift between docs and implementation

Prompt template:

```text
Audit the application for silent failures, drift, and release risk.

Produce findings with:
- severity
- category
- evidence
- impact
- minimum fix
- prevention test or guardrail
```

Gate:
All critical and high findings must have owners, fixes, or explicit acceptance before release.

---

## 16. Additional Operating Practices

These should be established as early as possible:

- Environment parity: CI and production should be materially similar.
- Dependency hygiene: pin dependencies, review updates on a schedule, and run dependency scanning in CI.
- Secret management: no secrets in code, examples only in committed env templates.
- Migration discipline: versioned migrations, tested in CI, with rollback thought through before merge.
- Feature flags: use for incomplete or high-risk releases, and define removal criteria.
- Performance budgets: set them early and enforce them automatically.
- Accessibility: build it into component and E2E tests, not as a cleanup pass.
- Error boundaries and user-facing fallbacks: every async path must fail safely.
- ADRs: record material architecture and policy decisions when they change.
- Maintain `PROGRAMBUILD_FILE_INDEX.md` whenever a critical file is added, renamed, deprecated, or replaced.
- Update `PROGRAMBUILD_CANONICAL.md` whenever document authority changes.

---

## 17. Which Variant To Use

Use [PROGRAMBUILD_LITE.md](PROGRAMBUILD_LITE.md) when:
- one developer or a very small team is building quickly
- the domain is low risk
- a lean delivery cycle matters more than full governance

Use [PROGRAMBUILD_PRODUCT.md](PROGRAMBUILD_PRODUCT.md) when:
- the product is customer-facing and meant to ship reliably
- multiple engineers are contributing
- quality gates matter, but enterprise ceremony would be excessive

Use [PROGRAMBUILD_ENTERPRISE.md](PROGRAMBUILD_ENTERPRISE.md) when:
- the product touches regulated data or multiple business units
- auditability, approvals, and operational readiness are mandatory
- the cost of failure is materially higher than the cost of extra process

---

## 18. Cardinal Lessons

- The most expensive bugs usually come from missing contracts, not missing features.
- If a route, auth rule, schema, or user-state expectation is implicit, it will drift.
- Research reduces bad bets.
- Risk spikes reduce expensive surprises.
- Structural tests prevent recurrence better than retrospective debugging.
- Release readiness is an engineering concern, not a postscript.

---

Last updated: 2026-03-27
Source: lessons from route alignment failures, auth bypasses, response schema drift, and test blind spots discovered in production projects
