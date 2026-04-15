# Project Guidelines

## Repository Role

This repository is a documentation-first planning system.
It contains two reusable workflows:

- `PROGRAMBUILD/` for product kickoff, stage gates, architecture, testing, release readiness, and audit discipline
- `USERJOURNEY/` for signup, onboarding, consent, activation, analytics, and first-run routing design

The machine-readable workflow rules live in `config/process-registry.json`.
When a task is about planning, execution order, document authority, drift, or “what should we do next,” prefer using the registry and the scripts in `scripts/` instead of relying on chat memory.

## Workflow Expectations

- Read `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` and `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md` before changing PROGRAMBUILD control behavior.
- Read `USERJOURNEY/DELIVERY_GAMEPLAN.md` before changing USERJOURNEY execution order or synchronization rules.
- Update canonical owner files before dependent files when a concern changes.
- Do not invent legal, consent, route, or activation behavior in downstream docs without updating the authority docs first.
- Treat `first_value_achieved` as the canonical USERJOURNEY activation event unless the source-of-truth docs explicitly change.
- During implementation (Stage 7+), re-read the applicable contracts in `PROGRAMBUILD/ARCHITECTURE.md` and the relevant requirement in `PROGRAMBUILD/REQUIREMENTS.md` before writing feature code. Do not implement from conversation memory.
- If implementation design contradicts `ARCHITECTURE.md`, update `ARCHITECTURE.md` first. Do not ship code that contradicts an authority doc.
- If you add a new contract, endpoint, or auth rule not documented in `ARCHITECTURE.md`, record it in `DECISION_LOG.md` and update `ARCHITECTURE.md` in the same commit.

## Preferred Automation

- Use `scripts/programstart_status.py` to summarize current stage, blockers, and next actions.
- Use `scripts/programstart_step_guide.py` to identify the authoritative files, scripts, and prompts for kickoff and stage-specific work.
- Use `scripts/programstart_workflow_state.py` to inspect or advance the active stage or phase instead of editing state files manually.
- Use `scripts/programstart_bootstrap.py` to create a new planning package instead of hand-copying files.
- Use `scripts/programstart_validate.py` to check required files and metadata.
- Use `scripts/programstart_drift_check.py` to detect source-of-truth drift.
- Use `scripts/programstart_refresh_integrity.py` to regenerate the manifest and verification report.

## Editing Rules

- Preserve the existing metadata block pattern in planning documents.
- Keep changes minimal and consistent with the authority model already documented in the repo.
- If a task changes workflow rules, update `config/process-registry.json` and the relevant markdown authority file in the same change.
- Repository boundary is explicit: do not inspect, edit, stage, commit, or push another repository unless the user explicitly names that repository and asks for that action.
- If the task may require work in another repository, stop and ask for express consent before proceeding.
- For new-project kickoff or stage-by-stage guidance, prefer registry-backed scripts and prompt files over freehand step ordering from chat memory.
- The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in authority docs (instruction files, PROGRAMBUILD_CANONICAL.md, DELIVERY_GAMEPLAN.md) are interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).
- Commit messages MUST follow Conventional Commits format: `<type>[optional scope]: <description>` — valid types are `feat`, `fix`, `docs`, `chore`, `ci`, `refactor`, `test`. Include `BREAKING CHANGE:` footer for schema changes, stage renames, or required-file renames.
- Significant architectural or policy decisions MUST be recorded as MADR decision records in `docs/decisions/` using `PROGRAMBUILD/PROGRAMBUILD_ADR_TEMPLATE.md` as the template.
- When an ADR is superseded, the same change set MUST update all three surfaces together: the ADR file frontmatter, `docs/decisions/README.md`, and any affected row in `PROGRAMBUILD/DECISION_LOG.md`.
- All `.prompt.md` files in `.github/prompts/` MUST conform to `.github/prompts/PROMPT_STANDARD.md`. Internal build prompts in `.github/prompts/internal/` are exempt.

## Source-of-Truth Protocol (JIT)

Follow this before any planning or documentation task:

1. **Derive context now** — run `programstart guide` to get the minimal file set; read only those files.
2. **Baseline first** — run `programstart drift` before changes; a clean baseline is required.
3. **Canonical before dependent** — identify the authority file in `config/process-registry.json` `sync_rules`; update it first; derive dependent changes from it.
4. **Verify after** — run `programstart validate --check all` and `programstart drift`; both must pass.

Never assert what an authority doc says from memory. Never update a dependent before its authority file. Use the `propagate-canonical-change` prompt when an authority doc changes.
