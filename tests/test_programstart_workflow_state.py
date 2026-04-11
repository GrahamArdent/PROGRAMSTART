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
from scripts.programstart_workflow_state import _check_challenge_gate_log, main, print_state, system_is_optional_and_absent


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
    monkeypatch.setattr("scripts.programstart_workflow_state._check_challenge_gate_log", lambda _step: None)
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
    monkeypatch.setattr("scripts.programstart_workflow_state._check_challenge_gate_log", lambda _step: None)
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


# --- Challenge Gate log check tests ---


def test_check_challenge_gate_log_missing_file(monkeypatch, tmp_path) -> None:
    """When the gate file does not exist, return None (no warning)."""
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workspace_path",
        lambda p: tmp_path / p,
    )
    assert _check_challenge_gate_log("inputs_and_mode_selection") is None


def test_check_challenge_gate_log_matching_entry(monkeypatch, tmp_path) -> None:
    """When a matching From Stage row exists, return None."""
    gate = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_CHALLENGE_GATE.md"
    gate.parent.mkdir(parents=True)
    gate.write_text(
        "### Challenge Gate Log\n\n"
        "| From Stage | To Stage | Date | Proceed? | Notes |\n"
        "|---|---|---|---|---|\n"
        "| inputs_and_mode_selection | feasibility | 2026-04-11 | Yes | clean |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workspace_path",
        lambda p: tmp_path / p,
    )
    assert _check_challenge_gate_log("inputs_and_mode_selection") is None


def test_check_challenge_gate_log_no_matching_entry(monkeypatch, tmp_path) -> None:
    """When no matching row exists, return a warning string."""
    gate = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_CHALLENGE_GATE.md"
    gate.parent.mkdir(parents=True)
    gate.write_text(
        "### Challenge Gate Log\n\n| From Stage | To Stage | Date | Proceed? | Notes |\n|---|---|---|---|---|\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workspace_path",
        lambda p: tmp_path / p,
    )
    result = _check_challenge_gate_log("inputs_and_mode_selection")
    assert result is not None
    assert "No Challenge Gate log entry" in result
    assert "--skip-gate-check" in result


def test_advance_dry_run_shows_gate_warning(capsys, monkeypatch, tmp_path) -> None:
    """During dry-run the gate warning appears but advance still proceeds."""
    gate = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_CHALLENGE_GATE.md"
    gate.parent.mkdir(parents=True)
    gate.write_text(
        "### Challenge Gate Log\n\n| From Stage | To Stage | Date | Proceed? |\n|---|---|---|---|\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workspace_path",
        lambda p: tmp_path / p,
    )
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _r, _s, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr("sys.argv", ["ws", "advance", "--system", "programbuild", "--dry-run"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "No Challenge Gate log entry" in out
    assert "Would advance" in out


# --- Cross-stage validation advisory tests ---


def _make_advance_state(active: str, next_step: str):
    return {
        "active_stage": active,
        "stages": {
            active: {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            next_step: {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }


_ALL_STEPS = [
    "inputs_and_mode_selection",
    "feasibility",
    "research",
    "requirements_and_ux",
    "architecture_and_risk_spikes",
    "scaffold_and_guardrails",
]


def test_cross_stage_advisory_not_shown_at_early_stages(capsys, monkeypatch) -> None:
    """Stages 0-2 should NOT show the cross-stage advisory."""
    active = "inputs_and_mode_selection"
    state = _make_advance_state(active, "feasibility")
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _r, _s, _state=None: active,
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: _ALL_STEPS,
    )
    monkeypatch.setattr("sys.argv", ["ws", "advance", "--system", "programbuild", "--dry-run"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Cross-Stage Validation" not in out


def test_cross_stage_advisory_shown_at_stage_3(capsys, monkeypatch) -> None:
    """Stage 3 (requirements_and_ux) should show the advisory."""
    active = "requirements_and_ux"
    state = _make_advance_state(active, "architecture_and_risk_spikes")
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _r, _s, _state=None: active,
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: _ALL_STEPS,
    )
    monkeypatch.setattr("sys.argv", ["ws", "advance", "--system", "programbuild", "--dry-run"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Cross-Stage Validation" in out


def test_cross_stage_advisory_suppressed_by_flag(capsys, monkeypatch) -> None:
    """--skip-cross-stage-check should suppress the advisory."""
    active = "requirements_and_ux"
    state = _make_advance_state(active, "architecture_and_risk_spikes")
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _r, _s, _state=None: active,
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: _ALL_STEPS,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["ws", "advance", "--system", "programbuild", "--dry-run", "--skip-cross-stage-check"],
    )
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Cross-Stage Validation" not in out
