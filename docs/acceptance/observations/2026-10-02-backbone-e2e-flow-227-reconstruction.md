# Backbone E2E Information Flow — #227 Cold Reconstruction

Date: **2026-10-02**
Contract under test: `docs/PROGRAMSTART_BACKBONE_END_TO_END_INFORMATION_FLOW.md`
Natural fixture: `GrahamArdent/programstart-autonomous-controller#227`
Mode: **fresh-context / read-only reconstruction**
Execution authority: **none**

## 1. Question

Given only durable ecosystem sources, can a fresh observer reconstruct the current #227 objective from semantic ingress to its first unsupported backbone boundary without chat memory or invented links?

Result: **PARTIAL / ARCHITECTURE CONTRACT FALSIFIER PASSES**

The objective can be reconstructed truthfully, but not yet through one machine-addressable causal chain. Several critical edges exist only as manually correlated durable prose.

## 2. Fresh currentness snapshot

Observed during this reconstruction:

- PROGRAMSTART main: `d79506a58ab165fcf39170ab3a0e999b768c48e6`
- Controller main: `d11ae41f18a05d5df5b5b90210e5688281e4516d`
- Paths main: `093b90c3d6429d376fc8dd7cbb8292e76827a0ec`
- Execution Node main: `36ab5891e2821ff962c0ab39b1bfd521872d9146`
- Compute Spine main: `a2ac6d31c1c1e2e12a2cee06a2e54640051a323e`
- Controller open PRs: none at observation time
- Controller current packet: `CURRENT_WORK_PACKET.md` = ACTIVE / #227 Paths-discovery consumption

Important: later currentness changes may invalidate this observation; use owner-native currentness before consequence.

## 3. Protected objective

Controller #227 owns:

`semantic objective -> actor/effect/target -> deterministic Paths query -> owner JIT verification -> existing typed effect -> durable result -> Controller continuation`

The caller must not select the realization/provider/transport/command/path/credential.

Terminality requires the complete fresh semantic-objective-to-durable-result flow plus automatic continuation/reclassification and truthful derived-state reconciliation.

## 4. Reconstruction table

| Flow stage | Durable source | Reconstruction quality | Current finding |
|---|---|---|---|
| INGRESS | Controller #227 body + latest live-convergence comment | **manual durable archaeology** | Private `POST /v1/programstart-objective` is proven; successful request `req-programstart-objective-backbone-227-complete-081653` |
| SEMANTIC_INTERPRETATION | #227 live-convergence comment | **manual durable archaeology** | semantic producer converged; owner resolved; sealed packet persisted |
| DECISION_SETTLEMENT | #227 authority/current packet | **not separately required for this fixture** | no new Decision-Closure artifact is needed merely to run the already-owned objective |
| OUTCOME_DECOMPOSITION | Controller #227 + `CURRENT_WORK_PACKET.md` | **direct owner file + issue** | acceptance, sequence and terminal condition are explicit |
| CURRENT_STATE_PROJECTION | #227 comments/current packet | **partial/manual** | prior collision dependencies were reconciled; no current Matrix record is needed to manufacture authority |
| WORK_SELECTION | Controller `CURRENT_WORK_PACKET.md` | **direct machine-addressable owner file** | #227 is the active Controller packet |
| CONTROLLER_ADMISSION | #227 live-convergence comment | **manual durable archaeology** | fresh run after repairs: root `root-8587f916b07c12daf753a297`, run `intent-164c265053d2b7b7`; operator intervention false |
| CAPABILITY_DISCOVERY | Paths `registry/effect-reachability.json` | **direct machine-readable prerequisite** | ER-012 is eligible/current/proven/owner-admitted, but the #227 run has **not yet selected it** |
| OWNER_ADMISSION | Paths ER-012 owner refs + EN #301 | **direct prerequisite / consequence-time JIT not yet reached** | EN owner admission exists for the fixed Class-0 action; #227 consequence-time owner-JIT binding is not yet proven |
| CONSEQUENCE | none for the intended ER-012 effect | **not reached** | no new private-tailnet reachability consequence has been emitted for this fresh root |
| EVIDENCE | Compute commit `a2ac6d31c1c1e2e12a2cee06a2e54640051a323e` | **direct durable result** | typed status diagnostic succeeded and proves the Controller repository is absent from EN repository capabilities |
| RECONSIDERATION | #227 live-convergence comment | **manual durable archaeology** | root/run recorded `AUTOMATION_GAP_RECORDED`; no human gate |
| OUTCOME_VALIDATION | #227 open state + current packet terminal condition | **direct owner truth** | protected outcome remains false/unproven because discovery/consequence/continuation has not been reached |
| RECONCILIATION | #227 comment | **manual durable archaeology** | blocker localized to Controller self-hosting repository capability; no Paths defect; no HOP/Matrix promotion earned |
| TERMINAL | Controller #227 = open | **direct owner truth** | nonterminal; first unsupported boundary is self-hosting repository capability |

## 5. Direct machine-readable facts already working well

### Paths discovery data

Current Paths `registry/effect-reachability.json` contains ER-012:

- `actor:execution-node-control-agent`
- `effect:private-tailnet-reachability-observe`
- target `vps-743d7c1d`
- eligibility `eligible`
- technical `available`
- configured `active`
- proven `proven`
- authorization envelope `owner_admitted_read_only`
- actor admission owner `GrahamArdent/execution-node-control`
- runtime release `63f172718029359d5ca69bf83d778980e817dfd7`
- `authorization_inferred=false`
- explicit evidence refs
- explicit invalidation conditions.

This is an example of the information-flow architecture already working correctly: discovery is machine-readable, bounded and non-authoritative.

### Typed currentness diagnostic

Compute commit `a2ac6d31c1c1e2e12a2cee06a2e54640051a323e` is the durable result for:

`req-vps-worker-227-status-diagnostic-0829`

It proves the typed Compute -> EN observation path succeeded and reports the current EN repository capability projection.

The result does **not** contain `GrahamArdent/programstart-autonomous-controller` in `repository_capabilities.repositories`.

This independently supports the #227 classification that the current first unsupported boundary is:

`Controller semantic run -> repository capability currentness -> Controller repository absent from EN typed repository fabric`.

## 6. Repairs that are durably addressable but not causally linked by a common lineage

### Controller PR #236

Merged as `194b63eb6fd6104b2e068ff88004165a4d5cea13`.

It repaired only the exact PREPARE admission token:

`repository.prepare:GrahamArdent/programstart-autonomous-controller`

The PR body identifies the originating request `req-programstart-objective-backbone-227-complete-081653`.

### Controller PR #237

Merged as `d11ae41f18a05d5df5b5b90210e5688281e4516d`.

It reuses the existing Runtime V3 `continue_initial_repository_prepare()` path for handed PROGRAMSTART objectives.

Its PR body identifies the fresh predecessor root/run that exposed that missing edge.

These records are durable and semantically useful, but the chain is reconstructed by reading prose fields rather than following a standardized causal reference.

## 7. Missing or weak lineage edges

### L1 — no canonical end-to-end lineage identity

The following identifiers all belong to the same larger objective but are not joined by one stable machine-level lineage ID:

- Controller issue `#227`;
- ingress request IDs;
- semantic effect ID;
- sealed Work Packet identity;
- Controller root ID;
- Controller run/intent ID;
- repair PR/commit IDs;
- Compute diagnostic request ID;
- nested EN child request ID;
- future Paths selection receipt;
- future typed consequence result.

A human can correlate them. A generic machine consumer cannot yet do so from one starting identifier.

### L2 — issue comments currently act as the integration ledger

The most decision-complete record of the end-to-end chain is the latest #227 issue comment.

That comment is durable, but it is narrative integration written after the fact. It is not a typed cross-component lineage contract.

This is the largest current information-flow weakness exposed by the fixture.

### L3 — Controller root/run is not directly discoverable from ingress identity through repository search

The successful run's root/run IDs are recoverable from the issue narrative, but the fresh observer did not find a direct repository-addressable mapping:

`ingress request -> sealed packet -> root -> run`.

The runtime may hold this relation internally; this test establishes that the relationship is not currently exposed as a generic ecosystem reconstruction surface.

### L4 — repair commits point backward through prose, not typed causality

PR #236 and #237 explain which live acceptance exposed each defect.

That is good human evidence but not a machine `caused_by` relationship.

### L5 — diagnostic evidence is strongly typed but not bound to the semantic root

The Compute result preserves:

- request identity;
- caller;
- transport;
- nested EN request;
- result hashes;
- repository capability result.

It does not carry a standard reference to #227's Controller root/run or originating objective.

The issue comment supplies that meaning manually.

### L6 — prerequisite proof and run-specific proof are correctly separate

Paths ER-012 is already proven and owner-admitted as a reusable capability.

That record must **not** be treated as evidence that the current #227 run selected/invoked ER-012.

This is not a defect. It is an important lineage boundary that the future envelope must preserve.

### L7 — no false completeness marker

Because the intended Paths selection/consequence has not been reached, a reconstruction must stop at the self-hosting gap.

A reconstruction system that fills the rest of the planned path from ER-012 prerequisite evidence would be incorrect.

## 8. Duplicated information observed

Some duplication is legitimate because records have different owners/purposes.

However, the fixture shows a recurring pattern where large narrative comments repeat:

- current repo/release heads;
- prior prerequisite state;
- blocker classifications;
- repair history;
- intended next chain.

The better long-term shape is:

- keep owner-native facts in their owner;
- carry exact durable references/currentness;
- retain one bounded semantic disposition;
- reconstruct the expanded view on demand.

Do not solve this by copying entire native payloads into one global record.

## 9. Minimum lineage fields earned by this fixture

The original architecture draft proposed a candidate envelope. #227 narrows the empirical minimum.

### Required correlation core

Every cross-boundary lineage record needs:

- `lineage_id`
- `record_id`
- `record_type`
- `producer_owner`
- `producer_record_ref`
- `caused_by[]`
- `root_objective_ref`

### Conditional decision-critical references

Include only when applicable:

- `owner_ref`
- `authority_ref`
- `currentness_ref`
- `protected_outcome_ref`
- `work_packet_ref`
- `controller_root_ref`
- `controller_run_ref`
- `semantic_effect_ref`
- `realization_ref`
- `effect_attempt_ref`
- `evidence_refs[]`
- `terminal_condition_ref`
- `resume_or_reconsider_ref`
- `invalidation_refs[]`

### Explicitly not earned

This fixture does not justify:

- a global payload field for full native records;
- one universal state enum;
- one global database;
- a centralized authority field that overrides owner currentness;
- caller-selected implementation/provider/transport fields;
- mandatory backfill of historical records.

## 10. Challenge of the empirical result

### Could the reconstruction be considered complete merely because all planned future pieces are known?

**No.**

The run has not reached Paths selection, consequence-time owner JIT, fresh reachability consequence or post-result continuation.

### Could ER-012's existing proof close #227?

**No.**

It proves reusable prerequisite capability only. #227 requires fresh consequence evidence for the new objective.

### Could the self-hosting gap be treated as a human gate?

**No.**

Current durable evidence classifies it as a machine capability/admission gap.

### Could the absence of a common lineage ID be solved by making Matrix authoritative?

**No.**

Matrix may project lineage but must not mint the underlying owner facts or execution authority.

### Does this fixture justify a machine-readable lineage schema next?

**Yes, as a bounded design candidate — not as an ecosystem-wide runtime rollout.**

The empirical pass identified a stable small correlation core and concrete missing edges. That is enough to design a schema/fixture next, but not enough to bulk-propagate it through every component.

## 11. Current fixture disposition

**BACKBONE FLOW:** partially reconstructable.

**FIRST UNSUPPORTED CURRENT EDGE:** Controller self-hosting repository capability in the existing typed repository fabric.

**PATHS/ER-012:** current reusable prerequisite; not yet selected by the fresh run.

**HUMAN GATE:** none.

**CONVERSATIONAL REENTRY REQUIRED:** should remain no.

**ARCHITECTURE FINDING:** the ecosystem has durable component truth but lacks a first-class cross-component causal lineage projection.

## 12. Next bounded architecture step

After PR #196 is accepted/current, the next architecture-only step is to define a **small machine-readable lineage schema + #227 fixture** for the fields earned above.

That schema should first prove:

1. it can represent the #227 chain without copying native payloads;
2. missing links remain `unknown/not_reached`, not fabricated;
3. lineage cannot grant authority;
4. one event may have multiple causes;
5. owner-handoff can preserve causality without transferring authority;
6. sensitive material is never required for correlation;
7. a fresh reader can reconstruct #227 to the current blocker from durable refs.

Do not wire it into Controller/Paths/Compute/EN until that representation is challenged and accepted.
