# PROGRAMSTART Learning Observation — Operational Path Readiness

Date: 2026-09-24
Source: Paths project
Disposition: **STRENGTHEN_EXISTING_OWNER**
Canonical owner: `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md`

## Candidate

Capability readiness requires proven operational paths when those paths are material to the claimed execution model.

## Evidence

The Paths work produced a concrete false-ready counterexample: VPS→Execution Node connectivity had existed and worked, and the relevant machines could be healthy/online, yet the intended unattended execution path encountered a fresh human identity step. Component health and historical connectivity therefore did not, by themselves, prove current unattended path readiness.

This observation is secret-safe and intentionally does not persist machine identifiers, credentials, tokens, or credential-bearing URLs.

## Existing-mechanism Challenge

PROGRAMSTART already had the necessary surrounding primitives:

- capability evidence and currentness/invalidation;
- identity/secret capability;
- effective-autonomy intersection;
- genuine human gate versus temporary automation gap;
- alternative actuation;
- recovery/verification requirements;
- owner routing and Authority-Gap reconciliation.

The missing activation was narrower: capability evidence did not explicitly require current evidence for the material actor→target operational paths on which the claimed execution model depends.

A new Path Authority, registry, readiness stage, controller, or mandatory path artifact is not earned.

## Counterexample Challenge

1. **Local CLI / no material operational dependency** — no path paperwork is introduced.
2. **Legitimate human authorization** — a path may be ready when the human authorization is explicit and intended for that operating model.
3. **Expiring credential + automatic rotation** — continuity, not immortal credentials, is the requirement.
4. **Low-risk prototype with one healthy path** — no fallback is required merely by this methodology rule.
5. **Path Authority duplication** — live inventory/state remains with Path Authority or the owning project.
6. **Component-green/path-broken** — unattended capability cannot be current when a material path introduces an unmodeled human identity step.
7. **Historical success invalidated by runtime/provider change** — normal currentness/invalidation semantics apply; age alone does not invalidate evidence.
8. **Capability versus authority** — a proven path never broadens project permission.
9. **Path explosion** — only paths whose failure can invalidate the current capability claim require evidence.
10. **Existing canonical coverage** — this strengthens Effective Autonomy instead of creating a parallel mechanism.

## Methodology delta

Effective Autonomy now states that when a capability materially depends on an operational path, component/end-point health alone is insufficient. Current accepted evidence must proportionally establish the path semantics needed by the intended operating model. Relevant properties may include reachability, authentication/authority, unattended-versus-human-gate behavior, lifecycle continuity, recovery/re-establishment, and machine-verifiable health.

Actual path inventory, role, live health, timestamps, invalidation, monitoring, and recovery procedures remain outside PROGRAMSTART methodology authority.

## ADR triage

No ADR is earned. This is a clarification/activation of existing Effective Autonomy acceptance semantics, not a new architectural authority boundary or irreversible architectural decision.

## Learning Gate

**Existing lesson strengthened / new ledger articulation earned as PSL-023, status implemented.**

A natural real retest remains required before validation.
