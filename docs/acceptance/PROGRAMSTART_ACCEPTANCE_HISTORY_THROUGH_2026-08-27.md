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
- At operator-handoff acceptance review, PR #2 remained open/mergeable at head `c8a3054ada5ac9dbb1eaea5d1c31a6bd62806f28` and its `Test` workflow was successful.

**Lesson classification:** systemic.

**PROGRAMSTART owner:** Mode-C live-authority orientation, environment-aware orchestration, and operator/manual-gate handoff semantics.

**Changes produced:** PROGRAMSTART PRs #53 and #54; PR #57 implements the evidence-earned operator/manual-gate handoff contract and decouples a manual boundary from cross-repository metadata.

**Result:** live-authority-over-handoff behavior is validated. PR #57 is protocol-validated against the real Email release boundary: PROGRAMSTART can derive a specific secret-safe action/evidence/resume handoff without inventing a companion repository or asking for project history already present in live authority. The actual operator-action → returned-evidence → resume cycle has not been executed in this acceptance session and remains a future real-use validation point.

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

### Resume Creator V6

**What it tested**

- mature, nearly complete Mode C rather than bootstrap or rebuild;
- deliberate re-entry after a project pause;
- stale execution/readiness documents versus substantially later implementation evidence;
- recognition that open dependency-maintenance PRs are not automatically unfinished product work;
- proportional verification after CI was deliberately removed during the pause;
- external-resource evidence continuity across Supabase, Vercel, and Render;
- PR #57 operator/manual-gate handoff semantics in a single-repository task with no companion dependency;
- whether PROGRAMSTART can decide that optional UX expansion should remain optional and that closure is a valid near-term outcome.

**Observed evidence**

- Resume Creator `main` was at `16a813295c3a5ce8e006d7d75b27ad9fbed6992a`, explicitly removing GitHub Actions while the project was paused.
- Repository history after the old March readiness plans contains broad April real-integration/security/test hardening and June JD/rewrite/reliability work, including a simplified `Finish Resume` path. This invalidated old plan-status assumptions without invalidating the historical proof itself.
- The current Supabase project `hfvrcwaoesairitwteyt` / `GrahamsProjects` was live-observed as `INACTIVE`; this blocks current live persistence proof but not safe repository preparation.
- GitHub produced a Vercel status context for the Resume re-entry branch while the connected Vercel account could not resolve the `resume-creator-v6` project by slug. PROGRAMSTART preserved historical existence/current visibility as separate facts rather than inventing a deletion conclusion.
- Current Render state could not be verified through an installed/connected provider tool, so the missing observation was classified as an environment/connector limit rather than a product fact.
- Resume Creator PR #16, `chore: rebaseline Resume V6 finish-line verification`, reconciles the existing production-readiness authority in place, restores a focused deterministic CI surface, and explicitly avoids product feature expansion.
- GitHub reported zero Actions runs for the re-entry branch even after the workflow was restored. PR #16 therefore uses the PR #57 compact operator-gate contract: `merge_gate`, GitHub Actions gate owner, exact action, no-secret handling, run/job return evidence, acceptance criteria, invalidation, `RESUME_AT` R1, and safe Lane-B work while waiting.

**Lesson classification:** primarily confirmation / no new methodology gap.

**PROGRAMSTART owner:** existing Mode-C authority precedence, evidence reuse/invalidation, blocker/safe-lane reasoning, external-resource continuity, proportional verification, closure judgment, and PR #57 operator-gate handoff.

**Result:** PROGRAMSTART correctly identified a Class-C project (validation/hardening/deployment remaining), reduced the apparent backlog instead of expanding it, preserved one existing execution spine, and derived a small repository-only verification slice before any live runtime mutation. No Stage-0 restart, deep research, portfolio plan, or speculative feature roadmap was needed.

**Paused/re-entry lesson:** this real re-entry case weakens the case for a new active/paused/inactive/retired lifecycle state machine. Existing Mode-C orientation plus evidence invalidation, safe lanes, and operator-gate handoff were sufficient to reason about the pause. Keep the dedicated lifecycle-model idea at observe unless future re-entry cases show friction these existing primitives cannot solve.

**Operator-gate retest:** PR #57 is now independently protocol-retested on a single-repository GitHub Actions boundary. The exact operator action → returned evidence → resumed execution cycle is still open because the required Actions run has not yet been returned. Do not overclaim end-to-end validation.

**PROGRAMSTART change produced by Resume Creator:** none. The needed operator-gate capability was already live on `main` before the Resume gate was derived, and the acceptance test did not expose a missing reusable rule that justified more machinery.

### Paused / inactive / retired repositories

Prior operations have included repositories that were paused, disabled, superseded, or otherwise not continuously active. That pattern suggests a future re-entry problem: dormant repositories should not be treated as if their execution state were continuously current.

Resume Creator V6 now provides one concrete live re-entry case. In that case, existing Mode-C orientation, evidence invalidation, safe-lane reasoning, external-resource continuity, and the operator-gate handoff were sufficient; a separate lifecycle state machine was not needed.

**Lesson classification:** possible systemic future concern, but dedicated new machinery is not currently earned.

**Likely lesson:** preserve explicit pause/re-entry evidence and revalidate only what the pause or runtime changes could invalidate before inventing lifecycle states.

**State:** observe. Resume Creator is evidence against premature implementation of a dedicated lifecycle model; revisit only if future real projects expose a reusable gap the existing primitives cannot express.

## Evidence-maturity view

These labels are maturity signals only. They are **not** a numbered roadmap and do not authorize work in any product repository.

### Implemented / validated

- **Cross-repository dependency orchestration** — PR #56 implements the narrow task-scoped model and the live Dedication + Calendar Bridge relationship validates the authority split, partial-satisfaction state, evidence reuse/invalidation, closure control, and external/manual boundary behavior at the connected-tool orchestration level.
- **Operator/manual gate handoff** — PR #57 implements the bounded handoff contract in the existing Work Packet/orchestration surface and fixes single-repository manual-boundary compatibility. Email Bridge PR #2 plus Calendar Bridge PR #5 validate the need and the handoff structure; Resume Creator PR #16 independently protocol-retests the single-repository form. The first real returned-evidence/resumption cycle remains an observe item rather than being falsely claimed here.

### Strong / ready for implementation

- **Concurrent Mode-C lane coordination** — Dedication/GCRM evidence shows multiple bounded safe streams can coexist under one spine without creating parallel Masters.

### Observe / test more

- **Verification evidence source/type** — distinguish repository CI, hosted runtime, provider, physical device, and human acceptance without building an evidence bureaucracy.
- **High-velocity/lightweight Mode C** — LinkedIn Generator shows the need for very low ceremony, but the smallest durable methodology change is not yet proven.
- **Paused/inactive/re-entry lifecycle** — Resume Creator shows current primitives can handle at least one real re-entry without a new lifecycle state machine; keep observing rather than implementing.
- **Operator-gate returned-evidence resumption** — confirm on the first real credential/device/reviewer/CI gate that returned evidence is sufficient to resume at the declared point without repeating broad orientation or verification.

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

## Acceptance result — operator/manual gate handoff

**Protected authority rule:** a handoff is derived execution context. The project keeps its existing spine and release/runtime authority. PROGRAMSTART may identify the unavailable action and define the evidence needed to resume, but it does not become the credential owner, provider authority, device operator, approver, or acceptance authority.

**Live acceptance evidence (2026-08-27):**

- Dedication-Email-Bridge PR #2 remained open/mergeable at head `c8a3054ada5ac9dbb1eaea5d1c31a6bd62806f28`; its `Test` workflow succeeded.
- PR #2 explicitly separates implemented Gmail OAuth/runtime composition from production activation. Remaining operator/release boundaries include Google OAuth client/consent provisioning, secure refresh-token and Supabase service-role provisioning, host/scheduler ownership, disconnect/revoke/re-auth operations, privacy-safe observability, controlled live-mailbox smoke, rollback/disable proof, and Stage 7 → 8 release convergence.
- Calendar Bridge PR #5 independently confirms the same class of boundary with Google credentials plus real initial and restart/incremental smoke.

**Derived Email handoff example:**

- `GATE_OWNER`: the deployment/operator boundary that owns the Google Cloud OAuth configuration and chosen server runtime/secret store;
- `REQUIRED_ACTION`: after repository code convergence, provision/confirm the Google OAuth client/consent configuration and required server-side configuration on the chosen runtime, then run the project-authorized controlled test-mailbox one-shot sync;
- `SENSITIVE_INPUT_HANDLING`: keep `GOOGLE_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`, `SUPABASE_SERVICE_ROLE_KEY`, and other secret values only in the owning Google/deployment secret surface; PROGRAMSTART may name required configuration keys but must not request their values as handoff evidence;
- `RETURN_EVIDENCE`: non-secret runtime/deployment reference plus the sanitized controlled `sync:once` outcome and any narrow project-authorized provider/runtime status needed to show the read-only path actually executed;
- `EVIDENCE_ACCEPTANCE`: the controlled live sync uses the approved read-only Gmail boundary, succeeds through the existing Dedication evidence path, returns sanitized output, and satisfies the exact live-smoke acceptance owned by Email Bridge release authority; this does not automatically prove unrelated release-readiness items;
- `GATE_INVALIDATION`: Email Bridge head/runtime composition, OAuth scope/client configuration, secret/runtime host configuration, Dedication integration contract, or directly conflicting live evidence changes;
- `RESUME_AT`: the existing Email Bridge Stage 7/release-readiness convergence point that owns live activation evidence, not a new PROGRAMSTART stage;
- `SAFE_WHILE_WAITING`: only repository review/convergence or other independently authorized Lane A/B preparation; no claim that production Gmail activation is complete.

**PROGRAMSTART change:** PR #57 adds the full handoff semantics to `PROGRAMBUILD_WORK_PACKET.md` and orchestration prompt v2.3, makes the handoff explicitly secret-safe/subordinate in canonical authority, and minimally corrects `programstart orchestrate` so `--manual-boundary` works without `--related-repository` and preserves the existing project spine as closure-control.

**Verification actually performed so far:** live Email/Calendar PR and workflow evidence review; branch-vs-main diff review; exact executable commit diff review showing only the intended manual-boundary decoupling; additive focused test coverage added without deleting existing tests. No product repository mutation was performed for acceptance. Local pytest/Ruff/Pyright/`programstart drift`/`nox -s ci` is not claimed in the connected-only environment.

**Acceptance result:** protocol-validated. The handoff is now specific enough to cross an unavailable operator boundary without asking for raw secrets, inventing a companion repository, treating action completion as acceptance, or losing the resume point. End-to-end validation remains intentionally open until a real operator returns evidence and PROGRAMSTART resumes from it.

## Acceptance result — Resume Creator late-stage re-entry

**Protected authority rule:** Resume Creator owns product intent, remaining-work sequencing, and release/closure decisions. PROGRAMSTART may reconcile stale evidence, derive a bounded packet, and expose a precise operator gate, but it must not create a parallel finish plan or keep the project alive through optional feature expansion.

**Live acceptance evidence (2026-08-27):**

- Resume Creator PR #16 is open and mergeable at head `6c72cef9fe796c43c9e39519ab3fb5da51b23f9e`.
- PR #16 changes only the existing readiness authority/index/instructions/branch-check documentation plus a focused deterministic CI workflow; no product feature code is changed.
- GitHub reports zero Actions workflow runs for the re-entry branch at the current acceptance checkpoint, so deterministic green proof is not claimed.
- GitHub still reports a `Vercel` status context for the branch while the connected Vercel lookup cannot resolve the project; the conflict remains explicit rather than being collapsed into deletion or success.
- Supabase project `hfvrcwaoesairitwteyt` remains inactive and is treated as a later runtime/operator gate rather than a reason to mutate production during repository rebaseline.

**PROGRAMSTART behavior under test:**

- Mode C preserved the existing production-readiness file and reconciled it in place instead of creating another Master;
- old planned/partial items were checked against later implementation evidence and optional UX expansion was demoted from MUST work where no current correctness/safety need justified it;
- deterministic repository proof was chosen before provider reactivation;
- the lack of Actions execution was classified narrowly as a merge gate, not a whole-project blocker;
- PR #57's single-repository operator handoff contract captured exact action, non-secret return evidence, acceptance, invalidation, resume point, and safe Lane-B work;
- no deep research or new methodology layer was triggered.

**Acceptance result:** successful late-stage protocol retest. PROGRAMSTART made the nearly finished project smaller and more explicit rather than more elaborate. The first returned-evidence/resumption cycle remains open pending actual Actions evidence.

**Methodology decision:** no PROGRAMSTART feature change is justified by Resume Creator at this checkpoint. The session confirms existing Mode-C/evidence/safe-lane/operator-gate machinery and provides evidence against prematurely adding a dedicated paused/inactive lifecycle state machine.

**Next evidence-earned candidate:** concurrent Mode-C lane coordination remains the strongest next systemic improvement after PR #57. Resume Creator did not produce stronger evidence for a different new feature; its most useful contribution is validation of late-stage reduction, operator-gate use, and the decision not to add lifecycle machinery.
