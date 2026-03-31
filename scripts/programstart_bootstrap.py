from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
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


def ensure_external_project_repo(destination_root: Path) -> None:
    template_root = workspace_path(".").resolve()
    try:
        destination_root.relative_to(template_root)
    except ValueError:
        return
    raise ValueError(
        "Destination must be outside the PROGRAMSTART template repo. Generated projects always belong in a new standalone repo."
    )


def stamp_bootstrapped_registry(destination_root: Path, *, project_name: str, dry_run: bool) -> None:
    registry_path = destination_root / "config" / "process-registry.json"
    if dry_run:
        print(f"STAMP  {registry_path}")
        return
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    workspace = dict(registry.get("workspace", {}))
    workspace["repo_role"] = "project_repo"
    workspace["project_name"] = project_name
    workspace["source_template_repo"] = "PROGRAMSTART"
    workspace["repo_boundary"] = "standalone_project_repo"
    workspace["provisioning_scope"] = "project_repo_only"
    validation = dict(registry.get("validation", {}))
    validation["enforce_engineering_ready_in_all"] = True
    integrity = dict(registry.get("integrity", {}))
    integrity["baselines"] = []
    registry["workspace"] = workspace
    registry["validation"] = validation
    registry["integrity"] = integrity
    write_json(registry_path, registry)


def sanitize_bootstrapped_secrets_baseline(destination_root: Path, dry_run: bool) -> None:
    baseline_path = destination_root / ".secrets.baseline"
    if dry_run or not baseline_path.exists():
        return

    payload = json.loads(baseline_path.read_text(encoding="utf-8"))
    results = dict(payload.get("results", {}))
    results.pop("config\\process-registry.json", None)
    results.pop("config/process-registry.json", None)
    payload["results"] = results
    baseline_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def refresh_secrets_baseline(destination_root: Path, dry_run: bool) -> None:
    baseline_path = destination_root / ".secrets.baseline"
    if dry_run or not baseline_path.exists():
        return

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "detect_secrets.main",
                "scan",
                "--all-files",
                "--baseline",
                baseline_path.name,
                ".",
            ],
            cwd=destination_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return


def initialize_git_repository(destination_root: Path, dry_run: bool) -> None:
    git_executable = shutil.which("git")
    if not git_executable:
        raise RuntimeError("git is required to initialize the generated project repository.")
    if dry_run:
        print(f"RUN    {git_executable} init -b main {destination_root}")
        return

    try:
        subprocess.run(
            [git_executable, "init", "-b", "main"],
            cwd=destination_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        subprocess.run(
            [git_executable, "init"],
            cwd=destination_root,
            check=True,
            capture_output=True,
            text=True,
        )


def write_bootstrap_readme(destination_root: Path, project_name: str, variant: str, dry_run: bool) -> None:
    readme_content = (
        f"# {project_name}\n\n"
        "This standalone project repository was bootstrapped from PROGRAMSTART.\n\n"
        "Included systems:\n\n"
        f"- PROGRAMBUILD variant: {variant}\n"
        "- USERJOURNEY: attach separately if this project needs onboarding, consent, or activation planning\n"
        "- Repo boundary: this repo is separate from PROGRAMSTART and should own its own remote/infrastructure\n"
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
    ensure_external_project_repo(destination_root)
    if destination_root.exists() and any(destination_root.iterdir()) and not force:
        raise FileExistsError("Destination exists and is not empty. Use --force to continue.")

    write_bootstrap_readme(destination_root, project_name, variant, dry_run)
    bootstrap_shared_assets(destination_root, registry, dry_run)
    bootstrap_programbuild(destination_root, registry, variant, dry_run)
    stamp_bootstrapped_registry(destination_root, project_name=project_name, dry_run=dry_run)
    sanitize_bootstrapped_secrets_baseline(destination_root, dry_run)
    refresh_secrets_baseline(destination_root, dry_run)
    initialize_git_repository(destination_root, dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a reusable PROGRAMSTART project repo in a new directory.")
    parser.add_argument("--dest", required=True, help="Destination directory for the new project repo.")
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
    except (FileExistsError, RuntimeError, ValueError) as exc:
        print(str(exc))
        return 1

    print(f"Bootstrap complete for {args.project_name} at {destination_root}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart bootstrap' or 'pb bootstrap'")
    raise SystemExit(main())
