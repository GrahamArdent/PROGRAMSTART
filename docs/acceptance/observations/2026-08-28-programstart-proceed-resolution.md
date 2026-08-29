# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-08-28
- **Project / repository:** repeated GCRM / Dedication / PROGRAMSTART Mode-C operator workflow; methodology owner `GrahamArdent/PROGRAMSTART`
- **PROGRAMSTART lesson ID:** `PSL-016`
- **Checkpoint / acceptance surface:** repeated recommendation → generic operator acceptance (`proceed`, `go ahead`, `proceed with your recommendation`, `do what you recommend`) after evidence-backed Mode-C analysis
- **Classification:** systemic

## What happened

Across recent mature-project sessions, PROGRAMSTART could usually determine a good next recommendation, preserve the project execution spine, route uncertainty, and derive safe work. A recurring ambiguity remained after the recommendation was accepted: the operator's generic `proceed` did not have one explicit methodology contract for deciding whether to execute inside current authority, reconcile a durable authority delta before/with execution, preserve a future recommendation without resequencing the active spine, or retain a stronger consequential approval gate.

The existing methodology already contained most required primitives: one-project/one-spine authority, Mode-C deltas, work packets, operator/manual gates, durable reconciliation, and post-implementation closure. The gap was the **acceptance-to-execution transition** between recommendation and packet execution.

The same session exposed a related completeness concern. PROGRAMSTART already had `PROGRAMBUILD_CHECKLIST.md`, `programstart progress`, and `docs/PROGRAMSTART_REAL_WORLD_ACCEPTANCE_CHECKLIST.md`, but recent methodology PRs could complete without explicitly reconciling applicable checklist obligations. The existing progress helper counts Markdown checked/unchecked boxes; it does not distinguish not-applicable, blocked, or authority-permitted deferred obligations and did not by itself make checklist reconciliation part of truthful closure.

## Evidence

- repository / PR / methodology evidence:
  - `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` already required one execution spine, Mode-C delta recommendations, and post-work reconciliation, but did not define generic operator-acceptance semantics.
  - `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` already required authority, scope, acceptance criteria, verification, durable updates, and reconciliation, but had no explicit accepted-recommendation disposition or checklist-closure contract.
  - `.github/prompts/start-programstart-project.prompt.md` v2.7 orchestrated through execution, verification, reconciliation, Learning Gate, and next slice, but did not explicitly resolve a generic acceptance of a prior recommendation.
  - `PROGRAMBUILD/PROGRAMBUILD_CHECKLIST.md` was active and extensive; `docs/PROGRAMSTART_REAL_WORLD_ACCEPTANCE_CHECKLIST.md` was an active subordinate methodology-acceptance checklist.
  - `scripts/programstart_checklist_progress.py` already summarized `[x]` completion counts, confirming checklist tooling existed but did not own richer closure semantics.
  - recent PROGRAMSTART PRs #63 and #64 described strong self-review/verification and Learning Gate behavior, but their PR bodies did not explicitly reconcile the existing checklist items as a closure contract.
- implementation evidence in PR #65:
  - Planning Operating Model now defines three accepted-recommendation dispositions plus an independent stronger-gate overlay and authority-worthiness test.
  - Work Packet now carries accepted-recommendation resolution and conditional checklist completeness/reconciliation fields.
  - orchestration prompt v2.8 handles natural-language generic acceptance from current context while deliberately avoiding a new CLI command/state machine or brittle keyword parser.
  - execution and real-world acceptance checklists now define active derived checklist semantics and closure reconciliation.
  - focused static-contract tests cover ordinary execution, authority delta, future deferral, stronger gate preservation, disproved recommendation, Mode-C preservation, checklist completeness, checklist anti-bloat, and no new CLI state machine.
- verification actually performed:
  - live `main` inspection of canonical authority, Planning Operating Model, Work Packet, Challenge Gate, execution checklist, checklist progress helper/tests, real-world acceptance checklist, Learning Loop, learning ledger, orchestration prompt, orchestration implementation, orchestration tests, bootstrap propagation, and recent merged PRs #63/#64;
  - connected-tool branch/PR review and focused regression-test code inspection.
- checks not performed / unavailable:
  - no local PROGRAMSTART CLI, pytest, Ruff, Pyright, nox, or manual convergence workflow run is claimed from this connected-tools environment unless later PR evidence explicitly records such a run.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** correctly preserved Mode-C project authority and produced recommendations, but left the semantic effect of later generic acceptance partly to agent judgment.
- **What helped:** current authority, Work Packet, operator-gate, reconciliation, and checklist primitives meant the gap could be closed by composition rather than a new lifecycle/state machine.
- **What created friction or uncertainty:** a natural operator word such as `proceed` could refer to direction acceptance, immediate execution authority, future preservation, and/or a consequential action. Without an explicit precedence rule, agents could either over-authorize, churn the Master, jump sequencing, or under-execute by asking unnecessary follow-ups. Existing checklists could also remain passive reference documents instead of active completeness aids.
- **Was existing methodology sufficient?** partially before PR #65; the bounded methodology extension is now implemented and awaits natural real-project validation.

## Learning decision

- **Existing lesson match:** no prior `PSL-001`–`PSL-015` lesson owned the recommendation-acceptance transition. `PSL-007` covers operator/manual gate handoffs after an environment/action boundary, not generic acceptance semantics. `PSL-008` covers lane selection, not accepted-recommendation disposition. `PSL-013` provides the Learning Gate that captured this observation.
- **Maturity before:** candidate during solution challenge
- **Maturity after:** implemented
- **Why the evidence changes or does not change maturity:** repeated real Mode-C ambiguity earned a bounded methodology change, and PR #65 implements it in existing owners with focused contract tests. It remains unvalidated because no later natural real-project `proceed` turn has yet exercised the completed v2.8 behavior.
- **PROGRAMSTART change required now:** implemented in PR #65 through existing Planning Operating Model, Work Packet, orchestration prompt, checklist surfaces, canonical/index authority, acceptance learning, and focused tests. No new lifecycle, persistent recommendation state machine, separate approval subsystem, hidden backlog, or top-level CLI command was added.

## Solution challenge result

The initially proposed four peer categories (`EXECUTION`, `AUTHORITY_DELTA`, `DEFERRED_DELTA`, `APPROVAL_GATE`) were broader than necessary.

Implemented smaller model:

1. **execute_current_authority** — accepted recommendation is already inside current authority; execute a bounded packet without strategic-plan churn.
2. **reconcile_authority_then_execute** — accepted recommendation changes durable project truth; reconcile the owning authority/decision record before or atomically with dependent implementation.
3. **defer_without_resequencing** — recommendation is accepted as valuable direction but is not currently authorized/next; preserve it only in an existing appropriate future/decision surface when warranted and return to the real current slice.

A stronger consequential approval/manual/security/cost/privacy/legal/release requirement is an **independent gate overlay**, not a fourth peer disposition. Generic acceptance can approve the recommendation direction while leaving a genuinely additional gate unsatisfied.

Checklist behavior extends existing Work Packet/checklist closure rather than creating a new checklist registry or execution spine. A separate checklist PSL was not created because current evidence supports checklist discipline as part of this acceptance-to-closure gap; future independent evidence can split it only if warranted.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** the next normal PROGRAMSTART-assisted real-project conversation where the operator accepts a recommendation with a generic phrase such as `proceed with your recommendation`.
- **What evidence would be sufficient:** the agent correctly derives one disposition from current authority, preserves any genuinely additional stronger gate, updates durable authority only when required, executes or defers proportionally, reconciles actual results, and uses applicable checklist obligations at closure without requiring the operator to restate methodology or adding unnecessary ceremony.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] The implemented change extends existing machinery rather than manufacturing a separate lifecycle/state machine.
