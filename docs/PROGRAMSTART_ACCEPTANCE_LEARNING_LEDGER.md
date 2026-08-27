# PROGRAMSTART Acceptance Learning Ledger

Purpose: retain reusable methodology lessons proven by real projects without turning conversations, acceptance projects, or this file into a portfolio plan.

Status: **subordinate / non-canonical**.

This file is **not** a game plan, execution spine, backlog, lifecycle stage, project authority, or portfolio master. Each real project keeps its own authority. Entries record evidence about PROGRAMSTART itself and may point to project evidence without copying or replacing that project's plan.

## Recording model

Use the smallest durable record that answers:

**REAL PROJECT OBSERVATION → SYSTEMIC OR LOCAL? → PROGRAMSTART OWNER → CHANGE, IF ANY → REAL RETEST → RESULT**

Evidence maturity labels describe how strongly a methodology lesson has been earned. They are not execution priority authority.

Allowed lesson states:

- **observe** — plausible signal; more real usage is needed;
- **candidate** — repeated or material evidence suggests a reusable change;
- **implemented** — PROGRAMSTART changed, but real-world retest is incomplete;
- **validated** — the change altered real execution behavior as intended;
- **rejected** — evidence showed the proposed methodology change was unnecessary or harmful.

## Real-world acceptance record

### Dedication Calendar Bridge

**What it tested**

- real production greenfield integration rather than a mock;
- PROGRAMSTART-generated PROGRAMBUILD structure;
- Google provider OAuth/read-only integration boundaries;
- deterministic normalization and incremental synchronization;
- replay/idempotency and cursor handling;
- a real cross-repository contract dependency on Dedication;
- credential/manual acceptance gates.

**Observed evidence**

- PROGRAMSTART PR #49 (`feat: add methodology-only greenfield bootstrap`) records that the Calendar Bridge exposed full-factory bootstrap cost and produced the lean methodology-only bootstrap.
- Live Calendar Bridge PR #5 (`fix: harden B5 Calendar convergence boundaries`) is open and explicitly depends on companion Dedication hardening for `sync_profile`, the six-argument Calendar CAS, and provider-neutral connection provision/disable RPCs.
- Live Dedication PR #46 (`Calendar B5a convergence hardening`) is open; its PR evidence records the companion contract as deployed to the hosted Dedication runtime, while repository convergence remains open.
- The current Calendar Bridge head passes `Verify Bridge`; the current Dedication companion head passes the relevant Supabase migration verification.

**Lesson classification:** systemic.

**PROGRAMSTART owner:** cross-repository dependency/authority reasoning in the existing orchestration/work-packet contract.

**Lesson:** cross-repository dependencies need first-class, task-scoped orchestration that can distinguish product/contract authority, implementation mechanics, partial dependency satisfaction, reusable companion evidence, repository convergence, and external/manual gates without creating a multi-project Master.

**Change produced:** PROGRAMSTART PR #56, `feat(programstart): orchestrate cross-repository dependencies`.

**Result:** validated at the connected-tool orchestration/protocol level against the live Dedication + Calendar Bridge relationship. The executable CLI regression coverage is present in PR #56, but local pytest/full convergence is not claimed in the connected-only environment.

### Dedication Email Bridge

**What it tested**

- real production greenfield integration;
- external evidence semantics and a deterministic foundation;
- the external PROGRAMSTART control plane;
- the environment-aware orchestration bridge;
- adaptive targeted research;
- Gmail OAuth/runtime composition;
- credential/manual release gates.

**Observed evidence**

- PROGRAMSTART PR #53 added the external target control plane after Email Bridge usage showed that lean project bootstraps still needed active PROGRAMSTART machinery.
- PROGRAMSTART PR #54 added `programstart orchestrate` as the environment-aware orchestration bridge.
- Dedication-Email-Bridge PR #1 merged the credential-free deterministic foundation.
- Dedication-Email-Bridge PR #2 explicitly records that live PROGRAMSTART orientation prevented skipping ahead: the deterministic foundation first had to converge and merge before Gmail OAuth/runtime activation became the actual next slice.
- PR #2 keeps production Gmail activation separate from implementation and retains Google credential/consent, host/scheduler, revoke/re-auth, live mailbox smoke, rollback, and release convergence as later/manual boundaries.

**Lesson classification:** systemic.

**PROGRAMSTART owner:** Mode-C live-authority orientation, environment-aware orchestration, and manual-boundary handoff semantics.

**Changes already produced:** PROGRAMSTART PRs #53 and #54.

**Result:** validated for live-authority-over-handoff behavior; manual/operator gate handoff remains a strong reusable candidate.

### GCRM

**What it tested**

- mature Mode C under an existing Master;
- stale Master/provider narrative versus live provider evidence;
- provider visibility/access discrepancy;
- an active closure-control row whose blocker was narrower than the whole milestone.

**Observed evidence**

- PROGRAMSTART PR #55 records the reusable failure mode and adds blocker-scope, safe-lane, and external-resource evidence-continuity rules.
- Current GCRM PR #34 is explicitly a Lane A/B preparation packet under the existing Master while the R4-02 deployment boundary remains closure-control; it avoids deliberate live provider/database/secret mutations and records the provider behavior actually observed.

**Lesson classification:** systemic.

**PROGRAMSTART owner:** Mode-C blocker scope, safe execution lanes, and external-resource evidence continuity.

**Change produced:** PROGRAMSTART PR #55.

**Result:** validated. A narrow blocker can remain closure-control while safe independent preparation proceeds.

### Dedication

**What it tested**

- mature Mode C under one Master with several legitimate bounded work streams;
- Android/runtime/Supabase/provider boundaries;
- physical-device acceptance separate from repository and emulator CI;
- real-user interaction defects discovered only after physical acceptance;
- cross-repository Calendar and Email integration work.

**Observed evidence**

- Recent Android PRs distinguish automated Android smoke from required Samsung physical acceptance instead of treating machine-green CI as equivalent proof.
- PRs #42 and #45 were focused corrections arising from physical Packet 2 acceptance defects.
- PRs #41/#43 and #46 demonstrate Dedication acting as product/contract/runtime authority for companion Email and Calendar bridge repositories.

**Lesson classification:** mixed systemic signals.

**Likely reusable lessons**

- concurrent bounded lanes can be legitimate under one project spine;
- verification evidence needs source/type distinctions so machine, hosted-runtime, physical-device, and human acceptance are not collapsed into one generic green state;
- companion repositories need an explicit authority/dependency split.

**State:** concurrent Mode-C lane coordination is strong/candidate; verification evidence source/type remains observe until another acceptance case proves the smallest useful model.

### LinkedIn Generator

**What it tested**

- legacy repository modernization;
- current product intent outranking stale prototype/README framing;
- many small high-velocity Mode-C slices;
- evidence-backed voice and quality changes;
- lightweight targeted verification;
- selective methodology propagation into an already adopted existing project.

**Observed evidence**

- PROGRAMSTART PR #50 fixed eight-dimension/Mode-C idea shaping after LinkedIn Generator exposed a Stage-0 restart hazard.
- PROGRAMSTART PR #51 fixed legacy-evidence authority precedence after the same modernization exposed ambiguity between stale prototype framing and current product intent.
- LinkedIn Generator has continued through many small bounded PRs without broad planning ceremony; recent PRs #14–#20 are narrow product-quality slices.
- LinkedIn Generator PR #19 selectively synchronized only the managed PROGRAMSTART Mode-C files that had materially changed, preserved LinkedIn product authority/state, and did not treat the sync as a strategic replan.

**Lesson classification:** systemic but overhead-sensitive.

**Likely reusable lessons**

- high-velocity Mode C must remain lightweight and proportional;
- not every small slice earns broad planning/research ceremony;
- selective methodology propagation is useful when it preserves project authority and only moves managed controls.

**State:** lightweight/high-velocity Mode C remains observe; selective methodology propagation is a later/supporting capability with one positive real example.

### Paused / inactive / retired repositories

Prior operations have included repositories that were paused, disabled, superseded, or otherwise not continuously active. That pattern suggests a future re-entry problem: dormant repositories should not be treated as if their execution state were continuously current.

This session did **not** re-verify enough live lifecycle evidence across the previously discussed inactive repositories to promote a concrete lifecycle model.

**Lesson classification:** possible systemic future concern.

**Likely lesson:** PROGRAMSTART may eventually need active / paused / inactive / retired awareness plus focused re-entry orientation.

**State:** observe. Do not implement from this ledger entry alone.

## Evidence-maturity view

These labels are maturity signals only. They are **not** a numbered roadmap and do not authorize work in any product repository.

### Implemented / validated

- **Cross-repository dependency orchestration** — PR #56 implements the narrow task-scoped model and the live Dedication + Calendar Bridge relationship validates the authority split, partial-satisfaction state, evidence reuse/invalidation, closure control, and external/manual boundary behavior at the connected-tool orchestration level.

### Strong / ready for implementation

- **Concurrent Mode-C lane coordination** — Dedication/GCRM evidence shows multiple bounded safe streams can coexist under one spine without creating parallel Masters.
- **Operator/manual gate handoff** — Calendar and Email both end at real credential/operator/runtime gates that need a clean exact handoff contract.

### Observe / test more

- **Verification evidence source/type** — distinguish repository CI, hosted runtime, provider, physical device, and human acceptance without building an evidence bureaucracy.
- **High-velocity/lightweight Mode C** — LinkedIn Generator shows the need for very low ceremony, but the smallest durable methodology change is not yet proven.
- **Paused/inactive/re-entry lifecycle** — plausible but not sufficiently revalidated in this session.

### Later / supporting capability

- **Selective PROGRAMSTART methodology propagation** — useful for existing adopters; LinkedIn Generator PR #19 is a positive example.
- **Richer acceptance reporting/matrix** — only warranted if this ledger/checklist proves too weak during repeated real use.

## Acceptance result — cross-repository orchestration

**Protected authority rule:** Dedication remains product/contract/runtime authority for its integration boundary. Dedication-Calendar-Bridge remains implementation authority for Google-specific bridge mechanics and its own PROGRAMBUILD execution state. PROGRAMSTART may derive a task-scoped relationship graph but may not create a shared Master, advance both projects, close both projects, or merge companion PRs merely because a dependency exists.

**Live acceptance evidence (2026-08-27):**

- Dedication PR #46 remained open and mergeable at acceptance review; head `a06eb375c95b6ff1562cdad009db108b5da1ae0a` had `Verify Supabase Migrations` successful, and the PR evidence records the companion Calendar contract as deployed to the hosted Dedication runtime.
- Dedication-Calendar-Bridge PR #5 remained open and mergeable; head `9cb6dc36ba7013b2224e0833bf7e67107e4bc2ad` had `Verify Bridge` successful and the PR still retains the B5 credential gate until companion convergence plus real Google initial and restart/incremental smoke.

**Derived authority/dependency result:**

- product/contract/runtime meaning: Dedication;
- Google-specific implementation mechanics: Dedication-Calendar-Bridge;
- dependency state: `partial`;
- reusable evidence: hosted Dedication Calendar contract plus the relevant successful companion repository checks;
- invalidation: companion PR/head/contract/runtime evidence changes or directly conflicting evidence;
- closure control: Calendar Bridge B5 credential gate;
- remaining external/manual boundary: Google OAuth credentials and the real initial + restart/incremental Calendar smoke;
- safe behavior: neither repository is automatically advanced, closed, merged, or edited as a cross-project transaction.

**PROGRAMSTART change:** PR #56 extends the existing `programstart orchestrate` / work-packet contract with one bounded related repository, relationship/authority ownership, `unknown | unsatisfied | partial | satisfied` dependency state, evidence/invalidation, closure control, and manual boundary. It does not create another lifecycle or portfolio planner.

**Verification actually performed:** complete PR file list and file-by-file patch review; source/test static review including correction of incidental single-repository behavior drift and newly introduced Ruff line-length issues; live PR/head/workflow evidence checks for both acceptance repositories. PROGRAMSTART has no automatic PR status checks on this branch by design, the connected surface cannot dispatch the repository's manual-only convergence workflow, and no local pytest, Ruff/Pyright, `programstart drift`, or `nox -s ci` result is claimed.

**Acceptance result:** validated for the connected-tool orchestration behavior. The change correctly represented a multi-plane partial dependency without becoming cross-project authority and returned the exact closure-control/manual boundary.

**New systemic lesson:** dependency satisfaction is multi-plane rather than boolean. Repository convergence, hosted runtime availability, provider readiness, and human/operator acceptance may differ at the same moment. The next reusable gap is therefore not a richer portfolio graph; it is a small operator/manual-gate handoff contract that says exactly what action is required, what evidence must come back, what would invalidate it, and where PROGRAMSTART resumes afterward.

**Next evidence-earned candidate:** operator/manual gate handoff. Concurrent Mode-C lane coordination remains strong, but it is not part of PR #56.