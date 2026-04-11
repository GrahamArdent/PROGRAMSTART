---
description: "Execute Phase 1.5 and Phase 2 of the improvegameplan.md implementation plan."
name: "Implement Gameplan Phase 1.5 + 2"
agent: "agent"
---

# Phase 1.5 + Phase 2 Implementation Prompt

**Authority:** `improvegameplan.md` Sections 10, 12, 14, and 15.3.
**Prerequisites:** Phase 1 is complete and committed. Validate + drift both pass.

---

## Binding Rules

1. **JIT-first.** Before any edit, run `programstart guide` for both systems + `programstart drift`. All must pass.
2. **Canonical-before-dependent.** If a change touches an authority file and a dependent, edit the authority first.
3. **Verify-after-each.** After each step, run `programstart validate --check all` and `programstart drift`. Both must pass before proceeding.
4. **No memory.** Re-read the actual target file before editing it. Do not edit from memory or from
   the code examples in improvegameplan.md Section 13 (those were written against a prior state).
5. **Conventional commits.** Every commit must follow `<type>[scope]: <description>`.
6. **Sync rules matter.** If you touch a file in a sync rule, review its paired files and update if needed.
7. **Tests required.** Every behavioral change must have a covering test. Fix any test regressions before proceeding.
8. **bootstrap_assets.** Any new file in `.github/prompts/` or `scripts/` must be added to `config/process-registry.json` `bootstrap_assets`.

---

## Step 0: Pre-flight

- [ ] Run `programstart guide --system programbuild` + `programstart guide --system userjourney` + `programstart drift`
- [ ] All three must pass before any edits
- Protocol: P1 JIT (Step 2 — clean baseline)

---

## Phase 1.5 — Quick Wins (no new tooling required)

### Step 1: Add `gate-safe` nox session

- [ ] Edit `noxfile.py` — add a new `gate_safe` session that runs: lint, typecheck, tests, validate, docs
- Purpose: A local pre-merge confidence bundle that excludes mutating smoke and package tests
- This is the same as the "Safe Gate" VS Code task but as a nox session for CLI users
- Verify: `nox -l` shows the new session

### Step 2: Add read-only route guard to `serve.py` (optional but recommended)

- [ ] Edit `scripts/programstart_serve.py` — add a `READONLY_MODE` environment variable check
- When `READONLY_MODE=1`, POST endpoints return 405 Method Not Allowed
- This provides defense-in-depth: even if someone runs the full smoke script against root workspace,
  no mutations can happen when the server is in read-only mode
- Verify: start server with `READONLY_MODE=1`, attempt POST to `/api/uj-phase`, confirm 405

### Step 3: Update docs for Phase 1.5 changes

- [ ] Update `README.md` and `QUICKSTART.md` if any new nox sessions or behaviors were added
- [ ] Update `PROGRAMBUILD/PROGRAMBUILD_CHANGELOG.md` with Phase 1.5 entry
- Verify: `programstart validate --check all` + `programstart drift`

### Step 4: Commit Phase 1.5

- [ ] `feat(programbuild): add gate-safe nox session and read-only route guard`
- [ ] Run `programstart validate --check all` + `programstart drift` — both must pass

---

## Phase 2 — Design-Required Items

### Step 5: Add Part H to Challenge Gate

- [ ] Edit `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md`
- Add "Part H — Architecture and Requirements Alignment" after Part G
- Questions (from improvegameplan.md Section 10.6):
  1. Have any ARCHITECTURE.md contracts been changed without updating the code or tests?
  2. Have any new contracts, endpoints, or auth rules been added in code without documenting in ARCHITECTURE.md?
  3. Does the implemented auth model still match ARCHITECTURE.md?
  4. Are any P0 requirements in REQUIREMENTS.md now impossible given current implementation?
  5. Has any planned USER_FLOWS.md flow been silently dropped or changed?
- Update the gate log header to include Part H column
- Update variant table: Part H required at Stages 6+ for Product/Enterprise
- Verify: `programstart validate --check all`

### Step 6: Create product-JIT prompt file

- [ ] Create `.github/prompts/product-jit-check.prompt.md`
- Purpose: A reusable prompt that tells the AI to re-read product docs before coding
- Content:
  1. Re-read ARCHITECTURE.md contracts relevant to the current task
  2. Re-read the REQUIREMENTS.md entry for the current feature
  3. Check DECISION_LOG.md for any decisions affecting this feature
  4. Confirm alignment before proceeding
  5. If any contradiction found, update the authority doc first
- Register in `config/process-registry.json` `bootstrap_assets`
- Verify: `programstart validate --check all` + `programstart prompt-eval --json`

### Step 7: Add implementation-alignment sync rules

- [ ] Edit `config/process-registry.json` — add sync rule(s):
  - `architecture_decision_alignment`: authority=ARCHITECTURE.md, dependent=DECISION_LOG.md,
    require_authority_when_dependents_change=false (decisions can be added independently),
    but when ARCHITECTURE.md changes, DECISION_LOG.md should be reviewed
  - Consider a rule for REQUIREMENTS.md → TEST_STRATEGY.md alignment
- Verify: `programstart validate --check all` + `programstart drift`

### Step 8: Add Challenge Gate log check to `programstart advance`

- [ ] Edit `scripts/programstart_workflow_state.py` — in the `advance` command:
  - Before advancing, check that `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` has a log entry
    for the current transition (from active_step to next_step)
  - If no log entry found, print a warning (not a hard block in Phase 2 — make it a hard block in Phase 3)
  - Add `--skip-gate-check` flag to bypass
- Verify: attempt `programstart advance --system programbuild --dry-run` — should show gate check warning

### Step 9: Update docs and changelog for Phase 2

- [ ] Update `PROGRAMBUILD/PROGRAMBUILD_CHANGELOG.md` with Phase 2 entry
- [ ] Update `README.md` if new sync rules or advance behavior added
- [ ] Update `improvegameplan.md` Section 15.3 to mark completed Phase 2 items
- Verify: `programstart validate --check all` + `programstart drift`

### Step 10: Commit Phase 2

- Recommended commit groupings:
  1. `docs(programbuild): add Part H architecture alignment check to Challenge Gate`
  2. `feat: add product-JIT prompt and implementation-alignment sync rules`
  3. `feat(programbuild): add Challenge Gate log check to advance command`
  4. `docs: update changelog and docs for Phase 2 changes`

### Step 11: Final gate

- [ ] Run `programstart validate --check all`
- [ ] Run `programstart drift`
- [ ] Run `uv run pytest --tb=short -q` — all tests must pass (except known pre-existing failures)
- [ ] Run `nox -s validate` — must pass
