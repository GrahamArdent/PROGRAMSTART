"""Overlay provenance and mutation-tool reports remain bounded and reproducible."""

import json

import pytest

from scripts import programstart_mutation_edit_hook as hook
from scripts import programstart_mutation_loop as loop
from scripts import programstart_sync as sync
from tests.test_programstart_adopt import _registry


@pytest.mark.parametrize("payload", ["{", "[]", '{"workspace":{"name":"kept"}}', '{"workspace":null}'])
def test_overlay_handles_absent_or_malformed_project_workspace(tmp_path, payload):
    path = tmp_path / "config/process-registry.json"
    path.parent.mkdir()
    path.write_text(payload)
    manifest = {"project_name": "Fixture", "mode": "external_control_plane_link"}
    result = sync._expected_overlay_registry(_registry(), manifest, (), tmp_path)
    assert result["workspace"]["runtime_mode"] == "external_control_plane"
    if "kept" in payload:
        assert result["workspace"]["name"] == "kept"


@pytest.mark.parametrize("derived", [False, True])
def test_manifest_refresh_without_source_head_preserves_known_provenance(tmp_path, derived):
    manifest = {"source_commit": "retained", "files": ["old"], "derived_files": ["config/process-registry.json"]}
    sync._refresh_manifest(tmp_path, manifest, current_files=["new"], template_commit="", derived_registry=derived)
    result = json.loads((tmp_path / sync.MANIFEST_FILENAME).read_text())
    assert result["source_commit"] == "retained" and result["files"] == ["new"]
    assert result["derived_files"] == ["config/process-registry.json"]
    assert sync._manifest_needs_refresh(result, ["new"], "retained") is False


def test_missing_and_unrecognized_mutation_keys_do_not_become_hotspots(tmp_path, monkeypatch):
    monkeypatch.setattr(loop, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(hook, "workspace_path", lambda relative: tmp_path / relative)
    assert loop.top_survivor_hotspots() == []
    path = tmp_path / "mutants/scripts/programstart_recommend.py.meta"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"exit_code_by_key": {"foreign-key": 0}}))
    assert loop.top_survivor_hotspots() == []
    assert hook.current_hotspots() == []


def test_edit_scenario_fallback_and_non_newline_append(tmp_path):
    known = hook.SCENARIOS[0]
    chosen = hook.choose_internal_scenario(set(), ["unknown-hotspot"])
    assert chosen == known
    assert hook.choose_internal_scenario({item.name for item in hook.SCENARIOS}, ["unknown-hotspot"]) is None
    path = tmp_path / "tests.py"
    path.write_text("# original")
    hook.append_scenario(path, "# next")
    assert path.read_text().startswith("# original\n") and path.read_text().endswith("# next\n")


def test_mutation_validation_failure_stops_before_mutation(tmp_path, monkeypatch):
    monkeypatch.setattr(loop, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(loop, "active_mutation_processes", lambda: [])
    monkeypatch.setattr(loop, "run_shell_command", lambda command: 1 if "validate" in command else 0)
    with pytest.raises(SystemExit, match="validate --check all failed"):
        loop.main(["--cycles", "1", "--allow-repeat-without-edits"])
    assert not list(tmp_path.rglob("*.jsonl"))


def test_two_mutation_cycles_retain_both_results_and_wait_between(tmp_path, monkeypatch):
    monkeypatch.setattr(loop, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(loop, "active_mutation_processes", lambda: [])
    monkeypatch.setattr(
        loop,
        "run_mutation_command",
        lambda: (0, "Mutation results materialized: total=1 pending=0 killed=1 survived=0 other=0\n"),
    )
    waits = []
    monkeypatch.setattr(loop.time, "sleep", lambda seconds: waits.append(seconds))
    assert (
        loop.main(
            [
                "--cycles",
                "2",
                "--skip-gates",
                "--allow-repeat-without-edits",
                "--sleep-seconds",
                "0",
                "--status-file",
                "status.json",
                "--history-file",
                "history.jsonl",
            ]
        )
        == 0
    )
    assert waits == [0]
    records = [json.loads(line) for line in (tmp_path / "history.jsonl").read_text().splitlines()]
    assert [record["cycle"] for record in records] == [1, 2]


def test_absent_overlay_registry_and_dormant_workflow_source_are_explicit(tmp_path):
    expected = sync._expected_overlay_registry(_registry(), {"project_name": "Fixture"}, (), tmp_path)
    assert expected["workspace"]["project_name"] == "Fixture"
    relative = sync.WORKFLOW_DESTINATION_PREFIX + "missing.yml"
    assert sync._template_source_path(tmp_path, relative) == tmp_path / relative
    preserve = tmp_path / ".programstart-preserve"
    preserve.write_text("\n# comment\n")
    # Loading a file containing only commentary must not add a blank preserve path.
    result = sync._preserve_path(tmp_path)
    assert "" not in result and "# comment" not in result
