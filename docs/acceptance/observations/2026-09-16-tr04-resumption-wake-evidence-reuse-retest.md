# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, merge authority, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-16
- **Project / repository:** Networking TR-04 / `GrahamArdent/programstart-autonomous-controller`, with methodology owner `GrahamArdent/PROGRAMSTART`
- **PROGRAMSTART lesson ID:** none new; confirmation/strengthening evidence for `PSL-007`, `PSL-018`, current Verification Economics behavior, and the 2026-09-15 PR-terminalization/resumption observation
- **Checkpoint / acceptance surface:** explicit continuation/durability experiment using TR-04 waiting/resume behavior and Controller AC-09 owner-handoff wake semantics
- **Classification:** PROGRAMSTART methodology `confirmation`; Controller product/system learning `mixed strengthening evidence with wake-trigger provenance still unproven`

## What happened

A bounded continuation experiment intentionally resumed TR-04 multiple times from a durable contract. An early formulation overemphasized “recover current authority / do not rely on remembered conversational state” and created unnecessary rediscovery pressure. Current PROGRAMSTART Challenge and Verification Economics rules already say session change alone is not invalidation: valid evidence should be reused, while only declared invalidators and volatile facts required by the next decision should be refreshed.

The resume contract was therefore narrowed to: resume from durable state, reuse still-valid verified evidence, refresh only changed owner/currentness/runtime inputs, and do not repeat completed tests merely because execution resumed. A subsequent TR-04 resume applied that rule successfully: prior live A/E acceptance, repository CI/Challenge, and the previous alternative-actuation search were preserved; only Controller #67 owner state and the Desktop Commander execution-surface policy were refreshed before confirming the same genuine gate.

A second continuation finding then evolved during this Learning Gate itself. Controller AC-09 issue #53 had durably declared `WAITING_OWNER_EVIDENCE / HUMAN_ACTION_REQUIRED=NONE` and required reconsideration when either Execution Node #145 returned accepted/current receiver readiness or PROGRAMSTART PR #111/current successor returned accepted/current target-helper readiness.

PROGRAMSTART PR #111 reached exact-head PR Validation success, post-reconciliation Challenge CLEAR, and merged as `794140faaea1632a8bd7fa97d40171b38c4587e7` at 2026-09-16T03:44:37Z. Execution Node #145 then reached `ACCEPTED / CURRENT`: PR #149 reconciled onto current EN main, exact candidate `e777e34b7280400d5ae565b005686fb9d42dc987` passed Control Plane CI #379, Challenge cleared, it merged/activated as `fe5e7496510e0bf001c0bd1df04d38a03e991ee4`, and the installed receiver exposed the fixed owner-handoff intake profile.

At an intermediate observation point, Controller #53 had not yet recorded a post-wake continuation. Before this Learning Gate completed, however, #53 updated at 2026-09-16T03:50:59Z, consumed both accepted/current owner results, advanced AC-09, and isolated the next exact gap as Compute Spine #72. Current disposition became `PARTIALLY_ACCEPTED / TARGET_HELPER_CURRENT / EN_RECEIVER_LIVE_ACCEPTED / WAITING_COMPUTE_OWNER_CARRIER_GAP #72`, with `HUMAN_ACTION_REQUIRED=NONE`.

That materially narrows the conclusion. Durable owner/wake contracts did lead to a correct next-owner continuation and avoided a new orchestration layer. But repository evidence alone does not prove what *caused* #53 to re-enter: an event-driven/detached runtime wake, a still-active executor, or another conversational execution context could all produce the durable update. Therefore this is positive continuation evidence but is **not yet proof of detached autonomous wake/resumption**.

The experiment’s “provide the exact smallest next prompt if execution cannot continue” rule remains useful operator ergonomics, but it is a degraded/manual fallback. Requiring Graham or ChatGPT to transport that prompt cannot count as successful autonomous resumption.

## Evidence

- PROGRAMSTART `main`: `794140faaea1632a8bd7fa97d40171b38c4587e7` (`feat: add bounded owner-handoff current-authority intake (#111)`).
- PROGRAMSTART PR #111 exact reconciled head `a2971075e3f7f2739987af28ba3dd3c3948a694c`:
  - PR Validation run #204: SUCCESS;
  - post-reconciliation PROGRAMSTART Challenge: CLEAR;
  - merge: `794140faaea1632a8bd7fa97d40171b38c4587e7`.
- Execution Node #145 current accepted receiver evidence:
  - reconciled exact candidate `e777e34b7280400d5ae565b005686fb9d42dc987`;
  - Control Plane CI #379: SUCCESS;
  - post-implementation Challenge: CLEAR;
  - merged and installed release `fe5e7496510e0bf001c0bd1df04d38a03e991ee4`;
  - live admitted action `repository_owner_handoff_intake`, fixed profile `programstart_owner_handoff_v1`, exact target SHA/current-authority reread, bounded dispositions, `delivery_is_acceptance=false`.
- Controller issue #53 requires: persisted handoff -> exact owner-native delivery -> target current-authority reread -> bounded disposition -> source dependency-correct resume/termination -> replay/restart safety -> `HUMAN_TRANSPORT=NO`.
- Controller #53’s durable wake conditions explicitly named EN #145 accepted/current receiver readiness and PROGRAMSTART PR #111/current successor accepted/current target-helper readiness, with “Do not wait for conversational prompting.”
- Controller #53 subsequently recorded a fresh continuation, consumed both owner results, and created/routed the next smallest carrier gap to `GrahamArdent/programstart-compute-spine#72` rather than inventing a new transport/orchestration layer.
- Compute #72 now owns only the bounded worker-bridge carrier mapping required to carry the accepted EN owner-handoff intake action; Controller retains semantic handoff/return authority.
- PROGRAMSTART `PROGRAMBUILD_CHALLENGE_GATE.md` Part B: age/session change alone is not invalidation; identify reusable evidence and run the smallest check needed after an actual invalidator.
- `docs/PROGRAMSTART_VERIFICATION_ECONOMICS.md`: do not replay historical acceptance merely because another change exists; reuse specialized evidence when its invalidators did not occur.
- Existing 2026-09-15 PR-terminalization/resumption observation already concluded that methodology semantics were sufficient and routed missing runtime continuation capability to Controller ownership.
- The existing Portfolio idea `IDEA-pr-terminalization-resumption-ownership` already preserves the cross-project concept; no duplicate idea entry is required.

Checks not performed here:
- no claim that AC-09 itself is accepted/complete;
- no claim that the #53 re-entry was triggered by a detached/event-driven runtime rather than an active executor/session;
- no new event/scheduler implementation;
- no claim that PR #111 or EN #145 alone provides full delivery/disposition/return semantics.

## Challenge Gate result

**Result: CLEAR with two important narrowings.**

- **A — viability:** evidence-invalidation-driven resumption is already supported by PROGRAMSTART and worked better than cold rediscovery in the TR-04 experiment.
- **B — evidence validity:** the experiment distinguishes durable reusable evidence from volatile owner/runtime facts. Conversation context may be used as a cache/orientation aid, but authority-bearing/currentness claims remain grounded in durable sources. The Learning Gate itself had to update an intermediate conclusion when #53 advanced during the review.
- **C — scope integrity:** a tiny fallback prompt is not a continuation platform. It must not become the hidden transport layer or success criterion.
- **D — deferred work:** detached automatic wake/resumption remains unproven. AC-09 itself has materially advanced, but its current exact gap is now Compute #72 carrier readiness and later natural delivery/disposition/return acceptance.
- **E — adversarial sequences:** (1) a wake condition fires but no owner reconsideration occurs; (2) an owner update is incorrectly assumed to prove event-driven wake even though an active executor caused it; (3) every resume reruns expensive completed proof; (4) a fallback prompt silently becomes recurring human transport; (5) a stale wake executes without rereading current authority; (6) duplicate wakes create duplicate effects. Current/future Controller acceptance must distinguish and mechanically disprove these where applicable.
- **F — decision reversal/narrowing:** replace the overbroad operational phrasing “do not rely on remembered conversational state” with “reuse still-valid durable evidence; refresh only authority/currentness/invalidation-sensitive facts.” Also replace the intermediate “owner remained asleep after wake” claim with the stronger but narrower fact: owner continuation occurred, while the trigger provenance remains unproven.
- **H — alignment:** owner routing behaved correctly: PROGRAMSTART target semantics stayed in PROGRAMSTART, EN owned mechanical receiver intake, Compute #72 now owns only the missing carrier mapping, and Controller #53 retains semantic continuation/return authority.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** already provided the right evidence-reuse/currentness semantics, one-spine ownership, Challenge framing, Learning routing, and continue-until-real-gate behavior.
- **What helped:** Part B evidence validity, Verification Economics, the existing PR-terminalization/resumption observation, and Learning Architecture owner routing prevented duplicate infrastructure and forced this observation to incorporate live counterevidence rather than preserve an obsolete snapshot.
- **What created friction or uncertainty:** conversational shorthand (“recover, do not remember”) was easy to over-apply as synthetic amnesia; separately, durable owner updates do not by themselves expose the trigger provenance needed to prove detached automatic resumption.
- **Was existing methodology sufficient?** yes for semantics/governance; runtime acceptance still must prove detached wake/return properties where they are claimed.

## Learning decision

- **Existing lesson match:** yes. Evidence reuse/invalidation is already canonical; PR-terminalization/resumption owner routing is already recorded; Controller AC-09 already owns `HUMAN_TRANSPORT=NO`, wait/resume, receiver current-authority reread, durable return, and replay safety.
- **Maturity before:** no new PROGRAMSTART lesson; Controller continuation behavior remains under active implementation/acceptance.
- **Maturity after:** no PROGRAMSTART methodology maturity change; stronger mixed product/system evidence: owner routing and continuation progressed correctly, while detached trigger provenance remains unproven.
- **Why:** the methodology predicted the correct behavior, prevented overbuilding, preserved valid evidence, and correctly routed each newly exposed gap. The remaining uncertainty is implementation/acceptance evidence, not a missing methodology rule.
- **PROGRAMSTART change required now:** none.
- **Owner-routed system learning:** continue through existing Controller #53 / Compute #72 authority. Do not create another scheduler, watcher, queue, Mission Control, or continuation subsystem merely because trigger provenance remains to be proven.

## Retest

- **Next real condition:** a Controller-owned dependent wait reaches its durable wake condition while the originating executor/session is demonstrably inactive or terminated.
- **Sufficient evidence:** trigger provenance shows the ecosystem itself detected the exact state transition; the correct owner is reconsidered without Graham/ChatGPT polling or prompt relay; current authority is reread; still-valid evidence is reused; stale/duplicate wake delivery is safe; the source resumes or terminalizes correctly; `HUMAN_TRANSPORT=NO` remains true.
- A manual tiny resume prompt remains acceptable as a diagnostic/recovery fallback, but its use must be reported as manual transport and cannot satisfy detached autonomous-resumption acceptance.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No new scheduler, queue, watcher, controller, or continuation platform was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] Existing idea/learning records were reused rather than duplicated.
- [x] New live counterevidence was incorporated before acceptance.
- [x] No unnecessary PROGRAMSTART methodology change was manufactured.
