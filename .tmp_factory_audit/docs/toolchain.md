# Toolchain

PROGRAMSTART now includes a reproducible hardening toolchain:

- `uv` for environment and dependency locking
- `Ruff` for linting and formatting
- `Pyright` for static typing
- `pre-commit` for local enforcement
- `check-jsonschema` for workflow/state schemas
- `pytest` and `coverage.py` for automated verification
- `Nox` for repeatable local sessions
- `Material for MkDocs` for searchable documentation

Primary entry points:

- `uv sync --extra dev`
- `uv run programstart help`
- `uv build`
- `pre-commit run --all-files`
- `nox`
- `nox -s ci`
- `mkdocs build --strict`

Preferred workflow commands now route through the unified CLI:

- `uv run programstart status`
- `uv run programstart validate --check all`
- `uv run programstart state show`
- `uv run programstart guide --system programbuild`
- `uv run programstart advance --system programbuild --dry-run`

Distribution verification is automated too:

- `uv run python scripts/programstart_cli_smoke.py --workspace .`
- `nox -s package`
- `uv run programstart validate --check authority-sync`
- `uv run programstart validate --check planning-references`
- `python -m pip install dist\programstart_workflow-*.whl`

Installed commands resolve the active planning workspace from the current directory. If needed, set `PROGRAMSTART_ROOT` to point at a different planning repo.
