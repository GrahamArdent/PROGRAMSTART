# PROGRAMSTART Challenge — First Live Lineage File-Level Patch Plan

Date: **2026-10-02**
Decision: **GO for bounded implementation after immediate currentness/collision recheck**

## Inputs challenged

- accepted Backbone Lineage V0.1 architecture;
- Controller #227 sequential fixture;
- Controller #71 async fixture;
- current Controller durable run/store implementation;
- current Compute Stage 0.5 execution-envelope/job/evidence implementation;
- current open PR write sets.

## Findings

1. Controller already has the correct durable mint point: transactional `create_run()` plus `run_created`.
2. Compute already has a strict read-only effect/evidence contract suitable for a first propagation proof.
3. A new lineage database is unnecessary.
4. Repository PREPARE/WORK/PUBLISH is too broad for the first proof despite having an existing attempt ledger.
5. Optional lineage preserves legacy callers.
6. Nullable Controller migration with no backfill preserves historical truth.
7. Current open PRs do not collide with the proposed Stage 0.5 Compute files; Controller currently has no open PR.

## Adversarial challenge

- **Forged authority:** must fail because lineage requires `execution_authority=false` and is excluded from admission logic.
- **Missing lineage:** must retain legacy Stage 0.5 behavior.
- **Unknown fields:** strict validation rejects payload/command smuggling.
- **Restart:** Controller persisted root binding must survive DB reopen.
- **Retry:** root lineage remains stable while native attempt identity remains separate.
- **Stale native authority:** lineage cannot override existing currentness checks.
- **Historical runs:** no synthetic backfill.
- **Scope creep:** first proof is read-only Stage 0.5 only.

## Decision

**GO** for the bounded implementation after a just-in-time head/PR recheck.

Any need to touch Paths, Watchtower, Execution Node, Matrix, Evidence Spine, repository mutation clients, provider adapters, or historical data is a **STOP / re-Challenge** condition.
