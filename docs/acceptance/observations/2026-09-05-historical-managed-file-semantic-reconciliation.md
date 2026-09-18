# Learning Observation — Historical Managed-File Semantic Reconciliation Candidate

**Date:** 2026-09-05  
**Source:** operator-authorized Conversation-to-Authority historical backfill, bounded to 2026-08-05 through the supplied export cutoff  
**Disposition:** **OBSERVE / PRESERVE — NO METHODOLOGY CHANGE**

## Recovered observation

A historical PROGRAMSTART discussion identified a possible autonomy improvement to downstream managed-file synchronization:

> Replace the coarse rule “modified managed file -> stop” with a bounded semantic reconciliation attempt that compares the prior PROGRAMSTART version, the downstream-modified version, and the new canonical version; automatically carry compatible non-conflicting downstream changes, and require a human/authority decision only when the same semantic concern has materially conflicting intent.

The discussion also preserved an important ownership boundary:

- canonical PROGRAMSTART changes remain methodology-owned;
- repository-specific changes remain downstream-project-owned;
- a downstream improvement that may be reusable becomes Learning-Gate evidence rather than being silently promoted into PROGRAMSTART.

## Current authority check

Current accepted sync authority remains `docs/decisions/0020-downstream-sync-mechanism-with-manifest-tracking.md`.

That decision already provides safe managed-set evolution, dry-run visibility, preserve rules, provenance verification, partial-sync honesty, and protection against destructive overwrite. For a newly managed or otherwise divergent existing path, however, current authority remains conservative: the divergence is treated as a conflict/preserve condition rather than as an automatically merged semantic three-way reconciliation.

Therefore the historical idea is **not already implemented**, but the historical conversation also does not provide sufficient real operational evidence to change the accepted sync contract now.

## Learning-Gate classification

- **Signal:** plausible reusable autonomy improvement.
- **Current evidence:** one recovered design discussion plus the confirmed existence of the conservative conflict boundary in current authority.
- **Missing evidence:** a real downstream synchronization case where current conflict handling causes material operator friction and a deterministic three-way semantic reconciliation can be shown to preserve both methodology and project-owned intent safely.
- **Current action:** preserve this observation only. Do not add a semantic merge engine, change `programstart sync`, or alter accepted decision 0020 from historical reasoning alone.

## Revisit trigger

Revisit through the normal PROGRAMSTART Learning Gate when a real adopted downstream repository presents a modified managed file and at least one of these is true:

1. current conflict/preserve behavior creates material avoidable operator intervention;
2. old-template + downstream + new-template evidence shows a clearly non-overlapping edit that could have been reconciled deterministically;
3. repeated managed-file divergence demonstrates the conservative stop/preserve rule is now a systemic autonomy bottleneck.

At that point, test the smallest possible three-way reconciliation primitive with explicit semantic/authority-conflict fail-closed behavior and rollback evidence. A successful local Git merge alone is not sufficient proof; repository-specific intent and methodology authority must remain distinct.

## Non-effects

This observation creates no roadmap item, priority, implementation permission, managed-file authority expansion, or downstream mutation. It does not supersede decision 0020 or advance a PROGRAMSTART lesson maturity state by itself.
