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
