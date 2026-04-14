# PROGRAMBUILD_LITE.md

# Program Build Lite

Use this version for a solo developer, a prototype, or a very small internal tool.
The goal is speed without abandoning the guardrails that prevent the most common structural mistakes.

Authority:
- `PROGRAMBUILD_CANONICAL.md` defines source-of-truth rules
- `PROGRAMBUILD_FILE_INDEX.md` is the lookup table for critical files
- `PROGRAMBUILD_IDEA_INTAKE.md` runs before Stage 0 — challenge the idea before filling the inputs block
- `PROGRAMBUILD_CHALLENGE_GATE.md` runs at every stage transition — Parts A, C, F, and H are required minimum for Lite
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

---

## Essential Stages

| Stage | Output | Standard |
|---|---|---|
| Inputs | filled inputs block | must be complete |
| Feasibility | short go/no-go note | 1 page max |
| Quick research | short validation note or decisions table | only enough to avoid an obvious bad bet |
| Requirements | lean requirements and top workflows | focused on P0 only |
| Architecture | one architecture note | only essential contracts |
| Scaffold | route layer, auth client, CI, basic tests | must be green |
| Build | feature loop | one feature at a time |
| Launch check | short readiness checklist | must be explicit |
| Post-launch note | short review and next actions | capture what changed after first real use |

---

## Non-Negotiables

- one contract layer for the dominant external surface: routes, endpoints, commands, jobs, or public API
- one auth-aware client, trusted caller wrapper, or equivalent boundary helper when access control exists
- no hardcoded protected paths, commands, or contract identifiers outside the contract layer
- one alignment test for the dominant contract surface
- one auth or trust-boundary test per protected surface
- one smoke scenario for the dominant execution mode
- one rollback note before first deployment
- one short decision log with the reasons for key tradeoffs
- critical planning files follow the `PROGRAMBUILD_*.md` naming convention

Attach `USERJOURNEY/` only if the lite project still has real onboarding, consent, activation, or first-run routing decisions to make.

---

## Suggested Subagents

See `PROGRAMBUILD_SUBAGENTS.md` for full prompts and workspace agent files.

| Agent | Use for |
|---|---|
| Discovery & Scoping | quick domain research, scope, and top workflows |
| Architecture & Security | essential contract surface and trust boundary |
| Quality & Release | smoke plan and short launch checklist |
| Risk Spike Agent | when an unknown is rated medium or high impact |
| Contract Auditor | route and auth drift check |

---

## Minimal Prompt Pattern

```text
Build a lean but production-conscious plan for this app.

Inputs:
- project inputs block

Choose the dominant execution mode first: interactive user flow, operator workflow, CLI scenario, service contract, or scheduled job.

Produce:
1. short feasibility note
2. quick stack and dependency validation
3. P0 requirements only
4. main workflow for the product shape
5. basic architecture and dominant contract surface
6. scaffold with the minimum contract layer and boundary helpers
7. essential tests: alignment, auth or trust boundary, smoke scenario
8. short launch checklist
9. short post-launch note
```

---

## Lite Definition Of Done

- primary P0 workflow works end to end
- protected boundaries reject unauthorized or invalid access
- dominant contract alignment test passes
- one smoke scenario for the main execution mode passes
- deployment and rollback steps are written down
- a short post-launch review is scheduled or completed

---

Last updated: 2026-04-14
