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
- what is in and out of scope?
- which current authority/evidence matters?
- what evidence can be reused?
- what could invalidate that evidence?
- what proves completion?
- what durable project state must be reconciled afterward?

A work packet is **not**:

- a new master plan;
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
2. **Classify blockers** — if the closure-control row is blocked, identify the exact blocked action and classify the narrowest truthful scope before treating work as stopped.
3. **Scan safe lanes** — consider Lane A read-only/analysis, Lane B reversible repository/preparation work, and Lane C live/irreversible/external work under the project's own dependency and safety rules. A blocker label never automatically authorizes Lane C.
4. **Narrow** to one coherent objective with explicit non-goals.
5. **Reference** only the exact authority sections/evidence needed now.
6. **Reuse** trustworthy evidence whose invalidation conditions have not occurred.
7. **Execute** without silently widening scope.
8. **Verify** the changed/at-risk surface with the smallest sufficient check set.
9. **Reconcile** material decisions/scope/architecture/status into durable authority.
10. **Close** the packet and derive the next slice from the newly current state.

If the packet needs its own backlog, milestones, or independent sequencing, it is too large. Split it.

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

---

## 7. Existing-Project / Research Rule

For an existing repository:

- read its current instructions and strategic execution spine first;
- use the packet only as the current execution lens;
- keep research/audits as evidence;
- convert useful findings into explicit deltas to current authority;
- if the active closure row is blocked, classify blocker scope and scan safe lanes before concluding the project must wait;
- reconcile accepted changes back into canonical project artifacts;
- close/replace the packet after the slice.

A newer packet or research report never outranks established project authority merely because it is newer.

---

## 8. Completion Rule

A packet is complete when:

- the scoped outcome is done or explicitly stopped;
- acceptance criteria are resolved;
- required targeted verification is complete;
- material durable decisions/state are reconciled;
- remaining blockers are durably tracked with their narrowest truthful scope;
- the next executable safe slice, or the exact reason no safe slice exists, can be derived from current project state without relying on the old packet as authority.

**Success test:** the packet reduced execution ambiguity more than it increased documentation work.
