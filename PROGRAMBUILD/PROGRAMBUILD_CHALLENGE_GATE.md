# PROGRAMBUILD_CHALLENGE_GATE.md

# Challenge Gate Protocol

Purpose: Reusable transition/convergence check that catches meaningful drift without turning every boundary into the same eight-part ceremony.
Owner: Stage Owner (or Solo Operator)
Last updated: 2026-10-05
Depends on: `PROGRAMBUILD.md`, `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, `FEASIBILITY.md`, `REQUIREMENTS.md`, `DECISION_LOG.md`
Authority: Canonical for stage-transition validation, risk-based gate selection, material-delta re-Challenge convergence, post-implementation adversarial closure review, and mid-stage convergence criteria.

---

## 1. Operating Principle

Stage completion asks: **did we produce the expected output?**

The Challenge Gate asks: **is the project coherent and safe enough to proceed?**

The operating rule is:

> **Narrow while executing; widen while converging; inspect only the risks that can matter at this boundary.**

Eight gate parts exist because they represent eight recurring failure classes. They are a **menu of controls**, not a requirement that every project fill every section at every transition.

No material risk may be omitted merely to save time, but irrelevant sections should not be completed as paperwork.

### Opening questions

Name the decision and the next authorized action. Open the review with three questions:

1. **What wrong result could look successful?** Identify a plausible failure and the observation that would distinguish it from success.
2. **What have we already proven?** Reuse evidence while its binding holds. Seek the smallest missing observation that could change the decision. Recheck facts that can change before a consequential action.
3. **What else could this change affect?** When behavior changes, inspect the relevant callers, data or workflows outside the intended path.

Use the answers to select the applicable controls below. Retain the decision, evidence and limits once in the existing owner record. When the next action is supported, continue within current authority. Material corrections still require fresh review under §2.2.

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

This is a **risk-triggered use of the existing Challenge Gate**, not a new lifecycle stage, document, agent, or mandatory ceremony for every PR.

The trigger is based on what the implementation actually changed, not merely what the work packet expected to change. A supposedly low-risk packet that reveals a material trust/persistence/side-effect boundary during implementation must activate the review before closure.

A team MAY configure time/slice reminders, but elapsed time or a fixed feature count is never proof that convergence is required.

---


### 2.2 Material-Delta Re-Challenge Convergence

For a deliberate design, plan, recommendation, handoff, or other convergence review, the Challenge result applies to the **exact candidate that was challenged**.

If the Challenge produces a material corrective delta that changes authority, objective/protected outcome, scope, consequential surface, architecture/contract assumptions, dependency order, execution mechanism, evidence/currentness requirements, verification, terminal condition, or another behavior-controlling part of the candidate:

1. incorporate the material correction;
2. treat the revised result as a new candidate;
3. run a fresh applicable Challenge against that revised candidate before reporting the boundary clear.

The Challenge that changes a candidate cannot simultaneously be the final clear result for the changed candidate.

Stop on the first fresh Challenge of the current candidate that yields no new material corrective delta and no blocking unresolved finding for the declared scope. Do not repeat identical clear passes merely to accumulate review count. Re-enter only when the candidate or a material part of its authority/evidence/instruction/currentness basis changes, or when another existing stronger gate independently requires review.

`CLEAR` is scoped convergence evidence, not owner acceptance, execution permission, or a new lifecycle state. Conversational shorthand such as “settled” must not collapse those boundaries.

#### Walk through a materially changed execution path

For a material plan/prompt change, the applicable review MUST walk through the
next affected execution path before clearing that boundary. Use the actual
helper/consumer contract and current owner evidence: required inputs and
preconditions, dependency order, intended effects and unrelated state that must
survive, interruption or UNKNOWN-result recovery, and observable completion.
Select only relevant risks. A walkthrough is review, not permission to execute
the operation or generate new product/model runs. If a controlling mechanism is
not yet available, retain that exact uncertainty and its gate rather than invent
behavior or claim the path verified.

Record the concrete observations and source identities once in the existing
owner evidence. Reuse a valid walkthrough while the candidate and its material
basis remain unchanged; do not require a new walkthrough for every handoff,
wording edit, or chat. Matching hashes, headings, or an obligation count cannot
substitute for this semantic review.

Classify proposed revisions by their effect on the protected outcome. A material
corrective finding must be resolved and re-reviewed under §2.2. Optional cleanup
or a nonmaterial observation MUST NOT by itself reopen acceptance, invalidate
unaffected evidence, or force another plan/prompt version. Clearly labelled
historical instructions are not active authority merely because their words
remain present. A required safety, owner, or consequence gate is never optional
cleanup.

This requirement belongs to the existing Challenge review. It adds no lifecycle
stage, checklist service, automatic tool interception, or universal enforcement
claim. Entry prompts reference this requirement rather than maintain another
copy of its procedure.

#### Close a substantive working session from current state

Before a substantive working session ends with a recommendation, handoff,
milestone or blocker, the producer MUST reconcile the actual outcome and apply
this existing Challenge to the proposed next action **or decision to stop**.
This is a current-state closeout, not a full new review for every conversational
reply. Reuse valid evidence and review; apply §2.2's fresh review only when a
material delta or another existing trigger requires it.

Take the perspective of the person or process that will use the result. Starting
from the original request, follow the recommendation or handoff as written and
ask: “Where would I first have to guess, correct something, or ask again to get
the requested outcome?” Try one plausible wrong result that still looks
successful. Using only what the receiver gets, identify how it would tell
the difference. Where the outcome depends on an original input, a current
decision, or prior approval, check what independently establishes each at use.
Naming the expected source or reading its present value cannot establish its
earlier identity or permission. Resolve material gaps within existing authority and
walk the corrected path again under §2.2. Record the concrete gap and its
disposition, or the observation that made the next action usable, in the
existing closeout evidence. Label a simulated walkthrough as self-review.

For an apparent owner decision, check existing delegation against the exact
effect, target and conditions under the Planning Operating Model §9.6.
When covered, use that authority within the current execution scope. Otherwise
prepare the recommended choice, its limits, the evidence needed and the action
that would follow approval. Keep that consequence pending with its actual owner.

Before dispatch, reconcile the existing game plan, execution prompt and owner
evidence for scope, authority, dependency order, verification, continuation and
terminal conditions. Update only artifacts whose meaning or observed state
changed; verify current bindings and retain completed work, original attempts
and spent budgets. A stale or partly saved package is not ready to dispatch.
Record the actual review basis/disposition and one exact next assignment or stop
reason in the existing owner evidence. A blocked implementation may hand off an
authorized review or recovery assignment, but MUST NOT be labelled cleared for
implementation. Unknown effects require original-result reconciliation before
any retry.

Use the host/consumer's existing handoff contract. For the prepared-prompt
continuation consumer, retain exactly `handoff_id`, `continue`, `prompt`:
true selects a nonblank exact next assignment; false requires null and selects
no launch. Neither value establishes business success or parent acceptance.
The producer performs the applicable Challenge; the receiver checks currentness
and executes the actual prepared assignment without routine duplicate review.
New material discrepancies activate the existing review/recovery rules.
A stable original identity and exact prompt must survive uncertain delivery.

A visible chat reply is not evidence that a completion callback consumed it.
Claim automatic continuation only for an admitted consumer with an observed
receipt; a requested ChatGPT handoff additionally needs the verified target
account/Project, original Send reconciliation and receiving conversation
acknowledgment. Keep source guidance, consumer-format validation, actual delivery
and business acceptance distinct. This rule adds no transport field, dispatcher,
daemon, universal chat interception or mechanical semantic-review claim.

### 2.3 Program Start Cycle Challenge Invocation

A direct operator request to run a **program start cycle challenge**, including
PROGRAMSTART and hyphenated/case variants, invokes this existing protocol and
§2.2 through `.github/prompts/programstart-convergence-packet.prompt.md`.
An explanation question, quotation, or historical mention does not dispatch work.
The invocation inherits the requested review scope and existing execution
authorization; it does not grant merge, release, provider, or credential authority.

When the candidate includes both a game plan and an execution prompt, challenge
the complete corrected pair after the plan converges. Check matching scope,
authority, dependency order, verification, continuation, and terminal conditions.
A material correction in that combined review requires a fresh review of the
corrected pair before reporting it clear.

Retain exact candidate and protocol/owner identities, material findings and
corrections, fresh-review provenance/result, applicable combined review, evidence
references, and invalidation conditions in the existing owner evidence surface.
A bare CLEAR label or a parsable record does not establish trusted owner
acceptance or mechanical merge/activation enforcement. Known relevant blockers
remain controlling until their owner reconciles them with applicable proof.

For the bounded GitHub CLI merge path, `scripts/programstart_challenge_merge.py`
consumes an explicit repository-owner disposition from authenticated GitHub API
metadata, the exact head and methodology identity, retained finding proofs, and
native blocking reviews. Run the adapter from an accepted methodology checkout,
not candidate-controlled code. Its interface and limits are documented in
`docs/CHALLENGE_MERGE_ADAPTER.md`. It does not run semantic review or confer
independent-review provenance. Its two reads and expected-head merge guard do
not atomically fence a new same-head disposition at GitHub's mutation boundary.
Use it only within existing merge authorization and record degraded coverage;
it cannot satisfy a contract requiring an atomic disposition fence. Any merged
result remains ineligible for activation until the actual release owner accepts
the composed release. This adapter does not close issue113 or replace its
merge/activation-currentness acceptance requirements.


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
| E — Blast radius / verification | architecture, contracts, implementation, config, schema, environment, integration, or release behavior changed or is about to change materially; **required for a triggered post-implementation adversarial closure review** |
| G — Dependency / KB health | Stage 4+ when a dependency/vendor/platform/research fact is material to the decision |
| H — Architecture / requirements / implementation alignment | Stage 6+, and earlier whenever implementation already exists or a contract/auth/schema change is being evaluated; **required when the triggered closure review concerns trust/contract/schema/behavior alignment** |

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

Age/session change alone is not invalidation unless the underlying fact is genuinely time-sensitive.

---

## Part C — Scope Integrity

Compare current work against the strategic execution spine, requirements, and explicit exclusions.

Ask:

- Was scope added/removed without a decision?
- Did an out-of-scope item quietly enter the work?
- Is the success metric still current or explicitly superseded?
- Has research, an audit, checklist, adaptive-router output, or work packet begun functioning as a second strategic plan?

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

Do not use “run everything” instead of impact reasoning. Do not use narrow tests instead of a required convergence gate.

### Post-Implementation Adversarial Closure Review

When the trigger in §2.1 applies, Part E must challenge the **completed implementation**, not just confirm the intended design or rerun the tests the builder already chose.

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

For material cross-system acceptance, challenge test-authority confusion, effects outside START/STOP, participant capture of foreign closure, and false chat independence. A real originating release dependency must remain blocking even when its work is handed off. An evidence owner must not mint execution or universal acceptance authority.

For consequential control/recovery acceptance, distinguish process liveness from useful end-to-end transaction/progress. Identify shared normal/recovery process, state, credential, network and consumer-loop failure domains. Recovery must not depend exclusively on the mechanism it must repair. Test the relevant failure boundary when required by the accepted consequence; name unavoidable shared host/kernel/network dependencies as residuals. Structural health or a green component test cannot certify stronger recovery behavior.

The reviewer should prefer the smallest counterexample set that covers the material invariants. One strong realistic sequence is better than ten generic hypotheticals.

If a counterexample exposes a plausible invariant violation:

1. do not declare the packet/PR merge-ready or complete;
2. add the smallest targeted regression test or equivalent proof that reproduces/protects the failure mode when practical;
3. correct the implementation or explicitly block/reshape the slice if the issue cannot be bounded safely;
4. rerun the affected verification and the adversarial closure review against the corrected state.

If no material counterexample survives current evidence, record the challenged invariant/failure sequence and the proof that cleared it. Do not claim “adversarial review passed” merely because existing CI was green.

A separate model/agent/reviewer MAY improve independence when available, but PROGRAMBUILD does not require a new reviewer role or tool. The required property is a fresh opposition framing against the actual completed implementation.

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

Append log dispositions in review order; the last matching stage row is current.
Its `Proceed?` value must explicitly be Yes, Conditional, or No. Missing or
unrecognized decisions block rather than imply CLEAR. A supplied CLI clear or
warning cannot override a current blocking log disposition; reconcile the log
after the required remediation/review first. These legacy stage records remain
operator attestations, not authenticated candidate-bound merge/release receipts.

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

Select gate parts using PROGRAMBUILD_CHALLENGE_GATE.md:
- Lite/Product baseline: A, C, F
- add B/D/E/G/H only when stage/risk makes them relevant
- Product: use full A–H for release readiness or other whole-system convergence
- Enterprise: full A–H with appropriate retained evidence/sign-off
- if §2.1 is triggered, run Part E's post-implementation adversarial closure review and add H/other parts only when the changed risk surface requires them

For a triggered adversarial closure review:
- do not merely confirm the intended design or rerun existing happy-path tests
- assume a hidden defect may remain
- construct at least one realistic failure sequence against a material invariant using only relevant lenses such as ordering, partial failure, retry/idempotency, concurrency, restart, provider failure, trust boundary, recovery, false success, or false suppression
- if a plausible invariant violation appears, add targeted proof/test + fix and re-review before merge-ready/complete status

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
| Turning adversarial review into a mandatory generic checklist for every PR | trigger it from actual risk/blast radius and use only the lenses that can matter |
| Treating a work packet as a mini-master-plan | derive it from the spine and close/reconcile it |
| Treating newer research as authority | adopt useful deltas through canonical process |
| Re-entry by rereading/retesting everything | revalidate plausible invalidation only |
| Triggering convergence from a fixed counter alone | use actual accumulated change/risk; counters are reminders only |
| Skipping a material risk because its gate part is optional | optional means relevance-driven, not ignorable |

---

## Operating Principle

**Rigor means knowing what is authoritative, what changed, what evidence remains valid, what could still fail despite current proof, and what must be proven now. Rigor is not the number of boxes filled.**
