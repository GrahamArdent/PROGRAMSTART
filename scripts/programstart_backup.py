from __future__ import annotations

import argparse
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from .programstart_common import load_registry, system_is_optional_and_absent, workflow_state_path, workspace_path
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import load_registry, system_is_optional_and_absent, workflow_state_path, workspace_path


def sanitize_label(label: str) -> str:
    sanitized = "-".join(label.strip().replace("_", " ").split()).lower()
    return "".join(char for char in sanitized if char.isalnum() or char == "-")


def backup_root() -> Path:
    return workspace_path("BACKUPS")


def build_backup_dirname(label: str, *, current_time: datetime | None = None) -> str:
    timestamp = current_time or datetime.now(UTC)
    date_prefix = timestamp.date().isoformat()
    normalized = sanitize_label(label)
    return f"{date_prefix}_{normalized}" if normalized else date_prefix


def next_backup_destination(root: Path, label: str, *, current_time: datetime | None = None) -> Path:
    base_name = build_backup_dirname(label, current_time=current_time)
    candidate = root / base_name
    if not candidate.exists():
        return candidate

    suffix = 2
    while True:
        candidate = root / f"{base_name}_{suffix}"
        if not candidate.exists():
            return candidate
        suffix += 1


def tracked_state_files(registry: dict[str, Any]) -> list[tuple[str, str, Path]]:
    files: list[tuple[str, str, Path]] = []
    for system_name in registry.get("systems", {}):
        if system_is_optional_and_absent(registry, system_name):
            continue
        relative_path = str(registry.get("workflow_state", {}).get(system_name, {}).get("state_file", "")).strip()
        if not relative_path:
            continue
        state_path = workflow_state_path(registry, system_name)
        if state_path.exists():
            files.append((system_name, relative_path, state_path))
    return files


def git_commit_hash() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=workspace_path("."),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "unknown"


def git_changed_files() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=workspace_path("."),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    changed: list[str] = []
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        changed.append(stripped[3:] if len(stripped) > 3 else stripped)
    return changed


def write_manifest(destination: Path, *, created_at: datetime, copied_files: list[Path]) -> Path:
    manifest_path = destination / "MANIFEST.txt"
    relative_files = [path.relative_to(destination).as_posix() for path in copied_files]
    changed_files = git_changed_files()
    lines = [
        "# PROGRAMSTART Backup Manifest",
        f"Created: {created_at.isoformat().replace('+00:00', 'Z')}",
        f"Git commit: {git_commit_hash()}",
        "",
        "Copied files:",
    ]
    lines.extend(f"- {relative_path}" for relative_path in relative_files)
    lines.append("")
    lines.append("Changed files:")
    if changed_files:
        lines.extend(f"- {path}" for path in changed_files)
    else:
        lines.append("- none")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest_path


def create_backup(registry: dict[str, Any], *, label: str = "") -> Path:
    root = backup_root()
    root.mkdir(parents=True, exist_ok=True)
    created_at = datetime.now(UTC)
    destination = next_backup_destination(root, label, current_time=created_at)
    destination.mkdir(parents=True, exist_ok=False)

    copied_files: list[Path] = []
    for _system_name, relative_path, source in tracked_state_files(registry):
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        copied_files.append(target)

    copied_files.append(write_manifest(destination, created_at=created_at, copied_files=copied_files))
    return destination


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create PROGRAMSTART workspace backups.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a backup snapshot of current workflow state files.")
    create_parser.add_argument("--label", default="", help="Optional label added to the backup directory name.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    registry = load_registry()

    if args.command == "create":
        destination = create_backup(registry, label=args.label)
        print(f"Backup created: {destination}")
        return 0

    parser.error(f"Unknown backup command: {args.command}")
    return 1  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())