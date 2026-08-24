# PROGRAMBUILD_FILE_INDEX.md

# Program Build File Index

This is the official index for critical Program Build files.
If a file is missing from this index, it is not a recognized PROGRAMBUILD control file.

---

## 1. Control Files

| File | Type | Status | Purpose | Canonical for |
|---|---|---|---|---|
| `PROGRAMBUILD_CANONICAL.md` | control | active | authority map and naming rules | document authority |
| `PROGRAMBUILD_FILE_INDEX.md` | control | active | inventory of critical files | file inventory |
| `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` | control | active | separates reusable methodology, project authority, active work, JIT context, and evidence reuse | planning-to-execution operating model |
| `PROGRAMBUILD_WORK_PACKET.md` | template/protocol | active | compact logical work-packet semantics plus optional persisted format | logical work-packet semantics |
| `PROGRAMBUILD_ADR_TEMPLATE.md` | template | active | MADR 4.0 format, status lifecycle, decision-log linkage, and supersession hygiene | ADR structure |
| `PROGRAMBUILD_CHANGELOG.md` | control | active | system-level change history | PROGRAMBUILD change history |
| `PROGRAMBUILD.md` | playbook | active | balanced default stage deliverables and operating practices | stage deliverables/base workflow |
| `PROGRAMBUILD_LITE.md` | variant | active | lean workflow | lite execution model |
| `PROGRAMBUILD_PRODUCT.md` | variant | active | standard production workflow with stage/risk-aware gates | product execution model |
| `PROGRAMBUILD_ENTERPRISE.md` | variant | active | high-consequence/audit-heavy workflow | enterprise execution model |
| `PROGRAMBUILD_KICKOFF_PACKET.md` | template | active | starter document pack and inputs | kickoff structure |
| `PROGRAMBUILD_SUBAGENTS.md` | catalog | active | optional specialist roles/prompts | subagent guidance |
| `PROGRAMBUILD_CHECKLIST.md` | checklist | active | concise execution checklist | execution tracking |
| `PROGRAMBUILD_IDEA_INTAKE.md` | protocol | active | 8-dimension idea/project-delta challenge | idea intake |
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

### Optional Persisted Execution Aid

The logical work packet normally lives in current task/issue/PR/session state. Persist a file only when that improves coordination/risk/resumption.

| File | Type | Status | Purpose | Canonical for |
|---|---|---|---|---|
| `CURRENT_WORK_PACKET.md` | derived output | optional | replaceable persisted view of the current logical packet | none — must defer to source authority |

---

## 3. Tooling and Enforcement Files

| File | Type | Purpose |
|---|---|---|
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
| `shape-idea.prompt.md` | 0 | idea/delta decomposition |
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
- Mark files as active/deprecated/replaced/derived as applicable.
- Do not create synonyms for the same purpose.
- Use `DECISION_LOG.md` for ongoing material project decisions.
- Use ADRs only when durable architecture/policy rationale warrants them under current policy.
- Filled project outputs never become canonical examples in PROGRAMSTART.
- A persisted `CURRENT_WORK_PACKET.md` is optional and derived; close/replace it rather than accumulating packet history as a second plan.
- Tooling may appear here for operator discoverability without becoming a PROGRAMBUILD authority concern.

---

Last updated: 2026-08-24
