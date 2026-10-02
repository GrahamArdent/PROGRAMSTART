# PROGRAMSTART Re-Challenge — First Live Lineage Boundary Correction

Date: **2026-10-02**
Status: **GO after stop-condition correction**

## Trigger

The file-level plan selected Compute Stage 0.5 `verify_repo_state` as the first read-only propagation fixture.

Just-in-time Controller inspection proved that Controller does **not** currently produce that Stage 0.5 envelope.

The plan explicitly required STOP rather than creating a new execution path.

## Existing reusable boundary discovered

Controller already owns:

`controller/compute_spine_capability_client.py`

with:

- `build_status_parent_request()`;
- `run_status_observation()`;
- fixed parent action `execution_node_observe`;
- fixed worker action `status`;
- Class-0/read-only semantics;
- current typed result verification.

Compute already owns the matching public parent protocol in:

`spine/worker_bridge_agent.py`

with:

- strict `EXPECTED_FIELDS`;
- exact observation allow-list;
- durable parent request state;
- bounded child dispatch;
- Compute-owned parent result builders for success/failure/uncertain delivery.

The Compute parent result is a sufficient first evidence-return boundary. Lineage does **not** need to propagate into the Execution Node child request for this slice.

## Corrected first live slice

### Controller

1. mint/bind stable lineage at `SQLiteControllerStore.create_run()`;
2. expose it through `RunRecord`;
3. allow `build_status_parent_request()` / `run_status_observation()` to receive one bounded optional lineage envelope from the admitted Controller root;
4. verify returned Compute parent-result lineage.

### Compute

1. allow exactly one optional top-level `lineage` field on the existing parent protocol;
2. validate its fixed V0.1 shape and require `execution_authority=false`;
3. do not copy lineage into the EN child request;
4. emit a Compute-owned result lineage record in success/failure/uncertain parent results;
5. bind the result record causally to the received Controller record;
6. preserve legacy parent requests without lineage unchanged.

## Why this is smaller

This reuses a currently deployed Controller -> Compute -> EN observation path but changes lineage only at the Controller/Compute ownership boundary.

Execution Node receives the same child request as before.

Therefore the first experiment tests cross-owner lineage without adding a third owner or modifying consequence semantics.

## Challenge

- New execution path introduced: **NO**
- New consequence type: **NO**
- EN schema/runtime mutation: **NO**
- Authority widening: **NO**
- Legacy callers broken: **NO, lineage optional**
- Existing observation action changed: **NO**
- Cross-owner causal edge added: **YES, Controller -> Compute parent evidence**
- Stop condition respected: **YES**

## GO / NO-GO

**GO** for bounded implementation on the already-created Controller and Compute feature branches, subject to the already-passed currentness/collision check.

**NO-GO** for passing lineage into the Execution Node child request in this slice.
