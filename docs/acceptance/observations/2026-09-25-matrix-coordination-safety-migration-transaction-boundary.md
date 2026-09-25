# PROGRAMSTART Learning Observation — Safety Migration Transaction Boundary

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-25
- **Project / repository:** `GrahamArdent/programstart-autonomous-controller` #114 under PROGRAMSTART #156
- **PROGRAMSTART lesson ID:** unassigned candidate; central learning-ledger mutation is intentionally deferred while overlapping ledger PRs remain active
- **Checkpoint / acceptance surface:** live shared-mutation coordination activation and post-release Challenge
- **Classification:** systemic candidate

## What happened

Controller #114 implemented run-scoped shared-mutation claims at the repository-effect admission boundary. A live-state audit then found three historical repository attempts still durably `RESERVED` from before the coordination system existed.

Those legacy attempts had to be quarantined before any new mutation could be admitted. The first hardening shape performed that protective reconciliation inside the same transaction as the new operation it was protecting.

Challenge exposed a rollback hole: the new operation is legitimately allowed to fail closed. If its failure rolled back the whole transaction, it could also erase the just-created legacy quarantine. The safety migration would therefore disappear precisely on a path where the protection was still required.

Controller PR #118 corrected the boundary: legacy quarantine is persisted as a one-way safety reconciliation before current admission is attempted. A later admission failure can no longer roll the quarantine back.

## Evidence

- PROGRAMSTART Matrix coordination contract: `GrahamArdent/PROGRAMSTART@6a2d2565d6723eca56b53b7f76139e6960c45c6a:docs/PROGRAMSTART_MATRIX_COORDINATION.md`.
- Initial Controller coordination implementation: PR #116.
- Live-state hardening: Controller PR #118, merged as `97f4dcaed4cbf8aaf282d07a67627b7c1f684851`.
- Controller #114 terminal packet records exact live release activation, read-only Matrix snapshot, legacy-quarantine acceptance, final Challenge CLEAR, and no authority/credential/network widening.
- Exact Controller tests prove legacy quarantine remains durable even when the new request is rejected, while unresolved legacy state does not gain new execution authority.

## PROGRAMSTART behavior

- **What helped:** post-implementation Challenge, live-state inspection, shared-mutation ownership, fail-closed admission, and exact durable-state tests exposed the rollback hole before the safety claim was treated as terminal.
- **What created risk:** treating a protective reconciliation write as merely another statement inside the transaction of the operation being protected.
- **Existing lesson match:** related to shared-mutation ownership, authority reconciliation, and shift-left verification, but none of the current learning-ledger lessons directly owns the rule that a one-way safety migration must survive an independently permitted downstream failure.
- **Was existing methodology sufficient?** sufficient to discover and correct the defect through Challenge; the reusable transaction-boundary rule is not yet explicit enough to justify an immediate global methodology change from one instance.

## Learning decision

**Candidate rule:**

> When a protective reconciliation or one-way safety migration must remain true even if the next operation legitimately fails, its durability boundary must not be coupled to rollback of that downstream operation. Commit/prove the protection first, or use an atomic design in which rolling it back is itself safe by construction.

- **Maturity:** candidate evidence only.
- **Central ledger action now:** none. Active learning-ledger PRs already own that shared mutation surface; do not create a competing rollup edit or assign a stable lesson number from this lane.
- **PROGRAMSTART change required now:** none beyond preserving this observation. Promote/deduplicate only when the ledger lane is free and evidence justifies it.

## Retest

Use the next real migration/quarantine/reconciliation that precedes an operation allowed to fail.

Sufficient evidence would show that:
1. the protection becomes durable before the fallible downstream operation, or rollback is mechanically proven safe;
2. deliberate downstream failure does not erase the protection;
3. replay remains idempotent;
4. no new authority is minted by the migration;
5. Challenge catches any transaction-boundary coupling before release.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No second coordinator, state store, or backlog was created.
- [x] No secrets/private payloads are present.
- [x] Evidence claims are bounded to checks and live acceptance that actually occurred.
- [x] No central learning-ledger mutation or premature stable lesson ID is claimed.
