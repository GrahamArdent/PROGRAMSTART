# PROGRAMBUILD_CHECKLIST.md

# Program Build Execution Checklist

Use this when checklist form is useful. Do not complete boxes that are irrelevant solely for ceremony; follow the authority/risk rules in `PROGRAMBUILD_CANONICAL.md`, `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, `PROGRAMBUILD_CHALLENGE_GATE.md`, and `PROGRAMBUILD_WORK_PACKET.md`.

A checklist is a **derived completeness / verification surface**. It does not own strategy, scope, sequencing, architecture, or project state.

- Authority answers **what matters**.
- The active work packet answers **what is being done now**.
- An applicable checklist answers **which already-authorized obligations must be accounted for before truthful closure**.

Use a checklist when omission risk is meaningful or when an existing applicable checklist already governs the current boundary. Do not create a large persisted checklist for a trivial, low-risk, single-step change merely because a checklist template exists.

When a checklist is used:

1. derive items from current authority, acceptance criteria, risk/gate obligations, declared handoffs, and other existing requirements;
2. cross-reference the source of material obligations when practical;
3. never let a checklist item silently create new project scope or sequencing;
4. reconcile each applicable item at closure as **satisfied**, **not applicable with reason**, **blocked with exact gate**, or **deferred only when current authority permits**;
5. prefer an inline checklist in the work packet, PR, issue/task, or current session unless persistence materially improves coordination/resumption;
6. discover and reuse an existing applicable durable checklist instead of inventing another one;
7. do not declare work complete while an applicable required item is merely forgotten or left unresolved.

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
- [ ] if real operational evidence could materially improve system behavior, apply the conditional Learning Architecture Gate from `docs/PROGRAMSTART_LEARNING_ARCHITECTURE.md` and route learning to the owner of the behavior
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
- [ ] when the Learning Architecture Gate is active, define evidence-based evaluation, promotion, regression/counterevidence, and rollback before learned behavior becomes trusted

---

## 8. Implementation Loop

For each coherent slice:

- [ ] run relevant Stage 6 → 7 gate controls before entering implementation
- [ ] define the compact logical work-packet fields from `PROGRAMBUILD_WORK_PACKET.md`
- [ ] if the slice follows an accepted recommendation, resolve the recommendation's effect under `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` before treating generic acceptance as execution authority
- [ ] preserve any stronger security/destructive/financial/credential/production/privacy/legal/release/operator gate; generic acceptance does not satisfy it automatically
- [ ] when autonomous execution is available, resolve the exact action under `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md`; new Controller/Compute/worker capability may automate only an already-authorized consequence class and must not create new permission
- [ ] persist `CURRENT_WORK_PACKET.md` only if persistence materially improves coordination/risk/resumption
- [ ] trace the slice to current authority and exact relevant requirements/contracts
- [ ] load only task-relevant authority/specialist context
- [ ] list reusable evidence + invalidation triggers
- [ ] define acceptance criteria + smallest sufficient verification set
- [ ] decide whether omission risk or an existing applicable durable checklist warrants an active checklist for this slice
- [ ] when a checklist is active, source its material items from current authority/acceptance/risk obligations and keep it subordinate
- [ ] implement without prospectively contradicting canonical authority
- [ ] update governed registries/contracts only when their surface changes
- [ ] run targeted verification plus broader checks triggered by invalidation/convergence
- [ ] record evidence once
- [ ] reconcile material decisions/scope/architecture/status
- [ ] when a checklist is active, reconcile every applicable item as satisfied / n/a-with-reason / blocked-with-exact-gate / authority-permitted-deferred
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
- [ ] reconcile every applicable release-readiness checklist obligation before go/no-go
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
- [ ] route reusable product/system operational learning to the behavior owner under `docs/PROGRAMSTART_LEARNING_ARCHITECTURE.md`
- [ ] propose PROGRAMBUILD changes only for systemic/reusable PROGRAMSTART prevention opportunities
- [ ] do not convert a fixed project-count threshold into methodology truth

---

## 12. Governance / Efficiency Checks

- [ ] one strategic execution spine exists
- [ ] authority ownership is clear
- [ ] no research/audit/checklist/packet is acting as a second master plan
- [ ] applicable checklist items came from authority/acceptance/risk obligations rather than silently creating scope
- [ ] an existing applicable durable checklist was reused rather than duplicated
- [ ] trivial work was not burdened with a large checklist merely for ceremony
- [ ] persisted `CURRENT_WORK_PACKET.md`, if present, is actually helping coordination/resumption
- [ ] evidence is reused until a relevant invalidation trigger occurs
- [ ] broad verification runs only for a real convergence reason
- [ ] specialist agents are used only when decomposition/review value justifies them
- [ ] learning-capable behavior, when activated, remains subordinate to deterministic permission/safety/budget/gate authority and cannot self-expand authority
- [ ] effective autonomy is consequence-scoped; newly available execution capability has not been mistaken for broader project authority or a project-wide `autonomous=true` permission
- [ ] a narrow human/consequence gate is not unnecessarily freezing unrelated safe work, and accepted gate evidence can resume without routine human transport where current runtime capability permits
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

Last updated: 2026-09-03
