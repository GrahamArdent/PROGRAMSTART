# PROGRAMBUILD_CHECKLIST.md

# Program Build Execution Checklist

Use this file when you want the Program Build system in checklist form instead of narrative form.
This checklist depends on the authority rules in `PROGRAMBUILD_CANONICAL.md` and the file list in `PROGRAMBUILD_FILE_INDEX.md`.

---

## 1. Setup

- [ ] choose one process file: lite, product, or enterprise
- [ ] confirm `PROGRAMBUILD_CANONICAL.md` is current
- [ ] confirm `PROGRAMBUILD_FILE_INDEX.md` is current
- [ ] fill the shared project inputs block

---

## 2. Feasibility

- [ ] create `FEASIBILITY.md`
- [ ] define business and technical risks
- [ ] define kill criteria
- [ ] record go, no-go, or limited-spike outcome

---

## 3. Research

- [ ] create `RESEARCH_SUMMARY.md`
- [ ] validate stack maturity
- [ ] document alternatives
- [ ] document compliance concerns
- [ ] identify costly late-stage failure patterns

---

## 4. Requirements And UX

- [ ] create `REQUIREMENTS.md`
- [ ] create `USER_FLOWS.md`
- [ ] define P0 and P1 requirements
- [ ] define measurable acceptance criteria
- [ ] define loading, empty, error, and retry states
- [ ] define out-of-scope list

---

## 5. Architecture And Risk Spikes

- [ ] create `ARCHITECTURE.md`
- [ ] create `RISK_SPIKES.md`
- [ ] define API contract table
- [ ] define auth matrix
- [ ] define data ownership
- [ ] run risk spikes for unknowns

---

## 6. Scaffold And Guardrails

- [ ] create route contract layer
- [ ] create auth-aware client layer
- [ ] create streaming auth helper if needed
- [ ] add route alignment tests
- [ ] add reverse alignment tests
- [ ] add auth matrix tests
- [ ] add no-hardcoded-URL check
- [ ] create CI with timeouts

---

## 7. Test Strategy

- [ ] create `TEST_STRATEGY.md`
- [ ] define unit and component coverage rules
- [ ] define purpose and auth test rules
- [ ] define golden policy
- [ ] define Playwright and Chromium smoke/regression split
- [ ] create endpoint-to-test registry

---

## 8. Implementation Loop

- [ ] write purpose and auth tests first
- [ ] implement backend contract
- [ ] register routes
- [ ] implement typed frontend client
- [ ] implement UI states
- [ ] add component tests
- [ ] add E2E coverage
- [ ] add golden baseline if applicable
- [ ] update test registry

---

## 9. Release Readiness

- [ ] create `RELEASE_READINESS.md`
- [ ] verify rollback plan
- [ ] verify migration plan
- [ ] verify monitoring and alerting
- [ ] verify smoke tests
- [ ] verify support ownership

---

## 10. Audit

- [ ] create `AUDIT_REPORT.md`
- [ ] verify route, auth, and schema consistency
- [ ] verify planned-route and deprecated-route safety
- [ ] verify invalid-input and isolation behavior
- [ ] assign owners for critical and high findings

---

## 11. File Governance

- [ ] all critical control files use `PROGRAMBUILD_*.md`
- [ ] all stage output files use the standard names from `PROGRAMBUILD_CANONICAL.md`
- [ ] `PROGRAMBUILD_FILE_INDEX.md` includes every critical file
- [ ] source-of-truth ownership is clear for every concern

---

Last updated: 2026-03-27