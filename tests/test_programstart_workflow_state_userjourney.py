"""USERJOURNEY-specific workflow state tests.

These tests are only copied to project repos when USERJOURNEY is attached.
They require the USERJOURNEY directory to exist.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from conftest import requires_userjourney

from scripts.programstart_workflow_state import main, print_state

pytestmark = requires_userjourney


def test_print_state_outputs_userjourney(capsys, monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    state = {
        "phases": {
            "phase_0": {"status": "completed", "signoff": {"decision": "approved", "date": "2026-03-27", "notes": ""}},
            "phase_1": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    print_state("userjourney", state, "phase_1")
    out = capsys.readouterr().out
    assert "active phase" in out


def test_main_show_optional_detached(capsys, monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.system_is_optional_and_absent", lambda _registry, system: system == "userjourney"
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "show", "--system", "userjourney"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "not attached" in out


def test_main_advance_final_step(capsys, monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_phase": "phase_9",
        "phases": {
            "phase_9": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step", lambda _registry, _system, _state=None: "phase_9"
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_steps", lambda _registry, _system: ["phase_9"])
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _registry, _system: [])
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state", lambda _registry, _system, value: saved.update(value)
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "userjourney"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Completed final userjourney step phase_9" in out


def test_main_advance_dry_run_final_step(capsys, monkeypatch) -> None:
    state = {
        "active_phase": "phase_9",
        "phases": {
            "phase_9": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step", lambda _registry, _system, _state=None: "phase_9"
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_steps", lambda _registry, _system: ["phase_9"])
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "userjourney", "--dry-run"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "would mark workflow complete" in out.lower()


def test_main_advance_rejects_optional_unattached(monkeypatch) -> None:
    monkeypatch.setattr("scripts.programstart_workflow_state.system_is_optional_and_absent", lambda _registry, _system: True)
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "userjourney"])
    with pytest.raises(SystemExit):
        main()


def test_main_set_updates_userjourney_signoff_and_active_phase(capsys, monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_phase": "phase_0",
        "phases": {
            "phase_0": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_steps", lambda _registry, _system: ["phase_0"])
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_entry_key", lambda _system: "phases")
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state", lambda _registry, _system, value: saved.update(value)
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "programstart_workflow_state.py",
            "set",
            "--system",
            "userjourney",
            "--step",
            "phase_0",
            "--status",
            "in_progress",
            "--decision",
            "go",
            "--date",
            "2026-03-27",
            "--notes",
            "ok",
        ],
    )
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Updated userjourney phase_0 to in_progress" in out
    assert saved["active_phase"] == "phase_0"
    assert saved["phases"]["phase_0"]["signoff"]["decision"] == "go"
    assert saved["phases"]["phase_0"]["signoff"]["date"] == "2026-03-27"
    assert saved["phases"]["phase_0"]["signoff"]["notes"] == "ok"


def test_main_set_planned_without_signoff_keeps_signoff_untouched(monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_phase": "phase_0",
        "phases": {
            "phase_0": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_steps", lambda _registry, _system: ["phase_0"])
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_entry_key", lambda _system: "phases")
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state", lambda _registry, _system, value: saved.update(value)
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "programstart_workflow_state.py",
            "set",
            "--system",
            "userjourney",
            "--step",
            "phase_0",
            "--status",
            "planned",
        ],
    )
    result = main()
    assert result == 0
    assert saved["phases"]["phase_0"]["signoff"] == {"decision": "", "date": "", "notes": ""}


def test_main_set_rejects_optional_unattached(monkeypatch) -> None:
    monkeypatch.setattr("scripts.programstart_workflow_state.system_is_optional_and_absent", lambda _registry, _system: True)
    monkeypatch.setattr(
        "sys.argv",
        ["programstart_workflow_state.py", "set", "--system", "userjourney", "--step", "phase_0", "--status", "planned"],
    )
    with pytest.raises(SystemExit):
        main()
