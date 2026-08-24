# PROGRAMBUILD.md

# Master Program Build Playbook

This is the default playbook for building or materially improving a software product with strong engineering discipline and low rework.
It is organized around decision gates, not just task lists.
The point is to prevent predictable failures such as silent bugs, auth gaps, schema drift, route drift, weak test coverage, duplicated planning authority, stale context, repeated low-value verification, and launch surprises.

Use this file when you want a balanced process: strong enough for a real production system, lighter than a full enterprise program.

Companion variants:
- `PROGRAMBUILD_LITE.md` for solo, prototype, or very small product work
- `PROGRAMBUILD_PRODUCT.md` for standard production product teams
- `PROGRAMBUILD_ENTERPRISE.md` for regulated, multi-team, audit-heavy delivery

Control files:
- `PROGRAMBUILD_CANONICAL.md` is the source of truth for document authority, naming, and stage ownership
- `PROGRAMBUILD_FILE_INDEX.md` is the index of all critical planning files and their roles
- `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` defines planning entry modes, one-spine authority, proportional rigor, task-scoped context loading, evidence reuse, and research-to-plan delta rules
- `PROGRAMBUILD_WORK_PACKET.md` defines the standard derived active-work packet; filled packets never outrank project authority
- `PROGRAMBUILD_ADR_TEMPLATE.md` defines the standard ADR structure for material design and policy decisions
- `PROGRAMBUILD_CHANGELOG.md` records how the PROGRAMBUILD system itself changes over time
- `PROGRAMBUILD_KICKOFF_PACKET.md` is the standardized starter pack for new projects and existing-project adoption
- `PROGRAMBUILD_SUBAGENTS.md` is the subagent catalog with reusable prompts
- `PROGRAMBUILD_CHECKLIST.md` is the execution checklist version of this system
- `PROGRAMBUILD_IDEA_INTAKE.md` is the pre-feasibility challenge interview for raw ideas, research-backed opportunities, and existing-project deltas
- `PROGRAMBUILD_CHALLENGE_GATE.md` defines the A–H risk controls and stage/risk-aware gate selection — run the appropriate gate at every stage boundary
- `PROGRAMBUILD_GAMEPLAN.md` is the chained execution sequence with cross-stage validation — use this to run stages in the correct order

---

## 1. How To Use This File

1. Read `PROGRAMBUILD_CANONICAL.md` and `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` first when the current task actually changes PROGRAMBUILD control behavior; otherwise orient with registry-backed status/guide output and load only the relevant authority.
2. Select the correct planning entry mode:
   - raw idea
   - research-backed project
   - existing / in-flight project
3. If the project already has a canonical roadmap, Master Game Plan, or equivalent strategic execution spine, identify and preserve it before creating planning artifacts. PROGRAMBUILD should strengthen that authority or propose explicit deltas to it, not silently create a competing plan.
4. Run `PROGRAMBUILD_IDEA_INTAKE.md` in the appropriate mode. Reuse valid existing evidence instead of re-asking settled questions.
5. Fill or reconcile the Inputs block from the intake output/current project authority.
6. Decide the dominant `PRODUCT_SHAPE`, whether `USERJOURNEY/` is needed, and which variant fits the risk and team model.
7. Use `PROGRAMBUILD_FILE_INDEX.md` only when you need to locate an authority; do not load the whole hierarchy by default.
8. Follow `PROGRAMBUILD_GAMEPLAN.md` to run stages in the correct order with cross-stage validation at each boundary.
9. Run `PROGRAMBUILD_CHALLENGE_GATE.md` at every stage transition using the gate parts required by the selected variant, current stage, and actual risk. Full A–H is a whole-system convergence control, not Product paperwork at every boundary.
10. During implementation, define a bounded logical work packet using `PROGRAMBUILD_WORK_PACKET.md`. Use the compact form by default; persist `CURRENT_WORK_PACKET.md` only when persistence materially improves coordination, risk control, or resumability.
11. Load context progressively: establish the stage baseline from registry guidance, then read only the authority sections and specialist references needed for the current slice.
12. Reuse still-valid verification evidence until a documented invalidation trigger occurs. Broaden verification again at stage transitions, release boundaries, and other meaningful convergence gates.
13. Treat every interface between layers as a contract that must be explicit and tested in both directions when that interface is material to the product.
14. Use this playbook inside the project repository created from the template, or map it explicitly onto an existing repository's authority model. Do not keep filled project outputs, work packets, or portfolio state in the PROGRAMSTART template repository.

---

## 2. Inputs

Fill these in once for a new PROGRAMBUILD-managed project. For an existing project, reconcile them against current authority and record only genuine deltas rather than rewriting settled scope without cause.

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

- `ENTRY_MODE`: raw idea, research-backed project, or existing/in-flight project.
- `EXECUTION_SPINE`: for an existing project, the authoritative roadmap/game plan/current stage that PROGRAMBUILD must defer to.
- `PRODUCT_SHAPE`: what execution model actually delivers the value.
- `Variant`: how much evidence and governance the project needs.
- `USERJOURNEY/`: attach it only if onboarding, consent, activation, or first-run routing is part of the product scope.

Bad kickoff patterns:
- picking a stack or variant first, then forcing the product into that shape;
- turning a newer research document or audit into a second master plan merely because it is newer;
- asking the operator to restate verified facts that are already current and authoritative.

Good kickoff pattern:
- identify the authority and execution model first, then choose the lightest workflow that still matches delivery risk and fill only the gaps that genuinely remain.

### Inputs Stage Gate Status

| Item | Status | Notes |
|---|---|---|
| Entry mode selected | Pending | Raw idea, research-backed, or existing project |
| Existing execution spine identified | Pending / N/A | Required for in-flight projects before planning deltas |
| Core inputs block completed/reconciled | Pending | All required fields populated or confirmed current |
| Project name assigned | Pending | Must be set before advancing to feasibility |
| Product shape identified | Pending | Drives which architecture patterns and guardrails apply |
| USERJOURNEY decision recorded | Pending | Attach only if real end-user onboarding or activation design exists |
| Delivery target set | Pending | Set after feasibility stage completes |
| Variant selected | Pending | Choose lite, product, or enterprise |
| Inputs reviewed by product owner | Pending | Use dashboard Signoff action to record approval where applicable |

---

## 3. Core Rules

- One project has one primary strategic execution spine. Research, audits, readiness reviews, checklists, and work packets MUST NOT silently become competing master plans.
- A work packet is a logical derived execution contract. Persist `CURRENT_WORK_PACKET.md` only when doing so adds real coordination/resumption value.
- Context loading is progressive: stage baseline first, current-slice authority second, specialist context only when needed.
- Verification is change-based: reuse trustworthy evidence until its invalidation trigger occurs, then rerun the smallest check set that restores confidence; widen again at required convergence gates.
- No hardcoded API paths outside the route contract layer when a route contract layer is part of the architecture.
- No raw network calls for authenticated endpoints outside the approved auth-aware client where such a client boundary exists.
- No endpoint is considered done until its material auth behavior, schema shape, and route registration are tested.
- No feature is considered done until its applicable loading, success, empty, error, or retry behavior is handled.
- No release is considered ready without rollback, observability, and support ownership appropriate to its operational risk.
- Every material decision should be recorded in `DECISION_LOG.md`; promote durable architecture/policy rationale into ADRs when the current ADR policy warrants a longer-lived record.
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
- `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`
- `PROGRAMBUILD_WORK_PACKET.md`
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

Optional persisted execution aid:
- `CURRENT_WORK_PACKET.md` — replaceable current-slice view; use only when persistence is beneficial; canonical for nothing

---

## 5. Suggested Subagents

Use specialist agents **when decomposition creates real value**. They are not a mandatory sequence for every build.

See `PROGRAMBUILD_SUBAGENTS.md` for full agent definitions, prompts, and invocation triggers.

Common specialist roles:

| Agent | Use when |
|---|---|
| Discovery & Scoping | domain ambiguity, scope uncertainty, or research synthesis is material |
| Architecture & Security | system/trust boundaries or architecture risk need independent review |
| Quality & Release | test/release risk benefits from a focused reviewer |
| Risk Spike Agent | a medium/high-impact unknown blocks a decision |
| Contract Auditor | contract/auth/schema drift is plausible or an audit/convergence boundary requires it |

Guidance:
- Do not spawn agents merely because a role exists.
- Use parallel specialists when work is genuinely decomposable and their outputs can be synthesized cleanly.
- Use the main agent/operator for synthesis, decisions, and coherent code changes.
- Require specialists to return findings, evidence, risks, and unresolved assumptions.
- Specialist output is evidence/advice until adopted into the appropriate canonical project owner.

---

## 6. Stage Overview

| Stage | Purpose | Main output | Gate |
|---|---|---|---|
| 0 | Inputs and mode selection | completed/reconciled inputs block | human review |
| 1 | Feasibility and kill criteria | `FEASIBILITY.md` | clear go / no-go |
| 2 | Research | `RESEARCH_SUMMARY.md` or explicit research delta | stack and market confidence |
| 3 | Requirements and UX | `REQUIREMENTS.md` and `USER_FLOWS.md` | approved scope and workflows |
| 4 | Architecture and risk spikes | `ARCHITECTURE.md` and `RISK_SPIKES.md` | approved contracts and resolved unknowns |
| 5 | Scaffold and guardrails | working skeleton and CI gates | structural tests green |
| 6 | Test strategy | `TEST_STRATEGY.md` | coverage plan approved |
| 7 | Implementation loop | bounded slices + feature code/tests + current evidence | slice DoD complete |
| 8 | Release readiness | `RELEASE_READINESS.md` | deploy convergence gate passed |
| 9 | Audit and drift control | `AUDIT_REPORT.md` | critical gaps resolved/adopted |
| 10 | Post-launch review and retrospective | `POST_LAUNCH_REVIEW.md` | learnings captured and follow-up owners assigned |

---

## 7. Gate Model By Variant

The stage order stays stable across variants, but the gate strength changes based on what you are building.

| Variant | Gate style | Evidence expectation |
|---|---|---|
| Lite | lightweight pass/fail notes | short decision notes and the minimum viable proof to move forward |
| Product | stage/risk-aware must-meet review | explicit decisions and evidence for the controls relevant to the boundary; full convergence at release/high-risk boundaries |
| Enterprise | scored gate with sign-off and retained evidence | approvals, ADRs for material changes, control traceability, and review evidence |

Use this default playbook as the balanced middle. Do not force enterprise ceremony into small-business or prototype work, and do not let high-risk enterprise work run with lite evidence.

Variant selection is independent from `PRODUCT_SHAPE`:
- a background automation can be lite, product, or enterprise depending on blast radius and governance needs
- an interactive end-user product can still be lite if it is small and low-risk
- `USERJOURNEY/` is decided by whether interactive onboarding/activation design exists, not by variant alone

Every stage gate should answer:
- Did any applicable kill criteria from `FEASIBILITY.md` become true?
- Are the must-meet conditions for the selected gate parts satisfied?
- What decision should be recorded in `DECISION_LOG.md`?
- Which previously accepted evidence remains valid, and which evidence was invalidated by changes since the last trusted convergence point?

ADR guidance for a mostly solo workflow:
- Use `DECISION_LOG.md` by default.
- Promote a decision to an ADR when the rationale needs durable architecture/policy history because the change is cross-cutting, hard/costly to reverse, changes a public/security/data/deployment/vendor contract, or is likely to be revisited later.
- Do not create an ADR merely because a numeric file/stage threshold was crossed.

---

## 8. Stage 1: Feasibility And Kill Criteria

Purpose:
Decide whether the product or material change is worth pursuing before substantial design or implementation effort.

Output:
`FEASIBILITY.md`

Must answer:
- Is the problem real and specific?
- Is the proposed solution materially better than current alternatives?
- What would cause us to stop or reshape the project early?
- What are the top 3 business and technical risks?
- For an existing project, does the proposed change strengthen the current strategic spine or conflict with it?

Prompt template:

```text
Create or update FEASIBILITY.md for this product/change.

Inputs:
- Project inputs block or existing project authority + proposed delta

Produce:
1. Problem statement
2. Primary user pain and evidence
3. Existing alternatives and why they are insufficient
4. Business viability assumptions
5. Technical feasibility assumptions
6. Top 3 risks
7. Kill criteria: what evidence would stop or materially redirect this project/change
8. Rough cost and effort estimate
9. Recommendation: go, limited spike, or no-go
10. Existing-project alignment note when applicable: what current authority changes, if anything
```

Gate:
Do not proceed without an explicit go or limited-spike decision, and record that decision in `DECISION_LOG.md`.

---

## 9. Stage 2: Research

Purpose:
Validate stack choices, understand the market, identify constraints, and find avoidable failure patterns before architecture is locked or materially changed.

Output:
`RESEARCH_SUMMARY.md` for a new project, or a clearly scoped research delta for an existing project when a full rewrite would create duplication.

Must answer:
- What already exists?
- Which stack choices are mature and supportable?
- Which compliance, AI, or integration concerns matter?
- Which pitfalls are expensive if discovered late?
- What existing project assumptions are confirmed, weakened, contradicted, or newly exposed?

Prompt template:

```text
Create or update the research evidence for this product.

Inputs:
- Project inputs block / existing execution spine
- Feasibility outcome
- Relevant existing research and verification evidence

Produce sections for:
1. Existing solutions and competitors
2. Technology validation
3. AI and automation opportunities
4. Compliance and regulatory considerations
5. Tooling recommendations
6. Known failure patterns and how to prevent them
7. Existing-project delta analysis when applicable

End with a decisions table:
| Decision | Proposed choice | Alternatives | Confidence | Open question |

If applying research to an existing project, also produce:
| Current authority item | Research finding | Recommended delta | Why | Confidence |

Research is evidence. It does not become a replacement execution plan merely because it is newer.
```

Gate:
Any low-confidence decision must be explicitly approved or deferred into a risk spike. Existing-project recommendations must be adopted through the project's authority process before they become execution instructions.

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
Create or update REQUIREMENTS.md and USER_FLOWS.md.

Inputs:
- Project inputs block
- Feasibility outcome
- Research summary/deltas

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
No architecture work begins until scope, user stories, and workflows are approved. In an existing project, update only the affected authority rather than duplicating already-current requirements or flows.

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
Create or update ARCHITECTURE.md and RISK_SPIKES.md.

Inputs:
- Project inputs block
- Requirements
- User flows
- Research summary/deltas

First adapt the deliverable to `PRODUCT_SHAPE`:
- if `web app` or `mobile app`, include client/server boundaries and user-facing state transitions
- if `API service`, emphasize endpoint contracts, auth, versioning, and consumers
- if `data pipeline`, emphasize job stages, inputs/outputs, scheduling, and recovery
- if `library`, emphasize public API surface, compatibility guarantees, and examples
- if `CLI tool` or `desktop app`, emphasize command or application lifecycle, packaging, local state, and update strategy

ARCHITECTURE.md must include:
1. System topology
2. Technology decision table
3. API/contract table appropriate to shape
4. Data model and ownership
5. Route/command/job/public-API contract plan where applicable
6. Auth/trust matrix
7. Error contract
8. Environment strategy
9. Observability plan

RISK_SPIKES.md must include:
1. Top material technical unknowns
2. Small prototype or investigation plan for each
3. Success and failure criteria
4. Result summary
5. Decision taken after each spike
```

Mandatory spike candidates where material:
- authentication and session lifecycle
- streaming or long-lived connection behavior
- external integrations
- AI or model cost/latency assumptions
- file handling or document processing

Gate:
Do not scaffold or implement a new contradictory design until the relevant architecture is approved and high-risk unknowns have been resolved or explicitly accepted.

---

## 12. Stage 5: Scaffold And Guardrails

Purpose:
Set the rules of the system before feature work begins.

Output:
Working repo skeleton with CI and structural tests appropriate to the product shape.

Required guardrails (select only those applicable):
- route or endpoint contract layer with canonical, deprecated, and planned states
- auth-aware client or trusted-caller boundary where applicable
- service/handler registration pattern where applicable
- repo-boundary consent rule for AI-assisted work: do not inspect, edit, stage, commit, or push another repository unless the user explicitly names it and asks for that action
- CI/local verification appropriate to the product's risk and active status
- local bootstrap command with no tribal knowledge

Required structural tests should protect the dominant contract surface, for example:
- route/endpoint/command/job alignment
- auth boundary discipline
- schema/interface completeness
- planned/deprecated contract safety

Prompt template:

```text
Create the project scaffold only.
Do not implement product features.

Inputs:
- Architecture
- User flows where relevant

Apply only the scaffold elements that fit PRODUCT_SHAPE.
Produce the minimum repo structure, contract/trust boundaries, structural tests, verification tooling, local setup, and deprecation pattern needed to make later feature work safe.
```

Gate:
Feature work starts only after the required structural checks for this architecture are green.

---

## 13. Stage 6: Test Strategy

Purpose:
Decide the testing model before writing features so coverage is designed, not improvised.

Output:
`TEST_STRATEGY.md`

Must answer:
- What belongs in unit, component, purpose, golden, contract, integration, and E2E tests for this product shape?
- What fixtures exist and who owns them?
- Which tests block PRs, regressions, and releases?
- Which evidence can be retained/reused across slices, and what invalidates it?

Prompt template:

```text
Create TEST_STRATEGY.md.

Inputs:
- Requirements
- User flows
- Architecture

Use PRODUCT_SHAPE and actual risk to determine the test layers. Browser E2E is not universal.

Include:
1. Test portfolio and purpose of each layer
2. Unit/component/contract/integration/E2E rules only where applicable
3. Test data and fixture strategy
4. Requirements traceability
5. Contract-to-test mapping for material contracts
6. Evidence-reuse and invalidation rules for expensive/stateful verification
7. Gaps that would prevent credible release confidence
```

Non-negotiables:
- mocked shapes match real contract shapes
- material auth/trust behavior is tested explicitly
- release-critical outcomes have named proof

Gate:
No feature implementation starts until the test model is sufficient for the P0 risk surface.

---

## 14. Stage 7: Implementation Loop

Purpose:
Build one bounded slice at a time with minimal necessary context and verification proportional to what changed.

Output:
Working feature code/tests plus current-slice evidence. A persisted `CURRENT_WORK_PACKET.md` is optional derived state, not the default artifact.

### Stage baseline

Use registry-backed guidance to establish the allowed Stage 7 authority surface. Do not fully reread every stage file for each slice.

### Work-packet loop

For each coherent slice:

1. Define the compact work-packet fields from `PROGRAMBUILD_WORK_PACKET.md`. Persist `CURRENT_WORK_PACKET.md` only when multi-session/multi-agent coordination, risk, dependencies/blockers, or resumability makes persistence useful.
2. Trace the slice to the strategic execution spine/current stage and exact relevant requirement IDs.
3. State one bounded objective and explicit non-goals.
4. Identify only the architecture contracts, requirement sections, flows, decisions, and specialist references needed now.
5. List trusted verification evidence and the conditions that would invalidate it.
6. Choose the smallest verification set that will prove the changed/at-risk surface.
7. Write purpose/auth/contract tests first where appropriate.
8. Implement the slice without prospectively contradicting authority.
9. Update contract/test registries only when the slice changes their governed surface.
10. Run targeted verification plus any broader check whose invalidation/convergence trigger occurred.
11. Record evidence actually produced once.
12. Reconcile material design/scope/status changes into canonical authority and `DECISION_LOG.md`.
13. Close/replace the logical or persisted packet and derive the next slice from updated state.

Definition of done:
- slice traces to approved scope/strategic authority
- material contract/trust behavior is verified where applicable
- applicable user/runtime states are handled
- reused evidence is still within scope or has been revalidated after invalidation
- durable decisions/state are reconciled
- the work packet did not become a second planning hierarchy

Prompt template:

```text
Implement one bounded slice using current project authority and test strategy.

State:
- objective + non-goals
- exact authority IDs/sections
- reusable evidence + invalidation triggers
- acceptance criteria
- targeted verification

Load only task-relevant context.
Stop if the implementation would prospectively contradict current authority; reconcile authority first.
Run targeted verification for what changed or became at risk.
```

Periodic convergence:
- widen when accumulated cross-slice interaction, blast radius, authority churn, invalidated evidence, dependency/environment change, milestone/handoff, or another Challenge Gate trigger makes the narrow slice view insufficient
- local time/slice reminders may prompt a review but are not proof that one is required
- run the stage/risk-relevant Challenge Gate controls from `PROGRAMBUILD_CHALLENGE_GATE.md`

---

## 15. Stage 8: Release Readiness

Purpose:
Prevent “it passed targeted slice tests” from being mistaken for “it is safe to launch.” Release readiness is a deliberate whole-system convergence point.

Output:
`RELEASE_READINESS.md`

Must answer:
- Can we deploy and roll back safely?
- Do we have visibility into failures?
- Are support/ownership/operational procedures defined where needed?
- Which retained verification evidence is still valid, and which release-critical evidence must be rerun?

Prompt template:

```text
Create or update RELEASE_READINESS.md.

Inputs:
- Architecture
- Test strategy
- Current implementation status
- Retained verification evidence + invalidation history

Include the launch scope/exclusions, environment readiness, deployment/rollback path, required monitoring/alerts/support ownership, release smoke/purpose checks, evidence reuse/revalidation decisions, and go/no-go risks.
```

Minimum gate:
- deployment path validated
- rollback path validated
- secrets/config verified where applicable
- critical smoke/purpose tests pass
- required observability/support coverage is active
- invalidated release-critical evidence has been re-established

---

## 16. Stage 9: Audit And Drift Control

Purpose:
Catch silent breakage and contract/authority drift after features have accumulated.

Output:
`AUDIT_REPORT.md`

Audit what is materially relevant: contracts, auth/trust, schemas, test blind spots, planned/deprecated behavior, isolation, release readiness, stale evidence, and duplicate planning authority.

Prompt template:

```text
Audit the application for silent failures, drift, release risk, and authority drift.

For each real finding provide severity, evidence, impact, minimum fix, recurrence prevention, and the canonical owner that must adopt the finding if authority changes.
```

Gate:
Critical/high findings need fixes, owners, or explicit risk acceptance. The audit remains evidence until adopted into canonical authority.

---

## 17. Stage 10: Post-Launch Review And Retrospective

Purpose:
Compare intended outcomes against reality and capture reusable lessons without turning retrospectives into mandatory template churn.

Output:
`POST_LAUNCH_REVIEW.md`

Must answer:
- Did the product achieve the success metric?
- Which decisions were validated/reversed/deferred?
- What incidents/support/adoption gaps appeared?
- What follow-up changes need ownership?
- Which systemic lessons, if any, should improve PROGRAMBUILD?

Prompt template:

```text
Create POST_LAUNCH_REVIEW.md from the success metric, release decision, audit evidence, and production signals.

Capture launch outcome, metrics, incidents/support, decision reversals/confirmations, follow-up owners, and only the template/process improvements supported by reusable systemic evidence.
```

Gate:
Do not treat the project as complete until meaningful follow-up ownership and lessons are recorded. A PROGRAMBUILD template change becomes warranted when evidence shows a recurring/systemic prevention opportunity; no universal project count turns an observation into policy.

---

## 18. Additional Operating Practices

Apply these proportionally rather than as universal ceremony:

- Authority discipline: one strategic execution spine; canonical concern ownership.
- Planning entry discipline: choose raw-idea, research-backed, or existing-project mode.
- Work-packet discipline: compact logical packet by default; persisted packet only when useful.
- JIT context discipline: stage baseline → exact slice authority → specialist context only when triggered.
- Evidence discipline: provenance/scope/invalidation for expensive or stateful verification; no broad reruns without cause.
- Convergence discipline: widen when risk/change requires it, especially stage/release boundaries.
- Environment parity: maintain where deployment/runtime differences can create real risk.
- Dependency hygiene: pin or constrain critical dependencies appropriately; check current dependency/vendor facts when they are material to architecture/release or when an invalidation signal occurs; use scanning at intentional verification/release gates rather than as an always-running heartbeat.
- Secret management: never commit secrets; use committed examples/templates only.
- Migration discipline: version and test migrations when the product has mutable persisted state.
- Feature flags: use when they materially reduce release risk; define removal criteria.
- Performance budgets: define/enforce only where performance is a product/reliability requirement.
- Accessibility: treat as a product requirement for user-facing surfaces where applicable.
- Error handling/fallbacks: make failures safe and observable for material async/external paths.
- ADRs: use when durable architecture/policy rationale is warranted; do not create them from a numeric threshold alone.
- Decision reversals: preserve history using the current reversal invariant in `PROGRAMBUILD_CHALLENGE_GATE.md`.
- Ownership clarity: name an owner where unresolved responsibility would create risk; do not add placeholders to low-value artifacts merely for ceremony.
- Requirements traceability: ensure P0 outcomes and release-blocking tests have credible traceability.
- Maintain `PROGRAMBUILD_FILE_INDEX.md` when a critical file is added/renamed/deprecated/replaced.
- Update `PROGRAMBUILD_CANONICAL.md` when document authority changes.
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
- multiple engineers are contributing or the system has enough operational weight to require explicit quality gates
- quality gates matter, but enterprise ceremony would be excessive

Use [PROGRAMBUILD_ENTERPRISE.md](PROGRAMBUILD_ENTERPRISE.md) when:
- the product touches regulated data or multiple business units
- auditability, approvals, and operational readiness are mandatory
- the cost of failure is materially higher than the cost of extra process

---

## 20. Cardinal Lessons

- One project needs one strategic execution spine; additional artifacts should clarify or derive from it, not compete with it.
- The most expensive bugs usually come from missing contracts, not missing features.
- If a material route, auth rule, schema, or user-state expectation is implicit, it will drift.
- Research reduces bad bets, but research is evidence until adopted into project authority.
- Risk spikes reduce expensive surprises when they target real unknowns.
- Bounded work packets reduce context drift only when the packet is smaller than the problem; persist them only when useful.
- Re-reading everything for every slice is not rigor; loading the right authority at the right time is rigor.
- Re-running everything after every change is not rigor; knowing what invalidates evidence and widening at convergence is rigor.
- Structural tests prevent recurrence better than retrospective debugging.
- Release readiness is an engineering convergence concern, not a postscript.
- More agents, documents, gates, and algorithms are not improvements unless they reduce real execution risk or cost.

---

Last updated: 2026-08-24
Source: lessons from route alignment failures, auth bypasses, response schema drift, test blind spots, duplicate planning authority, stale context, repeated low-value verification, and execution-friction analysis from active PROGRAMSTART use
