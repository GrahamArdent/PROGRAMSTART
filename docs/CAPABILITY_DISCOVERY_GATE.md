# Capability Discovery Gate

Status: PROGRAMSTART methodology enforcement primitive.

## Invariant

No consequential capability assumption, capability-absence claim, human escalation, or new execution-path design may pass PROGRAMSTART without deterministic Paths discovery appropriate to the required effect, followed by owner-native JIT verification when a realization or human gate is selected.

A caller assertion that discovery or widening occurred is not proof. Discovery evidence must be bound to a durable, reproducible Paths classifier receipt.

## Boundary

Paths remains discovery/read-model authority for path relationships, composition/reuse knowledge, and resilience. It does not grant semantic permission. Owning repositories/providers remain authority for permission, admission, release/currentness, human-gate irreducibility, and consequence.

The canonical discovery mechanism for this gate is the existing Paths composition classifier at scripts/find_capability_composition.py. PROGRAMSTART consumes its result; it does not create a second composition engine.

## Durable discovery receipt

A consequential decision must retain:

- the exact actor + effect + target and classifier constraints;
- the complete typed classifier result, including classification, reason, candidates, constituents, missing typed edges, owners/evidence/currentness and failure domains;
- authorization_inferred=false;
- the immutable GrahamArdent/paths commit SHA and classifier mechanism reference;
- a canonical SHA-256 of the classifier result;
- a verification reference for the Paths classifier/OBS-005 validation surface;
- explicit invalidation conditions.

This binds discovery to the PROGRAMSTART proof-durability invariant: evidence is not proof merely because a boolean or free-form reference says a search ran.

## Required sequence

1. Express the required effect as actor + effect + target.
2. Run the existing Paths composition classifier and retain a hash-bound durable receipt.
3. For absence/escalation conclusions, require current + proven + exclude-human-transport constraints so an obvious failed surface cannot hide another current machine realization.
4. If the classifier returns a usable machine realization/composition, reject human/unavailable/automation-gap/new-capability escalation.
5. Accept new_capability_required only when Paths returns GENUINELY_NEW_PATH_REQUIRED.
6. Verify a selected realization against current owner-native authority/currentness before consequential selection.
7. Accept human_required only with owner-native evidence that the remaining human gate is irreducible; Paths discovery alone cannot grant or infer that authority.
8. Re-run discovery at material failure or resumed/cold-start boundaries when its retained invalidation conditions may have fired.

## Scope of this slice

This gate prevents self-asserted widening and false new-capability escalation. It does not yet declare an existing component defective or authorize replacement after a composed failure. Failure-localization/component-preservation semantics remain a separate follow-on hardening, to be earned from durable discovery evidence rather than added as a parallel mechanism.

This is targeted retrieval, not a requirement to load the Paths corpus for every task.
