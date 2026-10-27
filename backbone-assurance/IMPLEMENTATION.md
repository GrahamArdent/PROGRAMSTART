# Implementation checkpoint — 27 October 2026

The operator-selected immediate source correction is published on [Paths draft PR81](https://github.com/GrahamArdent/paths/pull/81), commit [`ff1694e5deff607afd560cc879c28234bf227ce6`](https://github.com/GrahamArdent/paths/commit/ff1694e5deff607afd560cc879c28234bf227ce6). Its tree is `93ba8828b1d81e1ac51ae977a18078dc01448ce9`, exactly matching the locally prepared tree. Main is unchanged; no merge, installed activation or hosted re-enablement occurred.

The [owner-local repair record](https://github.com/GrahamArdent/paths/blob/ff1694e5deff607afd560cc879c28234bf227ce6/docs/evidence/lookup-test-gaps-2026-10-27/README.md) retains raw evidence, commands, test identities, the before/after failure, reproduction and review. This audit references those receipts instead of copying the repair evidence into another authority.

## What was closed at source level

| Finding | Change | Evidence |
|---|---|---|
| Unavailable routes were not protected by a direct outcome assertion | Added zero-callback/status assertion | Existing faulty variant now fails |
| Payload fidelity was unasserted | Added nested payload equality with an independent expected object and nonfinal readback status | Replacement and in-place corruption both fail |
| Required suite commands could disappear without a workflow-test failure | Parsed workflow checks require both exact executable commands once | Removal fault fails |
| Dependency path filters could disappear | Independently declared dependency paths must match PR and main-push filters | Script-filter removal fails |
| Jobs/steps could be disabled or failure suppressed | Reject unreviewed conditions, failure suppression and shell overrides in the protected job/steps | Disabled-job and suppressed-step faults fail |
| Discovery could silently select zero tests | Both lookup suites must import cleanly and discover at least one case | Empty suite fails |
| Parity documentation implied candidate gates were merged main | Corrected wording and pinned the actual repaired continuation gate | Exact blob parity passes |
| Broader validation found cross-effect recovery selection | Filter lexical recipe matches by requested primary effect; retain actor/target/currentness JIT obligations | Two failing real-registry cases now pass; legitimate Controller recovery remains |

## Observed validation and limits

The complete Paths parent source tree was reconstructed from 161 independently blob-checked files. The corrected source passed 33 lookup, four gate-parity and 17 root unittest methods: **54 distinct methods**, with repeated root execution inside the workflow not double-counted. All four registry command blocks and the MCP stdio suite passed. Twelve injected faults were rejected by assertion failures, not import/setup failures.

This expands the earlier partial-source pilot. It establishes selected local Linux/stdio behavior, not live Windows, real providers, an installed guard consumer, the independent positive publication verifier or owner acceptance. The original 86-method audit catalog remains a dated source inventory; the repair's expanded method counts are recorded with the actual owner rather than silently rewriting historical test identities. All 84 proposed journey scenarios remain NOT_RUN.

Hosted qualification remains unobserved and the existing hosted hold is preserved. Publication uses `[skip ci]` under that hold; this is not a waiver of required release checks. The current Paths owner checkpoint still requires installed first-call trace, admission/currentness, actual target readback and cold original-ID recovery. Source correctness cannot close those boundaries.

## Current continuation

1. Reuse the published source and receipts. Refresh only current owner/head/environment facts controlling the selected next action; do not repeat N04 as unfinished source work.
2. Within Paths #56's existing execution spine, qualify the remaining actual consumer/installed boundaries through an admitted route. Existing Windows EN545 fixed connectivity is not arbitrary test-runner permission. Preserve original effect identity and check eligible equivalent routes before escalation.
3. N02/N03 remain independent audit mapping for EN and Compute. Begin with protected outcomes and independently expected observations, then test adequacy and selection. Hosted constraints do not freeze independent read-only work.
4. Keep the audit under PROGRAMSTART while ownership and maintenance needs are measured. Extract a separate repository only on the concrete criteria in REPOSITORY_PLACEMENT.md.

The repository-placement decision, source correction and evidence retention complete this requested slice. They do not complete the ecosystem audit, qualify all environments or make the audit a new runtime/acceptance authority.
