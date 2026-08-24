# Project Guidelines

## Repository Role

This repository is a documentation-first planning and delivery system.
It contains two reusable workflows:

- `PROGRAMBUILD/` for project intake, scope, architecture, testing, bounded implementation, release readiness, audit, and learning
- `USERJOURNEY/` for signup, onboarding, consent, activation, analytics, and first-run routing design

The machine-readable workflow rules live in `config/process-registry.json`.
When a task is about planning, execution order, document authority, drift, or “what should we do next,” prefer the registry and scripts in `scripts/` over conversational memory.

## Workflow Expectations

- Read `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md`, `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md`, and `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` before changing PROGRAMBUILD control behavior.
- Preserve one strategic execution spine per real project. Research, audits, readiness reviews, checklists, and `CURRENT_WORK_PACKET.md` are evidence or derived execution aids unless explicitly adopted into canonical authority.
- For an existing/in-flight project, identify its current canonical roadmap/game plan before proposing new planning artifacts. Prefer explicit deltas to that authority over another master plan.
- Read `USERJOURNEY/DELIVERY_GAMEPLAN.md` before changing USERJOURNEY execution order or synchronization rules.
- Update canonical owner files before dependent files when a concern changes.
- Do not invent legal, consent, route, activation, product-scope, or architecture behavior in downstream docs without updating the authority owner first.
- Treat `first_value_achieved` as the canonical USERJOURNEY activation event unless its source-of-truth docs explicitly change.
- During implementation (Stage 7), establish the stage baseline with registry guidance, then narrow the current task using `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` when the slice is non-trivial.
- Re-read the exact applicable contracts in `PROGRAMBUILD/ARCHITECTURE.md`, requirement IDs/acceptance criteria in `PROGRAMBUILD/REQUIREMENTS.md`, and only the flow/decision sections relevant to the current slice. Do not implement from conversation memory, but do not re-read every planning file for every small task.
- If implementation design prospectively contradicts `ARCHITECTURE.md`, update `ARCHITECTURE.md` first. If a new contract, endpoint, or auth rule is needed, record the material decision and update architecture authority before implementing it.
- Reuse trustworthy prior verification until a documented invalidation trigger occurs. Re-run the smallest verification set that proves the changed or at-risk surface; widen verification again at stage transitions, periodic convergence reviews, and release gates.

## Preferred Automation

- Use `scripts/programstart_status.py` to summarize current strategic stage, blockers, and next actions.
- Use `scripts/programstart_step_guide.py` to identify the authoritative baseline files, scripts, and prompts for kickoff and stage-specific work.
- Treat guide output as the allowed stage context, not an instruction to fully load every listed file for every subtask.
- Use `scripts/programstart_workflow_state.py` to inspect or advance the active stage/phase instead of editing state files manually.
- Use `scripts/programstart_bootstrap.py` to create a new planning package instead of hand-copying files.
- Use `scripts/programstart_validate.py` for required validation and convergence gates.
- Use `scripts/programstart_drift_check.py` before/after planning-authority or registry changes and when source-of-truth drift is suspected.
- Use `scripts/programstart_refresh_integrity.py` to regenerate the manifest and verification report.

## Editing Rules

- Preserve the existing metadata block pattern in planning documents.
- Keep changes minimal and consistent with the authority model already documented in the repo.
- If a task changes workflow rules, update the registry/config fragment and relevant markdown authority in the same change.
- Repository boundary is explicit: do not inspect, edit, stage, commit, or push another repository unless the user explicitly names that repository and asks for that action.
- If the task may require work in another repository, stop and ask for express consent before proceeding.
- For new-project kickoff or stage-by-stage guidance, prefer registry-backed scripts and prompt files over freehand step ordering from chat memory.
- The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in authority docs are interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).
- Commit messages MUST follow Conventional Commits format: `<type>[optional scope]: <description>` — valid types are `feat`, `fix`, `docs`, `chore`, `ci`, `refactor`, `test`. Include `BREAKING CHANGE:` footer for schema changes, stage renames, or required-file renames.
- Significant architectural or policy decisions MUST be recorded as MADR decision records in `docs/decisions/` using `PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md` when the ADR threshold is met.
- When an ADR is superseded, the same change set MUST update the ADR frontmatter, `docs/decisions/README.md`, and any affected `PROGRAMBUILD/DECISION_LOG.md` row.
- All `.prompt.md` files in `.github/prompts/` MUST conform to `.github/prompts/PROMPT_STANDARD.md`. Internal build prompts in `.github/prompts/internal/` are exempt.

## Source-of-Truth Protocol (JIT)

Apply the task-scoped JIT protocol from `.github/instructions/source-of-truth.instructions.md`:

1. **Establish the stage baseline now** — run `programstart guide --system <system>`; do not rely on memory.
2. **Narrow the current slice** — for non-trivial PROGRAMBUILD implementation work, derive/refresh `CURRENT_WORK_PACKET.md` from `PROGRAMBUILD_WORK_PACKET.md`; name objective, non-goals, exact authority sections, specialist references, reusable evidence, invalidation triggers, acceptance criteria, and targeted verification.
3. **Baseline authority changes** — run `programstart drift` before changing planning authority or registry policy; resolve existing drift before adding a new authority change.
4. **Canonical before dependent** — identify the concern owner, update it first, then derive dependent changes.
5. **Verify proportionally** — planning/registry authority changes use full validation + drift; bounded implementation uses targeted verification plus any broader checks made necessary by invalidation or a convergence gate.
6. **Reconcile and close** — record evidence and material decisions in canonical project state, then replace/close the packet instead of accumulating a second planning hierarchy.

Never assert what an authority doc says from memory. Never update a dependent before its authority file. Never treat a work packet or research artifact as a competing master plan. Never repeat broad verification without an invalidation reason or required convergence gate. Use the `propagate-canonical-change` prompt when an authority doc changes and has registered dependents.
