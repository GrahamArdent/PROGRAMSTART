# PROGRAMSTART Learning Observation — Home Automation WP-19 Learning-Gate Retest

Status: **subordinate / non-canonical evidence**.

## Observation identity

- **Date:** 2026-09-17
- **Real project:** `GrahamArdent/home-automation-control`
- **Companion owner:** `GrahamArdent/secrets-control-plane`
- **Methodology owner:** `GrahamArdent/PROGRAMSTART`
- **Lesson retested:** `PSL-013`
- **Classification:** confirmation / validation
- **Product packet:** Home Automation WP-19 — API-First Provider Surface / Credential-Binding Convergence

## What happened

After PROGRAMSTART PR #120 wired the Learning Gate into the canonical Work Packet / Authority-Gap closure path, Home Automation completed a normal Mode-C packet whose changed surface was not created for methodology testing.

WP-19 reconciled a real product correction:

`useful supported API/protocol -> auth path -> Credential Profile -> fixed adapter/integration -> Home Assistant/canonical capability -> verified outcome`

The product work produced a machine-readable API surface register, strategic/workflow reconciliation, exact-head CI, a focused post-implementation Challenge, merge, and durable terminalization.

At closure, **without Graham asking whether there was a learning lesson**, the packet evaluated the Learning Gate.

## Learning-Gate result

The closure distinguished two outcomes correctly.

### Product/system learning

The reusable architecture finding belongs to Home Automation + Secrets Control Plane:

- API/protocol selection is orthogonal to credential custody;
- API-first must not collapse into static-key-first, cloud-first or Infisical-first;
- provider-native OAuth/session/local integration state can satisfy the common Credential Profile lifecycle without physical centralization.

That finding was persisted in the product/Secrets owners, not promoted into PROGRAMSTART methodology.

### PROGRAMSTART learning

No new methodology subsystem or lesson was earned.

Instead, the closure naturally retested PSL-013:

1. the Learning Gate ran at a qualifying packet closure automatically;
2. Graham did not need to prompt for it;
3. the result was allowed to be local/confirmation rather than forced systemic learning;
4. product merge/terminalization did not depend on PROGRAMSTART being writable;
5. only after product closure produced maturity-changing confirmation was a focused PROGRAMSTART learning update prepared.

This is the behavior PR #120 intended.

## Evidence

Home Automation:
- issue #56 — WP-19 owner;
- PR #57 candidate `a9365965f3a710525bb3e37af8016353a760fa58`;
- hosted CI `35302921051` — SUCCESS;
- implementation merge `05b86bbd5a5991f67a8d1f996079af834e3aec97`;
- focused Challenge — CLEAR WITH EXPLICIT RESIDUALS;
- PR #58 terminalization head `7196dda96d990445fc679f59b1f0d304b1c53b93`;
- hosted CI `35303133110` — SUCCESS;
- terminalization merge `15abd9e24880feb78ca29dcb86e132e469c9dfa4`;
- CURRENT_WORK_PACKET moved to truthful Secrets #69 BLOCKED state rather than leaving terminal WP-19 as current.

Secrets:
- issue #69 received the value-free API/Profile handoff;
- no secret value/provider/runtime mutation was required for this learning retest.

## Maturity decision

Promote `PSL-013` from **implemented** to **validated**.

The validation claim is narrow:

> normal packet closure can invoke the Learning Gate automatically, classify local/systemic/confirmation outcomes proportionally, avoid mandatory artifact creation for ordinary product learning, and route a maturity-changing methodology update only when earned.

This does not claim every future agent/session will execute methodology perfectly. Counterevidence should reopen/narrow the lesson if qualifying closures again skip the gate or turn it into ceremony.

## Next retest

Continue normal use. Record only counterevidence or materially stronger evidence; do not create routine learning records for every successful closure.
