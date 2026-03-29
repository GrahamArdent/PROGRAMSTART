from __future__ import annotations

import argparse
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
    from programstart_common import (  # type: ignore
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Attach USERJOURNEY to the current planning repository.")
    parser.add_argument("system", choices=["userjourney"], help="Attachment type to add.")
    parser.add_argument("--source", required=True, help="Path to a USERJOURNEY folder or repo containing one.")
    parser.add_argument("--force", action="store_true", help="Replace an existing USERJOURNEY folder.")
    parser.add_argument("--dry-run", action="store_true", help="Preview attachment without copying files.")
    args = parser.parse_args(argv)

    source_root = resolve_attachment_source(args.source)
    attach_userjourney(workspace_path("."), source_root, force=args.force, dry_run=args.dry_run)
    if not args.dry_run:
        print(f"Attached USERJOURNEY from {source_root}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation(
        "'uv run programstart attach userjourney --source <path>' or 'pb attach userjourney --source <path>'"
    )
    raise SystemExit(main())
