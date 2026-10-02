# Consequence Execution V1 — Machinery Reconciliation

Status: evidence-backed implementation map for PROGRAMSTART PR #188. Not runtime authority; preparatory branches are not promoted to proven capability.

## Executive result
Consequence Execution V1 is primarily a **normalization/composition problem, not five greenfield subsystems**. Existing machinery already proves most safety primitives independently. The smallest missing center is a shared typed grant representation plus deterministic bridges that bind existing Controller authority/coordination, Paths realization evidence, Secrets capability satisfaction, bounded adapters, and durable result reconciliation.

## Reconciliation map
| Requirement | Class | Existing machinery | Smallest delta |
|---|---|---|---|
| grant identity/schema | ADAPT | sealed Work Packet schema/compiler, semantic digest/specification ID/fingerprint | provider-neutral consequence-grant projection; never second authority |
| authority ref/version/currentness | REUSE | `SealedWorkPacketRecord`, packet integrity, owner/currentness binding | normalized projection |
| consequence/effect | ADAPT | allowed/prohibited effects, semantic tokens; #50/#125 consequence/effect fields | standard vocabulary |
| target/resource scope | ADAPT | Work Packet mutable surfaces; fixed adapter targets | normalized fields |
| bounded operation | REUSE/ADAPT | typed RepositoryAction; #50/#125 fixed provider grammars | common adapter contract |
| provider capability vs permission | REUSE/ADAPT | Secrets #54 H5/ATP-009B; non-secret `h5:` handles | capability-satisfaction record |
| write set | REUSE | `_coordination_write_set` exact equality | project into grant |
| mutation admission/fencing | REUSE | shared claims + monotonic fencing + conflict rejection | bind claim evidence |
| Paths realization | REUSE/ADAPT | reachability/composition classification with `authorization_inferred:false` | bind query/source/result digest |
| identity satisfaction | ADAPT | #54 safe capability/currentness model; adapters accept refs only | common record/invalidation |
| immediate preconditions | REUSE/ADAPT | Controller capability currentness; #125 exact PR/check verification | consequence-class verifier |
| postcondition/evidence | REUSE/ADAPT | result SHA/projections; #50/#125 typed evidence/fingerprint | normalized result envelope |
| replay/idempotency | REUSE | deterministic request IDs, attempt uniqueness/replay, contract fingerprints | carry grant fingerprint |
| unknown outcome | REUSE/ADAPT | RESERVED recovery/quarantine; #50/#125 reconcile-before-retry | common disposition/hook |
| terminal/invalidation | ADAPT | Paths invalidation + Controller terminal state | normalized set |
| provenance | REUSE/ADAPT | packet/authority/effect/fingerprint/result SHA | one provenance envelope |

## Five behaviors
- **typed_consequence_grant — mostly ADAPT:** authority, effects, mutable surfaces, digest/fingerprint and write set already exist. Missing a provider-neutral projection compiled from them.
- **provider_identity_capability_satisfaction — substantial REUSE:** #54 already separates H5 selection, ATP-009B identity, canonical custody and non-secret capability metadata. Missing a provider-neutral satisfaction record/live trust-plane composition.
- **consequence_realization_resolution — substantial REUSE:** Paths already models technical/configured/proven/authorized/latent state, actor admission, activation, owners, failure domains, evidence, invalidation and non-inferred authorization. Missing deterministic binding into the grant.
- **consequence_execution_admission — substantial REUSE:** Controller already validates authority/effect/currentness/predecessors/write-set/fencing/reservation; adapters enforce destination grammar. Missing the shared bridge.
- **consequence_result_reconciliation — substantial REUSE:** attempt ledger, deterministic IDs, fingerprints, result hashes/projections, replay and RESERVED recovery already exist; adapters already model reconcile-before-retry. Missing normalized result disposition/provenance.

## Patterns recognized
1. Authority attenuation is already the dominant architecture: capability/currentness/path/identity can narrow or satisfy authority, never mint it.
2. Fingerprints are the common join key: Work Packet digest, semantic fingerprint, adapter contract fingerprint and result SHA should compose rather than be replaced.
3. Semantic, path, identity and execution planes are already separate; V1 should standardize their handshake, not centralize them.
4. Unknown outcome is already first-class and compatible across Controller and Compute.
5. Typed adapters are the extensibility boundary; new capabilities should not require bespoke authorization plumbing or generic REST/shell.
6. Paths is already close to the required capability registry; the gap is evidence binding/currentness at grant compilation.
7. Secrets #54 is a reusable identity pattern, not a GitHub exception.
8. Matrix can measure convergence without becoming runtime state.

## Efficiency and accuracy controls
- JIT currentness first; #165/#186/#187 were observed merged and #188 remained draft.
- #188 Required PR Gate failure was treated as counterevidence, not ignored.
- Retrieval used the five behaviors/exact fields as keys; owner-native sources were expanded only when relevant.
- Owner-native sources outranked chat/history; #50/#125 remain preparatory, not runtime proof.
- Paths/Secrets/Controller reuse was exhausted before declaring gaps.
- Capability, provider permission, path availability and semantic authority remained separate.
- Only the smallest missing bridge is proposed; no second spine/store/path authority/Matrix scheduler.

## Recommended order
1. Make #188 green before treating the contract as accepted methodology.
2. Add a **pure consequence-grant projection/schema + validator in Controller**, compiled only from sealed Work Packet + current evidence; never a second authority source.
3. Bind existing write-set/fencing and deterministic Paths evidence.
4. Define provider-neutral non-secret capability satisfaction by reusing #54/H5 semantics.
5. Define a narrow typed-adapter protocol and adapt one existing proven repository effect first.
6. Normalize result/reconciliation using the existing attempt ledger and reconcile-before-retry semantics.
7. Prove one existing effect end-to-end; use #50 repository-create and #125 PR-integration as later structurally different cases only after independent owner gates.
8. Advance Matrix only from code+test/live evidence and run cold-start reconstruction.

## PROGRAMSTART challenge
**GO:** steps 1–2. They are the smallest reversible changes, preserve owner boundaries, reuse current machinery and create the stable join point needed by later composition.

**NO-GO now:** runtime activation of #50/#125, credential widening, generic provider execution, or promotion of Paths candidates from this reconciliation alone.
