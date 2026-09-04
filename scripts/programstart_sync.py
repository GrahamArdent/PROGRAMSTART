from __future__ import annotations

import argparse
import filecmp
import json
import subprocess
import sys
from datetime import UTC, datetime
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

try:
    from .programstart_adopt import _adopted_registry, _managed_prompt_assets
    from .programstart_attach import MANIFEST_FILENAME, PROGRAMBUILD_PRESERVE_EXISTING_FILES
    from .programstart_bootstrap import (
        WORKFLOW_DESTINATION_PREFIX,
        WORKFLOW_TEMPLATE_PREFIX,
        copy_file,
    )
    from .programstart_common import load_registry_from_path, warn_direct_script_invocation, workspace_path, write_json
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_adopt import _adopted_registry, _managed_prompt_assets
    from programstart_attach import MANIFEST_FILENAME, PROGRAMBUILD_PRESERVE_EXISTING_FILES
    from programstart_bootstrap import (
        WORKFLOW_DESTINATION_PREFIX,
        WORKFLOW_TEMPLATE_PREFIX,
        copy_file,
    )

    from programstart_common import load_registry_from_path, warn_direct_script_invocation, workspace_path, write_json

SYNC_DESCRIPTION = (
    "Propagate changed PROGRAMSTART files to/from a downstream repo.\n\n"
    "Push mode (--dest): copies changed files from the PROGRAMSTART template to a\n"
    "downstream repo.  Pull mode (--from-template): copies changed files from an\n"
    "upstream PROGRAMSTART template into the current (or --dest) repo.\n\n"
    "Reads the .programstart-manifest.json written at attach/adopt time. For lean\n"
    "managed overlays, sync also derives the current managed control set from the\n"
    "current template so later PROGRAMSTART assets can be discovered safely.\n"
    "Without --confirm the command runs in dry-run mode and shows what would change."
)


def _load_manifest(destination_root: Path) -> dict[str, Any]:
    manifest_path = destination_root / MANIFEST_FILENAME
    if not manifest_path.exists():
        print(f"ERROR: No manifest found at {manifest_path}", file=sys.stderr)
        print("  The destination may not have been attached with a manifest-aware version.", file=sys.stderr)
        print("  Re-attach/adopt with a current manifest-aware PROGRAMSTART version.", file=sys.stderr)
        raise SystemExit(1)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Manifest at {manifest_path} must be a JSON object")
    return payload


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
    """Resolve a downstream manifest path back to its source in the template repo."""
    direct = template_root / relative_path
    if direct.exists():
        return direct
    if relative_path.startswith(WORKFLOW_DESTINATION_PREFIX):
        suffix = relative_path.removeprefix(WORKFLOW_DESTINATION_PREFIX)
        dormant = template_root / WORKFLOW_TEMPLATE_PREFIX / suffix
        if dormant.exists():
            return dormant
    return direct


def _matches_filter(path: str, pattern: str) -> bool:
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


def _is_lean_managed_overlay(manifest: dict[str, Any]) -> bool:
    mode = str(manifest.get("mode") or "")
    return (
        mode == "existing_project_adoption"
        or mode.startswith("external_control")
        or manifest.get("control_plane") == "external_programstart_runtime"
    )


def _current_overlay_context(
    template_root: Path,
    manifest: dict[str, Any],
) -> tuple[dict[str, Any], tuple[str, ...], list[str]]:
    del manifest  # reserved for future mode-specific managed-set distinctions
    registry = load_registry_from_path(template_root / "config" / "process-registry.json")
    prompt_assets = _managed_prompt_assets(registry)
    state_file = registry["workflow_state"]["programbuild"]["state_file"]
    control_files = [path for path in registry["systems"]["programbuild"]["control_files"] if path != state_file]
    managed_files = sorted(set([*control_files, *prompt_assets]))
    return registry, prompt_assets, managed_files


def _expected_overlay_registry(
    template_registry: dict[str, Any],
    manifest: dict[str, Any],
    prompt_assets: tuple[str, ...],
    destination_root: Path,
) -> dict[str, Any]:
    project_name = str(manifest.get("project_name") or destination_root.name)
    expected = _adopted_registry(
        template_registry,
        project_name=project_name,
        prompt_assets=prompt_assets,
    )

    workspace = dict(expected.get("workspace", {}))
    current_path = destination_root / "config" / "process-registry.json"
    if current_path.exists():
        try:
            current = json.loads(current_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            current = {}
        if isinstance(current, dict):
            current_workspace_value = current.get("workspace")
            current_workspace = current_workspace_value if isinstance(current_workspace_value, dict) else {}
            for key in ("name", "description"):
                if current_workspace.get(key):
                    workspace[key] = current_workspace[key]

    mode = str(manifest.get("mode") or "")
    if manifest.get("control_plane") == "external_programstart_runtime" or mode.startswith("external_control"):
        workspace.update(
            {
                "repo_role": "managed_project_repo",
                "repo_boundary": "standalone_project_repo",
                "provisioning_scope": "external_programstart_control_plane",
                "runtime_mode": "external_control_plane",
            }
        )
    expected["workspace"] = workspace
    return expected


def _registry_needs_refresh(destination_root: Path, expected: dict[str, Any]) -> bool:
    path = destination_root / "config" / "process-registry.json"
    if not path.exists():
        return True
    try:
        current = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return True
    return current != expected


def _files_needing_sync(
    template_root: Path,
    destination_root: Path,
    managed_files: list[str],
    preserve: set[str],
    file_filter: str | None = None,
    newly_managed: set[str] | None = None,
) -> list[tuple[str, str]]:
    """Return (relative_path, reason) for managed files that need attention."""
    results: list[tuple[str, str]] = []
    newly_managed = newly_managed or set()
    for relative_path in managed_files:
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
            reason = "new-managed" if relative_path in newly_managed else "missing-in-dest"
            results.append((relative_path, reason))
            continue
        if not filecmp.cmp(source, destination, shallow=False):
            reason = "new-managed-conflict" if relative_path in newly_managed else "changed"
            results.append((relative_path, reason))
    return results


def _manifest_needs_refresh(
    manifest: dict[str, Any],
    current_files: list[str],
    template_commit: str,
) -> bool:
    if sorted(set(manifest.get("files", []))) != current_files:
        return True
    return bool(template_commit and str(manifest.get("source_commit") or "") != template_commit)


def _refresh_manifest(
    destination_root: Path,
    manifest: dict[str, Any],
    *,
    current_files: list[str],
    template_commit: str,
    derived_registry: bool,
) -> None:
    refreshed = dict(manifest)
    refreshed["files"] = current_files
    if template_commit:
        refreshed["source_commit"] = template_commit
    refreshed["last_synced_at"] = datetime.now(UTC).isoformat()
    if derived_registry:
        derived_files = list(refreshed.get("derived_files") or [])
        if "config/process-registry.json" not in derived_files:
            derived_files.append("config/process-registry.json")
        refreshed["derived_files"] = sorted(set(derived_files))
    write_json(destination_root / MANIFEST_FILENAME, refreshed)


def sync(
    destination_root: Path,
    *,
    confirm: bool = False,
    file_filter: str | None = None,
    template_root: Path | None = None,
) -> int:
    manifest = _load_manifest(destination_root)
    if template_root is None:
        template_root = workspace_path(".")
    template_root = template_root.resolve()
    preserve = _preserve_path(destination_root)

    original_files = sorted({str(path) for path in manifest.get("files", [])})
    lean_overlay = _is_lean_managed_overlay(manifest)
    template_registry: dict[str, Any] | None = None
    prompt_assets: tuple[str, ...] = ()
    expected_registry: dict[str, Any] | None = None
    registry_refresh_needed = False

    if lean_overlay:
        template_registry, prompt_assets, managed_files = _current_overlay_context(template_root, manifest)
        newly_managed = set(managed_files) - set(original_files)
        retired_files = sorted(set(original_files) - set(managed_files))
        if file_filter is None:
            expected_registry = _expected_overlay_registry(
                template_registry,
                manifest,
                prompt_assets,
                destination_root,
            )
            registry_refresh_needed = _registry_needs_refresh(destination_root, expected_registry)
    else:
        managed_files = original_files
        newly_managed = set()
        retired_files = []

    changes = _files_needing_sync(
        template_root,
        destination_root,
        managed_files,
        preserve,
        file_filter,
        newly_managed,
    )
    preserved_alignment_issues: list[tuple[str, str]] = []
    if lean_overlay and file_filter is None and preserve:
        all_pre_sync_issues = _files_needing_sync(
            template_root,
            destination_root,
            managed_files,
            preserve=set(),
            newly_managed=newly_managed,
        )
        preserved_alignment_issues = [(path, reason) for path, reason in all_pre_sync_issues if path in preserve]

    template_commit = _template_head_hash(template_root) if lean_overlay and file_filter is None else ""
    manifest_refresh_needed = (
        lean_overlay and file_filter is None and _manifest_needs_refresh(manifest, managed_files, template_commit)
    )

    if (
        not changes
        and not retired_files
        and not registry_refresh_needed
        and not manifest_refresh_needed
        and not preserved_alignment_issues
    ):
        print("  All manifest files are up to date. Nothing to sync.")
        return 0

    if changes:
        print(f"  {len(changes)} managed file(s) need attention:")
        for relative_path, reason in changes:
            marker = "!" if reason in {"removed-from-template", "new-managed-conflict"} else "+"
            print(f"    [{marker}] {relative_path}  ({reason})")
    if preserved_alignment_issues:
        print(f"  {len(preserved_alignment_issues)} preserved managed file(s) prevent exact alignment:")
        for relative_path, reason in preserved_alignment_issues:
            print(f"    [!] {relative_path}  (preserved-{reason})")
    if retired_files:
        print(f"  {len(retired_files)} file(s) retired from the current managed set (preserved in destination):")
        for relative_path in retired_files:
            print(f"    [~] {relative_path}  (retired-from-managed-set)")
    if registry_refresh_needed:
        print("    [+] config/process-registry.json  (derived-registry-changed)")
    if manifest_refresh_needed:
        print(f"    [+] {MANIFEST_FILENAME}  (managed-set/provenance-refresh)")
    if lean_overlay and file_filter is not None:
        print("  NOTE: filtered sync does not refresh full managed-set/provenance metadata.")

    blockers = [
        (path, reason)
        for path, reason in changes
        if reason == "new-managed-conflict" or (lean_overlay and reason == "removed-from-template")
    ]
    if blockers:
        print()
        print("  ERROR: Managed-set reconciliation has conflicts/template gaps; no full provenance refresh is safe.")
        for path, reason in blockers:
            print(f"    {path}: {reason}")
        return 2 if confirm else 0

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
        if reason in {"changed", "missing-in-dest", "new-managed"}:
            source = _template_source_path(template_root, relative_path)
            destination = destination_root / relative_path
            copy_file(source, destination, dry_run=False)
            copied += 1
            print(f"  SYNC {relative_path} ({reason})")

    alignment_issues: list[tuple[str, str]] = []
    if lean_overlay and file_filter is None:
        # Preserve policy controls copying, not provenance truth. Re-check the full
        # current managed set without preserve exclusions after safe copies complete.
        # Any remaining difference means the target cannot claim exact alignment with
        # the template commit, even when the difference is intentionally preserved.
        alignment_issues = _files_needing_sync(
            template_root,
            destination_root,
            managed_files,
            preserve=set(),
            newly_managed=set(),
        )

    if lean_overlay and file_filter is None and alignment_issues:
        print("  HOLD derived registry and manifest/source provenance: managed files are not fully aligned.")
        for relative_path, reason in alignment_issues:
            print(f"    [!] {relative_path}  ({reason})")
        print()
        print(f"  Synced {copied} managed file(s), skipped {skipped}; full reconciliation remains blocked.")
        return 2

    if lean_overlay and file_filter is None and expected_registry is not None and registry_refresh_needed:
        write_json(destination_root / "config" / "process-registry.json", expected_registry)
        print("  SYNC config/process-registry.json (derived registry)")

    if lean_overlay and file_filter is None:
        _refresh_manifest(
            destination_root,
            manifest,
            current_files=managed_files,
            template_commit=template_commit,
            derived_registry=expected_registry is not None,
        )
        print(f"  SYNC {MANIFEST_FILENAME} (managed set/provenance)")

    print()
    print(f"  Synced {copied} managed file(s), skipped {skipped}.")
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