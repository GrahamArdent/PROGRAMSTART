from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import programstart_adopt as adopt


def _registry() -> dict:
    return {
        "workspace": {"bootstrap_assets": ["pyproject.toml"]},
        "systems": {
            "programbuild": {
                "control_files": [
                    "PROGRAMBUILD/PROGRAMBUILD.md",
                    "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                ],
                "output_files": ["PROGRAMBUILD/REQUIREMENTS.md"],
            }
        },
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "active_key": "active_stage",
                "initial_step": "inputs_and_mode_selection",
                "step_order": ["inputs_and_mode_selection"],
            }
        },
        "prompt_registry": {
            "workflow_prompt_files": [".github/prompts/stage.prompt.md"],
            "operator_prompt_files": [],
            "internal_prompt_files": [],
        },
        "prompt_authority": {
            ".github/prompts/stage.prompt.md": {
                "authority_files": ["PROGRAMBUILD/PROGRAMBUILD.md"]
            }
        },
        "workflow_guidance": {"operator": {"unused": {}}, "programbuild": {}},
        "validation": {"enforce_engineering_ready_in_all": True},
        "integrity": {"baselines": [{"name": "template"}]},
        "repo_boundary_policy": {"enabled": True, "docs": ["README.md"]},
    }


def _fake_bootstrap(destination: Path, _registry: dict, variant: str, dry_run: bool) -> None:
    if dry_run:
        return
    pb = destination / "PROGRAMBUILD"
    pb.mkdir(parents=True)
    (pb / "PROGRAMBUILD.md").write_text("# Program Build\n", encoding="utf-8")
    (pb / "PROGRAMBUILD_STATE.json").write_text(
        json.dumps({"variant": variant}) + "\n",
        encoding="utf-8",
    )
    (pb / "REQUIREMENTS.md").write_text(
        "Purpose: Requirements\n---\n\n",
        encoding="utf-8",
    )


def test_adopt_preserves_host_toolchain_and_tracks_only_managed_methodology(
    tmp_path: Path,
    monkeypatch,
) -> None:
    template = tmp_path / "template"
    prompt = template / ".github" / "prompts" / "stage.prompt.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("# Stage Prompt\n", encoding="utf-8")

    destination = tmp_path / "existing"
    destination.mkdir()
    (destination / "README.md").write_text("host readme\n", encoding="utf-8")
    (destination / "pyproject.toml").write_text(
        "[project]\nname='host'\n",
        encoding="utf-8",
    )

    registry = _registry()
    monkeypatch.setattr(adopt, "load_registry", lambda: registry)
    monkeypatch.setattr(
        adopt,
        "_managed_prompt_assets",
        lambda _registry: (".github/prompts/stage.prompt.md",),
    )
    monkeypatch.setattr(adopt, "workspace_path", lambda relative: template / relative)
    monkeypatch.setattr(adopt, "bootstrap_programbuild", _fake_bootstrap)
    monkeypatch.setattr(adopt, "_git_head_hash", lambda: "abc123")

    adopt.adopt_programbuild(destination, project_name="Existing App", variant="product")

    assert (destination / "README.md").read_text(encoding="utf-8") == "host readme\n"
    assert (destination / "pyproject.toml").read_text(encoding="utf-8") == (
        "[project]\nname='host'\n"
    )
    assert (destination / ".github" / "prompts" / "stage.prompt.md").exists()

    project_registry = json.loads(
        (destination / "config" / "process-registry.json").read_text(encoding="utf-8")
    )
    assert project_registry["workspace"]["repo_role"] == "existing_project_repo"
    assert (
        project_registry["workspace"]["provisioning_scope"]
        == "programbuild_management_overlay_only"
    )
    assert "pyproject.toml" not in project_registry["workspace"]["bootstrap_assets"]
    assert project_registry["validation"]["enforce_engineering_ready_in_all"] is False

    manifest = json.loads(
        (destination / ".programstart-manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["mode"] == "existing_project_adoption"
    assert manifest["source_commit"] == "abc123"
    assert "PROGRAMBUILD/PROGRAMBUILD.md" in manifest["files"]
    assert ".github/prompts/stage.prompt.md" in manifest["files"]
    assert "PROGRAMBUILD/PROGRAMBUILD_STATE.json" not in manifest["files"]
    assert "PROGRAMBUILD/REQUIREMENTS.md" not in manifest["files"]
    assert "config/process-registry.json" not in manifest["files"]


def test_adopt_refuses_to_overwrite_existing_prompt(tmp_path: Path, monkeypatch) -> None:
    template = tmp_path / "template"
    prompt = template / ".github" / "prompts" / "stage.prompt.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("template\n", encoding="utf-8")

    destination = tmp_path / "existing"
    existing = destination / ".github" / "prompts" / "stage.prompt.md"
    existing.parent.mkdir(parents=True)
    existing.write_text("host\n", encoding="utf-8")

    monkeypatch.setattr(adopt, "load_registry", _registry)
    monkeypatch.setattr(
        adopt,
        "_managed_prompt_assets",
        lambda _registry: (".github/prompts/stage.prompt.md",),
    )
    monkeypatch.setattr(adopt, "workspace_path", lambda relative: template / relative)

    with pytest.raises(FileExistsError, match="would overwrite existing project file"):
        adopt.adopt_programbuild(destination, project_name="Existing App")

    assert not (destination / "PROGRAMBUILD").exists()


def test_adopt_dry_run_does_not_modify_repo(tmp_path: Path, monkeypatch, capsys) -> None:
    destination = tmp_path / "existing"
    destination.mkdir()
    monkeypatch.setattr(adopt, "load_registry", _registry)
    monkeypatch.setattr(adopt, "_managed_prompt_assets", lambda _registry: ())
    monkeypatch.setattr(adopt, "bootstrap_programbuild", _fake_bootstrap)

    adopt.adopt_programbuild(
        destination,
        project_name="Existing App",
        variant="lite",
        dry_run=True,
    )

    assert "ADOPT PROGRAMBUILD" in capsys.readouterr().out
    assert not (destination / "PROGRAMBUILD").exists()
    assert not (destination / ".programstart-manifest.json").exists()
