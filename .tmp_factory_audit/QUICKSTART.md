# PROGRAMSTART — Quick Start Guide

> You're in the right place if you're starting a new product or building to a repeated standard.
> This workspace is a reusable planning kit — it guides you from idea to launch without losing context.

---

## Workflow Modes

| System | Use it when... | Key state file |
|--------|----------------|----------------|
| **PROGRAMBUILD** | Defining scope, architecture, testing, release readiness | `PROGRAMBUILD/PROGRAMBUILD_STATE.json` |
| **USERJOURNEY** | Designing signup, consent, onboarding, activation | `USERJOURNEY/USERJOURNEY_STATE.json` when attached |

PROGRAMBUILD is the default workflow for every project. USERJOURNEY is optional and should be attached only when the product has real onboarding, consent, activation, or first-run routing work.

PROGRAMBUILD tracks 11 stages from _inputs_ to _audit_. When attached, USERJOURNEY tracks 9 phases from _product spec_ to _activation outcomes_.

---

## Day 1: Orient Yourself

```powershell
# Run from the workspace root
cd "c:\ PYTHON APPS\PROGRAMSTART"
.\scripts\pb.ps1 next
```

`pb next` prints your active stage, active phase, any blockers, and the exact files and prompts to work with right now. **This is always the right starting command.**

Recommended local setup for the hardened toolchain:

```powershell
uv sync --extra dev
pre-commit install
python -m playwright install chromium
uv run programstart validate --check bootstrap-assets
```

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

```
  ┌─────────────────────────────────────────────┐
  │  pb next          ← "where am I & what now?" │
  │  (do the work in the listed authority files) │
  │  pb validate      ← "is everything correct?" │
  │  pb advance       ← "I'm done, move forward" │
  └─────────────────────────────────────────────┘
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

### Step 2 — Do the work

Edit the files listed by `pb guide`. The registry knows which files belong to which stage — editing out-of-order files triggers a drift warning.

```powershell
.\scripts\pb.ps1 drift        # checks any recently changed files for order violations
```

### Step 3 — Validate before advancing

```powershell
.\scripts\pb.ps1 validate                       # all checks
.\scripts\pb.ps1 validate --check workflow-state  # state coherence only
```

### Step 4 — Advance to the next stage/phase

```powershell
# Preview first (never mutates state)
.\scripts\pb.ps1 advance --system programbuild --dry-run
# USERJOURNEY only if attached:
.\scripts\pb.ps1 advance --system userjourney --dry-run

# Then commit
.\scripts\pb.ps1 advance --system programbuild --decision "approved" --notes "Feasibility confirmed"
# USERJOURNEY only if attached:
.\scripts\pb.ps1 advance --system userjourney
```

The advance command records a dated sign-off and moves the next step to `in_progress`. CI will reject PR merges that skip this gate.

---

## Starting a New Project

Use bootstrap to create a fresh planning package in another folder:

```powershell
.\scripts\pb.ps1 bootstrap `
  --dest "C:\Projects\MyNewApp" `
  --project-name "MyNewApp" `
  --variant product
```

Variants: `lite` (fast planning), `product` (full), `enterprise` (full + audit trail).

Choose `PRODUCT_SHAPE` in the kickoff packet before you start filling outputs. Then decide whether USERJOURNEY is needed. If the project needs onboarding, consent, or activation planning, attach `USERJOURNEY/` separately from a project-specific source. It is not scaffolded by bootstrap.

Faster path:

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
programstart recommend
programstart impact PROGRAMBUILD/REQUIREMENTS.md
```

If the project later needs onboarding or activation planning:

```powershell
programstart attach userjourney --source "C:\ PYTHON APPS\PROGRAMSTART\USERJOURNEY"
```

---

## Emergency Reference Card

| Command | What it does |
|---------|-------------|
| `pb next` | Orient: status + active-step guide for both systems |
| `pb state show` | Show stage/phase and sign-off history |
| `pb validate` | Full workspace health check |
| `pb advance --system <s> --dry-run` | Preview next advancement |
| `pb advance --system <s>` | Complete active step, move to next |
| `pb guide --system <s>` | Files + prompts for active step |
| `pb drift` | Check changed files for order violations |
| `pb progress` | PROGRAMBUILD checklist % by section |
| `pb clean` | Remove disposable local caches and temp artifacts |
| `pb dashboard` | Regenerate `outputs/STATUS_DASHBOARD.md` |
| `pb status` | Detailed blockers and next actions |
| `pb help` | Full command list |
| `pb bootstrap` | Scaffold a new project package |
| `pb init` | Bootstrap and stamp a new project package |
| `pb recommend` | Recommend the right workflow variant and stacks |
| `pb impact <target>` | Show affected documents, concerns, and routes |
| `programstart next` | Same workflow surface without the PowerShell wrapper |
| `nox` | Run lint, type, test, smoke, and docs sessions |
| `nox -s ci` | Run the full local CI-equivalent gate, including package and security checks |
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

```
config/process-registry.json
       │
       ├── workflow_state  (which step is active + sign-off history)
       ├── workflow_guidance (files, scripts, prompts per step)
       ├── required_files  (all files that must exist to pass validation)
       └── sync_rules      (which doc is source-of-truth for each concern)
```

- **Source of truth for a concern lives in exactly one file.** Downstream files reference it, never contradict it.
- **You cannot advance until the prior step is approved** — the validator enforces this before CI merges.
- **Drift check** catches edits to files that belong to a future stage before the current stage is signed off.
- **External implementation references must be explicitly allowlisted** in `USERJOURNEY/USERJOURNEY_INTEGRITY_REFERENCE.json` before they can appear in the tracked USERJOURNEY planning docs.

---

## Current Active State

Run `pb state show` or open `outputs/STATUS_DASHBOARD.md` to see live state.

Generated PROGRAMBUILD-only repos are valid. If USERJOURNEY is not attached, the tools will report that explicitly instead of treating it as an error.
