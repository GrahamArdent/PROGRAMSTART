# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added deterministic dependency-graph primitives for typed prerequisite/dependent traversal, stable topological ordering, cycle reporting, blocker eligibility, and bounded provenance-preserving impact paths.
- Added immutable evidence-invalidation primitives that reuse verification evidence until an explicitly changed or graph-impacted scope/dependency invalidates it; evidence age remains metadata rather than an automatic expiry rule.
- Added a PROGRAMSTART-only `workflow_dispatch` manual convergence gate so full `nox -s ci` validation is available on demand without restoring push, PR, cron, or nightly CI noise.
- Extended `programstart impact` with deterministic dependency blast-radius paths over `depends_on` and `authority_dependency`, including start-node resolution, path provenance, machine-readable output, and optional `--max-depth` traversal bounds while preserving existing related-record discovery.
- Added `programstart-adopt` for non-destructive Mode-C adoption of PROGRAMBUILD into an existing repository. Adoption preserves the host engineering toolchain, adds only PROGRAMBUILD management/output surfaces plus workflow prompts and a project registry, and tracks only reusable methodology files in the sync manifest so project state and project outputs are never overwritten by template sync.
- Added `programstart target --repo <path> ...` so the central PROGRAMSTART runtime can operate status, guide, adaptive decision routing, JIT/drift, progress, prompt generation, state inspection/snapshots, and target-local validation against a lightweight external project checkout without vendoring PROGRAMSTART's scripts/dashboard/tests into that project.
- Added `programstart orchestrate` and an environment-aware orchestration prompt that convert a plain-language request into a bounded PROGRAMSTART execution contract for either local target control or connected repository/runtime tools without creating a second execution spine.

### Changed

- Added the PROGRAMBUILD planning operating model and bounded work-packet standard, including one-strategic-execution-spine authority, proportional rigor, task-scoped/JIT context loading, evidence reuse with invalidation triggers, and research-to-plan delta handling (ADR-0023 / DEC-020).
- Updated workflow guidance, prompts, registry metadata, canonical documentation, Challenge Gate behavior, and Stage 7/8 execution semantics to narrow during implementation and widen at meaningful convergence gates.
- Made status staleness and cross-system distance warnings explicitly non-authoritative heuristics; elapsed time or ordinal distance alone no longer implies that evidence is invalid or that re-entry is required.
- Simplified PROGRAMBUILD execution surfaces around navigator-first startup (`status` / `guide`), compact logical work packets by default, stage/risk-aware Product Challenge Gates, on-demand specialist agents, and targeted verification driven by invalidation rather than ritual.
- Reduced duplicated operational prose across the Gameplan, Checklist, Quick Start, JIT instructions, Product variant, and algorithm launcher so detailed methodology remains in its canonical owner instead of being reloaded or recopied everywhere.
- Changed generated-project `full-ci-gate.yml` to manual-only by default; projects may add automatic triggers when their own operating needs justify the cost.
- Added a machine-readable Lite artifact profile so `RISK_SPIKES.md` and `AUDIT_REPORT.md` remain reusable compatibility stubs without becoming mandatory operator work; JIT guidance, status, and the preferred `programstart advance` path now use explicit conditional-artifact activation while preserving legacy body-content fallback for older repos.
- Changed methodology-only greenfield bootstrap to include only the lightweight control surface required by the external PROGRAMSTART runtime: a flat project registry, managed workflow prompts, and sync manifest. The PROGRAMSTART executable runtime, dashboard, development tests/toolchain, and template workflows remain centralized and are still not vendored.

### Fixed

- Preserved the six intentionally inactive GitHub Actions definitions as dormant `templates/github-workflows/` sources. Bootstrap and PROGRAMBUILD attach materialize them into `.github/workflows/` in standalone project repositories, and downstream sync resolves those canonical project paths back to the dormant template sources. This restores bootstrap-asset validation without re-enabling recurring Actions in the PROGRAMSTART template repository.
- Corrected stale broad-JIT prompt-standard rules, Lite Challenge Gate minimums, decision-reversal examples, Product JIT verification-section structure, checklist gate columns, and several rigid numeric/calendar rules that conflicted with proportional-risk planning.
- Removed remaining universal feature/file/project/time/agent-count heuristics from active PROGRAMBUILD guidance where they had started acting like policy rather than optional local reminders.
- Fixed Lite conditional-artifact detection so the instructional headings, placeholder rows, and placeholder bullets in untouched `RISK_SPIKES.md` and `AUDIT_REPORT.md` templates do not falsely activate spike/audit work; new templates use `Activation: dormant|active` metadata and shaping prompts switch it explicitly when real work is warranted.

## [1.0.0] - 2026-04-17

### Features

- `programstart prompt-build --mode context` (Mode B): generates structured `.prompt.md` from arbitrary `--context key=value` pairs without requiring a bootstrapped PROGRAMBUILD project (ADR-0021, DEC-018).
- `programstart sync --from-template <path>` pull mode: copies changed files from an upstream PROGRAMSTART template into the current (or `--dest`) repo; bidirectional sync story now complete (ADR-0022, DEC-019).
- `programstart sync --dest <path>` command: propagates changed PROGRAMSTART files to a downstream repo using a manifest written at attach time; dry-run by default, `--confirm` to apply (ADR-0020, DEC-017).
- `.programstart-manifest.json` written during `programstart attach programbuild` with file list, source commit hash, and timestamp.
- `.programstart-preserve` file support for downstream repos to declare additional files protected from sync.

## [0.9.0] - 2026-04-17

### Features

- `programstart jit-check` command: wraps `guide` + `drift` + sync-rule summary into a single JIT source-of-truth protocol entry point (ADR-0017).
- `programstart advance --defer` flag: marks the active step as intentionally paused without advancing; staleness detection uses the deferred date (ADR-0018).
- `programstart prompt-build` command: generates a stage-specific `.prompt.md` file from the process registry (`--stage`, `--output`, `--eject`, `--list-stages`, `--json` flags).
- `programstart doctor` command: environment health checks for PATH, Python version, uv, and key dependencies.
- Typed Pydantic models for all 16 process-registry sections via `load_validated_registry()` alongside existing dict API (ADR-0019).
- Split `programstart_validate.py` (1710 lines) into `programstart_validate_core.py` (check implementations) and facade (CLI dispatch).
- Composed process registry from manifest + fragments (`config/registry/`) with stable merged `load_registry()` contract (ADR-0014).
- Separate workflow, operator, and internal prompt architecture with class-aware validation (ADR-0011).
- `lint-prompts` validation check: enforces PROMPT_STANDARD.md compliance rows against all `.prompt.md` files.
- `file-hygiene` validate check: catches stale or untracked planning artefacts.
- Prompt `version` field in frontmatter validated by compliance tests.
- Stage-gate validation checks for PROGRAMBUILD Stages 0–4: `intake-complete`, `feasibility-criteria`, `requirements-complete`, `architecture-contracts`.
- Per-stage dispatch in `preflight_problems()` — advancing a PROGRAMBUILD stage now runs the corresponding content validation automatically.
- Five collaborative shaping prompts for Stages 0–4: `shape-idea`, `shape-feasibility`, `shape-research`, `shape-requirements`, `shape-architecture`.
- DRY consolidation of registry and state helpers with file-locking via `filelock`.
- UI blind spot coverage: dashboard button-flow smoke, missing-route detection.
- JSON schema hardening: added schemas for knowledge-base and prompt-eval-scenarios.
- CI matrix hardening: lockfile check, pip-audit, CHANGELOG enforcement.
- Coverage push: all production modules ≥90% (retrieval ≥88%, mutation ≥80%), aggregate ≥93%.
- Post-advance sanity check, content quality gates, cross-system health warning.
- Recommendation engine companion surfaces: `suggested_companion_surfaces` field, cross-shape UI advisory, `ui_tier()` classifier, admin dashboard scaffold generator.
- 19 ADR decision records documenting significant architecture and policy choices.
- 1752 tests with comprehensive coverage across all modules.

### Fixes

- Dashboard static assets extracted to `dashboard/` (`index.html`, `style.css`, `app.js`); `programstart_serve.py` reduced from ~2450 to ~796 lines.
- Content-Security-Policy header on all HTML responses in the web dashboard.
- `GET /static/<filename>` route in the dashboard server with path-traversal protection.
- `_ensure_scripts_importable()` helper added to `programstart_common.py` to consolidate `sys.path` bootstrap logic across standalone scripts.
- Removed 29 redundant `# type: ignore` annotations from standalone import-fallback blocks across all scripts.
- `preflight_problems()` was returning `None` due to dead code trapped inside `_check_challenge_gate_log()` — restored full body with real checks.
- Monkeypatch lambda arity in advance tests updated for new `active_step` parameter.
- Narrow exception handlers and subprocess timeouts for robustness.

### Automation

- `.editorconfig` for consistent IDE settings.
- `.gitattributes` for cross-platform line-ending normalization.
- Dependabot configuration for automated dependency updates.
- Security scanning with Bandit and pip-audit in CI, Nox, and pre-commit.
- Secret detection with detect-secrets in pre-commit.
- YAML linting with yamllint in pre-commit.
- GitHub issue templates (bug report, feature request) and PR template.
- Nox sessions: `security`, `format_code`, `audit`, `clean`.
- CI caching for pre-commit and uv.
- Coverage report artifact upload in CI.
- CLI entry points in `pyproject.toml`.
- Pre-commit verification for bootstrapped repos in Nox and CI.
- Direct-script deprecation warnings for legacy `python scripts/programstart_*.py` entry paths.
- Unified CLI smoke automation for source and bootstrapped repos.
- Built wheel artifact upload and install smoke verification in CI.
- Packaged install support that resolves the planning workspace from the current directory or `PROGRAMSTART_ROOT`.
- Aggregate `nox -s ci` gate for local parity with the major CI checks.

### Docs

- `SECURITY.md` vulnerability disclosure policy.
- `CONTRIBUTING.md` contributor guide with updated coverage target (90%).
- `CODEOWNERS` file for PR routing.
- Authority-sync validation for canonical docs, file index, sync rules, and workflow guidance.
- Planning-reference validation for USERJOURNEY code-touch paths and external implementation references.
- Shared dashboard command registry so the web dashboard and unified CLI do not maintain separate workflow command maps.
- Registry-driven integrity baselines for backup snapshot comparison and USERJOURNEY attachment manifests.
- Explicit allowlisting for external USERJOURNEY implementation references.
- MkDocs nav updated with Decisions section.
- QUICKSTART.md cross-platform improvements.

## [0.1.0] - 2026-03-27

### Added

- Initial release of PROGRAMSTART workflow platform.
- PROGRAMBUILD planning system with 11 stages and 3 variants (lite, product, enterprise).
- USERJOURNEY planning system with 9 phases.
- Python toolchain: uv, Ruff, Pyright, pre-commit, pytest, coverage, Nox, MkDocs.
- JSON schemas for process registry, PROGRAMBUILD state, and USERJOURNEY state.
- Bootstrap script for generating new planning packages.
- HTTP dashboard server with API and browser smoke tests.
- CI pipeline with Windows/Linux matrix.
- Drift detection for authority/dependent file synchronization.
