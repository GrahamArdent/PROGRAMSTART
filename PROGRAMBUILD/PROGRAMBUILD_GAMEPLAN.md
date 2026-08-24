# PROGRAMBUILD_GAMEPLAN.md

# Execution Gameplan

Purpose: Canonical execution sequence connecting each PROGRAMBUILD stage to its required inputs, outputs, validation, and convergence behavior without creating duplicate planning authority.
Owner: Solo Operator or Project Lead
Last updated: 2026-08-24
Depends on: `PROGRAMBUILD.md`, `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, `PROGRAMBUILD_IDEA_INTAKE.md`, `PROGRAMBUILD_CHALLENGE_GATE.md`, `PROGRAMBUILD_WORK_PACKET.md`
Authority: Canonical for execution sequencing and cross-stage validation

---

## Why This Exists

`PROGRAMBUILD.md` defines what each stage produces. This file defines how stages execute in sequence and how active implementation work is narrowed into bounded slices.

It prevents:
- prompts or stages running out of order;
- research or audits turning into competing master plans;
- agents loading the entire project context for every small task;
- verification being repeated without a change-based reason;
- narrow task execution losing sight of stage-level convergence gates;
- contradictions between feasibility, requirements, architecture, tests, implementation, and release state.

---

## How To Use

1. Read `PROGRAMBUILD_CANONICAL.md` and `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` first.
2. Select the correct entry mode: raw idea, research-backed project, or existing/in-flight project.
3. If the project already has an authoritative roadmap/game plan, preserve it as the strategic execution spine unless replacement is explicitly approved.
4. Use the exact stage inputs listed below. Do not substitute from memory.
5. Run the Challenge Gate at every stage transition. `programstart advance` blocks missing or blocking gate evidence unless an exceptional bypass is explicitly recorded.
6. Run cross-stage validation where specified.
7. During Stage 7, derive bounded work packets for non-trivial slices. A packet is derived from the strategic spine/current stage and is canonical for nothing.
8. During a slice, load only the authority sections and specialist context required now.
9. Reuse trustworthy evidence until an invalidation trigger occurs. Verify changed/at-risk surfaces during slices; widen again at convergence gates.
10. If validation fails, fix the authoritative cause first and rerun only the checks necessary to restore confidence.

---

# Execution Sequence

## Pre-Stage: Planning Entry + Idea Intake

**Trigger:** A raw idea, substantial research that should become a project, or a proposed change to an existing/in-flight project.

**Protocols:**
- `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`
- `PROGRAMBUILD_IDEA_INTAKE.md`

### Steps

1. Select entry mode.
2. If existing/in-flight, identify the current canonical execution spine and current implementation/state needed to evaluate the change.
3. Run all **8** Idea Intake dimensions.
   - Raw idea: ask all questions directly.
   - Research-backed: prefill from trustworthy evidence and ask only missing, stale, ambiguous, or contradictory items.
   - Existing/in-flight: use the 8 dimensions as a delta audit against current authority.
4. Challenge red flags rather than mechanically accepting answers.
5. Produce:
   - clean problem/change statement;
   - success metric or impact target;
   - scope/exclusions;
   - kill/stop criteria;
   - cheapest useful validation;
   - go / investigate / stop recommendation;
   - existing-authority delta summary when applicable.
6. If `stop`, record why and end.
7. If `investigate`, run the smallest useful validation and re-evaluate.
8. If `go`, proceed to Stage 0.

**Output:** Structured intake evidence ready for Stage 0 or an existing-project planning delta.

---

## Stage 0: Inputs And Mode Selection

**Challenge Gate:** Idea Intake → Stage 0.

**Inputs:** Intake output + existing project authority when applicable.

### Steps

1. Fill or reconcile the project inputs block.
2. For existing projects, do not overwrite settled facts without evidence; record genuine deltas only.
3. Decide `PRODUCT_SHAPE`.
4. Decide variant: Lite, Product, or Enterprise.
5. Decide whether `USERJOURNEY/` is needed.
6. Record material decisions in `DECISION_LOG.md`.
7. Confirm one strategic execution spine.

### Validation

- [ ] Entry mode is explicit.
- [ ] Existing execution spine is identified when applicable.
- [ ] Required inputs are populated or explicitly confirmed current.
- [ ] PRODUCT_SHAPE is explicit.
- [ ] Variant is explicit.
- [ ] USERJOURNEY decision is recorded.
- [ ] ONE_LINE_DESCRIPTION remains outcome/problem focused.
- [ ] SUCCESS_METRIC is measurable.
- [ ] No new planning artifact has silently become a second strategic plan.

**Output:** Reconciled inputs + decision entries.

---

## Stage 1: Feasibility And Kill Criteria

**Challenge Gate:** Stage 0 → Stage 1.

**Inputs:** Reconciled inputs + intake evidence.

### Steps

1. Produce or update `FEASIBILITY.md`.
2. Define observable/falsifiable kill criteria.
3. Estimate effort/cost at the rigor appropriate to the variant and the precision supported by current evidence.
4. Record `go`, `limited spike`, or `no-go`.
5. For an existing project, state whether the proposed change aligns with, weakens, or requires a delta to current strategic authority.

### Cross-Stage Validation

- [ ] Problem/change statement is consistent with intake.
- [ ] Kill criteria were not silently softened.
- [ ] Success metric is consistent with the feasibility recommendation.
- [ ] Existing-project deltas are explicit rather than embedded as a replacement plan.

**Output:** `FEASIBILITY.md` + decisions.

---

## Stage 2: Research

**Challenge Gate:** Stage 1 → Stage 2.

**Inputs:** Inputs + feasibility + reusable existing research/evidence.

### Steps

1. Query current internal/curated knowledge where applicable before duplicating external research.
2. Gather only research needed to reduce material uncertainty.
3. Produce `RESEARCH_SUMMARY.md` for a new project, or a scoped research delta for an existing project when a full rewrite would duplicate current evidence.
4. Assign confidence to material findings.
5. Flag low-confidence decisions for approval or spike.
6. For an existing project, map each material finding to current authority as: confirmed / weakened / contradicted / new.

### Cross-Stage Validation

- [ ] Research contradictions to feasibility are explicit.
- [ ] Recommendations respect known constraints.
- [ ] Competitor/existing-solution evidence that affects viability triggers feasibility re-evaluation.
- [ ] Low-confidence decisions are recorded rather than buried.
- [ ] Research remains evidence until accepted into canonical authority.

**Output:** Research evidence + delta recommendations + decisions.

---

## Stage 3: Requirements And UX

**Challenge Gate:** Stage 2 → Stage 3.

**Inputs:** Inputs + feasibility + accepted research evidence/deltas.

### Steps

1. Create or update `REQUIREMENTS.md` with IDs and measurable acceptance criteria.
2. Create or update `USER_FLOWS.md` where direct interaction exists.
3. Trace every P0 requirement to the core problem/outcome.
4. For an existing project, update only affected authority rather than duplicating already-current scope.

### Cross-Stage Validation

- [ ] P0 requirements trace to the core problem/outcome.
- [ ] No requirement silently violates OUT_OF_SCOPE.
- [ ] P0 alone can plausibly achieve the success metric.
- [ ] User roles/personas are not invented without evidence.
- [ ] Priority language matches P0/P1/P2 discipline.

**Output:** Requirements + flows.

---

## Stage 4: Architecture And Risk Spikes

**Challenge Gate:** Stage 3 → Stage 4.

**Inputs:** Requirements + flows + accepted research evidence.

### Steps

1. Create or update `ARCHITECTURE.md` for the actual PRODUCT_SHAPE.
2. Create/update `RISK_SPIKES.md` for material unknowns.
3. Run the smallest spike that can resolve each blocking unknown whose impact justifies experimentation.
4. Record spike evidence and decisions.
5. Check dependency/KB freshness where relevant.

### Cross-Stage Validation

- [ ] Every material contract/system boundary serves a requirement or has an explicit reason.
- [ ] Auth/trust model covers relevant roles/consumers/operators.
- [ ] Technology commitments are consistent with research confidence or backed by spike/decision evidence.
- [ ] Inputs constraints are not violated.
- [ ] Applicable mandatory spike candidates are resolved or accepted.
- [ ] Superseded/deprecated dependencies are addressed.

**Output:** Architecture + risk-spike evidence + decisions.

---

## Stage 5: Scaffold And Guardrails

**Challenge Gate:** Stage 4 → Stage 5.

**Inputs:** Architecture + relevant flows.

### Steps

1. Create the scaffold appropriate to PRODUCT_SHAPE.
2. Implement the dominant contract layer.
3. Implement trust/auth boundary helpers where applicable.
4. Add structural tests.
5. Configure CI/gates with explicit timeouts and appropriate confidence tiers.
6. Verify scaffold guardrails before product feature work.

### Cross-Stage Validation

- [ ] Scaffold contracts trace to architecture.
- [ ] No product features were smuggled into scaffolding.
- [ ] Structural tests protect the actual dominant contract surface.
- [ ] Boundary/auth discipline is testable.

**Output:** Working skeleton + guardrails.

---

## Stage 6: Test Strategy

**Challenge Gate:** Stage 5 → Stage 6.

**Inputs:** Requirements + flows + architecture.

### Steps

1. Produce `TEST_STRATEGY.md` adapted to PRODUCT_SHAPE.
2. Map every P0 requirement to at least one purpose/outcome test.
3. Map material contracts to tests.
4. Define smoke/regression/golden/E2E use only where they add real confidence.
5. Define expensive/stateful evidence that may be reused and the events that invalidate it.

### Cross-Stage Validation

- [ ] Every P0 has outcome proof planned.
- [ ] Every material contract has appropriate test coverage.
- [ ] Browser E2E is not forced onto non-browser shapes.
- [ ] Theatre tests are not counted as outcome coverage.
- [ ] Evidence-reuse rules do not permit stale proof after relevant contract/environment changes.

**Output:** Test strategy + traceability/evidence model.

---

## Stage 7: Implementation Loop

**Challenge Gate:** Stage 6 → Stage 7 before implementation begins.

**Stage baseline inputs:** Requirements + architecture + relevant flows + test strategy + decision log + strategic execution spine/current stage.

### Work-Packet Loop

For every **non-trivial coherent slice**:

1. Derive or refresh `CURRENT_WORK_PACKET.md` using `PROGRAMBUILD_WORK_PACKET.md`.
2. Trace the packet to the strategic execution spine/current stage and exact requirement IDs.
3. Define one bounded objective and explicit non-goals.
4. Name expected changed surfaces.
5. Load only:
   - relevant architecture contracts/sections;
   - exact requirement IDs/acceptance criteria;
   - relevant flow sections if behavior/state is affected;
   - decisions that constrain this slice;
   - specialist material actually required now.
6. List trusted existing verification evidence and its invalidation triggers.
7. Identify the smallest verification set that will fail if the slice is wrong.
8. Write purpose/auth/contract tests first where appropriate.
9. Implement the slice without prospectively contradicting authority.
10. If design/scope must change, update canonical authority first and refresh the packet.
11. Update contract/test registries as needed.
12. Run targeted verification for changed or at-risk surfaces, plus any broader check whose invalidation trigger occurred.
13. Record evidence actually produced.
14. Reconcile material decisions/scope/architecture changes into canonical project state.
15. Mark the packet complete/replaced. Do not accumulate packets as a second game plan.
16. Derive the next packet from updated authority.

For trivial work, state the same objective/non-goal/context/evidence/verification fields inline instead of creating unnecessary packet ceremony.

### Convergence During Stage 7

Trigger a wider convergence review when the narrow packet view may no longer be sufficient. Use the trigger logic in `PROGRAMBUILD_CHALLENGE_GATE.md`, including accumulated cross-slice interaction, wider blast radius, architecture/scope/decision churn, evidence invalidation, dependency/environment change, or a meaningful milestone/handoff.

A project MAY configure local time- or slice-count reminders, but they are heuristics rather than universal PROGRAMBUILD gates.

At a Stage 7 convergence review:

- run the Challenge Gate parts required by the selected variant and the actual risks implicated by accumulated changes;
- re-check kill criteria and assumption/evidence validity;
- check cross-slice scope creep;
- reconcile decision reversals;
- review dependency health when due or invalidated;
- widen architecture/requirements alignment beyond the immediate packet;
- verify no `CURRENT_WORK_PACKET.md` has become de facto strategic authority;
- review which retained evidence remains valid and which needs re-establishment.

### Stage 7 Exit Criteria

- [ ] All required P0 slices are complete.
- [ ] Work packets are reconciled/closed, not acting as parallel plans.
- [ ] Requirements, architecture, decisions, and test registries match implemented reality.
- [ ] Relevant retained evidence remains valid or has been re-established after invalidation.
- [ ] No unreconciled high-risk deferred item blocks release readiness.

**Output:** Implemented product + tests + reconciled authority + verification evidence.

---

## Stage 8: Release Readiness — Convergence Gate

**Challenge Gate:** Stage 7 → Stage 8.

**Inputs:** Architecture + requirements + test strategy + implementation state + retained evidence/invalidation history.

Stage 8 deliberately widens context and verification after task-scoped Stage 7 execution.

### Steps

1. Produce/update `RELEASE_READINESS.md`.
2. Confirm launch scope and exclusions.
3. Verify deployment and rollback paths.
4. Verify environment/secrets/config.
5. Verify monitoring/alerts/support ownership.
6. Re-evaluate retained evidence:
   - reuse only evidence still within scope and not invalidated;
   - rerun release-critical checks invalidated by recent changes;
   - run required smoke/purpose/convergence suites.
7. Record go/no-go recommendation.

### Cross-Stage Validation

- [ ] Every P0 requirement is implemented and proven.
- [ ] Rollback references real deployment artifacts.
- [ ] Monitoring covers defined SLOs/SLIs.
- [ ] Kill criteria are still false.
- [ ] Active decisions remain coherent.
- [ ] Dependency health is current enough for release confidence.
- [ ] Release-critical evidence is current for the actual release candidate.

**Output:** Release readiness + go/no-go evidence.

---

## Stage 9: Audit And Drift Control

**Challenge Gate:** Stage 8 → Stage 9.

**Inputs:** Full codebase + canonical project outputs + release evidence + gate history.

### Steps

1. Run audit against explicit contracts/rules/requirements rather than stylistic preference.
2. Produce `AUDIT_REPORT.md` with severity, evidence, impact, fix, prevention, and canonical owner affected.
3. Identify stale evidence/invalidation misses and duplicate-authority drift.
4. Assign owners to critical/high findings.
5. Adopt accepted findings through the correct canonical authority; the audit itself does not become execution authority.

### Cross-Stage Validation

- [ ] Findings trace to explicit authority or verified behavior.
- [ ] Earlier gate warnings are checked against realized problems.
- [ ] Process misses become explicit template-improvement candidates.
- [ ] Audit did not create a competing remediation master plan without authority adoption.

**Output:** Audit findings + adopted deltas/owners.

---

## Stage 10: Post-Launch Review

**Challenge Gate:** Stage 9 → Stage 10.

**Inputs:** Success metric + release decision + audit findings + production signals + decision history.

### Steps

1. Produce `POST_LAUNCH_REVIEW.md`.
2. Compare actual results to the original success metric.
3. Review incidents/support/adoption gaps.
4. Review decision reversals and whether earlier signals could have reduced rework.
5. Capture lessons and owners.
6. Run Template Improvement Review.

### Template Improvement Review

For each systemic lesson, map it to the canonical PROGRAMBUILD owner most capable of preventing recurrence.

| Lesson type | Typical target |
|---|---|
| Intake failure pattern | `PROGRAMBUILD_IDEA_INTAKE.md` |
| Gate/risk detection gap | `PROGRAMBUILD_CHALLENGE_GATE.md` |
| Planning/execution/context/evidence failure | `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` or `PROGRAMBUILD_WORK_PACKET.md` |
| Feasibility/kill-criteria gap | `FEASIBILITY.md` template |
| Test/evidence gap | `TEST_STRATEGY.md` |
| Architecture spike gap | `PROGRAMBUILD.md` Stage 4 guidance |
| Execution sequencing gap | `PROGRAMBUILD_GAMEPLAN.md` |
| KB/research gap | knowledge-base/research assets |

A template change becomes mandatory when repeated evidence shows the lesson is systemic and the reusable methodology is the right prevention point. Teams MAY use a local recurrence count as a reminder, but PROGRAMBUILD does not define a universal number of projects that converts a lesson into truth.

**Output:** Post-launch review + follow-up ownership + template improvement proposals.

---

# Cross-Stage Validation Summary

| Stage | Validates against | Main contradiction being caught |
|---|---|---|
| 1 | Intake | Problem/change drift |
| 2 | Feasibility + inputs | Research contradicting viability/constraints |
| 3 | Feasibility + scope | Scope creep and metric mismatch |
| 4 | Requirements + research | Orphan contracts, trust gaps, bad technology assumptions |
| 5 | Architecture | Premature features and untracked contracts |
| 6 | Requirements + architecture | Untested outcomes/contracts and inappropriate test layers |
| 7 | Strategic spine + requirements + architecture + evidence model | Slice drift, stale context, duplicated authority, unnecessary/broken verification |
| 8 | Full release authority + current release candidate | Invalidated evidence, missing P0s, operational gaps |
| 9 | All prior authority + gate/evidence history | Drift gates should have caught |
| 10 | Success metric + feasibility + decision history + outcomes | Promise vs reality and systemic lessons |

---

# Variant Adjustments

| Variant | Gameplan rigor |
|---|---|
| Lite | Run all stages needed by the project; keep artifacts/packets brief. Challenge Gate minimum follows Lite rules. Reuse evidence aggressively when risk is low and invalidation is clear. |
| Product | Run all required stages with full cross-stage validation. Complete all **8** Challenge Gate parts at stage transitions as specified; Part G applies at Stages 4+ when dependency health is material, and Part H applies at Stages 6+. Use bounded packets for non-trivial implementation. |
| Enterprise | Full stages, approvals, retained evidence, all **8** Challenge Gate parts, stronger provenance/control traceability, and governed work packets. Evidence reuse requires explicit scope/provenance/invalidation conditions. |

---

# Operating Principle

**Narrow while executing; widen while converging.**

A work packet should make the next slice easier to reason about. It must never make the project forget its strategic spine. Likewise, broad validation should restore confidence at meaningful boundaries, not become a reflex that rechecks unchanged facts after every small edit.
