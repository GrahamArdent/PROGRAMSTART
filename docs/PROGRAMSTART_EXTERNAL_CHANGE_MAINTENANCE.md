# PROGRAMSTART External Change Maintenance

Purpose: convert verified external ecosystem changes into the smallest safe PROGRAMSTART/project maintenance action without turning vendor news into architecture authority, creating a second lifecycle, or requiring the operator to manually relay deterministic maintenance work.

Status: **PROGRAMSTART operational protocol / subordinate to PROGRAMBUILD canonical authority, the owning project's authority, Cost Governance, Challenge Gate, and Learning Loop.**

This protocol governs how PROGRAMSTART reacts when an external dependency, platform, tool, model, API, runtime, plan, pricing surface, required field, or capability changes after a prior decision was made.

---

## 1. Core Principle

External monitoring should normally terminate in **maintenance**, not merely notification.

Use this loop:

**DETECT → VERIFY → CLASSIFY → MAP IMPACT → ACT AT THE LOWEST SAFE AUTONOMY LEVEL → VERIFY → RECORD EVIDENCE → NOTIFY ONLY WHEN NEEDED**

A monitoring event is evidence. It is not authority to rewrite architecture, project scope, budget, security policy, or release state.

PROGRAMSTART should remove unnecessary operator work when the correct response is deterministic, while preserving human control where a real decision or consequential action remains.

---

## 2. Trigger Conditions

Activate this protocol only when current evidence indicates that an external change could invalidate or materially improve a PROGRAMSTART/project assumption.

Typical triggers include:

- a model, API version, command, action, package, runtime, or integration is deprecated or retired;
- an upstream provider adds a required field or contract requirement;
- a documented replacement or migration path becomes necessary;
- plan availability, usage limits, pricing, quotas, or included capacity change enough to affect an existing decision;
- a provider capability appears/disappears or moves between plans;
- a security advisory or upstream compatibility change invalidates a current dependency choice;
- a new provider/runtime capability materially changes a previously accepted architecture tradeoff;
- Watchtower, a scheduled monitor, an execution node, GitHub, or another trusted evidence source reports an upstream change relevant to a managed repository.

Do not run broad ecosystem research merely because time passed. Use evidence freshness and invalidation rules from the Planning Operating Model and Cost Governance.

---

## 3. Evidence Standard

Before maintenance is authorized, establish the minimum sufficient evidence for the claimed external change.

Prefer, in order:

1. official provider/product documentation or release notes;
2. official account/plan/runtime evidence when the fact is account-specific;
3. authoritative repository/runtime evidence showing the current target assumption;
4. secondary sources only as discovery aids when official evidence is unavailable.

Conflicting or ambiguous official evidence blocks deterministic maintenance and routes to `material_decision` or `automation_failed` until the conflict is resolved.

Do not persist a central vendor-price or feature catalogue as permanent truth. Preserve only the evidence needed to explain the affected decision plus its freshness/invalidation conditions.

---

## 4. External Change Record

When durable evidence improves coordination or resumption, derive a compact record:

```text
EXTERNAL_CHANGE_ID:
SOURCE_PROVIDER:
SOURCE_REF:
OBSERVED_AT:
EFFECTIVE_AT:
CHANGE_KIND:
AFFECTED_CAPABILITY:
VERIFIED_FACTS:
CURRENT_ASSUMPTION:
IMPACTED_TARGETS:
CLASSIFICATION:
AUTHORITY_OWNER:
VALIDATION_PLAN:
AUTONOMY_MODE:
OPERATOR_GATE:
INVALIDATION:
```

This record is derived evidence, not a roadmap, issue backlog, vendor registry, or project authority. Do not persist it when the PR/incident/decision record already preserves the necessary facts.

---

## 5. Classification

Every verified change routes to exactly one current classification.

### `no_effect`

The external fact does not affect PROGRAMSTART or any currently relevant managed decision.

Action:

- do nothing;
- do not create ledger noise;
- do not notify the operator unless explicitly requested.

### `evidence_refresh`

The change refreshes volatile evidence but does not require code/configuration/authority changes now.

Examples:

- current pricing changed but the project remains inside already-approved included capacity;
- plan packaging changed but the current execution path is unaffected;
- a newly available feature may matter only if a future trigger occurs.

Action:

- refresh only the decision-relevant evidence when persistence is useful;
- preserve the invalidation/revisit trigger;
- do not mutate architecture merely because an alternative became available.

### `deterministic_maintenance`

A current target is objectively stale/invalid and the verified replacement is unambiguous.

Examples:

- retired model identifier with an officially documented replacement;
- removed command replaced by one documented successor;
- upstream required field added with one compatible target representation;
- generated/tooling reference that must change to retain compatibility.

Deterministic maintenance requires all of the following:

- the external change is verified from authoritative evidence;
- the affected repository/assumption is identified from live authority or implementation;
- the replacement does not require a material architecture, security, privacy, spending, destructive, migration, release, or project-scope decision;
- the change is bounded enough to review and verify coherently;
- an applicable validation path exists;
- no stronger gate is triggered.

Action:

- prepare the smallest focused branch/PR automatically when the repository boundary is already authorized;
- run the smallest sufficient targeted validation;
- retain source evidence, target SHA, changed surface, validation result, and PR reference;
- auto-merge only when the target repository explicitly permits it under Section 7.

### `bounded_behavioral_maintenance`

The external change affects behavior/recommendations but the architectural direction remains intact and the adjustment is still bounded.

Action:

- use the Adaptive Decision Router only if the behavioral delta creates genuine uncertainty/consequence;
- prepare a focused PR automatically when authorized;
- default to **PR-only** until that maintenance playbook has earned stronger trust through repeated successful evidence;
- do not notify the operator when no decision/action is required and repository policy allows silent PR preparation/digest reporting.

### `material_decision`

The external change can alter architecture, security boundaries, privacy/legal posture, project authority, release policy, significant cost, destructive behavior, data/schema/migration strategy, or another hard-to-reverse choice.

Action:

- investigate only the missing decision-relevant evidence;
- use current project/PROGRAMSTART authority plus the Adaptive Decision Router and Cost Gate as applicable;
- prepare the recommendation and proposed change as far as safely possible;
- require the appropriate operator/project approval before the consequential decision is enacted.

### `automation_failed`

The maintenance loop cannot prove the change, impact, repository state, validation result, or safe action.

Action:

- stop mutation;
- preserve the exact failure/evidence boundary;
- notify the operator only when intervention is required or the failure leaves a meaningful exposure unresolved.

---

## 6. Authority and Downstream Project Boundary

PROGRAMSTART may identify multiple affected repositories, but it MUST NOT mutate them as one portfolio transaction.

For each affected project:

1. enter that project's current authority/Mode-C context;
2. verify that the external change actually invalidates or changes a current project assumption;
3. derive only the project-specific delta;
4. use a separate branch/PR/evidence boundary for that repository;
5. leave project sequencing, release, and closure decisions with the owning project authority.

A PROGRAMSTART update may improve the reusable methodology/control plane without automatically propagating a strategic replan to every project using PROGRAMSTART.

Selective sync/adoption mechanisms may propagate managed reusable controls when their existing authority permits it; project-owned implementation/configuration remains project-owned.

---

## 7. Autonomous PR and Auto-Merge Gate

Automatic PR creation and automatic merge are different trust levels.

### Automatic PR creation MAY occur when

- repository access/boundary consent is already authorized;
- the change is `deterministic_maintenance` or sufficiently bounded `bounded_behavioral_maintenance`;
- the target branch is based on current repository authority;
- the diff is focused and does not unexpectedly expand scope;
- the required evidence/validation can be produced truthfully.

### Auto-merge MAY occur only when all are true

- target repository policy explicitly enables auto-merge for the applicable maintenance playbook/change class;
- required branch/ruleset/status/convergence gates are actually enforced and green;
- no architecture/security/privacy/legal/billing/migration/destructive/project-authority/release gate is triggered;
- no protected/blocked surface is touched;
- validation covers the actual changed surface;
- the post-implementation Challenge Gate is clear when the actual implementation risk triggers it;
- rollback/recovery is understood;
- no contradictory evidence remains.

If the repository lacks an explicit auto-merge policy or an enforceable required validation gate, the safe default is **PR-only**, even for deterministic maintenance.

Do not weaken branch protection, validation, or repository policy merely to make external maintenance more automatic.

---

## 8. Operator Notification Policy

The desired normal state is **silence when the system safely handled the change**.

Notify the operator when one or more are true:

- a material decision or approval is required;
- security/privacy/legal/billing/destructive/migration/release authority is implicated;
- official evidence is contradictory or ambiguous;
- automated validation failed;
- an automatic maintenance PR cannot safely proceed or merge;
- the change creates unexpected cost/exposure;
- a previously trusted maintenance playbook regressed or needs to be disabled.

Successful routine maintenance may be summarized in a digest/audit view instead of interrupting the operator.

---

## 9. Watchtower Integration Boundary

Watchtower is a natural optional **sensor / incident / evidence / later execution-plane partner** for this protocol, but it is not PROGRAMSTART methodology authority.

A clean division of responsibility is:

- **Watchtower** — receive provider/repository/runtime signals, authenticate/normalize/dedupe them, maintain incident/evidence history, calculate health, and (when its own project authority permits) execute repository-policy-scoped remediation playbooks;
- **PROGRAMSTART** — interpret external changes against PROGRAMSTART/project authority, classify the maintenance delta, apply decision/cost/challenge/verification rules, and define the safe autonomy level;
- **target project** — owns its code, architecture, decisions, release state, repository policy, and final closure truth;
- **execution node / runner** — provides persistent shell/runtime capacity when maintenance requires real command/test execution.

If Watchtower's current authority is observe-only, PROGRAMSTART MUST treat it as a sensor/evidence source only. A future Watchtower milestone may enable `PR_ONLY` or `AUTO_MERGE` playbooks, but that permission must be earned in Watchtower's own authority and target-repository policy; PROGRAMSTART must not silently upgrade Watchtower's trust level.

The integration contract should remain event/evidence based rather than tightly coupling PROGRAMSTART's methodology internals to Watchtower implementation.

A future normalized Watchtower event may carry facts such as:

```text
provider
source_event_id
change_kind
affected_capability
evidence_reference
effective_at
suspected_repositories
```

PROGRAMSTART then performs authority/impact classification. Watchtower must not infer that detection alone authorizes a repository mutation.

---

## 10. Execution Runtime Independence

This protocol is independent of the monitoring/runtime implementation.

The detector/runner may be:

- a scheduled ChatGPT/OpenAI monitor;
- Watchtower;
- a GitHub App/webhook workflow;
- a PROGRAMSTART execution node;
- another trusted scheduler/worker.

The runtime must not change the authority rules.

An always-on execution node is useful for persistent checks, repository checkout, CLI execution, tests, browser validation, and queued maintenance; it is not itself permission to modify a project.

---

## 11. Circuit Breakers

Stop autonomous maintenance and downgrade to PR-only/manual review when:

- the same maintenance class causes a regression;
- the upstream provider reverses/flaps the relevant guidance;
- the diff expands beyond the predicted impact surface;
- validation cannot reproduce the claimed compatibility state;
- multiple official sources materially disagree;
- a supposedly deterministic change touches a protected consequential surface;
- repeated retries fail or create noisy duplicate work.

Do not retry indefinitely. Preserve enough evidence to resume after the root uncertainty is resolved.

---

## 12. Cost, Security, and Learning Composition

This protocol composes existing PROGRAMSTART controls instead of replacing them.

- **Cost Governance** — pricing/plan/quota changes are external evidence; cost-bearing decisions still use the Cost Envelope and remain subordinate to spending authority.
- **Adaptive Decision Router** — activates only when uncertainty/consequence can change the action; deterministic maintenance should not acquire research ceremony.
- **Challenge Gate** — applies when the actual completed maintenance touches risk surfaces that trigger it.
- **Learning Loop** — routine successful external maintenance is not automatically a PROGRAMSTART learning event. Use the Learning Gate only when the maintenance process itself materially helps/fails/reveals a reusable methodology lesson.
- **Portfolio Attention** — a provider change may invalidate a project's portfolio row, but external maintenance does not become a portfolio execution spine.

---

## 13. Success Test

External-change maintenance is working when:

- irrelevant changes disappear without operator noise;
- volatile evidence is refreshed only when it matters;
- objectively stale required fields/models/commands/configuration are corrected through focused verified maintenance without requiring the operator to relay the fix;
- material architecture/security/cost/project-authority choices still reach the correct human gate;
- successful maintenance leaves source, target SHA, validation, and PR/merge evidence;
- downstream projects remain independently authoritative;
- Watchtower can contribute sensing/evidence without becoming a shadow methodology or gaining mutation authority early;
- automation becomes more trusted only after the repository/playbook has earned that trust;
- failures stop safely and surface only the intervention actually required.
