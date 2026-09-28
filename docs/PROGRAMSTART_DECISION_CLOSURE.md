# PROGRAMSTART Decision-Closure Contract

Purpose: define the smallest reusable semantic contract for turning material conversation/research/audit outcomes into explicit, owner-routed closure evidence without creating a new authority or execution system.

Status: **PROGRAMSTART reusable semantic contract / subordinate to owning-project authority**.

Machine-readable form: `schemas/decision-closure.schema.json`.

This contract is a **receipt/projection contract**, not a lifecycle database, queue, backlog, orchestrator, Matrix authority, or execution grant.

## 1. Owner model

PROGRAMSTART owns the reusable Decision-Closure semantics because it already owns retention intent, accepted-recommendation resolution, Challenge/decision quality, and Authority-Gap reconciliation.

Other components retain their current responsibilities:

- **Portfolio Operations** — conversation recovery, candidate preservation, reconciliation plumbing, resurfacing, and producer/consumer use of closure receipts.
- **Owning project repositories** — substantive durable scope, architecture, acceptance, decisions, sequencing, and execution authority.
- **Evidence Spine** — evidence/provenance/currentness/invalidation where its existing authority applies.
- **Controller/runtime** — durable execution binding, continuation, retries, and resource ownership after real authority exists.
- **ecosystem-contracts** — genuinely cross-owner invariants only when separately earned; it is not the default home for conversation outcomes.
- **Matrix/read models** — may later project Decision-Closure results for coordination, but projection does not mint the underlying truth.
- **Decision Lifecycle repository** — prototype/falsification/salvage evidence after its 2026-09-25 re-foundation; not the target runtime owner.

## 2. Core invariant

> **Capture != acceptance != authority != execution.**

A Decision-Closure receipt may describe all four boundaries, but it may never collapse them.

The schema therefore requires `execution_authority: false` at both receipt and outcome level. A consumer must independently resolve current owner authority before consequential execution.

## 3. What the receipt represents

A receipt records, relative to a declared source scope:

1. what material outcomes were identified;
2. what coverage/omission challenge was actually performed;
3. each outcome's explicit disposition;
4. whether the outcome was accepted, not accepted, unresolved, or not applicable;
5. whether durable owner authority already exists, was reconciled, is absent, or remains unresolved;
6. currentness/supersession;
7. evidence/provenance references;
8. optional owner/revisit references.

It does **not** store raw conversation by default and does not become canonical over the referenced owner.

## 4. Coverage semantics

`coverage.status` is deliberately limited to:

- `unknown`
- `partial`
- `challenged`

There is no self-attested `complete=true`.

`challenged` requires an independent-review or adjudicated-fixture method plus evidence references. It means the declared source scope was challenged; it does not claim universal semantic completeness.

If source access is incomplete, the receipt must preserve that limitation in `coverage.residuals`.

## 5. Outcome semantics

Use the smallest truthful `kind` and one disposition:

- `ALREADY_DURABLE`
- `ROUTED_REFERENCE`
- `RECONCILED_AUTHORITY`
- `CANDIDATE_PRESERVED`
- `TRIGGER_ARMED`
- `READY_FOR_REVIEW`
- `PRIVACY_EXCLUDED`
- `ROUTINE_EXCLUDED`
- `UNRESOLVED`

Disposition is separate from:

- `acceptance_state`
- `authority_state`
- `currentness_state`

That separation is intentional. For example, a historically accepted decision can be `superseded`, while a useful proposal can be `CANDIDATE_PRESERVED` without becoming accepted authority.

## 6. Required proof rules

The schema mechanically enforces several boundaries:

- accepted outcomes require acceptance-evidence references;
- already-durable/reconciled authority requires an owner reference;
- owner-routed dispositions require an owner reference;
- superseded outcomes require a superseding reference;
- trigger-armed outcomes require a revisit trigger;
- challenged coverage requires independent/adjudicated evidence;
- execution authority is always false.

The schema cannot prove semantic recall by itself. Fixture-backed evaluation or another authorized coverage contract owns that proof.

## 7. When to use it

Use a machine-readable receipt when interoperability, auditability, handoff, Matrix projection, acceptance testing, or durable cross-session reconciliation benefits from one.

Do **not** require a receipt for every ordinary conversation. PROGRAMSTART's existing semantic retention/reconciliation behavior may remain lightweight when no machine-readable interchange is needed.

## 8. Natural acceptance fixture

`tests/fixtures/decision_closure/current_conversation.json` is the first natural fixture.

It proves that one receipt can simultaneously represent:

- an accepted/current owner decision;
- a preserved but unaccepted architecture proposal;
- an unresolved architecture question;
- a formerly accepted but superseded decision;
- a finding routed to the correct owner without becoming authority.

The fixture is acceptance evidence for contract expressiveness, not proof that every future conversation will be semantically complete.

## 9. Placement decision

The contract stays in PROGRAMSTART because the semantics are reusable methodology shared across projects.

It is **not** added to every generated child repository in this slice. Distribution/materialization into generated repos is a separate concern and should be reconciled with the active generated-repo transition work rather than widening this contract-placement change.

Likewise, Matrix gateway/storage/mandatory-ingress implementation remains outside this contract-placement objective.


## 10. Accepted-outcome decomposition and Matrix handoff

Decision Closure answers **what was decided**. When an accepted, current material outcome is to be operationalized, PROGRAMSTART must next derive **what must become true because of that decision** before bounded execution work is selected.

This is an **outcome decomposition**, not a new lifecycle, planner, backlog, authority source, or extension of the Decision-Closure receipt into execution state.

### 10.1 Eligibility

Decompose only an outcome that is both:

- `acceptance_state: accepted`; and
- `currentness_state: current`.

Rejected/not-accepted, unresolved, superseded, routine-excluded, or historical outcomes remain useful Decision-Closure evidence but do not silently become current Matrix obligations.

### 10.2 Derived handoff

For each eligible material outcome being operationalized, derive the smallest sufficient handoff containing:

- `decision_ref` — stable reference to the settled Decision-Closure outcome or its durable owner record;
- `protected_outcome` — observable result the accepted decision intends to make true;
- `obligations[]` — the minimum complete set of outcome obligations that must become true;
- `dependencies[]` — only material relationships needed to understand obligation readiness/order;
- `acceptance_conditions[]` — evidence conditions that demonstrate the obligations/protected outcome;
- `terminal_condition` — the condition under which the parent outcome can truthfully close;
- `invalidation_conditions[]` — events/evidence that require decomposition/currentness to be reconsidered.

Outcome obligations describe **required truths/results**, not prematurely invented implementation tasks. Owning project/runtime mechanisms determine implementation after reconciliation.

The handoff is derived/reconstructable and must not become a second copy of historical Decision-Closure state.

### 10.3 Completeness Challenge

Before a decomposition may be projected as complete, challenge it with:

> **Could every listed obligation be satisfied while the protected outcome is still materially false?**

If yes, the decomposition is incomplete. Add/correct the missing outcome obligation or narrow/reshape the protected outcome before downstream projection.

This Challenge is distinct from Decision Closure's source-coverage/omission Challenge:

- **source coverage** asks whether material outcomes from the declared source were missed;
- **outcome completeness** asks whether the accepted decision's derived obligations are sufficient to make its protected outcome true.

Neither permits a self-attested universal `complete=true`; retain evidence/residuals appropriate to the fixture or consumer.

### 10.4 Matrix projection boundary

After the decomposition survives the completeness Challenge, a Matrix/read-model consumer may project the **current** operational view, including:

- the protected outcome as parent objective/outcome;
- current obligations and their relationships/dependencies;
- acceptance and terminal conditions;
- current status/blocker/evidence/currentness references as supplied by their existing owners;
- the `decision_ref` needed to trace the operational view back to the settled semantic outcome.

Do not project rejected/superseded/history-only outcomes as current obligations merely to preserve conversation history. Decision Closure/owning decision records retain that history.

Matrix projection does not select implementation by itself. Existing PROGRAMSTART Work Packet semantics derive the bounded current executable slice only after the current obligations have been reconciled into the operational view.

### 10.5 Closure invariant

Task or Work Packet completion is not sufficient parent closure.

Before the parent outcome is considered fulfilled, re-evaluate the original `protected_outcome` against current acceptance evidence. If all known tasks are complete but the protected outcome remains false or materially unproven, the objective remains open and the decomposition must be challenged/reconciled rather than falsely terminalized.

### 10.6 Natural fixture

The first natural fixture for this extension is the 2026-09-28 conversation that challenged Decision Lifecycle placement, retained Decision Closure in PROGRAMSTART, rejected a new consequence-planner subsystem, and accepted:

`conversation -> Decision Closure -> protected outcome -> outcome decomposition -> completeness Challenge -> Matrix -> Work Packet -> execution/evidence -> protected-outcome validation`.

The fixture must preserve superseded/rejected/unresolved discussion without projecting it as current obligations, and must demonstrate that an intentionally incomplete obligation set fails the outcome-completeness Challenge.
