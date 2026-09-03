# Acceptance Observation — Autonomy Closure Authority-Gap Composition

Date: 2026-09-03

Status: **methodology composition implemented; first natural real retest open**

## Observation

A portfolio-wide autonomy audit produced a prioritized derived `AUTONOMY_CLOSURE_CHECKLIST.md` intended to route work across PROGRAMSTART-managed repositories.

The operator identified a critical ambiguity before using it: what should happen when a material checklist item is **not represented anywhere in the proposed owning repository's current Master/strategic authority**?

Executing directly from the checklist would violate the existing authority boundary. Requiring manual re-planning for every such finding would reintroduce operator glue and undermine Mode-C continuation.

## Existing primitives inspected

The live methodology already provides most of the required behavior:

- `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` preserves one project/one execution spine and converts new Mode-C findings into deltas rather than new game plans;
- accepted recommendations already resolve to `execute_current_authority`, `reconcile_authority_then_execute`, or `defer_without_resequencing`;
- the authority-worthiness test prevents both stale authority and unnecessary Master churn;
- `PROGRAMBUILD_WORK_PACKET.md` already supports task-scoped cross-repository ownership/dependency reasoning;
- `PROGRAMSTART_EFFECTIVE_AUTONOMY.md` makes capability subordinate to project authority and fails closed when consequential permission is absent;
- `PROGRAMSTART_LEARNING_LOOP.md` already distinguishes local/systemic/confirmation/counterevidence and requires extending existing mechanisms before inventing new machinery;
- Portfolio Operations remains derived routing/attention state rather than project authority.

This is consistent with the recent conversation-to-authority retest that found the existing Mode-C/accepted-recommendation/portfolio primitives sufficient and warned against creating another lifecycle or global backlog.

## Decision

Add a narrow named **Authority-Gap Reconciliation** application protocol that composes the existing primitives.

An Authority Gap means a current derived finding appears material and authority-worthy but is not represented strongly enough in the repository that should own the durable truth.

The phrase is routing shorthand only. It is **not**:

- a fourth recommendation disposition;
- a new project lifecycle state;
- a portfolio backlog;
- a new execution authority;
- permission to execute from a checklist/audit;
- automatic evidence that PROGRAMSTART itself is defective.

The required behavior is:

1. inspect current owning authority and live evidence;
2. reject/correct stale, duplicate, completed, superseded, or disproved findings;
3. select the real owner;
4. reconcile an authority-worthy existing-project delta using current Mode-C semantics;
5. keep cross-project authority separated by concern owner;
6. keep genuinely ownerless findings non-authoritative until promotion is earned;
7. derive dependent execution from reconciled authority;
8. return automatically to the originating flow when otherwise authorized;
9. at a meaningful Learning Gate, ask why the mismatch existed and route learning to the actual behavior owner.

## Learning decision

Do **not** create a new PSL lesson ID from this planning-only observation.

The current change is a named operational composition of already-established lessons/primitives, especially the behaviors represented by `PSL-016`, `PSL-017`, `PSL-018`, effective-autonomy authority separation, and the existing Learning Gate.

A new or strengthened methodology lesson is earned only if real use shows that these primitives remain insufficient, ambiguous, or repeatedly misapplied after the composition is available.

## First real retest condition

Use the **first natural Autonomy Closure Checklist item** that is materially useful but absent from its proposed owner's current authority.

Success requires:

- no direct execution from the checklist;
- current owning authority inspected first;
- stale/duplicate findings corrected rather than manufactured into work;
- correct owner selected or explicitly unresolved;
- authority-worthy delta reconciled into the existing owner rather than a second roadmap;
- dependent Work Packet derived from reconciled authority;
- automatic return to the originating checklist flow without redundant `proceed` when otherwise authorized;
- Learning Gate classification of the cause;
- no unnecessary new lifecycle/backlog/lesson.

If the first natural item is already represented, the checklist should simply execute under normal Mode C and the Authority-Gap retest remains open for the first case that genuinely matches it.

## Files changed by this methodology candidate

- `docs/PROGRAMSTART_AUTHORITY_GAP_RECONCILIATION.md`
- `PROGRAMBUILD/PROGRAMBUILD_CHECKLIST.md`
- `tests/test_authority_gap_reconciliation_contract.py`
- this observation

## Expected outcome

The operator should be able to say `Continue the Autonomy Closure Checklist` and have a derived finding route through current project authority deterministically, including safe correction/reconciliation when authority is missing, without the checklist becoming a shadow Master and without requiring the operator to manually invent the reconciliation procedure each time.
