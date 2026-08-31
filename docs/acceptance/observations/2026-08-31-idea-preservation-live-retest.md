# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, sequencing, portfolio priority, or project execution.

## Observation identity

- **Date:** 2026-08-31
- **Surface:** Dependency Intelligence / Portfolio Operations conversation-to-repository capture audit
- **Methodology repository:** `GrahamArdent/PROGRAMSTART`
- **Existing lesson retested:** `PSL-017`
- **Classification:** confirmation / real promotion-retrieval retest

## Trigger

A substantive Dependency Intelligence discussion produced a useful recommendation that was not yet current work:

> reuse the existing Auto-progress Portfolio automation as the independent verifier/resumption lane for `unreviewed` Dependency Intelligence candidates, while External Dependency Watch remains the detector.

Before the idea was promoted, the conversation moved to a broader concern: worthwhile reasoning should not remain only in chat. The recommendation was therefore captured as `IDEA-dependency-intelligence-verification-lane` in the new external Portfolio Operations `IDEA_LEDGER.md` with status `CANDIDATE` and explicit revisit conditions.

The idea was **not** executed merely because it was recorded.

During the subsequent conversation-to-repository audit, one of its declared revisit conditions became true: Dependency Intelligence authority was being reconciled. The record was retrieved just in time, evaluated against live Dependency Intelligence / PROGRAMSTART / automation boundaries, deliberately accepted, and promoted into the actual owning surfaces.

## Real retest sequence

The natural sequence was:

```text
worthwhile non-current conversation idea
        -> cheap durable Portfolio Operations Idea Record (CANDIDATE)
        -> conversation moves on without losing the idea
        -> declared revisit trigger fires
        -> retrieve the specific record, not the whole ledger
        -> evaluate against current authority/evidence
        -> reconcile Dependency Intelligence authority + decision log
        -> update existing Auto-progress Portfolio automation
        -> mark Idea Record ACCEPTED with PROMOTED_TO pointers
        -> execution derives from owning authority/automation contract, not the ledger
```

Concrete promoted owners:

- `GrahamArdent/dependency-intelligence/docs/DEPENDENCY_INTELLIGENCE_V0_1_EXECUTION.md`;
- `GrahamArdent/dependency-intelligence/DECISION_LOG.md` (DI-010 through DI-012);
- existing ChatGPT `Auto-progress portfolio` automation.

The external Portfolio Operations Idea Record was then changed from `CANDIDATE` to `ACCEPTED` and retained only as provenance/reference evidence.

## Why this validates PSL-017

The original PSL-017 retest required a natural idea that was worth preserving but not current work to be:

1. captured durably without becoming priority;
2. later retrieved/revisited when relevant;
3. promoted/rejected/shelved under current authority rather than by capture status;
4. prevented from silently resequencing active authority.

This event satisfies all four conditions.

The record survived a topic transition that otherwise could have stranded the recommendation in chat. Retrieval was trigger-based rather than a standing scan. Promotion required an explicit authority reconciliation. The Idea Ledger remained non-authoritative throughout.

## Additional adoption evidence

The same audit also found the practical destination gap anticipated by PSL-017's original implementation:

- PROGRAMSTART already contained the correct reusable semantics and orchestration checks;
- the live operator Portfolio Operations workspace initially had no cross-project idea-preservation surface;
- adding that external surface solved adoption without putting live portfolio state into PROGRAMSTART;
- a separate compact `CONVERSATION_CAPTURE_INBOX.md` was added for worthwhile ownerless conversation outcomes, allowing later routing to an existing project, cross-project ledger, Dependency Intelligence, PROGRAMSTART learning, or a newly recommended repository only when justified;
- the inbox and idea ledger are explicitly not recurring backlogs and are retrieved just in time.

This is supporting adoption evidence, not a new methodology mechanism. The existing rule was sufficient once the correct live destination existed.

## Counterexample check

The retest did **not** exhibit the failure modes PSL-017 was designed to prevent:

- capture did not imply priority;
- capture did not create project scope;
- the ledger did not become an execution spine;
- the automation did not scan every idea as a task queue;
- no new scheduler was created solely because an idea existed;
- project authority remained independent;
- no chat transcript was copied wholesale;
- no secrets/private payloads were persisted.

## Learning decision

**PSL-017: advance from `implemented` to `validated`.**

No additional PROGRAMSTART methodology change is warranted from this retest. Continue normal use and record counterevidence if future capture produces backlog drift, noisy over-capture, missed retrieval, authority leakage, or expensive routing ambiguity.

## Safety / authority check

- [x] live idea state remains outside PROGRAMSTART;
- [x] project-specific authority remains with owning repositories;
- [x] cross-project capture remained non-authoritative;
- [x] retrieval was trigger-based rather than portfolio-wide scanning;
- [x] promotion reconciled the owning authority before dependent execution;
- [x] no new methodology feature was manufactured merely because PROGRAMSTART was involved.
