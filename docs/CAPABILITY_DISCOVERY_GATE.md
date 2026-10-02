# Capability Discovery Gate

Status: PROGRAMSTART methodology enforcement primitive.

## Invariant
No consequential capability assumption, capability-absence claim, human escalation, or new execution-path design may pass PROGRAMSTART without deterministic Paths discovery appropriate to the required effect, followed by owner-native JIT verification when a realization is selected.

## Boundary
Paths remains discovery/read-model authority for path relationships and resilience. It does not grant semantic permission. Owning repositories/providers remain authority for permission, admission, release/currentness, and consequence.

## Required sequence
1. Express the required effect as actor + effect + target.
2. Query Paths effect reachability.
3. Verify selected realizations against current owner-native authority/currentness.
4. If the obvious realization fails, widen to equivalent/composable realizations before escalation.
5. Only after a zero-result widened search may PROGRAMSTART accept human_required, unavailable, automation_gap, or new_capability_required.
6. Re-run discovery at material failure or resumed/cold-start boundaries when evidence may be stale.

This is targeted retrieval, not a requirement to load the Paths corpus for every task.
