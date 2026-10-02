# Backbone Lineage V0.1 — Smallest Owner-Native Live Adoption Design

Date: **2026-10-02**
Owner: **GrahamArdent/PROGRAMSTART**
Mode: **architecture/design only**
Runtime mutation authorized by this document: **NO**

## 1. Decision

The smallest justified live adoption slice begins at **Controller durable root admission** and crosses exactly **one existing typed effect/evidence boundary**.

Controller is the first lineage minter because it is the earliest current owner that simultaneously has:

- the accepted semantic/root objective identity;
- the durable Controller root/run identity;
- the current Work Packet / protected-outcome context;
- admission authority for the next bounded consequence.

No new service, registry, database, lifecycle owner or authority surface is introduced.

The first downstream owner does **not** mint a new lineage identity and does **not** infer execution authority from lineage. It only persists/echoes bounded correlation fields with its native request/result evidence.

## 2. Why this is the smallest earned slice

Two independent natural fixtures now expose the same reconstruction gap:

- **Controller #227**: the semantic root/run and typed Compute diagnostic are durable, but their causal relation requires prose/manual archaeology.
- **Controller #71**: the durable wait/provider evidence/reconsideration chain is reconstructable, but cross-owner event correlation is preserved primarily in terminal narrative evidence rather than common emitted lineage fields.

The common missing capability is therefore not another state machine. It is a durable causal correlation edge across an already-authorized owner boundary.

## 3. Minting rule

### 3.1 Minter

**Controller** mints `lineage_id` exactly once when a semantic/root objective becomes durably admitted into a native Controller root.

### 3.2 Stability

The lineage identity MUST:

- remain stable across retries, reconsideration, waits and owner handoffs for the same root objective;
- not be regenerated for each Work Packet, run, effect attempt or provider event;
- not be reused across distinct root objectives;
- be recoverable from durable Controller state after restart;
- be correlation-only.

### 3.3 Root binding

At mint/admission time, Controller durably binds at minimum:

- `lineage_id`;
- `root_objective_ref`;
- native Controller root identity;
- first lineage `record_id`;
- `producer_record_ref`;
- `execution_authority=false`.

Work Packet/run references may be added when they exist, but they are not allowed to redefine the lineage root.

## 4. First emitted causal edge

The first live cross-owner envelope SHOULD be emitted only when Controller sends an already-authorized **existing typed effect request**.

Minimum correlation projection:

```json
{
  "contract_version": "0.1",
  "lineage_id": "<stable-root-lineage>",
  "root_objective_ref": "<durable-root-ref>",
  "record_id": "<controller-produced-record>",
  "caused_by": ["<prior-record-id>"],
  "producer_owner": "GrahamArdent/programstart-autonomous-controller",
  "producer_record_ref": "<durable-controller-record-ref>",
  "execution_authority": false
}
```

This is not a replacement for the typed request. It is bounded correlation metadata adjacent to the owner-native request.

## 5. First downstream behavior

The selected downstream owner MUST:

1. validate only the lineage envelope's syntax/version as correlation metadata;
2. never use lineage fields to satisfy mutation, provider, credential, repository, release or consequence authority;
3. persist the received correlation with its native request/effect-attempt record;
4. emit a new native lineage `record_id` for its result/evidence;
5. set `caused_by[]` to the received producer record;
6. preserve the same `lineage_id` and `root_objective_ref`;
7. return its own `producer_record_ref`;
8. keep `execution_authority=false`.

The downstream owner remains authoritative only for its existing native state and consequence.

## 6. First boundary selection

The first implementation fixture SHOULD use a **Controller -> existing typed Compute effect -> typed evidence return** boundary rather than Watchtower/Paths first.

Reasons:

- #227 already exposed the exact missing correlation between Controller semantic run and typed Compute evidence;
- Compute already returns typed durable request/result evidence;
- the boundary is synchronous/bounded enough to isolate lineage behavior;
- it avoids mixing the first propagation experiment with async provider delivery, Watchtower restart semantics or Paths realization selection;
- no new consequence type is required.

The first fixture SHOULD use a harmless observation/read-only typed effect, not a mutation effect.

## 7. Currentness / invalidation

Lineage correlation itself does not become stale merely because owner state advances.

Individual lineage records MUST reference owner-native currentness/invalidation evidence when the semantic conclusion depends on freshness.

Rules:

- `lineage_id` is stable historical correlation;
- `record_id` is immutable event/record identity;
- owner-native evidence/currentness determines whether a record still supports a current conclusion;
- a stale record remains part of history but MUST NOT satisfy current admission;
- lineage propagation MUST NOT bypass consequence-time JIT/currentness checks.

## 8. Non-authority guarantee

The following invariant is mandatory:

> Possession, propagation, persistence or successful validation of lineage metadata grants **zero execution authority**.

Specifically, lineage MUST NOT:

- authorize repository mutation;
- authorize a provider/effect/realization;
- authorize credentials;
- satisfy Controller PREPARE/WORK/PUBLISH admission;
- satisfy owner JIT/currentness;
- select Paths realizations;
- terminalize an objective;
- suppress a human gate;
- replace protected-outcome validation.

If removing all lineage metadata would cause an otherwise unauthorized consequence to become denied differently, the implementation has coupled correlation to authority and MUST fail acceptance.

## 9. Failure semantics

### Missing lineage

For the first bounded adoption slice, legacy callers without lineage remain behaviorally unchanged.

No global hard requirement is introduced yet.

### Malformed lineage

The typed owner may reject or omit lineage correlation according to the bounded experiment contract, but MUST NOT reinterpret malformed lineage as authority.

### Retry

Retry of the same native effect attempt preserves the root lineage and causal parent. Attempt identity remains owner-native.

### Duplicate evidence

Duplicate result/evidence MUST NOT create a new semantic consequence merely because it carries valid lineage.

### Owner handoff

A foreign owner echoes root correlation while retaining its own native authority and lifecycle.

## 10. Acceptance test

A fresh test objective through the selected Controller -> Compute observation boundary passes only if:

1. Controller mints one stable lineage identity at durable root admission;
2. restart/reload preserves the same identity;
3. the typed effect request carries the bounded correlation envelope;
4. Compute persists/returns the same root lineage without treating it as authority;
5. Compute result has a new record identity caused by the Controller request record;
6. Controller evidence/reconsideration can resolve the result from lineage without prose/manual archaeology;
7. existing authority/JIT/admission checks are unchanged;
8. a forged lineage envelope cannot authorize the effect;
9. missing lineage preserves legacy behavior for out-of-scope callers;
10. no secret/private native payload is copied into lineage;
11. cold reconstruction from `lineage_id` reaches root -> typed request -> typed result;
12. exact-head owner-native tests and PROGRAMSTART acceptance evidence pass.

## 11. PROGRAMSTART Challenge

### A — authority

**CLEAR if implemented exactly as bounded above.**

Lineage is correlation-only and explicitly excluded from all execution admission.

### B — evidence

**CLEAR.**

The design is derived from two accepted natural fixtures rather than hypothetical completeness.

### C — scope

**CLEAR after narrowing.**

Rejected for the first live slice:

- global propagation across all owners;
- Watchtower/provider async propagation;
- Paths realization propagation;
- Matrix projection;
- Evidence Spine indexing;
- historical backfill;
- mandatory lineage for legacy callers;
- new lineage service/database.

### D — failure challenge

#### Forged lineage

Must not change authorization outcome.

#### Missing lineage

Must not break legacy/out-of-scope callers.

#### Retry/restart

Must preserve the same root identity.

#### Duplicate evidence

Must not cause duplicate semantic continuation.

#### Stale evidence

Must remain historical but fail currentness where currentness is required.

#### Cross-owner handoff

Must preserve correlation without authority transfer.

#### Payload leakage

Only bounded references may propagate; no secrets/full owner payloads.

### E — reversal

**NO REVERSAL.**

This is the smallest implementation candidate of the already-accepted reference-first causal DAG architecture.

### F — dependency health

**CLEAR.**

No external runtime dependency is required for the first slice.

### G — architecture alignment

**CLEAR WITH IMPLEMENTATION GAP.**

Current Controller/Compute native schema locations still need owner-local implementation discovery before code mutation.

## 12. GO / NO-GO

### GO

Proceed to a **read-only owner-local implementation discovery** in Controller and Compute to identify:

- exact durable root/admission model;
- exact typed request model;
- exact typed result/evidence model;
- serialization/storage points;
- focused tests;
- collision/write ownership.

Then return a file-level implementation plan and re-challenge it before mutation.

### NO-GO

Do not mutate Controller or Compute directly from this architecture document.

Do not broaden to Watchtower, Paths, EN, Matrix or Evidence Spine in the first live adoption slice.
