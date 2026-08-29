# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-08-28
- **Project / repository:** repeated GCRM / Dedication / PROGRAMSTART Mode-C operator workflow; methodology owner `GrahamArdent/PROGRAMSTART`
- **PROGRAMSTART lesson ID:** proposed `PSL-016`
- **Checkpoint / acceptance surface:** repeated recommendation → generic operator acceptance (`proceed`, `go ahead`, `proceed with your recommendation`, `do what you recommend`) after evidence-backed Mode-C analysis
- **Classification:** systemic

## What happened

Across recent mature-project sessions, PROGRAMSTART could usually determine a good next recommendation, preserve the project execution spine, route uncertainty, and derive safe work. A recurring ambiguity remained after the recommendation was accepted: the operator's generic `proceed` did not have one explicit methodology contract for deciding whether to execute inside current authority, reconcile a durable authority delta before/with execution, preserve a future recommendation without resequencing the active spine, or retain a stronger consequential approval gate.

The existing methodology already contains most required primitives: one-project/one-spine authority, Mode-C deltas, work packets, operator/manual gates, durable reconciliation, and post-implementation closure. The gap is the **acceptance-to-execution transition** between recommendation and packet execution.

The same session exposed a related completeness concern. PROGRAMSTART already has `PROGRAMBUILD_CHECKLIST.md` and `docs/PROGRAMSTART_REAL_WORLD_ACCEPTANCE_CHECKLIST.md`, but recent methodology PRs can complete without explicitly reconciling applicable checklist obligations. A checklist can therefore exist as good reference material without necessarily functioning as an active closure aid.

## Evidence

- repository / PR / methodology evidence:
  - `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` already requires one execution spine, Mode-C delta recommendations, and post-work reconciliation, but does not define generic operator-acceptance semantics.
  - `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` already requires authority, scope, acceptance criteria, verification, durable updates, and reconciliation, but has no explicit accepted-recommendation disposition or checklist-closure contract.
  - `.github/prompts/start-programstart-project.prompt.md` v2.7 orchestrates through execution, verification, reconciliation, Learning Gate, and next slice, but does not explicitly resolve a generic acceptance of a prior recommendation.
  - `PROGRAMBUILD/PROGRAMBUILD_CHECKLIST.md` is active and extensive; `docs/PROGRAMSTART_REAL_WORLD_ACCEPTANCE_CHECKLIST.md` is an active subordinate methodology-acceptance checklist.
  - recent PROGRAMSTART PRs #63 and #64 describe strong self-review/verification and Learning Gate behavior, but their PR bodies do not explicitly reconcile the existing checklist items as a closure contract.
- verification actually performed:
  - live `main` inspection of canonical authority, Planning Operating Model, Work Packet, Challenge Gate, execution checklist, real-world acceptance checklist, Learning Loop, learning ledger, orchestration prompt, orchestration implementation, orchestration tests, and recent merged PRs #63/#64.
- checks not performed / unavailable at observation time:
  - no local PROGRAMSTART CLI, pytest, Ruff, Pyright, nox, or manual convergence workflow run is claimed from this connected-tools environment.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** correctly preserved Mode-C project authority and produced recommendations, but left the semantic effect of later generic acceptance partly to agent judgment.
- **What helped:** current authority, Work Packet, operator-gate, and reconciliation primitives mean the gap can likely be closed by composition rather than a new lifecycle/state machine.
- **What created friction or uncertainty:** a natural operator word such as `proceed` can refer to direction acceptance, immediate execution authority, future preservation, and/or a consequential action. Without an explicit precedence rule, agents can either over-authorize, churn the Master, jump sequencing, or under-execute by asking unnecessary follow-ups.
- **Was existing methodology sufficient?** partially

## Learning decision

- **Existing lesson match:** no current `PSL-001`–`PSL-015` lesson owns the recommendation-acceptance transition. `PSL-007` covers operator/manual gate handoffs after an environment/action boundary, not generic acceptance semantics. `PSL-008` covers lane selection, not accepted-recommendation disposition. `PSL-013` provides the Learning Gate that captured this observation.
- **Maturity before:** none
- **Maturity after:** candidate
- **Why the evidence changes or does not change maturity:** the ambiguity has appeared repeatedly in real Mode-C operator flow, is independent of any one product, and can affect authority correctness. Existing primitives reduce the needed change but do not fully specify the transition.
- **PROGRAMSTART change required now:** bounded extension of the existing Planning Operating Model, Work Packet/orchestration contract, checklist closure behavior, and focused tests. Do not add a new lifecycle, persistent recommendation state machine, separate approval subsystem, hidden backlog, or top-level CLI command.

## Solution challenge result before implementation

The initially proposed four peer categories (`EXECUTION`, `AUTHORITY_DELTA`, `DEFERRED_DELTA`, `APPROVAL_GATE`) are broader than necessary.

Preferred smaller model:

1. **execute_current_authority** — accepted recommendation is already inside current authority; execute a bounded packet without strategic-plan churn.
2. **reconcile_authority_then_execute** — accepted recommendation changes durable project truth; reconcile the owning authority/decision record before or atomically with dependent implementation.
3. **defer_without_resequencing** — recommendation is accepted as valuable direction but is not currently authorized/next; preserve it only in an existing appropriate future/decision surface when warranted and return to the real current slice.

A stronger consequential approval/manual/security/cost/privacy/legal/release requirement is an **independent gate overlay**, not a fourth peer disposition. Generic acceptance can approve the recommendation direction while leaving that stronger gate unsatisfied.

Checklist behavior should likewise extend existing Work Packet/checklist closure rather than create a new checklist registry or execution spine.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** the next normal PROGRAMSTART-assisted real-project conversation where the operator accepts a recommendation with a generic phrase such as `proceed with your recommendation`.
- **What evidence would be sufficient:** the agent correctly derives one disposition from current authority, preserves any stronger gate, updates durable authority only when required, executes or defers proportionally, reconciles actual results, and uses applicable checklist obligations at closure without requiring the operator to restate methodology.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] The proposed change extends existing machinery rather than manufacturing a separate lifecycle/state machine.
