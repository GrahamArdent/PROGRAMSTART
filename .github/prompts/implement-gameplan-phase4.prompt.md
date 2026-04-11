---
description: "Execute Phases 4-6 of the improvegameplan.md — confidence tiers, package contract, diagnostics."
name: "Implement Gameplan Phase 4"
agent: "agent"
---

# Phase 4 Implementation Prompt (Gameplan Phases 4-6)

**Authority:** `improvegameplan.md` Section 2 (Phases 4-6), Section 3.3 (remaining nox/task items).
**Prerequisites:** Phases 1, 1.5, 2, and 3 are complete and committed. Validate + drift both pass. All 604 tests pass (0 failures).

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
- [ ] `uv run pytest --tb=line -q` — 604 passed, 0 failed
- [ ] All must pass before any edits

---

## Step 1: Split nox `smoke` into confidence tiers (Phase 4)

**Current state:** The `smoke` nox session is a single monolith that runs dashboard API smoke, browser smoke, golden screenshots, bootstrapped-workspace validation, and factory smoke. It takes several minutes and requires Playwright + Chromium.

**Target state:** Three nox sessions that split by trust level:

- `smoke_readonly` — root-workspace read-only dashboard smoke + browser smoke (no mutations, no bootstrap). Use `scripts/programstart_dashboard_smoke_readonly.py` + browser smoke. Safe to run anytime.
- `smoke_isolated` — bootstrapped-workspace validation + mutating dashboard smoke + factory smoke (creates temp workspaces, exercises POST routes)
- `smoke` — runs both `smoke_readonly` and `smoke_isolated` via `session.notify()` (backwards compatible)

Update callers:
- `ci` session: replace `smoke` reference if needed (it uses `session.notify("smoke")` which should still work)
- `gate_safe` session: add `smoke_readonly` after `validate` — safe gate now includes read-only smoke confidence

Add a `quick` nox session for fast feedback (~10s):
- `quick` — runs `lint` + `typecheck` via `session.notify()`
- This is the fastest confidence check for "did I break anything obvious?"

Update `nox.options.sessions` default list if appropriate.

**Tests:**
- `test_programstart_command_registry.py` or `test_programstart_cli.py` may have nox session assertions — check and update if needed
- Verify: `nox -l` shows the new sessions, `nox -s smoke_readonly` runs successfully

---

## Step 2: Add VS Code tasks for new confidence tiers (Phase 4+5)

- [ ] Add task `PROGRAMSTART: Quick Check` → `uv run nox -s quick`
- [ ] Add task `PROGRAMSTART: Read-only Smoke` → `uv run nox -s smoke_readonly`
- [ ] Add task `PROGRAMSTART: Package Smoke` → `uv run nox -s package`
- [ ] Add task `PROGRAMSTART: Isolated Smoke` → `uv run nox -s smoke_isolated`

These make the confidence tiers visible in the VS Code task runner.

**Verify:** Tasks visible in VS Code, validate still passes.

---

## Step 3: Document confidence tiers in README (Phase 4)

- [ ] Add a "Confidence Tiers" or "Quality Gates" section to `README.md` 
- Explain the three tiers:
  1. **Quick** (`nox -s quick`): lint + typecheck. Use during active editing for fast feedback.
  2. **Safe Gate** (`nox -s gate_safe`): lint + typecheck + tests + validate + read-only smoke + docs. Use before committing. Local pre-merge confidence.
  3. **Full CI** (`nox -s ci`): everything including isolated smoke, package smoke, and security scanning. Use before pushing or when preparing a release.
- Reference the VS Code tasks that map to each tier

**Verify:** `nox -s docs` (MkDocs build) must still pass

---

## Step 4: Improve smoke diagnostic output (Phase 6)

- [ ] Review `scripts/programstart_dashboard_smoke_readonly.py` — ensure failed endpoint checks print the URL, status code, and response snippet (not just a generic assertion)
- [ ] Review `scripts/programstart_cli_smoke.py` — ensure failed command checks print the command, exit code, and stderr excerpt
- [ ] If diagnostic output is already adequate, skip this step and note it

**Verify:** Run `programstart_dashboard_smoke_readonly.py` manually, confirm output is clear on success; intentionally break something (e.g. stop server) and confirm the failure message is actionable

---

## Step 5: Update docs and changelog

- [ ] Update `PROGRAMBUILD/PROGRAMBUILD_CHANGELOG.md` with Phase 4 entry
- [ ] Update `improvegameplan.md` Section 2 to mark Phases 4-6 as DONE or note their status
- [ ] If any new files were created, register them in `config/process-registry.json` `bootstrap_assets`

**Verify:** `programstart validate --check all` + `programstart drift`

---

## Step 6: Commit Phase 4

Recommended commit groupings:

| Commit | Steps | Message |
|---|---|---|
| 1 | Step 1 | `refactor: split nox smoke into confidence tiers (quick, readonly, isolated)` |
| 2 | Step 2 | `feat: add VS Code tasks for confidence tiers and package smoke` |
| 3 | Steps 3-5 | `docs: document confidence tiers and update changelog` |

Each commit must pass `programstart validate --check all` and `programstart drift`.

---

## Step 7: Final gate

- [ ] `programstart validate --check all`
- [ ] `programstart drift`
- [ ] `uv run pytest --tb=line -q` — all pass, 0 failures
- [ ] `nox -s quick` — passes
- [ ] `nox -s gate_safe` — passes
- [ ] `git log --oneline` — verify commit messages follow Conventional Commits
