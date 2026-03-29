# Verification

PROGRAMSTART verification has two layers:

1. Static checks: linting, type checking, JSON schema validation, metadata validation.
2. Runtime checks: CLI tests, dashboard API smoke, browser smoke, and generated-repo smoke.

The key lesson is that template-only validation is insufficient. The platform must also verify a freshly bootstrapped PROGRAMBUILD-only repository.

Important commands:

- `uv run programstart validate --check all`
- `uv run programstart validate --check authority-sync`
- `uv run programstart validate --check planning-references`
- `uv run programstart validate --check workflow-state`
- `uv run programstart clean --dry-run`
- `uv run programstart refresh --date <YYYY-MM-DD>`
- `uv run python scripts/programstart_cli_smoke.py --workspace .`
- `uv run programstart state show`
- `uv run programstart guide --system programbuild`
- `uv run programstart bootstrap --dest <folder> --project-name <name> --variant product`
- `uv build`
- `uv run python scripts/programstart_dist_smoke.py --dist-dir dist --workspace .`
- `uv run python scripts/programstart_dashboard_smoke.py`
- `uv run python scripts/programstart_dashboard_browser_smoke.py --expect-userjourney attached`
- `uv run python scripts/programstart_dashboard_golden.py --expect-userjourney attached`
- bootstrap a fresh repo, then rerun the same checks with `--expect-userjourney absent`
- `nox -s ci` for a local aggregate gate that mirrors the major CI surfaces

Planning-reference validation is now fail-closed for external paths: if a USERJOURNEY planning doc points at an implementation file outside this workspace, the path must be declared in `USERJOURNEY/USERJOURNEY_INTEGRITY_REFERENCE.json` first.

Integrity refresh is also registry-driven: the script reads its snapshot root and attachment manifest from `config/process-registry.json` instead of relying on a hardcoded backup path.

Manifest collection is now registry-scoped as well: refresh includes the workspace readme, bootstrap assets, declared system files, and configured integrity baselines while excluding temp, generated, and previously emitted integrity artifacts.

Generated operational artifacts now default to `outputs/`: dashboard refresh writes `outputs/STATUS_DASHBOARD.md`, and integrity refresh writes dated manifests and verification reports there as well.

Dashboard visual regression coverage now includes purpose-based Playwright goldens. Run `uv run python scripts/programstart_dashboard_golden.py --update --expect-userjourney attached` to refresh the attached baselines intentionally, and regenerate the absent baseline from a bootstrapped PROGRAMBUILD-only repo when the dashboard visuals are intentionally changed.

CI now uploads any mismatch screenshots from `outputs/golden-failures/` in both the template repo and the bootstrapped repo. That means a failed `process-guardrails` run preserves the actual rendered captures needed to inspect a visual regression without reproducing it locally first.
