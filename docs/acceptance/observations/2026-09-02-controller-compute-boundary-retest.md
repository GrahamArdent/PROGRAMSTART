# PROGRAMSTART Acceptance Observation — Controller / Compute Spine Boundary Retest

Date: 2026-09-02
Status: **confirmation / explicit acceptance retest; no new methodology change earned**
Relevant existing lessons: `PSL-006`, `PSL-015`, `PSL-018`
`PSL-020` result: **not a qualifying validation retest**

## Why this observation exists

The operator explicitly asked to use an ecosystem-wide autonomy/architecture review as a PROGRAMSTART test while deciding what information should be promoted, where it belonged, and how to avoid future subsystem overlap.

The discussion identified a plausible future concern: `GrahamArdent/programstart-autonomous-controller` and `GrahamArdent/programstart-compute-spine` might both mature into persistent autonomous controllers.

Live owning-repository inspection showed that this was already concrete rather than hypothetical:

- Autonomous Controller PR #1 implemented restart-safe semantic controller state, finite retries, human-gate resume, idempotency and consequential-resource leases.
- Compute Spine future Stage 4/6/10 authority still described durable orchestration, queue/lease/idempotency/retry semantics and higher-autonomy multi-repository execution.

The test therefore became: **can existing PROGRAMSTART primitives detect, route, challenge, remediate and close a real cross-repository ownership collision without inventing another roadmap, controller, methodology mode or product-wide requirement?**

## What PROGRAMSTART behavior was exercised

1. Re-read live owning authority instead of treating the prior conversation/report as authority.
2. Kept each repository's single strategic spine primary.
3. Modeled the Controller ↔ Compute relationship as a cross-repository authority dependency rather than combining their roadmaps.
4. Routed the incumbent ownership correction to Compute Spine first.
5. Refused to treat green CI as closure when the first reconciliation draft left contradictory Stage 6/10 language in Compute Spine's single strategic spine.
6. Used post-implementation adversarial Challenge to construct a realistic failure sequence: two locally correct systems independently owning semantic queue/retry/lease/reroute state after restart/failure, producing divergent or duplicate continuation.
7. Remediated the actual owning strategic spine rather than only adding a subordinate decision note.
8. Re-ran exact-candidate CI and re-challenged before merging the incumbent correction.
9. Reconciled the dependent Autonomous Controller to the accepted Compute Spine boundary.
10. Challenged the exact Controller kernel for replay/idempotency, same-cause retry, stale/wrong-owner leases, human-gate false progress, duplicated admission/queue/attempt concepts and two-controller divergence.
11. Preserved unproven later integration obligations instead of claiming AC-00 proved them.
12. Refreshed Portfolio Operations only after owning repository truth changed.

## Resulting accepted boundary

Accepted stack:

`PROGRAMSTART + owning-project authority -> Autonomous Controller semantic orchestration -> Compute Spine execution fabric -> bounded workers -> evidence -> Controller/PROGRAMSTART verification/closure`

### Autonomous Controller owns

- durable semantic project/run state;
- Work-Packet sequencing/continuation;
- project-level retry/remediation/rerouting;
- human-gate wait/accepted-evidence resume;
- executor/capability selection;
- consequential shared-resource ownership;
- semantic provenance, closure progression and autonomy metrics.

### Compute Spine owns

- reusable hosting/runtime substrate;
- concrete execution-envelope runtime admission;
- worker federation/assignment;
- attempt/effect identity and duplicate-side-effect protection;
- runtime locks/reservations/capacity/health/transport;
- unchanged attempt-local transient runtime retry;
- worker-side revalidation immediately before mutation;
- runtime evidence and infrastructure recovery/resource accounting.

Layered safety controls may exist at both layers only when their effect scopes differ. Duplicate authority is not permitted.

## Retained evidence

### Compute Spine

- reconciliation PR: `GrahamArdent/programstart-compute-spine#29`
- exact challenged candidate: `a58e9776bfb7ce689e33bcf1ae0484a460d64f71`
- exact-head CI: run `33594638533` — PASS
- accepted merge: `d6b347d6e445489750767e44bc156a64b9160efc`
- the first draft was **not** merged despite green CI because the single strategic spine still retained contradictory Stage 6/10 ownership; remediation changed the strategic spine itself before re-challenge.

### Autonomous Controller

- AC-00 PR: `GrahamArdent/programstart-autonomous-controller#1`
- substantively challenged implementation/architecture candidate: `e0db8dd05fc914a730ac1409de449ddcdd1ad619`
- exact-head CI: run `33594982175` — PASS
- final closure-only candidate: `41a506f7cd3131defa0aeea83209ceb081ea9aa6`
- exact-head CI after closure reconciliation: run `33595229037` — PASS
- final compare from challenged candidate changed only `AUTONOMOUS_CONTROLLER_EXECUTION.md` and `CURRENT_WORK_PACKET.md`; narrow re-challenge found no semantic/kernel/boundary regression.
- accepted merge: `db9fca8623d451411c0e06c068234335c98f1f3d`

### Portfolio Operations

- stale derived state still reported Compute Spine Phase-C Windows acceptance and VPS status round trip as pending after owning authority had advanced.
- derived portfolio/operator/auto-progress surfaces were refreshed only after the owning reconciliations merged.
- accepted refresh: `GrahamArdent/portfolio-operations` PR #14 / merge `a73a39f12ee648a55c2dce59cc14735564bf31f3`.

## Challenge findings that remain future integration obligations

These are not AC-00 failures because the corresponding live capabilities are not activated yet:

1. **Human-gate evidence authenticity:** AC-00's store consumes an already-verified acceptance boolean. AC-05 must prove an adapter independently authenticates/verifies returned evidence before setting that boundary.
2. **End-to-end stale-effect suppression:** Controller semantic fencing is proven locally, but AC-03/AC-06 must prove stale/late side effects are suppressed across Controller consequence ownership plus Compute Spine/runtime/provider conditional operations or serialization.
3. **Worker-path ownership:** a future Controller path that grows independent privileged host/Execution-Node control around Compute Spine invalidates the accepted architecture and requires re-challenge.

## Learning classification

### `PSL-006` — confirmation

Cross-repository dependency reasoning remained task-scoped, preserved independent project spines, and routed correction to the actual owner instead of allowing one repository or Portfolio Operations to grant mutation authority to another.

No maturity change: already `validated`.

### `PSL-015` — strong confirmation

The post-implementation Challenge Gate materially changed the outcome. Green CI on the first Compute Spine reconciliation was insufficient because a realistic two-controller failure sequence still survived in the actual strategic spine. The Challenge forced remediation and exact-candidate re-verification before merge.

No maturity change: already `validated`.

### `PSL-018` — confirmation

Portfolio Operations was demonstrably stale but did not control owning truth. It was refreshed only after current owning-repository evidence was reconciled.

No maturity change: already `validated`.

### `PSL-020` — not yet validated

This exercise used PROGRAMSTART's **methodology learning loop** to route an architectural lesson. It did **not** exercise a learning-capable product/system that observes operational outcomes and changes its own owner-governed behavior through the conditional Learning Architecture Gate.

Therefore do not mark PSL-020 validated from this evidence. Its existing real retest condition remains open.

## Methodology-change decision

**No new PROGRAMSTART mechanism is earned.**

Do not add:

- a new Autonomous Mode / Mode D;
- an `AUTONOMOUS_CONTINUATION.md` subsystem;
- another portfolio/controller roadmap;
- a blanket rule that failures may bypass authority because “there is always a solution.”

Existing one-spine, blocker/safe-lane, cross-repository dependency, exact-evidence, Challenge, portfolio-staleness and Learning Gate semantics were sufficient to discover and safely resolve the issue.

The useful operational phrasing from the discussion — “blockers are routing problems until proven to be gates” — may remain a Controller design heuristic. It does not currently need promotion into new canonical PROGRAMSTART machinery because existing canonical behavior already requires unattended-safe convergence until a genuine gate, unavailable tool boundary, contradictory evidence or truthful packet completion.

## Invalidation / revisit condition

Revisit methodology only if future real Controller/Compute/worker integrations repeatedly expose a missing reusable rule that existing cross-repository authority, safe-lane, Challenge, exact-candidate or Learning Gate semantics cannot express without ad hoc handling.

Examples that could earn reconsideration:

- repeated confusion over semantic vs execution-fabric retry/idempotency/lease scope despite the accepted project boundaries;
- a system stops at implementation/tool failure while a safe authorized alternate executor/environment/provider route exists and current PROGRAMSTART convergence semantics fail to recover it;
- human intervention repeatedly occurs for cases later proven safely automatable under existing authority;
- a genuine learning-capable integration exercises PSL-020 and reveals missing owner-routing/promotion/rollback controls.

Until then, treat this result as **evidence that the existing methodology worked**, not as a reason to add more methodology.
