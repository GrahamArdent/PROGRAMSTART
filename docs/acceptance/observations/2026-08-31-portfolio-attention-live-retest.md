# Learning Observation — Portfolio Attention Control Live Retest

**Date:** 2026-08-31  
**System:** external `GrahamArdent/portfolio-operations` workspace + live multi-repository refresh  
**Classification:** systemic / validation evidence  
**Existing lesson:** `PSL-018`

## Trigger

After material state changes across several independently governed repositories, the operator asked for the portfolio-control recommendation to be carried forward into a dedicated repository and used to keep current work organized.

This was the natural retest condition recorded for `PSL-018`: refresh a real external portfolio after project state changes, correct stale assumptions cheaply, keep paused work non-urgent, separate one short operator gate from one primary build, preserve bounded WIP, and hand execution back to project authority without creating a shadow roadmap.

## External workspace boundary proved

The operator created private repository:

`GrahamArdent/portfolio-operations`

Live verification confirmed it was private and initially empty.

The workspace was then initialized with only the reusable surfaces prescribed by `PROGRAMBUILD/PROGRAMBUILD_PORTFOLIO_CONTROL.md`:

- `README.md` — authority/data-flow/anti-bloat contract;
- `PROJECT_REGISTRY.yaml` — retained derived attention metadata with authority/evidence/invalidation pointers;
- `PORTFOLIO_STATUS.md` — one current operator gate, one primary build, one secondary fallback, explicit no-action set;
- `PORTFOLIO_HISTORY.md` — meaningful attention transitions only.

The filled portfolio remained outside PROGRAMSTART. No project roadmap, milestone authority, release authority, or global execution queue was moved into PROGRAMSTART or Portfolio Operations.

## Cheap retained-state refresh changed the decision

The refresh did not deep-audit every repository. It verified only evidence capable of changing the attention decision and reused current authority where still valid.

### Execution Node

Current project authority remained `CURRENT_WORK_PACKET.md` under `docs/EXECUTION_NODE_STABILIZATION.md`.

Newer physical evidence showed a stale Stage-0 direct apply had rewritten the machine-readable provisioning checkpoint to older scope even though the previously accepted Stage-1 filesystem/local-state foundation remained physically present.

Derived attention:

- `OPERATOR_GATE` — restore checkpoint truth through the exact previously accepted Stage-1 source, then resume PR #21 physical acceptance.

The gate was selected because it is a short human/admin action with high closure/unlock value and because EN-02 PR #25 explicitly blocks physical execution until the EN-03 installed/repository divergence is resolved.

### PROGRAMSTART Compute Spine

Current authority remained `COMPUTE_SPINE_EXECUTION.md` Stage 1 / RS-009.

Live GitHub evidence showed PR #6 exact-head CI had already returned success. The stale state "waiting for CI" therefore did not survive the refresh.

Derived attention:

- `PRIMARY_BUILD` — perform the required exact-head post-implementation adversarial Challenge Gate on PR #6.

This work is executable without a paid/provider mutation and directly advances the future execution substrate intended to reduce operator relay burden.

### Repo Watchtower

Current authority showed V0.2 Slices 1-2 closed and Slice 3 next.

Derived attention:

- `SECONDARY_READY` — bounded fallback only, not permission for a second consequential build.

### Dedication

Live PR/check evidence corrected another stale assumption: Location Context V1 PR #49 still described CI as the next step, but the exact-head Android emulator smoke had already succeeded.

Derived attention:

- `WATCH` with `ci_returned` + `physical_acceptance_pending` closure signals;
- final Samsung acceptance remains the next meaningful project gate when it earns operator attention;
- Packet 2 speech polish PR #48 remains explicitly parked/non-blocking and was not promoted by age.

### GCRM

Current GCRM authority still named the Vercel production authorization/project-scope boundary as R4-02 closure-control.

A narrow live Vercel recheck was performed because provider state could change the attention decision. The connected team remained visible, but project listing still returned zero projects.

Derived attention:

- `WATCH` with `provider_gate`;
- the existing blocker was retained because current provider evidence still supported it;
- no extra safe-lane preparation was manufactured merely because it was executable.

### Resume Creator V6

Current `main` explicitly records the project as paused and disables GitHub Actions while paused.

Derived attention:

- `PARKED`.

The project did not rise in priority because its retained evidence was older.

### Dedication Email Bridge

Live `main` and GitHub Actions proved the deterministic Gmail evidence foundation was already merged and green, while `PROGRAMBUILD_STATE.json` still described final branch convergence/merge as the current implementation-loop slice.

Derived attention:

- `WATCH` with `authority_lag` closure signal;
- the correct next action is cheap authority reconciliation, not new implementation.

### Dedication Calendar Bridge

Credential-independent B5 work remains implemented; real-account smoke remains intentionally credential/provider gated.

Derived attention:

- `WATCH`.

The existence of a credential gate did not by itself create urgency.

### Secrets & Identity Control Plane

The recently created private repository was registered after a narrow live check. Current `main` records M1 metadata-only inventory complete with handoff to M2 Infisical pilot design.

Derived attention:

- `WATCH`.

Its high cross-project leverage was preserved without silently displacing the selected primary build.

## Bounded WIP proved useful

The resulting live status contained exactly:

- one `OPERATOR_GATE`: Execution Node checkpoint/source-truth restoration;
- one `PRIMARY_BUILD`: Compute Spine PR #6 Challenge Gate;
- one `SECONDARY_READY`: Watchtower V0.2 Slice 3;
- all other assessed projects as `WATCH` or `PARKED`.

This separated a short physical/admin closure action from substantive repo-only work and prevented multiple ready projects from becoming simultaneous active priorities.

## Closure debt remained a signal, not a backlog

The external registry/status added optional derived `closure_signals` only where current evidence justified them, including:

- `machine_truth_stale`;
- `ci_returned`;
- `physical_acceptance_pending`;
- `provider_gate`;
- `authority_lag`;
- `safe_lane_displacement`.

These flags do not create tasks or lifecycle states. They are removed when the underlying evidence resolves and never override owning-project authority.

## Handoff boundary preserved

Every promoted action terminates at the owning project:

- Execution Node -> current Work Packet / exact physical acceptance path;
- Compute Spine -> `COMPUTE_SPINE_EXECUTION.md` / PR #6 Challenge Gate;
- Watchtower -> `docs/WATCHTOWER_V0_2_EXECUTION.md` Slice 3 if fallback is needed.

Portfolio Operations does not close milestones, merge PRs, authorize provider mutations, or change project scope.

## Validation result

`PSL-018` is **validated**.

The real external-workspace retest demonstrated the intended behavior after material project-state changes:

- filled live portfolio state stayed outside PROGRAMSTART;
- retained rows were refreshed selectively rather than every repository being re-audited;
- live evidence corrected stale CI/authority assumptions;
- paused work stayed non-urgent despite age;
- one operator gate remained distinct from one primary build;
- one bounded fallback was visible without becoming parallel WIP;
- provider state was checked only where it could change attention;
- project execution handed back to Mode C / project-owned authority;
- no shadow roadmap, portfolio lifecycle, or global execution authority was created.

No additional PROGRAMSTART methodology feature is earned by this retest.

## Continued counterevidence conditions

Retain the existing mechanism but reconsider/narrow it if future real use shows that:

- maintaining the external registry costs more effort than direct repository reorientation;
- invalidation metadata repeatedly fails to prevent stale misrouting;
- bounded WIP systematically hides necessary concurrent operator work;
- closure signals drift into a shadow backlog;
- Watchtower or another evidence system naturally subsumes refresh mechanics without preserving the authority boundary;
- portfolio recommendations begin authorizing consequential mutations rather than handing back to project authority.

Until such evidence appears, the smallest correct outcome is maturity reconciliation only: `PSL-018 implemented -> validated` with no protocol expansion.
