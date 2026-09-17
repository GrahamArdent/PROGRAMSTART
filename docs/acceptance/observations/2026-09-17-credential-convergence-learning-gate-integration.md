# PROGRAMSTART Learning Observation — Credential Convergence / Learning-Gate Integration

Status: **subordinate / non-canonical evidence**.

## Observation identity

- **Date:** 2026-09-17
- **Real projects:** `GrahamArdent/home-automation-control` + `GrahamArdent/secrets-control-plane`
- **Methodology owner:** `GrahamArdent/PROGRAMSTART`
- **Existing lesson challenged:** `PSL-013`
- **Classification:** systemic counterevidence / integration refinement
- **Related protocols:** Work Packet, Authority-Gap Reconciliation, Challenge Gate, Learning Loop

## What happened

Home Automation credential recovery exposed a cross-project identity-ownership drift. The accepted Secrets architecture treated Infisical machine identities as scarce trust-boundary resources, but later consumer-specific Home Assistant/Govee work evolved toward per-adapter identity reconciliation. A consumer reconciler could treat sibling/legacy identity state as foreign and the ecosystem reached a credential breakage before the mismatch was widened into a cross-project convergence finding.

The immediate product defect belongs to the Secrets & Identity Control Plane and is now routed there as issue #69. Home Automation records the dependency/resume boundary separately as issue #55.

The methodology question is why an already-validated Learning Gate did not surface the drift earlier.

## Evidence / root cause

Current PROGRAMSTART already contains the needed concepts:

- `docs/PROGRAMSTART_LEARNING_LOOP.md` says Learning Gate evaluation is automatic at meaningful checkpoints, including packet closure, cross-repository dependency acceptance, provider/runtime evidence changes, and PROGRAMSTART-caused friction.
- `docs/PROGRAMSTART_AUTHORITY_GAP_RECONCILIATION.md` says every resolved Authority Gap should ask both immediate ownership and reusable-learning questions.
- `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` explicitly wires adversarial closure review into high-risk implementation closure.

But the canonical `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` lifecycle explicitly required Challenge closure and durable-state reconciliation, then went directly to `Close or hand off`. It did **not** contain an explicit conditional Learning-Gate closure step.

That composition gap made `PSL-013` depend too much on session/prompt discipline. The protocol existed and had been successfully used before, but the dominant execution contract could complete truthfully without calling it.

## Learning decision

This does **not** earn a new learning subsystem, new lifecycle, new agent, or new PSL lesson ID. It is counterevidence that narrows the prior claim that `PSL-013` was fully validated end-to-end.

Smallest earned correction:

1. add a conditional Learning-Gate evaluation step to Work Packet closure after durable-state reconciliation and before close/handoff;
2. define a resolved material Authority Gap as a Learning-Gate checkpoint when it exposed cross-project mismatch, systemic PROGRAMSTART friction/failure, or counterevidence to a prior methodology assumption;
3. retain `no reusable lesson` as a normal result with no mandatory observation/ledger write;
4. keep product completion independent from PROGRAMSTART repository write access.

`PSL-013` therefore returns from `validated` to `implemented` until a natural real packet/Authority-Gap closure proves the integration fires without operator prompting or ceremony.

## Why this prevents recurrence

The fix changes the failure mode from “someone must remember the Learning Loop exists” to “the canonical packet closure path must evaluate whether this checkpoint qualifies.”

It does not guarantee every architecture drift is caught immediately. The actual prevention stack remains:

- owning authority before dependent implementation;
- cross-repository dependency/Authority-Gap routing for shared concerns;
- Challenge Gate for high-risk changed trust surfaces;
- Learning Gate at closure for reusable methodology/system-routing evidence.

The credential-specific architecture correction remains owned by Secrets #69; PROGRAMSTART owns only the missing closure composition.

## Retest

Use the next natural PROGRAMSTART packet closure or resolved material Authority Gap. Success requires:

- Learning Gate evaluation happens without Graham explicitly asking for it;
- the result may legitimately be `no reusable lesson`, local, confirmation, counterevidence, or systemic;
- no redundant artifact is created when no maturity change exists;
- product closure is not blocked by inability to write PROGRAMSTART;
- a systemic finding is routed to its actual owner rather than remaining in chat.
