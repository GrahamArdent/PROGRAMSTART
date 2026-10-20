"""Lean greenfield bootstrap for projects that need PROGRAMBUILD methodology, not the factory toolchain.

The normal PROGRAMSTART bootstrap remains available for projects that intentionally want the
self-contained dashboard, scripts, tests, and workflow tooling. This path reuses the canonical
PROGRAMBUILD controls/state/output stubs while keeping those factory-development assets in the
PROGRAMSTART repository where they belong.
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .programstart_bootstrap import (
        bootstrap_programbuild,
        ensure_external_project_repo,
        initialize_git_repository,
        write_file,
        write_project_agent_entry,
    )
    from .programstart_common import load_registry, warn_direct_script_invocation
    from .programstart_target import prepare_target_control_plane
except ImportError:
    from programstart_bootstrap import (
        bootstrap_programbuild,
        ensure_external_project_repo,
        initialize_git_repository,
        write_file,
        write_project_agent_entry,
    )
    from programstart_target import prepare_target_control_plane

    from programstart_common import load_registry, warn_direct_script_invocation


def write_methodology_readme(destination_root: Path, project_name: str, variant: str, dry_run: bool) -> None:
    readme_content = (
        f"# {project_name}\n\n"
        "This standalone project repository was bootstrapped from PROGRAMSTART using the "
        "methodology-only greenfield path.\n\n"
        "Included system:\n\n"
        f"- PROGRAMBUILD variant: {variant}\n"
        "- PROGRAMBUILD control documents, workflow state, and blank project-output stubs\n"
        "- lightweight process registry, managed workflow prompts, and sync manifest for external PROGRAMSTART control\n"
        "- USERJOURNEY: not attached; add it only if onboarding, consent, or activation work requires it\n"
        "\n"
        "Deliberately not vendored:\n\n"
        "- PROGRAMSTART dashboard and factory implementation\n"
        "- PROGRAMSTART's own scripts, test suite, and development toolchain\n"
        "- template CI/research workflows\n"
        "\n"
        "The project owns its application stack, tests, CI, security configuration, and deployment choices. "
        "PROGRAMSTART can operate on this checkout from its central runtime with "
        "`programstart target --repo <path> <command>`. Keep one project execution spine "
        "and load PROGRAMBUILD context just in time.\n"
    )
    readme_content += """

## Reproduce the methodology runtime

Use an accepted PROGRAMSTART source checkout pinned to its full commit SHA; retain
that SHA in the project decision log. The source checkout supplies the methodology
assets as well as the CLI. A bare `programstart` command on PATH is not required.
Use the Python version in that checkout's `.python-version` (currently 3.12), Git,
and a recorded uv version from an approved installation source. Record platform,
Python/uv versions and the `uv.lock` identity with setup evidence.

Replace both absolute paths below with your actual runtime and project locations:

```bash
export PROGRAMSTART_RUNTIME=/absolute/path/to/pinned/PROGRAMSTART
export PROJECT_ROOT=/absolute/path/to/this/project
(cd "$PROGRAMSTART_RUNTIME" && uv sync --frozen --no-dev)
(cd "$PROGRAMSTART_RUNTIME" && uv run --frozen --no-dev programstart doctor --profile runtime)
(cd "$PROGRAMSTART_RUNTIME" && uv run --frozen --no-dev programstart target --repo "$PROJECT_ROOT" status)
(cd "$PROGRAMSTART_RUNTIME" && uv run --frozen --no-dev programstart target --repo "$PROJECT_ROOT" guide --system programbuild)
```

Run from the runtime checkout as shown; do not infer runtime location from the
project's working directory. Runtime doctor checks the methodology environment,
not application readiness. The default development profile additionally checks
PROGRAMSTART factory tools. A missing required tool fails readiness; fix the
reported prerequisite through the approved setup route and repeat the check.

## Project environment contract

Before implementation, retain the selected application environment in existing
REQUIREMENTS, ARCHITECTURE, DECISION_LOG and TEST_STRATEGY owners. For each needed
tool record purpose, required/optional status, supported platform/version,
installation source, manifest/lock/config owner, and exact setup and verification
commands. Verify a fresh environment and retain results. Lock dependencies and
formatter settings where the selected ecosystem supports them; record exceptions.
Python and Node are application choices. Prettier applies when the chosen stack
needs it; Python format/lint tools apply when Python is selected. Do not add tools,
a package manifest or services merely because they are available. Application
format/lint/test/build commands remain unselected until the project owns them.

If a route fails, inspect current Paths and admitted alternatives, including local
execution when available. Record route-specific prerequisites and failure evidence;
preserve permission, effect and repository boundaries when rerouting. A hosted
quota failure alone does not prove the objective is blocked on every route.
"""
    write_file(destination_root / "README.md", readme_content, dry_run)


def bootstrap_methodology_repository(
    destination_root: Path,
    *,
    project_name: str,
    variant: str,
    dry_run: bool = False,
    force: bool = False,
) -> None:
    registry = load_registry()
    ensure_external_project_repo(destination_root)
    if destination_root.exists() and any(destination_root.iterdir()) and not force:
        raise FileExistsError("Destination exists and is not empty. Use --force to continue.")

    write_methodology_readme(destination_root, project_name, variant, dry_run)
    bootstrap_programbuild(destination_root, registry, variant, dry_run)
    prepare_target_control_plane(
        destination_root,
        project_name=project_name,
        variant=variant,
        mode="methodology_only_greenfield",
        dry_run=dry_run,
    )
    write_project_agent_entry(
        destination_root, project_name=project_name, variant=variant, external_runtime=True, dry_run=dry_run
    )
    initialize_git_repository(destination_root, dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a lean PROGRAMBUILD project repo without vendoring PROGRAMSTART's factory toolchain."
    )
    parser.add_argument("--dest", required=True, help="Destination directory for the new project repo.")
    parser.add_argument("--project-name", required=True, help="Project name to stamp into the generated README.")
    parser.add_argument("--variant", choices=["lite", "product", "enterprise"], default="product")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    destination_root = Path(args.dest).resolve()
    try:
        bootstrap_methodology_repository(
            destination_root,
            project_name=args.project_name,
            variant=args.variant,
            dry_run=args.dry_run,
            force=args.force,
        )
    except (FileExistsError, RuntimeError, ValueError) as exc:
        print(str(exc))
        return 1

    print(f"Methodology-only bootstrap complete for {args.project_name} at {destination_root}")
    return 0


if __name__ == "__main__":
    warn_direct_script_invocation("'python scripts/programstart_bootstrap_methodology.py'")
    raise SystemExit(main())
