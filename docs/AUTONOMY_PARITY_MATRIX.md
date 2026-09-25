# PROGRAMSTART Autonomy Parity Matrix

> Derived acceptance evidence only. Canonical PROGRAMSTART sources remain authoritative.
> This is not a Master, scheduler, backlog, controller, methodology database, or execution spine.

- Contract: programstart.autonomy-parity.v1
- PROGRAMSTART baseline: GrahamArdent/PROGRAMSTART@e442fb0e6a6de37629d454b06e4d06038f70188b
- Controller observation baseline: GrahamArdent/programstart-autonomous-controller@c95372bd5640110cf13791546ae1930cd0abb240
- Durable reference: GrahamArdent/PROGRAMSTART#143
- Fingerprinted source files: 8
- Required source obligations covered: 422
- Parity behaviors: 49
- Accepted conversation decisions reconciled: 27
- Material hop instances: 37

## JIT usage invariant

Query this contract by the current trigger/effect. Never load the full matrix into every objective.
Reuse still-valid evidence; widen only on declared invalidation or convergence boundaries.

## Coverage summary

- human_gate: 1
- implemented: 8
- partial: 23
- prompt_only: 11
- semantic: 6

## Behavior matrix

| Behavior | Machinery | Mode | Closure | Owner |
|---|---|---|---|---|
| semantic_objective_ingress — Natural objective and semantic intent ingress | implemented | semantic | proven | Controller + PROGRAMSTART |
| data_grounding_instruction_isolation — Fetched artifacts remain data, not instructions | prompt_only | deterministic | unproven | PROGRAMSTART prompt/runtime boundary |
| jit_context_evidence_governor — JIT context and evidence governor | partial | hybrid | partial | PROGRAMSTART + Controller |
| live_orientation_currentness — Live orientation and exact currentness | implemented | deterministic | proven | PROGRAMSTART + Controller |
| canonical_before_dependent — Canonical owner before dependent mutation | partial | hybrid | partial | PROGRAMSTART + owning repository |
| mode_abc_resolution — Mode A/B/C entry resolution | partial | semantic | partial | PROGRAMSTART |
| idea_capture_promotion — Idea capture separated from promotion/execution | prompt_only | semantic | unproven | PROGRAMSTART |
| retention_intent — Semantic retention intent without execution escalation | semantic | semantic | unproven | PROGRAMSTART semantic layer |
| accepted_recommendation_resolution — Generic acceptance resolved against current authority | partial | semantic | partial | PROGRAMSTART + Controller |
| stronger_gate_overlay — Stronger consequence gate survives generic acceptance | partial | hybrid | partial | PROGRAMSTART + Controller |
| bounded_work_packet — Bounded replaceable Work Packet | implemented | deterministic | proven | PROGRAMSTART + Controller |
| cross_repository_dependency_graph — Task-scoped cross-repository dependency graph | partial | hybrid | partial | PROGRAMSTART + Controller |
| repository_independence — Cross-repository evidence does not authorize multi-project mutation | prompt_only | deterministic | unproven | PROGRAMSTART |
| blocker_scope_safe_lane — Narrow blocker scope and scan safe lanes | partial | hybrid | partial | PROGRAMSTART + Controller |
| coordinated_mode_c_lanes — Coordinate multiple Mode-C lanes without parallel authority | prompt_only | semantic | unproven | PROGRAMSTART |
| shared_mutation_ownership — Single owner for consequential shared mutation | partial | hybrid | partial | PROGRAMSTART + Controller |
| external_resource_evidence_continuity — Preserve external resource history/current visibility distinction | prompt_only | semantic | unproven | PROGRAMSTART |
| adaptive_research_depth — Adaptive research depth to decision sufficiency | semantic | semantic | unproven | PROGRAMSTART semantic layer |
| external_connection_surface_inventory — Enumerate connection surfaces before declaring automation unavailable | prompt_only | semantic | unproven | PROGRAMSTART capability resolution |
| cost_governance — Decision-scoped cost governance | semantic | hybrid | unproven | PROGRAMSTART semantic layer |
| conditional_checklist_completeness — Conditional checklist activation and reconciliation | partial | hybrid | partial | PROGRAMSTART |
| clean_candidate_publication — Prepare clean candidate before remote publication | partial | deterministic | partial | Owning repository + PROGRAMSTART |
| execute_one_selected_packet — Execute one selected bounded packet | implemented | deterministic | proven | Controller |
| operator_gate_exact_handoff — Exact secret-safe operator/manual handoff | partial | hybrid | partial | PROGRAMSTART + Controller |
| operator_gate_auto_verify_resume — Verify gate evidence and resume without redundant proceed | partial | deterministic | partial | Controller |
| credential_human_enablement_leverage — Credential/access human-enablement leverage test | partial | hybrid | partial | PROGRAMSTART + Controller |
| proportional_verification — Verify changed or newly-at-risk surfaces proportionally | prompt_only | hybrid | unproven | PROGRAMSTART + owning repository |
| risk_triggered_challenge — Risk-triggered post-implementation adversarial Challenge | semantic | semantic | unproven | PROGRAMSTART semantic layer |
| durable_state_reconciliation — Reconcile accepted durable truth to its owner | partial | hybrid | partial | PROGRAMSTART + owning repository |
| learning_gate — Triggered causal Learning Gate classification | semantic | semantic | unproven | PROGRAMSTART semantic layer |
| conditional_learning_persistence — Persist learning only when earned and owner-writable | prompt_only | hybrid | unproven | PROGRAMSTART |
| replay_idempotency — Durable replay and duplicate-effect suppression | implemented | deterministic | proven | Controller |
| wait_wake_retry — Durable wait/wake/retry for machine evidence | implemented | deterministic | proven | Controller |
| owner_handoff — Durable owner handoff persistence and delivery | implemented | deterministic | proven | Controller |
| exact_machine_currentness_binding — Machine currentness narrows but never grants authority | implemented | deterministic | proven | Controller |
| evidence_reuse_invalidation — Evidence reuse with explicit invalidation | partial | hybrid | partial | PROGRAMSTART + Controller |
| progressive_context_widening — Progressive narrowing then widening at convergence | prompt_only | semantic | unproven | PROGRAMSTART semantic layer |
| authority_non_minting_no_second_spine — Derived machinery cannot mint authority or a second execution spine | partial | deterministic | partial | PROGRAMSTART + Controller |
| objective_terminality_next_effect — Objective-level terminality and next-effect derivation | partial | semantic | partial | Controller + PROGRAMSTART |
| verification_claim_truthfulness — Verification claims match what actually ran | partial | deterministic | partial | PROGRAMSTART + Controller |
| proportional_rigor_routing — Select rigor proportional to consequence, uncertainty, reversibility, and blast radius | semantic | semantic | unproven | PROGRAMSTART |
| effective_autonomy_consequence_resolution — Resolve effective autonomy at consequence-class granularity | partial | hybrid | partial | PROGRAMSTART + Controller |
| runtime_capability_declaration — Expose machine-readable current capability evidence without granting project permission | partial | deterministic | partial | Controller + execution fabric |
| automatic_capability_adoption — Adopt a newly proven implementation capability without new semantic authority | partial | hybrid | partial | PROGRAMSTART + Controller |
| temporary_automation_gap_alternative_actuation — Search bounded alternative actuation before using a human as transport | prompt_only | semantic | unproven | PROGRAMSTART semantic layer |
| irreducible_human_consequence — Preserve genuinely non-delegable human authorization/judgment | human_gate | human | unproven | Human + owning consequence boundary |
| autonomy_metrics_observability — Measure avoidable gates, redundant continuation, and capability debt without creating authority | partial | deterministic | partial | Controller + PROGRAMSTART |
| learning_maturity_dedup_retest — Deduplicate lessons, track evidence maturity, and route only matching future retests | prompt_only | semantic | unproven | PROGRAMSTART |
| conversation_decision_reconciliation — Reconcile accepted conversation decisions into durable parity evidence | partial | hybrid | partial | PROGRAMSTART + owning project |

## Material hop instance matrix

> Generalized machinery may be reused, but every concrete material hop requires its own instance acceptance evidence.
> Physical path inventory/health/recovery remains authoritative in Paths/Path Authority or the owning project.

| Hop | Class | Source | Target | Mechanism | Status | Evidence |
|---|---|---|---|---|---|---|
| HOP-001 | objective_ingress | Windows operator / admitted private source | Controller private natural-objective ingress | tailscale_private_http_v1 | proven | GrahamArdent/programstart-autonomous-controller#97 |
| HOP-002 | objective_ingress | Mission-Control private operator surface | Controller private natural-objective ingress | Mission-Control private objective transport | partial | GrahamArdent/programstart-autonomous-controller#88<br>GrahamArdent/execution-node-control#218 |
| HOP-003 | semantic_pipeline | Controller contextual runtime | PROGRAMSTART JIT / intent runtime | installed PROGRAMSTART exact behavior selector and intent adapter | proven | GrahamArdent/programstart-autonomous-controller#102<br>GrahamArdent/PROGRAMSTART#145 |
| HOP-004 | semantic_pipeline | PROGRAMSTART bounded intent runtime | Compute semantic relay | local Unix semantic relay | proven | GrahamArdent/programstart-autonomous-controller#97 |
| HOP-005 | semantic_pipeline | Compute semantic relay | Execution Node typed semantic producer | fixed typed Execution Node semantic action | proven | GrahamArdent/programstart-autonomous-controller#97<br>GrahamArdent/execution-node-control#221 |
| HOP-006 | semantic_pipeline | Execution Node semantic producer | PROGRAMSTART semantic validation | typed semantic harvest return | proven | GrahamArdent/programstart-autonomous-controller#97 |
| HOP-007 | semantic_pipeline | PROGRAMSTART semantic validation | Controller durable admission | existing Controller contextual admission and sealed packet persistence | proven | GrahamArdent/programstart-autonomous-controller#97 |
| HOP-008 | execution_fabric | Controller execution owner | Compute worker bridge | Controller-to-Compute typed request/result bridge | proven | GrahamArdent/programstart-autonomous-controller#53<br>GrahamArdent/programstart-autonomous-controller#97 |
| HOP-009 | execution_fabric | Compute worker bridge | Execution Node typed normal work carrier | TR-05 typed Compute-to-Execution transport / fixed semantic carrier where already accepted | partial | GrahamArdent/programstart-compute-spine#75<br>GrahamArdent/programstart-autonomous-controller#97 |
| HOP-010 | execution_fabric | Execution Node typed action | Compute bounded result envelope | typed Execution Node result binding | proven | GrahamArdent/programstart-autonomous-controller#53<br>GrahamArdent/programstart-autonomous-controller#97 |
| HOP-011 | execution_fabric | Compute bounded result envelope | Controller continuation evidence | Controller request/result correlation | proven | GrahamArdent/programstart-autonomous-controller#53<br>GrahamArdent/programstart-autonomous-controller#97 |
| HOP-012 | async_continuation | GitHub provider terminal events | Watchtower authenticated event sensor | authenticated GitHub webhook intake and durable delivery identity | proven | GrahamArdent/programstart-autonomous-controller#71<br>GrahamArdent/repo-watchtower#16 |
| HOP-013 | async_continuation | Watchtower terminal evidence projection | Controller exact durable machine wait | bounded terminal-evidence projection plus exact wait correlation | partial | GrahamArdent/programstart-autonomous-controller#71<br>GrahamArdent/repo-watchtower#16<br>GrahamArdent/execution-node-control#188 |
| HOP-014 | async_continuation | Controller genuine human gate | Mission-Control operator interaction surface | Mission-Control human-gate notification/interaction transport | partial | GrahamArdent/programstart-autonomous-controller#71<br>GrahamArdent/programstart-autonomous-controller#88 |
| HOP-015 | async_continuation | Mission-Control operator evidence | Controller human-gate evidence acceptance | Mission-Control evidence return plus Controller human-gate acceptance | partial | GrahamArdent/programstart-autonomous-controller#71 |
| HOP-016 | async_continuation | Controller durable nonterminal wait | Controller semantic owner reconsideration | durable wait/wake/retry plus event-first recovery sweep | partial | GrahamArdent/programstart-autonomous-controller#71 |
| HOP-017 | control_plane | Execution fabric | GitHub repository/provider effects and observation | bounded GitHub App / authenticated gh CLI / repository broker capability | partial | GrahamArdent/execution-node-control#225<br>GrahamArdent/PROGRAMSTART#147 |
| HOP-018 | control_plane | Execution fabric | Secrets Control Plane / Infisical | owner-scoped Infisical machine identities and bounded secret consumers | partial | GrahamArdent/secrets-control-plane#69<br>GrahamArdent/secrets-control-plane#78 |
| HOP-019 | control_plane | Compute/VPS control plane | Execution Node independent control/recovery | accepted private recovery/control paths with typed control surface | proven | GrahamArdent/execution-node-control#180 |
| HOP-020 | control_plane | Execution Node control plane | VPS / Controller maintenance and release surfaces | fixed reviewed typed remote maintenance/release actions | proven | GrahamArdent/execution-node-control#154<br>GrahamArdent/execution-node-control#180 |
| HOP-021 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/PROGRAMSTART | owner_handoff_v1 + repository carrier + target-specific intake | proven | GrahamArdent/programstart-autonomous-controller#53<br>GrahamArdent/execution-node-control#145<br>GrahamArdent/programstart-compute-spine#72 |
| HOP-022 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/ecosystem-contracts | owner_handoff_v1 + per-target repository admission + target-owned intake | partial | GrahamArdent/ecosystem-contracts#24<br>GrahamArdent/programstart-autonomous-controller#106<br>GrahamArdent/execution-node-control#225 |
| HOP-023 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/programstart-autonomous-controller | Controller-local authority plus typed repository/release paths | proven | GrahamArdent/programstart-autonomous-controller#102 |
| HOP-024 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/programstart-compute-spine | existing Compute carrier/repository mechanisms plus owner-specific admission | partial | GrahamArdent/programstart-compute-spine#72<br>GrahamArdent/programstart-compute-spine#75 |
| HOP-025 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/execution-node-control | typed EN control/release machinery plus owner-specific repository admission | partial | GrahamArdent/execution-node-control#180<br>GrahamArdent/PROGRAMSTART#147 |
| HOP-026 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/mission-control | owner-specific repository intake plus typed Mission-Control release/runtime paths | partial | GrahamArdent/execution-node-control#218<br>GrahamArdent/programstart-autonomous-controller#88 |
| HOP-027 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/repo-watchtower | owner-specific repository/runtime intake while Watchtower remains sensor-only | partial | GrahamArdent/repo-watchtower#16<br>GrahamArdent/execution-node-control#188 |
| HOP-028 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/evidence-spine | owner-specific repository admission; Evidence Spine remains evidence owner, not Controller | partial | GrahamArdent/evidence-spine#1<br>GrahamArdent/PROGRAMSTART#147 |
| HOP-029 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/portfolio-operations | owner-specific repository admission and target-owned intake | partial | GrahamArdent/portfolio-operations#43<br>GrahamArdent/PROGRAMSTART#147 |
| HOP-030 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/dependency-intelligence | owner-specific repository admission and target-owned intake | unproven | GrahamArdent/PROGRAMSTART#147 |
| HOP-031 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/secrets-control-plane | owner-specific repository intake plus existing brokered secret/identity capabilities | partial | GrahamArdent/secrets-control-plane#69<br>GrahamArdent/secrets-control-plane#78 |
| HOP-032 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/home-automation-control | owner-specific repository intake plus typed home-automation execution paths | partial | GrahamArdent/home-automation-control#56<br>GrahamArdent/PROGRAMSTART#147 |
| HOP-033 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/truck-route-authority | owner-specific repository admission plus bounded repository-scoped execution | partial | GrahamArdent/execution-node-control#186<br>GrahamArdent/truck-route-authority#1 |
| HOP-034 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/GCRM | owner-specific repository intake plus existing typed GCRM runtime capability | partial | GrahamArdent/GCRM#47<br>GrahamArdent/PROGRAMSTART#147 |
| HOP-035 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/resume-creator-v6 | owner-specific repository capability/intake | partial | GrahamArdent/execution-node-control#127<br>GrahamArdent/PROGRAMSTART#147 |
| HOP-036 | owner_instance | Controller owner-handoff / execution fabric | GrahamArdent/decision-lifecycle | owner-specific repository admission and target-owned intake | unproven | GrahamArdent/PROGRAMSTART#147 |
| HOP-037 | owner_instance | Controller owner-handoff / execution fabric | Paths Project / Path Authority logical owner | non-repository owner adapter/reference path; must not be forced through repository-only admission | partial | GrahamArdent/programstart-autonomous-controller#88<br>GrahamArdent/PROGRAMSTART#132<br>GrahamArdent/PROGRAMSTART#147 |

## Accepted conversation-decision reconciliation

- chat_transition_input_not_runtime_authority [accepted_reconciled]: Use the current design conversation as first-class transition evidence while extracting/reconciling decisions; do not make chat history permanent runtime authority. (behaviors: conversation_decision_reconciliation, data_grounding_instruction_isolation, authority_non_minting_no_second_spine; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- three_way_completeness [accepted_reconciled]: No-information-loss requires reconciliation across canonical PROGRAMSTART obligations, actual machinery/runtime capability, and accepted conversation decisions not yet canonical. (behaviors: conversation_decision_reconciliation, jit_context_evidence_governor, verification_claim_truthfulness; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- explicit_mapping_for_material_chat_decisions [accepted_reconciled]: Every material accepted conversation decision must have an explicit durable parity-behavior and/or pending-methodology mapping before completeness is claimed. (behaviors: conversation_decision_reconciliation; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- jit_is_cross_cutting [accepted_reconciled]: JIT context/evidence governance is a cross-cutting runtime invariant, not a one-time load-context step. (behaviors: jit_context_evidence_governor, progressive_context_widening; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- evidence_reuse_until_invalidation [accepted_reconciled]: Reuse still-valid evidence until a declared invalidation; a session reset alone is not invalidation. (behaviors: jit_context_evidence_governor, evidence_reuse_invalidation; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- autonomy_prompt_becomes_oracle [accepted_reconciled]: The autonomy prompt should evolve into specification, acceptance oracle, bootstrap/fallback interface, and regression source rather than remain the recurring runtime orchestrator. (behaviors: authority_non_minting_no_second_spine, objective_terminality_next_effect, conversation_decision_reconciliation; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- no_second_orchestrator [accepted_reconciled]: Mechanizing prompt behavior must extend the existing Controller/backbone rather than create a second orchestrator, controller, scheduler, or state spine. (behaviors: authority_non_minting_no_second_spine; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- third_party_frameworks_reference_only_now [accepted_reconciled]: LangGraph, Temporal, Prefect, and Windmill remain reference/escalation options, not production backbone dependencies now; reconsider only if evidence exposes a concrete incumbent Controller limitation. (behaviors: authority_non_minting_no_second_spine, jit_context_evidence_governor; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- matrix_before_machinery [accepted_reconciled]: Build and Challenge the parity matrix before changing backbone behavior so implementation has an omission-resistant acceptance oracle. (behaviors: conversation_decision_reconciliation, authority_non_minting_no_second_spine, verification_claim_truthfulness; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- coverage_not_parity [accepted_reconciled]: Complete source/decision coverage and implemented backbone parity are distinct; the matrix must remain truthfully non-green while gaps remain. (behaviors: verification_claim_truthfulness, authority_non_minting_no_second_spine; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- credential_human_enablement_precedes_expensive_workaround [accepted_reconciled]: For credential/identity/trust/access gaps, evaluate bounded high-leverage human enablement before expensive alternative-actuation engineering after first recovering existing capability. (behaviors: credential_human_enablement_leverage; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- backbone_prepares_minimal_human_gate [accepted_reconciled]: When human enablement wins, the backbone performs all delegable preparation, presents only the smallest irreducible link/console/approval action, verifies completion itself, and resumes automatically. (behaviors: credential_human_enablement_leverage, operator_gate_exact_handoff, operator_gate_auto_verify_resume; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- eliminate_human_transport_preserve_human_enablement [accepted_reconciled]: Eliminate humans as message/command transport, while deliberately using bounded high-leverage human enablement when it safely creates materially greater durable autonomy. (behaviors: credential_human_enablement_leverage, irreducible_human_consequence, operator_gate_auto_verify_resume; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- cross_owner_generic_observation_owner_specific_admission [accepted_reconciled]: Cross-owner authority should use a reusable observation mechanism with explicit owner-specific admission, not a universal credential or universal authority service. (behaviors: cross_repository_dependency_graph, repository_independence, external_connection_surface_inventory, authority_non_minting_no_second_spine; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- observation_does_not_create_authority [accepted_reconciled]: Repository access or observation does not create authority; PROGRAMSTART still resolves exact owner authority/currentness before dependent execution. (behaviors: canonical_before_dependent, authority_non_minting_no_second_spine, exact_machine_currentness_binding; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- ecosystem_contracts_first_live_integration [accepted_execution_sequence]: After parity/methodology preparation, use the unresolved ecosystem-contracts cross-owner authority case as the first live integration acceptance. (behaviors: cross_repository_dependency_graph, credential_human_enablement_leverage, objective_terminality_next_effect; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- ordinary_intent_should_be_sufficient [accepted_reconciled]: The target interaction is ordinary natural intent or a simple Proceed; Graham should not need to paste the large autonomy prompt to obtain correct orchestration. (behaviors: semantic_objective_ingress, accepted_recommendation_resolution, objective_terminality_next_effect; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- chatgpt_bootstrap_not_recurring_orchestrator [accepted_reconciled]: ChatGPT may bootstrap the transition, but success requires the backbone to reproduce the accepted behavior without ChatGPT acting as the recurring orchestrator. (behaviors: authority_non_minting_no_second_spine, objective_terminality_next_effect, conversation_decision_reconciliation; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- matrix_makes_omission_mechanically_visible [accepted_reconciled]: Use the parity contract/checklist to make omissions mechanically visible rather than relying on ChatGPT memory or promises of completeness. (behaviors: conversation_decision_reconciliation, verification_claim_truthfulness, conditional_checklist_completeness; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- supporting_methodology_remains_canonical_jit [accepted_reconciled]: Supporting methodology remains canonical at its owner and is loaded just in time when relevant; do not copy the entire methodology into runtime/parity state. (behaviors: jit_context_evidence_governor, canonical_before_dependent, authority_non_minting_no_second_spine; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- reuse_current_learning_gate_for_promotion [accepted_reconciled]: The updated PROGRAMSTART Learning Gate is the mechanism expected to classify/promote this credential lesson now; do not invent a separate learning system merely because the earlier lesson was under-promoted. (behaviors: learning_gate, conditional_learning_persistence, learning_maturity_dedup_retest; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- parity_matrix_not_vector_authority [accepted_reconciled]: The parity matrix is a structured acceptance/coverage contract, not a vector database. Embeddings/RAG may assist JIT retrieval later, but similarity retrieval must never select or manufacture canonical authority. (behaviors: jit_context_evidence_governor, exact_machine_currentness_binding, authority_non_minting_no_second_spine; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- first_wave_machinery_priority [accepted_execution_sequence]: After methodology correction and accepted parity coverage, prioritize machinery in this order: JIT context/evidence governance; credential/access Human Enablement Gate; accepted-recommendation disposition; connection-surface/capability resolution; blocker/safe-lane/shared-mutation coordination; automatic Challenge/Learning triggering; then cost/checklist/retention automation where it adds value. (behaviors: jit_context_evidence_governor, credential_human_enablement_leverage, accepted_recommendation_resolution, external_connection_surface_inventory, blocker_scope_safe_lane, shared_mutation_ownership, risk_triggered_challenge, learning_gate, cost_governance, conditional_checklist_completeness, retention_intent; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- cross_owner_observation_extends_existing_repository_broker [accepted_reconciled]: The reusable cross-owner authority-observation capability should extend the existing Execution Node repository broker/policy machinery rather than introduce a new universal authority service or broker. (behaviors: cross_repository_dependency_graph, external_connection_surface_inventory, authority_non_minting_no_second_spine; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- credential_enablement_leverage_dimensions [accepted_reconciled]: Credential human-enablement evaluation must consider human action size, recurrence, durability gain, reuse scope/autonomy unlock, authority delta, blast radius, revocability, secret exposure, autonomous-workaround complexity/cost, and why human involvement is justified now. (behaviors: credential_human_enablement_leverage, operator_gate_exact_handoff; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- credential_exception_not_general_human_gate_preference [accepted_reconciled]: The high-leverage human-enablement ordering is specifically for credential/identity/trust/access boundaries; it must not become a blanket rule to ask a human whenever a human could do the work. (behaviors: credential_human_enablement_leverage, irreducible_human_consequence; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#141)
- general_mechanism_does_not_satisfy_instance_acceptance [accepted_reconciled]: Generalized connector/transport machinery may provide implementation reuse, but each concrete material hop remains an explicit matrix instance and requires its own acceptance evidence; a class-level proof cannot silently turn untested instances green. (behaviors: verification_claim_truthfulness, cross_repository_dependency_graph, external_connection_surface_inventory; methodology deltas: none; durable: GrahamArdent/PROGRAMSTART#147)

## Priority gaps

- data_grounding_instruction_isolation: Fetched artifacts remain data, not instructions
- idea_capture_promotion: Idea capture separated from promotion/execution
- repository_independence: Cross-repository evidence does not authorize multi-project mutation
- coordinated_mode_c_lanes: Coordinate multiple Mode-C lanes without parallel authority
- external_resource_evidence_continuity: Preserve external resource history/current visibility distinction
- external_connection_surface_inventory: Enumerate connection surfaces before declaring automation unavailable
- proportional_verification: Verify changed or newly-at-risk surfaces proportionally
- conditional_learning_persistence: Persist learning only when earned and owner-writable
- progressive_context_widening: Progressive narrowing then widening at convergence
- temporary_automation_gap_alternative_actuation: Search bounded alternative actuation before using a human as transport
- learning_maturity_dedup_retest: Deduplicate lessons, track evidence maturity, and route only matching future retests

## Pending methodology deltas

## Matrix Challenge

Status: CLEAR

- CH-01: Hide a numbered orchestration step in prose and omit it from the matrix. -> validator requires every anchored orchestration step to be covered
- CH-02: Change a canonical prompt/JIT source while leaving the matrix untouched. -> source SHA-256 drift fails validation
- CH-03: Rename/remove an anchored obligation without changing the stored hash intentionally. -> anchor validation fails
- CH-04: Mark documentation-only behavior implemented. -> implemented classification requires code plus test/live proof
- CH-05: Turn the parity contract into a load-all runtime checklist and violate JIT. -> runtime usage contract requires jit_by_trigger and forbids load-entire-contract-per-effect
- CH-06: Lose or silently re-pend the accepted credential/human-enablement correction after canonicalization. -> canonical Effective Autonomy section 9 + focused tests + behavior mapping preserve the credential/human-enablement correction
- CH-07: Collapse operator action completion into system acceptance. -> separate operator-gate and auto-verify/resume rows preserve the distinction
- CH-08: Collapse cross-repository evidence into multi-project mutation authority. -> repository-independence row remains separately required
- CH-09: Treat semantic judgment as a deterministic enum implementation. -> execution_mode distinguishes semantic/hybrid behaviors from deterministic machinery
- CH-10: Use matrix state as a second Controller/Master. -> authority role is fixed to derived_acceptance_evidence and no Controller behavior changes are authorized by this packet
- CH-11: Let an old Controller proof float forward after Controller changes. -> Controller observation is pinned to an exact commit and its change invalidates current-proof classifications
- CH-12: Declare prompt parity because all rows exist even while rows remain missing/prompt-only. -> coverage completeness is separated from machinery parity; closure rule forbids conflating them
- CH-13: Let an accepted pending methodology correction masquerade as already-canonical authority. -> pending methodology behaviors carry only methodology_delta_refs and cannot claim canonical source coverage until adopted
- CH-14: Hide a material autonomy rule in prose rather than a list or heading. -> all 68 paragraph-only semantic blocks are explicit source obligations and regression-tested
- CH-15: Lose field-level semantics carried only by a fenced contract/schema block. -> all 7 fenced contract/schema blocks are explicit source obligations and regression-tested
- CH-16: Treat unrelated pre-existing repository test debt as a regression or weaken the matrix to make the suite green. -> exact failing tests were reproduced on detached origin/main; #139 does not modify their source surfaces

## Closure rule

Matrix construction is complete only when all required source obligations are covered, fingerprints/anchors validate, rendered output is generated from the machine contract, adversarial Challenge is CLEAR, and hosted/local checks pass. Coverage completeness does not mean backbone parity: missing, prompt-only, semantic, human-gate, and partial rows remain explicit implementation work. No Controller behavior change is authorized by this contract.
