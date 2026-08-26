# PROGRAMBUILD_GAMEPLAN.md

# Execution Gameplan

Purpose: Define PROGRAMBUILD's canonical stage sequence, transition conditions, and cross-stage reconciliation without duplicating the detailed stage content in `PROGRAMBUILD.md`.
Owner: Solo Operator or Project Lead
Last updated: 2026-08-26
Depends on: `PROGRAMBUILD.md`, `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, `PROGRAMBUILD_IDEA_INTAKE.md`, `PROGRAMBUILD_CHALLENGE_GATE.md`, `PROGRAMBUILD_WORK_PACKET.md`
Authority: Canonical for execution sequencing and cross-stage validation.

---

## 1. How To Use

1. Orient from live state/registry guidance instead of chat memory.
2. Select entry mode: raw idea, research-backed, or existing/in-flight.
3. Preserve an existing project's strategic execution spine unless its authority process explicitly replaces it.
4. Use `PROGRAMBUILD.md` for detailed stage deliverables, `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` for adaptive decision/evidence routing, and `PROGRAMBUILD_CHALLENGE_GATE.md` for stage/risk-aware gate selection.
5. Run the appropriate Challenge Gate before each stage transition; `programstart advance` records/blocks the transition according to current gate policy.
6. During implementation, use one bounded **logical work packet** per coherent slice. Persist `CURRENT_WORK_PACKET.md` only when persistence materially improves coordination, risk control, or resumability.
7. Load only task-relevant authority/evidence.
8. Reuse trustworthy evidence until invalidated; verify the changed/at-risk surface and widen at meaningful convergence boundaries.
9. Use `programstart decide` only when a meaningful decision has uncertainty/consequence that could change the next action; do not route trivial work through extra ceremony.
10. When a check fails, fix the authoritative cause first and rerun only what is needed to restore confidence.

---

# 2. Execution Sequence

## Pre-Stage — Planning Entry / Idea Intake

**Trigger:** raw idea, research that should become execution, or a proposed change to an existing project.

**Do:**
- select entry mode;
- identify existing execution authority when applicable;
- run the 8 Idea Intake dimensions using current evidence rather than re-asking settled facts;
- identify problem/change, success target, scope/exclusions, stop criteria, cheapest useful validation, and go/investigate/stop recommendation;
- when a material decision is uncertain, route it through the adaptive decision/evidence rules instead of automatically starting broad research;
- for existing projects, produce deltas to current authority rather than a replacement plan.

**Exit:** `go`, `investigate`, or `stop` is explicit. A Mode-C `investigate` result returns to the existing execution spine after the bounded evidence gap is resolved; it does not create a Stage-0 restart.

---

## Stage 0 — Inputs And Mode Selection

**Challenge Gate:** Intake → Stage 0 using parts relevant to the selected variant/risk.

**Do:**
- reconcile inputs;
- select PRODUCT_SHAPE and variant;
- decide whether USERJOURNEY is needed;
- identify one strategic execution spine;
- record material decisions.

**Cross-stage check:** no newer research/checklist/packet silently became a second strategic plan.

**Exit:** inputs/mode/authority are explicit.

---

## Stage 1 — Feasibility And Kill Criteria

**Challenge Gate:** Stage 0 → 1.

**Do:** create/update `FEASIBILITY.md`, define falsifiable stop/reshape criteria, estimate effort only to the precision current evidence supports, and record go/limited-spike/no-go.

**Cross-stage check:** problem, success target, and stop criteria still match intake/current authority.

**Exit:** explicit feasibility decision + durable decision record.

---

## Stage 2 — Research (When Earned)

**Challenge Gate:** Stage 1 → 2 when the lifecycle actually requires a research stage.

Stage 2 is a reusable research workspace, not proof that every project or every decision requires research. A project MAY pass through it as part of its normal lifecycle, while a Mode-C project or later-stage decision MAY instead run a bounded targeted/deep research delta in place and return to its existing execution spine.

**Do:** gather only evidence needed to reduce material decision-relevant uncertainty; reuse current internal research; produce a research summary or scoped delta; assign confidence; map findings to existing authority where applicable; stop when the declared evidence-sufficiency condition is met.

**Cross-stage check:** research that weakens feasibility/constraints triggers re-evaluation rather than being buried downstream; research output remains evidence and does not become a second plan.

**Exit:** material uncertainty is reduced enough to define scope/continue the protected decision, or a bounded spike/decision is explicitly required. Do not continue researching for completeness.

---

## Stage 3 — Requirements And UX

**Challenge Gate:** Stage 2 → 3 when Stage 2 was used; otherwise use the current applicable transition policy.

**Do:** define/update requirement IDs, measurable acceptance criteria, and only the flows relevant to the product shape; update only affected authority in an existing project.

**Cross-stage check:** P0 requirements trace to the core outcome and do not violate exclusions or silently change the success metric.

**Exit:** P0 scope is coherent and testable.

---

## Stage 4 — Architecture And Risk Spikes

**Challenge Gate:** Stage 3 → 4. Product normally adds dependency/evidence controls when relevant; use the full gate only if the boundary needs whole-system convergence.

**Do:** define architecture for the actual PRODUCT_SHAPE, identify material unknowns, route decision-relevant uncertainty to the smallest sufficient evidence/research depth, run the smallest useful spikes, challenge unnecessary extraction/build-vs-buy complexity, and record architecture/technology decisions.

**Cross-stage check:** material boundaries/contracts trace to requirements; auth/trust/data/runtime assumptions are explicit; unresolved high-impact uncertainty is not disguised as architecture.

**Exit:** architecture is sufficient to scaffold safely and blocking unknowns are resolved or explicitly accepted.

---

## Stage 5 — Scaffold And Guardrails

**Challenge Gate:** Stage 4 → 5.

**Do:** build only the structural skeleton, dominant contract/trust boundaries, and structural verification needed by the architecture; configure CI/local gates appropriate to the product's risk and active status.

**Cross-stage check:** scaffold implements architecture rather than smuggling in unapproved product behavior.

**Exit:** required structural checks are green.

---

## Stage 6 — Test Strategy

**Challenge Gate:** Stage 5 → 6.

**Do:** define the test portfolio appropriate to product shape/risk, map P0 outcomes and material contracts to proof, and define evidence reuse/invalidation for expensive/stateful verification.

**Cross-stage check:** P0 outcomes have credible proof; browser/E2E/golden layers are used only where they add real confidence.

**Exit:** test strategy is sufficient for the P0 risk surface.

---

## Stage 7 — Implementation Loop

**Challenge Gate:** Stage 6 → 7 before implementation starts. Select gate parts from the actual stage/risk; implementation alignment/evidence controls become relevant here.

### Per-slice loop

For each coherent slice:

1. define the compact logical work-packet fields from `PROGRAMBUILD_WORK_PACKET.md`;
2. persist `CURRENT_WORK_PACKET.md` only when persistence is useful;
3. trace the slice to strategic authority/current stage and exact relevant requirement IDs;
4. state one objective + non-goals + expected changed surfaces;
5. load only relevant authority/evidence;
6. list reusable evidence + invalidation conditions;
7. if a material decision has unresolved uncertainty/consequence, use the adaptive router to select only the relevant evidence/consequence/boundary/proof/simplicity/Mode-C checks;
8. choose the smallest sufficient verification set;
9. implement without prospectively contradicting authority;
10. update governed registries/contracts only if their surface changed;
11. run targeted verification plus broader checks triggered by invalidation or convergence;
12. record evidence once;
13. reconcile material decisions/scope/architecture/status into canonical state;
14. close/replace the packet and derive the next slice from current state.

### Mid-Stage-7 convergence

Widen when the narrow slice view is no longer sufficient because of cross-slice interaction, wider blast radius, architecture/scope/decision churn, evidence invalidation, dependency/environment change, milestone/handoff, or another Challenge Gate trigger.

Local time/slice reminders MAY prompt inspection but are never proof that convergence is due.

At convergence, run only the Challenge Gate parts required by variant + accumulated risk. Use full Product A–H when the situation is genuinely whole-system (for example release readiness, broad invalidation, or a major reset).

### Stage 7 exit

- P0 slices complete;
- logical/persisted packets closed/reconciled;
- requirements/architecture/decisions/test mappings match implemented reality;
- retained evidence is still valid or re-established;
- no high-risk deferred item blocks release readiness.

---

## Stage 8 — Release Readiness / Whole-System Convergence

**Challenge Gate:** Stage 7 → 8. Product uses full A–H here; Enterprise uses full A–H with its retained-evidence/sign-off requirements.

**Do:** confirm release scope, deployment/rollback, environment/config/secrets where applicable, observability/support ownership, and release-candidate evidence validity.

**Cross-stage check:** every P0 is implemented/proven; release-critical evidence reflects the actual candidate; active decisions remain coherent; kill criteria remain false.

**Exit:** explicit go/no-go release decision.

---

## Stage 9 — Audit And Drift Control

**Challenge Gate:** Stage 8 → 9 using the parts relevant to post-release drift/risk; widen when audit scope is whole-system.

**Do:** audit against explicit requirements/contracts/rules/verified behavior, identify real findings and stale-evidence/duplicate-authority misses, and route accepted findings to their canonical owners.

**Cross-stage check:** findings trace to evidence; the audit itself does not become a competing remediation master plan.

**Exit:** critical/high findings are fixed, owned, or explicitly accepted.

---

## Stage 10 — Post-Launch Review

**Challenge Gate:** Stage 9 → 10 using outcome/systemic-learning controls relevant to closure.

**Do:** compare actual outcomes to the success metric, review incidents/support/adoption gaps and decision reversals, assign meaningful follow-ups, and identify systemic methodology improvements only when evidence supports reuse.

### Template Improvement Rule

Map a systemic lesson to the canonical PROGRAMBUILD owner most capable of preventing recurrence.

| Lesson type | Typical owner |
|---|---|
| Intake failure | `PROGRAMBUILD_IDEA_INTAKE.md` |
| Gate/risk gap | `PROGRAMBUILD_CHALLENGE_GATE.md` |
| Planning/context/evidence/routing gap | `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` / `PROGRAMBUILD_WORK_PACKET.md` |
| Feasibility gap | `FEASIBILITY.md` template |
| Test/evidence gap | `TEST_STRATEGY.md` |
| Architecture/spike gap | `PROGRAMBUILD.md` Stage 4 guidance |
| Sequencing gap | `PROGRAMBUILD_GAMEPLAN.md` |
| Research/KB gap | knowledge/research assets |

A template change is warranted when the evidence shows the lesson is systemic and reusable methodology is the right prevention point. A local recurrence count may be a reminder, never a PROGRAMBUILD-wide truth threshold.

**Exit:** outcomes/lessons/follow-up ownership are durably captured.

---

# 3. Cross-Stage Validation Summary

| Stage | Main contradiction being caught |
|---|---|
| 1 | problem / feasibility drift |
| 2 | evidence contradicts viability or constraints, or research continues after sufficiency |
| 3 | scope / success-metric drift |
| 4 | orphan contracts, trust gaps, unsupported technology/runtime assumptions, unnecessary extraction |
| 5 | scaffold contradicts architecture or contains premature product behavior |
| 6 | P0 outcomes/contracts lack credible proof |
| 7 | slice drift, stale context/evidence, duplicated authority, unnecessary/broken verification |
| 8 | targeted-slice confidence mistaken for release confidence |
| 9 | contract/authority/evidence drift missed earlier |
| 10 | promise vs actual outcome; isolated lesson mistaken for systemic policy |

---

# 4. Variant Adjustments

| Variant | Gameplan rigor |
|---|---|
| Lite | Keep stage outputs and gates brief; A/C/F minimum plus risk-relevant parts; reuse evidence aggressively when invalidation is clear; skip research that cannot change the next decision. |
| Product | Run required stages with explicit cross-stage validation; A/C/F baseline plus stage/risk-relevant parts; full A–H at release/whole-system convergence; compact logical packets by default; route research depth from actual uncertainty. |
| Enterprise | Full stages, A–H controls, retained provenance/evidence and approvals appropriate to risk; persisted packets only when useful for governed coordination/resumption; high rigor still does not justify redundant research or proof. |

---

# Operating Principle

**Narrow while executing; widen while converging; investigate only uncertainty that can change a decision; do not duplicate detail whose canonical owner already exists.**

A work packet should make the current slice easier to reason about. A gate should inspect the risks that matter at the boundary. Research should stop when the protected decision has enough evidence. A validation suite should run because confidence needs restoring—not because a counter, calendar, or session changed.
