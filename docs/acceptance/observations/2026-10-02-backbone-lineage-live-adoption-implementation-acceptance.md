# Backbone Lineage V0.1 — First Live Adoption Implementation Acceptance

Date: **2026-10-02**
Status: **owner-native implementation merged; live runtime proof pending**

## Accepted owner merges

### Compute Spine

PR: `GrahamArdent/programstart-compute-spine#128`

Merged main: `737edd2e184958f735117d14be3965d4ba6ba74d`

Exact candidate: `36fbda254021cdca04348b3938fea8638637645e`

CI: **PASS**

Accepted behavior:

- optional strict V0.1 lineage on the existing Compute parent protocol;
- `execution_authority=false` required;
- arbitrary/smuggled lineage fields rejected;
- lineage is not forwarded into the Execution Node child request;
- Compute creates a new causal lineage record on parent evidence;
- legacy parent requests without lineage remain valid.

### Autonomous Controller

PR: `GrahamArdent/programstart-autonomous-controller#241`

Merged main: `93d71f3f9219b719fbc3ade316e647ff4ec19195`

Exact candidate: `850d2fcd00fe683007ea3f91fbd282f1bd6efdcb`

CI:

- controller-ci Python 3.12: **PASS**
- controller-ci Python 3.13: **PASS**
- contextual-runtime: **PASS**

Accepted behavior:

- Controller run admission mints a stable correlation-only lineage identity;
- lineage/root/record binding is persisted in the existing Controller SQLite run state;
- DB reopen/restart preserves the binding;
- existing databases gain nullable columns with no historical backfill;
- existing read-only status observation can optionally carry the lineage envelope;
- returned Compute lineage is checked for root identity, causal parent and non-authority;
- legacy status observation remains lineage-free/compatible.

## Challenge corrections preserved

The original file plan proposed Compute Stage 0.5 `verify_repo_state`.

JIT discovery proved Controller had no existing producer for that contract.

The implementation correctly stopped and reused the already-existing:

`Controller compute_spine_capability_client -> Compute worker_bridge_agent execution_node_observe/status`

boundary instead.

No new execution path was introduced.

## Runtime status

**NOT YET PROVEN LIVE.**

Merge proves source/test acceptance only.

No claim is made yet that deployed Controller/Compute runtime is at the merged commits or that a fresh live lineage round trip has occurred.

## Next bounded gate

1. observe current deployed Controller and Compute release/currentness;
2. determine the existing owner-native release/update path for each changed component;
3. activate only if current authority permits and no newer incompatible head supersedes these merges;
4. submit one fresh harmless Controller status observation with a newly admitted root lineage;
5. prove:
   - same lineage survives Controller persistence/reload;
   - Compute receives it;
   - EN child request remains lineage-free;
   - Compute parent evidence returns a new record caused by the Controller record;
   - Controller verifies the returned lineage;
   - observation remains read-only and authority behavior is unchanged;
6. persist owner-native proof;
7. reconcile PROGRAMSTART lineage acceptance.

Runtime activation beyond those exact components is not authorized by this acceptance record.
