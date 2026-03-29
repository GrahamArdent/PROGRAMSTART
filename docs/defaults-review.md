# Defaults Review

This page records a review of which USERJOURNEY ideas should become PROGRAMBUILD defaults for all generated repos, and which should remain optional.

## Short Answer

Do not promote the full USERJOURNEY package into every generated repo.

Do promote several USERJOURNEY disciplines into PROGRAMBUILD as default thinking patterns for interactive products.

## Decision Frame

PROGRAMBUILD is the reusable core for all products, including services, automations, libraries, and internal systems.

USERJOURNEY is an optional attachment for products that have real end-user onboarding, consent, activation, and first-run routing complexity.

That means the question is not whether every USERJOURNEY file should become standard. The real question is which ideas deserve to become built-in defaults at the PROGRAMBUILD level.

## Promote Into PROGRAMBUILD As Default Patterns

### 1. Explicit Activation Checkpoint For Interactive Products

PROGRAMBUILD should always ask interactive products to define:

- what counts as onboarding complete
- what counts as first value
- what event marks activation

Reason:

- this sharpens requirements, analytics, routing, and test strategy early

Promotion target:

- kickoff guidance
- requirements prompts
- test-strategy expectations

### 2. Route/State Freeze Discipline

Interactive products should define major lifecycle states and transition rules before implementation expands.

Reason:

- this prevents auth, onboarding, callback handling, and workspace routing from drifting apart

Promotion target:

- PROGRAMBUILD requirements and architecture guidance for interactive apps

### 3. Consent And Policy-Version Questions

Interactive products that gather sensitive or AI-mediated inputs should define:

- required acceptance points
- policy-version handling
- resume behavior after interruption

Reason:

- these decisions are difficult to retrofit cleanly

Promotion target:

- requirements and release-readiness checklists

### 4. Resume-Point And Skip-State Semantics

Whenever a product has multi-step setup, PROGRAMBUILD should encourage defining:

- how interrupted flows resume
- whether skipped setup is equivalent to completion
- what the minimal allowed post-skip state is

Reason:

- teams otherwise blur partial setup and completed activation

Promotion target:

- requirements and user-flow review prompts

## Keep As Optional USERJOURNEY Attachment Assets

These files should remain optional and should not be copied into every generated repo by default:

- `USERJOURNEY/UX_COPY_DRAFT.md`
- `USERJOURNEY/SCREEN_INVENTORY.md`
- `USERJOURNEY/LEGAL_REVIEW_NOTES.md`
- `USERJOURNEY/TERMS_OF_SERVICE_DRAFT.md`
- `USERJOURNEY/PRIVACY_POLICY_DRAFT.md`
- `USERJOURNEY/EXECUTION_SLICES.md`
- `USERJOURNEY/FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md`
- `USERJOURNEY/IMPLEMENTATION_TRACKER.md`

Reason:

- these documents are high-value only when a product has a real end-user journey and the repo is carrying that work explicitly

## Keep As Optional But Strong Candidates For Interactive Products

These concepts are valuable enough that PROGRAMBUILD should reference them conditionally, but they still do not belong in every repo as full files:

- route and state freeze
- lifecycle state definitions
- activation event definition
- acceptance criteria tied to onboarding and activation
- analytics tied to activation rather than raw signup completion

The right model is conditional promotion of the concept, not unconditional copying of the USERJOURNEY file set.

## Recommended Platform Direction

PROGRAMSTART should keep the current structural split:

1. `PROGRAMBUILD/` stays universal
2. `USERJOURNEY/` stays optional

But future PROGRAMBUILD guidance should likely add a light interactive-product checkpoint that asks:

- does this product have a first-run journey
- does it require consent or policy acceptance
- does it need a defined activation milestone
- does it need a route/state freeze before implementation

## Conclusion

The right promotion is not "copy USERJOURNEY everywhere."

The right promotion is:

- bring the lifecycle discipline into PROGRAMBUILD
- keep the document-heavy onboarding package optional
- attach USERJOURNEY only when the product genuinely needs onboarding, consent, activation, or first-run routing design
