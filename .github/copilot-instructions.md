# PROGRAMSTART Repository Instructions

## Repository Role

PROGRAMSTART is a reusable planning/delivery system. `PROGRAMBUILD/` owns reusable project methodology; `USERJOURNEY/` is optional journey-planning. Machine-readable workflow rules live in `config/process-registry.json` and are preferred over conversational memory.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in authority docs follow RFC 2119.

## Startup / JIT

Do not read the documentation tree up front.

1. inspect current repository/PR state;
2. use `scripts/programstart_status.py` / `programstart status` and `programstart guide --system <system>` to orient;
3. identify the current strategic execution spine/stage;
4. load only the exact authority sections/evidence needed for the current task;
5. use `.github/instructions/source-of-truth.instructions.md` for detailed JIT behavior.

## Portfolio Attention Checkpoints

`PROGRAMBUILD/PROGRAMBUILD_PORTFOLIO_CONTROL.md` defines optional cross-project attention routing. Portfolio attention is derived operator context, never project execution authority.

- Do **not** read, rebuild, or refresh a live portfolio workspace on every project turn.
- At startup inside a specific project, project authority remains primary. Portfolio state is relevant only when the operator asks a portfolio-level question or when a meaningful project checkpoint can invalidate the current portfolio row.
- A meaningful portfolio checkpoint includes a milestone/packet merge or closure, blocker/operator-gate change, dependency change, explicit pause/resume, or provider/runtime evidence that materially changes the project's next executable action or attention class.
- At such a checkpoint, if an already-authorized live external portfolio workspace is available and writable, reconcile only the current project's row and meaningful attention history after project truth has been reconciled in its owning repository.
- If the external workspace is unavailable, unwritable, or would require crossing an unapproved repository boundary, do not block truthful project closure. Report portfolio reconciliation as pending rather than inventing or silently persisting state elsewhere.
- When the operator asks "what should we work on?", "where should my attention go?", or equivalent across projects, use the live portfolio workspace first when available, refresh only evidence that could change the decision, and apply the bounded `OPERATOR_GATE` + `PRIMARY_BUILD` + `SECONDARY_READY` model from Portfolio Attention Control.
- Staleness is never urgency. Paused/parked work must not rise in priority merely because time passed.
- Portfolio state can never close a project milestone, approve a release, change project scope, or override newer repository/runtime/provider truth.

## External Change Maintenance

`docs/PROGRAMSTART_EXTERNAL_CHANGE_MAINTENANCE.md` defines the bounded maintenance response when a verified provider/tool/platform/model/API/runtime/plan change may invalidate PROGRAMSTART or a managed project's current assumptions.

- Do not terminate at notification when the correct response is safely deterministic. Classify the verified change as `no_effect`, `evidence_refresh`, `deterministic_maintenance`, `bounded_behavioral_maintenance`, `material_decision`, or `automation_failed`.
- Use official/current evidence plus live repository/project authority before claiming impact. External news is evidence, not architecture or project authority.
- For authorized `deterministic_maintenance`, prepare the smallest focused branch/PR and run the smallest sufficient truthful validation without asking the operator to relay routine maintenance steps.
- Auto-merge is a stronger trust level than automatic PR creation. It is allowed only when target-repository policy explicitly permits the playbook and required enforced validation is actually green; otherwise remain PR-only.
- Architecture, security/privacy/legal, billing/spending, migrations/data, destructive actions, release authority, project scope/sequencing, secrets, and other hard-to-reverse decisions retain their stronger project/operator gates.
- If multiple projects are affected, route each through its own current authority/Mode-C delta and repository PR boundary. Never turn one provider change into an implicit portfolio-wide mutation transaction.
- Watchtower may supply authenticated/deduplicated incident evidence and may later execute policy-scoped maintenance when Watchtower's own authority permits it; observe-only Watchtower deployments remain sensor/evidence sources only.
- Successful routine maintenance should be quiet or digestible. Notify the operator when a decision/action is required, evidence is ambiguous, cost/security exposure changes, validation fails, or automation cannot safely continue.

## Authority Rules

- Preserve one strategic execution spine per real project.
- Research, audits, readiness reviews, checklists, and work packets are evidence/derived aids unless canonical authority adopts them.
- Existing/in-flight projects keep their current roadmap/game plan unless replacement is explicitly approved.
- Update a concern's canonical owner before dependent representations.
- If implementation would prospectively contradict `ARCHITECTURE.md`, update architecture/decision authority in the same coherent change first.
- If validated behavior reveals stale documentation, reconcile the authority before further dependent work.

## Work Packets

`PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` defines packet semantics.

Use the compact logical packet by default. Persist `CURRENT_WORK_PACKET.md` only when multi-session/multi-agent coordination, risk, dependencies/blockers, or resumability makes persistence useful. A packet never becomes strategic authority.

## Verification Economy

- Reuse trustworthy verification until a relevant invalidation trigger occurs.
- During a slice, run the smallest sufficient verification for the changed/at-risk surface.
- Widen at meaningful convergence boundaries, not from an arbitrary feature/time counter.
- Do not rerun broad checks merely because a session changed.
- Use the manual convergence workflow only when a full-repository gate is actually warranted.

## Preferred Commands / Enforcement

- `scripts/programstart_status.py` / `programstart status` — current strategic orientation
- `scripts/programstart_step_guide.py` / `programstart guide --system <system>` — JIT baseline
- `scripts/programstart_drift_check.py` / `programstart drift` — authority/registry drift when relevant
- `scripts/programstart_validate.py` / `programstart validate ...` — required validation/convergence checks
- `scripts/programstart_workflow_state.py` / `programstart advance ...` — workflow transitions

Prefer registry-backed commands over freehand reconstruction of execution order.

## Editing / Governance

- Keep changes bounded and coherent.
- Do not create documentation diaries for micro-steps.
- Record evidence once and reference it elsewhere.
- Use `PROGRAMBUILD/DECISION_LOG.md` for ordinary material choices; record durable architecture/policy decisions in `docs/decisions/` when the current ADR policy warrants it.
- All `.github/prompts/*.prompt.md` files must follow `.github/prompts/PROMPT_STANDARD.md`; internal build prompts are exempt where the standard says so.
- Commit messages must use Conventional Commits.

Repository boundary is explicit: do not inspect, edit, stage, commit, or push another repository unless the user explicitly names that repository and asks for that action.
If the task may require work in another repository, stop and ask for express consent before proceeding.

## Success Test

An agent should quickly answer: what is authoritative, what is happening now, what context is needed, what evidence remains valid, what changed enough to verify, and what proves this slice is done.

If answering those requires reading the whole repo or interpreting competing plans, simplify before adding more process.
