# Execution Readiness Convergence — Non-Authoritative Design Record

**Date:** 2026-10-05  
**Status:** DESIGN CONVERGED / NON-AUTHORITATIVE  
**Repository:** `GrahamArdent/PROGRAMSTART`  
**Placement:** `devlog/notes/`  
**Execution authority:** None.  
**Canonical authority changed by this file:** None.  
**Design convergence basis:** repeated PROGRAMSTART Challenge application against the current PROGRAMBUILD/JIT/Work Packet/Challenge/Decision-Closure/Capability-Discovery doctrine until the latest candidate produced no new material corrective delta.

> This record is durable reference material only. It does not amend PROGRAMBUILD, create a new lifecycle, grant execution permission, override repository or executor instructions, replace owner-native authority, or make this proposal current PROGRAMSTART methodology.

---

# 1. Executive design decision

PROGRAMSTART should support a reusable **Execution Readiness Convergence** behavior for meaningful implementation, repair, configuration, deployment-preparation, or other consequential execution slices.

Its purpose is to make three things mechanical before consequential mutation:

1. resolve the **governing execution instructions and established repository policy/authority** that actually apply to the intended consequential surface;
2. bind the material constraints from those sources into the current bounded execution candidate;
3. run the candidate through the **existing PROGRAMSTART Challenge machinery**, incorporate every material corrective delta, and re-Challenge each materially revised candidate until the current candidate is clear for its declared scope.

The design does **not** create a second Challenge Gate, second Work Packet, second strategic plan, universal instruction registry, global policy database, or new execution authority.

The preferred composition is:

```text
objective / protected outcome
  -> current owner-native authority
  -> bounded consequential surface
  -> governing execution-instruction resolution
  -> established repository policy/authority resolution
  -> material local constraints
  -> current evidence / currentness
  -> existing capability / Paths discovery only when its trigger applies
  -> bounded Work Packet / execution candidate
  -> existing PROGRAMSTART Challenge Gate
  -> material corrective deltas?
       yes -> revise exact candidate -> re-Challenge
       no  -> readiness convergence CLEAR for declared scope
  -> preserve stronger approval/consequence gates
  -> execute only when independently authorized
  -> risk-triggered post-implementation Challenge
  -> durable evidence / protected-outcome / owner reconciliation
```

The central rule is:

> **Resolve what governs the actual surface, derive from current authority, Challenge the exact candidate, and never reuse a clear result after its basis materially changes.**

---

# 2. Problem being solved

PROGRAMSTART already has strong controls for:

- current authority and just-in-time context;
- one strategic execution spine;
- bounded Work Packets;
- evidence reuse and invalidation;
- proportional rigor;
- adaptive decision routing;
- owner-native reconciliation;
- stage/convergence Challenge Gates;
- post-implementation adversarial review;
- capability discovery through Paths when consequential capability conclusions are made;
- proof durability.

Repositories and execution environments may also contain strong local operating constraints in mechanisms such as:

- `AGENTS.md` or nested agent files when supported by the current executor;
- repository-wide or path-scoped agent/Copilot instruction channels;
- repository-defined contribution, build, validation, publication, or release policy;
- current architecture/requirements/decision authority;
- tool/runtime-specific execution constraints.

The gap is not merely “an agent forgot to read AGENTS.md.”

The broader gap is:

> An executor can form and even Challenge an implementation plan without proving that the current plan reflects the instructions, local policy, owner authority, and exact changed surface that actually govern the intended consequence.

This can produce:

1. **Passive-instruction failure** — governing instructions exist but do not materially shape the plan.
2. **Root-only failure** — a generic instruction source is considered while a more specific applicable source is missed.
3. **Instruction/policy conflation** — arbitrary repository prose is promoted to model instruction authority.
4. **Scope-expansion failure** — new surfaces enter execution without re-resolving their governing constraints.
5. **One-pass Challenge failure** — a Challenge changes the plan materially, but the changed plan is never challenged.
6. **Stale-clear failure** — a previous clear result is reused after the candidate, authority, instructions, or evidence changed.
7. **Duplicate-gate failure** — a new template quietly invents a second Challenge protocol.
8. **False-settlement failure** — “settled” is mistaken for owner acceptance, execution authority, universal completeness, or permanent validity.
9. **Capability-assumption failure** — an executor declares a path unavailable, invents a new mechanism, or escalates to a human without the already-required Paths discovery.
10. **Proof-without-durability failure** — a clear result is later relied on even though no durable evidence identifies what exact candidate was challenged.

Execution Readiness Convergence is intended to close those gaps without adding a second planning hierarchy.

---

# 3. Terminology and semantic boundaries

## 3.1 Execution candidate

The current bounded proposal for the next consequential slice.

It may be represented as:

- a compact logical Work Packet;
- a persisted `CURRENT_WORK_PACKET.md` when justified;
- a PR/task implementation plan;
- a bounded execution plan in the active context;
- another project-native derived execution representation.

It is never canonical over the project’s strategic, architectural, requirements, decision, or owner-native authority.

## 3.2 Consequential surface

The files, directories, repositories, contracts, schemas, configuration, runtime/provider resources, deployment targets, or other surfaces that the candidate expects to mutate or whose current state materially controls the consequence.

Read-only evidence surfaces may matter to currentness, but this design does not require treating every file read as an “instruction scope.”

## 3.3 Governing execution instruction

A source that the **current execution environment/tool contract actually recognizes as an instruction channel** for the executor and current path/scope.

Examples can include:

- system/developer instructions supplied by the execution environment;
- `AGENTS.md` hierarchy where the current executor natively supports it;
- repository-wide or path-scoped instruction channels recognized by the current agent tooling;
- other executor-native instruction mechanisms.

PROGRAMSTART must not invent a universal precedence model for these channels. Precedence and applicability come from the current execution environment/tool contract.

## 3.4 Established repository policy/authority

Repository-owned content that constrains the work because the repository has established it as policy or canonical authority, for example:

- contribution/publication rules;
- build/test/release contracts;
- architecture;
- requirements;
- decision records;
- current strategic execution spine;
- project-specific safety or approval rules.

These sources can be authoritative **project data** without becoming higher-priority model instructions.

That distinction is required.

## 3.5 Supporting repository data

Ordinary documentation, planning prose, issue text, research, comments, or other content that may provide evidence/context but is not automatically a governing instruction or canonical authority.

The existing PROGRAMSTART Data Grounding Rule still applies: user-authored planning/document content does not become an instruction merely because it contains imperative wording.

## 3.6 Material local constraint

A resolved instruction or repository-policy constraint that changes the candidate’s:

- allowed scope;
- mutation surface;
- sequencing;
- tool/command/publication path;
- authority resolution;
- safety boundary;
- dependency handling;
- validation;
- evidence requirement;
- acceptance condition;
- terminal condition;
- post-implementation review requirement.

Do not copy non-material instruction prose into the candidate.

## 3.7 Material corrective delta

A Challenge finding is material when incorporating it changes one or more of:

- owner/authority resolution;
- objective or protected outcome;
- scope or exclusions;
- consequential surface;
- applicable instruction/policy basis;
- architecture/contract assumption;
- sequencing/dependency order;
- capability realization;
- execution mechanism;
- blocker scope;
- mutation ownership;
- stronger approval/consequence gate;
- currentness/evidence requirement;
- verification;
- acceptance/terminal condition;
- post-implementation Challenge trigger.

Editorial restatement or observations that do not change behavior are not material corrective deltas.

## 3.8 Converged / clear for scope

The normative result of this design is **readiness convergence CLEAR for declared scope**.

It means:

> The exact current candidate, under the declared current authority, governing instruction/policy basis, evidence/currentness basis, and scope, has received the applicable current PROGRAMSTART Challenge and that Challenge produced no new material corrective delta or blocking unresolved finding for the next independently authorized boundary.

This is intentionally **not** a new lifecycle state.

The word **settled** may be used conversationally as shorthand for this condition, but this design must not introduce a canonical `settled` execution state because PROGRAMSTART already uses owner settlement in Decision Closure and those semantics must remain distinct.

---

# 4. Non-goals and invariants

Execution Readiness Convergence must preserve the following.

## 4.1 No new authority

A clear convergence result:

- does not accept a decision on behalf of its owner;
- does not create owner-native authority;
- does not authorize repository mutation/merge;
- does not satisfy a stronger security/credential/financial/privacy/legal/release/production gate;
- does not grant sudo/root/provider permission;
- does not make Matrix authoritative;
- does not replace current runtime/provider truth.

## 4.2 No second Challenge Gate

This design does not own a new A–H-like checklist.

It composes the current `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md`.

Gate-part selection remains owned there.

For a Mode-C pre-implementation candidate, A/C/F and B/E/H may commonly be relevant, but this design must not freeze a new universal subset. The existing stage/risk rules decide.

## 4.3 No duplicated instruction corpus

Do not copy whole `AGENTS.md`, Copilot instructions, contribution docs, or repository policy into a Work Packet.

Reference the governing source and retain only the material constraints required by the slice.

## 4.4 No universal instruction format

PROGRAMSTART must not require every repository to adopt `AGENTS.md`, `.github/instructions`, or another single format merely to use this design.

Use the executor/repository-native mechanism already in force.

## 4.5 No new strategic plan

The execution candidate remains derived from the project’s existing execution spine.

Mode C remains Mode C.

A readiness review must not restart Stage 0 or become a new Master.

## 4.6 No self-attested universal completeness

A clear convergence result is scoped.

It does not mean “everything is correct.”

It means no new material corrective delta survived the applicable Challenge for the declared candidate/basis.

## 4.7 No ceremonial repetition

One fresh Challenge may be sufficient for a simple current candidate.

A second pass is required when the first pass materially changes the candidate.

Repeated identical clear passes add no evidence unless an existing stronger review requirement independently applies.

---

# 5. Activation and proportionality

## 5.1 When the behavior applies

Use Execution Readiness Convergence before a meaningful consequential mutation or before handing off an implementation-ready candidate that another executor will rely on.

Typical triggers include:

- code/config implementation;
- repair of a consequential behavior;
- schema/migration work;
- runtime/provider/deployment preparation or mutation;
- security/auth/trust changes;
- material automation/integration changes;
- a non-trivial repository slice where local instructions/policy can materially affect execution;
- a plan that will be persisted, handed off, or resumed later.

## 5.2 Lightweight cases

For a trivial, low-risk, single-surface change:

- the executor may already have the governing instruction channel loaded automatically;
- one current authority check;
- one narrow candidate;
- one applicable Challenge;
- one-line evidence of the material instruction constraint

may be enough.

Do not create a persisted packet or multi-pass ceremony when there is no material delta.

## 5.3 Durable/replayable cases

When the convergence result will:

- survive the current invocation;
- be used by another agent/person;
- justify later resumption;
- gate a consequential mutation;
- support a PR/merge/release decision;
- cross repositories/systems;

the convergence evidence must be durable enough to identify the exact candidate and material basis that were challenged.

---

# 6. Instruction and repository-policy resolution

## 6.1 Resolution order

For each intended consequential surface:

1. identify the repository/system and current semantic owner;
2. identify the instruction channels that the **current executor** recognizes for that surface;
3. resolve their applicability/precedence using the executor’s native rules;
4. identify the repository policy/canonical authority that materially constrains the slice;
5. keep ordinary repository/planning prose classified as data/evidence unless its repository role establishes otherwise;
6. extract only material local constraints;
7. bind those constraints to the execution candidate;
8. record the conditions that require re-resolution.

PROGRAMSTART must not elevate arbitrary imperative-looking text into an instruction.

## 6.2 Minimum useful representation

The semantic record may be compact:

```text
EXECUTION_GOVERNANCE_BASIS:
  consequential_surface:
    - <repo/path/resource>
  governing_instruction_refs:
    - <executor-recognized instruction source/ref>
  repository_policy_authority_refs:
    - <canonical policy/authority ref>
  material_constraints:
    - <constraint that changes this slice>
  unresolved_conflicts:
    - <none | exact conflict>
  invalidation_triggers:
    - <condition>
```

Not every low-risk slice needs this exact formatting. The semantics matter more than the form.

## 6.3 If instructions are automatically supplied

Do not reread or re-copy them solely for ceremony.

The executor may record that the current execution environment supplied the governing instruction scope and then capture only the material constraints relevant to the candidate.

## 6.4 Conflicts

If governing instruction channels conflict, use the executor/platform-defined precedence.

If established repository authorities conflict, use the repository’s canonical conflict rules.

If a material conflict remains unresolved:

- fail closed for the dependent consequential mutation;
- keep independently safe unrelated work available;
- route the conflict to the correct owner;
- do not pick the most convenient rule.

## 6.5 Cross-repository instruction isolation

Resolve governing execution instructions and repository policy **per repository**.

Do not invent one merged cross-repository instruction hierarchy.

Cross-repository dependency/authority semantics remain governed by existing PROGRAMSTART rules.

---

# 7. Exact candidate and basis binding

A convergence claim must make it unambiguous what was challenged.

## 7.1 Candidate basis

The current candidate should be associated with:

```text
CANDIDATE_BASIS:
  candidate_ref:
  declared_scope:
  owner_authority_refs:
  governing_instruction_refs:
  repository_policy_authority_refs:
  evidence_currentness_refs:
  capability_discovery_ref: <when triggered>
  stronger_gate_overlay:
  invalidation_triggers:
```

## 7.2 Candidate reference strength

For same-invocation low-risk work, an unambiguous current task/packet representation can be sufficient.

For durable, handed-off, resumed, or consequentially reused convergence evidence, prefer immutable or reconstructable references such as:

- exact commit/PR head SHA;
- immutable issue/comment/evidence reference;
- file blob SHA;
- canonical hash of a durable candidate record;
- other owner-native immutable evidence.

Do not invent a global candidate-ID service merely to support this rule.

## 7.3 Changed candidate means changed basis

If a material corrective delta changes the candidate, the previous Challenge clear cannot be carried forward as the clear result for the new candidate.

The revised candidate must be challenged.

---

# 8. Convergence algorithm

## 8.1 Entry

Before starting the convergence loop, establish enough current context to form a bounded candidate:

- objective/protected outcome;
- current owner/project authority;
- consequential surface;
- governing instructions/repository policy;
- current evidence and invalidation conditions;
- material dependencies;
- existing capability discovery only where required;
- stronger gates;
- targeted verification and terminal condition.

## 8.2 Challenge

Run the **current existing PROGRAMSTART Challenge Gate** at the appropriate planning/convergence boundary.

Do not substitute a home-grown mini-gate.

The Challenge should use the parts and evidence required by the current stage/risk/change.

For this design’s purpose, the reviewer must be able to detect at least:

- authority mismatch;
- scope drift;
- stale/invalid evidence;
- duplicate planning authority;
- unresolved instruction/policy applicability;
- dependency/currentness mismatch;
- inappropriate new capability or human escalation;
- insufficient verification/terminal proof;
- implementation/architecture/requirements contradiction;
- stronger-gate leakage.

Those concerns are lenses, not a new canonical checklist.

## 8.3 Classify findings

Each finding should be one of:

- `MATERIAL_CORRECTIVE_DELTA`
- `NON_MATERIAL_OBSERVATION`
- `OUT_OF_SCOPE_FOLLOWUP`
- `BLOCKING_UNRESOLVED`

An out-of-scope follow-up must not silently expand the candidate.

Preserve it through the correct owner/idea/finding mechanism if it is worth retaining.

## 8.4 Revise

Incorporate every material corrective delta into the candidate.

Update the candidate basis when the delta changes:

- scope;
- owner/authority;
- instructions/policy;
- evidence/currentness;
- capability realization;
- stronger gates;
- verification/terminal condition.

## 8.5 Re-Challenge

If the candidate changed materially, run a new Challenge against the revised exact candidate.

A Challenge against the superseded candidate cannot clear the revised candidate.

## 8.6 Clear condition

Readiness convergence is CLEAR when the latest fresh Challenge against the latest candidate yields:

- no new material corrective delta;
- no blocking unresolved finding that controls the next boundary;
- current instruction/policy resolution;
- current owner authority;
- still-valid evidence/currentness basis;
- no unsatisfied stronger gate being misrepresented as satisfied.

## 8.7 Stop condition

Stop on the first clear pass unless another existing independent/review/convergence requirement applies.

Do not seek an arbitrary number of identical clear passes.

---

# 9. Re-entry and invalidation

A clear result is valid only while its material basis remains valid.

## 9.1 Scope invalidation

Re-enter when execution introduces:

- a new repository;
- a new path governed by different instructions/policy;
- a new schema/contract/trust boundary;
- a new runtime/provider/deployment consequence;
- materially wider blast radius.

## 9.2 Authority invalidation

Re-enter when:

- owner-native decision changes;
- strategic execution spine changes materially;
- architecture/requirements/decision authority changes;
- accepted-recommendation disposition changes;
- stronger-gate authority changes.

## 9.3 Instruction/policy invalidation

Re-enter when:

- an applicable governing instruction changes;
- a newly discovered more-specific instruction applies;
- repository policy/canonical authority changes;
- prior precedence/conflict resolution becomes uncertain.

## 9.4 Evidence/currentness invalidation

Re-enter when:

- code/config/schema/environment changed on the relied-upon surface;
- a dependency/provider/runtime changed materially;
- prior evidence is contradicted;
- a currentness fence reports mismatch;
- an exact candidate/head changed.

## 9.5 Plan invalidation

Re-enter when:

- implementation approach changes materially;
- a new prerequisite appears;
- selected capability realization changes;
- acceptance/terminal proof changes.

Elapsed time or a new chat/session alone is not invalidation unless the underlying fact is genuinely time-sensitive.

---

# 10. Capability Discovery Gate composition

Execution Readiness Convergence must not create a generic “search for tools” ritual.

Instead, defer to the existing `docs/CAPABILITY_DISCOVERY_GATE.md` when its current trigger applies.

That includes consequential conclusions such as:

- capability is unavailable;
- a human is required;
- a new execution path/capability must be built;
- an existing capability should be replaced;
- a realization/composition is being selected for consequence.

When triggered:

1. express actor + effect + target;
2. use the existing Paths composition classifier;
3. retain the required durable receipt;
4. verify the selected realization against current owner-native authority/currentness before consequence;
5. bind the resulting capability evidence into the candidate basis;
6. honor its invalidation conditions.

Paths discovery remains read/discovery authority, not semantic execution permission.

If the candidate does not make a consequential capability conclusion, do not run Paths discovery merely because this design exists.

---

# 11. Authority, currentness, and stronger gates

## 11.1 Authority before consequence

A clear readiness result cannot substitute for current owner-native authority.

If a materially new accepted decision is not yet current owner truth, use the existing Decision Closure / owner-reconciliation semantics before dependent consequence.

## 11.2 Validated implementation reality

Preserve current PROGRAMBUILD temporal semantics:

- retroactively discovered validated behavior/tests may prove planning authority stale;
- prospectively, do not intentionally implement behavior that contradicts current authority without reconciling that authority first.

Execution Readiness Convergence must not use “code is truth” as permission to bypass prospective authority.

## 11.3 Stronger gates are overlays

Security, credential, provider-console, destructive, financial, privacy/legal, production, release, or explicit operator gates remain independent overlays.

A readiness convergence result may say:

```text
READINESS: clear
NEXT_CONSEQUENTIAL_BOUNDARY: blocked_by_operator_gate
```

That is truthful.

It must not convert a generic clear result into stronger approval.

---

# 12. Cross-repository behavior

For a candidate spanning repositories:

1. preserve one execution spine/authority per repository;
2. resolve governing instructions/policy separately per repository;
3. classify the exact dependency relationship;
4. retain current dependency evidence and invalidation conditions;
5. preserve shared-mutation ownership when sibling lanes can affect the same consequential external/runtime/provider/device/deployment resource;
6. Challenge the candidate as a composed dependency view without creating a cross-repository Master;
7. do not treat one repository’s clear result as acceptance in another repository.

A cross-repository candidate may converge as a derived plan while individual mutations remain separately gated by each owner.

---

# 13. Relationship to current PROGRAMSTART mechanisms

## 13.1 Idea Intake

Idea Intake challenges a raw idea or Mode-C delta before execution planning.

Execution Readiness Convergence applies once there is a concrete bounded execution candidate.

Do not repeat already-settled intake questions without an invalidation reason.

## 13.2 Adaptive decision router

Reuse its current decision/evidence result.

This design does not create a second research router.

## 13.3 Work Packet

The Work Packet is the natural derived carrier for current-slice governance basis and convergence evidence.

Possible future conditional fields:

```text
EXECUTION_GOVERNANCE_BASIS:
CANDIDATE_REF:
READINESS_CONVERGENCE:
  challenge_ref:
  result: [clear | warning | blocked]
  material_deltas: [none | ...]
  invalidation_triggers:
```

Do not add these as mandatory empty fields for trivial tasks.

## 13.4 Challenge Gate

The Challenge Gate remains the canonical owner of gate-part selection and adversarial convergence behavior.

The key candidate delta this design proposes for eventual adoption is:

> When a Challenge materially changes the candidate, the changed candidate must be re-Challenged before the boundary is treated as clear.

## 13.5 JIT source-of-truth protocol

The JIT protocol is the natural owner for resolving the smallest current governance basis.

A future canonical change should distinguish:

- executor-native governing instructions;
- project canonical authority/policy;
- ordinary repository/planning data.

## 13.6 Product JIT Check

The existing Product JIT Check is the preferred operator-facing entry point.

Extend it before creating a new general-purpose prompt.

## 13.7 Decision Closure

Decision Closure continues to own semantic decision settlement when triggered.

For a materially new accepted decision being operationalized:

```text
conversation/evidence
  -> Decision Closure
  -> owner-native acceptance/currentness
  -> re-read owner truth
  -> protected outcome / obligations
  -> completeness Challenge
  -> Matrix projection when operationalized
  -> bounded Work Packet
  -> Execution Readiness Convergence
  -> independently authorized execution
```

This design does not redefine owner settlement.

## 13.8 Matrix

Matrix remains derived coordination/read projection.

It may help expose current obligations/dependencies but cannot mint execution authority or local repository instruction applicability.

## 13.9 Post-implementation adversarial Challenge

Pre-implementation readiness convergence does not prove the code/config/runtime implementation is correct.

The existing risk-triggered post-implementation Challenge still applies to the actual changed surface.

---

# 14. Durable proof and replay

PROGRAMSTART’s proof-durability invariant applies whenever a readiness result must survive beyond ephemeral reasoning.

## 14.1 Durable convergence evidence should identify

- exact candidate reference;
- declared scope;
- current owner/authority references;
- governing instruction references;
- repository policy/authority references;
- material constraints that affected the candidate;
- evidence/currentness references;
- capability-discovery receipt when triggered;
- Challenge result/evidence;
- material corrective deltas that changed the candidate;
- final clear/blocked result;
- stronger gates still active;
- invalidation conditions.

## 14.2 Do not preserve a diary

Durability does not require retaining every conversational iteration.

Preserve:

- the final candidate;
- the material design/execution decisions that changed it;
- the evidence required to reconstruct why it was clear or blocked.

Discard repetitive non-material Challenge prose.

## 14.3 Replay rule

A later executor may reuse the convergence result only after checking that none of its declared invalidation conditions fired.

If the exact candidate or material basis changed, refresh the affected portion and re-Challenge as required.

---

# 15. Reference execution-readiness shape

This is a derived reference, not a new canonical required artifact.

```text
EXECUTION READINESS

OBJECTIVE / PROTECTED OUTCOME:
CURRENT OWNER / AUTHORITY:
DECLARED CONSEQUENTIAL SURFACE:

EXECUTION GOVERNANCE BASIS
- governing instruction refs:
- repository policy/authority refs:
- material local constraints:
- unresolved conflicts:
- governance invalidation triggers:

CURRENT EVIDENCE / CURRENTNESS:
CAPABILITY DISCOVERY: [not-triggered | durable receipt ref]
DEPENDENCIES:
STRONGER GATE OVERLAY:
IN SCOPE:
OUT OF SCOPE:

CANDIDATE
- candidate ref:
- implementation approach:
- targeted verification:
- terminal condition:
- invalidation triggers:

PROGRAMSTART CHALLENGE
- challenge ref / parts selected by current gate:
- result:
- material corrective deltas:
- blocking unresolved findings:

IF MATERIAL DELTAS:
- revise candidate
- refresh candidate basis
- re-Challenge revised candidate

READINESS CONVERGENCE
- result: [clear | warning | blocked]
- exact candidate ref:
- declared scope:
- evidence basis:
- stronger gates still active:
- next independently authorized boundary:

POST-IMPLEMENTATION
- inspect actual changed surface for existing adversarial closure trigger
```

---

# 16. Failure semantics

## 16.1 Governing instruction source unavailable

If a known governing instruction source required for the intended surface cannot be read/resolved:

- do not guess;
- block dependent mutation;
- preserve independently safe work.

## 16.2 Arbitrary document looks like an instruction

Treat it as repository data unless the current executor or repository authority establishes its role.

Do not elevate imperative wording into instruction precedence.

## 16.3 Material instruction conflict

Use native precedence where defined.

If unresolved, block only the dependent consequence.

## 16.4 Challenge changes the candidate

Candidate is not clear.

Revise and re-Challenge.

## 16.5 Repeated identical Challenge result

Stop.

Do not perform another pass solely to accumulate “clear” results.

## 16.6 Owner authority changes

Invalidate the affected readiness basis, re-read current owner truth, refresh the candidate, and re-Challenge.

## 16.7 Capability conclusion without Paths evidence

If `CAPABILITY_DISCOVERY_GATE.md` is triggered, do not accept the capability-absence/human/new-path/replacement conclusion until its existing discovery contract is satisfied.

## 16.8 Matrix is stale

Owner truth remains authoritative.

Rebuild/reconcile Matrix through current doctrine; do not roll back owner truth.

## 16.9 Implementation expands scope

Do not mutate the newly expanded consequential surface until the affected governance basis and readiness convergence are refreshed.

## 16.10 Pre-implementation clear but post-implementation risk appears

Run the existing post-implementation adversarial Challenge.

Pre-implementation clear is not a waiver.

---

# 17. Examples

## 17.1 Nested AGENTS-style instruction hierarchy

A tool natively supports repository/nested `AGENTS.md`.

The intended file is under a nested directory.

The executor resolves the applicable native instruction chain according to that tool’s rules, records only the material constraints, and derives the candidate from current project authority.

Challenge finds that the proposed retry change touches persistence semantics and lacks a recovery proof.

That changes verification materially.

The candidate is revised and re-Challenged.

The revised candidate clears.

Result: clear for that exact scope/candidate, not globally.

## 17.2 PROGRAMSTART itself

PROGRAMSTART currently has repository-wide Copilot guidance and path-scoped `.github/instructions`.

An executor editing `PROGRAMBUILD/*.md` must not invent an `AGENTS.md` requirement.

It resolves the instruction channels its current environment recognizes plus PROGRAMBUILD canonical policy/authority.

Ordinary planning prose remains data.

## 17.3 Scope expansion

A frontend candidate clears.

During implementation, it becomes necessary to mutate auth middleware governed by a different instruction/policy surface.

The frontend clear result cannot authorize the middleware mutation.

Resolve the middleware governance basis, update the candidate, and re-Challenge.

## 17.4 Capability escalation

A candidate claims the current automation path cannot perform the effect and proposes a human workaround.

That conclusion triggers the existing Capability Discovery Gate.

Paths finds a current machine composition.

Human escalation is rejected and the candidate changes materially.

Re-Challenge the revised machine-path candidate.

## 17.5 One-pass low-risk clear

A tiny documentation correction has:

- current scope authority;
- no materially different nested instruction;
- no behavior/runtime effect;
- trivial verification.

The first applicable Challenge yields no material corrective delta.

Stop after one pass.

No ceremonial second pass is required.

---

# 18. Candidate acceptance fixtures for future adoption

A future canonical implementation should prove at least:

1. **Executor-native instruction resolution**
   - recognized instruction channels are applied without PROGRAMSTART inventing precedence.

2. **Planning-data grounding**
   - arbitrary imperative text in planning docs cannot become governing instruction authority.

3. **Root + nested applicability**
   - a more-specific applicable instruction surface changes the candidate when required.

4. **No duplicated instruction corpus**
   - derived evidence stores references/material constraints, not full copied instruction files.

5. **Scope expansion invalidates affected clear**
   - new consequential surface forces affected governance refresh before mutation.

6. **Exact candidate binding**
   - a clear result cannot be reused for a materially different candidate/head.

7. **Material Challenge delta requires re-Challenge**
   - the Challenge that changes the plan cannot simultaneously be the final clear for that revised plan.

8. **One-pass convergence**
   - a simple candidate can clear in one pass.

9. **No ceremonial repeat**
   - non-material restatement does not force another pass.

10. **Owner/currentness invalidation**
    - relevant authority/currentness change reopens only the affected basis.

11. **Capability-gate composition**
    - human/new-capability/unavailable-path conclusion routes through existing Paths discovery instead of a new mechanism.

12. **Stronger-gate preservation**
    - readiness clear cannot satisfy a separate explicit consequence/approval gate.

13. **Cross-repository isolation**
    - each repository keeps its own authority/instructions; no global instruction hierarchy is created.

14. **Post-implementation independence**
    - pre-implementation clear does not suppress a risk-triggered completed-change Challenge.

15. **Mode-C preservation**
    - readiness convergence produces a bounded delta under the existing spine rather than a replacement master plan.

---

# 19. Falsifiers

The design should be rejected, narrowed, or simplified if real implementation evidence shows that it:

- duplicates existing JIT/Work Packet/Challenge behavior without preventing a meaningful failure class;
- causes agents to read broad repository trees to discover instructions;
- promotes arbitrary documentation into model instruction authority;
- forces a universal instruction-file format;
- creates a second Challenge Gate or lifecycle;
- requires repetitive passes after no material delta remains;
- materially slows trivial work;
- copies instruction corpora into packets;
- creates a global candidate registry or instruction registry;
- confuses readiness convergence with Decision Closure owner settlement;
- allows a clear result to float forward after candidate/currentness change;
- bypasses the existing Paths Capability Discovery Gate;
- encourages self-certification of stronger execution authority.

---

# 20. Adoption map if implementation is later authorized

Do not promote this file wholesale into canonical authority.

Prefer owner-native deltas:

| Concern | Existing likely owner |
|---|---|
| instruction/policy/data classification + JIT resolution | `.github/instructions/source-of-truth.instructions.md` |
| proportional activation, invalidation/re-entry semantics | `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` |
| derived candidate/governance/convergence fields | `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` |
| materially changed candidate must be re-Challenged | `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` |
| operator-facing pre-implementation use | `.github/prompts/product-jit-check.prompt.md` |
| capability conclusion routing | existing `docs/CAPABILITY_DISCOVERY_GATE.md` — reference/reuse, do not duplicate |
| canonical/index/registry changes | only if a genuinely new critical canonical concern is created |

Current preferred implementation creates **no new canonical PROGRAMBUILD control file**.

---

# 21. Design decision log

This log records only design-changing conclusions from the convergence cycle. It is not a history of every draft.

## D-ERC-01 — Do not create a standalone canonical execution-readiness template

**Finding:** A new canonical template would duplicate JIT, Work Packet, and Challenge ownership.  
**Decision:** Keep this record non-authoritative and, if adopted, implement through small deltas to existing owners.

## D-ERC-02 — Do not make the design AGENTS.md-specific

**Finding:** Repositories/executors use different native instruction mechanisms.  
**Decision:** Resolve the governing instruction channels recognized by the current executor; `AGENTS.md` is one possible mechanism, not a universal requirement.

## D-ERC-03 — Separate executor instructions from repository authority/data

**Finding:** “Repository-native instruction” was broad enough to promote arbitrary docs into instruction authority.  
**Decision:** Distinguish executor-governing instructions, established repository policy/canonical authority, and supporting repository data. Preserve the Data Grounding Rule.

## D-ERC-04 — Reuse the existing Challenge Gate; do not invent a mini-gate

**Finding:** An embedded custom readiness checklist could become a second Challenge protocol.  
**Decision:** The convergence loop composes the current `PROGRAMBUILD_CHALLENGE_GATE.md`; stage/risk selection remains owned there.

## D-ERC-05 — Material-delta convergence, not repeat-count convergence

**Finding:** “Challenge until settled” can become infinite or ceremonial.  
**Decision:** Re-Challenge only when the candidate materially changes or its basis is invalidated. Stop on the first fresh clear pass.

## D-ERC-06 — Bind Challenge evidence to the exact candidate and basis

**Finding:** A previous clear could otherwise float forward after plan/head/authority/instruction changes.  
**Decision:** Convergence evidence must identify the exact/reconstructable candidate and material authority/instruction/evidence basis, with stronger immutable binding when reused across contexts.

## D-ERC-07 — Use “converged/clear for scope” normatively

**Finding:** PROGRAMSTART already uses owner settlement in Decision Closure.  
**Decision:** “Settled” remains conversational shorthand only; no new `settled` execution state is created.

## D-ERC-08 — Compose the existing Capability Discovery Gate

**Finding:** Generic “capability discovery” wording risked duplicating or weakening deterministic Paths discovery.  
**Decision:** When a consequential capability conclusion triggers `CAPABILITY_DISCOVERY_GATE.md`, use that gate and bind its durable receipt; otherwise do not run Paths ceremonially.

## D-ERC-09 — Preserve stronger consequence gates after readiness clear

**Finding:** Readiness quality and permission to execute are different boundaries.  
**Decision:** A candidate can be readiness-clear while still blocked on an independent security/operator/release/etc. gate.

## D-ERC-10 — Pre-implementation convergence never replaces completed-change adversarial review

**Finding:** A correct plan can still produce defective implementation.  
**Decision:** Continue to evaluate the actual changed surface against the existing post-implementation Challenge trigger.

---

# 22. Current design convergence result

**Declared design scope:** define a reusable, non-authoritative PROGRAMSTART design for binding local execution governance into bounded implementation planning and re-Challenging materially revised candidates before consequential execution.

**Current PROGRAMSTART basis reviewed:**

- PROGRAMBUILD canonical authority rules;
- PROGRAMBUILD planning operating model;
- PROGRAMBUILD Work Packet semantics;
- PROGRAMBUILD Challenge Gate;
- JIT source-of-truth protocol;
- Product JIT prompt;
- Decision Closure owner-settlement semantics;
- Capability Discovery Gate / Paths composition rule;
- proof-durability behavior and exact-candidate evidence patterns.

**Challenge cycle result:**

- initial design produced material corrections;
- revised candidates were re-Challenged;
- final relevant authority/scope/evidence/blast-radius/alignment/capability/duplicate-authority pass produced **no new material corrective delta**.

**Result:** **READINESS DESIGN CONVERGENCE — CLEAR FOR DECLARED DESIGN SCOPE.**

This is still non-authoritative reference material.

---

# 23. Recommended next step

If adoption is authorized, run a fresh Mode-C implementation plan against the then-current PROGRAMSTART head.

The implementation plan should:

1. re-read the current canonical owners in §20;
2. compare them to this non-authoritative design and produce only owner-native deltas;
3. define focused fixtures for §18;
4. use the existing Capability Discovery Gate only where implementation makes a consequential capability conclusion;
5. Challenge the exact implementation plan;
6. incorporate material corrective deltas and re-Challenge until the plan is clear for scope;
7. implement on a bounded branch/PR;
8. run repository-required validation/drift/CI;
9. Challenge the actual completed implementation when the current risk trigger requires it;
10. reconcile durable PROGRAMSTART authority only after the implementation earns acceptance.

**Design GO/NO-GO:** **GO to a bounded implementation-plan / canonical-delta proposal.**  
**NO-GO for treating this design record itself as canonical policy or execution authority.**
