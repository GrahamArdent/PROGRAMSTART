# ACCEPTANCE_CRITERIA.md

Purpose: Testable acceptance criteria for signup, onboarding, consent, and first-run activation.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: PRODUCT_SPEC.md, USER_FLOWS.md, STATES_AND_RULES.md
Authority: Canonical acceptance criteria for USERJOURNEY behavior

---

## Goal

Translate the new-user journey into precise, testable requirements that design, frontend, backend, and QA can align on.

## Auth Entry Criteria

1. Given an anonymous user visits the auth entry, when the page loads, then the UI presents both sign-in and create-account paths.
2. Given an anonymous user visits the auth entry, when the page loads, then the UI communicates the product's core value in plain language.

## Signup Criteria

1. Given a new user submits signup, when required fields are missing, then signup does not complete and the user receives a specific validation error.
2. Given a new user submits signup, when password and confirmation do not match, then signup does not complete.
3. Given a new user submits signup, when Terms and Privacy acceptance is not explicitly provided, then signup does not complete.
4. Given a new user submits valid signup data, when account creation succeeds, then the user is routed to a verification-pending state.

## Verification Criteria

1. Given an unverified user, when verification has not yet occurred, then workspace access is blocked.
2. Given a valid verification callback, when the account has not completed onboarding, then the user is routed to onboarding rather than the normal workspace.
3. Given a valid verification callback, when the account is already onboarded, then the user is routed to the workspace.
4. Given an invalid or expired verification callback, when callback handling fails, then the user is routed to a recovery state with resend guidance.

## Consent Criteria

1. Given a new user creates an account, when signup succeeds, then the accepted Terms version and Privacy version are conceptually recordable.
2. Given a user reaches first upload or first AI generation, when the AI/data notice has not yet been acknowledged, then the user must be shown that notice before continuing.
3. Given a user declines optional marketing consent, when signup otherwise succeeds, then onboarding continues normally.

## Onboarding Criteria

1. Given a first-time verified user, when onboarding begins, then the user is shown a welcome step with clear next actions.
2. Given onboarding begins, when the user has not yet created a profile, then the system offers import and start-from-scratch paths.
3. Given the explore path exists, when selected, then it does not silently create ambiguous persisted user data.
4. Given onboarding is interrupted, when the user returns with a valid session, then onboarding resumes from a meaningful checkpoint.

## Import Path Criteria

1. Given a user selects import, when they upload an unsupported or invalid file, then the system rejects it with a clear error.
2. Given a valid resume upload, when parsing succeeds, then the user is shown extracted content for review before final profile confirmation.
3. Given parsed content is reviewed and confirmed, when the user continues, then an initial profile is created.

## Start-From-Scratch Criteria

1. Given a user selects start from scratch, when they submit minimum starter data, then the system creates a starter profile.
2. Given a starter profile is created, when the user continues, then they are routed into a guided editor or equivalent first-run workspace state.

## Activation Criteria

1. Given a user has no first profile, when they complete legal acceptance only, then they are not yet marked activated.
2. Given a user has created or imported a first profile, when they reach a usable first artifact or tailoring workflow, then first value is achieved.
3. Given first value is achieved, when onboarding finalizes, then onboarding is marked complete and future sessions bypass first-run onboarding.

## Returning User Criteria

1. Given a returning onboarded user signs in, when authentication succeeds, then the user is routed to workspace rather than onboarding.
2. Given a returning user is partially onboarded, when authentication succeeds, then the user resumes onboarding instead of being treated as fully activated.

## Analytics Criteria

1. Given a user enters the flow, when key milestones occur, then analytics events can be emitted for signup, verification, onboarding start, first profile creation, first value, and onboarding completion.
2. Given onboarding drop-off occurs, when analytics are reviewed, then the product team can identify the stage where abandonment happened.
