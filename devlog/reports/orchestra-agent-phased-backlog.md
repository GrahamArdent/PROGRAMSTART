# Orchestra Agent Phased Backlog

Purpose: Convert the trustworthy-decision-support roadmap into an implementation-shaped backlog that can be used in Orchestra Agent or any similar decision-support agent project.
Status: Planning backlog only. This is not an approved execution plan.
Basis: Derived from `devlog/reports/orchestra-trustworthy-decision-support-roadmap.md` and the broader Orchestra review set.
Last updated: 2026-04-16

---

## Executive Summary

This backlog turns the roadmap into ordered work that improves trust first and breadth later.

The sequence is deliberate:

1. tighten the trust boundary,
2. stabilize repeated workflows,
3. improve context and memory quality,
4. measure recommendation quality,
5. only then expand portfolio and operator features.

If the order is reversed, the system will gain more surface area before it gains the discipline needed to trust that surface area.

---

## Phase 1: Separate Analysis From Action

### Goal

Stop treating broad action-taking as a normal extension of advice generation.

### Work items

- Add an explicit analysis-to-action handoff state.
- Remove auto-commit as a default or first-class path.
- Add mode-specific tool allowlists.
- Require structured recommendation output before any action-bearing follow-up.
- Mark write, shell, scheduling, and delegation tools as approval-gated when running in decision-support modes.

### Deliverables

- capability policy by mode,
- structured recommendation schema,
- explicit approval gate for action paths,
- downgraded or removed auto-commit path.

### Exit criteria

- decision-support mode cannot mutate a repo without explicit approval,
- recommendations are persisted in a structured format,
- mode labels correspond to real permission differences.

### Why this phase is first

This phase raises the trust floor fastest. Without it, later improvements to memory, workflows, or analytics still sit on top of an ambiguous action model.

---

## Phase 2: Replace Prompt Recurrence With Typed Operations

### Goal

Make repeated work stable, inspectable, and comparable over time.

### Work items

- Convert playbooks from prompt chains into typed workflows.
- Replace cron prompt scheduling with scheduling of named operations.
- Define workflow metadata for purpose, required context, allowed tools, expected output, stop conditions, and evidence emitted.
- Add workflow-level run records so recurring jobs can be reviewed as operations rather than chat transcripts.

### Deliverables

- typed workflow format,
- named operation scheduler,
- evidence schema for recurring jobs,
- workflow run history model.

### Exit criteria

- recurring jobs are defined as named operations,
- the same scheduled task means the same thing each run,
- failures can be traced to workflow steps rather than prompt interpretation drift.

### Why this phase is second

Once action is bounded, the next problem is recurrence. Prompt scheduling is too unstable to serve as trustworthy automation.

---

## Phase 3: Upgrade Context And Memory Quality

### Goal

Raise the recommendation quality floor by improving what the system knows and how confidently it knows it.

### Work items

- Replace shallow project detection with explicit project context bundles.
- Add memory classes for verified facts, preferences, prior decisions, tentative notes, and expired items.
- Add supersession and freshness rules for memories.
- Distinguish current project facts from user-entered freeform notes.
- Ensure recommendations cite which context bundle and memory classes were used.

### Deliverables

- project context bundle model,
- classified memory model,
- freshness and supersession rules,
- recommendation trace showing evidence sources.

### Exit criteria

- recommendations can point to a concrete context bundle,
- stale notes are not surfaced as if they were current verified truth,
- memory recall is visibly categorized by trust level.

### Why this phase is third

Better workflows still produce weak decisions if the underlying context model is shallow or stale.

---

## Phase 4: Measure Recommendation Quality Directly

### Goal

Evaluate the product on decision usefulness rather than activity volume.

### Work items

- Add accepted or rejected status to recommendations.
- Record eventual outcomes for major decisions.
- Add confidence capture and later calibration review.
- Create scenario replay evaluations for representative decision tasks.
- Distinguish infrastructure telemetry from recommendation-quality telemetry.

### Deliverables

- decision outcome tracking,
- confidence calibration dataset,
- scenario replay suite,
- product-quality metrics separate from tool metrics.

### Exit criteria

- the system can show whether recommendations were useful,
- confidence can be compared against later correctness,
- product evaluation is not limited to tool counts and durations.

### Why this phase is fourth

Only after actions, workflows, and context are disciplined does recommendation evaluation become meaningfully diagnostic rather than noisy.

---

## Phase 5: Expand Portfolio-Scale Capabilities Carefully

### Goal

Add broader multi-project features without collapsing back into an ambiguous general-purpose agent shell.

### Work items

- strengthen the multi-project registry with richer repo health semantics,
- add portfolio dashboards tied to named operations and decision records,
- support cross-repo review or triage views that remain read-mostly by default,
- add role-specific or mode-specific portfolio views rather than one broad omnipotent surface.

### Deliverables

- richer project registry,
- portfolio operations dashboard,
- read-mostly cross-repo triage flows,
- narrowed portfolio action policies.

### Exit criteria

- multi-project views improve operator attention routing without expanding default mutation power,
- portfolio features remain compatible with the earlier trust boundary and typed workflow model.

### Why this phase is last

Portfolio scope multiplies ambiguity. It should come only after the single-project trust model is stable.

---

## Cross-Cutting Backlog Rules

The backlog should be executed under four rules:

1. No new high-permission feature without an explicit policy boundary.
2. No recurring automation defined only as a prompt.
3. No memory surfaced without a trust class and freshness expectation.
4. No product-quality claim based only on infrastructure telemetry.

These rules prevent the backlog from recreating the same architectural problems it is meant to fix.

---

## Fastest High-Value Slice

If only one small slice is funded first, it should be:

- explicit approval gate,
- mode-specific tool allowlists,
- structured recommendation schema,
- removal or demotion of auto-commit.

That slice does not make the system fully trustworthy, but it does remove the most obvious mismatch between decision support and autonomous action.

---

## Risks If The Backlog Is Ignored

- feature breadth will continue to outpace trustworthiness,
- recurring automation will remain prompt-fragile,
- memory will continue to mix stale notes with important facts,
- operator confidence will rest on polish rather than measured reliability.

These are strategic risks, not just code-quality issues.

---

## Bottom Line

The right implementation sequence for Orchestra Agent is not “add more tools.” It is “add more trust structure.”

That means the backlog should harden boundaries, type repeated work, improve context quality, measure recommendation quality, and only then expand scope.
