# PROGRAMBUILD_LITE.md

# Program Build Lite

Use this version for a solo developer, a prototype, or a very small internal tool.
The goal is speed without abandoning the guardrails that prevent the most common structural mistakes.

Authority:
- `PROGRAMBUILD_CANONICAL.md` defines source-of-truth rules
- `PROGRAMBUILD_FILE_INDEX.md` is the lookup table for critical files
- `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` defines planning entry modes, one-spine authority, proportional rigor, JIT context loading, and evidence reuse
- `PROGRAMBUILD_WORK_PACKET.md` defines the optional derived current-slice packet; it never becomes a second game plan
- `PROGRAMBUILD_IDEA_INTAKE.md` runs before Stage 0 — challenge the idea or existing-project delta before filling the inputs block
- `PROGRAMBUILD_CHALLENGE_GATE.md` runs at every stage transition — Parts A, C, and F are the Lite minimum; add B, D, E, G, or H when the change/risk makes them relevant
- `PROGRAMBUILD_GAMEPLAN.md` defines the execution order with cross-stage validation

---

## When To Use

Use this file when:
- the team is 1 to 3 people
- the product is low risk
- the budget or timeline is tight
- the system is not regulated or enterprise-critical

This can still be a small interactive product, an internal service, a CLI, a scriptable automation, or a lightweight background job.

Do not use this file when:
- the app stores sensitive regulated data
- the system needs formal approvals or audit trails
- multiple teams must coordinate contracts

Lite means **less ceremony**, not weaker authority discipline. Keep one strategic execution spine, load only the context needed for the current slice, and reuse valid evidence until an invalidation trigger occurs.

---

## Essential Stages

| Stage | Output | Standard |
|---|---|---|
| Inputs | filled inputs block or explicit existing-project delta | must be clear |
| Feasibility | short go/no-go note | concise and decision-useful |
| Quick research | short validation note or decisions table | only enough to avoid an obvious bad bet |
| Requirements | lean requirements and top workflows | focused on P0 only |
| Architecture | one architecture note | only essential contracts |
| Scaffold | contract layer, boundary helper, CI, basic tests | must be green |
| Build | feature loop | one bounded slice at a time |
| Launch check | short readiness checklist | must be explicit |
| Post-launch note | short review and next actions | capture what changed after first real use |

---

## Non-Negotiables

- one strategic execution spine for the project; research, audits, and work packets do not become competing plans
- one contract layer for the dominant external surface: routes, endpoints, commands, jobs, or public API
- one auth-aware client, trusted caller wrapper, or equivalent boundary helper when access control exists
- no hardcoded protected paths, commands, or contract identifiers outside the contract layer
- one alignment test for the dominant contract surface
- one auth or trust-boundary test per protected surface
- one smoke scenario for the dominant execution mode
- one rollback note before first deployment
- one short decision log with the reasons for key tradeoffs
- critical planning files follow the `PROGRAMBUILD_*.md` naming convention
- non-trivial implementation work SHOULD use a bounded work packet; trivial work MAY state the same objective/non-goal/context/evidence fields inline instead
- existing verification SHOULD be reused when no documented invalidation trigger occurred
- convergence reviews SHOULD be triggered by risk, blast radius, accumulated cross-slice change, uncertainty, evidence invalidation, or a stage/release boundary rather than an arbitrary feature count

Attach `USERJOURNEY/` only if the lite project still has real onboarding, consent, activation, or first-run routing decisions to make.

---

## Suggested Subagents

See `PROGRAMBUILD_SUBAGENTS.md` for full prompts and workspace agent files.

| Agent | Use for |
|---|---|
| Discovery & Scoping | quick domain research, scope, and top workflows |
| Architecture & Security | essential contract surface and trust boundary |
| Quality & Release | smoke plan and short launch checklist |
| Risk Spike Agent | when a material unknown blocks a decision |
| Contract Auditor | contract/auth drift check when warranted |

---

## Minimal Prompt Pattern

```text
Build a lean but production-conscious plan for this app or existing-project change.

Inputs:
- project inputs block, research-backed intake, or existing execution spine + proposed delta

First select the correct entry mode from PROGRAMBUILD_PLANNING_OPERATING_MODEL.md.
Preserve any existing project execution authority instead of creating another master plan.
Choose the dominant execution mode: interactive user flow, operator workflow, CLI scenario, service contract, or scheduled job.

Produce only the artifacts needed for the risk:
1. short feasibility note
2. quick stack/dependency validation or research delta
3. P0 requirements only
4. main workflow for the product shape
5. basic architecture and dominant contract surface
6. scaffold with the minimum contract layer and boundary helpers
7. essential tests: alignment, auth/trust boundary, smoke scenario
8. bounded implementation slices; use CURRENT_WORK_PACKET.md only when it materially improves focus
9. short launch checklist
10. short post-launch note

For each implementation slice, name reusable evidence, its invalidation triggers, and the smallest verification set needed for what changed.
Trigger a wider convergence review when accumulated change/risk warrants it or a stage/release boundary requires it; do not use a fixed feature count as a universal rule.
```

---

## Lite Definition Of Done

- primary P0 workflow works end to end
- protected boundaries reject unauthorized or invalid access
- dominant contract alignment test passes
- one smoke scenario for the main execution mode passes
- deployment and rollback steps are written down
- any current work packet is reconciled back into canonical project state rather than accumulated as a second plan
- a short post-launch review is scheduled or completed

---

Last updated: 2026-08-24
