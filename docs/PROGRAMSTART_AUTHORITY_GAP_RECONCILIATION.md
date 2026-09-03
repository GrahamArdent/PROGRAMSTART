# PROGRAMSTART Authority-Gap Reconciliation

Purpose: define the deterministic PROGRAMSTART response when a derived checklist, audit, portfolio finding, accepted conversation outcome, research result, or other non-authoritative evidence identifies worthwhile work that is not represented in the owning project's current authority.

Status: **PROGRAMSTART operational application protocol / subordinate to owning-project authority**.

This protocol composes existing PROGRAMSTART primitives. It does **not** create a new lifecycle, recommendation disposition, backlog, execution spine, authority source, or portfolio state machine.

Primary dependencies:

- `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`
- `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md`
- `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md`
- `docs/PROGRAMSTART_LEARNING_LOOP.md`
- `PROGRAMBUILD/PROGRAMBUILD_PORTFOLIO_CONTROL.md`

---

## 1. Core rule

> **A derived finding may discover missing work, but it cannot create execution authority.**

An **Authority Gap** exists when all of the following are true:

1. a current derived/evidence surface identifies a material requirement, accepted delta, risk, dependency, acceptance obligation, or architectural need;
2. the finding is not already represented strongly enough in the current authority of the repository that should own it;
3. dependent execution would make the owning authority materially false, misleading, contradictory, or unsafe if it proceeded unchanged.

An Authority Gap is a routing condition, not a new project state.

Do not use `AUTHORITY_GAP` as a fourth accepted-recommendation disposition. Use the existing Planning Operating Model dispositions, especially `reconcile_authority_then_execute` when durable project truth must change.

---

## 2. Detection sources

Common sources include:

- a derived portfolio or closure checklist;
- an audit/readiness review;
- accepted conversation outcomes;
- research findings or recommendations;
- current runtime/provider/device evidence;
- a cross-project integration finding;
- a verification or Challenge result;
- a stale derived surface that no longer matches project truth.

The source remains evidence/reference. It does not become the owning project's execution spine.

---

## 3. Required resolution sequence

When a candidate Authority Gap is encountered, perform this sequence before dependent implementation:

1. **Re-read owning authority.** Load the current strategic execution spine/current stage, active Work Packet when present, and only the task-relevant authority/evidence needed to evaluate the finding.
2. **Re-verify the premise.** Determine whether the derived finding is still current, already completed, superseded, contradicted, or based on stale assumptions.
3. **Classify ownership and effect.** Select the smallest truthful case below.
4. **Reconcile before dependent execution when required.** Use the existing owner of durable scope/sequencing/architecture/dependency/milestone/acceptance/decision truth.
5. **Verify authority now exists.** Do not infer success merely because a note or checklist field was updated.
6. **Derive the bounded Work Packet from reconciled authority.** Normal PROGRAMSTART consequence/gate/effective-autonomy rules apply.
7. **Return to the originating flow.** Resume the checklist/audit/portfolio task automatically when current authority permits; do not require a redundant generic `proceed`.

---

## 4. Classification

### A. Already represented

The finding is already covered by current project authority strongly enough to authorize the proposed consequence.

Action:

- do not churn the Master/strategic spine;
- execute through current authority;
- correct only stale derived status if needed.

Typical disposition: `execute_current_authority`.

### B. Stale, disproved, duplicate, or unnecessary derived finding

Current authority/evidence shows the finding is already complete, superseded, duplicated, contradicted, or no longer useful.

Action:

- reconcile/correct the derived source;
- do not manufacture project work;
- preserve useful rationale only when it has future retrieval value.

### C. Existing-project authority delta

The finding belongs to an existing project and changes durable scope, sequencing, architecture, dependency, milestone/definition-of-done, acceptance criteria, or a material prior decision.

Action:

- reconcile the existing owning authority **before or atomically with dependent implementation**;
- then derive the Work Packet from the updated authority.

Typical disposition: `reconcile_authority_then_execute`.

### D. Cross-project architectural/dependency finding

More than one repository is involved, but one repository clearly owns each relevant meaning/contract/capability.

Action:

- preserve separate project execution spines;
- route each durable concern to its actual owner;
- use the task-scoped cross-repository dependency graph from `PROGRAMBUILD_WORK_PACKET.md`;
- reference, do not duplicate, companion authority.

### E. Worthwhile future direction, not current sequence

The operator accepts the direction or the finding is useful, but current authority/dependency order says it is not current executable work.

Action:

- preserve it in the appropriate existing idea/future/decision/reference surface;
- do not resequence current work merely because the finding is worthwhile.

Typical disposition: `defer_without_resequencing`.

### F. No legitimate owner yet

No existing repository clearly owns the finding after checking plausible owners.

Action:

- do not execute from the derived finding;
- preserve the smallest useful non-authoritative record in the operator's portfolio/planning workspace;
- record candidate owners and the trigger/evidence that would resolve ownership;
- create a new project/repository only when normal PROGRAMSTART idea/promotion rules earn it.

### G. External limitation rather than project-authority defect

The missing step is caused by a provider, credential scope, physical device, machine capability, or other external boundary rather than missing project authority.

Action:

- keep project authority truthful;
- route the missing capability/identity/provider work to its real owner;
- preserve the actual human/consequence gate when one is genuinely required;
- do not rewrite project authority merely to make the external limitation disappear.

---

## 5. Minimal Authority-Gap record

Do not create a global Authority-Gap ledger by default.

When persistence materially improves resumption or cross-session coordination, the originating derived surface or current Work Packet may carry a compact record such as:

```yaml
authority_gap:
  source: <derived finding / checklist item / audit>
  finding: <material delta>
  authority_search:
    represented: false
  classification: <existing_project_delta | cross_project | future_direction | no_owner | external_limit>
  proposed_owner: <repo/artifact or unresolved>
  reconciliation:
    status: <pending | complete | rejected | superseded>
    authority_ref: <exact owning artifact/ref when complete>
  return_to: <originating flow/item>
```

The record is derived routing evidence. It is not execution authority and does not need to exist for simple same-session reconciliation.

---

## 6. Learning loop

Every resolved Authority Gap should answer two different questions:

1. **Immediate ownership:** Where does this work or correction belong?
2. **Reusable learning:** Why was the material finding absent or mismatched?

Do not assume every Authority Gap is a PROGRAMSTART defect.

At the next meaningful Learning Gate, classify the cause under `docs/PROGRAMSTART_LEARNING_LOOP.md`:

- **genuinely new information** — no methodology defect;
- **local project omission** — reconcile locally;
- **stale/incorrect derived state** — fix the deriving/routing surface;
- **systemic PROGRAMSTART friction/failure** — evaluate a reusable methodology change;
- **confirmation/counterevidence** — strengthen, narrow, or reject an existing lesson when warranted;
- **external limitation** — route to the owning system/provider integration, not PROGRAMSTART by default.

Search the existing learning ledger before creating a new lesson. Existing validated primitives such as accepted-recommendation reconciliation, idea promotion, Mode-C preservation, portfolio routing, and effective-autonomy consequence separation should be reused rather than renamed.

A project must not be blocked merely because PROGRAMSTART learning evidence cannot be persisted at that moment.

---

## 7. Automatic orchestration behavior

When a PROGRAMSTART-assisted flow consumes a derived checklist/audit/portfolio item:

1. treat the item as evidence/attention routing;
2. identify the owning project/repository;
3. enter Mode C when the project is existing/in-flight;
4. search current authority before execution;
5. if represented, proceed normally;
6. if not represented and authority-worthy, run this Authority-Gap reconciliation;
7. if no current owner exists, preserve/reroute without executing;
8. after reconciliation, resume the originating item automatically when the remaining action is already authorized and effectively automatable;
9. stop only at the narrowest real human/consequence/capability boundary.

The desired operator experience is that a command such as `Continue the Autonomy Closure Checklist` can route into current project authority without turning the checklist into authority or requiring the operator to restate PROGRAMSTART mechanics.

---

## 8. First real retest

The first natural real retest should be the first Autonomy Closure Checklist item that is materially useful but not represented in its proposed owner's current authority.

Success requires:

- the checklist item does not execute directly;
- current project authority is inspected first;
- the correct owner is selected or explicitly unresolved;
- a real authority-worthy delta is reconciled into the existing owning artifact rather than a second roadmap;
- dependent execution derives from the reconciled authority;
- the originating checklist resumes without a redundant `proceed` when otherwise authorized;
- the Learning Gate determines whether the gap was new information, local/derived friction, external limitation, or reusable PROGRAMSTART evidence;
- no duplicate lifecycle, backlog, or lesson is created merely because the phrase `Authority Gap` was used.

If the first real case is already solved by existing primitives with no additional methodology change, that is a successful retest.

---

## 9. Anti-bloat invariants

- One project keeps one execution spine.
- A derived checklist/audit may discover work but never authorize it.
- `AUTHORITY_GAP` is routing shorthand, not a lifecycle state.
- Do not create a global authority-gap backlog by default.
- Do not create a new Master Game Plan merely to absorb a finding.
- Do not churn durable authority for ordinary implementation details.
- Do not create a new PROGRAMSTART lesson when an existing lesson already explains the failure mode.
- Do not let methodology learning block product/project completion.
- After reconciliation, return to the actual current execution flow instead of remaining in analysis.