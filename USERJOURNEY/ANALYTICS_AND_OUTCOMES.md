# ANALYTICS_AND_OUTCOMES.md

Purpose: Define expected outcomes, analytics checkpoints, and activation metrics for the new-user journey.
Owner: Solo operator
Last updated: 2026-03-31
Depends on: PRODUCT_SPEC.md, STATES_AND_RULES.md
Authority: Canonical analytics and outcome model for onboarding success

---

## Why This Exists

The new-user journey should be measurable. Without explicit checkpoints, it is impossible to know whether users are dropping off at signup, verification, consent, upload, or first value.

## Expected Outcomes

Expected outcomes from implementing this spec:

1. higher signup-to-activation conversion
2. lower confusion in the first session
3. stronger trust through better disclosure
4. better separation between account creation and real product activation
5. cleaner legal audit trail for consent events

## Outcome To Route And Milestone Mapping

Not every desired outcome is a route concern. Some outcomes are delivered by a route transition, some by a state transition, and some by analytics or consent records.

| Desired outcome | Primary route or state anchor | Primary milestone or evidence |
|---|---|---|
| higher signup-to-activation conversion | `/auth/signup` -> `/auth/verify-pending` -> onboarding route family -> `/workspace` | `first_value_achieved` occurs more often after signup |
| lower confusion in the first session | `/auth/login`, `/auth/signup`, `/onboarding/welcome`, `/onboarding/notice` | lower abandonment before `first_profile_created`; fewer users stall before path selection |
| stronger trust through better disclosure | `/onboarding/notice` and required consent capture before risky actions | `ai_notice_seen`, `ai_notice_acknowledged`, versioned legal acceptance records |
| better separation between account creation and real product activation | `/auth/verify-pending`, `/auth/callback`, onboarding route family, `/workspace` with unactivated skip state | verified users are not counted as activated until `first_value_achieved` |
| cleaner legal audit trail for consent events | signup and notice checkpoints rather than a single route | timestamped, versioned consent events for Terms, Privacy, and AI notice acknowledgement |

## Planned Route Anchors

The route family that supports these outcomes is defined in `ROUTE_AND_STATE_FREEZE.md` and `USER_FLOWS.md`.

| Outcome checkpoint | Planned logical route or state |
|---|---|
| auth entry viewed | `/auth/login` and `/auth/signup` |
| signup accepted, verification still pending | `/auth/verify-pending` |
| verification callback branches user by state | `/auth/callback` |
| onboarding orientation and path choice | `/onboarding/welcome` |
| AI and data disclosure gate | `/onboarding/notice` |
| import resume path | `/onboarding/import` |
| import review and confirmation | `/onboarding/review-import` |
| start-from-scratch path | `/onboarding/start` |
| choose first goal after profile creation | `/onboarding/goal` |
| skip-guided-onboarding recovery path | `/workspace` with `unactivated_skip` state |
| activated handoff | `/workspace` |

## Outcomes Without A Single Route

The following desired outcomes should not be treated as single-page or single-route requirements:

1. `first_value_achieved` is a milestone, not a route. It occurs when the user reaches a usable artifact or tailoring workflow.
2. cleaner legal audit trail for consent events depends on stored event records and versioning, not a standalone screen.
3. higher signup-to-activation conversion is an aggregate funnel result, not a route.
4. better analytics around onboarding drop-off depends on event coverage across multiple steps, not one page.

## Current Template-Repo Reality

This template repository does **not** currently implement the end-user onboarding route family above.

What exists today in code is the local operator dashboard route set in `scripts/programstart_serve.py`:

1. `/` and `/index.html`
2. `/api/state`
3. `/api/doc`
4. `/api/run`
5. `/api/uj-phase`
6. `/api/uj-slice`
7. `/api/workflow-signoff`
8. `/api/workflow-advance`
9. `/api/bootstrap`

Those routes support planning, inspection, and workflow control. They do not satisfy the planned user-facing onboarding outcomes by themselves.

## Current Gaps By Desired Outcome

| Desired outcome | Planned route support exists in docs | Implemented route support exists in this repo | Gap summary |
|---|---|---|---|
| higher signup-to-activation conversion | Yes | No | requires real auth, onboarding, and first-value product flow implementation |
| lower confusion in the first session | Yes | No | requires end-user entry, welcome, and notice surfaces |
| stronger trust through better disclosure | Yes | No | requires enforced AI notice and consent event recording in product code |
| better separation between account creation and real product activation | Yes | No | requires callback branching, activation milestone storage, and unactivated skip-state handling |
| cleaner legal audit trail for consent events | Partially | No | requires persisted versioned consent records, not just planning docs |

## Primary Funnel

Suggested funnel:

1. auth_entry_viewed
2. signup_started
3. signup_submitted
4. verification_email_sent
5. email_verified
6. onboarding_started
7. ai_notice_seen
8. ai_notice_acknowledged
9. import_resume_selected or start_from_scratch_selected or skip_guided_onboarding_selected
10. first_profile_created
11. first_value_achieved
12. onboarding_completed
13. workspace_activated

## Suggested Event Definitions

### auth_entry_viewed

Triggered when the user loads the login/signup entry surface.

### signup_started

Triggered when the user begins the signup form.

### signup_submitted

Triggered when the user submits a valid signup form.

### email_verified

Triggered when auth callback completes successfully for verification.

### onboarding_started

Triggered when a first-time verified user lands on onboarding welcome.

### ai_notice_acknowledged

Triggered when the user explicitly continues past the AI/data notice.

### first_profile_created

Triggered when the system has a persisted initial profile.

### first_value_achieved

Triggered when the user has a usable first artifact or active tailoring flow.

This is the canonical activation event for reporting.

### onboarding_completed

Triggered when the first-run journey is complete and the user is ready for normal workspace behavior.

### workspace_activated

Triggered when the user is handed off into the normal activated workspace after first value is already achieved.

This is a downstream handoff event, not the canonical activation metric.

## Core Metrics

1. signup completion rate
2. verification completion rate
3. onboarding completion rate
4. first profile creation rate
5. first value achievement rate
6. time from signup to first value
7. drop-off by onboarding step
8. skip-guided-onboarding usage rate
9. activation rate for skip users vs guided users
10. drop-off by funnel variant, with skip-state users tracked separately from guided users

## Product Health Questions

This analytics model should answer:

1. Are users failing at signup or at verification?
2. Are users reading the AI notice and abandoning?
3. Do imported-resume users activate faster than start-from-scratch users?
4. Does first-run tailoring increase or reduce activation?
5. Which step causes the largest abandonment?
6. Does skip-onboarding help activation, or just hide abandonment deeper in the workspace?

## Interpreting Outcomes

### Positive Indicators

1. short time from verification to first profile creation
2. strong completion rate for import path
3. strong return rate after onboarding completion
4. skip users still convert into first value at acceptable rates

### Negative Indicators

1. many verified users never start onboarding
2. many users enter onboarding but never create a profile
3. many users create a profile but do not reach first value
4. many skip users never reach first value, indicating skip is masking friction rather than reducing it

## Target Benchmarks

Recommended targets for the first release of this flow:

1. median time from verification to first value <= 3 minutes
2. p75 time from verification to first value <= 5 minutes
3. skip-onboarding users should not underperform guided users so severely that skip becomes a dead-end path

## Review Thresholds

Product review should be triggered when any onboarding step loses 20% or more of its entrants over a meaningful sample window.

Use this as an operating threshold, not a claim that every step must always convert above 80% in every small sample.

## Option 3 Clarification

The earlier "option 3" referred to producing a full product specification instead of only discussion notes.

Expected outcome of that approach:

1. implementation-ready requirements
2. testable acceptance criteria
3. clearer handoff to design and engineering
4. explicit routing and state behavior
5. measurable product outcomes instead of vague goals
