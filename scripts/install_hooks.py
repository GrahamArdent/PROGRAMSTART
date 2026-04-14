"""install_hooks.py — install or uninstall PROGRAMSTART git hooks.

Usage:
    uv run python scripts/install_hooks.py            # install all hooks
    uv run python scripts/install_hooks.py --uninstall  # remove installed hooks
    uv run python scripts/install_hooks.py --check    # verify hooks are installed (exit 0/1)
"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS_SOURCE_DIR = Path(__file__).resolve().parent / "hooks"
GIT_HOOKS_DIR = ROOT / ".git" / "hooks"

_HOOK_NAMES = ["pre-push"]


def _make_executable(path: Path) -> None:
    """Add execute permission bits (no-op on Windows; git handles exec bit via config)."""
    if sys.platform != "win32":
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install_hooks(*, dry_run: bool = False) -> int:
    if not GIT_HOOKS_DIR.is_dir():
        print(f"ERROR: .git/hooks directory not found at {GIT_HOOKS_DIR}", file=sys.stderr)
        return 1
    for name in _HOOK_NAMES:
        source = HOOKS_SOURCE_DIR / name
        dest = GIT_HOOKS_DIR / name
        if not source.exists():
            print(f"WARNING: hook source not found: {source}", file=sys.stderr)
            continue
        if dry_run:
            print(f"INSTALL (dry-run) {source} -> {dest}")
            continue
        shutil.copy2(source, dest)
        _make_executable(dest)
        print(f"Installed {name} -> {dest}")
    return 0


def uninstall_hooks(*, dry_run: bool = False) -> int:
    for name in _HOOK_NAMES:
        dest = GIT_HOOKS_DIR / name
        if not dest.exists():
            continue
        if dry_run:
            print(f"REMOVE (dry-run) {dest}")
            continue
        dest.unlink()
        print(f"Removed {dest}")
    return 0


def check_hooks() -> int:
    missing = [name for name in _HOOK_NAMES if not (GIT_HOOKS_DIR / name).exists()]
    if missing:
        print(f"Hooks not installed: {', '.join(missing)}", file=sys.stderr)
        return 1
    print("All hooks installed.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install or uninstall PROGRAMSTART git hooks.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--uninstall", action="store_true", help="Remove installed hooks")
    group.add_argument("--check", action="store_true", help="Verify hooks are installed (exit 1 if not)")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing")
    args = parser.parse_args(argv)

    if args.check:
        return check_hooks()
    if args.uninstall:
        return uninstall_hooks(dry_run=args.dry_run)
    return install_hooks(dry_run=args.dry_run)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
