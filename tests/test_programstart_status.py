from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry
from scripts.programstart_status import main, summarize_programbuild, summarize_userjourney, system_is_attached


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


def test_summarize_userjourney_not_attached(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_status.system_is_attached", lambda _registry, _system: False)
    lines = summarize_userjourney(registry)
    assert any("not attached" in line for line in lines)


def test_summarize_userjourney_missing_files(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_status.load_workflow_state", lambda _registry, _system: {"active_phase": "phase_1"})
    monkeypatch.setattr("scripts.programstart_status.workflow_active_step", lambda _registry, _system, _state=None: "phase_1")

    def fake_exists(path: Path) -> bool:
        rel = path.relative_to(ROOT).as_posix()
        return rel != "USERJOURNEY/PRODUCT_SPEC.md"

    monkeypatch.setattr(Path, "exists", fake_exists)
    lines = summarize_userjourney(registry)
    assert any("restore missing core USERJOURNEY files" in line for line in lines)


def test_summarize_userjourney_open_items(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_status.load_workflow_state", lambda _registry, _system: {"active_phase": "phase_2"})
    monkeypatch.setattr("scripts.programstart_status.workflow_active_step", lambda _registry, _system, _state=None: "phase_2")
    monkeypatch.setattr("scripts.programstart_status.extract_numbered_items", lambda _text, _heading: ["Legal review"])
    monkeypatch.setattr(
        "scripts.programstart_status.parse_markdown_table",
        lambda _text, _heading: [{"Phase": "Phase 2", "Goal": "Enable", "Blockers": "Legal", "Status": "in progress"}],
    )
    lines = summarize_userjourney(registry)
    assert any("unresolved external decisions: 1" in line for line in lines)
    assert any("close or explicitly defer" in line for line in lines)


def test_summarize_userjourney_without_open_items(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_status.load_workflow_state", lambda _registry, _system: {"active_phase": "phase_9"})
    monkeypatch.setattr("scripts.programstart_status.workflow_active_step", lambda _registry, _system, _state=None: "phase_9")
    monkeypatch.setattr("scripts.programstart_status.extract_numbered_items", lambda _text, _heading: [])
    monkeypatch.setattr("scripts.programstart_status.parse_markdown_table", lambda _text, _heading: [])
    lines = summarize_userjourney(registry)
    assert any("no incomplete phases found" in line for line in lines)
    assert any("execute the next incomplete slice" in line.lower() for line in lines)


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


def test_main_userjourney_only(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_status.py", "--system", "userjourney"])
    result = main()
    out = capsys.readouterr().out
    assert result == 0
    assert "USERJOURNEY" in out
