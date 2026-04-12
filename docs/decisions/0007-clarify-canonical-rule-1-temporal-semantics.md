---
status: accepted
date: 2026-04-12
deciders: [solo operator]
consulted: []
informed: []
---

# 0007. Clarify CANONICAL Rule 1 Temporal Semantics

## Context and Problem Statement

`PROGRAMBUILD_CANONICAL.md` rule 1 stated: "Validated code and validated tests MUST outrank any planning document." Meanwhile, `copilot-instructions.md` states: "Do not ship code that contradicts an authority doc." These two statements create apparent tension without temporal qualification — rule 1 could be read as license to skip doc updates entirely.

## Decision Drivers

- Rule 1 is the escape hatch when code has already diverged from stale docs; removing it would be harmful.
- The prospective duty to update docs before introducing contradictory code is equally important.
- Both rules serve different temporal contexts: retroactive conflict resolution vs. prospective planning discipline.
- Without clarification, developers could reasonably interpret rule 1 in either direction.

## Considered Options

- Option A — Add temporal clarification to rule 1 (this decision)
- Option B — Remove rule 1 entirely
- Option C — Add clarification only to `source-of-truth.instructions.md`, leave CANONICAL ambiguous

## Decision Outcome

Chosen option: **Option A (temporal clarification in rule 1)**, because it makes both the retroactive and prospective rules explicit and coherent. The CANONICAL file itself should not be ambiguous about its most important rule.

### Consequences

- Good: Rule 1 is now precise — "MUST outrank" applies retroactively when conflicts are discovered.
- Good: The prospective duty ("MUST update the authority document before introducing contradictory code") is now stated in rule 1 itself, not only in other files.
- Good: Cross-references to `copilot-instructions.md` and `source-of-truth.instructions.md` close the interpretation gap.
- Bad: Rule 1 is now longer and more nuanced than the original one-liner.
- Neutral: `source-of-truth.instructions.md` also gained a "Temporal Semantics" section to match.

## Confirmation

- `PROGRAMBUILD_CANONICAL.md` rule 1 contains "when conflicts are discovered retroactively" and cross-references.
- `source-of-truth.instructions.md` has a "Temporal semantics" section defining retroactive vs. prospective.
- `programstart drift` passes after the change.

## Links

- [DEC-004 in DECISION_LOG.md](../../PROGRAMBUILD/DECISION_LOG.md)
- [PROGRAMBUILD_ADR_TEMPLATE.md](../../PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md)
