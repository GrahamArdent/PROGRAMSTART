# Downstream Methodology Distribution Miss — LinkedIn Generator

Date: 2026-09-01  
Project evidence source: `GrahamArdent/LinkedIn_Generator`  
PROGRAMSTART owner surface: adoption/sync + external target control  
Learning classification: systemic / strengthens `PSL-012`; also exercises the operator-relay failure mode described by `PSL-019`

## Observation

During a Mode-C reevaluation of LinkedIn Generator, current PROGRAMSTART methodology contained newer idea-preservation, learning-architecture, and managed support/control changes that were not represented by the repository's adopted PROGRAMSTART overlay.

Live evidence showed:

- LinkedIn Generator `main` was current for its own product work, but `.programstart-manifest.json` still identified PROGRAMSTART source commit `f74d51f40a54b5d13482faff4ff577ea1c097eb2` from the original 2026-08-25 adoption.
- The manifest stored a fixed `files` list created at adoption time.
- Current PROGRAMSTART `main` was `4ece1af3bc6afff9834e551bc9f4e2d8e791b317`.
- `scripts/programstart_sync.py` used only `manifest["files"]` to decide what could be synchronized.
- Therefore a file that became a managed reusable control/support asset after the downstream repo was adopted was invisible to that existing manifest. The sync command could update an already-known file but could not discover a newly managed file.
- `programstart sync` itself is an explicitly invoked dry-run/`--confirm` mechanism. No repository evidence inspected in this retest showed an automatic fan-out runtime that reacts to every PROGRAMSTART methodology change and invokes safe reconciliation across all adopted repositories.
- LinkedIn Generator's local `config/process-registry.json` was also an adoption-era derived registry. The external target control plane uses the target's local registry through `PROGRAMSTART_ROOT`, so stale derived control metadata can remain relevant even when the central PROGRAMSTART scripts are newer.
- A prior LinkedIn Generator PR (#19) manually/ selectively synchronized selected methodology files to a then-current PROGRAMSTART commit, but that did not refresh the adoption manifest's managed membership/provenance. The repository could therefore appear partially synchronized while its durable distribution metadata remained stale.

## Important Non-Defect

`PROGRAMBUILD/IDEA_LEDGER.md` is intentionally an optional preservation template and is deliberately not a mandatory generated-project output. Its absence from LinkedIn Generator was not itself a downstream distribution failure.

LinkedIn Generator now chooses to maintain its own project-specific `IDEA_LEDGER.md` because the operator explicitly requested durable idea preservation. That is project adoption, not a reason for PROGRAMSTART to force the ledger into every repository.

## Root Cause

The original manifest design treated attach-time file membership as both:

1. an audit record of what PROGRAMSTART copied at adoption time; and
2. the future authoritative membership set for sync.

Those are not equivalent once the reusable methodology evolves.

For lean managed overlays, the current template/registry owns the current managed reusable set. The downstream manifest should describe the **last safely reconciled managed set and provenance**, not permanently freeze adoption-time membership.

A second, separate gap remains at the runtime level: even a correct sync primitive does not create automatic downstream distribution unless a trusted scheduler/controller/maintenance plane actually detects the PROGRAMSTART change, enumerates affected repositories, and invokes project-scoped reconciliation under repository authority.

## Bounded Correction

The proposed correction on branch `fix/downstream-sync-manifest-evolution` changes only lean managed overlay modes (`existing_project_adoption` and external-control-plane links):

- derive the current PROGRAMBUILD controls (excluding mutable workflow state) and current managed prompt/support assets from the current template registry;
- compare that current managed set with the downstream manifest;
- discover newly managed assets that did not exist in the old manifest;
- copy a newly managed path only when it is absent; if a different project-owned file already exists at that path, stop with a conflict instead of seizing ownership;
- preserve files retired from the current managed set instead of deleting them;
- refresh the derived downstream `config/process-registry.json` while preserving project identity/description metadata;
- refresh manifest `files`, `source_commit`, `last_synced_at`, and derived-registry provenance after a successful unfiltered sync;
- do not claim full provenance refresh after a filtered/partial sync;
- retain legacy fixed-manifest semantics for manifests outside the lean managed-overlay modes.

## Why This Strengthens PSL-012

`PSL-012` previously observed that selective PROGRAMSTART methodology propagation can update managed controls without becoming a strategic replan. LinkedIn PR #19 supported that claim, but this later retest exposed an incomplete assumption: selective propagation is not reliable if the downstream managed-set definition itself cannot evolve.

The strengthened lesson is:

> **Managed overlay sync for an existing adopted repository must derive current reusable membership from the current attachment-mode authority, safely reconcile newly managed/retired paths, and refresh provenance. Attach-time manifest membership is evidence of the previous reconciliation, not permanent authority over future managed membership.**

This remains distinct from project strategy: syncing reusable controls does not authorize PROGRAMSTART to rewrite a project's architecture, sequencing, implementation, or optional project artifacts.

## Relationship To PSL-019

The operator expected this kind of reusable methodology maintenance not to require manual rediscovery/relay. The fact that the mismatch surfaced only because a project conversation explicitly compared live PROGRAMSTART against LinkedIn Generator is evidence that the **invocation/fan-out layer remains incomplete** even after the sync primitive is corrected.

This does not mean every PROGRAMSTART commit should be blindly pushed into every project. The external maintenance rules still require project-scoped impact classification, separate PR/evidence boundaries, and stronger gates where a change is not deterministic reusable maintenance.

## Named Real Retest

After the sync fix is merged, use the already-adopted `GrahamArdent/LinkedIn_Generator` repository as the real retest:

1. start from its old adoption manifest rather than destructive re-attach;
2. run/replicate a full lean-overlay sync against current PROGRAMSTART;
3. prove newly managed current controls/support assets are discovered;
4. prove a conflicting project-owned path is not overwritten;
5. prove retired managed paths are preserved rather than deleted;
6. prove the downstream derived registry is refreshed without changing project-owned identity/description;
7. prove manifest managed membership/provenance advances to the reconciled PROGRAMSTART source;
8. prove optional/project-specific `IDEA_LEDGER.md` is not forced into the managed set;
9. then separately test the runtime/Program Store expectation: a future new managed asset should trigger project-scoped reconciliation without the operator having to notice and relay the update manually.

Until both the sync primitive and an authorized invocation path pass real retest, do not claim automatic downstream PROGRAMSTART distribution is solved.
