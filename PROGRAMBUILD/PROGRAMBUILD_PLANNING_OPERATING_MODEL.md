# PROGRAMBUILD_PLANNING_OPERATING_MODEL.md

# Program Build Planning Operating Model

Purpose: Define how planning, research, execution authority, active work, context loading, and verification fit together without creating competing plans or unnecessary process overhead.
Owner: Project Lead / Operator
Last updated: 2026-08-24
Depends on: `PROGRAMBUILD_CANONICAL.md`, `PROGRAMBUILD_FILE_INDEX.md`, `PROGRAMBUILD_GAMEPLAN.md`, `DECISION_LOG.md`
Authority: Canonical for planning-to-execution separation, proportional rigor, progressive disclosure, and evidence-reuse rules.

---

## 1. Core Principle

PROGRAMBUILD is a reusable methodology. It is not the live execution authority for every project that uses it.

The operating model has four distinct layers:

1. **Reusable methodology** — PROGRAMBUILD explains how projects should be planned and executed.
2. **Project authority** — each real project owns its own current execution spine, decisions, requirements, architecture, and state.
3. **Active work packet** — the current coherent unit of work is derived from project authority and relevant evidence; it is not a second game plan.
4. **Evidence and reference material** — research, audits, prior verification, external guidance, and specialist documents support decisions but do not silently become execution authority.

The layers MUST remain distinct.

---

## 2. Authority Boundary

### PROGRAMSTART / PROGRAMBUILD owns

- reusable project-planning methodology
- reusable lifecycle and stage guidance
- proportional-rigor rules
- intake and challenge protocols
- work-packet structure
- context-loading rules
- evidence-reuse and re-verification rules
- reusable templates and agent guidance

### A project repository owns

- the project's actual strategic roadmap or master execution spine
- current implementation status
- project-specific requirements and architecture
- project-specific decisions and reversals
- current risks, blockers, acceptance criteria, and release state

### PROGRAMSTART / PROGRAMBUILD MUST NOT own

- a live global portfolio registry of the operator's actual projects
- filled project plans for unrelated repositories
- project-specific execution state that belongs in another repository
- duplicate copies of another project's master plan presented as authority

A registry **schema or template** MAY live here. A live portfolio registry SHOULD live in the operator's planning workspace or another dedicated portfolio system.

---

## 3. One Project, One Execution Spine

A project MUST have one primary execution spine for active strategic sequencing.

Examples include:

- an existing Master Game Plan
- a canonical roadmap
- a release/remediation ledger
- the default `PROGRAMBUILD_GAMEPLAN.md` sequence for a newly bootstrapped project

Research reports, audits, readiness reviews, implementation checklists, and work packets MUST NOT become competing strategic plans.

When new research suggests changes to an existing execution spine:

1. analyze the new evidence against the current authoritative plan;
2. identify deltas, omissions, risks, or sequencing improvements;
3. recommend specific edits to the authoritative plan;
4. do not silently replace or create a second master plan;
5. let the project's normal authority process decide whether those recommendations are adopted.

---

## 4. Entry Modes

Not every project begins as a blank-sheet idea. Select the correct entry mode before applying ceremony.

### Mode A — Raw Idea

Use when the project is genuinely new and little reliable planning exists.

- run the full `PROGRAMBUILD_IDEA_INTAKE.md` challenge
- establish feasibility and kill criteria
- create the normal PROGRAMBUILD project outputs
- choose the lightest suitable variant

### Mode B — Research-Backed Project

Use when substantial research already exists but the project has not yet been structured for execution.

- treat the research as evidence, not as an execution plan
- extract the problem, desired outcome, constraints, risks, unresolved questions, and candidate decisions
- use existing evidence to answer intake dimensions where possible
- investigate only genuine gaps or stale claims
- create or select the project's execution spine after the research has been converted into decisions and scope

### Mode C — Existing / In-Flight Project

Use when a repository, product, or program already has plans, code, decisions, and execution state.

Before proposing new structure:

1. locate the current canonical authority documents;
2. inspect the current repository or operational state;
3. identify what planning system is already in force;
4. preserve the existing execution spine unless the project's authority process explicitly replaces it;
5. convert new research or audits into delta recommendations rather than a new game plan;
6. reuse prior valid evidence rather than re-running checks without an invalidation reason.

For an existing project, PROGRAMBUILD is advisory methodology unless that project has explicitly adopted PROGRAMBUILD as its canonical process.

---

## 5. Proportional Rigor

The process MUST be proportional to risk, uncertainty, blast radius, reversibility, and project duration.

Use the lightest process that still protects the project.

### Low-rigor work

Typical characteristics:
- easily reversible
- low blast radius
- short-lived
- few dependencies
- little security/compliance impact

Expected behavior:
- small intake
- minimal documentation
- narrow verification
- one concise work packet when useful

### Standard-rigor work

Typical characteristics:
- production impact
- multiple components or dependencies
- meaningful user impact
- moderate uncertainty

Expected behavior:
- explicit strategic plan or PROGRAMBUILD stage sequence
- decision logging
- work packets for coherent execution slices
- targeted cross-stage verification

### High-rigor work

Typical characteristics:
- regulated or security-sensitive
- difficult to reverse
- large blast radius
- multi-team or long-running
- significant migration/data/availability risk

Expected behavior:
- formal authority map
- stronger retained evidence
- explicit approvals and acceptance gates
- higher verification depth
- ADRs where durable architecture/policy decisions warrant them

More documents do not automatically mean more rigor. Rigor is the quality of decisions, evidence, boundaries, and verification.

---

## 6. Strategic Plan Versus Active Work Packet

The strategic plan answers:

- where the project is going
- what remains
- major sequencing and dependencies
- what must be true to advance

The active work packet answers:

- what are we doing **now**
- which authoritative sources matter for this slice
- what is explicitly in and out of scope
- what evidence is already trusted
- what acceptance criteria prove this slice is complete
- what must be re-verified because this work could invalidate it

Use `PROGRAMBUILD_WORK_PACKET.md` to create the active packet.

A work packet MUST be derived from project authority. It MUST NOT redefine project strategy.

---

## 7. Progressive Context Loading

Do not load every project document for every task.

Use three context tiers.

### Tier 1 — Always-needed control context

Load only the small set needed to orient the task, typically:

- canonical authority map or repository instructions
- current strategic execution spine or current stage
- current active work packet, if one exists

### Tier 2 — Task-specific authoritative context

Load only the authoritative artifacts needed for the current slice, such as:

- relevant requirements
- relevant architecture/contracts
- relevant test strategy
- relevant decision records
- relevant deployment or operational state

### Tier 3 — Specialist / evidence context

Load only when triggered by the task:

- deep research
- security review
- legal/compliance guidance
- vendor documentation
- historical audits
- external comparisons
- prior incident evidence

Agents SHOULD prefer retrieval and just-in-time loading over repeatedly stuffing the complete documentation hierarchy into context.

---

## 8. Evidence Reuse And Re-Verification

Verified evidence SHOULD be reused until something material could have invalidated it.

Do not re-check a fact merely because a new work session started.

### Typical invalidation triggers

Re-verify when one or more of these occurred:

- relevant code changed
- relevant configuration changed
- a deployment changed
- data/schema/migration state changed
- a dependency or external API version changed
- an environment or secret changed
- the underlying source is time-sensitive and its freshness window expired
- new evidence directly contradicts the prior result
- the current work touches the surface that the prior verification covered

### Verification economy rule

Verification SHOULD be risk-based and change-based.

For each work packet:

1. identify what is already proven;
2. identify what this work can invalidate;
3. verify the affected surface;
4. avoid broad re-verification unless the change or risk justifies it.

A previous verified result is not permanent truth, but neither is it disposable merely because the context window changed.

---

## 9. Research Integration Rule

Deep research is a reference layer.

When research enters a project:

1. preserve the research as evidence;
2. separate factual findings from recommendations;
3. compare findings to current project authority and implementation state;
4. identify decision deltas;
5. identify recommended plan edits;
6. identify new invalidation triggers or verification needs;
7. update the authoritative project artifacts only through that project's normal decision process.

Do not rename a research report into a game plan simply to make it actionable.

---

## 10. Work Packet Lifecycle

A work packet represents one coherent execution slice.

Typical lifecycle:

1. **Derive** — generate from the strategic plan/current stage and only the relevant supporting context.
2. **Validate** — confirm scope, authority, known state, and acceptance criteria.
3. **Execute** — perform the work without widening scope silently.
4. **Verify** — run the targeted verification defined in the packet.
5. **Reconcile** — update decisions, project state, and the strategic execution spine where required.
6. **Close** — mark the packet complete or blocked; do not keep completed packets as competing plans.
7. **Generate next** — derive the next packet from the newly current project state.

For long-running work, a repository MAY keep a `CURRENT_WORK_PACKET.md` as a derived, replaceable artifact. It is never canonical over the strategic plan, requirements, architecture, or decision log.

---

## 11. Re-Entry After A Pause

When work resumes after a pause:

- locate the current execution authority
- inspect changes since the last trusted checkpoint
- reuse still-valid evidence
- run only the re-entry checks needed to detect drift
- regenerate the active work packet from current state
- do not reconstruct the entire project from chat memory

For PROGRAMBUILD-managed projects, also use the Re-Entry Protocol in `PROGRAMBUILD_CHALLENGE_GATE.md` where applicable.

---

## 12. Anti-Patterns

Avoid:

- multiple documents each claiming to be the master plan
- research reports promoted to execution authority without a decision
- giant prompts containing the entire repository documentation set
- re-running unchanged checks every session
- implementation checklists that quietly redefine strategy
- project-specific state stored in the reusable template repository
- forcing small projects through enterprise ceremony
- treating a large document count as evidence of planning quality
- continuing to use stale verification after a known invalidation trigger

---

## 13. Adoption In Existing Repositories

When applying this operating model to an existing repository:

1. identify the repository's current authority hierarchy;
2. name the existing execution spine;
3. identify supporting research/audit documents;
4. identify duplicate or competing planning artifacts;
5. define what should be loaded always versus just in time;
6. define evidence-reuse and invalidation rules;
7. introduce work packets as a derived execution aid if useful;
8. recommend edits to the existing master plan rather than replacing it;
9. record any material process change through the repository's decision mechanism.

The goal is less planning friction with stronger control, not more documentation.

---

## 14. Success Test

This operating model is working when an operator or agent can answer these quickly:

- What is authoritative?
- What are we doing now?
- Which documents actually matter for this slice?
- What has already been proven?
- What changed enough to require re-verification?
- What proves this slice is complete?
- Where will any durable decision be recorded?

If answering those questions requires loading the whole repository or interpreting several competing plans, the planning system needs simplification.
