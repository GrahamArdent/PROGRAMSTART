# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-15
- **Project / repository:** `GrahamArdent/home-automation-control` + `GrahamArdent/portfolio-operations`
- **PROGRAMSTART lesson ID:** `PSL-013`, `PSL-017` (confirmation only); Authority-Gap Reconciliation protocol
- **Checkpoint / acceptance surface:** explicit operator-requested PROGRAMSTART retest of the Home Automation strategic-spine reconciliation and cross-project idea-capture decision
- **Classification:** confirmation

## What happened

A Home Automation architecture discussion exposed material strategic truth that had become clearer than the owning `HOME_AUTOMATION_EXECUTION.md` spine: canonical household capabilities, selective Alexa/Google exposure, cross-ecosystem mediation through Home Assistant, deterministic-before-adaptive AI, bounded agent authority, local-vs-VPS placement, degradation behavior, and a networking-isolation boundary.

The owning Home Automation spine was reconciled before selecting another work packet. A second, broader observation was then preserved in `GrahamArdent/portfolio-operations/IDEA_LEDGER.md` as `IDEA-strategic-spine-reconciliation-discipline`: mature repositories should independently verify spine freshness when relevant triggers fire, but no repo-specific backlog item should be pre-created without evidence of a local gap.

The operator then explicitly requested that this result be run through CURRENT PROGRAMSTART Challenge and Learning gates to see whether methodology reached the same conclusion.

## Evidence

- repository / PR / commit / run / provider / runtime evidence:
  - `GrahamArdent/home-automation-control/HOME_AUTOMATION_EXECUTION.md` current mainline strategic spine, updated 2026-09-15.
  - `GrahamArdent/portfolio-operations` PR #63, merged as `c4adb0b87f40c916f09f1b1df6f63ad0c4664e97`, adding only the cross-project candidate `IDEA-strategic-spine-reconciliation-discipline`.
  - `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` current Challenge Gate.
  - `docs/PROGRAMSTART_AUTHORITY_GAP_RECONCILIATION.md` current authority-gap protocol.
  - `docs/PROGRAMSTART_LEARNING_LOOP.md` current Learning Gate.
  - `docs/PROGRAMSTART_ACCEPTANCE_LEARNING_LEDGER.md` current lessons, including validated `PSL-013` and `PSL-017`.
- exact current state relevant to the observation:
  - Home Automation now explicitly declares one strategic execution spine and requires strategic-spine reconciliation before materially reshaping downstream work when architecture/authority truth changed.
  - Portfolio Operations preserves the broader concern only as a non-authoritative `CANDIDATE`, with repo-local read-only verification triggers and no implied execution priority.
  - No other repository was changed by the candidate.
- verification actually performed:
  - Challenge Gate lenses A/C/F plus relevant B/D/H were applied to the decision.
  - Current Authority-Gap classifications were checked against the observed case.
  - Existing PROGRAMSTART lessons were searched before considering new learning.
- checks not performed / unavailable:
  - No portfolio-wide repo-by-repo strategic-spine audit was run; the current evidence does not justify claiming every mature repo has the same defect.
  - No runtime, device, network, provider, or deployment mutation was part of this retest.

## Challenge Gate result

**Result: CLEAR.**

- **A — Kill criteria / viability:** no evidence that the Home Automation strategic direction became invalid; the reconciliation reduced contradiction rather than introducing a new product direction.
- **B — Assumption/evidence validity:** the broad systemic premise is intentionally bounded. One concrete Home Automation case proves the pattern can occur, not that every repository is stale.
- **C — Scope integrity:** clear. The Home Automation spine remains the project authority; the Portfolio idea is explicitly non-authoritative and does not become a second plan or portfolio backlog.
- **D — skipped/deferred work:** repo-local audits are deliberately deferred until a real trigger fires. This is not hidden blocking work because no evidence currently establishes those repos require correction.
- **F — decision reversal:** none. The result aligns with existing PROGRAMSTART rules rather than reversing them.
- **H — architecture/authority alignment:** clear. `PROGRAMSTART_AUTHORITY_GAP_RECONCILIATION.md` already requires owner-local authority reconciliation before dependent execution for authority-worthy deltas and explicitly prohibits a global authority-gap backlog or second spine.

**Adversarial challenge:** Assume the umbrella candidate is over-broad and causes every mature repo to receive speculative cleanup work. The current record defeats that failure mode by requiring an actual repo-local trigger/evidence check before creating a local candidate or reconciling a spine. Conversely, assume no umbrella record exists: the cross-project pattern can be lost and rediscovered repeatedly. One non-authoritative portfolio candidate with trigger-based resurfacing is the smaller control.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** provided existing primitives for one-spine authority, Authority-Gap reconciliation, cheap non-authoritative idea capture, trigger-based resurfacing, Challenge, and conditional Learning Gate handling.
- **What helped:** the current methodology independently converged on the same structure as the prior recommendation: reconcile Home Automation locally; preserve one cross-project candidate; do not pre-create per-repo work; route repeated systemic evidence through the Learning Gate.
- **What created friction or uncertainty:** the methodology rule already existed, but the real conversation exposed that operators/agents may still move too quickly from new architectural truth into work-packet thinking. This is evidence worth watching, but one case does not earn additional mechanical enforcement.
- **Was existing methodology sufficient?** yes.

## Learning decision

- **Existing lesson match:** `PSL-017` directly covers cheap non-authoritative preservation and trigger-based later promotion; `PSL-013` covers the correct no-change Learning Gate outcome. Authority-Gap Reconciliation already covers owner-local reconciliation before dependent implementation.
- **Maturity before:** validated (`PSL-013`, `PSL-017`)
- **Maturity after:** no change
- **Why the evidence changes or does not change maturity:** this is useful confirmation that the existing primitives produce the intended answer in a different real project, but it does not expose a new methodology gap or materially strengthen a still-open maturity claim.
- **PROGRAMSTART change required now:** none.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** another mature Mode-C repository naturally reaches architecture-changing work and either (a) current PROGRAMSTART reliably detects/reconciles a stale spine before packet execution, or (b) repeated evidence shows the rule is skipped despite current prompts/checklists, creating real rework or authority drift.
- **What evidence would be sufficient:** current owning spine + packet/decision evidence showing either successful owner-local reconciliation with no speculative backlog, or a second/third concrete failure where stale authority materially affected downstream execution and existing methodology failed to stop it.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] If no reusable lesson was found, no unnecessary PROGRAMSTART change was manufactured.
