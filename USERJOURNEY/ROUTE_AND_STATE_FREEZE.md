# ROUTE_AND_STATE_FREEZE.md

Purpose: Freeze the proposed route map and state model before implementation planning expands.
Owner: Solo operator
Last updated: 2026-03-31
Depends on: STATES_AND_RULES.md, USER_FLOWS.md
Authority: Canonical routing and state baseline for onboarding planning

---

## Purpose

This document prevents routing drift during implementation planning. It is a planning baseline, not a final code contract.

The local operator dashboard in this template repository is not part of the end-user onboarding route family defined here.

## Frozen Principles

1. Authentication is not the same as activation.
2. Onboarding is not the same as normal workspace usage.
3. Returning users should bypass first-run onboarding unless a policy or state reason requires otherwise.
4. First-run onboarding should not depend on deep branching inside the activated workspace shell.

## Proposed Logical Routes

These names are descriptive and can be adjusted later, but the separation should remain.

| Logical Route | Purpose | Notes |
|---|---|---|
| `/auth/login` | returning-user authentication | existing concept |
| `/auth/signup` | new-user account creation | existing concept |
| `/auth/verify-pending` | email verification waiting state | new planned state |
| `/auth/callback` | verification or auth callback handling | existing concept |
| `/onboarding/welcome` | first-run orientation | new planned state |
| `/onboarding/notice` | AI/data notice before first upload or generation | new planned state |
| `/onboarding/import` | import resume step | planned surface |
| `/onboarding/review-import` | review parsed content | planned surface |
| `/onboarding/start` | start-from-scratch onboarding surface | planned adaptation of existing capability |
| `/onboarding/goal` | choose first goal | planned surface |
| `/workspace` with `unactivated_skip` state | minimal workspace after guided onboarding is skipped | allowed but not equivalent to activated workspace |
| `/workspace` | activated dashboard/workspace entry | conceptually separate from onboarding |

## State Baseline

| State | Meaning | Allowed Destination |
|---|---|---|
| anonymous | no session | auth entry or public surfaces only |
| account_created_unverified | account exists, email not verified | verify pending |
| verified_not_onboarded | session valid, onboarding incomplete | onboarding route family |
| consent_complete_no_profile | legal steps complete, no profile yet | onboarding import or scratch |
| profile_created_not_activated | first profile exists, first value not yet achieved | onboarding goal or first-run workspace handoff |
| guided_onboarding_skipped_not_activated | user bypassed guided flow but is not yet activated | minimal workspace with recovery CTA |
| activated | onboarding complete and first value achieved | workspace |

## Branching Rules

### Callback Branching

1. If callback succeeds and user is activated: route to workspace.
2. If callback succeeds and user is not onboarded: route to onboarding welcome or resume point.
3. If callback succeeds and user has skipped guided onboarding but is not activated: route to minimal workspace state.
3. If callback fails: route to recovery state.

### Workspace Access Branching

1. If user is anonymous: route to login.
2. If user is verified but not onboarded: route to onboarding.
3. If user is guided-onboarding-skipped but not activated: allow minimal workspace access only.
4. If user is activated: allow workspace access.

## Explicit Freeze On Current Risks

The following approaches are considered anti-patterns for this work unless re-approved:

1. expanding the current root workspace page into the primary onboarding router
2. treating the existing start-from-scratch modal as the complete onboarding system without adaptation
3. inferring all onboarding state only from whether profile data exists
4. storing consent state only in client local storage
5. treating skipped onboarding as equivalent to completed onboarding

## Change Control

If this route/state baseline changes, update:

1. `DECISION_LOG.md`
2. `USER_FLOWS.md`
3. `IMPLEMENTATION_PLAN.md`
4. `IMPLEMENTATION_TRACKER.md`

## Approval And Exit Gate Status

This section records the Phase 0 exit gate review against the route and state baseline.

| Item | Status | Notes |
|---|---|---|
| Route family defined (login, signup, verify, onboarding, workspace) | Complete | 11 logical routes defined above |
| State baseline covers all meaningful user conditions | Complete | 7 states covering anonymous through activated |
| Callback branching rules documented | Complete | 4 rules covering activated, not-onboarded, skip-state, and failure paths |
| Workspace access branching rules documented | Complete | 4 rules covering all access conditions |
| Anti-patterns frozen | Complete | 5 anti-patterns explicitly prohibited |
| Alignment with DECISION_LOG.md confirmed | Complete | Route and state decisions are consistent with logged decisions |
| Product owner sign-off | Pending | Use dashboard Signoff action on USERJOURNEY phase_0 to record approval |

Last updated: 2026-03-27
