# PROGRAMBUILD_CHECKLIST.md

# Program Build Execution Checklist

Use this file when you want the Program Build system in checklist form instead of narrative form.
This checklist depends on the authority rules in `PROGRAMBUILD_CANONICAL.md` and the file list in `PROGRAMBUILD_FILE_INDEX.md`.

---

## 1. Setup

- [ ] run `PROGRAMBUILD_IDEA_INTAKE.md` interview before filling the inputs block
- [ ] choose one process file: lite, product, or enterprise
- [ ] record the dominant `PRODUCT_SHAPE` before naming stack or tooling choices
- [ ] decide whether the project needs a USERJOURNEY attachment based on whether real end-user onboarding, consent, activation, or first-run interaction must be designed
- [ ] confirm `PROGRAMBUILD_CANONICAL.md` is current
- [ ] confirm `PROGRAMBUILD_FILE_INDEX.md` is current
- [ ] run Challenge Gate (Idea Intake → Stage 0)
- [ ] fill the shared project inputs block
- [ ] create `DECISION_LOG.md`
- [ ] if using product or enterprise workflow, define gate approvers and evidence expectations
- [ ] if resuming a paused project, run the Re-Entry Protocol from `PROGRAMBUILD_CHALLENGE_GATE.md`

---

## 2. Feasibility

- [ ] run Challenge Gate (Stage 0 → Stage 1)
- [ ] create `FEASIBILITY.md`
- [ ] define business and technical risks
- [ ] define kill criteria
- [ ] fill T-shirt estimation table per area
- [ ] define rough cost and effort estimate
- [ ] record go, no-go, or limited-spike outcome
- [ ] record the decision in `DECISION_LOG.md`

---

## 3. Research

- [ ] run Challenge Gate (Stage 1 → Stage 2)
- [ ] create `RESEARCH_SUMMARY.md`
- [ ] validate stack maturity
- [ ] document alternatives
- [ ] document compliance concerns
- [ ] identify costly late-stage failure patterns
- [ ] record low-confidence decisions and follow-up spikes in `DECISION_LOG.md`

---

## 4. Requirements And UX

- [ ] run Challenge Gate (Stage 2 → Stage 3)
- [ ] create `REQUIREMENTS.md`
- [ ] create `USER_FLOWS.md`
- [ ] define P0 and P1 requirements
- [ ] define measurable acceptance criteria
- [ ] define loading, empty, error, and retry states
- [ ] define out-of-scope list
- [ ] confirm whether any feasibility kill criteria now apply

---

## 5. Architecture And Risk Spikes

- [ ] run Challenge Gate (Stage 3 → Stage 4)
- [ ] create `ARCHITECTURE.md`
- [ ] create `RISK_SPIKES.md`
- [ ] apply the `PRODUCT_SHAPE` checklist before filling route, API, UI, or job-model sections
- [ ] define API contract table
- [ ] define auth matrix
- [ ] define data ownership
- [ ] define external dependency table and fallback plan
- [ ] define dependency heat map
- [ ] run KB dependency health check (`programstart research --status`)
- [ ] run risk spikes for unknowns
- [ ] promote material architecture decisions into ADRs if needed

---

## 6. Scaffold And Guardrails

- [ ] run Challenge Gate (Stage 4 → Stage 5)
- [ ] create the dominant contract layer: routes, endpoints, commands, jobs, or public API
- [ ] create the boundary helper that fits the shape: auth-aware client, trusted caller wrapper, or operator helper
- [ ] document and enforce the repo-boundary consent rule for AI-assisted work before touching any other repository
- [ ] create streaming, scheduler, worker, or lifecycle helper if needed
- [ ] add alignment tests for the dominant contract surface
- [ ] add reverse alignment tests where discoverability matters
- [ ] add auth matrix tests
- [ ] add no-hardcoded-contract-identifier check
- [ ] create CI with timeouts

---

## 7. Test Strategy

- [ ] run Challenge Gate (Stage 5 → Stage 6)
- [ ] create `TEST_STRATEGY.md`
- [ ] apply the `PRODUCT_SHAPE` testing checklist before choosing browser, API, job, or command-level coverage
- [ ] define unit and component coverage rules
- [ ] define purpose and auth test rules
- [ ] verify every P0 requirement has at least one purpose test
- [ ] define golden policy
- [ ] define E2E smoke/regression split
- [ ] define requirements-to-test traceability matrix
- [ ] create endpoint-to-test registry

---

## 8. Implementation Loop

- [ ] run Challenge Gate (Stage 6 → Stage 7)
- [ ] write purpose and auth tests first
- [ ] implement producer-side contract or execution unit
- [ ] register routes, commands, jobs, handlers, or public APIs
- [ ] implement consumer, operator, or client layer
- [ ] implement visible states only where a person interacts with the system
- [ ] add component, integration, or scenario tests as appropriate
- [ ] add smoke coverage for the dominant execution mode
- [ ] add golden baseline if applicable
- [ ] update test registry
- [ ] run mid-implementation Challenge Gate every 3–5 features
- [ ] check for decision reversals in DECISION_LOG.md
- [ ] update decision log or ADRs for material design changes

---

## 9. Release Readiness

- [ ] run Challenge Gate (Stage 7 → Stage 8)
- [ ] create `RELEASE_READINESS.md`
- [ ] verify rollback plan
- [ ] verify migration plan
- [ ] verify monitoring and alerting
- [ ] verify SLO and SLI targets are defined
- [ ] verify smoke tests
- [ ] verify support ownership
- [ ] run KB dependency health check — no deprecated or superseded dependencies remain
- [ ] verify all DECISION_LOG.md entries are reconciled — no unreconciled reversals

---

## 10. Audit

- [ ] run Challenge Gate (Stage 8 → Stage 9)
- [ ] create `AUDIT_REPORT.md`
- [ ] verify route, auth, and schema consistency
- [ ] verify planned-route and deprecated-route safety
- [ ] verify invalid-input and isolation behavior
- [ ] assign owners for critical and high findings
- [ ] record any explicit residual-risk acceptance

---

## 11. Post-Launch Review

- [ ] create `POST_LAUNCH_REVIEW.md`
- [ ] compare actual metrics to the success metric
- [ ] record incidents, support load, and adoption gaps
- [ ] capture lessons learned
- [ ] assign owners for follow-up actions
- [ ] run Template Improvement Review — propose updates for systemic lessons
- [ ] apply template improvements or record as deferred with rationale

---

## 12. File Governance

- [ ] all critical control files use `PROGRAMBUILD_*.md`
- [ ] all stage output files use the standard names from `PROGRAMBUILD_CANONICAL.md`
- [ ] `PROGRAMBUILD_FILE_INDEX.md` includes every critical file
- [ ] source-of-truth ownership is clear for every concern

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

Last updated: 2026-03-31
