# Capability Discovery Gate

Status: PROGRAMSTART methodology enforcement primitive.

## Invariant

No consequential capability assumption, capability-absence claim, human escalation, or new execution-path design may pass PROGRAMSTART without deterministic Paths discovery appropriate to the required effect, followed by owner-native JIT verification when a realization or human gate is selected.

A caller assertion that discovery or widening occurred is not proof. Discovery evidence must be bound to a durable, reproducible Paths classifier receipt.

## Boundary

Paths remains discovery/read-model authority for path relationships, composition/reuse knowledge, and resilience. It does not grant semantic permission. Owning repositories/providers remain authority for permission, admission, release/currentness, human-gate irreducibility, and consequence.

Discovery evidence never implies credential use, repository mutation/merge, release activation, sudo/root, provider-policy, or human-approval authority. Those remain consequence-specific owner decisions. Owner-native verification is required when a realization is selected for consequence (and when an irreducible human gate is asserted), not merely to retain a read-only discovery receipt.

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

## Post-discovery failure localization and mutation admission

A higher-order or end-to-end failure does not automatically invalidate previously earned component proof. After durable discovery, PROGRAMSTART must identify the first proven failing boundary before admitting a consequential mutation to an existing capability.

The failure-localization receipt retains:

- the existing capability and its current contract reference;
- prior proof references that remain evidence until an explicit invalidation applies;
- current contract evidence and one typed contract disposition: satisfied, contradicted, insufficient, stale/unknown, or superseded;
- the first proven failing boundary and its evidence;
- independent degradation evidence when an external dependency failed separately;
- replacement-necessity evidence when replacement is proposed;
- a canonical SHA-256 of the localization facts plus verification mechanism/reference and invalidation conditions.

The admitted action must match the localized evidence:

- dispatcher, adapter, composition, or invocation failure + satisfied component contract -> repair the composition boundary;
- stale/unknown component evidence -> reverify before blaming or replacing the component;
- independent external degradation + satisfied component contract -> isolate the degradation without invalidating the component;
- bad test assumption + satisfied component contract -> correct the test/assumption;
- component boundary + contradicted own contract -> repair the existing capability;
- component boundary + insufficient own contract -> extend the existing capability;
- replacement is allowed only when the first proven failing boundary is the component, its own contract is contradicted/insufficient/superseded, and durable evidence shows repair or extension is not the sufficient bounded remediation.

This is not a sunk-cost rule and does not make previously passing components immortal. New evidence may invalidate old proof. The constraint is causal: a composed failure alone is not evidence that every constituent failed.

## Scope

This gate now covers both pre-escalation capability discovery and post-discovery mutation admission. It reuses existing PROGRAMSTART evidence/currentness and Paths composition knowledge; it does not create another evidence engine, graph authority, orchestrator, or execution plane.

This is targeted retrieval, not a requirement to load the Paths corpus for every task.
