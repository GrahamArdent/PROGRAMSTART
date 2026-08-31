# PROGRAMBUILD_FILE_INDEX.md

# Program Build File Index

This is the official index for critical Program Build files and key PROGRAMSTART methodology-support surfaces referenced by the orchestration protocol.
A PROGRAMBUILD critical control file missing from this index is not recognized. PROGRAMSTART support surfaces may be indexed for routing/discoverability without becoming PROGRAMBUILD control files.

---

## 1. Control Files

| File | Type | Status | Purpose | Canonical for |
|---|---|---|---|---|
| `PROGRAMBUILD_CANONICAL.md` | control | active | authority map and naming rules | document authority |
| `PROGRAMBUILD_FILE_INDEX.md` | control | active | inventory of critical files | file inventory |
| `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` | control | active | separates reusable methodology, project authority, non-authoritative idea preservation/promotion, active work, JIT context, blocker scope/safe-lane reasoning, adaptive decision/evidence routing, accepted-recommendation resolution, checklist activation, external-resource evidence continuity, and evidence reuse | planning-to-execution operating model |
| `PROGRAMBUILD_PORTFOLIO_CONTROL.md` | protocol | active | lightweight cross-project operator attention routing with external live-workspace boundary, bounded WIP, evidence freshness, and handoff back to project authority | reusable portfolio-attention semantics only — canonical for no project's state, scope, sequencing, or completion |
| `PROGRAMBUILD_WORK_PACKET.md` | template/protocol | active | compact logical work-packet semantics, accepted-recommendation disposition/gate evidence, checklist completeness/closure, blocker/safe-lane fields, coordinated Mode-C lane selection, task-scoped cross-repository dependency/authority evidence, operator/manual-gate handoff semantics, plus optional persisted format | logical work-packet semantics |
| `PROGRAMBUILD_ADR_TEMPLATE.md` | template | active | MADR 4.0 format, status lifecycle, decision-log linkage, and supersession hygiene | ADR structure |
| `PROGRAMBUILD_CHANGELOG.md` | control | active | system-level change history | PROGRAMBUILD change history |
| `PROGRAMBUILD.md` | playbook | active | balanced default stage deliverables and operating practices | stage deliverables/base workflow |
| `PROGRAMBUILD_LITE.md` | variant | active | lean workflow | lite execution model |
| `PROGRAMBUILD_PRODUCT.md` | variant | active | standard production workflow with stage/risk-aware gates | product execution model |
| `PROGRAMBUILD_ENTERPRISE.md` | variant | active | high-consequence/audit-heavy workflow | enterprise execution model |
| `PROGRAMBUILD_KICKOFF_PACKET.md` | template | active | starter document pack and inputs | kickoff structure |
| `PROGRAMBUILD_SUBAGENTS.md` | catalog | active | optional specialist roles/prompts | subagent guidance |
| `PROGRAMBUILD_CHECKLIST.md` | checklist | active | reusable execution checklist plus derived checklist activation/source/status/closure discipline | execution tracking |
| `PROGRAMBUILD_IDEA_INTAKE.md` | protocol | active | 8-dimension idea/project-delta challenge; consumes captured/shelved idea evidence without treating capture as approval | idea intake |
| `PROGRAMBUILD_CHALLENGE_GATE.md` | protocol | active | A–H risk controls plus variant/stage/risk-based gate-part selection | stage/convergence gates |
| `PROGRAMBUILD_GAMEPLAN.md` | playbook | active | canonical stage sequence and cross-stage validation without duplicating stage detail | execution sequencing |

---

## 2. Project Output Files

These are standard project artifacts. In PROGRAMSTART they remain reusable templates; filled content belongs in the real project repository.

| File | Type | Status | Purpose | Canonical for |
|---|---|---|---|---|
| `FEASIBILITY.md` | output | standard | go/no-go and kill criteria | project viability |
| `DECISION_LOG.md` | output | standard | material decisions, reversals, rationale | project decision history |
| `RESEARCH_SUMMARY.md` | output | standard | market/technical research evidence | research findings |
| `REQUIREMENTS.md` | output | standard | scope and requirements | product scope |
| `USER_FLOWS.md` | output | standard | primary workflows/state behavior where applicable | UX/flow behavior |
| `ARCHITECTURE.md` | output | standard | contracts, topology, data/trust model | technical architecture |
| `RISK_SPIKES.md` | output | standard | material unknowns and proofs | technical risk resolution |
| `TEST_STRATEGY.md` | output | standard | test model, traceability, evidence rules | quality model |
| `RELEASE_READINESS.md` | output | standard | launch convergence and operational readiness | release readiness |
| `AUDIT_REPORT.md` | output | standard | drift and risk findings | audit findings |
| `POST_LAUNCH_REVIEW.md` | output | standard | outcomes, lessons, follow-up | post-launch learning |

### Optional Persisted Preservation / Execution Aids

These artifacts are optional. Use an existing compatible project/workspace surface instead when one already exists.

| File | Type | Status | Purpose | Canonical for |
|---|---|---|---|---|
| `IDEA_LEDGER.md` | derived/reference output | optional | preserve worthwhile captured/candidate/investigating/shelved/accepted/rejected/superseded ideas without implying scope, priority, or execution | none — lifecycle semantics come from Planning Operating Model |
| `CURRENT_WORK_PACKET.md` | derived output | optional | replaceable persisted view of the current logical packet | none — must defer to source authority |

A portfolio-wide `IDEA_LEDGER.md` instance belongs in the operator's planning workspace or another dedicated portfolio system, not in PROGRAMSTART's reusable template repository.

---

## 3. Tooling, Enforcement, and PROGRAMSTART Support Files

| File | Type | Purpose |
|---|---|---|
| `scripts/programstart_decision.py` | advisory tooling | routes a material decision to the minimum justified evidence/check/research depth; never a separate authority layer |
| `scripts/programstart_orchestrate.py` | advisory tooling | derives environment/mode/authority/blocker-aware execution contracts, including safe-lane, evidence-continuity, task-scoped cross-repository dependency/authority, and operator/manual-boundary guidance; free-form recommendation acceptance remains authority-derived in the agent protocol rather than brittle CLI keyword parsing |
| `docs/PROGRAMSTART_COST_GOVERNANCE.md` | protocol | owns the conditional decision-scoped Cost Envelope for paid/metered/quota-limited dependencies, cost-evidence freshness, cap/reuse/pay-when semantics, and the anti-registry guardrail; subordinate to project budget/architecture authority |
| `docs/PROGRAMSTART_EXTERNAL_CHANGE_MAINTENANCE.md` | operational protocol | classifies verified external ecosystem changes and routes them to no-op/evidence refresh/deterministic or bounded maintenance/material decision/failure behavior, including PR-vs-auto-merge gates and the optional Watchtower sensor/execution-plane boundary; subordinate to project authority and existing Cost/Challenge/Learning controls |
| `docs/PROGRAMSTART_LEARNING_LOOP.md` | protocol | owns PROGRAMSTART acceptance-learning triggers, observation/rollup semantics, maturity rules, conditional persistence, and future-retest routing |
| `docs/PROGRAMSTART_ACCEPTANCE_LEARNING_LEDGER.md` | derived rollup | concise lesson maturity/index view; not an activity log or project authority |
| `docs/PROGRAMSTART_REAL_WORLD_ACCEPTANCE_CHECKLIST.md` | checklist | real-project acceptance and Learning Gate closure checklist |
| `docs/acceptance/LEARNING_OBSERVATION_TEMPLATE.md` | evidence template | append-only meaningful PROGRAMSTART learning observation structure |
| `docs/acceptance/observations/*.md` | derived evidence | individual real-project/system observations used to mature or challenge lessons |
| `docs/acceptance/PROGRAMSTART_ACCEPTANCE_HISTORY_THROUGH_2026-08-27.md` | historical snapshot | byte-preserved detailed pre-learning-loop ledger history |
| `templates/portfolio/PROJECT_REGISTRY.yaml` | workspace template | reusable external live-registry schema; filled project state belongs outside PROGRAMSTART |
| `templates/portfolio/PORTFOLIO_STATUS.md` | workspace template | concise operator attention/status view with one primary build plus optional operator gate/fallback |
| `templates/portfolio/PORTFOLIO_HISTORY.md` | workspace template | meaningful attention transitions only; does not mirror repository history |
| `scripts/check_commit_msg.py` | enforcement | validates Conventional Commits |
| `.github/instructions/conventional-commits.instructions.md` | instruction | commit message rules |
| `.gitlint` | spec-reference | commit-message enforcement spec |
| `docs/decisions/README.md` | index | MADR decision-record index |
| `docs/decisions/NNNN-*.md` | decision record | durable MADR records |
| `noxfile.py` | automation | nox session definitions and local/full convergence composition |
| `.vscode/tasks.json` | tooling | editor workflow shortcuts |
| `.github/workflows/manual-convergence.yml` | repo-specific automation | PROGRAMSTART full repository gate, manual `workflow_dispatch` only; not a generated-project bootstrap asset |
| `templates/github-workflows/full-ci-gate.yml` | generated-project template | manual-only full gate materialized into generated repos; projects may add automatic triggers when justified |

---

## 4. Shaping Prompts

Prompts live in `.github/prompts/`, are registered in the process registry, and must follow `PROMPT_STANDARD.md` where applicable.

| File | Stage | Purpose |
|---|---|---|
| `shape-idea.prompt.md` | 0 | idea/delta decomposition plus conditional adaptive evidence routing |
| `shape-feasibility.prompt.md` | 1 | kill criteria and viability |
| `shape-research.prompt.md` | 2 | evidence gathering |
| `shape-requirements.prompt.md` | 3 | requirements/flows |
| `shape-architecture.prompt.md` | 4 | topology/contracts/technology |
| `shape-scaffold.prompt.md` | 5 | skeleton and structural guardrails |
| `shape-test-strategy.prompt.md` | 6 | test/evidence strategy |
| `shape-release-readiness.prompt.md` | 8 | release convergence |
| `shape-post-launch-review.prompt.md` | 10 | outcome/learning review |

---

## 5. Index Rules

- Add new **critical PROGRAMBUILD control files** here when created.
- Index PROGRAMSTART support protocols/artifacts here when the orchestration system depends on them for discoverability/authority routing.
- Mark files as active/deprecated/replaced/derived as applicable.
- Do not create synonyms for the same purpose.
- Advisory tooling may be indexed for discoverability without becoming a new canonical concern.
- Use `DECISION_LOG.md` for ongoing material project decisions.
- Use ADRs only when durable architecture/policy rationale warrants them under current policy.
- Filled project outputs never become canonical examples in PROGRAMSTART.
- An Idea Record or `IDEA_LEDGER.md` is optional non-authoritative preservation evidence. Capture may be broad; promotion must reconcile into the existing owning authority. Do not turn captured ideas into a shadow roadmap/backlog or require the ledger to exist when an equivalent durable surface already does the job.
- A persisted `CURRENT_WORK_PACKET.md` is optional and derived; close/replace it rather than accumulating packet history as a second plan.
- Accepted-recommendation resolution is derived from the current recommendation plus project authority; it is not a durable recommendation registry, approval state machine, or backlog.
- An active checklist is derived from current authority/acceptance/risk obligations; it is not scope authority and should be closed/discarded with the packet unless an existing durable checklist already owns the boundary.
- A task-scoped cross-repository dependency graph is derived evidence, not a control file or project execution spine.
- An operator/manual-gate handoff is derived execution context, not a credential store, project authority, or independent lifecycle.
- A coordinated Mode-C lane view is derived execution context under one project spine, not a backlog, scheduler, or second sequencing authority.
- A decision-scoped Cost Envelope is derived execution/decision evidence, not a purchasing authority, vendor-price registry, portfolio budget, or second execution spine.
- An external-change maintenance classification/event is derived operational evidence; it may trigger a bounded project-specific maintenance PR but never becomes architecture, budget, release, portfolio, or project authority by itself.
- A portfolio-attention view is derived operator routing context; live filled state belongs outside PROGRAMSTART and cannot override any project's execution authority.
- A learning observation is derived methodology evidence; the learning ledger is a maturity rollup, not an activity log or roadmap.
- Tooling/support files may appear here for operator discoverability without becoming product-project authority.

---

Last updated: 2026-08-31