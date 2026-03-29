# ADDITIONAL_SUGGESTIONS.md

Purpose: Additional recommendations for keeping the USERJOURNEY work organized, actionable, and low-risk.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: Entire USERJOURNEY package
Authority: Advisory recommendations only

---

## Organizational Suggestions

1. Keep USERJOURNEY as the single home for onboarding, signup, consent, and activation decisions. Do not scatter follow-up notes into unrelated root markdown files.
2. When implementation starts, add one execution tracker here rather than mixing implementation tasks into the product spec itself.
3. Version legal drafts explicitly. For example, `TERMS_OF_SERVICE_DRAFT_v1.md` only if you later need parallel legal review variants.
4. When a decision is finalized, move it out of `OPEN_QUESTIONS.md` and into the canonical doc it affects.

## Product Suggestions

1. Decide early whether onboarding is a dedicated route flow or a workspace-embedded shell. That choice affects nearly everything else.
2. Keep import-first as the default recommendation unless research shows scratch users dominate the audience.
3. Treat "first value" as a hard product milestone, not a vague aspiration. If you cannot name the exact artifact produced, the onboarding flow is probably too loose.

## Legal And Trust Suggestions

1. Align product copy and policy text early so the signup surface does not overpromise anything the policy cannot support.
2. Add a short internal data-retention note before implementation. Privacy promises fail when retention behavior is undefined.
3. Be conservative in trust copy. Promise reviewability and control, not perfection.

## Implementation Suggestions

1. Before coding, freeze a small route map and state model in writing. Otherwise onboarding logic will sprawl into the existing root page.
2. Avoid using only client-side local state for legal acceptance or onboarding completion.
3. Plan testing before implementation. Callback branching and interrupted onboarding are exactly the sort of flows that regress silently.

## Documentation Suggestions

1. If implementation begins, create a `USERJOURNEY/IMPLEMENTATION_TRACKER.md` file instead of turning the spec docs into changelogs.
2. If design work begins, create a `USERJOURNEY/SCREEN_INVENTORY.md` file with one row per screen, state, owner, and status.
3. If legal review begins, create a `USERJOURNEY/LEGAL_REVIEW_NOTES.md` file so policy edits and unresolved concerns stay centralized.

## Best Next Steps

1. Resolve the open decisions that affect route structure and consent storage.
2. Review the legal drafts against actual operational behavior.
3. Convert the implementation plan into a scoped execution sequence before writing code.
