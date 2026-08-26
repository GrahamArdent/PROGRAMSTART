from __future__ import annotations

"""Lean greenfield bootstrap for projects that need PROGRAMBUILD methodology, not the factory toolchain.

The normal PROGRAMSTART bootstrap remains available for projects that intentionally want the
self-contained dashboard, scripts, tests, and workflow tooling. This path reuses the canonical
PROGRAMBUILD controls/state/output stubs while keeping those factory-development assets in the
PROGRAMSTART repository where they belong.
"""

import argparse
from pathlib import Path

try:
    from .programstart_bootstrap import (
        bootstrap_programbuild,
        ensure_external_project_repo,
        initialize_git_repository,
        write_file,
    )
    from .programstart_common import load_registry, warn_direct_script_invocation
    from .programstart_target import prepare_target_control_plane
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_bootstrap import (
        bootstrap_programbuild,
        ensure_external_project_repo,
        initialize_git_repository,
        write_file,
    )
    from programstart_common import load_registry, warn_direct_script_invocation
    from programstart_target import prepare_target_control_plane


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
        "`programstart target --repo <path> <command>`. Keep one project execution spine and load PROGRAMBUILD context just in time.\n"
    )
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


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'python scripts/programstart_bootstrap_methodology.py'")
    raise SystemExit(main())
