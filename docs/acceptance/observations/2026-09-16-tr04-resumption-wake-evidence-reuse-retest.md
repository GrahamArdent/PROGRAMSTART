# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, merge authority, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-16
- **Project / repository:** Networking TR-04 / `GrahamArdent/programstart-autonomous-controller`, with methodology owner `GrahamArdent/PROGRAMSTART`
- **PROGRAMSTART lesson ID:** none new; confirmation/strengthening evidence for `PSL-007`, `PSL-018`, current Verification Economics behavior, and the 2026-09-15 PR-terminalization/resumption observation
- **Checkpoint / acceptance surface:** explicit continuation/durability experiment using TR-04 waiting/resume behavior and Controller AC-09 owner-handoff wake semantics
- **Classification:** PROGRAMSTART methodology `confirmation`; Controller product/system learning `systemic candidate / strengthening evidence`

## What happened

A bounded continuation experiment intentionally resumed TR-04 multiple times from a durable contract. An early formulation overemphasized “recover current authority / do not rely on remembered conversational state” and caused unnecessary rediscovery pressure. Current PROGRAMSTART Challenge and Verification Economics rules already say session change alone is not invalidation: valid evidence should be reused, while only declared invalidators and volatile facts required by the next decision should be refreshed.

The resume contract was therefore narrowed to: resume from durable state, reuse still-valid verified evidence, refresh only changed owner/currentness/runtime inputs, and do not repeat completed tests merely because execution resumed. A subsequent TR-04 resume applied that rule successfully: prior live A/E acceptance, repository CI/Challenge, and the previous alternative-actuation search were preserved; only Controller #67 owner state and the Desktop Commander execution-surface policy were refreshed before confirming the same genuine gate.

A stronger continuation finding then appeared. Controller AC-09 issue #53 durably stated `WAITING_OWNER_EVIDENCE / HUMAN_ACTION_REQUIRED=NONE` and explicitly required automatic reconsideration when PROGRAMSTART PR #111/current successor returned accepted/current target-helper readiness. PROGRAMSTART PR #111 later reached exact-head PR Validation success, post-reconciliation Challenge CLEAR, and merged to current `main` as `794140faaea1632a8bd7fa97d40171b38c4587e7` at 2026-09-16T03:44:37Z. At this observation checkpoint, Controller #53 remained open with its latest durable update predating that merge and no recorded automatic reconsideration after the wake condition became true.

The experiment’s “provide the exact smallest next prompt if execution cannot continue” rule was useful operator ergonomics, but it must remain a degraded/manual fallback. Requiring Graham or ChatGPT to transport that prompt cannot count as successful autonomous resumption.

## Evidence

- PROGRAMSTART `main`: `794140faaea1632a8bd7fa97d40171b38c4587e7` (`feat: add bounded owner-handoff current-authority intake (#111)`).
- PROGRAMSTART PR #111 exact reconciled head `a2971075e3f7f2739987af28ba3dd3c3948a694c`:
  - PR Validation run #204: SUCCESS;
  - post-reconciliation PROGRAMSTART Challenge: CLEAR;
  - merge: `794140faaea1632a8bd7fa97d40171b38c4587e7`.
- Controller issue #53 currently requires: persisted handoff -> exact owner-native delivery -> target current-authority reread -> bounded disposition -> source dependency-correct resume/termination -> replay/restart safety -> `HUMAN_TRANSPORT=NO`.
- Controller #53’s durable wake condition explicitly included PROGRAMSTART PR #111/current successor returning accepted/current target-helper readiness and said: “Do not wait for conversational prompting.”
- Controller #53 latest durable update observed at this checkpoint predates PR #111 merge; no later owner reconsideration was recorded when checked.
- PROGRAMSTART `PROGRAMBUILD_CHALLENGE_GATE.md` Part B: age/session change alone is not invalidation; identify reusable evidence and run the smallest check needed after an actual invalidator.
- `docs/PROGRAMSTART_VERIFICATION_ECONOMICS.md`: do not replay historical acceptance merely because another change exists; reuse specialized evidence when its invalidators did not occur.
- Existing 2026-09-15 PR-terminalization/resumption observation already concluded that methodology semantics were sufficient and routed missing runtime continuation capability to Controller ownership.
- The existing Portfolio idea `IDEA-pr-terminalization-resumption-ownership` already preserves the cross-project concept; no duplicate idea entry is required.

Checks not performed here:
- no claim that AC-09 itself is accepted/complete;
- no new Controller runtime mutation;
- no new event/scheduler implementation;
- no claim that PR #111 alone provides automatic wake/delivery/return semantics.

## Challenge Gate result

**Result: CLEAR with an important narrowing.**

- **A — viability:** evidence-invalidation-driven resumption is already supported by PROGRAMSTART and worked better than cold rediscovery in the TR-04 experiment.
- **B — evidence validity:** the experiment distinguishes durable reusable evidence from volatile owner/runtime facts. Conversation context may be used as a cache/orientation aid, but authority-bearing/currentness claims remain grounded in durable sources.
- **C — scope integrity:** a tiny fallback prompt is not a continuation platform. It must not become the hidden transport layer or success criterion.
- **D — deferred work:** automatic wake/reconsideration remains an open Controller AC-09 capability/acceptance obligation; this observation does not implement it.
- **E — adversarial sequences:** (1) wake condition fires while owner remains asleep; (2) every resume reruns expensive completed proof; (3) a fallback prompt silently becomes recurring human transport; (4) a stale wake is executed without rereading current authority; (5) duplicate wakes create duplicate effects. Existing Controller acceptance must mechanically disprove these where applicable.
- **F — decision reversal/narrowing:** replace the overbroad operational phrasing “do not rely on remembered conversational state” with “reuse still-valid durable evidence; refresh only authority/currentness/invalidation-sensitive facts.” This is a wording/operational correction, not a methodology reversal.
- **H — alignment:** the missing property remains Controller-owned. PR #111 supplies bounded target-side current-authority intake but explicitly does not close AC-09 or supply natural machine-native delivery/disposition/return.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** already provided the right evidence-reuse/currentness semantics, one-spine ownership, Challenge framing, Learning routing, and the rule to continue until a real gate or truthful completion.
- **What helped:** Part B evidence validity, Verification Economics, the existing PR-terminalization/resumption observation, and Learning Architecture owner routing prevented a duplicate scheduler/platform from being invented.
- **What created friction or uncertainty:** conversational shorthand (“recover, do not remember”) was easy to over-apply as synthetic amnesia, and methodology alone still does not cause a sleeping owner to wake when its declared durable condition becomes true.
- **Was existing methodology sufficient?** yes for semantics/governance; runtime implementation/acceptance remains incomplete.

## Learning decision

- **Existing lesson match:** yes. Evidence reuse/invalidation is already canonical; PR-terminalization/resumption owner routing is already recorded; Controller AC-09 already owns `HUMAN_TRANSPORT=NO`, wait/resume, receiver current-authority reread, durable return, and replay safety.
- **Maturity before:** no new PROGRAMSTART lesson; Controller continuation behavior remains under active implementation/acceptance.
- **Maturity after:** no PROGRAMSTART methodology maturity change; stronger product/system evidence for Controller AC-09.
- **Why:** the methodology predicted the correct behavior and prevented overbuilding. The new evidence primarily demonstrates that the runtime wake/resumption property is still not proven even after a declared wake condition became true.
- **PROGRAMSTART change required now:** none.
- **Owner-routed system learning:** Controller #53 should consume this as acceptance evidence. Do not create another scheduler, watcher, queue, Mission Control, or continuation subsystem merely to address it.

## Retest

- **Next real condition:** an AC-09 dependent wait reaches a durable wake condition while the originating chat/process is inactive.
- **Sufficient evidence:** the exact owner is automatically reconsidered without Graham/ChatGPT polling or prompt relay; current authority is reread; still-valid evidence is reused; stale/duplicate wake delivery is safe; the source resumes or terminalizes correctly; `HUMAN_TRANSPORT=NO` remains true.
- A manual tiny resume prompt remains acceptable as a diagnostic/recovery fallback, but its use must be reported as manual transport and cannot satisfy the autonomous-resumption acceptance case.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No new scheduler, queue, watcher, controller, or continuation platform was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] Existing idea/learning records were reused rather than duplicated.
- [x] No unnecessary PROGRAMSTART methodology change was manufactured.