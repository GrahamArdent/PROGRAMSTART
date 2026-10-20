"""Health observations preserve unknown/read failures and signoff drift."""

import json

from scripts import programstart_health_probe as probe


def test_metadata_directory_and_unowned_changed_file_are_bounded(tmp_path):
    (tmp_path / "directory.md").mkdir()
    registry = {
        "systems": {"programbuild": {"metadata_required": ["directory.md"]}},
        "workflow_state": {"programbuild": {"active_key": "active", "step_order": ["research"], "step_files": {}}},
    }
    assert probe._check_metadata(tmp_path, registry, "programbuild") == ["Cannot read directory.md"]
    assert probe._check_step_order(tmp_path, registry, "programbuild", {"active": "research"}, ["foreign.txt"]) == []


def test_all_authorities_are_required_for_all_match_rule(tmp_path):
    registry = {
        "sync_rules": [
            {
                "name": "all-owner",
                "system": "programbuild",
                "authority_files": ["a.md", "b.md"],
                "dependent_files": ["c.md"],
                "authority_match": "all",
                "require_authority_when_dependents_change": True,
            }
        ]
    }
    errors, notes = probe._check_authority_sync(tmp_path, registry, ["a.md", "c.md"])
    assert len(errors) == 1 and "b.md" in errors[0] and notes == []


def test_invalid_signoff_date_remains_unknown_and_nonobjects_are_ignored():
    state = {
        "stages": {
            "bad": None,
            "done": {"status": "completed", "signoff": {"date": "not-a-date", "decision": "approved", "commit_hash": "a" * 40}},
        }
    }
    info = probe._signoff_info(state, "programbuild")
    assert info[3] is None and info[4] == ["done"]


def test_no_active_systems_is_structural_failure(tmp_path):
    (tmp_path / "config").mkdir()
    (tmp_path / "config/process-registry.json").write_text(json.dumps({"version": "fixture", "systems": {}}))
    result = probe.probe_target(tmp_path)
    assert result.structural_problems == ["No active systems found in registry"]
    assert result.overall_health != "healthy"


def test_summary_reports_changed_signoff_and_last_date(capsys):
    system = probe.SystemHealthReport(
        system="programbuild",
        present=True,
        last_signoff_commit_hash="a" * 40,
        last_signoff_date="2026-10-20",
        files_changed_since_signoff=2,
    )
    report = probe.HealthProbeReport(systems=[system])
    health, summary = probe._classify_health(report)
    assert health == "warnings" and "changed_since_signoff=2" in summary
    probe.print_multi_summary([report])
    assert "2026-10-20" in capsys.readouterr().out


def test_signoff_with_commit_runs_real_git_drift_probe(tmp_path):
    registry = {
        "systems": {"programbuild": {"control_files": [], "output_files": [], "metadata_required": []}},
        "workflow_state": {"programbuild": {"file": "state.json", "active_key": "active_stage", "step_order": ["research"]}},
        "sync_rules": [],
    }
    (tmp_path / "state.json").write_text(
        json.dumps(
            {
                "active_stage": "research",
                "stages": {"research": {"status": "in_progress", "signoff": {"date": "2026-10-20", "commit_hash": "a" * 40}}},
            }
        )
    )
    report = probe.probe_system(tmp_path, registry, "programbuild", [])
    assert report and report.last_signoff_commit_hash == "a" * 40
    assert report.files_changed_since_signoff is None


def test_health_ignores_blank_git_records_and_unknown_signoff_shape(tmp_path, monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setattr(probe.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0, stdout="\nnew.md\nnew.md\n"))
    assert probe._git_changed_files(tmp_path) == ["new.md"]
    assert probe._signoff_info({"stages": {"research": {"signoff": None}}}, "programbuild")[0] == ""
    (tmp_path / "config").mkdir()
    (tmp_path / "config/process-registry.json").write_text('{"systems":{"unused":{}}}')
    assert probe.probe_target(tmp_path).systems == []
