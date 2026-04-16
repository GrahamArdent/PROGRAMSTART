---
status: accepted
date: 2026-04-15
deciders: [Solo operator]
consulted: []
informed: []
---

# 0011. Separate workflow and operator prompt architecture

<!-- DEC-008 -->

## Context and Problem Statement

PROGRAMSTART currently mixes product workflow prompts, PROGRAMSTART maintenance prompts, and internal build prompts under one broad prompt model. In practice this causes route-facing workflow semantics, prompt registration, prompt standards, and compliance validation to bleed into prompts that are not part of stage or phase progression. Because future generated programs will build from this repository, leaving that ambiguity in place would propagate the same structural confusion downstream.

## Decision Drivers

- Future generated programs must not inherit PROGRAMSTART maintenance behavior by accident.
- Workflow routing must remain explicit and limited to workflow control surfaces.
- Prompt standards should reflect actual prompt purpose rather than a one-size-fits-all template.
- Validation must mechanically enforce prompt boundaries instead of relying on convention.
- `devlog/` gameplans must remain non-canonical execution artifacts.

## Considered Options

- Option A — Keep one universal prompt model and add more exceptions for maintenance prompts.
- Option B — Split prompt architecture into explicit workflow, operator, and internal classes with class-aware standards, registry placement, and validation.
- Option C — Move maintenance prompts out of the main prompt set without changing standards or registry semantics.

## Decision Outcome

Chosen option: **Option B**, because it fixes the root cause instead of masking it with exemptions. PROGRAMSTART will treat prompt class, routing eligibility, registry placement, and validation semantics as explicit architectural concerns.

### Approved Decisions

1. **Prompt taxonomy is an explicit architecture rule.**
   PROGRAMSTART defines three prompt classes: `workflow`, `operator`, and `internal`.

2. **Workflow routing applies only to workflow prompts.**
   Only `workflow` prompts may participate in stage or phase progression semantics, including workflow-routing next steps and stage-transition guidance.

3. **Prompt discoverability is separate from workflow routing.**
   Registry structures MUST distinguish between prompts that are discoverable and prompts that are part of workflow guidance or routing.

4. **Workflow prompts and operator prompts use separate standards.**
   The current shaping-prompt standard remains the workflow standard. Operator prompts must use a dedicated standard that requires truth hierarchy, pre-flight baseline, resumption protocol, execution loop, stop conditions, verification, and checkpoint semantics without inheriting workflow-routing requirements.

5. **`devlog/` gameplans remain non-canonical.**
   Gameplans in `devlog/` may guide operator execution but MUST NOT become product workflow authority or route authority.

6. **Prompt class must be machine-enforced.**
   Lint and compliance tests MUST validate prompt requirements, routing semantics, and registry placement by prompt class.

7. **All existing prompts must be classified before migration planning.**
   Every current prompt in `.github/prompts/` must be assigned to exactly one class: `workflow`, `operator`, or `internal`.

8. **Cross-cutting workflow registration is narrowed in scope.**
   Cross-cutting prompt registration applies only to cross-cutting `workflow` prompts. It does not imply that all prompts discoverable in the repository are workflow-routed prompts.

9. **Generated-program inheritance must be explicit.**
   Only prompts intentionally designed for generated repositories may flow into downstream repos. PROGRAMSTART-only maintenance prompts remain scoped to PROGRAMSTART unless explicitly exported.

10. **Implementation planning is architecture-first.**
    Any remediation gameplan for this change must begin from accepted architectural decisions, then proceed through standards, registry, validation, migration, and documentation workstreams.

### Open Exclusions

The following are intentionally excluded from this decision and any immediate follow-up plan unless later work proves them necessary:

- Changing PROGRAMBUILD stage order or USERJOURNEY delivery order.
- Changing product route/state authority in `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md` or related authority docs.
- Rewriting unrelated PROGRAMBUILD or USERJOURNEY canonical content.
- Treating `devlog/` as a canonical source of truth.
- Broad repo refactors unrelated to prompt architecture boundaries.
- Automatically exporting PROGRAMSTART operator prompts into generated repositories.

### Implementation-Entry Criteria

No implementation plan may begin until all of the following are true:

1. The three prompt classes (`workflow`, `operator`, `internal`) are frozen and unambiguous.
2. Routing eligibility is frozen: only `workflow` prompts may participate in workflow routing.
3. The target registry model separates discoverability from workflow guidance.
4. The standards strategy is frozen: one standard for workflow prompts and one for operator prompts.
5. The `devlog/` non-canonical boundary is reaffirmed.
6. Validation goals are frozen, including class-aware lint/compliance enforcement.
7. The existing prompt inventory can be classified without a miscellaneous bucket.
8. The ADR layer is consistent about the narrowed meaning of cross-cutting prompt registration.
9. Generated-repo inheritance policy is frozen.
10. The future remediation gameplan is explicitly architecture-first rather than edit-first.

### Consequences

- Good: Prompt intent, routing eligibility, and validation boundaries become explicit rather than implied.
- Good: PROGRAMSTART maintenance prompts no longer need to masquerade as workflow-routing prompts.
- Good: Future generated repos are less likely to inherit PROGRAMSTART-only maintenance semantics.
- Good: Compliance checks can fail structural regressions instead of accepting exception-heavy prompt drift.
- Bad: Registry, standards, tests, and existing prompt inventory will require coordinated follow-up work.
- Neutral: Existing prompt documentation and ADR language will need to be clarified to align with the new model.

## Pros and Cons of the Options

### Option A

- Good, because it avoids immediate structural changes.
- Bad, because it preserves the current ambiguity and normalizes exception-driven maintenance.
- Bad, because future generated programs remain exposed to the same conceptual leak.

### Option B

- Good, because it creates a clean architecture boundary between workflow control and repo maintenance.
- Good, because it supports deterministic registry placement and class-aware validation.
- Bad, because it requires deliberate migration work across standards, registry, tests, and prompt inventory.

### Option C

- Good, because it would reduce some prompt-surface confusion quickly.
- Bad, because it leaves standards and validation semantics contradictory.
- Bad, because it treats symptoms instead of the underlying architecture problem.

## Confirmation

This decision is implemented correctly when all of the following are true:

- The repository contains a documented prompt taxonomy with `workflow`, `operator`, and `internal` classes.
- Cross-cutting workflow registration only applies to workflow prompts.
- Workflow prompt standards no longer govern operator prompts by default.
- Class-aware validation fails prompts that use the wrong routing or structural semantics for their class.
- The prompt inventory is fully classified and no generated-repo inheritance happens implicitly.

## Links

- [0008-cross-cutting-prompts-registry.md](0008-cross-cutting-prompts-registry.md)
- [README.md](README.md)
- [PROGRAMBUILD_ADR_TEMPLATE.md](../../PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md)
- [DECISION_LOG.md](../../PROGRAMBUILD/DECISION_LOG.md)
- [.github/prompts/PROMPT_STANDARD.md](../../.github/prompts/PROMPT_STANDARD.md)
- [config/process-registry.json](../../config/process-registry.json)
- [.github/instructions/source-of-truth.instructions.md](../../.github/instructions/source-of-truth.instructions.md)
