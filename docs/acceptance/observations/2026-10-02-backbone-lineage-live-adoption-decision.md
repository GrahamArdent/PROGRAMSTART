# PROGRAMSTART Decision Record — Backbone Lineage First Live Adoption

Date: **2026-10-02**
Decision class: **architecture / implementation admission**
Status: **GO for read-only owner-local discovery; NO-GO for runtime mutation**

## Settled decision

Use Controller durable root admission as the first lineage minting boundary.

Use one existing Controller -> Compute typed observation/evidence boundary as the first live propagation candidate.

The lineage envelope is correlation-only. It never grants authority.

## Why

The accepted #227 and #71 fixtures differ substantially in runtime shape but expose the same reconstruction defect: cross-owner causal correlation is not emitted durably enough to reconstruct from machine-readable owner records without manual prose archaeology.

The narrowest repair is therefore one emitted causal edge, not a new lifecycle or storage authority.

## Challenge outcome

- Authority boundary: **PASS**
- Evidence basis: **PASS**
- Scope integrity: **PASS after narrowing**
- Collision risk: **NOT YET CLEARED for code mutation**
- Runtime dependency: **NONE introduced**
- Schema widening: **NOT EARNED**
- Backfill: **NOT REQUIRED**
- Live mutation: **NOT AUTHORIZED YET**

## Required next evidence

Before implementation:

1. locate the current Controller durable root/admission model;
2. locate the exact existing typed Compute request/evidence boundary;
3. locate serialization/storage and restart recovery points;
4. identify tests proving authority behavior is unchanged;
5. check current open PR/write ownership on those exact files;
6. produce a file-level patch plan;
7. run that plan through PROGRAMSTART Challenge.

Only after those seven items are current and collision-free may the first live adoption slice receive GO for mutation.
