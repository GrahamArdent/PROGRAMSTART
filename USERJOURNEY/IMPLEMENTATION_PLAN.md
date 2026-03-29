# IMPLEMENTATION_PLAN.md

Purpose: Non-code implementation plan for the new-user journey, with critical mapping to the current application structure.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: PRODUCT_SPEC.md, STATES_AND_RULES.md, ACCEPTANCE_CRITERIA.md
Authority: Canonical implementation-planning document for USERJOURNEY

---

## Goal

Map the desired onboarding and consent design to the current application structure without writing code yet.

## Current Surface Summary

Current relevant surfaces already exist:

1. login page at `frontend/app/auth/login/page.tsx`
2. signup page at `frontend/app/auth/signup/page.tsx`
3. auth callback route at `frontend/app/auth/callback/route.ts`
4. auth session context at `frontend/lib/auth-context.tsx`
5. main workspace entry at `frontend/app/page.tsx`
6. existing start-from-scratch builder modal at `frontend/components/builder/StartFromScratchModal.tsx`
7. existing workspace shell and sidebar in the dashboard/editor experience

This is useful because the product does not need a completely separate auth system. It does, however, need more structure around first-run state.

The recommended approach is to treat onboarding and consent as a bounded subsystem of the app, not as a separate product and not as a loose extension of the root workspace page.

## Critical Mapping Assessment

### What Maps Cleanly

1. The current signup page can conceptually host required legal checkboxes.
2. The current callback route is the natural place to branch verified first-time users into onboarding.
3. The current auth context is the natural place to expose onboarding and activation metadata once that exists.
4. The existing start-from-scratch modal proves the product already has a builder flow worth reusing.
5. The current workspace already distinguishes dashboard and editor, which is useful for activated users.

### Where The Current Mapping Is Weak

1. The current callback route only handles auth exchange and redirect. It does not model onboarding state, legal state, or recovery beyond simple auth failure.
2. The current auth context only exposes `user`, `session`, and `loading`. That is insufficient for first-run routing decisions.
3. The current home page assumes authentication should lead directly into workspace loading behavior and saved-profile bootstrap. That assumption conflicts with the proposed onboarding state machine.
4. The current `StartFromScratchModal` is implemented as a modal inside the workspace shell. That is convenient for existing users, but a poor default for first-time onboarding because it makes onboarding feel secondary instead of primary.
5. The current sidebar and dashboard shell assume the user already has an active resume workspace. That makes them a poor first surface for unactivated users.

### Critical Warning

The biggest structural risk is trying to bolt first-run onboarding onto `frontend/app/page.tsx` as more conditional branches. That file already carries auth redirect behavior, persisted local state, saved-profile bootstrap, dashboard/editor tab routing, and modal orchestration. If onboarding logic is added directly there without separation, it will become the wrong kind of god entrypoint.

## Recommended Architectural Direction

### Direction 1: Separate First-Run Routing From Activated Workspace Routing

Recommended conceptual split:

1. auth routes decide whether a session is valid
2. onboarding routes decide whether the user has completed required setup
3. workspace routes serve only activated users

With one exception:

4. skipped-onboarding users may enter a minimal unactivated workspace state, but must not be treated as activated users

This means onboarding should not just be a modal inside the existing workspace by default.

### Direction 2: Reuse Existing Builder Components Selectively

Recommended reuse:

1. reuse `StartFromScratchModal` logic and form sequence
2. do not necessarily reuse its current modal presentation for first-run
3. extract its business flow into an onboarding-capable surface later

Critical note:

The current builder modal is evidence of product capability, not necessarily evidence of good onboarding architecture.

### Direction 3: Add Explicit Onboarding Metadata

Conceptual metadata needed for routing:

1. email verified
2. terms accepted version and timestamp
3. privacy accepted version and timestamp
4. AI notice acknowledged timestamp
5. onboarding completed timestamp
6. first profile created timestamp
7. first value achieved timestamp

Without these, routing decisions will become brittle heuristics based on whether profile data exists.

## Proposed Workstreams

### Workstream 1: Product And Legal Definition

Inputs:

- finalize user journey
- finalize consent model
- finalize Terms and Privacy text

Output:

- approved product and policy requirements

### Workstream 2: Routing Model

Conceptual tasks:

1. define first-run route structure
2. define callback branching rules
3. define interrupted-onboarding resume rules

Critical concern:

If routing continues to rely on "authenticated means go to `/`", the proposed onboarding flow will never be structurally clean.

### Workstream 3: Auth And Account Metadata

Conceptual tasks:

1. determine where consent and onboarding state live
2. determine how versioned policy acceptance is stored
3. determine how first-run status is fetched on session bootstrap

Critical concern:

Do not hide onboarding state entirely in client-only local state. That would fail across browsers and devices and break legal defensibility.

### Workstream 4: Onboarding UI

Conceptual tasks:

1. create welcome step
2. create AI/data notice step
3. adapt import flow for first-run use
4. adapt start-from-scratch flow for first-run use
5. add first-goal selection
6. define skip-onboarding workspace behavior

Critical concern:

Do not overload the existing dashboard home to do all of this. A dashboard is not the same thing as an onboarding flow.

### Workstream 5: Workspace Handoff

Conceptual tasks:

1. define what marks onboarding complete
2. define the first activated workspace state
3. define the post-onboarding empty state or next-step state

Critical concern:

If onboarding completion is marked too early, users may land in an activated workspace without a useful artifact. That is a false activation.

The same applies to skip-onboarding users. Skip is a flexibility path, not an activation shortcut.

## Suggested Sequencing

1. finalize product and legal decisions
2. define state model and acceptance criteria
3. define route model and data ownership
4. define UI copy and screen structure
5. implement consent and metadata capture
6. implement onboarding routes and resume points
7. adapt import and builder flows for first-run
8. implement skip-onboarding minimal workspace behavior
9. implement activated workspace handoff
10. add tests for callback branching, resume points, skip-state behavior, and first-run outcomes

## Mapping Risks And Tradeoffs

### Risk 1: Reusing The Modal Builder As-Is

Why risky:

- a modal implies optionality
- onboarding for first-time users should feel primary
- modal state living inside the workspace shell makes resume-point recovery harder

Recommendation:

Reuse the flow logic, not necessarily the current presentation model.

### Risk 2: Using Profile Existence As A Proxy For Activation

Why risky:

- a user can have a profile but still be unactivated
- a profile can exist without legal acceptance history or AI notice acknowledgment

Recommendation:

Track explicit activation milestones instead of inferring everything from `profiles` state.

### Risk 3: Expanding `app/page.tsx` Further

Why risky:

- it already handles too many responsibilities
- onboarding, saved-profile bootstrap, workspace routing, and modal orchestration will become tightly coupled

Recommendation:

Keep first-run orchestration separate from the long-lived activated workspace shell.

### Risk 4: Treating Legal Acceptance As Pure Frontend UI

Why risky:

- no auditability
- no policy version history
- no cross-device consistency

Recommendation:

Treat legal acceptance as persisted account state, not just checkbox behavior.

### Risk 5: Overbuilding Before Decisions Are Locked

Why risky:

- legal text may change
- route structure may change
- explore-first may be cut

Recommendation:

Freeze product decisions first, then implement in sequence.

### Risk 6: Treating Skip As A Shortcut To Activation

Why risky:

- users may bypass the parts that produce actual value
- analytics become misleading
- workspace behavior becomes inconsistent

Recommendation:

Treat skip as an alternate path into an unactivated workspace state with visible recovery back into setup.

## Test Planning Notes

Future implementation should be verified at minimum with:

1. signup validation tests
2. callback branch tests for onboarded vs not onboarded users
3. interrupted onboarding resume tests
4. first-run import success and failure tests
5. first-run start-from-scratch tests
6. activated workspace handoff tests
7. consent persistence and policy-version tests

## Bottom-Line Recommendation

Do not implement this as a thin patch on top of the current login page and root workspace route. The auth pieces are reusable, but the first-run journey deserves its own state model and route flow. The current app structure can support that, but only if onboarding is treated as a first-class product surface rather than another modal or dashboard branch.
