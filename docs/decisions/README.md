# Decision Records

This directory contains Markdown Architectural Decision Records (MADRs) for the PROGRAMSTART system.

MADRs are used for significant decisions that affect core contracts, workflow rules, data policies, or multi-stage behavior. Routine per-project decisions live in `DECISION_LOG.md`.

## Index

| ID | Title | Status | Date |
|---|---|---|---|
| [0001](0001-use-programbuild-workflow-system.md) | Use PROGRAMBUILD workflow system as repo scaffold | accepted | 2026-03-27 |
| [0002](0002-adopt-conventional-commits.md) | Adopt Conventional Commits for all commit messages | accepted | 2026-03-31 |
| [0003](0003-adopt-madr-for-architecture-decisions.md) | Adopt MADR 4.0 for architecture decision records | accepted | 2026-03-31 |
| [0004](0004-root-workspace-smoke-readonly.md) | Root-workspace smoke must be read-only | accepted | 2026-04-11 |
| [0005](0005-cap-signoff-history-at-100-entries.md) | Cap signoff history at 100 entries | accepted | 2026-04-11 |
| [0006](0006-accept-sys-argv-mutation-pattern.md) | Accept sys.argv mutation pattern | accepted | 2026-04-12 |
| [0007](0007-clarify-canonical-rule-1-temporal-semantics.md) | Clarify CANONICAL rule 1 temporal semantics | accepted | 2026-04-12 |

## Rules

- ADRs are append-only. To supersede a decision, create a new ADR with an incremented number and update the old record's `status` to `superseded by ADR-NNNN`.
- Use `PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md` as the template for new records.
- Update this index whenever a new ADR is added.
