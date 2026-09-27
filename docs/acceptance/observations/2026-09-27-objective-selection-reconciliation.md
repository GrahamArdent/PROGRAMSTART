# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-27
- **Project / repository:** PROGRAMSTART / programstart-autonomous-controller / Secrets Control Plane
- **PROGRAMSTART lesson ID:** proposed PSL-024
- **Checkpoint / acceptance surface:** objective re-entry after dependency/currentness repair
- **Classification:** systemic

## What happened

A durable Secrets #48 Controller root remained valid while the operator's foreground objective had moved to PROGRAMSTART #158 HOPS convergence. After subordinate Controller/Execution Node dependencies were repaired, the preserved #48 root was awakened and began driving Secrets/Govee/Infisical lifecycle observations. The root was valid, but it was no longer the foreground-selected objective. This caused technically correct continuation machinery to pursue an independent objective and made unrelated credential health appear to block HOPS.

The operator identified the mismatch. JIT reconciliation confirmed Secrets #48 is independently valid and relevant to HOP-018/HOP-031, but is not a prerequisite for unrelated HOPS rows. #48 was parked and #158 was re-entered through the admitted objective ingress.

## Evidence

- repository / PR / commit / run / provider / runtime evidence:
  - GrahamArdent/PROGRAMSTART#158
  - GrahamArdent/secrets-control-plane#48
  - GrahamArdent/programstart-autonomous-controller#128
  - GrahamArdent/programstart-autonomous-controller#167
  - GrahamArdent/execution-node-control#251
  - PROGRAMSTART #158 reconciliation comment 5851323179
  - execution-node semantic result req-spine-bc8e3abcc640d7316db3-programstart-semantic-produce
- exact current state relevant to the observation:
  - #158 is the HOPS convergence wrapper.
  - #48 remains an independent durable root.
  - #48 credential health must not become an unrelated HOPS prerequisite.
- verification actually performed:
  - current #158 authority/body read;
  - current 37-row matrix read;
  - current Learning Loop/ledger read;
  - admitted objective ingress re-entered #158;
  - semantic producer returned PASS/converged with the independence constraint.
- checks not performed / unavailable:
  - no claim yet that Controller runtime itself enforces objective-selection reconciliation before every consequence.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** preserved a valid durable root and correctly resumed it after dependency repair.
- **What helped:** root durability, JIT authority/currentness, fail-closed ingress, and semantic continuation all behaved as designed locally.
- **What created friction or uncertainty:** root validity was implicitly treated as sufficient for foreground continuation. Current selection/eligibility was not independently proven before the awakened root produced new consequences.
- **Was existing methodology sufficient?** partially

## Learning decision

- **Existing lesson match:** PSL-011 is related to re-entry but does not distinguish durable validity from foreground selection; PSL-008 permits multiple legitimate lanes but does not govern awakened-root consequence eligibility.
- **Maturity before:** none
- **Maturity after:** candidate
- **Why the evidence changes or does not change maturity:** this is a material cross-owner misrouting class that can recur whenever blocked durable objectives awaken after operator focus changes. It is broader than Secrets/HOPS and directly affects autonomous consequence selection.
- **PROGRAMSTART change required now:** bounded objective-selection reconciliation contract using existing Controller/OCP machinery; no second orchestrator or global single-active-objective service.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** Root A is durably blocked/parked; operator selects independent Root B; A's dependency later clears.
- **What evidence would be sufficient:** A remains durable but does not produce a new consequence unless current selection/eligibility proves it may; B remains foreground; safe explicitly admitted parallel roots may still proceed.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] If no reusable lesson was found, no unnecessary PROGRAMSTART change was manufactured.
