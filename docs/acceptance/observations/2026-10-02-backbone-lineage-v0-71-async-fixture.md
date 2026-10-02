# Backbone Lineage V0.1 — Independent Async Fixture Challenge (#71)

Date: **2026-10-02**
Owner: **GrahamArdent/PROGRAMSTART**
Schema under test: `schemas/backbone-lineage.schema.json`
Independent natural fixture: `GrahamArdent/programstart-autonomous-controller#71`
Mode: **read-only reconstruction / no runtime propagation**

## Objective

Challenge Backbone Lineage V0.1 against a materially different causal shape from Controller #227.

#227 primarily exercised a sequential semantic-objective / repair / evidence chain with an explicit not-reached boundary.

#71 exercises:

- a durable machine-evidence wait;
- a separate sensor owner;
- a subordinate restart/recovery dependency;
- external provider events arriving after the semantic owner is detached;
- exact wait/event joins;
- semantic reconsideration;
- retained-wait progression across more than one event;
- terminal cleanup after existing continuation;
- explicit absence of conversational/human transport.

The test question is:

> Can V0.1 represent this async/event-driven chain truthfully without adding event-specific or wait-specific global fields, copying native payloads, or granting authority?

## Preflight / collision check

At fixture start:

- PROGRAMSTART main: `6148573f3cdb3a5ada29555794f8965ee72b75be`;
- Controller #71: closed / terminal owner acceptance recorded;
- Watchtower #16: terminal owner acceptance recorded;
- Execution Node #302: closed / typed restart acceptance recorded;
- PROGRAMSTART PR #195 remains a separate derived HOP/Matrix projection and does not own the lineage schema/fixture surfaces.

No Controller, Watchtower, Execution Node, provider, Matrix or runtime mutation is admitted by this fixture.

## Empirical causal shape

The accepted chain is reconstructed as:

```text
Controller #71 objective
    |
    v
sensor-currentness blocker
    |
    v
EN #302 controlled restart proof
    |
    v
Watchtower #16 terminal sensor acceptance
    |
    v
fresh Controller acceptance -> fail-closed packet identity conflict
    |
    v
Controller PR #232 bounded repair
    |
    v
exact release activation
    |
    v
fresh run + durable machine wait
    |
    +----------------------+
    |                      |
    |                provider event attempt 3
    |                      |
    +----------+-----------+
               v
       native reconsideration
       semantic_decision_required
               |
               +----------------------+
               |                      |
               |                provider event attempt 4
               |                      |
               +----------+-----------+
                          v
                 terminal reconsideration
                 PREPARE_EXECUTED
                          |
                          v
                 owner terminal acceptance
```

This is a causal DAG with real joins, not a linear trace.

## Challenge result

### A — Does V0.1 need a global `wait_ref`?

**NO.**

The wait is itself a typed lineage record:

- record type identifies machine-wait semantics;
- native wait identity remains in bounded owner evidence;
- Controller run and Work Packet references are already supported;
- downstream records cite the wait record through `caused_by[]`.

Adding a universal wait field would make a Controller-specific concept part of every lineage record without evidence that other owners need it.

### B — Does V0.1 need a global `provider_event_ref`?

**NO.**

Provider events are represented as typed evidence records with owner/currentness/evidence references.

The common contract needs causal identity, not provider-specific event structure.

### C — Can the graph represent async joins?

**YES.**

The first native reconsideration has two causes:

`durable wait + provider event attempt 3`.

The terminal reconsideration also has two causes:

`prior retained-wait state + provider event attempt 4`.

No schema extension is required.

### D — Does owner handoff transfer authority?

**NO.**

Execution Node and Watchtower records remain owned by their native repositories and carry `execution_authority=false`.

Their evidence returns into the Controller lineage without granting either owner Controller continuation authority.

### E — Can a prerequisite sub-objective retain the root objective?

**YES, as a reconstruction projection.**

EN #302 and Watchtower #16 retain their own native owners/authority. In this fixture their records also preserve #71 as the root lineage being reconstructed because their accepted evidence was a causal dependency of #71 closure.

This root reference is correlation only and does not redefine their native strategic roots.

### F — Does the fixture preserve fail-closed behavior?

**YES.**

The corrected fresh acceptance request exposed a durable Work Packet identity conflict.

That failed attempt is represented as evidence before PR #232; the graph does not skip directly from sensor acceptance to success.

### G — Does terminal cleanup imply arbitrary disappearance?

**NO.**

The terminal owner record states that current deployed code removes the wait only after existing continuation reports `acceptance=PASS` and `continuation_status=PREPARE_EXECUTED`.

The lineage graph therefore connects terminality to reconsideration/continuation evidence rather than mere absence of a wait.

### H — Does the schema need widening?

**NO.**

The existing V0.1 fields are sufficient.

This fixture earns a stronger conclusion than #227 alone:

> The common contract can represent both sequential blocked flows and async event-driven joins without introducing owner-specific fields.

## Residuals preserved

V0.1 still does **not** solve:

1. generic lookup from root objective to native Controller wait/snapshot state;
2. common emitted lineage fields across Watchtower and Controller;
3. automatic graph construction;
4. live propagation;
5. Matrix/Evidence-Spine indexing.

Those remain implementation/adoption questions, not schema defects.

## PROGRAMSTART Challenge

### Scope integrity

**CLEAR.**

This fixture adds no runtime behavior and makes no schema change.

### Authority

**CLEAR.**

Every graph/record remains mechanically non-authoritative.

### Counterfactual failure

If #71 required adding fields such as `wait_ref`, `workflow_run_id`, `delivery_id`, or `provider_event_type` to the common schema merely to describe this one owner-specific flow, V0.1 would be overfit/insufficient.

The fixture demonstrates those details can remain owner-native evidence referenced by typed records.

### Decision reversal

**NO REVERSAL.**

The result strengthens the existing reference-first / causal-DAG design.

## GO / NO-GO

### GO

Accept #71 as the second independent natural V0.1 fixture.

### NO-GO

Do not widen the schema.

Do not yet propagate lineage through live components merely because two fixtures validate.

## What this earns next

V0.1 has now survived two materially different natural shapes:

1. #227 — sequential semantic flow with repairs and an explicit `not_reached` boundary;
2. #71 — async event-driven flow with owner handoff, durable wait, multi-parent joins, reconsideration and terminal continuation.

That is sufficient to begin a **separate architecture/design pass** for the smallest owner-native propagation/adoption slice.

The next pass should determine:

- which existing component should mint the stable `lineage_id`;
- where `root_objective_ref` first becomes durable;
- which boundary should first emit `record_id / caused_by[] / producer_record_ref`;
- how to add lineage without changing execution authority;
- whether a single narrow Controller <-> Compute/Watchtower boundary is the safest first live adoption fixture.

No runtime propagation is authorized by this observation.
