# PROGRAMSTART Learning Observation — Autonomy-Parity Capability Recovery

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-25
- **Project / repository:** autonomy-parity first live integration across `GrahamArdent/ecosystem-contracts`, `GrahamArdent/execution-node-control`, and Controller
- **PROGRAMSTART lesson ID:** `PSL-021`
- **Checkpoint / acceptance surface:** credential/access Human Enablement retest during the accepted `ecosystem-contracts` first-live integration
- **Classification:** confirmation with materially stronger evidence

## What happened

The first pass incorrectly treated the GitHub connector's lack of deploy-key administration as evidence that a human authorization gate might remain.

A broader capability search then found that the Execution Node already had an authenticated `gh` CLI identity with repository scope and provider access sufficient to read `ecosystem-contracts` deploy-key metadata. That meant the connector limitation was only a tool-surface limitation, not proof of a genuine human gate.

Separately, a missing `sqlite3` CLI on the VPS was initially routed around using Python's built-in SQLite support. The operator correctly challenged that default because `sqlite3` is a small, reusable host capability. The CLI was then installed and mechanically verified instead of preserving the missing-tool condition.

## Evidence

- PROGRAMSTART #141 selected `credential_human_enablement_leverage` and `GrahamArdent/ecosystem-contracts` as the first live integration.
- Private ingress request `req-programstart-objective-parity-20260925-034050` created run `intent-f35e8a4a15e1e8ab`; the run stopped with `no_admitted_semantic_effect_derivation`, not a human gate.
- Read-only provider capability check through the existing authenticated `gh` CLI successfully returned `ecosystem-contracts` deploy-key metadata without exposing token or key values.
- At that checkpoint, no deploy key was registered for the target repository.
- VPS `sqlite3` was installed and verified as version `3.46.1`.
- `ecosystem-contracts` PR #25 merged as `5c82dc21dba59586dcfa35a890775104ddcb2ad6`; exact-main Contract Validation run `36093187467` passed.
- Execution Node PR #226 merged as `6051b8fcff6bf1fe9cef52ec176ebec1f32d3439`; PR CI run `36093993464` passed and exact-main workflow-dispatch run `36094179848` passed.
- No human credential value, private key, token, or secret was requested in chat.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** required capability recovery and alternative-actuation search before declaring a credential/access human gate.
- **What helped:** the existing PSL-021 rule caused the search to expand beyond the first connector surface and preserve the distinction between a provider authorization boundary and a missing tool surface.
- **What created friction or uncertainty:** the first diagnostic path over-weighted the currently visible connector and initially treated a missing reusable CLI as something to route around rather than a capability gap worth cheaply eliminating.
- **Was existing methodology sufficient?** partially. PSL-021 already required broader capability search, but this run adds concrete evidence that search must include authenticated CLIs and that cheap reusable host-tool installation should be considered as bounded capability repair when owner authority permits.

## Learning decision

- **Existing lesson match:** `PSL-021`.
- **Maturity before:** `implemented` in the current concise rollup, with older detailed evidence already describing validation.
- **Maturity after:** no central-rollup change in this observation because active PROGRAMSTART PRs concurrently modify the learning ledger.
- **Why the evidence changes or does not change maturity:** this is the exact preferred `ecosystem-contracts` credential/access retest named by PSL-021 and it materially strengthens the lesson, but shared-mutation ownership requires the central rollup to be reconciled by the existing ledger lane.
- **PROGRAMSTART change required now:** no new lesson ID or new subsystem. Reconcile the stronger evidence into PSL-021 when the current ledger mutation lane is free. Treat cheap reusable host CLI installation as an option inside existing temporary-automation-gap/capability-debt handling, not as permission to install arbitrary tooling.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** another credential/access boundary where the first visible tool lacks an action but another accepted CLI/API/runtime path may exist, or where a small missing reusable utility can be safely installed.
- **What evidence would be sufficient:** the system searches accepted capability surfaces before escalating, distinguishes absent connector action from absent authority, installs a bounded reusable utility only when justified by owner authority and durability, preserves secret boundaries, and requests human action only if a genuine irreducible authorization remains.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] No unnecessary new PROGRAMSTART lesson ID was manufactured.
