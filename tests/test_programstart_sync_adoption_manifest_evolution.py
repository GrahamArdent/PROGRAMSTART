from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from scripts import programstart_sync as sync


def _registry(*, support_files: list[str]) -> dict:
    return {
        "workspace": {
            "generated_repo_prompt_policy": {
                "allowed_prompt_classes": ["workflow"],
                "support_files": support_files,
            }
        },
        "prompt_registry": {
            "workflow_prompt_files": [],
            "operator_prompt_files": [],
            "internal_prompt_files": [],
        },
        "workflow_guidance": {},
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
            }
        },
        "systems": {
            "programbuild": {
                "control_files": [
                    "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md",
                    "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                ]
            }
        },
    }


def _write_manifest(
    destination: Path,
    *,
    mode: str = "existing_project_adoption",
    source_commit: str = "old-template",
    files: list[str] | None = None,
) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    payload = {
        "programstart_version": "1.0.0",
        "source_commit": source_commit,
        "attached_at": "2026-09-01T00:00:00+00:00",
        "mode": mode,
        "project_name": "Example",
        "variant": "enterprise",
        "files": files or ["PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md"],
    }
    (destination / ".programstart-manifest.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def _read_manifest(destination: Path) -> dict:
    return json.loads((destination / ".programstart-manifest.json").read_text(encoding="utf-8"))


def _write_template_file(template: Path, relative_path: str, content: str) -> None:
    path = template / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_full_adoption_sync_discovers_new_support_file_and_advances_pin(tmp_path: Path) -> None:
    template = tmp_path / "template"
    destination = tmp_path / "destination"
    support = "docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md"

    _write_template_file(template, "config/process-registry.json", "{}\n")
    _write_template_file(template, "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "canonical\n")
    _write_template_file(template, support, "autonomy\n")
    _write_manifest(destination)
    _write_template_file(destination, "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "canonical\n")

    with (
        patch.object(sync, "load_registry_from_path", return_value=_registry(support_files=[support])),
        patch.object(sync, "_template_head_hash", return_value="new-template"),
    ):
        assert sync.sync(destination, confirm=True, template_root=template) == 0

    assert (destination / support).read_text(encoding="utf-8") == "autonomy\n"
    manifest = _read_manifest(destination)
    assert manifest["source_commit"] == "new-template"
    assert support in manifest["files"]
    assert "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md" in manifest["files"]
    assert "PROGRAMBUILD/PROGRAMBUILD_STATE.json" not in manifest["files"]


def test_adoption_sync_dry_run_reports_but_does_not_evolve_manifest(tmp_path: Path) -> None:
    template = tmp_path / "template"
    destination = tmp_path / "destination"
    support = "docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md"

    _write_template_file(template, "config/process-registry.json", "{}\n")
    _write_template_file(template, "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "canonical\n")
    _write_template_file(template, support, "autonomy\n")
    _write_manifest(destination)
    _write_template_file(destination, "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "canonical\n")
    before = _read_manifest(destination)

    with (
        patch.object(sync, "load_registry_from_path", return_value=_registry(support_files=[support])),
        patch.object(sync, "_template_head_hash", return_value="new-template"),
    ):
        assert sync.sync(destination, template_root=template) == 0

    assert not (destination / support).exists()
    assert _read_manifest(destination) == before


def test_filtered_adoption_sync_does_not_evolve_manifest_or_pin(tmp_path: Path) -> None:
    template = tmp_path / "template"
    destination = tmp_path / "destination"
    support = "docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md"

    _write_template_file(template, "config/process-registry.json", "{}\n")
    _write_template_file(template, "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "new canonical\n")
    _write_template_file(template, support, "autonomy\n")
    _write_manifest(destination)
    _write_template_file(destination, "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "old canonical\n")

    with (
        patch.object(sync, "load_registry_from_path", return_value=_registry(support_files=[support])),
        patch.object(sync, "_template_head_hash", return_value="new-template"),
    ):
        assert (
            sync.sync(
                destination,
                confirm=True,
                file_filter="PROGRAMBUILD/*",
                template_root=template,
            )
            == 0
        )

    assert (destination / "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md").read_text(encoding="utf-8") == "new canonical\n"
    assert not (destination / support).exists()
    manifest = _read_manifest(destination)
    assert manifest["source_commit"] == "old-template"
    assert support not in manifest["files"]


def test_legacy_attachment_manifest_keeps_frozen_file_set(tmp_path: Path) -> None:
    template = tmp_path / "template"
    destination = tmp_path / "destination"
    support = "docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md"

    _write_template_file(template, "config/process-registry.json", "{}\n")
    _write_template_file(template, "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "canonical\n")
    _write_template_file(template, support, "autonomy\n")
    _write_manifest(destination, mode="legacy_attachment")
    _write_template_file(destination, "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "canonical\n")

    with (
        patch.object(sync, "load_registry_from_path", return_value=_registry(support_files=[support])),
        patch.object(sync, "_template_head_hash", return_value="new-template"),
    ):
        assert sync.sync(destination, confirm=True, template_root=template) == 0

    assert not (destination / support).exists()
    manifest = _read_manifest(destination)
    assert manifest["source_commit"] == "old-template"
    assert support not in manifest["files"]


def test_removed_managed_file_holds_adoption_pin(tmp_path: Path) -> None:
    template = tmp_path / "template"
    destination = tmp_path / "destination"
    removed = "docs/REMOVED_PROTOCOL.md"

    _write_template_file(template, "config/process-registry.json", "{}\n")
    _write_template_file(template, "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "canonical\n")
    _write_manifest(
        destination,
        files=["PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", removed],
    )
    _write_template_file(destination, "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md", "canonical\n")
    _write_template_file(destination, removed, "historical\n")

    with (
        patch.object(sync, "load_registry_from_path", return_value=_registry(support_files=[])),
        patch.object(sync, "_template_head_hash", return_value="new-template"),
    ):
        assert sync.sync(destination, confirm=True, template_root=template) == 0

    manifest = _read_manifest(destination)
    assert manifest["source_commit"] == "old-template"
    assert removed in manifest["files"]


def test_workspace_registry_declares_authority_and_autonomy_support_files() -> None:
    root = Path(__file__).resolve().parents[1]
    workspace = json.loads((root / "config/registry/workspace.json").read_text(encoding="utf-8"))
    support_files = workspace["workspace"]["generated_repo_prompt_policy"]["support_files"]

    assert "docs/PROGRAMSTART_AUTHORITY_GAP_RECONCILIATION.md" in support_files
    assert "docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md" in support_files
