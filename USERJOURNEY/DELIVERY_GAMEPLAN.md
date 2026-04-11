# DELIVERY_GAMEPLAN

Purpose: Provide the implementation-ready gameplan that keeps USERJOURNEY decisions, docs, and code-touch planning synchronized.
Owner: Solo operator
Last updated: 2026-03-31
Depends on: README.md, DECISION_LOG.md, ROUTE_AND_STATE_FREEZE.md, IMPLEMENTATION_TRACKER.md, EXECUTION_SLICES.md, FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md
Authority: Canonical cross-document execution and sync guide for USERJOURNEY

---

## Goal

Move from planning to implementation without letting route logic, legal copy, analytics, and file-level execution drift apart.

This is written to support a mostly solo builder. References to UX, legal, or engineering concerns are concern buckets to keep the docs coherent, not a requirement for separate team roles.

This document is the operating layer that ties together:

1. the product and legal requirements
2. the route and state model
3. the execution slices
4. the actual repo files likely to be touched
5. the rules for keeping every related document synchronized

## Current Planning Status

The USERJOURNEY package is now in a good pre-implementation state:

1. product, UX, consent, and analytics defaults are frozen in `DECISION_LOG.md`
2. route and state separation is frozen in `ROUTE_AND_STATE_FREEZE.md`
3. implementation slicing exists in `EXECUTION_SLICES.md`
4. file-level review targets exist in `FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md`
5. the remaining unresolved items are legal or operational approvals in `OPEN_QUESTIONS.md`

That means implementation can proceed in a controlled way as long as legal and operational unknowns are not silently invented in code or public copy.

## Source Of Truth Matrix

Use the following authority chain whenever something changes.

| Concern | Source Of Truth | Supporting Files | When To Update |
|---|---|---|---|
| product goals and first-run promise | `PRODUCT_SPEC.md` | `USER_FLOWS.md`, `UX_COPY_DRAFT.md` | when the user journey itself changes |
| resolved defaults and product decisions | `DECISION_LOG.md` | `OPEN_QUESTIONS.md` | when a decision is made or reversed |
| unresolved or externally blocked items | `OPEN_QUESTIONS.md` | `LEGAL_REVIEW_NOTES.md` | when a decision cannot yet be finalized |
| route structure and state boundaries | `ROUTE_AND_STATE_FREEZE.md` | `STATES_AND_RULES.md`, `USER_FLOWS.md` | before any routing implementation changes |
| lifecycle semantics and activation rules | `STATES_AND_RULES.md` | `ACCEPTANCE_CRITERIA.md`, `ANALYTICS_AND_OUTCOMES.md` | when milestone meaning changes |
| legal and consent requirements | `LEGAL_AND_CONSENT.md` | `TERMS_OF_SERVICE_DRAFT.md`, `PRIVACY_POLICY_DRAFT.md`, `LEGAL_REVIEW_NOTES.md` | when policy or disclosure behavior changes |
| UX surfaces and copy | `SCREEN_INVENTORY.md` and `UX_COPY_DRAFT.md` | `USER_FLOWS.md` | when a surface is added, removed, or repurposed |
| measurable outcomes and funnel logic | `ANALYTICS_AND_OUTCOMES.md` | `ACCEPTANCE_CRITERIA.md` | when event taxonomy or activation criteria change |
| implementation order, slice readiness, and risk control | `IMPLEMENTATION_TRACKER.md` and `EXECUTION_SLICES.md` | `FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md` | when the build sequence, current slice focus, or ownership changes |
| code-touch planning for this repo | `FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md` | `IMPLEMENTATION_PLAN.md` | before engineering starts a slice |

## Operating Rule

Do not update code-planning documents independently. If one of the concerns above changes, update the authority file first and then its dependent files in the same session.

## Detailed Delivery Sequence

### Step 1: Close Remaining External Decisions

Primary docs:

1. `OPEN_QUESTIONS.md`
2. `LEGAL_REVIEW_NOTES.md`
3. `EXTERNAL_REVIEW_PACKET.md`
4. `TERMS_OF_SERVICE_DRAFT.md`
5. `PRIVACY_POLICY_DRAFT.md`

Outcome:

1. governing law decided
2. liability wording approved
3. retention language aligned with verified operations
4. published support and privacy contact path defined

Rule:

Do not let implementation invent legal text that is not reflected in these docs.

Use `EXTERNAL_REVIEW_PACKET.md` when asking counsel or operations to decide the remaining blocked items. It is the review-ready framing layer, not the source of truth.

### Step 2: Freeze The Execution Baseline

Primary docs:

1. `DECISION_LOG.md`
2. `ROUTE_AND_STATE_FREEZE.md`
3. `STATES_AND_RULES.md`
4. `ACCEPTANCE_CRITERIA.md`

Outcome:

1. no ambiguity about activated vs unactivated skip-state behavior
2. no ambiguity about when consent gates appear
3. no ambiguity about the canonical activation event

Rule:

If an engineer proposes a route or state change, update these files before implementation continues.

### Step 3: Prepare UI Surface Ownership

Primary docs:

1. `SCREEN_INVENTORY.md`
2. `UX_COPY_DRAFT.md`
3. `USER_FLOWS.md`

Primary repo files to inspect first:

1. `frontend/app/auth/login/page.tsx`
2. `frontend/app/auth/signup/page.tsx`
3. dashboard home surface
4. workspace navigation surface
5. `frontend/components/builder/StartFromScratchModal.tsx`

Outcome:

1. each onboarding state has one primary screen owner
2. the skip-state workspace has explicit incomplete-state treatment
3. builder reuse is limited to flow logic, not blindly to modal presentation

For solo use:

Treat this step as a surface review pass, not a designer handoff.

### Step 4: Prepare Auth, Callback, And Metadata Ownership

Primary docs:

1. `IMPLEMENTATION_PLAN.md`
2. `FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md`
3. `LEGAL_AND_CONSENT.md`
4. `ROUTE_AND_STATE_FREEZE.md`

Primary repo files to inspect first:

1. `frontend/app/auth/callback/route.ts`
2. `frontend/lib/auth-context.tsx`
3. `frontend/app/page.tsx`
4. `backend/app/routes/profiles.py`
5. backend account metadata client

Outcome:

1. callback branching logic has a defined source of truth
2. onboarding and consent metadata needs are explicit
3. `app/page.tsx` is protected from becoming the onboarding router

### Step 5: Execute By Slices, Not By File Grab-Bag

Use `EXECUTION_SLICES.md` as the build order authority and `FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md` as the file review companion.
Use `IMPLEMENTATION_TRACKER.md` as the current slice readiness and execution-status snapshot.

Ordered sequence:

1. Slice 1: Consent and state model freeze
2. Slice 2: Auth entry and signup contract
3. Slice 3: Callback branching and route guards
4. Slice 4: Onboarding welcome and skip path
5. Slice 5: AI notice gating
6. Slice 6: Import resume first-run flow
7. Slice 7: Start-from-scratch first-run flow
8. Slice 8: Goal selection and first value handoff
9. Slice 9: Analytics and policy-version handling

Rule:

Do not start Slice 6 or Slice 7 until Slice 3 and Slice 5 are structurally clear. Otherwise first-run upload/generation behavior will drift away from consent gates.

### Step 6: Verify Against Acceptance, Not Intuition

Primary docs:

1. `ACCEPTANCE_CRITERIA.md`
2. `ANALYTICS_AND_OUTCOMES.md`
3. `IMPLEMENTATION_TRACKER.md`

Outcome:

1. each slice has explicit verification targets
2. activation is measured as `first_value_achieved`
3. skip-state behavior is measured separately from guided onboarding

## Repo File Mapping By Slice

| Slice | First Docs To Open | First Repo Files To Review | Main Risk |
|---|---|---|---|
| 1 | `DECISION_LOG.md`, `ROUTE_AND_STATE_FREEZE.md`, `STATES_AND_RULES.md` | none before freeze is explicit | building UI on unstable semantics |
| 2 | `LEGAL_AND_CONSENT.md`, `UX_COPY_DRAFT.md`, `ACCEPTANCE_CRITERIA.md` | `frontend/app/auth/login/page.tsx`, `frontend/app/auth/signup/page.tsx` | signup expands into intake clutter |
| 3 | `ROUTE_AND_STATE_FREEZE.md`, `IMPLEMENTATION_PLAN.md`, `FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md` | `frontend/app/auth/callback/route.ts`, `frontend/lib/auth-context.tsx`, `frontend/app/page.tsx` | returning-user or workspace routing regression |
| 4 | `SCREEN_INVENTORY.md`, `USER_FLOWS.md`, `UX_COPY_DRAFT.md` | onboarding route surfaces, `DashboardHome.tsx`, `Sidebar.tsx` | skip-state looks fully activated |
| 5 | `LEGAL_AND_CONSENT.md`, `STATES_AND_RULES.md` | notice surface, auth or onboarding metadata layer | disclosure becomes decorative instead of enforced |
| 6 | `USER_FLOWS.md`, `ACCEPTANCE_CRITERIA.md` | import surfaces, `frontend/lib/profilesApi.ts`, `backend/app/routes/profiles.py` | parse review gets skipped and creates low-quality profiles |
| 7 | `IMPLEMENTATION_PLAN.md`, `SCREEN_INVENTORY.md` | `StartFromScratchModal.tsx`, `profilesApi.ts`, `profiles.py` | modal semantics leak into first-run onboarding |
| 8 | `PRODUCT_SPEC.md`, `ANALYTICS_AND_OUTCOMES.md` | goal-selection surface, workspace handoff surfaces | first-value event is logged too early |
| 9 | `ANALYTICS_AND_OUTCOMES.md`, `LEGAL_REVIEW_NOTES.md` | analytics layer, policy-version handling surfaces | events and legal state diverge |

## Sync Rules

### If Route Or State Logic Changes

Update in this order:

1. `DECISION_LOG.md`
2. `ROUTE_AND_STATE_FREEZE.md`
3. `STATES_AND_RULES.md`
4. `USER_FLOWS.md`
5. `SCREEN_INVENTORY.md`
6. `IMPLEMENTATION_PLAN.md`
7. `IMPLEMENTATION_TRACKER.md`

### If Legal Or Consent Behavior Changes

Update in this order:

1. `DECISION_LOG.md` if the behavior itself changed
2. `LEGAL_AND_CONSENT.md`
3. `TERMS_OF_SERVICE_DRAFT.md`
4. `PRIVACY_POLICY_DRAFT.md`
5. `LEGAL_REVIEW_NOTES.md`
6. `UX_COPY_DRAFT.md`
7. `ACCEPTANCE_CRITERIA.md`

### If UX Surfaces Or Copy Change

Update in this order:

1. `SCREEN_INVENTORY.md`
2. `USER_FLOWS.md`
3. `UX_COPY_DRAFT.md`
4. `ACCEPTANCE_CRITERIA.md`
5. `ANALYTICS_AND_OUTCOMES.md` if event points move

### If Implementation Sequence Changes

Update in this order:

1. `IMPLEMENTATION_TRACKER.md`
2. `EXECUTION_SLICES.md`
3. `FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md`
4. `DELIVERY_GAMEPLAN.md`

## Anti-Drift Rules

1. Do not let `app/page.tsx` become the default place to absorb onboarding changes.
2. Do not add new first-run screens without updating `SCREEN_INVENTORY.md` first.
3. Do not log activation at route entry alone; activation is `first_value_achieved`.
4. Do not treat profile existence alone as proof of onboarding completion.
5. Do not promise retention durations or deletion capabilities beyond verified operations.
6. Do not let skip-state UX hide the fact that setup is incomplete.

## Definition Of Ready For Engineering

In a solo workflow, this means ready for implementation by the same person, not ready for another team handoff.

Engineering should treat onboarding work as ready when all of the following are true:

1. `OPEN_QUESTIONS.md` contains only true external approvals or has been cleared
2. `DECISION_LOG.md` and `ROUTE_AND_STATE_FREEZE.md` match each other
3. `SCREEN_INVENTORY.md`, `USER_FLOWS.md`, and `UX_COPY_DRAFT.md` describe the same surfaces
4. `ANALYTICS_AND_OUTCOMES.md` and `ACCEPTANCE_CRITERIA.md` agree on activation and funnel checkpoints
5. the slice being started has a clear first file review path in `FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md`

## Definition Of Done For The Planning Package

This planning package is considered internally synchronized when:

1. no resolved item remains listed as open
2. no route or state rule is contradicted across files
3. no legal UX promise exceeds what legal review notes say is supportable
4. the execution tracker, execution slices, and file checklist describe the same build order
5. this gameplan still matches the actual authority chain in the folder
