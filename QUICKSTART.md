# PROGRAMSTART — Quick Start Guide

> You're in the right place if you're starting a new product, converting research into a project, or applying a repeated delivery standard to an existing project.
> This workspace is a reusable planning kit — it guides work from intent to launch without losing authority, context, or evidence.

---

## Workflow Modes

| System | Use it when... | Key state file |
|--------|----------------|----------------|
| **PROGRAMBUILD** | Defining or improving scope, architecture, testing, implementation, and release readiness | `PROGRAMBUILD/PROGRAMBUILD_STATE.json` |
| **USERJOURNEY** | Designing signup, consent, onboarding, activation | `USERJOURNEY/USERJOURNEY_STATE.json` when attached |

PROGRAMBUILD is the default workflow for every project. USERJOURNEY is optional and should be attached only when the product has real onboarding, consent, activation, or first-run routing work.

Repo boundary rule: PROGRAMSTART work stays inside this repo unless the user explicitly names another repo and asks you to work there.

PROGRAMBUILD tracks 11 stages from _inputs_ to _post-launch review_. When attached, USERJOURNEY tracks 9 phases from _product spec_ to _activation outcomes_.

Before planning, select the entry mode from `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`:

- **Raw idea** — little reliable planning/evidence exists.
- **Research-backed project** — substantial research exists and should be converted into durable project structure.
- **Existing / in-flight project** — current repository/product authority already exists; preserve its execution spine and propose explicit deltas instead of creating a second master plan.

---

## Day 1: Orient Yourself

```bash
# Run from the workspace root (cross-platform)
cd "c:\ PYTHON APPS\PROGRAMSTART"
uv run programstart next
```

`programstart next` prints your active stage, active phase, blockers, and the registry-backed baseline files/prompts for the current step. **This is the right orientation command.** The guide output is the allowed stage context, not an instruction to fully re-read every file for every small task.

### Windows shortcut

`scripts/pb.ps1` is a PowerShell convenience wrapper. It's equivalent to `uv run programstart <command>`. Use the `uv run` form for cross-platform compatibility.

```powershell
.\scripts\pb.ps1 next
```

Recommended local setup for the hardened toolchain:

```powershell
uv sync --extra dev
pre-commit install
python -m playwright install chromium
uv run programstart validate --check bootstrap-assets
uv run --extra dev pyright
```

Use `uv run --extra dev pyright` for local type checks. The pyright gate depends on dev-only tooling packages such as `nox`, `playwright`, and `pillow`, so `uv run pyright` is not the truthful command surface.

`nox -s smoke_readonly` runs the dashboard browser and golden smoke on both Windows and Linux. Windows smoke uses a higher golden diff budget to absorb Chromium rasterization differences while still checking the normalized shell and signoff modal surfaces.

`nox -s mutation` runs `mutmut` from the repo root, resets the generated `mutants/` workspace before each canonical run, and accepts an optional target filter argument when you want to narrow the run. On Windows, the session delegates through WSL, rebuilds a fresh `.nox/mutation-wsl` virtual environment, and still expects Ubuntu to have `python3-pip` and `python3-venv` installed. The session fails closed if `mutmut` returns without materializing real mutation outcomes in the metadata file.

If you want the tool outside a dev checkout, build and install the wheel:

```powershell
uv build
python -m pip install dist\programstart_workflow-*.whl
programstart next
```

Run the installed command from the planning repo root, or set `PROGRAMSTART_ROOT` before invoking it from another folder.

Or use **VS Code**: press `Ctrl+Shift+P` → **Tasks: Run Task** → **PROGRAMSTART: What To Do Next**

---

## The Day-to-Day Loop

PROGRAMBUILD now separates **strategic orientation** from the **immediate bounded work slice**.

```text
  pb next / pb guide
        ↓
  establish stage baseline + strategic next milestone
        ↓
  derive/refresh CURRENT_WORK_PACKET.md for non-trivial work
        ↓
  load only exact authority sections + specialist context needed now
        ↓
  reuse still-valid evidence; identify invalidation triggers
        ↓
  do the bounded work
        ↓
  run targeted verification for changed/at-risk surfaces
        ↓
  reconcile decisions/state into canonical authority
        ↓
  next packet OR wider stage/release convergence gate
```

### JIT source-of-truth check

`programstart jit-check --system programbuild` derives the current guide set, runs drift, and prints active sync rules. It is a **planning-authority baseline check**, especially useful before/after editing canonical planning or registry files and at convergence points.

Do not run it before and after every code-only slice solely for ceremony. For bounded implementation work, follow `product-jit-check.prompt.md` and the work packet's evidence/invalidation rules.

```powershell
.\scripts\pb.ps1 jit-check --system programbuild
# USERJOURNEY only if attached:
.\scripts\pb.ps1 jit-check --system userjourney
```

### Step 1 — Understand what's active

```powershell
.\scripts\pb.ps1 next
# or individually:
.\scripts\pb.ps1 state show
.\scripts\pb.ps1 guide --system programbuild
# USERJOURNEY only if attached:
.\scripts\pb.ps1 guide --system userjourney
```

The guide output defines the stage baseline. During implementation, the registry also surfaces `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` and `PROGRAMBUILD_WORK_PACKET.md` so the next immediate slice can be narrowed without losing authority.

### Step 2 — Define the immediate slice

For non-trivial implementation work, derive or refresh `CURRENT_WORK_PACKET.md` from `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md`.

A packet should contain:

- strategic execution spine/current stage
- one bounded objective
- explicit non-goals
- exact requirement IDs and authority sections needed now
- expected changed surfaces
- specialist references needed only for this slice
- trusted existing verification evidence
- invalidation triggers for that evidence
- acceptance criteria
- targeted verification

`CURRENT_WORK_PACKET.md` is optional derived execution state. It never becomes a second roadmap/game plan.

For a trivial task, state the same fields briefly instead of creating unnecessary ceremony.

### Step 3 — Do the work with task-scoped context

Read the relevant current sections named by the packet/slice, not every file in the stage in full.

If planned implementation would contradict current architecture, requirements, or a durable decision, update the canonical owner first and then refresh the packet.

Run `pb drift` before planning-authority/registry edits or when you need to confirm order/sync integrity:

```powershell
.\scripts\pb.ps1 drift
```

### Step 4 — Verify what changed

Do not default to the full suite after every small slice.

Ask:

1. What changed?
2. What contracts/requirements/behaviors could that invalidate?
3. Which prior evidence remains trustworthy because its invalidation trigger did not occur?
4. What is the smallest verification set that proves the changed/at-risk surface?

Examples:

- contract/auth change → relevant contract/auth/integration/alignment tests
- isolated internal refactor with unchanged contracts → focused unit/regression tests
- planning/registry authority change → full validation + drift
- stage transition / release → wider Challenge Gate or release convergence checks

For planning-authority or registry changes:

```powershell
.\scripts\pb.ps1 validate
.\scripts\pb.ps1 drift
```

### Step 5 — Close the packet and advance when appropriate

After a bounded slice:

- record the verification evidence actually produced
- reconcile material design/scope changes into canonical authority and `DECISION_LOG.md`
- replace/close the current packet instead of accumulating a second planning hierarchy
- derive the next packet from updated state

Only advance the PROGRAMBUILD stage when the **stage gate**, not merely one packet, is complete.

```powershell
# Preview first (never mutates state)
.\scripts\pb.ps1 advance --system programbuild --dry-run
# USERJOURNEY only if attached:
.\scripts\pb.ps1 advance --system userjourney --dry-run

# Then commit when the gate is truly satisfied
.\scripts\pb.ps1 advance --system programbuild --decision "approved" --notes "Stage criteria confirmed"
# USERJOURNEY only if attached:
.\scripts\pb.ps1 advance --system userjourney
```

The advance command records a dated sign-off and moves the next step to `in_progress`. CI will reject PR merges that skip this gate when CI is enabled.

> **Commit before you advance.** The preflight checks git-changed files. If you have modified
> files from the current stage that are not yet committed, the drift check will treat them as
> uncommitted future-stage content and block the advance. Run `git add -A && git commit` after
> completing each stage, then advance. If you are on a freshly bootstrapped project and have
> not yet made your first commit, run `git add -A && git commit -m "chore: bootstrap project"`
> before your first advance.

---

## Starting a New Project

Use the factory path to create a fresh standalone project repo in another folder:

```powershell
programstart create `
  --dest "C:\Projects\MyNewApp" `
  --project-name "MyNewApp" `
  --product-shape "API service" `
  --owner "Your Name"
```

This writes a generated kickoff plan to `outputs/factory/create-plan.md` inside the new repo.
It also writes `outputs/factory/provisioning-plan.md` so GitHub and project-scoped service dependencies stay attached to the generated repo instead of PROGRAMSTART.
It also writes a runnable starter scaffold under `starter/` based on the chosen product shape.
The destination must be outside the PROGRAMSTART repo, and the generated repo gets its own local git initialization automatically.

If you want the factory to create the GitHub remote and provision supported services too:

```powershell
programstart create `
  --dest "C:\Projects\MyNewApp" `
  --project-name "MyNewApp" `
  --product-shape "web app" `
  --github-repo "your-org/MyNewApp" `
  --create-github-repo `
  --provision-services `
  --supabase-org-id "your-supabase-org-id"
```

Set `SUPABASE_ACCESS_TOKEN` before the run if you want Supabase automation. Set `VERCEL_ACCESS_TOKEN` before the run if you want Vercel automation. Set `NEON_API_KEY` if you want Neon database automation for API/data-shaped repos. Web shapes infer both Supabase and Vercel automatically, API services infer Neon, and generated starters emit `.env.example` files with service-specific placeholders plus reusable third-party API env templates. The factory also writes `outputs/factory/setup-surface.md` so new repos have a concrete CLI/auth checklist instead of another blank setup pass. Additional services can still be declared with `--service`.

If you need the lower-level scaffold only, use bootstrap:

```powershell
.\scripts\pb.ps1 bootstrap `
  --dest "C:\Projects\MyNewApp" `
  --project-name "MyNewApp" `
  --variant product
```

Variants: `lite` (fast planning), `product` (full), `enterprise` (full + audit trail).

Run the planning operating model and Idea Intake before locking outputs. Choose `PRODUCT_SHAPE` in the kickoff packet, then decide whether USERJOURNEY is needed. If the project needs onboarding, consent, or activation planning, attach `USERJOURNEY/` separately from a project-specific source. It is not scaffolded by bootstrap.

Lower-level stamped path:

```powershell
programstart init `
  --dest "C:\Projects\MyNewApp" `
  --project-name "MyNewApp" `
  --product-shape "API service" `
  --one-line-description "Typed service for ..." `
  --owner "Your Name"
```

Then run:

```powershell
programstart validate --check engineering-ready
programstart prompt-eval --json
programstart impact PROGRAMBUILD/REQUIREMENTS.md
```

If the project later needs onboarding or activation planning:

```powershell
programstart attach userjourney --source "C:\ PYTHON APPS\PROGRAMSTART\USERJOURNEY"
```

---

## Applying PROGRAMBUILD to an Existing Project

Do not bootstrap a second planning hierarchy into an in-flight repository.

1. Identify the repository's existing canonical roadmap/game plan/current execution state.
2. Use **existing / in-flight project** mode from `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`.
3. Run Idea Intake as a delta audit, reusing current evidence rather than re-asking settled questions.
4. Convert new research/audits into explicit recommended deltas.
5. Adopt accepted deltas through the existing project's authority process.
6. During implementation, derive bounded work packets from that existing spine.

PROGRAMBUILD owns the reusable methodology. The real project owns its live plan and execution state.

---

## Emergency Reference Card

| Command | What it does |
|---------|-------------|
| `pb next` | Orient: status + active-step guide for both systems |
| `pb state show` | Show stage/phase and sign-off history |
| `pb validate` | Full workspace health check; use at authority/convergence gates, not automatically after every tiny slice |
| `pb advance --system <s> --dry-run` | Preview next advancement |
| `pb advance --system <s>` | Complete active step, move to next |
| `pb guide --system <s>` | Baseline files + prompts for active step |
| `pb jit-check --system <s>` | Guide + drift + sync-rule baseline for authority edits/convergence |
| `pb drift` | Check changed files for order/sync violations |
| `pb progress` | PROGRAMBUILD checklist % by section |
| `pb clean` | Remove disposable local caches and temp artifacts |
| `pb dashboard` | Regenerate `outputs/STATUS_DASHBOARD.md` |
| `pb status` | Detailed blockers and next actions |
| `pb help` | Full command list |
| `pb bootstrap` | Scaffold a new standalone project repo |
| `pb create` | One-shot factory create with generated kickoff and provisioning plans |
| `pb init` | Bootstrap and stamp a new standalone project repo |
| `pb recommend` | Recommend the right workflow variant and stacks |
| `pb impact <target>` | Show affected documents, concerns, and routes |
| `programstart next` | Same workflow surface without the PowerShell wrapper |
| `nox` | Run default sessions: lint, type, test, validate, smoke (readonly + isolated), docs |
| `nox -s quick` | Fast feedback: lint + typecheck only (~10s) |
| `nox -s gate_safe` | Local pre-merge gate: lint, typecheck, tests, validate, readonly smoke, docs |
| `nox -s ci` | Full CI-equivalent gate: everything including package and security |
| `nox -s mutation [target]` | Clean-slate mutation test pass from the repo root, with an optional target filter (Linux or WSL) |
| `mkdocs build --strict` | Build the searchable docs site |

---

## VS Code Tasks (Ctrl+Shift+P → Tasks: Run Task)

| Task | Equivalent command |
|------|--------------------|
| PROGRAMSTART: What To Do Next | `pb next` |
| PROGRAMSTART: Validate All | `pb validate` |
| PROGRAMSTART: Advance PROGRAMBUILD (dry-run) | `pb advance --system programbuild --dry-run` |
| PROGRAMSTART: Advance PROGRAMBUILD | `pb advance --system programbuild` |
| PROGRAMSTART: Advance USERJOURNEY (dry-run) | `pb advance --system userjourney --dry-run` |
| PROGRAMSTART: Advance USERJOURNEY | `pb advance --system userjourney` |
| PROGRAMSTART: Clean Workspace | `pb clean` |
| PROGRAMSTART: Refresh Dashboard | `pb dashboard` |

**Tip:** `Ctrl+Shift+B` runs **What To Do Next** directly (it's the default build task).

---

## The Authority Model (Why Editing Out of Order Fails)

```text
PROGRAMBUILD_CANONICAL.md
       │
       ├── one concern → one canonical owner
       ├── one project → one strategic execution spine
       └── derived packets/research/audits never silently replace authority

config/process-registry.json
       │
       ├── workflow_state     (which step is active + sign-off history)
       ├── workflow_guidance  (baseline files, scripts, prompts per step)
       ├── required_files     (files that must exist to pass validation)
       └── sync_rules         (which doc is source-of-truth for each concern)
```

- **Source of truth for a concern lives in exactly one file.** Downstream files reference it, never contradict it.
- **Strategic and immediate execution are different layers.** The roadmap/game plan owns strategic sequence; `CURRENT_WORK_PACKET.md` may describe only the current bounded slice.
- **You cannot advance until the prior step is approved** — the validator enforces this before CI merges when CI is active.
- **Drift check** catches edits to files that belong to a future stage before the current stage is signed off.
- **External implementation references must be explicitly allowlisted** in `USERJOURNEY/USERJOURNEY_INTEGRITY_REFERENCE.json` before they can appear in tracked USERJOURNEY planning docs.

---

## Current Active State

Run `pb state show` or open `outputs/STATUS_DASHBOARD.md` to see live state.

Generated PROGRAMBUILD-only repos are valid. If USERJOURNEY is not attached, the tools will report that explicitly instead of treating it as an error.
