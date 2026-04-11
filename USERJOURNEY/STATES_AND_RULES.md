# STATES_AND_RULES.md

Purpose: Define lifecycle states, routing rules, and activation logic for new and returning users.
Owner: Solo operator
Last updated: 2026-04-01
Depends on: PRODUCT_SPEC.md, USER_FLOWS.md
Authority: Canonical state and routing model for onboarding

---

## Lifecycle States

### State 1: Anonymous

User has no authenticated session.

### State 2: Account Created, Unverified

User account exists, but email verification is incomplete.

### State 3: Verified, Not Onboarded

User has a valid session and verified identity, but onboarding is not complete.

### State 4: Consent Complete, No Profile Yet

User has accepted required legal terms and AI notice where needed, but has not created or imported a first profile.

### State 5: Profile Created, Not Activated

User has a profile, but has not yet reached first value.

### State 5B: Guided Onboarding Skipped, Not Activated

User intentionally bypassed guided onboarding but has not yet achieved first value and must not be treated as fully activated.

### State 6: Activated User

User has completed onboarding and reached a first value moment.

### State 7: Returning Activated User

User should bypass onboarding and go to workspace restoration.

## Core Routing Rules

1. Anonymous users attempting to access workspace routes are sent to login.
2. Unverified users are sent to verification-pending state.
3. Verified users without completed onboarding are sent to onboarding.
4. Onboarded users are sent to workspace.
5. Users with incomplete onboarding should resume from the last meaningful onboarding step rather than always restarting.
6. Users who skip guided onboarding should still be able to complete setup later from inside the workspace.

## Account Milestones

Conceptual milestones to distinguish:

1. account_created_at
2. email_verified_at
3. terms_accepted_at
4. privacy_accepted_at
5. ai_notice_acknowledged_at
6. onboarding_completed_at
7. first_profile_created_at
8. first_value_achieved_at

## Activation Rule

User is considered activated when both conditions are true:

1. a first profile exists
2. the user has reached a first value moment

First value moment can be one of:

- imported resume reviewed and confirmed
- starter profile created and opened in editor
- tailoring workflow started with a JD against a valid profile

## Resume Point Rules

If onboarding is interrupted:

1. resume at last incomplete onboarding stage
2. do not discard prior consent state
3. do not force the user to re-enter already confirmed information unless policy version changed

## Policy Update Rule

If Terms or Privacy version changes after prior acceptance:

1. user may be prompted again before continued product use
2. consent event must capture the new version

## Operational Rules

1. Signup completion does not imply workspace readiness.
2. Verification completion does not imply onboarding completion.
3. First login after verification should not route to the normal workspace unless onboarding is already complete.
4. Returning users should not repeatedly see onboarding interstitials without a versioned consent reason.

## Edge Conditions

### Verified User With No Profile

Send to onboarding resume point.

### Verified User With Profile But No Onboarding Completion Flag

Treat as partial onboarding and resume from the most defensible checkpoint.

### User Declines Optional Marketing Consent

Continue product onboarding normally.

### User Refuses Required Legal Acceptance

Do not complete signup activation.

### User Skips Guided Onboarding

Allow workspace entry only into a minimal unactivated state.

### User Has Session But Callback Failed

Send to recovery flow and re-check account state.
