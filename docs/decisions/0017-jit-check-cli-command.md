---
status: accepted
date: 2026-04-17
deciders: [Solo operator]
consulted: []
informed: []
---

# 0017. JIT Check CLI Command

<!-- DEC-014 -->

## Context and Problem Statement

The JIT source-of-truth protocol (`.github/instructions/source-of-truth.instructions.md`) requires four steps before any planning or documentation task: derive context via `guide`, verify baseline via `drift`, identify authority files, and verify after edits. Operators must currently run three separate commands (`guide`, `drift`, manually inspect sync rules) and remember the correct order. This friction means the protocol is sometimes skipped or partially executed.

## Decision Drivers

- The JIT protocol is the core operational discipline of PROGRAMSTART — it must be easy to invoke correctly.
- Operators should not need to remember multi-step sequences for routine discipline checks.
- Existing `guide` and `drift` commands are well-tested and should not be duplicated.
- Exit codes must be unambiguous for CI and scripting use.

## Considered Options

- Option A — Standalone script (`scripts/programstart_jit_check.py`) with its own `main()` function
- Option B — Inline function in `programstart_cli.py` that composes existing commands (like `run_next`)
- Option C — Shell alias or task-only composition (no CLI command)

## Decision Outcome

Chosen option: **Option B**, because the `jit-check` command is a composition of existing commands with a small amount of additional output (sync rule summary). This matches the established pattern of `run_next` in `programstart_cli.py`, which also composes `status`, `guide`, and `drift` calls. Creating a standalone module would add unnecessary file overhead for what is essentially a dispatch function.

### Exit Code Semantics

| Code | Meaning |
|------|---------|
| 0 | Clean — guide succeeded, no drift detected |
| 1 | Drift — guide succeeded but drift check found violations |
| 2 | Guide failure — guide command returned non-zero |

### Scope

- `jit-check` **wraps** `guide` and `drift`; it does not replace them.
- `jit-check` accepts `--system programbuild` or `--system userjourney` to scope the guide output.
- `jit-check` prints the authority → dependent sync rules from the registry as an aid for Step 3 of the protocol.
- `jit-check` does **not** perform edits, advance stages, or validate files beyond what `guide` and `drift` already do.

### Consequences

- Good: Single command replaces a three-step manual sequence.
- Good: Exit codes enable CI gating and script composition.
- Good: No new module file — keeps the codebase lean.
- Neutral: The `next` command already calls `guide` and `drift` but with different intent (orientation vs. discipline check). Both commands coexist.

## Pros and Cons of the Options

### Option A — Standalone script

- Good, because it follows the one-module-per-command convention used by most commands.
- Bad, because the logic is pure composition (~20 lines) and does not warrant its own module.
- Bad, because it would require import wiring in both the package and standalone fallback blocks.

### Option B — Inline in CLI dispatcher

- Good, because it matches the `run_next` pattern already established.
- Good, because no new imports or module wiring needed.
- Bad, because it adds another inline function to `programstart_cli.py`, which is already long.

### Option C — Shell alias / task-only

- Good, because it requires zero code changes.
- Bad, because it cannot be tested, gated in CI, or composed programmatically.
- Bad, because it violates the principle that operational discipline should be in the CLI control plane.
