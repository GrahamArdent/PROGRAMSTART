# Connection-surface completeness — Tailscale / Secrets natural learning observation

**Date:** 2026-09-20
**Learning candidate:** PSL-023
**Origin:** Execution Node #211, Secrets #78/#79, Secrets PR #80

## Trigger

A Tailscale durability packet initially narrowed the provider consequence to a manual admin-console gate, then narrowed again toward a preferred API authentication strategy. The operator challenged both reductions: Tailscale had additional command/API routes, and different connection mechanisms expose different capabilities.

Fresh live/provider evidence showed the problem was not merely one missing command. The architecture had conflated:

- a preferred authentication path for one effect;
- the full set of available connection surfaces for the provider.

That conflation can manufacture human gates, hide useful recovery paths, and discard distinct capabilities/failure domains.

## Real correction

Secrets Control Plane #79 / PR #80 implemented:

`CONNECTION_COMPLETE_BY_DEFAULT`

Canonical distinction:

`complete connection inventory != every credential materialized != every surface activated`

The accepted Secrets contract now requires complete connection discovery before operation-specific auth selection and explicitly states the Authentication Path Resolver is not winner-take-all.

The Tailscale natural retest retained 13 distinct surfaces, including management API, API-token authentication, OAuth client, OAuth app, CLI/daemon, device web UI, Tailscale SSH, ordinary SSH over the tailnet, private data plane, admin console, webhooks, configuration audit-log API and log streaming.

The implementation also mechanically enforces that:

- preferred surface does not suppress alternatives;
- discovery does not imply activation;
- discovery does not imply credential creation;
- selection is per operation;
- unknown provider-specific surfaces are discovered/registered instead of discarded for not fitting a predefined class.

## Methodology implication

Before PROGRAMSTART concludes "automation unavailable", "human gate", or "use the preferred provider path", it should first enumerate materially supported connection surfaces relevant to the effect.

This is broader than Secrets. It applies whenever a provider/system/resource offers multiple APIs, CLIs, SDKs, OAuth/session models, webhooks/events, native integrations, connected apps, private-network/machine paths, local protocols or admin surfaces.

The owning project still controls provider/domain semantics and consequence authority. Connection completeness is discovery/evidence, not permission to activate everything.

## Challenge

1. **Does this force agents to provision every credential?** No.
2. **Does it activate every discovered interface?** No.
3. **Does it prohibit a preferred path?** No; preference is effect-scoped.
4. **Does it create another provider/API gateway?** No.
5. **Could discovery become unbounded research ceremony?** The scope is materially supported surfaces relevant to current/adjacent operational capability; use JIT research and provider-current evidence.
6. **Could a deprecated path clutter architecture?** Record currentness/deprecation/retirement evidence instead of silently deleting it.
7. **Does the rule reduce human relay?** In the originating case it corrected a premature manual Tailscale gate and exposed machine/provider alternatives without widening authority.

## Disposition

`PSL-023=IMPLEMENTED`

Natural validation is still required on the next unrelated provider/system with multiple viable connection surfaces.

The retest should prove:
- alternatives are discovered before path selection;
- capability/trust differences are retained;
- one path is chosen per effect;
- other surfaces remain visible;
- no unnecessary credential/provider activation occurs;
- no human gate is manufactured solely because one surface is unavailable.
