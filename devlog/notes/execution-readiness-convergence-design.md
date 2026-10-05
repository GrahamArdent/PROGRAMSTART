# Execution Readiness Convergence — Non-Authoritative Design Record

**Date:** 2026-10-05  
**Status:** DESIGN PROPOSAL / NON-AUTHORITATIVE  
**Repository:** `GrahamArdent/PROGRAMSTART`  
**Placement:** `devlog/notes/`  
**Intent:** Durable reference for a proposed PROGRAMSTART improvement.  
**Execution authority:** None.  
**Canonical authority changed by this file:** None.

> This document is deliberately non-authoritative. It records a design that has been challenged to a stable position for the current scope, but it does not amend PROGRAMBUILD policy, grant execution permission, replace repository-native instructions, or supersede any current PROGRAMSTART control file.

---

## 1. Executive design decision

PROGRAMSTART should gain a reusable **Execution Readiness Convergence** pattern that ensures consequential implementation planning actually consumes the repository-native instructions that govern the intended work surface, then challenges the resulting execution candidate repeatedly until no new **material corrective delta** survives.

The pattern is not a replacement for repository instruction files, `AGENTS.md`, PROGRAMBUILD Work Packets, the JIT source-of-truth protocol, the Challenge Gate, Decision Closure, Matrix projection, or owner-native authority.

It is a bridge among those mechanisms.

The proposed pattern is:

```text
objective
  -> current owner / authority
  -> intended read + write surface
  -> applicable repository-native instruction resolution
  -> material instruction-derived constraints
  -> existing machinery / capability discovery
  -> bounded candidate plan / Work Packet
  -> PROGRAMSTART Challenge
  -> incorporate material corrective deltas
  -> re-Challenge revised candidate
  -> repeat until no new material corrective delta survives
  -> scoped GO / NO-GO
  -> authority reconciliation when required
  -> re-read current owner truth
  -> execute
  -> post-implementation adversarial Challenge when triggered
  -> durable evidence / terminality reconciliation
```

The central design rule is:

> **Resolve instructions from the work surface, derive the plan from current authority, and converge the plan through material-delta Challenge before consequential mutation.**

---

## 2. Problem being solved

PROGRAMSTART already contains strong methodology for:

- current authority and JIT context loading;
- one strategic execution spine;
- bounded Work Packets;
- proportional rigor;
- evidence reuse and invalidation;
- adaptive decision routing;
- Challenge Gates;
- canonical-before-dependent changes;
- owner-native decision settlement;
- post-implementation adversarial review.

Repositories may also contain strong local operating knowledge in mechanisms such as:

- `AGENTS.md`;
- repository-wide Copilot or agent instruction files;
- path-scoped instruction files;
- contribution guidance;
- generated workflow guidance;
- tool-specific instruction surfaces;
- local validation/publication rules.

The observed gap is not that this information does not exist. The gap is that an executor can technically "have" repository instructions available without demonstrating that the instructions applicable to the actual intended write surface materially shaped the execution plan.

That creates several failure modes:

1. **Passive-instruction failure** — repository guidance exists but is not operationally reflected in the plan.
2. **Root-only failure** — an executor reads one top-level instruction file while missing path-specific instructions governing the changed files.
3. **Scope-expansion failure** — a plan begins under one instruction set, expands to a new surface, and continues under stale assumptions.
4. **Template-duplication failure** — a new universal template restates local instructions, drifts from them, and becomes a shadow authority.
5. **One-pass review failure** — a plan receives a Challenge, changes materially, but the changed candidate is not challenged again.
6. **Ceremonial-loop failure** — "challenge until settled" becomes an arbitrary repeat count or endless review loop rather than evidence-driven convergence.
7. **False-settlement failure** — "settled" is mistaken for owner acceptance, execution permission, universal completeness, or permanent validity.

Execution Readiness Convergence is designed specifically to prevent these failures without creating another strategic plan or lifecycle.

---

## 3. Design constraints

The design must preserve the following existing PROGRAMSTART doctrines.

### 3.1 One concern, one primary owner

This design must not create a new canonical file that duplicates responsibilities already owned by:

- `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`;
- `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md`;
- `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md`;
- `.github/instructions/source-of-truth.instructions.md`;
- current project/repository authority.

If adopted, the design should be decomposed into small deltas to those owners rather than promoted wholesale as a new competing control document.

### 3.2 Repository instructions remain authoritative for local operating constraints

Execution Readiness Convergence must reference repository-native instructions, not copy them into a second truth store.

The design therefore requires:

- references to applicable instruction sources;
- extraction only of the material constraints needed by the current slice;
- re-resolution when scope changes.

It must not create a PROGRAMSTART-maintained mirror of every repository's instructions.

### 3.3 Work Packets remain derived context

A Work Packet may carry the resolved instruction evidence and convergence result, but it remains subordinate to current project authority.

A Work Packet must not become:

- strategy;
- architecture authority;
- decision authority;
- instruction authority;
- a hidden backlog.

### 3.4 "Settled" is scoped convergence evidence, not authority

In this design, `settled` means:

> The current candidate, for the declared scope and currently trusted evidence, has received a fresh adversarial Challenge and that Challenge produced no new material corrective delta that must be incorporated before the candidate can proceed to its next authorized boundary.

It does **not** mean:

- the idea is accepted by the owner;
- execution is authorized;
- the result is universally complete;
- no future evidence can reopen the design;
- Matrix is authoritative;
- Decision Closure has been bypassed;
- post-implementation review can be skipped.

### 3.5 Narrow while executing; widen while converging

The design should preserve PROGRAMBUILD's existing economy rule.

Instruction discovery, evidence loading, and Challenge scope should be the smallest set sufficient for the actual changed surface and current risk.

"Use all instructions" does not mean "load the entire repository."

---

## 4. Terminology

### Execution candidate

The current bounded proposal for how to perform the next consequential slice.

It may be represented by:

- a compact Work Packet;
- a persisted Work Packet when warranted;
- a PR/task plan;
- an implementation plan;
- another current derived execution representation.

### Intended work surface

The files, directories, repositories, runtime/provider resources, contracts, schemas, configuration, or other consequential surfaces the candidate expects to read, change, or rely on.

The write surface is especially important because path-scoped instructions may differ.

### Repository-native instruction source

Any current, project-recognized instruction mechanism that constrains how work on the intended surface must be performed.

Examples include `AGENTS.md`, `.github/copilot-instructions.md`, path-scoped `.github/instructions/*.instructions.md`, contribution/build instructions, or equivalent repository-native mechanisms.

This design intentionally does not hard-code `AGENTS.md` as the only valid instruction form.

### Material instruction-derived constraint

A repository instruction that can change the candidate's:

- allowed scope;
- write surface;
- sequencing;
- command/tool choice;
- authority resolution;
- safety boundary;
- validation;
- publication path;
- evidence requirement;
- terminal condition;
- dependency handling.

Non-material prose need not be copied into the packet.

### Material corrective delta

A Challenge finding that changes one or more of:

- authority or owner resolution;
- protected outcome or objective;
- scope or exclusions;
- intended read/write surface;
- applicable instruction set;
- architecture or contract assumptions;
- sequencing or dependency order;
- execution mechanism;
- blocker classification;
- safety/gate boundary;
- evidence or currentness requirements;
- verification;
- acceptance or terminal condition;
- post-implementation review trigger.

Editorial wording changes, restatements, or observations that do not alter the candidate's behavior are not material corrective deltas.

### Convergence pass

One Challenge of the **current candidate**, followed by classification of findings into material corrective deltas versus non-material observations.

### Settled candidate

A candidate whose latest fresh Challenge produces no new material corrective delta for the declared scope and evidence state.

---

## 5. Instruction-resolution contract

Before consequential implementation planning is treated as execution-ready, the executor should resolve the instruction set applicable to the intended work surface.

### 5.1 Required output

The smallest useful representation is:

```text
INSTRUCTION_RESOLUTION:
  intended_surface:
    - <repo/path/resource>
  instruction_sources:
    - <current repository-native source/reference>
  material_constraints:
    - <constraint that actually affects this slice>
  unresolved_instruction_conflicts:
    - <none | explicit conflict>
  re_resolution_triggers:
    - <scope/path/authority/instruction change that invalidates this result>
```

This may be compressed when simple.

The requirement is semantic, not paperwork. A one-file low-risk edit may need only a sentence. A multi-repository or path-sensitive change may require a fuller map.

### 5.2 Resolution algorithm

For each intended mutation surface:

1. identify the repository and current owner;
2. identify the repository-native instruction mechanisms recognized by that repository/tooling;
3. resolve repository-wide instructions;
4. resolve any more-specific path-scoped instructions applicable to the target;
5. resolve precedence/conflict using the repository's own instruction semantics;
6. extract only constraints material to the current candidate;
7. bind those constraints into the plan/Work Packet;
8. record what would invalidate the resolution.

### 5.3 Scope expansion

If execution discovers a new consequential write surface that was not part of the settled candidate:

1. stop mutation on the new surface;
2. add the new surface to the candidate;
3. resolve applicable instructions for it;
4. re-evaluate current authority and dependency implications;
5. determine whether the change is a material corrective delta;
6. if material, re-Challenge the revised candidate before proceeding.

Read-only discovery may continue where independently safe and authorized.

### 5.4 Instruction conflicts

If two applicable instruction sources materially conflict and repository-native precedence cannot resolve the conflict:

- fail closed for the conflicting dependent mutation;
- preserve unrelated safe work where independently authorized;
- route the conflict to the appropriate repository owner/authority;
- do not silently choose whichever instruction is more convenient.

---

## 6. Execution Readiness Convergence loop

### 6.1 Entry

The loop begins after the executor has enough current context to form a bounded candidate.

Typical prerequisites are:

- objective / protected outcome understood;
- current project or owner authority identified;
- intended work surface bounded enough to resolve instructions;
- reusable evidence/currentness understood;
- existing machinery/capability discovery performed to the degree material to the plan.

For a Mode-C existing project, do not restart a new lifecycle. The candidate must be a delta to the current execution spine.

### 6.2 Challenge pass

Challenge the current candidate using the minimum relevant PROGRAMSTART controls.

At minimum, ask:

1. **Authority:** Does the candidate trace to current owner/project authority?
2. **Instruction fit:** Were all materially applicable repository-native instructions resolved for the intended surface?
3. **Scope:** Is the candidate bounded, or has a hidden adjacent problem entered?
4. **Reuse:** Is existing machinery being reused before inventing new mechanisms?
5. **Dependency/currentness:** Are the authority, dependencies, and evidence current enough for this decision?
6. **Execution surface:** Does the plan name the actual surfaces it intends to mutate?
7. **Proof:** Is there a credible targeted verification and terminal condition?
8. **Failure semantics:** Does the plan say what happens if a prerequisite, projection, validation, or runtime step fails?
9. **Duplicate-authority test:** Is any derived artifact becoming a second strategic or local-instruction authority?
10. **Completeness:** Could every listed step succeed while the objective remains materially false?

Use more specific Challenge Gate parts when the current boundary requires them.

### 6.3 Incorporation

Each Challenge finding is classified:

- `MATERIAL_CORRECTIVE_DELTA`;
- `NON_MATERIAL_OBSERVATION`;
- `OUT_OF_SCOPE_FOLLOWUP`;
- `BLOCKING_UNRESOLVED`.

Material corrective deltas are incorporated into the candidate before the next pass.

An out-of-scope follow-up must not silently expand the current candidate. Preserve it through the normal owner/idea/finding mechanism if it is worth retaining.

A blocking unresolved finding prevents settlement only for the dependent boundary it controls.

### 6.4 Re-Challenge

If one or more material corrective deltas were incorporated, the revised candidate is a new candidate.

Challenge the new candidate again.

Do not declare settlement from a Challenge performed against a superseded version of the plan.

### 6.5 Stop condition

The loop stops successfully on the first pass where:

- no new material corrective delta is produced;
- no blocking unresolved finding controls the next boundary;
- the instruction-resolution evidence remains current;
- the candidate still traces to current owner/project authority.

This is **material-delta convergence**, not a fixed number of passes.

### 6.6 Anti-loop rule

Do not continue re-Challenging merely to obtain another identical "clear."

A further pass requires an invalidation signal such as:

- candidate changed materially;
- scope changed;
- applicable instructions changed;
- authority changed;
- new contradictory evidence appeared;
- relevant dependency/runtime state changed;
- evidence was invalidated;
- an explicitly required independent/convergence review boundary was reached.

---

## 7. Settlement invalidation

A settled candidate is reopened when an event can materially change its correctness.

Default invalidation triggers include:

### Scope invalidation

- new repository;
- new directory/path governed by different instructions;
- new runtime/provider/deployment mutation;
- materially wider blast radius.

### Authority invalidation

- owner decision changed;
- current strategic execution spine changed;
- accepted recommendation disposition changed;
- relevant architecture/requirements/decision record changed.

### Instruction invalidation

- applicable repository instruction file changed;
- a newly discovered more-specific instruction source applies;
- instruction precedence/conflict was previously unresolved.

### Evidence/currentness invalidation

- code/config/schema/environment changed on the relied-upon surface;
- dependency/provider behavior materially changed;
- prior evidence was contradicted;
- a currentness fence reports mismatch.

### Plan invalidation

- implementation approach changed materially;
- a prerequisite was discovered;
- execution mechanism changed;
- the terminal condition or acceptance proof changed.

A session boundary or elapsed time alone is not invalidation unless the underlying fact is time-sensitive.

---

## 8. Relationship to current PROGRAMSTART mechanisms

### 8.1 Idea Intake

Idea Intake asks whether a proposed idea or Mode-C delta is coherent enough to advance.

Execution Readiness Convergence begins later, when there is a concrete bounded execution candidate.

It should not duplicate the eight Idea Intake dimensions when they are already settled and current.

### 8.2 Adaptive decision router

The adaptive router determines whether the next material decision can execute, needs focused checks, or needs additional evidence.

Its current evidence can be reused by Execution Readiness Convergence.

The convergence loop does not become a second research router.

### 8.3 Work Packet

The Work Packet is the natural carrier for task-scoped instruction-resolution and convergence evidence.

If adopted, likely additions would be conditional fields such as:

```text
INSTRUCTION_RESOLUTION:
MATERIAL_INSTRUCTION_CONSTRAINTS:
INSTRUCTION_INVALIDATION_TRIGGERS:
READINESS_CONVERGENCE:
  candidate_ref:
  challenge_passes:
  latest_result: [clear | warning | blocked]
  latest_material_deltas: [none | ...]
  settled_for_scope: [yes | no]
  settlement_scope:
  invalidation_triggers:
```

These should be conditional, not mandatory boilerplate for trivial tasks.

### 8.4 Challenge Gate

The existing Challenge Gate should remain the owner of adversarial stage/convergence/closure review.

If this design is adopted, Challenge Gate semantics may need a small clarification:

> When a Challenge changes the candidate materially, re-Challenge the corrected candidate before treating that boundary as clear.

This is a general convergence rule, not a new gate.

### 8.5 JIT source-of-truth protocol

The JIT protocol is the natural owner for instruction discovery.

A future canonical delta would likely say that the "smallest current authority/evidence set" includes the repository-native instructions applicable to the actual intended surface, not merely a generic root instruction reference.

### 8.6 Product JIT Check

The existing Product JIT Check is the best current operator-facing reference point.

Rather than creating a second general-purpose execution template, it can eventually become the reusable prompt/view that asks the executor to:

- state intended write surfaces;
- resolve applicable repository-native instructions;
- show material constraints;
- run readiness convergence before implementation.

### 8.7 Decision Closure

Decision Closure remains upstream when a materially new or changed accepted decision needs owner settlement.

Execution Readiness Convergence must not convert conversational acceptance into execution authority.

Where Decision Closure applies:

```text
conversation / evidence
  -> material decision classification
  -> owner-native settlement
  -> re-read current owner truth
  -> protected outcome / obligations
  -> Matrix projection when operationalized
  -> bounded Work Packet
  -> Execution Readiness Convergence
  -> execution
```

A non-operational accepted decision may stop at owner durability as current doctrine permits.

### 8.8 Matrix

Matrix remains projection/read model, not authority.

A Matrix view may help resolve current obligations and dependencies, but a settled execution candidate must still bind to current owner truth and the applicable local execution instructions.

### 8.9 Post-implementation adversarial review

Pre-implementation convergence does not prove implementation correctness.

If the actual completed change triggers the post-implementation adversarial Challenge Gate, that review still runs against the completed implementation.

A plan may be settled and the code may still be wrong.

---

## 9. Proposed compact reusable template

This is a **reference shape**, not a new canonical file.

```text
EXECUTION READINESS

OBJECTIVE:
CURRENT OWNER / AUTHORITY:
PROTECTED OUTCOME:
INTENDED READ SURFACE:
INTENDED WRITE SURFACE:

INSTRUCTION RESOLUTION
- applicable sources:
- material constraints:
- unresolved conflicts:
- re-resolution triggers:

EXISTING MACHINERY / CAPABILITY REUSE:
DEPENDENCIES / CURRENTNESS:
IN SCOPE:
OUT OF SCOPE:
TARGETED VERIFICATION:
TERMINAL CONDITION:

READINESS CONVERGENCE
Pass 1:
- challenge result:
- material corrective deltas:
- corrections incorporated:

Pass N:
- challenge result:
- new material corrective deltas:

SETTLED FOR DECLARED SCOPE:
[yes | no]

SETTLEMENT BASIS:
Latest fresh Challenge produced no new material corrective delta.

INVALIDATION TRIGGERS:
- scope expansion
- applicable instruction change
- authority/currentness change
- contradictory evidence
- material plan change

GO / NO-GO:
- exact boundary authorized to proceed:
- exact boundary still blocked:

POST-IMPLEMENTATION CHALLENGE TRIGGER:
[known-required | evaluate actual changed surface at closure]
```

The pass history should stay compact. Preserve only deltas that materially changed the candidate; do not create a diary of repetitive clear passes.

---

## 10. Failure semantics

### Missing instruction source

If the repository has a recognized instruction mechanism but the required instruction source cannot be read:

- do not guess its contents;
- block dependent mutation;
- continue unrelated safe work only if independently authorized.

### Unknown instruction mechanism

If the executor cannot determine how repository-native instructions are represented:

- use existing repository/tooling discovery first;
- do not default to creating a universal `AGENTS.md`;
- treat unresolved local-operating policy as a bounded readiness gap.

### Material Challenge delta found

Candidate is not settled.

Incorporate the delta and re-Challenge.

### Repeated identical Challenge result

Stop. Additional identical passes add no evidence unless a separate required independent review applies.

### Owner authority changes during convergence

Discard stale settlement claim, re-read current owner truth, refresh candidate, and re-Challenge.

### Matrix becomes stale

Owner truth remains authoritative.

Rebuild/reconcile Matrix as current doctrine requires; do not roll back owner truth merely because projection is stale.

### Implementation discovers wider scope

Do not mutate the newly discovered scope until instruction resolution, authority/currentness, and readiness convergence are updated for that scope.

---

## 11. Design examples

### Example A — narrow code change

A project has:

- repository-wide `AGENTS.md`;
- a nested `src/payments/AGENTS.md`;
- current issue authority permitting a fix in `src/payments/retry.py`.

The executor resolves both applicable instruction files, extracts that payment retries require an idempotency regression test and a specific local command, and adds those constraints to the Work Packet.

Challenge finds the plan would change persistence semantics without recovery testing.

That is a material corrective delta.

The plan is corrected and challenged again.

The second pass finds no new material delta.

The candidate is settled **for the declared payment-retry scope**, not globally.

### Example B — scope expansion

A settled frontend candidate later discovers that the fix requires changing an auth middleware path governed by different instructions.

The original settlement is not valid for the middleware mutation.

The agent may keep inspecting, but before mutating middleware it must:

- resolve the middleware instruction set;
- refresh authority/architecture implications;
- update the candidate;
- re-Challenge.

### Example C — PROGRAMSTART itself

PROGRAMSTART currently uses repository-wide `.github/copilot-instructions.md` plus path-scoped `.github/instructions/*.instructions.md`.

An implementation agent editing `PROGRAMBUILD/*.md` should therefore not assume `AGENTS.md` is the required mechanism.

It should resolve the actual current instruction sources that govern `PROGRAMBUILD/` and the JIT/source-of-truth rules material to the change.

This example is one reason the design uses the term **repository-native instruction set** rather than **AGENTS file**.

### Example D — no material delta

A small documentation typo has current authority, one applicable repo-wide instruction, no path-specific constraints, no behavior impact, and trivial verification.

The first Challenge produces no material corrective delta.

Settlement occurs in one pass.

The design must not require an artificial second pass merely to prove repetition.

---

## 12. Challenge history that produced this design

This record captures the converged result of the 2026-10-05 brainstorming cycle.

### Pass 1 — standalone "agent-aware execution template"

Finding:

- a standalone canonical template would duplicate Work Packet, JIT, and Challenge Gate responsibilities;
- risk of creating a second authority.

Correction:

- integrate semantics into current PROGRAMSTART owners;
- keep any reusable template as a derived/operator-facing representation.

### Pass 2 — `AGENTS.md`-specific design

Finding:

- too narrow;
- PROGRAMSTART itself relies on repository-wide and path-scoped `.github` instruction mechanisms.

Correction:

- define repository-native instruction resolution;
- make `AGENTS.md` one possible mechanism.

### Pass 3 — "challenge until settled"

Finding:

- unconstrained repetition can become ceremonial or infinite.

Correction:

- define material-delta convergence;
- re-Challenge only after material candidate change/invalidation;
- stop on the first fresh pass with no new material corrective delta.

### Pass 4 — settlement semantics

Finding:

- "settled" could be misread as authority, acceptance, or permanent completeness.

Correction:

- settlement is scoped convergence evidence only;
- define explicit invalidation triggers;
- preserve owner-native authority and stronger gates.

### Pass 5 — final structural challenge

Attacks applied:

- duplicate authority;
- instruction precedence;
- scope expansion;
- stale currentness;
- self-attested completeness;
- infinite-loop risk;
- Decision Closure collision;
- Matrix authority leakage;
- post-implementation false confidence;
- trivial-work ceremony.

Result:

- no further material structural correction identified for the current design scope.

This result is evidence that the design is stable enough to preserve for reference. It is not proof that PROGRAMSTART should adopt it unchanged.

---

## 13. Candidate canonical adoption map

If later implementation is approved, prefer **small owner-native deltas** rather than promoting this file to authority.

Likely owners:

| Concern | Candidate current owner |
|---|---|
| instruction-resolution / JIT discovery semantics | `.github/instructions/source-of-truth.instructions.md` |
| proportional use, Mode-C behavior, settlement invalidation | `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` |
| task-scoped fields / evidence carrier | `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` |
| challenge -> correction -> re-Challenge convergence rule | `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` |
| operator-facing pre-implementation reference | `.github/prompts/product-jit-check.prompt.md` |
| cross-file authority/index only if a new critical owner is actually created | `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md`, `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md`, registry |

The preferred design currently creates **no new canonical PROGRAMBUILD control file**.

---

## 14. Candidate acceptance tests for future adoption

A future implementation should not be considered successful merely because documentation was edited.

Useful acceptance fixtures should prove behavior such as:

1. **Root + nested instruction resolution**
   - nested write surface activates the correct more-specific instruction constraints.

2. **No duplicated instruction truth**
   - packet stores references/material constraints, not a copied instruction corpus.

3. **Scope expansion invalidates settlement**
   - a new path with a different instruction scope forces re-resolution before mutation.

4. **Material Challenge delta forces re-Challenge**
   - candidate cannot report settled from the Challenge that changed it.

5. **Non-material wording change does not force loop**
   - no ceremony from irrelevant deltas.

6. **One-pass settlement is valid**
   - first fresh Challenge may settle a simple candidate.

7. **Owner change invalidates settlement**
   - stale plan cannot continue after relevant authority changes.

8. **Instruction conflict fails closed**
   - unresolved conflicting local guidance blocks only the dependent mutation.

9. **Post-implementation Challenge remains independent**
   - pre-implementation settlement does not suppress risk-triggered closure review.

10. **Mode-C preservation**
    - applying the design to an existing project produces a bounded delta, not a new master plan.

11. **Repository-native mechanism neutrality**
    - fixture works with `AGENTS.md`, `.github` instructions, or another recognized mechanism without PROGRAMSTART forcing one universal format.

12. **No execution authority leakage**
    - settlement receipt/result cannot itself authorize a stronger action.

---

## 15. Falsifiers

The design should be rejected or materially simplified if implementation evidence shows that it:

- consistently duplicates existing Work Packet/JIT behavior without preventing a real failure class;
- requires broad repository reads for ordinary tasks;
- causes agents to copy instruction files into derived artifacts;
- creates a de facto new lifecycle/status system;
- materially slows trivial work;
- makes "settled" harder to reason about than the current Challenge Gate;
- competes with repository-specific instruction precedence;
- causes frequent false invalidations on session/time changes;
- encourages agents to self-certify authority;
- makes a new universal instruction format necessary.

---

## 16. Open design questions

These are implementation questions, not blockers to preserving this design.

1. **How much of instruction resolution should be mechanically discoverable?**
   - The preferred direction is to use repository/tool-native discovery when available and avoid a bespoke global instruction registry.

2. **Should a compact Work Packet expose an explicit `settled_for_scope` field?**
   - It may be useful, but a boolean risks overclaiming. A result plus scope + latest Challenge evidence may be safer.

3. **Should the Product JIT prompt own the user-facing template, or should a separate prompt be introduced?**
   - Current preference: extend Product JIT before creating another prompt.

4. **How should instruction-currentness be referenced?**
   - Prefer current commit/blob/ref evidence already available through repository mechanisms rather than inventing a global instruction version service.

5. **What independent-review level is required for high-risk readiness convergence?**
   - Reuse existing Challenge Gate risk semantics rather than hard-coding a new reviewer-count rule.

---

## 17. Recommended next step if adoption is later authorized

Run a fresh Mode-C implementation pass against current PROGRAMSTART head and:

1. re-read the current canonical owners named in §13;
2. check for intervening changes since this design record;
3. derive the smallest canonical deltas;
4. define focused fixtures/tests for §14;
5. Challenge the implementation plan using this design's own convergence rule;
6. only then edit canonical PROGRAMSTART surfaces;
7. run repository-required validation/drift/CI;
8. apply post-implementation adversarial review if the actual changed surface triggers it.

This document itself must not be used as execution authority for that implementation.

---

## 18. Reference summary

**Name:** Execution Readiness Convergence  
**Problem:** repository instructions and PROGRAMSTART methodology can exist without being mechanically bound into the actual execution candidate.  
**Core mechanism:** resolve applicable repository-native instructions by intended work surface; bind material constraints into the bounded candidate; Challenge; incorporate material deltas; re-Challenge until the latest current candidate yields no new material corrective delta.  
**Settlement meaning:** scoped convergence evidence only.  
**Primary invalidators:** scope, authority, instructions, evidence/currentness, or material plan change.  
**Preferred adoption:** small deltas to existing canonical owners; no new lifecycle and no new canonical template by default.
