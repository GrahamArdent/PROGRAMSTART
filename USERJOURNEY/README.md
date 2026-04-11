# USERJOURNEY

Purpose: Canonical index for the new-user journey, signup, onboarding, and consent design.
Owner: Solo operator
Last updated: 2026-03-31
Depends on: Existing auth flow, workspace routing, product goals
Authority: Canonical index for the USERJOURNEY folder

---

## Goal

Define the intended journey for new users from account creation through first value, without implementation details.

## Attachment Status

This folder is a project-specific example attachment kept in the template repository for reference. It is not part of the reusable PROGRAMBUILD template system and should not be copied into every project by default.

Attach a USERJOURNEY package only when the product includes real end-user onboarding, consent, activation, or first-run routing work.

## What This Folder Contains

- `PRODUCT_SPEC.md` — complete product spec for signup, onboarding, and activation
- `USER_FLOWS.md` — screen-by-screen user journeys and route transitions
- `UX_COPY_DRAFT.md` — screen-by-screen UX and microcopy draft for the first-run journey
- `LEGAL_AND_CONSENT.md` — Terms, Privacy, AI notice, and consent requirements
- `EXTERNAL_REVIEW_PACKET.md` — review-ready packet for the remaining legal and operational approvals
- `IMPLEMENTATION_PLAN.md` — non-code implementation mapping, risks, and sequencing
- `IMPLEMENTATION_TRACKER.md` — phased execution tracker with risks, owners, and impacted files
- `EXECUTION_SLICES.md` — concrete implementation slices and test scope before coding begins
- `FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md` — file-level execution checklist for the current repo
- `DELIVERY_GAMEPLAN.md` — synced execution and change-control gameplan using the full USERJOURNEY package
- `SCREEN_INVENTORY.md` — canonical inventory of onboarding-related screens and states
- `ROUTE_AND_STATE_FREEZE.md` — proposed route map and state model frozen for implementation planning
- `LEGAL_REVIEW_NOTES.md` — legal review checklist, issues, and follow-up notes
- `STATES_AND_RULES.md` — lifecycle states, routing logic, and system rules
- `ACCEPTANCE_CRITERIA.md` — testable requirements for product, UX, and routing behavior
- `ANALYTICS_AND_OUTCOMES.md` — expected business outcomes, analytics events, and success metrics
- `TERMS_OF_SERVICE_DRAFT.md` — first draft of product-tailored Terms of Service
- `PRIVACY_POLICY_DRAFT.md` — first draft of product-tailored Privacy Policy
- `ADDITIONAL_SUGGESTIONS.md` — organizational and product recommendations beyond the current scope
- `REUSE_STRATEGY.md` — guidance for evaluating whether this attachment pattern is worth reusing in future projects
- `USERJOURNEY_TEMPLATE_STARTER.md` — portable starter reference if a future project truly needs this attachment type
- `DECISION_LOG.md` — canonical record of resolved onboarding and consent decisions
- `OPEN_QUESTIONS.md` — decisions still requiring product or legal owner input

## Scope

In scope:

- account creation
- email verification
- new-user onboarding
- consent capture
- first-run routing
- first value moment
- analytics and activation outcomes

Out of scope:

- visual design implementation
- frontend or backend code changes
- billing and subscription flows
- enterprise SSO

## Product Summary

The current app already supports login, signup, and auth callback handling in the existing product surface. The missing layer is the intentional first-time user journey and the legal/consent structure around resume uploads, job-description processing, and AI-assisted suggestions.

## Intended Outcome

New users should not verify their email and land in a generic workspace. They should move through a defined activation path that:

1. captures required consent
2. explains AI and data handling in plain language
3. gets the user to import or create a resume
4. produces a first meaningful artifact quickly
5. then hands off to the normal workspace experience

## Planning Discipline

This package should work for a mostly solo builder. The docs split product, UX, legal, route/state, and implementation concerns for clarity and drift control, not because separate specialists are required on every project.

When implementation starts:

1. treat `ROUTE_AND_STATE_FREEZE.md` as the routing baseline unless a decision is explicitly changed
2. record resolved decisions in `DECISION_LOG.md`
3. track progress and ownership in `IMPLEMENTATION_TRACKER.md`
4. keep unresolved issues in `OPEN_QUESTIONS.md`
5. use `DELIVERY_GAMEPLAN.md` as the cross-document sync and execution order reference
6. use `EXTERNAL_REVIEW_PACKET.md` when the remaining blockers need to be handed to counsel or operations as a decision package
