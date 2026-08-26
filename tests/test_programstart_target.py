from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from scripts import programstart_target as target


def _registry() -> dict:
    return {
        "systems": {
            "programbuild": {
                "control_files": [
                    "PROGRAMBUILD/PROGRAMBUILD.md",
                    "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                ]
            }
        },
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
            }
        },
    }


def test_prepare_links_existing_methodology_repo_without_touching_programbuild(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    template = tmp_path / "template"
    prompt = template / ".github" / "prompts" / "stage.prompt.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("# Stage Prompt\n", encoding="utf-8")

    destination = tmp_path / "email-bridge"
    programbuild = destination / "PROGRAMBUILD"
    programbuild.mkdir(parents=True)
    control = programbuild / "PROGRAMBUILD.md"
    control.write_text("# Existing Project Control\n", encoding="utf-8")
    (programbuild / "PROGRAMBUILD_STATE.json").write_text(
        json.dumps({"variant": "lite"}) + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(target, "load_registry", _registry)
    monkeypatch.setattr(target, "_managed_prompt_assets", lambda _registry: (".github/prompts/stage.prompt.md",))
    monkeypatch.setattr(target, "workspace_path", lambda relative: template / relative)
    monkeypatch.setattr(
        target,
        "_adopted_registry",
        lambda registry, *, project_name, prompt_assets: {
            "systems": registry["systems"],
            "workflow_state": registry["workflow_state"],
            "workspace": {
                "project_name": project_name,
                "bootstrap_assets": ["config/process-registry.json", *prompt_assets],
            },
            "validation": {"enforce_engineering_ready_in_all": False},
        },
    )
    monkeypatch.setattr(target, "_git_head_hash", lambda: "abc123")

    target.prepare_target_control_plane(destination, project_name="Email Bridge")

    assert control.read_text(encoding="utf-8") == "# Existing Project Control\n"
    assert (destination / ".github" / "prompts" / "stage.prompt.md").read_text(encoding="utf-8") == (
        "# Stage Prompt\n"
    )

    project_registry = json.loads(
        (destination / "config" / "process-registry.json").read_text(encoding="utf-8")
    )
    assert project_registry["workspace"]["repo_role"] == "managed_project_repo"
    assert project_registry["workspace"]["runtime_mode"] == "external_control_plane"
    assert project_registry["workspace"]["provisioning_scope"] == "external_programstart_control_plane"
    assert project_registry["validation"]["enforce_engineering_ready_in_all"] is False

    manifest = json.loads((destination / ".programstart-manifest.json").read_text(encoding="utf-8"))
    assert manifest["mode"] == "external_control_plane_link"
    assert manifest["source_commit"] == "abc123"
    assert manifest["variant"] == "lite"
    assert manifest["control_plane"] == "external_programstart_runtime"
    assert "PROGRAMBUILD/PROGRAMBUILD.md" in manifest["files"]
    assert "PROGRAMBUILD/PROGRAMBUILD_STATE.json" not in manifest["files"]


def test_prepare_refuses_to_replace_conflicting_prompt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    template = tmp_path / "template"
    prompt = template / ".github" / "prompts" / "stage.prompt.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("template\n", encoding="utf-8")

    destination = tmp_path / "repo"
    (destination / "PROGRAMBUILD").mkdir(parents=True)
    existing_prompt = destination / ".github" / "prompts" / "stage.prompt.md"
    existing_prompt.parent.mkdir(parents=True)
    existing_prompt.write_text("project-owned\n", encoding="utf-8")

    monkeypatch.setattr(target, "load_registry", _registry)
    monkeypatch.setattr(target, "_managed_prompt_assets", lambda _registry: (".github/prompts/stage.prompt.md",))
    monkeypatch.setattr(target, "workspace_path", lambda relative: template / relative)

    with pytest.raises(FileExistsError, match="would overwrite existing project file"):
        target.prepare_target_control_plane(destination)

    assert not (destination / "config" / "process-registry.json").exists()


def test_run_target_command_reexecutes_central_runtime_against_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "repo"
    registry_path = destination / "config" / "process-registry.json"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text("{}\n", encoding="utf-8")

    completed = Mock(returncode=0)
    run = Mock(return_value=completed)
    monkeypatch.setattr(target.subprocess, "run", run)

    assert target.run_target_command(destination, ["guide", "--system", "programbuild"]) == 0

    command = run.call_args.args[0]
    kwargs = run.call_args.kwargs
    assert command[:3] == [target.sys.executable, "-m", "scripts.programstart_cli"]
    assert command[3:] == ["guide", "--system", "programbuild"]
    assert kwargs["cwd"] == destination.resolve()
    assert kwargs["env"]["PROGRAMSTART_ROOT"] == str(destination.resolve())
    assert str(Path(target.__file__).resolve().parents[1]) in kwargs["env"]["PYTHONPATH"]


def test_target_rejects_factory_and_stage_mutation_commands(tmp_path: Path) -> None:
    destination = tmp_path / "repo"
    registry_path = destination / "config" / "process-registry.json"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text("{}\n", encoding="utf-8")

    for arguments in (["bootstrap"], ["advance", "--system", "programbuild"], ["closeout"]):
        with pytest.raises(ValueError, match="not allowed"):
            target.run_target_command(destination, list(arguments))


def test_target_state_surface_is_read_or_evidence_only(tmp_path: Path) -> None:
    destination = tmp_path / "repo"
    registry_path = destination / "config" / "process-registry.json"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text("{}\n", encoding="utf-8")

    target._validate_target_command(["state", "show", "--system", "programbuild"])
    target._validate_target_command(["state", "snapshot", "--label", "checkpoint"])

    with pytest.raises(ValueError, match="state mutation is intentionally disabled"):
        target._validate_target_command(["state", "set", "--system", "programbuild"])


def test_target_validation_requires_target_local_check() -> None:
    target._validate_target_command(["validate", "--check", "required-files", "--system", "programbuild"])

    with pytest.raises(ValueError, match="Bare `validate`"):
        target._validate_target_command(["validate"])

    with pytest.raises(ValueError, match="not target-local"):
        target._validate_target_command(["validate", "--check", "authority-sync"])


def test_target_cli_can_prepare_and_run_in_one_command(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    destination = tmp_path / "repo"
    destination.mkdir()
    calls: list[str] = []

    def fake_prepare(*args, **kwargs) -> None:
        calls.append("prepare")

    def fake_run(*args, **kwargs) -> int:
        calls.append("status")
        return 0

    monkeypatch.setattr(target, "prepare_target_control_plane", fake_prepare)
    monkeypatch.setattr(target, "run_target_command", fake_run)

    assert target.main(["--repo", str(destination), "--prepare", "status"]) == 0
    assert calls == ["prepare", "status"]
