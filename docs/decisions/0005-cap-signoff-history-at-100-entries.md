---
status: accepted
date: 2026-04-11
deciders: [solo operator]
consulted: []
informed: []
---

# 0005. Cap Signoff History at 100 Entries

<!-- DEC-002 -->

## Context and Problem Statement

`save_workflow_signoff()` and `advance_workflow_with_signoff()` in `scripts/programstart_serve.py` append to the `signoff_history` array in STATE.json without any size limit. Over long-running multi-year projects, this array grows unboundedly, bloating the state file and slowing JSON parsing.

## Decision Drivers

- STATE.json must remain fast to read and write for dashboard responsiveness.
- No signoff data is permanently lost — git history preserves all prior state file versions.
- The cap must be generous enough for even multi-year projects.

## Considered Options

- Option A — Cap at 100 entries with FIFO trim and stderr warning (this decision)
- Option B — Archive old entries to a separate file
- Option C — No cap (accept unbounded growth)
- Option D — Warning-only at a threshold, no trim

## Decision Outcome

Chosen option: **Option A (100-entry FIFO cap with warning)**, because 100 entries covers approximately 50 stage transitions with 2 signoffs each — more than sufficient for even multi-year projects. FIFO trim preserves the most recent entries. A stderr warning informs the operator when entries are dropped.

### Consequences

- Good: STATE.json remains bounded in size regardless of project duration.
- Good: Operators are notified via stderr when trimming occurs.
- Bad: Old signoff entries beyond 100 are no longer directly visible in STATE.json.
- Neutral: Git history retains all prior state file versions for forensic needs.

## Confirmation

- `test_signoff_history_capped_at_max` in `tests/test_programstart_serve.py` verifies the 100-entry cap.
- `MAX_SIGNOFF_HISTORY = 100` constant in `scripts/programstart_serve.py`.

## Links

- [DEC-002 in DECISION_LOG.md](../../PROGRAMBUILD/DECISION_LOG.md)
- [PROGRAMBUILD_ADR_TEMPLATE.md](../../PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md)
