# Consequence Execution V1 — Decision Control

Status: durable execution-decomposition/control artifact for the active Consequence Execution V1 PROGRAMSTART lane. This document is **not** semantic authority, runtime admission, a scheduler, queue, second Controller, or a replacement for owner-native state.

## Currentness snapshot and precedence

Owner-native sources outrank this document. Re-read them JIT before every consequence.

Observed during the 2026-10-02 handoff:
- PROGRAMSTART `main`: `c2592e8` ("Localize failures before capability replacement", PR #191). Re-resolve full SHA before consequence.
- PROGRAMSTART PR #188: open, draft, mergeable; branch `methodology/consequence-execution-contract-v1`; pre-repair head `8a45d493c888e770d0c99a45cd9c96c1dc89bfa4`.
- #188 Required PR Gate on that head: failed intrinsically because `ruff-format` reformatted one changed test file. Secret scanning passed. The formatter defect is repaired in the same #188 lane and must be revalidated on the new exact head.
- Controller current Work Packet: `ISSUE-71-P11-ROOT-MACHINE-EVIDENCE-RECLAMATION`, active/acceptance-first, owner `GrahamArdent/programstart-autonomous-controller#71`.
- Controller #71 currently owns the VPS Controller/Compute runtime release boundary and an explicit narrow write set. Consequence Execution DC-02 is not part of that Work Packet.
- Open Controller #227 records Paths-realization consumption but explicitly remains planning/evidence-only pending collision/currentness and PROGRAMSTART #187 reconciliation.

Currentness/invalidation triggers for this artifact include: PR #188 head/base or state change; PROGRAMSTART methodology/Challenge change; Controller Work Packet/authority/write-set change; a new mutation owner on anticipated surfaces; Paths/Secrets/Compute owner evidence change; parity contract/generated Matrix change; accepted evidence invalidation.

## Control rules

1. Flow is: PROGRAMSTART methodology -> Decision Control decomposition -> owner-native implementation/admission -> durable evidence -> Matrix parity projection.
2. Matrix is completeness/read projection only.
3. Paths discovers and proves realizations/currentness; it never grants semantic permission.
4. Provider identity/capability proves technical satisfaction only; it never grants semantic permission.
5. Generic mechanism proof never substitutes for concrete instance proof.
6. Before every mutation, re-read authority, exact intended write set, active mutation owners, branch/PR/Work Packet overlap, and current admission.
7. Different files are not automatically independent.
8. Before declaring a capability/automation gap, perform deterministic Paths discovery and owner-native verification.
9. Reuse existing machinery before creating a new schema/service/control plane.
10. A step marked complete here does not advance Matrix parity without the evidence required by the parity contract.

## Machinery reconciliation

Current evidence continues to support the normalization/composition hypothesis:
- Controller already provides sealed Work Packet identity/integrity, semantic digest/fingerprints, authority/currentness, exact write-set coordination, claims/fencing, effect reservation, attempt/result/replay and ambiguous-outcome reconciliation.
- Paths already provides realization/reachability/composition evidence, availability/currentness, actor admission, owners/failure domains/recovery and explicit non-inference of authorization.
- Secrets/identity machinery already separates canonical custody, provider capability/currentness and semantic authority.
- Compute/typed adapters already use bounded grammars/effect identities/postcondition evidence/reconcile-before-retry patterns.
- The smallest missing center remains normalized typed projections/bindings, not five new subsystems.

## Controlled steps

### DC-01 — Methodology acceptance
- Required outcome: #188/current successor is exact-head green, current, challenged and accepted before downstream methodology claims.
- Owning repository/project: PROGRAMSTART.
- Semantic authority source: current PROGRAMSTART methodology + #188 accepted contract.
- Implementation owner: #188/current successor lane.
- Exact anticipated write surface: current #188 changed files plus this Decision Control artifact; only intrinsic validation repair may extend it.
- Current collision/mutation owner: #188 branch/lane; no competing Matrix mutation may be created.
- Prerequisites: current main/head/base; required-check identity/log; current Challenge.
- Reused machinery: Required PR Gate, parity validator, generated Matrix discipline, Challenge.
- Smallest required delta: repair intrinsic formatter defect; keep parity rows truthful/unproven.
- Paths evidence requirement: none for source-only methodology mutation; Paths required before downstream capability-gap claims.
- Evidence/acceptance: exact-head required check green; focused parity tests; current Challenge disposition; merge/acceptance under repository policy.
- Matrix behaviors: all five consequence behaviors below.
- Current disposition: **IN_PROGRESS** — formatter defect repaired; exact-head revalidation pending.
- Stop condition: failed required check not explained/bounded; conflicting mutation owner; current methodology contradicts contract.
- Terminal condition: accepted current methodology with durable exact-head validation/Challenge evidence.
- Successor: DC-02 only after terminal acceptance/currentness.

### DC-02 — Typed consequence-grant projection
- Required outcome: pure provider-neutral grant schema/projection + validator compiled from sealed Work Packet/current evidence; no second authority object.
- Owner: Controller.
- Semantic authority: current sealed Work Packet/project owner authority, never the projection itself.
- Implementation owner: Controller under a current admitted Work Packet.
- Anticipated write surface: **to be derived JIT** from current Controller architecture; prefer new pure module/tests if current authority permits. Do not touch #71-owned runtime surfaces merely for convenience.
- Current collision owner: Controller #71 owns current packet and shared runtime release boundary; its explicit write set does not admit DC-02.
- Prerequisites: DC-01 terminal; Controller current Work Packet either admits DC-02 or owner-native sequencing releases/transfers authority.
- Reuse: packet authority version, semantic digest/fingerprint, mutable surfaces, expected write set, effect identity/currentness.
- Smallest delta: normalization/projection + fail-closed validator only.
- Paths requirement: only if selecting/declaring a realization while designing exact bindings; no capability-gap declaration without discovery.
- Evidence: source tests proving no widening, stale/missing-field rejection, deterministic identity, projection equivalence to owner authority.
- Matrix: `typed_consequence_grant`.
- Current disposition: **BLOCKED_BY_CURRENT_MUTATION_OWNER / NOT ADMITTED**, not HUMAN_REQUIRED.
- Stop: absent/ambiguous semantic authority; current packet excludes write set; overlap with active Controller owner.
- Terminal: exact current Controller source proof accepted; no runtime/provider effect activated.
- Successor: DC-03/DC-05 binding slices only after current owner sequencing permits.

### DC-03 — Paths realization evidence binding
- Outcome: deterministic effect/target discovery evidence is bound to grant with source/currentness/result identity and `authorization_inferred=false`.
- Owners: Paths for realization evidence; Controller for consuming/binding it.
- Authority: owner project + Controller admission; never Paths.
- Write surface: JIT derive from current Paths query contract and Controller consumer; do not duplicate Paths registry.
- Collision owner: reconcile Controller #227 and any current Paths packet before mutation.
- Prerequisites: DC-01; DC-02 projection or equivalent accepted field contract; current Paths owner evidence.
- Reuse: effect-reachability/composition/currentness/invalidation records.
- Smallest delta: deterministic binding/reference, not new registry.
- Paths evidence: mandatory exact effect/target query + owner-native verification for consequential use.
- Acceptance: stale/ambiguous/no-realization fail closed; discovery cannot mint permission.
- Matrix: `consequence_realization_resolution`.
- Disposition: **PLANNED / OWNER-RECONCILIATION REQUIRED**.
- Stop: discovery stale/contradictory; competing #227/current owner write set; inferred authorization.
- Terminal: accepted deterministic binding with currentness/invalidation proof.
- Successor: DC-05.

### DC-04 — Provider identity capability satisfaction
- Outcome: provider-neutral non-secret capability-satisfaction evidence.
- Owners: Secrets/identity owner + Controller boundary.
- Authority: provider permission is technical upper bound only; owning project remains semantic authority.
- Write surface: JIT derive; do not export credentials or copy custody.
- Collision owner: current Secrets/identity packet(s) and Controller consumer packet.
- Prerequisites: DC-01; existing H5/ATP-009B/#54 evidence revalidated; DC-02 field contract when required.
- Reuse: canonical custody, non-secret capability refs/currentness, identity lifecycle.
- Smallest delta: normalized satisfaction reference/invalidation evidence.
- Paths evidence: use Paths if provider/identity realization path availability is material; never treat identity as path authority.
- Acceptance: no secret export; insufficient/stale provider envelope fails closed; permission != semantic authority.
- Matrix: `provider_identity_capability_satisfaction`.
- Disposition: **PLANNED / REUSE-FIRST**.
- Stop: requires credential broadening/export or bypasses custody owner.
- Terminal: accepted non-secret satisfaction evidence contract and owner-current proof.
- Successor: DC-05.

### DC-05 — Consequence execution admission bridge
- Outcome: current authority + exact grant + write-set/fencing + Paths evidence + identity satisfaction admit exactly one bounded effect.
- Owner: Controller.
- Authority: current project owner compiled/admitted by Controller.
- Write surface: JIT derive from existing coordination/admission/reservation code; avoid shared runtime surfaces while another packet owns them.
- Collision owner: then-current Controller Work Packet/mutation claim owner.
- Prerequisites: DC-01; accepted DC-02/03/04 equivalents; current mutation ownership.
- Reuse: exact write-set equality, claims/fencing, effect reservation, currentness and typed dispatch.
- Smallest delta: bridge existing checks around common grant identity.
- Paths: mandatory current realization evidence for consequential dispatch.
- Acceptance: capability-without-authority rejection; conflicting write set/fence rejection; one-effect scope.
- Matrix: `consequence_execution_admission`.
- Disposition: **PLANNED**.
- Stop: ambiguous authority/ownership/currentness; broad adapter required.
- Terminal: accepted source-level admission proof before live family activation.
- Successor: DC-06.

### DC-06 — Bounded typed-adapter acceptance
- Outcome: one existing proven effect consumes common contract without generic REST/shell or bespoke authority plumbing.
- Owner: owning execution repo/adapter.
- Authority: owning project + Controller admitted grant.
- Write surface: exact adapter-specific surface discovered JIT.
- Collision owner: current adapter/Compute/EN packet.
- Prerequisites: DC-05 source acceptance; natural existing effect selected from current evidence.
- Reuse: existing typed grammar, destination policy, contract fingerprint, postcondition evidence.
- Smallest delta: adapt one proven effect; do not activate preparatory #50/#125 merely because they resemble target families.
- Paths: prove selected realization/currentness.
- Acceptance: grammar no broader than grant; negative wider-operation rejection.
- Matrix: primarily `consequence_execution_admission`, supports result/realization rows.
- Disposition: **PLANNED**.
- Stop: only generic shell/REST path exists; current effect is preparatory/unaccepted; owner conflict.
- Terminal: one natural typed effect accepted through common contract.
- Successor: DC-07/DC-08.

### DC-07 — Result/reconciliation envelope
- Outcome: grant/effect/result provenance plus replay/idempotency/unknown-outcome reconciliation compose through existing attempt/result machinery.
- Owner: Controller + effect owner.
- Authority: existing Controller/effect owner contracts.
- Write surface: JIT derive from attempt ledger/result projection and adapter reconciliation.
- Collision owner: then-current Controller/effect packet.
- Prerequisites: DC-02 identity/fingerprint; DC-06 effect.
- Reuse: deterministic request IDs, attempt uniqueness, result SHA/projection, RESERVED recovery/quarantine, reconcile-before-retry.
- Smallest delta: normalized result disposition/provenance.
- Paths: preserve realization evidence/invalidation linkage when result depends on selected path.
- Acceptance: duplicate/replay one consequence at most; ambiguous result reconciled before retry.
- Matrix: `consequence_result_reconciliation`.
- Disposition: **PLANNED**.
- Stop: cannot bind result to exact grant/effect; blind retry would be required.
- Terminal: durable accepted result/reconciliation envelope.
- Successor: DC-08.

### DC-08 — Natural end-to-end acceptance
- Outcome: one natural existing effect proves authority -> grant -> coordination -> Paths -> identity -> typed adapter -> evidence -> reconciliation, plus capability-without-authority rejection.
- Owners: composed existing owners; no new central owner.
- Write surface: only the already-owned accepted slices; no manufactured demo subsystem.
- Collision owner: all participating current Work Packets/claims.
- Prerequisites: DC-01 through DC-07 as materially required.
- Reuse: all accepted machinery.
- Smallest delta: acceptance harness/evidence only unless natural test exposes a bounded defect.
- Paths: mandatory deterministic current realization and owner verification.
- Acceptance: durable E2E evidence, restart/replay where material, no chat as state.
- Matrix: all five consequence behaviors.
- Disposition: **PLANNED**.
- Stop: any owner/currentness/collision ambiguity or synthetic proof standing in for natural consequence.
- Terminal: one natural effect accepted and one technical-capability-without-semantic-authority adversarial rejection proven.
- Successor families: repository create; protected PR integration; reversible GitHub mutation; non-GitHub mutation; local/runtime machine mutation. Each requires its own instance proof.

### DC-09 — Matrix reconciliation and cold-start proof
- Outcome: Matrix advances only from accepted code/test/live evidence; generated view current; fresh worker reconstructs objective -> contract -> owners -> parity -> missing edges -> mutation owner -> next safe action without chat.
- Owner: PROGRAMSTART parity/acceptance.
- Authority: parity contract/source evidence; Matrix remains non-authoritative.
- Write surface: `config/autonomy-parity-contract.json`, generated `docs/AUTONOMY_PARITY_MATRIX.md`, tests only under the current parity mutation owner.
- Collision owner: #188/current successor or then-current parity lane.
- Prerequisites: accepted owner-native evidence for rows being advanced.
- Reuse: parity validator/generator/JIT behavior selector.
- Smallest delta: evidence-backed status/proof refs only.
- Paths: fresh worker must use Paths for realization/currentness where required.
- Acceptance: parity validation green; generated projection exact; cold-start reconstruction succeeds.
- Matrix: five consequence behaviors.
- Disposition: **WAITING_ON_EVIDENCE**; all five remain prompt_only/unproven until parity evidence earns change.
- Stop: Decision Control completion presented as parity proof; competing Matrix mutation.
- Terminal: truthful Matrix projection and cold-start proof.
- Successor: objective-level next work selected only under current PROGRAMSTART sequencing.

## PROGRAMSTART Challenge — current next step

Candidate next step: complete DC-01 exact-head repair/revalidation.

Challenge:
- Necessary? **Yes.** Current Required PR Gate is failed on the observed head; downstream methodology acceptance cannot be claimed.
- Existing machinery already satisfies it? **Partially.** Contract/reconciliation/parity rows exist; only intrinsic formatting/current validation/Challenge acceptance remains.
- Owner correct? **Yes: PROGRAMSTART #188 lane.**
- Collision-free? **Yes, if confined to #188-owned changed surface + this Decision Control artifact and no competing Matrix mutation is created.**
- Duplicate authority/control-plane risk? **No.** Decision Control is decomposition/indexing only.
- Acceptance scope proportional? **Yes.** Exact-head required validation + current Challenge/merge acceptance; no runtime activation.

Disposition: **GO WITH NARROWING** — finish DC-01 only. Do not begin Controller DC-02 mutation while Controller #71 remains the current packet and its explicit write set does not admit this work.

## Immediate resume point

1. Re-read #188 exact head and Required PR Gate after this lane update.
2. If validation fails, classify only the new exact-head failure and repair intrinsic bounded defects.
3. Re-run/observe exact-head validation; preserve secret/lint/methodology gates.
4. Re-read current PROGRAMSTART Challenge and PR acceptance/merge state.
5. Only after DC-01 terminal, re-read Controller CURRENT_WORK_PACKET + open PRs/issues/claims and challenge whether DC-02 is now admitted, already satisfied, or must wait/route through owner-native sequencing.
