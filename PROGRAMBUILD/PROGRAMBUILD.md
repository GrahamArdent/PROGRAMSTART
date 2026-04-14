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
- `PROGRAMBUILD_ADR_TEMPLATE.md` defines the standard ADR structure for material design and policy decisions
- `PROGRAMBUILD_CHANGELOG.md` records how the PROGRAMBUILD system itself changes over time
- `PROGRAMBUILD_KICKOFF_PACKET.md` is the standardized starter pack for new projects
- `PROGRAMBUILD_SUBAGENTS.md` is the subagent catalog with reusable prompts
- `PROGRAMBUILD_CHECKLIST.md` is the execution checklist version of this system
- `PROGRAMBUILD_IDEA_INTAKE.md` is the pre-feasibility challenge interview — run this before filling the inputs block
- `PROGRAMBUILD_CHALLENGE_GATE.md` is the 8-part stage-transition checklist (A–H) with architecture alignment — run this at every stage boundary
- `PROGRAMBUILD_GAMEPLAN.md` is the chained execution sequence with cross-stage validation — use this to run stages in the correct order

---

## 1. How To Use This File

1. Run `PROGRAMBUILD_IDEA_INTAKE.md` before filling the inputs block. The Idea Intake interview challenges the raw idea before any planning begins.
2. Fill in the Inputs block using the Idea Intake output.
3. Decide the dominant `PRODUCT_SHAPE`, whether `USERJOURNEY/` is needed, and which variant fits the risk and team model.
4. Read `PROGRAMBUILD_CANONICAL.md` first and treat it as authoritative when documents disagree.
5. Use `PROGRAMBUILD_FILE_INDEX.md` to locate the right planning artifact.
6. Follow `PROGRAMBUILD_GAMEPLAN.md` to run stages in the correct order with cross-stage validation at each boundary.
7. Run `PROGRAMBUILD_CHALLENGE_GATE.md` at every stage transition. This is not optional.
8. Do not start the next stage until the current stage output is reviewed and the Challenge Gate passes.
9. Treat every interface between layers as a contract that must be explicit and tested in both directions.
10. Use this playbook inside the project repository created from the template. Do not keep filled project outputs in the template repository.

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
PRODUCT_SHAPE:            [web app | mobile app | CLI tool | desktop app | API service | data pipeline | library | other]
KNOWN_CONSTRAINTS:
OUT_OF_SCOPE:
COMPLIANCE_OR_SECURITY_NEEDS:
TEAM_SIZE:
DELIVERY_TARGET:
```

Technology decisions (stack, database, auth, deployment, integrations) belong in `ARCHITECTURE.md`, not the inputs block. The inputs block defines *what* you are building and *why* — not *how*.

### PRODUCT_SHAPE Conditionals

Use `PRODUCT_SHAPE` to decide which guardrails and prompts apply. Do not force every project through a web-app interpretation.

- `web app`: route contracts, authenticated client behavior, UI states, and browser-level E2E coverage usually apply.
- `mobile app`: screen/state flows, client auth handling, offline/retry behavior, and device-level test coverage usually matter more than browser routing.
- `CLI tool`: command contract, config/source-of-truth rules, stdout/stderr behavior, exit codes, and fixture-driven integration tests matter more than UI states.
- `desktop app`: local state, updater behavior, packaging, OS permissions, and crash recovery need explicit treatment.
- `API service`: endpoint contracts, auth, tenancy, schema evolution, observability, and consumer compatibility dominate.
- `data pipeline`: job boundaries, idempotency, scheduling, retry/backfill behavior, and data-quality assertions dominate.
- `library`: public API stability, versioning, compatibility matrix, and examples/tests replace route-focused guidance.
- `other`: define the dominant execution model explicitly in `ARCHITECTURE.md` before adopting guardrails from later stages.

When a stage mentions routes, handlers, UI states, or E2E behavior, interpret that guidance through `PRODUCT_SHAPE` rather than treating every item as mandatory.

### Kickoff Triage

Resolve these choices before you leave Stage 0:

- `PRODUCT_SHAPE`: what execution model actually delivers the value.
- `Variant`: how much evidence and governance the project needs.
- `USERJOURNEY/`: attach it only if onboarding, consent, activation, or first-run routing is part of the product scope.

Bad kickoff pattern:
- picking a stack or variant first, then forcing the product into that shape.

Good kickoff pattern:
- identify the execution model first, then choose the lightest workflow that still matches the delivery risk.

### Inputs Stage Gate Status

| Item | Status | Notes |
|---|---|---|
| Core inputs block completed | Pending | All required fields populated above |
| Project name assigned | Pending | Must be set before advancing to feasibility |
| Product shape identified | Pending | Drives which architecture patterns and guardrails apply |
| USERJOURNEY decision recorded | Pending | Attach only if real end-user onboarding or activation design exists |
| Delivery target set | Pending | Set after feasibility stage completes |
| Variant selected | Pending | Choose lite, product, or enterprise |
| Inputs reviewed by product owner | Pending | Use dashboard Signoff action to record approval |

---

## 3. Core Rules

- No hardcoded API paths outside the route contract layer.
- No raw network calls for authenticated endpoints outside the approved auth-aware client.
- No endpoint is considered done until auth behavior, schema shape, and route registration are tested.
- No feature is considered done until it has loading, success, empty, and error behavior where applicable.
- No release is considered ready without rollback, observability, and support ownership.
- Every material decision should be recorded in `DECISION_LOG.md`; enterprise work should promote major architecture or policy changes into ADRs.
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
- `PROGRAMBUILD_ADR_TEMPLATE.md`
- `PROGRAMBUILD_CHANGELOG.md`
- `PROGRAMBUILD_KICKOFF_PACKET.md`
- `PROGRAMBUILD_SUBAGENTS.md`
- `PROGRAMBUILD_CHECKLIST.md`
- `PROGRAMBUILD_IDEA_INTAKE.md`
- `PROGRAMBUILD_CHALLENGE_GATE.md`
- `PROGRAMBUILD_GAMEPLAN.md`

Recommended stage outputs for each project:
- `FEASIBILITY.md`
- `DECISION_LOG.md`
- `RESEARCH_SUMMARY.md`
- `REQUIREMENTS.md`
- `USER_FLOWS.md`
- `ARCHITECTURE.md`
- `RISK_SPIKES.md`
- `TEST_STRATEGY.md`
- `RELEASE_READINESS.md`
- `AUDIT_REPORT.md`
- `POST_LAUNCH_REVIEW.md`

---

## 5. Suggested Subagents

If you are using an AI workflow with subagents, assign specialized work instead of asking one agent to do everything.

See `PROGRAMBUILD_SUBAGENTS.md` for full agent definitions, prompts, and invocation triggers.

Core agents (run in sequence for every build):

| Agent | Use for | Workspace agent |
|---|---|---|
| Discovery & Scoping | domain research, scope, user stories, kill criteria, user flows | `.github/agents/discovery-scoping.agent.md` |
| Architecture & Security | system boundaries, API contracts, auth model, threat model | `.github/agents/architecture-security.agent.md` |
| Quality & Release | test strategy, release readiness, launch gate | `.github/agents/quality-release.agent.md` |

On-demand agents (trigger only when the condition is met):

| Agent | Trigger | Use for |
|---|---|---|
| Risk Spike Agent | unknown rated medium or high impact in RISK_SPIKES.md | prototype risky integrations, auth flow, streaming, AI cost |
| Contract Auditor | Stage 9 audit or any mid-implementation alignment check | route, auth, schema, and contract drift |

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
| 10 | Post-launch review and retrospective | `POST_LAUNCH_REVIEW.md` | learnings captured and follow-up owners assigned |

---

## 7. Gate Model By Variant

The stage order stays stable across variants, but the gate strength changes based on what you are building.

| Variant | Gate style | Evidence expectation |
|---|---|---|
| Lite | lightweight pass/fail notes | short decision notes and the minimum viable proof to move forward |
| Product | must-meet and should-meet review | explicit decision log entries, approved outputs, and coverage expectations |
| Enterprise | scored gate with sign-off and retained evidence | approvals, ADRs for material changes, control traceability, and review evidence |

Use this default playbook as the balanced middle. Do not force enterprise ceremony into small-business or prototype work, and do not let high-risk enterprise work run with lite evidence.

Variant selection is independent from `PRODUCT_SHAPE`:
- a background automation can be lite, product, or enterprise depending on blast radius and governance needs
- an interactive end-user product can still be lite if it is small and low-risk
- `USERJOURNEY/` is decided by whether interactive onboarding/activation design exists, not by variant alone

Every stage gate should answer:
- Did any kill criteria from `FEASIBILITY.md` become true?
- Are the must-meet conditions satisfied?
- What decision should be recorded in `DECISION_LOG.md`?

Recommended gate scoring pattern:
- Lite: pass/fail note written by the owner
- Product: all must-meet items pass and most should-meet items pass
- Enterprise: all must-meet items pass, score recorded, approver named, evidence retained

ADR threshold for a mostly solo workflow:
- Use `DECISION_LOG.md` by default.
- Promote a decision to an ADR only when at least 2 of these are true:
- it changes a core contract, auth rule, data policy, deployment model, or vendor dependency
- it affects 3 or more files or more than 1 stage of the workflow
- reversing it would likely cost more than 1 focused workday
- you expect to revisit the reasoning later and a short decision-log row would be insufficient

---

## 8. Stage 1: Feasibility And Kill Criteria

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
8. Rough cost and effort estimate
9. Recommendation: go, limited spike, or no-go
```

Gate:
Do not proceed without an explicit go or limited-spike decision, and record that decision in `DECISION_LOG.md`.

---

## 9. Stage 2: Research

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

## 10. Stage 3: Requirements And UX

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

## 11. Stage 4: Architecture And Risk Spikes

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

First adapt the deliverable to `PRODUCT_SHAPE`:
- if `web app` or `mobile app`, include client/server boundaries and user-facing state transitions
- if `API service`, emphasize endpoint contracts, auth, versioning, and consumers
- if `data pipeline`, emphasize job stages, inputs/outputs, scheduling, and recovery
- if `library`, emphasize public API surface, compatibility guarantees, and examples
- if `CLI tool` or `desktop app`, emphasize command or application lifecycle, packaging, local state, and update strategy

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

## 12. Stage 5: Scaffold And Guardrails

Purpose:
Set the rules of the system before feature work begins.

Output:
Working repo skeleton with CI and structural tests.

Required guardrails (adapt to product shape — not all apply to every architecture):
- route or endpoint contract layer with canonical, deprecated, and planned states
- auth-aware client (and authenticated streaming helper if applicable)
- service or handler registration pattern for all endpoints
- repo-boundary consent rule for AI-assisted work: do not inspect, edit, stage, commit, or push another repository unless the user explicitly names it and asks for that action
- CI with lint, types, tests, build, and timeouts
- local bootstrap command with no tribal knowledge

Required structural tests (select those applicable to your architecture):
- route alignment: declared routes or endpoints resolve to live handlers
- reverse alignment: live handlers are either used or explicitly documented
- auth client discipline: authenticated endpoints do not use raw network calls
- auth matrix: 401, 403, and cross-tenant expectations are enforced
- schema completeness: declared interfaces map to actual handler contracts
- no hardcoded URLs or paths outside the contract layer
- planned-route safety: stubs are documented and not accidentally called from live code

Prompt template:

```text
Create the project scaffold only.
Do not implement product features.

Inputs:
- Architecture
- User flows

Apply only the scaffold elements that fit `PRODUCT_SHAPE`. Do not invent route layers, UI shells, or browser tooling for shapes that do not need them.

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

## 13. Stage 6: Test Strategy

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

Use `PRODUCT_SHAPE` to determine the dominant test layers. Browser E2E is not universal.

Include:
1. Test pyramid targets
2. Unit test rules
3. Component test rules
4. Service-layer purpose and auth test rules
5. Golden baseline policy
7. E2E and smoke/regression strategy
7. Test data and fixture strategy
8. Requirements traceability matrix
9. Endpoint-to-test registry
10. Gap analysis
```

Non-negotiables:
- golden tests use the exact production code path
- mocked shapes match real contract shapes
- auth behavior is tested explicitly, not assumed
- every endpoint appears in a registry that points to its tests

Gate:
No feature implementation starts until the test model is approved.

---

## 14. Stage 7: Implementation Loop

Purpose:
Build one feature at a time with a repeatable definition of done.

Output:
Working feature code with complete coverage for its risk profile.

Implementation loop (adapt to architecture — not all steps apply to every product shape):
1. Write purpose and auth tests first.
2. Implement service contract and validation.
3. Register endpoint and keep alignment tests green.
4. Implement client or consumer layer using contract constants and auth-aware helpers.
5. Build user-facing layer with loading, success, empty, and error states where applicable.
6. Add component or integration tests.
7. Add E2E coverage for P0 behavior.
8. Add or update golden baseline if the feature produces complex or AI-driven output.
9. Update the endpoint-to-test registry.
10. Re-run the relevant structural tests.

Definition of done:
- contract shape matches between producer and consumer layers
- auth behavior is verified
- endpoint or route registration is verified
- user-visible states are covered where applicable
- logging and error handling are in place
- decision log or ADR updated if the design changed

Prompt template:

```text
Implement one feature using the approved contracts and test strategy.

Inputs:
- Feature user story
- Relevant API contract rows
- Relevant user flow
- Relevant test strategy rows

Adapt the implementation steps to `PRODUCT_SHAPE` rather than assuming a web frontend and backend split.

Follow the implementation loop exactly and stop if any gate cannot be met.
```

---

## 15. Stage 8: Release Readiness

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

## 16. Stage 9: Audit And Drift Control

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

## 17. Stage 10: Post-Launch Review And Retrospective

Purpose:
Close the loop after launch by comparing intended outcomes against reality and capturing lessons before they are forgotten.

Output:
`POST_LAUNCH_REVIEW.md`

Must answer:
- Did the product achieve the stated success metric?
- Which decisions were validated, reversed, or deferred?
- What incidents, support issues, or adoption gaps appeared after launch?
- What follow-up changes should be scheduled and owned?

Prompt template:

```text
Create POST_LAUNCH_REVIEW.md.

Inputs:
- Success metric from the inputs block
- Release readiness decision
- Audit findings
- Early production signals

Include:
1. Launch summary
2. Metrics versus targets
3. Incident and support notes
4. Decision reversals or confirmations
5. Lessons learned
6. Follow-up actions with owners
7. Template improvement proposals — for each systemic lesson, propose a specific
   update to a PROGRAMBUILD template file (see PROGRAMBUILD_GAMEPLAN.md Stage 10
   for the Template Improvement Review format and target mapping)
```

Gate:
Do not treat the project as complete until lessons learned, follow-up ownership, and template improvement proposals are recorded. If 3+ projects produce the same systemic lesson without a template update, the system has a feedback failure.

---

## 18. Additional Operating Practices

These should be established as early as possible:

- Environment parity: CI and production should be materially similar.
- Dependency hygiene: pin dependencies, review updates on a schedule, and run dependency scanning in CI. Use the KB (`config/knowledge-base.json`) and `programstart research --status` to check for superseded, deprecated, or stale dependencies at every Challenge Gate from Stage 4 onward.
- Secret management: no secrets in code, examples only in committed env templates.
- Migration discipline: versioned migrations, tested in CI, with rollback thought through before merge.
- Feature flags: use for incomplete or high-risk releases, and define removal criteria.
- Performance budgets: set them early and enforce them automatically.
- Accessibility: build it into component and E2E tests, not as a cleanup pass.
- Error boundaries and user-facing fallbacks: every async path must fail safely.
- ADRs: record material architecture and policy decisions when they change.
- Decision reversal discipline: when a decision is overridden, add a new `REVERSED` entry referencing the original decision ID, and mark the original `SUPERSEDED`. Both entries must exist. See `PROGRAMBUILD_CHALLENGE_GATE.md` Part F for the format.
- Ownership clarity: assign a named owner or `[ASSIGN]` placeholder in every output file until ownership is confirmed.
- Requirements traceability: map requirement IDs to architecture choices and release-blocking tests.
- Dependency review: document critical vendors, third-party services, and fallback behavior before release.
- Maintain `PROGRAMBUILD_FILE_INDEX.md` whenever a critical file is added, renamed, deprecated, or replaced.
- Update `PROGRAMBUILD_CANONICAL.md` whenever document authority changes.
- Repository scope is explicit in AI-assisted workflows: keep work inside the current repo unless the user explicitly names another repo and asks for that action.

---

## 19. Which Variant To Use

Use [PROGRAMBUILD_LITE.md](PROGRAMBUILD_LITE.md) when:
- one developer or a very small team is building quickly
- the domain is low risk
- a lean delivery cycle matters more than full governance
- the dominant execution mode can still be a service, CLI, automation, or small interactive product, but the blast radius stays limited

Use [PROGRAMBUILD_PRODUCT.md](PROGRAMBUILD_PRODUCT.md) when:
- the product or service is meant to ship reliably
- multiple engineers are contributing
- quality gates matter, but enterprise ceremony would be excessive
- the system may be interactive or background, but it has enough operational weight that partial guardrails are not acceptable

Use [PROGRAMBUILD_ENTERPRISE.md](PROGRAMBUILD_ENTERPRISE.md) when:
- the product touches regulated data or multiple business units
- auditability, approvals, and operational readiness are mandatory
- the cost of failure is materially higher than the cost of extra process
- the dominant execution mode may be end-user, operator-driven, or fully automated; the gate strength follows risk, not UI presence

---

## 20. Cardinal Lessons

- The most expensive bugs usually come from missing contracts, not missing features.
- If a route, auth rule, schema, or user-state expectation is implicit, it will drift.
- Research reduces bad bets.
- Risk spikes reduce expensive surprises.
- Structural tests prevent recurrence better than retrospective debugging.
- Release readiness is an engineering concern, not a postscript.

---

Last updated: 2026-03-27
Source: lessons from route alignment failures, auth bypasses, response schema drift, and test blind spots discovered in production projects
