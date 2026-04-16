# Loop Report

Purpose: Critical review of where PROGRAMSTART can and cannot benefit from mutation-loop-style orchestration.
Scope: Design analysis only. No implementation recommendations in this document should be treated as approved work.
Basis: Review of `scripts/programstart_mutation_loop.py`, `scripts/programstart_health_probe.py`, `scripts/programstart_closeout.py`, and the current unified CLI command surface.
Last updated: 2026-04-16

---

## Executive View

PROGRAMSTART can reuse the general loop pattern, but only for work that has all of the following properties:

1. A deterministic cycle definition.
2. Machine-checkable results.
3. Explicit stop conditions.
4. A bounded write surface, or preferably no write surface at all.

The current mutation loop is a good fit because it runs a fixed command sequence, parses a materialized result, records history, and can distinguish between a settled run and an in-progress or invalid one.

That pattern does **not** generalize safely to every part of PROGRAMSTART. The repo is governance-heavy. In many areas, the expensive part is not running commands but deciding what is authoritative. A loop that observes or records can be useful. A loop that starts making authority decisions on its own is much more dangerous.

## Core Test

Before adding any new loop, apply this test:

**Can the loop define success, failure, no-op, and stop conditions without human interpretation?**

If the answer is yes, the area is a candidate for a loop.
If the answer is no, the area should stay interactive.

## Why The Mutation Loop Works

The existing loop in `scripts/programstart_mutation_loop.py` has a structure that is unusually favorable for automation:

- It waits for an exclusive resource: an active mutation run.
- It can run pre-cycle work through a bounded hook.
- It runs canonical gates first: drift and validate.
- It runs one expensive command with a known output shape.
- It records the result only after seeing a materialized summary.
- It treats missing settled output as failure, not success.

This is a strong orchestration pattern because the loop is not deciding what good architecture is. It is repeatedly measuring a narrow technical outcome.

## Candidate Loop Types

### 1. Read-Only Audit Loop

**What it would do**

- Run `programstart health`, `programstart drift`, selected `programstart validate --check ...` commands, and possibly `programstart status` or `programstart guide` snapshots.
- Persist a cycle history and current status summary.
- Classify each cycle into `healthy`, `warnings`, `degraded`, or `critical`.
- Optionally watch one repo or many repos.

**Why it is good**

- `scripts/programstart_health_probe.py` already has a read-only structured report model.
- The outputs are inherently machine-classifiable.
- Read-only assessment is operationally safe.
- It would be useful for catching drift, missing control files, signoff staleness, and validation regressions without changing the repo.
- It aligns well with PROGRAMSTART's governance posture because it produces evidence instead of inventing fixes.

**Why it is bad**

- It can easily become alert spam if run too often with no escalation logic.
- Repeatedly surfacing known warnings without suppression or dedupe reduces signal.
- A read-only audit loop can tell you what is wrong, but not necessarily what should happen next.
- If people start treating the loop's classification as a substitute for human checkpoint review, it will be over-trusted.

**Verdict**

Good candidate, especially as the first non-mutation loop example.

### 2. Evidence / Closeout Loop

**What it would do**

- Periodically run closeout-style evidence capture using drift, authority sync, ADR coherence, and changed-file inspection.
- Write timestamped evidence artifacts only.
- Possibly stop when the repo reaches a clean checkpoint state.

**Why it is good**

- `scripts/programstart_closeout.py` already packages multiple governance checks into a durable artifact.
- The write surface is narrow and derived: evidence files, not authority docs.
- It would create a durable audit trail for repeated checkpoints.
- It is compatible with the repo's current "prove it" style of validation.

**Why it is bad**

- Closeout is not purely mechanical. The ADR result still reflects human intent.
- If automated too aggressively, it risks generating lots of low-value governance artifacts.
- A loop could create the appearance of formal signoff discipline without any real human checkpoint decision.
- It is easy to confuse "produced evidence" with "actually ready."

**Verdict**

Possible, but only if the loop is framed as evidence collection rather than automatic closeout approval.

### 3. Health / Watchdog Loop

**What it would do**

- Repeatedly run `programstart health` and selected dashboard or service smoke checks.
- Detect transitions rather than just absolute failures.
- Record degradation events and recovery events.

**Why it is good**

- Works well for long-lived surfaces like the dashboard, local serving, or multi-repo monitoring.
- Useful when a user wants ambient awareness rather than an on-demand report.
- Machine classification is strong: healthy, warning, degraded, critical.

**Why it is bad**

- Risks duplicating standard monitoring behavior without enough additional value.
- If the loop checks too much on every cycle, it becomes expensive and noisy.
- Health results are only as good as the checks. Weak checks produce false reassurance.

**Verdict**

Good candidate if scoped narrowly to the repo's actual operational surfaces.

### 4. Factory Smoke Loop

**What it would do**

- Repeatedly generate temporary repos from representative shapes.
- Run bootstrap, validation, and smoke checks.
- Record which factory scenarios regress over time.

**Why it is good**

- PROGRAMSTART is a template/orchestration repo, so generated-repo integrity matters.
- Scenario-based repetition is a good fit for loop orchestration.
- Results are measurable: pass, fail, timeout, or degraded.
- This would likely catch template regressions early.

**Why it is bad**

- It is more expensive than audit loops because it creates and validates whole repos.
- Temporary repo generation can consume significant time and disk.
- If the scenario list is weak, the loop gives shallow confidence.
- It is more CI-like than day-to-day governance-like, so it may belong in scheduled quality automation rather than a local background loop.

**Verdict**

Strong candidate, but better treated as regression infrastructure than as an always-on local loop.

### 5. Prompt Evaluation Loop

**What it would do**

- Re-run saved prompt evaluation scenarios.
- Track score drift or output regressions.
- Persist changes in prompt quality over time.

**Why it is good**

- Repetition is natural for evaluation.
- The scope is bounded and test-like.
- It supports comparison over time rather than one-off snapshots.

**Why it is bad**

- Prompt evaluation can be noisier and less stable than mutation or validation data.
- The scoring regime matters a lot; weak metrics produce false confidence.
- This is only useful if the repo has stable, trusted prompt-eval scenarios that truly represent user-facing quality.

**Verdict**

Good candidate if prompt evaluation is already treated as a stable benchmark surface.

### 6. Recommendation Hardening Loop

**What it would do**

- Similar to the current mutation hardening loop: targeted tests, focused gates, canonical measurement, and history.
- Could apply to other deterministic recommendation or scoring subsystems.

**Why it is good**

- Same success profile as the current mutation loop.
- Fits areas with clear exact-output regression surfaces.
- Useful when the problem is "reduce survivor ambiguity" or "increase output determinism."

**Why it is bad**

- This pattern is specialized, not general.
- It only works where exact-output testing is a defensible measure of improvement.
- If extended to fuzzy or high-interpretation surfaces, the loop loses meaning fast.

**Verdict**

Good, but only in tightly bounded technical surfaces.

## Bad Candidates

### 1. Auto-Advance Workflow Loop

**What it would do**

- Repeatedly try to move PROGRAMBUILD or USERJOURNEY forward automatically until validation passes.

**Why it is bad**

- Stage and phase advancement are governance decisions, not just structural transitions.
- Passing validation does not prove readiness to advance.
- It would encourage cargo-cult progression through the workflow.
- A loop cannot reliably infer whether the necessary human thinking happened.

**Verdict**

Bad candidate. Do not automate this as a loop.

### 2. Auto-Repair Drift Loop

**What it would do**

- Detect drift and attempt to rewrite files until drift clears.

**Why it is bad**

- Drift is often a symptom of authority tension, not just a formatting mismatch.
- Auto-repair would risk editing the wrong side of a canonical/dependent relationship.
- It could mask real governance disagreements instead of surfacing them.
- In PROGRAMSTART, that is exactly the class of error the source-of-truth protocol is meant to prevent.

**Verdict**

Bad candidate. Observation is useful; self-healing is unsafe.

### 3. Auto-Closeout / Auto-Signoff Loop

**What it would do**

- Generate signoff or checkpoint artifacts automatically whenever checks pass.

**Why it is bad**

- Signoff is meaningful only if it reflects actual review intent.
- It confuses "mechanically clean" with "decision made."
- It creates audit-looking artifacts that may not represent real governance.

**Verdict**

Bad candidate unless the system is clearly restricted to evidence generation and never claims approval.

### 4. Auto-Architecture / Canonical Doc Loop

**What it would do**

- Continuously update canonical docs or requirements based on observed repo state.

**Why it is bad**

- This inverts the repo's authority model.
- It makes derived behavior rewrite the thing that is supposed to govern it.
- The risk of inventing policy is much higher than the potential efficiency gain.

**Verdict**

Very bad candidate.

## Recommended Safety Model

If PROGRAMSTART ever generalizes loop support, it should separate loop types explicitly:

### Observe

- Read-only.
- Can classify and record.
- Cannot edit repo files.

**Good uses**: audit loop, health loop, signoff-staleness loop.

### Measure And Record

- Can write derived artifacts such as logs, reports, or evidence.
- Cannot edit authority or product files.

**Good uses**: closeout evidence loop, prompt-eval history loop, factory regression history.

### Measure And Apply Bounded Hook

- Can invoke a tightly scoped change hook before measurement.
- Must have clear, narrow edit boundaries.
- Must still run canonical gates after each change.

**Good uses**: mutation hardening, exact-output regression tightening, maybe some temporary-repo smoke repair experiments.

This three-tier model matters because "loop" is not one thing. The difference between an observer and an editor is the difference between useful automation and untrustworthy automation.

## Design Principles For Any Future Loop

1. Canonical command first.
   The loop should call the same command a human would trust, not a private shortcut.

2. Fail closed.
   Missing settled output must be failure, not success.

3. Persist history.
   A loop without durable cycle records becomes opaque fast.

4. Separate in-progress from settled.
   Spinner output, partial JSON, or incomplete logs must never be treated as a final result.

5. Distinguish observation from authority changes.
   The more a loop can change, the more constrained it must be.

6. Encode stop conditions explicitly.
   Retry budgets, severity thresholds, and no-op handling should be first-class.

7. Avoid fake productivity.
   A loop should not create artifacts, warnings, or checkpoint files just to show activity.

## Overall Recommendation

The strongest next example is a **read-only audit loop** built from the existing health, drift, and validation surfaces.

That option is good because:

- the data is already structured,
- the classification model already exists,
- the operational risk is low,
- and it respects PROGRAMSTART's source-of-truth model.

The worst direction is a loop that edits governance or canonical materials on its own.

That option is bad because:

- it confuses observation with decision-making,
- it risks inventing authority,
- and it would undermine the exact discipline PROGRAMSTART is designed to enforce.

The broader conclusion is:

**PROGRAMSTART should reuse the loop pattern selectively, not universally.**

Loops are best where the repo needs repeated measurement, structured evidence, and bounded actions. They are worst where the repo needs judgment about what is canonical.