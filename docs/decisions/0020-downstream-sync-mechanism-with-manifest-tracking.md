---
status: accepted
date: 2026-04-18
deciders: [Solo operator]
consulted: []
informed: []
---

# 0020. Downstream Sync Mechanism with Manifest Tracking

## Context and Problem Statement

When PROGRAMSTART attaches or adopts its PROGRAMBUILD workflow in a downstream consumer repo, it copies managed control/support files. After attachment, if PROGRAMSTART's tooling or reusable methodology evolves, the downstream repo needs a safe way to receive those updates without re-adopting destructively or hand-maintaining a growing file list.

The original sync implementation correctly used a manifest to bound writes, but an `existing_project_adoption` manifest froze its `files` list at adoption time and never advanced `source_commit`. That meant a downstream repo could sync every file it already knew about while still missing newly managed support protocols and could not truthfully prove which PROGRAMSTART commit its adopted overlay matched.

## Decision Drivers

- Downstream repos need a low-friction way to receive PROGRAMSTART tooling/methodology updates.
- Accidental overwrites of downstream customizations (README, .gitignore, explicit preserve paths) must be prevented.
- The sync mechanism must be auditable: operators/workers need to see what will change before applying it.
- Existing-project adoption must be able to discover newly managed PROGRAMBUILD controls and generated-repo prompt/support files without destructive re-adoption.
- A source commit pin must advance only when a complete sync can truthfully claim the managed adoption surface matches that template commit.
- Historical manifest entries must not disappear merely because a template file was removed.

## Considered Options

- Option A — Full re-attach/re-adopt with force (destructive or incompatible with an already adopted existing repo).
- Option B — Keep the manifest file list permanently frozen and require manual edits for every new managed asset (safe but does not scale and makes the source pin stale).
- Option C — Additively evolve existing-project adoption manifests from the current registry during full sync, while retaining dry-run/preserve/removal safeguards.
- Option D — Replace manifest tracking with Git subtree/submodule inheritance (complex and inappropriate for project-owned repository boundaries).

## Decision Outcome

Chosen option: **Option C**.

For `mode: existing_project_adoption`, an unfiltered sync derives the current managed adoption set from:

1. PROGRAMBUILD control files declared by the current template registry, excluding the project state file; and
2. generated-repo workflow prompt/support assets selected by current registry policy.

The effective sync set is the **union** of that current managed set and historical manifest entries. This is intentionally additive: previously managed paths remain visible so a file removed from the template is reported rather than silently forgotten or deleted.

Legacy/non-adoption manifests retain their recorded file set until a separately justified migration exists.

### Source-pin rule

For a full confirmed `existing_project_adoption` sync:

- copy changed/newly managed files subject to the existing preserve policy;
- if no historical managed path is `removed-from-template`, update the manifest's additive file list;
- when the template Git HEAD can be resolved, advance `source_commit` to that exact commit only after the full managed sync completes;
- if a managed file was removed from the template, hold the manifest/source pin rather than claiming complete alignment;
- if template Git HEAD cannot be resolved, do not invent a source commit.

A filtered sync (`--files`) intentionally **does not evolve the managed file set or source pin**, because it cannot prove that all managed files match one template commit.

Dry-run remains the default and may report newly managed files and a prospective pin change without mutating the destination.

### Consequences

- Good: Existing adopted projects can receive newly added managed protocols without destructive re-adoption.
- Good: Exact PROGRAMSTART pinning remains meaningful instead of becoming a stale decoration.
- Good: New managed files are registry-driven rather than hand-added independently to every downstream manifest.
- Good: Historical removals remain explicit and block a false alignment claim.
- Good: Preserve rules and project-owned files remain protected.
- Neutral: Legacy attachment manifests remain frozen to preserve backward compatibility until separately evaluated.
- Neutral: The adoption registry must correctly classify reusable support protocols that downstream projects need; registry omissions remain a validation concern.

## Confirmation

- `programstart sync --dest <path>` shows current-file differences, newly managed adoption files, and any prospective source-pin transition without `--confirm`.
- `programstart sync --dest <path> --confirm` copies the full managed adoption surface and updates the adoption manifest only when safe.
- `programstart sync ... --files <glob>` may update the selected files but does not claim whole-template alignment.
- Existing preserve rules remain active.
- Removed template paths are reported and never auto-deleted; for adopted repos they hold source-pin advancement.
- Regression tests cover additive managed-file discovery, state-file exclusion, dry-run behavior, filtered-sync pin protection, legacy-manifest compatibility, and removed-file pin holding.

## Links

- <!-- DEC-017 -->
- [Decision log](../../PROGRAMBUILD/DECISION_LOG.md)
- ADR-0022 (`--from-template` pull mode)
- Upgrade gameplan Phase E (OP-02): `devlog/gameplans/upgradegameplan.md`
