---
status: accepted
date: 2026-11-12
deciders: [solo operator]
consulted: []
informed: []
---

# 0028. Bound Dependency Reads Without Granting Foreign Mutations

<!-- DEC-025 -->

## Context and Problem Statement

The repository instructions and literal registry policy prohibit all foreign inspection until a repository is named separately. That conflicts with authorized cross-owner objectives that require bounded dependency contracts and evidence, and causes repeated generic permission requests.

## Decision Drivers

- Preserve canonical rule 15: dependency reasoning remains derived and task scoped.
- Allow only necessary reads under an actually authorized cross-owner objective.
- Keep exact repository, effect, target and native admission for foreign mutations.
- Scope a blocked consequence without stopping independent authorized work.

## Considered Options

- Retain the blanket inspection prohibition, repeating consent for necessary reads.
- Grant broad foreign-repository access, losing task and mutation boundaries.
- Distinguish admitted bounded reads from exact-authorized mutations in the existing policy and its dependent instructions.

## Decision Outcome

Choose the third option. Dependency reads require an authorized cross-owner objective, actual task relevance, admitted read route and recorded owner/source binding. Shared history/ownership, unrelated exploration and secret access do not qualify. Reads or relationships never grant foreign mutation permission. Existing native/provider/platform gates remain controlling for each consequence; reuse actual current authorization and continue independent authorized work while a mutation is blocked.

### Consequences

- A dependency contract can be read without asking again for generic approval.
- Foreign edit, stage, commit, push, merge or deployment still needs exact current authority and native admission.
- Registry phrase checks validate the documented rule; they do not intercept connected APIs or enforce runtime authorization.
- Original pending/UNKNOWN effects still require original-identity reconciliation before any affected retry.

## Confirmation

- Use the existing registry boundary validator with all required phrases intact.
- Exercise missing no-grant and missing bounded-read clauses in disposable text fixtures; the validator must reject them.
- Trace a real authorized dependency read and retain exact source binding.
- Review the read-then-foreign-push counterexample; no permission may transfer from the read.

## Links

- [DEC-025](../../PROGRAMBUILD/DECISION_LOG.md)
- [Canonical rule 15](../../PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md)
- [Source-of-truth protocol](../../.github/instructions/source-of-truth.instructions.md)
