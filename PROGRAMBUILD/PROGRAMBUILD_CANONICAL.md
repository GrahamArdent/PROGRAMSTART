# PROGRAMBUILD_CANONICAL.md

# Program Build Canonical Authority

This file is the control document for the Program Build system.
If two planning documents disagree, this file decides which one is authoritative.

---

## 1. Canonical Rules

1. Validated code and validated tests outrank any planning document.
2. This file defines which planning document is authoritative for each concern.
3. `PROGRAMBUILD_FILE_INDEX.md` is the official inventory of critical planning files.
4. No duplicate authority is allowed. One concern, one primary owner.
5. If a file is deprecated or replaced, the file index and this file must be updated in the same change.
6. The PROGRAMSTART repository is a template repository. Filled project outputs belong in the project repository created from this template, not in the template repository itself.
7. `USERJOURNEY/` is not part of the reusable PROGRAMBUILD template system. If used, it is a project attachment that may be present or absent depending on the project.

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

---

## 3. Authority Map

| Concern | Canonical file |
|---|---|
| overall process and stage order | `PROGRAMBUILD.md` |
| lighter-weight process | `PROGRAMBUILD_LITE.md` |
| standard product process | `PROGRAMBUILD_PRODUCT.md` |
| enterprise process | `PROGRAMBUILD_ENTERPRISE.md` |
| document authority and naming rules | `PROGRAMBUILD_CANONICAL.md` |
| critical file inventory and status | `PROGRAMBUILD_FILE_INDEX.md` |
| ADR structure and status vocabulary | `PROGRAMBUILD_ADR_TEMPLATE.md` |
| system-level change history | `PROGRAMBUILD_CHANGELOG.md` |
| new-project starter packet | `PROGRAMBUILD_KICKOFF_PACKET.md` |
| subagent definitions and prompt templates | `PROGRAMBUILD_SUBAGENTS.md` |
| execution checklist format | `PROGRAMBUILD_CHECKLIST.md` |
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

---

## 4. Conflict Resolution

When documents disagree, resolve in this order:

1. validated code and tests
2. `PROGRAMBUILD_CANONICAL.md`
3. the file named in the authority map for that concern
4. all other supporting files

If a conflict is found:
- update the canonical owner first
- update dependent files second
- record the change in the file index

---

## 5. Canonical Maintenance Rules

- No new critical file is added without an entry in `PROGRAMBUILD_FILE_INDEX.md`.
- No critical file is renamed without updating all references in the same change.
- No concern is split across multiple “source of truth” files unless one is explicitly marked derived.
- Derived summaries must point back to the canonical owner.
- Material architecture and policy changes should be recorded in `DECISION_LOG.md`, with enterprise work promoting major decisions into ADRs using `PROGRAMBUILD_ADR_TEMPLATE.md`.
- The template repository should keep project output files in reusable template form. Do not store filled, project-specific feasibility, requirements, architecture, or release documents here.

---

Last updated: 2026-03-27
