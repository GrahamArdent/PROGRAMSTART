# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-25
- **Project / repository:** GrahamArdent/decision-lifecycle
- **PROGRAMSTART lesson ID:** proposed PSL-024
- **Checkpoint / acceptance surface:** Mode-B factory bootstrap → first durable baseline → Stage 0/5/6 transitions in a generated Product/API-service repository
- **Classification:** systemic

## What happened

A real PROGRAMSTART-created repository reached multiple false or avoidable control-plane failures that were not Decision Lifecycle product defects:

1. Before the first baseline commit, generated future-stage placeholder files were all treated as changed/premature work by stage preflight.
2. The generated child inherited template self-test CI. Its compatibility matrix attempted to factory-create other product shapes and expected an attached USERJOURNEY even though this child correctly had no USERJOURNEY.
3. The child inherited a template-inventory validator that rejected the child's own new product CI file because it was not a template bootstrap asset.
4. The child inherited CodeQL workflow configuration that could not complete for this private repository because GitHub Code Security was not enabled; a locally available security gate was sufficient for P0.
5. A fresh child worktree running the supported `programstart advance` command failed because `jsonschema` was unavailable until the development extra was synced, even though the command itself depended on it.

The project progressed only after explicitly establishing a baseline and adapting the generated repository's controls to child-repo reality.

## Evidence

- repository / PR / commit / run / provider / runtime evidence:
  - GrahamArdent/decision-lifecycle PR #11
  - merged scaffold commit `3856c01297b2bf560fb5b734388355e59ebea951`
  - failing CI Guardrails run #11: factory dry-run failed because USERJOURNEY was absent
  - subsequent generated-repo CI Guardrails runs became green across Linux/Windows and Python 3.12–3.14 after removing template-only assumptions
  - CodeQL run failed at SARIF upload because code scanning was not enabled for the private repository; product Bandit scan passed with zero findings
  - fresh `decision-lifecycle-test-strategy` worktree reproduced `ModuleNotFoundError: jsonschema` during `programstart advance` before `uv sync --extra dev`
- exact current state relevant to the observation:
  - Decision Lifecycle scaffold is merged and Stage 6/test-strategy work is active.
  - Child-specific product CI and generated-repo guardrails are green.
  - PROGRAMSTART main remains at `947730fa08552d5e94e777e071218a0d325ce324` for this observation.
- verification actually performed:
  - reproduced the same PROGRAMSTART authority-sync defect on PROGRAMSTART main before using a bounded child preflight bypass;
  - proved scaffold/product checks locally and remotely;
  - verified the stale local planning branch tree was identical before reusing/resetting it;
  - verified the fresh worktree dependency failure and successful recovery after syncing the dev environment.
- checks not performed / unavailable:
  - no claim that GitHub CodeQL code-scanning upload succeeded; it did not.
  - no PROGRAMSTART factory/bootstrap implementation change is claimed by this observation.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** Correctly selected Mode B, provided bootstrap/adoption machinery, stage gates, architecture/test validators, and bounded preflight bypass. Its generated repository also retained template-era controls and bootstrap assumptions that were not valid after the child became an independent project.
- **What helped:** Stage-specific validators, challenge/advance machinery, generated planning authority, and the ability to continue with a scoped preflight bypass.
- **What created friction or uncertainty:** No explicit generated-repo transition contract established a baseline, child-specific validation/CI profile, and self-contained operational CLI environment before stage gates began.
- **Was existing methodology sufficient?** partially

## Learning decision

- **Existing lesson match:** PSL-001 covers lean greenfield bootstrap but not post-bootstrap child operability; PSL-004 covers environment-aware orchestration but not factory materialization of child-specific controls; PSL-022 covers publication gates but not generated-repo bootstrap identity.
- **Maturity before:** none
- **Maturity after:** candidate
- **Why the evidence changes or does not change maturity:** Multiple independently observed failures shared one owner/surface: the transition from PROGRAMSTART template/factory state to an independent generated repository. The failures caused false gates and manual recovery in a real project, and the corrected child profile immediately removed them.
- **PROGRAMSTART change required now:** bounded change + owner — factory/bootstrap should establish a child-repo transition contract that (a) creates/recognizes a clean baseline before change-sensitive stage checks, (b) materializes generated-repo CI/validators rather than template self-tests, and (c) ensures supported child CLI commands have their required runtime environment/dependencies.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** the next PROGRAMSTART-created Product/API/CLI repository should move from factory creation through first stage advancement and first PR without editing inherited template CI, adding a fake USERJOURNEY, manually creating a baseline solely to placate future-step checks, or discovering a missing runtime dependency.
- **What evidence would be sufficient:** fresh generated repo; clean first stage gate; child-scoped CI green on its own shape; supported `programstart status/guide/advance` commands run from the documented one-command environment; no template-only factory/bootstrap test is required inside the child.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] If no reusable lesson was found, no unnecessary PROGRAMSTART change was manufactured.
