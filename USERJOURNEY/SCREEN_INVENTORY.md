# SCREEN_INVENTORY.md

Purpose: Canonical inventory of onboarding-related screens, states, and ownership.
Owner: Solo operator
Last updated: 2026-03-31
Depends on: UX_COPY_DRAFT.md, USER_FLOWS.md, ROUTE_AND_STATE_FREEZE.md
Authority: Canonical screen inventory for USERJOURNEY

---

## Inventory

| Surface | Purpose | Audience | State Trigger | Primary Outcome | Owner | Status |
|---|---|---|---|---|---|---|
| Auth Entry | choose sign in vs create account | anonymous | no session | user selects path | Product / Design | Planned |
| Signup | create account and capture required consent | new user | signup selected | account created | Product / Frontend | Planned |
| Verification Pending | instruct user to verify email | unverified user | signup success | verification email acted on | Product / Frontend | Planned |
| Verification Recovery | recover from bad callback link | new or returning user | callback failure | resend or recover auth | Product / Frontend | Planned |
| Onboarding Welcome | orient user to first-run journey | first-time verified user | verified and not onboarded | initial path selected | Product / Design | Planned |
| AI/Data Notice | disclose data and AI processing | first-run user | before upload or generation | informed continuation | Product / Legal | Planned |
| Import Resume | collect resume file | import-path user | import selected | file uploaded | Frontend | Planned |
| Import Review | confirm extracted content | import-path user | parse success | initial profile confirmed | Frontend / Product | Planned |
| Start From Scratch | create starter profile | scratch-path user | scratch selected | starter profile created | Frontend | Existing capability, needs adaptation |
| Minimal Workspace (Skipped Onboarding) | allow low-friction entry without false activation | first-run user who skipped setup | skip selected | user can work, but still sees incomplete-state recovery | Product / Frontend | Planned |
| Choose First Goal | set initial intent | first-run user with profile | profile exists, not activated | workspace emphasis chosen | Product | Planned |
| Activated Dashboard | show next steps for onboarded user | activated user | onboarding complete | user continues in workspace | Product / Frontend | Existing surface, needs adaptation |
| Activated Editor | editing workspace | activated user | resume workspace entered | user edits or tailors content | Frontend | Existing |

## Notes On Existing Surface Reuse

### Existing And Reusable

1. signup page structure exists
2. login page structure exists
3. callback route exists
4. start-from-scratch flow exists as a modal capability
5. dashboard and editor shell exist

### Existing But Not Ready As-Is

1. existing builder modal is not yet a dedicated onboarding surface
2. current dashboard is for activated or near-activated users, not first-run orientation
3. current root workspace route assumes auth implies workspace entry
4. current workspace shell does not yet define an explicit unactivated skip state

## Additional Surface Rules

1. The minimal workspace must keep a persistent, high-visibility `Complete setup` action until activation.
2. Target role collection should happen after import review or starter profile creation, not on the welcome screen for import-first users.
3. The operator dashboard in this template repo is not a substitute for the end-user onboarding surface family.
4. Route-shaped onboarding outcomes are not considered implemented until the corresponding end-user surfaces exist in product code.

## Screen Discipline Rules

1. Each named state should have one primary surface.
2. Avoid splitting one state across multiple hidden modal layers.
3. Avoid making onboarding depend on dashboard tab assumptions.
4. Do not invent extra first-run screens unless they reduce risk or confusion.
