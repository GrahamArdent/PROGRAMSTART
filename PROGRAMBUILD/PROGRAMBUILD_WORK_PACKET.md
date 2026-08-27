# PROGRAMBUILD_WORK_PACKET.md

# Program Build Work Packet

Purpose: Define the smallest useful current-slice planning structure without creating a competing game plan or unnecessary documentation ceremony.
Owner: Project Lead / Operator
Last updated: 2026-08-27
Depends on: `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, the project's strategic execution spine, relevant requirements/architecture/decisions
Authority: Canonical for work-packet semantics. A filled packet is derived execution context and is never canonical over project authority.

---

## 1. Core Rule

A **work packet is a logical execution contract**, not necessarily a file.

It answers:

- what are we doing now?
- why is it authorized/next?
- what exact action is blocked, if any, and how narrowly is that blocker scoped?
- what safe execution lane remains available, if any?
- if another repository is a real dependency, which repository owns which meaning/mechanics and what is the current dependency state?
- what cross-repository evidence is reusable, what invalidates it, and what external/manual boundary remains?
- what is in and out of scope?
- which current authority/evidence matters?
- what evidence can be reused?
- what could invalidate that evidence?
- what proves completion?
- what durable project state must be reconciled afterward?

A work packet is **not**:

- a new master plan;
- a cross-project or portfolio master plan;
- a second requirements/architecture document;
- a running diary;
- a place to copy the whole repository;
- mandatory paperwork for trivial or single-step work.

---

## 2. Choose Compact Or Extended

### Compact packet — default

Use for ordinary coherent work that can be executed and reviewed without a durable packet file.

The compact packet may live in:

- the task/issue/PR description;
- the agent's current task state;
- a concise planning block in the active session.

Required fields:

```text
OBJECTIVE:
WHY_NOW / AUTHORITY:
BLOCKER_SCOPE: [none | row_only | merge_gate | mutation_gate | milestone | release | unresolved]
SAFE_EXECUTION_LANE: [A | B | C | none] + why it is actually allowed
CLOSURE_CONTROL:
RELATED_REPOSITORY_DEPENDENCY: [none | repository + relationship type + authority owner]
DEPENDENCY_STATE: [unknown | unsatisfied | partial | satisfied]
DEPENDENCY_EVIDENCE:
DEPENDENCY_INVALIDATION:
MANUAL_BOUNDARY:
IN_SCOPE:
OUT_OF_SCOPE:
REQUIRED_CONTEXT:
REUSABLE_EVIDENCE:
INVALIDATION_TRIGGERS:
ACCEPTANCE_CRITERIA:
TARGETED_VERIFICATION:
DURABLE_UPDATES_IF_NEEDED:
```

`SAFE_EXECUTION_LANE` is not an automatic permission. It must be supported by the project's own authority, dependency state, and safety rules.

Cross-repository fields may be `none` when the packet has no real companion dependency. Do not manufacture a relationship merely because two repositories are related historically or organizationally.

### Extended persisted packet — only when useful

Persist `CURRENT_WORK_PACKET.md` when one or more of these materially benefits execution:

- the slice spans sessions;
- multiple agents/people must share the same active context;
- dependencies or blockers make resumption non-obvious;
- the slice is high-risk or has meaningful blast radius;
- the evidence/invalidation model is non-trivial;
- the task is likely to pause and resume;
- the work is complex enough that a durable packet reduces, rather than adds, coordination cost.

Do **not** persist a file merely because the work is labelled "non-trivial."

A project MAY keep at most one active replaceable `CURRENT_WORK_PACKET.md` unless its own authority explicitly defines a different mechanism.

---

## 3. Compact Packet Lifecycle

1. **Derive** from the current strategic execution spine/stage and live project state.
2. **Resolve bounded cross-repository dependencies when relevant** — identify the companion repository, relationship type, authority owner, dependency state/evidence, invalidation conditions, and manual boundary. Keep each repository's execution spine separate.
3. **Classify blockers** — if the closure-control row is blocked, identify the exact blocked action and classify the narrowest truthful scope before treating work as stopped.
4. **Scan safe lanes** — consider Lane A read-only/analysis, Lane B reversible repository/preparation work, and Lane C live/irreversible/external work under the project's own dependency and safety rules. A blocker label never automatically authorizes Lane C.
5. **Narrow** to one coherent objective with explicit non-goals.
6. **Reference** only the exact authority sections/evidence needed now.
7. **Reuse** trustworthy evidence whose invalidation conditions have not occurred, including valid evidence from a companion repository.
8. **Execute** without silently widening scope or treating a dependency graph as multi-project mutation authority.
9. **Verify** the changed/at-risk surface with the smallest sufficient check set.
10. **Reconcile** material decisions/scope/architecture/status into the repository that actually owns each durable concern.
11. **Close** the packet and derive the next slice from the newly current state.

If the packet needs its own backlog, milestones, or independent sequencing, it is too large. Split it.

### 3.1 Cross-repository dependency rule

A cross-repository relationship is a **derived, task-scoped authority/dependency graph**. It is canonical for nothing.

For a bounded relationship, identify only what the current decision needs:

- **primary/implementation repository** — the repository whose current slice is being orchestrated;
- **related repository** — the repository that owns a product meaning, contract, runtime boundary, or other prerequisite relevant to the slice;
- **relationship type** — for example product contract, runtime contract, companion dependency, or another explicitly described relation;
- **authority owner** — the exact concern the related repository owns;
- **dependency state** — `unknown`, `unsatisfied`, `partial`, or `satisfied`;
- **dependency evidence** — the exact repository/runtime/test evidence supporting that state;
- **invalidation conditions** — what would make that evidence unsafe to reuse;
- **manual boundary** — credential, physical-device, provider, operator, or other external action still required;
- **closure control** — the project/slice that still controls closure after reusable companion evidence is considered.

`partial` is intentionally first-class. A dependency may be satisfied on one plane and still open on another, such as a hosted runtime contract already deployed while companion repository convergence or real provider acceptance remains incomplete.

A derived graph MAY support:

- read;
- orient;
- classify;
- plan;
- verify;
- reuse still-valid cross-repository evidence.

It MUST NOT by itself authorize PROGRAMSTART to:

- advance both projects;
- close both projects;
- merge companion PRs;
- edit multiple execution spines as one transaction;
- turn the relationship into a portfolio Master.

Independent work in the primary repository may proceed only when that repository's own authority proves the work does not assume an unsatisfied part of the dependency.

---

## 4. Extended `CURRENT_WORK_PACKET.md` Template

Use this only when persistence is justified.

```markdown
# CURRENT_WORK_PACKET.md

PACKET_ID:
STATUS: [ready | active | blocked | complete | superseded]
PROJECT:
CURRENT_STAGE_OR_MILESTONE:
AUTHORITY_SPINE:
AUTHORITY_VERSION_OR_COMMIT:
BLOCKER_SCOPE: [none | row_only | merge_gate | mutation_gate | milestone | release | unresolved]
SAFE_EXECUTION_LANE: [A | B | C | none]
BLOCKED_ACTION:
CLOSURE_CONTROL:

## Cross-Repository Dependency
RELATED_REPOSITORY: [none | repository]
RELATIONSHIP_TYPE: [product_contract | runtime_contract | companion | other]
RELATED_AUTHORITY_OWNER:
RELATED_EXECUTION_SPINE:
DEPENDENCY_STATE: [unknown | unsatisfied | partial | satisfied]
DEPENDENCY_EVIDENCE:
DEPENDENCY_INVALIDATION:
MANUAL_BOUNDARY:

## Objective
One concrete outcome.

## Why This Is Next
Trace to the execution spine, dependency order, blocker resolution, safe-lane preparation, or current stage.

## Scope
### In
- item

### Out
- item

## Required Context
- exact authority file/section/ID
- specialist evidence only when triggered

## Trusted Evidence + Invalidation
| Evidence | Why reusable | Invalidated by |
|---|---|---|
| | | |

When an external resource is involved, preserve **historical existence** separately from **current visibility/accessibility**. A resource that is currently missing or inaccessible is not automatically proven never to have existed or to have been deleted.

For cross-repository evidence, preserve the repository/runtime/test source and the exact invalidation condition. Do not collapse a partially satisfied dependency into a boolean green state.

## Assumptions / Unknowns
| Item | Confidence | Action |
|---|---|---|
| | high / medium / low | reuse / verify / spike / decide |

## Acceptance Criteria
- [ ] criterion

## Verification
| Changed / at-risk surface | Check | Result |
|---|---|---|
| | | pending |

## Stop / Escalation Conditions
- condition

## Durable Updates On Completion
- execution spine/status:
- decision log / ADR:
- requirements:
- architecture:
- tests / registry:
- release / operations:
- companion repository, only if that repository's own authority requires an update:

## Close-Out
OUTCOME:
VERIFICATION_SUMMARY:
EVIDENCE_INVALIDATED_OR_REUSED:
AUTHORITY_RECONCILED:
REMAINING_BLOCKERS:
NEXT_RECOMMENDED_SLICE:
```

---

## 5. Context-Minimization Rule

Reference authority instead of copying it.

Prefer:

```text
ARCHITECTURE.md §4.2
Requirement FR-017
Decision DEC-021
```

Do not paste pages of authoritative text into a packet unless the task genuinely needs that text inline.

For a companion repository, load only the authority/evidence needed to resolve the declared dependency. Do not load its entire planning hierarchy merely because a cross-repository edge exists.

The packet should make context **smaller**.

---

## 6. Evidence-Reuse Rule

For each verification concern, ask in this order:

1. Has this already been proven?
2. Is the evidence still in scope?
3. Did this slice trigger an invalidation condition?
4. What is the narrowest check that closes the remaining uncertainty?

Do not repeat broad verification by habit.
Do not reuse evidence after a relevant invalidation trigger.
Age/session change alone is not invalidation unless the underlying fact is genuinely time-sensitive.

For provider/runtime resources, keep these facts distinct:

- verified historical existence;
- current visibility/accessibility;
- current operational state;
- cause of any discrepancy, when actually known.

`not visible` or `inaccessible` MUST NOT silently rewrite verified historical existence to `never existed` or `deleted`.

For cross-repository dependencies, evidence remains reusable only while its declared assumptions and invalidation conditions still hold. Repository merge state, head changes, contract/runtime changes, provider state, credential state, or directly conflicting evidence may invalidate only the relevant portion rather than forcing a full re-audit of both repositories.

---

## 7. Existing-Project / Research Rule

For an existing repository:

- read its current instructions and strategic execution spine first;
- use the packet only as the current execution lens;
- keep research/audits as evidence;
- convert useful findings into explicit deltas to current authority;
- if another repository is a real prerequisite, inspect only enough of its authority/evidence to classify the dependency while preserving both execution spines;
- if the active closure row is blocked, classify blocker scope and scan safe lanes before concluding the project must wait;
- reconcile accepted changes back into the repository that owns the relevant canonical artifact;
- close/replace the packet after the slice.

A newer packet, research report, or cross-repository graph never outranks established project authority merely because it is newer.

---

## 8. Completion Rule

A packet is complete when:

- the scoped outcome is done or explicitly stopped;
- acceptance criteria are resolved;
- required targeted verification is complete;
- material durable decisions/state are reconciled;
- remaining blockers are durably tracked with their narrowest truthful scope;
- any cross-repository dependency state is supported by current evidence and does not overstate partial satisfaction;
- any remaining external/manual boundary is exact;
- the next executable safe slice, or the exact reason no safe slice exists, can be derived from current project state without relying on the old packet as authority.

**Success test:** the packet reduced execution ambiguity more than it increased documentation work.