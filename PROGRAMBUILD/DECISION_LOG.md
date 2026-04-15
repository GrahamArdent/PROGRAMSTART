# DECISION_LOG.md

Purpose: Running record of material project decisions, reversals, and rationale.
Owner: Solo operator
Last updated: 2026-04-14
Depends on: FEASIBILITY.md, RESEARCH_SUMMARY.md, ARCHITECTURE.md
Authority: Canonical for project decision history

---

## Status Vocabulary

| Status | Meaning |
|---|---|
| PROPOSED | Decision is under consideration — not yet committed |
| ACTIVE | Decision is committed and in force |
| REVERSED | This row replaces an earlier decision. The `Replaces` column points to the original ID. |
| SUPERSEDED | This original decision has been overridden. See the `Replaces` column of the REVERSED entry. |

**Reversal rule:** When a decision is overridden, add a new REVERSED row and update the original row's status to SUPERSEDED. Both rows must exist — do not delete the original. See `PROGRAMBUILD_CHALLENGE_GATE.md` Part F for the enforcement rules.

---

## Decision Register

| ID | Date | Stage | Decision | Status | Replaces | Owner | Related file |
|---|---|---|---|---|---|---|---|
| DEC-001 | 2026-04-11 | inputs_and_mode_selection | Root-workspace smoke MUST be read-only; mutating dashboard smoke MUST run only in isolated temp workspaces | ACTIVE | — | Solo operator | noxfile.py, scripts/programstart_dashboard_smoke.py |
| DEC-002 | 2026-04-11 | inputs_and_mode_selection | signoff_history arrays in STATE.json capped at 100 entries (FIFO trim); oldest dropped when exceeded; warning logged to stderr | ACTIVE | — | Solo operator | scripts/programstart_serve.py |
| DEC-003 | 2026-04-12 | inputs_and_mode_selection | Accept sys.argv mutation pattern in temporary_argv() as-is — single-threaded CLI, properly restores in finally block | ACTIVE | — | Solo operator | scripts/programstart_cli.py |
| DEC-004 | 2026-04-12 | inputs_and_mode_selection | Clarify CANONICAL rule 1 with temporal semantics: code outranks docs retroactively; developers MUST update docs proactively | ACTIVE | — | Solo operator | PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md |
| DEC-005 | 2026-04-12 | inputs_and_mode_selection | Cross-cutting prompts registered via `cross_cutting_prompts` array at workflow_guidance level, merged by step_guide at display time — avoids polluting every stage's prompts array | ACTIVE | — | Solo operator | config/process-registry.json, scripts/programstart_step_guide.py |
| DEC-006 | 2026-04-13 | inputs_and_mode_selection | Both `PROGRAMBUILD_CANONICAL.md §N` and `PROGRAMBUILD.md §N` required in shaping prompt Authority Loading — CANONICAL provides stage boundaries and required output list; PROGRAMBUILD.md provides procedural protocol for how to do the work | ACTIVE | — | Solo operator | .github/prompts/shape-*.prompt.md |
| DEC-007 | 2026-04-14 | inputs_and_mode_selection | Expose retrieval and state snapshot operations through unified CLI aliases (`programstart kb`, `programstart diff`) and require explicit `--confirm` for `programstart state rollback` restores | ACTIVE | — | Solo operator | scripts/programstart_cli.py, scripts/programstart_workflow_state.py, PROGRAMBUILD/ARCHITECTURE.md |

## Decision Details

### DEC-001

- Context: Dashboard smoke script exercises 3 POST routes that mutate the live workspace (uj-phase, uj-slice, workflow-signoff). Only workflow-advance uses dry_run. The signoff route is accumulative — each run adds a new history entry to STATE.json.
- Decision: Read-only smoke for root workspace. Mutating smoke isolated to bootstrapped temp workspaces only.
- Why: Trust boundary. Operators must trust that orientation tools (guide, drift, dashboard) do not silently change state. Repeated smoke runs must not leave artifacts.
- Alternatives considered: (1) Add dry_run to all POST routes — still requires trusting the flag. (2) Environment variable guard on server — smoke-level isolation is simpler to reason about.
- Consequences: Dashboard smoke split into read-only script and existing mutating script. CI continues running mutating smoke in bootstrapped workspaces. Root-workspace smoke is guaranteed non-mutating.
- Follow-up: Phase 1.5 may add route-level read-only guard for defense-in-depth.

### DEC-002

- Context: `save_workflow_signoff()` and `advance_workflow_with_signoff()` in `scripts/programstart_serve.py` append to the `signoff_history` array in STATE.json without any size limit. Over long-running multi-year projects, this grows unboundedly.
- Decision: Cap `signoff_history` at 100 entries using FIFO trim. When new entries push the list past 100, the oldest entries are dropped. A warning is logged to stderr when trimming occurs.
- Why: 100 entries covers ~50 stage transitions with 2 signoffs each — more than sufficient for even multi-year projects. Git history already preserves all prior state file versions, so no data is permanently lost.
- Alternatives considered: (1) Archive to separate file — adds complexity for no practical value. (2) No cap — eventual data bloat in STATE.json. (3) Warning-only at threshold — doesn't prevent growth.
- Consequences: Old signoff entries are dropped after 100. Operators see a stderr warning when this occurs. git history retains all prior states for forensic needs.

### DEC-003

- Context: `run_passthrough()` in `scripts/programstart_cli.py` uses `temporary_argv()` to mutate `sys.argv` before calling subcommand `main()` functions. This is not thread-safe.
- Decision: Accept the pattern as-is. No refactoring needed.
- Why: The CLI is single-threaded by design. The context manager properly restores `sys.argv` in a `finally` block. Refactoring would require changing every script's `main()` signature for no practical benefit.
- Alternatives considered: (1) Refactor all `main()` functions to accept optional `argv` parameter — high churn, no benefit for single-threaded CLI. (2) Replace with subprocess calls — slower, more complex. (3) Thread-local storage — unnecessary complexity for single-threaded program.
- Consequences: Pattern is documented. If the CLI ever becomes multi-threaded, this becomes a known refactoring target. Revisit only if threading is introduced.

### DEC-004

- Context: PROGRAMBUILD_CANONICAL.md rule 1 says "Validated code and validated tests MUST outrank any planning document." Meanwhile, copilot-instructions.md says "Do not ship code that contradicts an authority doc." These create apparent tension without temporal qualification.
- Decision: Add temporal clarification to rule 1. "MUST outrank" applies retroactively when conflicts are discovered. Developers MUST update authority docs proactively before introducing contradictory code.
- Why: Without clarification, rule 1 could be read as license to skip doc updates entirely. The temporal distinction resolves the tension between the two guidelines.
- Alternatives considered: (1) Remove rule 1 — weakens the practical escape hatch when code diverges from stale docs. (2) Add clarification only in source-of-truth.instructions.md — leaves CANONICAL itself ambiguous.
- Consequences: Rule 1 is now precise. The copilot-instructions.md prospective rules and the CANONICAL retroactive rules work together without contradiction.

### DEC-005

- Context: Stage guide prompts were being mixed into per-stage prompts arrays, causing duplication across all stages.
- Decision: Register cross-cutting prompts (programstart-stage-guide, programstart-stage-transition) via a `cross_cutting_prompts` array at the workflow_guidance level. The step_guide script merges them at display time.
- Why: Avoids polluting every stage's prompts array with identical entries. Single registration point.
- Alternatives considered: Add them to every stage's prompts array — creates maintenance burden (N copies).
- Consequences: programstart guide shows cross-cutting prompts at every stage without separate registration per stage.

### DEC-006

- Context: Shaping prompts (shape-research, shape-requirements, shape-architecture, shape-scaffold, shape-test-strategy, shape-release-readiness, shape-post-launch-review) cited `PROGRAMBUILD_CANONICAL.md §N` in Authority Loading but not `PROGRAMBUILD.md §N`, even though Protocol Declaration already cited PROGRAMBUILD.md §N. This created a gap: CANONICAL provides stage boundaries and required output list; PROGRAMBUILD.md provides the procedural protocol for how to do the work.
- Decision: Add `PROGRAMBUILD.md §N` bullet immediately after `PROGRAMBUILD_CANONICAL.md §N` in Authority Loading of all 7 affected stage shaping prompts.
- Why: Protocol Declaration tells the AI what authority section to follow, but if that file isn't pre-loaded in Authority Loading, the AI may proceed without reading it. Loading both ensures complete authority coverage.
- Alternatives considered: Remove Protocol Declaration's PROGRAMBUILD.md reference — weakens the protocol clarity.
- Consequences: All 7 stage shaping prompts now pre-load both authority files before beginning work.

### DEC-007

- Context: Retrieval commands and snapshot comparison already existed in lower-level script modules, but the unified `programstart` CLI did not expose a first-class `kb` alias or a top-level `diff` alias. State restore capability was also missing, despite existing snapshot infrastructure.
- Decision: Add `programstart kb search` and `programstart kb ask` as unified CLI aliases over `programstart_retrieval`; add `programstart diff` as a unified CLI alias over workflow-state diff; add `programstart state rollback` that restores from a saved snapshot only when `--confirm` is provided.
- Why: The unified CLI is the documented operator entry point. Aliases reduce command-surface fragmentation while reusing existing retrieval and state-snapshot logic. Mandatory confirmation on rollback keeps destructive state restoration explicit.
- Alternatives considered: (1) Keep retrieval and diff only in script-specific CLIs — leaves the unified CLI incomplete. (2) Add interactive rollback selection — increases complexity and is less automation-friendly. (3) Restore without a safety flag — too risky for workflow state.
- Consequences: Operators can query the knowledge base and compare snapshots entirely through `programstart`. Rollback now creates a pre-rollback snapshot before restoring saved state and refuses to run without explicit confirmation.

---
