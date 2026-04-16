from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_attach as attach

# ── helpers ────────────────────────────────────────────────────────────────────


def make_valid_source(base: Path) -> Path:
    """Create a USERJOURNEY source directory with all required files."""
    source = base / "source_uj"
    source.mkdir(parents=True, exist_ok=True)
    for name in attach.REQUIRED_USERJOURNEY_FILES:
        (source / name).write_text(f"# {name}", encoding="utf-8")
    return source


def make_programbuild_template(base: Path) -> tuple[Path, dict]:
    template = base / "template"
    (template / "PROGRAMBUILD").mkdir(parents=True, exist_ok=True)
    (template / "config").mkdir(parents=True, exist_ok=True)
    (template / "PROGRAMBUILD" / "PROGRAMBUILD.md").write_text("# PROGRAMBUILD\n", encoding="utf-8")
    (template / "PROGRAMBUILD" / "PROGRAMBUILD_CANONICAL.md").write_text("# CANONICAL\n", encoding="utf-8")
    (template / "README.md").write_text("template readme\n", encoding="utf-8")
    (template / ".gitignore").write_text("template ignore\n", encoding="utf-8")
    (template / "pyproject.toml").write_text("[project]\nname='programstart'\n", encoding="utf-8")
    (template / "config" / "process-registry.json").write_text("{}\n", encoding="utf-8")
    (template / "PROGRAMBUILD" / "ARCHITECTURE.md").write_text(
        "Purpose: Architecture\n---\nReal content that should not copy\n",
        encoding="utf-8",
    )
    registry = {
        "workspace": {
            "bootstrap_assets": [
                "README.md",
                ".gitignore",
                "pyproject.toml",
                "config/process-registry.json",
            ]
        },
        "systems": {
            "programbuild": {
                "control_files": [
                    "PROGRAMBUILD/PROGRAMBUILD.md",
                    "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md",
                    "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                ],
                "output_files": ["PROGRAMBUILD/ARCHITECTURE.md"],
            }
        },
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "active_key": "current_stage",
                "initial_step": "inputs_and_mode_selection",
                "step_order": ["inputs_and_mode_selection", "feasibility_and_kill_criteria"],
            }
        },
    }
    return template, registry


# ── resolve_attachment_source ──────────────────────────────────────────────────


def test_resolve_source_accepts_direct_userjourney_dir(tmp_path: Path) -> None:
    uj = tmp_path / "USERJOURNEY"
    uj.mkdir()
    result = attach.resolve_attachment_source(str(uj))
    assert result == uj


def test_resolve_source_accepts_parent_with_nested_userjourney(tmp_path: Path) -> None:
    uj = tmp_path / "USERJOURNEY"
    uj.mkdir()
    result = attach.resolve_attachment_source(str(tmp_path))
    assert result == uj


def test_resolve_source_raises_for_nonexistent_path(tmp_path: Path) -> None:
    bad = tmp_path / "no_such_thing"
    with pytest.raises(FileNotFoundError):
        attach.resolve_attachment_source(str(bad))


def test_resolve_source_raises_when_no_userjourney_child(tmp_path: Path) -> None:
    (tmp_path / "OTHER").mkdir()
    with pytest.raises(FileNotFoundError):
        attach.resolve_attachment_source(str(tmp_path))


# ── validate_attachment_source ─────────────────────────────────────────────────


def test_validate_returns_empty_when_all_required_files_present(tmp_path: Path) -> None:
    for name in attach.REQUIRED_USERJOURNEY_FILES:
        (tmp_path / name).write_text("x", encoding="utf-8")
    assert attach.validate_attachment_source(tmp_path) == []


def test_validate_returns_missing_file_names(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    missing = attach.validate_attachment_source(tmp_path)
    assert "DELIVERY_GAMEPLAN.md" in missing
    assert "USERJOURNEY_TEMPLATE_STARTER.md" in missing


def test_validate_returns_all_files_when_directory_empty(tmp_path: Path) -> None:
    missing = attach.validate_attachment_source(tmp_path)
    assert set(missing) == attach.REQUIRED_USERJOURNEY_FILES


# ── attach_userjourney ─────────────────────────────────────────────────────────


def test_attach_dry_run_prints_without_copying(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    source = make_valid_source(tmp_path)
    dest_root = tmp_path / "dest"
    dest_root.mkdir()
    attach.attach_userjourney(dest_root, source, dry_run=True)
    captured = capsys.readouterr()
    assert "ATTACH USERJOURNEY" in captured.out
    assert not (dest_root / "USERJOURNEY").exists()


def test_attach_copies_required_files(tmp_path: Path) -> None:
    source = make_valid_source(tmp_path)
    dest_root = tmp_path / "dest"
    dest_root.mkdir()
    with (
        patch.object(attach, "load_registry", return_value={}),
        patch.object(attach, "create_default_workflow_state", return_value={"stage": "kickoff"}),
        patch.object(attach, "write_json"),
    ):
        attach.attach_userjourney(dest_root, source)
    for name in attach.REQUIRED_USERJOURNEY_FILES:
        assert (dest_root / "USERJOURNEY" / name).exists()


def test_attach_writes_state_json_when_missing(tmp_path: Path) -> None:
    source = make_valid_source(tmp_path)
    dest_root = tmp_path / "dest"
    dest_root.mkdir()
    written: list[tuple] = []
    with (
        patch.object(attach, "load_registry", return_value={}),
        patch.object(attach, "create_default_workflow_state", return_value={"stage": "kickoff"}),
        patch.object(attach, "write_json", side_effect=lambda p, d: written.append((p, d))),
    ):
        attach.attach_userjourney(dest_root, source)
    assert any("USERJOURNEY_STATE.json" in str(p) for p, _ in written)


def test_attach_raises_fileexistserror_without_force(tmp_path: Path) -> None:
    source = make_valid_source(tmp_path)
    dest_root = tmp_path / "dest"
    (dest_root / "USERJOURNEY").mkdir(parents=True)
    with pytest.raises(FileExistsError, match="--force"):
        attach.attach_userjourney(dest_root, source)


def test_attach_force_replaces_existing_destination(tmp_path: Path) -> None:
    source = make_valid_source(tmp_path)
    dest_root = tmp_path / "dest"
    dest_uj = dest_root / "USERJOURNEY"
    dest_uj.mkdir(parents=True)
    (dest_uj / "stale.md").write_text("old content", encoding="utf-8")
    with (
        patch.object(attach, "load_registry", return_value={}),
        patch.object(attach, "create_default_workflow_state", return_value={}),
        patch.object(attach, "write_json"),
    ):
        attach.attach_userjourney(dest_root, source, force=True)
    assert not (dest_uj / "stale.md").exists()
    assert (dest_uj / "README.md").exists()


def test_attach_raises_filenotfounderror_for_missing_required_source_files(tmp_path: Path) -> None:
    source = tmp_path / "bad_source"
    source.mkdir()
    dest_root = tmp_path / "dest"
    dest_root.mkdir()
    with pytest.raises(FileNotFoundError, match="required files"):
        attach.attach_userjourney(dest_root, source)


def test_attach_programbuild_dry_run_prints_without_copying(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    template_root, registry = make_programbuild_template(tmp_path)
    destination = tmp_path / "dest"
    destination.mkdir()
    with (
        patch.object(attach, "load_registry", return_value=registry),
        patch.object(
            attach, "workspace_path", side_effect=lambda relative: template_root if relative == "." else template_root / relative
        ),
    ):
        attach.attach_programbuild(destination, project_name="Orchestra Agent", dry_run=True)
    captured = capsys.readouterr()
    assert "ATTACH PROGRAMBUILD" in captured.out
    assert not (destination / "PROGRAMBUILD").exists()


def test_attach_programbuild_preserves_existing_root_files(tmp_path: Path) -> None:
    template_root, registry = make_programbuild_template(tmp_path)
    destination = tmp_path / "dest"
    destination.mkdir()
    (destination / "README.md").write_text("host readme\n", encoding="utf-8")
    (destination / ".gitignore").write_text("host ignore\n", encoding="utf-8")
    with (
        patch.object(attach, "load_registry", return_value=registry),
        patch.object(
            attach, "workspace_path", side_effect=lambda relative: template_root if relative == "." else template_root / relative
        ),
        patch.object(attach, "create_default_workflow_state", return_value={"stage": "inputs_and_mode_selection"}),
        patch.object(attach, "stamp_bootstrapped_registry") as mock_stamp,
        patch.object(attach, "sanitize_bootstrapped_secrets_baseline"),
        patch.object(attach, "refresh_secrets_baseline"),
    ):
        attach.attach_programbuild(destination, project_name="Orchestra Agent")

    assert (destination / "PROGRAMBUILD" / "PROGRAMBUILD.md").exists()
    assert (destination / "PROGRAMBUILD" / "PROGRAMBUILD_CANONICAL.md").exists()
    assert (destination / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json").exists()
    assert (destination / "pyproject.toml").exists()
    assert (destination / "config" / "process-registry.json").exists()
    assert (destination / "README.md").read_text(encoding="utf-8") == "host readme\n"
    assert (destination / ".gitignore").read_text(encoding="utf-8") == "host ignore\n"
    architecture_stub = (destination / "PROGRAMBUILD" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert architecture_stub.endswith("---\n\n")
    assert "Real content that should not copy" not in architecture_stub
    mock_stamp.assert_called_once()


def test_attach_programbuild_raises_when_programbuild_exists_without_force(tmp_path: Path) -> None:
    destination = tmp_path / "dest"
    (destination / "PROGRAMBUILD").mkdir(parents=True)
    with pytest.raises(FileExistsError, match="--force"):
        attach.attach_programbuild(destination, project_name="Orchestra Agent")


def test_attach_restores_userjourney_prompt_delta_from_shared_policy(tmp_path: Path) -> None:
    source = make_valid_source(tmp_path)
    template_root = tmp_path / "template"
    template_prompts = template_root / ".github" / "prompts"
    template_prompts.mkdir(parents=True)
    (template_prompts / "workflow.prompt.md").write_text("workflow\n", encoding="utf-8")
    (template_prompts / "shape-uj-ux-surfaces.prompt.md").write_text("userjourney\n", encoding="utf-8")
    (template_prompts / "PROMPT_STANDARD.md").write_text("standard\n", encoding="utf-8")

    registry = {
        "workspace": {
            "generated_repo_prompt_policy": {
                "allowed_prompt_classes": ["workflow"],
                "support_files": [".github/prompts/PROMPT_STANDARD.md"],
            },
            "userjourney_bootstrap_assets": [],
        },
        "prompt_registry": {
            "workflow_prompt_files": [
                ".github/prompts/workflow.prompt.md",
                ".github/prompts/shape-uj-ux-surfaces.prompt.md",
            ],
            "operator_prompt_files": [],
            "internal_prompt_files": [],
        },
        "prompt_authority": {
            ".github/prompts/shape-uj-ux-surfaces.prompt.md": {"authority_files": ["USERJOURNEY/USER_FLOWS.md"]}
        },
        "workflow_guidance": {
            "kickoff": {"prompts": [".github/prompts/workflow.prompt.md"]},
            "cross_cutting_workflow_prompts": [],
            "programbuild": {},
            "userjourney": {"phase_2": {"prompts": [".github/prompts/shape-uj-ux-surfaces.prompt.md"]}},
        },
    }

    dest_root = tmp_path / "dest"
    (dest_root / "config").mkdir(parents=True)
    (dest_root / "config" / "process-registry.json").write_text(
        json.dumps(
            {
                "workspace": {"bootstrap_assets": [".github/prompts/workflow.prompt.md", ".github/prompts/PROMPT_STANDARD.md"]},
                "prompt_registry": {
                    "workflow_prompt_files": [".github/prompts/workflow.prompt.md"],
                    "operator_prompt_files": [],
                    "internal_prompt_files": [],
                },
                "prompt_authority": {},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    with (
        patch.object(attach, "load_registry", return_value=registry),
        patch.object(attach, "workspace_path", side_effect=lambda relative: template_root / relative),
        patch.object(attach, "create_default_workflow_state", return_value={"phase": "phase_0"}),
    ):
        attach.attach_userjourney(dest_root, source)

    assert (dest_root / ".github" / "prompts" / "shape-uj-ux-surfaces.prompt.md").exists()
    assert not (dest_root / ".github" / "prompts" / "workflow.prompt.md").exists()
    project_registry = json.loads((dest_root / "config" / "process-registry.json").read_text(encoding="utf-8"))
    assert ".github/prompts/shape-uj-ux-surfaces.prompt.md" in project_registry["prompt_registry"]["workflow_prompt_files"]
    assert project_registry["prompt_authority"] == {
        ".github/prompts/shape-uj-ux-surfaces.prompt.md": {"authority_files": ["USERJOURNEY/USER_FLOWS.md"]}
    }


# ── main ───────────────────────────────────────────────────────────────────────


def test_main_returns_zero_on_success(tmp_path: Path) -> None:
    resolved = tmp_path / "USERJOURNEY"
    resolved.mkdir()
    ws = tmp_path / "ws"
    ws.mkdir()
    with (
        patch.object(attach, "resolve_attachment_source", return_value=resolved),
        patch.object(attach, "workspace_path", return_value=ws),
        patch.object(attach, "attach_userjourney") as mock_attach,
    ):
        result = attach.main(["userjourney", "--source", str(resolved)])
    assert result == 0
    mock_attach.assert_called_once()


def test_main_passes_dry_run_flag(tmp_path: Path) -> None:
    resolved = tmp_path / "USERJOURNEY"
    resolved.mkdir()
    ws = tmp_path / "ws"
    ws.mkdir()
    with (
        patch.object(attach, "resolve_attachment_source", return_value=resolved),
        patch.object(attach, "workspace_path", return_value=ws),
        patch.object(attach, "attach_userjourney") as mock_attach,
    ):
        result = attach.main(["userjourney", "--source", str(resolved), "--dry-run"])
    assert result == 0
    _, kwargs = mock_attach.call_args
    assert kwargs.get("dry_run") is True


def test_main_passes_force_flag(tmp_path: Path) -> None:
    resolved = tmp_path / "USERJOURNEY"
    resolved.mkdir()
    ws = tmp_path / "ws"
    ws.mkdir()
    with (
        patch.object(attach, "resolve_attachment_source", return_value=resolved),
        patch.object(attach, "workspace_path", return_value=ws),
        patch.object(attach, "attach_userjourney") as mock_attach,
    ):
        result = attach.main(["userjourney", "--source", str(resolved), "--force"])
    assert result == 0
    _, kwargs = mock_attach.call_args
    assert kwargs.get("force") is True


def test_main_programbuild_uses_dest_variant_and_project_name(tmp_path: Path) -> None:
    destination = tmp_path / "orchestra"
    destination.mkdir()
    with patch.object(attach, "attach_programbuild") as mock_attach:
        result = attach.main(
            [
                "programbuild",
                "--dest",
                str(destination),
                "--variant",
                "enterprise",
                "--project-name",
                "Orchestra Agent",
            ]
        )
    assert result == 0
    mock_attach.assert_called_once()
    args, kwargs = mock_attach.call_args
    assert args[0] == destination.resolve()
    assert kwargs["variant"] == "enterprise"
    assert kwargs["project_name"] == "Orchestra Agent"
