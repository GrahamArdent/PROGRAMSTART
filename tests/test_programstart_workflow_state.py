from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry
from scripts.programstart_workflow_state import main, print_state, system_is_optional_and_absent


def test_system_is_optional_and_absent(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_workflow_state.workspace_path", lambda _relative: ROOT / "_missing_optional")
    assert system_is_optional_and_absent(registry, "userjourney")


def test_print_state_outputs_programbuild(capsys, monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    state = {
        "variant": "product",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    print_state("programbuild", state, "inputs_and_mode_selection")
    out = capsys.readouterr().out
    assert "PROGRAMBUILD" in out
    assert "active stage" in out


def test_main_init_creates_missing_state(tmp_path: Path, capsys, monkeypatch) -> None:
    registry = load_registry()
    state_path = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json"

    def fake_save(_registry, _system, state) -> None:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state), encoding="utf-8")

    monkeypatch.setattr("scripts.programstart_workflow_state.load_registry", lambda: registry)
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_state_path", lambda _registry, _system: state_path)
    monkeypatch.setattr("scripts.programstart_workflow_state.save_workflow_state", fake_save)
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "init", "--system", "programbuild"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Initialized" in out


def test_main_init_reports_existing_state(tmp_path: Path, capsys, monkeypatch) -> None:
    registry = load_registry()
    state_path = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr("scripts.programstart_workflow_state.load_registry", lambda: registry)
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_state_path", lambda _registry, _system: state_path)
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "init", "--system", "programbuild"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Exists:" in out


def test_main_init_skips_optional_unattached(capsys, monkeypatch) -> None:
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.system_is_optional_and_absent", lambda _registry, system: system == "userjourney"
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "init"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Skipped optional unattached system: userjourney" in out


def test_main_show_all(capsys, monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "show"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "PROGRAMBUILD" in out


def test_main_show_detached_first_system_adds_separator(capsys, monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.system_is_optional_and_absent", lambda _registry, system: system == "programbuild"
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "show"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "\n\n" in out


def test_main_advance_dry_run(capsys, monkeypatch) -> None:
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "programbuild", "--dry-run"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Would advance programbuild" in out


def test_main_advance_writes_next_step(capsys, monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _registry, _system: [])
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state", lambda _registry, _system, value: saved.update(value)
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "programbuild"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Advanced programbuild" in out
    assert saved["active_stage"] == "feasibility"


def test_main_advance_keeps_existing_next_step_status(capsys, monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "blocked", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _registry, _system: [])
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state", lambda _registry, _system, value: saved.update(value)
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "programbuild"])
    result = main()
    assert result == 0
    assert saved["stages"]["feasibility"]["status"] == "blocked"


def test_main_advance_rejects_non_in_progress(monkeypatch) -> None:
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps", lambda _registry, _system: ["inputs_and_mode_selection"]
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "programbuild"])
    with pytest.raises(SystemExit):
        main()


def test_main_set_updates_status_and_variant(capsys, monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_stage": "inputs_and_mode_selection",
        "variant": "product",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps", lambda _registry, _system: ["inputs_and_mode_selection"]
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_entry_key", lambda _system: "stages")
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state", lambda _registry, _system, value: saved.update(value)
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "programstart_workflow_state.py",
            "set",
            "--system",
            "programbuild",
            "--step",
            "inputs_and_mode_selection",
            "--status",
            "completed",
            "--variant",
            "enterprise",
        ],
    )
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Updated programbuild inputs_and_mode_selection to completed" in out
    assert saved["variant"] == "enterprise"
    assert saved["stages"]["inputs_and_mode_selection"]["signoff"]["decision"] == "approved"


def test_main_set_rejects_unknown_step(monkeypatch) -> None:
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps", lambda _registry, _system: ["inputs_and_mode_selection"]
    )
    monkeypatch.setattr(
        "sys.argv",
        ["programstart_workflow_state.py", "set", "--system", "programbuild", "--step", "unknown", "--status", "planned"],
    )
    with pytest.raises(SystemExit):
        main()
