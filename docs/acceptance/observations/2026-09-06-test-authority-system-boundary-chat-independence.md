# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence — implementation acceptance in progress**.

This record does not own product scope, execution order, release state, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-06
- **Project / repository:** cross-ecosystem boundary review; methodology owner `GrahamArdent/PROGRAMSTART`
- **PROGRAMSTART lesson ID:** proposed `PSL-023`
- **Checkpoint / acceptance surface:** explicit operator-designated PROGRAMSTART acceptance test: test authority / cross-owner closure / ChatGPT-window independence
- **Classification:** systemic

## A. Pre-implementation hypothesis from the originating conversation

The conversation proposed that material cross-system work should distinguish:

1. goal/product authority — owns the desired outcome;
2. execution authority — owns permission for consequential effects;
3. test authority — owns the behavioral proposition, scenario boundary, and verdict criteria;
4. evidence authority — owns provenance/integrity/currentness/evidence-purpose validity;
5. acceptance authority — decides whether verified evidence satisfies the declared claim.

It further proposed:

- exactly one test authority per behavioral proposition;
- explicit START/STOP boundaries for material cross-system tests;
- participant systems should not inherit another test owner's backlog merely because they participate;
- cross-owner findings should become durable handoffs rather than foreign closure obligations unless the originating project's own authority explicitly makes that external outcome a true acceptance dependency;
- Evidence Spine should normally be evidence authority, not behavioral owner for Controller/application/provider/Portfolio behavior;
- the literal ChatGPT-window-independence acceptance should be owned by the system whose continuation behavior is being tested, with later chat inspection observational only.

This section deliberately preserves the proposal before implementation so later review can compare what changed.

## B. What live PROGRAMSTART orientation found

Current methodology at `GrahamArdent/PROGRAMSTART@617aa008fafc5cecfd6e62d0a5f0b84ca6e963a8` already solved much of the surrounding problem:

- `PROGRAMBUILD_CANONICAL.md` already requires one primary owner per concern and keeps cross-repository dependency reasoning derived/task-scoped;
- `PROGRAMBUILD_WORK_PACKET.md` already separates project authority, current packet, dependency evidence, operator gates, checklist completeness, coordinated Mode-C lanes, and exclusive shared-mutation ownership;
- `PROGRAMSTART_EFFECTIVE_AUTONOMY.md` already separates permission from capability and requires alternative-actuation search before human transport;
- `PROGRAMBUILD_CHALLENGE_GATE.md` already challenges second-master/checklist scope creep and high-risk implementation failure sequences;
- the Learning Loop already routes reusable methodology observations separately from owner-local system learning.

The missing reusable concept was narrower than the conversation initially implied: PROGRAMSTART had no explicit behavioral **TEST_AUTHORITY** / **EVIDENCE_AUTHORITY** / **ACCEPTANCE_AUTHORITY** separation or bounded cross-system test envelope, so an evidence/integration participant could still accumulate another owner's unresolved work in its own closure surface.

The implementation therefore extends existing Work Packet + Test Strategy + Challenge Gate semantics instead of creating another test system, controller, registry, or lifecycle.

## C. Concrete Evidence Spine regression that exposed the gap

Live `GrahamArdent/evidence-spine` authority already states that Evidence Spine owns evidence/provenance/currentness and does **not** own Controller orchestration, project execution, universal acceptance, provider credentials, human-gate decisions, or automatic resume.

Its P4 implementation is already accepted/merged, but the retained closure checklist still contains unchecked Controller, Secrets, Portfolio, Compute, runtime-attestation, Challenge, and literal chat-window-independence items. The checklist itself says these are owner-only concerns, yet structurally they remain indistinguishable from unfinished Evidence Spine closure work.

This is the natural regression case for the methodology correction. The intended owner-local repair is to preserve those observations as explicit owner handoffs while removing false Evidence Spine closure ownership. No evidence/history should be erased.

## D. ChatGPT-window dependency audit — current classification

| Surface | Classification | Current truth / owner direction | Non-chat target / retirement acceptance |
|---|---|---|---|
| Controller durable semantic run/restart/replay after execution has begun | `CHAT_UI_ONLY` for later observation; stronger detachment acceptance still unproven | Autonomous Controller already has persistent semantic state and duplicate-suppressed restart/replay evidence | genuine objective durably admitted before detachment and reaches terminal/recovery without later chat-carried state/command |
| Contextual `Proceed` / natural-language intent ingress | `ARCHITECTURE_GAP` / `BOOTSTRAP_DEBT` | PROGRAMSTART V0.2 explicitly says repository-level implementation only and does not claim live chat-runtime semantic harvesting; Controller owns durable admission after a sealed packet exists | durable trusted semantic ingress/operator surface produces current sealed packet without session-memory dependence |
| Get 'er Done four-chat manual lane dispatch/context transport | `ARCHITECTURE_GAP` | lane semantics exist, but separate native chats do not form a durable dispatcher | one operator ingress routes durable work to Controller/owner workers; Graham is not message bus |
| Portfolio status/currentness refresh | `ARCHITECTURE_GAP` / `BOOTSTRAP_DEBT` | derived Portfolio files have repeatedly remained stale until a chat/lane sweep noticed owner changes | owner/event/currentness-driven generated refresh; chat sweep not required to discover completed/changed owner state |
| Vercel ChatGPT connector project visibility | `CONNECTOR_LIMITATION` / prior `FALSE_DEPENDENCY` | provider-native Execution Node session proves the intended team/project while ChatGPT connector returned contradictory zero-project/404 state | provider-native currentness remains authoritative for the bounded consequence; connector cannot block merely because it disagrees |
| Initial provider device authorization for a human-backed native session | `HUMAN_PRESENCE_BOUNDARY` | Secrets/H5 owns auth-path classification; initial user presence can be legitimate | after accepted session exists, bounded existing-path consequences continue without repeated human/chat relay; human session is not laundered into universal service identity |
| Polling CI/worker/provider results after a durable request exists | `FALSE_DEPENDENCY` where durable result transport is already available | Controller/Compute/GitHub result paths can retain machine evidence | backend wait/result/resume path drives continuation; chat polling is optional observation only |
| Human-gate durable state/resume | `CHAT_UI_ONLY` for awareness, but end-to-end operator response plane still needs real acceptance | Controller owns `WAITING_HUMAN` state and accepted-evidence resume; Mission Control is intended operator interaction plane | accepted authenticated response resumes exactly once without generic `proceed` or chat-carried gate state |
| Evidence Spine progression | `FALSE_DEPENDENCY` if chat is used as state/evidence bus; Evidence Spine itself is evidence-only | Evidence Spine already has deterministic Git-native evidence/currentness mechanisms | producer/consumer evidence references and invalidation signals remain durable; Evidence Spine does not own execution progression |
| Challenge/Learning invocation | `BOOTSTRAP_DEBT` candidate where a live agent/session is still the only trigger | PROGRAMSTART owns methodology trigger rules; owner systems own operational learning | natural owner/controller checkpoints trigger required Challenge/Learning without relying on a particular chat window; do not automate into ceremony without evidence |
| Mission Control | `CHAT_UI_ONLY` target posture | operator/client interaction plane, not execution authority | UI may disappear/reconnect without losing Controller execution state |

This audit is ownership/routing evidence, not a new global backlog. Each non-UI gap must be promoted only through its existing real owner when current authority warrants implementation.

## E. Current methodology implementation on the acceptance branch

Branch: `methodology/test-authority-boundaries-20260906`, based on exact live PROGRAMSTART `617aa008fafc5cecfd6e62d0a5f0b84ca6e963a8`.

Implemented so far:

- added `tests/test_programstart_test_authority_contract.py` first as a failing contract/regression;
- extended `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` with a conditional material cross-system test envelope and cross-owner handoff rule;
- extended `PROGRAMBUILD/TEST_STRATEGY.md` with cross-system authority semantics and a chat-detachment acceptance rule;
- extended `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` so scope/closure review challenges test-authority confusion, test-envelope leakage, foreign-closure capture, evidence/acceptance/execution authority confusion, and false chat-independence.

The change deliberately does **not** create a test platform, central test registry, second Controller, new lifecycle, or mandatory test-envelope paperwork for ordinary unit/component tests.

Exact PR/head/CI/Challenge/merge evidence will be added after repository acceptance completes.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** Mode-C orientation narrowed a broad architecture concern to a missing reusable ownership primitive inside existing Work Packet/Test Strategy/Challenge surfaces.
- **What helped:** one-spine authority, cross-repository dependency rules, checklist non-authority, Effective Autonomy, and Learning owner-routing prevented a new test/orchestration system from being created.
- **What created friction or uncertainty:** the methodology said participant/checklist/evidence artifacts were non-authoritative but lacked a positive rule naming who owns a cross-system behavioral test and when a participant's foreign finding stops being closure work.
- **Was existing methodology sufficient?** partially.

## Learning decision

- **Existing lesson match:** strongest overlap is PSL-006 (cross-repository authority graph), PSL-015 (adversarial Challenge), PSL-016 (checklist scope discipline), PSL-020 (owner-routed learning), but none explicitly owns behavioral test authority/test-envelope semantics.
- **Maturity before:** none
- **Maturity after:** candidate — bounded methodology implementation in progress
- **Why the evidence changes or does not change maturity:** Evidence Spine supplies a concrete natural failure mode where prose authority was correct but the checklist structure still captured foreign owner work; the explicit user request designates this as a real PROGRAMSTART acceptance exercise rather than speculative cleanup.
- **PROGRAMSTART change required now:** bounded extension of Work Packet, Test Strategy, and Challenge Gate; no new subsystem.

## Retest

- **Next real condition that could strengthen/challenge this lesson:** first genuine cross-system acceptance after methodology merge, preferably the Controller-owned durable chat-detachment scenario or another natural test where evidence/behavior/acceptance owners differ.
- **What evidence would be sufficient:** one current Work Packet/test surface names a single behavioral owner and bounded START/STOP, participant work remains owner-local, no test-created consequence bypass occurs, and closure does not depend on a foreign checklist item unless owning product authority explicitly requires it.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets/private payloads were copied into this observation.
- [x] Evidence claims match checks actually performed at this checkpoint.
- [x] The methodology change extends existing owners rather than manufacturing a new subsystem.
