# PROGRAMBUILD_PRODUCT.md

# Program Build Product

Use this version for a normal production product: customer-facing or operationally important, multi-feature, and maintained by a small or medium-sized team.
This is the recommended default for most real applications.

Authority:
- `PROGRAMBUILD_CANONICAL.md` defines source-of-truth rules
- `PROGRAMBUILD_FILE_INDEX.md` is the lookup table for critical files
- `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` defines planning entry modes, one-spine authority, proportional rigor, task-scoped context loading, and evidence reuse
- `PROGRAMBUILD_WORK_PACKET.md` defines the derived current execution slice; a filled packet never outranks project authority
- `PROGRAMBUILD_IDEA_INTAKE.md` runs before Stage 0 — challenge the raw idea, research-backed opportunity, or existing-project delta before filling the inputs block
- `PROGRAMBUILD_CHALLENGE_GATE.md` runs at every stage transition — all 8 parts required; Part G required at Stages 4+
- `PROGRAMBUILD_GAMEPLAN.md` defines the execution order with full cross-stage validation

---

## When To Use

Use this file when:
- the team is 3 to 12 people
- the product is customer-facing, revenue-affecting, or operationally important
- multiple feature areas share contracts and infrastructure
- quality gates matter more than pure speed

This variant fits both interactive products and non-interactive systems such as APIs, internal services, and background automations that still need real release discipline.

If this workflow is being applied to an existing project, identify that project's current strategic execution spine first. PROGRAMBUILD should strengthen that authority or propose explicit deltas to it, not silently create a competing plan.

---

## Required Stages

| Stage | Output | Gate |
|---|---|---|
| Feasibility | `FEASIBILITY.md` | go or limited spike |
| Research | `RESEARCH_SUMMARY.md` | decisions reviewed; findings reconciled as evidence/deltas |
| Requirements and UX | `REQUIREMENTS.md`, `USER_FLOWS.md` | scope approved |
| Architecture and risk spikes | `ARCHITECTURE.md`, `RISK_SPIKES.md` | contracts approved |
| Scaffold and guardrails | repo skeleton and CI | structural tests green |
| Test strategy | `TEST_STRATEGY.md` | coverage approved |
| Implementation loop | bounded feature/work packets | feature/slice DoD |
| Release readiness | `RELEASE_READINESS.md` | go / no-go convergence gate |
| Audit | `AUDIT_REPORT.md` | critical issues resolved; findings remain evidence until adopted |
| Post-launch review | `POST_LAUNCH_REVIEW.md` | lessons captured and follow-up owned |

---

## Required Guardrails

- one strategic execution spine; no research document, audit, readiness review, checklist, or work packet silently becomes a second master plan
- contract layer with canonical, deprecated, and planned states for routes, endpoints, commands, jobs, or public APIs
- auth-aware API client, trusted caller helper, or equivalent boundary adapter
- auth matrix tests
- alignment and reverse-alignment tests for the dominant contract surface
- schema completeness checks
- no hardcoded contract identifier checks
- requirements-to-test traceability
- contract-to-test registry
- smoke suite for the dominant execution mode on PRs
- scheduled regression/golden runs where their value justifies cost
- decision log updates for material changes
- critical planning files follow the `PROGRAMBUILD_*.md` naming convention
- non-trivial implementation slices use `PROGRAMBUILD_WORK_PACKET.md` to identify objective, non-goals, exact authority, reusable evidence, invalidation triggers, and targeted verification
- broad revalidation is reserved for invalidated surfaces and convergence gates rather than repeated automatically after every small change

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
Create or operate a full product delivery plan for this application.

Inputs:
- project inputs block, or
- existing project execution spine + current authority + proposed change

First select the correct planning entry mode from PROGRAMBUILD_PLANNING_OPERATING_MODEL.md.
If an existing project already has a master roadmap/game plan, preserve it as the strategic spine unless replacement is explicitly approved.

Produce or update only the authoritative artifacts warranted by the current state:
1. feasibility and kill criteria
2. decision log entries for each material gate/change
3. research summary or research delta
4. requirements and workflows appropriate to the product shape
5. architecture and risk spikes
6. scaffold and structural tests
7. test strategy with risk-appropriate smoke/regression split
8. implementation loop using bounded work packets for non-trivial slices
9. release readiness plan
10. post-build audit plan
11. post-launch review plan

For each work packet:
- trace it to the strategic execution spine/current stage
- name exact authority sections and specialist references required now
- reuse valid verification evidence until a documented invalidation trigger occurs
- run the smallest verification set that proves the changed/at-risk surface
- widen context and verification again at stage/release convergence gates
```

---

## Product Definition Of Done

- every dominant contract surface is declared, registered, and covered by the registry
- auth, trust-boundary, schema, and contract behavior are verified structurally
- primary execution scenarios have smoke/purpose coverage appropriate to risk
- release readiness includes rollback, monitoring, and ownership
- audit finds no unresolved critical issues
- any completed work packets have been reconciled into canonical authority/state and replaced rather than accumulated as a parallel plan
- post-launch review records actual outcomes against the success metric

---

Last updated: 2026-08-24