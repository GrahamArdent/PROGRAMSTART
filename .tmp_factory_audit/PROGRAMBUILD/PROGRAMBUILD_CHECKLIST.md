# PROGRAMBUILD_CHECKLIST.md

# Program Build Execution Checklist

Use this file when you want the Program Build system in checklist form instead of narrative form.
This checklist depends on the authority rules in `PROGRAMBUILD_CANONICAL.md` and the file list in `PROGRAMBUILD_FILE_INDEX.md`.

---

## 1. Setup

- [ ] choose one process file: lite, product, or enterprise
- [ ] record the dominant `PRODUCT_SHAPE` before naming stack or tooling choices
- [ ] decide whether the project needs a USERJOURNEY attachment based on whether real end-user onboarding, consent, activation, or first-run interaction must be designed
- [ ] confirm `PROGRAMBUILD_CANONICAL.md` is current
- [ ] confirm `PROGRAMBUILD_FILE_INDEX.md` is current
- [ ] fill the shared project inputs block
- [ ] create `DECISION_LOG.md`
- [ ] if using product or enterprise workflow, define gate approvers and evidence expectations

---

## 2. Feasibility

- [ ] create `FEASIBILITY.md`
- [ ] define business and technical risks
- [ ] define kill criteria
- [ ] define rough cost and effort estimate
- [ ] record go, no-go, or limited-spike outcome
- [ ] record the decision in `DECISION_LOG.md`

---

## 3. Research

- [ ] create `RESEARCH_SUMMARY.md`
- [ ] validate stack maturity
- [ ] document alternatives
- [ ] document compliance concerns
- [ ] identify costly late-stage failure patterns
- [ ] record low-confidence decisions and follow-up spikes in `DECISION_LOG.md`

---

## 4. Requirements And UX

- [ ] create `REQUIREMENTS.md`
- [ ] create `USER_FLOWS.md`
- [ ] define P0 and P1 requirements
- [ ] define measurable acceptance criteria
- [ ] define loading, empty, error, and retry states
- [ ] define out-of-scope list
- [ ] confirm whether any feasibility kill criteria now apply

---

## 5. Architecture And Risk Spikes

- [ ] create `ARCHITECTURE.md`
- [ ] create `RISK_SPIKES.md`
- [ ] apply the `PRODUCT_SHAPE` checklist before filling route, API, UI, or job-model sections
- [ ] define API contract table
- [ ] define auth matrix
- [ ] define data ownership
- [ ] define external dependency table and fallback plan
- [ ] define dependency heat map
- [ ] run risk spikes for unknowns
- [ ] promote material architecture decisions into ADRs if needed

---

## 6. Scaffold And Guardrails

- [ ] create the dominant contract layer: routes, endpoints, commands, jobs, or public API
- [ ] create the boundary helper that fits the shape: auth-aware client, trusted caller wrapper, or operator helper
- [ ] create streaming, scheduler, worker, or lifecycle helper if needed
- [ ] add alignment tests for the dominant contract surface
- [ ] add reverse alignment tests where discoverability matters
- [ ] add auth matrix tests
- [ ] add no-hardcoded-contract-identifier check
- [ ] create CI with timeouts

---

## 7. Test Strategy

- [ ] create `TEST_STRATEGY.md`
- [ ] apply the `PRODUCT_SHAPE` testing checklist before choosing browser, API, job, or command-level coverage
- [ ] define unit and component coverage rules
- [ ] define purpose and auth test rules
- [ ] define golden policy
- [ ] define E2E smoke/regression split
- [ ] define requirements-to-test traceability matrix
- [ ] create endpoint-to-test registry

---

## 8. Implementation Loop

- [ ] write purpose and auth tests first
- [ ] implement producer-side contract or execution unit
- [ ] register routes, commands, jobs, handlers, or public APIs
- [ ] implement consumer, operator, or client layer
- [ ] implement visible states only where a person interacts with the system
- [ ] add component, integration, or scenario tests as appropriate
- [ ] add smoke coverage for the dominant execution mode
- [ ] add golden baseline if applicable
- [ ] update test registry
- [ ] update decision log or ADRs for material design changes

---

## 9. Release Readiness

- [ ] create `RELEASE_READINESS.md`
- [ ] verify rollback plan
- [ ] verify migration plan
- [ ] verify monitoring and alerting
- [ ] verify SLO and SLI targets are defined
- [ ] verify smoke tests
- [ ] verify support ownership

---

## 10. Audit

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

---

## 12. File Governance

- [ ] all critical control files use `PROGRAMBUILD_*.md`
- [ ] all stage output files use the standard names from `PROGRAMBUILD_CANONICAL.md`
- [ ] `PROGRAMBUILD_FILE_INDEX.md` includes every critical file
- [ ] source-of-truth ownership is clear for every concern

---

## 13. Gate Sign-Off Log

| Stage | Variant | Decision | Approver | Date | Evidence Or Notes |
|---|---|---|---|---|---|
| | | | | | |

---

Last updated: 2026-03-27
