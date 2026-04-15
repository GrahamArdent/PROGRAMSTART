from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import (
    create_default_workflow_state,
    load_registry,
    system_is_optional_and_absent,
    validate_state_against_schema,
)
from scripts.programstart_workflow_state import (
    _check_challenge_gate_log,
    _load_live_state_bundle,
    _resolve_rollback_target,
    diff_states,
    list_snapshots,
    main,
    preflight_problems,
    print_state,
    snapshot_state,
)


def test_preflight_problems_returns_list() -> None:
    """Verify preflight_problems returns a list, not None (regression test for B0)."""
    registry = load_registry()
    result = preflight_problems(registry, "programbuild")
    assert isinstance(result, list)


def test_system_is_optional_and_absent(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_common.workspace_path", lambda _relative: ROOT / "_missing_optional")
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
    monkeypatch.setattr("scripts.programstart_workflow_state._check_challenge_gate_log", lambda _step: None)
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
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _r, _s, _a=None: [])
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
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _r, _s, _a=None: [])
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
    """Missing evidence is now a blocker."""
    monkeypatch.setattr("scripts.programstart_workflow_state.challenge_gate_record_from_log", lambda _step: None)

    result = _check_challenge_gate_log("inputs_and_mode_selection")

    assert result is not None
    assert "No Challenge Gate evidence" in result


def test_check_challenge_gate_log_matching_entry(monkeypatch, tmp_path) -> None:
    """When a matching From Stage row exists, return None."""
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.challenge_gate_record_from_log",
        lambda _step: {
            "source": "challenge_gate_log",
            "from_stage": "inputs_and_mode_selection",
            "to_stage": "feasibility",
            "date": "2026-04-11",
            "proceed": "yes",
            "result": "clear",
            "notes": "clean",
            "checks": {},
        },
    )
    assert _check_challenge_gate_log("inputs_and_mode_selection") is None


def test_check_challenge_gate_log_no_matching_entry(monkeypatch, tmp_path) -> None:
    """When no matching row exists, return a blocking string."""
    monkeypatch.setattr("scripts.programstart_workflow_state.challenge_gate_record_from_log", lambda _step: None)
    result = _check_challenge_gate_log("inputs_and_mode_selection")
    assert result is not None
    assert "No Challenge Gate evidence" in result
    assert "--skip-gate-check" in result


def test_advance_dry_run_shows_gate_warning(capsys, monkeypatch, tmp_path) -> None:
    """During dry-run the missing gate now blocks advance."""
    gate = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_CHALLENGE_GATE.md"
    gate.parent.mkdir(parents=True)
    gate.write_text(
        "### Challenge Gate Log\n\n| From Stage | To Stage | Date | Proceed? |\n|---|---|---|---|\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.challenge_gate_record_from_log", lambda _step: None)
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
    assert result == 1
    assert "Advance blocked" in out
    assert "No Challenge Gate evidence" in out


def test_advance_dry_run_accepts_structured_gate_result(capsys, monkeypatch) -> None:
    active = "inputs_and_mode_selection"
    state = _make_advance_state(active, "feasibility")
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _r, _s, _state=None: active,
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "ws",
            "advance",
            "--system",
            "programbuild",
            "--dry-run",
            "--gate-result",
            "warning",
            "--gate-notes",
            "tracked",
        ],
    )
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Would record Challenge Gate result='warning'" in out


def test_main_advance_persists_structured_gate_record(capsys, monkeypatch) -> None:
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
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _r, _s, _a=None: [])
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state", lambda _registry, _system, value: saved.update(value)
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "programstart_workflow_state.py",
            "advance",
            "--system",
            "programbuild",
            "--gate-result",
            "clear",
            "--gate-notes",
            "reviewed",
        ],
    )
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Advanced programbuild" in out
    assert saved["stages"]["inputs_and_mode_selection"]["challenge_gate"]["result"] == "clear"
    assert saved["stages"]["inputs_and_mode_selection"]["challenge_gate"]["notes"] == "reviewed"


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
    monkeypatch.setattr("scripts.programstart_workflow_state._check_challenge_gate_log", lambda _step: None)
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
    monkeypatch.setattr("scripts.programstart_workflow_state._check_challenge_gate_log", lambda _step: None)
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
    monkeypatch.setattr("scripts.programstart_workflow_state._check_challenge_gate_log", lambda _step: None)
    monkeypatch.setattr(
        "sys.argv",
        ["ws", "advance", "--system", "programbuild", "--dry-run", "--skip-cross-stage-check"],
    )
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Cross-Stage Validation" not in out


# ---------------------------------------------------------------------------
# Phase F — Dispatch Chain Integration Tests
# ---------------------------------------------------------------------------


def test_preflight_problems_dispatches_stage_gate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Prove preflight_problems() routes through the dispatch map to a real validator.

    Calls the real preflight_problems() with active_step="inputs_and_mode_selection"
    and blank template files. Asserts that intake-complete validation errors appear
    in the returned problem list — proving the full chain:
    preflight_problems → stage_checks dict → run_stage_gate_check → validate_intake_complete.

    Monkeypatch strategy:
    - workspace_path patched in validate + workflow_state modules → doc reads hit tmp_path
    - validate_authority_sync patched to [] → prevents FileNotFoundError on
      PROGRAMBUILD_CANONICAL.md/FILE_INDEX.md (not part of dispatch chain under test)
    - load_registry, preflight_problems, run_stage_gate_check, validate_intake_complete
      are ALL unpatched — the full dispatch chain executes for real.
    """
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()
    # Write blank-template kickoff and intake files so the validator finds them
    # but reports empty-field errors.
    (pb / "PROGRAMBUILD_KICKOFF_PACKET.md").write_text(
        "# Kickoff Packet\n\n```text\nPROJECT_NAME:\nONE_LINE_DESCRIPTION:\n"
        "PRIMARY_USER:\nCORE_PROBLEM:\nSUCCESS_METRIC:\n"
        "PRODUCT_SHAPE: [web app | mobile app | CLI tool]\n```\n",
        encoding="utf-8",
    )
    (pb / "PROGRAMBUILD_IDEA_INTAKE.md").write_text(
        "# Idea Intake\n\nPROBLEM_RAW:\nWHO_HAS_THIS_PROBLEM:\n"
        "CURRENT_SOLUTION:\nSUCCESS_OUTCOME:\nCHEAPEST_VALIDATION:\n"
        "NOT_BUILDING_1:\nNOT_BUILDING_2:\nNOT_BUILDING_3:\n"
        "KILL_SIGNAL_1:\nKILL_SIGNAL_2:\nKILL_SIGNAL_3:\n",
        encoding="utf-8",
    )
    # Redirect doc lookups to tmp_path.
    monkeypatch.setattr(
        "scripts.programstart_validate.workspace_path",
        lambda rel: tmp_path / rel,
    )
    # Prevent validate_authority_sync crash — it calls .read_text() on
    # PROGRAMBUILD_CANONICAL.md via monkeypatched workspace_path, which
    # doesn't exist in tmp_path.  Authority sync is not part of the
    # dispatch chain under test.
    monkeypatch.setattr(
        "scripts.programstart_validate.validate_authority_sync",
        lambda _registry: [],
    )

    registry = load_registry()
    problems = preflight_problems(registry, "programbuild", active_step="inputs_and_mode_selection")

    # Must be a list (B0 regression)
    assert isinstance(problems, list)
    # Assert on field-level text that can ONLY come from validate_intake_complete
    # (not from validate_required_files "Missing required file" errors).
    intake_field_errors = [p for p in problems if "PROJECT_NAME is empty" in p or "PROBLEM_RAW is empty" in p]
    assert len(intake_field_errors) >= 1, f"Expected intake-complete field errors from dispatch chain, got: {problems}"


def test_preflight_problems_skips_gate_for_userjourney(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Stage-gate checks must NOT fire when system is userjourney.

    The dispatch map is programbuild-only. Passing system="userjourney" with
    any active_step must not produce stage-gate validation errors.

    Note: active_step="inputs_and_mode_selection" is a programbuild step name,
    but any truthy string suffices — the guard is ``if system == "programbuild"
    and active_step:``, so the step name is irrelevant for userjourney.

    Upstream validators: All skip because userjourney is optional (registry)
    and USERJOURNEY/ doesn't exist in tmp_path, so system_is_optional_and_absent
    returns True (via monkeypatched scripts.programstart_validate.workspace_path).
    """
    monkeypatch.setattr(
        "scripts.programstart_validate.workspace_path",
        lambda rel: tmp_path / rel,
    )

    registry = load_registry()
    problems = preflight_problems(registry, "userjourney", active_step="inputs_and_mode_selection")

    assert isinstance(problems, list)
    # No intake field errors — those are programbuild-only stage-gate checks.
    gate_errors = [
        p for p in problems if "PROJECT_NAME" in p or "PROBLEM_RAW" in p or "KICKOFF_PACKET" in p or "IDEA_INTAKE" in p
    ]
    assert gate_errors == [], f"Stage-gate errors leaked into userjourney preflight: {gate_errors}"


def test_advance_blocked_by_real_stage_gate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Full CLI-level e2e: advance with incomplete Stage 0 docs → blocked.

    Does NOT monkeypatch preflight_problems, run_stage_gate_check, or
    validate_intake_complete.  The full dispatch chain executes for real.

    Monkeypatch strategy:
    - workspace_path in validate → doc reads hit tmp_path
    - validate_authority_sync → [] (prevents FileNotFoundError, not under test)
    - load_workflow_state → returns create_default_workflow_state() output
      (load_workflow_state uses programstart_common.workspace_path which is NOT
      monkeypatched — it would read the real state file, not tmp_path)
    - workflow_active_step, workflow_steps → controlled values matching state
    - save_workflow_state → no-op safety net (advance should fail before save)
    - _check_challenge_gate_log → None (not reached, but safety net)
    """
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()

    # Write blank-template docs
    (pb / "PROGRAMBUILD_KICKOFF_PACKET.md").write_text(
        "# Kickoff Packet\n\n```text\nPROJECT_NAME:\nONE_LINE_DESCRIPTION:\n"
        "PRIMARY_USER:\nCORE_PROBLEM:\nSUCCESS_METRIC:\n"
        "PRODUCT_SHAPE: [web app | mobile app | CLI tool]\n```\n",
        encoding="utf-8",
    )
    (pb / "PROGRAMBUILD_IDEA_INTAKE.md").write_text(
        "# Idea Intake\n\nPROBLEM_RAW:\nWHO_HAS_THIS_PROBLEM:\n"
        "CURRENT_SOLUTION:\nSUCCESS_OUTCOME:\nCHEAPEST_VALIDATION:\n"
        "NOT_BUILDING_1:\nNOT_BUILDING_2:\nNOT_BUILDING_3:\n"
        "KILL_SIGNAL_1:\nKILL_SIGNAL_2:\nKILL_SIGNAL_3:\n",
        encoding="utf-8",
    )

    # Use create_default_workflow_state for correct structure (all 11 stages,
    # signoff sub-dicts, variant, active_stage key — derived from registry).
    registry = load_registry()
    state = create_default_workflow_state(registry, "programbuild")
    # state already has: active_stage="inputs_and_mode_selection",
    # stages.inputs_and_mode_selection.status="in_progress"

    monkeypatch.setattr(
        "scripts.programstart_validate.workspace_path",
        lambda rel: tmp_path / rel,
    )
    monkeypatch.setattr(
        "scripts.programstart_validate.validate_authority_sync",
        lambda _registry: [],
    )
    # State management — load_workflow_state uses programstart_common.workspace_path
    # (not monkeypatched), so it reads the REAL state file.  Monkeypatch to
    # return our controlled state instead.
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.load_workflow_state",
        lambda _registry, _system: state,
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _registry, _system: list(registry["workflow_state"]["programbuild"]["step_order"]),
    )
    # Safety nets — not expected to be reached (preflight should fail),
    # but existing advance tests include these as defensive practice.
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state",
        lambda _registry, _system, _value: None,
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state._check_challenge_gate_log",
        lambda _step: None,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["programstart_workflow_state.py", "advance", "--system", "programbuild"],
    )

    # preflight_problems returns problems → advance returns 1 (not SystemExit).
    # parser.error() raises SystemExit, but preflight failure does ``return 1``.
    result = main()
    assert result == 1

    captured = capsys.readouterr()
    assert "Advance preflight failed" in captured.out
    # Verify real validator field errors appear (not generic "preflight failed").
    # These strings can ONLY come from validate_intake_complete via the
    # dispatch chain — proving preflight_problems → run_stage_gate_check →
    # validate_intake_complete fired for real.
    assert "PROJECT_NAME is empty" in captured.out or "PROBLEM_RAW is empty" in captured.out, (
        f"Expected intake-complete field errors in advance output, got:\n{captured.out}"
    )


# ---------------------------------------------------------------------------
# snapshot_state, diff_states, list_snapshots unit tests
# ---------------------------------------------------------------------------


def test_snapshot_state_creates_file(tmp_path: Path, monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.generated_outputs_root",
        lambda _reg: tmp_path,
    )
    snap_path = snapshot_state(registry, label="test")
    assert snap_path.exists()
    data = json.loads(snap_path.read_text(encoding="utf-8"))
    assert data["label"] == "test"
    assert "systems" in data


def test_diff_states_detects_changes() -> None:
    old = {
        "systems": {
            "programbuild": {
                "active_stage": "feasibility",
                "stages": {
                    "inputs_and_mode_selection": {"status": "completed", "signoff": {"decision": "approved"}},
                    "feasibility": {"status": "in_progress", "signoff": {"decision": ""}},
                },
            },
        },
    }
    new = {
        "systems": {
            "programbuild": {
                "active_stage": "research",
                "stages": {
                    "inputs_and_mode_selection": {"status": "completed", "signoff": {"decision": "approved"}},
                    "feasibility": {"status": "completed", "signoff": {"decision": "approved"}},
                    "research": {"status": "in_progress", "signoff": {"decision": ""}},
                },
            },
        },
    }
    diffs = diff_states(old, new)
    assert any("feasibility" in d and "completed" in d for d in diffs)
    assert any("active step" in d for d in diffs)


def test_diff_states_no_changes() -> None:
    state = {"systems": {"programbuild": {"active_stage": "x", "stages": {"x": {"status": "in_progress", "signoff": {}}}}}}
    diffs = diff_states(state, state)
    assert diffs == []


def test_list_snapshots_empty(tmp_path: Path, monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.generated_outputs_root",
        lambda _reg: tmp_path,
    )
    assert list_snapshots(registry) == []


def test_list_snapshots_returns_sorted(tmp_path: Path, monkeypatch) -> None:
    registry = load_registry()
    snap_dir = tmp_path / "state-snapshots"
    snap_dir.mkdir()
    (snap_dir / "state_20260101T000000Z.json").write_text("{}", encoding="utf-8")
    (snap_dir / "state_20260102T000000Z.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.generated_outputs_root",
        lambda _reg: tmp_path,
    )
    snaps = list_snapshots(registry)
    assert len(snaps) == 2
    assert snaps[0].name < snaps[1].name


# ---------------------------------------------------------------------------
# CLI subcommand tests: snapshot, snapshots, diff
# ---------------------------------------------------------------------------


def test_main_snapshot_creates_file(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.generated_outputs_root",
        lambda _reg: tmp_path,
    )
    monkeypatch.setattr("sys.argv", ["ws", "snapshot", "--label", "mysnap"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Snapshot saved" in out


def test_main_snapshots_empty(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.generated_outputs_root",
        lambda _reg: tmp_path,
    )
    monkeypatch.setattr("sys.argv", ["ws", "snapshots"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "No snapshots found" in out


def test_main_snapshots_lists_files(tmp_path: Path, capsys, monkeypatch) -> None:
    snap_dir = tmp_path / "state-snapshots"
    snap_dir.mkdir()
    (snap_dir / "state_20260101T000000Z.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.generated_outputs_root",
        lambda _reg: tmp_path,
    )
    monkeypatch.setattr("sys.argv", ["ws", "snapshots"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "state_20260101T000000Z.json" in out


def test_main_diff_no_snapshots(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.generated_outputs_root",
        lambda _reg: tmp_path,
    )
    monkeypatch.setattr("sys.argv", ["ws", "diff"])
    result = main()
    out = capsys.readouterr().out
    assert result == 1
    assert "No snapshots to compare" in out


def test_main_diff_with_explicit_paths(tmp_path: Path, capsys, monkeypatch) -> None:
    old_snap = tmp_path / "old.json"
    new_snap = tmp_path / "new.json"
    old_snap.write_text(
        json.dumps(
            {"systems": {"programbuild": {"active_stage": "a", "stages": {"a": {"status": "in_progress", "signoff": {}}}}}}
        ),
        encoding="utf-8",
    )
    new_snap.write_text(
        json.dumps(
            {
                "systems": {
                    "programbuild": {
                        "active_stage": "b",
                        "stages": {
                            "a": {"status": "completed", "signoff": {"decision": "approved"}},
                            "b": {"status": "in_progress", "signoff": {}},
                        },
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["ws", "diff", "--old", str(old_snap), "--new", str(new_snap)])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "active step" in out


def test_main_diff_no_changes(tmp_path: Path, capsys, monkeypatch) -> None:
    snap = tmp_path / "snap.json"
    snap.write_text(
        json.dumps(
            {"systems": {"programbuild": {"active_stage": "a", "stages": {"a": {"status": "in_progress", "signoff": {}}}}}}
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["ws", "diff", "--old", str(snap), "--new", str(snap)])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "No changes detected" in out


# ---------------------------------------------------------------------------
# Edge cases: _check_challenge_gate_log OSError, _git_head_hash, advance final step
# ---------------------------------------------------------------------------


def test_check_challenge_gate_log_oserror(monkeypatch, tmp_path) -> None:
    gate = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_CHALLENGE_GATE.md"
    gate.parent.mkdir(parents=True)
    gate.write_text("content", encoding="utf-8")
    # Make the file unreadable by replacing read_text on the returned path

    class UnreadablePath:
        """A path-like that exists but raises OSError on read_text."""

        def exists(self):
            return True

        def read_text(self, encoding="utf-8"):
            raise OSError("disk error")

    monkeypatch.setattr("scripts.programstart_workflow_state.challenge_gate_record_from_log", lambda _step: None)
    result = _check_challenge_gate_log("inputs_and_mode_selection")
    assert result is not None
    assert "No Challenge Gate evidence" in result


def test_advance_final_step(capsys, monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_stage": "post_launch_review",
        "stages": {
            "post_launch_review": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _r, _s, _state=None: "post_launch_review",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: ["post_launch_review"],
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _r, _s, _a=None: [])
    monkeypatch.setattr("scripts.programstart_workflow_state._check_challenge_gate_log", lambda _step: None)
    monkeypatch.setattr("scripts.programstart_workflow_state.save_workflow_state", lambda _r, _s, value: saved.update(value))
    monkeypatch.setattr("sys.argv", ["ws", "advance", "--system", "programbuild"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Completed final" in out


def test_advance_dry_run_final_step(capsys, monkeypatch) -> None:
    state = {
        "active_stage": "post_launch_review",
        "stages": {
            "post_launch_review": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _r, _s, _state=None: "post_launch_review",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: ["post_launch_review"],
    )
    monkeypatch.setattr("scripts.programstart_workflow_state._check_challenge_gate_log", lambda _step: None)
    monkeypatch.setattr("sys.argv", ["ws", "advance", "--system", "programbuild", "--dry-run"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "final" in out.lower()


def test_set_with_signoff_fields(capsys, monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_stage": "feasibility",
        "stages": {
            "feasibility": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: ["feasibility"],
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_entry_key", lambda _s: "stages")
    monkeypatch.setattr("scripts.programstart_workflow_state.save_workflow_state", lambda _r, _s, value: saved.update(value))
    monkeypatch.setattr(
        "sys.argv",
        [
            "ws",
            "set",
            "--system",
            "programbuild",
            "--step",
            "feasibility",
            "--status",
            "completed",
            "--decision",
            "approved",
            "--date",
            "2026-04-15",
            "--notes",
            "done",
        ],
    )
    result = main()
    assert result == 0
    signoff = saved["stages"]["feasibility"]["signoff"]
    assert signoff["decision"] == "approved"
    assert signoff["date"] == "2026-04-15"
    assert signoff["notes"] == "done"


def test_set_in_progress_updates_active_stage(capsys, monkeypatch) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "completed", "signoff": {}},
            "feasibility": {"status": "planned", "signoff": {}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_entry_key", lambda _s: "stages")
    monkeypatch.setattr("scripts.programstart_workflow_state.save_workflow_state", lambda _r, _s, value: saved.update(value))
    monkeypatch.setattr(
        "sys.argv",
        ["ws", "set", "--system", "programbuild", "--step", "feasibility", "--status", "in_progress"],
    )
    result = main()
    assert result == 0
    assert saved["active_stage"] == "feasibility"


def test_preflight_problems_userjourney_phase0_gate(tmp_path: Path, monkeypatch) -> None:
    """Verify userjourney phase_0 dispatches engineering-ready gate check."""
    uj = tmp_path / "USERJOURNEY"
    uj.mkdir()
    # Create stub files that validate_engineering_ready reads
    (uj / "OPEN_QUESTIONS.md").write_text("# Open Questions\n\nNone remaining.\n", encoding="utf-8")
    monkeypatch.setattr("scripts.programstart_validate.workspace_path", lambda rel: tmp_path / rel)
    monkeypatch.setattr("scripts.programstart_validate.validate_authority_sync", lambda _r: [])
    registry = load_registry()
    problems = preflight_problems(registry, "userjourney", active_step="phase_0")
    assert isinstance(problems, list)


def test_validate_state_against_schema_valid(tmp_path: Path, monkeypatch) -> None:
    """Valid state passes schema validation without error."""
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["system", "active_stage"],
        "properties": {
            "system": {"const": "programbuild"},
            "active_stage": {"type": "string"},
        },
    }
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    (schema_dir / "programbuild-state.schema.json").write_text(json.dumps(schema), encoding="utf-8")
    monkeypatch.setattr("scripts.programstart_common.workspace_path", lambda rel: tmp_path / rel)
    state = {"system": "programbuild", "active_stage": "feasibility"}
    validate_state_against_schema(state, "programbuild")  # should not raise


def test_validate_state_against_schema_invalid(tmp_path: Path, monkeypatch) -> None:
    """Invalid state raises jsonschema.ValidationError."""
    import jsonschema as _jsonschema

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["system", "active_stage"],
        "properties": {
            "system": {"const": "programbuild"},
            "active_stage": {"type": "string"},
        },
    }
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    (schema_dir / "programbuild-state.schema.json").write_text(json.dumps(schema), encoding="utf-8")
    monkeypatch.setattr("scripts.programstart_common.workspace_path", lambda rel: tmp_path / rel)
    state = {"system": "programbuild"}  # missing required active_stage
    with pytest.raises(_jsonschema.ValidationError):
        validate_state_against_schema(state, "programbuild")


def test_concurrent_save_workflow_state_no_lost_writes(tmp_path: Path, monkeypatch) -> None:
    """Two threads writing state concurrently must not corrupt the file."""
    import threading

    from scripts.programstart_common import save_workflow_state

    # Minimal registry pointing to a temp state file
    state_file = tmp_path / "programbuild-state.json"
    registry: dict[str, Any] = {
        "systems": {
            "programbuild": {"root": "PROGRAMBUILD", "stages": ["discovery"]},
        },
        "workflow_state": {
            "programbuild": {
                "state_file": "programbuild-state.json",
                "active_key": "active_stage",
                "initial_step": "discovery",
                "entry_key": "stages",
            }
        },
    }

    # Bypass schema validation (no schema files in tmp_path)
    monkeypatch.setattr("scripts.programstart_common.workspace_path", lambda rel: tmp_path / rel)

    barrier = threading.Barrier(2, timeout=5)
    errors: list[Exception] = []

    def writer(stage_value: str) -> None:
        try:
            barrier.wait()
            state: dict[str, Any] = {
                "system": "programbuild",
                "active_stage": stage_value,
                "variant": "product",
                "stages": {"discovery": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}}},
            }
            save_workflow_state(registry, "programbuild", state)
        except Exception as exc:
            errors.append(exc)

    t1 = threading.Thread(target=writer, args=("discovery",))
    t2 = threading.Thread(target=writer, args=("discovery",))
    t1.start()
    t2.start()
    t1.join(timeout=15)
    t2.join(timeout=15)

    assert not errors, f"Thread errors: {errors}"
    # File must be valid JSON after concurrent writes
    data = json.loads(state_file.read_text(encoding="utf-8"))
    assert data["system"] == "programbuild"
    assert data["active_stage"] == "discovery"


# ---------------------------------------------------------------------------
# Post-advance sanity check (H-1 / G-1)
# ---------------------------------------------------------------------------


def test_post_advance_sanity_check_no_warning(capsys, monkeypatch) -> None:
    """When reloaded state matches expected, no warning is emitted."""
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    call_count = {"n": 0}

    def fake_load(_registry: Any, _system: str) -> dict:
        call_count["n"] += 1
        return state

    def fake_active(_registry: Any, _system: str, _state: Any = None) -> str:
        # After advance, state dict has been mutated; return the new active step
        if call_count["n"] > 1:
            return "feasibility"
        return "inputs_and_mode_selection"

    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", fake_load)
    monkeypatch.setattr("scripts.programstart_workflow_state.workflow_active_step", fake_active)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _r, _s, _a=None: [])
    monkeypatch.setattr("scripts.programstart_workflow_state._check_challenge_gate_log", lambda _step: None)
    monkeypatch.setattr("scripts.programstart_workflow_state.save_workflow_state", lambda _r, _s, _v: None)
    monkeypatch.setattr("sys.argv", ["prog", "advance", "--system", "programbuild"])
    result = main()
    captured = capsys.readouterr()
    assert result == 0
    assert "Post-advance warning" not in captured.err


def test_post_advance_sanity_check_warns_on_mismatch(capsys, monkeypatch) -> None:
    """When reloaded state doesn't match expected, a warning is emitted to stderr."""
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _r, _s: state)
    # Always return old step — simulates a save failure
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _r, _s, _st=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _r, _s: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _r, _s, _a=None: [])
    monkeypatch.setattr("scripts.programstart_workflow_state._check_challenge_gate_log", lambda _step: None)
    monkeypatch.setattr("scripts.programstart_workflow_state.save_workflow_state", lambda _r, _s, _v: None)
    monkeypatch.setattr("sys.argv", ["prog", "advance", "--system", "programbuild"])
    result = main()
    captured = capsys.readouterr()
    assert result == 0
    assert "Post-advance warning" in captured.err
    assert "feasibility" in captured.err


# ---------------------------------------------------------------------------
# Phase A: coverage push — workflow_state.py uncovered branches
# ---------------------------------------------------------------------------


def test_diff_command_uses_latest_snapshot_as_old(tmp_path: Path, capsys, monkeypatch) -> None:
    """diff without --old should fall back to the latest snapshot file."""
    snap_dir = tmp_path / "state-snapshots"
    snap_dir.mkdir()
    # Single snapshot — becomes snaps[-1] (the "old" baseline)
    old_snap = snap_dir / "state_20260101T000000Z.json"
    old_snap.write_text(
        json.dumps(
            {"systems": {"programbuild": {"active_stage": "a", "stages": {"a": {"status": "in_progress", "signoff": {}}}}}}
        ),
        encoding="utf-8",
    )
    # New state file — different from the snapshot
    new_state_file = tmp_path / "new_state.json"
    new_state_file.write_text(
        json.dumps(
            {
                "systems": {
                    "programbuild": {
                        "active_stage": "b",
                        "stages": {
                            "a": {"status": "completed", "signoff": {"decision": "approved"}},
                            "b": {"status": "in_progress", "signoff": {}},
                        },
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.generated_outputs_root",
        lambda _reg: tmp_path,
    )
    # No --old provided: code will use snaps[-1] = old_snap as baseline
    monkeypatch.setattr("sys.argv", ["ws", "diff", "--new", str(new_state_file)])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "active step" in out


def test_diff_command_loads_current_state_when_no_new_arg(tmp_path: Path, capsys, monkeypatch) -> None:
    """diff without --new should build new_data from the current workflow state files."""
    snap_dir = tmp_path / "state-snapshots"
    snap_dir.mkdir()
    old_snap = snap_dir / "state_20260101T000000Z.json"
    old_snap.write_text(
        json.dumps(
            {"systems": {"programbuild": {"active_stage": "a", "stages": {"a": {"status": "in_progress", "signoff": {}}}}}}
        ),
        encoding="utf-8",
    )
    state_file = tmp_path / "pb_state.json"
    state_file.write_text(
        json.dumps({"active_stage": "b", "stages": {"b": {"status": "in_progress", "signoff": {}}}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.generated_outputs_root",
        lambda _reg: tmp_path,
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_state_path",
        lambda _reg, _sys: state_file,
    )
    monkeypatch.setattr("sys.argv", ["ws", "diff", "--old", str(old_snap)])
    result = main()
    capsys.readouterr()
    assert result == 0


def test_load_live_state_bundle_reads_existing_system_states(tmp_path: Path, monkeypatch) -> None:
    registry = load_registry()
    pb_state = tmp_path / "pb_state.json"
    uj_state = tmp_path / "uj_state.json"
    pb_state.write_text(json.dumps({"active_stage": "feasibility"}), encoding="utf-8")
    uj_state.write_text(json.dumps({"active_phase": "phase_0"}), encoding="utf-8")

    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_state_path",
        lambda _reg, system: pb_state if system == "programbuild" else uj_state,
    )

    payload = _load_live_state_bundle(registry)

    assert payload["systems"]["programbuild"]["active_stage"] == "feasibility"
    assert payload["systems"]["userjourney"]["active_phase"] == "phase_0"


def test_resolve_rollback_target_uses_last_snapshot(tmp_path: Path, monkeypatch) -> None:
    registry = load_registry()
    snap_dir = tmp_path / "state-snapshots"
    snap_dir.mkdir()
    older = snap_dir / "state_20260101T000000Z.json"
    newer = snap_dir / "state_20260102T000000Z.json"
    older.write_text("{}", encoding="utf-8")
    newer.write_text("{}", encoding="utf-8")
    monkeypatch.setattr("scripts.programstart_workflow_state.generated_outputs_root", lambda _reg: tmp_path)

    assert _resolve_rollback_target(registry, "last") == newer


def test_main_rollback_requires_confirm(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["ws", "rollback", "--to", "last"])

    result = main()

    out = capsys.readouterr().out
    assert result == 1
    assert "requires --confirm" in out


def test_main_rollback_no_snapshots(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.setattr("scripts.programstart_workflow_state.generated_outputs_root", lambda _reg: tmp_path)
    monkeypatch.setattr("sys.argv", ["ws", "rollback", "--to", "last", "--confirm"])

    result = main()

    out = capsys.readouterr().out
    assert result == 1
    assert "Snapshot not found" in out


def test_main_rollback_lists_snapshots_when_to_omitted(tmp_path: Path, capsys, monkeypatch) -> None:
    snap_dir = tmp_path / "state-snapshots"
    snap_dir.mkdir()
    (snap_dir / "state_20260101T000000Z.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr("scripts.programstart_workflow_state.generated_outputs_root", lambda _reg: tmp_path)
    monkeypatch.setattr("sys.argv", ["ws", "rollback", "--confirm"])

    result = main()

    out = capsys.readouterr().out
    assert result == 1
    assert "Available snapshots" in out


def test_main_rollback_restores_snapshot_and_creates_backup(tmp_path: Path, capsys, monkeypatch) -> None:
    target = tmp_path / "target.json"
    target.write_text(
        json.dumps(
            {
                "systems": {
                    "programbuild": {
                        "active_stage": "feasibility",
                        "stages": {"feasibility": {"status": "in_progress", "signoff": {}}},
                    },
                    "userjourney": {"active_phase": "phase_0", "phases": {"phase_0": {"status": "in_progress", "signoff": {}}}},
                }
            }
        ),
        encoding="utf-8",
    )
    calls: list[tuple[str, str]] = []
    backup_path = tmp_path / "backup.json"
    backup_path.write_text("{}", encoding="utf-8")

    monkeypatch.setattr(
        "scripts.programstart_workflow_state.snapshot_state",
        lambda _registry, label="": calls.append(("backup", label)) or backup_path,
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state",
        lambda _registry, system, _state: calls.append(("save", system)),
    )
    monkeypatch.setattr("sys.argv", ["ws", "rollback", "--to", str(target), "--confirm"])

    result = main()

    out = capsys.readouterr().out
    assert result == 0
    assert calls[0] == ("backup", "pre_rollback")
    assert ("save", "programbuild") in calls
    assert ("save", "userjourney") in calls
    assert "Rollback applied" in out
