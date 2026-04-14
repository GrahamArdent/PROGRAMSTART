# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Stage-gate validation checks for PROGRAMBUILD Stages 0-4: `intake-complete`, `feasibility-criteria`, `requirements-complete`, `architecture-contracts`.
- Per-stage dispatch in `preflight_problems()` — advancing a PROGRAMBUILD stage now runs the corresponding content validation automatically.
- `run_stage_gate_check()` dispatcher in `programstart_validate.py` for stage-gate content checks.
- Five collaborative shaping prompts for Stages 0-4: `shape-idea`, `shape-feasibility`, `shape-research`, `shape-requirements`, `shape-architecture`.
- 36 new tests across 4 test files for stage-gate validators.
- 3 integration tests for the `preflight_problems → stage-gate dispatch → validator` chain: dispatch fires for programbuild (field-level assertions), skips for userjourney, and advance blocks with real validator output.

### Fixed

- `preflight_problems()` was returning `None` due to dead code trapped inside `_check_challenge_gate_log()` — restored full body with real checks.
- Monkeypatch lambda arity in advance tests updated for new `active_step` parameter.

### Changed

- `.editorconfig` for consistent IDE settings.
- `.gitattributes` for cross-platform line-ending normalization.
- `SECURITY.md` vulnerability disclosure policy.
- `CONTRIBUTING.md` contributor guide.
- `CODEOWNERS` file for PR routing.
- `CHANGELOG.md` (this file).
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
- Authority-sync validation for canonical docs, file index, sync rules, and workflow guidance.
- Planning-reference validation for USERJOURNEY code-touch paths and external implementation references.
- Shared dashboard command registry so the web dashboard and unified CLI do not maintain separate workflow command maps.
- Aggregate `nox -s ci` gate for local parity with the major CI checks.
- Registry-driven integrity baselines for backup snapshot comparison and USERJOURNEY attachment manifests.
- Explicit allowlisting for external USERJOURNEY implementation references.

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
