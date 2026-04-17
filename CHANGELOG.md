# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Features

- `programstart prompt-build --mode context` (Mode B): generates structured `.prompt.md` from arbitrary `--context key=value` pairs without requiring a bootstrapped PROGRAMBUILD project (ADR-0021, DEC-018).
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
