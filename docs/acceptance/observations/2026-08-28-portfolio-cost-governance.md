# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-08-28
- **Project / repository:** Cross-project portfolio evidence; methodology owner `GrahamArdent/PROGRAMSTART`
- **PROGRAMSTART lesson ID:** proposed `PSL-014`
- **Checkpoint / acceptance surface:** Explicit PROGRAMSTART self-hosting experiment after a live infrastructure/API cost audit across current projects
- **Classification:** systemic

## What happened

A live portfolio-level audit was requested after secrets-management research raised the broader question of infrastructure cost. Current repository/provider evidence showed several materially different cost shapes across real PROGRAMSTART-assisted projects:

- Supabase currently has two active development projects on the Free organization, with tiny current databases relative to free capacity; the immediate issue is the active-project/production-reliability boundary rather than capacity pressure.
- Dedication currently uses a lean Supabase/Next.js shape and its bridge work can plausibly reuse existing runtime capacity instead of automatically creating additional paid hosts.
- Resume Creator V6 explicitly documents a Vercel-free + Render Starter backend deployment path, making a small fixed always-on fee an intentional reliability tradeoff.
- GCRM contains a separate Render Starter agent-runtime plan plus an LLM configuration whose example safety ceiling is materially larger than its present development need; optional observability and enrichment providers are also prefigured in environment configuration.
- LinkedInGenV2 contains a historical Ayrshare free-tier assumption that no longer matches current public pricing, proving that provider pricing embedded as durable architecture knowledge can become stale.
- Secrets-management research independently showed that a capable initial vault architecture can remain free while later identity/RBAC/rotation needs can earn a paid tier.

The repeated issue is not one expensive vendor. It is the absence of a reusable decision contract that asks when free/included capacity is sufficient, what specifically starts billing, whether exposure is capped, whether current infrastructure can be reused safely, and what evidence would justify paying.

## Evidence

- repository / PR / commit / run / provider / runtime evidence:
  - `GrahamArdent/GCRM` `.env.example` — OpenAI budget ceiling plus LangSmith/Langfuse/Apollo/Clearbit surfaces;
  - `GrahamArdent/GCRM` `render.yaml` and ADR-017 — separate Starter agent runtime;
  - `GrahamArdent/resume-creator-v6` `DEPLOYMENT.md` and `render.yaml` — explicit Vercel Hobby + Render Starter deployment shape;
  - `GrahamArdent/Dedication`, `Dedication-Calendar-Bridge`, and `Dedication-Email-Bridge` — lean current dependencies and evidence that separate components do not automatically require separate paid control planes;
  - `GrahamArdent/LinkedInGenV2` `.env.example` — stale Ayrshare free-tier statement;
  - connected Supabase organization evidence on 2026-08-28 — Free plan, GCRM + Dedication active, one older inactive project, low current database sizes;
  - connected Vercel evidence on 2026-08-28 — Hobby team, no projects visible in the connected team;
  - current official provider pricing/limit research performed on 2026-08-28 for relevant infrastructure/API services.
- exact current state relevant to the observation:
  - current portfolio development can remain mostly on free/included infrastructure;
  - small fixed costs can be rational when they buy an actual always-on/reliability requirement;
  - metered AI/API surfaces need explicit normal budgets and provider-side caps where possible;
  - copying vendor price/free-tier claims into long-lived project docs without freshness/invalidation semantics creates drift.
- verification actually performed:
  - live GitHub repository inspection across the named projects;
  - live Supabase organization/project inspection and bounded database-size/user/cron checks;
  - live Vercel team/project inspection;
  - current provider-pricing research for the cost audit;
  - current PROGRAMSTART v2.5 orchestration, adaptive decision router, Work Packet, Learning Loop, and lesson ledger reviewed before proposing a methodology change.
- checks not performed / unavailable:
  - no private invoices/credit-card statements or unavailable provider billing dashboards were accessed;
  - no local PROGRAMSTART runtime, pytest/Ruff/Pyright/full convergence workflow execution is claimed in the connected-tools environment;
  - no product repository was mutated to manufacture this acceptance case.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** Current v2.5 correctly routed the session as Mode C against PROGRAMSTART itself, preserved live repository authority, reused current evidence, and exposed the existing `cost-resource`/`build-vs-buy` simplicity concern in the adaptive decision router.
- **What helped:** Existing proportional-rigor, research-stop, Mode-C delta, Learning Gate, and anti-portfolio-master rules prevented the audit from becoming a new project lifecycle or blanket migration exercise.
- **What created friction or uncertainty:** `cost-resource` currently activates only a generic simplicity challenge. PROGRAMSTART has no structured answer for included/free capacity, charge trigger, cap behavior, reuse alternatives, `PAY_WHEN` evidence, or price invalidation. The previously suggested idea of a central portfolio cost registry would also conflict with evidence-freshness and one-spine principles because volatile provider pricing would become stale central authority.
- **Was existing methodology sufficient?** partially

## Learning decision

- **Existing lesson match:** `PSL-003` covers proportional decision/research routing but not the cost-specific decision contract. `PSL-005` and `PSL-006` cover blockers/dependencies rather than economic exposure. This is a materially different owner/surface.
- **Maturity before:** none
- **Maturity after:** implemented
- **Why the evidence changes or does not change maturity:** Multiple real projects independently expose fixed, metered, free-tier, stale-pricing, and reuse-vs-new-service decisions. The repeated evidence is strong enough for one bounded extension, but not for a global price database, procurement system, or automated provider migration layer.
- **PROGRAMSTART change required now:** bounded change — add a decision-scoped Cost Envelope protocol and integrate it into the existing orchestration path only when a cost-bearing decision is material.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** the next normal PROGRAMSTART-assisted project slice that proposes a new paid/metered provider, an upgrade from included capacity, or another independently billed runtime.
- **What evidence would be sufficient:** PROGRAMSTART should automatically activate the Cost Gate only because the decision is materially cost-bearing, derive a current Cost Envelope, reuse/refresh pricing evidence proportionally, compare existing/cheaper options where warranted, produce a truthful `stay_free | reuse_existing | pay | defer | investigate` conclusion, and avoid creating a central vendor catalogue or unnecessary process for ordinary $0 work.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] If no reusable lesson was found, no unnecessary PROGRAMSTART change was manufactured.
