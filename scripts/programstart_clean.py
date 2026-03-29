from __future__ import annotations

import argparse
import shutil
from pathlib import Path

try:
    from .programstart_common import ROOT, display_workspace_path, generated_outputs_root, warn_direct_script_invocation
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import ROOT, display_workspace_path, generated_outputs_root, warn_direct_script_invocation


DEFAULT_EXACT_PATHS = (
    ".benchmarks",
    ".coverage",
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tmp_ci_bootstrap",
    ".tmp_dist_smoke",
    "build",
    "htmlcov",
    "site",
)

DEFAULT_GLOBS = (
    ".tmp_bootstrap_*",
    "*.egg-info",
)


def collect_cleanup_targets(include_dist: bool, include_outputs: bool) -> list[Path]:
    targets: dict[str, Path] = {}

    for relative in DEFAULT_EXACT_PATHS:
        path = ROOT / relative
        if path.exists():
            targets.setdefault(str(path.resolve()), path)

    for pattern in DEFAULT_GLOBS:
        for path in ROOT.glob(pattern):
            if path.exists():
                targets.setdefault(str(path.resolve()), path)

    if include_dist:
        dist_path = ROOT / "dist"
        if dist_path.exists():
            targets.setdefault(str(dist_path.resolve()), dist_path)

    if include_outputs:
        outputs_path = generated_outputs_root()
        if outputs_path.exists():
            targets.setdefault(str(outputs_path.resolve()), outputs_path)

    return sorted(targets.values(), key=lambda path: path.name.lower())


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
        return
    path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove disposable local PROGRAMSTART artifacts.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be removed without deleting anything.")
    parser.add_argument("--include-dist", action="store_true", help="Also remove the dist/ build output directory.")
    parser.add_argument(
        "--include-outputs",
        action="store_true",
        help="Also remove the dedicated generated outputs directory.",
    )
    args = parser.parse_args()

    targets = collect_cleanup_targets(include_dist=args.include_dist, include_outputs=args.include_outputs)
    if not targets:
        print("No disposable artifacts found.")
        return 0

    action = "Would remove" if args.dry_run else "Removed"
    for path in targets:
        if not args.dry_run:
            remove_path(path)
        print(f"{action} {display_workspace_path(path)}")

    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart clean' or 'pb clean'")
    raise SystemExit(main())
