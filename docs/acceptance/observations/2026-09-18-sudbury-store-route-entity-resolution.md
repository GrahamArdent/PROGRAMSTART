# PROGRAMSTART Acceptance Observation — Sudbury Store-Route Entity Resolution

Status: **explicit real-world acceptance replay / research-routing confirmation / no methodology change earned**.

This record is subordinate, non-canonical evidence. It does not own product scope, execution order, release state, route-planning behavior, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-09-18
- **Project / repository:** real-world one-off navigation task; methodology owner `GrahamArdent/PROGRAMSTART`
- **PROGRAMSTART lesson ID:** none new; confirmation of existing adaptive decision/research routing; `PSL-013` governs the Learning Gate recording path only
- **Checkpoint / acceptance surface:** explicit operator-requested replay of the original highlighted-store screenshot through current PROGRAMSTART methodology after a real wrong-destination incident
- **Classification:** confirmation with an execution/conformance failure outside PROGRAMSTART invocation

## Input fixture and privacy boundary

The original chat attachment is treated as the immutable source fixture for this replay.

- **Original screenshot SHA-256:** `835d95087622d3af792809ca4c9433916fddfe491fa5cb0bd8e6029287817345`
- **Semantic highlighted set extracted from the screenshot:**
  1. Metro — 900 Lasalle Blvd — Sudbury
  2. Food Basics #610 — 1800 Lasalle Blvd — Sudbury
  3. Food Basics #638 — 1875 Regent St. S. — Sudbury
  4. Food Basics #697 — 400 Notre Dame St. — Sudbury
- The screenshot itself remains a chat attachment; this observation persists its hash plus the bounded semantic fixture rather than copying user conversation media into PROGRAMSTART.
- **Private live user location is deliberately not persisted.** The acceptance target does not require it.
- The public starting-business concept (Sudbury Costco) is not needed to prove the entity-resolution failure and is therefore not made part of the durable acceptance fixture.

## What happened

A real navigation request was answered directly from the highlighted store list without first treating the extracted real-world destination data as evidence requiring verification.

The failure sequence was:

1. the highlighted rows were read as executable routing inputs;
2. the Notre Dame Food Basics address was accepted as a plain address string;
3. a current source conflict around `Street` versus `Avenue` was not discovered before routing;
4. the ambiguous address was geocoded to the wrong physical place;
5. after the first error, later conversational turns reconstructed the remaining-stop list from dialogue rather than preserving the original four-store set as the canonical task set plus separate completion state;
6. this allowed omissions, reintroduced completed stops, and repeated correction by the operator.

The observed consequence was material: the operator was sent to the wrong physical destination and had to spend additional travel/time correcting the route.

## Current PROGRAMSTART replay

Current PROGRAMSTART `main` was re-read before this replay.

- **Current main SHA:** `20cc75e2185933d3728a310a3fe4eaf5e44b09f5`
- Relevant current surfaces:
  - `scripts/programstart_decision.py`
  - `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md`
  - `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md`
  - `docs/PROGRAMSTART_LEARNING_LOOP.md`
  - `docs/PROGRAMSTART_REAL_WORLD_ACCEPTANCE_CHECKLIST.md`
  - `docs/PROGRAMSTART_ACCEPTANCE_LEARNING_LEDGER.md`

### Pass 1 — initial screenshot before external verification

A truthful decision context is:

- decision protected: route the operator to the four highlighted real-world stores without sending them to the wrong physical destination;
- impact: medium;
- uncertainty: medium;
- reversibility: costly;
- evidence state: partial;
- volatility: changing;
- concern: verification.

Under the current router logic this yields:

- **route:** `investigate`
- **research depth:** `targeted`
- **evidence action:** `reuse-valid-evidence-and-fill-only-the-gaps`
- **activated checks:** evidence, consequence, proof.

Therefore current PROGRAMSTART would not treat the screenshot-only address strings as sufficient executable destination evidence.

### Pass 2 — after targeted source checking exposes the Notre Dame conflict

Current source evidence produces a decision-relevant contradiction:

- Food Basics' current store page for #697 says **400 Notre Dame Street**, Sudbury, ON P3C 5K5, phone **705-675-5845**:
  - https://www.foodbasics.ca/find-a-grocery/100697
- City of Greater Sudbury planning material identifies **Store No. 697** at **400 Notre Dame Avenue**, Greater Sudbury:
  - https://www.greatersudbury.ca/do-business/planning-and-development/committee-of-adjustmentsign-variance-committee/coa-pdf-folder/oct-15-agenda/
- A local Sudbury business listing independently associates the same store/phone with **400 Notre Dame Ave**:
  - https://www.sudbury.com/directory/grocery-stores/food-basics-sudbury-60753
- A construction certificate independently associates **Food Basics 697** with **400 Notre Dame Avenue**:
  - https://canada.constructconnect.com/dcn/certificates-and-notices/782E317F-A767-4C21-85DF-D664B9EB1851

With evidence state `conflicting`, current PROGRAMSTART still yields bounded investigation rather than execution:

- **route:** `investigate`
- **research depth:** `targeted`
- **evidence action:** `resolve-the-decision-relevant-conflict`.

The safe disposition is not to choose `Street` or `Avenue` merely because one source looks more convenient. The destination should be bound to the intended real-world entity — **Food Basics #697 + phone 705-675-5845 + verified business identity/pin** — and the ambiguous text address must not be passed directly to routing until identity/location is resolved.

The other highlighted stores were also checked against current first-party store listings:

- Food Basics #610 — 1800 Lasalle Boulevard:
  - https://www.foodbasics.ca/find-a-grocery/100610
- Food Basics #638 — 1875 Regent Street South:
  - https://www.foodbasics.ca/find-a-grocery/100638
- Metro Lasalle Court Mall — 900 Lasalle Boulevard:
  - https://www.metro.ca/en/find-a-grocery/278

## Canonical task-state replay

The original screenshot defines one canonical four-entity task set. Completion is a separate property of those entities.

The replayed state rule is:

`canonical item identity != conversational completion status`

A completion statement may transition a matched item from `PENDING` to `COMPLETED`; it must not silently add, remove, substitute, rename, or resurrect canonical items.

If a later natural-language claim conflicts with the canonical set — for example, describing two Food Basics locations on Lasalle when the canonical set contains only one Food Basics on Lasalle — the correct behavior is to reconcile the contradiction against the canonical set before changing state.

This observation does **not** claim that PROGRAMSTART currently provides a standalone persisted grocery-task state engine. It records the acceptance semantics that a PROGRAMSTART-governed work packet/current-authority flow should preserve and identifies the original chat behavior as non-conformant with that discipline.

## Mechanical acceptance criteria

- **A1 — exact extraction:** recover exactly the four highlighted entities from the fixture; no omission, duplicate, or invented store.
- **A2 — evidence classification:** screenshot-only real-world business-location data is classified as partial/changing, not sufficient.
- **A3 — router activation:** the current adaptive router returns `investigate / targeted` before navigation.
- **A4 — current verification:** each physical destination is checked against current credible evidence before routing.
- **A5 — conflict preservation:** the #697 Street/Avenue disagreement remains `CONFLICTING_EVIDENCE` until resolved; the router remains investigative.
- **A6 — entity-first resolution:** ambiguous address text is not sent directly to navigation; resolve Food Basics #697 by store identity, matching phone/business identity, and a verified physical pin/location.
- **A7 — immutable canonical set:** the four source entities remain the canonical task set throughout the session.
- **A8 — completion is separate state:** later completion statements update item status only; a contradictory statement triggers reconciliation rather than silent mutation.
- **A9 — route eligibility:** only `VERIFIED + PENDING` items are eligible for route computation.
- **A10 — closure challenge:** every original highlighted entity is accounted for exactly once; no completed item is resurrected and no pending item is omitted.
- **A11 — privacy:** private/live operator location is not persisted in PROGRAMSTART acceptance evidence.
- **A12 — evidence honesty:** do not claim a durable runtime task-state engine or navigation engine was tested when this replay only verified current methodology/routing semantics and source evidence.

## Evidence

### Repository / methodology evidence

- PROGRAMSTART current main recovered at `20cc75e2185933d3728a310a3fe4eaf5e44b09f5`.
- Current adaptive router logic was inspected directly from `scripts/programstart_decision.py`.
- The current Learning Loop, acceptance checklist, Work Packet discipline, Challenge Gate, and concise learning ledger were inspected before classifying the result.
- The concise ledger was searched before considering any new lesson. No existing lesson identity was replaced and no new `PSL-###` is created by this observation.

### External evidence actually checked

- first-party Food Basics listings for #610, #638, and #697;
- first-party Metro listing for 900 Lasalle;
- Greater Sudbury municipal material for Food Basics #697;
- bounded independent corroboration for the #697 Avenue identity.

### Checks not performed / not claimed

- No route-optimization algorithm was benchmarked.
- No navigation provider's turn-by-turn engine was acceptance-tested.
- No standalone persisted task-state runtime was created or validated.
- No user live-location data was added to PROGRAMSTART.
- No production machinery, controller, scheduler, database, route planner, or state service was changed.

## PROGRAMSTART behavior

- **What PROGRAMSTART did in the replay:** current authority was recovered first; the adaptive decision router was applied to the actual decision/evidence shape; current evidence was checked only to the point needed to resolve the routing decision; the Learning Gate and existing lesson ledger were consulted before persistence.
- **What helped:** current router semantics would have forced targeted verification before route execution and would have kept the discovered #697 conflict in investigation rather than silently geocoding it.
- **What created friction or uncertainty:** PROGRAMSTART was not invoked in the original ordinary chat flow, so the assistant treated extracted address text as executable fact. The secondary conversational task-state drift occurred outside a durable PROGRAMSTART work-packet/state surface.
- **Was existing methodology sufficient?** **Yes for the entity/evidence-routing failure.** Current methodology already encodes the needed targeted-research and conflict-resolution behavior. The casual-chat durable task-state case is not proven as a standalone runtime capability and does not by itself earn new machinery.

## Learning decision

- **Existing lesson match:** no exact new lesson required; this is a confirmation of existing adaptive decision/research routing plus a useful explicit Learning Gate observation.
- **Maturity before:** no dedicated lesson.
- **Maturity after:** no change.
- **Why maturity does not change:** the real incident is material, but replaying it against current PROGRAMSTART shows the core preventive behavior already exists. The failure was primarily invocation/conformance: the methodology was not applied before action.
- **PROGRAMSTART change required now:** **none**.
- **First broken contract:** screenshot-derived real-world destinations were treated as sufficient executable facts instead of partial/changing evidence, so the adaptive decision/evidence router was not invoked before navigation.
- **Secondary broken contract:** the canonical four-item task set and item completion status were allowed to collapse into conversational reconstruction instead of remaining separate concepts.

## Retest

- **Next real condition that could strengthen/challenge this finding:** another natural one-off task begins from an image/list of time-sensitive real-world entities and requires an action with a meaningful physical consequence.
- **Sufficient evidence:** PROGRAMSTART is actually invoked; initial partial/changing evidence routes to targeted verification; any identity/address conflict blocks action until entity resolution; the canonical item set survives later completion updates without omission/substitution/resurrection; private live location remains ephemeral; the final action uses only verified pending entities.
- If that flow still sends the operator to an unresolved/wrong entity, the evidence would challenge the conclusion that current methodology is sufficient and could earn a bounded owner-level change.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio spine was created.
- [x] No secrets or unnecessary private payloads were copied into this observation.
- [x] Private live location was intentionally excluded.
- [x] Evidence claims match checks actually performed.
- [x] The explicit acceptance test is preserved without manufacturing a new lesson or methodology change.
