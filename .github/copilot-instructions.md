# PROGRAMSTART Repository Instructions

## Repository Role

PROGRAMSTART is a reusable planning/delivery system. `PROGRAMBUILD/` owns reusable project methodology; `USERJOURNEY/` is an optional journey-planning workflow. Machine-readable workflow state/rules live under `config/` and are preferred over conversational memory.

## Startup / JIT

Do not read the documentation tree up front.

1. inspect current repository/PR state;
2. use `programstart status` and `programstart guide --system <system>` (or current equivalents) to orient;
3. identify the current strategic execution spine/stage;
4. load only the exact authority sections/evidence needed for the current task;
5. use `.github/instructions/source-of-truth.instructions.md` for the detailed JIT protocol.

## Authority Rules

- Preserve one strategic execution spine per real project.
- Research, audits, readiness reviews, checklists, and work packets are evidence/derived aids unless canonical authority adopts them.
- Existing/in-flight projects keep their current roadmap/game plan unless replacement is explicitly approved.
- Update a concern's canonical owner before dependent representations.
- If implementation would prospectively contradict `ARCHITECTURE.md`, update architecture/decision authority in the same coherent change first.
- If validated behavior reveals stale documentation, reconcile the authority before further dependent work.

## Work Packets

`PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` defines work-packet semantics.

Use the compact logical packet by default. Persist `CURRENT_WORK_PACKET.md` only when multi-session/multi-agent coordination, risk, dependencies/blockers, or resumability make persistence useful. A packet never becomes strategic authority.

## Verification Economy

- Reuse trustworthy verification until a relevant invalidation trigger occurs.
- During a slice, run the smallest sufficient verification for the changed/at-risk surface.
- Widen at meaningful convergence boundaries (shared-contract change, stage transition, release readiness, material risk), not from an arbitrary feature/time counter.
- Do not rerun broad checks merely because a new session began.
- Use the manual convergence workflow only when a full-repository gate is actually warranted.

## Preferred Commands

- `programstart status` — current strategic state / orientation
- `programstart guide --system <system>` — JIT authority baseline
- `programstart drift` — authority/registry drift when relevant
- `programstart validate ...` — required validation/convergence checks
- `programstart advance ...` — workflow state transitions

Prefer registry-backed commands over freehand reconstruction of execution order.

## Editing / Governance

- Keep changes bounded and coherent.
- Do not create documentation diaries for micro-steps.
- Record evidence once and reference it elsewhere.
- ADRs are for durable architecture/policy decisions that cross the repository's current ADR threshold; use `DECISION_LOG.md` for ordinary material choices.
- All `.github/prompts/*.prompt.md` files must follow `.github/prompts/PROMPT_STANDARD.md`; internal build prompts are exempt where the standard says so.
- Commit messages must use Conventional Commits.

Repository boundary is explicit: do not inspect, edit, stage, commit, or push another repository unless the user explicitly names that repository and asks for that action.
If the task may require work in another repository, stop and ask for express consent before proceeding.

## Success Test

An agent should be able to answer quickly:

- what is authoritative?
- what are we doing now?
- what context is actually needed?
- what evidence is still valid?
- what changed enough to verify?
- what proves this slice is done?

If answering those requires reading the whole repo or interpreting multiple competing plans, simplify before adding more process.
