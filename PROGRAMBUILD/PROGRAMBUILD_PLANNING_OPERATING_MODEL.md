# PROGRAMBUILD_PLANNING_OPERATING_MODEL.md

# Program Build Planning Operating Model

Purpose: Define how planning, idea preservation, research, execution authority, active work, context loading, adaptive decision routing, blocker scope, safe-lane execution, accepted recommendations, checklist completeness, convergence output/durable packet routing, and verification fit together without creating competing plans or unnecessary process overhead.
Owner: Project Lead / Operator
Last updated: 2026-10-05
Depends on: `PROGRAMBUILD_CANONICAL.md`, `PROGRAMBUILD_FILE_INDEX.md`, `PROGRAMBUILD_GAMEPLAN.md`, `DECISION_LOG.md`
Authority: Canonical for planning-to-execution separation, idea capture/promotion semantics, proportional rigor, progressive disclosure, adaptive decision routing, blocker/safe-lane handling, accepted-recommendation resolution, convergence output/durable packet routing, evidence sufficiency, and evidence-reuse rules.

---

### Start here for existing work

1. Find the project owner’s current record and terminal objective. Start with the repository’s declared work references or Issues. Use the [Paths owner lookup](https://github.com/GrahamArdent/paths/blob/main/CHATGPT.md#resuming-work-from-a-repository-name) when the entry is stale, ambiguous, or missing.
2. Check for an original attempt before choosing a new effect. For a pending or unknown result, reconcile with the owner’s native records using the original request ID and canonical input digest. Resume or read back that original. A successor requires a known disposition and applicable authority.
3. Identify the exact next admitted effect and choose a callable route for it. Use the normal repository route for authorized routine source work. For detached operation, use the admitted backend and its durable checkpoint. Protected work requires current owner admission for the effect, target, and conditions. If any prerequisite is unresolved, record the owner, required proof, and resume point, and continue safe work.
4. Verify through the consumer that owns acceptance. Use the repository’s normal review and verification for source work. For cross-system work, verify the receiving seam and obtain the applicable owner disposition before claiming closure. Record the result and next action in the existing owner record.

## 1. Core Principle

PROGRAMBUILD is a reusable methodology. It is not the live execution authority for every project that uses it.

The operating model has four distinct layers:

1. **Reusable methodology** — PROGRAMBUILD explains how projects should be planned and executed.
2. **Project authority** — each real project owns its own current execution spine, decisions, requirements, architecture, and state.
3. **Active work packet** — the current coherent unit of work is derived from project authority and relevant evidence; it is not a second game plan.
4. **Evidence and reference material** — research, audits, prior verification, external guidance, specialist documents, captured ideas, and derived checklists support decisions but do not silently become execution authority.

The layers MUST remain distinct.

The governing rigor principle is:

> **Use exactly as much rigor as the decision warrants.**

Research exists to retire decision-relevant uncertainty, not to maximize knowledge.

For idea preservation, use the equally important rule:

> **Capture broadly. Promote deliberately. Execute only from authority.**

---

## 2. Authority Boundary

Validated implementation establishes observed behavior; it does not grant execution permission. Apply `PROGRAMBUILD_CANONICAL.md` rule 1 when reconciling descriptive drift: unauthorized working behavior is a defect, and operator, owner, provider and platform restrictions remain controlling. Prospective authorized contradictions still require updating their owning authority before implementation.

### PROGRAMSTART / PROGRAMBUILD owns

- reusable project-planning methodology
- reusable lifecycle and stage guidance
- proportional-rigor rules
- idea-preservation and promotion semantics
- adaptive decision-routing and evidence-sufficiency rules
- blocker-scope and safe-lane reasoning rules
- accepted-recommendation resolution rules
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

A registry **schema or template** MAY live here. A live portfolio registry or cross-project idea collection SHOULD live in the operator's planning workspace or another dedicated portfolio system.

### 2.1 Idea Preservation Versus Promotion

A worthwhile idea does not need to be current work in order to deserve durable preservation.

PROGRAMBUILD distinguishes three separate acts:

1. **Capture** — preserve an idea because it is worth remembering.
2. **Promote** — deliberately evaluate/adopt the idea into the owning project's real scope, architecture, sequencing, milestone, decision, or acceptance authority.
3. **Execute** — perform work only after current authority permits it.

Capture is deliberately cheap. Do not require full Idea Intake, feasibility work, research, prioritization, or roadmap placement merely to remember something useful.

When capture cost is low, an operator/agent SHOULD preserve an idea when:

- the operator explicitly says it is interesting, useful, worth remembering, or should be saved;
- it could plausibly affect a current or future project;
- it is a meaningful alternative whose value may change with future evidence;
- rejected/shelved reasoning would be expensive to reconstruct later;
- research or implementation reveals a future opportunity outside current scope;
- losing the idea would likely require non-trivial reasoning to be repeated.

When uncertain whether a non-trivial idea will matter later, prefer capture over relying on chat/session memory.

Use an existing project/workspace idea, issue, note, or discovery surface when it already fits. Otherwise `IDEA_LEDGER.md` is the optional reusable preservation template. A portfolio-wide ledger belongs outside PROGRAMSTART in the operator's planning workspace or another dedicated portfolio system.

Use the following status vocabulary when a durable Idea Record is helpful:

- **`CAPTURED`** — worth remembering; no priority implied.
- **`CANDIDATE`** — worth deliberate future evaluation.
- **`INVESTIGATING`** — a bounded validation/research step is active.
- **`SHELVED`** — deliberately not current; preserve a revisit trigger when knowable.
- **`ACCEPTED`** — accepted for promotion; point to the owning authority after reconciliation.
- **`REJECTED`** — deliberately not adopted under current evidence; preserve rationale/reconsideration evidence.
- **`SUPERSEDED`** — replaced by another idea/decision; link the replacement when practical.

Status is descriptive, not priority or sequencing.

A minimal Idea Record may contain only:

```text
TITLE:
STATUS:
OWNER_OR_CONTEXT:
IDEA:
WHY_INTERESTING:
ORIGIN_OR_EVIDENCE:
RELATED:
PROMOTION_OR_REVISIT_TRIGGER:
DECISION_OR_RATIONALE:
PROMOTED_TO:
```

Fill only fields that improve retrieval, future evaluation, deduplication, or safe resumption.

A captured/shelved/rejected idea MUST NOT become project scope, backlog priority, sequencing, architecture, budget, or execution authority merely because it was recorded. When an idea is promoted, reconcile the existing artifact that owns the resulting durable truth and execute from that authority. The Idea Record remains provenance/reference evidence.

Rejected and superseded ideas SHOULD normally be preserved when their rationale could prevent repeated analysis later.

Do not load or review an entire idea collection on every project turn. Retrieve relevant records only when the current request, a stated revisit trigger, or related project evidence makes them decision-relevant.

---

## 3. One Project, One Execution Spine

A project MUST have one primary execution spine for active strategic sequencing.

Examples include:

- an existing Master Game Plan
- a canonical roadmap
- a release/remediation ledger
- the default `PROGRAMBUILD_GAMEPLAN.md` sequence for a newly bootstrapped project

Research reports, idea ledgers/records, audits, readiness reviews, implementation checklists, adaptive-router outputs, recommendation-resolution results, and work packets MUST NOT become competing strategic plans.

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
- no persisted checklist when omission risk is trivial and no applicable durable checklist exists

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
- active checklist use when omission risk or an existing applicable checklist materially helps closure

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
- explicit reconciliation of applicable checklist/gate obligations before closure; every applicable item must be dispositioned as `satisfied`, `not applicable`, `blocked`, or `deferred` with the reason/evidence required by the owning checklist

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
- relevant captured/shelved idea records
- security review
- legal/compliance guidance
- vendor documentation
- historical audits
- external comparisons
- prior incident evidence

Agents SHOULD prefer retrieval and just-in-time loading over repeatedly stuffing the complete documentation hierarchy into context.

---

### 7.1 Objective-level convergence

JIT context remains anchored to an authority-derived terminal condition. At a material transition, ask which part of that condition the next action advances or protects. Load context for current uncertainty, dependency, consequence or proof, and classify discoveries as blocking, required dependency, non-blocking relevant or unrelated. Continue authorized machine-safe dependencies through existing Work Packet lifecycle; locally green intermediate artifacts are not completion. Route useful non-blocking findings without abandoning the objective. Authority/evidence may legitimately revise the condition, and stronger gates still govern their exact consequence. Anti-drift does not authorize unrelated cleanup or a new continuation engine.

---

### Receiving-seam example — B and isolated #601

Use the receiving owner’s current contract to load only the fields needed at each handoff. Keep the historical B observation at `verifying`. The [#601 evidence](https://chatgpt.com/library?file_id=libfile_fde3_f-62fa20d3eae481919e806225ec37b8c0_b2a2be3545e48191a4e5216544ded2e4&account_id=personal) records a distinct isolated attempt with stubbed boundaries.

| Producer → consumer | Minimum evidence and receiving decision |
|---|---|
| Product authority → Controller | At admission, read current owner scope, approved objective and sealed Work Packet. Bind request ID, canonical input digest and root. Hold on an authority or digest mismatch. The admitted root and attempt identify the next authorized effect. |
| Controller → Compute | At dispatch, bind the effect and original attempt to the Compute parent and exact input. Compute validates the binding before forwarding. An unknown response requires lookup of that original, with no replacement dispatch. |
| Compute → Execution Node | Before worker execution, bind the child, worker revision and sealed fixture descriptor. A matching filename with different bytes fails the custody check. Wait for the bound worker result and preserve its evidence or the exact rejection. |
| Execution Node → Compute → Controller | Bind the original child result to its parent journal and verify the returned digest before recording the result on the original attempt. Pending stays pending. A reconciled worker result can move the run to verifying. In isolated #601, the normal tick recovered the original parent on the same attempt and a repeat tick submitted nothing. |
| Controller → business verifier → product owner | Grade the intended result against the Work Packet, then return the bound grade and original evidence to the owner for terminal disposition. The isolated 300-cent oracle supports the example’s business check. Owner settlement and cleanup for that attempt remain open. |

See §11 for settlement and release. Retrieve the exact original identities and proof limits from the owner evidence rather than copying them into new work packets.

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

Do not build a research knowledge-management platform merely to support this classification. Existing repository evidence, the dependency/evidence helpers, research ledger, idea records, and normal authority documents remain the sources.

### 9.5 Mode-C protection

For Mode C, the router MUST:

- start from current project authority/runtime state;
- reuse valid evidence;
- activate only checks relevant to the delta;
- never create a fresh Stage-0 lifecycle merely because investigation occurred;
- classify blocker scope and scan safe execution lanes before treating an active-row blocker as a whole-project stop;
- return to the existing project's actual next executable slice after the delta is resolved.

### 9.6 Accepted Recommendation / Generic “Proceed” Resolution

The adaptive router answers whether a recommendation is sufficiently supported. It does **not** by itself define what a later generic operator acceptance authorizes.

When an agent has made a concrete recommendation and the operator later responds with a generic acceptance such as `proceed`, `go ahead`, `proceed with your recommendation`, `do what you recommend`, or an equivalent phrase, resolve the acceptance against **current project authority and the recommendation's actual effect** before executing.

Do not ask the operator to restate methodology that can be derived from current authority.

Use exactly one primary disposition:

1. **`execute_current_authority`** — the accepted recommendation fits inside the current authorized slice/strategy and does not change durable project truth.
   - derive/continue the bounded work packet and execute it;
   - do not rewrite the Master/strategic spine merely because an implementation detail, local fix, file choice, test, or tactic changed;
   - reconcile normal status/evidence at closure.
2. **`reconcile_authority_then_execute`** — the accepted recommendation changes durable project truth, for example strategic scope/sequencing, architecture, durable dependency, milestone/definition-of-done, acceptance criteria, or a material prior decision.
   - record the accepted delta in the artifact that already owns that concern **before or atomically with dependent implementation**;
   - then derive the executable packet from the reconciled authority;
   - do not let code/runtime intentionally move ahead of knowingly stale authority.
3. **`defer_without_resequencing`** — the operator accepts the recommendation as useful direction, but current authority/dependency order says it is not the next executable work.
   - preserve the idea in an existing appropriate durable idea/future/decision/reference surface; when no compatible surface exists and the idea is worth remembering, use the optional `IDEA_LEDGER.md` pattern rather than relying on session memory;
   - mark it `CAPTURED`, `CANDIDATE`, or `SHELVED` according to the evidence; capture status does not imply priority;
   - do not create a hidden PROGRAMSTART backlog or a second Master;
   - do not reorder the active spine merely because the operator liked the idea;
   - return to the current project's actual next executable slice.

A stronger approval/manual/consequence requirement is an **independent gate overlay**, not a fourth recommendation disposition. Examples include security-sensitive or destructive mutations, credential/provider actions, explicit financial commitments, production/release actions, privacy/legal approvals, or other project-defined gates.

Rules for the gate overlay:

- generic acceptance MAY approve the recommendation's direction;
- generic acceptance MUST NOT silently satisfy a stronger gate whose authority requires a more specific action/approval/evidence boundary;
- preserve the gate owner, action, acceptance evidence, and resume point using the existing operator/manual-gate or project-specific mechanism;
- when no stronger gate exists, do not invent one merely because the operator used a generic phrase.

### 9.7 Authority-worthiness test

Before changing a Master, strategic spine, decision record, architecture, or another durable authority surface, ask:

> **Would leaving the current authority unchanged make it materially false, misleading, contradictory, or unsafe for the next dependent work?**

Usually authority-worthy:

- durable scope addition/removal;
- changed strategic sequencing or closure control;
- milestone advancement/definition change;
- architecture, trust, contract, or durable dependency change;
- changed acceptance criteria or definition of done;
- material decision reversal/supersession;
- newly durable blocker/constraint that changes what can proceed.

Usually normal execution detail:

- local implementation mechanics already within scope;
- filenames/module organization that do not alter architecture/contract authority;
- ordinary bug fixes already required by the current slice;
- small tests/fixtures;
- temporary investigation notes;
- reversible tactics that do not change durable project truth.

**Not authority-worthy does not mean not worth remembering.** If a thought/change/opportunity has future reuse value but does not belong in current authority, preserve it as an Idea Record or other appropriate non-authoritative evidence instead of forcing it into the Master or discarding it.

When evidence discovered during execution disproves the accepted recommendation's premise, **do not force the accepted recommendation through**. Stop at the smallest safe point, reconcile the new evidence/authority that actually changed, and derive the next slice from current truth. Operator acceptance authorizes a direction under stated/current assumptions; it does not make disproved assumptions true.

### 9.8 Checklist completeness discipline

Checklists are derived completeness aids, not strategy.

Activate a checklist when:

- omission risk is meaningful;
- the slice has several independent acceptance/risk/handoff obligations that are easy to forget;
- a stage/release/security/acceptance boundary already has an applicable durable checklist;
- multi-session or multi-person work benefits from an explicit completion inventory.

Do not create a large checklist artifact for trivial low-risk single-step work when no applicable durable checklist exists.

When active:

1. derive material items from current authority, acceptance criteria, risk/gate obligations, and declared handoffs;
2. cross-reference the owning source when practical;
3. do not let checklist items silently create new scope;
4. reuse an existing applicable durable checklist instead of creating a duplicate;
5. before closure, reconcile every applicable item as `satisfied`, `not_applicable` with reason, `blocked` with exact gate, or `deferred` only when current authority permits;
6. unresolved required items prevent truthful `complete`/`merge-ready` status;
7. keep the checklist in the smallest useful surface: session/work-packet/PR/task by default, persisted file only when persistence earns its cost.

`PROGRAMBUILD_CHECKLIST.md` provides the reusable checklist form. The Work Packet owns how checklist completeness participates in current-slice closure.

---


### 9.9 Convergence Output And Durable Packet Routing

When an operator deliberately asks for a material design, implementation plan, recommendation, handoff, or other result to be challenged until the current candidate is clear, preserve the useful result without turning the reporting artifact into a second authority.

Use this behavior when at least one is true:

- the operator explicitly requests a durable Markdown result;
- repeated Challenge/re-Challenge materially shapes the candidate;
- the result is intended for later implementation or handoff;
- reconstructing the reasoning from chat/session history would be costly or unreliable;
- a non-authoritative decision/rationale record has genuine future reuse value.

Do not require it for routine status, simple factual questions, trivial edits, or work already durably represented by its real owner.

#### Output contract

When activated, produce:

1. a **concise operator summary** containing the result, exact GO/NO-GO boundary, recommended next step, and only material caveats; and
2. one complete **Markdown Convergence Packet** carrying the reconstructable detail.

A ChatGPT-like host may target roughly 150 words or less for the concise response when the complete packet is available, or honor a tighter operator-requested limit. The methodology does not depend on a particular UI, attachment mechanism, or word count; do not omit a material blocker, safety boundary, or currentness qualification merely to satisfy presentation brevity.

The packet should contain the smallest complete set needed to reconstruct the result:

- title/date/mode/declared scope;
- convergence status;
- authority status and owner references;
- evidence basis and mutations performed;
- executive conclusion;
- candidate/objective evaluated;
- only the **material** Challenge findings that changed the candidate or boundary;
- final converged recommendation/design/plan;
- compact decision log when multiple material decisions were made;
- residuals/blockers;
- GO/NO-GO;
- recommended next step;
- durable owner/reconciliation references.

Do not preserve repetitive drafts or raw conversation transcripts merely to prove that multiple passes occurred.

#### Authority labels

Use truthful derived-state labels such as:

- `NON_AUTHORITATIVE_REFERENCE`;
- `DERIVED_FROM_CURRENT_AUTHORITY`;
- `OWNER_RECONCILIATION_REQUIRED`;
- `OWNER_RECONCILED`.

A Convergence Packet is not project authority merely because it is complete, polished, or Challenge-clear. If a material accepted result has not yet become current owner-native truth, preserve that distinction and route it through the existing owner/Decision-Closure reconciliation path before dependent consequence.

#### Durable routing

Route a durable packet by semantic ownership:

1. **Project-specific result** — store with the owning project using an existing compatible non-authoritative report/design/note surface. Reference canonical owner truth rather than copying it as a replacement.
2. **PROGRAMSTART-methodology result** — use an existing PROGRAMSTART non-authoritative design/evidence surface when appropriate.
3. **Genuine cross-project/operator reference** — use the operator's external non-authoritative workspace or another already-earned portfolio/reference surface. Such an archive is not a queue, backlog, priority source, currentness source, or execution authority.
4. **Owner unclear** — do not use a convergence archive as a catch-all inbox. Use existing owner-search, idea-preservation, conversation-capture, or Authority-Gap routing until the correct owner is known.

A downloadable/ephemeral copy and a repository-persisted copy are delivery/reference views of the same result, not two independently maintained truths. When a durable copy is created, expose its durable reference when practical.

For a material Convergence Packet that is intended to govern future implementation or handoff, **downloadable delivery alone is not reconstructable durability**. Before claiming the result can be resumed without the originating chat/session, the owning project MUST expose a durable machine-addressable owner record that preserves the material operationalization semantics. Use the reusable Decision Operationalization Manifest contract when structured reconstruction/Matrix projection is warranted. The owning project chooses its existing compatible durable surface; PROGRAMSTART does not impose a universal folder.

A durable plan may be classified as `REFERENCE_PLAN` while implementation is deferred. That classification preserves reconstruction and associations without creating executable obligations. Only explicit current owner authority may advance the plan to `ACTIVE_OPERATIONALIZATION`.

#### Reuse and retrieval

Do not scan packet archives on every project turn. Retrieve a packet only when the current request, owner reference, handoff, or explicit revisit trigger makes it relevant.

If current owner truth conflicts with a stored packet, the packet is stale. Reconcile or supersede the derived packet; never rewrite current project truth to match the archive.


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
2. **Resolve accepted recommendation when relevant** — if this invocation follows generic operator acceptance of a prior recommendation, derive the correct disposition under §9.6 and preserve any stronger gate before treating the acceptance as execution authority.
3. **Classify blockers / safe lanes when relevant** — distinguish the blocked closure action from safe independent preparation before deciding execution must stop.
4. **Validate** — confirm scope, authority, known state, acceptance criteria, and whether checklist completeness should be active.
5. **Execute** — perform the work without widening scope silently.
6. **Verify** — run the targeted verification defined in the packet.
7. **Reconcile** — update decisions, project state, and the strategic execution spine where required; reconcile any active checklist against actual evidence.
8. **Close** — mark the packet complete or blocked; do not keep completed packets or checklists as competing plans.
9. **Generate next** — derive the next packet from the newly current project state.

For long-running work, a repository MAY keep a `CURRENT_WORK_PACKET.md` as a derived, replaceable artifact. It is never canonical over the strategic plan, requirements, architecture, or decision log.

---

### Verify milestones at the accepting boundary

| Milestone | Producer → consumer and acceptance rule |
|---|---|
| Admission | The project owner supplies the current scope and Work Packet. Controller admits the exact effect against the owner revision, root and input digest, or waits for the missing scope or evidence. |
| Effect observed | The execution owner supplies the original result and receipt. Controller reconciles the native request ID, canonical input digest and parent/child evidence before advancing the same attempt. Unknown stays attached to the original. |
| Independent business verification | The designated verifier grades the bound result against the Work Packet’s criteria and returns the evidence to the acceptance owner. Missing or rejected evidence keeps settlement open. |
| Terminal owner disposition | The authorized owner records the decision against the exact candidate, receipt and applicable criteria. A run in verifying is still awaiting this decision. |
| Resource release, where required | The custody owner reconciles the exact claim or fence, resource and execution unit with current state. Confirm normal release and positive proof that the prior execution and any surviving actors cannot mutate the resource. Hold custody while that proof is missing. See [Work Packet custody rules](PROGRAMBUILD_WORK_PACKET.md). |

Within the existing Controller lifecycle, compare the reconciled original receipt with the Work Packet. Sufficient evidence advances to owner closure without a verifier dispatch. In the qualification scenario, a recoverable missing fact permits one narrowly scoped admitted read, deterministic first. Reconcile that read by its own identity if delivery is uncertain. If historical evidence of actual artifact use is irrecoverable, retain the existing root and seek owner disposition. A later read of current bytes cannot establish earlier worker use.

A separate settled example is [TRA PR-0](https://github.com/GrahamArdent/truck-route-authority/issues/1#issuecomment-7000843648). The exact candidate has an owner-delegated ACCEPT and terminal receipt. The [independent Controller coordination snapshot](https://github.com/GrahamArdent/programstart-compute-spine/blob/main/control/controller-results/req-controller-tra353-terminalstate-20261012t162208398z/result.json) observes the same terminal root with no claims or reserved attempts. The owner’s [Controller record](https://github.com/GrahamArdent/programstart-autonomous-controller/issues/353) records the normal fence release and cleanup evidence. Apply these observations only to that case.

## 12. Re-Entry After A Pause

Start by resolving the original request ID and canonical input digest with the owner’s native result store. Bind the lookup to the original root, Work Packet and attempt. A wrong digest must fail closed. Preserve the original request and evidence.

| Native disposition | Next action |
|---|---|
| Pending or in progress | Rejoin the admitted original or wait on the native result. Keep the same attempt and any required custody. |
| Unknown | Reconcile the exact original with its owner. A route failure or an empty search does not establish absence. Keep the effect held while the outcome is unknown. |
| Settled | Read back the bound result and apply the existing verification and owner-disposition rules. Preserve receipts and avoid a second dispatch. |
| Verified absent | Record the native proof of absence. A successor requires separately admissible authority for the exact effect, target and conditions. |

Use [Paths failure diagnosis](https://github.com/GrahamArdent/paths/blob/main/CHATGPT.md) for a route or selector failure. An equivalent admitted route may restore access to the same target and effect. A protected effect remains held until its owner’s prerequisite is satisfied across all routes. Apply the [Work Packet operator gate](PROGRAMBUILD_WORK_PACKET.md#32-operator--manual-gate-handoff-rule) and shared-mutation controls. Record the waiting state, next owner, safe independent work, acceptable return proof and exact resume point. Resume the same objective after validating that proof.

When work resumes after a pause:

- locate the current execution authority
- inspect changes since the last trusted checkpoint
- reuse still-valid evidence
- retrieve only captured/shelved ideas whose stated trigger or current decision makes them relevant; do not scan the whole idea collection by default
- route only genuinely uncertain/changed decisions through additional scrutiny
- classify any newly observed blocker at its narrowest truthful scope and scan safe lanes
- run only the re-entry checks needed to detect drift
- regenerate the active work packet from current state
- discover/reuse an applicable durable checklist when its obligations still govern the resumed boundary
- do not reconstruct the entire project from chat memory

For PROGRAMBUILD-managed projects, also use the Re-Entry Protocol in `PROGRAMBUILD_CHALLENGE_GATE.md` where applicable.

---

## 13. Anti-Patterns

Avoid:

- multiple documents each claiming to be the master plan
- research reports promoted to execution authority without a decision
- idea ledgers/records treated as backlog priority, accepted scope, or sequencing authority
- discarding worthwhile ideas solely because they are not current work
- giant prompts containing the entire repository documentation set
- re-running unchanged checks every session
- implementation checklists that quietly redefine strategy
- checklists created and then ignored at closure
- duplicating an applicable durable checklist instead of reusing it
- making generic `proceed` either a universal permission slip or a reason to ask the operator to restate already-derivable methodology
- rewriting the strategic Master for ordinary implementation detail
- accepted future ideas silently resequencing active work
- stronger approval gates being erased by generic acceptance
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
4. identify the existing idea/opportunity preservation surface and reuse it; if none exists, introduce `IDEA_LEDGER.md` only when there are worthwhile ideas to preserve;
5. identify duplicate or competing planning artifacts;
6. define what should be loaded always versus just in time;
7. define evidence-reuse and invalidation rules, including provider/resource continuity where relevant;
8. introduce work packets as a derived execution aid if useful;
9. use adaptive routing only for decisions whose delta actually earns it;
10. classify blockers narrowly and scan safe lanes before stopping useful independent work;
11. resolve accepted recommendations against current authority rather than treating generic acceptance as unbounded permission;
12. discover and reuse existing applicable checklists when omission risk makes them useful;
13. recommend edits to the existing master plan rather than replacing it;
14. record any material process change through the repository's decision mechanism.

The goal is less planning friction with stronger control, not more documentation.

---

## 15. Success Test

This operating model is working when an operator or agent can answer these quickly:

- What is authoritative?
- What are we doing now?
- Which documents actually matter for this slice?
- What has already been proven?
- Which worthwhile ideas are merely captured/shelved versus actually promoted into authority?
- If the closure row is blocked, what exact action is blocked and what safe lane remains?
- For external resources, what is verified historically versus currently visible/accessibile?
- Do we know enough to make the next important decision?
- If not, what exact evidence is missing and what could it change?
- Is targeted research enough, or is deep research genuinely justified?
- What is the stop condition?
- If the operator just accepted a recommendation, does that mean execute now, reconcile durable authority then execute, or defer without resequencing?
- Is there a stronger gate that generic acceptance cannot satisfy?
- Does an applicable checklist need to be active, and are all required items accounted for before closure?
- What changed enough to require re-verification?
- What proves this slice is complete?
- Where will any durable decision be recorded?

If answering those questions requires loading the whole repository, scanning every stored idea, invoking every gate, interpreting several competing plans, or asking the operator to restate already-derivable methodology, the planning system needs simplification.
