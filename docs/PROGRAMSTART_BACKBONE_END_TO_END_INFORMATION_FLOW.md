# PROGRAMSTART Backbone End-to-End Information Flow Contract

Status: **ACCEPTED REUSABLE METHODOLOGY CONTRACT / INFORMATION-FLOW ARCHITECTURE**
Owner: **GrahamArdent/PROGRAMSTART**
Date: **2026-10-02**

Machine-readable reconstruction form: `schemas/backbone-lineage.schema.json` (V0.1).
Natural representability fixture: `tests/fixtures/backbone_lineage/controller_227.json`.
Runtime propagation status: **not implemented / not implied by this contract**.

## 1. Purpose

The GrahamArdent autonomy ecosystem already has strong owner-local contracts for semantic intake, decision closure, work-packet compilation, Controller admission/continuation, Paths discovery, execution, evidence, async events, Matrix projection, Challenge and Learning.

The missing system property is an explicit end-to-end information-flow contract that answers:

> **What information enters each backbone boundary, what meaning is transformed there, what must travel forward, what remains owner-native and reference-only, what proves the transition, and how can the original objective be reconstructed from ingress to truthful terminal outcome?**

This contract defines that reusable information-flow architecture.

It does **not** create a new Controller, scheduler, queue, lifecycle database, semantic authority, task database, evidence store, path registry, Matrix authority, Decision Lifecycle, execution engine, or cross-project roadmap.

It does **not** claim the full contract is implemented today.

## 2. Existing owners remain authoritative

This contract composes existing owners; it does not replace them.

- **PROGRAMSTART** owns reusable methodology, semantic ingress/compilation rules, Decision Closure semantics, outcome decomposition, Work Packet semantics, Challenge, Learning, authority-gap reconciliation and this information-flow contract.
- **Owning repositories** own project-specific intent, scope, architecture, decisions, requirements, mutable surfaces, acceptance and closure.
- **Controller** owns durable semantic admission, run/root state, continuation, waits/reconsideration, exact mutation coordination, retries/recovery and genuine human gates after authority exists.
- **Paths** owns path/capability discovery, reachability, composition knowledge, currentness/invalidation and equivalent-effect relationships. Paths never grants semantic permission.
- **Compute Spine / Execution Node / provider-specific owners** own admitted concrete execution mechanics and typed result production.
- **Evidence Spine** owns canonical evidence/provenance/currentness where its accepted contract applies; acceptance remains scoped to owning projects.
- **Watchtower** is an authenticated sensor/event-evidence source, not a continuation authority.
- **Ecosystem Matrix/read models** may compose current operational state; projection does not mint owner truth or execution authority.
- **Mission Control/operator surfaces** submit intent and render/interact with derived state and genuine gates; they are not execution authorities.
- **Portfolio Operations** remains derived attention/routing only.

The governing invariant remains:

> **Capture != acceptance != authority != execution.**

## 3. Canonical end-to-end flow

The backbone is modeled as a causal information flow, not one monolithic state machine:

```text
operator / Mission Control / external event
    |
    v
[1] INGRESS
    natural objective / observation / event
    |
    v
[2] SEMANTIC INTERPRETATION
    trusted interpretation + current owner/authority resolution
    |
    v
[3] DECISION SETTLEMENT
    Decision Closure / durable owner decision when needed
    |
    v
[4] OUTCOME DECOMPOSITION
    protected outcome + obligations + dependencies
    + acceptance + terminal + invalidation conditions
    |
    v
[5] CURRENT-STATE PROJECTION
    Matrix/read models compose current owner-native truth
    |
    v
[6] WORK SELECTION
    bounded Work Packet derived from current authority
    |
    v
[7] CONTROLLER ADMISSION
    sealed packet + run/root + coordination/currentness
    |
    v
[8] CAPABILITY / EFFECT DISCOVERY
    actor + effect + target -> eligible realizations
    |
    v
[9] OWNER JIT ADMISSION
    selected realization owner confirms exact current admission/currentness
    |
    v
[10] CONSEQUENCE
    existing typed Compute / Execution Node / provider / repository effect
    |
    v
[11] EVIDENCE
    typed result + canonical evidence/event references
    |
    v
[12] RECONSIDERATION
    Controller continues / retries / waits / owner-handoffs / gates
    |
    v
[13] OUTCOME VALIDATION
    re-evaluate the original protected outcome
    |
    +---- false/unproven -> derive the next required truth/effect
    |
    v
[14] RECONCILIATION / TERMINALITY
    owner truth -> evidence/currentness -> Matrix/HOP projections
    -> Challenge -> Learning -> truthful terminal disposition
```

A real objective MAY omit stages that are unnecessary. For example, a simple already-authorized observation may require no new Decision Closure record. A stage name is therefore a **projection category**, not a mandatory lifecycle state.

## 4. Stage projection vocabulary

The following vocabulary is for ecosystem-wide observability and reconstruction only:

- `INGRESS`
- `SEMANTIC_INTERPRETATION`
- `DECISION_SETTLEMENT`
- `OUTCOME_DECOMPOSITION`
- `CURRENT_STATE_PROJECTION`
- `WORK_SELECTION`
- `CONTROLLER_ADMISSION`
- `CAPABILITY_DISCOVERY`
- `OWNER_ADMISSION`
- `CONSEQUENCE`
- `EVIDENCE`
- `RECONSIDERATION`
- `OUTCOME_VALIDATION`
- `RECONCILIATION`
- `TERMINAL`

These names MUST NOT replace native component states such as Controller run states, Decision-Closure dispositions, Paths eligibility states, Matrix rows or owner-specific acceptance states.

A component MAY project one native record into one or more conceptual stages. No transition is authorized merely because a projected stage label changes.

## 5. Backbone lineage, not a universal payload

The backbone needs durable causal lineage across independently owned schemas, but it MUST NOT force every component into one giant object.

Use the following principle:

> **Propagate identity and decision-critical references. Keep owner-native payloads in their owning systems and fetch them JIT when required.**

### 5.1 Backbone Lineage V0 reconstruction envelope

The accepted V0.1 machine-readable form is a **non-authoritative reconstruction graph**, not yet an on-wire/runtime propagation format. Its records remain deliberately small.

Core correlation fields:

- `lineage_id` — stable identity for the end-to-end objective/causal flow;
- `record_id` — identity of this specific producer record;
- `record_type` — producer-defined bounded type;
- `producer_owner` — owner of the record semantics;
- `producer_record_ref` — durable reference to the canonical native record;
- `caused_by[]` — zero or more causal predecessor record references;
- `root_objective_ref` — durable reference to the originating objective when applicable;
- `owner_ref` — current substantive owner relevant to this record;
- `stage_projection` — optional informational category from section 4;
- `created_at` — producer timestamp.

Decision-critical references are conditional, not universally copied:

- `decision_ref`;
- `protected_outcome_ref`;
- `work_packet_ref`;
- `controller_run_ref`;
- `semantic_effect_ref`;
- `realization_ref`;
- `effect_attempt_ref`;
- `evidence_refs[]`;
- `authority_refs[]`;
- `currentness_refs[]`;
- `terminal_condition_ref`;
- `resume_or_reconsider_ref`;
- `invalidation_refs[]`.

This is a **lineage/correlation envelope only**. It grants no authority and cannot override the referenced owner record.

### 5.2 Causal graph, not forced tree

`caused_by[]` is plural intentionally.

Backbone work can branch, join, depend on multiple accepted facts, receive asynchronous evidence, or owner-handoff into a separately governed target lifecycle. A single parent pointer is insufficient.

The architecture therefore permits a causal DAG while retaining one stable lineage identity where the work still belongs to the same root objective.

A foreign owner MAY create its own native root/run identity while retaining a source causal reference. Causal relationship does not transfer authority.

### 5.3 Historical compatibility

Do not backfill every historical record merely to satisfy a new lineage format.

For already-existing objectives:

1. reuse an existing stable root identity when one is already canonical and sufficient;
2. derive a bounded lineage projection only when reconstruction/interoperability requires it;
3. preserve uncertainty rather than inventing missing ancestry.

No lineage record may claim complete historical coverage when the underlying evidence is partial.

## 6. Transformation receipts

The most important boundary is often not transport but **meaning change**.

Examples:

- natural language -> interpreted objective;
- accepted decision -> protected outcome;
- protected outcome -> obligations;
- current obligations -> Work Packet;
- semantic intent -> actor/effect/target;
- actor/effect/target -> selected Paths realization;
- admitted semantic effect -> typed execution request;
- typed result -> accepted owner evidence;
- evidence -> next-effect/reconsideration decision.

A material semantic transformation SHOULD be reconstructable from a compact receipt containing:

- input record/reference(s);
- output record/reference;
- transformation kind;
- producer/semantic owner;
- contract/methodology version;
- relevant authority/currentness references;
- evidence or deterministic reconstruction reference;
- invalidation conditions when material.

A transformation receipt SHOULD normally be represented by the producing component's existing durable record plus the common lineage fields. Do **not** create a second shadow artifact merely to say the same thing twice.

## 7. Information utility rule

Every handoff must distinguish:

### Propagate
Small decision-critical information needed by the next consumer without another semantic guess, such as:

- stable lineage/correlation identity;
- exact owner;
- exact authority/currentness reference;
- protected outcome / terminal-condition reference where relevant;
- exact Work Packet or effect identity;
- exact causal predecessor;
- exact invalidation/resume reference when continuation depends on it.

### Reference
Information that remains canonically available elsewhere and can be loaded JIT:

- full planning documents;
- large research/audit material;
- full logs;
- entire evidence payloads;
- historical conversation;
- unchanged architecture/requirements files;
- complete Paths registry output when an immutable revision/digest + selected typed fields is sufficient.

### Never propagate by default
- passwords, tokens, private keys or reusable credentials;
- unnecessary private/personal data;
- arbitrary provider responses;
- raw chat transcripts merely for convenience;
- caller-supplied implementation paths that would bypass discovery/owner authority;
- derived status presented as though it were owner truth.

This applies the same security lesson used by distributed context propagation systems: correlation context should remain minimal, bounded and safe to cross trust boundaries.

## 8. Boundary contract

For every material backbone boundary, the architecture must eventually be able to answer these questions:

1. **Input** — what exact record/reference enters?
2. **Owner** — who owns the incoming meaning?
3. **Transformation** — what meaning may this component derive?
4. **Forbidden inference** — what may it explicitly not infer?
5. **Output** — what durable native record/reference is produced?
6. **Lineage** — how is causality preserved?
7. **Authority/currentness** — what must be revalidated before consequence?
8. **Evidence** — what proves the transition actually happened?
9. **Invalidation** — what makes the output unsafe to reuse?
10. **Continuation** — who decides what happens next?
11. **Terminality** — what parent condition must eventually be re-evaluated?

A locally green component is not an end-to-end pass if one of these boundary answers is missing.

## 9. Round-trip closure invariant

The backbone is not complete at:

`objective -> execution -> result`

The required loop is:

```text
objective
 -> semantic settlement
 -> protected outcome
 -> decomposition
 -> bounded execution
 -> evidence
 -> semantic reconsideration
 -> protected-outcome validation
 -> next required effect OR truthful terminality
```

The existing Decision-Closure invariant remains controlling:

> **Task or Work Packet completion is not sufficient parent closure.**

When all known work is complete but the protected outcome remains false, ambiguous or materially unproven, the objective remains open and must be re-decomposed/reconciled rather than terminalized.

## 10. Cold-reconstruction acceptance

The strongest acceptance test for this contract is a **fresh-context reconstruction**.

Given only one stable starting identity — preferably `lineage_id`, or a canonical pre-existing root objective identity — a fresh observer should be able to reconstruct, through durable references rather than chat memory:

1. the original objective;
2. semantic interpretation and owner;
3. material settled decision(s), if any;
4. protected outcome;
5. current obligations/dependencies;
6. current Work Packet;
7. Controller root/run;
8. relevant mutation/currentness admission;
9. capability/effect discovery result;
10. owner JIT admission/currentness;
11. exact consequence/effect attempt;
12. resulting evidence;
13. any async wait/event/human gate;
14. Controller reconsideration;
15. current protected-outcome status;
16. exact terminal/blocker/next-effect reason;
17. any derived Matrix/HOP/portfolio projection;
18. evidence/invalidation conditions supporting the current conclusion.

The observer MUST be able to distinguish:

- **not present**;
- **not required**;
- **unknown/partial coverage**;
- **known but stale/invalidated**;
- **current and proven**.

It must never fabricate a missing link merely to produce a complete-looking trace.

Passing this test demonstrates **decision-complete reconstruction**, not execution authority.

## 11. Natural falsification fixture: Controller #227

`GrahamArdent/programstart-autonomous-controller#227` is the first natural black-box fixture because it already spans multiple backbone boundaries without being created for this documentation contract.

Its protected path is:

`semantic objective -> actor/effect/target -> deterministic Paths query -> owner JIT verification -> existing typed effect -> durable result -> Controller continuation`.

### 11.1 What #227 has already proven

A fresh private semantic objective reached the deployed backbone through the actual external contract:

- private objective ingress;
- trusted semantic interpretation;
- owner authority resolution;
- sealed packet persistence;
- real Controller root/run creation;
- no caller-selected realization/provider/command/path;
- no recurring conversational transport.

The live fixture then exposed real missing boundaries one at a time.

#### Boundary A — exact PREPARE admission

Semantic implementation permission did not imply the exact machine PREPARE token required by the existing Controller continuation machinery.

Controller PR #236 repaired only that admission token rather than widening generic authority.

#### Boundary B — objective-ingress continuation

After semantic handoff, the private PROGRAMSTART objective ingress stopped instead of reusing the already-accepted Runtime V3 initial repository continuation.

Controller PR #237 / commit `d11ae41f18a05d5df5b5b90210e5688281e4516d` repaired the composition by reusing the existing continuation primitive.

#### Boundary C — Controller self-hosting repository capability

The next fresh live objective advanced farther and truthfully stopped because the current Execution Node repository capability fabric did not admit `GrahamArdent/programstart-autonomous-controller`.

That is currently a Controller self-hosting capability gap, not a Paths defect and not a human gate.

### 11.2 Why #227 is a valid falsifier

#227 demonstrates the exact architectural failure class this contract is intended to expose:

```text
locally accepted segment
 -> previously implicit handoff
 -> fresh end-to-end run
 -> first unsupported boundary becomes visible
```

The contract must therefore **not** describe an idealized flow as though it already exists.

A cold reconstruction of #227 today should end truthfully at the current self-hosting capability boundary. It must show the successful prior transitions and the current first unproven edge.

After that owner-native capability is repaired, the same fixture should continue without changing the original semantic objective until the Paths discovery / owner-JIT / typed result / continuation sequence is either proven or the next real unsupported boundary is localized.

## 12. External architecture patterns used only as references

This contract intentionally borrows principles, not dependencies.

### W3C Trace Context

W3C Trace Context standardizes portable request/parent correlation across independently deployed components. The relevant lesson is durable cross-component correlation with explicit ancestry, not adoption of HTTP tracing headers as semantic authority.

Reference: https://www.w3.org/TR/trace-context/

### CloudEvents

CloudEvents separates small context attributes from producer-specific event data. The relevant lesson is a small interoperable envelope around owner-native payloads rather than a universal business schema.

Reference: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md

### OpenTelemetry context propagation

OpenTelemetry demonstrates propagated correlation plus an important security boundary: arbitrary baggage can leak sensitive/internal data across service boundaries. The relevant lesson is to propagate only bounded correlation/decision-critical context.

Reference: https://opentelemetry.io/docs/concepts/context-propagation/

### DBOS durable workflow recovery

DBOS recovers durable workflows from previously completed steps after interruption. The Controller already uses DBOS for its own durable semantic workflow substrate; the relevant gap here is not another durability engine but cross-owner semantic lineage.

Reference: https://docs.dbos.dev/python/tutorials/workflow-tutorial

None of these references becomes an ecosystem production dependency through this document.

## 13. PROGRAMSTART Challenge result

This proposal was challenged against current PROGRAMSTART authority before persistence.

### Part B — assumption/evidence validity

**CLEAR WITH RESIDUALS.**

Current owner boundaries are supported by PROGRAMSTART Decision Closure, Matrix Coordination, Work Packet semantics, current Controller/Paths/Execution Node/Evidence Spine repository authority, and the live #227 history.

Residual: the complete lineage envelope has not yet been implemented or proven end-to-end. This document therefore defines architecture/acceptance semantics only.

### Part C — scope integrity

**CLEAR after narrowing.**

Rejected shapes:

- a new global lifecycle/state machine;
- a universal payload schema;
- a second Matrix;
- a global task database;
- a new evidence store;
- a new Controller/orchestrator;
- mandatory artifact creation at every boundary;
- retroactive backfill of all historical work.

The stage vocabulary is informational projection only. Owner-native state remains authoritative.

### Part D — skipped/deferred work

**EXPLICITLY DEFERRED / NON-BLOCKING FOR THIS CONTRACT.**

Not implemented by the architecture contract itself:

- live Controller/Paths/Compute/Execution Node lineage propagation;
- Matrix lineage projection;
- Evidence Spine indexing changes;
- automatic cold-reconstruction CLI/API;
- historical migration/backfill.

The bounded V0.1 reconstruction schema and first natural fixture are now defined separately and remain non-authoritative.

Those are follow-on implementation candidates only if this architecture survives natural fixtures. Their absence means **not implemented**, not a failed documentation contract.

### Part E — blast radius / failure challenge

**CLEAR after adversarial corrections.**

Counterexamples considered:

1. **One parent pointer cannot represent joins/async evidence.**
   - Correction: `caused_by[]` is plural; causal DAG allowed.

2. **A lineage ID could accidentally become execution authority.**
   - Correction: lineage is correlation only; consequence still requires current owner authority and Controller admission.

3. **A stage model could become a second runtime lifecycle.**
   - Correction: stage names are derived projections; native states remain controlling.

4. **A foreign-owner handoff could falsely imply authority transfer.**
   - Correction: target may have a distinct native lifecycle while preserving source causal references; transport/lineage never transfers authority.

5. **Cold reconstruction could fabricate missing history.**
   - Correction: `unknown/partial` is first-class; no self-attested completeness.

6. **A universal envelope could duplicate sensitive/full payloads.**
   - Correction: propagate minimal references; JIT-load owner-native payloads; secrets/private payloads prohibited by default.

7. **A complete-looking execution chain could still miss the user's end goal.**
   - Correction: protected-outcome validation is the required return edge before terminality.

8. **A known capability could be selected from stale reachability evidence.**
   - Correction: discovery and consequence-time owner currentness/admission remain distinct.

### Part F — decision reversal

**NO REVERSAL REQUIRED.**

This contract extends and composes the accepted Decision Closure -> outcome decomposition -> Matrix -> Work Packet -> execution/evidence -> protected-outcome-validation model. It does not supersede that decision.

### Part G — dependency / external-reference health

**CLEAR.**

External standards are reference patterns only and are not runtime dependencies.

### Part H — architecture / requirement / implementation alignment

**CLEAR WITH EXPLICIT IMPLEMENTATION GAP.**

The architecture matches current owner boundaries. The lineage/cold-reconstruction property is not yet fully implemented across those owners.

That gap is the point of the contract and must remain visible rather than being declared solved by documentation.

## 14. GO / NO-GO

### GO

Adopt this as the reusable architecture contract for auditing and designing backbone information flow.

Use #227 as the first natural falsification fixture.

Use the cold-reconstruction test as the acceptance oracle for any later lineage implementation.

### NO-GO

Do not yet:

- create another orchestration service;
- introduce another lifecycle database;
- bulk-modify all owner schemas;
- force every record into one payload;
- create a central authority registry;
- backfill the ecosystem;
- mark the flow contract implemented merely because this document exists.

## 15. Next bounded step after Lineage V0.1 representability acceptance

The next step is still **not runtime propagation**.

Challenge the V0.1 reconstruction model against at least one independent natural objective whose causal shape materially differs from #227—for example an async-event or genuine human-gate flow—before treating the schema as reusable enough to wire across live components.

The second fixture must test the abstraction rather than replay #227's exact shape. If it exposes missing fields, change the reconstruction contract first. If V0.1 survives, then separately design the smallest owner-native propagation/adoption slice and challenge its write surfaces before runtime mutation.

That preserves PROGRAMSTART's rule:

> **Research and architecture exist to retire decision-relevant uncertainty; extend existing mechanisms before creating new ones.**
