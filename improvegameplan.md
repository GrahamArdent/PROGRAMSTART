# Improve Gameplan

Purpose: Detailed implementation plan for strengthening PROGRAMSTART automation and protocol surfacing without executing changes yet.
Status: Ready for implementation — all review passes complete, code examples verified 2026-04-11
Authority: Non-canonical working plan derived from current source-of-truth files and automation review.
Last updated: 2026-04-11

---

## 1. What We Learned And How JIT Is Already Surfaced

The Just-in-Time source-of-truth protocol is not absent in PROGRAMSTART. It is already surfaced in multiple layers, but those layers are inconsistent in force and visibility.

### 1.1 Instruction Layer

JIT is explicitly defined in:

- `.github/instructions/source-of-truth.instructions.md`
- `.github/copilot-instructions.md`

Current surfacing strengths:

- clearly states `guide -> drift -> canonical first -> validate + drift`
- frames JIT as mandatory before planning or config changes
- names the authority files by concern

Current weakness:

- this layer is strong for AI-assisted work and careful human operators, but it is not the primary surface most repo users interact with day to day
- the rule exists in prose, but the default automation path does not fully enforce it

### 1.2 CLI Layer

JIT is surfaced directly through commands:

- `programstart guide`
- `programstart drift`
- `programstart validate`

Current surfacing strengths:

- the command surface gives users the right primitives
- command registry includes `guide.*` and `drift`
- CLI smoke exercises `guide --system programbuild`, `validate --check workflow-state`, `state show`, and `next`
- CLI smoke does NOT exercise `drift` or `guide --system userjourney` — these are absent from the smoke script entirely

Current weakness:

- the commands exist, but users are still expected to remember the correct sequence
- the CLI does not currently make the JIT sequence the default validated path for local work

### 1.3 Dashboard Layer

JIT is surfaced in the dashboard through:

- guide panels
- drift summary widgets
- dashboard buttons for `Refresh Guide` and `Drift Check`
- dashboard API state carrying drift summary data

Current surfacing strengths:

- the dashboard exposes JIT as a visible workflow concept, not just a hidden script
- the operator can trigger guide and drift from the UI

Current weakness:

- the dashboard currently mixes read-only orientation with mutating operations
- as implemented, smoke coverage for the dashboard can exercise write endpoints against the live workspace, which weakens trust in the dashboard as a safe orientation surface

### 1.4 Docs Layer

JIT is surfaced in:

- `README.md`
- `QUICKSTART.md`
- `docs/context-layer.md`
- `docs/dashboard-api.md`

Current surfacing strengths:

- `QUICKSTART.md` already gives a usable path with `pb guide` and `pb drift`
- `README.md` explains drift and source-of-truth behavior clearly

Current weakness:

- the docs describe JIT well, but the task and nox surfaces still undersignal it
- there is no single “safe default operator sequence” exposed as the dominant local workflow contract

### 1.5 Nox And Task Layer

JIT is only partially surfaced here.

Current surfacing strengths:

- `validate` runs multiple validation passes
- VS Code tasks expose `guide` and several validate variants

Current weakness:

- `programstart drift` is not embedded as a first-class gate in `validate`
- there is no dedicated `Drift Check` task in `.vscode/tasks.json`
- the most visible automation paths still emphasize validate/test/docs over authority-first workflow control

### 1.6 Summary Judgment

JIT is already surfaced in PROGRAMSTART at the instruction, CLI, dashboard, and docs levels.

The actual problem is not discovery. The problem is enforcement hierarchy.

PROGRAMSTART currently treats JIT as:

- explicit in instructions
- available in commands
- visible in UI
- documented in onboarding

But not yet as:

- mandatory in default automation
- isolated from unsafe smoke behavior
- central in the editor task surface

That mismatch is the core implementation gap.

---

## 2. Updated Gameplan

This gameplan keeps the previously identified priorities, but now anchors them explicitly to how JIT and source-of-truth behavior are already surfaced.

### Phase 1: Stabilize Protocol Surfacing And Smoke Safety

Purpose:

- make JIT visible in the automation surfaces users actually run
- stop smoke automation from weakening confidence in the dashboard and live workspace

Outcome that must be true:

- root-workspace smoke is read-only
- JIT is exposed as an explicit task and gate, not just as guidance text
- contributors can follow a default local workflow that naturally enforces `guide -> drift -> validate`

Why first:

- this is the highest-leverage improvement because it changes operator behavior and tool trust at the same time
- it reduces the chance that future automation work bakes in the wrong assumptions

### Phase 2: Make Drift A Mandatory Gate

Purpose:

- align automation with the documented Source-of-Truth JIT protocol

Outcome that must be true:

- `programstart drift` runs in the standard validate path before and after change verification
- drift is visible as a first-class task in VS Code

### Phase 3: Add Clean-Tree Assertions For Root-Workspace Automation

Purpose:

- detect silent mutation in repo-level smoke or orientation flows

Outcome that must be true:

- any root-workspace smoke that dirties tracked files fails loudly

### Phase 4: Reframe Local And CI Gates By Confidence Level

Purpose:

- separate fast confidence, safe merge confidence, and full release confidence

Outcome that must be true:

- operators can choose a gate intentionally instead of guessing which bundle matters

### Phase 5: Strengthen Package And Fresh-Workspace Contract Testing

Purpose:

- make installed CLI behavior and bootstrapped workspace behavior first-class supported contracts

Outcome that must be true:

- package smoke is easy to run locally
- the generated workspace behaves like a supported product boundary

### Phase 6: Improve Diagnostics And Windows Resilience

Purpose:

- reduce failure ambiguity and make Windows a fully covered operating mode

Outcome that must be true:

- smoke and validate failures produce actionable diagnostics
- Windows path, cleanup, and subprocess edge cases are explicitly covered

---

## 3. Concrete Change Package Spec For Phase 1 Only

Phase 1 scope is intentionally narrow. It is about safe protocol surfacing and smoke boundaries, not about every planned improvement.

### 3.1 Objective

Change PROGRAMSTART so that the most visible operator paths reinforce the JIT protocol and do not mutate the live workspace during smoke checks.

### 3.2 Files To Modify

Primary files:

- `noxfile.py`
- `.vscode/tasks.json`
- `scripts/programstart_dashboard_smoke.py`
- `scripts/programstart_cli_smoke.py`
- `scripts/programstart_serve.py`
- `README.md`
- `QUICKSTART.md`

Likely test files:

- `tests/test_programstart_command_registry.py`
- `tests/test_programstart_dashboard.py`
- `tests/test_programstart_serve.py`
- `tests/test_serve_endpoints.py`
- `tests/test_programstart_cli.py`

Possible new test or helper files:

- `tests/test_programstart_dashboard_smoke_contract.py`
- `scripts/programstart_repo_clean_check.py`

Optional doc touchpoints if wording needs alignment:

- `docs/dashboard-api.md`
- `docs/context-layer.md`

### 3.3 Exact New Tasks, Sessions, And Scripts

#### New Or Changed Nox Sessions

1. Update `validate`

Add:

- `programstart drift` before `programstart validate --check all`
- `programstart drift` after the validate sequence

Reason:

- makes baseline and post-change drift verification part of the normal automation contract

2. Split current `smoke`

Replace the current overloaded behavior with:

- `smoke-readonly`
- `smoke-isolated-dashboard`
- `smoke-browser`

Suggested meanings:

- `smoke-readonly`: root-workspace, non-mutating, safe to run any time
- `smoke-isolated-dashboard`: mutating endpoint exercise only in temporary bootstrapped workspace
- `smoke-browser`: browser-level dashboard checks, no workflow mutation required against root workspace

3. Add `gate-safe`

Suggested contents:

- `lint`
- `typecheck`
- `tests`
- `validate`
- `smoke-readonly`
- `docs`
- `package`

Reason:

- gives contributors a realistic pre-merge confidence bundle

#### New Or Changed VS Code Tasks

Add:

- `PROGRAMSTART: Drift Check`
- `PROGRAMSTART: Guide + Drift PROGRAMBUILD`
- `PROGRAMSTART: Guide + Drift USERJOURNEY`
- `PROGRAMSTART: Package Smoke`
- `PROGRAMSTART: Read-only Dashboard Smoke`
- `PROGRAMSTART: Isolated Dashboard Smoke`
- `PROGRAMSTART: Safe Gate`

Change:

- keep `PROGRAMSTART: Full CI Gate`
- make the new `Safe Gate` the recommended local confidence task

Reason:

- the task surface should make the safe JIT path obvious without reading repo internals first

#### New Or Changed Scripts

1. Refactor `scripts/programstart_dashboard_smoke.py`

Target behavior:

- default mode is read-only
- add an explicit isolated mode or move mutating coverage into a new script

Recommended options:

- Option A: `programstart_dashboard_smoke.py --mode readonly|isolated-write`
- Option B: split into two scripts
  - `programstart_dashboard_smoke.py` for read-only
  - `programstart_dashboard_mutation_smoke.py` for isolated writes

Preferred direction:

- split the scripts

Reason:

- separate trust boundaries are easier to reason about and harder to misuse

2. Add repo cleanliness helper

Recommended new helper:

- `scripts/programstart_repo_clean_check.py`

Responsibilities:

- capture git cleanliness before a root-workspace smoke
- capture git cleanliness after the smoke
- fail with file-level summary if tracked files changed unexpectedly

3. Update `scripts/programstart_cli_smoke.py`

Add or reinforce checks for:

- `guide --system programbuild`
- `guide --system userjourney`
- `drift`
- optionally `guide --kickoff`

Reason:

- JIT surfacing should be part of CLI contract smoke, not incidental

4. Update `scripts/programstart_serve.py`

If necessary, introduce a server mode or runtime guard that prevents write endpoints from being exercised in read-only smoke mode.

Possible implementations:

- environment flag to reject mutating POST routes in read-only smoke mode
- request-time guard around `/api/uj-phase`, `/api/uj-slice`, `/api/workflow-signoff`, `/api/workflow-advance`

Preferred direction:

- smoke isolation at script level first
- route-level read-only guard only if script isolation alone is not sufficient

### 3.4 Acceptance Tests

Acceptance tests for Phase 1 must prove the new behavior operationally, not only structurally.

#### A. JIT Surfacing Tests

1. Task surface exposes JIT actions

Verify `.vscode/tasks.json` includes:

- drift task
- guide + drift tasks
- safe gate task

2. CLI smoke includes JIT path

Verify smoke covers:

- `programstart guide --system programbuild`
- `programstart guide --system userjourney`
- `programstart drift`

3. Docs reflect the recommended local sequence

Verify `README.md` and `QUICKSTART.md` show the operator path as:

- guide
- drift
- edit
- validate
- drift

#### B. Smoke Safety Tests

4. Read-only dashboard smoke does not call write endpoints

Verify the read-only smoke script performs only GET requests or other explicitly non-mutating actions.

5. Root-workspace smoke leaves repo clean

Test behavior:

- capture git status before smoke
- run read-only smoke
- assert git status is unchanged after smoke

6. Mutating dashboard smoke only runs in temp workspace

Test behavior:

- bootstrapped temp workspace is created
- mutating routes are exercised there
- root workspace remains clean

7. Dashboard UI still exposes guide and drift controls

Verify buttons or command hooks for guide and drift remain present and functional.

#### C. Session Wiring Tests

8. `validate` runs drift before and after validation

Test behavior:

- inspect or invoke session wiring to confirm drift is part of the validate sequence

9. `gate-safe` includes package smoke and read-only smoke

Test behavior:

- inspect nox session composition or run a command registry style test to prove expected membership

### 3.5 Rollback Criteria

Rollback Phase 1 if any of the following occur:

1. The new smoke split increases ambiguity instead of reducing it.

Evidence:

- operators cannot tell which smoke to run
- task names do not communicate trust boundaries clearly

2. Read-only smoke loses meaningful coverage.

Evidence:

- important dashboard regressions are no longer caught
- route coverage drops to trivial HTML load only

3. Isolated mutating smoke becomes too brittle or too slow to be usable.

Evidence:

- repeated failures caused by temp workspace orchestration rather than product behavior
- runtime becomes unacceptable for routine use

4. Drift wiring in `validate` produces false failures on clean repos.

Evidence:

- reproducible clean baseline still fails drift without real divergence
- validate becomes noisy enough that operators ignore it

5. Clean-tree assertions create cross-platform instability.

Evidence:

- Windows-specific file timing or newline handling causes flaky failures unrelated to real mutations

Rollback method:

- revert the new nox session split first if it is the source of confusion
- preserve any doc improvements that remain correct
- keep root-workspace write protections if they reduce risk without causing friction

### 3.6 Non-Goals For Phase 1

Do not include these in Phase 1:

- full local-versus-CI gate redesign beyond one safe gate addition
- Windows hardening beyond what is necessary for the new smoke boundary
- package/install contract expansion beyond task exposure where needed
- broad dashboard endpoint redesign
- large documentation overhaul beyond JIT surfacing updates

Reason:

- Phase 1 is about correcting trust boundaries and making JIT operationally visible
- broadening scope would reduce the chance of landing the right change cleanly

---

## 4. Recommended Phase 1 Delivery Order

1. Refactor smoke boundaries first.
2. Add clean-tree check helper second.
3. Wire drift into validate third.
4. Add VS Code tasks fourth.
5. Update README and QUICKSTART last, after behavior is settled.

---

## 5. Exit Criteria For Approving Execution

Phase 1 is ready to implement when all of the following are accepted:

- `improvegameplan.md` is accepted as the working plan
- JIT surfacing is explicitly acknowledged as an enforcement problem, not a discovery problem
- root-workspace smoke must be read-only by policy
- isolated temp-workspace smoke is accepted for mutating dashboard paths
- the repo is willing to make drift a standard validate dependency

---

## 6. Gaps And Blockers Found (Review 2026-04-11)

This section records specific findings from the 2026-04-11 source-of-truth review. All items below must be resolved or explicitly accepted before Phase 1 execution begins.

### 6.1 Source-of-Truth Gaps Already Fixed

The following gaps were identified and fixed in the same review session (canonical-first per JIT protocol):

1. **No declared authority for automation gates** — `PROGRAMBUILD_CANONICAL.md` had no authority map entry for `noxfile.py` or `.vscode/tasks.json`. Fixed: both entries added to authority map and `PROGRAMBUILD_FILE_INDEX.md` Section 3. `PROGRAMBUILD_CHANGELOG.md` updated.

2. **No sync rule for the JIT automation bundle** — `config/process-registry.json` had no `sync_rule` binding `noxfile.py`, `.vscode/tasks.json`, and `source-of-truth.instructions.md` as an aligned set. Fixed: `automation_gate_jit_alignment` sync rule added. This means `programstart drift` will now flag divergence between these files when one changes without the others being reviewed.

### 6.2 Gameplan Inaccuracies (Corrections Required)

3. **`validate` session already calls `guide`** — Section 1.5 of this gameplan states "JIT is only partially surfaced here" and implies the nox layer does not call `guide`. This is incorrect. The current `validate` nox session at line ~104 of `noxfile.py` already calls `programstart guide --system programbuild`, `programstart guide --system userjourney`, and `programstart state show`. The only missing element is `programstart drift`. The enforcement gap is drift-only, not guide+drift.

4. **`workflow-advance` already uses `dry_run=True`, but the other three POST routes are genuine mutations** — `POST /api/workflow-advance` passes `"dry_run": True` in smoke. However, the remaining routes are NOT safely idempotent:
   - `POST /api/uj-phase` calls `update_implementation_tracker_phase()` which writes to `USERJOURNEY/IMPLEMENTATION_TRACKER.md` and updates the `Last updated:` datestamp unconditionally.
   - `POST /api/uj-slice` calls `update_implementation_tracker_slice()` with the same write behavior.
   - `POST /api/workflow-signoff` calls `save_workflow_signoff()` which **appends** a new entry to the `signoff_history` array in STATE.json and writes a `saved_at` timestamp. This is accumulative — each smoke run adds a new history entry. It is NOT idempotent.
   - The prior assessment that these "write current values back" was an understatement. The signoff route in particular creates artifacts that accumulate over repeated runs.

### 6.3 Blockers For Phase 1

5. **No DECISION_LOG entry planned** — The smoke safety policy (root-workspace smoke MUST be read-only) is a significant policy decision. Before or during Phase 1 execution, this decision must be recorded in `PROGRAMBUILD/DECISION_LOG.md` per the authority model.

6. **`PROGRAMBUILD_CHANGELOG.md` not in Phase 1 delivery scope** — `PROGRAMBUILD_CANONICAL.md` rule 5 states: "system-level change history" is canonical on `PROGRAMBUILD_CHANGELOG.md`. Any Phase 1 change to nox sessions, `.vscode/tasks.json`, or smoke script trust boundaries is a system-level change. `PROGRAMBUILD_CHANGELOG.md` must be updated as part of Phase 1 delivery, not after.

7. **Phase 1 delivery order has a dependency gap** — The current Section 4 order (smoke split → clean-tree check → wire drift → VS Code tasks → docs) places docs last. However, the new `automation_gate_jit_alignment` sync rule means that when `noxfile.py` is changed, `source-of-truth.instructions.md`, `QUICKSTART.md`, and `README.md` become dependent files that must be reviewed. Doc updates are not optional if noxfile changes. Delivery order must be revised accordingly.

8. **`improvegameplan.md` not tracked in `process-registry.json` bootstrap_assets** — This file is discoverable by name but not through `programstart guide` or `programstart validate`. Decision needed: treat it as a scratch/working document (leave unregistered, accept it will not be drift-checked) or add it to bootstrap_assets (which would cause validate to fail if it is absent from any bootstrapped workspace). Recommended treatment: leave unregistered and add an explicit note to this file header that it is scratch/non-canonical.

### 6.4 Automation Possibilities Not Yet In The Gameplan

9. **`jit-check` as a first-class nox session** — Instead of only embedding drift inside `validate`, expose a new `jit-check` session that runs `guide --system programbuild → guide --system userjourney → drift → state show`. This makes JIT an explicitly named automation concept, easy to run standalone and easy to compose into gate tiers. Currently `validate` runs guide but not drift; a named `jit-check` session would make the full sequence discoverable.

10. **`PROGRAMSTART: JIT Check` as a VS Code task** — A single task that runs the full JIT sequence (`guide` both systems + `drift`) gives operators a one-click pre-edit safety check. This is more actionable than separate guide and drift tasks, which require the operator to know to run them in sequence.

11. **`What To Do Next` task should depend on JIT** — The default build task (`PROGRAMSTART: What To Do Next`) runs `programstart next` but does not verify the baseline is clean first. Adding either a pre-task dependency on `Drift Check` or a compound task convention would enforce JIT at the most common operator entry point.

12. **`automation_gate_jit_alignment` sync rule is now active in drift checker** — When Phase 1 changes `noxfile.py` or `.vscode/tasks.json`, running `programstart drift` will detect if `source-of-truth.instructions.md`, `QUICKSTART.md`, or `README.md` have not been reviewed. This is now the enforcement mechanism — it does not require a code guard; it requires following the sync rule in the same commit.

---

## 7. Revised Phase 1 Delivery Order

Updated from Section 4 to reflect the blocker findings above.

1. Record the smoke safety policy decision in `PROGRAMBUILD/DECISION_LOG.md` first.
2. Refactor smoke boundaries (split `programstart_dashboard_smoke.py`).
3. Add `programstart_repo_clean_check.py` helper.
4. Wire `programstart drift` into the `validate` nox session (before and after validate chain).
5. Add `jit-check` nox session.
6. Add VS Code tasks (`Drift Check`, `JIT Check`, `Guide + Drift PROGRAMBUILD/USERJOURNEY`, `Package Smoke`, `Safe Gate`).
7. Review and update `source-of-truth.instructions.md`, `QUICKSTART.md`, and `README.md` together — required by the `automation_gate_jit_alignment` sync rule.
8. Update `PROGRAMBUILD_CHANGELOG.md` to record all nox and task surface changes.
9. Run `programstart validate --check all` and `programstart drift` — both must pass before merge.

---

## 8. Second-Pass Audit Findings (2026-04-12)

This section records findings from a comprehensive codebase re-audit. Every item below is net-new relative to the original 2026-04-11 review.

### 8.1 JIT Enforcement Gaps

**Gap A: `programstart next` does not run drift.**

`run_next()` in `scripts/programstart_cli.py` (lines 82–96) executes `status`, `guide --system programbuild`, and `guide --system userjourney` — but NOT `drift`. This is the default build task (`PROGRAMSTART: What To Do Next`) and the most common operator entry point. The JIT protocol says `guide → drift → edit`, but the primary "what should I do" path stops at `guide`.

Severity: High. This means operators following the default path get guidance without baseline verification.

Recommendation: Phase 1 should add `drift` to `run_next()`, or the `What To Do Next` VS Code task should chain a drift step.

**Gap B: Nox `validate` does not run drift, but CI does.**

The nox `validate` session calls `guide` for both systems and `state show`, but never calls `drift`. Meanwhile, `.github/workflows/process-guardrails.yml` runs `uv run programstart drift` as a standalone step (line 165). This creates a local-vs-CI divergence: CI enforces drift, local nox validate does not.

Severity: Medium. Developers who rely on `nox -s validate` locally get a weaker check than CI.

Recommendation: Already in Phase 1 scope (Section 3.3 item 1). This audit confirms the fix is correctly scoped.

**Gap C: CLI smoke missing `guide --system userjourney` and `drift`.**

`scripts/programstart_cli_smoke.py` exercises: help, status, prompt-eval --json, clean --dry-run, validate --check workflow-state, guide --system programbuild, state show, next. It does NOT exercise `drift` or `guide --system userjourney`. The USERJOURNEY guide path is completely unverified by CLI smoke.

Severity: Medium. Regressions in the USERJOURNEY guide path or the drift command would not be caught by CLI smoke.

Recommendation: Already partially scoped in Phase 1 (Section 3.3 item 3). This audit confirms both `drift` AND `guide --system userjourney` must be added.

### 8.2 Smoke Safety Findings (Verified By Code Inspection)

**Finding D: Dashboard smoke writes are confirmed by source code inspection.**

Manual inspection of `scripts/programstart_serve.py` route handlers:

- `update_implementation_tracker_phase()` (line 568): calls `tracker_path.write_text()` on `USERJOURNEY/IMPLEMENTATION_TRACKER.md`. Also unconditionally updates the `Last updated:` date line.
- `update_implementation_tracker_slice()`: same write pattern to IMPLEMENTATION_TRACKER.md.
- `save_workflow_signoff()` (line 655): loads STATE.json, creates a signoff record with `saved_at` timestamp, appends to `signoff_history` list, calls `save_workflow_state()`. This is NOT idempotent — every call adds a new history entry.
- `advance_workflow_with_signoff()` (line 678): supports `dry_run` parameter. Returns preview text when True. Smoke passes `True`.

Conclusion: 3 of 4 POST routes exercised by dashboard smoke are real filesystem writes. Only `workflow-advance` has dry_run protection. The Section 6.2 item 4 correction above now reflects this.

**Finding E: Factory smoke has no cleanup.**

`scripts/programstart_factory_smoke.py` creates repos at `.tmp_factory_smoke/run_<timestamp>/` for cli, api, api_agents, data, web scenarios. These directories persist after the test completes. The nox `clean` session (which cleans `.tmp_nox_bootstrap`, `.tmp_nox_create`, `.tmp_dist_smoke`) does not include `.tmp_factory_smoke`.

Severity: Low. Disk hygiene issue, not a correctness issue.

Recommendation: Add `.tmp_factory_smoke` to the nox `clean` session and to the `programstart clean` CLI command. This is minor enough to include in Phase 1 without scope creep.

**Finding F: CI dashboard smoke runs against template repo with USERJOURNEY attached.**

`process-guardrails.yml` runs dashboard smoke after bootstrap, against a repo that has USERJOURNEY attached. This means the CI dashboard smoke also triggers the write endpoints (uj-phase, uj-slice, workflow-signoff) against the bootstrapped repo. This is acceptable because it runs in a temporary CI workspace, not the root repo. But it means CI is exercising the mutation paths in isolation — which is exactly the pattern Phase 1 wants to formalize locally.

Severity: Informational. No fix needed, but documents why the CI version of dashboard smoke is already safe.

### 8.3 Source-of-Truth Sync Status

**Finding G: `process-registry.json` version was stale.**

Version field read `"2026-03-31"` but the `automation_gate_jit_alignment` sync rule was added on 2026-04-11. Updated to `"2026-04-11"` in this review pass.

**Finding H: All other authority files verified consistent.**

- `PROGRAMBUILD_CANONICAL.md`: authority map has `./noxfile.py` and `.vscode/tasks.json` entries. Correct.
- `PROGRAMBUILD_FILE_INDEX.md`: Section 3 has both entries. Last updated 2026-04-11. Correct.
- `PROGRAMBUILD_CHANGELOG.md`: has 2026-04-11 entry for "Automation Gate Authority Registration." Correct.
- `config/process-registry.json`: `automation_gate_jit_alignment` sync rule present and correctly structured. Correct.

No additional authority file updates needed beyond the version bump.

### 8.4 Drift Checker Design Boundary

**Finding I: Drift checker only detects violations in uncommitted/PR-diff changes.**

`scripts/programstart_drift_check.py` uses `git_changed_files()` which runs `git diff HEAD --name-only`. This means drift only catches sync rule violations in files that are currently changed relative to HEAD. It cannot detect historical staleness — if a canonical file was changed in a past commit and its dependents were never updated, drift will pass as long as no new changes are pending.

This is not a bug. It is a deliberate design boundary — drift is a commit-time guard, not a full historical audit tool. But it means:

- Drift passing does not prove the repo is fully in sync historically.
- The only guarantee is: "among the files you changed right now, sync rules are respected."
- Template repos additionally skip step-order gating (line ~73: `if is_template_repo: continue`).

Recommendation: Document this boundary in `docs/context-layer.md` or a new paragraph in `source-of-truth.instructions.md`. No code change needed.

### 8.5 Phase 1 Scope Risk Assessment

**Finding J: Phase 1 file list is wide for a "narrow" phase.**

Section 3.2 lists 7 primary files + 5 test files + 2 new files + 2 optional docs = 16 files. For a phase labeled "intentionally narrow," that is broad.

Recommended prioritization within Phase 1 (highest-leverage first):

1. Split `programstart_dashboard_smoke.py` (read-only vs. mutating) — eliminates the core trust problem.
2. Wire `drift` into nox `validate` — closes the local-vs-CI divergence.
3. Add VS Code tasks (Drift Check, JIT Check, Safe Gate) — makes JIT discoverable in the editor.
4. Update `programstart_cli_smoke.py` — adds missing coverage for drift and USERJOURNEY guide.
5. Update docs (README, QUICKSTART, source-of-truth.instructions.md) — required by sync rule when noxfile changes.

Lower priority (can defer to Phase 1.5 without losing core value):

- `programstart_repo_clean_check.py` — valuable but not blocking the smoke split.
- `serve.py` read-only guard — the smoke split makes this unnecessary for Phase 1.
- `gate-safe` nox session — useful but not required for the core fixes.

### 8.6 Additional Automation Possibilities

**Possibility K: `programstart next` should run drift.**

Adding `drift` to the `run_next()` function makes the default build task JIT-complete. This is a one-line change (`_run("programstart", "drift")`) with outsized impact on operator behavior.

**Possibility L: Nox `clean` should include `.tmp_factory_smoke`.**

One-line addition to make `clean` comprehensive.

**Possibility M: Pre-commit hook for drift.**

Not recommended for Phase 1 (too aggressive), but worth noting: a pre-commit hook running `programstart drift` would catch sync rule violations before they reach CI. Consider for Phase 3 or later.

---

## 9. Go/No-Go Assessment

### Prerequisites Checklist

| Prerequisite | Status |
|---|---|
| Source-of-truth files are in sync | PASS — all authority files verified, version date corrected |
| Drift check passes | PASS — `programstart drift` clean as of this review |
| improvegameplan.md reflects actual codebase state | PASS — corrections applied in Sections 1.2, 6.2, and this Section 8 |
| JIT protocol is understood end-to-end | PASS — enforcement gaps documented (Gaps A, B, C) |
| No structural blockers for Phase 1 | PASS — see blocker assessment below |
| Phase 1 scope is actionable | PASS — prioritized subset identified (Finding J) |

### Blocker Assessment

| Blocker from Section 6.3 | Resolution |
|---|---|
| No DECISION_LOG entry planned | Must be first delivery step — already in revised order (Section 7 item 1) |
| PROGRAMBUILD_CHANGELOG.md not in delivery scope | Must be last delivery step — already in revised order (Section 7 item 8) |
| Delivery order has dependency gap | Fixed in revised Section 7 — docs move to step 7 alongside noxfile |
| improvegameplan.md not tracked | Decision: leave unregistered, header already states non-canonical |

No unresolved blockers remain.

### Risk Summary

| Risk | Severity | Mitigation |
|---|---|---|
| Phase 1 scope wider than intended | Medium | Use prioritized subset from Finding J; defer repo_clean_check and serve.py guard |
| Dashboard smoke split may reduce coverage | Low | Mutating smoke moves to isolated workspace, not removed |
| `programstart next` change may surprise operators | Low | Drift is fast; add `--quiet` flag if output is noisy |
| Sync rule fires on noxfile change | Expected | Docs update is already step 7 in delivery order |

### Verdict

**GO** — Phase 1 implementation may proceed.

Conditions:

1. Follow the revised delivery order in Section 7.
2. Use the prioritized subset from Finding J (items 1–5) as the core deliverable.
3. Defer `programstart_repo_clean_check.py`, `serve.py` read-only guard, and `gate-safe` nox session to Phase 1.5.
4. Record the smoke safety policy decision in DECISION_LOG before any code changes.
5. Run `programstart validate --check all` and `programstart drift` after each delivery step.

---

## 10. Prompt And Product-JIT Audit (2026-04-12)

This section records findings from a critical review of how JIT is surfaced when the PROGRAMBUILD method is used to actually build a product. The question: do the prompts and instructions tell the AI/operator to reference the *product's own* source-of-truth docs during implementation?

### 10.1 The Core Problem

PROGRAMSTART has two kinds of source-of-truth documents:

1. **Process docs** — workflow state, stage gates, sync rules, challenge gates. These govern *how the PROGRAMBUILD method works*.
2. **Product docs** — ARCHITECTURE.md, REQUIREMENTS.md, USER_FLOWS.md, RISK_SPIKES.md. These govern *what the product is and how it must be built*.

JIT is currently enforced for process docs. It is **not enforced** for product docs during active implementation. This means:

- An operator building a product can write code that contradicts ARCHITECTURE.md and nothing in the system will catch it.
- The AI can implement features that are not in REQUIREMENTS.md and no prompt tells it to check first.
- If ARCHITECTURE.md changes mid-implementation, no sync rule or prompt requires in-progress code to be re-verified.

### 10.2 Evidence: What `programstart guide` Returns During Implementation

Running `programstart guide --system programbuild` during the `implementation_loop` stage returns:

**Files returned:**
- PROGRAMBUILD/TEST_STRATEGY.md
- PROGRAMBUILD/DECISION_LOG.md
- PROGRAMBUILD/PROGRAMBUILD_CHECKLIST.md
- PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md
- PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md

**Files NOT returned (but critical for implementation):**
- PROGRAMBUILD/ARCHITECTURE.md — the authority for system design, contracts, auth model
- PROGRAMBUILD/REQUIREMENTS.md — the authority for what must be built
- PROGRAMBUILD/USER_FLOWS.md — the authority for user journey behavior

This means the JIT protocol's Step 1 ("run `programstart guide` to get the minimal file set; read only those files") actively *excludes* the product's most important documents from the implementation workflow.

### 10.3 Evidence: What The Prompts Say

All 8 prompt files were reviewed. None of them tell the AI to re-read product docs before writing implementation code.

| Prompt | References product docs? | What it actually says |
|---|---|---|
| `start-programstart-project.prompt.md` | No | Run `programstart_step_guide.py --kickoff`, use registry |
| `programstart-stage-guide.prompt.md` | No | Return files from `programstart_step_guide.py` |
| `programstart-what-next.prompt.md` | No | Run status + step guide, return stage/blockers/next files |
| `programstart-stage-transition.prompt.md` | Transition only | Challenge Gate checks kill criteria, scope, assumptions at boundaries |
| `programstart-cross-stage-validation.prompt.md` | Transition only | Cross-stage checks at transitions, not during active work |
| `audit-process-drift.prompt.md` | No | Uses process-registry sync rules (which don't bind implementation) |
| `propagate-canonical-change.prompt.md` | No | Propagates process doc changes to dependent process docs |
| `userjourney-next-slice.prompt.md` | No | Reads USERJOURNEY docs, not product ARCHITECTURE/REQUIREMENTS |

### 10.4 Evidence: What The Instructions Say

| Instruction file | Tells AI to read product docs during coding? | What it actually covers |
|---|---|---|
| `source-of-truth.instructions.md` | No | Process JIT only. Authority table lists PROGRAMBUILD_CANONICAL.md, process-registry.json, etc. Does NOT list ARCHITECTURE.md or REQUIREMENTS.md. |
| `programbuild.instructions.md` | No | Applies to `PROGRAMBUILD/**/*.md` edits only, not implementation code. |
| `copilot-instructions.md` | No | "Never assert from memory" applies to process docs. No parallel rule for product docs. |
| `conventional-commits.instructions.md` | No | Commit format only. |

### 10.5 Evidence: What The Sync Rules Cover

`config/process-registry.json` has 12+ sync rules. None of them bind implementation behavior to product docs:

| Sync rule | Binds implementation to product docs? |
|---|---|
| `programbuild_architecture_contracts` | No — binds ARCHITECTURE.md to TEST_STRATEGY.md, RELEASE_READINESS.md, RISK_SPIKES.md (all process docs) |
| `programbuild_requirements_scope` | No — binds REQUIREMENTS.md to USER_FLOWS.md, ARCHITECTURE.md, TEST_STRATEGY.md (all stage outputs) |
| `programbuild_feasibility_cascade` | No — binds FEASIBILITY.md to downstream process docs |
| `automation_gate_jit_alignment` | No — binds noxfile.py to source-of-truth.instructions.md |
| All others | No — all bind process docs to process docs |

**Zero sync rules bind ARCHITECTURE.md or REQUIREMENTS.md to implementation-stage behavior.**

### 10.6 Evidence: What The Challenge Gate Misses

The Mid-Implementation Challenge Gate (run every 3–5 features) checks:

- Part A: Kill criteria — process concern ✅
- Part B: Assumptions — process concern ✅
- Part C: Scope vs REQUIREMENTS.md — process concern ✅ (but only "has scope crept?", not "does code match architecture?")
- Part D: Deferred work — process concern ✅
- Part E: Blast radius — process concern ✅
- Part F: Decision reversals — process concern ✅
- Part G: Dependency health — external dependencies ✅

**Missing: Part H — Architecture And Requirements Alignment.** No check asks:
- "Does implemented code still match ARCHITECTURE.md contracts?"
- "Have any new contracts been added that are not documented?"
- "Does the implemented auth model match ARCHITECTURE.md?"
- "Are any P0 requirements in REQUIREMENTS.md now impossible given current implementation?"

### 10.7 Evidence: PROGRAMBUILD_CANONICAL.md Defines Authorities But Not Usage Timing

PROGRAMBUILD_CANONICAL.md correctly identifies ARCHITECTURE.md as the authority for "system boundaries, contracts, data model, auth model" and REQUIREMENTS.md as the authority for "requirements and scope."

But it also says: "validated code and tested tests MUST outrank any planning document." This creates an asymmetry: process docs are authority-first (read before edit), but product docs are code-first (code outranks docs). Without an explicit re-read rule, this means:

- A developer makes an architecture decision while coding.
- The code diverges from ARCHITECTURE.md.
- PROGRAMBUILD_CANONICAL.md says code wins.
- ARCHITECTURE.md silently becomes stale.
- No one is told to update it.

This is the exact drift failure mode that JIT was designed to prevent — but it only prevents it for process docs.

### 10.8 The Fundamental Design Gap

PROGRAMSTART treats JIT as a **process governance tool**, not a **product development tool**.

| Concern | JIT applies? | Evidence |
|---|---|---|
| Is the workflow state correct? | Yes | `programstart guide`, `programstart drift`, `programstart validate` |
| Are stage gates met before transition? | Yes | Challenge Gate, Cross-Stage Validation |
| Are process docs in sync with each other? | Yes | Sync rules, drift checker |
| Are process docs in sync with automation? | Yes | `automation_gate_jit_alignment` sync rule |
| Does implementation code match ARCHITECTURE.md? | **No** | No prompt, instruction, sync rule, or gate checks this |
| Does implementation code match REQUIREMENTS.md? | **No** | No prompt, instruction, sync rule, or gate checks this |
| Does the AI re-read product docs before coding? | **No** | No instruction tells it to |

**JIT governs the map. It does not govern the territory.**

### 10.9 Impact On Real-World Usage

When we used PROGRAMBUILD to build a product (e.g., `whats` app), what actually happened:

- The AI was told to follow the stage sequence — this worked.
- The AI was told to run `programstart guide` — this returned process docs, not product docs.
- During implementation, the AI relied on **conversation memory** for architecture decisions, not on re-reading ARCHITECTURE.md.
- If a conversation context window was exhausted or the session restarted, the AI had no prompt telling it to re-read the product's own source-of-truth docs before resuming coding.
- The JIT protocol's rule "never assert from memory" was enforced for process docs but ignored for the product docs that actually mattered during coding.

This is where JIT should be surfaced most aggressively, and it is currently not surfaced at all.

### 10.10 Recommended Fixes (Scope Assessment For Phasing)

These fixes address the product-JIT gap. They are categorized by complexity and impact.

#### Fix 1: Add product docs to `implementation_loop` workflow_guidance (Low complexity, High impact)

Change `config/process-registry.json` `workflow_guidance.programbuild.implementation_loop.files` to include:

- `PROGRAMBUILD/ARCHITECTURE.md`
- `PROGRAMBUILD/REQUIREMENTS.md`
- `PROGRAMBUILD/USER_FLOWS.md`

This alone fixes the `programstart guide` gap — the most common JIT entry point will now return the product docs that matter.

#### Fix 2: Add product-JIT rule to `source-of-truth.instructions.md` (Low complexity, High impact)

Add to the authority table:

| Concern | Authority file |
|---|---|
| Product architecture | `PROGRAMBUILD/ARCHITECTURE.md` |
| Product requirements | `PROGRAMBUILD/REQUIREMENTS.md` |
| User journey behavior | `PROGRAMBUILD/USER_FLOWS.md` |

Add a new rule: "Before writing implementation code, re-read the applicable sections of ARCHITECTURE.md and REQUIREMENTS.md. Do not implement from memory."

#### Fix 3: Add product-JIT guidance to `copilot-instructions.md` (Low complexity, High impact)

Add to Workflow Expectations:

- "Before writing code for a feature, re-read the applicable ARCHITECTURE.md contracts and the REQUIREMENTS.md entry."
- "If implementation design contradicts ARCHITECTURE.md, update ARCHITECTURE.md first. Do not ship code that contradicts authority docs."
- "If you discover a new contract or endpoint not in ARCHITECTURE.md, record the change in DECISION_LOG.md and update ARCHITECTURE.md in the same commit."

#### Fix 4: Add Part H to Challenge Gate (Medium complexity, High impact)

Add a "Part H — Architecture And Requirements Alignment" check to `PROGRAMBUILD_CHALLENGE_GATE.md` for the mid-implementation gate:

- Have any ARCHITECTURE.md contracts been changed without update?
- Have any new contracts been added without documentation?
- Does the implemented auth model still match ARCHITECTURE.md?
- Are any P0 requirements now impossible given current implementation?
- Has any planned USER_FLOWS.md flow been silently dropped or changed?

#### Fix 5: Add product-JIT prompt (Medium complexity, Medium impact)

Create `.github/prompts/product-jit-check.prompt.md` that tells the AI:

1. Re-read ARCHITECTURE.md contracts relevant to the current task.
2. Re-read the REQUIREMENTS.md entry for the current feature.
3. Check DECISION_LOG.md for any decisions affecting this feature.
4. Confirm alignment before proceeding.

#### Fix 6: Update `programstart-stage-guide.prompt.md` (Low complexity, Medium impact)

Add a task: "For the implementation_loop stage, also list the upstream product docs (ARCHITECTURE.md, REQUIREMENTS.md, USER_FLOWS.md) and remind the operator that these are living authorities during coding, not just stage inputs."

#### Fix 7: Add implementation-alignment sync rules (Medium complexity, Medium impact)

Add sync rule(s) to `config/process-registry.json` that bind ARCHITECTURE.md and REQUIREMENTS.md as authorities during implementation. While drift cannot check code files, it can check that when ARCHITECTURE.md is changed, DECISION_LOG.md is also updated in the same commit — ensuring architecture changes are at least tracked.

### 10.11 Phasing Assessment

| Fix | Phase | Rationale |
|---|---|---|
| Fix 1: Add product docs to workflow_guidance | Phase 1 | One JSON change, immediate guide impact |
| Fix 2: Add product-JIT to source-of-truth.instructions.md | Phase 1 | Directly extends the existing JIT protocol |
| Fix 3: Add product-JIT to copilot-instructions.md | Phase 1 | Aligns AI behavior with the JIT principle |
| Fix 4: Add Part H to Challenge Gate | Phase 2 | Requires careful design of the check questions |
| Fix 5: Add product-JIT prompt | Phase 2 | Depends on Fixes 1–3 being in place first |
| Fix 6: Update stage-guide prompt | Phase 1 | Small prompt edit, immediate behavior change |
| Fix 7: Add implementation-alignment sync rules | Phase 2 | Requires design for code-vs-doc drift detection |

Fixes 1, 2, 3, and 6 are low-complexity, high-impact, and should be included in Phase 1. They change what the system tells operators/AI to read, without requiring new tooling.

---

## 11. Revised Go/No-Go Assessment (Post Prompt Audit)

### What Changed Since Section 9

Section 9 gave a GO for Phase 1 based on the automation and smoke safety audit. Section 10 now reveals a deeper structural problem: **JIT is not surfaced in prompts for product-level source-of-truth docs during implementation.** This is not a Phase 1 blocker per se — Phase 1 is about automation gates and smoke safety. But it changes the overall scope picture.

### Updated Prerequisites Checklist

| Prerequisite | Status |
|---|---|
| Source-of-truth files are in sync | PASS |
| Drift check passes | PASS |
| improvegameplan.md reflects actual codebase state | PASS — corrected in Section 8, extended in Section 10 |
| JIT protocol is understood end-to-end | PASS — but now reveals process-only enforcement |
| Product-JIT gap is documented | PASS — Section 10 provides full evidence chain |
| Phase 1 scope is actionable with product-JIT fixes | PASS — Fixes 1, 2, 3, 6 are low-complexity |
| No structural blockers | PASS |

### Scope Decision Required

Phase 1 must now include the product-JIT fixes (Section 10 Fixes 1, 2, 3, 6) alongside the automation fixes. The product-JIT fixes are low-complexity edits to existing files (one JSON change, two instruction file edits, one prompt edit). They do not add new infrastructure. Excluding them would mean shipping an "improved JIT" that still has the same fundamental gap — JIT governs the map but not the territory.

### Updated Phase 1 Delivery Order

1. Record the smoke safety policy decision in `PROGRAMBUILD/DECISION_LOG.md`.
2. Add product docs to `implementation_loop` workflow_guidance in `config/process-registry.json` (Fix 1).
3. Add product-JIT rules to `source-of-truth.instructions.md` (Fix 2).
4. Add product-JIT rules to `copilot-instructions.md` (Fix 3).
5. Update `programstart-stage-guide.prompt.md` with product-doc reminder for implementation (Fix 6).
6. Split `programstart_dashboard_smoke.py` (read-only vs. mutating).
7. Wire `drift` into nox `validate` session.
8. Add VS Code tasks (Drift Check, JIT Check, Safe Gate).
9. Update `programstart_cli_smoke.py` with drift + guide USERJOURNEY.
10. Review and update `QUICKSTART.md` and `README.md` (required by sync rule).
11. Update `PROGRAMBUILD_CHANGELOG.md`.
12. Run `programstart validate --check all` and `programstart drift` — both must pass.

### Risk Summary

| Risk | Severity | Mitigation |
|---|---|---|
| Phase 1 scope expanded by 4 items | Low | Fixes 1–3, 6 are each single-file edits |
| Product-JIT instructions may cause AI over-reading | Low | Instructions say "applicable sections," not "entire doc" |
| Process-registry version changes trigger sync rule | Expected | Docs update is already in delivery order |
| Challenge Gate Part H deferred to Phase 2 | Acceptable | Phase 1 fixes the guidance gap; Phase 2 adds enforcement |

### Verdict

**GO** — Phase 1 implementation may proceed with the expanded scope.

Conditions:

1. Phase 1 MUST include product-JIT Fixes 1, 2, 3, and 6 (Section 10.10) alongside the automation fixes.
2. Follow the updated delivery order in Section 11.
3. Use the prioritized core subset from Section 8 Finding J for the automation items.
4. Defer Challenge Gate Part H (Fix 4), product-JIT prompt (Fix 5), and implementation-alignment sync rules (Fix 7) to Phase 2.
5. Defer `programstart_repo_clean_check.py`, `serve.py` read-only guard, and `gate-safe` nox session to Phase 1.5.
6. Record the smoke safety policy decision in DECISION_LOG before any code changes.
7. Run `programstart validate --check all` and `programstart drift` after each delivery step.

---

## 12. Complete Protocol Inventory (Derived From Source-of-Truth Files)

This section maps every protocol defined in the repository's authority documents, where each is enforced, and where enforcement gaps exist. Every claim below is derived from a specific source-of-truth file, cited inline.

### 12.1 Protocol Map

The following protocols are defined in the repository. Each entry cites the canonical authority file.

| # | Protocol | Authority File | Purpose |
|---|---|---|---|
| P1 | JIT Source-of-Truth Loading | `.github/instructions/source-of-truth.instructions.md` | Prevent context drift by re-reading docs before changes |
| P2 | Challenge Gate | `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` | Prevent kill criteria staleness, scope creep, assumption rot at stage boundaries |
| P3 | Cross-Stage Validation | `PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md` | Catch contradictions between stage outputs |
| P4 | Canonical-Before-Dependent | `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` Section 4, `source-of-truth.instructions.md` Step 3 | Authority files updated before dependents |
| P5 | Conflict Resolution | `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` Section 4 | Hierarchy: code → CANONICAL → authority map → other |
| P6 | Conventional Commits | `.github/instructions/conventional-commits.instructions.md` | Structured commit messages |
| P7 | ADR Decision Recording | `.github/copilot-instructions.md`, `PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md` | Material decisions recorded as MADR records |
| P8 | Re-Entry After Pause | `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` Re-Entry Protocol | Verify all prior outputs still valid after >4 weeks |
| P9 | Sync Rule Enforcement | `config/process-registry.json` `sync_rules` | Machine-readable binding between authority and dependent files |
| P10 | USERJOURNEY Authority Chain | `.github/instructions/userjourney.instructions.md` | Route/state/legal/consent authority before dependents |
| P11 | Metadata Block Preservation | `.github/copilot-instructions.md` Editing Rules | All planning docs keep metadata blocks |
| P12 | Repository Boundary | `.github/copilot-instructions.md` Editing Rules | Never cross into another repo without explicit consent |

### 12.2 Enforcement Surface For Each Protocol

| Protocol | Where Enforced | Where NOT Enforced (Gap) |
|---|---|---|
| **P1 JIT** | `.github/instructions/source-of-truth.instructions.md` (AI sessions), `.github/copilot-instructions.md` (AI sessions), CI `process-guardrails.yml` (drift step) | Nox `validate` (no drift call — Gap B), `programstart next` (no drift — Gap A), CLI smoke (no drift — Gap C), VS Code tasks (no drift task), implementation stage guidance (no product docs — Section 10) |
| **P2 Challenge Gate** | `PROGRAMBUILD_GAMEPLAN.md` (prose at each stage), `PROGRAMBUILD_CHALLENGE_GATE.md` (checklist), `programstart-stage-transition.prompt.md` (AI prompt) | No automation enforcing it — entirely honor-system. No nox session runs it. No VS Code task surfaces it. No script validates that it was actually run. `programstart advance` does not check for a Challenge Gate log entry. |
| **P3 Cross-Stage Validation** | `PROGRAMBUILD_GAMEPLAN.md` (inline checklists at each stage), `programstart-cross-stage-validation.prompt.md` (AI prompt) | Same as P2 — entirely prose-based. No automation verifies cross-stage checks were completed. |
| **P4 Canonical-Before-Dependent** | `source-of-truth.instructions.md` Step 3 (AI sessions), `config/process-registry.json` sync_rules `require_authority_when_dependents_change` (drift checker), `copilot-instructions.md` (AI sessions) | Drift only checks uncommitted changes. Historical misorderings are not detected. |
| **P5 Conflict Resolution** | `PROGRAMBUILD_CANONICAL.md` Section 4 (prose), `copilot-instructions.md` (AI sessions) | Entirely instruction-based. No automation detects conflicts between two docs. |
| **P6 Conventional Commits** | `.github/instructions/conventional-commits.instructions.md` (AI sessions), `scripts/check_commit_msg.py` (pre-commit hook), `.gitlint` (pre-commit), `.pre-commit-config.yaml` (pre-commit hook), sync rule `commit_enforcement_alignment` | Well-enforced. Pre-commit hook + gitlint + AI instructions + sync rule. Minor gap: pre-commit can be bypassed with `--no-verify`. |
| **P7 ADR Recording** | `copilot-instructions.md` (AI sessions), `PROGRAMBUILD_ADR_TEMPLATE.md` (template), `docs/decisions/README.md` (index), sync rule `decisions_adr_template` | Instruction-based. No automation checks whether a material decision exists without an ADR. |
| **P8 Re-Entry** | `PROGRAMBUILD_CHALLENGE_GATE.md` Re-Entry Protocol (prose) | Entirely prose. No automation detects inactivity or suggests re-entry. No timestamp comparison against last state change. |
| **P9 Sync Rules** | `config/process-registry.json` (machine-readable), `scripts/programstart_drift_check.py` (automation), CI `process-guardrails.yml` (drift step) | Only checks uncommitted/PR-diff files. Nox `validate` doesn't run drift locally. Design limitation documented in Section 8.4. |
| **P10 USERJOURNEY Authority** | `.github/instructions/userjourney.instructions.md` (AI sessions), sync rules `userjourney_*` (drift checker) | Same drift limitation as P9. Further gap: `guide --system userjourney` not in CLI smoke (Gap C). |
| **P11 Metadata Blocks** | `copilot-instructions.md` (AI sessions), `scripts/programstart_validate.py` metadata checks | Reasonably well-enforced by validate. |
| **P12 Repository Boundary** | `copilot-instructions.md` Editing Rules (AI sessions), `scripts/programstart_bootstrap.py` `ensure_external_project_repo()` (code guard) | Bootstrap script enforces this for generated projects. AI instructions enforce for copilot sessions. No enforcement for manual operations. |

### 12.3 Enforcement Quality Summary

| Enforcement Level | Protocols | Count |
|---|---|---|
| **Well-enforced** (automation + instructions + sync rules) | P6 Conventional Commits, P11 Metadata Blocks | 2 |
| **Partially enforced** (drift checker covers some cases) | P4 Canonical-Before-Dependent, P9 Sync Rules, P10 USERJOURNEY Authority | 3 |
| **Instruction-only** (AI prompt/instruction, no automation) | P1 JIT (partially), P5 Conflict Resolution, P7 ADR Recording, P12 Repository Boundary | 4 |
| **Not enforced** (prose in docs, no instruction or automation) | P2 Challenge Gate, P3 Cross-Stage Validation, P8 Re-Entry | 3 |

### 12.4 Safeguards Currently In Place

These safeguards exist in the codebase. Source file cited for each.

**Automation safeguards:**

| Safeguard | Source File | What It Prevents |
|---|---|---|
| `programstart drift` | `scripts/programstart_drift_check.py` | Authority/dependent desync in uncommitted changes |
| `programstart validate --check all` | `scripts/programstart_validate.py` | Missing files, bad metadata, schema violations, broken references |
| `programstart validate --check authority-sync` | Same | Metadata owner/date mismatches across authority files |
| `programstart validate --check workflow-state` | Same | State file schema violations |
| `programstart validate --check planning-references` | Same | Broken cross-references between planning docs |
| `programstart validate --check bootstrap-assets` | Same | Missing bootstrapped assets |
| Pre-commit hooks | `.pre-commit-config.yaml` | Commit format, secrets, JSON/YAML schema, linting |
| CI matrix (Ubuntu + Windows) | `.github/workflows/process-guardrails.yml` | Cross-platform regressions |
| `ensure_external_project_repo()` | `scripts/programstart_bootstrap.py` line ~147 | Generated projects created inside template repo |
| `programstart prompt-eval --json` | `scripts/programstart_prompt_eval.py` | Prompt quality regressions |
| `bandit -r scripts/` | Nox `security` session | Security vulnerabilities in scripts |
| `pip-audit` | Nox `security` session | Vulnerable dependencies |
| JSON schema validation | Nox `lint` session (check-jsonschema) | Invalid STATE.json or process-registry.json |

**Instruction safeguards (AI-session only):**

| Safeguard | Source File | What It Prevents |
|---|---|---|
| "Never assert from memory — re-read" | `source-of-truth.instructions.md` | Stale context in AI sessions |
| "Canonical before dependent" | `source-of-truth.instructions.md` Step 3 | Edit ordering violations |
| "Do not invent behavior not in authority docs" | `source-of-truth.instructions.md`, `copilot-instructions.md` | Phantom requirements |
| "Do not cross repo boundary" | `copilot-instructions.md` Editing Rules | Accidental cross-repo edits |
| RFC 2119 keywords | Multiple instruction files | Ambiguity in MUST/SHOULD language |

**Missing safeguards (identified by this review):**

| Missing Safeguard | What It Would Prevent | Protocol Affected |
|---|---|---|
| `programstart advance` requiring Challenge Gate log entry | Skipping stage gates | P2 |
| Drift in nox `validate` | Local-vs-CI enforcement divergence | P1, P9 |
| Product-doc JIT during implementation | Architecture/requirements drift during coding | P1 |
| Staleness detection (>4 weeks since last state change) | Resuming without re-entry protocol | P8 |
| ADR existence check for material decisions | Decisions without formal records | P7 |
| Cross-stage contradiction detection automation | Undetected output conflicts | P3 |

---

## 13. Code Examples For Phase 1 Changes

All code examples below target the exact files and line ranges read during this review. They are derived from the current codebase state, not invented from memory.

### 13.1 Fix 1: Add Product Docs To `implementation_loop` workflow_guidance

**Source file:** `config/process-registry.json` — `workflow_guidance.programbuild.implementation_loop` (currently at ~line 752)

**Current state** (from `config/process-registry.json`):
```json
"implementation_loop": {
    "description": "Build, test, and iterate — the main development cycle.",
    ...
    "files": [
        "PROGRAMBUILD/TEST_STRATEGY.md",
        "PROGRAMBUILD/DECISION_LOG.md",
        "PROGRAMBUILD/PROGRAMBUILD_CHECKLIST.md",
        "PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md",
        "PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md"
    ],
```

**Proposed change:**
```json
"implementation_loop": {
    "description": "Build, test, and iterate — the main development cycle.",
    ...
    "files": [
        "PROGRAMBUILD/ARCHITECTURE.md",
        "PROGRAMBUILD/REQUIREMENTS.md",
        "PROGRAMBUILD/USER_FLOWS.md",
        "PROGRAMBUILD/TEST_STRATEGY.md",
        "PROGRAMBUILD/DECISION_LOG.md",
        "PROGRAMBUILD/PROGRAMBUILD_CHECKLIST.md",
        "PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md",
        "PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md"
    ],
```

**Effect:** `programstart guide --system programbuild` during implementation_loop will now return the three product authority docs (ARCHITECTURE.md, REQUIREMENTS.md, USER_FLOWS.md) alongside the existing process docs. This is the single most impactful change — it makes the JIT entry point product-aware.

**Validation:** After this change, running `programstart guide --system programbuild --stage implementation_loop` must list all 8 files.

### 13.2 Fix 2: Add Product-JIT Rules To `source-of-truth.instructions.md`

**Source file:** `.github/instructions/source-of-truth.instructions.md`

**Current authority table** (from the file):
```markdown
| Concern | Authority file |
|---|---|
| Stage order and gates | `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` |
| Which files are control files | `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md` |
| USERJOURNEY execution order | `USERJOURNEY/DELIVERY_GAMEPLAN.md` |
| Route, state, activation rules | `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md` |
| Legal and consent behaviour | `USERJOURNEY/LEGAL_AND_CONSENT.md` |
| Decisions and reversals | `USERJOURNEY/DECISION_LOG.md` |
| Registry of all rules | `config/process-registry.json` |
```

**Proposed addition to the authority table:**
```markdown
| Concern | Authority file |
|---|---|
| Stage order and gates | `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` |
| Which files are control files | `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md` |
| Product architecture and contracts | `PROGRAMBUILD/ARCHITECTURE.md` |
| Product requirements and scope | `PROGRAMBUILD/REQUIREMENTS.md` |
| Product user flows | `PROGRAMBUILD/USER_FLOWS.md` |
| USERJOURNEY execution order | `USERJOURNEY/DELIVERY_GAMEPLAN.md` |
| Route, state, activation rules | `USERJOURNEY/ROUTE_AND_STATE_FREEZE.md` |
| Legal and consent behaviour | `USERJOURNEY/LEGAL_AND_CONSENT.md` |
| Decisions and reversals | `USERJOURNEY/DECISION_LOG.md` |
| Registry of all rules | `config/process-registry.json` |
```

**Proposed addition — new section after "What to never do":**
```markdown
## Product-level JIT during implementation

The protocol above applies to process/planning tasks. During active implementation (Stage 7),
you MUST also apply JIT to *product* authority docs:

- Before writing code for a feature, re-read the applicable contracts in `PROGRAMBUILD/ARCHITECTURE.md`.
- Before writing code for a feature, re-read the relevant requirement in `PROGRAMBUILD/REQUIREMENTS.md`.
- You MUST NOT implement from memory. Re-read the actual doc.
- If implementation design contradicts `ARCHITECTURE.md`, update `ARCHITECTURE.md` first (canonical-before-dependent).
- If you discover a new contract, endpoint, or auth rule not in `ARCHITECTURE.md`, record it in `DECISION_LOG.md` and update `ARCHITECTURE.md` in the same commit.
- Every 3–5 features, re-read the full contracts section of `ARCHITECTURE.md` to catch silent drift.
```

**Validation:** The authority table now has 10 rows (was 7). The new section gives explicit implementation-time guidance.

### 13.3 Fix 3: Add Product-JIT Rules To `copilot-instructions.md`

**Source file:** `.github/copilot-instructions.md`

**Current "Workflow Expectations" section** (from the file):
```markdown
## Workflow Expectations

- Read `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` and `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md` before changing PROGRAMBUILD control behavior.
- Read `USERJOURNEY/DELIVERY_GAMEPLAN.md` before changing USERJOURNEY execution order or synchronization rules.
- Update canonical owner files before dependent files when a concern changes.
- Do not invent legal, consent, route, or activation behavior in downstream docs without updating the authority docs first.
- Treat `first_value_achieved` as the canonical USERJOURNEY activation event unless the source-of-truth docs explicitly change.
```

**Proposed addition to end of Workflow Expectations:**
```markdown
- During implementation (Stage 7+), re-read the applicable contracts in `PROGRAMBUILD/ARCHITECTURE.md` and the relevant requirement in `PROGRAMBUILD/REQUIREMENTS.md` before writing feature code. Do not implement from conversation memory.
- If implementation design contradicts `ARCHITECTURE.md`, update `ARCHITECTURE.md` first. Do not ship code that contradicts an authority doc.
- If you add a new contract, endpoint, or auth rule not documented in `ARCHITECTURE.md`, record it in `DECISION_LOG.md` and update `ARCHITECTURE.md` in the same commit.
```

**Validation:** These three new lines extend the existing instruction pattern. They do not restructure the file.

### 13.4 Fix 6: Update `programstart-stage-guide.prompt.md`

**Source file:** `.github/prompts/programstart-stage-guide.prompt.md`

**Current full content:**
```markdown
---
description: "Show the correct files, scripts, and prompts for a specific PROGRAMSTART step."
name: "PROGRAMSTART Stage Guide"
argument-hint: "Use kickoff, a PROGRAMBUILD stage name, or a USERJOURNEY phase key"
agent: "agent"
---
Determine the correct assets to use for a specific PROGRAMSTART step.

Tasks:

1. Use `scripts/programstart_step_guide.py` with the requested kickoff, PROGRAMBUILD stage, or USERJOURNEY phase.
2. Return the authoritative files to open first.
3. Return the scripts to run first.
4. Return the prompts that should be used instead of relying on chat memory.
5. If the requested step is missing from the registry, say so explicitly instead of inventing a sequence.

Prefer the registry-backed guide output over ad hoc step ordering.
```

**Proposed replacement:**
```markdown
---
description: "Show the correct files, scripts, and prompts for a specific PROGRAMSTART step."
name: "PROGRAMSTART Stage Guide"
argument-hint: "Use kickoff, a PROGRAMBUILD stage name, or a USERJOURNEY phase key"
agent: "agent"
---
Determine the correct assets to use for a specific PROGRAMSTART step.

Tasks:

1. Use `scripts/programstart_step_guide.py` with the requested kickoff, PROGRAMBUILD stage, or USERJOURNEY phase.
2. Return the authoritative files to open first.
3. Return the scripts to run first.
4. Return the prompts that should be used instead of relying on chat memory.
5. If the requested step is missing from the registry, say so explicitly instead of inventing a sequence.
6. For the implementation_loop stage: remind the operator that ARCHITECTURE.md, REQUIREMENTS.md, and USER_FLOWS.md are living authorities during coding. They must be re-read before each feature, not just at stage entry. If the guide output includes these files, call them out as "re-read before each feature" rather than "read once at stage start."

Prefer the registry-backed guide output over ad hoc step ordering.
```

### 13.5 Wire `drift` Into Nox `validate` Session

**Source file:** `noxfile.py` lines 103–116

**Current state:**
```python
@nox.session(reuse_venv=True)
def validate(session: nox.Session) -> None:
    install_dev(session)
    session.run("programstart", "validate", "--check", "all")
    session.run("programstart", "prompt-eval", "--json")
    session.run("programstart", "validate", "--check", "authority-sync")
    session.run("programstart", "validate", "--check", "planning-references")
    session.run("programstart", "validate", "--check", "workflow-state")
    session.run("python", "scripts/programstart_cli_smoke.py", "--workspace", str(ROOT))
    session.run("programstart", "guide", "--system", "programbuild")
    session.run("programstart", "guide", "--system", "userjourney")
    session.run("programstart", "state", "show")
```

**Proposed change:**
```python
@nox.session(reuse_venv=True)
def validate(session: nox.Session) -> None:
    install_dev(session)
    session.run("programstart", "drift")
    session.run("programstart", "validate", "--check", "all")
    session.run("programstart", "prompt-eval", "--json")
    session.run("programstart", "validate", "--check", "authority-sync")
    session.run("programstart", "validate", "--check", "planning-references")
    session.run("programstart", "validate", "--check", "workflow-state")
    session.run("python", "scripts/programstart_cli_smoke.py", "--workspace", str(ROOT))
    session.run("programstart", "guide", "--system", "programbuild")
    session.run("programstart", "guide", "--system", "userjourney")
    session.run("programstart", "state", "show")
    session.run("programstart", "drift")
```

**Effect:** Drift runs first (baseline check per JIT Step 2) and last (post-validation verification per JIT Step 4). This closes Gap B — nox `validate` now matches CI enforcement.

### 13.6 Add `drift` To `run_next()` in CLI

**Source file:** `scripts/programstart_cli.py` lines 86–96

**Current state:**
```python
def run_next(arguments: list[str]) -> int:
    if arguments:
        raise SystemExit("'next' does not accept additional arguments")

    print()
    print("  PROGRAMSTART - What To Do Next")
    print()

    steps = [
        run_passthrough(programstart_status.main, "programstart status", []),
        run_passthrough(programstart_step_guide.main, "programstart guide", ["--system", "programbuild"]),
        run_passthrough(programstart_step_guide.main, "programstart guide", ["--system", "userjourney"]),
    ]
    return next((code for code in steps if code != 0), 0)
```

**Proposed change:**
```python
def run_next(arguments: list[str]) -> int:
    if arguments:
        raise SystemExit("'next' does not accept additional arguments")

    print()
    print("  PROGRAMSTART - What To Do Next")
    print()

    steps = [
        run_passthrough(programstart_status.main, "programstart status", []),
        run_passthrough(programstart_step_guide.main, "programstart guide", ["--system", "programbuild"]),
        run_passthrough(programstart_step_guide.main, "programstart guide", ["--system", "userjourney"]),
        run_passthrough(programstart_drift_check.main, "programstart drift", []),
    ]
    return next((code for code in steps if code != 0), 0)
```

**Effect:** The default build task now runs the full JIT sequence: status → guide (both systems) → drift. This closes Gap A — the most common operator entry point becomes JIT-complete.

**Prerequisite:** `programstart_drift_check` must be imported at the top of `programstart_cli.py` alongside the other module imports.

### 13.7 Update `programstart_cli_smoke.py`

**Source file:** `scripts/programstart_cli_smoke.py` lines 33–41

**Current checks list:**
```python
    checks = [
        ["help"],
        ["status"],
        ["prompt-eval", "--json"],
        ["clean", "--dry-run"],
        ["validate", "--check", "workflow-state"],
        ["guide", "--system", "programbuild"],
        ["state", "show"],
        ["next"],
    ]
```

**Proposed change:**
```python
    checks = [
        ["help"],
        ["status"],
        ["prompt-eval", "--json"],
        ["clean", "--dry-run"],
        ["validate", "--check", "workflow-state"],
        ["guide", "--system", "programbuild"],
        ["guide", "--system", "userjourney"],
        ["drift"],
        ["state", "show"],
        ["next"],
    ]
```

**Effect:** CLI smoke now exercises `guide --system userjourney` and `drift`. This closes Gap C.

### 13.8 New VS Code Tasks

**Source file:** `.vscode/tasks.json`

**Proposed new tasks to add** (insert before the closing `]` of the tasks array):

```json
    {
      "label": "PROGRAMSTART: Drift Check",
      "type": "shell",
      "command": "uv",
      "args": ["run", "programstart", "drift"],
      "presentation": { "reveal": "always", "panel": "shared", "clear": true },
      "group": "test",
      "problemMatcher": []
    },
    {
      "label": "PROGRAMSTART: JIT Check",
      "type": "shell",
      "command": "uv",
      "args": ["run", "programstart", "guide", "--system", "programbuild"],
      "presentation": { "reveal": "always", "panel": "shared", "clear": true },
      "dependsOn": ["PROGRAMSTART: Drift Check"],
      "dependsOrder": "sequence"
    },
    {
      "label": "PROGRAMSTART: Safe Gate",
      "type": "shell",
      "command": "uv",
      "args": ["run", "nox", "-s", "lint", "typecheck", "tests", "validate", "docs"],
      "presentation": { "reveal": "always", "panel": "shared", "clear": true, "focus": true },
      "group": "test",
      "problemMatcher": []
    }
```

**Effect:** Three new tasks surfacing JIT in the editor. `JIT Check` depends on `Drift Check` so they always run in the correct sequence. `Safe Gate` runs the core sessions without the mutating smoke.

### 13.9 Split Dashboard Smoke (Read-Only Script)

**Source file:** `scripts/programstart_dashboard_smoke.py`

**Concept:** Split the existing script into two files. The read-only version exercises only GET endpoints. The mutation version (for use against temp workspaces) exercises POST endpoints.

**Proposed new file `scripts/programstart_dashboard_smoke_readonly.py`** (sketch):
```python
"""Read-only dashboard smoke — safe to run against the root workspace at any time."""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
SERVER = ROOT / "scripts" / "programstart_serve.py"


def choose_port(port: int) -> int:
    if port > 0:
        return port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request_json(base_url: str, path: str) -> dict[str, Any]:
    with urllib.request.urlopen(f"{base_url}{path}", timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def request_text(base_url: str, path: str) -> str:
    with urllib.request.urlopen(f"{base_url}{path}", timeout=10) as response:
        return response.read().decode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only dashboard smoke test.")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--startup-timeout", type=float, default=12.0)
    args = parser.parse_args()

    port = choose_port(args.port)
    base_url = f"http://127.0.0.1:{port}"
    env = {**os.environ, "NO_COLOR": "1"}
    process = subprocess.Popen(
        [PYTHON, str(SERVER), "--port", str(port), "--no-open"],
        cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )

    checks: list[tuple[str, bool, str]] = []
    try:
        # ... wait_for_server logic (reuse from existing script) ...

        # Only GET requests — no POST, no mutations
        state = request_json(base_url, "/api/state")
        checks.append(("GET /api/state", "active" in str(state), "state loaded"))

        html = request_text(base_url, "/")
        for marker in ["Recent Projects", "Sync And Drift", "uj-slice-status", "modal-date"]:
            checks.append((f"GET / marker {marker}", marker in html, "found" if marker in html else "missing"))

        # Verify guide and drift endpoints (read-only API)
        guide = request_json(base_url, "/api/guide?system=programbuild")
        checks.append(("GET /api/guide", bool(guide), "guide loaded"))

    finally:
        process.terminate()
        process.wait(timeout=5)

    failures = sum(1 for _, ok, _ in checks if not ok)
    for name, ok, detail in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Effect:** Root-workspace smoke is guaranteed read-only. The existing `programstart_dashboard_smoke.py` continues to be used only in isolated temp workspaces (nox `smoke` session bootstraps a workspace first).

### 13.10 Add `.tmp_factory_smoke` To Nox `clean`

**Source file:** `noxfile.py` lines 260–275

**Current clean targets list:**
```python
    targets = [
        ".coverage",
        "htmlcov",
        ".pytest_cache",
        "dist",
        "build",
        "site",
        ".nox",
        ".tmp_nox_bootstrap",
        ".tmp_nox_create",
        ".tmp_dist_smoke",
    ]
```

**Proposed change:**
```python
    targets = [
        ".coverage",
        "htmlcov",
        ".pytest_cache",
        "dist",
        "build",
        "site",
        ".nox",
        ".tmp_nox_bootstrap",
        ".tmp_nox_create",
        ".tmp_nox_factory_smoke",
        ".tmp_dist_smoke",
        ".tmp_factory_smoke",
    ]
```

**Effect:** Both nox-path and direct-path factory smoke directories are cleaned.

---

## 14. Final Go/No-Go Assessment (Post Full Protocol Review)

### What Changed Since Section 11

Section 11 gave a GO with expanded scope for product-JIT fixes. This section adds:
- A complete protocol inventory (12 protocols mapped)
- Enforcement surface analysis for every protocol
- Code examples for every Phase 1 change
- Discovery that 3 protocols (P2 Challenge Gate, P3 Cross-Stage Validation, P8 Re-Entry) have zero enforcement — not even AI instructions in some cases

### Are We Missing Any Protocols?

No. The 12 protocols in Section 12.1 are exhaustively derived from:
- `PROGRAMBUILD_CANONICAL.md` (rules 1–7, authority map, conflict resolution)
- `PROGRAMBUILD_CHALLENGE_GATE.md` (parts A–G, re-entry protocol)
- `PROGRAMBUILD_GAMEPLAN.md` (cross-stage validation at every stage)
- `source-of-truth.instructions.md` (JIT steps 1–4)
- `copilot-instructions.md` (workflow expectations, editing rules, source-of-truth protocol)
- `conventional-commits.instructions.md` (commit format)
- `userjourney.instructions.md` (authority chain)
- `config/process-registry.json` (sync_rules, 13 rules)

### What We Are Not Fixing In Phase 1

| Protocol | Status | Phase |
|---|---|---|
| P2 Challenge Gate enforcement | No automation — entirely prose-based | Phase 2+ (requires `programstart advance` to check gate log) |
| P3 Cross-Stage Validation enforcement | No automation — entirely prose-based | Phase 2+ (requires contradiction detection tooling) |
| P5 Conflict Resolution enforcement | Instruction-only — no automation | Not planned (acceptable as instruction-only) |
| P7 ADR existence checking | Instruction-only — no automation | Phase 2+ (requires decision-to-ADR mapping) |
| P8 Re-Entry staleness detection | No automation — no timestamp comparison | Phase 3+ (requires state timestamp analysis) |

These are documented as known gaps. Phase 1 focuses on the highest-leverage fixes: making JIT product-aware and making automation surfaces match their protocols.

### Updated Prerequisites Checklist

| Prerequisite | Status | Evidence |
|---|---|---|
| Source-of-truth files in sync | PASS | `programstart validate --check all` and `programstart drift` both pass |
| All protocols mapped | PASS | 12 protocols in Section 12.1, all cited to authority files |
| Enforcement gaps documented | PASS | Section 12.2 maps every gap per protocol |
| Code examples ready | PASS | Section 13 has 10 code examples with file paths and line numbers |
| Product-JIT gap documented with evidence | PASS | Section 10 provides full evidence chain |
| Phase 1 scope is concrete and executable | PASS | Every change has a code example |
| No unresolved blockers | PASS | Section 6.3 blockers all resolved or accepted |

### Final Verdict

**GO** — Phase 1 implementation may proceed.

Conditions (updated from Section 11 with code examples):

1. Follow the delivery order in Section 11: DECISION_LOG entry → Fix 1 (registry) → Fix 2 (source-of-truth instructions) → Fix 3 (copilot instructions) → Fix 6 (stage-guide prompt) → smoke split → nox drift wiring → VS Code tasks → CLI smoke → docs → changelog → validate + drift.
2. Use the exact code patterns from Section 13. Each example cites the source file and current line range.
3. After each delivery step, run `programstart validate --check all` and `programstart drift`.
4. Defer P2/P3/P8 enforcement automation to Phase 2+.
5. Defer `programstart_repo_clean_check.py`, `serve.py` read-only guard, and `gate-safe` nox session to Phase 1.5.
6. The smoke safety policy decision MUST be the first item recorded in DECISION_LOG (per P4 canonical-before-dependent — the policy decision is the authority for all subsequent smoke changes).
7. All changed files that are in a sync rule MUST be reviewed together in the same commit (per P9 — the `automation_gate_jit_alignment` sync rule binds `noxfile.py`, `.vscode/tasks.json`, and `source-of-truth.instructions.md`).

---

## 15. Consolidated Implementation Plan

This section supersedes all prior delivery orders (Sections 4, 7, 11). It is the single reference for Phase 1 execution. Every item below maps to a code example in Section 13 or a specific authority file.

### 15.1 Superseded Sections

| Section | Status |
|---|---|
| Section 4 (Original delivery order) | **Superseded** by Section 7, then by Section 11, now by this section |
| Section 7 (Revised delivery order) | **Superseded** by Section 11, now by this section |
| Section 9 (Original Go/No-Go) | **Superseded** by Section 11, then by Section 14 |
| Section 11 (Revised Go/No-Go) | **Superseded** by Section 14 |
| Section 14 (Final Go/No-Go) | **Active** — incorporated into this section |

### 15.2 Definitive Phase 1 Delivery Checklist

Every item has: delivery step number, file(s) to change, code example reference, protocol satisfied, and verification command.

#### Step 0: Pre-flight

- [ ] Run `programstart guide --system programbuild` + `programstart guide --system userjourney` + `programstart drift`
- [ ] All three must pass before any edits
- Protocol: P1 JIT (Step 2 — clean baseline)

#### Step 1: Record smoke safety policy decision

- [ ] Add entry to `PROGRAMBUILD/DECISION_LOG.md`
- Decision: "Root-workspace smoke MUST be read-only. Mutating dashboard smoke MUST run only in isolated temp workspaces."
- Protocol: P7 ADR Recording, P4 Canonical-Before-Dependent (policy is authority for all subsequent smoke changes)
- Verify: `programstart validate --check all` + `programstart drift`

#### Step 2: Add product docs to implementation_loop guidance

- [ ] Edit `config/process-registry.json` — add ARCHITECTURE.md, REQUIREMENTS.md, USER_FLOWS.md to `implementation_loop.files`
- Code example: Section 13.1
- Protocol: P1 JIT (product docs now surfaced by `programstart guide`)
- Verify: `programstart guide --system programbuild --stage implementation_loop` must list 8 files

#### Step 3: Add product-JIT rules to source-of-truth instructions

- [ ] Edit `.github/instructions/source-of-truth.instructions.md` — add 3 product authority rows to table + new "Product-level JIT during implementation" section
- Code example: Section 13.2
- Protocol: P1 JIT (AI sessions now instructed to re-read product docs)
- Verify: `programstart validate --check all` + `programstart drift`

#### Step 4: Add product-JIT rules to copilot instructions

- [ ] Edit `.github/copilot-instructions.md` — add 3 new lines to Workflow Expectations
- Code example: Section 13.3
- Protocol: P1 JIT (copilot sessions now instructed to re-read product docs)
- Verify: `programstart validate --check all` + `programstart drift`

#### Step 5: Update stage-guide prompt

- [ ] Edit `.github/prompts/programstart-stage-guide.prompt.md` — add task 6 for implementation product-doc reminder
- Code example: Section 13.4
- Protocol: P1 JIT (prompt now reminds operator about product docs)
- Verify: `programstart prompt-eval --json`

#### Step 6: Split dashboard smoke (read-only vs. mutating)

- [ ] Create `scripts/programstart_dashboard_smoke_readonly.py`
- [ ] Update nox `smoke` session to use read-only script for root-workspace checks
- Code example: Section 13.9
- Protocol: P12 Repository Boundary (root workspace not mutated)
- Verify: Run read-only smoke, confirm no POST calls, confirm `git status` unchanged

#### Step 7: Wire drift into nox validate

- [ ] Edit `noxfile.py` — add `session.run("programstart", "drift")` before and after validate chain
- Code example: Section 13.5
- Protocol: P1 JIT (local automation now matches CI), P9 Sync Rules
- Verify: `nox -s validate`

#### Step 8: Add drift to `run_next()` in CLI

- [ ] Edit `scripts/programstart_cli.py` — add drift to `run_next()` steps list
- Code example: Section 13.6
- Protocol: P1 JIT (default operator entry point is now JIT-complete)
- Verify: `programstart next`

#### Step 9: Update CLI smoke

- [ ] Edit `scripts/programstart_cli_smoke.py` — add `["guide", "--system", "userjourney"]` and `["drift"]`
- Code example: Section 13.7
- Protocol: P1 JIT, P10 USERJOURNEY Authority Chain
- Verify: `python scripts/programstart_cli_smoke.py`

#### Step 10: Add VS Code tasks

- [ ] Edit `.vscode/tasks.json` — add Drift Check, JIT Check, Safe Gate tasks
- Code example: Section 13.8
- Protocol: P1 JIT (editor surface now has JIT actions)
- Verify: open VS Code tasks panel, confirm new tasks visible

#### Step 11: Add factory smoke cleanup to nox clean

- [ ] Edit `noxfile.py` — add `.tmp_factory_smoke` and `.tmp_nox_factory_smoke` to clean targets
- Code example: Section 13.10
- Protocol: Disk hygiene
- Verify: `nox -s clean`

#### Step 12: Update docs (required by sync rule)

- [ ] Review and update `QUICKSTART.md` — reflect the new JIT operator path (guide → drift → edit → validate → drift)
- [ ] Review and update `README.md` — reflect new tasks and smoke split
- [ ] Review and update `source-of-truth.instructions.md` if any wording changed during Steps 3-4
- Protocol: P9 Sync Rules (`automation_gate_jit_alignment` binds noxfile.py, tasks.json, source-of-truth.instructions.md)
- Verify: `programstart drift`

#### Step 13: Update changelog

- [ ] Edit `PROGRAMBUILD/PROGRAMBUILD_CHANGELOG.md` — record all nox, task, smoke, and JIT changes
- Protocol: P4 Canonical-Before-Dependent (PROGRAMBUILD_CANONICAL.md rule 5 requires changelog for system-level changes)
- Verify: `programstart validate --check all` + `programstart drift`

#### Step 14: Final gate

- [ ] Run `programstart validate --check all`
- [ ] Run `programstart drift`
- [ ] Run `nox -s lint typecheck tests validate docs`
- [ ] All must pass

### 15.3 What Phase 1 Does NOT Include (Deferred)

| Item | Deferred To | Reason |
|---|---|---|
| Challenge Gate Part H (architecture alignment check) | ~~Phase 2~~ DONE | Implemented 2026-04-11 — 8 parts, gate log header, variant table, prompts updated |
| Product-JIT prompt file (`product-jit-check.prompt.md`) | ~~Phase 2~~ DONE | Implemented 2026-04-11 — registered in bootstrap_assets |
| Implementation-alignment sync rules | ~~Phase 2~~ DONE | Implemented 2026-04-11 — architecture_decision_alignment + requirements_test_alignment |
| `programstart_repo_clean_check.py` | Phase 1.5 | Useful but not blocking smoke split |
| `serve.py` read-only route guard | ~~Phase 1.5~~ DONE | Implemented 2026-04-11 — PROGRAMSTART_READONLY env var, 5 tests |
| `gate-safe` nox session | ~~Phase 1.5~~ DONE | Implemented 2026-04-11 — nox -s gate_safe |
| P2 Challenge Gate automation | ~~Phase 2+~~ DONE | Implemented 2026-04-11 — advance warns on missing gate log entry, --skip-gate-check bypass |
| P3 Cross-Stage Validation automation | Phase 2+ | Requires contradiction detection tooling |
| P8 Re-Entry staleness detection | Phase 3+ | Requires state timestamp analysis |
| P7 ADR existence checking | Phase 2+ | Requires decision-to-ADR mapping |

### 15.4 Commit Strategy

All Phase 1 changes MUST follow Conventional Commits (P6).

Recommended commit groupings:

| Commit | Steps | Message |
|---|---|---|
| 1 | Step 1 | `docs(programbuild): record smoke safety policy in DECISION_LOG` |
| 2 | Steps 2-5 | `feat(schema): add product docs to implementation_loop and product-JIT guidance` |
| 3 | Step 6 | `feat(programbuild): split dashboard smoke into read-only and mutating scripts` |
| 4 | Steps 7-11 | `feat(programbuild): wire drift into validate, next, cli smoke, tasks, and clean` |
| 5 | Steps 12-13 | `docs: update quickstart, readme, and changelog for Phase 1 changes` |
| 6 | Step 14 | No commit — verification only |

Each commit must pass `programstart validate --check all` and `programstart drift` before proceeding to the next.

### 15.5 Implementation Go/No-Go

#### Prerequisites (all verified 2026-04-11)

| Prerequisite | Status | Evidence |
|---|---|---|
| Source-of-truth files in sync | PASS | `programstart validate --check all` + `programstart drift` both pass |
| All 12 protocols mapped | PASS | Section 12.1 |
| Enforcement gaps documented | PASS | Section 12.2 |
| Code examples verified against live files | PASS | Spot-checked 2026-04-11 — all code examples match actual content |
| Product-JIT gap documented with evidence | PASS | Section 10 |
| Delivery order is concrete and dependency-ordered | PASS | Section 15.2 (14 steps, each with file, code ref, protocol, verify) |
| No unresolved blockers | PASS | Section 6.3 blockers all resolved |
| Deferred items explicitly listed | PASS | Section 15.3 |
| Commit strategy defined | PASS | Section 15.4 |

#### Risks accepted

| Risk | Severity | Mitigation |
|---|---|---|
| Phase 1 touches ~12 files | Medium | Grouped into 5 logical commits with verify-after-each |
| Dashboard smoke split may need iteration | Low | Mutating smoke still exists, just isolated |
| `programstart next` adding drift may slow default task | Low | Drift is fast; non-blocking |
| Sync rule fires on noxfile change | Expected | Docs update in same commit group (Step 12) |

#### Verdict

**GO — Phase 1 implementation may proceed.**

Begin at Step 0 (pre-flight JIT baseline). Follow the checklist in Section 15.2 sequentially. Verify after each step. Do not skip steps.
