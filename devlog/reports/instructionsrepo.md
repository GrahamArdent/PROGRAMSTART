# Durable JIT-Check Design And Automation Analysis

Purpose: Capture the shortest defensible instructions for the durable `jit-check` design, plus a critical view of what should and should not be automated.
Status: Analysis and operator instructions only. No implementation is approved by this document.
Basis: Review of the current PROGRAMSTART CLI, command registry, wrapper script, and VS Code task surface, along with the attached PROGRAMBUILD adoption now present in Orchestra Agent.
Last updated: 2026-04-16

---

## Short Answer

Do **not** solve this with another standalone script.

The durable design is:

1. add `jit-check` as a real `programstart` CLI command in PROGRAMSTART,
2. make the VS Code task call that command,
3. sync the small changed file set into Orchestra Agent,
4. verify it there.

Everything else is detail.

---

## Minimum Steps

These are the fewest steps that still make architectural sense.

### Step 1: Implement it in PROGRAMSTART

Workspace:

- `C:\ PYTHON APPS\PROGRAMSTART`

Terminal:

- terminal opened in `C:\ PYTHON APPS\PROGRAMSTART`

Do this:

- add `jit-check` to `scripts/programstart_command_registry.py`
- implement the real sequence in `scripts/programstart_cli.py`
- update `.vscode/tasks.json` so `PROGRAMSTART: JIT Check` calls `uv run programstart jit-check --system programbuild`
- add the minimal tests in `tests/test_programstart_command_registry.py` and `tests/test_programstart_cli.py`

Critical reason:

- the command belongs in the CLI control plane, not in `pb.ps1` and not only in tasks.

### Step 2: Verify it in PROGRAMSTART

Workspace:

- `C:\ PYTHON APPS\PROGRAMSTART`

Terminal:

- terminal opened in `C:\ PYTHON APPS\PROGRAMSTART`

Run:

```powershell
uv run pytest tests/test_programstart_command_registry.py tests/test_programstart_cli.py
uv run programstart validate
uv run programstart drift
```

Critical reason:

- if it is not authoritative and clean in PROGRAMSTART first, it should not be propagated anywhere.

### Step 3: Sync only the changed files into Orchestra Agent

Workspace:

- `C:\PYTHON APPS\Orchestra Agent`

Terminal:

- terminal opened in `C:\PYTHON APPS\Orchestra Agent`

Sync only:

- `scripts/programstart_command_registry.py`
- `scripts/programstart_cli.py`
- `tests/test_programstart_command_registry.py`
- `tests/test_programstart_cli.py`
- `.vscode/tasks.json` if changed

Critical reason:

- reattaching the whole structure for one command is bad discipline and too much blast radius.

### Step 4: Verify it in Orchestra Agent

Workspace:

- `C:\PYTHON APPS\Orchestra Agent`

Terminal:

- terminal opened in `C:\PYTHON APPS\Orchestra Agent`

Run:

```powershell
uv run pytest tests/test_programstart_command_registry.py tests/test_programstart_cli.py
uv run programstart validate
uv run programstart drift
uv run programstart jit-check --system programbuild
```

Optional wrapper check:

```powershell
.\scripts\pb.ps1 jit-check --system programbuild
```

Critical reason:

- Orchestra Agent is downstream. It should consume the authoritative change, not invent its own variant.

---

## Critical Cuts

If you are trying to keep this minimal, cut these first:

- Do not write a new standalone script.
- Do not treat `pb.ps1` as the implementation site.
- Do not keep the real logic only in `.vscode/tasks.json`.
- Do not reattach the whole PROGRAMBUILD structure to Orchestra Agent for this one change.
- Do not implement it in Orchestra Agent first.

Those are all attractive shortcuts, but they are the wrong shortcuts.

---

## Automation View

### What is worth automating

1. The operator sequence itself.
  Best form: `programstart jit-check`.

2. The downstream verification sequence.
  Best form: a fixed check bundle in Orchestra Agent after syncing the small file set.

### What is not worth automating blindly

1. Full repo reattach for small tooling changes.
  Reason: too much blast radius.

2. Generic auto-propagation from PROGRAMSTART into Orchestra Agent.
  Reason: too much hidden coupling.

3. Heuristic file selection for downstream sync.
  Reason: eventually it will overwrite host-repo intent.

### Most defensible automation shape

If you automate anything beyond the CLI command itself, the best shape is:

1. implement `jit-check` in the CLI,
2. define a **small explicit manifest** for the files that own that command,
3. automate copy plus verification for only those files,
4. keep the decision to sync into Orchestra Agent explicit.

That is the only automation path here that is both useful and disciplined.

---

## Bottom Line

The fewest defensible steps are:

1. build `jit-check` as a real CLI command in PROGRAMSTART,
2. verify it there,
3. sync only the changed command files into Orchestra Agent,
4. verify it there.

Anything shorter than that stops being durable and starts becoming a shortcut that will drift.