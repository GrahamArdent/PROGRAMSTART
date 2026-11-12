---
status: accepted
date: 2026-11-12
deciders: [solo operator]
consulted: []
informed: []
---

# 0027. Separate Observed Behavior from Permission

<!-- DEC-024 -->

## Context and Problem Statement

CANONICAL rule 1 and conflict resolution rank validated code and tests above planning documents for retroactive conflicts. That factual precedence can be misread as permission to retain unauthorized behavior merely because it works.

## Decision Drivers

- Preserve DEC-004 / ADR-0007 retroactive evidence and prospective authority updates.
- Keep current operator, owner, provider and platform restrictions controlling.
- Clarify the canonical owner and its existing dependent instructions together.

## Considered Options

- Clarify CANONICAL rule 1, conflict resolution and existing dependent instructions.
- Remove factual implementation precedence, losing useful evidence of descriptive drift.
- Change only client instructions, leaving the canonical rule ambiguous.

## Decision Outcome

Choose canonical clarification. Validated implementation resolves descriptive claims about what happened; it cannot grant permission, scope or privilege. Unauthorized working behavior remains a defect. Prospective authorized behavior that contradicts authority still requires the authority update first.

This clarifies DEC-004 / ADR-0007 without reversing their temporal semantics. No executable admission, schema, provider restriction or installed enforcement changes. Documentation is guidance; actual action consumers retain enforcement and acceptance.

### Consequences

- An API accepting a deployment without required owner admission is an authorization defect even when a test passes.
- Descriptive drift can still be corrected using validated implementation evidence.
- No universal approval, review or test gate is introduced.

## Confirmation

- Read the complete CANONICAL rule 1 and conflict-resolution example with the operating model and client temporal wording.
- Check the unauthorized-but-working deployment remains a defect while authorized descriptive reconciliation remains allowed.
- Run repository validation, drift and required publication gates; their actual results are execution evidence, not implied by this record.

## Links

- [DEC-024](../../PROGRAMBUILD/DECISION_LOG.md)
- [ADR-0007](0007-clarify-canonical-rule-1-temporal-semantics.md)
- [Canonical authority](../../PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md)
