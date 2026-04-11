---
description: "Execute Phase 1 of the improvegameplan.md — JIT product surfacing, smoke safety, drift wiring, and task additions. Follows Section 15.2 delivery checklist step by step."
name: "Implement Gameplan Phase 1"
agent: "agent"
---

# Implement Gameplan Phase 1

You are executing Phase 1 of `improvegameplan.md` in the PROGRAMSTART workspace at `C:\ PYTHON APPS\PROGRAMSTART`.

## Binding Rules

1. **Source-of-truth protocol is mandatory.** Before ANY edit, run `programstart guide --system programbuild`, `programstart guide --system userjourney`, and `programstart drift`. All three must pass. If drift fails, STOP and fix before proceeding.
2. **Canonical before dependent.** When editing authority files and their dependents, edit the authority file first. Never invent content that does not exist in the authority file.
3. **Verify after every step.** After every step in the checklist below, run `programstart validate --check all` and `programstart drift`. Both must pass before the next step.
4. **Conventional Commits.** All commits use format `<type>[optional scope]: <description>`. Valid types: `feat`, `fix`, `docs`, `chore`, `ci`, `refactor`, `test`.
5. **Do not implement deferred items.** Section 15.3 of the gameplan lists items deferred to Phase 1.5, 2, and 3. Do NOT implement any of them.
6. **Do not modify files outside Phase 1 scope.** Only touch the files specified in each step.
7. **Repository boundary.** All work stays inside `C:\ PYTHON APPS\PROGRAMSTART`. Never touch another repo.
8. **Read before writing.** Before editing any file, re-read the current content. Do not edit from memory.
9. **Keep changes minimal.** Do not refactor, add comments, or "improve" code beyond what the gameplan specifies.

## Pre-Flight (Step 0)

Run these commands and confirm all pass:

```
uv run programstart guide --system programbuild
uv run programstart guide --system userjourney
uv run programstart drift
```

If any fail, STOP. Do not proceed until baseline is clean.

## Step 1: Record Smoke Safety Policy Decision

Add an entry to `PROGRAMBUILD/DECISION_LOG.md`:

- ID: `DEC-001`
- Date: `2026-04-11`
- Stage: `inputs_and_mode_selection`
- Decision: Root-workspace smoke MUST be read-only. Mutating dashboard smoke MUST run only in isolated temp workspaces.
- Status: `ACTIVE`
- Owner: Solo operator
- Related file: `noxfile.py`, `scripts/programstart_dashboard_smoke.py`

Add a matching Decision Details section with:
- Context: Dashboard smoke script exercises 3 POST routes that mutate the live workspace (uj-phase, uj-slice, workflow-signoff). Only workflow-advance uses dry_run. Signoff route is accumulative — each run adds a history entry.
- Decision: Read-only smoke for root workspace. Mutating smoke isolated to bootstrapped temp workspaces.
- Why: Trust boundary. Operators must trust that orientation tools (guide, drift, dashboard) do not silently change state.
- Alternatives considered: (1) Add dry_run to all POST routes — still requires trusting the flag. (2) Environment variable guard on server — smoke-level isolation is simpler to reason about.
- Consequences: Dashboard smoke split into two scripts. CI continues running mutating smoke in bootstrapped workspaces.
- Follow-up: Phase 1.5 may add route-level read-only guard for defense-in-depth.

Update the `Last updated:` metadata to `2026-04-11`.

**Verify:** `programstart validate --check all` + `programstart drift`

## Step 2: Add Product Docs to implementation_loop Guidance

Edit `config/process-registry.json`. In `workflow_guidance.programbuild.implementation_loop.files`, prepend these three entries before the existing five:

```json
"PROGRAMBUILD/ARCHITECTURE.md",
"PROGRAMBUILD/REQUIREMENTS.md",
"PROGRAMBUILD/USER_FLOWS.md",
```

The resulting files array must have 8 entries: ARCHITECTURE.md, REQUIREMENTS.md, USER_FLOWS.md, TEST_STRATEGY.md, DECISION_LOG.md, PROGRAMBUILD_CHECKLIST.md, PROGRAMBUILD_CHALLENGE_GATE.md, PROGRAMBUILD_GAMEPLAN.md.

**Verify:** `programstart validate --check all` + `programstart drift`

## Step 3: Add Product-JIT Rules to source-of-truth.instructions.md

Edit `.github/instructions/source-of-truth.instructions.md`:

1. In the authority table under "Quick reference: authority files by concern", add three new rows AFTER "Which files are control files" and BEFORE "USERJOURNEY execution order":

```markdown
| Product architecture and contracts | `PROGRAMBUILD/ARCHITECTURE.md` |
| Product requirements and scope | `PROGRAMBUILD/REQUIREMENTS.md` |
| Product user flows | `PROGRAMBUILD/USER_FLOWS.md` |
```

2. Add a new section AFTER "What to never do" and BEFORE "Quick reference":

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

**Verify:** `programstart validate --check all` + `programstart drift`

## Step 4: Add Product-JIT Rules to copilot-instructions.md

Edit `.github/copilot-instructions.md`. Add three new lines at the END of the "Workflow Expectations" section (after the `first_value_achieved` line):

```markdown
- During implementation (Stage 7+), re-read the applicable contracts in `PROGRAMBUILD/ARCHITECTURE.md` and the relevant requirement in `PROGRAMBUILD/REQUIREMENTS.md` before writing feature code. Do not implement from conversation memory.
- If implementation design contradicts `ARCHITECTURE.md`, update `ARCHITECTURE.md` first. Do not ship code that contradicts an authority doc.
- If you add a new contract, endpoint, or auth rule not documented in `ARCHITECTURE.md`, record it in `DECISION_LOG.md` and update `ARCHITECTURE.md` in the same commit.
```

**Verify:** `programstart validate --check all` + `programstart drift`

## Step 5: Update Stage-Guide Prompt

Edit `.github/prompts/programstart-stage-guide.prompt.md`. Add a new task 6 BEFORE the final "Prefer the registry-backed..." line:

```markdown
6. For the implementation_loop stage: remind the operator that ARCHITECTURE.md, REQUIREMENTS.md, and USER_FLOWS.md are living authorities during coding. They must be re-read before each feature, not just at stage entry. If the guide output includes these files, call them out as "re-read before each feature" rather than "read once at stage start."
```

**Verify:** `programstart prompt-eval --json`

## Step 6: Create Read-Only Dashboard Smoke Script

Create `scripts/programstart_dashboard_smoke_readonly.py`. This script must:

- Start the dashboard server on an ephemeral port
- Exercise ONLY GET endpoints: `/api/state`, `/`, `/api/guide?system=programbuild`, `/api/doc`
- Check HTML markers: "Recent Projects", "Sync And Drift", "uj-slice-status", "modal-date"
- NEVER call any POST endpoint
- Print PASS/FAIL per check and return exit code 1 on any failure
- Reuse the same `choose_port`, `request_json`, `request_text`, `wait_for_server` patterns from the existing `programstart_dashboard_smoke.py`

The existing `programstart_dashboard_smoke.py` stays UNCHANGED — it continues to be used in the nox `smoke` session bootstrapped workspace.

**Verify:** Run `python scripts/programstart_dashboard_smoke_readonly.py` from the workspace root. All checks pass. Run `git status` — no files changed by the smoke run.

## Step 7: Wire Drift Into Nox Validate

Edit `noxfile.py`. In the `validate` session function:

1. Add `session.run("programstart", "drift")` as the FIRST command after `install_dev(session)`
2. Add `session.run("programstart", "drift")` as the LAST command in the session

Do not change any other session.

**Verify:** `nox -s validate` (must pass without errors)

## Step 8: Add Drift to run_next() in CLI

Edit `scripts/programstart_cli.py`. In the `run_next()` function, add one new entry to the `steps` list AFTER the last `run_passthrough` call:

```python
run_passthrough(programstart_drift_check.main, "programstart drift", []),
```

`programstart_drift_check` is already imported at the top of this file — verify this before editing.

**Verify:** `programstart next` (drift now runs at the end)

## Step 9: Update CLI Smoke

Edit `scripts/programstart_cli_smoke.py`. In the `checks` list, add two new entries AFTER `["guide", "--system", "programbuild"]` and BEFORE `["state", "show"]`:

```python
["guide", "--system", "userjourney"],
["drift"],
```

**Verify:** `python scripts/programstart_cli_smoke.py`

## Step 10: Add VS Code Tasks

Edit `.vscode/tasks.json`. Add three new task objects BEFORE the final `]` of the tasks array (after the Launch Web Dashboard task):

```json
,
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

**Verify:** Open VS Code task picker, confirm all three new tasks are listed.

## Step 11: Add Factory Smoke Cleanup to Nox Clean

Edit `noxfile.py`. In the `clean` session, add two entries to the `targets` list:

```python
".tmp_nox_factory_smoke",
".tmp_factory_smoke",
```

Insert them after `".tmp_nox_create"` and before `".tmp_dist_smoke"`.

**Verify:** `nox -s clean` runs without errors.

## Step 12: Update Documentation (Required by Sync Rule)

### QUICKSTART.md

Update the "Day-to-Day Loop" section to reflect the recommended JIT operator path. Under "Step 1 — Understand what's active", add drift after guide:

```powershell
.\scripts\pb.ps1 drift         # verify baseline is clean before editing
```

Add a note: "The `pb next` command now includes a drift check automatically."

### README.md

In the validation section (near `programstart validate` and `programstart drift` boxes), add a note that `nox -s validate` now includes drift checks before and after, and that three new VS Code tasks (Drift Check, JIT Check, Safe Gate) are available.

Keep changes minimal — only update sections that describe the validate/drift/task surfaces.

**Verify:** `programstart drift` (sync rule must pass with docs updated alongside noxfile+tasks)

## Step 13: Update Changelog

Edit `PROGRAMBUILD/PROGRAMBUILD_CHANGELOG.md`. Add a new entry at the TOP (after the header, before the existing 2026-04-11 entry):

```markdown
## 2026-04-11 (Phase 1 — JIT Product Surfacing, Smoke Safety, Drift Wiring)

- added ARCHITECTURE.md, REQUIREMENTS.md, USER_FLOWS.md to `implementation_loop.files` in `config/process-registry.json` so `programstart guide` returns product docs during implementation
- added product-JIT rules to `source-of-truth.instructions.md`: three new authority table entries and new "Product-level JIT during implementation" section
- added product-JIT guidance to `copilot-instructions.md` Workflow Expectations: re-read product docs before feature code
- added implementation_loop product-doc reminder to `programstart-stage-guide.prompt.md`
- created `scripts/programstart_dashboard_smoke_readonly.py` for read-only root-workspace smoke
- wired `programstart drift` into nox `validate` session (before and after validate chain)
- added drift step to `run_next()` in `scripts/programstart_cli.py`
- added `guide --system userjourney` and `drift` to CLI smoke checks
- added VS Code tasks: Drift Check, JIT Check, Safe Gate
- added `.tmp_factory_smoke` and `.tmp_nox_factory_smoke` to nox `clean` targets
- recorded smoke safety policy decision in `DECISION_LOG.md` (DEC-001)
- updated `QUICKSTART.md` and `README.md` to reflect new JIT operator path
```

**Verify:** `programstart validate --check all` + `programstart drift`

## Step 14: Final Gate

Run all of these. ALL must pass:

```
programstart validate --check all
programstart drift
nox -s lint typecheck tests validate docs
```

If any fail, diagnose and fix before declaring Phase 1 complete.

## Commit Strategy

After ALL steps pass the final gate, commit in these groups:

| Commit | Steps | Message |
|---|---|---|
| 1 | Step 1 | `docs(programbuild): record smoke safety policy in DECISION_LOG` |
| 2 | Steps 2-5 | `feat(schema): add product docs to implementation_loop and product-JIT guidance` |
| 3 | Step 6 | `feat(programbuild): add read-only dashboard smoke script` |
| 4 | Steps 7-11 | `feat(programbuild): wire drift into validate, next, cli smoke, tasks, and clean` |
| 5 | Steps 12-13 | `docs: update quickstart, readme, and changelog for Phase 1 changes` |

Each commit must individually pass `programstart validate --check all` and `programstart drift`.

## Safety Checklist (Check Before Every Edit)

- [ ] Did I re-read the file I'm about to edit?
- [ ] Am I editing an authority file before its dependents?
- [ ] Is this change within Phase 1 scope?
- [ ] Did I run validate + drift after the last step?
- [ ] Am I following the exact code patterns from Section 13 of the gameplan?
