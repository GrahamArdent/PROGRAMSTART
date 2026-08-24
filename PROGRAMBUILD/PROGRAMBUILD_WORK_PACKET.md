# PROGRAMBUILD_WORK_PACKET.md

# Program Build Work Packet

Purpose: Define the standard structure for the current coherent unit of execution without creating a competing game plan.
Owner: Project Lead / Operator
Last updated: 2026-08-24
Depends on: `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, the project's canonical execution spine, relevant requirements/architecture/decisions
Authority: Canonical for active work-packet structure. A filled work packet is derived execution state and is never canonical over project authority.

---

## 1. What A Work Packet Is

A work packet is the smallest useful planning artifact that answers:

- what are we doing now?
- why is this the next coherent slice?
- what is in scope and out of scope?
- which authoritative sources matter?
- what evidence can be reused?
- what could this work invalidate?
- what acceptance criteria prove completion?
- what durable project artifacts must be updated afterward?

A work packet is **not**:

- a new master plan
- a replacement for the project's game plan or roadmap
- a second requirements document
- a running diary
- a place to restate the entire repository

For long-running work, a project MAY keep one replaceable derived file named `CURRENT_WORK_PACKET.md`.

---

## 2. Creation Rules

Create or refresh a work packet when:

- beginning a coherent implementation/remediation slice
- moving to the next phase of an existing plan
- resuming after a meaningful pause
- new research or evidence materially changes what should happen next
- a blocker forces replanning of the current slice

Do not create a packet for trivial work that can be safely completed immediately with obvious scope and verification.

Before creating the packet:

1. identify the project's canonical execution spine;
2. identify the current stage/status;
3. locate the relevant authoritative files;
4. identify trustworthy existing evidence;
5. determine what changed since that evidence was produced.

---

## 3. Work Packet Template

```markdown
# CURRENT_WORK_PACKET.md

## Packet Metadata

PACKET_ID:
STATUS: [ready | active | blocked | complete | superseded]
CREATED:
LAST_UPDATED:
OWNER:
PROJECT:
CURRENT_STAGE_OR_MILESTONE:
AUTHORITY_SPINE:
AUTHORITY_VERSION_OR_COMMIT:

## 1. Objective

State one concrete outcome for this packet.

## 2. Why This Is Next

Explain how this packet follows from the canonical execution spine, current state, dependency order, or blocker resolution.

## 3. In Scope

- item
- item

## 4. Explicitly Out Of Scope

- item
- item

## 5. Required Context

### Always-load authority
- file / source

### Task-specific authority
- file / source

### Just-in-time specialist context
- file / source and trigger for loading it

## 6. Trusted Existing Evidence

| Evidence | Verified when / against | Why still valid | Invalidation trigger |
|---|---|---|---|
| | | | |

## 7. Assumptions And Unknowns

| Item | Type | Confidence | Action |
|---|---|---|---|
| | assumption / unknown | high / medium / low | reuse / verify / spike / decide |

## 8. Planned Changes / Actions

1. action
2. action
3. action

## 9. Acceptance Criteria

- [ ] measurable completion criterion
- [ ] measurable completion criterion

## 10. Verification Map

| Change / Risk | Verification required | Existing evidence reusable? | Result |
|---|---|---|---|
| | | yes / no / partial | pending |

## 11. Stop / Escalation Conditions

Stop or escalate if:
- condition
- condition

## 12. Durable Updates Required On Completion

- execution spine / roadmap: [yes/no + required edit]
- decision log: [yes/no + decision]
- requirements: [yes/no + change]
- architecture: [yes/no + change]
- test strategy / registry: [yes/no + change]
- release / operational state: [yes/no + change]

## 13. Completion Reconciliation

OUTCOME:
VERIFICATION_SUMMARY:
DECISIONS_RECORDED:
AUTHORITY_UPDATED:
REMAINING_BLOCKERS:
NEXT_RECOMMENDED_SLICE:
```

---

## 4. Scope Rule

A packet SHOULD contain one coherent slice that can be reasoned about and verified as a unit.

Good packet examples:

- reconcile one migration boundary and prove the affected data path
- implement one feature family sharing the same contracts
- review one research result against an existing master plan and produce specific amendment recommendations
- remediate one deployment failure class and verify only the affected release surfaces

Bad packet examples:

- "finish the entire project"
- "fix everything in the repository"
- a packet containing several unrelated workstreams just because they are all open

If a packet grows large enough to need independent sequencing, split it.

---

## 5. Context-Minimization Rule

The packet SHOULD point to authoritative context rather than duplicate it.

Prefer:

```text
Relevant contract: ARCHITECTURE.md §4.2
Relevant requirement: FR-017
Relevant decision: DEC-021
```

Over copying several pages from those documents into the packet.

This keeps the active context small and reduces the chance that duplicated text becomes stale.

---

## 6. Evidence-Reuse Rule

For every verification step, ask in this order:

1. Has this already been proven?
2. Is that evidence still valid?
3. Did the current work touch something that can invalidate it?
4. What is the narrowest verification that closes the remaining uncertainty?

Do not re-run broad verification by habit.
Do not reuse evidence after a known invalidation trigger.

---

## 7. Research-To-Packet Rule

When the packet exists because new research was introduced:

- the research remains reference evidence
- the packet identifies which findings matter to the current project
- the packet compares those findings to current authority and implementation state
- the output should usually be specific decision deltas, risk updates, and proposed edits to the current execution spine
- the packet MUST NOT declare a new master plan unless the project authority explicitly decides to replace the old one

---

## 8. Existing-Project Rule

For an existing repository:

- read its repository instructions and canonical authority before acting
- preserve its established execution spine
- use the packet as a temporary execution lens
- record durable changes back into the project's canonical artifacts
- mark the packet complete or superseded after reconciliation

The packet should make the project easier to resume, but the project must remain understandable without treating old work packets as the source of truth.

---

## 9. Completion Rule

A packet is complete only when:

- the scoped work is finished or explicitly stopped;
- defined acceptance criteria are resolved;
- required targeted verification is complete;
- material decisions are recorded in the proper durable authority;
- the project execution spine/status is reconciled if the outcome changes it;
- blockers and next recommended slice are explicit.

After completion, generate the next packet from the newly current project state. Do not simply carry forward stale assumptions from the previous packet.
