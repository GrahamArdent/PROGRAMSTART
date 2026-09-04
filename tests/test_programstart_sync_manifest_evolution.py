from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from scripts import programstart_sync as sync


def _registry() -> dict:
    return {
        "version": "test",
        "workspace": {
            "name": "PROGRAMSTART",
            "description": "template",
            "generated_repo_prompt_policy": {
                "allowed_prompt_classes": ["workflow"],
                "support_files": ["docs/NEW_GUIDE.md"],
            },
        },
        "validation": {"enforce_engineering_ready_in_all": False},
        "repo_boundary_policy": {"enabled": True},
        "integrity": {"baselines": []},
        "systems": {
            "programbuild": {
                "control_files": [
                    "PROGRAMBUILD/CURRENT.md",
                    "PROGRAMBUILD/STATE.json",
                ],
                "output_files": [],
            }
        },
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/STATE.json",
                "active_key": "current_stage",
                "initial_step": "inputs",
                "step_order": ["inputs"],
            }
        },
        "prompt_registry": {
            "workflow_prompt_files": [".github/prompts/flow.prompt.md"],
            "operator_prompt_files": [],
            "internal_prompt_files": [],
        },
        "prompt_authority": {
            ".github/prompts/flow.prompt.md": {"class": "workflow"},
        },
        "workflow_guidance": {},
        "planning_reference_rules": {},
        "metadata_rules": {},
    }


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _setup(tmp_path: Path, *, conflict_new_asset: bool = False, retired: bool = False):
    template = tmp_path / "template"
    dest = tmp_path / "dest"
    template.mkdir()
    dest.mkdir()

    registry = _registry()
    _write(template / "config/process-registry.json", json.dumps(registry))
    _write(template / "PROGRAMBUILD/CURRENT.md", "current-control\n")
    _write(template / ".github/prompts/flow.prompt.md", "current-prompt\n")
    _write(template / "docs/NEW_GUIDE.md", "new-guide\n")

    _write(dest / "PROGRAMBUILD/CURRENT.md", "current-control\n")
    _write(dest / ".github/prompts/flow.prompt.md", "current-prompt\n")
    _write(
        dest / "config/process-registry.json",
        json.dumps(
            {
                "version": "old",
                "workspace": {
                    "name": "ExampleProject",
                    "description": "Project-owned description",
                    "repo_role": "existing_project_repo",
                },
            }
        ),
    )
    if conflict_new_asset:
        _write(dest / "docs/NEW_GUIDE.md", "project-owned-different-content\n")
    if retired:
        _write(dest / "docs/OLD_GUIDE.md", "old-managed-file\n")

    manifest_files = [
        "PROGRAMBUILD/CURRENT.md",
        ".github/prompts/flow.prompt.md",
    ]
    if retired:
        manifest_files.append("docs/OLD_GUIDE.md")
    manifest = {
        "programstart_version": "1.0.0",
        "source_commit": "oldsha",
        "attached_at": "2026-08-25T00:00:00+00:00",
        "mode": "existing_project_adoption",
        "project_name": "ExampleProject",
        "variant": "product",
        "files": sorted(manifest_files),
    }
    _write(dest / ".programstart-manifest.json", json.dumps(manifest, indent=2) + "\n")
    return template, dest


def test_old_adoption_manifest_discovers_new_managed_asset_in_dry_run(tmp_path: Path, capsys):
    template, dest = _setup(tmp_path)

    with patch.object(sync, "_template_head_hash", return_value="newsha"):
        result = sync.sync(dest, template_root=template)

    assert result == 0
    output = capsys.readouterr().out
    assert "docs/NEW_GUIDE.md" in output
    assert "new-managed" in output
    assert "derived-registry-changed" in output
    assert "managed-set/provenance-refresh" in output
    assert not (dest / "docs/NEW_GUIDE.md").exists()


def test_confirm_adds_new_managed_asset_and_refreshes_registry_and_manifest(tmp_path: Path):
    template, dest = _setup(tmp_path)

    with patch.object(sync, "_template_head_hash", return_value="newsha"):
        result = sync.sync(dest, confirm=True, template_root=template)

    assert result == 0
    assert (dest / "docs/NEW_GUIDE.md").read_text(encoding="utf-8") == "new-guide\n"

    manifest = json.loads((dest / ".programstart-manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_commit"] == "newsha"
    assert "docs/NEW_GUIDE.md" in manifest["files"]
    assert "config/process-registry.json" in manifest["derived_files"]
    assert manifest["attached_at"] == "2026-08-25T00:00:00+00:00"
    assert manifest["last_synced_at"]

    derived_registry = json.loads((dest / "config/process-registry.json").read_text(encoding="utf-8"))
    assert derived_registry["workspace"]["name"] == "ExampleProject"
    assert derived_registry["workspace"]["description"] == "Project-owned description"
    assert "docs/NEW_GUIDE.md" in derived_registry["workspace"]["bootstrap_assets"]
    assert "docs/NEW_GUIDE.md" not in derived_registry["systems"]["programbuild"]["control_files"]


def test_new_managed_path_conflict_is_not_overwritten_or_claimed(tmp_path: Path):
    template, dest = _setup(tmp_path, conflict_new_asset=True)
    original_manifest = (dest / ".programstart-manifest.json").read_text(encoding="utf-8")

    with patch.object(sync, "_template_head_hash", return_value="newsha"):
        result = sync.sync(dest, confirm=True, template_root=template)

    assert result == 2
    assert (dest / "docs/NEW_GUIDE.md").read_text(encoding="utf-8") == "project-owned-different-content\n"
    assert (dest / ".programstart-manifest.json").read_text(encoding="utf-8") == original_manifest


def test_retired_managed_file_is_preserved_but_removed_from_refreshed_manifest(tmp_path: Path):
    template, dest = _setup(tmp_path, retired=True)

    with patch.object(sync, "_template_head_hash", return_value="newsha"):
        result = sync.sync(dest, confirm=True, template_root=template)

    assert result == 0
    assert (dest / "docs/OLD_GUIDE.md").read_text(encoding="utf-8") == "old-managed-file\n"
    manifest = json.loads((dest / ".programstart-manifest.json").read_text(encoding="utf-8"))
    assert "docs/OLD_GUIDE.md" not in manifest["files"]
    assert "docs/NEW_GUIDE.md" in manifest["files"]


def test_filtered_sync_does_not_claim_full_managed_set_or_provenance(tmp_path: Path):
    template, dest = _setup(tmp_path)
    _write(template / "PROGRAMBUILD/CURRENT.md", "updated-control\n")
    original_manifest = json.loads((dest / ".programstart-manifest.json").read_text(encoding="utf-8"))

    with patch.object(sync, "_template_head_hash", return_value="newsha"):
        result = sync.sync(
            dest,
            confirm=True,
            file_filter="PROGRAMBUILD/*",
            template_root=template,
        )

    assert result == 0
    assert (dest / "PROGRAMBUILD/CURRENT.md").read_text(encoding="utf-8") == "updated-control\n"
    manifest = json.loads((dest / ".programstart-manifest.json").read_text(encoding="utf-8"))
    assert manifest == original_manifest
    assert not (dest / "docs/NEW_GUIDE.md").exists()


def test_legacy_manifest_keeps_fixed_file_list_semantics(tmp_path: Path, capsys):
    template, dest = _setup(tmp_path)
    manifest_path = dest / ".programstart-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.pop("mode")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    result = sync.sync(dest, confirm=True, template_root=template)

    assert result == 0
    assert not (dest / "docs/NEW_GUIDE.md").exists()
    refreshed = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert refreshed == manifest
    assert "new-managed" not in capsys.readouterr().out
