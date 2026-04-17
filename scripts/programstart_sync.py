from __future__ import annotations

import argparse
import filecmp
import json
import sys
from pathlib import Path

try:
    from .programstart_attach import MANIFEST_FILENAME, PROGRAMBUILD_PRESERVE_EXISTING_FILES
    from .programstart_bootstrap import copy_file
    from .programstart_common import warn_direct_script_invocation, workspace_path
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_attach import MANIFEST_FILENAME, PROGRAMBUILD_PRESERVE_EXISTING_FILES
    from programstart_bootstrap import copy_file

    from programstart_common import warn_direct_script_invocation, workspace_path

SYNC_DESCRIPTION = (
    "Propagate changed PROGRAMSTART files to/from a downstream repo.\n\n"
    "Push mode (--dest): copies changed files from the PROGRAMSTART template to a\n"
    "downstream repo.  Pull mode (--from-template): copies changed files from an\n"
    "upstream PROGRAMSTART template into the current (or --dest) repo.\n\n"
    "Reads the .programstart-manifest.json written at attach time and copies only\n"
    "files that differ between the template and the destination. Without --confirm\n"
    "the command runs in dry-run mode and shows what would change."
)


def _load_manifest(destination_root: Path) -> dict:
    manifest_path = destination_root / MANIFEST_FILENAME
    if not manifest_path.exists():
        print(f"ERROR: No manifest found at {manifest_path}", file=sys.stderr)
        print("  The destination may not have been attached with a manifest-aware version.", file=sys.stderr)
        print("  Re-attach with: programstart attach programbuild --dest <path> --force", file=sys.stderr)
        raise SystemExit(1)
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def _preserve_path(destination_root: Path) -> set[str]:
    preserve_file = destination_root / ".programstart-preserve"
    base = set(PROGRAMBUILD_PRESERVE_EXISTING_FILES)
    if preserve_file.exists():
        for line in preserve_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                base.add(stripped)
    return base


def _files_needing_sync(
    template_root: Path,
    destination_root: Path,
    manifest_files: list[str],
    preserve: set[str],
    file_filter: str | None = None,
) -> list[tuple[str, str]]:
    """Return list of (relative_path, reason) for files that need syncing."""
    results: list[tuple[str, str]] = []
    for relative_path in manifest_files:
        if relative_path in preserve:
            continue
        if file_filter and not _matches_filter(relative_path, file_filter):
            continue
        source = template_root / relative_path
        destination = destination_root / relative_path
        if not source.exists():
            results.append((relative_path, "removed-from-template"))
            continue
        if not destination.exists():
            results.append((relative_path, "missing-in-dest"))
            continue
        if not filecmp.cmp(source, destination, shallow=False):
            results.append((relative_path, "changed"))
    return results


def _matches_filter(path: str, pattern: str) -> bool:
    from fnmatch import fnmatch

    return fnmatch(path, pattern)


def sync(
    destination_root: Path,
    *,
    confirm: bool = False,
    file_filter: str | None = None,
    template_root: Path | None = None,
) -> int:
    manifest = _load_manifest(destination_root)
    manifest_files: list[str] = manifest.get("files", [])
    if template_root is None:
        template_root = workspace_path(".")
    preserve = _preserve_path(destination_root)

    changes = _files_needing_sync(template_root, destination_root, manifest_files, preserve, file_filter)

    if not changes:
        print("  All manifest files are up to date. Nothing to sync.")
        return 0

    print(f"  {len(changes)} file(s) differ:")
    for relative_path, reason in changes:
        marker = "!" if reason == "removed-from-template" else "+"
        print(f"    [{marker}] {relative_path}  ({reason})")

    if not confirm:
        print()
        print("  Dry-run mode. Re-run with --confirm to apply changes.")
        return 0

    copied = 0
    skipped = 0
    for relative_path, reason in changes:
        if reason == "removed-from-template":
            print(f"  SKIP {relative_path} (removed from template — delete manually if desired)")
            skipped += 1
            continue
        source = template_root / relative_path
        destination = destination_root / relative_path
        copy_file(source, destination, dry_run=False)
        copied += 1
        print(f"  SYNC {relative_path}")

    print()
    print(f"  Synced {copied} file(s), skipped {skipped}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="programstart sync",
        description=SYNC_DESCRIPTION,
    )
    parser.add_argument("--dest", help="Destination repository root (default: current directory with --from-template).")
    parser.add_argument(
        "--from-template",
        metavar="PATH",
        help="Pull mode: path to the upstream PROGRAMSTART template root. Copies changed files into --dest (or .).",
    )
    parser.add_argument("--confirm", action="store_true", help="Apply changes (default is dry-run).")
    parser.add_argument("--files", dest="file_filter", help="Only sync files matching this glob pattern.")
    args = parser.parse_args(argv)

    if not args.dest and not args.from_template:
        parser.error("--dest or --from-template is required")

    # Pull mode: --from-template sets template_root; --dest defaults to "."
    template_root: Path | None = None
    if args.from_template:
        template_root = Path(args.from_template).resolve()
        if not template_root.is_dir():
            print(f"ERROR: Template root does not exist: {template_root}", file=sys.stderr)
            return 1

    destination_root = Path(args.dest).resolve() if args.dest else Path.cwd()
    if not destination_root.is_dir():
        print(f"ERROR: Destination does not exist: {destination_root}", file=sys.stderr)
        return 1

    return sync(
        destination_root,
        confirm=args.confirm,
        file_filter=args.file_filter,
        template_root=template_root,
    )


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart sync --dest <path>'")
    raise SystemExit(main())
