---
status: accepted
date: 2026-04-17
deciders: [Solo operator]
consulted: []
informed: []
---

# 0018. Workflow Deferral Mechanism

<!-- DEC-015 -->

## Context and Problem Statement

PROGRAMSTART is a template/orchestration tool, not a user-facing product. Its own PROGRAMBUILD and USERJOURNEY workflow states have been in their initial stages for 15–20 days, triggering persistent STALE flags in `programstart status` and `programstart next` output. Advancing the stages to match reality is dishonest — PROGRAMSTART has no "feasibility" or "phase_2" in the product-lifecycle sense. Ignoring the flags normalizes stale state.

## Decision Drivers

- STALE flags must not become persistent noise that operators learn to ignore.
- The state file must honestly represent what is happening — not advance past stages that were never executed in the traditional sense.
- The deferral date must reset the staleness timer so the operator is not repeatedly warned.
- Deferred state must be distinguishable from in-progress or completed state.

## Considered Options

- Option A — Advance both systems to match actual reality
- Option B — Add `--defer` support to `programstart advance` to mark a stage as intentionally paused
- Option C — Create a "template" variant that disables staleness detection for the PROGRAMSTART repo

## Decision Outcome

Chosen option: **Option B**, because it honestly represents the state ("this stage is intentionally paused, not abandoned") and resets the staleness timer without lying about stage completion. The mechanism is generic and useful for any project where a stage is paused for legitimate reasons.

### Deferral mechanism

- `programstart advance --system <s> --defer --notes "reason"` records a `deferred` object on the active step entry:
  ```json
  {
    "deferred": {
      "date": "2026-04-17",
      "reason": "Template repo — stage gates apply to generated repos, not PROGRAMSTART itself"
    }
  }
  ```
- The step status remains `in_progress`. The active stage/phase does not change.
- `_stale_label()` and `staleness_warnings()` treat the deferred date as the latest activity date, resetting the staleness timer.
- Subsequent `advance` (without `--defer`) works normally — it completes the step and moves forward, clearing the deferred field.
- `programstart state show` displays the deferral reason inline.

### Consequences

- Good: STALE flags are resolved without dishonest state advancement.
- Good: The mechanism is reusable for any project where a stage is paused.
- Good: No schema changes needed — `additionalProperties: true` allows the `deferred` field.
- Neutral: Operators must re-defer every 14 days if they want to suppress staleness indefinitely.
