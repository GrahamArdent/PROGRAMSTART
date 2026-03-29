from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry
from scripts.programstart_drift_check import load_changed_files, main, system_is_optional_and_absent


def test_system_is_optional_and_absent_programbuild() -> None:
    registry = load_registry()
    assert not system_is_optional_and_absent(registry, "programbuild")


def test_system_is_optional_and_absent_userjourney_if_present() -> None:
    registry = load_registry()
    # USERJOURNEY is present in this template repo
    assert not system_is_optional_and_absent(registry, "userjourney")


def test_drift_check_passes_when_no_files_changed(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_drift_check.py"])
    monkeypatch.setattr("scripts.programstart_drift_check.git_changed_files", lambda: [])
    result = main()
    assert result == 0
    assert "No changed files" in capsys.readouterr().out


def test_drift_check_passes_with_no_violations(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_drift_check.py", "README.md"])
    result = main()
    assert result == 0
    assert "Drift check passed" in capsys.readouterr().out


def test_drift_check_with_authority_only_shows_note(capsys, monkeypatch) -> None:
    registry = load_registry()
    authority_files = registry["sync_rules"][0]["authority_files"]
    monkeypatch.setattr("sys.argv", ["programstart_drift_check.py", authority_files[0]])
    result = main()
    captured = capsys.readouterr().out
    assert result == 0
    assert "Drift check passed" in captured


def test_drift_check_allows_programbuild_changelog_without_authority(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_drift_check.py", "PROGRAMBUILD/PROGRAMBUILD_CHANGELOG.md"])
    result = main()
    captured = capsys.readouterr().out
    assert result == 0
    assert "Drift check passed" in captured


def test_drift_check_system_filter(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_drift_check.py", "--system", "programbuild", "README.md"])
    result = main()
    assert result == 0


def test_load_changed_files_from_file_list(tmp_path: Path, monkeypatch) -> None:
    file_list = tmp_path / "changed.txt"
    file_list.write_text("PROGRAMBUILD/FEASIBILITY.md\nREADME.md\n", encoding="utf-8")

    import argparse

    ns = argparse.Namespace(changed_file_list=str(file_list), files=[])
    result = load_changed_files(ns)
    assert result == ["PROGRAMBUILD/FEASIBILITY.md", "README.md"]


def test_load_changed_files_from_args(monkeypatch) -> None:
    import argparse

    ns = argparse.Namespace(changed_file_list=None, files=["PROGRAMBUILD/FEASIBILITY.md"])
    result = load_changed_files(ns)
    assert result == ["PROGRAMBUILD/FEASIBILITY.md"]


def test_drift_check_detects_sync_rule_violation(capsys, monkeypatch) -> None:
    registry = load_registry()
    # Find a sync rule that requires authority when dependents change
    rule = next(
        (r for r in registry["sync_rules"] if r.get("require_authority_when_dependents_change")),
        None,
    )
    if rule is None:
        return  # Skip if no such rule exists
    dependent = rule["dependent_files"][0]
    monkeypatch.setattr("sys.argv", ["programstart_drift_check.py", dependent])
    result = main()
    captured = capsys.readouterr().out
    assert result == 1
    assert "Drift check failed" in captured


def test_drift_check_passes_with_both_authority_and_dependent(capsys, monkeypatch) -> None:
    registry = load_registry()
    rule = next(
        (r for r in registry["sync_rules"] if r.get("require_authority_when_dependents_change")),
        None,
    )
    if rule is None:
        return
    files = [rule["authority_files"][0], rule["dependent_files"][0]]
    monkeypatch.setattr("sys.argv", ["programstart_drift_check.py", *files])
    result = main()
    captured = capsys.readouterr().out
    assert result == 0
    assert "Drift check passed" in captured


def test_drift_check_detects_future_step_violation(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_drift_check.py", "PROGRAMBUILD/ARCHITECTURE.md"])
    monkeypatch.setattr(
        "scripts.programstart_drift_check.load_registry",
        lambda: {"sync_rules": [], "systems": {"programbuild": {}, "userjourney": {"optional": True, "root": "_missing"}}},
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.system_is_optional_and_absent", lambda _registry, system: system == "userjourney"
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.load_workflow_state",
        lambda _registry, _system: {
            "stages": {
                "feasibility": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
                "architecture": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
            }
        },
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.workflow_state_config",
        lambda _registry, _system: {"step_files": {"architecture": ["PROGRAMBUILD/ARCHITECTURE.md"]}},
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.workflow_steps", lambda _registry, _system: ["feasibility", "architecture"]
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.workflow_active_step", lambda _registry, _system, _state=None: "feasibility"
    )
    result = main()
    out = capsys.readouterr().out
    assert result == 1
    assert "belongs to future step 'architecture'" in out


def test_drift_check_detects_prior_step_not_approved(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_drift_check.py", "PROGRAMBUILD/FEASIBILITY.md"])
    monkeypatch.setattr(
        "scripts.programstart_drift_check.load_registry",
        lambda: {"sync_rules": [], "systems": {"programbuild": {}, "userjourney": {"optional": True, "root": "_missing"}}},
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.system_is_optional_and_absent", lambda _registry, system: system == "userjourney"
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.load_workflow_state",
        lambda _registry, _system: {
            "stages": {
                "inputs": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
                "feasibility": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            }
        },
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.workflow_state_config",
        lambda _registry, _system: {"step_files": {"feasibility": ["PROGRAMBUILD/FEASIBILITY.md"]}},
    )
    monkeypatch.setattr("scripts.programstart_drift_check.workflow_steps", lambda _registry, _system: ["inputs", "feasibility"])
    monkeypatch.setattr(
        "scripts.programstart_drift_check.workflow_active_step", lambda _registry, _system, _state=None: "feasibility"
    )
    result = main()
    out = capsys.readouterr().out
    assert result == 1
    assert "changed before prior step 'inputs'" in out


def test_drift_check_allows_completed_prior_steps(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_drift_check.py", "PROGRAMBUILD/FEASIBILITY.md"])
    monkeypatch.setattr(
        "scripts.programstart_drift_check.load_registry",
        lambda: {"sync_rules": [], "systems": {"programbuild": {}, "userjourney": {"optional": True, "root": "_missing"}}},
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.system_is_optional_and_absent", lambda _registry, system: system == "userjourney"
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.load_workflow_state",
        lambda _registry, _system: {
            "stages": {
                "inputs": {"status": "completed", "signoff": {"decision": "approved", "date": "2026-03-27", "notes": ""}},
                "feasibility": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            }
        },
    )
    monkeypatch.setattr(
        "scripts.programstart_drift_check.workflow_state_config",
        lambda _registry, _system: {"step_files": {"feasibility": ["PROGRAMBUILD/FEASIBILITY.md"]}},
    )
    monkeypatch.setattr("scripts.programstart_drift_check.workflow_steps", lambda _registry, _system: ["inputs", "feasibility"])
    monkeypatch.setattr(
        "scripts.programstart_drift_check.workflow_active_step", lambda _registry, _system, _state=None: "feasibility"
    )
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Drift check passed" in out
