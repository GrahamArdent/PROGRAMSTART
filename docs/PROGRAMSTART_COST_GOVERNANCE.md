# PROGRAMSTART Cost Governance

Purpose: keep PROGRAMSTART-assisted projects economically lean without turning cost tracking into a second execution spine, a stale vendor-price catalogue, or a reason to compromise reliability/security.

Status: **PROGRAMSTART operational protocol / subordinate to project authority**.

This protocol owns the **decision-scoped Cost Envelope** used when a current slice introduces or materially changes a paid, metered, quota-limited, or operationally expensive external dependency. It does **not** own product budgets, procurement authority, project sequencing, release decisions, or portfolio planning.

## 1. Core Principle

**Spend and operational complexity must be earned by current evidence.**

The goal is not `always choose free`.

The goal is:

**REUSE EXISTING CAPABILITY → USE INCLUDED/FREE CAPACITY WHEN SUFFICIENT → CAP METERED RISK → PAY WHEN THE BENEFIT OR PRODUCTION REQUIREMENT IS REAL → RECHECK WHEN ASSUMPTIONS CHANGE**

A $0 service that adds a fragile new control plane, weakens security, or consumes disproportionate operator time may be more expensive than a small paid service. A paid service may be the lean choice when it removes a real reliability, security, availability, or productivity blocker.

## 2. When the Cost Gate Activates

Activate the Cost Gate only when a current decision can materially change spend or operational cost.

Default triggers:

- adding a new hosted service, database, queue, worker, observability platform, secrets manager, email/SMS/push provider, enrichment provider, social-publishing service, or other external dependency;
- changing from free/included capacity to a paid tier;
- introducing a usage-metered API such as LLM, maps/places, search, enrichment, email, storage, compute, or bandwidth;
- creating another always-on runtime or independently billed project/service;
- a free-tier limit, sleep policy, quota, retention rule, commercial-use restriction, or reliability boundary can change architecture or release readiness;
- current pricing/limits are stale, unknown, conflicting, or likely to have changed;
- a repository contains a latent budget/subscription configuration that could become a real charge when activated;
- the operator explicitly asks for cost minimization, budget review, or a cost audit.

Do **not** activate durable cost ceremony merely because:

- a dependency is open source;
- a package appears in `package.json`/`requirements.txt` but has no external service cost;
- a routine request stays entirely inside already-approved included capacity;
- the cost is already governed by a still-valid project decision and no relevant assumption changed.

## 3. Decision-Scoped Cost Envelope

When the Cost Gate is active, derive the smallest envelope needed for the decision.

```text
COST_GATE: active
COST_SURFACE:
EXPOSURE_TYPE: [fixed | metered | mixed | unknown]
CURRENT_COST_EVIDENCE:
INCLUDED_OR_FREE_CAPACITY:
CHARGE_TRIGGER:
HARD_CAP_OR_BUDGET:
CAP_BEHAVIOR: [fail | throttle | pause | bill | unknown]
EXISTING_INFRA_REUSE:
LOWER_COST_ALTERNATIVES:
PAY_WHEN:
APPROVAL_OWNER:
COST_INVALIDATION:
COST_DECISION: [stay_free | reuse_existing | pay | defer | investigate]
```

Fields may be `not applicable` when genuinely irrelevant. Do not invent exact prices, quotas, or provider behavior when current evidence is unavailable.

### Field semantics

- **COST_SURFACE** — the exact service, API, runtime, tier, or architectural choice under review.
- **EXPOSURE_TYPE** — fixed recurring fee, usage-metered exposure, both, or unresolved.
- **CURRENT_COST_EVIDENCE** — current provider/account/repository evidence, including the evidence date when volatility matters. Prefer official pricing/account evidence for consequential decisions.
- **INCLUDED_OR_FREE_CAPACITY** — the capacity already available without incremental spend, including material limitations such as sleeping, retention, project counts, commercial restrictions, or reduced support.
- **CHARGE_TRIGGER** — the concrete condition that starts or increases billing: tier upgrade, additional project, request/token/storage threshold, seat/identity, always-on compute, etc.
- **HARD_CAP_OR_BUDGET** — the configured or proposed maximum exposure. `none` is a finding, not a harmless omission, for a metered production surface.
- **CAP_BEHAVIOR** — what happens at the limit. Prefer fail/throttle/pause over surprise billing where product requirements allow it.
- **EXISTING_INFRA_REUSE** — whether an already-operated platform can satisfy the need without adding another control plane.
- **LOWER_COST_ALTERNATIVES** — only credible alternatives that preserve the required capability/security/reliability. Do not list alternatives for list-making's sake.
- **PAY_WHEN** — the evidence threshold that would justify spending: production availability, real users, measured usage, saved operator time, security/compliance need, quality gain, or another named benefit.
- **APPROVAL_OWNER** — the project/operator authority that may authorize spend. PROGRAMSTART never grants itself purchasing authority.
- **COST_INVALIDATION** — changes that require a refresh, such as provider pricing/limits, usage growth, architecture change, new security requirements, or a cheaper existing capability becoming available.
- **COST_DECISION** — the current bounded conclusion. It is evidence for the project decision, not a permanent vendor verdict.

## 4. Cost Evidence and Freshness

Pricing, quotas, free tiers, and product packaging are volatile evidence.

Rules:

1. For a material provider/tier decision, use current provider/account evidence when tools permit.
2. Record the **date/source of the decision-relevant evidence**, not a permanent promise that the price will remain unchanged.
3. If pricing evidence is stale and could change the choice, route only the freshness delta through the existing adaptive decision/research mechanism.
4. Stop researching when the cost envelope is decision-sufficient. Do not perform broad market research when current included capacity already resolves the choice.
5. Distinguish `currently free/included` from `cannot ever cost money`.
6. Distinguish a published free tier from the account's actual plan/usage state when live account evidence is available.

## 5. No Central Vendor-Price Registry

PROGRAMSTART MUST NOT maintain a canonical catalogue of vendor prices/free-tier numbers across the portfolio.

Why:

- prices and packaging change frequently;
- account-specific credits/tiers differ;
- a central table becomes stale authority quickly;
- project decisions need current, local context;
- a portfolio price registry risks becoming a second planning/control surface.

Durable project evidence may record the price/limit that supported a material decision at that time, plus invalidation conditions. Future work refreshes only when that evidence is decision-relevant and stale.

A separate monitoring/reminder system may alert the operator that pricing changed, but the alert is evidence to re-evaluate a decision, not authority to mutate project architecture automatically.

## 6. Reuse Before New Infrastructure

Before adding another billed service or independently operated free service, ask in order:

1. Can the current project/platform already provide the capability safely?
2. Can an existing portfolio platform provide it without unacceptable coupling or authority leakage?
3. Can included/free capacity satisfy the current requirement with acceptable reliability?
4. If a new provider is still warranted, what is the smallest viable tier/runtime?
5. What exact condition earns an upgrade?

Reuse is not mandatory when it would create unsafe coupling. Database/security boundaries, independent failure domains, data residency, compliance, or product ownership may justify separate infrastructure.

## 7. Metered-Cost Safety

For usage-based services:

- configure provider-side hard budgets, quotas, rate limits, or spend controls when available;
- prefer a safe failure/throttle mode over unlimited surprise billing unless the product explicitly requires continued service;
- pair application-level limits with provider-side limits for high-variance surfaces such as LLMs, maps/places, enrichment, messaging, storage, bandwidth, and compute;
- choose the lowest-cost model/tier that meets the measured quality/reliability target rather than defaulting to the most capable option;
- make test/dev budgets materially smaller than production budgets;
- do not use a large budget ceiling as a substitute for deciding what normal spend should be.

## 8. Fixed-Cost Safety

For fixed monthly/annual services:

- identify whether the fee repeats per project, service, seat, identity, environment, or team;
- challenge designs where every new component automatically receives its own paid runtime/database/observability/secrets product;
- consolidate where ownership/security/reliability permit it;
- shut down or downgrade dormant development infrastructure when resumption cost is low;
- treat annual commitments as higher-reversibility decisions than month-to-month trials.

## 9. Free Is Not Automatically Lean

Do not self-host or add another free platform solely to avoid a small justified fee when doing so creates material:

- patching/backup/availability responsibility;
- secret-security risk;
- data-loss/recovery risk;
- operator toil;
- cross-provider complexity;
- debugging/observability burden.

Security boundaries are non-negotiable. Never centralize unrelated secrets, weaken tenant isolation, expose service-role credentials, or merge unrelated databases merely to avoid a small infrastructure fee.

## 10. Optional Lean Approval Profile

Projects/operators may adopt a lean profile. This is a **default decision heuristic, not universal purchasing authority**.

Example monthly recurring thresholds in the operator's chosen currency:

- **development default:** target $0 incremental recurring spend;
- **up to ~$10:** require a concrete reliability/productivity blocker or clearly named benefit;
- **~$10–$25:** require explicit benefit plus confirmation existing/included capability is insufficient;
- **over ~$25 for one vendor/surface:** compare credible alternatives before approval;
- **over ~$50:** require measurable usage, saved work, production requirement, or operational ROI;
- **over ~$100:** require explicit operator-level approval and a stated re-evaluation condition.

Usage-metered APIs also require a normal expected budget separate from the absolute safety ceiling.

A project may set stricter or looser thresholds. Its own approved budget authority outranks this example profile.

## 11. Relationship to Existing PROGRAMSTART Machinery

This protocol extends existing mechanisms rather than creating a new lifecycle:

- **Adaptive decision router** — `cost-resource` / `build-vs-buy` concerns activate simplicity/evidence scrutiny; research depth remains `none`, `targeted`, or `deep` based on actual uncertainty/consequence.
- **Work Packet** — the Cost Envelope is derived current-slice context. Persist it only when it materially improves resumption/coordination.
- **Challenge Gate** — stage/convergence authority remains unchanged; valid cost evidence should be reused instead of repeated as ceremony.
- **Mode C** — preserve the existing project spine and evaluate only the cost delta. Do not restart planning because a provider decision appears.
- **Cross-repository orchestration** — one project's provider choice does not authorize portfolio-wide infrastructure mutation.
- **Operator gates** — purchasing, billing enablement, credential entry, and provider-console actions remain operator-owned when the current environment cannot perform them.
- **Learning Gate** — repeated cost-governance friction may improve PROGRAMSTART, but routine savings do not require methodology writes.

## 12. Verification Gate

Before accepting a cost-bearing dependency decision, confirm:

1. the cost surface and exposure type are explicit;
2. current evidence is fresh enough for the decision;
3. included/free capacity and its material limitations were considered;
4. the concrete charge trigger is understood;
5. metered exposure has an intentional budget/cap, or the absence is explicitly accepted by the proper authority;
6. cap behavior is understood;
7. existing infrastructure reuse was considered without forcing unsafe coupling;
8. credible lower-cost alternatives were considered when the spend/risk warranted it;
9. `PAY_WHEN` names evidence, not optimism;
10. security/reliability was not weakened merely to remain free;
11. the conclusion is recorded only where the owning project needs durable evidence;
12. no central stale vendor-price registry or second portfolio execution spine was created.

## 13. Success Test

Cost governance is working when projects:

- remain at $0/included capacity while that is genuinely sufficient;
- pay small justified costs without unnecessary ceremony;
- do not accumulate one paid control plane per component by default;
- cap high-variance usage before it surprises the operator;
- know the condition that earns each upgrade;
- refresh volatile price evidence only when it could change a decision;
- preserve security/reliability boundaries;
- can explain **why this cost exists now** and **what would make it change**.
