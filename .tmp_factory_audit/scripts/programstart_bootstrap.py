from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

try:
    from .programstart_common import (
        create_default_workflow_state,
        load_registry,
        warn_direct_script_invocation,
        workspace_path,
        write_json,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        create_default_workflow_state,
        load_registry,
        warn_direct_script_invocation,
        workspace_path,
        write_json,
    )


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"CREATE {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_file(source: Path, destination: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"COPY   {source} -> {destination}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        content = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        shutil.copy2(source, destination)
        return

    newline = "\r\n" if source.suffix.lower() in {".ps1", ".bat", ".cmd"} else "\n"
    with destination.open("w", encoding="utf-8", newline=newline) as handle:
        handle.write(content)


def bootstrap_programbuild(destination_root: Path, registry: dict, variant: str, dry_run: bool) -> None:
    state_file = registry["workflow_state"]["programbuild"]["state_file"]
    for relative_path in registry["systems"]["programbuild"]["control_files"]:
        if relative_path == state_file:
            continue
        source = workspace_path(relative_path)
        destination = destination_root / relative_path
        copy_file(source, destination, dry_run)
    state_path = destination_root / state_file
    if dry_run:
        print(f"CREATE {state_path}")
    else:
        state = create_default_workflow_state(registry, "programbuild")
        state["variant"] = variant
        write_json(state_path, state)

    for relative_path in registry["systems"]["programbuild"]["output_files"]:
        source = workspace_path(relative_path)
        destination = destination_root / relative_path
        copy_file(source, destination, dry_run)


def bootstrap_shared_assets(destination_root: Path, registry: dict, dry_run: bool) -> None:
    for relative_path in registry.get("workspace", {}).get("bootstrap_assets", []):
        source = workspace_path(relative_path)
        destination = destination_root / relative_path
        copy_file(source, destination, dry_run)


def write_bootstrap_readme(destination_root: Path, project_name: str, variant: str, dry_run: bool) -> None:
    readme_content = (
        f"# {project_name}\n\n"
        "This planning repository was bootstrapped from PROGRAMSTART.\n\n"
        "Included systems:\n\n"
        f"- PROGRAMBUILD variant: {variant}\n"
        "- USERJOURNEY: attach separately if this project needs onboarding, consent, or activation planning\n"
        "\n"
        "Recommended first-time setup:\n\n"
        "- uv sync --extra dev\n"
        "- pre-commit install\n"
        "- python -m playwright install chromium\n"
        "- nox\n"
    )
    write_file(destination_root / "README.md", readme_content, dry_run)


def stamp_owner_and_dates(destination_root: Path, *, owner: str, last_updated: str) -> None:
    registry = load_registry()
    for relative_path in registry["systems"]["programbuild"].get("metadata_required", []):
        path = destination_root / relative_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"^Owner:\s*.*$", f"Owner: {owner}", text, flags=re.MULTILINE)
        text = re.sub(r"^Last updated:\s*.*$", f"Last updated: {last_updated}", text, flags=re.MULTILINE)
        path.write_text(text, encoding="utf-8")


def bootstrap_repository(
    destination_root: Path,
    *,
    project_name: str,
    variant: str,
    dry_run: bool = False,
    force: bool = False,
) -> None:
    registry = load_registry()
    if destination_root.exists() and any(destination_root.iterdir()) and not force:
        raise FileExistsError("Destination exists and is not empty. Use --force to continue.")

    write_bootstrap_readme(destination_root, project_name, variant, dry_run)
    bootstrap_shared_assets(destination_root, registry, dry_run)
    bootstrap_programbuild(destination_root, registry, variant, dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a reusable PROGRAMSTART planning package.")
    parser.add_argument("--dest", required=True, help="Destination directory for the new planning package.")
    parser.add_argument("--project-name", required=True, help="Project name to stamp into the generated files.")
    parser.add_argument("--variant", choices=["lite", "product", "enterprise"], default="product")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    destination_root = Path(args.dest).resolve()
    try:
        bootstrap_repository(
            destination_root,
            project_name=args.project_name,
            variant=args.variant,
            dry_run=args.dry_run,
            force=args.force,
        )
    except FileExistsError as exc:
        print(str(exc))
        return 1

    print(f"Bootstrap complete for {args.project_name} at {destination_root}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart bootstrap' or 'pb bootstrap'")
    raise SystemExit(main())
