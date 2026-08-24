# PROGRAMBUILD_CHECKLIST.md

# Program Build Execution Checklist

Use this when checklist form is useful. Do not complete boxes that are irrelevant solely for ceremony; follow the authority/risk rules in `PROGRAMBUILD_CANONICAL.md`, `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, `PROGRAMBUILD_CHALLENGE_GATE.md`, and `PROGRAMBUILD_WORK_PACKET.md`.

---

## 1. Setup / Entry

- [ ] select raw-idea, research-backed, or existing-project entry mode
- [ ] for an existing project, identify its strategic execution spine first
- [ ] run the relevant Idea Intake dimensions, reusing settled current evidence
- [ ] choose PRODUCT_SHAPE and Lite/Product/Enterprise rigor
- [ ] attach USERJOURNEY only when its problem actually exists
- [ ] confirm one strategic execution spine
- [ ] establish live orientation with registry-backed status/guide output
- [ ] if resuming after a meaningful pause/change, run risk/invalidation-based re-entry

---

## 2. Feasibility

- [ ] run the stage/risk-relevant Challenge Gate for Stage 0 → 1
- [ ] define/update `FEASIBILITY.md`
- [ ] define observable kill/reshape criteria
- [ ] estimate effort/cost only to support the decision
- [ ] record go / limited spike / no-go

---

## 3. Research

- [ ] run the relevant Stage 1 → 2 gate controls
- [ ] gather only research that reduces material uncertainty
- [ ] reuse current internal evidence before duplicating research
- [ ] produce a summary or scoped delta
- [ ] record low-confidence decisions/spikes
- [ ] keep research subordinate until adopted into project authority

---

## 4. Requirements / UX

- [ ] run relevant Stage 2 → 3 gate controls
- [ ] define/update P0 requirements with measurable acceptance criteria
- [ ] define flows only where direct/operator/service interaction requires them
- [ ] preserve exclusions and success metric
- [ ] confirm no feasibility kill criterion became true

---

## 5. Architecture / Risk Spikes

- [ ] run relevant Stage 3 → 4 gate controls
- [ ] define architecture for the actual PRODUCT_SHAPE
- [ ] make material contract/data/trust boundaries explicit
- [ ] identify only material unknowns
- [ ] run the smallest useful spikes for blocking uncertainty
- [ ] check dependency/vendor/research freshness when material
- [ ] record durable decisions; use ADR only when the current ADR policy warrants it

---

## 6. Scaffold / Guardrails

- [ ] run relevant Stage 4 → 5 gate controls
- [ ] scaffold only what architecture requires
- [ ] establish dominant contract/trust boundaries
- [ ] add structural tests that prevent real drift classes
- [ ] configure local/CI verification appropriate to risk and repository activity
- [ ] preserve repo-boundary consent for cross-repository AI work

---

## 7. Test Strategy

- [ ] run relevant Stage 5 → 6 gate controls
- [ ] define a test portfolio appropriate to product shape/risk
- [ ] ensure every P0 outcome has meaningful proof
- [ ] map material contracts to tests where drift risk warrants it
- [ ] define smoke/regression/golden/E2E only where they add signal
- [ ] define evidence reuse + invalidation for expensive/stateful checks

---

## 8. Implementation Loop

For each coherent slice:

- [ ] run relevant Stage 6 → 7 gate controls before entering implementation
- [ ] define the compact logical work-packet fields from `PROGRAMBUILD_WORK_PACKET.md`
- [ ] persist `CURRENT_WORK_PACKET.md` only if persistence materially improves coordination/risk/resumption
- [ ] trace the slice to current authority and exact relevant requirements/contracts
- [ ] load only task-relevant authority/specialist context
- [ ] list reusable evidence + invalidation triggers
- [ ] define acceptance criteria + smallest sufficient verification set
- [ ] implement without prospectively contradicting canonical authority
- [ ] update governed registries/contracts only when their surface changes
- [ ] run targeted verification plus broader checks triggered by invalidation/convergence
- [ ] record evidence once
- [ ] reconcile material decisions/scope/architecture/status
- [ ] close/replace the packet; do not accumulate a parallel plan
- [ ] widen to a mid-implementation Challenge Gate when accumulated change/risk makes the narrow slice view insufficient

---

## 9. Release Readiness

- [ ] run full Product A–H or Enterprise convergence for Stage 7 → 8; Lite uses its required/risk-relevant controls
- [ ] create/update `RELEASE_READINESS.md`
- [ ] verify deployment/rollback
- [ ] verify environment/config/secrets where applicable
- [ ] verify required observability/support ownership
- [ ] verify critical smoke/purpose outcomes
- [ ] re-establish release-critical evidence that was invalidated
- [ ] record go / no-go

---

## 10. Audit / Drift

- [ ] run relevant Stage 8 → 9 gate controls
- [ ] create/update `AUDIT_REPORT.md`
- [ ] audit material contract/auth/schema/behavior/evidence/authority drift
- [ ] give critical/high findings owners/fixes/risk acceptance
- [ ] keep audit findings as evidence until adopted into canonical authority

---

## 11. Post-Launch

- [ ] compare outcomes with the success metric
- [ ] capture incidents/support/adoption gaps
- [ ] record decision reversals/confirmations
- [ ] assign meaningful follow-up ownership
- [ ] propose PROGRAMBUILD changes only for systemic/reusable prevention opportunities
- [ ] do not convert a fixed project-count threshold into methodology truth

---

## 12. Governance / Efficiency Checks

- [ ] one strategic execution spine exists
- [ ] authority ownership is clear
- [ ] no research/audit/checklist/packet is acting as a second master plan
- [ ] persisted `CURRENT_WORK_PACKET.md`, if present, is actually helping coordination/resumption
- [ ] evidence is reused until a relevant invalidation trigger occurs
- [ ] broad verification runs only for a real convergence reason
- [ ] specialist agents are used only when decomposition/review value justifies them
- [ ] no universal numeric/time threshold is being substituted for risk judgment
- [ ] project-specific state is not stored in reusable PROGRAMSTART methodology

---

## 13. Gate Result

Use the log/advance mechanism from `PROGRAMBUILD_CHALLENGE_GATE.md`.

Record:
- gate parts actually run;
- clear / warning / blocked;
- material evidence reused/invalidated;
- reconciliation required;
- whether stage advance is permitted.

Do not duplicate the full gate prose in this checklist.

---

Last updated: 2026-08-24
