---
description: "Execute Phase 3 of the improvegameplan.md implementation plan — remaining deferred items."
name: "Implement Gameplan Phase 3"
agent: "agent"
---

# Phase 3 Implementation Prompt

**Authority:** `improvegameplan.md` Sections 12, 14, and 15.3.
**Prerequisites:** Phases 1, 1.5, and 2 are complete and committed. Validate + drift both pass.

---

## Binding Rules

1. **JIT-first.** Before any edit, run `programstart guide` for both systems + `programstart drift`. All must pass.
2. **Canonical-before-dependent.** If a change touches an authority file and a dependent, edit the authority first.
3. **Verify-after-each.** After each step, run `programstart validate --check all` and `programstart drift`. Both must pass before proceeding.
4. **No memory.** Re-read the actual target file before editing it. Do not edit from memory.
5. **Conventional commits.** Every commit must follow `<type>[scope]: <description>`.
6. **Sync rules matter.** If you touch a file in a sync rule, review its paired files and update if needed.
7. **Tests required.** Every behavioral change must have a covering test. Fix any test regressions before proceeding.
8. **bootstrap_assets.** Any new file in `.github/prompts/` or `scripts/` must be added to `config/process-registry.json` `bootstrap_assets`.

---

## Step 0: Pre-flight

- [ ] Run `programstart guide --system programbuild` + `programstart guide --system userjourney` + `programstart drift`
- [ ] All three must pass before any edits

---

## Step 1: Add `programstart_repo_clean_check.py`

- [ ] Create `scripts/programstart_repo_clean_check.py`
- Purpose: Assert that git working tree is clean before and after an operation (e.g. root-workspace smoke)
- Interface:
  - `capture_git_status() -> set[str]` — returns set of changed/untracked file paths
  - `assert_repo_clean(label: str) -> None` — raises `SystemExit(1)` with file-level summary if any changed files
  - `assert_repo_unchanged(before: set[str], after: set[str], label: str) -> None` — fails if new changes appeared
  - CLI: `python scripts/programstart_repo_clean_check.py` — exits 0 if clean, 1 with diff summary if dirty
- Register in `config/process-registry.json` `bootstrap_assets`
- Add tests in `tests/test_programstart_repo_clean_check.py`:
  - Test clean repo returns empty set
  - Test dirty repo returns changed files
  - Test `assert_repo_unchanged` passes when before == after
  - Test `assert_repo_unchanged` fails when new files appear
- Verify: `programstart validate --check all` + `uv run pytest tests/test_programstart_repo_clean_check.py`

---

## Step 2: Add P3 Cross-Stage Validation automation

- [ ] Edit `scripts/programstart_workflow_state.py` — in the `advance` command:
  - After the existing Challenge Gate log check, add a cross-stage validation reminder
  - Check if `.github/prompts/programstart-cross-stage-validation.prompt.md` exists
  - If at stage 3+ (architecture stage onward), print an advisory:
    "Tip: Run the cross-stage validation prompt before advancing: @workspace /prompt Cross-Stage Validation"
  - This is advisory only (not blocking) — the prompt does the actual checking
- [ ] Add a `--skip-cross-stage-check` flag to suppress the advisory (parallel to `--skip-gate-check`)
- Tests:
  - Test that advisory appears for programbuild advance at stage 3+
  - Test that advisory does not appear for stages 0-2
  - Test `--skip-cross-stage-check` suppresses it
- Verify: `programstart advance --system programbuild --dry-run`

---

## Step 3: Add P7 ADR existence advisory

- [ ] Create a validation check in `scripts/programstart_validate.py` or a standalone helper
- Purpose: Check if DECISION_LOG.md has entries without corresponding ADR files in `docs/decisions/`
- Logic:
  - Parse DECISION_LOG.md Decision Register table
  - For each DEC-NNN entry whose status is ACTIVE or ACCEPTED:
    - Check if `docs/decisions/` contains an ADR referencing that decision (by ID or related topic)
  - If any active decision has no ADR reference, emit a warning (not a hard failure)
- This check should be callable from `programstart validate --check adr-coverage` (new check target)
- Tests:
  - Test with matching ADR → no warning
  - Test with missing ADR → warning emitted
  - Test with no decisions → no warning
- Verify: `programstart validate --check adr-coverage`

---

## Step 4: Add P8 Re-Entry staleness detection

- [ ] Add staleness check to `programstart status` or `programstart next`
- Purpose: Detect when the last state change was >4 weeks ago and suggest re-entry protocol
- Logic:
  - Read the active step's `signoff.date` (or the most recent signoff date across all steps)
  - If no signoff date is available, check the most recent git commit date touching STATE.json
  - Compare to today's date
  - If >28 days since last state activity:
    - Print warning: "⚠ Last state change was N days ago. Consider running the Re-Entry Protocol
      (PROGRAMBUILD_CHALLENGE_GATE.md) before continuing."
  - If >56 days: escalate to stronger warning
- Add `--skip-staleness-check` flag or respect a `PROGRAMSTART_SKIP_STALENESS` env var
- Tests:
  - Test recent date → no warning
  - Test 30-day-old date → warning
  - Test 60-day-old date → escalated warning
  - Test skip flag suppresses warning
- Verify: `programstart status` with mocked dates

---

## Step 5: Update docs and changelog

- [ ] Update `PROGRAMBUILD/PROGRAMBUILD_CHANGELOG.md` with Phase 3 entry
- [ ] Update `improvegameplan.md` Section 15.3 to mark all remaining items as DONE or DEFERRED
- [ ] If any new validate checks were added, update `README.md` validation section
- Verify: `programstart validate --check all` + `programstart drift`

---

## Step 6: Commit Phase 3

Recommended groupings:
1. `feat: add programstart_repo_clean_check helper with tests`
2. `feat(programbuild): add cross-stage validation advisory to advance`
3. `feat: add ADR coverage check and re-entry staleness detection`
4. `docs: update changelog and docs for Phase 3 completion`

---

## Step 7: Final gate

- [ ] Run `programstart validate --check all`
- [ ] Run `programstart drift`
- [ ] Run `uv run pytest --tb=short -q` — all tests pass (except known pre-existing failures)
- [ ] Run `nox -s validate` — must pass
