# PROGRAMSTART Learning Observation — JIT Context / Objective-Level Convergence

Date: 2026-09-24
Source: Paths project execution/recovery work
Classification: reusable methodology gap; smallest-owner strengthening
Candidate lesson: objective-level convergence should govern just-in-time context loading and discovery handling.

## Observation

The Paths work reinforced an existing PROGRAMSTART strength and exposed one missing explicit connection.

PROGRAMSTART already required:

- one strategic execution spine;
- bounded Work Packets;
- progressive / just-in-time context loading;
- evidence reuse and invalidation;
- narrow blocker classification and safe-lane continuation;
- research only for decision-relevant uncertainty.

Those controls limited context and ceremony, but the canonical operating model did not explicitly bind them to a packet-level terminal condition. In long dependency chains, that leaves room for a locally successful intermediate result, a newly discovered adjacent issue, stale artifact, open PR, or interesting improvement to become the de facto stopping point or redirect execution even when authorized unattended-safe work remains toward the actual objective.

## Challenge

A new subsystem, drift registry, global checklist, or separate convergence authority is not earned.

The gap is representational, not architectural. The existing Planning Operating Model and Work Packet already own the relevant behavior.

The smallest change is therefore:

1. make the terminal condition explicit for non-trivial packets;
2. load extra context only when it can resolve a current uncertainty, dependency, consequence, or proof obligation;
3. classify discoveries against that terminal condition;
4. continue through required dependencies instead of stopping at locally green intermediate artifacts;
5. route non-blocking findings to their existing owners without abandoning the selected objective.

## Counterexamples / limits

- A material discovery that invalidates a required premise is blocking even if it is inconvenient.
- A stronger human/security/cost/privacy/legal/release gate still stops the consequence it governs.
- The terminal condition cannot be invented by the packet; it is derived from current authority.
- Anti-drift does not authorize broader scope, unrelated cleanup, or hidden dependency creation.
- Trivial/single-step work should not gain unnecessary ceremony.

## Learning disposition

**IMPLEMENTED candidate; real retest required.**

Owner surfaces:

- `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md`
- `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md`

No new runtime subsystem or mandatory persisted artifact is created.

## Real retest condition

Use the next natural multi-step Mode-C packet where execution encounters at least one adjacent/non-blocking discovery or locally green intermediate result before the authority-derived terminal condition. Validation requires that execution stays on the objective, routes the discovery correctly, and reaches the terminal condition (or a genuine blocking/stronger gate) without scope expansion.
