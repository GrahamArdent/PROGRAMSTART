# PROGRAMBUILD_CHECKLIST.md

# Program Build Execution Checklist

Use this file when you want the Program Build system in checklist form instead of narrative form.
This checklist depends on the authority rules in `PROGRAMBUILD_CANONICAL.md`, the planning rules in `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, and the file list in `PROGRAMBUILD_FILE_INDEX.md`.

---

## 1. Setup

- [ ] read `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` and select the correct entry mode
- [ ] if this is an existing project, identify its current canonical execution spine before creating new planning artifacts
- [ ] run `PROGRAMBUILD_IDEA_INTAKE.md` in the appropriate mode before filling the inputs block or proposing a planning delta
- [ ] challenge all 8 intake dimensions; reuse valid evidence in research-backed/existing-project modes instead of re-asking settled questions
- [ ] choose one process file: lite, product, or enterprise for a PROGRAMBUILD-managed project
- [ ] record the dominant `PRODUCT_SHAPE` before naming stack or tooling choices
- [ ] decide whether the project needs a USERJOURNEY attachment based on whether real end-user onboarding, consent, activation, or first-run interaction must be designed
- [ ] confirm `PROGRAMBUILD_CANONICAL.md` is current
- [ ] confirm `PROGRAMBUILD_FILE_INDEX.md` is current
- [ ] run Challenge Gate (Idea Intake → Stage 0) when using the PROGRAMBUILD stage sequence
- [ ] fill the shared project inputs block
- [ ] create `DECISION_LOG.md`
- [ ] if using product or enterprise workflow, define gate approvers and evidence expectations
- [ ] if resuming a paused project, run the Re-Entry Protocol from `PROGRAMBUILD_CHALLENGE_GATE.md`
- [ ] if the current slice benefits from explicit execution scoping, derive `CURRENT_WORK_PACKET.md` using `PROGRAMBUILD_WORK_PACKET.md`

---

## 2. Feasibility

- [ ] run Challenge Gate (Stage 0 → Stage 1)
- [ ] create `FEASIBILITY.md`
- [ ] define business and technical risks
- [ ] define kill criteria
- [ ] estimate effort at the level of precision the current evidence can support
- [ ] define rough cost and effort estimate
- [ ] record go, no-go, or limited-spike outcome
- [ ] record the decision in `DECISION_LOG.md`

---

## 3. Research

- [ ] run Challenge Gate (Stage 1 → Stage 2)
- [ ] create `RESEARCH_SUMMARY.md` or the minimum research delta warranted by existing evidence
- [ ] validate stack maturity
- [ ] document alternatives
- [ ] document compliance concerns
- [ ] identify costly late-stage failure patterns
- [ ] record low-confidence decisions and follow-up spikes in `DECISION_LOG.md`
- [ ] treat research as evidence, not as a replacement execution plan
- [ ] when research affects an existing project, produce specific delta recommendations for its current authority spine

---

## 4. Requirements And UX

- [ ] run Challenge Gate (Stage 2 → Stage 3)
- [ ] create or update `REQUIREMENTS.md`
- [ ] create or update `USER_FLOWS.md` when direct interaction is in scope
- [ ] define P0 and P1 requirements
- [ ] define measurable acceptance criteria
- [ ] define loading, empty, error, and retry states where applicable
- [ ] define out-of-scope list
- [ ] confirm whether any feasibility kill criteria now apply

---

## 5. Architecture And Risk Spikes

- [ ] run Challenge Gate (Stage 3 → Stage 4)
- [ ] create or update `ARCHITECTURE.md`
- [ ] create or update `RISK_SPIKES.md`
- [ ] apply the `PRODUCT_SHAPE` checklist before filling route, API, UI, or job-model sections
- [ ] define the dominant contract surface
- [ ] define auth/trust boundaries where applicable
- [ ] define data ownership
- [ ] define external dependency table and fallback plan
- [ ] define dependency risk/health view appropriate to the project
- [ ] run KB dependency health check (`programstart research --status`) when relevant
- [ ] run risk spikes for material unknowns that block a decision
- [ ] promote material architecture decisions into ADRs if the repository's ADR threshold is met

---

## 6. Scaffold And Guardrails

- [ ] run Challenge Gate (Stage 4 → Stage 5)
- [ ] create the dominant contract layer: routes, endpoints, commands, jobs, or public API
- [ ] create the boundary helper that fits the shape: auth-aware client, trusted caller wrapper, or operator helper
- [ ] document and enforce the repo-boundary consent rule for AI-assisted work before touching any other repository
- [ ] create streaming, scheduler, worker, or lifecycle helper if needed
- [ ] add alignment tests for the dominant contract surface
- [ ] add reverse alignment tests where discoverability matters
- [ ] add auth/trust-boundary tests where applicable
- [ ] add no-hardcoded-contract-identifier check where it protects a real drift risk
- [ ] create CI with bounded timeouts and appropriate confidence tiers

---

## 7. Test Strategy

- [ ] run Challenge Gate (Stage 5 → Stage 6)
- [ ] create `TEST_STRATEGY.md`
- [ ] apply the `PRODUCT_SHAPE` testing checklist before choosing browser, API, job, or command-level coverage
- [ ] define unit/component/contract/integration coverage appropriate to the shape
- [ ] define purpose and auth/trust test rules
- [ ] verify every P0 requirement has at least one meaningful outcome proof
- [ ] define golden policy only where a golden adds durable value
- [ ] define smoke/regression split
- [ ] define requirements-to-test traceability matrix
- [ ] create contract-to-test registry
- [ ] define which expensive/stateful evidence may be reused and what invalidates it

---

## 8. Implementation Loop

- [ ] run Challenge Gate (Stage 6 → Stage 7)
- [ ] derive or refresh the current work packet from the authoritative execution spine/current stage when the slice is non-trivial
- [ ] load only the authority and specialist context required for the current slice
- [ ] list trusted existing verification evidence and the changes that could invalidate it
- [ ] write purpose/auth/contract tests first where appropriate
- [ ] implement producer-side contract or execution unit
- [ ] register routes, commands, jobs, handlers, or public APIs where applicable
- [ ] implement consumer, operator, or client layer
- [ ] implement visible states only where a person interacts with the system
- [ ] add component, integration, scenario, or E2E tests as appropriate
- [ ] add smoke coverage for the dominant execution mode when it materially improves confidence
- [ ] add/update golden baseline only if the governed output changed
- [ ] update test registry
- [ ] verify the changed/at-risk surfaces; do not repeat broad checks without an invalidation reason
- [ ] trigger a mid-implementation convergence review when accumulated change, blast radius, uncertainty, evidence invalidation, cross-slice interaction, or milestone risk warrants it; do not use a fixed feature count as a universal rule
- [ ] check for decision reversals in `DECISION_LOG.md`
- [ ] update decision log or ADRs for material design changes
- [ ] reconcile completed work-packet outcomes back into canonical project artifacts before generating the next packet

---

## 9. Release Readiness

- [ ] run Challenge Gate (Stage 7 → Stage 8)
- [ ] create `RELEASE_READINESS.md`
- [ ] verify rollback plan
- [ ] verify migration plan where applicable
- [ ] verify monitoring and alerting
- [ ] verify SLO and SLI targets where appropriate
- [ ] verify critical smoke/purpose tests
- [ ] verify support ownership
- [ ] run KB dependency health check when dependency freshness materially affects release confidence
- [ ] verify all `DECISION_LOG.md` entries are reconciled — no unreconciled reversals
- [ ] confirm any reused release evidence still survives its invalidation triggers

---

## 10. Audit

- [ ] run Challenge Gate (Stage 8 → Stage 9)
- [ ] create `AUDIT_REPORT.md`
- [ ] verify contract, auth/trust, and schema consistency
- [ ] verify planned/deprecated contract safety
- [ ] verify invalid-input and isolation behavior where applicable
- [ ] assign owners for critical and high findings
- [ ] record any explicit residual-risk acceptance
- [ ] ensure audit findings remain evidence until adopted through the canonical project authority

---

## 11. Post-Launch Review

- [ ] create `POST_LAUNCH_REVIEW.md`
- [ ] compare actual metrics to the success metric
- [ ] record incidents, support load, and adoption gaps
- [ ] capture lessons learned
- [ ] assign owners for follow-up actions
- [ ] run Template Improvement Review — propose updates for systemic lessons
- [ ] apply template improvements when recurrence/evidence shows the lesson is systemic, or record a rationale for not changing the template; do not rely on an arbitrary universal project-count threshold

---

## 12. File Governance

- [ ] all critical control files use `PROGRAMBUILD_*.md`
- [ ] all stage output files use the standard names from `PROGRAMBUILD_CANONICAL.md`
- [ ] `PROGRAMBUILD_FILE_INDEX.md` includes every critical file
- [ ] source-of-truth ownership is clear for every concern
- [ ] there is one strategic execution spine for the project
- [ ] `CURRENT_WORK_PACKET.md`, if present, is explicitly derived and does not redefine strategy
- [ ] project-specific live portfolio state is not stored in the reusable PROGRAMSTART template

---

## 13. Gate Sign-Off Log

Use the log format from `PROGRAMBUILD_CHALLENGE_GATE.md`. One row per stage transition.
After each gate pass, run `programstart advance --system programbuild` to keep workflow state current.

Programmatic log commands:
- `programstart log --system programbuild` — view full sign-off history
- `programstart progress --system programbuild` — view checklist completion percentage

| From Stage | To Stage | Date | Kill OK | Assumptions OK | Scope OK | Skipped OK | Decisions OK | Dependencies OK | Proceed? | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/n/a | Yes / No / Conditional | |

Status codes: ✅ All clear | ⚠️ Issues found but managed — recorded in DECISION_LOG.md | ❌ Blocking issue — do not proceed

---

Last updated: 2026-08-24
