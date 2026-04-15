---
status: accepted
date: 2026-04-14
deciders: [Solo operator]
consulted: []
informed: []
---

# 0010. Unified CLI aliases for knowledge-base and state recovery workflows

<!-- DEC-007 -->

## Context and Problem Statement

PROGRAMSTART already had retrieval subcommands in `programstart_retrieval.py` and state snapshot/diff support in `programstart_workflow_state.py`, but the unified `programstart` CLI did not expose equivalent first-class operator commands. This left the documented primary entry point incomplete and forced operators to remember lower-level script surfaces for common retrieval and state-comparison tasks. The repository also lacked a rollback path for workflow state despite having snapshot infrastructure.

## Decision Drivers

- The unified `programstart` CLI is the primary operator entry point and should expose routine retrieval and workflow-state operations.
- Workflow-state restore is destructive enough to require an explicit safety guard.
- Existing retrieval and snapshot logic should be reused rather than duplicated.

## Considered Options

- Option A — Keep retrieval and snapshot comparison only in script-specific CLIs.
- Option B — Add unified CLI aliases for retrieval and diff, plus a confirmed rollback command backed by saved snapshots.
- Option C — Add an interactive rollback flow instead of a flag-driven one.

## Decision Outcome

Chosen option: **Option B**, because it completes the unified command surface while preserving automation-friendly behavior and reusing existing module logic.

### Consequences

- Good: Operators can use `programstart kb search` and `programstart kb ask` without dropping to a separate retrieval entry point.
- Good: Operators can use `programstart diff` as a top-level alias over workflow snapshot comparison.
- Good: `programstart state rollback` restores from a saved snapshot only when `--confirm` is supplied and creates a pre-rollback backup first.
- Neutral: Rollback selection remains non-interactive; operators must pass `--to <path>` or `--to last`.

## Confirmation

`test_programstart_cli.py` must cover `kb` and `diff` dispatch. `test_programstart_workflow_state.py` must cover rollback confirmation and restore behavior. `uv run programstart validate --check all`, `uv run programstart drift`, and the full pytest suite must pass after the change.

## Links

- DEC-007 in `PROGRAMBUILD/DECISION_LOG.md`
- `scripts/programstart_cli.py`
- `scripts/programstart_workflow_state.py`
- `PROGRAMBUILD/ARCHITECTURE.md`
