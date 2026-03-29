# PROGRAMBUILD_FILE_INDEX.md

# Program Build File Index

This is the official index for critical Program Build files.
If a file is missing from this index, it is not a recognized control file in this system.

---

## 1. Control Files

| File | Type | Status | Purpose | Canonical for |
|---|---|---|---|---|
| `PROGRAMBUILD_CANONICAL.md` | control | active | authority map and naming rules | document authority |
| `PROGRAMBUILD_FILE_INDEX.md` | control | active | inventory of critical files | file inventory |
| `PROGRAMBUILD_ADR_TEMPLATE.md` | template | active | ADR format and status terms | ADR structure |
| `PROGRAMBUILD_CHANGELOG.md` | control | active | system-level change history | PROGRAMBUILD change history |
| `PROGRAMBUILD.md` | playbook | active | balanced default process | stage order and base workflow |
| `PROGRAMBUILD_LITE.md` | variant | active | lean workflow | lite execution model |
| `PROGRAMBUILD_PRODUCT.md` | variant | active | standard production workflow | product execution model |
| `PROGRAMBUILD_ENTERPRISE.md` | variant | active | enterprise workflow | enterprise execution model |
| `PROGRAMBUILD_KICKOFF_PACKET.md` | template | active | starter document pack | kickoff structure |
| `PROGRAMBUILD_SUBAGENTS.md` | catalog | active | subagent roles and prompts | subagent guidance |
| `PROGRAMBUILD_CHECKLIST.md` | checklist | active | execution checklist format | execution tracking |

---

## 2. Project Output Files

These output files are standard project artifacts. In the template repository they should remain clean templates. Filled project content belongs in the separate project repository created from this template.

| File | Type | Status | Purpose | Canonical for |
|---|---|---|---|---|
| `FEASIBILITY.md` | output | standard | go/no-go and kill criteria | project viability |
| `DECISION_LOG.md` | output | standard | material decisions, reversals, and rationale | project decision history |
| `RESEARCH_SUMMARY.md` | output | standard | market and technical research | research findings |
| `REQUIREMENTS.md` | output | standard | scope and requirements | product scope |
| `USER_FLOWS.md` | output | standard | primary workflows and state behavior | UX flow behavior |
| `ARCHITECTURE.md` | output | standard | contracts, topology, data model | technical architecture |
| `RISK_SPIKES.md` | output | standard | unknowns and proofs | technical risk resolution |
| `TEST_STRATEGY.md` | output | standard | test model and registry | quality model |
| `RELEASE_READINESS.md` | output | standard | launch gate and operational readiness | release readiness |
| `AUDIT_REPORT.md` | output | standard | drift and risk findings | audit findings |
| `POST_LAUNCH_REVIEW.md` | output | standard | launch outcomes, lessons, and follow-up actions | post-launch learning |

---

## 3. Index Rules

- Add new critical files here when they are created.
- Mark files as `active`, `deprecated`, `replaced`, or `derived`.
- If a file becomes derived, name its canonical owner in the Purpose column.
- Do not create synonyms for the same purpose.
- Use `DECISION_LOG.md` for ongoing project decisions and `PROGRAMBUILD_ADR_TEMPLATE.md` when a project needs durable ADR records.
- Do not treat filled project outputs in this template repository as canonical examples. Canonical project outputs live in the project repository that was bootstrapped from these templates.

---

Last updated: 2026-03-27
