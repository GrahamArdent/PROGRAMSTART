# IMPLEMENTATION_TRACKER.md

Purpose: Phased execution tracker for implementing the new-user journey without losing scope control.
Owner: Solo operator
Last updated: 2026-03-29
Depends on: IMPLEMENTATION_PLAN.md, ROUTE_AND_STATE_FREEZE.md, ACCEPTANCE_CRITERIA.md, DELIVERY_GAMEPLAN.md
Authority: Canonical execution tracker for USERJOURNEY implementation planning

---

## Usage Rules

1. Update this file when implementation planning or execution status changes.
2. Do not turn the product spec into a changelog.
3. Do not mark phases complete without explicit evidence.
4. Keep phase status, slice readiness, and blockers aligned with `DELIVERY_GAMEPLAN.md`.

## Phase Overview

| Phase | Status | Goal | Primary Owner | Blockers | Exit Gate |
|---|---|---|---|---|---|
| 0 | Completed | Freeze decisions and route/state model | Solo operator | none; all product decisions resolved; external legal items scoped to Phase 1 | route/state freeze approved |
| 1 | In Progress | Finalize legal and consent model | Solo operator with legal review as needed | 5 legal/operational items triaged — counsel review pending on Q1 and Q2; operational defaults set for Q4 and Q5 | legal review items categorized into accepted / revise / unresolved |
| 2 | Planned | Define UI surfaces and UX text | Solo operator | route freeze, consent model | screen inventory approved |
| 3 | Planned | Define data ownership and onboarding metadata | Solo operator | legal/versioning decisions | metadata model approved |
| 4 | Planned | Define implementation slices and test plan | Solo operator | prior phases incomplete | execution slices approved |
| 5 | Planned | Implement auth and routing changes | Solo operator | code execution not started | callback + route behavior verified |
| 6 | Planned | Implement onboarding flows | Solo operator | route and metadata dependencies | first-run paths verified |
| 7 | Planned | Implement activated workspace handoff | Solo operator | onboarding surfaces complete | first-value handoff verified |
| 8 | Planned | Validate analytics and legal audit trail | Solo operator with external review if needed | implementation complete | acceptance criteria satisfied |

## Slice Readiness

Status values: `Pending`, `Selected`, `Ready`, `Blocked`, `Completed`

| Slice | Status | Readiness Gate | Notes |
|---|---|---|---|
| Slice 1 | Selected | route/state and consent semantics frozen | current starting slice once phase 0 exits |
| Slice 2 | Pending | auth entry contract and required consent behavior approved | signup contract and verification-pending state cannot be finalized until Slice 1 consent events and skip-onboarding rules are frozen |
| Slice 3 | Pending | callback branching contract and guard rules approved | callback branch and workspace guard rules depend on Slice 2 signup contract being stable; highest regression risk in the sequence |
| Slice 4 | Pending | welcome, skip-state, and incomplete-state treatment approved | welcome screen and skip-state routing directly depend on Slice 3 guard rules; do not design skip-state UX before guard semantics are confirmed |
| Slice 5 | Pending | AI notice gating rules approved | AI notice gate placement relies on knowing the skip-state entry path (Slice 4) and confirmed consent coverage from Slice 1; misalignment here affects every upload and generation trigger |
| Slice 6 | Pending | import review flow and profile creation contract approved | import surface depends on stable route guards (Slice 3) and confirmed AI notice gate point (Slice 5); profile creation timing must not be resolved before import session completes |
| Slice 7 | Pending | scratch flow ownership and builder reuse boundaries approved | scratch flow reuse boundaries must be defined after import review (Slice 6) to protect onboarding from modal-leakage patterns documented in the risk register |
| Slice 8 | Pending | first-value handoff and intent persistence rules approved | activation handoff requires at least one of import (Slice 6) or scratch (Slice 7) to be structurally complete; intent persistence rules must avoid double-counting partial completions |
| Slice 9 | Pending | event taxonomy and policy-version handling approved | analytics event taxonomy and consent-version recording must be added last after the behavioral flow is stable; premature instrumentation locks in wrong funnel semantics |

## Phase 0: Decision Freeze

### Scope

- finalize onboarding shape
- finalize route separation
- finalize activation definition

### Key Decisions Required

1. dedicated onboarding routes or embedded workspace flow
2. account-before-upload policy
3. import-first default path
4. definition of first value moment

### Risks

1. implementation begins before route model is frozen
2. onboarding is patched into existing root page branches

### Impacted Files / Areas

- `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md`
- `USERJOURNEY/DECISION_LOG.md`
- `USERJOURNEY/OPEN_QUESTIONS.md`

### Exit Gate

- route and state model approved by product owner

### Exit Gate Checklist

| Criterion | Status | Evidence |
|---|---|---|
| All key product decisions resolved | Complete | 26 decisions in `DECISION_LOG.md` |
| Dedicated onboarding route family confirmed | Complete | `ROUTE_AND_STATE_FREEZE.md` — Proposed Logical Routes |
| State baseline with 7 named states documented | Complete | `ROUTE_AND_STATE_FREEZE.md` — State Baseline |
| Branching rules for callback and workspace access written | Complete | `ROUTE_AND_STATE_FREEZE.md` — Branching Rules |
| Anti-patterns frozen | Complete | `ROUTE_AND_STATE_FREEZE.md` — Explicit Freeze On Current Risks |
| Activation event defined | Complete | `first_value_achieved` in `DECISION_LOG.md` |
| Account-before-upload confirmed | Complete | `DECISION_LOG.md` |
| Import-first default confirmed | Complete | `DECISION_LOG.md` |
| Skip-onboarding rules defined | Complete | `DECISION_LOG.md` — skip routes to unactivated workspace |
| Consent semantics captured | Complete | `LEGAL_AND_CONSENT.md` (Phase 1 will harden with legal review) |
| Remaining external items triaged into Phase 1 | Complete | `OPEN_QUESTIONS.md` — 5 legal/operational items scoped to Phase 1 |
| Product owner sign-off on route/state baseline | Complete | Approved 2026-03-27 — recorded in USERJOURNEY_STATE.json |

## Phase 1: Legal And Consent Model

### Scope

- confirm Terms structure
- confirm Privacy structure
- confirm AI notice behavior
- confirm retention claims

### Risks

1. product copy overpromises data handling
2. retention promises are made before operations are defined

### Impacted Files / Areas

- `USERJOURNEY/LEGAL_AND_CONSENT.md`
- `USERJOURNEY/TERMS_OF_SERVICE_DRAFT.md`
- `USERJOURNEY/PRIVACY_POLICY_DRAFT.md`
- `USERJOURNEY/LEGAL_REVIEW_NOTES.md`

### Exit Gate

- legal review items categorized into accepted / revise / unresolved

## Phase 2: UX Surface Definition

### Scope

- freeze required onboarding screens
- align copy with legal model
- define first-run empty states and handoff states

### Risks

1. onboarding is modeled as a collection of ad hoc modals
2. screens are not tied to route/state transitions

### Impacted Files / Areas

- `USERJOURNEY/SCREEN_INVENTORY.md`
- `USERJOURNEY/UX_COPY_DRAFT.md`
- `USERJOURNEY/USER_FLOWS.md`

### Exit Gate

- every required state has a named surface and next action

## Phase 3: Metadata And Ownership Planning

### Scope

- define conceptual storage of consent and onboarding metadata
- define ownership of route decisions
- define how interrupted onboarding resumes

### Risks

1. onboarding state is tracked only in local client state
2. legal versioning is not persisted

### Impacted Files / Areas

- `USERJOURNEY/STATES_AND_RULES.md`
- `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md`
- future auth/account metadata model

### Exit Gate

- metadata and source of truth approved for implementation

## Phase 4: Execution Slicing And Test Planning

### Scope

- break implementation into safe slices
- map acceptance criteria to tests
- identify highest-risk regressions

### Risks

1. auth callback changes break returning users
2. workspace routing regressions are missed

### Impacted Files / Areas

- `USERJOURNEY/ACCEPTANCE_CRITERIA.md`
- `USERJOURNEY/IMPLEMENTATION_PLAN.md`

### Exit Gate

- execution plan approved with test coverage expectations

## Critical Risk Register

| Risk | Severity | Why It Matters | Mitigation |
|---|---|---|---|
| Onboarding logic expands `app/page.tsx` further | High | Root page already mixes auth, bootstrap, dashboard, editor, and modal behavior | keep onboarding outside activated workspace route |
| Builder modal reused as-is for first-run onboarding | High | modal semantics are weak for primary onboarding | reuse flow logic, not necessarily modal presentation |
| Legal acceptance kept only in UI state | High | not auditable, not cross-device, weak for policy changes | persist versioned consent metadata |
| Activation inferred only from profile existence | Medium | false positives and poor routing | track explicit milestones |
| Explore-first path introduces ambiguous state | Medium | users can become stuck or partially activated | keep explore path constrained or cut it |

## File-Level Ownership Hints

| Area | Likely Owner | Reason |
|---|---|---|
| auth entry, signup, callback | Frontend + auth owner | user entry and callback branching |
| onboarding route surfaces | Frontend | dedicated first-run flow |
| consent/version metadata | Backend + auth/data owner | persistent source of truth |
| policy text | Product + Legal | must match actual behavior |
| analytics funnel | Product + frontend/backend | track activation and drop-off |
