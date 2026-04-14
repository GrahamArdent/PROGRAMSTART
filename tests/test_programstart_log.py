from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry, system_is_optional_and_absent
from scripts.programstart_log import main, print_log


def test_log_all_systems(capsys, monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr("sys.argv", ["programstart_log.py"])
    result = main()
    assert result == 0
    out = capsys.readouterr().out
    assert "PROGRAMBUILD" in out


def test_log_programbuild_only(capsys, monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr("sys.argv", ["programstart_log.py", "--system", "programbuild"])
    result = main()
    assert result == 0
    out = capsys.readouterr().out
    assert "PROGRAMBUILD" in out


def test_log_userjourney_only(capsys, monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr("sys.argv", ["programstart_log.py", "--system", "userjourney"])
    result = main()
    assert result == 0


def test_print_log_contains_steps(capsys, monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    registry = load_registry()
    print_log("programbuild", registry)
    out = capsys.readouterr().out
    assert "inputs_and_mode_selection" in out
    assert "status:" in out


def test_system_is_optional_and_absent() -> None:
    registry = load_registry()
    assert not system_is_optional_and_absent(registry, "programbuild")


def test_log_userjourney_detached_message(capsys, monkeypatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr(
        "scripts.programstart_log.system_is_optional_and_absent", lambda _registry, system: system == "userjourney"
    )
    monkeypatch.setattr("sys.argv", ["programstart_log.py"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "not attached in this repository" in out
