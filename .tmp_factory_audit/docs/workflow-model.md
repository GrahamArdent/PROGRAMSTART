# Workflow Model

PROGRAMSTART has two workflow layers:

- `PROGRAMBUILD/` is the reusable template core.
- `USERJOURNEY/` is an optional project attachment for onboarding, consent, activation, and first-run routing work.

The machine-readable source of truth is `config/process-registry.json`.

Key operating rules:

- choose `PRODUCT_SHAPE` before picking stack-specific implementation details
- choose the lightest variant that still matches project risk
- attach `USERJOURNEY/` only when real end-user journey design exists
- prefer `programstart init` over raw bootstrap when starting a new project because it stamps kickoff inputs and reduces manual setup drift
- use `programstart recommend` before filling architecture when stack direction is still ambiguous
- use `programstart impact <target>` before editing authority docs to understand downstream blast radius
- validate both the template repo and a freshly bootstrapped repo

Primary operator surface:

- use `uv run programstart ...` as the cross-platform workflow entry point
- treat `scripts/pb.ps1` as a thin Windows convenience wrapper over the unified CLI
