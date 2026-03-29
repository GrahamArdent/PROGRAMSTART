# ANALYTICS_AND_OUTCOMES.md

Purpose: Define expected outcomes, analytics checkpoints, and activation metrics for the new-user journey.
Owner: Solo operator
Last updated: 2026-03-27
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
