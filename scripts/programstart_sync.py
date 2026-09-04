from __future__ import annotations

import argparse
import filecmp
import json
import subprocess
import sys
from pathlib import Path

try:
    from .programstart_attach import MANIFEST_FILENAME, PROGRAMBUILD_PRESERVE_EXISTING_FILES
    from .programstart_bootstrap import (
        WORKFLOW_DESTINATION_PREFIX,
        WORKFLOW_TEMPLATE_PREFIX,
        copy_file,
        generated_repo_prompt_assets_for_mode,
    )
    from .programstart_common import (
        load_registry_from_path,
        warn_direct_script_invocation,
        workspace_path,
        write_json,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_attach import MANIFEST_FILENAME, PROGRAMBUILD_PRESERVE_EXISTING_FILES
    from programstart_bootstrap import (
        WORKFLOW_DESTINATION_PREFIX,
        WORKFLOW_TEMPLATE_PREFIX,
        copy_file,
        generated_repo_prompt_assets_for_mode,
    )
    from programstart_common import (
        load_registry_from_path,
        warn_direct_script_invocation,
        workspace_path,
        write_json,
    )

SYNC_DESCRIPTION = (
    "Propagate changed PROGRAMSTART files to/from a downstream repo.\n\n"
    "Push mode (--dest): copies changed files from the PROGRAMSTART template to a\n"
    "downstream repo.  Pull mode (--from-template): copies changed files from an\n"
    "upstream PROGRAMSTART template into the current (or --dest) repo.\n\n"
    "Reads the .programstart-manifest.json written at attach/adopt time and copies\n"
    "files that differ between the template and the destination. Existing-project\n"
    "adoption manifests also discover newly managed control/support files from the\n"
    "current template registry during a full sync. Without --confirm the command\n"
    "runs in dry-run mode and shows what would change."
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


def _template_source_path(template_root: Path, relative_path: str) -> Path:
    """Resolve a downstream manifest path back to its source in the template repo.

    Direct same-path sources remain authoritative for backward compatibility. If a
    generated project's `.github/workflows/*` asset is intentionally dormant in the
    template repo, fall back to the matching `templates/github-workflows/*` source.
    """
    direct = template_root / relative_path
    if direct.exists():
        return direct
    if relative_path.startswith(WORKFLOW_DESTINATION_PREFIX):
        suffix = relative_path.removeprefix(WORKFLOW_DESTINATION_PREFIX)
        dormant = template_root / WORKFLOW_TEMPLATE_PREFIX / suffix
        if dormant.exists():
            return dormant
    return direct


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
        source = _template_source_path(template_root, relative_path)
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


def _template_head_hash(template_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=template_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return ""


def _current_adoption_manifest_files(template_root: Path, manifest: dict) -> list[str]:
    """Return the additively evolved managed file set for an adopted existing repo.

    Legacy attachment manifests remain frozen to their recorded file list. Existing-
    project adoption manifests are safe to evolve because their managed surface is
    explicitly defined as PROGRAMBUILD controls (excluding state) plus generated-repo
    prompt/support assets. Historical entries are retained so removals remain visible
    as `removed-from-template` rather than becoming implicit deletions.
    """
    recorded = list(manifest.get("files", []))
    if manifest.get("mode") != "existing_project_adoption":
        return recorded

    registry_path = template_root / "config" / "process-registry.json"
    if not registry_path.exists():
        return recorded

    registry = load_registry_from_path(registry_path)
    state_file = registry["workflow_state"]["programbuild"]["state_file"]
    managed_controls = {
        path for path in registry["systems"]["programbuild"]["control_files"] if path != state_file
    }
    managed_support = generated_repo_prompt_assets_for_mode(registry, include_userjourney=False)
    return sorted(set(recorded) | managed_controls | managed_support)


def _write_adoption_manifest_if_safe(
    destination_root: Path,
    *,
    manifest: dict,
    manifest_files: list[str],
    template_root: Path,
    alignment_issues: list[tuple[str, str]],
) -> bool:
    """Advance adoption metadata only when every managed file matches the template.

    Preserve rules control copying, not truth. A preserved managed file may remain
    intentionally divergent, but in that case the downstream repository cannot claim
    exact alignment with the template commit and the source pin must remain unchanged.
    """
    if manifest.get("mode") != "existing_project_adoption" or alignment_issues:
        return False

    updated = dict(manifest)
    updated["files"] = sorted(manifest_files)
    template_commit = _template_head_hash(template_root)
    if template_commit:
        updated["source_commit"] = template_commit

    if updated == manifest:
        return False

    write_json(destination_root / MANIFEST_FILENAME, updated)
    return True


def sync(
    destination_root: Path,
    *,
    confirm: bool = False,
    file_filter: str | None = None,
    template_root: Path | None = None,
) -> int:
    manifest = _load_manifest(destination_root)
    recorded_manifest_files: list[str] = list(manifest.get("files", []))
    if template_root is None:
        template_root = workspace_path(".")

    # A filtered sync intentionally does not evolve the managed set or source pin:
    # it cannot prove that every managed file is synchronized to the template commit.
    manifest_files = recorded_manifest_files if file_filter else _current_adoption_manifest_files(template_root, manifest)
    preserve = _preserve_path(destination_root)
    changes = _files_needing_sync(template_root, destination_root, manifest_files, preserve, file_filter)

    newly_managed = sorted(set(manifest_files) - set(recorded_manifest_files))
    template_commit = _template_head_hash(template_root) if not file_filter else ""
    source_pin_change = bool(
        manifest.get("mode") == "existing_project_adoption"
        and template_commit
        and manifest.get("source_commit") != template_commit
    )
    manifest_evolution = bool(newly_managed or source_pin_change)

    if not changes and not manifest_evolution:
        print("  All manifest files are up to date. Nothing to sync.")
        return 0

    if changes:
        print(f"  {len(changes)} file(s) differ:")
        for relative_path, reason in changes:
            marker = "!" if reason == "removed-from-template" else "+"
            print(f"    [{marker}] {relative_path}  ({reason})")

    if newly_managed:
        print(f"  {len(newly_managed)} newly managed adoption file(s) discovered:")
        for relative_path in newly_managed:
            print(f"    [+] {relative_path}")

    if source_pin_change:
        print(f"  Adoption source pin: {manifest.get('source_commit', '')} -> {template_commit}")

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
        source = _template_source_path(template_root, relative_path)
        destination = destination_root / relative_path
        copy_file(source, destination, dry_run=False)
        copied += 1
        print(f"  SYNC {relative_path}")

    manifest_updated = False
    if not file_filter:
        # Re-check the full managed surface without preserve exclusions. This makes
        # source_commit a proven exact-alignment claim rather than a best-effort sync
        # marker. It also catches missing files, template removals, preserved drift,
        # or any copy that failed to produce byte-identical content.
        alignment_issues = _files_needing_sync(
            template_root,
            destination_root,
            manifest_files,
            preserve=set(),
        )
        manifest_updated = _write_adoption_manifest_if_safe(
            destination_root,
            manifest=manifest,
            manifest_files=manifest_files,
            template_root=template_root,
            alignment_issues=alignment_issues,
        )
        if alignment_issues and manifest.get("mode") == "existing_project_adoption":
            print("  HOLD adoption manifest/source pin: managed files are not fully aligned with the template.")
            for relative_path, reason in alignment_issues:
                print(f"    [!] {relative_path}  ({reason})")

    if manifest_updated:
        print(f"  SYNC {MANIFEST_FILENAME} (managed set/source pin)")

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
