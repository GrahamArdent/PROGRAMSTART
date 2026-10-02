# Backbone Lineage V0.1 — First Live Adoption File-Level Plan

Date: **2026-10-02**
Owner: **GrahamArdent/PROGRAMSTART**
Status: **PROGRAMSTART-challenged implementation plan**
Mutation performed by this plan: **NO**

## 1. Fresh owner-local discovery

Discovery used current repository heads plus read-only filesystem inspection of exact owner worktrees.

Observed heads at discovery:

- Controller: `1dab161a4db9a5193318a0272e150f9c3adbc291`
- Compute Spine: `ad14bf983ecb036b41029bc18b77e9b4dd5a0b2b`
- PROGRAMSTART design base: `16cd1bba51db78b829dbabe8c688f295c35f98e0`

Open-PR collision check:

- Controller: no open PRs.
- Compute: open PR #125 touches only `spine/github_pr_integration_adapter.py` and its test; #50 touches only repository-create adapter/test; #39 touches VPS readiness docs/script/test.
- None overlaps the proposed first-slice files below.

## 2. Exact current seams

### Controller durable root

`controller/model.py`

`RunRecord` currently carries:

- `run_id`
- `project_repository`
- `objective`
- `work_packet_id`
- Controller/authority versions
- state/timestamps

`controller/store.py`

`SQLiteControllerStore.create_run()` transactionally creates the `runs` row and `run_created` event.

This is the correct mint/bind point. It is already restart-durable and occurs before downstream consequence execution.

### Controller typed-effect seam

For the first observation-only fixture, use the existing Stage 0.5 Compute execution contract rather than repository PREPARE/WORK/PUBLISH mutation paths.

The first implementation must locate/use the current Controller builder/caller for that existing Stage 0.5 `verify_repo_state` envelope. If current Controller main no longer owns such a caller directly, implementation must add only a bounded adapter to the existing Compute Stage 0.5 contract; it must not repurpose repository mutation clients.

### Compute contract

`spine/contracts.py`

Strictly validates the Stage 0.5 execution envelope and rejects unknown fields.

`schemas/execution-envelope.schema.json`

Defines the machine envelope.

`schemas/job.schema.json`

Defines the read-only `verify_repo_state` job.

`spine/worker.py`

`execute_stage05()` is genuinely read-only and creates evidence through `_base_evidence()`.

`schemas/evidence.schema.json`

Defines the strict returned evidence shape.

Focused tests already exist in:

- `tests/test_contracts.py`
- `tests/test_worker.py`

## 3. Minimal patch surfaces

### Controller

Expected files:

1. `controller/model.py`
   - add durable correlation fields to `RunRecord` only if needed for typed access.

2. `controller/store.py`
   - add backward-compatible `runs` columns for `lineage_id`, `root_objective_ref`, and root lineage `record_id`;
   - migrate existing databases without rewriting historical runs;
   - mint deterministic/stable lineage once at `create_run()`;
   - include the correlation binding in `run_created` details;
   - preserve values on reload/restart.

3. exact current Stage 0.5 request builder/caller file discovered at implementation preflight
   - attach a bounded `lineage` object to the existing execution envelope;
   - no change to authority selection/admission.

4. focused Controller tests
   - create/reload stability;
   - distinct roots get distinct lineage IDs;
   - retries/runs for same durable root do not silently remint within one admitted root;
   - forged lineage cannot affect authority/admission;
   - legacy DB migration.

### Compute Spine

Expected files:

1. `schemas/execution-envelope.schema.json`
   - add optional `lineage` object for V0.1 adoption;
   - legacy envelopes remain valid.

2. `spine/contracts.py`
   - validate exact bounded lineage fields;
   - reject unknown lineage fields;
   - require `execution_authority=false`;
   - no lineage input participates in `admit_stage05`.

3. `spine/worker.py`
   - copy validated correlation into returned evidence;
   - create a Compute-produced result `record_id`;
   - `caused_by[]` contains the Controller producer record;
   - no authority behavior changes.

4. `schemas/evidence.schema.json`
   - add optional returned lineage object;
   - legacy evidence remains valid.

5. `tests/test_contracts.py`
   - valid lineage accepted;
   - forged `execution_authority=true` rejected;
   - arbitrary lineage payload/command rejected;
   - missing lineage remains valid.

6. `tests/test_worker.py`
   - lineage round trip;
   - Compute result gets a new record ID;
   - root identity preserved;
   - admission outcome identical with/without lineage;
   - read-only/zero-cost/worktree invariants unchanged.

## 4. Proposed wire shape

The first live wire object is intentionally smaller than the full reconstruction graph:

```json
{
  "contract_version": "0.1",
  "lineage_id": "<stable Controller-root lineage>",
  "root_objective_ref": "<durable root reference>",
  "record_id": "<Controller request record>",
  "caused_by": ["<prior record>"],
  "producer_owner": "GrahamArdent/programstart-autonomous-controller",
  "producer_record_ref": "<durable Controller record ref>",
  "execution_authority": false
}
```

Compute result returns the same root correlation but replaces:

- `record_id` with a Compute-owned result record;
- `producer_owner` with `GrahamArdent/programstart-compute-spine`;
- `producer_record_ref` with the native Compute evidence reference;
- `caused_by[]` with the received Controller request record.

## 5. Migration rule

No historical backfill.

Existing Controller databases gain nullable lineage columns.

Existing runs with no lineage remain legacy/unprojected until a separate explicitly authorized migration decision exists.

Newly admitted roots after activation receive lineage.

This prevents fabricated historical causality.

## 6. Authority non-interference test

The implementation must prove:

```text
admit(effect, native_request, no_lineage)
==
admit(effect, native_request, valid_lineage)
```

and:

```text
admit(effect, unauthorized_native_request, forged_lineage)
==
DENY
```

No code path may read lineage when deciding:

- consequence permission;
- repository/provider target;
- credentials;
- approval;
- currentness;
- budget/network policy;
- PREPARE/WORK/PUBLISH admission;
- retry permission.

## 7. First live proof

Use a fresh harmless Stage 0.5 `verify_repo_state` observation.

Acceptance requires:

1. one new Controller root with durable lineage;
2. restart/reload returns same lineage;
3. exact typed Compute request carries lineage;
4. Compute evidence echoes root correlation with a new result record;
5. zero mutation / zero cost / clean worktree proof remains true;
6. Controller can reconstruct root -> request -> evidence without prose;
7. same observation without lineage still passes as legacy behavior;
8. forged authority-bearing lineage fails contract validation;
9. exact-head tests pass in both repos;
10. owner-native PRs remain collision-free.

## 8. PROGRAMSTART Challenge

### Evidence validity

**PASS.** Exact current files were inspected, not inferred from repository naming.

### Scope integrity

**PASS after one correction.**

Do not use `controller/compute_spine_repository_client.py` for the first proof merely because it already has an execution-attempt ledger. That path owns repository PREPARE/WORK/PUBLISH effects and would unnecessarily couple lineage adoption to mutation-capable semantics.

Use the read-only Stage 0.5 observation contract first.

### Collision

**PASS at discovery time.**

No current open Controller PR. Current Compute open PRs do not touch proposed Stage 0.5 contract/worker files.

Recheck immediately before branch creation.

### Schema compatibility

**PASS if lineage is optional for V0.1 adoption.**

Mandatory lineage would break legacy callers and is not yet earned.

### Migration

**PASS if nullable/no-backfill.**

Retroactive synthesized lineage is prohibited.

### Authority

**PASS only with non-interference tests.**

The strongest test is behavioral equivalence of native admission with and without valid lineage.

### Failure/retry

**PASS if stable root correlation is persisted before transport.**

Downstream retry must reuse root lineage; effect-attempt identity remains native.

## 9. GO / NO-GO

### GO for implementation, subject to immediate currentness recheck

A bounded two-repository implementation is now sufficiently specified to mutate:

- Controller durable run binding + exact Stage 0.5 envelope producer;
- Compute Stage 0.5 envelope validation + evidence echo;
- focused tests only.

### NO-GO for broader propagation

Do not include:

- repository PREPARE/WORK/PUBLISH effects;
- Paths;
- Watchtower;
- Execution Node;
- Matrix;
- Evidence Spine;
- historical backfill;
- mandatory lineage across all callers.

## 10. Stop conditions

Stop before mutation if:

- Controller/Compute main moved and invalidates inspected seams;
- a new PR owns any exact planned file;
- the Stage 0.5 Controller producer cannot be located without introducing a new execution path;
- implementation would require lineage to influence authority;
- backward compatibility cannot be preserved;
- more than the bounded two-owner slice is required merely to prove round-trip correlation.
