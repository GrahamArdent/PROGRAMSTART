---
status: accepted
date: 2026-04-12
deciders: [solo operator]
consulted: []
informed: []
---

# 0006. Accept sys.argv Mutation Pattern

## Context and Problem Statement

`run_passthrough()` in `scripts/programstart_cli.py` uses `temporary_argv()` to mutate `sys.argv` before calling subcommand `main()` functions. This context manager pattern is not thread-safe. The question is whether to refactor all script `main()` functions to accept an optional `argv` parameter, or to accept the current pattern.

## Decision Drivers

- The CLI is single-threaded by design; no concurrent command dispatch exists.
- The `temporary_argv()` context manager properly restores `sys.argv` in a `finally` block.
- Refactoring would touch every script's `main()` signature for no practical benefit.
- Several scripts (e.g., `programstart_health_probe.py`) already accept `argv` parameters independently.

## Considered Options

- Option A — Accept the pattern as-is (this decision)
- Option B — Refactor all `main()` functions to accept optional `argv` parameter
- Option C — Replace with subprocess calls to each script
- Option D — Thread-local storage for argv isolation

## Decision Outcome

Chosen option: **Option A (accept the pattern)**, because the CLI is single-threaded, the context manager handles cleanup correctly, and the refactoring cost is high with no practical benefit.

### Consequences

- Good: No churn across script `main()` signatures.
- Good: Pattern is now documented and explicitly accepted rather than implicitly tolerated.
- Bad: If the CLI ever becomes multi-threaded, this is a known refactoring target.
- Neutral: Individual scripts may independently adopt `argv` parameters for testability, which is fine.

## Confirmation

- CLI smoke exercises all passthrough commands successfully.
- `temporary_argv()` context manager has a `finally` block that restores original `sys.argv`.
- No threading is introduced in the CLI dispatch path.

## Links

- [DEC-003 in DECISION_LOG.md](../../PROGRAMBUILD/DECISION_LOG.md)
- [PROGRAMBUILD_ADR_TEMPLATE.md](../../PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md)
