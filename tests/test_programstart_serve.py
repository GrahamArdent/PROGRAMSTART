from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_serve
from scripts.programstart_serve import (
    ALLOWED_COMMANDS,
    advance_workflow_with_signoff,
    run_command,
    save_workflow_signoff,
    strip_ansi,
    update_implementation_tracker_phase,
    update_implementation_tracker_slice,
)


def test_allowed_commands_contains_core_entries() -> None:
    assert "state.show" in ALLOWED_COMMANDS
    assert "validate" in ALLOWED_COMMANDS
    assert "status" in ALLOWED_COMMANDS
    assert "guide.programbuild" in ALLOWED_COMMANDS
    assert "guide.kickoff" in ALLOWED_COMMANDS
    assert "log" in ALLOWED_COMMANDS
    assert "drift" in ALLOWED_COMMANDS
    assert "progress" in ALLOWED_COMMANDS
    assert ALLOWED_COMMANDS["status"][:3] == [sys.executable, "-m", "scripts.programstart_cli"]


def test_run_command_unknown_returns_error() -> None:
    result = run_command("nonexistent.command")
    assert result["exit_code"] == 1
    assert "unknown command" in result["output"]


def test_run_command_rejects_disallowed_extra_args() -> None:
    result = run_command("status", ["--evil-arg"])
    assert result["exit_code"] == 1
    assert "not permitted" in result["output"]


def test_run_command_status_succeeds() -> None:
    result = run_command("status")
    assert result["exit_code"] == 0
    assert "PROGRAMBUILD" in result["output"]


def test_run_command_validate_succeeds() -> None:
    result = run_command("validate")
    assert result["exit_code"] == 0


def test_strip_ansi_removes_escape_codes() -> None:
    assert strip_ansi("\033[32mgreen\033[0m") == "green"
    assert strip_ansi("plain text") == "plain text"
    assert strip_ansi("\033[1;31mbold red\033[0m") == "bold red"


def test_allowed_commands_all_have_list_values() -> None:
    for key, value in ALLOWED_COMMANDS.items():
        assert isinstance(value, list), f"{key} should be a list"
        assert len(value) >= 1, f"{key} should have at least one element"


def test_update_implementation_tracker_phase_updates_status_and_sanitizes_blockers(tmp_path: Path, monkeypatch) -> None:
    tracker = tmp_path / "USERJOURNEY" / "IMPLEMENTATION_TRACKER.md"
    tracker.parent.mkdir(parents=True)
    tracker.write_text(
        "# Implementation Tracker\n"
        "Last updated: 2026-03-27\n\n"
        "| Phase | Status | Exit Gate | Target Route | Current blockers | Notes |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| 2 | Planned | Gate | /activate | none | note |\n\n"
        "| Slice | Status | Window | Notes |\n"
        "| --- | --- | --- | --- |\n"
        "| Slice 3 | Pending | Soon | initial |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(programstart_serve, "ROOT", tmp_path)

    result = update_implementation_tracker_phase("2", "Blocked", "Need | review\nnow")

    updated = tracker.read_text(encoding="utf-8")
    assert result["exit_code"] == 0
    assert "| 2 | Blocked | Gate | /activate | Need ¦ review now | note |" in updated
    assert "Last updated:" in updated


def test_update_implementation_tracker_slice_updates_notes_and_status(tmp_path: Path, monkeypatch) -> None:
    tracker = tmp_path / "USERJOURNEY" / "IMPLEMENTATION_TRACKER.md"
    tracker.parent.mkdir(parents=True)
    tracker.write_text(
        "# Implementation Tracker\n"
        "Last updated: 2026-03-27\n\n"
        "| Phase | Status | Exit Gate | Target Route | Current blockers | Notes |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| 2 | Planned | Gate | /activate | none | note |\n\n"
        "| Slice | Status | Window | Notes |\n"
        "| --- | --- | --- | --- |\n"
        "| Slice 3 | Pending | Soon | initial |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(programstart_serve, "ROOT", tmp_path)

    result = update_implementation_tracker_slice("Slice 3", "Ready", "Ship | this\nweek")

    updated = tracker.read_text(encoding="utf-8")
    assert result["exit_code"] == 0
    assert "| Slice 3 | Ready | Soon | Ship ¦ this week |" in updated


def test_save_workflow_signoff_persists_signoff_history(monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {}, "signoff_history": []},
        },
    }
    registry = {"systems": {"programbuild": {}}}

    monkeypatch.setattr(programstart_serve, "load_registry", lambda: registry)
    monkeypatch.setattr(programstart_serve, "load_workflow_state", lambda _registry, _system: deepcopy(state))
    monkeypatch.setattr(
        programstart_serve,
        "workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(programstart_serve, "workflow_entry_key", lambda _system: "stages")
    monkeypatch.setattr(programstart_serve, "save_workflow_state", lambda _registry, _system, value: saved.update(value))

    result = save_workflow_signoff("programbuild", "approved", "2026-04-01", "Ship | it\nnow")

    assert result["exit_code"] == 0
    signoff = saved["stages"]["inputs_and_mode_selection"]["signoff"]
    assert signoff["decision"] == "approved"
    assert signoff["date"] == "2026-04-01"
    assert signoff["notes"] == "Ship ¦ it now"
    assert saved["stages"]["inputs_and_mode_selection"]["signoff_history"][0]["notes"] == "Ship ¦ it now"


def test_advance_workflow_with_signoff_completes_current_and_promotes_next(monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {}, "signoff_history": []},
            "feasibility": {"status": "planned", "signoff": {}, "signoff_history": []},
        },
    }
    registry = {"systems": {"programbuild": {}}}

    monkeypatch.setattr(programstart_serve, "load_registry", lambda: registry)
    monkeypatch.setattr(programstart_serve, "load_workflow_state", lambda _registry, _system: deepcopy(state))
    monkeypatch.setattr(
        programstart_serve,
        "workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(programstart_serve, "workflow_entry_key", lambda _system: "stages")
    monkeypatch.setattr(
        programstart_serve,
        "workflow_steps",
        lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr(programstart_serve, "save_workflow_state", lambda _registry, _system, value: saved.update(value))

    result = advance_workflow_with_signoff("programbuild", "approved", "2026-04-02", "Ready | now", False)

    assert result["exit_code"] == 0
    assert saved["active_stage"] == "feasibility"
    assert saved["stages"]["inputs_and_mode_selection"]["status"] == "completed"
    assert saved["stages"]["feasibility"]["status"] == "in_progress"
    assert saved["stages"]["inputs_and_mode_selection"]["signoff_history"][0]["notes"] == "Ready ¦ now"
