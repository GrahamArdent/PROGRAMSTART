# PROGRAMSTART Autonomy Parity Matrix

> Derived acceptance evidence only. Canonical PROGRAMSTART sources remain authoritative.
> This is not a Master, scheduler, backlog, controller, methodology database, or execution spine.

- Contract: programstart.autonomy-parity.v1
- PROGRAMSTART baseline: GrahamArdent/PROGRAMSTART@4552d32f4884242a23b21955957fa5d7e691cf87
- Controller observation baseline: GrahamArdent/programstart-autonomous-controller@c95372bd5640110cf13791546ae1930cd0abb240
- Durable reference: GrahamArdent/PROGRAMSTART#139
- Fingerprinted source files: 8
- Required source obligations covered: 422
- Parity behaviors: 48

## JIT usage invariant

Query this contract by the current trigger/effect. Never load the full matrix into every objective.
Reuse still-valid evidence; widen only on declared invalidation or convergence boundaries.

## Coverage summary

- human_gate: 1
- implemented: 8
- missing: 1
- partial: 21
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
| credential_human_enablement_leverage — Credential/access human-enablement leverage test | missing | hybrid | pending_methodology | PROGRAMSTART + Controller |
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

## Priority gaps

- data_grounding_instruction_isolation: Fetched artifacts remain data, not instructions
- idea_capture_promotion: Idea capture separated from promotion/execution
- repository_independence: Cross-repository evidence does not authorize multi-project mutation
- coordinated_mode_c_lanes: Coordinate multiple Mode-C lanes without parallel authority
- external_resource_evidence_continuity: Preserve external resource history/current visibility distinction
- external_connection_surface_inventory: Enumerate connection surfaces before declaring automation unavailable
- credential_human_enablement_leverage: Credential/access human-enablement leverage test
- proportional_verification: Verify changed or newly-at-risk surfaces proportionally
- conditional_learning_persistence: Persist learning only when earned and owner-writable
- progressive_context_widening: Progressive narrowing then widening at convergence
- temporary_automation_gap_alternative_actuation: Search bounded alternative actuation before using a human as transport
- learning_maturity_dedup_retest: Deduplicate lessons, track evidence maturity, and route only matching future retests

## Pending methodology deltas

### credential_human_enablement_v1

For credential, identity, trust, and access gaps, recover existing capability first, then evaluate whether a tiny bounded human authorization creates materially greater durable/reusable autonomy before investing in alternative-actuation engineering. When human enablement clearly wins, the backbone prepares everything delegable, presents only the irreducible action, verifies completion itself, and resumes automatically.

Durable reference: GrahamArdent/PROGRAMSTART#139

## Matrix Challenge

Status: CLEAR

- CH-01: Hide a numbered orchestration step in prose and omit it from the matrix. -> validator requires every anchored orchestration step to be covered
- CH-02: Change a canonical prompt/JIT source while leaving the matrix untouched. -> source SHA-256 drift fails validation
- CH-03: Rename/remove an anchored obligation without changing the stored hash intentionally. -> anchor validation fails
- CH-04: Mark documentation-only behavior implemented. -> implemented classification requires code plus test/live proof
- CH-05: Turn the parity contract into a load-all runtime checklist and violate JIT. -> runtime usage contract requires jit_by_trigger and forbids load-entire-contract-per-effect
- CH-06: Lose the accepted credential/human-enablement correction before canonicalization. -> pending methodology delta must be covered by a behavior row
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
