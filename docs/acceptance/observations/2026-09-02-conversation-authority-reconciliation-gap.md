# Learning Observation — Conversation-to-Authority Reconciliation Gap

**Date:** 2026-09-02  
**System:** Portfolio Operations / PROGRAMSTART conversation-capture plumbing  
**Classification:** systemic counterevidence / composition gap  
**Related lessons:** `PSL-016`, `PSL-017`, `PSL-018`  
**Status:** subordinate / non-canonical evidence

## Trigger

A live operator review identified a recurring organizational-memory concern: substantive project conversations may produce accepted work, material rationale, dependencies, or future work, but attention can move elsewhere before that meaning reaches the owning project's Master/execution/decision authority or later resurfaces.

This is not merely a conversational impression. Live repository evidence shows:

- Portfolio Operations already has `IDEA_LEDGER.md`, `CONVERSATION_CAPTURE_INBOX.md`, a pre-execution capture checkpoint, and a twice-daily Conversation Capture Sweep;
- the most recent `CONVERSATION_CAPTURE_STATUS.md` on 2026-09-02 reported `COVERAGE: PARTIAL` because ordinary ChatGPT conversation history is not exposed as a deterministic message-by-message stream with a durable cursor;
- the current capture model correctly distinguishes preservation from execution authority, but its receipts and routing semantics do not strongly prove whether a substantive outcome was merely preserved, actually reconciled into owning authority, or armed for later trigger-based resurfacing;
- the live Portfolio Operations `IDEA-conversation-to-durable-capture` revisit condition therefore fired.

The operator explicitly authorized moving this gap forward immediately.

## What happened

The live system had already validated two useful but separate behaviors:

1. `PSL-016`: a generic acceptance of a concrete recommendation can resolve to `reconcile_authority_then_execute` when current authority requires reconciliation;
2. `PSL-017`: worthwhile ideas can be preserved cheaply and non-authoritatively, then later promoted deliberately when a trigger fires.

Real portfolio use exposed a seam between them:

```text
substantive conversation
    -> useful outcome exists
    -> outcome may be preserved
    -> conversation/topic changes
    -> preservation alone does not prove accepted outcome reached owning authority
    -> trigger/relevance may later arise
    -> current system may not prove that the outcome resurfaced or was reconciled
```

The preservation mechanism is therefore not disproven. The counterevidence is that preservation plus current recovery routing is insufficient evidence for end-to-end conversation-to-authority continuity.

## PROGRAMSTART help / hinder / failure analysis

### What helped

Existing PROGRAMSTART primitives prevented a bad fix:

- `PSL-016` already provides deterministic accepted-recommendation resolution and authority reconciliation;
- `PSL-017` already separates preservation from promotion/execution and prevents idea-ledger backlog drift;
- `PSL-018` already keeps Portfolio Operations derived/non-authoritative;
- Mode C already requires reuse of current project authority rather than creating competing plans;
- the Learning Gate prevents immediately inventing a new lifecycle or mandatory artifact.

### What failed or remained ambiguous

The existing primitives are not yet composed strongly enough at the conversation-capture boundary.

Specifically:

- a capture receipt can prove that something was noticed without proving it reached the correct concern owner;
- a preserved record can contain a revisit trigger without a sufficiently explicit end-to-end resurfacing/reconciliation disposition;
- conversation recovery currently emphasizes capture/routing semantics more than `preserved vs reconciled authority vs trigger armed vs ready for review` distinctions;
- a future agent can plausibly mistake `durably captured` for `organizationally resolved` even though the owning project was never reconciled.

## Local vs systemic

**Systemic.** The failure mode is independent of a particular product. Any PROGRAMSTART-managed project whose operator develops direction conversationally can encounter it.

However, the current evidence does **not** earn a new PROGRAMSTART lifecycle, global backlog, transcript artifact, or portfolio state machine.

The likely change, if earned by retest, is a bounded composition/clarification across existing accepted-recommendation, idea-preservation, Mode-C re-entry, and portfolio-attention surfaces.

## Existing lesson deduplication

Do not create a new lesson ID yet.

This observation most directly narrows/strengthens the boundary of:

- `PSL-016` — accepted recommendations must reconcile into authority before execution when required;
- `PSL-017` — preservation is valuable but explicitly non-authoritative;
- `PSL-018` — portfolio routing must converge into owning-project truth and execution rather than treating derived portfolio state as completion.

The new evidence says these primitives may need a stronger explicit composition rule at the conversation-capture/recovery seam.

## Evidence maturity

- `PSL-016`: remains **validated**.
- `PSL-017`: remains **validated for preservation/promotion separation**, but this observation is counterevidence to any broader interpretation that preservation alone solves conversation-to-project continuity.
- `PSL-018`: remains **validated** for portfolio attention/execution convergence.
- Candidate composition improvement: **observe/candidate pending live Portfolio Operations V0.1 retest**.

## Does PROGRAMSTART need to change now?

**Not canonically yet.**

The operator-authorized immediate owner is `GrahamArdent/portfolio-operations`, where `docs/CONVERSATION_TO_AUTHORITY_RECONCILIATION_V0_1.md` defines a bounded live implementation/retest.

Candidate PROGRAMSTART deltas to evaluate after that retest:

1. make the pre-execution conversation checkpoint explicitly distinguish `preserved` from `authority reconciled`;
2. when an operator has clearly accepted a conversation outcome, require a concern-owner reconciliation check before treating the outcome as durably resolved;
3. during Mode-C orientation, surface a specific preserved record when current evidence directly satisfies its declared dependency/revisit trigger;
4. in capture/recovery semantics, distinguish `ALREADY_DURABLE`, `CANDIDATE_PRESERVED`, `RECONCILED_AUTHORITY`, `TRIGGER_ARMED`, and `READY_FOR_REVIEW` without making them lifecycle states or priorities.

Prefer the smallest canonical owner/surface that composes existing rules. Do not add a new lifecycle unless the V0.1 retest proves existing mechanisms cannot express the behavior.

## Live implementation / retest

Portfolio Operations branch/work:

- `docs/CONVERSATION_TO_AUTHORITY_RECONCILIATION_V0_1.md` defines the implementation contract;
- the live Conversation Capture Sweep automation is being upgraded to distinguish preservation, authority reconciliation, trigger arming, and ready-for-review outcomes;
- the original portfolio `IDEA-conversation-to-durable-capture` record is being re-reviewed because its stated revisit condition fired.

## Next real retest condition

Use the next natural substantive project conversation where one of these occurs:

- a clearly accepted project delta would otherwise remain only in chat;
- a non-current candidate has a concrete dependency/revisit trigger that later becomes true;
- a recovery sweep finds a meaningful outcome and must distinguish `already durable` from `preserved but non-authoritative` from `accepted but not reconciled`.

Success requires proving that:

1. the correct owning authority is identified;
2. accepted meaning is reconciled through normal project discipline rather than from the portfolio ledger/inbox;
3. non-current meaning remains non-authoritative;
4. fired triggers surface only the relevant record and do not turn the ledger into a recurring backlog;
5. no unnecessary transcript/private material is persisted.

After the retest, run the Learning Gate again. If the V0.1 composition works and exposes a reusable methodology requirement, make the smallest focused PROGRAMSTART change and mark it `implemented` until another real retest earns validation.

## Safety / authority check

- [x] product/project authority remains outside PROGRAMSTART learning evidence;
- [x] no raw transcript is stored here;
- [x] no secret/private payload is persisted;
- [x] no global backlog or new lifecycle is created;
- [x] live product/system fix is owned by Portfolio Operations first;
- [x] PROGRAMSTART change remains conditional on evidence from the real retest.
