# PROGRAMSTART Matrix Coordination Contract

Purpose: define the reusable PROGRAMSTART semantics for mandatory autonomous mutation coordination without turning the Matrix into a new authority, scheduler, database, or execution spine.

Status: **PROGRAMSTART reusable coordination contract / subordinate to owning-project authority and Controller runtime currentness**.

## 1. Protected invariant

> **No consequential autonomous mutation may cross the mutation boundary without current owner authority and a current Controller coordination admission for the exact declared write set.**

The Matrix is a composed coordination/read model. It may expose current authority references, active mutation ownership, conflicts, currentness, and execution state, but it does not create any of those truths.

## 2. Owner model

- **PROGRAMSTART** owns the reusable coordination semantics, compiled Work Packet write-set declaration, parity/acceptance contract, and Challenge/Learning rules.
- **Controller** owns live run-scoped mutation-claim admission, transactional serialization, fencing/currentness binding, and the read-only operational projection.
- **Owning repositories** own substantive project scope, architecture, accepted decisions, declared mutable surfaces, and effect authority.
- **Decision Closure** supplies semantic outcome/disposition receipts when useful; those receipts explicitly cannot grant execution authority.
- **Evidence Spine** owns evidence/provenance/currentness where already applicable.
- **Paths / Path Authority** owns availability, failover, recovery, and proof of the mandatory coordination access path.
- **Mission Control** may render/operator-interact with Matrix state but is not an authority source.

No new Matrix repository, state database, queue, scheduler, or orchestration layer is implied by this contract.

## 3. Existing packet is the coordination declaration

PROGRAMSTART compiled Work Packets already carry:

- `scope.surfaces` with mutable/read-only access;
- `dependencies.expected_write_set`;
- `dependencies.conflicts`;
- exact owning repository, authority commit, methodology commit, and Work Packet identity.

Those fields are the only admitted semantic write-set declaration for the Controller path. Do not create a parallel Matrix resource-declaration channel.

A Controller consumer must fail closed when a mutating packet's write set is absent, malformed, inconsistent with its mutable surfaces, or no longer current.

## 4. Mandatory ingress

For an admitted autonomous mutating effect:

1. revalidate the sealed Work Packet and current run authority;
2. derive the exact declared write set from the sealed packet;
3. atomically acquire or prove current ownership of all declared resources for the current run;
4. reserve the concrete effect attempt in the same serialized Controller transaction;
5. dispatch only after that admission succeeds;
6. revalidate current authority at existing downstream mutation boundaries;
7. retain claims for the active Work Packet/run;
8. release claims through explicit terminal/supersession/currentness-aware lifecycle.

A caller, chat, renderer, Matrix projection, worker, or repository result cannot supply or widen this write set.

## 5. Claim semantics

Shared mutation ownership is a **run-scoped currentness claim**, not a time-based optimistic lock.

Required properties:

- one active owner per resource key;
- multi-resource acquisition is atomic as a bundle;
- replay by the same run/Work Packet is idempotent;
- a different nonterminal run cannot seize the resource;
- monotonic fencing identity prevents stale release/transfer;
- terminal/invalidation transition releases the run's claims deterministically;
- a crashed process may recover the same durable run and retain its claim;
- time passage alone is not permission to take over a nonterminal owner's claim;
- transfer requires prior owner terminal/released/superseded truth plus new current authority.

The existing generic TTL lease primitive may continue serving other bounded uses, but blind TTL expiry is not sufficient proof for shared-mutation ownership.

## 6. Parallelism rule

Parallelism is permitted when declared write sets do not overlap.

The first safe implementation may serialize an entire declared repository surface when that is what current owner authority declares. Finer same-repository parallelism must be earned by declaring narrower consequential authority/provider/runtime surfaces and proving their independence; it must not be inferred from different filenames alone.

The repository execution fabric already creates isolated workspaces per admitted Work Packet. Matrix coordination therefore does not create a second worktree-lock system.

## 7. Fail-closed behavior

If coordination state is unavailable, inconsistent, stale, or cannot be atomically admitted:

- consequential autonomous mutation is blocked;
- read-only observation/diagnosis may continue when current authority permits;
- safe independent lanes with disjoint admitted write sets may continue;
- ordinary autonomous work may not bypass the Matrix/Controller path.

Recovery of the coordination gateway is a separately governed control-plane operation through Paths/Path Authority or the owning infrastructure authority. Recovery restores the same coordination authority; it is not an alternate product-mutation route.

## 8. Operational Matrix projection

Controller may expose a read-only live projection composed from existing state, for example:

- resource key;
- owner run ID;
- Work Packet ID;
- authority version;
- fencing identity;
- acquired/observed time;
- run state;
- currentness/invalidation status.

PROGRAMSTART parity/Decision-Closure references may be joined for display or reasoning.

The projection is not the mutation claim itself and is never sufficient authorization for a consumer to mutate. Consequential admission must be checked transactionally against Controller-owned current state.

## 9. Relationship to the existing Autonomy Parity Matrix

`config/autonomy-parity-contract.json` remains the machine-readable static capability/acceptance contract.

`docs/AUTONOMY_PARITY_MATRIX.md` remains its generated human-readable projection.

Neither becomes the live claim store.

The broader logical **Ecosystem Matrix** may compose:
- static PROGRAMSTART parity/behavior truth;
- Decision-Closure semantic receipts/references;
- live Controller run/claim state;
- owner authority/currentness references;
- Paths availability/recovery state.

Composition does not collapse ownership.

## 10. Acceptance cases

Before claiming this contract implemented for a mutation path, prove at least:

1. two independently admitted runs with the same write-set resource cannot both reserve mutation;
2. disjoint write sets can reserve independently;
3. replay/restart of the current owner remains idempotent;
4. a different run cannot take ownership merely because time passed;
5. terminal/invalidation releases claims and a later run receives a higher fencing identity;
6. stale release/transfer fails closed;
7. a malformed/missing write set blocks mutation;
8. stale owner authority blocks admission;
9. the operational projection reports active claims without becoming mutation authority;
10. gateway unavailability blocks mutation while read-only/recovery semantics remain truthful.

## 11. Scope of first implementation

The first implementation target is the existing Controller repository-effect admission path because it already provides:

- sealed PROGRAMSTART Work Packet persistence;
- current authority revalidation;
- atomic execution-attempt reservation;
- isolated repository workspaces;
- durable run state.

After this path is proven, other mutation-producing Controller actions must either consume the same coordination admission or be explicitly classified as non-mutating/read-only before ecosystem-wide mandatory-ingress closure can be claimed.
