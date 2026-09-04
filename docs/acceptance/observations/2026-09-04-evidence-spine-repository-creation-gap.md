# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-04 UTC
- **Project / repository:** proposed `GrahamArdent/evidence-spine`; control evidence in `GrahamArdent/execution-node-control`
- **PROGRAMSTART lesson ID:** none — direct retest of the current Effective Autonomy `temporary_automation_gap` rule
- **Checkpoint / acceptance surface:** explicit greenfield repository-creation autonomy test
- **Classification:** confirmation with owner-routed infrastructure gap

## What happened

Evidence Spine was explicitly authorized as a new repository and the operator required autonomous repository creation to be attempted before requesting any manual setup.

The connected GitHub capability could inspect and mutate existing repositories but exposed no repository-create operation. A first Execution Node bootstrap preflight was rejected before privileged dispatch because `bootstrap_exec_v0` requires risk class 3. The corrected read-only preflight passed and proved `gh`, `git`, and `uv` were installed, but the root/bootstrap environment had no GitHub CLI login and no local PROGRAMSTART checkout. Current Secrets authority also keeps supervised personal `gh` sessions outside unattended machine authority.

The repository-create step is therefore mechanical, already authorized, and currently unavailable only because no accepted machine identity/tool surface has account-level repository-creation capability. It is a `temporary_automation_gap`, not a genuine human judgment gate.

Independent safe work continued: the V0.1 Evidence Spine architecture, schemas, code, P0-02 normalization fixture, tests, Challenge findings, and required governance artifacts were prepared locally without widening credentials or asking the operator to shuttle files/commands.

## Evidence

- target repository lookup: `GrahamArdent/evidence-spine` not found at the start of the test;
- Execution Node rejected preflight result: commit `283bfa178cc6d56eb79b06e5d10837b564d5f092` — rejected before privileged dispatch because `risk_class must equal 3 for action bootstrap_exec_v0`;
- corrected preflight request: `GrahamArdent/execution-node-control` commit `98022b1b13b0c503a85d19f3404d4c98b1c9a4bf`;
- corrected preflight result: commit `eef37d51f0d70feb72376c89746c89ed252ac55f` — PASS, proving `/usr/bin/gh`, `/usr/bin/git`, `/usr/local/bin/uv`, no root/bootstrap GitHub login, and no discovered local PROGRAMSTART checkout;
- current PROGRAMSTART commit `330aa70508113c63b3f85f449dd152648fc3681a` already requires classification of `temporary_automation_gap` vs `genuine_human_gate`;
- prepared Evidence Spine V0.1 preflight: 32 deterministic tests passed plus compile/validate/reconcile/derived-state verification.

Checks not performed / unavailable:

- no account-level machine GitHub token/session was read, copied, or created;
- Graham's personal `gh` session was not borrowed for unattended execution;
- no provider permission was widened;
- no remote Evidence Spine CI could run because the repository does not yet exist.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** classified current-environment inability as an automation gap, preserved consequence/security boundaries, continued independent safe work, and reduced the fallback action to the smallest mechanical step.
- **What helped:** the new Effective Autonomy distinction prevented a tooling limitation from being mislabeled as a permanent human gate; Mode-C safe-lane behavior prevented the missing remote from blocking architecture/code/test preparation.
- **What created friction or uncertainty:** the PROGRAMSTART greenfield factory supports GitHub repository creation when authenticated `gh` is available, but the current connected/Execution Node identity fabric does not expose an accepted account-level repository-create capability.
- **Was existing methodology sufficient?** yes. The defect is currently in execution/identity capability, not in the methodology rule.

## Learning decision

- **Existing lesson match:** current Effective Autonomy manual-boundary-origin rule introduced by PR #92; also consistent with credentialless-first owner routing in Secrets.
- **Maturity before:** implemented methodology rule / real retest open
- **Maturity after:** no methodology change; additional confirming retest evidence
- **Why the evidence changes or does not change maturity:** this case independently confirms the distinction on an account-level GitHub operation, while revealing a concrete execution-identity gap. It does not show a missing lifecycle or governance primitive.
- **PROGRAMSTART change required now:** none. Route the capability gap to the owning GitHub machine-identity/execution-fabric work when that owner is next reconciled; do not create a credential merely to make the Evidence Spine bootstrap aesthetically autonomous.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** a future authorized greenfield project where the connected or machine GitHub surface has repository-create authority.
- **What evidence would be sufficient:** unattended creation of the exact repository under bounded machine identity, followed by normal PROGRAMSTART bootstrap without operator transport; or counterevidence showing repository creation intrinsically requires a genuine human authorization boundary.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] No unnecessary PROGRAMSTART methodology change was manufactured.
