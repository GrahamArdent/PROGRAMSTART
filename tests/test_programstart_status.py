from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry, system_is_attached
from scripts.programstart_status import main, staleness_warnings, summarize_programbuild


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
