# PRODUCT_SPEC.md

Purpose: Product specification for new-user signup, onboarding, consent, and first-run activation.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: USER_FLOWS.md, LEGAL_AND_CONSENT.md, STATES_AND_RULES.md
Authority: Canonical product spec for the new-user journey

---

## Product Problem

The application currently supports authentication, but the post-signup experience is underdefined. A new user can technically create an account, but there is no deliberate activation flow that explains what the product does, how resume and job-description data are handled, or what the user should do first.

This creates three risks:

1. weak first-run clarity
2. weak legal consent coverage for AI-assisted processing
3. weak activation because new users can fall into a generic workspace before reaching value

## Product Goal

Design a first-time user journey that moves a new account from signup to first value with minimal friction and explicit consent.

## Success Definition

A successful first-run journey means the user:

1. creates and verifies an account
2. accepts required legal terms
3. understands that resume and job-description content may be processed by AI-backed features
4. chooses an initial path
5. creates or imports a first resume profile
6. reaches a clear first value moment
7. lands in the workspace in an activated state

## Primary User Types

### User Type 1: Resume Improver

Has an existing resume and wants to improve it quickly.

### User Type 2: Job Tailorer

Has a resume and a specific job description and wants tailored output.

### User Type 3: From-Scratch Builder

Does not have a usable resume and wants guided help creating one.

## Core Product Principles

1. Signup is not activation.
2. Verification is not onboarding completion.
3. The first session must produce a useful artifact.
4. Legal consent must be explicit and versioned.
5. AI usage must be disclosed in context, not hidden only in legal pages.
6. Returning users should bypass onboarding and resume where they left off.

## Proposed Journey

### Stage 1: Entry

The auth entry should clearly present:

- sign in
- create account

The product promise should be outcome-oriented: improve, tailor, and build resumes.

### Stage 2: Account Creation

Required inputs:

- email
- password
- confirm password
- required agreement to Terms of Service and Privacy Policy

Optional input:

- marketing / product updates consent

### Stage 3: Verification

After signup, the user enters a waiting state:

- account exists
- email not yet verified
- onboarding not started or not completed

The user receives a verification email and can resend it.

### Stage 4: First Auth Callback Decision

After verification, the system routes based on account state.

If user is a first-time verified user with incomplete onboarding:

- route to onboarding welcome

If user is already onboarded:

- route to workspace

If callback fails:

- route to recovery state

### Stage 5: Welcome / Orientation

The app explains:

- what the product does
- what the next 1 to 2 minutes will look like
- that the user will either import a resume or create one

Primary choices:

- import existing resume
- start from scratch
- skip setup for now

### Stage 6: AI And Data Notice

Before the user uploads a resume or requests generation, present a clear disclosure:

- content may be stored in the account
- some features may send content to AI providers to analyze or transform it
- generated output must be reviewed by the user before use

This is product-level notice, not a substitute for legal acceptance.

### Stage 7A: Import Resume Path

User uploads supported file.

System behavior:

1. validate file
2. parse resume
3. present extracted content for review
4. ask user to confirm or correct parsed data
5. create initial profile

### Stage 7B: Start From Scratch Path

User provides a lightweight starter set:

- name
- current or target role
- years of experience
- optional links or summary

System behavior:

1. create starter profile
2. open guided editing mode
3. offer first-run suggestions

### Stage 7C: Skip Guided Onboarding Path

New users may choose to skip the guided onboarding flow.

This should not mean:

- skipping auth
- skipping required Terms and Privacy acceptance
- being treated as fully activated

Instead, skip should mean:

1. user is routed to a minimal workspace state
2. user sees a persistent `Complete setup` path
3. AI/data notice still blocks first upload or first generation if not yet acknowledged
4. activation is still incomplete until first value is achieved

### Stage 8: Intent Selection

After the first profile exists, the app asks what the user wants next:

- improve my resume
- tailor to a job description
- build a fresh version

This determines the first workspace emphasis.

### Stage 9: First Value Moment

The first session should end with at least one of the following:

- parsed and editable resume content
- a starter draft
- a tailored resume workflow started against a JD

Blank dashboards are failure states for first-run activation.

### Stage 10: Activated Workspace

Once the first value moment is achieved, the user enters the normal workspace with:

- saved primary profile
- autosave ready
- relevant CTA order for their selected path
- onboarding marked complete

## User Stories

1. As a new user, I want to know what this product does before I create an account.
2. As a new user, I want a simple signup form that does not ask for too much too early.
3. As a new user, I want to understand how my resume data will be used.
4. As a new user, I want to quickly import an existing resume and review the extracted content.
5. As a new user without a resume, I want the app to guide me through creating one from scratch.
6. As a returning user, I want to skip onboarding and go back to my workspace.
7. As the product owner, I want legal consent captured in a way that is explicit and versioned.
8. As the product owner, I want clear activation checkpoints so we can measure drop-off and improvement.

## Non-Goals

1. Do not turn signup into a long intake questionnaire.
2. Do not ask for all profile data before the user understands the product.
3. Do not send new users directly to a blank editor after verification.
4. Do not hide AI-processing disclosure only inside dense legal text.
5. Do not treat skipped onboarding as completed onboarding.

## Expected Outcomes

Expected product outcomes from this design:

1. better signup-to-activation conversion
2. fewer confused first-time users
3. stronger legal defensibility around consent and AI disclosure
4. cleaner distinction between verified users and activated users
5. better analytics around onboarding drop-off and feature adoption
