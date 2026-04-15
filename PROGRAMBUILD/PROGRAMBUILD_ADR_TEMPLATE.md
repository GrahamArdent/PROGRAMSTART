# PROGRAMBUILD_ADR_TEMPLATE.md

# Program Build ADR Template (MADR 4.0)

Use this template when a project needs durable architecture or policy decision records beyond the running `DECISION_LOG.md`.
This template follows the [MADR (Markdown Architectural Decision Records) 4.0](https://adr.github.io/madr/) format.

## Status vocabulary

| Status | Meaning |
|---|---|
| `proposed` | Under discussion; not yet binding |
| `accepted` | Approved and in effect |
| `superseded by ADR-NNN` | Replaced — link to the superseding record |
| `deprecated` | No longer relevant but kept for history |
| `rejected` | Considered and not adopted |

## Naming convention

- File: `docs/decisions/NNNN-short-hyphenated-title.md` (zero-padded to 4 digits)
- ADRs are append-only. When a decision changes, create a new ADR and update the old one's status to `superseded by ADR-NNNN`.
- Every ADR MUST link back to the related `DEC-xxx` row in `PROGRAMBUILD/DECISION_LOG.md`.
- When an ADR is superseded, update the ADR file status, `docs/decisions/README.md`, and any stale `PROGRAMBUILD/DECISION_LOG.md` row that still points at the superseded ADR in the same change.

## When to write an ADR

Write an ADR when at least 2 of the following are true:
- The decision changes a core contract, auth rule, data policy, deployment model, or vendor dependency.
- The decision affects 3 or more files or more than 1 stage of delivery.
- Undoing the decision would likely cost more than 1 focused workday.
- The reason will probably need to be understood again later, and a short `DECISION_LOG.md` entry would be too thin.

For routine decisions, use `DECISION_LOG.md`.

---

## Template

```markdown
---
status: proposed | accepted | superseded by ADR-NNNN | deprecated | rejected
date: YYYY-MM-DD
deciders: [list of people or roles]
consulted: [list of people or roles]
informed: [list of people or roles]
---

# NNNN. Title

## Context and Problem Statement

What problem, constraint, or opportunity forced this decision?
Describe the context in 2–4 sentences.

## Decision Drivers

- driver 1
- driver 2

## Considered Options

- Option A — brief description
- Option B — brief description
- Option C — brief description

## Decision Outcome

Chosen option: **Option X**, because [justification].

### Consequences

- Good: …
- Bad: …
- Neutral: …

## Pros and Cons of the Options

### Option A

- Good, because …
- Bad, because …

### Option B

- Good, because …
- Bad, because …

## Confirmation

How will you verify this decision is implemented correctly?
(e.g., "Pre-commit schema validation catches deviations.")

## Links

- <!-- DEC-xxx -->
- [Related ADR](NNNN-related-title.md)
- [Decision log](../../PROGRAMBUILD/DECISION_LOG.md)
- [External reference](https://example.com)
```

---

Last updated: 2026-03-31
