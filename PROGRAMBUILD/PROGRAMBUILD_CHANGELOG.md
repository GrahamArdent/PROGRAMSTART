# PROGRAMBUILD_CHANGELOG.md

# Program Build Changelog

Tracks changes to the reusable PROGRAMBUILD system itself.

---

## 2026-04-11 (Phase 7 — Security Hardening)

- replaced 14 hardcoded npm package versions with semver ranges in starter scaffold (T1)
- added Data Grounding Rule to 5 prompts that read user-authored planning docs (T2)
- capped signoff_history at 100 entries with FIFO trim in save_workflow_signoff and advance_workflow_with_signoff (T3)
- replaced `.parents` path traversal check with `is_relative_to()` in get_doc_preview (T7)
- added `agent: "agent"` frontmatter to product-jit-check.prompt.md (T8)
- pinned all GitHub Actions to commit SHAs across 6 workflow files (T13)
- recorded signoff history cap policy decision as DEC-002 in DECISION_LOG

---

## 2026-04-11 (Phase 4 — Confidence Tiers and Gate Reframe)

- split nox `smoke` session into `smoke_readonly` (read-only root-workspace, safe anytime) and `smoke_isolated` (bootstrapped temp workspaces, mutating) — `smoke` now delegates to both via `session.notify()`
- added `quick` nox session — lint + typecheck only for fast feedback (~10s)
- updated `gate_safe` nox session — now includes `smoke_readonly` for read-only smoke confidence before merge
- updated `nox.options.sessions` default list to `smoke_readonly` + `smoke_isolated`
- added VS Code tasks: `Quick Check`, `Read-only Smoke`, `Isolated Smoke`, `Package Smoke`
- updated `Safe Gate` VS Code task to use `nox -s gate_safe` instead of inline session list
- added "Quality Gates — Confidence Tiers" section to README.md documenting the 3-tier model
- updated QUICKSTART.md nox command reference to reflect new session structure
- fixed `validate_bootstrap_assets` — userjourney test files are now skipped when USERJOURNEY is absent (fixes `test_bootstrap_repo_stays_programbuild_only`)
- created `.github/prompts/implement-gameplan-phase4.prompt.md` execution prompt
- smoke diagnostic output reviewed — both readonly and CLI smoke already produce actionable `[PASS]/[FAIL]` output per check with URLs, status codes, and stderr excerpts

---

## 2026-04-11 (Phase 3 — Deferred Automation: Repo Check, ADR Coverage, Staleness)

- created `scripts/programstart_repo_clean_check.py` — git working-tree cleanliness helper with `capture_git_status()`, `assert_repo_clean()`, `assert_repo_unchanged()`, and CLI entry point
- added 10 tests in `tests/test_programstart_repo_clean_check.py`
- added P3 cross-stage validation advisory to `programstart advance` — at stage 3+ prints a reminder to run the cross-stage validation prompt; suppressed by `--skip-cross-stage-check`
- added 3 cross-stage advisory tests in `tests/test_programstart_workflow_state.py`
- added `programstart validate --check adr-coverage` — parses DECISION_LOG.md Decision Register and warns when ACTIVE/ACCEPTED decisions have no corresponding ADR in `docs/decisions/`
- added 6 ADR coverage tests in `tests/test_programstart_validate.py`
- added P8 re-entry staleness detection to `programstart status` — warns when last signoff date is >28 days old, escalates at >56 days; suppressed by `--skip-staleness-check` or `PROGRAMSTART_SKIP_STALENESS=1`
- added 6 staleness tests in `tests/test_programstart_status.py`
- created `.github/prompts/implement-gameplan-phase3.prompt.md` execution prompt

---

## 2026-04-11 (Phase 2 — Architecture Alignment and Implementation Sync)

- added Part H (Architecture and Requirements Alignment) to `PROGRAMBUILD_CHALLENGE_GATE.md` with 6 questions checking ARCHITECTURE.md contracts, REQUIREMENTS.md feasibility, USER_FLOWS.md integrity, and DECISION_LOG.md currency
- updated Challenge Gate log header, variant table, prompt template, and re-entry protocol to reference 8 parts
- created `.github/prompts/product-jit-check.prompt.md` — reusable pre-coding alignment prompt against product authority docs
- added `architecture_decision_alignment` sync rule binding ARCHITECTURE.md → DECISION_LOG.md (non-blocking, advisory)
- added `requirements_test_alignment` sync rule binding REQUIREMENTS.md → TEST_STRATEGY.md (blocking)
- added Challenge Gate log entry check to `programstart advance` — warns when no gate log row matches the current stage transition, with `--skip-gate-check` bypass flag
- added 4 tests for Challenge Gate log check in `test_programstart_workflow_state.py`

---

## 2026-04-11 (Phase 1.5 — Gate-Safe Session and Read-Only Route Guard)

- added `gate_safe` nox session (lint, typecheck, tests, validate, docs) as local pre-merge confidence gate
- added `PROGRAMSTART_READONLY` environment variable guard to `serve.py` — when set, all POST endpoints return 405
- added readonly mode integration tests to `test_serve_endpoints.py` (5 endpoints covered)
- created `.github/prompts/implement-gameplan-phase2.prompt.md` execution prompt for Phase 1.5 + Phase 2

---

## 2026-04-11 (Phase 1 — Product-JIT and Automation Hardening)

- added ARCHITECTURE.md, REQUIREMENTS.md, USER_FLOWS.md to `implementation_loop.files` in `config/process-registry.json` so `programstart guide` surfaces product authority docs during implementation
- added 3 product authority rows (architecture, requirements, user flows) to `source-of-truth.instructions.md` authority table
- added new "Product-level JIT during implementation" section to `source-of-truth.instructions.md` with re-read-before-each-feature rules
- added 3 product-JIT lines to `.github/copilot-instructions.md` Workflow Expectations
- added task 6 (implementation product-doc reminder) to `programstart-stage-guide.prompt.md`
- created `scripts/programstart_dashboard_smoke_readonly.py` — read-only dashboard smoke exercising only GET endpoints, safe against root workspace
- wired `programstart drift` before and after the validate chain in `noxfile.py` validate session
- added `programstart drift` to `run_next()` in `scripts/programstart_cli.py` so `programstart next` includes drift
- added `guide --system userjourney` and `drift` to `scripts/programstart_cli_smoke.py` checks
- added Drift Check, JIT Check, and Safe Gate tasks to `.vscode/tasks.json`
- added `.tmp_factory_smoke` and `.tmp_nox_factory_smoke` cleanup targets to `noxfile.py` clean session
- recorded smoke safety policy as DEC-001 in DECISION_LOG.md
- created `.github/prompts/implement-gameplan-phase1.prompt.md` implementation prompt
- updated QUICKSTART.md day-to-day loop to include drift before and after editing
- added VS Code tasks reference table to README.md validation section

---

## 2026-04-11 (Automation Gate Authority Registration)

- added `noxfile.py` and `.vscode/tasks.json` to `PROGRAMBUILD_CANONICAL.md` authority map as canonical owners for automation gate definitions and editor task surface respectively
- added `noxfile.py` and `.vscode/tasks.json` to `PROGRAMBUILD_FILE_INDEX.md` Section 3 (Tooling and Enforcement Files) with purpose descriptions
- added `automation_gate_jit_alignment` sync rule to `config/process-registry.json` binding `noxfile.py`, `.vscode/tasks.json`, and `source-of-truth.instructions.md` as a coherent JIT automation bundle; dependent files are `copilot-instructions.md`, `QUICKSTART.md`, and `README.md`

---

## 2026-03-31 (Phase 4 — Self-Audit Fixes)

- fixed `PROGRAMBUILD.md` Section 1 "How To Use" to start with Idea Intake as the first step, not the inputs block
- added Idea Intake, Challenge Gate, and Gameplan to the control files list at the top of `PROGRAMBUILD.md`
- added all three new control files to the "Required critical files" list in `PROGRAMBUILD.md` Section 4
- replaced the stale 9-agent subagent table in `PROGRAMBUILD.md` with the 5-agent model matching `PROGRAMBUILD_SUBAGENTS.md`
- added Idea Intake, Challenge Gate, and Gameplan references to the Authority sections of `PROGRAMBUILD_LITE.md`, `PROGRAMBUILD_PRODUCT.md`, and `PROGRAMBUILD_ENTERPRISE.md`
- replaced stale subagent tables in all three variant files to match the consolidated agent model
- added Idea Intake challenge step and per-stage Challenge Gate items to `PROGRAMBUILD_KICKOFF_PACKET.md`
- fixed `DECISION_LOG.md` template to match Challenge Gate Part F reversal format: added `Replaces` column, updated status vocabulary to PROPOSED / ACTIVE / REVERSED / SUPERSEDED
- fixed `PROGRAMBUILD_CHECKLIST.md` gate log table from 6-column format to 10-column Challenge Gate format
- added the missing Stage 0 → Stage 1 gate to `PROGRAMBUILD_CHECKLIST.md` (was collapsed into one entry)
- moved the Idea Intake → Stage 0 gate into Setup section; Feasibility section now correctly starts with Stage 0 → Stage 1
- updated last-updated dates on Lite, Product, Enterprise, Kickoff Packet, Checklist, and Decision Log

## 2026-03-31 (Phase 3 — Gap Fixes: Decision Reversal, Re-Entry, Dependency Health, Template Feedback, Estimation)

- added Part F (Decision Reversal Check) to `PROGRAMBUILD_CHALLENGE_GATE.md` with REVERSED/SUPERSEDED status model and reconciliation rules
- added Part G (Dependency and KB Health Check) to `PROGRAMBUILD_CHALLENGE_GATE.md` wired into KB `supersedes_for_new_work` and research delta system
- added Re-Entry Protocol to `PROGRAMBUILD_CHALLENGE_GATE.md` for projects resuming after a significant pause
- added Template Improvement Review to `PROGRAMBUILD_GAMEPLAN.md` Stage 10 with lesson-type-to-target mapping table and mandatory-update rule for 3+ recurring lessons
- added KB dependency health checks to `PROGRAMBUILD_GAMEPLAN.md` Stages 4, 7, and 8
- added T-shirt estimation method and per-area sizing table to `FEASIBILITY.md` template
- added template improvement proposals to Stage 17 prompt in `PROGRAMBUILD.md`
- added KB dependency hygiene and decision reversal discipline to `PROGRAMBUILD.md` Section 18 (Operating Practices)
- updated `programstart-stage-transition.prompt.md` to reference Parts F and G and the Re-Entry Protocol
- updated `PROGRAMBUILD_CHECKLIST.md` with new items for Challenge Gate, KB check, decision reversals, purpose test enforcement, template review, and Re-Entry Protocol

## 2026-03-31 (Phase 2 — Gap Fixes: Idea Intake, Challenge Gate, Gameplan, Purpose Tests, Cross-Stage Validation)

- created `PROGRAMBUILD_IDEA_INTAKE.md`: 7-question structured challenge interview that runs before the inputs block
- created `PROGRAMBUILD_CHALLENGE_GATE.md`: 5-part (expanded to 7) stage-transition checklist preventing silent drift, scope creep, and assumption rot
- created `PROGRAMBUILD_GAMEPLAN.md`: chained execution sequence connecting every stage to its prompt, inputs, validation checks, and outputs
- added purpose test and theatre test definitions, litmus test, enforcement rules, and template to `TEST_STRATEGY.md`
- added `PROGRAMBUILD_IDEA_INTAKE.md`, `PROGRAMBUILD_CHALLENGE_GATE.md`, and `PROGRAMBUILD_GAMEPLAN.md` to `PROGRAMBUILD_CANONICAL.md` authority map
- added the three new control files to `PROGRAMBUILD_FILE_INDEX.md`
- added all three new files, new prompts, and stage-transition workflow guidance to `config/process-registry.json`
- created `.github/prompts/programstart-cross-stage-validation.prompt.md`
- created `.github/prompts/programstart-stage-transition.prompt.md`



## 2026-03-29

- added a scheduled full CI gate workflow to run the heavier nox-based quality lane outside normal PR and push validation
- implemented the three core PROGRAMBUILD specialist roles as workspace agents in `.github/agents/`
- clarified in repository docs that `USERJOURNEY/` remains an optional reference attachment and is not required for every bootstrapped project
- hardened workflow caching and artifact capture, normalized agent/workflow line endings, and reduced bootstrapped nox smoke noise in CI
- adjusted drift policy so `PROGRAMBUILD_CHANGELOG.md` entries do not require concurrent canonical or file-index edits unless authority or inventory actually changes
- added a one-shot `programstart create` factory flow, bootstrapped project-level readiness policy, runtime compatibility smoke coverage, and CodeQL scanning

---

## 2026-03-27

- established PROGRAMBUILD and USERJOURNEY as separate systems with registry-backed validation and drift checks
- added `pb.ps1` PowerShell wrapper and `STATUS_DASHBOARD.md` generation
- added `DECISION_LOG.md` and `POST_LAUNCH_REVIEW.md` as standard PROGRAMBUILD outputs
- added ADR template guidance, gate sign-off log, requirements traceability, external dependency review, and post-launch review stage
- clarified variant-aware expectations so lite, product, and enterprise processes keep different evidence levels

---

Last updated: 2026-03-31
