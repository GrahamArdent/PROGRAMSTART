"""Real temporary overlays and bounded filesystem/process failure paths."""

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import programstart_adopt as adopt
from scripts import programstart_bootstrap as bootstrap


def test_binary_stub_falls_back_to_lossless_copy(tmp_path):
    source, destination = tmp_path / "binary", tmp_path / "target"
    source.write_bytes(b"\xff\xfe")
    assert bootstrap._extract_file_header(source) == ""
    bootstrap.copy_output_stub(source, destination, False)
    assert destination.read_bytes() == source.read_bytes()


def test_prompt_policy_includes_only_explicitly_allowed_classes():
    registry = {
        "workspace": {"generated_repo_prompt_policy": {"allowed_prompt_classes": ["operator", "internal"]}},
        "prompt_registry": {
            "workflow_prompt_files": ["workflow"],
            "operator_prompt_files": ["operator"],
            "internal_prompt_files": ["internal"],
        },
    }
    assert bootstrap.generated_repo_prompt_assets(registry) == {"operator", "internal"}
    assert bootstrap.generated_repo_prompt_authority(registry) == {}


def test_initialize_requires_git_and_dry_run_writes_nothing(tmp_path, monkeypatch):
    with monkeypatch.context() as patch:
        patch.setattr(bootstrap.shutil, "which", lambda _: None)
        with pytest.raises(RuntimeError, match="git is required"):
            bootstrap.initialize_git_repository(tmp_path, False)
    bootstrap.initialize_git_repository(tmp_path, True)
    assert not (tmp_path / ".git").exists()


def test_git_initialization_falls_back_for_older_git(tmp_path, monkeypatch):
    run = subprocess.run
    calls = []

    def legacy(argv, **kwargs):
        calls.append(argv)
        if "-b" in argv:
            raise subprocess.CalledProcessError(129, argv)
        return run(argv, **kwargs)

    monkeypatch.setattr(bootstrap.subprocess, "run", legacy)
    bootstrap.initialize_git_repository(tmp_path, False)
    assert (tmp_path / ".git").is_dir() and len(calls) == 2


def test_secret_scan_failure_does_not_destroy_baseline(tmp_path, monkeypatch):
    path = tmp_path / ".secrets.baseline"
    path.write_text("original")

    def unavailable(*args, **kwargs):
        raise OSError("scanner unavailable")

    monkeypatch.setattr(bootstrap.subprocess, "run", unavailable)
    bootstrap.refresh_secrets_baseline(tmp_path, False)
    assert path.read_text() == "original"


def test_instruction_create_race_preserves_competing_owner_file(tmp_path, monkeypatch):
    original = Path.open
    destination = tmp_path / "AGENTS.md"

    def concurrent(path, mode="r", *args, **kwargs):
        if path == destination and mode == "x":
            with original(path, "w") as handle:
                handle.write("owner instructions")
        return original(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", concurrent)
    bootstrap.write_project_agent_entry(tmp_path, project_name="Fixture", variant="lite", external_runtime=True, dry_run=False)
    assert destination.read_text() == "owner instructions"


def test_unavailable_source_identity_and_missing_metadata_remain_explicit(tmp_path, monkeypatch):
    monkeypatch.setattr(bootstrap.subprocess, "run", lambda *_a, **_k: SimpleNamespace(stdout="invalid"))
    bootstrap.write_project_agent_entry(tmp_path, project_name="Fixture", variant="lite", external_runtime=True, dry_run=False)
    assert "UNKNOWN (resolve" in (tmp_path / "AGENTS.md").read_text()
    monkeypatch.setattr(bootstrap, "load_registry", lambda: {"systems": {"programbuild": {"metadata_required": ["missing.md"]}}})
    bootstrap.stamp_owner_and_dates(tmp_path, owner="owner", last_updated="2026-10-20")
    assert not (tmp_path / "missing.md").exists()


@pytest.mark.parametrize("relative", ["PROGRAMBUILD", "config/process-registry.json", ".programstart-manifest.json"])
def test_adoption_rejects_already_owned_management_surfaces(tmp_path, relative):
    path = tmp_path / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if relative == "PROGRAMBUILD":
        path.mkdir()
    else:
        path.write_text("owner data")
    with pytest.raises(FileExistsError):
        adopt._assert_safe_destination(tmp_path, ())


def test_adoption_rejects_non_file_prompt_and_missing_repo(tmp_path, monkeypatch):
    path = tmp_path / "prompt.md"
    path.mkdir()
    monkeypatch.setattr(adopt, "workspace_path", lambda relative: tmp_path / "missing-source" / relative)
    assert adopt._git_head_hash() == ""
    with pytest.raises(FileExistsError, match="overwrite"):
        adopt._assert_safe_destination(tmp_path, ("prompt.md",))
    with pytest.raises(FileNotFoundError, match="does not exist"):
        adopt.adopt_programbuild(tmp_path / "absent", project_name="Fixture")


def test_actual_adoption_cli_preserves_host_readme(tmp_path):
    (tmp_path / "README.md").write_text("host readme")
    assert adopt.main(["--dest", str(tmp_path), "--variant", "lite"]) == 0
    assert (tmp_path / "README.md").read_text() == "host readme"
    manifest = json.loads((tmp_path / adopt.MANIFEST_FILENAME).read_text())
    assert manifest["variant"] == "lite"
    assert (tmp_path / "PROGRAMBUILD/PROGRAMBUILD.md").is_file()


@pytest.mark.parametrize("dry_run", [False, True])
def test_adoption_preserves_identical_existing_managed_prompt(tmp_path, dry_run, capsys):
    registry = adopt.load_registry()
    relative = adopt._managed_prompt_assets(registry)[0]
    target = tmp_path / relative
    target.parent.mkdir(parents=True)
    target.write_bytes(adopt.workspace_path(relative).read_bytes())
    before = target.read_bytes()
    assert adopt.main(["--dest", str(tmp_path), *(["--dry-run"] if dry_run else [])]) == 0
    assert target.read_bytes() == before
    if dry_run:
        assert "PRESERVE" in capsys.readouterr().out
        assert not (tmp_path / "PROGRAMBUILD").exists()


def test_unseparated_output_header_is_preserved_and_empty_header_stays_empty(tmp_path):
    path = tmp_path / "output.md"
    path.write_text("Purpose: fixture\nOwner: operator\n")
    assert bootstrap._extract_file_header(path) == path.read_text()
    path.write_text("")
    assert bootstrap._extract_file_header(path) == ""


def test_clean_source_identity_is_not_marked_dirty(tmp_path, monkeypatch):
    source = tmp_path / "source"
    source.mkdir()
    bootstrap.initialize_git_repository(source, False)
    subprocess.run(
        [
            "git",
            "-C",
            str(source),
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "--allow-empty",
            "-qm",
            "fixture",
        ],
        check=True,
    )
    head = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    monkeypatch.setattr(bootstrap, "workspace_path", lambda _: source)
    bootstrap.write_project_agent_entry(tmp_path, project_name="Fixture", variant="lite", external_runtime=True, dry_run=False)
    content = (tmp_path / "AGENTS.md").read_text()
    assert head in content and "uncommitted changes:" not in content


def test_explicit_operator_prompt_policy_survives_bootstrap_and_adoption(tmp_path):
    registry = adopt.load_registry()
    registry["workspace"]["generated_repo_prompt_policy"]["allowed_prompt_classes"] = ["workflow", "operator"]
    assert registry["prompt_registry"]["operator_prompt_files"]
    result = adopt._adopted_registry(registry, project_name="Fixture", prompt_assets=())
    assert result["workflow_guidance"]["operator"] == registry["workflow_guidance"]["operator"]
    path = tmp_path / "config/process-registry.json"
    path.parent.mkdir()
    path.write_text(json.dumps(registry))
    bootstrap.stamp_bootstrapped_registry(tmp_path, project_name="Fixture", dry_run=False)
    assert json.loads(path.read_text())["workflow_guidance"]["operator"] == registry["workflow_guidance"]["operator"]
