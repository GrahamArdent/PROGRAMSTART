# PROGRAMBUILD_PORTFOLIO_CONTROL.md

# Program Build Portfolio Attention Control

Purpose: Define a lightweight cross-project attention-control protocol for operators managing many independently governed repositories without creating a portfolio master plan, shadow backlog, or global execution authority.
Owner: Project Lead / Operator
Last updated: 2026-08-29
Depends on: `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`, `PROGRAMBUILD_WORK_PACKET.md`, `PROGRAMBUILD_FILE_INDEX.md`, `docs/PROGRAMSTART_LEARNING_LOOP.md`
Authority: Canonical only for reusable portfolio-attention semantics, storage boundaries, refresh discipline, attention lanes, WIP limits, and handoff back to project authority. It is canonical for **no project's product state, scope, sequencing, or completion status**.

---

## 1. Problem This Protocol Solves

A repository ledger can answer **what changed**. A project execution spine can answer **what this project should do next**. Neither necessarily answers the operator-level question:

> **Where should limited attention go next across many repositories?**

When many repositories coexist, several failure modes become likely:

- every unfinished repository feels equally urgent;
- a deliberately paused project looks neglected merely because time passed;
- a five-minute operator/device/provider gate is buried under a large implementation queue;
- a blocked project consumes attention even when another project has a clear executable slice;
- recent activity is mistaken for priority;
- a cross-project dashboard silently becomes a second roadmap;
- the operator repeatedly reconstructs current state from chat memory.

Portfolio Attention Control exists to reduce that cognitive and coordination burden while preserving every project's independent authority.

---

## 2. Non-Negotiable Authority Boundary

PROGRAMSTART / PROGRAMBUILD may own:

- the reusable portfolio-attention method;
- schemas/templates for an operator portfolio workspace;
- rules for evidence freshness, prioritization, WIP, and project handoff;
- guidance for producing a concise attention recommendation.

PROGRAMSTART / PROGRAMBUILD MUST NOT own:

- the operator's live global project registry;
- a filled portfolio of unrelated repositories;
- another project's current milestone state as durable truth;
- a global backlog that can sequence work inside projects;
- a project lifecycle state machine that overrides project-owned state;
- a central completion authority.

The **live** portfolio belongs in the operator's planning workspace or another dedicated portfolio system. It may be a spreadsheet, database, private repository, or another durable surface that can hold current operator-owned cross-project metadata.

A portfolio row is a **derived attention view**. The owning project's current authority and verified implementation/runtime evidence remain authoritative for project truth.

When portfolio state disagrees with a project's current authority or verified reality, the portfolio is stale. Refresh the portfolio; do not rewrite the project to match the portfolio.

---

## 3. Keep Three Concerns Separate

### 3.1 Project progress

Owned by the individual repository's execution spine, current implementation, decisions, requirements, runtime/provider evidence, and acceptance artifacts.

Answers:

- Where is this project?
- What does this project need next?
- What is blocked or accepted?

### 3.2 Historical / methodology evidence

Owned by the appropriate project history, change ledger, decision records, acceptance evidence, or PROGRAMSTART Learning Loop.

Answers:

- What changed?
- What was learned?
- Why was a decision made?

### 3.3 Portfolio attention

Owned by the operator's external portfolio workspace using this protocol.

Answers:

- Which project deserves attention now?
- Is there a short operator action that unlocks high-value work?
- Which repositories should explicitly receive no attention right now?

Portfolio attention MUST NOT absorb the responsibilities of the other two concerns.

---

## 4. Minimal Live Workspace

The first useful version needs only three logical surfaces. They may be files, spreadsheet tabs, or equivalent database views.

### 4.1 Project Registry

One row/record per known project or repository.

Recommended fields:

- `PROJECT_ID` — stable operator-facing identifier.
- `REPOSITORY` — repository or primary system reference.
- `PURPOSE` — short description sufficient to distinguish the project.
- `OBSERVED_PROJECT_STATE` — descriptive project-owned state such as `R4 active`, `paused`, `physical acceptance pending`, or `unassessed`; this is not a PROGRAMSTART lifecycle.
- `AUTHORITY_REF` — exact project execution spine / status authority when known.
- `STRATEGIC_STATE` — concise current milestone/phase from current evidence.
- `IMMEDIATE_NEXT` — smallest coherent next action currently supported by authority.
- `BLOCKER_OR_GATE` — current external/manual/provider/device/release constraint if material.
- `DEPENDENCY_OR_LEVERAGE` — cross-project dependency or unlock value when material.
- `ATTENTION_CLASS` — derived operator attention class from Section 5.
- `LAST_VERIFIED_AT` — when the row was last grounded against live evidence.
- `EVIDENCE_REF` — commit, PR, authority section, provider/runtime proof, or other retrievable evidence.
- `INVALIDATION_TRIGGER` — what would make the row unsafe to reuse.
- `NOTES` — only if they materially improve safe resumption.

Do not require every field to be filled. Missing precision should become `unknown` / `unassessed`, not invented certainty.

### 4.2 Portfolio Status / Attention Queue

A short human-readable view optimized for a fast operator decision.

It SHOULD answer, in order:

1. **Operator gate now** — at most one short human/device/provider action worth doing now.
2. **Primary build now** — exactly one repository when executable work is available.
3. **Secondary ready** — at most one fallback/safe lane to use if the primary is blocked, completed, or intentionally deferred.
4. **Watch / parked / no-action projects** — brief reasons they should not consume current attention.
5. **Unassessed repositories** — visible but excluded from priority until they earn triage.

The status view is not a roadmap. It should normally be readable in a few minutes.

### 4.3 Portfolio History

Record only meaningful attention-state changes, such as:

- a project becomes the primary build;
- an operator gate is completed or becomes newly blocking;
- a project is deliberately removed from current attention;
- a dependency materially changes priority;
- a stale row is corrected after live verification.

Do not mirror commits, PRs, or every portfolio refresh. Repository history already exists elsewhere.

---

## 5. Attention Classes

Use attention classes only for **current operator routing**. They are not project lifecycle states.

- **`PRIMARY_BUILD`** — the one project selected for current substantive execution.
- **`OPERATOR_GATE`** — the one short operator/device/provider/manual action currently worth doing because it unlocks or closes meaningful work.
- **`SECONDARY_READY`** — one bounded fallback or safe lane that is executable if the primary cannot proceed.
- **`WATCH`** — current state matters, but no active intervention is justified now.
- **`PARKED`** — deliberately excluded from current attention; preserve the reason or revisit trigger when useful.
- **`UNASSESSED`** — known project, insufficient current evidence for prioritization; not urgent merely because it exists or is old.

A project may have a project-owned state such as `paused`, `active`, `complete`, or `maintenance` in `OBSERVED_PROJECT_STATE`. Do not convert that descriptive evidence into a new PROGRAMSTART lifecycle system.

---

## 6. WIP Discipline

Default portfolio WIP is intentionally narrow:

- maximum **one `PRIMARY_BUILD`**;
- maximum **one `OPERATOR_GATE`**;
- maximum **one `SECONDARY_READY`** fallback shown prominently;
- everything else is `WATCH`, `PARKED`, or `UNASSESSED` until evidence justifies movement.

`SECONDARY_READY` is not permission to run a second consequential build in parallel. It is the next safe choice when the primary is blocked, completed, or deliberately deferred.

The operator may intentionally override the WIP limit, but the portfolio view should make that choice explicit rather than silently accumulating active work.

---

## 7. How To Choose What Deserves Attention

Do not rank primarily by repository age, number of open tasks, or most recent commit.

Use an evidence-backed qualitative comparison across these dimensions:

- **Outcome value** — how much meaningful product/operator value the next slice creates.
- **Dependency leverage** — whether completing it unlocks one or more other projects or removes repeated friction.
- **Urgency / timing** — genuine deadlines, expiring evidence, provider windows, or time-sensitive risk.
- **Risk reduction** — material security, reliability, data, release, or operational risk retired by the slice.
- **Execution readiness** — whether authority, environment, tools, and evidence make a bounded next action executable now.
- **Operator effort** — whether a very small human action can unlock disproportionately valuable progress.
- **Cost / effort burden** — expected work, paid/metered cost, setup burden, or context-loading cost.
- **Blocking constraints** — whether current progress depends on a provider, credential, device, approval, or unavailable environment.

A numeric score is optional and usually unnecessary. If used, it is advisory evidence only. Do not pretend a formula can replace judgment or project authority.

Every promoted item should have a short **WHY_NOW** explanation grounded in current evidence.

---

## 8. Operator-Gate Selection

A portfolio-level operator gate is useful when a small human action can unlock or close meaningful work across an otherwise healthy implementation.

Prefer the gate with the best combination of:

- shortest reasonable operator effort;
- highest unlock/closure value;
- clear exact action;
- clear safe handling of credentials/private inputs;
- clear return evidence;
- clear resume point.

Reuse the operator/manual-gate contract in `PROGRAMBUILD_WORK_PACKET.md` after handing off to the selected project.

Do not put secrets, tokens, private provider payloads, recovery codes, or sensitive user content in the portfolio workspace.

---

## 9. Refresh Protocol

A portfolio sweep should be cheap by default.

### 9.1 Start from retained state

Read the live portfolio workspace first. Do not re-audit every repository from scratch.

### 9.2 Verify only what can change the attention decision

For candidate/current projects, prefer a narrow sequence such as:

1. repository/default-branch existence and recent meaningful commits/PR state;
2. the exact current project execution authority / status section;
3. blocker or manual-gate evidence;
4. provider/runtime/device state only when it can change the attention decision.

Do not run broad deployment, database, security, or provider audits merely to refresh a dashboard row.

### 9.3 Reuse evidence until invalidated

Keep `LAST_VERIFIED_AT`, `EVIDENCE_REF`, and `INVALIDATION_TRIGGER` so unchanged rows can be reused cheaply.

Typical invalidation triggers include:

- execution-spine update;
- merge/closure of the named packet;
- new provider/runtime evidence;
- changed dependency state;
- operator-gate completion;
- explicit project pause/resume;
- contradictory implementation/CI evidence.

### 9.4 Staleness is not urgency

An old `LAST_VERIFIED_AT` means **verify before relying on the row**. It does not mean **work on the project**.

A deliberately parked or paused project must not rise in priority simply because it has been untouched.

### 9.5 Unassessed projects do not crowd the queue

A known repository may remain `UNASSESSED` until:

- the operator asks about it;
- another project depends on it;
- its purpose/status becomes decision-relevant;
- a periodic bounded triage is intentionally scheduled.

Do not deep-audit a long tail of repositories merely to make a registry look complete.

---

## 10. Portfolio Recommendation Output

When the operator asks **“What should we work on?”**, **“Where should my attention go?”**, or equivalent, return a compact recommendation grounded in the live portfolio workspace and refreshed evidence.

Use this order:

### Operator gate now

- project
- exact operator action
- why it is worth doing now
- return evidence / resume point

Omit this section when no operator gate currently earns attention.

### Primary build now

- project
- strategic state
- one bounded immediate objective
- why now
- exact project authority to load
- blocker/stop condition
- targeted verification / convergence gate

### Secondary ready

- project
- why it is the fallback
- when to switch to it

### Explicit no-action set

Name only the projects that would otherwise create operator confusion. State the evidence-backed reason to leave them alone (for example, explicitly paused, waiting on a larger manual gate, healthy/maintenance, or unassessed).

Do not return a long unprioritized list merely because many projects exist.

---

## 11. Handoff Back To Project Authority

Portfolio control ends when a project is selected.

For an existing repository:

1. enter PROGRAMSTART Mode C;
2. read the owning project's current execution spine and only the concern-specific authority needed for the selected slice;
3. verify the portfolio row has not become stale;
4. derive one logical Work Packet when useful;
5. execute from project authority;
6. reconcile the project inside its own repository;
7. refresh the external portfolio row only after project truth changes.

The portfolio never closes a project milestone, approves a release, changes project scope, or authorizes a mutation by itself.

---

## 12. Relationship To Existing PROGRAMSTART Mechanisms

### Repository / change ledger

Keep it. It answers historical/change questions. Portfolio control should reference it only when its evidence affects attention.

### Cross-repository dependency orchestration

Keep it task-scoped. Portfolio control may notice that a dependency has high leverage, but once selected, the existing Work Packet / cross-repository authority graph owns the bounded dependency reasoning.

### Coordinated Mode-C lanes

Keep them inside one project. Portfolio lanes are operator-level attention classes and must not replace a project's internal lane selection.

### Idea Ledger

Keep idea preservation separate. An idea can be worth remembering without becoming portfolio priority. Portfolio control must not turn captured ideas into a shadow backlog.

### Learning Loop

A repeated portfolio-control defect may become PROGRAMSTART learning evidence. Ordinary queue refreshes should not create methodology churn.

---

## 13. Anti-Bloat Guardrails

Do not add, absent repeated evidence:

- a portfolio project-management application;
- autonomous multi-repository mutation scheduling;
- a universal numeric priority formula;
- a duplicate global issue tracker;
- another Master Game Plan;
- mandatory detailed audits for every repository;
- project-owned lifecycle replication inside PROGRAMSTART;
- automatic promotion from `UNASSESSED` / `WATCH` into active work based on age;
- a requirement that every repository use PROGRAMSTART before it can appear in the registry.

Start with a durable registry, a concise status view, meaningful history, one operator gate, and one primary build.

Automation should be added only when repeated manual portfolio refresh work proves the value of the specific automation.

---

## 14. Initial Acceptance Criteria

The first Portfolio Attention Control implementation is acceptable when it can demonstrate that:

- PROGRAMSTART retains only reusable protocol/templates, not the operator's filled live portfolio;
- the live workspace points to project authority rather than copying/replacing it;
- one explicitly paused project can remain out of the active queue without being treated as stale urgent work;
- one externally/manual-gated project can be distinguished from a repo-only executable project;
- one short operator gate can be surfaced separately from the primary build;
- exactly one primary build is recommended with a bounded immediate next action;
- unassessed repositories remain visible without forcing broad audits;
- a selected project hands back to Mode C and its own execution spine;
- meaningful attention changes can be recorded without duplicating repository history.

---

## 15. Reusable Templates

PROGRAMSTART provides schema/examples only:

- `templates/portfolio/PROJECT_REGISTRY.yaml`
- `templates/portfolio/PORTFOLIO_STATUS.md`
- `templates/portfolio/PORTFOLIO_HISTORY.md`

Instantiate them outside PROGRAMSTART in the operator's planning workspace or dedicated portfolio system.
