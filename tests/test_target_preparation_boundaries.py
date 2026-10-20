"""External target preparation preserves existing project data and stays bounded."""

import json

import pytest

from scripts import programstart_target as target


def test_prepare_rejects_missing_repo_and_methodology(tmp_path):
    with pytest.raises(FileNotFoundError, match="does not exist"):
        target.prepare_target_control_plane(tmp_path / "absent")
    with pytest.raises(FileNotFoundError, match="no PROGRAMBUILD"):
        target.prepare_target_control_plane(tmp_path)
    with pytest.raises(FileNotFoundError, match="does not exist"):
        target.run_target_command(tmp_path / "absent", ["status"])
    with pytest.raises(FileNotFoundError, match="no control registry"):
        target.run_target_command(tmp_path, ["status"])


def test_prepare_preserves_existing_control_or_rejects_inconsistent_link(tmp_path):
    (tmp_path / "PROGRAMBUILD").mkdir()
    manifest = tmp_path / target.MANIFEST_FILENAME
    manifest.write_text("{}")
    with pytest.raises(FileExistsError, match="inconsistent link"):
        target.prepare_target_control_plane(tmp_path)
    registry = tmp_path / "config/process-registry.json"
    registry.parent.mkdir()
    registry.write_text('{"project":"unchanged"}')
    target.prepare_target_control_plane(tmp_path)
    assert registry.read_text() == '{"project":"unchanged"}'


def test_prepare_dry_run_creates_nothing_and_variant_fallback_is_bounded(tmp_path, capsys):
    target.prepare_target_control_plane(tmp_path / "not-created", dry_run=True)
    assert not (tmp_path / "not-created").exists()
    assert "CREATE" in capsys.readouterr().out
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD/PROGRAMBUILD_STATE.json").write_text("{")
    assert target._read_variant(tmp_path) == "product"


@pytest.mark.parametrize("dry_run", [False, True])
def test_identical_prompt_is_preserved(tmp_path, monkeypatch, dry_run):
    template, project = tmp_path / "template", tmp_path / "project"
    for root in [template, project]:
        (root / "prompts").mkdir(parents=True)
        (root / "prompts/stage.md").write_text("identical")
    monkeypatch.setattr(target, "workspace_path", lambda relative: template / relative)
    target._copy_managed_prompts(project, ("prompts/stage.md",), dry_run=dry_run)
    assert (project / "prompts/stage.md").read_text() == "identical"
    (project / "prompts/stage.md").unlink()
    (project / "prompts/stage.md").mkdir()
    with pytest.raises(FileExistsError, match="overwrite"):
        target._copy_managed_prompts(project, ("prompts/stage.md",), dry_run=dry_run)


@pytest.mark.parametrize("arguments", [[], ["validate", "--check"]])
def test_incomplete_target_commands_fail_before_execution(arguments):
    with pytest.raises(ValueError, match="Provide|requires a check name"):
        target._validate_target_command(arguments)


def test_cli_prepare_and_invalid_option_combinations(tmp_path, capsys):
    assert target.main(["--repo", str(tmp_path / "dry"), "--prepare", "--dry-run"]) == 0
    assert not (tmp_path / "dry").exists()
    with pytest.raises(SystemExit) as exc:
        target.main(["--repo", str(tmp_path), "--project-name", "invalid"])
    assert exc.value.code == 2
    with pytest.raises(SystemExit) as exc:
        target.main(["--repo", str(tmp_path)])
    assert exc.value.code == 2
    assert target.main(["--repo", str(tmp_path), "status"]) == 1
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "config").mkdir()
    (tmp_path / "config/process-registry.json").write_text(json.dumps({"preserved": True}))
    assert target.main(["--repo", str(tmp_path), "--prepare"]) == 0
