# Learning Observation — Portfolio Attention Control Self-Hosting

**Date:** 2026-08-29  
**System:** PROGRAMSTART self-hosting + bounded live portfolio sweep  
**Classification:** systemic / implementation evidence  
**Candidate lesson:** multi-project operator attention needs a lightweight external derived control surface, distinct from both project execution authority and repository/change history.

## Trigger

The operator reported a natural coordination problem after PROGRAMSTART had been used across many repositories: the existing ledger helped track repository updates, but it had become difficult to remember where each project stood and decide where limited attention should go next.

The request was not to manufacture another roadmap. It was to keep progress organized across many repositories and direct effort to the right project at the right time.

## Existing machinery that already worked

PROGRAMSTART already had strong primitives for:

- one project / one execution spine;
- Mode-C re-entry and current-authority preservation;
- bounded work packets;
- blocker scope and safe lanes;
- coordinated Mode-C lanes inside one project;
- task-scoped cross-repository dependency reasoning;
- operator/manual-gate handoff;
- evidence reuse and invalidation;
- idea preservation without backlog promotion;
- acceptance learning.

Those mechanisms answer **how to work safely once a project/slice is selected**. The repository/change ledger and project authorities also answer **what changed** and **what a specific project needs next**.

The missing question was operator-level:

> **Which project should receive attention now?**

## Self-hosting correction

The first conversational design proposed placing the live registry under `PROGRAMSTART/ops/portfolio/`.

That proposal was rejected by live PROGRAMSTART authority before implementation. `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` already states that PROGRAMSTART must not own a live global portfolio registry of the operator's actual projects; only reusable schemas/templates may live in PROGRAMSTART, while the filled portfolio belongs in the operator planning workspace or another dedicated portfolio system.

This was a useful self-hosting result: current repository authority overruled the conversational recommendation, preventing a new competing authority layer from being created.

The corrected design therefore keeps:

- reusable portfolio-attention semantics/templates in PROGRAMSTART;
- filled live portfolio state outside PROGRAMSTART;
- project truth inside each project's existing authority and verified implementation/runtime evidence.

## Bounded live acceptance sweep

The first sweep intentionally did not deep-audit every known repository. It inspected current authority/evidence only where it could materially affect the initial attention decision.

### Repo Watchtower

Current authority: `docs/WATCHTOWER_V0_2_EXECUTION.md`.

Observed state:

- V0.2 Slice 2 durable persistence is complete and merged;
- the stable repository-identity correction is complete and merged;
- the authority explicitly states Slice 3 is next;
- Slice 3 is a bounded repository-only incident-lifecycle/repository-registration slice with no identified external operator/provider blocker.

Derived attention: `PRIMARY_BUILD`.

### Dedication

Current authority: `ops/gameplans/DEDICATION_REMAINING_ISSUES_GAMEPLAN_2026-08-20.md` plus newer repository evidence.

Observed state:

- Interaction Packet 2 implementation/checkpoint work is merged;
- physical Samsung acceptance remains pending.

Derived attention: `OPERATOR_GATE` because a short physical-device acceptance action can close already-implemented work without displacing the primary build queue.

### GCRM

Current authority: `ops/gameplans/GCRM_MASTER_GAMEPLAN_2026-08-22.md`.

Observed state:

- R4 is active;
- R4-02 Next.js deployment remains closure-control;
- the Vercel production mutation/access boundary remains blocking for canonical R4-02 closure;
- reversible R4-04 secret-inventory/rotation-procedure preparation is explicitly allowed while preserving R4-02 closure control.

Derived attention: `SECONDARY_READY` fallback.

### Dedication Calendar Bridge

Current authority: `PROGRAMBUILD/PROGRAMBUILD_GAMEPLAN.md`.

Observed state:

- B5 credential-independent implementation is complete;
- deterministic suite evidence is retained;
- remaining work is a larger user credential/OAuth/provider-smoke gate.

Derived attention: `WATCH` rather than competing with the smaller current Dedication operator gate.

### Resume Creator V6

Observed repository evidence explicitly disables scheduled automation and GitHub Actions while the project is paused.

Derived attention: `PARKED`.

This is useful counterpressure against a dedicated global lifecycle engine: the portfolio can preserve the project-owned fact `paused` while using `PARKED` only as an attention-routing label. It also demonstrates that staleness must not manufacture urgency.

### Long-tail repositories

Other known repositories remain visible as `UNASSESSED` until operator interest, a dependency, or new evidence makes one decision-relevant.

No broad audit was run merely to fill a dashboard.

## External live-workspace experiment

A three-tab operator workbook was generated outside PROGRAMSTART:

- `Dashboard` — one operator gate, one primary build, one secondary fallback, explicit no-action set;
- `Registry` — known repositories, current evidence/authority pointers where assessed, invalidation triggers, and `UNASSESSED` long tail;
- `History` — meaningful attention transitions only.

The workbook was programmatically inspected and scanned for formula errors; no formula-error matches were found.

A native Google Sheets import was attempted as a convenient operator surface. The connected Google Drive credential returned `ACCESS_TOKEN_SCOPE_INSUFFICIENT` for file creation/import. No Sheet was claimed to exist. This provider-permission limitation does not alter the reusable portfolio-control design.

## Methodology delta implemented

The focused change adds `PROGRAMBUILD/PROGRAMBUILD_PORTFOLIO_CONTROL.md` plus external-workspace templates.

Key protections:

- attention classes are not project lifecycle states;
- one primary build + one short operator gate + one fallback by default;
- staleness is verification debt, not priority;
- ranking is qualitative/evidence-backed rather than a false-precision universal score;
- unassessed repositories do not trigger broad audits;
- live filled state remains outside PROGRAMSTART;
- project authority takes over immediately after selection;
- no automatic multi-repository consequential execution is introduced.

## Learning interpretation

This is a **new systemic lesson**, distinct from task-scoped cross-repository dependency orchestration (`PSL-006`) and the narrowed lifecycle lesson (`PSL-011`).

Proposed maturity after merge: **implemented**, not validated.

A real retest should occur on the next natural operator request equivalent to **“What should we work on?”** after one or more project states have materially changed. Validation should require that the external portfolio view can be refreshed cheaply, stale rows are corrected from project authority, paused/parked work does not become urgent by age, an operator gate remains distinct from the primary build, and exactly one bounded project is handed back to Mode C without the portfolio becoming execution authority.

## Counterevidence / narrowing conditions

Narrow or reject this mechanism if future use shows that:

- maintaining the live portfolio costs more effort than re-orienting directly from repositories;
- the status view routinely becomes stale and misroutes work despite invalidation rules;
- operators consistently need more than the bounded WIP model;
- attention classes become a shadow project lifecycle/backlog;
- Watchtower or another existing system naturally earns and subsumes this concern without duplicating authority.

Do not build additional automation until repeated refresh work proves a specific automation is worth its complexity.
