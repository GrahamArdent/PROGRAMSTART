from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from .programstart_adopt import _adopted_registry, _git_head_hash, _managed_prompt_assets
    from .programstart_attach import MANIFEST_FILENAME
    from .programstart_bootstrap import copy_file
    from .programstart_common import load_registry, warn_direct_script_invocation, workspace_path, write_json
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_adopt import _adopted_registry, _git_head_hash, _managed_prompt_assets
    from programstart_attach import MANIFEST_FILENAME
    from programstart_bootstrap import copy_file
    from programstart_common import load_registry, warn_direct_script_invocation, workspace_path, write_json

# External control starts deliberately narrow. These commands are either read-only,
# write only derived prompt/snapshot evidence, or operate entirely on the decision
# router. Stage mutation and template-runtime convergence stay local until their
# validators explicitly understand the split runtime/project boundary.
TARGET_COMMANDS = frozenset(
    {
        "decide",
        "diff",
        "drift",
        "guide",
        "jit-check",
        "next",
        "progress",
        "prompt-build",
        "state",
        "status",
        "validate",
    }
)

TARGET_STATE_COMMANDS = frozenset({"show", "snapshot", "snapshots", "diff"})
TARGET_VALIDATE_CHECKS = frozenset(
    {
        "required-files",
        "metadata",
        "workflow-state",
        "placeholder-content",
        "intake-complete",
        "feasibility-criteria",
        "research-complete",
        "requirements-complete",
        "architecture-contracts",
        "risk-spikes",
        "risk-spikes-resolved",
        "test-strategy-complete",
        "scaffold-complete",
        "implementation-entry",
        "release-ready",
        "audit-complete",
        "post-launch-review",
    }
)


def _read_variant(destination_root: Path, fallback: str = "product") -> str:
    state_path = destination_root / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json"
    if not state_path.exists():
        return fallback
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback
    variant = str(payload.get("variant", "")).strip().lower()
    return variant if variant in {"lite", "product", "enterprise"} else fallback


def _copy_managed_prompts(destination_root: Path, prompt_assets: tuple[str, ...], *, dry_run: bool) -> None:
    for relative_path in prompt_assets:
        source = workspace_path(relative_path)
        destination = destination_root / relative_path
        if destination.exists():
            try:
                identical = source.read_bytes() == destination.read_bytes()
            except OSError:
                identical = False
            if not identical:
                raise FileExistsError(
                    f"External control preparation would overwrite existing project file: {relative_path}"
                )
            if dry_run:
                print(f"PRESERVE {destination}")
            continue
        copy_file(source, destination, dry_run)


def _write_control_manifest(
    destination_root: Path,
    *,
    registry: dict[str, Any],
    project_name: str,
    variant: str,
    prompt_assets: tuple[str, ...],
    mode: str,
) -> None:
    state_file = registry["workflow_state"]["programbuild"]["state_file"]
    managed_controls = [
        path for path in registry["systems"]["programbuild"]["control_files"] if path != state_file
    ]
    manifest = {
        "programstart_version": "1.0.0",
        "source_commit": _git_head_hash(),
        "attached_at": datetime.now(UTC).isoformat(),
        "mode": mode,
        "project_name": project_name,
        "variant": variant,
        "control_plane": "external_programstart_runtime",
        "files": sorted([*managed_controls, *prompt_assets]),
    }
    write_json(destination_root / MANIFEST_FILENAME, manifest)


def prepare_target_control_plane(
    destination_root: Path,
    *,
    project_name: str | None = None,
    variant: str | None = None,
    mode: str = "external_control_plane_link",
    dry_run: bool = False,
) -> None:
    """Add only the static control metadata needed for central PROGRAMSTART operation."""
    destination_root = destination_root.expanduser().resolve()
    if not dry_run and not destination_root.is_dir():
        raise FileNotFoundError(f"Target repository does not exist: {destination_root}")
    if not dry_run and not (destination_root / "PROGRAMBUILD").is_dir():
        raise FileNotFoundError(
            "Target repository has no PROGRAMBUILD directory. Bootstrap/adopt PROGRAMBUILD "
            "before linking the external control plane."
        )

    registry_path = destination_root / "config" / "process-registry.json"
    if registry_path.exists():
        print(f"External control surface already present: {registry_path}")
        return

    manifest_path = destination_root / MANIFEST_FILENAME
    if manifest_path.exists():
        raise FileExistsError(
            f"{MANIFEST_FILENAME} exists but config/process-registry.json is missing; "
            "repair that inconsistent link before preparing."
        )

    registry = load_registry()
    prompt_assets = _managed_prompt_assets(registry)
    resolved_project_name = project_name or destination_root.name
    resolved_variant = variant or _read_variant(destination_root)

    if dry_run:
        print(f"PREPARE EXTERNAL CONTROL -> {destination_root}")

    _copy_managed_prompts(destination_root, prompt_assets, dry_run=dry_run)
    managed_registry = _adopted_registry(
        registry,
        project_name=resolved_project_name,
        prompt_assets=prompt_assets,
    )
    workspace = dict(managed_registry.get("workspace", {}))
    workspace.update(
        {
            "repo_role": "managed_project_repo",
            "repo_boundary": "standalone_project_repo",
            "provisioning_scope": "external_programstart_control_plane",
            "runtime_mode": "external_control_plane",
        }
    )
    managed_registry["workspace"] = workspace

    if dry_run:
        print(f"CREATE {registry_path}")
        print(f"CREATE {manifest_path}")
        return

    write_json(registry_path, managed_registry)
    _write_control_manifest(
        destination_root,
        registry=registry,
        project_name=resolved_project_name,
        variant=resolved_variant,
        prompt_assets=prompt_assets,
        mode=mode,
    )


def _validate_target_command(arguments: list[str]) -> None:
    if not arguments:
        raise ValueError("Provide a target command such as `status` or `guide --system programbuild`.")

    command = arguments[0]
    if command not in TARGET_COMMANDS:
        allowed = ", ".join(sorted(TARGET_COMMANDS))
        raise ValueError(
            f"Command '{command}' is not allowed through the external target control plane. Allowed: {allowed}"
        )

    if command == "state":
        if len(arguments) < 2 or arguments[1] not in TARGET_STATE_COMMANDS:
            allowed = ", ".join(sorted(TARGET_STATE_COMMANDS))
            raise ValueError(
                "External target state mutation is intentionally disabled in this slice. "
                f"Allowed state operations: {allowed}"
            )

    if command == "validate":
        if "--check" not in arguments:
            allowed = ", ".join(sorted(TARGET_VALIDATE_CHECKS))
            raise ValueError(
                "Bare `validate` includes template-runtime checks that do not belong in a lean target. "
                f"Choose a target-local --check. Allowed: {allowed}"
            )
        index = arguments.index("--check")
        if index + 1 >= len(arguments):
            raise ValueError("`validate --check` requires a check name.")
        check_name = arguments[index + 1]
        if check_name not in TARGET_VALIDATE_CHECKS:
            allowed = ", ".join(sorted(TARGET_VALIDATE_CHECKS))
            raise ValueError(
                f"Validation check '{check_name}' is not target-local. "
                f"Allowed through external control: {allowed}"
            )


def run_target_command(destination_root: Path, arguments: list[str]) -> int:
    """Run central PROGRAMSTART machinery against a linked target checkout."""
    destination_root = destination_root.expanduser().resolve()
    if not destination_root.is_dir():
        raise FileNotFoundError(f"Target repository does not exist: {destination_root}")
    registry_path = destination_root / "config" / "process-registry.json"
    if not registry_path.exists():
        raise FileNotFoundError(
            "Target has no control registry. Run `programstart target --repo <path> --prepare` once, "
            "or recreate it with the current methodology-only bootstrap."
        )

    _validate_target_command(arguments)

    env = os.environ.copy()
    env["PROGRAMSTART_ROOT"] = str(destination_root)
    package_root = str(Path(__file__).resolve().parents[1])
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(part for part in (package_root, existing_pythonpath) if part)

    completed = subprocess.run(
        [sys.executable, "-P", "-m", "scripts.programstart_cli", *arguments],
        cwd=destination_root,
        env=env,
        check=False,
    )
    return int(completed.returncode)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Operate PROGRAMSTART's central runtime against a lightweight external project repository."
    )
    parser.add_argument("--repo", required=True, help="Local checkout path for the target project repository.")
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Add the lightweight registry/prompts/manifest control surface before running the command.",
    )
    parser.add_argument("--project-name", help="Project name to stamp when --prepare is used.")
    parser.add_argument(
        "--variant",
        choices=["lite", "product", "enterprise"],
        help="Variant override for --prepare.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview --prepare without writing files.")
    args, command_arguments = parser.parse_known_args(argv)
    destination_root = Path(args.repo)

    try:
        if args.prepare:
            prepare_target_control_plane(
                destination_root,
                project_name=args.project_name,
                variant=args.variant,
                dry_run=args.dry_run,
            )
            if args.dry_run:
                return 0
        elif args.project_name or args.variant or args.dry_run:
            parser.error("--project-name, --variant, and --dry-run are valid only with --prepare")

        if not command_arguments:
            if args.prepare:
                return 0
            parser.error("Provide a target command after the target options, for example `status`.")
        return run_target_command(destination_root, command_arguments)
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart target --repo <path> <command>'")
    raise SystemExit(main())
