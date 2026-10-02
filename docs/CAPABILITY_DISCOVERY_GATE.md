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

## Failure localization after discovery

A higher-order failure does not erase previously earned component evidence by itself. After durable discovery, PROGRAMSTART must localize the first causal boundary before declaring an existing capability defective or replacement-required.

Allowed failure classes are:

- composition/wiring gap;
- component-contract failure;
- component-contract insufficiency;
- currentness/activation failure;
- independent degradation;
- test/assumption failure;
- unknown/unresolved.

The localization record must identify the observed failure, the component and its contract, the first failed boundary, preserved evidence, any contradictory evidence, explicit invalidated proof, independent-degradation evidence, and any requirement gap. It remains diagnostic only and must set authorization_inferred=false.

Replacement is fail-closed:

- composition/wiring failure => preserve the component and repair the missing boundary when prior proof remains valid;
- component-contract failure => defect/replacement requires contradictory component evidence plus explicit invalidation of the affected component proof;
- component-contract insufficiency => replacement/extension requires an evidenced requirement gap; historical proof may remain valid for the narrower old contract;
- currentness/activation failure => recheck currentness rather than infer defect;
- independent degradation => record separately and do not attribute component defect without counterevidence;
- test/assumption failure => correct the test/model rather than replace the component;
- unresolved boundary => further localization only.

This rule does not forbid redesign. It prevents a composed failure from being treated as proof that every lower-level capability failed. The smallest architecturally complete causal repair remains preferred, while repeated composition failures may still justify a later contract-boundary redesign when evidence supports that conclusion.

## Acceptance examples

The primary regression is the actuator/dispatcher case: a proven reachability actuator remains valid while a higher-order scenario fails because dispatcher wiring is absent. PROGRAMSTART must preserve the actuator proof and select boundary repair; replacement must fail closed.

Counterexamples deliberately permit replacement when fresh evidence contradicts the actuator's own contract or proves that the old contract cannot satisfy a newly required effect.

## Scope

This gate now owns both pre-design capability discovery and post-failure localization for consequential capability conclusions. It remains a decision/evidence gate only: it does not execute repairs, grant semantic permission, replace owner authority, or become a second Paths registry.

This is targeted retrieval, not a requirement to load the Paths corpus for every task.
