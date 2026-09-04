# Contributing to PROGRAMSTART

Thank you for your interest in contributing! This guide explains how to get started.

## Quick Setup

```bash
git clone <repo-url> && cd PROGRAMSTART
uv sync --extra dev
pre-commit install
uv run python scripts/install_hooks.py
python -m playwright install chromium
```

## Development Workflow

1. Create a feature branch from `main`.
2. Make your changes with tests.
3. Before committing, run the repository hooks explicitly:
   ```bash
   uv run pre-commit run --all-files
   ```
   If deterministic hooks modify files, inspect the changes, stage them, and rerun. Autonomous workers may perform at most two deterministic auto-fix passes before stopping for diagnosis rather than looping indefinitely.
4. Commit only after the repository hooks are clean.
5. Before pushing, run the repository-owned local confidence gate:
   ```bash
   uv run nox -s gate_safe
   ```
   The installed `pre-push` hook runs this same gate again before publication.
6. Submit a pull request with a clear description. GitHub Actions remains the independent authoritative verifier.

### Autonomous publication contract

PROGRAMSTART uses one semantic publication sequence, while each repository owns the concrete tools behind its gate:

`edit -> deterministic fix -> local validation -> commit -> pre-push validation -> GitHub verification`

For PROGRAMSTART itself, `pre-commit` owns deterministic hygiene and `nox -s gate_safe` owns the pre-push confidence gate. Other repositories may use different repo-defined commands such as ESLint/Prettier, TypeScript, shell or infrastructure validation, or project-specific contract tests. Do not install a universal toolchain merely to satisfy this sequence.

Git hooks are convenience/enforcement on normal Git CLI paths, not proof that validation happened. Mutation paths that bypass hooks, including direct GitHub/API file writes, MUST run the repository's equivalent validation contract on an executable candidate before publication whenever that capability is available. If no executable validation surface is available, record that limitation and do not claim local validation; GitHub CI remains authoritative.

Deterministic auto-fixes must be inspected and incorporated before publication. Never suppress, waive, or rewrite a semantic/test failure merely to make CI green.

## Code Style

- **Python**: PEP 8, enforced by Ruff (line length 130).
- **Type hints**: All new functions should include type annotations.
- **Commits**: Use conventional commits (`feat:`, `fix:`, `docs:`, `chore:`).
- **Tests**: Maintain 90%+ test coverage (enforced by CI with `fail_under = 90`).

## What to Contribute

- Bug fixes with a regression test.
- Tests for untested scripts.
- Documentation improvements.
- New workflow guidance or templates.

## What to Avoid

- Changing canonical authority files without updating dependents (see `config/process-registry.json` sync rules).
- Adding runtime dependencies unless strictly necessary.
- Modifying `PROGRAMBUILD_CANONICAL.md` or `PROGRAMBUILD_FILE_INDEX.md` without reading them first.

## Devlog Retention

Entries in `devlog/` older than 12 months SHOULD be archived to `devlog/archive/YYYY/`.
They MAY be deleted after archival.

## Running Checks Individually

| Check          | Command                                       |
|----------------|-----------------------------------------------|
| Lint           | `uv run ruff check .`                         |
| Format         | `uv run ruff format --check .`                |
| Type check     | `uv run pyright`                              |
| Tests          | `uv run pytest`                               |
| Docs           | `uv run mkdocs build --strict`                |
| Validation     | `uv run programstart validate --check all`    |
| Authority sync | `uv run programstart validate --check authority-sync` |
| Planning refs  | `uv run programstart validate --check planning-references` |
| Clean preview  | `uv run programstart clean --dry-run`         |
| CLI smoke      | `uv run python scripts/programstart_cli_smoke.py --workspace .` |
| Package smoke  | `nox -s package`                              |
| Pre-push gate  | `uv run nox -s gate_safe`                     |
| Full local gate| `nox -s ci`                                   |
| All (via Nox)  | `nox`                                         |

## Pull Request Checklist

- [ ] Deterministic hooks are clean (`uv run pre-commit run --all-files`).
- [ ] Pre-push confidence gate passes (`uv run nox -s gate_safe`).
- [ ] New code has tests.
- [ ] Documentation updated if behaviour changed.
- [ ] No unrelated changes included.
