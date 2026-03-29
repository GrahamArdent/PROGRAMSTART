# FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md

Purpose: File-level, non-code implementation checklist for onboarding and consent work in the current repo.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: EXECUTION_SLICES.md, IMPLEMENTATION_PLAN.md, ROUTE_AND_STATE_FREEZE.md
Authority: Canonical file-level implementation planning checklist for this repo

---

## How To Use This File

1. Use this after decisions are frozen and before code changes begin.
2. Treat each file below as a review checkpoint, not an automatic change list.
3. If a file is marked `Validate before changing`, read it carefully and confirm the change really belongs there.

## Critical Mapping Note

This checklist is intentionally conservative. It names files that are likely to be involved, but it avoids pretending every file listed must change. The current app has overlapping responsibilities in the root workspace entry and builder flow, so careless expansion there is a real risk.

## Frontend Auth And Entry Files

### `v6_clean_repo_candidate/v6_nextjs_migration/frontend/app/auth/login/page.tsx`

Status: Likely change

Checklist:

1. confirm entry messaging matches new auth + activation model
2. confirm returning-user emphasis remains clear
3. confirm links and recovery behavior stay aligned with signup and callback states

### `v6_clean_repo_candidate/v6_nextjs_migration/frontend/app/auth/signup/page.tsx`

Status: Likely change

Checklist:

1. add required legal acceptance contract at planning level
2. define verification-pending handoff cleanly
3. avoid turning signup into a long intake form

### `v6_clean_repo_candidate/v6_nextjs_migration/frontend/app/auth/callback/route.ts`

Status: High-risk change

Checklist:

1. define branch behavior for activated, not-onboarded, and skipped-onboarding users
2. define recovery behavior for failure states
3. ensure callback is not treated as a simple redirect-only mechanism anymore

## Frontend Session And Routing Files

### `v6_clean_repo_candidate/v6_nextjs_migration/frontend/lib/auth-context.tsx`

Status: Likely change

Checklist:

1. define what additional onboarding and consent metadata the frontend needs
2. avoid bloating this context into a full workflow engine
3. keep session state and onboarding state responsibilities explicit

### `v6_clean_repo_candidate/v6_nextjs_migration/frontend/app/page.tsx`

Status: Validate before changing

Checklist:

1. confirm whether this should remain activated-workspace entry only
2. do not automatically expand this into the onboarding router
3. if touched at all, prefer narrowing responsibilities rather than adding more branching

Critical warning:

This file is already overloaded. Treat it as a high-risk integration point, not the default place to add onboarding logic.

## Frontend Existing Workspace Surfaces

### `v6_clean_repo_candidate/v6_nextjs_migration/frontend/components/dashboard/DashboardHome.tsx`

Status: Possible change

Checklist:

1. define whether it supports a minimal skip-state workspace variant
2. ensure it can present incomplete-state next actions without pretending the user is activated

### `v6_clean_repo_candidate/v6_nextjs_migration/frontend/components/dashboard/Sidebar.tsx`

Status: Possible change

Checklist:

1. define whether skip-state users need different nav treatment
2. avoid exposing activated-only assumptions in the skipped-onboarding state

## Frontend Builder And Profile Flow Files

### `v6_clean_repo_candidate/v6_nextjs_migration/frontend/components/builder/StartFromScratchModal.tsx`

Status: High-interest, high-risk reuse candidate

Checklist:

1. identify what business flow can be reused
2. separate reusable creation logic from modal-specific assumptions
3. do not assume the current modal presentation is acceptable for first-run onboarding

### `v6_clean_repo_candidate/v6_nextjs_migration/frontend/lib/profilesApi.ts`

Status: Likely review

Checklist:

1. confirm current profile creation and save contracts support first-run paths
2. confirm no false assumption that profile existence equals activation

## Backend And Persistence Files

### `v6_clean_repo_candidate/v6_nextjs_migration/backend/app/routes/profiles.py`

Status: Likely review

Checklist:

1. identify what onboarding-related profile creation metadata may eventually need support
2. confirm profile creation contract is compatible with import and scratch onboarding paths

### `v6_clean_repo_candidate/v6_nextjs_migration/backend/app/supabase_client.py`

Status: Likely review

Checklist:

1. identify where consent and onboarding metadata would conceptually live if persisted with account-adjacent data
2. confirm deletion/export language in planning remains consistent with actual supported operations

## New Planned Surface Areas

These are not current files, but they are planned responsibilities that likely deserve dedicated ownership rather than expansion of existing god files.

1. onboarding route entry / welcome surface
2. AI/data notice surface
3. import review surface
4. skip-state workspace treatment
5. onboarding metadata fetch / guard layer

## Slice Mapping

| Slice | Primary Files To Review First |
|---|---|
| Slice 1 | `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md`, `USERJOURNEY/DECISION_LOG.md` |
| Slice 2 | `frontend/app/auth/login/page.tsx`, `frontend/app/auth/signup/page.tsx` |
| Slice 3 | `frontend/app/auth/callback/route.ts`, `frontend/lib/auth-context.tsx`, `frontend/app/page.tsx` |
| Slice 4 | onboarding welcome surface, `DashboardHome.tsx`, `Sidebar.tsx` |
| Slice 5 | onboarding notice surface, auth/onboarding state layer |
| Slice 6 | import surfaces, `profilesApi.ts`, `profiles.py` |
| Slice 7 | `StartFromScratchModal.tsx`, `profilesApi.ts`, `profiles.py` |
| Slice 8 | goal-selection surface, dashboard/editor handoff |
| Slice 9 | analytics layer, policy-version handling surfaces |

## Final Review Rule

Before code starts, walk this checklist against the current codebase and explicitly decide which listed files are:

1. must change
2. should probably change
3. should be protected from further growth
