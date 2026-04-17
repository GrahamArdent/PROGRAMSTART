from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry, system_is_attached
from scripts.programstart_status import (
    _stale_label,
    cross_system_health_warning,
    main,
    staleness_warnings,
    summarize_programbuild,
)


def test_system_is_attached_false(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_common.workspace_path", lambda _relative: ROOT / "_definitely_missing")
    assert not system_is_attached(registry, "programbuild")


def test_summarize_programbuild_missing_control(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_status.load_workflow_state", lambda _registry, _system: {"variant": "product"})
    monkeypatch.setattr("scripts.programstart_status.workflow_active_step", lambda _registry, _system, _state=None: "feasibility")

    def fake_exists(path: Path) -> bool:
        rel = path.relative_to(ROOT).as_posix()
        return rel != "PROGRAMBUILD/PROGRAMBUILD.md"

    monkeypatch.setattr(Path, "exists", fake_exists)
    lines = summarize_programbuild(registry)
    assert any("restore missing control files" in line for line in lines)


def test_summarize_programbuild_missing_output(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_status.load_workflow_state", lambda _registry, _system: {"variant": "product"})
    monkeypatch.setattr("scripts.programstart_status.workflow_active_step", lambda _registry, _system, _state=None: "feasibility")

    def fake_exists(path: Path) -> bool:
        rel = path.relative_to(ROOT).as_posix()
        return rel != "PROGRAMBUILD/FEASIBILITY.md"

    monkeypatch.setattr(Path, "exists", fake_exists)
    lines = summarize_programbuild(registry)
    assert any("create or restore PROGRAMBUILD/FEASIBILITY.md" in line for line in lines)


def test_summarize_programbuild_all_present(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_status.load_workflow_state", lambda _registry, _system: {"variant": "enterprise"})
    monkeypatch.setattr(
        "scripts.programstart_status.workflow_active_step", lambda _registry, _system, _state=None: "architecture"
    )
    lines = summarize_programbuild(registry)
    assert any("all standard PROGRAMBUILD" in line for line in lines)
    assert any("architecture" in line for line in lines)


def test_main_all_systems(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_status.py"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "PROGRAMBUILD" in out
    assert "USERJOURNEY" in out


def test_main_programbuild_only(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_status.py", "--system", "programbuild"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "PROGRAMBUILD" in out


# ---------- Staleness detection ----------

from datetime import date


def _make_state(signoff_date: str) -> dict:
    return {
        "stages": {
            "inputs_and_mode_selection": {
                "status": "in_progress",
                "signoff": {"decision": "approved", "date": signoff_date, "notes": ""},
            },
        },
    }


def test_staleness_no_warning_recent(monkeypatch) -> None:
    registry = load_registry()
    today = date(2026, 4, 15)
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _r, _s: _make_state("2026-04-01"),
    )
    warnings = staleness_warnings(registry, "programbuild", today=today)
    assert warnings == []


def test_staleness_warning_at_30_days(monkeypatch) -> None:
    registry = load_registry()
    today = date(2026, 5, 1)
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _r, _s: _make_state("2026-04-01"),
    )
    warnings = staleness_warnings(registry, "programbuild", today=today)
    assert len(warnings) == 1
    assert "30 days ago" in warnings[0]
    assert "Consider running" in warnings[0]


def test_staleness_escalated_warning_at_60_days(monkeypatch) -> None:
    registry = load_registry()
    today = date(2026, 6, 1)
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _r, _s: _make_state("2026-04-01"),
    )
    warnings = staleness_warnings(registry, "programbuild", today=today)
    assert len(warnings) == 1
    assert "Strongly consider" in warnings[0]


def test_staleness_no_warning_when_no_dates(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _r, _s: {"stages": {"inputs_and_mode_selection": {"status": "in_progress", "signoff": {}}}},
    )
    warnings = staleness_warnings(registry, "programbuild", today=date(2026, 6, 1))
    assert warnings == []


def test_staleness_skip_flag(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_status.py", "--system", "programbuild", "--skip-staleness-check"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "days ago" not in out


def test_staleness_skip_env_var(capsys, monkeypatch) -> None:
    monkeypatch.setenv("PROGRAMSTART_SKIP_STALENESS", "1")
    monkeypatch.setattr("sys.argv", ["programstart_status.py", "--system", "programbuild"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "days ago" not in out


# ---------- Cross-system health warning (H-3 / G-2) ----------


def _make_pb_state(active: str) -> dict:
    return {"active_stage": active, "stages": {active: {"status": "in_progress"}}}


def _make_uj_state(active: str) -> dict:
    return {"active_phase": active, "phases": {active: {"status": "in_progress"}}}


def test_cross_system_no_warning_when_close(monkeypatch) -> None:
    registry = load_registry()
    pb_steps = ["inputs_and_mode_selection", "feasibility", "research"]
    uj_steps = ["phase_0", "phase_1", "phase_2"]
    monkeypatch.setattr("scripts.programstart_status.system_is_attached", lambda _r, _s: True)
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _r, s: _make_pb_state("feasibility") if s == "programbuild" else _make_uj_state("phase_1"),
    )
    monkeypatch.setattr(
        "scripts.programstart_status.workflow_active_step",
        lambda _r, s, _st=None: "feasibility" if s == "programbuild" else "phase_1",
    )
    monkeypatch.setattr(
        "scripts.programstart_status.workflow_steps",
        lambda _r, s: pb_steps if s == "programbuild" else uj_steps,
    )
    warnings = cross_system_health_warning(registry)
    assert warnings == []


def test_cross_system_warning_when_pb_ahead(monkeypatch) -> None:
    registry = load_registry()
    pb_steps = ["s0", "s1", "s2", "s3"]
    uj_steps = ["p0", "p1", "p2"]
    monkeypatch.setattr("scripts.programstart_status.system_is_attached", lambda _r, _s: True)
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _r, s: _make_pb_state("s3") if s == "programbuild" else _make_uj_state("p0"),
    )
    monkeypatch.setattr(
        "scripts.programstart_status.workflow_active_step",
        lambda _r, s, _st=None: "s3" if s == "programbuild" else "p0",
    )
    monkeypatch.setattr(
        "scripts.programstart_status.workflow_steps",
        lambda _r, s: pb_steps if s == "programbuild" else uj_steps,
    )
    warnings = cross_system_health_warning(registry)
    assert len(warnings) == 1
    assert "PROGRAMBUILD" in warnings[0]
    assert "consider advancing USERJOURNEY" in warnings[0]


def test_cross_system_warning_when_uj_ahead(monkeypatch) -> None:
    registry = load_registry()
    pb_steps = ["s0", "s1", "s2"]
    uj_steps = ["p0", "p1", "p2", "p3"]
    monkeypatch.setattr("scripts.programstart_status.system_is_attached", lambda _r, _s: True)
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _r, s: _make_pb_state("s0") if s == "programbuild" else _make_uj_state("p3"),
    )
    monkeypatch.setattr(
        "scripts.programstart_status.workflow_active_step",
        lambda _r, s, _st=None: "s0" if s == "programbuild" else "p3",
    )
    monkeypatch.setattr(
        "scripts.programstart_status.workflow_steps",
        lambda _r, s: pb_steps if s == "programbuild" else uj_steps,
    )
    warnings = cross_system_health_warning(registry)
    assert len(warnings) == 1
    assert "USERJOURNEY" in warnings[0]
    assert "consider advancing PROGRAMBUILD" in warnings[0]


def test_cross_system_no_warning_when_uj_not_attached(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_status.system_is_attached", lambda _r, _s: False)
    warnings = cross_system_health_warning(registry)
    assert warnings == []


# ---------------------------------------------------------------------------
# F-1: Stage stale label tests
# ---------------------------------------------------------------------------


def test_stale_label_no_signoffs_returns_empty(monkeypatch) -> None:
    """_stale_label returns '' when there are no signoff dates in the state."""
    from scripts.programstart_common import load_registry

    registry = load_registry()
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _reg, _sys: {"stages": {}},
    )
    result = _stale_label(registry, "programbuild")
    assert result == ""


def test_stale_label_recent_signoff_returns_empty(monkeypatch) -> None:
    """_stale_label returns '' when last signoff is within the threshold."""
    from datetime import date, timedelta

    from scripts.programstart_common import load_registry

    registry = load_registry()
    recent = (date.today() - timedelta(days=5)).isoformat()
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _reg, _sys: {"stages": {"kickoff": {"signoff": {"date": recent}}}},
    )
    monkeypatch.setenv("PROGRAMSTART_STALE_DAYS", "14")
    result = _stale_label(registry, "programbuild")
    assert result == ""


def test_stale_label_old_signoff_returns_label(monkeypatch) -> None:
    """_stale_label returns '[STALE — N days]' when last signoff exceeds threshold."""
    from datetime import date, timedelta

    from scripts.programstart_common import load_registry

    registry = load_registry()
    old = (date.today() - timedelta(days=20)).isoformat()
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _reg, _sys: {"stages": {"kickoff": {"signoff": {"date": old}}}},
    )
    monkeypatch.setenv("PROGRAMSTART_STALE_DAYS", "14")
    result = _stale_label(registry, "programbuild")
    assert "STALE" in result
    assert "20 days" in result


def test_stale_label_custom_threshold_via_env(monkeypatch) -> None:
    """PROGRAMSTART_STALE_DAYS env var controls the stale threshold."""
    from datetime import date, timedelta

    from scripts.programstart_common import load_registry

    registry = load_registry()
    old = (date.today() - timedelta(days=10)).isoformat()
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _reg, _sys: {"stages": {"kickoff": {"signoff": {"date": old}}}},
    )
    # With threshold=7, 10 days ago IS stale
    monkeypatch.setenv("PROGRAMSTART_STALE_DAYS", "7")
    result = _stale_label(registry, "programbuild")
    assert "STALE" in result

    # With threshold=30, 10 days ago is NOT stale
    monkeypatch.setenv("PROGRAMSTART_STALE_DAYS", "30")
    result2 = _stale_label(registry, "programbuild")
    assert result2 == ""


# ---------------------------------------------------------------------------
# Phase F: deferred date resets staleness timer
# ---------------------------------------------------------------------------


def test_stale_label_deferred_date_resets_staleness(monkeypatch) -> None:
    """A recent deferred date prevents the STALE label even when signoff is old."""
    from datetime import date, timedelta

    from scripts.programstart_common import load_registry

    registry = load_registry()
    old_signoff = (date.today() - timedelta(days=30)).isoformat()
    recent_defer = (date.today() - timedelta(days=2)).isoformat()
    monkeypatch.setattr(
        "scripts.programstart_status.load_workflow_state",
        lambda _reg, _sys: {
            "stages": {
                "kickoff": {
                    "signoff": {"date": old_signoff},
                    "deferred": {"date": recent_defer, "reason": "Template repo"},
                },
            }
        },
    )
    monkeypatch.setenv("PROGRAMSTART_STALE_DAYS", "14")
    result = _stale_label(registry, "programbuild")
    assert result == ""


def test_latest_activity_date_picks_deferred_over_signoff() -> None:
    """_latest_activity_date returns the most recent date across signoff and deferred."""
    from datetime import date

    from scripts.programstart_status import _latest_activity_date

    entries = {
        "step_a": {
            "signoff": {"date": "2026-03-01"},
            "deferred": {"date": "2026-04-15"},
        },
        "step_b": {
            "signoff": {"date": "2026-04-01"},
        },
    }
    result = _latest_activity_date(entries)
    assert result == date(2026, 4, 15)


def test_latest_activity_date_no_dates_returns_none() -> None:
    """_latest_activity_date returns None when no dates are present."""
    from scripts.programstart_status import _latest_activity_date

    entries = {"step_a": {"signoff": {}}}
    assert _latest_activity_date(entries) is None
