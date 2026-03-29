# PROGRAMBUILD_ADR_TEMPLATE.md

# Program Build ADR Template

Use this template when a project needs durable architecture or policy decision records beyond the running `DECISION_LOG.md`.

Status terms:
- proposed
- accepted
- superseded
- rejected

Naming convention:
- `ADR-001-short-title.md`
- keep ADRs append-only
- when a decision changes, create a new ADR and mark the prior one as superseded

Recommended threshold for a mostly solo workflow:
- keep routine decisions in `DECISION_LOG.md`
- write an ADR only when at least 2 of the following are true:
- the decision changes a core contract, auth rule, data policy, deployment model, or vendor dependency
- the decision affects 3 or more files or more than 1 stage of delivery
- undoing the decision would likely cost more than 1 focused workday
- the reason will probably need to be understood again later and a short log entry would be too thin

---

## Template

```text
# ADR-XXX: Title

Status: proposed | accepted | superseded | rejected
Date: YYYY-MM-DD
Deciders:
Consulted:
Informed:

## Context

What problem or constraint forced this decision?

## Decision

What was chosen?

## Consequences

What becomes easier, harder, riskier, or mandatory because of this choice?

## Alternatives Considered

- alternative
- alternative

## Follow-Up

- required action
- owner
```

---

Last updated: 2026-03-27
