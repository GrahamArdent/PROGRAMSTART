# USERJOURNEY_TEMPLATE_STARTER.md

Purpose: Portable starter template for reusing the USERJOURNEY planning subsystem in future applications.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: REUSE_STRATEGY.md
Authority: Portable template seed for future projects

---

## What This Is

This is a generic starter for planning signup, onboarding, consent, and activation in a new product.

It is designed to be copied into a new project and adapted quickly.

## Core Principle

Treat onboarding as a bounded subsystem with explicit entry, exit, resume, and activation rules.

## Recommended Starter Files

1. `PRODUCT_SPEC.md`
2. `USER_FLOWS.md`
3. `STATES_AND_RULES.md`
4. `LEGAL_AND_CONSENT.md`
5. `ACCEPTANCE_CRITERIA.md`
6. `IMPLEMENTATION_PLAN.md`
7. `IMPLEMENTATION_TRACKER.md`
8. `EXECUTION_SLICES.md`
9. `SCREEN_INVENTORY.md`
10. `ROUTE_AND_STATE_FREEZE.md`
11. `DECISION_LOG.md`
12. `OPEN_QUESTIONS.md`
13. `REUSE_STRATEGY.md`

## Reusable Milestone Model

Use these milestones unless the new product has a strong reason not to:

1. account created
2. email verified
3. legal acceptance complete
4. contextual data-use notice acknowledged
5. guided onboarding completed or skipped
6. first artifact created
7. first value achieved
8. activated user state

## Reusable Open Questions

1. What is the first value moment in this product?
2. Should account creation happen before the first meaningful user input?
3. What legal consent is required at signup?
4. What contextual notice is required before sensitive actions?
5. Is guided onboarding skippable?
6. If skipped, what is the minimal unactivated workspace state?
7. What marks activation?

## Reusable Anti-Patterns

Do not:

1. treat authentication as activation
2. hide legal acceptance only in footer links
3. store consent state only in client local storage
4. infer all onboarding state from one product data object
5. route skipped users into the same experience as fully activated users without distinction

## Reusable Decision Defaults

If no product-specific reason exists otherwise, default to:

1. required Terms and Privacy acceptance at signup
2. contextual AI or data notice before first sensitive processing action
3. separate onboarding routes from the activated workspace
4. import or fast-start path as the primary CTA for first-run users
5. skip-guided-onboarding allowed, but not treated as activation

## How To Adapt For A New App

Replace these product-specific elements:

1. what is being created or imported
2. what counts as first value
3. which sensitive data needs contextual disclosure
4. what the activated workspace or core app surface is

Keep these structural elements:

1. milestones
2. decision log
3. route and state freeze
4. execution slices
5. legal review notes
