---
status: accepted
date: 2026-04-18
deciders: [Solo operator]
consulted: []
informed: []
---

# 0020. Downstream Sync Mechanism with Manifest Tracking

## Context and Problem Statement

When PROGRAMSTART attaches its PROGRAMBUILD workflow to a downstream consumer repo, it copies ~100+ bootstrap files. After attachment, if PROGRAMSTART's tooling evolves (scripts, configs, tests, prompts), the downstream repo has no mechanism to pull those updates. The operator must manually identify and copy changed files — a process that scales poorly as more repos adopt PROGRAMSTART.

## Decision Drivers

- Downstream repos need a low-friction way to receive PROGRAMSTART tooling updates
- Accidental overwrites of downstream customizations (README, .gitignore) must be prevented
- The sync mechanism must be auditable — operators need to see what will change before applying
- Future bidirectional sync (J-6: `sync --from-template`) should share manifest format

## Considered Options

- Option A — Full re-attach with `--force` (destructive, loses downstream customizations)
- Option B — Manifest-tracked sync with dry-run default and `--confirm` for writes
- Option C — Git-based subtree or submodule approach (complex, fragile with Windows paths)

## Decision Outcome

Chosen option: **Option B**, because it provides the minimum viable sync with safety-by-default (dry-run), preserves downstream customizations via the preserve list, and the manifest format is extensible for future bidirectional sync.

### Consequences

- Good: Operators can propagate template changes with a single command
- Good: Dry-run default prevents accidental overwrites
- Good: Manifest written at attach time provides a complete audit trail
- Good: `.programstart-preserve` file lets downstream repos declare additional protected files
- Bad: Manifest must be regenerated if attach predates manifest support (re-attach with `--force`)
- Neutral: Files removed from template are flagged but not auto-deleted in downstream

## Confirmation

- `programstart sync --dest <path>` shows diff summary without `--confirm`
- `programstart sync --dest <path> --confirm` copies changed files
- `programstart validate --check bootstrap-assets` verifies the new files are registered
- 16 tests cover: no-op sync, changed files, dry-run, confirm, preserve list, custom preserve, file filter, missing manifest, removed-from-template, and CLI entry points

## Links

- <!-- DEC-017 -->
- [Decision log](../../PROGRAMBUILD/DECISION_LOG.md)
- Upgrade gameplan Phase E (OP-02): `devlog/gameplans/upgradegameplan.md`
