# PROGRAMSTART Consequence Execution Contract V1

Status: **PROGRAMSTART reusable semantic/acceptance contract; not runtime authority, credential authority, path authority, or a new execution spine.**

## Objective

Allow the ecosystem to adopt existing and future machine capabilities without bespoke authorization plumbing per effect while preserving owner authority, least-consequence execution, currentness, collision safety, credential custody, bounded actuation, durable evidence, and recovery.

## Core invariant

A provider capability proves only that a principal can technically satisfy provider/resource/permission requirements. It never grants semantic permission. A consequential machine effect may execute only when current owner authority is compiled by Controller into an exact typed consequence grant, current mutation coordination admits its write set, Paths resolves a current realization, the identity owner satisfies the grant's provider requirements without exporting secrets, and a bounded adapter enforces the exact operation grammar.

## Typed consequence grant

The canonical grant must bind, at minimum:

- grant schema/version and deterministic grant identity;
- owning authority reference and authority version/currentness;
- consequence class and typed effect identity;
- provider/target and exact resource scope;
- operation plus bounded operation constraints;
- required provider capabilities/permissions, expressed independently from semantic permission;
- declared consequential write set and Controller mutation/fencing admission reference when mutating;
- selected Paths realization/composition evidence and invalidation conditions;
- non-secret identity/capability satisfaction reference;
- exact preconditions/currentness checks immediately before consequence;
- expected postcondition/evidence contract;
- replay/idempotency/unknown-outcome reconciliation semantics;
- terminal/invalidation conditions and result provenance.

Missing, stale, contradictory, or widened fields fail closed for consequential execution.

## Owner boundaries

- **Owning project/repository/provider policy** owns substantive permission and accepted consequence scope.
- **PROGRAMSTART** owns reusable consequence semantics, Challenge/Learning, compilation requirements, and parity/acceptance obligations. It does not issue live grants.
- **Controller** owns live compilation/admission of the exact grant, current owner-authority binding, mutation claims/fencing, effect reservation, replay/reconciliation, and continuation.
- **Paths / Path Authority** owns discovery of realizations/compositions, availability/currentness/failure-domain evidence, and recovery knowledge. Paths never grants semantic permission.
- **Secrets / identity owner** owns credential custody and proves whether a current identity can satisfy the grant's provider/resource/permission requirements. Provider permission is an upper technical bound, not semantic authority.
- **Compute / typed execution adapters** enforce the admitted operation grammar and return bounded evidence. They do not reinterpret project permission.
- **Matrix** is the omission-resistant parity/completeness oracle and read projection. It neither issues grants nor admits runtime mutation.

## Mandatory sequence

1. Resolve current owner authority and exact consequence class.
2. Compile an exact typed consequence grant; do not infer permission from capability existence.
3. For mutation, acquire current Controller coordination admission for the grant's declared write set.
4. Resolve a current Paths realization/composition for the exact effect/target and retain durable discovery evidence.
5. Resolve identity/provider capability satisfaction without exposing or relabeling credentials into broader semantic authority.
6. Revalidate authority, resource, target, selected realization, identity satisfaction, and exact operation preconditions immediately before dispatch.
7. Dispatch only through an adapter whose grammar is no broader than the grant.
8. Persist provider/runtime result evidence bound to grant/effect identity.
9. On ambiguous mutation outcome, reconcile observed state before retry; never blind-retry a possibly completed consequence.
10. Reconcile terminal evidence into Controller continuation and parity/acceptance evidence without making Matrix or evidence records authoritative.

## Capability reuse rule

One provider identity may satisfy multiple independently authorized grants when its provider/resource/permission envelope is sufficient. Reuse does not merge semantic authority between effects. Do not create a new credential architecture merely because a new typed effect is introduced; create or widen provider identity only when the existing identity cannot safely satisfy the required provider envelope.

## General mechanism versus instance acceptance

A proven generic grant/identity/adapter mechanism never implies acceptance of a concrete consequence instance. Each material consequence still requires current owner authority, instance-specific currentness, coordination where mutating, a current realization, identity satisfaction, bounded dispatch, and result evidence.

## Fail-closed boundaries

Reject execution when any of the following is true:

- provider permission is being used as project permission;
- the grant omits or widens owner authority, consequence class, effect, target/resource, operation constraints, or write set;
- Paths evidence is stale/absent for a consequential realization decision;
- identity satisfaction would require secret export or an unapproved provider-scope expansion;
- mutation ownership is absent, stale, or conflicting;
- adapter grammar is broader than the grant;
- exact preconditions/currentness cannot be verified;
- prior mutation outcome is ambiguous and has not been reconciled;
- evidence cannot bind the observed result to the exact grant/effect.

## Acceptance families

The reusable contract is not ecosystem-proven until materially different instances demonstrate it without special-purpose authority plumbing:

1. GitHub repository creation.
2. Exact protected PR integration.
3. GitHub issue/repository-reversible mutation.
4. A non-GitHub provider mutation.
5. A local/runtime machine mutation.

Each family requires its own instance evidence. At least one adversarial case per family must prove that technical capability without semantic authority is rejected.

## Matrix relationship

`config/autonomy-parity-contract.json` is the machine-readable completeness/acceptance oracle and `docs/AUTONOMY_PARITY_MATRIX.md` is its generated view. Consequence Execution V1 must be represented there before ecosystem-wide implementation claims are made. Matrix coverage does not itself enforce runtime execution; Controller admission and owner-native boundaries do.

## Cold-start durability criterion

A fresh worker using current PROGRAMSTART + targeted Matrix selection + Paths + owner-native sources must be able to reconstruct: objective -> consequence contract -> behavior/acceptance obligations -> implementation owners -> current parity -> missing typed edges -> current mutation owner -> next executable step, without relying on originating chat history.
