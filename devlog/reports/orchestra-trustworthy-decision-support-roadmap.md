# Orchestra Agent Trustworthy Decision-Support Roadmap

Purpose: Focused report on how Orchestra Agent could evolve from a broad prompt-driven agent shell into a trustworthy technical decision-support system.
Status: Analysis only. This is not an approved implementation roadmap.
Basis: Direct review of Orchestra Agent runtime behavior and support modules.
Last updated: 2026-04-16

---

## Executive Summary

Orchestra Agent becomes more useful when it does **less pretending to be an autonomous operator** and more to become a disciplined evidence-and-recommendation system.

The current design already has useful ingredients:

- audit logging,
- guardrails,
- hooks,
- session persistence,
- project registry,
- analytics.

What it lacks is a tight trust model.

Right now, the system mixes:

- open-ended reasoning,
- broad action capability,
- recurring automation,
- freeform memory,
- and weak evaluation.

That mixture makes the agent look powerful, but it does not make it trustworthy.

The correct direction is to make decision support the center and to make action paths explicit, typed, reviewable, and secondary.

---

## What Trustworthy Decision Support Actually Requires

For this kind of product, trust does not come from sounding intelligent. It comes from six concrete properties:

1. Clear separation between analysis and action.
2. Evidence-backed recommendations.
3. Stable reusable operations.
4. Explicit memory quality and lifecycle.
5. Measurable recommendation quality.
6. Permission boundaries that match the declared mode.

Orchestra Agent is currently partial on all six.

---

## Core Architectural Shifts

### 1. Make the product identity narrower

The product should explicitly say what it is:

- a system for gathering evidence,
- comparing options,
- and emitting structured recommendations.

It should not treat coding, automation, scheduling, and git mutation as co-equal default behaviors.

Why this matters:

- Narrow products are easier to evaluate.
- Users understand what kind of trust to grant.
- Policy becomes easier to enforce.

### 2. Split analysis from execution

The same orchestration loop should not both decide and act with broad permissions.

Better structure:

- analysis phase: inspect, compare, synthesize,
- proposal phase: emit recommendation with evidence,
- action phase: only after explicit approval or predefined bounded policy.

Why this matters:

- It avoids accidental mutation.
- It makes the recommendation legible before side effects occur.
- It preserves the original value proposition of decision support.

### 3. Replace prompt chains with typed workflows

Prompt chains are easy to create and hard to trust.

Typed workflows should declare:

- purpose,
- allowed tools,
- required context,
- expected output schema,
- stop conditions,
- review points,
- evidence emitted.

Why this matters:

- Named operations become repeatable.
- Results become comparable over time.
- Failures become diagnosable.

### 4. Schedule operations, not prompts

Prompt scheduling is attractive because it is simple, but it is the wrong abstraction for trustworthy recurrence.

Recurring work should run a named operation such as:

- repo health summary,
- decision backlog review,
- stale branch report,
- architecture drift scan.

Why this matters:

- A recurring unit should mean the same thing every time.
- Operational failures should be attributable to a known workflow, not to prompt interpretation drift.

### 5. Upgrade memory into a knowledge system

Memory should not be one large pile of recallable text.

It should distinguish at least:

- verified fact,
- user preference,
- prior decision,
- open question,
- tentative hypothesis,
- expired or superseded item.

Why this matters:

- The system should know what it knows, what it suspects, and what it should no longer trust.
- Decision support degrades quickly when stale context reappears as if it were current truth.

### 6. Measure recommendation quality directly

A decision-support agent should primarily optimize for whether its recommendations were useful and correct.

That means tracking things like:

- recommendation accepted or rejected,
- later outcome,
- confidence calibration,
- revisit trigger,
- scenario replay score,
- user-rated usefulness.

Why this matters:

- Tool counts are a systems metric.
- Recommendation quality is a product metric.

### 7. Build explicit context bundles

Project detection should move beyond stack flavor inference.

The agent should construct context bundles including:

- build and test entry points,
- repo topology,
- deployment surfaces,
- major contracts and boundaries,
- policy files,
- recent changes,
- risk hotspots,
- optional human notes.

Why this matters:

- Better context is one of the few reliable ways to improve recommendation quality without increasing model power.

### 8. Make permissions mode-specific

Modes like planning, architecture, and security should not share the same tool rights.

Example:

- planning mode can read, compare, summarize, and create decision records,
- architecture mode can inspect contracts and diagrams,
- security mode can run only approved scans,
- execution mode must be explicit and separately authorized.

Why this matters:

- Capability boundaries should match the user's intent.
- Mode labels are meaningless if they do not change policy.

---

## Proposed Target Model

The trustworthy version of Orchestra Agent would behave more like this:

1. Build or refresh a project context bundle.
2. Run only the allowed evidence-gathering operations for the chosen mode.
3. Produce a structured recommendation with evidence, options, assumptions, and confidence.
4. Persist that recommendation as a decision record.
5. Optionally request approval for any action-bearing follow-up.
6. Revisit the decision later and record the actual outcome.

This is far less flashy than a broad agent loop, but much more useful over time.

---

## Recommended Roadmap

### Phase 1: Stabilize the trust boundary

- Remove or sharply demote auto-commit behavior.
- Make action-taking opt-in and explicit.
- Add mode-specific tool allowlists.
- Make the recommendation object mandatory and structured.

Goal:

- Stop mixing advice and execution.

### Phase 2: Structure repeated work

- Convert playbooks into typed workflows.
- Convert cron prompts into scheduled named operations.
- Attach evidence schemas to recurring jobs.

Goal:

- Make recurrence stable and inspectable.

### Phase 3: Improve context and memory quality

- Replace shallow detection with explicit context bundles.
- Add verified-memory classes and supersession rules.
- Distinguish current truth from stale recall.

Goal:

- Raise the quality floor of recommendations.

### Phase 4: Add quality feedback loops

- Track whether recommendations were accepted.
- Record eventual outcomes.
- Add scenario replay evaluation.
- Compare confidence against actual later correctness.

Goal:

- Measure the product on what users actually care about.

### Phase 5: Expand carefully

- Only after the above is in place, add stronger multi-project and portfolio views.
- Keep execution features narrow and justified.

Goal:

- Grow without reintroducing ambiguity.

---

## What Orchestra Agent Should Stop Doing

If the goal is trustworthy decision support, the following behaviors should stop being central:

- presenting broad tool access as a virtue by itself,
- treating prompt scheduling as acceptable unattended automation,
- letting chat history stand in for decision memory,
- using generic stack detection as if it were serious project understanding,
- and implying maturity through feature breadth instead of measured reliability.

These are not minor paper cuts. They directly suppress trust.

---

## Why These Choices Are Better

These choices are better because they make the system more honest about what it can and cannot reliably do.

That matters not only for Orchestra Agent itself, but for any program trying to build useful agent support:

- trust rises when evidence is durable,
- trust rises when permissions are narrow,
- trust rises when repeated workflows are typed,
- trust rises when memory is classified,
- trust rises when recommendation quality is measured.

Conversely:

- trust falls when action power is vague,
- trust falls when prompts are scheduled as if they were deterministic jobs,
- trust falls when a system recalls text without knowing whether it is still true.

---

## Broader Transferable Lessons

Programs other than PROGRAMSTART can still benefit from the same design corrections:

- deployment assistants need analysis/action separation,
- review bots need decision records,
- portfolio dashboards need typed recurring operations,
- coding agents need policy outside the prompt,
- advisory systems need verified memory rather than ambient recall.

The lesson is not tied to one repository. It is tied to a category of systems that confuse versatility with trustworthiness.

---

## Bottom Line

To become much more useful for its intended purpose, Orchestra Agent should stop trying to be a broad autonomous shell and become a sharper system for evidence gathering, structured comparison, and explicit recommendation.

That shift is not cosmetic. It is the difference between a tool that feels capable and a tool that becomes dependable.
