from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from .programstart_attach import MANIFEST_FILENAME
    from .programstart_bootstrap import (
        bootstrap_programbuild,
        copy_file,
        generated_repo_prompt_assets_for_mode,
        generated_repo_prompt_authority_for_mode,
        generated_repo_prompt_registry_for_mode,
    )
    from .programstart_common import (
        load_registry,
        warn_direct_script_invocation,
        workspace_path,
        write_json,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_attach import MANIFEST_FILENAME
    from programstart_bootstrap import (
        bootstrap_programbuild,
        copy_file,
        generated_repo_prompt_assets_for_mode,
        generated_repo_prompt_authority_for_mode,
        generated_repo_prompt_registry_for_mode,
    )
    from programstart_common import (
        load_registry,
        warn_direct_script_invocation,
        workspace_path,
        write_json,
    )


def _git_head_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace_path("."),
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return ""


def _managed_prompt_assets(registry: dict[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(generated_repo_prompt_assets_for_mode(registry, include_userjourney=False)))


def _assert_safe_destination(destination_root: Path, prompt_assets: tuple[str, ...]) -> None:
    if (destination_root / "PROGRAMBUILD").exists():
        raise FileExistsError("PROGRAMBUILD already exists in destination; adoption will not overwrite it.")
    if (destination_root / "config" / "process-registry.json").exists():
        raise FileExistsError(
            "config/process-registry.json already exists in destination; adoption will not overwrite it."
        )
    if (destination_root / MANIFEST_FILENAME).exists():
        raise FileExistsError(
            f"{MANIFEST_FILENAME} already exists in destination; repository may already be linked."
        )

    for relative_path in prompt_assets:
        destination = destination_root / relative_path
        if not destination.exists():
            continue
        source = workspace_path(relative_path)
        try:
            identical = source.read_bytes() == destination.read_bytes()
        except OSError:
            identical = False
        if not identical:
            raise FileExistsError(f"Adoption would overwrite existing project file: {relative_path}")


def _adopted_registry(
    registry: dict[str, Any],
    *,
    project_name: str,
    prompt_assets: tuple[str, ...],
) -> dict[str, Any]:
    adopted = json.loads(json.dumps(registry))

    workspace = dict(adopted.get("workspace", {}))
    workspace.update(
        {
            "repo_role": "existing_project_repo",
            "project_name": project_name,
            "source_template_repo": "PROGRAMSTART",
            "repo_boundary": "standalone_existing_project_repo",
            "provisioning_scope": "programbuild_management_overlay_only",
            "bootstrap_assets": ["config/process-registry.json", *prompt_assets],
        }
    )
    adopted["workspace"] = workspace

    validation = dict(adopted.get("validation", {}))
    validation["enforce_engineering_ready_in_all"] = False
    adopted["validation"] = validation

    integrity = dict(adopted.get("integrity", {}))
    integrity["baselines"] = []
    adopted["integrity"] = integrity

    prompt_registry = generated_repo_prompt_registry_for_mode(registry, include_userjourney=False)
    prompt_authority = generated_repo_prompt_authority_for_mode(registry, include_userjourney=False)
    adopted["prompt_registry"] = prompt_registry
    adopted["prompt_authority"] = prompt_authority

    workflow_guidance = dict(adopted.get("workflow_guidance", {}))
    if not prompt_registry.get("operator_prompt_files"):
        workflow_guidance["operator"] = {}
    adopted["workflow_guidance"] = workflow_guidance

    repo_boundary_policy = dict(adopted.get("repo_boundary_policy", {}))
    repo_boundary_policy["enabled"] = False
    adopted["repo_boundary_policy"] = repo_boundary_policy

    adopted.pop("prompt_generation", None)
    adopted.pop("include", None)
    return adopted


def _write_adoption_manifest(
    destination_root: Path,
    *,
    registry: dict[str, Any],
    project_name: str,
    variant: str,
    prompt_assets: tuple[str, ...],
) -> None:
    state_file = registry["workflow_state"]["programbuild"]["state_file"]
    managed_controls = [
        path for path in registry["systems"]["programbuild"]["control_files"] if path != state_file
    ]
    manifest = {
        "programstart_version": "1.0.0",
        "source_commit": _git_head_hash(),
        "attached_at": datetime.now(UTC).isoformat(),
        "mode": "existing_project_adoption",
        "project_name": project_name,
        "variant": variant,
        "files": sorted([*managed_controls, *prompt_assets]),
    }
    write_json(destination_root / MANIFEST_FILENAME, manifest)


def adopt_programbuild(
    destination_root: Path,
    *,
    project_name: str,
    variant: str = "product",
    dry_run: bool = False,
) -> None:
    """Add PROGRAMBUILD management without replacing an existing repo's engineering stack."""
    destination_root = destination_root.resolve()
    if not destination_root.is_dir():
        raise FileNotFoundError(f"Destination repository does not exist: {destination_root}")

    registry = load_registry()
    prompt_assets = _managed_prompt_assets(registry)
    _assert_safe_destination(destination_root, prompt_assets)

    if dry_run:
        print(f"ADOPT PROGRAMBUILD -> {destination_root}")

    bootstrap_programbuild(destination_root, registry, variant, dry_run)

    for relative_path in prompt_assets:
        source = workspace_path(relative_path)
        destination = destination_root / relative_path
        if destination.exists():
            if dry_run:
                print(f"PRESERVE {destination}")
            continue
        copy_file(source, destination, dry_run)

    registry_path = destination_root / "config" / "process-registry.json"
    if dry_run:
        print(f"CREATE {registry_path}")
        print(f"CREATE {destination_root / MANIFEST_FILENAME}")
        return

    write_json(
        registry_path,
        _adopted_registry(
            registry,
            project_name=project_name,
            prompt_assets=prompt_assets,
        ),
    )
    _write_adoption_manifest(
        destination_root,
        registry=registry,
        project_name=project_name,
        variant=variant,
        prompt_assets=prompt_assets,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Adopt PROGRAMBUILD in an existing repository without replacing "
            "its native engineering toolchain."
        )
    )
    parser.add_argument("--dest", required=True, help="Existing repository root to adopt.")
    parser.add_argument("--project-name", help="Project name to stamp into the adopted registry.")
    parser.add_argument(
        "--variant",
        choices=["lite", "product", "enterprise"],
        default="product",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the management overlay without writing files.",
    )
    args = parser.parse_args(argv)

    destination_root = Path(args.dest).expanduser().resolve()
    project_name = args.project_name or destination_root.name
    adopt_programbuild(
        destination_root,
        project_name=project_name,
        variant=args.variant,
        dry_run=args.dry_run,
    )
    if not args.dry_run:
        print(f"Adopted PROGRAMBUILD in existing repository: {destination_root}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart-adopt --dest <path>'")
    raise SystemExit(main())
