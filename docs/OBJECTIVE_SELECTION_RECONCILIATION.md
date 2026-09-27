# Objective Selection Reconciliation

Status: **PROGRAMSTART candidate contract / Challenge-bounded**.

## Invariant

A durable root may remain valid without remaining currently selected for consequence production.

Before an awakened or reconsidered root produces a new consequence, the existing Controller/objective-convergence machinery must prove that the root is currently eligible for that consequence.

Root durability, authority validity, dependency satisfaction, and currentness are necessary but are not by themselves proof of foreground selection.

## Selection dispositions

The reconciliation surface must distinguish at least:

- **SELECTED** — currently eligible to produce the next consequence;
- **PARKED** — durable and resumable, but not currently eligible to produce a new consequence;
- **SUPERSEDED** — replaced by a later objective/selection decision;
- **AMBIGUOUS** — current evidence cannot safely determine consequence eligibility.

PARKED, SUPERSEDED, and AMBIGUOUS fail closed for new consequence dispatch. They do not destroy durable state.

## Parallelism

This contract does **not** require a global single foreground objective.

Multiple roots may be SELECTED when current authority and collision/resource evidence explicitly admit safe parallel consequences. Selection is therefore consequence-scoped eligibility, not a permanent global foreground-objective variable.

## Reconciliation triggers

Re-prove selection/eligibility before consequence dispatch when any of these occur:

- dependency or currentness evidence wakes a previously nonterminal root;
- wait/retry returns;
- owner handoff returns;
- reorientation/recovery resumes;
- restart/replay resumes durable state;
- operator intent selects or re-selects another root;
- evidence invalidation causes reconsideration.

## Fail-closed rule

If current selection evidence is absent, stale, conflicting, or ambiguous, do not dispatch the consequence. Reorient to current objective selection using existing PROGRAMSTART/Controller authority and ingress semantics. Do not infer selection merely from root age, durability, readiness, or recently repaired dependencies.

## Regression acceptance

Given:

1. Root A is valid and durably blocked;
2. the operator selects independent Root B;
3. Root A's dependency later clears;

acceptance requires:

- Root A remains durable;
- Root A does not produce a new consequence unless selection/eligibility currently admits it;
- Root B remains selected according to current evidence;
- no duplicate root is created merely to represent parking;
- no ChatGPT memory/state is required;
- no second scheduler/orchestrator/authority database is introduced;
- explicitly authorized safe parallel roots remain possible.

## Challenge result

The tempting alternative—a single mutable global foreground-objective identifier—is rejected at this stage because it would incorrectly serialize legitimate parallel work and risks becoming a second authority/control surface.

The smallest compatible change is a consequence-scoped eligibility proof integrated into existing objective continuation/reconsideration.

## Learning Gate

This contract is **candidate**, not yet validated. A real blocked-A / selected-B / A-wakes retest is required after implementation before promotion to validated.
