# REUSE_STRATEGY.md

Purpose: Define how USERJOURNEY should be treated as a reusable subsystem for future applications.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: Entire USERJOURNEY package
Authority: Canonical portability guidance for USERJOURNEY

---

## Short Answer

This should not be treated as a totally separate product, but it should be treated as a separate subsystem of the program.

The right mental model is:

1. core application
2. auth and identity layer
3. onboarding and consent subsystem
4. activated workspace or main product surface

That separation is what makes it reusable across future apps.

## Recommended Reusable Pattern

The reusable pattern is not `resume onboarding`. The reusable pattern is:

1. account creation
2. legal acceptance
3. contextual data-use disclosure
4. first-run orientation
5. optional guided setup with skip path
6. first value milestone
7. handoff to core application

Only steps 4 through 7 need app-specific customization.

## What Should Stay Generic Across Future Apps

1. milestone model: signup, verification, consent, onboarding, activation
2. decision log and open-questions process
3. route/state freeze discipline
4. implementation tracker and execution slices
5. legal review checklist structure
6. analytics funnel structure

## What Should Be Application-Specific

1. first-run path choices
2. first value definition
3. AI notice wording details
4. import or setup steps
5. activated workspace handoff

## Recommended Packaging Approach For Future Projects

If you want to reuse this in other apps, keep it as a planning framework with these portable files:

1. `PRODUCT_SPEC.md`
2. `USER_FLOWS.md`
3. `STATES_AND_RULES.md`
4. `LEGAL_AND_CONSENT.md`
5. `ACCEPTANCE_CRITERIA.md`
6. `IMPLEMENTATION_TRACKER.md`
7. `ROUTE_AND_STATE_FREEZE.md`
8. `DECISION_LOG.md`
9. `OPEN_QUESTIONS.md`

Then swap in app-specific documents for:

1. UX copy
2. legal drafts
3. first-run surfaces
4. activation criteria

## Architectural Recommendation

For this project and future ones, treat onboarding as a bounded subsystem with explicit handoff points.

That means:

1. it should not be buried inside a single main page component
2. it should not rely only on app-specific local UI state
3. it should have explicit entry, exit, and resume conditions

## Portability Benefits

If you keep it structured this way, future projects get:

1. faster product planning
2. fewer auth/onboarding mistakes
3. reusable legal and consent thinking
4. clearer activation analytics from the beginning
5. less drift between auth and first-run experience

## Recommendation For This Repo

Yes, treat USERJOURNEY as a distinct planning subsystem within the repo.

No, do not treat it as isolated from the main product.

The right relationship is:

- USERJOURNEY defines how users get into the product responsibly
- the core app defines what they do after activation
