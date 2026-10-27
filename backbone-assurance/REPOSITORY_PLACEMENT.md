# Repository placement decision — 27 October 2026

Graham selected documenting the findings durably, closing the demonstrated Paths test gaps immediately, and putting the audit under Git alongside that work. A separate repository will depend on demonstrated ownership and maintenance needs.

## Decision and rationale

Incubate the audit in PROGRAMSTART's `backbone-assurance/` area. The audit merits version control, stable identifiers, reviewable changes and a durable entry point. Its current evidence does not establish an independent maintenance or release lifecycle requiring another repository.

A dedicated repository could provide a stable home for cross-repository journeys, versioned requirements/evidence mappings and an explicit findings backlog. Those are real benefits. Its risks are equally concrete: duplicated inventory/status/evidence, stale copies, component tests separated from their implementations, another place to maintain, and additional CI sweeps that consume resources without better fault detection. A separate repository would not make a checker independent or its conclusions trustworthy.

The immediate value is in stronger owner-local protections. Paths owns the unavailable-route, payload, workflow-selection and discovered recovery-applicability corrections. Repository organization should support delivery of those protections rather than delay it.

## Current ownership evidence

| Concern | Retrieved owner contract | Observation and implication |
|---|---|---|
| Isolated experiments, injected faults, reproducible observations | [Ecosystem Lab charter](https://github.com/GrahamArdent/ecosystem-lab/blob/main/CHARTER.md), blob `eefc36dbad0c04bc6bdec8dc30c383c3de219bac`; README `ad8832626e05bed23dc6485543db4f9bc679167b`; Lab contract `b2b1ce24a56d95d99ee018662d4385c219a2d3c2` | The Lab owns experiments and observations, not production truth, methodology, adoption or acceptance. Reusable experiment implementations belong there; a passed experiment is not self-adopting. |
| Evidence, provenance, scoped acceptance and lifecycle | [Evidence Spine README](https://github.com/GrahamArdent/evidence-spine/blob/main/README.md), blob `3f718b0fae4087b8585dd8f201be8dd788992dff` | Canonical facts should be captured once; acceptance remains scoped to owners. Its Git-native design does not require another database, service or credential. Enrollment/integration must be demonstrated. |
| Cross-owner current-state projection | [Matrix README](https://github.com/GrahamArdent/ecosystem-matrix/blob/main/README.md), blob `f866c58bc2c9b78dadbcab671fc398ab0c7074c6`; [ownership map](https://github.com/GrahamArdent/ecosystem-matrix/blob/main/OWNERSHIP_AND_SOURCE_MAP.md), blob `80625978ffc576c097a0b838e784a2ab580a22ed` | Compute135 coverage is bounded and broader coverage partial. Evidence Spine/Matrix projection boundaries remain subject to reconciliation. Existing responsibility claims are evidence to evaluate, not proof of delivered behavior. |
| Regression tests and implementation fixes | Paths PR81 and each component's existing source/owner contracts | Keep tests close to the behavior they protect. Cross-repository cases may reference multiple owners without relocating their unit/contract suites. |
| Audit outcomes, coverage questions and correction tracking | This operator-selected reference under PROGRAMSTART | The audit specifies questions and evidence gaps; it does not mint component acceptance or become another strategic execution spine. |

These documents were retrieved on 27 October 2026. Their declared boundaries do not by themselves prove live integration. URLs on `main` are discovery locations; the recorded blobs identify the observations.

## External research and its limits

[DORA test automation](https://dora.dev/capabilities/test-automation/) supports developer responsibility for test maintenance, continuous curation, fast feedback and moving detection into the cheapest adequate test layer. [Google's E2E testing analysis](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html) explains why broad E2E suites can make failures slow to diagnose and advocates smaller integration checks where sufficient.

These sources support the testing approach. Neither establishes that a separate audit repository is the correct organizational choice, nor supplies a universal E2E count. The placement decision is an inference from current ecosystem ownership and maintenance needs, not a research-mandated architecture.

## Alternatives and review triggers

1. **New audit repository now:** deferred because an independent lifecycle and ownership need are not demonstrated; it risks duplicating several existing responsibilities.
2. **Put everything in Ecosystem Lab:** rejected for this slice because methodology, owner acceptance and a cross-project audit register exceed its isolated-experiment charter.
3. **Keep only documents/workbooks outside Git:** insufficient for ongoing reviewable changes, stable source references and correction tracking; retained exports remain useful snapshots.
4. **PROGRAMSTART reference with owner-local implementation:** selected as the smallest current arrangement. It has one entry point and links outward to actual owners.

Reconsider extraction when an independently maintained cross-repository harness, different access controls, a separate release cadence or measured coordination cost demonstrates a benefit. Document the observed need, destination owner, migration and rollback before extraction. A growing file count or the importance of the subject is not sufficient by itself.

ADR triage: this is bounded placement of a non-authoritative audit reference, with no change to core execution, acceptance or lifecycle contracts. PROGRAMSTART validation requires every ACTIVE decision to have an ADR link. ADR-0027 records this operator-selected incubation boundary without creating a general central archive or superseding the owner-routing policy.
