"""Temporary state files exercise refusal and advisory paths without owner mutation."""

import json
import sys

import pytest

from scripts import programstart_common as common
from scripts import programstart_workflow_state as state


@pytest.fixture
def local_state(tmp_path, monkeypatch):
    registry = common.load_registry()
    monkeypatch.setattr(common, "ROOT", tmp_path)
    monkeypatch.setattr(state, "load_registry", lambda: registry)
    return tmp_path, registry


def invoke(monkeypatch, *arguments):
    monkeypatch.setattr(sys, "argv", ["state", *arguments])
    return state.main()


def test_rollback_refuses_absent_and_empty_snapshots(local_state, monkeypatch, capsys):
    root, _ = local_state
    assert invoke(monkeypatch, "rollback", "--confirm") == 1
    assert "No snapshots" in capsys.readouterr().out
    empty = root / "empty.json"
    empty.write_text(json.dumps({"systems": {}}))
    assert invoke(monkeypatch, "rollback", "--confirm", "--to", str(empty)) == 1
    assert "no system state" in capsys.readouterr().out


def test_rollback_ignores_foreign_system_names(local_state, monkeypatch):
    root, _ = local_state
    foreign = root / "foreign.json"
    foreign.write_text(json.dumps({"systems": {"foreign": {"active": "do-not-import"}}}))
    assert invoke(monkeypatch, "rollback", "--confirm", "--to", str(foreign)) == 0
    assert not (root / "PROGRAMBUILD/PROGRAMBUILD_STATE.json").exists()


def test_blocked_gate_and_content_advisories_do_not_mutate_state(local_state, monkeypatch, capsys):
    root, registry = local_state
    current = common.create_default_workflow_state(registry, "programbuild")
    current["active_stage"] = "research"
    for step, entry in current["stages"].items():
        entry["status"] = "in_progress" if step == "research" else "planned"
    common.save_workflow_state(registry, "programbuild", current)
    path = common.workflow_state_path(registry, "programbuild")
    original = path.read_bytes()
    assert invoke(monkeypatch, "advance", "--system", "programbuild", "--dry-run", "--gate-result", "blocked") == 1
    assert "Structured Challenge Gate" in capsys.readouterr().out
    (root / "PROGRAMBUILD/RESEARCH_SUMMARY.md").write_text("TODO: unresolved fixture\n")
    assert invoke(monkeypatch, "advance", "--system", "programbuild", "--dry-run", "--gate-result", "clear") == 0
    assert "Content quality warnings" in capsys.readouterr().out
    assert path.read_bytes() == original


def test_git_process_unavailable_is_unknown(monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("git unavailable")

    monkeypatch.setattr(state.subprocess, "run", fail)
    assert state._git_head_hash() is None


def test_blocking_native_gate_log_is_retained(local_state):
    root, _ = local_state
    path = root / "PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "## Challenge Gate Log\n\n| From Stage | To Stage | Date | Proceed? | Notes |\n|---|---|---|---|---|\n"
        "| research | requirements_and_ux | 2026-10-20 | No | unresolved |\n"
    )
    result = state._check_challenge_gate_log("research")
    assert result is not None and "blocking" in result


def test_missing_state_is_absent_from_live_snapshot(local_state, monkeypatch, capsys):
    root, registry = local_state
    assert state._load_live_state_bundle(registry) == {"systems": {}}
    snapshot = root / "old.json"
    snapshot.write_text('{"systems": {"programbuild": {"active_stage": "research"}}}')
    assert invoke(monkeypatch, "diff", "--old", str(snapshot)) == 0
    assert "programbuild" in capsys.readouterr().out
    monkeypatch.chdir(root)
    assert state._git_head_hash() is None


def test_custom_stage_and_architecture_list_both_execute_real_preflight():
    registry = common.load_registry()
    unknown = state.preflight_problems(registry, "programbuild", active_step="owner_custom_stage")
    architecture = state.preflight_problems(registry, "programbuild", active_step="architecture_and_risk_spikes")
    assert isinstance(unknown, list) and isinstance(architecture, list)


def test_completed_status_does_not_invent_commit_when_git_is_unavailable(local_state, monkeypatch):
    root, registry = local_state
    current = common.create_default_workflow_state(registry, "userjourney")
    common.save_workflow_state(registry, "userjourney", current)
    (root / "USERJOURNEY").mkdir(exist_ok=True)

    def unavailable(*args, **kwargs):
        raise OSError("git unavailable")

    monkeypatch.setattr(state.subprocess, "run", unavailable)
    step = common.workflow_steps(registry, "userjourney")[0]
    assert invoke(monkeypatch, "set", "--system", "userjourney", "--step", step, "--status", "completed") == 0
    result = common.load_workflow_state(registry, "userjourney")
    assert not result["phases"][step]["signoff"].get("commit_hash")


def test_preflight_rejects_sync_drift_from_an_explicit_git_worktree(tmp_path, monkeypatch):
    import subprocess

    registry = common.load_registry()
    registry["sync_rules"] = [
        {
            "name": "fixture_authority_pair",
            "system": "programbuild",
            "authority_files": ["authority.md"],
            "dependent_files": ["dependent.md"],
            "require_dependents_when_authority_changes": True,
        }
    ]
    subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True)
    (tmp_path / "authority.md").write_text("Changed authority requires its dependent update.\n")

    def changed_fixture_files():
        with monkeypatch.context() as scoped:
            scoped.setattr(common, "ROOT", tmp_path)
            changed = common.git_changed_files()
        assert changed == ["authority.md"]
        return changed

    monkeypatch.setattr(state.programstart_drift_check, "git_changed_files", changed_fixture_files)
    problems = state.preflight_problems(registry, "programbuild", active_step="owner_custom_stage")
    assert any("fixture_authority_pair: authority files changed without dependent files" in problem for problem in problems)
