# Idea Ledger

**Status:** optional non-authoritative preservation surface  
**Purpose:** preserve worthwhile ideas, opportunities, rejected concepts, and shelved possibilities without turning them into current scope, priority, sequencing, or execution authority.

Use this file only when a project or planning workspace does not already have an appropriate durable idea/opportunity surface. An existing issue tracker, notes system, product-discovery database, or equivalent may be used instead if it preserves the same semantics.

PROGRAMSTART itself MUST NOT contain the operator's live cross-project idea portfolio. A portfolio-wide instance belongs in the operator's planning workspace or another dedicated portfolio system. Project-specific instances belong with the owning project.

## Core Principle

> **Capture broadly. Promote deliberately. Execute only from authority.**

A captured idea means only:

> This was worth remembering.

It does **not** mean:

- approved;
- prioritized;
- scheduled;
- in scope;
- funded;
- accepted architecture;
- part of the current execution spine.

When capture cost is low and an idea is plausibly useful later, prefer preserving it over relying on chat/session memory.

## Status Vocabulary

Use one status per record:

- **`CAPTURED`** — worth remembering; not yet evaluated enough to imply priority.
- **`CANDIDATE`** — worth deliberate future evaluation or comparison against current evidence.
- **`INVESTIGATING`** — a bounded validation/research step is actively testing the idea.
- **`SHELVED`** — deliberately not current; preserve it for a stated revisit/promotion condition when known.
- **`ACCEPTED`** — accepted for promotion into the owning project's real authority. The record must point to that authority once reconciled; this ledger never becomes the execution spine.
- **`REJECTED`** — deliberately not adopted under current evidence. Preserve the rationale and any evidence that would justify reconsideration.
- **`SUPERSEDED`** — replaced by another idea/decision; link the replacement when known.

Status is descriptive, not priority. Do not infer that `CANDIDATE` outranks `CAPTURED`, or that older records should execute before newer ones.

## Minimal Idea Record

Keep the record as small as the future value warrants.

```text
TITLE:
STATUS: [CAPTURED | CANDIDATE | INVESTIGATING | SHELVED | ACCEPTED | REJECTED | SUPERSEDED]
CAPTURED_AT:
OWNER_OR_CONTEXT:
IDEA:
WHY_INTERESTING:
ORIGIN_OR_EVIDENCE:
RELATED:
PROMOTION_OR_REVISIT_TRIGGER:
DECISION_OR_RATIONALE:
PROMOTED_TO:
LAST_REVIEWED:
```

Only `TITLE`, `STATUS`, `OWNER_OR_CONTEXT`, and `IDEA` are universally useful. Fill the other fields when they materially improve retrieval, future evaluation, deduplication, or safe resumption.

A stable local reference such as `IDEA-<short-name>` MAY be added when cross-referencing helps. IDs are references only, never ranking or roadmap numbers.

## Capture Triggers

Capture an idea when one or more of these is true:

- the operator explicitly says it is interesting, useful, worth remembering, or should be saved;
- it could plausibly affect a current or future project;
- it is a meaningful alternative that may become better if conditions change;
- a rejected option contains reasoning worth avoiding or reusing later;
- research or implementation exposes a future opportunity outside current scope;
- the idea connects multiple existing observations in a way that may become strategically useful;
- losing the idea would likely require reconstructing non-trivial reasoning later.

Do not require full Idea Intake merely to preserve something. Capture first; evaluate later if/when promotion becomes relevant.

## Promotion Rule

When a captured idea becomes a real candidate for action:

1. load only the idea record and the current authority/evidence needed to evaluate it;
2. use `PROGRAMBUILD_IDEA_INTAKE.md` in the correct Mode A/B/C as appropriate;
3. apply adaptive research/decision routing only to material uncertainty;
4. if accepted, reconcile the existing artifact that owns scope, architecture, sequencing, decision, milestone, or acceptance truth;
5. set the idea record to `ACCEPTED` and link `PROMOTED_TO` to the owning authority;
6. execute only from that reconciled authority, never from this ledger.

## Shelved, Rejected, And Superseded Ideas

Do not delete useful reasoning merely because the idea is not current.

For `SHELVED`, preserve the revisit trigger when knowable, for example:

- after provider capability X exists;
- when usage reaches Y;
- after current milestone Z closes;
- if cost/security/latency evidence changes.

For `REJECTED`, preserve the reason and any reconsideration evidence. This prevents repeating the same analysis later.

For `SUPERSEDED`, point to the replacement idea/decision when practical.

## Deduplication And Hygiene

- Prefer one evolving record over several synonymous ideas.
- Link related ideas rather than merging genuinely distinct concepts prematurely.
- Periodic review is optional; do not create a mandatory calendar cadence just because the ledger exists.
- Review records when a related project changes, a stated trigger fires, or a decision naturally needs them.
- Archive only when the storage system requires it; historical idea records may remain useful evidence.
- Never store secrets, credentials, unnecessary private payloads, or sensitive raw data merely to explain an idea.

## Relationship To Other PROGRAMBUILD Artifacts

- **Idea Ledger:** what was worth remembering, including things not currently accepted.
- **Idea Intake:** whether/how an idea should be challenged before promotion.
- **Research Summary:** evidence gathered to retire a material uncertainty.
- **Decision Log / ADR:** material decisions and durable rationale after the decision boundary is reached.
- **Requirements / Architecture / Master execution spine:** accepted project truth and current sequencing.
- **Work Packet:** what is executing now.

The ledger is intentionally upstream/subordinate to all execution authority.