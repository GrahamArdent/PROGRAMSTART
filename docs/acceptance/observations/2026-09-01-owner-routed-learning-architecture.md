# PROGRAMSTART Learning Observation — Owner-Routed Learning Architecture

Date: 2026-09-01
Status: meaningful methodology observation
Proposed lesson: `PSL-020`

## What happened

While preparing a new PROGRAMSTART Mission Control greenfield project, the operator explicitly challenged the plan because Mission Control was framed as a PROGRAMSTART learning exercise but not as a learning exercise for `GrahamArdent/programstart-compute-spine`.

Live repository inspection showed that Compute Spine already contains `docs/PROGRAMSTART_LEARNING_LOOP.md`, but that protocol is intentionally about real projects improving PROGRAMSTART methodology. It does not define how Compute Spine, Mission Control, or another learning-capable product/system should itself improve from operational evidence.

The same planning conversation also showed why routing matters: a single future Mission Control integration event could expose a PROGRAMSTART methodology problem, a Compute Spine control-plane defect/capability gap, a Mission Control UX defect, an Execution Node worker limitation, or an external provider limitation. Treating all such observations as PROGRAMSTART lessons would misroute ownership and bloat the methodology ledger.

## Did PROGRAMSTART materially help, hinder, or fail?

Current PROGRAMSTART helped by preserving one-owner/one-authority boundaries and by explicitly classifying product-specific learning as local rather than methodology learning.

The gap is that it did not provide a reusable architecture rule for software that should learn from real operation, nor a reusable owner-routing discipline for those operational lessons.

This was material because the next proposed greenfield system, Mission Control, is expected to exercise Compute Spine directly and would otherwise have required project-specific prompt language to rediscover the distinction.

## Classification

`systemic`

The concern applies beyond Compute Spine or Mission Control. Systems involving routing, recommendations, recovery, repeated human corrections, adaptive policies, operational cost/performance choices, or model/prompt optimization may benefit from learning capability while still requiring deterministic authority and safety boundaries.

## Existing lesson search

The existing PROGRAMSTART Learning Loop (`PSL-013`) covers how real projects teach PROGRAMSTART methodology. It does not own product/system operational learning.

No existing lesson in the current ledger owns the separate concern of conditional learning-capable-system architecture plus owner-routed learning.

## Evidence maturity

`implemented`

A bounded methodology change is being implemented on branch `methodology/owner-routed-learning-architecture`:

- new `docs/PROGRAMSTART_LEARNING_ARCHITECTURE.md`;
- canonical owner/rule wiring;
- file-index routing;
- explicit separation from the PROGRAMSTART Learning Loop.

This is not yet `validated` because no real project has used the new gate end-to-end after merge.

## Why the change is bounded

The change deliberately does **not** add:

- a mandatory `LEARNING_PLAN.md`;
- a universal learning ledger;
- a model-training requirement;
- a second project lifecycle;
- an autonomous self-modification authority;
- permission for learned behavior to broaden credentials, spending, production access, or other authority.

It reuses existing project requirements, architecture, test, decision, execution-spine, Work Packet, and post-launch surfaces by default.

## Intended real retest

Use the next genuine learning-capable project/system interaction, preferably the Mission Control ↔ Compute Spine integration, to prove that:

1. the Learning Architecture Gate activates only where operational learning is materially useful;
2. an observation is correctly routed to PROGRAMSTART, Compute Spine, Mission Control, Execution Node, the current product, or an external limitation according to ownership;
3. the product/system can retain/evaluate a useful learning signal without creating a shadow backlog or methodology-ledger noise;
4. a proposed learned improvement follows evaluation/promotion/rollback rules;
5. no learned success is treated as permission to broaden authority.

If the gate creates repeated ceremony without changing decisions, misroutes ownership, or duplicates existing project authority, narrow or reject the lesson.
