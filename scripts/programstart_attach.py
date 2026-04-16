from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

try:
    from .programstart_bootstrap import (
        bootstrap_programbuild,
        copy_file,
        generated_repo_bootstrap_assets_for_mode,
        generated_repo_prompt_assets_for_mode,
        generated_repo_prompt_authority_for_mode,
        generated_repo_prompt_registry_for_mode,
        refresh_secrets_baseline,
        sanitize_bootstrapped_secrets_baseline,
        stamp_bootstrapped_registry,
    )
    from .programstart_common import (
        create_default_workflow_state,
        load_registry,
        warn_direct_script_invocation,
        workspace_path,
        write_json,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_bootstrap import (
        bootstrap_programbuild,
        copy_file,
        generated_repo_bootstrap_assets_for_mode,
        generated_repo_prompt_assets_for_mode,
        generated_repo_prompt_authority_for_mode,
        generated_repo_prompt_registry_for_mode,
        refresh_secrets_baseline,
        sanitize_bootstrapped_secrets_baseline,
        stamp_bootstrapped_registry,
    )

    from programstart_common import (
        create_default_workflow_state,
        load_registry,
        warn_direct_script_invocation,
        workspace_path,
        write_json,
    )


REQUIRED_USERJOURNEY_FILES = {
    "README.md",
    "DELIVERY_GAMEPLAN.md",
    "USERJOURNEY_TEMPLATE_STARTER.md",
}
PROGRAMBUILD_PRESERVE_EXISTING_FILES = {
    "README.md",
    ".gitignore",
}


def _copy_text_or_binary(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        content = source.read_text(encoding="utf-8")
        with destination.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    except UnicodeDecodeError:
        shutil.copy2(source, destination)


def _copy_userjourney_bootstrap_assets(destination_root: Path, registry: dict) -> None:
    """Copy USERJOURNEY-specific test files listed in the registry into the project repo."""
    template_root = workspace_path(".")
    for relative_path in registry.get("workspace", {}).get("userjourney_bootstrap_assets", []):
        source = template_root / relative_path
        if not source.exists():
            continue
        _copy_text_or_binary(source, destination_root / relative_path)


def _attached_userjourney_prompt_assets(registry: dict) -> list[str]:
    base_assets = generated_repo_prompt_assets_for_mode(registry, include_userjourney=False)
    attached_assets = generated_repo_prompt_assets_for_mode(registry, include_userjourney=True)
    return sorted(attached_assets - base_assets)


def _copy_userjourney_prompt_assets(destination_root: Path, registry: dict) -> None:
    template_root = workspace_path(".")
    for relative_path in _attached_userjourney_prompt_assets(registry):
        source = template_root / relative_path
        if not source.exists():
            continue
        _copy_text_or_binary(source, destination_root / relative_path)


def _sync_attached_userjourney_registry(destination_root: Path, template_registry: dict) -> None:
    registry_path = destination_root / "config" / "process-registry.json"
    if not registry_path.exists():
        return

    project_registry = json.loads(registry_path.read_text(encoding="utf-8"))
    base_prompt_registry = generated_repo_prompt_registry_for_mode(template_registry, include_userjourney=False)
    attached_prompt_registry = generated_repo_prompt_registry_for_mode(template_registry, include_userjourney=True)
    restored_prompt_paths = [
        path
        for path in attached_prompt_registry["workflow_prompt_files"]
        if path not in base_prompt_registry["workflow_prompt_files"]
    ]

    prompt_registry = dict(project_registry.get("prompt_registry", {}))
    workflow_prompt_files = list(prompt_registry.get("workflow_prompt_files", []))
    for prompt_path in restored_prompt_paths:
        if prompt_path not in workflow_prompt_files:
            workflow_prompt_files.append(prompt_path)
    prompt_registry["workflow_prompt_files"] = workflow_prompt_files
    project_registry["prompt_registry"] = prompt_registry

    prompt_authority = dict(project_registry.get("prompt_authority", {}))
    base_prompt_authority = generated_repo_prompt_authority_for_mode(template_registry, include_userjourney=False)
    attached_prompt_authority = generated_repo_prompt_authority_for_mode(template_registry, include_userjourney=True)
    for prompt_path, payload in attached_prompt_authority.items():
        if prompt_path in base_prompt_authority:
            continue
        prompt_authority[prompt_path] = payload
    project_registry["prompt_authority"] = prompt_authority

    workspace = dict(project_registry.get("workspace", {}))
    bootstrap_assets = list(workspace.get("bootstrap_assets", []))
    base_bootstrap_assets = generated_repo_bootstrap_assets_for_mode(template_registry, include_userjourney=False)
    attached_bootstrap_assets = generated_repo_bootstrap_assets_for_mode(template_registry, include_userjourney=True)
    for relative_path in attached_bootstrap_assets:
        if relative_path in base_bootstrap_assets:
            continue
        if relative_path not in bootstrap_assets:
            bootstrap_assets.append(relative_path)
    workspace["bootstrap_assets"] = bootstrap_assets
    project_registry["workspace"] = workspace

    write_json(registry_path, project_registry)


def _copy_programbuild_bootstrap_assets(
    destination_root: Path,
    registry: dict,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> None:
    template_root = workspace_path(".")
    for relative_path in generated_repo_bootstrap_assets_for_mode(registry, include_userjourney=False):
        source = template_root / relative_path
        destination = destination_root / relative_path
        if destination.exists() and relative_path in PROGRAMBUILD_PRESERVE_EXISTING_FILES and not force:
            if dry_run:
                print(f"PRESERVE {destination}")
            continue
        if destination.exists() and not force:
            raise FileExistsError(f"Destination already has {relative_path}. Use --force to replace it.")
        copy_file(source, destination, dry_run)


def attach_programbuild(
    destination_root: Path,
    *,
    project_name: str,
    variant: str = "product",
    force: bool = False,
    dry_run: bool = False,
) -> None:
    programbuild_root = destination_root / "PROGRAMBUILD"
    if programbuild_root.exists() and not force:
        raise FileExistsError("PROGRAMBUILD already exists in destination. Use --force to replace it.")

    registry = load_registry()
    if dry_run:
        print(f"ATTACH PROGRAMBUILD -> {destination_root}")

    _copy_programbuild_bootstrap_assets(destination_root, registry, force=force, dry_run=dry_run)
    bootstrap_programbuild(destination_root, registry, variant, dry_run)
    stamp_bootstrapped_registry(destination_root, project_name=project_name, dry_run=dry_run)
    sanitize_bootstrapped_secrets_baseline(destination_root, dry_run)
    refresh_secrets_baseline(destination_root, dry_run)


def resolve_attachment_source(source: str) -> Path:
    candidate = Path(source).expanduser().resolve()
    if candidate.is_dir() and candidate.name == "USERJOURNEY":
        return candidate
    nested = candidate / "USERJOURNEY"
    if nested.exists() and nested.is_dir():
        return nested
    raise FileNotFoundError(f"Could not resolve USERJOURNEY source from: {source}")


def validate_attachment_source(source_root: Path) -> list[str]:
    missing = [name for name in sorted(REQUIRED_USERJOURNEY_FILES) if not (source_root / name).exists()]
    return missing


def attach_userjourney(
    destination_root: Path,
    source_root: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> None:
    destination = destination_root / "USERJOURNEY"
    if destination.exists() and not force:
        raise FileExistsError("USERJOURNEY already exists in destination. Use --force to replace it.")

    missing = validate_attachment_source(source_root)
    if missing:
        raise FileNotFoundError(f"USERJOURNEY source is missing required files: {', '.join(missing)}")

    if dry_run:
        print(f"ATTACH USERJOURNEY {source_root} -> {destination}")
        return

    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source_root, destination)

    registry = load_registry()
    state_path = destination / "USERJOURNEY_STATE.json"
    if not state_path.exists():
        write_json(state_path, create_default_workflow_state(registry, "userjourney"))

    # Copy USERJOURNEY-specific prompt, test, and asset files into the project repo.
    _copy_userjourney_prompt_assets(destination_root, registry)
    _copy_userjourney_bootstrap_assets(destination_root, registry)
    _sync_attached_userjourney_registry(destination_root, registry)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Attach PROGRAMSTART systems to an existing repository.")
    parser.add_argument("system", choices=["programbuild", "userjourney"], help="Attachment type to add.")
    parser.add_argument("--source", help="Path to a USERJOURNEY folder or repo containing one.")
    parser.add_argument("--dest", help="Destination repository root. Defaults to the current workspace.")
    parser.add_argument("--project-name", help="Project name to stamp when attaching PROGRAMBUILD.")
    parser.add_argument("--variant", choices=["lite", "product", "enterprise"], default="product")
    parser.add_argument("--force", action="store_true", help="Replace an existing USERJOURNEY folder.")
    parser.add_argument("--dry-run", action="store_true", help="Preview attachment without copying files.")
    args = parser.parse_args(argv)

    destination_root = Path(args.dest).resolve() if args.dest else workspace_path(".")

    if args.system == "userjourney":
        if not args.source:
            parser.error("--source is required when attaching USERJOURNEY")
        source_root = resolve_attachment_source(args.source)
        attach_userjourney(destination_root, source_root, force=args.force, dry_run=args.dry_run)
        if not args.dry_run:
            print(f"Attached USERJOURNEY from {source_root}")
        return 0

    project_name = args.project_name or destination_root.name
    attach_programbuild(
        destination_root,
        project_name=project_name,
        variant=args.variant,
        force=args.force,
        dry_run=args.dry_run,
    )
    if not args.dry_run:
        print(f"Attached PROGRAMBUILD to {destination_root}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation(
        "'uv run programstart attach programbuild --dest <path>' or 'uv run programstart attach userjourney --source <path> --dest <path>'"
    )
    raise SystemExit(main())
