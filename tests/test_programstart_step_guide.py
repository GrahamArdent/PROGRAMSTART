from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from conftest import requires_userjourney

from scripts.programstart_common import load_registry, system_is_attached
from scripts.programstart_step_guide import main, print_section


def test_system_is_attached_programbuild() -> None:
    registry = load_registry()
    assert system_is_attached(registry, "programbuild")


def test_print_section_outputs_items(capsys) -> None:
    print_section("TestSection", ["alpha", "beta"])
    out = capsys.readouterr().out
    assert "TestSection:" in out
    assert "- alpha" in out
    assert "- beta" in out


def test_print_section_empty_list(capsys) -> None:
    print_section("Empty", [])
    assert capsys.readouterr().out == ""


def test_kickoff_guide(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--kickoff"])
    result = main()
    assert result == 0
    out = capsys.readouterr().out
    assert "Kickoff" in out


def test_operator_guide(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--operator"])
    result = main()
    assert result == 0
    out = capsys.readouterr().out
    assert "Operator Prompts" in out
    assert "execute-hardening-gameplan.prompt.md" in out


def test_programbuild_guide(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--system", "programbuild"])
    result = main()
    assert result == 0
    out = capsys.readouterr().out
    assert "PROGRAMBUILD" in out


@requires_userjourney
def test_userjourney_guide(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--system", "userjourney"])
    result = main()
    assert result == 0


def test_programbuild_guide_with_stage(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--system", "programbuild", "--stage", "feasibility"])
    result = main()
    assert result == 0
    out = capsys.readouterr().out
    assert "feasibility" in out.lower()


def test_audit_stage_guide_excludes_operator_prompt(capsys, monkeypatch) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["programstart_step_guide.py", "--system", "programbuild", "--stage", "audit_and_drift_control"],
    )
    result = main()
    assert result == 0
    out = capsys.readouterr().out
    assert "shape-audit.prompt.md" in out
    assert "audit-process-drift.prompt.md" not in out


def test_no_system_errors(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py"])
    with pytest.raises(SystemExit):
        main()


def test_programbuild_unknown_stage_errors(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--system", "programbuild", "--stage", "unknown"])
    with pytest.raises(SystemExit):
        main()


@requires_userjourney
def test_userjourney_not_attached_message(capsys, monkeypatch) -> None:
    monkeypatch.setattr("scripts.programstart_step_guide.system_is_attached", lambda _registry, _system: False)
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--system", "userjourney"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "not attached" in out


@requires_userjourney
def test_userjourney_unknown_phase_errors(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--system", "userjourney", "--phase", "unknown"])
    with pytest.raises(SystemExit):
        main()
