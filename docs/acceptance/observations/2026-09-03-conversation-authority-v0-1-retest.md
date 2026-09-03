# Learning Observation — Conversation-to-Authority V0.1 Real Retest

**Date:** 2026-09-03  
**System:** Portfolio Operations / PROGRAMSTART conversation-to-authority composition  
**Classification:** confirmation / owner-boundary resolution  
**Related lessons:** `PSL-016`, `PSL-017`, `PSL-018`  
**Prior observation:** `docs/acceptance/observations/2026-09-02-conversation-authority-reconciliation-gap.md`  
**Status:** subordinate / non-canonical evidence

## Retest trigger

The 2026-09-02 observation left one composition question deliberately open: do existing PROGRAMSTART primitives become sufficient when Portfolio Operations explicitly distinguishes preservation, authority reconciliation, trigger arming, and trigger-based resurfacing, or does PROGRAMSTART itself need another canonical lifecycle/artifact/state?

Two natural real cases have now exercised the promised retest conditions.

## Case A — preserved deferred outcome resurfaced on evidence

Portfolio Operations had previously preserved a Home Automation resource-monitoring guardrail because its owning-project write/PR path was incomplete.

On the 2026-09-03 Conversation-to-Authority sweep:

1. the specific recorded write-completion trigger became true;
2. only that relevant record was reopened rather than scanning the idea/inbox surfaces as a backlog;
3. current Home Automation ownership was rechecked;
4. the project reference PR was opened;
5. project CI passed;
6. the reference was merged into the owning project;
7. the unresolved capture was no longer left shadowing the project.

This proves the `TRIGGER_ARMED -> READY_FOR_REVIEW -> owning-project routing` composition can work without age-based priority or a global task queue.

## Case B — already-accepted conversation outcome had never reached project authority

A 2026-09-01 Resume Creator conversation explicitly accepted a streamlining change and authorized PROGRAMSTART planning plus implementation. The accepted outcome centered on lower-friction job-description intake, company context/research, ATS-aware tailoring, approval, and higher application throughput.

Resume Creator's live execution authority had last been reconciled on 2026-08-27 and explicitly discouraged reopening feature scope while completing finish-line verification. The later accepted operator decision therefore materially post-dated and conflicted with the older scope assumption.

The 2026-09-03 V0.1 acceptance check found:

- the accepted September 1 delta was absent from the Resume Creator owning execution spine;
- no equivalent Portfolio Operations durable record existed;
- the older finish-line authority was still valid for its original release/closure purpose and should not be discarded;
- Resume Creator already contained the expensive core JD, tailoring, ATS, cover-letter, preview and export capabilities.

PROGRAMSTART Mode C then used the existing accepted-recommendation semantics rather than inventing a new planning lifecycle:

```text
accepted conversation outcome
  -> detect missing owning authority
  -> compare against newer/older project evidence
  -> classify as reconcile_authority_then_execute
  -> update the existing owning execution spine
  -> begin a bounded stacked project branch/PR
```

`docs/PRODUCTION_READINESS_GAMEPLAN_2026-03-24.md` in `GrahamArdent/resume-creator-v6` was reconciled in place with a bounded Section 7 product lane while preserving the pre-existing R1-R4 finish-line sequence.

The first implementation slice is intentionally narrow: structured job-target intake with an explicit approval boundary. Remote source acquisition/company web research is separately gated behind current security/provider evidence rather than being inferred from the conversation acceptance.

## What PROGRAMSTART did in the retest

Existing primitives were sufficient:

- `PSL-016` / accepted-recommendation handling already defines `reconcile_authority_then_execute` when durable project truth changes;
- Mode C already requires current authority inspection and delta reconciliation instead of a new competing Master;
- `PSL-017` already keeps captured ideas non-authoritative and supports trigger-based promotion/revisit;
- `PSL-018` already requires derived portfolio attention/routing to converge into owning-project truth;
- the Learning Gate prevented the implementation gap from turning into another lifecycle/state machine.

The missing behavior was operational composition in Portfolio Operations, not an absent PROGRAMSTART state.

## Result

**The candidate canonical PROGRAMSTART composition change from the 2026-09-02 observation is not earned.**

Resolve it as:

- Portfolio Operations V0.1 implementation/recovery contract: **validated by real use for the two tested failure modes**;
- `PSL-016`: remains **validated**;
- `PSL-017`: remains **validated**, with preservation explicitly understood as insufficient by itself until promotion/reconciliation occurs;
- `PSL-018`: remains **validated**;
- new PROGRAMSTART lesson ID: **not warranted**;
- new lifecycle/artifact/global backlog: **rejected as unnecessary under current evidence**.

This is not a claim that conversation coverage is complete. Ordinary ChatGPT history still lacks a deterministic message cursor in the current operating surface, so the forward recovery sweep continues to report partial coverage and the separate user-authorized historical-export backfill remains useful.

## Why no canonical methodology patch follows

The real Resume Creator case exercised the exact semantic rule already present in PROGRAMSTART: when an accepted recommendation changes durable project truth, reconcile the owning authority before or atomically with dependent implementation.

The Home Automation case exercised the existing preservation/revisit rule without turning preservation into priority.

Adding another canonical PROGRAMSTART state such as `conversation_reconciled`, a mandatory transcript artifact, or another promotion lifecycle would duplicate proven primitives and increase ceremony/context cost without solving the remaining event-ingress limitation.

## Future reopen condition

Reopen the methodology question only if real operation shows one or more of these despite V0.1 being active:

- clearly accepted outcomes repeatedly remain outside the owning project after a capture/reconciliation pass;
- the system cannot distinguish accepted current work from merely preserved candidates using existing `reconcile_authority_then_execute` / Mode-C semantics;
- trigger-based resurfacing becomes noisy, age-driven, or acts like an unauthorized backlog;
- current PROGRAMSTART ownership rules prevent a safe concern-owner reconciliation that the project genuinely needs;
- deterministic conversation-event access changes the operating model enough that the current JIT/recovery composition becomes obsolete.

## Safety / authority check

- [x] owning projects remain authoritative;
- [x] no raw transcript/private payload is stored;
- [x] accepted conversation meaning reached Resume Creator authority before dependent implementation;
- [x] deferred Home Automation meaning resurfaced only when its trigger fired;
- [x] no global backlog or new lifecycle was introduced;
- [x] implementation verification/merge gates remain project-owned and are not bypassed by reconciliation success;
- [x] historical completeness remains a separate private backfill concern.
