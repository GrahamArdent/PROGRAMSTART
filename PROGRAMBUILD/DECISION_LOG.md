# DECISION_LOG.md

Purpose: Running record of material project decisions, reversals, and rationale.
Owner: Solo operator
Last updated: 2026-04-18
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
| DEC-008 | 2026-04-15 | inputs_and_mode_selection | Separate prompt architecture into `workflow`, `operator`, and `internal` classes; restrict workflow routing to `workflow` prompts; and require class-aware standards, registry placement, and validation | ACTIVE | — | Solo operator | docs/decisions/0011-separate-workflow-and-operator-prompt-architecture.md |
| DEC-009 | 2026-04-15 | inputs_and_mode_selection | Structural hardening sessions MUST run ADR triage and a targeted audit loop before checkpoint close-out; Phase J items MUST do this every session | SUPERSEDED | DEC-010 | Solo operator | docs/decisions/0012-require-hardening-adr-triage-and-audit-loop.md |
| DEC-010 | 2026-04-15 | inputs_and_mode_selection | Long-form operator execution prompts that can land durable structural or policy changes MUST require a governance close-out loop and truthful direct-command verification; ADR-0013 supersedes the hardening-only framing of ADR-0012 | REVERSED | DEC-009 | Solo operator | docs/decisions/0013-require-governance-close-out-for-durable-operator-checkpoints.md |
| DEC-011 | 2026-04-15 | inputs_and_mode_selection | Split the template `process-registry` into a root manifest plus fragments, keep `load_registry()` as the stable merged contract, and stamp generated project repos back to a flat registry during bootstrap | ACTIVE | — | Solo operator | docs/decisions/0014-compose-process-registry-from-manifest-and-fragments.md |
| DEC-012 | 2026-04-16 | inputs_and_mode_selection | External agent systems SHOULD be reused by adopt/adapt/reject decomposition: keep transferable evidence-and-policy scaffolding, but do not adopt prompt-led control loops wholesale as the governing architecture | ACTIVE | — | Solo operator | docs/decisions/0015-reuse-external-agent-systems-by-pattern-not-wholesale.md |
| DEC-013 | 2026-04-16 | inputs_and_mode_selection | Every operator gameplan MUST have a corresponding execution prompt unless it declares an explicit exemption (infrastructure-repair or bootstrap); `programstart validate --check gameplan-prompt-pairing` enforces this rule | ACTIVE | — | Solo operator | docs/decisions/0016-require-execution-prompt-for-operator-gameplans.md |
| DEC-014 | 2026-04-17 | inputs_and_mode_selection | `programstart jit-check` wraps `guide` + `drift` + sync-rule summary into a single CLI command; exit 0 = clean, 1 = drift, 2 = guide failure; implemented inline in `programstart_cli.py` following the `run_next` pattern | ACTIVE | — | Solo operator | docs/decisions/0017-jit-check-cli-command.md |
| DEC-015 | 2026-04-17 | inputs_and_mode_selection | `programstart advance --defer` marks the active step as intentionally paused without advancing; records a `deferred` object with date and reason; staleness detection treats the deferred date as latest activity | ACTIVE | — | Solo operator | docs/decisions/0018-workflow-deferral-mechanism.md |
| DEC-016 | 2026-04-18 | inputs_and_mode_selection | Add typed Pydantic models for the process registry via parallel `load_validated_registry()` alongside existing `load_registry()` dict API; lazy import; `extra="allow"` for schema evolution | ACTIVE | — | Solo operator | docs/decisions/0019-typed-pydantic-models-for-process-registry.md |
| DEC-017 | 2026-04-18 | inputs_and_mode_selection | `programstart sync --dest <path>` propagates changed PROGRAMSTART files to a downstream repo using a manifest written at attach time; dry-run by default, `--confirm` required for writes; `.programstart-preserve` for downstream customization protection | ACTIVE | — | Solo operator | docs/decisions/0020-downstream-sync-mechanism-with-manifest-tracking.md |
| DEC-018 | 2026-04-19 | inputs_and_mode_selection | `programstart prompt-build --mode context` generates structured `.prompt.md` from arbitrary `--context key=value` pairs without requiring a bootstrapped PROGRAMBUILD project; required key: `goal`; well-known keys: `project`, `stage`, `stack`, `shape` | ACTIVE | — | Solo operator | docs/decisions/0021-prompt-builder-mode-b-context-driven-generation.md |

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

### DEC-008

- Context: PROGRAMSTART currently mixes product workflow prompts, PROGRAMSTART maintenance prompts, and internal build prompts under one broad prompt model. That causes workflow-routing semantics, prompt standards, registry placement, and compliance validation to bleed into prompts that are not part of stage or phase progression.
- Decision: Define three prompt classes: `workflow`, `operator`, and `internal`. Restrict workflow routing to `workflow` prompts only. Separate prompt discoverability from workflow routing in the registry. Keep `devlog/` gameplans non-canonical. Require class-aware standards and validation.
- Why: Future generated programs will build from this repository. Ambiguous prompt architecture here would propagate maintenance semantics and routing confusion downstream.
- Alternatives considered: (1) Keep one universal prompt model and add exceptions. (2) Move maintenance prompts without changing standards or registry semantics. Both leave the root ambiguity in place.
- Consequences: A follow-up remediation gameplan must start from this architecture decision and then update standards, registry semantics, compliance checks, prompt classification, and inheritance rules. ADR 0011 supersedes the broad interpretation of DEC-005/ADR-0008 by narrowing cross-cutting registration to workflow prompts only.

### DEC-009

- Context: Hardening work now includes strategic refactors and workflow-policy changes, but the durable audit machinery in PROGRAMBUILD is still anchored at Stage 9 and the hardening prompt did not explicitly force ADR triage at each checkpoint. That created room for structural sessions to finish green while leaving the ADR decision implicit.
- Decision: Require a hardening close-out loop for structural or policy-affecting work. Before closing a hardening checkpoint, run `programstart validate --check adr-coverage`, `programstart validate --check authority-sync`, and `programstart drift`, then compare the change against the ADR threshold. Phase J items must do this on every session.
- Why: Green tests and drift checks are necessary but insufficient for governance-heavy refactors. The explicit loop keeps architecture history, authority alignment, and strategic-session checkpoints tied together.
- Alternatives considered: (1) Rely on final Stage 9 audit only — too late for template hardening sessions. (2) Rely on memory or reviewer discretion to decide ADR need — not mechanically dependable enough.
- Consequences: Hardening sessions now end with an explicit “ADR required / not required” decision. Strategic refactors cannot quietly bypass architecture-history hygiene, and authority-sync drift is checked before the session is considered complete.

### DEC-010

- Context: The hardening-specific close-out loop exposed a broader pattern: long-form operator prompts can change durable repo policy or structure, but the operator standard itself did not require a governance close-out loop or truthful direct-command verification. That left the same ambiguity available in enhancement, gate-repair, and remediation sessions.
- Decision: Require long-form operator execution prompts that can land durable structural or policy changes to define a governance close-out loop and use the truthful direct command surface without truncated diagnosis. ADR-0013 supersedes ADR-0012 by generalizing the rule beyond hardening.
- Why: The gap is architectural, not hardening-specific. Fixing it at the operator-prompt layer prevents repeated prompt-by-prompt rediscovery and keeps durable repo changes auditable.
- Alternatives considered: (1) Keep the hardening-only rule — leaves the same weakness elsewhere. (2) Rely on reviewers to infer when governance close-out is needed — not deterministic enough.
- Consequences: Operator prompts now have a shared governance pattern for durable checkpoints. Hardening remains a concrete application, but enhancement, gate repair, and prompt-architecture remediation now follow the same close-out model.

### DEC-011

- Context: `config/process-registry.json` had grown into a large monolith that mixed workspace assets, workflow guidance, prompt metadata, and workflow-state config in one file. J-2 required splitting that structure without breaking the many scripts, tests, and generated-project flows that depend on `load_registry()`.
- Decision: Convert the template registry to a root manifest plus fragment files under `config/registry/`, keep `scripts.programstart_common.load_registry()` and `load_registry_from_path()` as the stable merged interface, and stamp bootstrapped project repos back to a flat registry so generated repos do not inherit template-only fragments accidentally.
- Why: This isolates change domains inside the template repo, reduces edit blast radius, and preserves backward compatibility for runtime consumers and generated project repos.
- Alternatives considered: (1) Keep the monolith and accept ongoing merge conflicts and high-risk edits. (2) Split the registry and force all consumers, including generated repos, to become fragment-aware immediately.
- Consequences: Template-side tooling now validates a composed registry, schema enforcement runs through a dedicated script, and generated repos remain compatible because bootstrap resolves the manifest before writing the project registry.

---

### DEC-012

- Context: External agent systems (Orchestra, CrewAI, AutoGen, etc.) offer reusable patterns for evidence-gathering and policy scaffolding, but their prompt-led control loops are incompatible with PROGRAMSTART's evidence-and-registry governance model.
- Decision: Reuse external agent systems by adopt/adapt/reject decomposition rather than wholesale adoption.
- Why: Prompt-based scheduling lacks the trustworthiness guarantees needed for durable governance. Extracting transferable patterns gives the benefit without the liability.
- Alternatives considered: (1) Adopt an external agent framework wholesale. (2) Ignore external systems entirely.
- Consequences: PROGRAMSTART retains its own governance model while selectively adopting useful patterns like structured health probes, assessment prompts, and evidence-gathering protocols.

---

### DEC-013

- Context: No written rule defined when an operator gameplan requires an execution prompt. During hardening Phase G, the execution prompt's verification protocol required all gates to pass, but Phase G exposed broken gate infrastructure. The prompt's scope guard forbade gate repairs, creating a circular dependency that blocked execution.
- Decision: Every operator gameplan MUST have a corresponding `execute-*` operator prompt registered in `operator_prompt_files` — unless it declares an explicit exemption (`infrastructure-repair` or `bootstrap`). Machine enforcement via `programstart validate --check gameplan-prompt-pairing`.
- Why: Execution prompts enforce JIT protocol, scope guards, verification gates, and governance close-out loops. Without them, multi-phase work lacks predictability and resumability. The exemptions prevent the Phase G deadlock pattern where a prompt's protocol depends on infrastructure the gameplan is repairing.
- Alternatives considered: (1) Require a prompt for every gameplan with no exceptions. (2) Continue with the implicit de facto pattern and no enforcement.
- Consequences: Operator gameplans get execution prompts by default with machine-enforced pairing. Exempt gameplans must declare their exemption explicitly. The Phase G deadlock pattern is documented and prevented.

---
