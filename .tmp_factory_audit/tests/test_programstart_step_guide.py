from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry
from scripts.programstart_step_guide import main, print_section, system_is_attached


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


def test_programbuild_guide(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--system", "programbuild"])
    result = main()
    assert result == 0
    out = capsys.readouterr().out
    assert "PROGRAMBUILD" in out


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


def test_no_system_errors(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py"])
    with pytest.raises(SystemExit):
        main()


def test_programbuild_unknown_stage_errors(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--system", "programbuild", "--stage", "unknown"])
    with pytest.raises(SystemExit):
        main()


def test_userjourney_not_attached_message(capsys, monkeypatch) -> None:
    monkeypatch.setattr("scripts.programstart_step_guide.system_is_attached", lambda _registry, _system: False)
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--system", "userjourney"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "not attached" in out


def test_userjourney_unknown_phase_errors(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_step_guide.py", "--system", "userjourney", "--phase", "unknown"])
    with pytest.raises(SystemExit):
        main()
