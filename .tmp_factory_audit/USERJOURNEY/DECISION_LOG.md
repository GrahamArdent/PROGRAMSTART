# DECISION_LOG.md

Purpose: Canonical log of resolved product decisions for the new-user journey.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: PRODUCT_SPEC.md, ROUTE_AND_STATE_FREEZE.md
Authority: Canonical resolved-decision record for USERJOURNEY

---

## How To Use This File

1. Record only resolved decisions here.
2. Keep unresolved items in `OPEN_QUESTIONS.md`.
3. When a decision changes, update the prior entry instead of creating contradictory notes.
4. For a mostly solo workflow, keep decisions here unless the change is cross-system or expensive enough that it needs a fuller ADR in PROGRAMBUILD.

## Current Decisions

| Date | Decision | Reason | Affects |
|---|---|---|---|
| 2026-03-27 | Treat signup, verification, onboarding, and activation as separate milestones | avoids false activation and routing ambiguity | product spec, analytics, routing |
| 2026-03-27 | Keep Terms and Privacy acceptance required at signup | legal baseline for account creation | signup UX, consent state |
| 2026-03-27 | Show AI/data notice before first upload or first generation | contextual disclosure improves trust and defensibility | onboarding UX, consent state |
| 2026-03-27 | Do not send newly verified first-time users directly to the normal workspace | first-run users need deliberate activation flow | callback and route model |
| 2026-03-27 | Treat first value moment as a required activation milestone | prevents empty-workspace false activation | analytics, workspace handoff |
| 2026-03-27 | Use a dedicated onboarding route family separate from the activated workspace | current root workspace entry is already too overloaded to be the primary onboarding router | routing, implementation plan, execution slicing |
| 2026-03-27 | Require account creation before resume upload | keeps consent, persistence, and ownership state coherent from the first user action | product flow, legal, auth |
| 2026-03-27 | Use import-first as the recommended primary CTA for first-run users | fastest path to value for the current product shape | onboarding UX, activation |
| 2026-03-27 | Allow users to skip guided onboarding, but not skip required auth or legal consent | reduces friction without losing control of consent and activation state | onboarding UX, state model |
| 2026-03-27 | Skipping onboarding routes the user into a minimal unactivated workspace state, not the full activated experience | avoids false activation while preserving flexibility | workspace handoff, activation logic |
| 2026-03-27 | Do not auto-create an empty default profile before import or scratch flow produces meaningful data | avoids ambiguous state and weak activation metrics | profile creation, analytics |
| 2026-03-27 | Job-description tailoring should not start before import review is complete | imported data quality must be confirmed before tailoring depends on it | import flow, tailoring flow |
| 2026-03-27 | Canonical onboarding event taxonomy is the funnel defined in ANALYTICS_AND_OUTCOMES.md | reduces analytics drift | analytics implementation |
| 2026-03-27 | Target first value should be median <= 3 minutes and p75 <= 5 minutes for first session | forces the onboarding design to stay lean and outcome-focused | product KPIs, analytics |
| 2026-03-27 | The minimal skip-state workspace should be dashboard-first, not editor-first | a blank or half-configured editor is a worse false-start for skipped users; dashboard-first can show incomplete-state guidance and clear recovery actions | skip-state UX, workspace handoff |
| 2026-03-27 | USERJOURNEY should be extracted as a reusable planning subsystem pattern for future apps | the milestone/state/consent framework is portable even when the product-specific first-value flow changes | reuse strategy, PROGRAMSTART export |
| 2026-03-27 | Do not add a separate read-only explore mode in the first release | skip-onboarding already provides the low-friction bypass; an additional explore mode would create another ambiguous activation state | onboarding scope, routing |
| 2026-03-27 | Name the first profile after the first meaningful artifact exists, not during initial signup | reduces front-loaded friction and avoids asking users to label an empty shell | onboarding UX, profile creation |
| 2026-03-27 | AI/data notice should block only the first upload or generation trigger; later reminders are informational unless policy state changes require a new gate | keeps disclosure contextual without repeatedly interrupting normal use | notice UX, consent gating |
| 2026-03-27 | Re-acceptance should be forced only after material Terms or Privacy changes | avoids unnecessary friction while preserving defensible consent refresh behavior | policy version handling, legal UX |
| 2026-03-27 | Target role should be collected after import review or starter profile creation, not on the initial welcome screen for import users | preserves import-first speed to value and keeps the welcome step lightweight | onboarding flow, goal selection |
| 2026-03-27 | The minimal workspace must keep a persistent, high-visibility `Complete setup` recovery CTA until activation | skip must remain recoverable and visibly incomplete | skip-state UX, dashboard, sidebar |
| 2026-03-27 | Skip-state users should see the AI/data notice at the first upload or generation trigger, not on bare workspace entry | matches the contextual notice rule and avoids front-loading another interstitial after skip | skip-state UX, consent gating |
| 2026-03-27 | `first_value_achieved` is the canonical activation event for reporting; `workspace_activated` is a downstream handoff event | ties activation to real user value rather than a route transition | analytics, dashboards |
| 2026-03-27 | Skip-onboarding users should be tracked as a separate funnel variant from guided users | measures whether skip reduces friction or only hides abandonment later | analytics, experimentation |
| 2026-03-27 | Trigger onboarding review when any step loses 20% or more of its entrants over a meaningful sample window | gives the team an explicit threshold for funnel intervention instead of subjective judgment | analytics operations, product review |
| 2026-03-27 | Until retention operations are explicitly validated, public docs should avoid numeric retention promises | prevents policy text from overcommitting beyond verified operations | privacy policy, legal review |

## Pending Decisions Not Yet Resolved

Refer to `OPEN_QUESTIONS.md` for unresolved items.
