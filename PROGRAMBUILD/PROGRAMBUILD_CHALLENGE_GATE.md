# PROGRAMBUILD_CHALLENGE_GATE.md

# Challenge Gate Protocol

Purpose: Reusable transition/convergence check that catches meaningful drift without turning every boundary into the same eight-part ceremony.
Owner: Stage Owner (or Solo Operator)
Last updated: 2026-09-09
Depends on: `PROGRAMBUILD.md`, `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, `PROGRAMBUILD_WORK_PACKET.md`, `FEASIBILITY.md`, `REQUIREMENTS.md`, `DECISION_LOG.md`
Authority: Canonical for stage-transition validation, risk-based gate selection, post-implementation adversarial closure review, and mid-stage convergence criteria.

---

## 1. Operating Principle

Stage completion asks: **did we produce the expected output?**

The Challenge Gate asks: **is the project coherent and safe enough to proceed?**

The operating rule is:

> **Narrow while executing; widen while converging; inspect only the risks that can matter at this boundary.**

Eight gate parts exist because they represent eight recurring failure classes. They are a **menu of controls**, not a requirement that every project fill every section at every transition.

No material risk may be omitted merely to save time, but irrelevant sections should not be completed as paperwork.

### Adaptive Router Boundary

`PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` owns adaptive **decision-time** routing: whether a material decision can execute now, needs focused checks, or needs targeted/deep evidence before it should proceed.

This file owns **stage-transition, post-implementation closure, and convergence** controls. The adaptive router does not replace a Challenge Gate where the lifecycle or actual changed surface requires one, and a router result does not create a stage transition or convergence event by itself.

Reuse the same evidence instead of duplicating analysis. Typical correspondence is:

| Adaptive check family | Existing Challenge Gate parts commonly relevant later |
|---|---|
| evidence | B / G |
| consequence | A / E / F as applicable |
| boundary | E / G / H |
| proof | E / H |
| simplicity | C / E / H |
| Mode-C delta | B / C / F / H as applicable |

The table is a reuse map, not a requirement to run every listed part. If the adaptive router already produced current evidence that remains valid at a later Challenge Gate, cite/reuse it rather than rediscovering it.

If an adaptive investigation delays a protected decision, it should identify the decision being protected, missing evidence, risk of proceeding, minimum evidence required to continue, and stop condition. Do not keep a decision blocked merely because additional analysis might be interesting.

---

## 2. When To Run

Run a Challenge Gate before each PROGRAMBUILD stage transition.

During Stage 7, also run a convergence review when the current narrow execution view may no longer be sufficient, for example when:

- completed slices now interact across a shared contract/state/dependency boundary;
- architecture, requirements, auth/trust, schema, migration, environment, or dependency assumptions changed;
- trusted evidence was invalidated;
- scope/decision churn is accumulating;
- a meaningful milestone or handoff is reached;
- the next slice has materially wider blast radius;
- the operator/agent can no longer answer quickly what is authoritative and what evidence remains valid.

### 2.1 Post-Implementation Adversarial Closure Trigger

Before a completed work packet, implementation PR, or equivalent code/config change is declared **ready to merge**, **accepted**, or **complete**, run a focused post-implementation Challenge Gate when the **actual changed surface** materially affects one or more of:

- authentication, authorization, permissions, secrets, trust boundaries, security, compliance, or sensitive data;
- persistence, transactionality, delivery semantics, idempotency, retries, concurrency, ordering, or durable state;
- schema or migration behavior;
- destructive operations, payments, or consequential external side effects;
- production runtime, deployment, infrastructure, provider, or availability boundaries;
- another high-impact or hard-to-reverse invariant where a subtle implementation defect could survive ordinary happy-path tests.

Also run the focused closure review when a supposedly successful path itself supplies material counterevidence, for example:

- the work succeeded only after repeated materially similar failed attempts with little new information;
- an operator had to correct command syntax, formatting, path, permission, target, or another machine-resolvable detail after the handoff was declared ready;
- the implementation pivoted between materially different concepts after evidence weakened or falsified the original premise;
- apparent final success may hide a brittle, unsafe, unnecessarily human-dependent, or non-repeatable execution trajectory.

This is a **risk-triggered use of the existing Challenge Gate**, not a new lifecycle stage, document, agent, or mandatory ceremony for every PR.

The trigger is based on what the implementation actually changed and what the execution trajectory actually revealed, not merely what the work packet expected to change. A supposedly low-risk packet that reveals a material trust/persistence/side-effect or human-readiness defect during implementation must activate the review before closure.

A team MAY configure time/slice reminders, but elapsed time or a fixed feature count is never proof that convergence is required.

---

## 3. Gate-Part Selection

### Lite

Minimum: **A, C, F**.

Add B, D, E, G, or H only when the current transition/change makes that risk relevant.

### Product

Minimum at every stage transition: **A, C, F**.

Add stage/risk-relevant parts:

| Part | Add when |
|---|---|
| B — Assumptions / evidence | prior assumptions/evidence materially support the next decision, or an invalidation trigger may have occurred |
| D — Skipped work | anything was deferred, partial, blocked, TODO, or intentionally omitted |
| E — Blast radius / verification | architecture, contracts, implementation, config, schema, environment, integration, release behavior, or a materially suspect execution trajectory changed or is about to change materially; **required for a triggered post-implementation adversarial closure review** |
| G — Dependency / KB health | Stage 4+ when a dependency/vendor/platform/research fact is material to the decision |
| H — Architecture / requirements / implementation alignment | Stage 6+, and earlier whenever implementation already exists or a contract/auth/schema/behavior boundary is being evaluated; **required when the triggered closure review concerns trust/contract/schema/behavior alignment** |

**Full A–H Product convergence is required** when the boundary itself justifies a whole-system view, especially:

- Stage 7 → Stage 8 release readiness;
- material release candidate / production handoff;
- major architecture/scope/decision reset;
- evidence invalidation crosses several control surfaces;
- the selected parts reveal uncertainty whose blast radius cannot be bounded safely.

A post-implementation adversarial closure review does **not** automatically require full A–H. Select the minimum gate parts that cover the changed risk surface; Part E is the normal owner, with H and other parts added only when relevant.

### Enterprise

Use all eight parts with retained evidence and approver/sign-off behavior appropriate to the project. Enterprise may still reuse valid evidence; it does not need to rerun unchanged proof without an invalidation reason.

---

# The Eight Gate Parts

## Part A — Kill Criteria Re-Check

Re-read the actual applicable kill criteria from `FEASIBILITY.md`.

Ask:

- Is any kill criterion now true or materially trending true?
- Did new evidence make the original go/limited-spike decision invalid?

If yes, stop and record whether to kill, pause, reshape, or run a bounded spike.

---

## Part B — Assumption Decay And Evidence Validity

Ask:

- What relevant assumption/evidence does the next step rely on?
- What changed since it was verified?
- Did a documented invalidation trigger occur?
- What evidence remains reusable?
- What is the smallest check that re-establishes invalidated confidence?
- When concept viability was materially uncertain, is the selected concept still `supported`, or did current evidence make it `inconclusive` / `falsified`?
- If another materially similar attempt is proposed, what changed and why can that change alter the result rather than merely repeat the same hypothesis?

Age/session change alone is not invalidation unless the underlying fact is genuinely time-sensitive.

---

## Part C — Scope Integrity

Compare current work against the strategic execution spine, requirements, and explicit exclusions.

Ask:

- Was scope added/removed without a decision?
- Did an out-of-scope item quietly enter the work?
- Is the success metric still current or explicitly superseded?
- Has research, an audit, checklist, adaptive-router output, or work packet begun functioning as a second strategic plan?

For a material cross-system test, also challenge its **test authority** and **test envelope**:

- Is there exactly one behavioral owner for each proposition, or did several participants become accidental co-owners?
- Are START and STOP bounded, or can the test absorb unrelated work indefinitely?
- Did a participant inherit another owner's backlog/closure merely because it supplied evidence or a runtime hop?
- Does any evidence/currentness system appear to own the behavior merely because it can observe it?
- Is a foreign-owner item genuinely an originating-project acceptance dependency, or merely a durable handoff discovered during the test?

Reconcile unauthorized scope before proceeding.

---

## Part D — Skipped / Deferred Work

Ask:

- What was deferred, partial, blocked, TODO, or intentionally skipped?
- Is it durably tracked?
- Does it block or materially weaken the next step?
- Was something skipped because it was hard rather than unnecessary?

Resolve or explicitly accept/track blocking deferred work before proceeding.

---

## Part E — Blast Radius And Verification Scope

Ask:

- What changed since the last trusted convergence point?
- Which requirements/contracts/decisions/flows/schema/environment/runtime behaviors can it affect?
- Which prior evidence remains valid?
- Which evidence was invalidated?
- What targeted checks restore confidence?
- Does this boundary also require wider convergence verification?
- Did the execution path reveal a premise, retry, human-readiness, or repeatability defect that would be hidden if we looked only at the final state?

Do not use “run everything” instead of impact reasoning. Do not use narrow tests instead of a required convergence gate.

### Post-Implementation Adversarial Closure Review

When the trigger in §2.1 applies, Part E must challenge the **completed implementation and materially relevant execution trajectory**, not just confirm the intended design or rerun the tests the builder already chose.

Use this rule:

> **Assume the implementation may contain a hidden defect despite green current tests. Construct at least one realistic failure sequence against an important invariant on the changed risk surface.**

Select only the lenses relevant to the actual change. Common lenses are:

- **ordering** — what if operations complete in a different order than the happy path assumes?
- **partial failure** — what if a later step fails after earlier state has already changed?
- **retry / idempotency** — what if the same legitimate operation or provider delivery occurs twice?
- **concurrency** — what if two valid executions overlap?
- **restart / state loss** — what if the process, worker, device, or container dies at the worst boundary?
- **dependency/provider failure** — what if the database, API, queue, storage layer, or provider fails halfway through?
- **trust boundary** — can unauthenticated, unauthorized, replayed, malformed, stale, or cross-tenant input reach a privileged path?
- **rollback / recovery** — after failure, can the system retry/recover without corrupting or losing required state?
- **false success** — can the system report success before the required durable/observable outcome exists?
- **false suppression** — can unfinished or failed work be mistaken for already-completed work and suppressed?
- **concept lock-in** — did implementation keep perturbing one mechanism after evidence materially weakened/falsified its premise?
- **low-information retry** — were substantially similar attempts repeated without a material delta that could change the outcome?
- **human-gate readiness** — was the operator asked to execute/debug a procedure before machine-resolvable syntax, target, permission, destination, version, rollback, or post-check uncertainty was closed?
- **trajectory quality** — would the same path be safe/repeatable to standardize, or did final success depend on accidental state, manual correction, stale evidence, or avoidable human transport?

For cross-system test/acceptance changes, add the smallest relevant ownership failures:

- **test-authority confusion** — can evidence authority, acceptance authority, or a participant silently become behavioral/execution authority?
- **scope leakage** — can work outside the declared test envelope piggyback merely because the systems are already connected?
- **foreign-closure capture** — can an owner-local completed slice remain falsely open because another system's independent backlog item was observed during the test?
- **false chat independence** — when the claim is backend continuation after ChatGPT/operator-UI detachment, was the objective durably admitted before detachment, or did chat later carry command/state/polling/resume information that the backend actually needed?

For a consequential self-hosted control/recovery surface, Challenge must also test the claimed **failure domain** rather than equate structural liveness with useful control progress:

- identify the normal control path and the recovery path;
- name any shared process/unit/checkout/state store/credential/network/consumer-loop dependencies;
- ask whether failure of the normal path can eliminate the only recovery actuator;
- state exactly what a `healthy` result claims, and require a useful end-to-end transaction/progress proof when capability health — rather than merely process/service/checkout health — is being accepted;
- verify recovery can activate or restore an exact known-good version without arbitrary shell or blind replay when that is the accepted recovery consequence;
- exercise or explicitly retain residual failure domains for loss of normal transport, recovery transport, controller/VPS, and upstream provider/control-plane connectivity as applicable;
- distinguish local functions that continue without control-plane connectivity from functions that do not;
- mechanically or live exercise the relevant failure domain before broad recovery closure when that proof is required by the accepted consequence.

The invariant is scoped to consequential control/recovery systems, not every process: **no recovery claim may depend exclusively on the mechanism it is responsible for repairing, and no capability-health claim may be stronger than the transaction/progress evidence actually observed.** Shared host/kernel/network dependencies may remain when unavoidable, but name them as residual failure domains rather than hiding them.

For a concept-viability or human-gate surface, also challenge:

- whether the concept itself remained supported before deeper investment;
- whether the smallest useful falsification test was defined/run when uncertainty warranted it;
- whether each repeated attempt carried a material attempt delta plus a reason it could change the result;
- whether exploration stopped/pivoted when expected information gain became low or the premise was contradicted;
- whether an operator handoff was issued only after `GATE_READINESS: ready` and the `HUMAN_ONLY_REMAINDER` was explicit;
- whether non-secret/dummy portions, exact tool/shell/version/target, formatting/quoting/path/config shape, permission/destination, post-check, and recovery were validated to the degree warranted by the consequence before the operator was involved;
- whether any operator correction after handoff is being treated as counterevidence to the readiness claim and routed to the behavior owner.

The reviewer should prefer the smallest counterexample set that covers the material invariants. One strong realistic sequence is better than ten generic hypotheticals.

If a counterexample exposes a plausible invariant violation:

1. do not declare the packet/PR merge-ready or complete;
2. add the smallest targeted regression test or equivalent proof that reproduces/protects the failure mode when practical;
3. correct the implementation, concept, procedure, or handoff; or explicitly block/reshape the slice if the issue cannot be bounded safely;
4. rerun the affected verification and the adversarial closure review against the corrected state.

If no material counterexample survives current evidence, record the challenged invariant/failure sequence and the proof that cleared it. Do not claim “adversarial review passed” merely because existing CI was green or the final outcome eventually succeeded.

A separate model/agent/reviewer MAY improve independence when available, but PROGRAMBUILD does not require a new reviewer role or tool. The required property is a fresh opposition framing against the actual completed implementation and relevant trajectory.

---

## Part F — Decision Reversal Check

Review `DECISION_LOG.md` for contradicted, overridden, obsolete, or silently abandoned decisions.

When a decision is reversed:

- add a new row with status `REVERSED`;
- reference the original decision in the new row's `Replaces` field;
- mark the original `SUPERSEDED`;
- point the original row's `Replaces` field back to the replacing decision;
- keep both historical rows.

Example:

| ID | Date | Decision | Status | Replaces | Rationale |
|---|---|---|---|---|---|
| D-005 | 2026-04-01 | Use Postgres instead of SQLite | REVERSED | D-002 | Concurrency spike invalidated the original assumption |
| D-002 | 2026-03-15 | Use SQLite for persistence | SUPERSEDED | D-005 | Original decision superseded by D-005 |

Two contradictory active decisions are a blocking undefined state.

---

## Part G — Dependency And KB Health

Use when dependency/vendor/platform/research freshness is material.

Ask:

- Has a chosen dependency/platform been superseded or materially changed?
- Did pricing/licensing/API/support/ownership materially change?
- Is relevant knowledge current enough for this decision?
- Did a dependency/environment change invalidate trusted verification?

At implementation/release, “unknown” is unacceptable for a dependency fact that materially controls risk. Run the smallest current check/research delta needed.

---

## Part H — Architecture / Requirements / Implementation Alignment

Use when implementation exists or a contract/auth/schema/behavior boundary is material.

Ask:

- Did code/config introduce or change a contract without current architecture authority?
- Does auth/trust behavior match architecture?
- Did any P0 requirement become impossible or silently change?
- Did a relevant user/state flow change?
- Are material decisions current?
- Does the current logical/persisted work packet still trace to strategic authority?
- Were completed packets reconciled rather than accumulated as a parallel hierarchy?
- Did current changes invalidate retained test/environment/device/migration evidence?
- For a material cross-system test, does each behavioral proposition still have one test authority, with execution/evidence/acceptance authority separately respected?
- Did the test envelope end where declared, with foreign findings routed to their owners rather than silently retained as participant backlog?
- When agent behavior is part of the execution path, does the applicable `AGENTS.md` remain subordinate to and correctly reference current methodology/project authority rather than carrying stale duplicate truth?

Prospective contradiction: update canonical authority before implementing the contradictory design.

Retroactive discovery: reconcile stale authority to validated reality before further dependent work.

---

# Recording The Result

Record one machine-verifiable transition result, not eight pages of duplicated prose.

Preferred:

```bash
programstart advance --system programbuild --gate-result <clear|warning|blocked> --gate-notes "parts=<A,C,F,...>; adversarial=<not-triggered|clear|warning|blocked>; ..."
```

Compatible fallback: add a row to the Challenge Gate Log, then run `programstart advance --system programbuild`.

For a triggered post-implementation adversarial closure review that does not advance a lifecycle stage, retain the smallest useful result in the PR/work packet/owning project evidence surface: trigger reason, challenged invariant/failure sequence, result, and targeted proof/fix if any.

### Challenge Gate Log

| From Stage | To Stage | Date | Kill Criteria OK | Assumptions OK | Scope OK | Skipped Work OK | Decisions OK | Dependencies OK | Architecture OK | Proceed? | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | ✅/⚠️/❌ | ✅/⚠️/❌/n/a | ✅/⚠️/❌ | ✅/⚠️/❌/n/a | ✅/⚠️/❌ | ✅/⚠️/❌/n/a | ✅/⚠️/❌/n/a | Yes / No / Conditional | include parts run + material evidence |

Status codes:
- ✅ clear
- ⚠️ manageable issue recorded in canonical tracking
- ❌ blocking — do not proceed
- n/a = gate part was not relevant at this boundary

`programstart advance` treats missing required gate evidence and blocking results as failures unless `--skip-gate-check` is explicitly used. Any bypass is exceptional recovery and MUST be explained in `DECISION_LOG.md`.

A mid-implementation or post-implementation convergence review does not advance workflow state by itself. Record only durable findings/evidence in the appropriate canonical owner, decision log, issue/task/PR, or persisted packet when one is justified.

---

# Re-Entry Protocol

Use re-entry after a pause/material external change when prior confidence could plausibly have decayed.

Re-entry is triggered by **plausible invalidation**, not a universal number of days/weeks.

Examples:

- relevant dependency/platform/API/pricing/licensing changed;
- team/ownership change altered assumptions or operating responsibility;
- market/regulation/security/production conditions changed;
- code/config/data/deployment changed outside the trusted checkpoint;
- a relevant research track contradicts the old baseline;
- the pause was long relative to the volatility of facts the resumed work depends on.

Steps:

1. identify the strategic execution spine and last trusted checkpoint;
2. identify only the authority/evidence whose invalidation conditions could plausibly have occurred;
3. classify it: valid / invalidated / unknown-needs-check;
4. run the gate parts required by the project's variant and actual resumed risk;
5. update stale authority/evidence;
6. stop if a kill criterion is true.

Do not reread every historic file or rerun every historic test merely because time passed.

---

# Prompt Template

```text
Run the PROGRAMBUILD Challenge Gate for the current transition/convergence/closure point.

First identify:
- strategic execution spine + current stage
- what changed since the last trusted convergence point
- current logical/persisted work packet if any
- reusable evidence + invalidation triggers
- the actual completed implementation/config/runtime surface when closure or merge-readiness is being evaluated
- any concept-viability / repeated-attempt / human-gate-readiness evidence that materially affected the execution path

Select gate parts using PROGRAMBUILD_CHALLENGE_GATE.md:
- Lite/Product baseline: A, C, F
- add B/D/E/G/H only when stage/risk makes them relevant
- Product: use full A–H for release readiness or other whole-system convergence
- Enterprise: full A–H with appropriate retained evidence/sign-off
- if §2.1 is triggered, run Part E's post-implementation adversarial closure review and add H/other parts only when the changed risk surface requires them

For a triggered adversarial closure review:
- do not merely confirm the intended design or rerun existing happy-path tests
- assume a hidden defect may remain
- construct at least one realistic failure sequence against a material invariant using only relevant lenses such as ordering, partial failure, retry/idempotency, concurrency, restart, provider failure, trust boundary, recovery, false success, false suppression, concept lock-in, low-information retry, human-gate readiness, or trajectory quality
- if a plausible invariant violation appears, add targeted proof/test + fix and re-review before merge-ready/complete status

For a material cross-system test, challenge test-authority ownership, test-envelope START/STOP, participant scope, evidence-vs-acceptance-vs-execution authority, and foreign-owner handoff behavior. If the claim is chat-independent backend continuation, verify durable admission occurred before chat detachment and that no later chat-carried state/command/polling/resume was needed.

For a consequential control/recovery surface, distinguish process/service/checkout liveness from useful end-to-end control progress and challenge shared normal/recovery failure domains against the exact capability being accepted.

For a concept-viability or human-gate surface, challenge the premise separately from the implementation, require material attempt deltas for retries, reject low-information persistence, and verify `GATE_READINESS: ready` plus the exact `HUMAN_ONLY_REMAINDER` before treating operator involvement as justified.

Reuse current adaptive-router/research evidence when it remains valid. Do not rerun analysis solely because this is a transition.
Challenge vague answers. Do not fill irrelevant sections as ceremony.

Return:
- parts run and why
- adversarial closure: not-triggered / clear / warning / blocked
- challenged invariant/failure sequence when triggered
- clear / warning / blocked
- exact blockers/conditions
- evidence reused
- evidence invalidated + narrow re-verification required
- canonical reconciliation required
- whether stage advance / merge-ready / closure is permitted
```

---

# Anti-Patterns

| Anti-Pattern | Better behavior |
|---|---|
| Filling all sections without risk relevance | select the minimum gate parts that cover material risk |
| Running the adaptive router and Challenge Gate as duplicate checklists | use the router for decision-time selection, then reuse its evidence at required transition/convergence gates |
| Saying “no scope change” reflexively | compare against current requirements/spine |
| Running every test at every gate | identify invalidation, then run targeted + required convergence checks |
| Keeping verification too narrow at release | widen at release/whole-system convergence |
| Declaring a high-risk implementation merge-ready because intended behavior and current CI are green | challenge the actual completed implementation with at least one relevant counterexample/failure sequence before closure |
| Treating eventual success as proof that the execution path was sound | inspect materially suspect retry/handoff/trajectory evidence before standardizing or closing the lesson |
| Repeating substantially identical attempts after failure | require a material attempt delta plus a reason it could change the outcome; otherwise gather discriminating evidence or pivot |
| Asking the operator to debug syntax/format/path/permissions of an unvalidated procedure | finish machine-side validation and establish human-gate readiness first; operator supplies only the human-only remainder |
| Persisting with a falsified concept because more implementations are imaginable | preserve the evidence and pivot/stop; exploration is bounded by information value, not exhaustiveness |
| Burying critical agent execution rules only in deep methodology docs | keep a lean applicable `AGENTS.md` that points agents to the current owners without becoming authority itself |
| Turning adversarial review into a mandatory generic checklist for every PR | trigger it from actual risk/blast radius and use only the lenses that can matter |
| Treating a work packet as a mini-master-plan | derive it from the spine and close/reconcile it |
| Treating an evidence collector as the owner of every behavior it observes | keep test authority with the behavioral owner; evidence authority verifies evidence |
| Letting participant systems inherit another test owner's backlog | keep the test envelope bounded and route foreign findings as owner handoffs unless product authority makes them a real dependency |
| Calling a test chat-independent because a background job kept running | require durable semantic admission before detachment and no later chat-carried continuation state |
| Treating process/service/checkout liveness as proof of useful control health | match the health claim to transaction/progress evidence and challenge the failure domain the recovery claim actually covers |
| Treating newer research as authority | adopt useful deltas through canonical process |
| Re-entry by rereading/retesting everything | revalidate plausible invalidation only |
| Triggering convergence from a fixed counter alone | use actual accumulated change/risk; counters are reminders only |
| Skipping a material risk because its gate part is optional | optional means relevance-driven, not ignorable |

---

## Operating Principle

**Rigor means knowing what is authoritative, what changed, what evidence remains valid, whether the premise still deserves investment, whether human involvement is technically ready and genuinely human-only, what could still fail despite current proof, and what must be proven now. Rigor is not the number of boxes filled.**