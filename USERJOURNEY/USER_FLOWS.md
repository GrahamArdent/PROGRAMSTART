# USER_FLOWS.md

Purpose: Route-level and screen-level definition of the new-user journey.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: PRODUCT_SPEC.md
Authority: Canonical flow definition for user-facing onboarding behavior

---

## Flow 1: New User Signup To Activation

1. User lands on auth entry.
2. User chooses `Create account`.
3. User submits email, password, confirmation, required legal acceptance.
4. System creates account in unverified state.
5. User sees verification-required page.
6. User verifies email.
7. Auth callback checks onboarding state.
8. User is routed to onboarding welcome.
9. User selects initial path.
10. User acknowledges AI/data notice before upload or generation.
11. User imports resume or starts from scratch.
12. System creates initial profile.
13. User reaches first value moment.
14. User is routed to activated workspace.

## Flow 1B: New User Skip Guided Onboarding

1. User lands on onboarding welcome.
2. User selects `Skip setup for now`.
3. System records guided onboarding skipped state.
4. User is routed to minimal workspace state, not full activated state.
5. Workspace surfaces persistent `Complete setup` action.
6. AI/data notice is still required before first upload or first generation if not yet acknowledged.
7. User becomes activated only after first value is achieved.

## Flow 2: Returning User Login

1. User lands on auth entry.
2. User chooses `Sign in`.
3. User submits credentials.
4. Auth session is established.
5. System checks onboarding completion.
6. If onboarding complete, route to workspace.
7. If onboarding incomplete, route to onboarding resume point.

## Flow 3: Verification Link Failure

1. User clicks invalid, expired, or already-used verification link.
2. System routes to recovery state.
3. User sees explanation and next action.
4. User can resend verification email or return to login.

## Flow 4: Import Existing Resume

1. User chooses import path.
2. User sees supported formats and data-use notice.
3. User uploads resume.
4. System validates file and rejects unsupported or invalid payloads.
5. System parses content.
6. User reviews parsed content.
7. User confirms or edits extracted sections.
8. System saves initial profile.
9. User lands in workspace with import-success state.

## Flow 5: Start From Scratch

1. User chooses start-from-scratch path.
2. User enters minimum starter data.
3. System generates empty or starter profile scaffold.
4. User enters guided builder or editor state.
5. System presents recommended next action.
6. User lands in workspace with starter-profile state.

## Flow 6: Tailor To Job Description First

1. User imports or creates a first profile.
2. System asks for first objective.
3. User selects `Tailor to a job description`.
4. User is prompted to paste or upload JD.
5. System starts tailoring workflow.
6. User sees tailored recommendations or transformed content.

## Route Intent Model

Suggested logical routes and states:

- `/auth/login`
- `/auth/signup`
- `/auth/verify-pending`
- `/auth/callback`
- `/onboarding/welcome`
- `/onboarding/consent-notice`
- `/onboarding/import`
- `/onboarding/review-import`
- `/onboarding/start-from-scratch`
- `/onboarding/choose-goal`
- `/workspace`

Actual route names can vary. The important point is the state separation, not the exact path strings.

## UX Requirements By Step

### Auth Entry

Must answer:

- what the product is
- where a new user starts
- where a returning user signs in

### Verification Pending

Must answer:

- what happened
- what the user must do next
- how to resend the email

### Welcome

Must answer:

- what happens in the next 1 to 2 minutes
- whether resume upload is optional
- what paths are available

### AI/Data Notice

Must answer:

- what content may be processed
- why it is processed
- what responsibility remains with the user

### Import Review

Must answer:

- what the parser extracted
- what may need correction
- what happens when the user confirms

## Failure States

Failure states that must be explicitly designed:

1. duplicate email signup attempt
2. weak or mismatched password
3. verification email not received
4. expired callback link
5. invalid or empty resume upload
6. parse failure
7. onboarding abandoned midway
8. user verified but has no profile and no onboarding completion

## First-Run Success Criteria

First-run experience is successful when the user can answer yes to these questions:

1. Do I know what this product is for?
2. Do I know what happened to my uploaded or entered data?
3. Do I know what to do next?
4. Do I already have something useful to work with?
