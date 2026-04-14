---
description: "Implement Phase F of stage2gameplan.md — dispatch chain integration tests. Commit 7."
mode: "agent"
---

# Implement Phase F: Dispatch Chain Integration Tests

## Authority

This prompt implements **Commit 7 (Phase F)** from `stage2gameplan.md` Section 15.
The gameplan is the SOLE specification — do not invent behaviour not documented there.

Read the following before any code change:

1. `stage2gameplan.md` — Section 13 "Implementation Phase F" (the full spec with corrected test code from the ninth-pass audit)
2. `tests/test_programstart_workflow_state.py` — current imports and test patterns
3. `CHANGELOG.md` — current `[Unreleased]` section

## JIT Protocol (mandatory)

Before writing any code:

1. Run `uv run programstart guide --system programbuild` — derive file context from registry
2. Run `uv run programstart drift` — verify clean baseline; STOP if violations exist
3. After all edits: run `uv run programstart validate --check all` and `uv run programstart drift` — both must pass

## Scope

Phase F adds exactly **3 integration tests** and a **CHANGELOG entry**. No other files are modified.

### Step F1: `test_preflight_problems_dispatches_stage_gate`

**Purpose test:** Proves the full dispatch chain fires — `preflight_problems() → stage_checks dict → run_stage_gate_check() → validate_intake_complete()` — without monkeypatching the dispatch path.

**Monkeypatch strategy (from gameplan Section 13 "Monkeypatch architecture"):**

- `scripts.programstart_validate.workspace_path` → `lambda rel: tmp_path / rel`
- `scripts.programstart_workflow_state.workspace_path` → `lambda rel: tmp_path / rel`
- `scripts.programstart_validate.validate_authority_sync` → `lambda _registry: []` (prevents `FileNotFoundError` — F-B1)

**NOT monkeypatched:** `load_registry`, `preflight_problems`, `run_stage_gate_check`, `validate_intake_complete` — the chain under test.

**Setup:** Create `PROGRAMBUILD/` in `tmp_path`, write blank-template `PROGRAMBUILD_KICKOFF_PACKET.md` and `PROGRAMBUILD_IDEA_INTAKE.md` with empty field values.

**Assertions:**
- `isinstance(problems, list)` — B0 regression guard
- At least one problem containing `"PROJECT_NAME is empty"` or `"PROBLEM_RAW is empty"` — field-level text that can ONLY come from `validate_intake_complete` (not from upstream `validate_required_files`)

### Step F2: `test_preflight_problems_skips_gate_for_userjourney`

**Purpose test:** Proves the `if system == "programbuild" and active_step:` guard prevents stage-gate checks from leaking into userjourney.

**Monkeypatch strategy:**

- `scripts.programstart_validate.workspace_path` → `lambda rel: tmp_path / rel`
- `scripts.programstart_workflow_state.workspace_path` → `lambda rel: tmp_path / rel`

**Assertions:**
- `isinstance(problems, list)`
- Zero problems containing `"PROJECT_NAME"`, `"PROBLEM_RAW"`, `"KICKOFF_PACKET"`, or `"IDEA_INTAKE"` — none should appear for userjourney

### Step F3: `test_advance_blocked_by_real_stage_gate`

**Purpose test:** Full CLI e2e — advance command with incomplete Stage 0 docs blocked by real stage-gate validation. The dispatch chain is NOT monkeypatched.

**Monkeypatch strategy (from gameplan Section 13, audit findings F-B1 through F-B5):**

- `scripts.programstart_validate.workspace_path` → `lambda rel: tmp_path / rel`
- `scripts.programstart_workflow_state.workspace_path` → `lambda rel: tmp_path / rel`
- `scripts.programstart_validate.validate_authority_sync` → `lambda _registry: []` (F-B1)
- `scripts.programstart_workflow_state.load_workflow_state` → returns `create_default_workflow_state(registry, "programbuild")` (F-B4: `load_workflow_state` uses `programstart_common.workspace_path` which is NOT monkeypatched)
- `scripts.programstart_workflow_state.workflow_active_step` → `"inputs_and_mode_selection"` (F-B4)
- `scripts.programstart_workflow_state.workflow_steps` → real step_order from registry (F-B4)
- `scripts.programstart_workflow_state.save_workflow_state` → no-op safety net (F-D2)
- `scripts.programstart_workflow_state._check_challenge_gate_log` → `None` safety net (F-D4)
- `sys.argv` → advance command without `--dry-run` or `--skip-preflight`

**NOT monkeypatched:** `preflight_problems`, `run_stage_gate_check`, `validate_intake_complete` — the dispatch chain.

**State:** Use `create_default_workflow_state(registry, "programbuild")` — canonical constructor producing all 11 stages with correct keys (`active_stage`, `stages`, `variant`, `signoff` sub-dicts). Source: `config/process-registry.json` via `programstart_common.py`. (F-B2, F-J1)

**Assertions:**
- `result = main()` then `assert result == 1` (NOT `pytest.raises(SystemExit)` — F-B5)
- `"Advance preflight failed"` in stdout
- `"PROJECT_NAME is empty"` or `"PROBLEM_RAW is empty"` in stdout — field-level proof that the dispatch chain fired

### Step F4: CHANGELOG

Add to `### Added` under `[Unreleased]`:

```
- 3 integration tests for the `preflight_problems → stage-gate dispatch → validator` chain: dispatch fires for programbuild (field-level assertions), skips for userjourney, and advance blocks with real validator output. Authority sync and state loading isolated; dispatch chain exercised without monkeypatching.
```

### Import requirement

The test file needs `from scripts.programstart_common import create_default_workflow_state` added to the imports. Verify it is not already present before adding.

## Safety rules

- Do NOT modify any file other than `tests/test_programstart_workflow_state.py` and `CHANGELOG.md`.
- Do NOT change existing tests — only append new ones.
- Do NOT monkeypatch `preflight_problems`, `run_stage_gate_check`, or `validate_intake_complete` — the dispatch chain must execute for real.
- Every assertion must be a **purpose test** — it tests a specific behaviour described in the gameplan, not an implementation detail.
- Use the exact test code from gameplan Section 13 Steps F1-F3 (ninth-pass corrected versions).
- Run `uv run pytest tests/test_programstart_workflow_state.py -v --tb=short` after all edits — all tests must pass.

## Verification checklist (Section 17, items 10-14)

After implementation, verify:

- [ ] All tests in `test_programstart_workflow_state.py` pass
- [ ] `test_preflight_problems_dispatches_stage_gate` asserts on `"PROJECT_NAME is empty"` (field-level, not filename)
- [ ] `test_advance_blocked_by_real_stage_gate` uses `result == 1` (not `SystemExit`)
- [ ] `validate_authority_sync` is monkeypatched to `[]` in F1 and F3
- [ ] F3 uses `create_default_workflow_state(registry, "programbuild")` (not hand-crafted dict)
- [ ] `uv run programstart validate --check all` passes
- [ ] `uv run programstart drift` passes
