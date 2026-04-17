# Decision Records

This directory contains Markdown Architectural Decision Records (MADRs) for the PROGRAMSTART system.

MADRs are used for significant decisions that affect core contracts, workflow rules, data policies, or multi-stage behavior. Routine per-project decisions live in `DECISION_LOG.md`.

Legacy pre-register ADRs: `0001`-`0003` predate the current `DECISION_LOG.md` linkage regime. They are historically valid architecture records, are intentionally exempt from the `<!-- DEC-xxx -->` linkage comment requirement, and are classified in `config/process-registry.json` under `adr_policy.legacy_pre_register_adrs`.

## Index

| ID | Title | Status | Date |
|---|---|---|---|
| [0001](0001-use-programbuild-workflow-system.md) | Use PROGRAMBUILD Workflow System as Repository Scaffold | accepted | 2026-03-27 |
| [0002](0002-adopt-conventional-commits.md) | Adopt Conventional Commits for All Commit Messages | accepted | 2026-03-31 |
| [0003](0003-adopt-madr-for-architecture-decisions.md) | Adopt MADR 4.0 for Architecture Decision Records | accepted | 2026-03-31 |
| [0004](0004-root-workspace-smoke-readonly.md) | Root-Workspace Smoke Must Be Read-Only | accepted | 2026-04-11 |
| [0005](0005-cap-signoff-history-at-100-entries.md) | Cap Signoff History at 100 Entries | accepted | 2026-04-11 |
| [0006](0006-accept-sys-argv-mutation-pattern.md) | Accept sys.argv Mutation Pattern | accepted | 2026-04-12 |
| [0007](0007-clarify-canonical-rule-1-temporal-semantics.md) | Clarify CANONICAL Rule 1 Temporal Semantics | accepted | 2026-04-12 |
| [0008](0008-cross-cutting-prompts-registry.md) | Cross-cutting prompts registered at workflow_guidance level | superseded by ADR-0011 | 2026-04-12 |
| [0009](0009-canonical-section-alignment.md) | Canonical section alignment in shaping prompts | accepted | 2026-04-13 |
| [0010](0010-unified-cli-kb-diff-rollback.md) | Unified CLI aliases for knowledge-base and state recovery workflows | accepted | 2026-04-14 |
| [0011](0011-separate-workflow-and-operator-prompt-architecture.md) | Separate workflow and operator prompt architecture | accepted | 2026-04-15 |
| [0012](0012-require-hardening-adr-triage-and-audit-loop.md) | Require ADR triage and targeted audit loop for structural hardening checkpoints | superseded by ADR-0013 | 2026-04-15 |
| [0013](0013-require-governance-close-out-for-durable-operator-checkpoints.md) | Require governance close-out loop for durable operator checkpoints | accepted | 2026-04-15 |
| [0014](0014-compose-process-registry-from-manifest-and-fragments.md) | Compose process registry from a manifest and fragments | accepted | 2026-04-15 |
| [0015](0015-reuse-external-agent-systems-by-pattern-not-wholesale.md) | Reuse external agent systems by pattern, not wholesale | accepted | 2026-04-16 |
| [0016](0016-require-execution-prompt-for-operator-gameplans.md) | Require execution prompt for operator gameplans | accepted | 2026-04-16 |
| [0017](0017-jit-check-cli-command.md) | JIT Check CLI Command | accepted | 2026-04-17 |
| [0018](0018-workflow-deferral-mechanism.md) | Workflow Deferral Mechanism | accepted | 2026-04-17 |
| [0019](0019-typed-pydantic-models-for-process-registry.md) | Typed Pydantic Models for Process Registry | accepted | 2026-04-18 |
| [0020](0020-downstream-sync-mechanism-with-manifest-tracking.md) | Downstream Sync Mechanism with Manifest Tracking | accepted | 2026-04-18 |
| [0021](0021-prompt-builder-mode-b-context-driven-generation.md) | Prompt Builder Mode B — Context-Driven Generation | accepted | 2026-04-19 |
| [0022](0022-sync-pull-mode-with-from-template.md) | Sync Pull Mode with --from-template | accepted | 2026-04-19 |

## Rules

- ADRs are append-only. To supersede a decision, create a new ADR with an incremented number and update the old record's `status` to `superseded by ADR-NNNN`.
- Use `PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md` as the template for new records.
- Update this index whenever a new ADR is added.
- Keep this index synchronized with each ADR file's frontmatter for `status`, `date`, and title.
- When an ADR is superseded, update any `PROGRAMBUILD/DECISION_LOG.md` row that still points at the superseded ADR so active decisions do not reference stale architecture records.
