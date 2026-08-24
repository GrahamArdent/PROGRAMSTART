# PROGRAMBUILD_PRODUCT.md

# Program Build Product

Use this version for a normal production product: customer-facing or operationally important, multi-feature, and maintained by a small or medium-sized team.
This is the recommended default for most real applications.

Authority:
- `PROGRAMBUILD_CANONICAL.md` defines source-of-truth rules
- `PROGRAMBUILD_FILE_INDEX.md` is the lookup table for critical files
- `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` defines planning entry modes, one-spine authority, proportional rigor, task-scoped context loading, and evidence reuse
- `PROGRAMBUILD_WORK_PACKET.md` defines logical current-slice execution context; persisted packets remain derived and never outrank project authority
- `PROGRAMBUILD_IDEA_INTAKE.md` challenges the raw idea, research-backed opportunity, or existing-project delta before Stage 0
- `PROGRAMBUILD_CHALLENGE_GATE.md` runs at stage transitions using A/C/F plus the parts relevant to stage/risk; full A–H is required at release/whole-system Product convergence
- `PROGRAMBUILD_GAMEPLAN.md` defines execution order and cross-stage reconciliation

---

## When To Use

Use this file when:
- the product is intended to ship and be maintained reliably
- several features/components share contracts or infrastructure
- mistakes have meaningful user/revenue/operational cost
- quality gates matter, but enterprise ceremony would be excessive

Team size is a signal, not the deciding rule. A small team can need Product rigor when blast radius is meaningful, and a larger team can still use lighter treatment for a bounded low-risk tool.

This variant fits interactive products and non-interactive systems such as APIs, internal services, and background automations.

For an existing project, identify and preserve its current strategic execution spine first. PROGRAMBUILD should propose explicit deltas rather than create a competing plan.

---

## Required Stages

| Stage | Output | Gate intent |
|---|---|---|
| Feasibility | `FEASIBILITY.md` | credible go / limited spike / no-go |
| Research | `RESEARCH_SUMMARY.md` or delta | material uncertainty reduced |
| Requirements and UX | `REQUIREMENTS.md`, flows where applicable | P0 scope is coherent/testable |
| Architecture and risk spikes | `ARCHITECTURE.md`, `RISK_SPIKES.md` | contracts/unknowns safe enough to scaffold |
| Scaffold and guardrails | skeleton + structural verification | dominant boundaries protected |
| Test strategy | `TEST_STRATEGY.md` | P0 risk surface has credible proof |
| Implementation | bounded logical slices | slice DoD + targeted evidence |
| Release readiness | `RELEASE_READINESS.md` | full Product convergence / go-no-go |
| Audit | `AUDIT_REPORT.md` | critical drift/risk resolved or owned |
| Post-launch | `POST_LAUNCH_REVIEW.md` | outcomes + systemic lessons captured |

---

## Product Guardrails

Apply guardrails to the actual product shape/risk rather than mechanically installing every pattern:

- one strategic execution spine;
- explicit dominant contract/trust boundary where relevant;
- auth/trust tests for protected surfaces;
- alignment tests where producer/consumer drift is plausible;
- requirements-to-proof traceability for P0 outcomes;
- contract-to-test mapping for material public/internal contracts;
- smoke/purpose verification for the dominant execution mode;
- decision-log updates for material choices;
- broad revalidation only when invalidation or a convergence boundary requires it;
- no scheduled regression/golden job unless its signal is worth its cost.

Attach `USERJOURNEY/` only when onboarding, consent, activation, or first-run behavior actually needs design.

---

## Work-Slice Rule

For each meaningful implementation slice, define the compact work-packet fields from `PROGRAMBUILD_WORK_PACKET.md`:

- objective / why now;
- in/out of scope;
- exact authority/context;
- reusable evidence;
- invalidation triggers;
- acceptance criteria;
- targeted verification;
- durable reconciliation if needed.

Persist `CURRENT_WORK_PACKET.md` only when cross-session/multi-agent coordination, risk, dependency complexity, blockers, or resumability makes persistence useful.

---

## Product Challenge Gates

At each stage transition, run:

- A — kill criteria;
- C — scope integrity;
- F — decision reversals;
- plus B/D/E/G/H when the current stage/change makes those risks material.

Use full A–H for release readiness and other genuinely whole-system Product convergence conditions defined in `PROGRAMBUILD_CHALLENGE_GATE.md`.

No material risk can be skipped because a gate part is conditional. Conditional means **relevance-driven**, not optional safety.

---

## Specialist Agents

Use specialist agents only when they improve decomposition or review quality.

Typical triggers:

| Agent | Trigger |
|---|---|
| Discovery & Scoping | material domain/scope ambiguity |
| Architecture & Security | important system/trust-boundary decision |
| Quality & Release | testing/release-risk review benefits from separate focus |
| Risk Spike Agent | material unknown blocks a decision |
| Contract Auditor | contract/auth/schema drift is plausible or audit is due |

Do not spawn all agents merely because the roles exist. Their outputs remain evidence until canonical authority adopts them.

---

## Product Prompt Pattern

```text
Operate this production product with PROGRAMBUILD Product rigor.

First identify live project authority/stage and select the correct entry mode.
Preserve any existing strategic execution spine.

Use programstart status/guide to orient, then load only task-relevant authority.

For the current slice:
- define compact work-packet fields;
- persist CURRENT_WORK_PACKET.md only if persistence adds coordination/resumption value;
- reuse valid evidence until invalidated;
- run the smallest verification set that proves changed/at-risk surfaces;
- use stage/risk-relevant Challenge Gate controls;
- widen to full Product convergence at release or another whole-system boundary;
- reconcile material outcomes back into canonical project state.

Do not create a new planning hierarchy, rerun checks from habit, or spawn specialist agents without a real decomposition/review reason.
```

---

## Product Definition Of Done

- P0 outcomes work and have credible proof;
- material contract/trust/schema behavior is aligned and verified;
- release readiness includes rollback, observability, and ownership appropriate to operational risk;
- release/whole-system Product convergence passes;
- no unresolved critical audit finding remains without explicit ownership/risk acceptance;
- logical/persisted work packets are closed/reconciled rather than accumulated;
- post-launch review compares real outcomes to the success metric.

---

Last updated: 2026-08-24
