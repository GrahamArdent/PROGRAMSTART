---
status: accepted
date: 2026-04-19
deciders: [solo operator]
consulted: []
informed: []
---

# 0022. Sync Pull Mode with --from-template

## Context and Problem Statement

`programstart sync --dest <path>` (Phase E) pushes changed PROGRAMSTART files from
the template to a downstream repo. However, if you are working inside a downstream
repo and want to pull the latest PROGRAMSTART tooling and prompts, you must navigate
back to the PROGRAMSTART repo and run the push command. There is no way to pull from
the downstream side.

## Decision Drivers

- Inverse of `sync --dest` — complete the bidirectional sync story.
- Share manifest format, preserve logic, and conflict resolution with existing `--dest` mode.
- Downstream repos should be able to pull without modifying the template.

## Considered Options

1. **`--from-template <path>` flag on existing `sync` command** — overrides the
   template root; `--dest` defaults to `.` (current directory).
2. **Separate `sync-pull` subcommand** — new command with its own entry point.
3. **Auto-detect mode** — infer push vs pull based on whether a manifest exists
   in the current directory.

## Decision Outcome

Chosen option: **1 — `--from-template <path>` flag on existing `sync` command**.

Rationale: Reuses all existing infrastructure (`_files_needing_sync`, preserve
logic, filter, dry-run/confirm). No new CLI command needed. The `sync()` function
gains an optional `template_root` parameter — when `None`, it defaults to
`workspace_path(".")` (push mode); when set, it uses the specified path (pull mode).

### Implementation

- `sync()` gains `template_root: Path | None = None` parameter.
- `main()` accepts `--from-template <path>` and makes `--dest` optional (defaults
  to current directory when `--from-template` is used).
- At least one of `--dest` or `--from-template` is required.
- All existing push-mode behavior is unchanged.

### Consequences

- Good: Bidirectional sync is complete — push with `--dest`, pull with `--from-template`.
- Good: Zero code duplication — both modes share the same `sync()` function.
- Good: `--from-template` + `--dest` can be combined for explicit two-path operation.
- Neutral: Pull mode still requires a `.programstart-manifest.json` in the target repo.

## Related

- <!-- DEC-019 -->
- DEC-019 in `PROGRAMBUILD/DECISION_LOG.md`
- ADR-0020 (downstream sync mechanism, push mode)
- Hardening gameplan J-6 (STR-03 / S-7)
- Upgrade gameplan Phase J, J-2
