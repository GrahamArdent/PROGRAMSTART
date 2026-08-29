# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, sequencing, release state, portfolio priority, or a live idea backlog.

## Observation identity

- **Date:** 2026-08-29
- **Surface:** Planning Projects capture-audit correction / PROGRAMSTART self-hosting
- **Methodology repository:** `GrahamArdent/PROGRAMSTART`
- **Implementation PR:** #68 — `feat(programbuild): preserve worthwhile ideas without promoting them`
- **Existing lesson retested:** `PSL-016`
- **New lesson proposed/implemented:** `PSL-017`
- **Classification:** systemic correction + natural accepted-recommendation retest

## Trigger

Immediately after the Planning Projects conversation-to-repository capture audit, the operator challenged one conclusion:

> worthwhile/interesting ideas should generally still be recorded, even when they do not belong in the active backlog or current execution authority.

The prior audit correctly rejected turning every discussion into a project Master/backlog item, but it overreached by treating deliberate non-promotion as a reason some worthwhile ideas could remain only in conversation memory.

The operator then accepted the recommended correction with the natural response:

> **“I agree. You may go ahead.”**

This produced two independent PROGRAMSTART learning results:

1. a real generic-acceptance retest for `PSL-016`; and
2. evidence for a missing durable distinction between **idea preservation** and **idea promotion/execution**.

## Existing methodology evidence

The live methodology already contained pieces that implied the missing distinction:

- `PROGRAMBUILD_IDEA_INTAKE.md` explicitly supported **revisiting a shelved idea to decide if conditions have changed**;
- the Planning Operating Model separated evidence/reference material from project authority;
- `defer_without_resequencing` correctly prevented a liked future recommendation from silently becoming current work;
- PROGRAMSTART already prohibited a live operator portfolio registry inside the reusable methodology repository.

But no current owner clearly answered:

> If an idea is worth remembering but not worth promoting now, should it be durably preserved, and what does that preservation mean?

Without an explicit answer, an agent could interpret “do not create a backlog item” as “do not record the idea.” That makes later shelved-idea re-entry depend on chat/session memory.

## Systemic lesson — PSL-017

### Lesson

**Worthwhile ideas need cheap durable non-authoritative preservation that is explicitly separate from promotion and execution. Capture broadly; promote deliberately; execute only from authority.**

A durable Idea Record:

- preserves what was worth remembering;
- may retain why it was interesting, origin/evidence, related concepts, and revisit/promotion conditions;
- may retain rejection/shelving/supersession rationale to prevent repeated analysis;
- does **not** imply priority, current scope, sequencing, budget, architecture, or authorization to execute;
- becomes `ACCEPTED` only when deliberately promoted, at which point the actual owning project authority must be reconciled and execution derives from that authority.

### Status vocabulary implemented

- `CAPTURED`
- `CANDIDATE`
- `INVESTIGATING`
- `SHELVED`
- `ACCEPTED`
- `REJECTED`
- `SUPERSEDED`

These are descriptive idea/evidence states, not roadmap priority states.

## Implementation

PR #68 implements the smallest systemic change:

- adds optional `PROGRAMBUILD/IDEA_LEDGER.md` as a non-authoritative preservation template;
- makes the Planning Operating Model canonical for capture/promotion semantics;
- updates Idea Intake so full intake is required at **promotion/evaluation time**, not merely to save an idea;
- updates canonical/file-index authority boundaries;
- evolves the agent orchestration prompt to v2.9 so worthwhile non-current ideas are preserved while execution still follows current authority;
- adds static contract coverage;
- deliberately does **not** add `IDEA_LEDGER.md` to generated-project output files, so every repository does not receive another mandatory artifact;
- keeps the operator's live cross-project idea portfolio outside PROGRAMSTART itself, in the planning workspace or another dedicated portfolio system.

## PSL-016 natural retest

The accepted recommendation was concrete: revise PROGRAMSTART so worthwhile ideas are durably preserved without turning them into current backlog/authority.

The operator response was a generic natural acceptance: **“I agree. You may go ahead.”**

The live methodology resolves this as:

```text
ACCEPTED_RECOMMENDATION:
  Add lightweight durable idea-preservation semantics to PROGRAMSTART.

RECOMMENDATION_DISPOSITION:
  reconcile_authority_then_execute

AUTHORITY_RECONCILIATION_BEFORE_EXECUTION:
  Planning Operating Model + Idea Intake + Canonical/File Index + orchestration contract

STRONGER_GATE_OVERLAY:
  none
```

Why this disposition is correct:

- the recommendation changes durable methodology truth, so `execute_current_authority` would be insufficient;
- the change is accepted for execution now, so `defer_without_resequencing` would be false;
- no separate security/destructive/credential/provider/financial/production/privacy/legal/release gate is implicated by this documentation/orchestration methodology change.

The operator was not asked to restate PROGRAMSTART mechanics. The recommendation was resolved from current authority and executed through the owning surfaces.

**PSL-016 result:** this is the clean natural real-project/methodology self-hosting retest requested by its prior `implemented` maturity. If PR #68 closes with coherent static/adversarial verification, `PSL-016` should advance to **validated**.

## Adversarial challenge of the idea-preservation design

The implementation was challenged against realistic failure modes rather than accepting the attractive slogan at face value.

### Failure sequence 1 — idea ledger becomes a second backlog/Master

**Risk:** every captured idea acquires implied priority, ordering, or execution pressure.

**Control:** Idea Records are explicitly non-authoritative; status is descriptive rather than priority; current project authority remains the only execution source; a live cross-project portfolio ledger cannot live in PROGRAMSTART.

### Failure sequence 2 — every fleeting sentence creates permanent noise

**Risk:** “capture broadly” is interpreted as recording every conversational fragment and creating maintenance burden.

**Control:** trigger is **worth remembering / plausibly useful later**, especially when capture cost is low; the template allows a very small record; no mandatory full intake, cadence, or project-wide review is introduced.

### Failure sequence 3 — capture silently becomes approval

**Risk:** a `CAPTURED`/`CANDIDATE` idea is later treated as accepted scope because it exists in a durable file.

**Control:** lifecycle definitions explicitly deny scope/priority/authorization; Idea Intake consumes the record as evidence; `ACCEPTED` requires promotion/reconciliation into the actual owning authority; execution never derives from the ledger.

### Failure sequence 4 — rejected ideas disappear and get rediscovered repeatedly

**Risk:** rejection is treated as deletion, losing the reasoning that made the option unattractive.

**Control:** `REJECTED`, `SHELVED`, and `SUPERSEDED` remain durable when their rationale/revisit conditions can save future reasoning.

### Failure sequence 5 — PROGRAMSTART becomes the operator's portfolio database

**Risk:** a methodology template accumulates live project/idea state and becomes another portfolio authority.

**Control:** PROGRAMSTART owns only reusable semantics/template; project-specific idea records belong with the project; a cross-project ledger belongs in the Planning Projects workspace or another dedicated portfolio system.

### Failure sequence 6 — routine context loading grows because agents scan every idea

**Risk:** preserving ideas increases context cost on every turn.

**Control:** JIT retrieval is explicit; agents load only idea records relevant to the current request, a fired revisit trigger, or changed evidence.

### Failure sequence 7 — idea records become a sensitive-data dumping ground

**Risk:** agents preserve credentials/private payloads merely to keep idea context.

**Control:** the template/orchestration guardrails prohibit secrets and unnecessary sensitive raw data.

## Challenge result

**CLEAR for the bounded methodology scope.**

The design preserves the user's intended benefit—ideas are not casually lost—while maintaining PROGRAMSTART's existing one-spine/anti-backlog/authority boundaries.

The remaining uncertainty is operational rather than conceptual: will a later real project successfully capture a worthwhile non-current idea and then retrieve/revisit/promote or keep it shelved without creating prioritization drift?

That is the real validation condition for `PSL-017`.

## Learning decision

- **PSL-016:** advance from `implemented` to **validated** after PR #68 verification/merge.
- **PSL-017:** add at **implemented** because methodology changed; do not mark validated from the same implementation event.
- **PSL-017 next real retest:** in a normal Planning Projects/project session, capture a worthwhile idea that is not current work, then later retrieve it because a related request/evidence/revisit trigger makes it relevant; prove it can be evaluated/promoted/rejected/shelved without silently resequencing the active project.

## Correction to the prior capture audit

The prior observation remains append-only historical evidence. Its anti-backlog conclusion is narrowed by this later evidence:

> **Do not create a portfolio backlog merely to preserve interesting ideas** remains correct.

But it must now be read together with:

> **Do preserve worthwhile ideas in a lightweight non-authoritative idea/reference surface. Lack of promotion is not a reason to rely on ephemeral conversation memory.**

No historical observation is rewritten to make the learning path appear cleaner than it was.

## Safety / authority check

- [x] no real project's execution spine was replaced;
- [x] no live portfolio backlog was added to PROGRAMSTART;
- [x] no idea status creates priority or execution authority;
- [x] no full Idea Intake is required merely for capture;
- [x] no mandatory generated-repository artifact was added;
- [x] no secrets/private payloads were stored;
- [x] the natural generic acceptance was resolved without asking the operator to restate methodology;
- [x] the methodology change has an explicit future real-world validation condition.