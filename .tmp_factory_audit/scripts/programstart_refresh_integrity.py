from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, cast

try:
    from .programstart_common import (
        collect_registry_integrity_files,
        display_workspace_path,
        generated_outputs_root,
        load_registry,
        to_posix,
        warn_direct_script_invocation,
        workspace_path,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        collect_registry_integrity_files,
        display_workspace_path,
        generated_outputs_root,
        load_registry,
        to_posix,
        warn_direct_script_invocation,
        workspace_path,
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def integrity_config(registry: dict[str, Any]) -> dict[str, Any]:
    return cast(dict[str, Any], registry.get("integrity", {}))


def baseline_for(registry: dict[str, Any], name: str) -> dict[str, Any]:
    for baseline in cast(list[dict[str, Any]], integrity_config(registry).get("baselines", [])):
        if baseline.get("name") == name:
            return baseline
    raise KeyError(f"Missing integrity baseline: {name}")


def load_attachment_manifest(registry: dict[str, Any], name: str) -> dict[str, Any] | None:
    baseline = baseline_for(registry, name)
    manifest_path = workspace_path(str(baseline["manifest"]))
    if not manifest_path.exists():
        return None
    return cast(dict[str, Any], json.loads(manifest_path.read_text(encoding="utf-8")))


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate the manifest and verification report.")
    parser.add_argument("--date", required=True, help="Date stamp for output files, for example 2026-03-27.")
    parser.add_argument("--output-dir", default=None, help="Output directory. Defaults to outputs/.")
    args = parser.parse_args()

    registry = load_registry()
    output_dir = Path(args.output_dir) if args.output_dir else generated_outputs_root(registry)
    if not output_dir.is_absolute():
        output_dir = workspace_path(str(output_dir))
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / f"MANIFEST_{args.date}.txt"
    report_path = output_dir / f"VERIFICATION_REPORT_{args.date}.md"
    files = collect_registry_integrity_files(registry)

    manifest_lines = ["# PROGRAMSTART File Manifest", f"Generated: {args.date}", ""]
    for path in files:
        manifest_lines.append(f"{sha256(path)}  {to_posix(path).replace('/', '\\')}")
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    snapshot_baseline = baseline_for(registry, "programbuild_backup_snapshot")
    backup_root = workspace_path(str(snapshot_baseline["root"]))
    programbuild_root = workspace_path(registry["systems"]["programbuild"]["root"])
    userjourney_root = workspace_path("USERJOURNEY")
    userjourney_attached = userjourney_root.exists()
    core_folders_present = programbuild_root.exists() and backup_root.exists()
    programbuild_matches_backup = True
    compared_files = 0
    tracked_programbuild_files = (
        registry["systems"]["programbuild"]["control_files"] + registry["systems"]["programbuild"]["output_files"]
    )
    for relative_path in tracked_programbuild_files:
        relative_name = Path(relative_path).name
        backup_file = backup_root / relative_name
        current_file = programbuild_root / relative_name
        if backup_file.exists() and current_file.exists():
            compared_files += 1
            if sha256(backup_file) != sha256(current_file):
                programbuild_matches_backup = False

    userjourney_reference_manifest = load_attachment_manifest(registry, "userjourney_attachment_reference")
    userjourney_reference_manifest_present = userjourney_reference_manifest is not None
    userjourney_expected_files = registry["systems"]["userjourney"]["core_files"]
    userjourney_present_files = sum(1 for relative_path in userjourney_expected_files if workspace_path(relative_path).exists())
    userjourney_allowlisted_paths = len(cast(list[str], (userjourney_reference_manifest or {}).get("allowed_external_paths", [])))
    userjourney_verification_mode = str((userjourney_reference_manifest or {}).get("verification_mode", "not configured"))
    userjourney_source_workspace = str((userjourney_reference_manifest or {}).get("source_workspace", "not configured"))

    report_lines = [
        "# PROGRAMSTART Verification Report",
        "",
        f"Date: {args.date}",
        f"Status: {'PASS' if core_folders_present else 'FAIL'}",
        "",
        "## Verified Structure",
        "",
        f"- Root: {'present' if workspace_path('.').exists() else 'missing'}",
        f"- PROGRAMBUILD/: {'present' if programbuild_root.exists() else 'missing'}",
        f"- USERJOURNEY/: {'present (optional attachment)' if userjourney_attached else 'not attached (optional)'}",
        f"- {snapshot_baseline['root']}/: {'present' if backup_root.exists() else 'missing'}",
        (
            "- USERJOURNEY integrity manifest: present"
            if userjourney_attached and userjourney_reference_manifest_present
            else "- USERJOURNEY integrity manifest: missing"
            if userjourney_attached
            else "- USERJOURNEY integrity manifest: not applicable (attachment not present)"
        ),
        "",
        "## Inventory Counts",
        "",
        f"- PROGRAMBUILD file count: {len(list(programbuild_root.glob('*.md')))}",
        (
            f"- USERJOURNEY file count: {len(list(userjourney_root.glob('*.md')))}"
            if userjourney_attached
            else "- USERJOURNEY file count: not applicable (attachment not present)"
        ),
        (
            f"- USERJOURNEY declared core files present: {userjourney_present_files}/{len(userjourney_expected_files)}"
            if userjourney_attached
            else "- USERJOURNEY declared core files present: not applicable (attachment not present)"
        ),
        f"- Backup snapshot file count: {len(list(backup_root.glob('*.md')))}",
        f"- Total tracked repo files in manifest: {len(files)}",
        "",
        "## Integrity Checks",
        "",
        f"- PROGRAMBUILD files compared against backup snapshot using SHA-256: {compared_files} files",
        f"- PROGRAMBUILD files match backup snapshot: {'yes' if programbuild_matches_backup else 'no'}",
        (
            f"- USERJOURNEY attachment source workspace: {userjourney_source_workspace}"
            if userjourney_attached and userjourney_reference_manifest_present
            else "- USERJOURNEY attachment source workspace: not configured"
            if userjourney_attached
            else "- USERJOURNEY attachment source workspace: not applicable (attachment not present)"
        ),
        (
            f"- USERJOURNEY verification mode: {userjourney_verification_mode}"
            if userjourney_attached and userjourney_reference_manifest_present
            else "- USERJOURNEY verification mode: not configured"
            if userjourney_attached
            else "- USERJOURNEY verification mode: not applicable (attachment not present)"
        ),
        (
            f"- USERJOURNEY allowlisted external implementation paths: {userjourney_allowlisted_paths}"
            if userjourney_attached and userjourney_reference_manifest_present
            else "- USERJOURNEY allowlisted external implementation paths: 0"
            if userjourney_attached
            else "- USERJOURNEY allowlisted external implementation paths: not applicable (attachment not present)"
        ),
        "- Registry-declared workspace assets, attached system files, and integrity baselines included in manifest",
        "",
        "## Result",
        "",
        f"- All required template folders are {'present' if core_folders_present else 'not fully present'}.",
        f"- PROGRAMBUILD matches the preserved backup snapshot: {'yes' if programbuild_matches_backup else 'no'}.",
        "- A mismatch against the preserved backup indicates intentional "
        "workspace evolution unless unexpected edits were made to the backup itself.",
        "- Temp, generated, and previously emitted integrity artifacts are excluded from manifest collection.",
        (
            "- USERJOURNEY attachment integrity is tracked through the declared core files and integrity reference manifest."
            if userjourney_attached and userjourney_reference_manifest_present
            else "- USERJOURNEY attachment integrity is not fully configured until its reference manifest is present."
            if userjourney_attached
            else "- USERJOURNEY attachment integrity is not applicable when the attachment is absent."
        ),
    ]
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Wrote {display_workspace_path(manifest_path)}")
    print(f"Wrote {display_workspace_path(report_path)}")
    return 0 if core_folders_present else 1


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart refresh' or 'pb refresh'")
    raise SystemExit(main())
