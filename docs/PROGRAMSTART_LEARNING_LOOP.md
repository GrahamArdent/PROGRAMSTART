# PROGRAMSTART Learning Loop

Purpose: make real-project usage improve PROGRAMSTART without turning product projects into methodology experiments, creating a portfolio plan, or recording every routine action as "learning."

Status: **PROGRAMSTART operational protocol / subordinate to product-project authority**.

This protocol owns how PROGRAMSTART evaluates, records, matures, and retests reusable methodology lessons. It does **not** own any product project's scope, execution spine, lifecycle, release decision, backlog, or product/system operational-learning policy. When real operation reveals a potential improvement to the software/system itself, route that observation through `docs/PROGRAMSTART_LEARNING_ARCHITECTURE.md` to the owner of the behavior.

## 1. Core Loop

PROGRAMSTART learns through:

**REAL PROJECT EXECUTION → MEANINGFUL CHECKPOINT → LEARNING GATE → OBSERVATION RECORD → MATURITY ROLLUP → PROGRAMSTART CHANGE, IF EARNED → REAL RETEST**

The loop is evidence-driven. A project may complete a PROGRAMSTART-assisted slice and teach PROGRAMSTART **nothing new**. `no reusable lesson` is a successful Learning Gate result.

## 2. When the Learning Gate Runs

Run the Learning Gate at a **meaningful checkpoint**, not after every commit or chat turn.

Default triggers:

- a bounded PROGRAMSTART work packet is accepted/closed;
- a material operator/manual gate returns evidence and execution resumes;
- a significant Mode-C re-entry or convergence pass completes;
- a cross-repository dependency acceptance point is resolved;
- a real physical-device/provider/runtime/human acceptance step changes what was believed;
- PROGRAMSTART itself caused material friction, ambiguity, wasted work, unsafe routing, unnecessary ceremony, or a useful reduction in work;
- the user explicitly declares the project/session a PROGRAMSTART acceptance test;
- a previously open PROGRAMSTART lesson is directly retested by the current situation.

Do **not** trigger a durable learning write merely because:

- PROGRAMSTART was mentioned;
- a routine commit/PR merged;
- normal implementation succeeded exactly as expected;
- the observation is purely product-specific and has no reusable methodology implication;
- the only result would duplicate an already-recorded observation without strengthening or challenging it.

## 3. Learning Gate Questions

At a trigger, answer in order:

1. **What happened in the real project?** Use repository/runtime/provider/acceptance evidence, not conversational impression alone.
2. **Did PROGRAMSTART materially help, hinder, or fail?** Name the exact behavior.
3. **Is the observation local or systemic?**
   - `local` — belongs only in the product/system owner's evidence/authority; if it implies reusable operational improvement to that system, route it through `docs/PROGRAMSTART_LEARNING_ARCHITECTURE.md` rather than forcing it into the PROGRAMSTART ledger;
   - `systemic` — plausibly reusable across projects as PROGRAMSTART methodology;
   - `confirmation` — retests an existing PROGRAMSTART rule without exposing a new gap;
   - `counterevidence` — weakens, rejects, or narrows an existing PROGRAMSTART lesson.
4. **Does an existing lesson already cover it?** Search the maturity ledger before creating a new lesson.
5. **What changed in evidence maturity?** `none`, `observe`, `candidate`, `implemented`, `validated`, or `rejected`.
6. **Does PROGRAMSTART need to change now?** Complexity must be earned by repeated/material evidence. A new feature is not the default result.
7. **What real situation should retest the lesson next?** Name a condition, not a speculative project roadmap.

## 4. Recording Model

Use two layers so the central ledger stays readable.

### A. Observation records — append evidence

Path:

`docs/acceptance/observations/YYYY-MM-DD-<project-or-system>-<slug>.md`

Observation records are append-only evidence artifacts. They capture one meaningful acceptance observation and remain subordinate/non-canonical.

Use `docs/acceptance/LEARNING_OBSERVATION_TEMPLATE.md`.

Observation records MAY be created when:

- a new systemic lesson appears;
- an existing lesson receives materially stronger or contradictory evidence;
- a methodology change is really retested;
- an explicit acceptance test produces a useful `no change`/confirmation result that would otherwise be lost.

Do not create a new observation for routine duplicate confirmation with no maturity impact.

### B. Learning ledger — synthesize maturity

`docs/PROGRAMSTART_ACCEPTANCE_LEARNING_LEDGER.md` is the concise rollup.

Update it only when the evidence materially changes one of:

- lesson summary;
- maturity state;
- implementation/validation status;
- strongest evidence pointer;
- next retest condition;
- rejection/narrowing conclusion.

The ledger is **not** the raw activity log. Detailed history belongs in observation records and preserved historical snapshots.

## 5. Lesson Identity and Deduplication

Before recording a new lesson:

1. search the current ledger for the same failure mode/outcome;
2. search recent observation records for equivalent evidence;
3. prefer strengthening/narrowing an existing lesson over inventing a synonym;
4. create a new lesson only when the owning PROGRAMSTART behavior is materially different.

A lesson should identify:

- a stable lesson ID such as `PSL-001`;
- concise problem/behavior statement;
- current maturity;
- PROGRAMSTART owner/surface;
- strongest evidence pointers;
- current implementation PR/commit when applicable;
- next retest condition.

Lesson IDs are organizational references, not execution priority.

## 6. Maturity Rules

- **observe** — plausible reusable signal; insufficient evidence for a methodology change.
- **candidate** — repeated or materially strong evidence supports a bounded change.
- **implemented** — PROGRAMSTART changed; meaningful real retest still open.
- **validated** — real retest shows the change altered execution as intended.
- **rejected** — evidence shows the proposed change was unnecessary, harmful, over-broad, or already solved by existing primitives.

Do not promote maturity because time passed, because many words were written, or because one project was inconvenient.

Counterevidence can demote/narrow a lesson. Example: one paused-project re-entry may show existing Mode-C primitives are sufficient and therefore weaken the case for a dedicated lifecycle state machine.

## 7. Automatic Behavior in PROGRAMSTART Sessions

When the current agent/session is using PROGRAMSTART orchestration:

1. normal product execution remains primary;
2. do not load the full learning history during routine implementation;
3. at a Learning Gate trigger, inspect only the current ledger plus the most relevant observation evidence;
4. classify the result;
5. if `no reusable lesson`, finish product work without a PROGRAMSTART write;
6. if a durable observation is warranted and `GrahamArdent/PROGRAMSTART` is writable in the current environment, create/update a **focused PROGRAMSTART learning PR or existing authorized PROGRAMSTART methodology branch**;
7. if PROGRAMSTART is not writable, return a structured learning handoff; product completion must not be blocked by inability to update the methodology repository;
8. never mutate PROGRAMSTART `main` merely because a product task ended; normal repository review/merge discipline still applies.

This is "automatic" in the orchestration sense: the Learning Gate evaluation is part of the protocol. The result is conditional, evidence-based persistence rather than unconditional ledger writes.

## 8. Future-Retest Routing

PROGRAMSTART should reuse the ledger in the opposite direction too.

During orientation, **only when the current situation directly matches an open retest condition**, surface the relevant lesson as acceptance context. Examples:

- a credential/device/CI gate can retest operator returned-evidence resumption;
- a project with one blocked closure row plus independently authorized preparation can retest coordinated Mode-C lanes;
- a new physical-device acceptance case can strengthen or challenge verification evidence-source/type rules.

Do not turn the ledger into a checklist that every project must exercise.

When a retest occurs:

- preserve product authority;
- do the product work for its own value;
- collect only evidence naturally produced by that work;
- update the observation/ledger after the fact if maturity changes.

## 9. PROGRAMSTART Change Gate

A learning observation does not automatically authorize a methodology change.

Before changing PROGRAMSTART:

- confirm the problem is systemic or materially high-impact;
- confirm current PROGRAMSTART does not already solve it;
- identify the smallest canonical owner/surface;
- prefer extending an existing mechanism over adding a new lifecycle/artifact/agent;
- define a real acceptance case;
- keep the methodology PR focused;
- record actual verification and do not claim unavailable checks.

After merge, mark the lesson `implemented` until a meaningful real retest earns `validated`.

## 10. Safety and Privacy

Learning records MUST NOT become a data-exfiltration path.

Do not persist:

- raw secrets, refresh tokens, service-role keys, private keys, passwords;
- unnecessary personal/private user data;
- full provider logs when a bounded result/reference is enough;
- product-private content that is irrelevant to the methodology lesson.

Prefer repository/PR/commit/run/resource references plus sanitized outcome summaries.

## 11. Organization and Maintenance

The durable learning surfaces are intentionally small:

- `docs/PROGRAMSTART_LEARNING_LOOP.md` — this protocol;
- `docs/PROGRAMSTART_ACCEPTANCE_LEARNING_LEDGER.md` — concise maturity rollup;
- `docs/PROGRAMSTART_REAL_WORLD_ACCEPTANCE_CHECKLIST.md` — human/agent checkpoint checklist;
- `docs/acceptance/observations/` — append-only meaningful observations;
- `docs/acceptance/PROGRAMSTART_ACCEPTANCE_HISTORY_THROUGH_2026-08-27.md` — preserved pre-loop detailed history.

Do not create a PROGRAMSTART portfolio Master, central product backlog, or mandatory project registry from this mechanism.

## 12. Relationship to Learning-Capable Software

PROGRAMSTART methodology learning and product/system operational learning are separate concerns.

At a meaningful checkpoint, classify the observation before persisting it:

- if PROGRAMSTART methodology caused or prevented the behavior, use this Learning Loop;
- if the product/system itself can improve from the evidence, route the observation to the owner through `docs/PROGRAMSTART_LEARNING_ARCHITECTURE.md`;
- if both are true, retain separate owner-specific evidence and changes;
- if the limitation belongs to an external provider, record only the evidence needed by the owning project's decision/handling path.

PROGRAMSTART owns the routing discipline, not every resulting lesson.

## 13. Success Test

The learning loop is working when:

- real projects keep their own authority;
- PROGRAMSTART notices methodology friction/confirmation at meaningful checkpoints;
- product/system lessons are routed to their actual owners rather than bloating the PROGRAMSTART ledger;
- useful evidence is retained without flooding the ledger;
- repeated lessons become easier to recognize across projects;
- methodology changes are smaller and evidence-earned;
- later projects naturally retest earlier lessons;
- `no PROGRAMSTART change needed` remains a common and respected outcome.