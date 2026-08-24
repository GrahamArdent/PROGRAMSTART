---
status: accepted
date: 2026-08-24
deciders: [solo operator]
consulted: []
informed: []
---

# 0023. Use One Strategic Execution Spine with Bounded Work Packets

## Context and Problem Statement

PROGRAMBUILD already had a stage-gated authority model, but active execution had become increasingly stage-centric: implementation guidance could require broad context reloads and repeated validation around small slices of work, while research, audits, and readiness material could accidentally grow into parallel plans. Existing projects also need a way to absorb new research or planning improvements without replacing their established Master Game Plan or execution authority.

The planning operating model therefore needs to preserve strong project governance while making day-to-day execution smaller, faster, and more context-efficient.

## Decision Drivers

- Preserve one authoritative strategic execution spine per real project.
- Prevent research, audits, readiness reviews, checklists, and agent outputs from silently becoming competing master plans.
- Use progressive disclosure so agents load only the authority needed for the current slice after the stage baseline is known.
- Reuse trusted evidence until a defined invalidation trigger makes re-verification necessary.
- Keep verification proportional to the changed surface during execution while widening again at explicit convergence points.
- Support raw ideas, research-backed projects, and already-active projects without forcing them through the same blank-sheet intake path.
- Keep rigor proportional to project risk without weakening source-of-truth discipline.

## Considered Options

1. **Keep the existing stage-centric model unchanged.** Continue loading broad stage context and running broad validation around implementation slices.
2. **Replace stage governance with task/work-packet execution.** Make work packets the primary source of truth and remove most stage-level authority.
3. **Use a layered model.** Keep stage-level strategic authority, derive bounded non-canonical work packets for active execution, use targeted verification inside a slice, and widen context/verification again at convergence points.

## Decision Outcome

Chosen option: **3 — layered strategic authority plus bounded work packets and convergence gates**.

A real project MUST retain one strategic execution spine. In a PROGRAMBUILD-native project that is normally `PROGRAMBUILD_GAMEPLAN.md` together with the canonical stage authority documents. In an existing project with an already-established Master Game Plan or equivalent execution ledger, PROGRAMBUILD MUST preserve that project-owned authority unless an explicit decision replaces it.

`PROGRAMBUILD_WORK_PACKET.md` defines the standard for a derived current execution slice. A project MAY maintain `CURRENT_WORK_PACKET.md`, but it is non-canonical and replaceable. It narrows the current task to the exact authority sections, evidence, non-goals, acceptance criteria, invalidation triggers, and targeted verification needed for that slice.

Stage guidance establishes the baseline. Task execution then narrows. Periodic reviews, stage transitions, release readiness, audits, or any invalidation event widen context and verification again. Evidence that remains inside its stated validity conditions SHOULD be reused rather than reflexively re-proved.

Research and specialist-agent outputs remain evidence and recommendations until the project authority adopts them. For an in-flight project, new research SHOULD produce explicit deltas against the existing execution spine rather than a second master plan.

### Consequences

- Good: Active implementation can use much smaller context windows and verification surfaces.
- Good: Existing project roadmaps remain authoritative instead of being displaced by PROGRAMBUILD artifacts.
- Good: Repeated work is reduced because trusted evidence can be reused until invalidated.
- Good: Governance is preserved because stage boundaries and convergence gates deliberately widen the review surface again.
- Good: Lite, Product, and Enterprise variants can differ in ceremony and evidence strength without changing the authority model.
- Bad: Work packets must be written carefully; a poor packet can omit a relevant dependency or invalidation trigger.
- Bad: Operators must respect convergence points rather than allowing narrow verification to continue indefinitely.
- Neutral: This changes operating policy and documentation much more than runtime code; the CLI still exposes existing `guide`, `drift`, `validate`, and `jit-check` commands.

## Confirmation

This decision is implemented when:

- `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` is canonical for planning-to-execution separation, entry modes, proportional rigor, evidence reuse, and progressive context loading.
- `PROGRAMBUILD_WORK_PACKET.md` defines bounded active execution and explicitly marks `CURRENT_WORK_PACKET.md` as derived/non-canonical.
- `PROGRAMBUILD.md`, the Lite/Product/Enterprise variants, `PROGRAMBUILD_GAMEPLAN.md`, and `PROGRAMBUILD_CHALLENGE_GATE.md` use the layered model consistently.
- Stage 7 uses bounded work packets and targeted verification, while Stage 8 and periodic Stage 7 reviews act as wider convergence points.
- JIT instructions and prompts distinguish stage-baseline context from task-scoped context.
- Specialist agents return evidence/deltas rather than taking over project authority.
- Repository validation, drift checks, prompt-compliance tests, and the relevant pytest suite pass before merge when an execution environment is available.

## Links

- <!-- DEC-020 -->
- [Decision log](../../PROGRAMBUILD/DECISION_LOG.md)
- [Planning operating model](../../PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md)
- [Work packet standard](../../PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md)
- [Existing JIT CLI decision](0017-jit-check-cli-command.md)
