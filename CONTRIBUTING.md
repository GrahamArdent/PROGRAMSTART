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
3. Run the full check suite:
   ```bash
   nox
   ```
4. Submit a pull request with a clear description.

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
| Full local gate| `nox -s ci`                                   |
| All (via Nox)  | `nox`                                         |

## Pull Request Checklist

- [ ] Tests pass locally (`nox`).
- [ ] New code has tests.
- [ ] Documentation updated if behaviour changed.
- [ ] No unrelated changes included.
