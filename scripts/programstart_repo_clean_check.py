"""Utility to check git working-tree cleanliness.

Primary use case: assert that root-workspace smoke scripts (or any other
operation) leave the repo unchanged.  Also usable standalone to quickly
check whether the working tree is clean.

CLI
---
    python scripts/programstart_repo_clean_check.py          # exits 0 if clean
    uv run python scripts/programstart_repo_clean_check.py   # same via uv
"""

from __future__ import annotations

import subprocess
from pathlib import Path

try:
    from .programstart_common import ROOT, warn_direct_script_invocation
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import ROOT, warn_direct_script_invocation  # type: ignore[no-redef]


def capture_git_status(repo: Path | None = None) -> set[str]:
    """Return the set of changed / untracked file paths reported by ``git status``.

    Each path is relative to the repo root, as printed by ``git status --porcelain``.
    An empty set means the working tree is completely clean.
    """
    cwd = str(repo) if repo else str(ROOT)
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    paths: set[str] = set()
    for line in result.stdout.splitlines():
        # porcelain format: XY <path>  (first 3 chars are status + space)
        if len(line) > 3:
            paths.add(line[3:].strip())
    return paths


def assert_repo_clean(label: str = "repo", *, repo: Path | None = None) -> None:
    """Raise ``SystemExit(1)`` with a file-level summary if the working tree is dirty."""
    dirty = capture_git_status(repo)
    if dirty:
        print(f"FAIL: {label} — working tree is not clean ({len(dirty)} file(s) changed):")
        for p in sorted(dirty):
            print(f"  {p}")
        raise SystemExit(1)


def assert_repo_unchanged(
    before: set[str],
    after: set[str],
    label: str = "operation",
) -> None:
    """Fail if new changes appeared that were not present before the operation."""
    new_changes = after - before
    if new_changes:
        print(f"FAIL: {label} — {len(new_changes)} new file(s) changed during operation:")
        for p in sorted(new_changes):
            print(f"  {p}")
        raise SystemExit(1)


def main() -> int:
    """CLI entry point — exit 0 if clean, 1 with summary if dirty."""
    warn_direct_script_invocation("programstart validate")
    dirty = capture_git_status()
    if dirty:
        print(f"Working tree is dirty ({len(dirty)} file(s)):")
        for p in sorted(dirty):
            print(f"  {p}")
        return 1
    print("Working tree is clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
