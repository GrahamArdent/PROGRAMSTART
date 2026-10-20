"""Behavior regressions for small filesystem and lifecycle tool boundaries."""

import json
import sys

import pytest

from scripts import install_hooks
from scripts import programstart_artifact_profiles as profiles
from scripts import programstart_attach as attach
from scripts import programstart_common as common
from scripts import programstart_starter_scaffold as scaffold
from scripts import programstart_sync as sync


def test_hook_uninstall_tolerates_absent_hooks_and_windows_mode(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(install_hooks, "GIT_HOOKS_DIR", tmp_path)
    assert install_hooks.uninstall_hooks(dry_run=False) == 0
    marker = tmp_path / "marker"
    marker.write_text("unchanged")
    before = marker.stat().st_mode
    monkeypatch.setattr(sys, "platform", "win32")
    install_hooks._make_executable(marker)
    assert marker.stat().st_mode == before


def test_malformed_profile_configuration_fails_conservatively(tmp_path):
    registry = {
        "systems": {
            "programbuild": {
                "artifact_profiles": {"lite": {"conditional_output_files": "not-a-list", "conditional_stage_checks": "not-a-map"}}
            }
        }
    }
    assert profiles.conditional_output_files(registry, variant="lite") == ()
    assert profiles.stage_check_required(registry, "risk-spikes", state={"variant": "lite"}) is True
    assert profiles.artifact_has_body(tmp_path / "missing") is False
    path = tmp_path / "binary.md"
    path.write_bytes(b"\xff\xfe")
    assert profiles.artifact_has_body(path) is False


def test_binary_attachment_is_copied_without_decoding(tmp_path):
    source, target = tmp_path / "binary", tmp_path / "nested/target"
    source.write_bytes(b"\x00\xff\xfe")
    attach._copy_text_or_binary(source, target)
    assert target.read_bytes() == source.read_bytes()


def test_non_git_template_head_is_unknown_not_fabricated(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert attach._git_head_hash() == ""
    assert sync._template_head_hash(tmp_path) == ""


def test_missing_userjourney_assets_are_not_created(tmp_path, monkeypatch):
    registry = {
        "workspace": {"userjourney_bootstrap_assets": ["missing.md"]},
        "prompt_registry": {"workflow_prompt_files": [".github/prompts/userjourney-missing.prompt.md"]},
    }
    target = tmp_path / "target"
    target.mkdir()
    monkeypatch.setattr(attach, "workspace_path", lambda relative: tmp_path / "source" / relative)
    attach._copy_userjourney_bootstrap_assets(target, registry)
    attach._copy_userjourney_prompt_assets(target, registry)
    assert list(target.iterdir()) == []


def test_sync_manifest_rejects_non_object_and_detects_missing_registry(tmp_path):
    manifest = tmp_path / ".programstart-manifest.json"
    manifest.write_text("[]")
    with pytest.raises(ValueError, match="JSON object"):
        sync._load_manifest(tmp_path)
    assert sync._registry_needs_refresh(tmp_path, {}) is True
    (tmp_path / "config").mkdir()
    (tmp_path / "config/process-registry.json").write_text("{")
    assert sync._registry_needs_refresh(tmp_path, {}) is True
    assert sync._manifest_needs_refresh({"files": []}, ["new.md"], "") is True


def test_save_state_without_lock_still_writes_complete_json(tmp_path, monkeypatch):
    monkeypatch.setattr(common, "ROOT", tmp_path)
    registry = {"workflow_state": {"programbuild": {"state_file": "state.json"}}}
    common.save_workflow_state(registry, "programbuild", {"active": "research"}, acquire_lock=False)
    assert json.loads((tmp_path / "state.json").read_text()) == {"active": "research"}


def test_integrity_inventory_applies_all_exclusions_and_ignores_non_files(tmp_path, monkeypatch):
    monkeypatch.setattr(common, "ROOT", tmp_path)
    for name in ["README.md", "assets/keep.md", "assets/exclude.md", "private/secret.md", "skip.txt"]:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture")
    (tmp_path / "assets/empty").mkdir()
    registry = {
        "workspace": {"root_readme": "README.md", "bootstrap_assets": ["", "assets", "private", "skip.txt", "missing"]},
        "systems": {},
        "integrity": {
            "manifest_collection": {
                "exclude_prefixes": ["private"],
                "exclude_names": ["skip.txt"],
                "exclude_globs": ["**/exclude.md"],
            },
            "baselines": [{"root": "", "manifest": ""}],
        },
    }
    assert common.collect_registry_integrity_files(registry) == [tmp_path / "README.md", tmp_path / "assets/keep.md"]


def test_scaffold_env_covers_selected_service_credentials():
    from tests.test_programstart_starter_scaffold import _make_recommendation

    recommendation = _make_recommendation("web app", api_names=["Resend", "PostHog", "Sentry"])
    # Use the public recommendation shape accepted by the scaffold's API selector.
    result = scaffold.api_env_example("example", recommendation, ".")
    assert result is not None
    _, text = result
    for name in ["RESEND_API_KEY", "POSTHOG", "SENTRY"]:
        assert name in text


@pytest.mark.parametrize(
    "collection", [{"include_workspace_readme": False, "include_bootstrap_assets": False, "include_baseline_roots": False}, {}]
)
def test_empty_integrity_configuration_has_no_invented_files(tmp_path, monkeypatch, collection):
    monkeypatch.setattr(common, "ROOT", tmp_path)
    assert (
        common.collect_registry_integrity_files(
            {"workspace": {}, "systems": {}, "integrity": {"manifest_collection": collection}}
        )
        == []
    )
    common._ensure_scripts_importable()


def test_porcelain_transport_blank_records_are_ignored(monkeypatch):
    from types import SimpleNamespace

    from scripts import programstart_repo_clean_check as clean

    monkeypatch.setattr(clean.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout="\n?? good.txt\n \n"))
    assert clean.capture_git_status() == {"good.txt"}


def test_explicit_prompt_registry_can_have_no_stages():
    from scripts.programstart_prompt_build import list_stages

    assert list_stages({}) == []


def test_cleanup_ignores_dangling_glob_link(tmp_path, monkeypatch):
    from scripts import programstart_clean as clean

    monkeypatch.setattr(clean, "ROOT", tmp_path)
    (tmp_path / "dangling.egg-info").symlink_to(tmp_path / "missing")
    assert clean.collect_cleanup_targets(False, False) == []


def test_backup_skips_absent_optional_system(tmp_path, monkeypatch):
    from scripts import programstart_backup as backup

    monkeypatch.setattr(common, "ROOT", tmp_path)
    registry = {"systems": {"userjourney": {"optional": True, "root": "missing"}}, "workflow_state": {}}
    assert backup.tracked_state_files(registry) == []
