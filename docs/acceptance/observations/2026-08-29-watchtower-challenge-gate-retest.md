# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-08-29
- **Project / repository:** `GrahamArdent/repo-watchtower`
- **PROGRAMSTART lesson ID:** `PSL-015`
- **Checkpoint / acceptance surface:** Watchtower V0.2 Slice 2 / PR #2 post-implementation adversarial closure
- **Classification:** confirmation / validation retest

## What happened

Watchtower V0.2 Slice 2 implemented durable PostgreSQL persistence with transactional delivery handling, incident deduplication, evidence persistence, retry/idempotency behavior, and real PostgreSQL CI coverage. The completed implementation initially reached green CI with 19 tests.

Because the actual changed surface materially affected persistence, idempotency, concurrency, retry, and trust-boundary invariants, the PROGRAMSTART post-implementation adversarial Challenge Gate activated before closure. The review inspected the completed implementation rather than relying only on intended design and existing green tests.

A realistic failure sequence exposed a material false-success/provenance defect: duplicate handling trusted `(provider, delivery_id)` alone even though the durable receipt also retained event identity and the original body hash. A different valid signed body reusing the same delivery ID could therefore have been acknowledged as an ordinary duplicate.

The implementation was corrected to compare committed event identity plus exact-body SHA-256 and return `409` on mismatch. The adversarial pass also added a real concurrency proof that a waiting contender can process successfully when the first claimant rolls back. Final CI passed with 22 behavior tests, and the completed implementation was challenged again before merge.

## Evidence

- Watchtower PR #2: `feat: add durable transactional Watchtower persistence`.
- Merged head: `58c9622b8fb78af052de4153d1b907e2e4d9e002`; merge commit `fbab6da25851456f8b55a1c6f3e8ae567c87276d`.
- PR evidence states the pre-challenge implementation was green with 19 tests and the post-correction suite reached 22 passing tests.
- Final CI run recorded by the PR: `33229389299` with PostgreSQL 16 + TypeScript + 22 behavior tests.
- The PR explicitly records the Challenge Gate result as `CLEAR for Slice 2 scope` after correction and re-challenge.
- Follow-up PR #3 later corrected a separate stable-repository-identity defect and passed its own adversarial review; this strengthens confidence in the methodology but is not required to validate the original PSL-015 retest condition.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** automatically activated a post-implementation adversarial review because the completed change affected high-risk persistence/idempotency/concurrency surfaces.
- **What helped:** the review assumed existing green tests might still miss a defect and required a concrete failure-sequence attempt against a material invariant.
- **What changed the product outcome:** the Challenge Gate found a defect that the existing green suite had missed, forced a behavioral correction, and added targeted regression evidence before merge-ready closure.
- **Was ceremony proportional?** yes. The challenge stayed focused on the actual high-risk invariants and did not introduce a generic objection checklist or a new lifecycle stage.

## Learning decision

- **Existing lesson match:** `PSL-015`.
- **Maturity before:** implemented.
- **Maturity after:** validated.
- **Why:** this is the exact real-project retest PSL-015 required: a later material high-risk implementation reached closure, the actual changed surface triggered the adversarial gate, the gate constructed a realistic failure sequence, found and corrected a defect that current green tests missed, and retained targeted regression proof without burdening unrelated low-risk work.
- **PROGRAMSTART methodology change required now:** none. The existing post-implementation Challenge Gate behaved as intended.

## Retest / continued observation

No further retest is required to establish baseline validation. Future high-risk closures should continue to exercise the gate opportunistically. Counterevidence should be recorded if the gate later becomes overly broad, fails to activate on a material risk surface, or repeatedly adds ceremony without improving correctness.

## Safety / authority check

- [x] Watchtower product authority remains owned by Watchtower.
- [x] No project backlog or portfolio execution spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match the merged PR/CI record.
- [x] No new PROGRAMSTART methodology feature is proposed from this validation.
