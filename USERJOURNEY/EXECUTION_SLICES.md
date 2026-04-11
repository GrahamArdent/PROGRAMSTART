# EXECUTION_SLICES.md

Purpose: Define concrete implementation slices and test scope before coding begins.
Owner: Solo operator
Last updated: 2026-03-31
Depends on: IMPLEMENTATION_PLAN.md, IMPLEMENTATION_TRACKER.md, ACCEPTANCE_CRITERIA.md
Authority: Canonical pre-coding execution sequence for USERJOURNEY

---

## Goal

Break the onboarding implementation into safe, reviewable slices that minimize routing regressions and make testing explicit.

## Slice 1: Consent And State Model Freeze

### Outcome

Consent/version rules and activation milestones are frozen before any UI or routing work begins.

### Scope

1. finalize required consent events
2. finalize skip-onboarding rules
3. finalize activation definition

### Primary Risk

Building UI before state semantics are fixed causes rework and policy drift.

### Test Scope

Planning-only verification against `ACCEPTANCE_CRITERIA.md` and `ROUTE_AND_STATE_FREEZE.md`.

## Slice 2: Auth Entry And Signup Contract

### Outcome

Signup surface is defined to capture required legal acceptance without overloading the form.

### Scope

1. auth entry behavior
2. signup contract
3. verification-pending and recovery states

### Critical Mapping Note

This should reuse existing login/signup concepts, but not assume they are functionally complete for onboarding.

### Test Scope

1. signup validation behavior
2. required consent presence
3. verification pending and recovery scenarios

## Slice 3: Callback Branching And Route Guards

### Outcome

Verified users branch to onboarding, skip-state workspace, or activated workspace correctly.

### Scope

1. callback branch rules
2. workspace guard rules
3. unactivated skip-state handling

### Critical Mapping Note

This is the highest regression-risk slice because it touches the boundary between auth and the main workspace.

### Test Scope

1. valid callback for activated user
2. valid callback for not-onboarded user
3. valid callback for skip-state user
4. invalid callback recovery
5. anonymous access to workspace

## Slice 4: Onboarding Welcome And Skip Path

### Outcome

First-time users get a clear welcome surface with import-first, scratch, and skip options.

### Scope

1. welcome surface
2. skip guided onboarding path
3. persistent `Complete setup` recovery path

### Critical Mapping Note

Do not implement skip by routing users into the same experience as activated users without visible incomplete-state treatment.

### Test Scope

1. welcome path selection
2. skip path state recording
3. workspace incomplete-state behavior after skip

## Slice 5: AI Notice Gating

### Outcome

AI/data notice is enforced before first upload or generation when required.

### Scope

1. notice display rules
2. notice acknowledgment behavior
3. skip-onboarding interaction with notice gating

### Critical Mapping Note

This should not be treated as decorative copy; it is a real gate tied to state.

### Test Scope

1. first upload blocked until notice is acknowledged
2. first generation blocked until notice is acknowledged
3. already-acknowledged users are not re-blocked unnecessarily

## Slice 6: Import Resume First-Run Flow

### Outcome

Import path supports first-run creation and review before activation.

### Scope

1. upload entry
2. parse review
3. initial profile confirmation

### Critical Mapping Note

Tailoring should not start before import review is confirmed.

### Test Scope

1. invalid file rejection
2. parse success review state
3. confirmed import creates initial profile

## Slice 7: Start-From-Scratch First-Run Flow

### Outcome

Existing builder capability is adapted into first-run onboarding without relying on modal semantics.

### Scope

1. starter information capture
2. initial profile creation
3. first workspace handoff for scratch users

### Critical Mapping Note

Reuse the flow logic where possible, but do not assume the current modal presentation is the right onboarding shell.

### Test Scope

1. starter flow validation
2. profile creation success
3. handoff to unactivated or activated workspace state as designed

## Slice 8: Goal Selection And First Value Handoff

### Outcome

Users choose initial intent and are moved into the right first workspace state.

### Scope

1. improve current resume
2. tailor to JD
3. build fresh version

### Test Scope

1. goal selection persistence
2. route or UI emphasis correctness
3. first value event conditions

## Slice 9: Analytics And Policy-Version Handling

### Outcome

Onboarding funnel and policy-version acceptance can be measured and re-checked.

### Scope

1. canonical event taxonomy
2. activation event
3. policy version re-acceptance logic

### Test Scope

1. funnel event emission points
2. activation event consistency
3. policy change behavior

## Recommended Build Order

1. Slice 1
2. Slice 2
3. Slice 3
4. Slice 4
5. Slice 5
6. Slice 6
7. Slice 7
8. Slice 8
9. Slice 9

## Outcome-To-Slice Backlog

This matrix converts the desired-outcome analysis into an execution-ready backlog. Use it to decide which slice owns each missing capability.

| Desired outcome | Primary slice owner | Route or state anchors | First files to review | Required proof |
|---|---|---|---|---|
| higher signup-to-activation conversion | Slices 2, 3, 4, 6, 7, 8 | `/auth/signup`, `/auth/verify-pending`, `/auth/callback`, onboarding family, `/workspace` | `frontend/app/auth/signup/page.tsx`, `frontend/app/auth/callback/route.ts`, onboarding route surfaces, `profilesApi.ts` | route tests, onboarding flow tests, activation event test |
| lower confusion in the first session | Slices 2, 4, 5 | `/auth/login`, `/auth/signup`, `/onboarding/welcome`, `/onboarding/notice` | `frontend/app/auth/login/page.tsx`, `frontend/app/auth/signup/page.tsx`, onboarding welcome and notice surfaces | content assertions, route-state tests, browser flow test |
| stronger trust through better disclosure | Slices 1, 5, 9 | consent checkpoints plus `/onboarding/notice` | consent metadata layer, notice surface, analytics layer | notice-gate tests, consent event tests, versioning tests |
| better separation between account creation and real product activation | Slices 1, 3, 4, 8, 9 | `/auth/verify-pending`, `/auth/callback`, unactivated skip state, `/workspace` | `frontend/app/auth/callback/route.ts`, `frontend/lib/auth-context.tsx`, `frontend/app/page.tsx`, dashboard surfaces | callback branching tests, guard tests, first-value event tests |
| cleaner legal audit trail for consent events | Slices 1, 5, 9 | signup checkpoint and AI-notice checkpoint | consent metadata model, auth/session state layer, analytics layer | persisted consent-record tests, policy-version tests |

## Route-To-Proof Backlog

| Planned route or state | Owning slice | Primary outcome protected | Minimum test type required |
|---|---|---|---|
| `/auth/login` | Slice 2 | lower confusion in the first session | browser or component rendering test |
| `/auth/signup` | Slice 2 | higher signup-to-activation conversion | validation test plus consent-contract test |
| `/auth/verify-pending` | Slice 2 | better separation between account creation and activation | route and recovery test |
| `/auth/callback` | Slice 3 | better separation between account creation and real product activation | callback branch matrix test |
| `/onboarding/welcome` | Slice 4 | lower confusion in the first session | path-selection test |
| `/onboarding/notice` | Slice 5 | stronger trust through better disclosure | gating and acknowledgement test |
| `/onboarding/import` | Slice 6 | higher signup-to-activation conversion | upload validation test |
| `/onboarding/review-import` | Slice 6 | higher signup-to-activation conversion | parse-review confirmation test |
| `/onboarding/start` | Slice 7 | higher signup-to-activation conversion | starter-profile creation test |
| `/onboarding/goal` | Slice 8 | better separation between profile creation and first value | goal-persistence test |
| `/workspace` with `unactivated_skip` state | Slice 4 and Slice 8 | better separation between account creation and real product activation | skip-state guard test |
| `/workspace` activated handoff | Slice 8 | higher signup-to-activation conversion | first-value handoff test |

## Why This Order

This order isolates the highest-risk work first:

1. state definition before UI drift
2. auth/callback behavior before onboarding polish
3. first-run branching before workspace handoff
4. analytics after product behavior is stable
