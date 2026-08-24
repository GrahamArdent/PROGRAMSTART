# PROGRAMBUILD_CHALLENGE_GATE.md

# Challenge Gate Protocol

Purpose: Reusable stage-transition and convergence checklist that prevents silent drift, scope creep, assumption rot, duplicate execution authority, and stale verification evidence.
Owner: Stage Owner (or Solo Operator)
Last updated: 2026-08-24
Depends on: `PROGRAMBUILD.md`, `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, `FEASIBILITY.md`, `REQUIREMENTS.md`, `DECISION_LOG.md`
Authority: Canonical for stage transition validation and mid-stage convergence criteria

---

## Why This Exists

Stage completion answers “did we produce the expected output?” The Challenge Gate asks whether the project is still coherent enough to proceed.

It catches eight recurring failure classes:

1. kill criteria becoming true without anyone noticing;
2. assumptions weakening while downstream work treats them as settled;
3. scope drifting outside approved requirements;
4. deferred work being silently forgotten;
5. blast radius being underestimated;
6. decisions being reversed without reconciliation;
7. dependency/research evidence going stale;
8. architecture, requirements, implementation, work packets, and verification evidence drifting apart.

The operating rule is: **narrow while executing; widen while converging.** Work packets may narrow daily execution. Challenge Gates deliberately widen the view again.

---

## When To Run

Run this gate before starting a new PROGRAMBUILD stage.

| Transition | Challenge Gate Required |
|---|---|
| Idea Intake → Stage 0 (Inputs) | Yes |
| Stage 0 → Stage 1 (Feasibility) | Yes |
| Stage 1 → Stage 2 (Research) | Yes |
| Stage 2 → Stage 3 (Requirements) | Yes |
| Stage 3 → Stage 4 (Architecture) | Yes |
| Stage 4 → Stage 5 (Scaffold) | Yes |
| Stage 5 → Stage 6 (Test Strategy) | Yes |
| Stage 6 → Stage 7 (Implementation) | Yes |
| Stage 7 → Stage 8 (Release Readiness) | Yes |
| Stage 8 → Stage 9 (Audit) | Yes |
| Stage 9 → Stage 10 (Post-Launch) | Yes |

During Stage 7, also run a **mid-implementation convergence review when risk indicates that the narrow work-packet view is no longer enough**. Typical triggers include:

- several completed slices now interact across the same contract, state, or dependency boundary;
- architecture, requirements, auth/trust, schema, migration, environment, or dependency assumptions changed;
- previously trusted evidence was invalidated;
- scope or decision churn is accumulating;
- a meaningful milestone or handoff has been reached;
- the blast radius of the next slice is materially wider than the current packet;
- the operator or agent can no longer answer quickly what remains authoritative and what evidence is still valid.

A team MAY choose a time- or slice-based reminder as a local heuristic, but PROGRAMBUILD does not define a universal feature count or calendar cadence as proof that convergence is due.

---

# The Eight-Part Checklist

## Part A — Kill Criteria Re-Check

Re-read the actual kill criteria from `FEASIBILITY.md`.

| Kill Criterion | Still False? | Evidence | Action If True |
|---|---|---|---|
| (copy from FEASIBILITY.md) | Yes / No / Trending | | |
| | | | |
| | | | |

If any criterion is true or trending materially toward true, stop and record the finding in `DECISION_LOG.md`. Decide whether to kill, pause, reshape, or run a bounded spike.

Do not rely on an old “all clear” result if a relevant assumption, dependency, market condition, regulation, architecture choice, or production signal changed since that result.

---

## Part B — Assumption Decay And Evidence Validity

List the top assumptions and important retained evidence from prior stages/slices.

| Assumption / Evidence | Source | Current Direction | Invalidation Trigger Occurred? | Action |
|---|---|---|---|---|
| | | ↑ Stronger / → Same / ↓ Weaker | Yes / No | |
| | | | | |
| | | | | |

Ask:

- What changed since the last convergence point?
- Which assumption or verification artifact could that change invalidate?
- Which prior evidence remains trustworthy because its scope and invalidation conditions still hold?
- Which evidence must be re-established now?

If an assumption weakened, name the blast radius. If evidence was invalidated, rerun the smallest check set needed to restore confidence. Do not repeat broad verification when no relevant trigger occurred.

---

## Part C — Scope Integrity Check

Compare current work against the inputs block, `REQUIREMENTS.md`, and the strategic execution spine for an existing/in-flight project.

| Question | Answer |
|---|---|
| Has anything been added that is not authorized by the inputs/requirements/execution spine? | Yes / No — if yes, list it |
| Has anything been removed without a recorded decision? | Yes / No — if yes, list it |
| Has any out-of-scope item quietly moved into scope? | Yes / No — if yes, name it |
| Is the success metric still the same or explicitly superseded? | Yes / No |
| Has a research document, audit, readiness review, checklist, or `CURRENT_WORK_PACKET.md` started functioning as a second master plan? | Yes / No — if yes, reconcile it |

If scope changed without a decision entry, record and reconcile it before proceeding.

A work packet may contain the **current slice** only. It must not redefine project strategy, requirements, architecture, or milestone sequence.

---

## Part D — Skipped Work Check

| Question | Answer |
|---|---|
| Was anything in the previous stage/slice deferred, partially completed, or marked TODO? | Yes / No — if yes, list it |
| Is deferred work durably tracked? | Yes / No |
| Does it block the next stage/convergence decision? | Yes / No |
| Was anything skipped because it was difficult rather than unnecessary? | Yes / No |
| Did closing/replacing a work packet strand any unresolved obligation outside canonical tracking? | Yes / No |

If deferred work blocks the next stage, resolve it or record explicit risk acceptance/deferral before proceeding.

---

## Part E — Blast Radius And Verification Scope

| Question | Answer |
|---|---|
| What changed since the last gate/convergence point? | |
| Which requirements, contracts, decisions, flows, migrations, environments, or operational behaviors could that change affect? | |
| What is the most expensive mistake the next stage could make? | |
| Which existing evidence remains valid? | |
| Which invalidation triggers occurred? | |
| What targeted checks are required now? | |
| What broader convergence checks are required at this boundary? | |

The gate must distinguish **slice verification** from **convergence verification**.

- Slice verification proves the changed/at-risk surface.
- Convergence verification checks cross-slice coherence and release/stage-wide assumptions.

Do not use “run everything” as a substitute for blast-radius reasoning. Do not use narrow tests as a substitute for a required convergence gate.

---

## Part F — Decision Reversal Check

Review `DECISION_LOG.md` for contradicted, overridden, or obsolete decisions.

| Question | Answer |
|---|---|
| Are there decisions whose rationale no longer holds? | Yes / No — if yes, list them |
| Are active decisions contradictory? | Yes / No — if yes, identify both |
| Has a decision been silently abandoned? | Yes / No — if yes, name it |
| Did a work packet, audit, or research recommendation introduce a material decision that never reached the decision log/canonical owner? | Yes / No |

### Reversal rule

When a decision is reversed:

- add a new row with status `REVERSED`;
- reference the original decision in the new row's `Replaces` field;
- mark the original `SUPERSEDED`;
- point the original row's `Replaces` field back to the replacing decision, matching the repository's enforced reciprocal-link invariant;
- keep both historical rows.

Example:

| ID | Date | Decision | Status | Replaces | Rationale |
|---|---|---|---|---|---|
| D-005 | 2026-04-01 | Use Postgres instead of SQLite | REVERSED | D-002 | Concurrency spike invalidated the original assumption |
| D-002 | 2026-03-15 | Use SQLite for persistence | SUPERSEDED | D-005 | Original decision superseded by D-005 |

Two contradictory active decisions are a blocking undefined state.

---

## Part G — Dependency And KB Health Check

Run at Stages 4+ for Product; follow the stricter Enterprise requirements where applicable.

Use current dependency evidence, the PROGRAMSTART knowledge base, and research delta tooling.

| Question | Answer |
|---|---|
| Are relevant research tracks current enough for this decision? | Yes / No — if no, list them |
| Has a chosen dependency been superseded for new work? | Yes / No — if yes, name it |
| Has pricing, licensing, API behavior, support status, or ownership materially changed? | Yes / No / Unknown |
| Is a critical KB coverage domain only seed/partial? | Yes / No |
| Did a dependency/environment change invalidate previously trusted verification? | Yes / No — if yes, what must be rerun? |
| For new decisions, what downstream authority is affected? | List or n/a |

At Stage 7+, “Unknown” on a material dependency question is not acceptable. Run a current check or research delta proportional to the decision.

If a dependency is deprecated/superseded or materially changed, record the decision to migrate, accept risk, or spike an alternative.

---

## Part H — Architecture, Requirements, Work-Packet, And Implementation Alignment

Run at Stages 6+. Required during Stage 7 convergence reviews for Product/Enterprise. Lite adds Part H whenever the current change can affect architecture, requirements, auth/trust, contracts, schema, or cross-slice behavior.

| Question | Answer |
|---|---|
| Have architecture contracts changed in code without updating `ARCHITECTURE.md`? | Yes / No — if yes, list them |
| Were new contracts/endpoints/auth rules introduced without architecture authority? | Yes / No — if yes, list them |
| Does implemented auth/trust behavior match architecture? | Yes / No / Not yet implemented |
| Are any P0 requirements now impossible or silently changed? | Yes / No — if yes, name them |
| Has a relevant `USER_FLOWS.md` behavior been silently dropped/changed? | Yes / No / n/a |
| Is `DECISION_LOG.md` current for material design/scope changes? | Yes / No |
| Does every active `CURRENT_WORK_PACKET.md` still trace to current strategic authority and exact scope? | Yes / No / n/a |
| Are completed/replaced packets reconciled into canonical state instead of accumulating as a parallel hierarchy? | Yes / No / n/a |
| Did any code/config change invalidate retained test/environment/device/migration evidence? | Yes / No — if yes, list required re-verification |

If implementation diverges from architecture prospectively, update architecture authority first before continuing the contradictory design.

If an existing conflict is discovered retroactively, validated behavior may reveal stale documentation; reconcile the canonical documents and decisions before further dependent work.

If a P0 requirement is impossible, stop and re-run Part A/feasibility reasoning as needed.

---

# Recording The Result

After all required parts, record a machine-verifiable outcome before advancing.

Preferred:

```bash
programstart advance --system programbuild --gate-result <clear|warning|blocked> --gate-notes "..."
```

Compatible fallback: add a row to the Challenge Gate Log, then run `programstart advance --system programbuild`.

### Challenge Gate Log

| From Stage | To Stage | Date | Kill Criteria OK | Assumptions OK | Scope OK | Skipped Work OK | Decisions OK | Dependencies OK | Architecture OK | Proceed? | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌/n/a | ✅/⚠️/❌/n/a | Yes / No / Conditional | |

Status codes:
- ✅ All clear
- ⚠️ Manageable issue recorded in canonical tracking
- ❌ Blocking issue — do not proceed

`programstart advance` treats missing gate evidence and blocking results as failures unless `--skip-gate-check` is explicitly used. Any bypass is exceptional recovery and MUST be explained in `DECISION_LOG.md`.

A **mid-implementation convergence review** does not advance workflow state. Record its findings/evidence in the appropriate canonical owner, decision log, work packet close-out, or project issue tracker.

---

# Variant Adjustments

| Variant | Gate Rigor |
|---|---|
| Lite | Parts A, C, and F minimum; add B, D, E, G, or H whenever the current risk/change makes them relevant. |
| Product | Complete all eight parts at stage transitions. Part G required at Stages 4+. Part H required at Stages 6+. Mid-Stage-7 convergence reviews may focus on the parts implicated by the accumulated changes, but cannot omit a material risk merely for brevity. |
| Enterprise | Complete all eight parts with retained evidence and approver sign-off. Part G required at stages where dependency health is material. Evidence reuse requires provenance, scope, and invalidation conditions. |

---

# Re-Entry Protocol

Use this instead of the normal gate when a project resumes after a pause or material external change that could have invalidated the prior baseline.

Re-entry is triggered by **plausible evidence decay**, not a universal number of days or weeks. Examples include:

| Condition | Trigger |
|---|---|
| Time/pause | long enough relative to project volatility that relevant facts, dependencies, state, or assumptions may have changed |
| Team/ownership | material ownership or responsibility change |
| Dependency/platform | relevant version, API, pricing, licensing, support, or ownership change |
| Research | a relevant research track reports a changed recommendation or stale critical evidence |
| External environment | market, regulation, vendor, security, deployment, or operating condition affects prior assumptions |
| Project state | code/config/data/deployment changed outside the prior trusted checkpoint |

A team MAY configure local reminder intervals for its domain, but those are heuristics, not PROGRAMBUILD-wide truth.

### Re-Entry Steps

1. Identify the strategic execution spine and last trusted project checkpoint from durable state, not memory.
2. Identify the **minimal prior authority/evidence set whose invalidation conditions could plausibly have occurred during the pause**.
3. Review that set with a risk-based lens:
   - still valid;
   - stale;
   - invalidated;
   - unknown and requires current check.
4. Check relevant dependencies/research freshness.
5. Re-read kill criteria relevant to the resumed work.
6. Run all eight Challenge Gate parts for the transition back into active work when Product/Enterprise requires the full gate; Lite follows its risk-proportional rule.
7. Record a re-entry result and update stale authority before proceeding.
8. If a kill criterion is true, stop rather than resuming on momentum.

Do not blindly reread every historic file or rerun every historic test merely because time passed. Re-entry should be broad enough to restore confidence, but driven by plausible invalidation and current risk.

---

# Prompt Template

```text
Act as a critical reviewer. Run the PROGRAMBUILD Challenge Gate for the current transition or convergence point.

First identify:
- current strategic execution spine and stage
- what changed since the last gate/convergence point
- any current/recent work packet(s)
- trusted prior evidence and documented invalidation triggers

Then run the gate parts required by the selected variant and current risk. Product/Enterprise stage transitions use all eight parts:
A. Kill Criteria
B. Assumption Decay + Evidence Validity
C. Scope Integrity
D. Skipped Work
E. Blast Radius + Verification Scope
F. Decision Reversals
G. Dependency/KB Health
H. Architecture/Requirements/Work-Packet/Implementation Alignment

Challenge vague answers. Distinguish targeted slice verification from required convergence verification. Do not accept a research/audit/work packet as strategic authority unless the canonical project process adopted it.

Return:
- clear / warning / blocked
- exact blockers/conditions
- evidence that remains reusable
- evidence that was invalidated and must be re-established
- canonical files/decisions that need reconciliation
- whether stage advance is permitted
```

---

# Anti-Patterns

| Anti-Pattern | Why It Fails | Better Behavior |
|---|---|---|
| Filling the log without reading current kill criteria | ceremony replaces risk detection | read actual current authority |
| Saying “no scope change” reflexively | hides drift | compare against requirements/spine |
| Running every test at every gate without blast-radius reasoning | expensive and obscures why evidence matters | identify invalidation, then run targeted + required convergence checks |
| Keeping verification too narrow at release | slice confidence is not release confidence | widen at convergence |
| Treating a work packet as a mini-master-plan | creates authority split | derive it from the spine and replace it |
| Treating newer research as automatically authoritative | recency is not authority | adopt deltas through canonical process |
| Re-entry by rereading/retesting everything | high cost, low signal | risk/invalidation-based revalidation |
| Triggering convergence only because a fixed counter/time elapsed | substitutes arbitrary cadence for risk reasoning | use local reminders as heuristics, but gate on accumulated change/risk |
| Skipping a required gate because of urgency | pushes uncertainty downstream | run the appropriate gate; Lite can be concise |

---

## Operating Principle

**Rigor means knowing what is authoritative, what changed, what evidence is still valid, and what must be proven now. It does not mean maximizing document reads, test reruns, or fixed process counters.**
