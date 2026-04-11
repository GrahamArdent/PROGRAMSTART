# PROGRAMBUILD_ENTERPRISE.md

# Program Build Enterprise

Use this version for regulated, multi-team, or high-consequence systems where auditability, governance, and operational control are mandatory.

Authority:
- `PROGRAMBUILD_CANONICAL.md` defines source-of-truth rules
- `PROGRAMBUILD_FILE_INDEX.md` is the lookup table for critical files
- `PROGRAMBUILD_IDEA_INTAKE.md` runs before Stage 0 — challenge the idea before filling the inputs block
- `PROGRAMBUILD_CHALLENGE_GATE.md` runs at every stage transition — all 7 parts required at all stages; approver sign-off required on each gate log entry
- `PROGRAMBUILD_GAMEPLAN.md` defines the execution order with full cross-stage validation and retained evidence

---

## When To Use

Use this file when:
- the system handles regulated, financial, legal, medical, or highly sensitive data
- multiple teams or vendors share ownership
- formal approvals are required
- outages, leakage, or drift would have material business or compliance impact

This variant applies equally to end-user products, internal control planes, service platforms, and fully automated systems when the consequence of failure is high.

---

## Enterprise Expectations

- documented ownership for every service and data domain
- formal sign-off gates between stages
- threat model and security review before implementation
- change management through ADRs or equivalent records using `PROGRAMBUILD_ADR_TEMPLATE.md`
- release readiness with support, rollback, monitoring, and incident path defined
- evidence retained for audits
- critical planning files follow the `PROGRAMBUILD_*.md` naming convention

If the product is non-interactive, replace journey-centric assumptions with operator, service-identity, scheduler, and downstream-consumer controls.

---

## Required Stages

| Stage | Output | Additional enterprise requirement |
|---|---|---|
| Feasibility | `FEASIBILITY.md` | sponsor sign-off |
| Research | `RESEARCH_SUMMARY.md` | compliance review included |
| Requirements and UX | `REQUIREMENTS.md`, `USER_FLOWS.md` | traceability to controls |
| Architecture and risk spikes | `ARCHITECTURE.md`, `RISK_SPIKES.md` | threat model and data classification |
| Scaffold and guardrails | repo skeleton and CI | policy-as-code where possible |
| Test strategy | `TEST_STRATEGY.md` | release-blocking control mapping |
| Implementation loop | feature code | evidence and approvals captured |
| Release readiness | `RELEASE_READINESS.md` | operational go/no-go board |
| Audit and drift control | `AUDIT_REPORT.md` | remediation owners and due dates |
| Post-launch review | `POST_LAUNCH_REVIEW.md` | residual risk review and lessons assigned |

---

## Required Enterprise Additions

- data classification matrix
- tenancy and access-control model
- secret rotation and key management plan
- audit logging requirements
- dependency and vulnerability governance
- backup and restore validation
- disaster recovery objectives
- incident response ownership
- vendor and third-party integration review
- retention and deletion policy mapping
- RACI or equivalent responsibility model
- explicit residual-risk acceptance log

---

## Suggested Subagents

See `PROGRAMBUILD_SUBAGENTS.md` for full prompts and workspace agent files.

| Agent | Use for | Output |
|---|---|---|
| Discovery & Scoping | domain research, scope, control traceability, standards review | research + requirements + compliance notes |
| Architecture & Security | system boundaries, API contracts, data classification, threat model | architecture review + security report |
| Quality & Release | control-to-test mapping, release readiness, DR and rollback validation | test strategy + readiness report |
| Risk Spike Agent | proofs for risky integrations or operational assumptions | spike evidence |
| Contract Auditor | route, schema, auth, and ownership drift review with owner and due dates | audit report |

---

## Enterprise Prompt Pattern

```text
Create an enterprise-grade delivery playbook for this application.

Inputs:
- project inputs block

First identify whether the dominant execution mode is end-user interaction, operator workflow, service contract, or background automation. Keep the governance level high either way.

Produce:
1. feasibility with sponsor-level kill criteria
2. research with compliance and standards review
3. requirements with control traceability
4. architecture with threat model, data classification, and risk spikes
5. scaffold with policy and structural guardrails
6. test strategy that maps controls to tests and release gates
7. implementation loop with evidence capture
8. release readiness with rollback, incident, backup, and DR planning
9. drift audit with owners, dates, and residual risk acceptance
10. post-launch review with outcomes, reversals, and follow-up owners
```

---

## Enterprise Definition Of Done

- design decisions are recorded and approved
- security and compliance controls are mapped to implementation and tests
- release readiness has an owner for deployment, rollback, monitoring, support, and automated recovery where applicable
- evidence exists for the critical gates
- unresolved risks are explicitly accepted by the correct owner
- post-launch review confirms actual outcomes and any decision reversals

---

Last updated: 2026-03-31
