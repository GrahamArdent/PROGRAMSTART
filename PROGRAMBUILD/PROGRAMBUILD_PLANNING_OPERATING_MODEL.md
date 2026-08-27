# PROGRAMBUILD_PLANNING_OPERATING_MODEL.md

# Program Build Planning Operating Model

Purpose: Define how planning, research, execution authority, active work, context loading, adaptive decision routing, blocker scope, safe-lane execution, and verification fit together without creating competing plans or unnecessary process overhead.
Owner: Project Lead / Operator
Last updated: 2026-08-27
Depends on: `PROGRAMBUILD_CANONICAL.md`, `PROGRAMBUILD_FILE_INDEX.md`, `PROGRAMBUILD_GAMEPLAN.md`, `DECISION_LOG.md`
Authority: Canonical for planning-to-execution separation, proportional rigor, progressive disclosure, adaptive decision routing, blocker/safe-lane handling, evidence sufficiency, and evidence-reuse rules.

---

## 1. Core Principle

PROGRAMBUILD is a reusable methodology. It is not the live execution authority for every project that uses it.

The operating model has four distinct layers:

1. **Reusable methodology** — PROGRAMBUILD explains how projects should be planned and executed.
2. **Project authority** — each real project owns its own current execution spine, decisions, requirements, architecture, and state.
3. **Active work packet** — the current coherent unit of work is derived from project authority and relevant evidence; it is not a second game plan.
4. **Evidence and reference material** — research, audits, prior verification, external guidance, and specialist documents support decisions but do not silently become execution authority.

The layers MUST remain distinct.

The governing rigor principle is:

> **Use exactly as much rigor as the decision warrants.**

Research exists to retire decision-relevant uncertainty, not to maximize knowledge.

---

## 2. Authority Boundary

### PROGRAMSTART / PROGRAMBUILD owns

- reusable project-planning methodology
- reusable lifecycle and stage guidance
- proportional-rigor rules
- adaptive decision-routing and evidence-sufficiency rules
- blocker-scope and safe-lane reasoning rules
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

Research reports, audits, readiness reviews, implementation checklists, adaptive-router outputs, and work packets MUST NOT become competing strategic plans.

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
6. reuse prior valid evidence rather than re-running checks without an invalidation reason;
7. route only the genuinely new decision/delta through additional scrutiny;
8. if the closure-control slice is blocked, classify the blocker scope and scan safe execution lanes before concluding no useful work remains;
9. return to the existing project's next executable slice after the delta is resolved.

For an existing project, PROGRAMBUILD is advisory methodology unless that project has explicitly adopted PROGRAMBUILD as its canonical process.

Mode C MUST NOT restart at Stage 0 merely because new analysis, research, or an adaptive-router result occurred.

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
- no research when current evidence is sufficient

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
- targeted research only for material unknowns

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
- deeper research only when high-impact uncertainty cannot be bounded cheaply

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

### 6.1 Blocker scope and safe execution lanes

A blocked closure row does not automatically mean the whole project must stop.

Before returning **blocked** in an existing/in-flight project:

1. identify the exact action that cannot proceed;
2. classify the narrowest truthful blocker scope: `ROW_ONLY`, `MERGE_GATE`, `MUTATION_GATE`, `MILESTONE`, or `RELEASE`; use `UNRESOLVED` only while evidence is insufficient to classify it;
3. distinguish closure sequencing from executable preparation sequencing;
4. scan the following candidate lanes under the project's own authority and dependency rules:
   - **Lane A — read-only / analysis:** inspection, diagnosis, targeted research, design, evidence reconciliation;
   - **Lane B — reversible repository / preparation:** branch-only code, tests, documentation, deployment preparation, migrations not yet applied;
   - **Lane C — live / irreversible / externally consequential:** production mutations, secrets, paid infrastructure, destructive changes, consequential external writes;
5. derive the next bounded packet from a safe lane when project authority proves it independent enough to proceed;
6. if no safe lane remains, state the exact blocker/manual action rather than a generic project-wide stop.

A blocker label is a constraint, not a permission. PROGRAMBUILD MUST NOT infer that Lane C is safe merely because the blocker was classified narrowly. Project-specific safety and dependency authority still governs consequential work.

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

- targeted or deep research
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

Age alone does not make stable evidence stale. Freshness matters when the underlying fact is volatile, a defined freshness window has expired, or a plausible invalidation signal exists.

### 8.1 External-resource evidence continuity

For provider/runtime resources, preserve these as separate facts:

- **historical existence** — whether trustworthy evidence proved the resource existed at a prior point;
- **current visibility/accessibility** — whether the current tool/account can see or access it now;
- **current operational state** — whether it is running/healthy/failed/deleted when that state is actually observable;
- **cause of discrepancy** — deletion, authorization scope, account/team mismatch, provider outage, or unknown.

Current `not visible`, `404`, or `inaccessible` evidence MUST NOT silently rewrite a verified historical resource to `never existed` or `deleted` unless the evidence actually proves deletion.

When the cause is unresolved, preserve the historical fact and state the current visibility/access problem plus the unresolved alternatives. This prevents volatile provider access from corrupting durable project history.

---

## 9. Adaptive Decision Router

Use the adaptive router when a meaningful decision has uncertainty, consequence, system-boundary complexity, proof obligations, or a Mode-C delta that could change how work should proceed.

Do **not** invoke it as mandatory ceremony for every trivial edit. Its purpose is to remove unnecessary work as often as it adds scrutiny.

The router asks:

> **Do we know enough to make the next important decision, and what is the smallest additional scrutiny that could change it?**

The repository-native helper is:

```bash
programstart decide --decision "<decision being protected>" ...
```

The router produces one of three execution routes:

- **execute** — current evidence is sufficient and no additional check is justified;
- **execute_with_checks** — no research is required, but one or more consequence/boundary/proof/simplicity/Mode-C checks matter;
- **investigate** — a bounded evidence gap must be retired before the protected decision should proceed.

The router is advisory methodology and a compact reasoning aid. Its output is not a new lifecycle, master plan, or authority document.

### 9.1 Composable check families

Candidate concerns are deliberately combined into a small set of check families rather than separate sequential gates:

1. **Evidence** — evidence sufficiency, reuse, freshness, conflict, and research depth.
2. **Consequence** — risk escalation, reversibility, destructive/irreversible effects, and meaningful cost/resource consequences.
3. **Boundary** — contract clarity, runtime reality, architecture extraction, and build-vs-buy questions.
4. **Proof** — verification and observability needed to prove success/failure.
5. **Simplicity** — complexity budget, unnecessary fragmentation, and avoidable operational/tool/resource burden.
6. **Mode-C delta** — preserve existing authority/evidence and inspect only what is genuinely new.

These families compose existing PROGRAMBUILD controls; they do not replace `PROGRAMBUILD_CHALLENGE_GATE.md` at required stage transitions/convergence points.

### 9.2 Evidence sufficiency and research depth

Research is not a boolean switch.

Use qualitative heuristics, not a weighted score that implies false precision:

- **No research** when current credible evidence is sufficient for the decision and no material unresolved uncertainty could change it.
- **Targeted research** when a bounded unknown, stale fact, provider behavior, contract detail, runtime constraint, build-vs-buy question, or evidence conflict can be retired with a focused check/delta.
- **Deep research** only when the decision is high-impact, uncertainty is high, evidence is absent/conflicting, and the decision surface is consequential enough that a focused check is unlikely to bound the risk safely.

Security/compliance importance by itself does **not** imply deep research. It increases consequence/proof rigor; research depth still depends on what is actually unknown.

Staleness by itself does **not** imply deep research. Refresh the time-sensitive evidence first.

Cheaply reversible low-impact decisions SHOULD be made faster. Do not demand broad research merely because more knowledge could be useful.

### 9.3 Blocking research discipline

Any research route that delays the protected decision MUST be able to state:

- **decision being protected**;
- **missing evidence**;
- **why/risk of proceeding without it**;
- **what outcome could change based on the answer**;
- **minimum evidence required to continue**;
- **stop condition**.

The stop condition is mandatory in spirit even when generated compactly:

> Stop when the minimum evidence is met and further research is unlikely to change the protected decision. Record residual uncertainty instead of researching for completeness.

### 9.4 Evidence reuse/freshness behavior

Classify decision-relevant evidence as:

- **sufficient** — reuse it;
- **partial** — reuse the valid portion and fill only the material gap;
- **stale** — refresh only the time-sensitive/invalidation-sensitive portion;
- **absent** — collect only evidence needed by the protected decision;
- **conflicting** — resolve the decision-relevant conflict before widening research.

Do not build a research knowledge-management platform merely to support this classification. Existing repository evidence, the dependency/evidence helpers, research ledger, and normal authority documents remain the sources.

### 9.5 Mode-C protection

For Mode C, the router MUST:

- start from current project authority/runtime state;
- reuse valid evidence;
- activate only checks relevant to the delta;
- never create a fresh Stage-0 lifecycle merely because investigation occurred;
- classify blocker scope and scan safe execution lanes before treating an active-row blocker as a whole-project stop;
- return to the existing project's actual next executable slice after the delta is resolved.

---

## 10. Research Integration Rule

Research is a subordinate evidence layer, whether targeted or deep.

When research enters a project:

1. name the decision it protects and the evidence gap before broadening the search;
2. preserve useful findings as evidence;
3. separate factual findings from recommendations;
4. compare findings to current project authority and implementation state;
5. identify decision deltas;
6. identify recommended plan edits;
7. identify new invalidation triggers or verification needs;
8. stop when the declared sufficiency condition is met;
9. update authoritative project artifacts only through that project's normal decision process.

Do not rename a research report into a game plan simply to make it actionable.

---

## 11. Work Packet Lifecycle

A work packet represents one coherent execution slice.

Typical lifecycle:

1. **Derive** — generate from the strategic plan/current stage and only the relevant supporting context.
2. **Classify blockers / safe lanes when relevant** — distinguish the blocked closure action from safe independent preparation before deciding execution must stop.
3. **Validate** — confirm scope, authority, known state, and acceptance criteria.
4. **Execute** — perform the work without widening scope silently.
5. **Verify** — run the targeted verification defined in the packet.
6. **Reconcile** — update decisions, project state, and the strategic execution spine where required.
7. **Close** — mark the packet complete or blocked; do not keep completed packets as competing plans.
8. **Generate next** — derive the next packet from the newly current project state.

For long-running work, a repository MAY keep a `CURRENT_WORK_PACKET.md` as a derived, replaceable artifact. It is never canonical over the strategic plan, requirements, architecture, or decision log.

---

## 12. Re-Entry After A Pause

When work resumes after a pause:

- locate the current execution authority
- inspect changes since the last trusted checkpoint
- reuse still-valid evidence
- route only genuinely uncertain/changed decisions through additional scrutiny
- classify any newly observed blocker at its narrowest truthful scope and scan safe lanes
- run only the re-entry checks needed to detect drift
- regenerate the active work packet from current state
- do not reconstruct the entire project from chat memory

For PROGRAMBUILD-managed projects, also use the Re-Entry Protocol in `PROGRAMBUILD_CHALLENGE_GATE.md` where applicable.

---

## 13. Anti-Patterns

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
- invoking every adaptive check defensively
- deep research without a protected decision and stop condition
- numeric rigor scores that imply unsupported precision
- treating security importance as automatic justification for deep research
- treating evidence age alone as proof of staleness
- treating a narrow row/merge/mutation blocker as an automatic whole-project stop
- treating current provider invisibility as proof that a historically verified resource never existed
- restarting Mode C from Stage 0 after a research or analysis delta

---

## 14. Adoption In Existing Repositories

When applying this operating model to an existing repository:

1. identify the repository's current authority hierarchy;
2. name the existing execution spine;
3. identify supporting research/audit documents;
4. identify duplicate or competing planning artifacts;
5. define what should be loaded always versus just in time;
6. define evidence-reuse and invalidation rules, including provider/resource continuity where relevant;
7. introduce work packets as a derived execution aid if useful;
8. use adaptive routing only for decisions whose delta actually earns it;
9. classify blockers narrowly and scan safe lanes before stopping useful independent work;
10. recommend edits to the existing master plan rather than replacing it;
11. record any material process change through the repository's decision mechanism.

The goal is less planning friction with stronger control, not more documentation.

---

## 15. Success Test

This operating model is working when an operator or agent can answer these quickly:

- What is authoritative?
- What are we doing now?
- Which documents actually matter for this slice?
- What has already been proven?
- If the closure row is blocked, what exact action is blocked and what safe lane remains?
- For external resources, what is verified historically versus currently visible/accessibile?
- Do we know enough to make the next important decision?
- If not, what exact evidence is missing and what could it change?
- Is targeted research enough, or is deep research genuinely justified?
- What is the stop condition?
- What changed enough to require re-verification?
- What proves this slice is complete?
- Where will any durable decision be recorded?

If answering those questions requires loading the whole repository, invoking every gate, or interpreting several competing plans, the planning system needs simplification.
