# PROGRAMBUILD_CHALLENGE_GATE.md

# Challenge Gate Protocol

Purpose: Reusable stage-transition checklist that prevents silent drift, scope creep, and assumption rot between stages.
Owner: Stage Owner (or Solo Operator)
Last updated: 2026-03-31
Depends on: PROGRAMBUILD.md (stage order), FEASIBILITY.md (kill criteria), REQUIREMENTS.md (scope baseline), DECISION_LOG.md
Authority: Canonical for stage transition validation

---

## Why This Exists

Stage gates in PROGRAMBUILD check "did you produce the output?" They do not check "is the output still consistent with everything that came before it?" This creates three failure modes:

1. **Kill criteria go stale.** A kill criterion identified at Stage 1 quietly becomes true by Stage 4, and nobody re-checks.
2. **Scope drifts silently.** Requirements appear in Stage 3 that were not in the inputs block, and nobody notices until Stage 7.
3. **Assumptions rot.** A feasibility assumption weakens with new evidence, but the downstream stages treated it as settled.

The Challenge Gate is a five-minute checklist that runs at every stage transition. It catches these failures before they compound.

---

## When To Run

Run this checklist **before starting any new stage.** It is not optional. It is not "when you have time." It is the first thing you do when you sit down to work on the next stage.

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

---

## The Checklist

### Part A — Kill Criteria Re-Check

Re-read the kill criteria from `FEASIBILITY.md`. Answer each one honestly.

| Kill Criterion | Still False? | Evidence | Action If True |
|---|---|---|---|
| (copy from FEASIBILITY.md) | Yes / No / Trending | | |
| | | | |
| | | | |

**If any kill criterion is true or trending true:** Stop. Do not start the next stage. Record the finding in `DECISION_LOG.md` and decide: kill, pause, or reshape.

### Part B — Assumption Decay Check

List the top 3 assumptions from the previous stage outputs. For each one, rate whether evidence has strengthened, weakened, or remained unchanged.

| Assumption | Source Stage | Evidence Direction | Notes |
|---|---|---|---|
| | | ↑ Stronger / → Same / ↓ Weaker | |
| | | | |
| | | | |

**If any assumption has weakened:** Name the blast radius. Does it invalidate only the current stage, or does it cascade to earlier outputs? Record the finding and decide whether to proceed, revisit, or spike.

### Part C — Scope Integrity Check

Compare the current scope against the inputs block and `REQUIREMENTS.md` (if it exists yet).

| Question | Answer |
|---|---|
| Has anything been added to scope since the last stage that was not in the inputs block or REQUIREMENTS.md? | Yes / No — if yes, list it |
| Has anything been removed from scope without being recorded in DECISION_LOG.md? | Yes / No — if yes, list it |
| Has any "out of scope" item quietly moved into scope? | Yes / No — if yes, name it |
| Is the success metric from the inputs block still the same? If it changed, is the change recorded? | Yes / No |

**If scope changed without a decision log entry:** Record it now before proceeding.

### Part D — Skipped Work Check

| Question | Answer |
|---|---|
| Was anything in the previous stage deferred, partially completed, or marked "TODO"? | Yes / No — if yes, list it |
| Is the deferred work tracked somewhere (decision log, checklist, issue tracker)? | Yes / No |
| Does the deferred work block the next stage? | Yes / No |
| Was anything skipped because it was hard or uncomfortable rather than unnecessary? | Yes / No — be honest |

**If deferred work blocks the next stage:** Resolve it before proceeding.

### Part E — Blast Radius Assessment

| Question | Answer |
|---|---|
| If the output of this next stage turns out to be wrong, how many previous outputs must be revised? | |
| Which downstream stages depend on the output of this next stage? | |
| What is the most expensive mistake this stage could make? | |
| How would you detect that mistake before the next gate? | |

### Part F — Decision Reversal Check

Review `DECISION_LOG.md` for any decisions that have been contradicted, overridden, or made obsolete by later work.

| Question | Answer |
|---|---|
| Are there any decisions in DECISION_LOG.md whose rationale no longer holds? | Yes / No — if yes, list them |
| Are there any pairs of decisions that contradict each other? | Yes / No — if yes, name both entries |
| Has any decision been silently abandoned without a formal reversal entry? | Yes / No — if yes, name it |

**How to record a reversal:** Add a new row to `DECISION_LOG.md` with status `REVERSED`. The `Replaces` column must reference the original decision ID. The original row stays in the log with its status changed to `SUPERSEDED`. Both rows must exist — do not delete the original.

**Reversal log format:**

| ID | Date | Decision | Status | Replaces | Rationale |
|---|---|---|---|---|---|
| D-005 | 2026-04-01 | Use Postgres instead of SQLite | ACTIVE | D-002 | Spike at Stage 4 showed SQLite cannot handle concurrent writes at expected load |
| D-002 | 2026-03-15 | Use SQLite for persistence | SUPERSEDED | — | Original decision based on feasibility estimate; superseded by D-005 |

**If any unreconciled contradictions exist:** Resolve them now. Two contradicting active decisions is a system in an undefined state.

### Part G — Dependency And KB Health Check

*Run at Stages 4+ (Architecture onward). Optional at earlier stages.*

Check whether the external dependencies and technology choices recorded in `ARCHITECTURE.md` are still healthy. Use the PROGRAMSTART knowledge base (`config/knowledge-base.json`) and the research delta system (`programstart research --status`) as primary sources.

| Question | Answer |
|---|---|
| Run `programstart research --status`. Are any research tracks overdue? | Yes / No — if yes, list them |
| Run `programstart retrieval "<stack or dependency name>"` to query the KB. Has any dependency been superseded per `supersedes_for_new_work` relationships? | Yes / No — if yes, name it |
| Has any external dependency in ARCHITECTURE.md changed pricing, licensing, or API contract since it was chosen? | Yes / No / Unknown |
| Has any dependency been deprecated, abandoned, or acquired since it was chosen? | Yes / No / Unknown |
| Are there any KB coverage domains marked `seed` or `partial` that are critical to your project? | Yes / No — if yes, name the gap |
| Run `programstart impact "<concern>"` for any new decisions made this stage. Which downstream docs are affected? | List them or n/a |

**If "Unknown" on any dependency question:** That is not an acceptable answer at Stage 7+. Run a quick research check or research delta before proceeding.

**If any dependency is deprecated or superseded:** Record the finding in `DECISION_LOG.md` and decide: migrate, accept the risk, or spike an alternative.

### Part H — Architecture And Requirements Alignment

*Run at Stages 6+ (Test Strategy onward). Required during implementation (Stage 7).*

Check whether the implemented code and design still match the product authority documents.

| Question | Answer |
|---|---|
| Have any `ARCHITECTURE.md` contracts been changed in code without updating the doc? | Yes / No — if yes, list them |
| Have any new contracts, endpoints, or auth rules been added in code without documenting in `ARCHITECTURE.md`? | Yes / No — if yes, list them |
| Does the implemented auth model still match `ARCHITECTURE.md`? | Yes / No / Not yet implemented |
| Are any P0 requirements in `REQUIREMENTS.md` now impossible given the current implementation? | Yes / No — if yes, name them |
| Has any planned `USER_FLOWS.md` flow been silently dropped or changed? | Yes / No — if yes, name it |
| Has `DECISION_LOG.md` been updated for every architecture-level decision made during this stage? | Yes / No — if no, record them now |

**If any contract divergence exists:** Update `ARCHITECTURE.md` first (canonical-before-dependent), then update tests and code to match. Record the change in `DECISION_LOG.md`.

**If any P0 requirement is impossible:** Stop. This is a potential kill criterion. Escalate to `FEASIBILITY.md` and run Part A again.

---

## Recording The Result

After completing all parts, record the outcome in a machine-verifiable form before you advance.

- Preferred: run `programstart advance --system programbuild --gate-result <clear|warning|blocked> --gate-notes "..."`
- Compatible fallback: add one line to the Challenge Gate Log table below, then run `programstart advance --system programbuild`
- If the gate result is `blocked` or `Proceed? = No`, the transition is blocked. Do not advance.

### Challenge Gate Log

| From Stage | To Stage | Date | Kill Criteria OK | Assumptions OK | Scope OK | Skipped Work OK | Decisions OK | Dependencies OK | Architecture OK | Proceed? | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌/n/a | ✅/⚠️/❌/n/a | Yes / No / Conditional | |

Status codes:
- ✅ All clear
- ⚠️ Issues found but manageable — recorded in DECISION_LOG.md
- ❌ Blocking issue — do not proceed
`programstart advance` now treats missing gate evidence and blocking gate results as hard failures unless you explicitly pass `--skip-gate-check`. That bypass is for exceptional recovery only and MUST be accompanied by a `DECISION_LOG.md` entry explaining why the machine gate was bypassed.

If the gate result is **Proceed: Yes** or **Proceed: Conditional** with manageable findings recorded, run:

```bash
programstart advance --system programbuild --gate-result clear
```

This moves the workflow state to the next stage and stores structured gate evidence in `PROGRAMBUILD_STATE.json` so `programstart status`, `programstart log`, and `programstart drift` all reflect the same transition record. Without this step, the drift check compares changed files against a stale active stage.
---

## Variant Adjustments

| Variant | Gate Rigor |
|---|---|
| Lite | Complete Parts A, C, and F minimum. Others optional but recommended. Part G optional at all stages. Part H optional. |
| Product | Complete all eight parts. Record the log entry. Part G required at Stages 4+. Part H required at Stages 6+. |
| Enterprise | Complete all eight parts. Log entry required. Approver sign-off required. Evidence retained. Part G required at all stages. Part H required at Stages 6+. |

---

## Re-Entry Protocol

When a project resumes after a significant pause, prior stage outputs may have decayed: market conditions shifted, dependencies updated, team members changed, or assumptions expired.

### When To Run

Run this protocol instead of (not in addition to) the normal Challenge Gate when **any** of these conditions are true:

| Condition | Threshold |
|---|---|
| Calendar time since last stage output was produced or reviewed | > 4 weeks |
| Team membership changed (people joined or left) | Any change |
| A dependency in ARCHITECTURE.md had a major version release | Any |
| A KB research track covering your stack was updated with a `changed` outcome | Any |
| An external event invalidates a feasibility assumption (competitor launch, regulation change, vendor acquisition) | Any |

### Re-Entry Steps

1. **Identify the last completed stage.** Read the Challenge Gate Log to find the most recent entry.
2. **Fast-scan all prior stage outputs from Stage 0 forward.** For each completed stage output, answer:
   - Is this still true? (Check facts, not just format.)
   - Has anything external changed that invalidates this?
   - Are the dependencies and tools referenced here still current? (Use `programstart research --status` and check the KB.)
3. **Run a full Challenge Gate (all 8 parts) for the transition into the next stage.** This replaces the normal gate — it does not add to it.
4. **Record a Re-Entry row in the Challenge Gate Log** with the note: `RE-ENTRY after [N] weeks — prior stages re-validated`. Then run `programstart advance --system programbuild` to re-sync workflow state to the correct stage.
5. **If any prior stage output is stale:** Update that output before proceeding. Record the update in `DECISION_LOG.md`.
6. **If a kill criterion became true during the pause:** Stop. Record the finding. Do not resume.

### Re-Entry Prompt Template

```text
Act as a critical reviewer. This project is resuming after a pause of [N] weeks.

Run the Re-Entry Protocol from PROGRAMBUILD_CHALLENGE_GATE.md.

1. Fast-scan each completed stage output (Stage 0 through Stage [last completed]).
   For each one, state: still valid / stale / invalidated — with evidence.
2. Check ARCHITECTURE.md dependencies against the KB (config/knowledge-base.json).
   Flag any that have been superseded, deprecated, or had breaking changes.
3. Run `programstart research --status` and report any overdue research tracks.
4. Re-read FEASIBILITY.md kill criteria. Any now true?
5. Run the full 8-part Challenge Gate for the next stage transition.
6. Produce the Re-Entry log entry.
7. Recommend: resume, resume with updates, or stop.
```

---

## Prompt Template

Use this prompt when running the Challenge Gate with an AI agent:

```text
Act as a critical reviewer. Run the Challenge Gate Protocol from PROGRAMBUILD_CHALLENGE_GATE.md.

Context:
- We are transitioning from Stage [N] to Stage [N+1].
- The previous stage output is: [name the file].
- Kill criteria are in FEASIBILITY.md.
- The inputs block and scope are in PROGRAMBUILD.md and REQUIREMENTS.md.
- The decision log is in DECISION_LOG.md.

For each of the 8 parts (Kill Criteria, Assumption Decay, Scope Integrity, Skipped Work, Blast Radius, Decision Reversals, Dependency Health, Architecture Alignment):
1. Ask the questions.
2. Challenge vague or dismissive answers.
3. If a red flag appears, name it explicitly and recommend an action.
4. Do not let "it's probably fine" pass as an answer.
5. For Part G, use the KB (config/knowledge-base.json) and `programstart research --status` as primary sources.

After all 8 parts:
- Produce the one-line log entry.
- State clearly: proceed, proceed with conditions, or stop.
- If stopping, explain exactly what must be resolved first.
```

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | What To Do Instead |
|---|---|---|
| Filling the gate log without reading kill criteria | You are recording ceremony, not catching risk | Re-read the actual kill criteria text every time |
| Answering "No" to every scope change question reflexively | Scope always changes; pretending it didn't hides drift | Answer honestly, then record the change |
| Skipping the gate "because we're in a hurry" | The gate takes 5 minutes. The rework from skipping takes days | Run it. It is faster than fixing the downstream damage. |
| Running the gate but not recording findings | Unrecorded findings are forgotten findings | Write the log entry. It is one row. |
| Treating ⚠️ as ✅ | A warning that is never resolved is a failure in slow motion | Resolve or explicitly accept the risk in DECISION_LOG.md |
| Silently overriding a decision without a reversal entry | Two contradicting active decisions is an undefined state | Add a REVERSED entry and mark the original SUPERSEDED |
| Skipping Part G because "our stack hasn't changed" | Dependencies change around you, not because of you | Check the KB and research status. It takes 2 minutes. |
| Resuming a paused project without running the Re-Entry Protocol | Every week of pause is a week of assumption decay | Run the Re-Entry scan. Stale outputs cause expensive rework. |

---
