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
