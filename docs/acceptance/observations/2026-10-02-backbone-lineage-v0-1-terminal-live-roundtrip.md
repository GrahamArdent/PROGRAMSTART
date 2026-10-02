# Backbone Lineage V0.1 — Terminal Live Round-Trip Acceptance

Date: **2026-10-02**
Status: **LIVE ROUND-TRIP PROVEN**

## Accepted releases

- Controller: `5476a11792badad0d1ee48d18d6e24adf739efa3`
- Compute Spine worker bridge: `737edd2e184958f735117d14be3965d4ba6ba74d`
- PROGRAMSTART architecture/implementation acceptance: `6991d968283fd159beca94e000f6f404b8ae8473`

All release activation used the existing typed `controller_release_update_local` broker. Compute reported `ALREADY_CURRENT` on the final Controller releases.

## Fresh private-ingress proof

Request:

`req-programstart-objective-lineage-terminal-20261002133747`

Transport:

- `tailscale_private_http_v1`
- source node admitted by existing hash-only policy
- semantic Controller/Compute ingress: `local_unix_socket`
- Git not used as semantic Controller/Compute ingress
- no operator intervention required
- no secret values exported

Fresh identities:

- root: `root-fb6dca81e9cd1ff86dcd1e9d`
- run: `intent-25dc42da12ce3254`
- Work Packet: `WPK-25dc42da12ce3254`
- lineage: `lineage:controller:fb6dca81e9cd1ff86dcd1e9dae5f325d`
- root objective ref: `controller:run:intent-25dc42da12ce3254:objective`
- root record: `controller-run-created:fb6dca81e9cd1ff86dcd1e9dae5f325d`

## Durable Controller request record

Event:

- event id: `194`
- type: `lineage_effect_request`
- request: `req-vps-worker-controller-capability-082a488a998274a6c440`
- record: `controller-effect-request:60ccb8a8f4565f2dacc47f1f7eef2eb1`
- caused by: `controller-run-created:fb6dca81e9cd1ff86dcd1e9dae5f325d`
- producer owner: `GrahamArdent/programstart-autonomous-controller`
- execution authority: `false`

The request record was persisted before transport.

## Durable Compute result record

Event:

- event id: `195`
- type: `lineage_effect_result`
- request: `req-vps-worker-controller-capability-082a488a998274a6c440`
- record: `compute-parent-result:83fbe4806b93e9474dc01d3938693e8e`
- caused by: `controller-effect-request:60ccb8a8f4565f2dacc47f1f7eef2eb1`
- producer owner: `GrahamArdent/programstart-compute-spine`
- producer ref: `compute:parent-result:req-vps-worker-controller-capability-082a488a998274a6c440:sha256:e54dde4e48d33ac1256c64f504dd1198f8bd18df09f0d2cf6cfdedfbb0a7a161`
- execution authority: `false`

Controller persisted this result only after verifying that its causal parent was an already-durable Controller lineage request record.

## Proven causal chain

```text
controller-run-created:fb6dca81e9cd1ff86dcd1e9dae5f325d
  -> controller-effect-request:60ccb8a8f4565f2dacc47f1f7eef2eb1
  -> compute-parent-result:83fbe4806b93e9474dc01d3938693e8e
```

All three records preserve:

- lineage `lineage:controller:fb6dca81e9cd1ff86dcd1e9dae5f325d`
- root objective `controller:run:intent-25dc42da12ce3254:objective`
- `execution_authority=false`

No conversational/manual correlation is required to join the three records.

## Non-authority and EN boundary

The deployed Compute release is exactly the accepted #128 implementation. Its parent protocol:

- requires `execution_authority=false`;
- rejects unknown/smuggled lineage fields;
- creates a Compute-owned causal result record;
- deliberately does **not** copy lineage into the Execution Node child request.

Exact-head Compute tests proving the EN child request remains lineage-free passed before merge and the exact tested commit is the deployed release.

The terminal live proof exercised the same deployed parent protocol and returned the Compute-owned causal result above.

## Fail-closed observations earned during proof

The proof sequence also exercised useful failure behavior:

1. a read-only request classified as `audit` failed closed before Controller admission rather than widening authority;
2. a stale release request was rejected by expected-current currentness;
3. a transient stale worker supplementary-group process failed before broker mutation and succeeded only after the durable unit identity was active;
4. optional lineage projection was corrected so projection failure cannot alter semantic outcome;
5. Controller result persistence rejects a Compute lineage result whose `caused_by` parent is not a durable Controller request.

## Acceptance

### PASS

Backbone Lineage V0.1 has now been demonstrated on a fresh real semantic objective through:

`private semantic ingress -> Controller durable root -> durable Controller status request -> deployed Compute parent protocol -> durable Compute causal result -> Controller verification/persistence -> non-authoritative lineage projection`

This proves the first bounded cross-owner live propagation slice.

### Explicitly not claimed

This acceptance does **not** claim:

- lineage propagation through repository PREPARE/WORK/PUBLISH;
- lineage propagation into Execution Node;
- Watchtower/Paths/Matrix/Evidence Spine adoption;
- mandatory lineage for legacy callers;
- historical backfill;
- authority from lineage metadata;
- terminal completion of unrelated Controller #227 acceptance conditions.

## PROGRAMSTART Challenge

The live result falsifies the earlier concern that a new lineage service/database/state machine was required.

The smallest implementation remains owner-local:

- Controller existing SQLite run/event ledger;
- existing Controller -> Compute status observation;
- existing Compute parent protocol;
- reference-only projection in private ingress evidence.

**Decision: ACCEPT V0.1 first live slice.**

Further propagation requires a separate objective/Challenge and must be justified by a real reconstruction need rather than generalized rollout pressure.
