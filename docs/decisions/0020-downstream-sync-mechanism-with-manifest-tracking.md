---
status: accepted
date: 2026-04-18
deciders: [Solo operator]
consulted: []
informed: []
---

# 0020. Downstream Sync Mechanism with Manifest Tracking

## Context and Problem Statement

When PROGRAMSTART attaches or adopts PROGRAMBUILD into a downstream consumer repo, it copies a bounded set of reusable controls/assets. After attachment, PROGRAMSTART itself continues to evolve. Downstream repositories need a safe way to receive managed methodology/tooling updates without destructive re-attach or accidental overwrite of project-owned files.

A real LinkedIn Generator retest on 2026-09-01 exposed an important evolution of the original design: a manifest whose `files` list is frozen at attach time cannot discover a file that becomes a managed reusable asset later. Attach-time membership is therefore useful evidence of the previous reconciliation, but it cannot be permanent authority over future managed membership for a lean managed overlay.

## Decision Drivers

- Downstream repos need a low-friction way to receive PROGRAMSTART tooling/methodology updates.
- Accidental overwrites of downstream customizations must be prevented.
- Sync must be auditable; operators/runtimes need to see what will change before applying it.
- Existing lean adopted repositories must be able to discover newly managed reusable assets without destructive re-attach.
- Files that leave the managed set must not be silently deleted from a project.
- Partial/filtered sync must not falsely claim full PROGRAMSTART provenance/currentness.
- Project strategy, architecture, implementation, optional project artifacts, and mutable workflow state remain project-owned.

## Considered Options

- Option A — Full re-attach with `--force` (destructive and unnecessarily broad).
- Option B — Manifest-tracked sync with dry-run default and `--confirm` for writes, with managed-set evolution for lean overlays.
- Option C — Git subtree/submodule distribution (greater coupling/operational complexity).
- Option D — Freeze attach-time manifest membership forever (safe against expansion but fails to distribute later managed controls).

## Decision Outcome

Chosen option: **Option B**.

For legacy/full manifests, retain fixed-manifest behavior unless a separate migration is explicitly earned.

For lean managed overlays such as `existing_project_adoption` and external PROGRAMSTART control-plane links:

1. derive the current managed reusable set from the current PROGRAMSTART registry and attachment mode;
2. exclude mutable project workflow state from the reusable control copy set;
3. compare current managed membership with the last reconciled downstream manifest;
4. newly managed files may be created when absent, but a different existing downstream file at the same path is a conflict and must not be overwritten automatically;
5. files retired from the managed set remain in the project and are removed only from managed membership, not from disk;
6. refresh the downstream derived process registry from current methodology while preserving explicitly project-owned identity/description fields;
7. after a successful unfiltered reconciliation, refresh manifest membership, source commit/provenance, sync timestamp, and derived-file metadata;
8. a filtered/partial sync may change the requested files but must not advance full managed-set/provenance state;
9. sync remains a safe reconciliation primitive, not permission to strategically replan the target repository.

## Consequences

- Good: Existing lean adopted repos can discover newly managed PROGRAMSTART controls/support assets.
- Good: Attach-time manifests become a record of the last safe reconciliation instead of a permanent stale membership definition.
- Good: Conflicting project-owned paths stop rather than being silently seized by PROGRAMSTART.
- Good: Retired managed files are preserved, reducing destructive behavior.
- Good: Derived target control metadata can advance with current methodology.
- Good: Partial sync can no longer masquerade as full currentness.
- Neutral: `programstart sync` is still an invocation primitive; automatic portfolio fan-out requires a separate trusted scheduler/controller/maintenance runtime and project-scoped authority.
- Neutral: Optional artifacts such as project-specific `IDEA_LEDGER.md` are not automatically made managed merely because PROGRAMSTART provides a reusable template.
- Bad: Reconciliation logic is more mode-aware than the original fixed-list implementation and therefore requires explicit regression coverage.

## Confirmation

Expected checks now include:

- dry-run reports changed, missing, newly managed, retired, registry, and provenance deltas;
- `--confirm` copies changed/missing/newly managed safe files;
- newly managed path conflicts are not overwritten or claimed;
- retired managed files remain on disk but leave refreshed manifest membership;
- lean-overlay derived registry/provenance refreshes only after a successful unfiltered sync;
- filtered sync does not advance full provenance;
- legacy manifests retain their previous fixed-file behavior;
- a real already-adopted repository (LinkedIn Generator) is used as the downstream retest before this evolution is considered validated.

## Links

- <!-- DEC-017 -->
- [Decision log](../../PROGRAMBUILD/DECISION_LOG.md)
- Upgrade gameplan Phase E (OP-02): `devlog/gameplans/upgradegameplan.md`
- `docs/acceptance/observations/2026-09-01-downstream-methodology-distribution-miss.md`
