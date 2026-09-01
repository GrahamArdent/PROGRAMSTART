# PROGRAMBUILD_CANONICAL.md

# Program Build Canonical Authority

This file is the control document for the Program Build system.
If two planning documents disagree, this file decides which one is authoritative.

---

## 1. Canonical Rules

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this section are interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

1. Validated code and validated tests MUST outrank any planning document when conflicts are discovered retroactively. However, developers MUST update the relevant authority document before introducing new code that would contradict it.
2. This file defines which planning document is authoritative for each concern.
3. `PROGRAMBUILD_FILE_INDEX.md` is the official inventory of critical planning files.
4. No duplicate authority is allowed. One concern, one primary owner. A file MUST NOT be canonical for more than one concern.
5. If a file is deprecated or replaced, the file index and this file MUST be updated in the same change.
6. PROGRAMSTART is a template repository. Filled project outputs belong in the real project repository, not here.
7. `USERJOURNEY/` is an optional project attachment, not a mandatory PROGRAMBUILD subsystem.
8. A project MUST have one primary strategic execution spine. Research, audits, readiness reviews, checklists, adaptive-router outputs, accepted-recommendation resolutions, idea ledgers/records, and work packets MUST NOT silently become competing master plans.
9. A work packet is a **logical derived execution contract**. It MAY be persisted as `CURRENT_WORK_PACKET.md` when persistence adds coordination/risk/resumption value; whether persisted or not, it MUST defer to the strategic spine, requirements, architecture, decisions, and validated implementation state.
10. Challenge Gate parts A–H are canonical risk controls, but the Product variant MUST select them by stage/risk. Full A–H is required only where `PROGRAMBUILD_CHALLENGE_GATE.md` defines whole-system Product convergence; Enterprise keeps its full-gate requirements.
11. No universal feature count, calendar cadence, file count, project count, agent count, or numeric rigor score becomes PROGRAMBUILD policy unless evidence and the canonical owner explicitly justify that threshold.
12. Adaptive decision routing MUST select additional scrutiny from actual decision-relevant uncertainty/consequence; it MUST NOT create a second lifecycle, execution spine, or mandatory all-gates sequence.
13. In Mode C, a blocked closure-control row MUST be scoped before the project is treated as stopped. Safe-lane reasoning belongs to `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`; a narrow blocker does not authorize consequential work that project-specific dependencies or safety rules still prohibit.
14. For external/provider resources, verified historical existence MUST remain distinct from current visibility/accessibility. Current invisibility alone MUST NOT rewrite history as `never existed` or `deleted` without evidence that proves that conclusion.
15. Cross-repository dependency reasoning MUST remain derived and task-scoped. Each repository MUST retain its own execution spine, decisions, state, and closure authority. A dependency/authority graph MAY support read/orient/classify/plan/verify work, but MUST NOT silently create a portfolio Master or grant authority to advance, close, merge, or mutate multiple projects as one transaction.
16. Operator/manual gate handoffs MUST remain derived and subordinate. When the current environment cannot perform the exact next action, the handoff MUST identify the gate owner, required action, secret-safe input boundary, non-secret return evidence, acceptance/invalidation conditions, safe work while waiting, and exact resume point when those facts are knowable. Operator action completion MUST NOT be treated as system acceptance without the required evidence, and a handoff MUST NOT request or persist secret values merely to make the gate durable.
17. Concurrent Mode-C lane coordination MUST remain a derived view of one project's existing execution spine. It MAY expose multiple relevant current lanes only when project authority proves they can coexist, but each invocation MUST select one bounded current work packet. A lane view MUST NOT create a parallel backlog, second sequencing authority, automatic multi-agent scheduler, or permission to run consequential mutations concurrently. When sibling lanes can mutate the same consequential external/runtime/provider/device/deployment resource, exactly one explicit mutation owner MUST serialize that resource across invocations until an explicit release or transfer condition is satisfied; sibling work may continue only when it is proven unable to mutate that shared resource.
18. PROGRAMSTART acceptance learning MUST remain evidence-driven and subordinate to product execution. Meaningful checkpoints MAY produce learning observations and maturity updates, but ordinary PROGRAMSTART usage MUST NOT automatically create ledger noise or authorize methodology changes. Product completion MUST NOT depend on the ability to mutate the PROGRAMSTART repository, and the learning ledger MUST NOT become a product backlog, portfolio Master, or execution authority.
19. PROGRAMSTART cost governance MUST remain decision-scoped and subordinate to project budget, architecture, security, and release authority. A Cost Envelope MAY structure material paid/metered/quota decisions, but it MUST NOT become a central vendor-price registry, procurement authority, portfolio budget, or second execution spine. Volatile pricing/limit evidence MUST be refreshed only when its staleness can materially change the current decision.
20. Generic operator acceptance of a concrete recommendation MUST be resolved against current project authority before execution. `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` owns the disposition rules. Generic acceptance MUST NOT silently resequence future work, churn strategic authority for ordinary implementation detail, or satisfy a stronger explicit approval/operator/consequence gate merely because the operator said `proceed`.
21. Checklists MUST remain derived completeness/verification surfaces. They MAY be activated when omission risk or an applicable durable checklist warrants them, but MUST NOT create scope, sequencing, a second Master, or mandatory ceremony for trivial work. When a checklist is active for a slice, applicable required items MUST be reconciled before truthful closure according to `PROGRAMBUILD_WORK_PACKET.md` and `PROGRAMBUILD_CHECKLIST.md`.
22. Worthwhile ideas SHOULD be durably preserved without being silently promoted. `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` owns capture/promotion semantics. A captured, candidate, investigating, shelved, rejected, or superseded Idea Record is evidence/reference material only; recording it MUST NOT imply priority, scope, sequencing, budget, architecture, or permission to execute. An accepted idea MUST reconcile into the existing project authority that owns the changed truth before dependent execution. A live cross-project idea portfolio MUST NOT be stored in PROGRAMSTART itself.
23. Learning-capable software MUST use owner-routed learning when real operational evidence can materially improve behavior. `docs/PROGRAMSTART_LEARNING_ARCHITECTURE.md` owns the conditional Learning Architecture Gate, owner-classification, evaluation/promotion/rollback discipline, and the rule that learned behavior MUST NOT silently broaden authority. Learning capability MUST NOT create a mandatory project artifact, shadow backlog, autonomous policy authority, or uncontrolled self-modification mechanism merely because telemetry or AI is present.

---

## 2. Critical Naming Standard

All critical control and planning files use uppercase snake case.

Prefix rules:
- System-level control files use the `PROGRAMBUILD_` prefix.
- Project execution outputs use direct functional names without a prefix when they are stage outputs.

System control files:
- `PROGRAMBUILD_CANONICAL.md`
- `PROGRAMBUILD_FILE_INDEX.md`
- `PROGRAMBUILD_ADR_TEMPLATE.md`
- `PROGRAMBUILD_CHANGELOG.md`
- `PROGRAMBUILD_KICKOFF_PACKET.md`
- `PROGRAMBUILD_SUBAGENTS.md`
- `PROGRAMBUILD_CHECKLIST.md`
- `PROGRAMBUILD_IDEA_INTAKE.md`
- `PROGRAMBUILD_CHALLENGE_GATE.md`
- `PROGRAMBUILD_GAMEPLAN.md`
- `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`
- `PROGRAMBUILD_WORK_PACKET.md`
- `PROGRAMBUILD.md`
- `PROGRAMBUILD_LITE.md`
- `PROGRAMBUILD_PRODUCT.md`
- `PROGRAMBUILD_ENTERPRISE.md`

Project execution outputs:
- `FEASIBILITY.md`
- `DECISION_LOG.md`
- `RESEARCH_SUMMARY.md`
- `REQUIREMENTS.md`
- `USER_FLOWS.md`
- `ARCHITECTURE.md`
- `RISK_SPIKES.md`
- `TEST_STRATEGY.md`
- `RELEASE_READINESS.md`
- `AUDIT_REPORT.md`
- `POST_LAUNCH_REVIEW.md`

Optional preservation / execution aids:
- `IDEA_LEDGER.md` — optional non-authoritative idea/opportunity preservation surface; may be replaced by an existing equivalent project/workspace system
- `CURRENT_WORK_PACKET.md` — replaceable persisted view of the current logical packet; never canonical and not required when compact task/session state is sufficient

---

## 3. Authority Map

| Concern | Canonical file |
|---|---|
| overall process and stage deliverables | `PROGRAMBUILD.md` |
| lighter-weight process | `PROGRAMBUILD_LITE.md` |
| standard product process | `PROGRAMBUILD_PRODUCT.md` |
| enterprise process | `PROGRAMBUILD_ENTERPRISE.md` |
| document authority and naming rules | `PROGRAMBUILD_CANONICAL.md` |
| critical file inventory and status | `PROGRAMBUILD_FILE_INDEX.md` |
| planning-to-execution separation, idea capture/promotion semantics, proportional rigor, blocker scope/safe-lane reasoning, adaptive decision/evidence routing, accepted-recommendation resolution, checklist activation rules, context loading, and evidence reuse | `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` |
| logical work-packet semantics, accepted-recommendation disposition evidence, checklist completeness/closure, blocker/safe-lane fields, coordinated Mode-C lane view and shared-mutation ownership, cross-repository dependency/authority fields, operator/manual-gate handoff semantics, and optional persisted packet format | `PROGRAMBUILD_WORK_PACKET.md` |
| PROGRAMSTART decision-scoped cost governance, Cost Envelope semantics, cost-evidence freshness, cap/reuse/pay-when rules, and anti-registry boundary | `docs/PROGRAMSTART_COST_GOVERNANCE.md` |
| PROGRAMSTART acceptance-learning triggers, observation/rollup semantics, maturity rules, and future-retest routing | `docs/PROGRAMSTART_LEARNING_LOOP.md` |
| conditional product/system Learning Architecture Gate, owner-routed operational learning, learning-data boundaries, evaluation/promotion/rollback discipline, and authority-safe adaptive improvement | `docs/PROGRAMSTART_LEARNING_ARCHITECTURE.md` |
| ADR structure, decision-log linkage, and supersession hygiene | `PROGRAMBUILD_ADR_TEMPLATE.md` |
| architecture decision records index | `docs/decisions/README.md` |
| commit message format and enforcement | `.github/instructions/conventional-commits.instructions.md` |
| system-level change history | `PROGRAMBUILD_CHANGELOG.md` |
| new-project starter packet | `PROGRAMBUILD_KICKOFF_PACKET.md` |
| subagent definitions and prompt templates | `PROGRAMBUILD_SUBAGENTS.md` |
| reusable execution-checklist form and checklist status discipline | `PROGRAMBUILD_CHECKLIST.md` |
| 8-dimension idea decomposition and pre-feasibility challenge | `PROGRAMBUILD_IDEA_INTAKE.md` |
| stage transition/convergence risk controls and gate-part selection | `PROGRAMBUILD_CHALLENGE_GATE.md` |
| execution sequencing and cross-stage validation | `PROGRAMBUILD_GAMEPLAN.md` |
| project viability decision | `FEASIBILITY.md` |
| material project decisions and reversals | `DECISION_LOG.md` |
| external research and stack validation | `RESEARCH_SUMMARY.md` |
| requirements and scope | `REQUIREMENTS.md` |
| user journey and state behavior | `USER_FLOWS.md` |
| system boundaries, contracts, data model, auth model | `ARCHITECTURE.md` |
| risky unknowns and proofs | `RISK_SPIKES.md` |
| test model and coverage plan | `TEST_STRATEGY.md` |
| launch and operational gate | `RELEASE_READINESS.md` |
| post-build drift and risk findings | `AUDIT_REPORT.md` |
| post-launch outcomes and lessons learned | `POST_LAUNCH_REVIEW.md` |
| automation gate definitions and nox session composition | `./noxfile.py` |
| editor task surface and operator workflow shortcuts | `.vscode/tasks.json` |

`IDEA_LEDGER.md` is an optional storage template, not a canonical authority surface. Its lifecycle meaning comes from `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`.

---

## 4. Conflict Resolution

When documents disagree, resolve in this order:

1. validated code and tests
2. `PROGRAMBUILD_CANONICAL.md`
3. the file named in the authority map for that concern
4. all other supporting files

If a conflict is found:
- update the canonical owner first;
- update dependent files second;
- update the file index only when inventory/status/role semantics changed.

A logical or persisted work packet never outranks its source authority. Correct/regenerate the packet rather than changing authority merely to match derived task state.

An adaptive-router result is advisory derived reasoning. It never outranks the project's execution spine, accepted decisions, requirements, architecture, or validated implementation state.

An accepted-recommendation resolution is derived from current authority. It never makes a deferred recommendation current merely because the operator accepted it, and it never makes contradicted assumptions authoritative merely because they were previously recommended.

An Idea Record or Idea Ledger never outranks project authority. Capturing, shelving, rejecting, or investigating an idea does not make it current work. When an idea is accepted for promotion, reconcile the owning project artifact and point the record to that authority rather than using the idea surface as a substitute roadmap.

A checklist never outranks the requirement/decision/gate/acceptance source from which its items were derived. Correct the checklist when authority changes rather than preserving stale checklist scope.

A derived cross-repository graph never outranks either repository's authority. Correct the dependency facts or regenerate the graph rather than using it to rewrite either project's execution spine.

An operator/manual handoff never outranks project authority and never proves the gated outcome merely because the requested human/provider/device action occurred. Reconcile returned evidence against the declared acceptance condition, then resume the existing spine at the declared point.

A coordinated Mode-C lane view never outranks the project's execution spine or dependency order. Correct/regenerate the lane view when live project authority changes rather than preserving stale lane priority as derived state. A shared-mutation ownership lease is conflict control only: it cannot grant broader mutation authority, and any contradictory resource/owner evidence must be reconciled before consequential mutation resumes.

A decision-scoped Cost Envelope never outranks project budget, architecture, security, operational, or release authority. Correct/refresh the cost evidence when pricing, limits, usage, or requirements change rather than preserving stale provider economics as methodology truth.

A PROGRAMSTART learning observation or ledger entry never outranks the real project's authority and never proves a methodology change is required merely because friction was observed. Correct the learning classification/maturity from evidence rather than using the ledger to rewrite product state.

A product/system learning observation, adaptive recommendation, experiment result, or learned policy never outranks the owning project's requirements, architecture, decisions, security, budget, release, or execution authority. Route the evidence to the owner and promote changes only through that owner's normal authority path; learned success never grants broader authority by itself.

---

## 5. Canonical Maintenance Rules

- No new critical file is added without an entry in `PROGRAMBUILD_FILE_INDEX.md`.
- No critical file is renamed without updating all references in the same change.
- No concern is split across multiple sources of truth unless one is explicitly derived.
- Derived summaries must point back to the canonical owner.
- `PROGRAMBUILD_CHANGELOG.md` records system-level changes but does not redefine authority.
- Material decisions go in `DECISION_LOG.md`; promote durable architecture/policy rationale to an ADR when the repository's current ADR policy warrants it, not because an arbitrary numeric threshold was crossed.
- The template repository keeps project outputs reusable; do not store filled project-specific feasibility, requirements, architecture, release, packet, idea-portfolio, or portfolio state here.
- Research that affects an existing project should become explicit delta recommendations adopted through that project's authority process.
- Preserve worthwhile future ideas in the owning project/workspace's existing idea/reference system, or use the optional `IDEA_LEDGER.md` template when no compatible surface exists. Do not require full intake merely to capture, do not delete useful rejected/shelved rationale by default, and do not turn the ledger into a shadow backlog.
- Accepted recommendation resolution should retain only enough context to identify the recommendation, disposition, authority reconciliation need, and stronger gate. Do not turn accepted recommendations into a new durable registry or hidden backlog.
- Checklists should retain only the obligations needed to avoid meaningful omission and should reference current authority where practical. Close/discard derived slice checklists with the work packet; do not turn them into shadow strategy.
- Cross-repository orchestration may retain only the task-scoped relationship/evidence needed to derive the current packet. A live portfolio registry or cross-project Master belongs outside PROGRAMSTART unless a future explicit authority decision creates one.
- Operator/manual handoffs should retain only the task-scoped action/evidence/resume contract needed to cross the gate. Do not turn them into a parallel ticketing system, credential store, or independent execution ledger.
- Concurrent Mode-C lane coordination may retain only enough derived lane state to select the current packet, preserve closure-control/dependency truth, and serialize any proven shared consequential mutation resource through one explicit owner plus a release/transfer condition. Do not persist a parallel lane backlog or global lock system when the project spine already owns sequencing.
- Cost governance may retain current decision evidence and invalidation conditions where a project needs durable rationale, but PROGRAMSTART must not maintain a central vendor-price/free-tier catalogue whose volatility would turn stale evidence into false authority.
- PROGRAMSTART learning should retain detailed evidence in append-only observation records and keep the main learning ledger as a concise maturity rollup. Do not load or rewrite detailed history by default during normal product work.
- Product/system learning should reuse existing requirements, architecture, test, decision, execution-spine, Work Packet, and post-launch authority surfaces by default. Create a dedicated learning ledger only when retained learning state genuinely earns one, and keep it subordinate to the owning system rather than turning it into a shadow backlog or autonomous authority.
- Specialist agents, extra documents, broader gates, recurring automation, checklists, idea ledgers, learning ledgers, and adaptive routing are mechanisms, not goals. Use them only when they reduce real uncertainty/risk/coordination/omission/reconstruction cost or measurably improve outcomes.

---

Last updated: 2026-09-01