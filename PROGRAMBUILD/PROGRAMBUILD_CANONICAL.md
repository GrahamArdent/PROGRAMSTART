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
8. A project MUST have one primary strategic execution spine. Research, audits, readiness reviews, checklists, and work packets MUST NOT silently become competing master plans.
9. A work packet is a **logical derived execution contract**. It MAY be persisted as `CURRENT_WORK_PACKET.md` when persistence adds coordination/risk/resumption value; whether persisted or not, it MUST defer to the strategic spine, requirements, architecture, decisions, and validated implementation state.
10. Challenge Gate parts A–H are canonical risk controls, but the Product variant MUST select them by stage/risk. Full A–H is required only where `PROGRAMBUILD_CHALLENGE_GATE.md` defines whole-system Product convergence; Enterprise keeps its full-gate requirements.
11. No universal feature count, calendar cadence, file count, project count, or agent count becomes PROGRAMBUILD policy unless evidence and the canonical owner explicitly justify that threshold.

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

Optional persisted execution aid:
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
| planning-to-execution separation, proportional rigor, context loading, and evidence reuse | `PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` |
| logical work-packet semantics and optional persisted packet format | `PROGRAMBUILD_WORK_PACKET.md` |
| ADR structure, decision-log linkage, and supersession hygiene | `PROGRAMBUILD_ADR_TEMPLATE.md` |
| architecture decision records index | `docs/decisions/README.md` |
| commit message format and enforcement | `.github/instructions/conventional-commits.instructions.md` |
| system-level change history | `PROGRAMBUILD_CHANGELOG.md` |
| new-project starter packet | `PROGRAMBUILD_KICKOFF_PACKET.md` |
| subagent definitions and prompt templates | `PROGRAMBUILD_SUBAGENTS.md` |
| execution checklist format | `PROGRAMBUILD_CHECKLIST.md` |
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

---

## 5. Canonical Maintenance Rules

- No new critical file is added without an entry in `PROGRAMBUILD_FILE_INDEX.md`.
- No critical file is renamed without updating all references in the same change.
- No concern is split across multiple sources of truth unless one is explicitly derived.
- Derived summaries must point back to the canonical owner.
- `PROGRAMBUILD_CHANGELOG.md` records system-level changes but does not redefine authority.
- Material decisions go in `DECISION_LOG.md`; promote durable architecture/policy rationale to an ADR when the repository's current ADR policy warrants it, not because an arbitrary numeric threshold was crossed.
- The template repository keeps project outputs reusable; do not store filled project-specific feasibility, requirements, architecture, release, packet, or portfolio state here.
- Research that affects an existing project should become explicit delta recommendations adopted through that project's authority process.
- Specialist agents, extra documents, broader gates, and recurring automation are mechanisms, not goals. Use them only when they reduce real uncertainty/risk/coordination cost.

---

Last updated: 2026-08-24
