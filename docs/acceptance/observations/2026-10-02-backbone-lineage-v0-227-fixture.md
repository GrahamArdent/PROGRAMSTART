# Backbone Lineage V0 — #227 Schema / Fixture Challenge

Date: **2026-10-02**
Owner: **GrahamArdent/PROGRAMSTART**
Scope: **schema + fixture only; no runtime propagation**
Natural fixture: **GrahamArdent/programstart-autonomous-controller#227**

## Objective

Test whether the accepted Backbone End-to-End Information Flow Contract can be represented machine-readably with the smallest useful lineage model, using the real #227 history rather than designing from a blank sheet.

The protected property is:

> A fresh reader can reconstruct #227's causal path to the current first unsupported boundary from durable references, while missing/not-reached links remain explicit and the lineage representation cannot grant authority.

## Currentness used

At this pass:

- PROGRAMSTART main: `e3a909773327258321ec50313fbece5628cf9f42`
- Controller main: `d11ae41f18a05d5df5b5b90210e5688281e4516d`
- Paths main: `093b90c3d6429d376fc8dd7cbb8292e76827a0ec`
- Compute main: `a2ac6d31c1c1e2e12a2cee06a2e54640051a323e`
- Execution Node main: `36ab5891e2821ff962c0ab39b1bfd521872d9146`
- Controller #227: open
- Controller open PRs: none at preflight

The fixture is evidence-bound to these observations and must not be treated as live currentness after an invalidating change.

## Proposed V0 representation

The representation has two layers only:

1. a **lineage graph projection** containing one root objective, challenged coverage, bounded records and residuals;
2. **lineage records** that carry correlation/reference fields only.

The record core is:

- `record_id`
- `record_type`
- `producer_owner`
- `producer_record_ref`
- `caused_by[]`
- `root_objective_ref`
- `stage_projection[]`
- `execution_authority=false`

Decision-critical fields are optional references such as Work Packet, Controller root/run, semantic effect, realization, effect attempt, evidence, authority/currentness, terminal and reconsideration references.

There is no native payload copy and no universal runtime state field.

## Why a graph document rather than a runtime envelope

V0 is deliberately a **reconstruction projection**, not yet an on-wire format.

That makes the first test falsifiable without requiring any production owner to change its schema.

If this model cannot represent #227 truthfully as a read model, propagating it through Controller/Paths/Compute/EN would be premature.

## Challenge

### A — Authority / kill boundary

**CLEAR.**

The schema mechanically requires `execution_authority=false` at graph and record level.

No field can grant repository, provider, credential, merge, release or runtime authority.

### B — Evidence/currentness

**CLEAR WITH EXPLICIT INVALIDATION.**

The fixture binds current repository/issue evidence by exact durable refs where available.

It does not claim the graph remains current after owner records change.

### C — Scope integrity

**CLEAR AFTER NARROWING.**

Rejected from V0:

- runtime propagation;
- central lineage service/database;
- mutation of Controller/Paths/Compute/EN;
- universal native state enum;
- copied owner payloads;
- historical ecosystem backfill;
- credentials or private provider content;
- using lineage to choose a realization or authorize consequence.

### D — Skipped/deferred work

**EXPLICITLY DEFERRED.**

Not part of this slice:

- emitting lineage fields from live components;
- automatic graph construction;
- generic cross-repo lookup API;
- Matrix lineage rendering;
- Evidence Spine indexing;
- backfill/migration.

### E — Adversarial failure sequences

#### Failure 1 — false ER-012 consequence

A fixture could include proven Paths ER-012 and accidentally imply the fresh #227 run selected/executed it.

**Protection:** the fixture contains ER-012 only as evidence/reference; no lineage record claims `realization_ref=ER-012`, and a `not_reached` residual covers discovery/consequence.

#### Failure 2 — lineage grants authority

A consumer could treat a common lineage record as execution permission.

**Protection:** graph and every record require `execution_authority=false`; owner authority/currentness remain references.

#### Failure 3 — causal tree cannot express a join

The blocker classification depends on both the semantic run and typed diagnostic.

**Protection:** `caused_by[]` is plural and the fixture includes a real two-parent reconstruction record.

#### Failure 4 — dangling or cyclic causal graph

A malformed graph could produce misleading ancestry.

**Protection:** focused tests require all causal IDs to resolve and reject cycles/self-links.

#### Failure 5 — missing links get fabricated

A reader could fill in planned future stages because the intended architecture is known.

**Protection:** residuals are first-class; the current fixture explicitly stops before Paths selection/consequence.

#### Failure 6 — native payload duplication

A lineage layer could become another state store.

**Protection:** schema has `additionalProperties=false` and no arbitrary `payload`, command, provider, credential or native-result object.

#### Failure 7 — prerequisite capability becomes causal child of the objective

ER-012 predates #227 and was not caused by it.

**Protection:** the fixture references ER-012 as prerequisite evidence but does not place the native ER-012 record inside the objective's causal record set.

### F — Decision reversal

**NO REVERSAL.**

V0 implements the already-accepted contract's candidate lineage model as a bounded read projection.

### G — Dependency health

**CLEAR.**

Uses existing JSON Schema Draft 2020-12 tooling already present in PROGRAMSTART.

No new package or provider dependency is introduced.

### H — Architecture alignment

**CLEAR WITH RUNTIME GAP PRESERVED.**

The schema demonstrates representability only. It does not claim the backbone now emits or consumes lineage.

## GO / NO-GO

### GO

- persist `schemas/backbone-lineage.schema.json`;
- persist the #227 fixture;
- persist focused schema/causal-integrity tests;
- register the new PROGRAMSTART assets;
- run the exact-head Required PR Gate.

### NO-GO

Do not wire lineage into live Controller/Paths/Compute/EN from this slice.

## Acceptance

This slice is accepted only if:

1. JSON Schema itself validates;
2. #227 fixture validates;
3. execution authority cannot be set true;
4. causal references resolve;
5. causal graph is acyclic;
6. a real multi-parent join is represented;
7. root objective stays stable;
8. fixture does not falsely claim ER-012 selection/consequence;
9. unearned payload/command fields fail;
10. challenged coverage requires evidence;
11. Required PR Gate passes on exact head.

Passing these proves **representability**, not runtime implementation.
