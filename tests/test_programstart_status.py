from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry
from scripts.programstart_status import main, summarize_programbuild, system_is_attached


def test_system_is_attached_false(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_status.workspace_path", lambda _relative: ROOT / "_definitely_missing")
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
