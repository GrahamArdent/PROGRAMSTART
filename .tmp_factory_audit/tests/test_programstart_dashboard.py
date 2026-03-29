from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry
from scripts.programstart_dashboard import main, section_programbuild, section_userjourney, system_is_attached


def test_system_is_attached_programbuild() -> None:
    registry = load_registry()
    assert system_is_attached(registry, "programbuild")


def test_section_programbuild_returns_markdown() -> None:
    registry = load_registry()
    lines = section_programbuild(registry)
    assert any("## PROGRAMBUILD" in line for line in lines)
    assert any("Control files" in line for line in lines)
    assert any("Active stage" in line for line in lines)


def test_section_userjourney_returns_markdown() -> None:
    registry = load_registry()
    lines = section_userjourney(registry)
    assert any("## USERJOURNEY" in line for line in lines)


def test_main_writes_dashboard(monkeypatch, tmp_path) -> None:
    output = tmp_path / "STATUS_DASHBOARD.md"
    monkeypatch.setattr("sys.argv", ["programstart_dashboard.py", "--output", str(output)])
    result = main()
    assert result == 0
    assert output.exists()
    text = output.read_text(encoding="utf-8")
    assert "# PROGRAMSTART Status Dashboard" in text
    assert "## PROGRAMBUILD" in text


def test_main_writes_dashboard_to_generated_outputs_by_default(monkeypatch, tmp_path) -> None:
    output_root = tmp_path / "outputs"
    monkeypatch.setattr("scripts.programstart_dashboard.generated_outputs_root", lambda _registry: output_root)
    monkeypatch.setattr("sys.argv", ["programstart_dashboard.py"])

    result = main()

    output = output_root / "STATUS_DASHBOARD.md"
    assert result == 0
    assert output.exists()


def test_section_programbuild_reports_missing_files_and_metadata(monkeypatch) -> None:
    registry = load_registry()

    def fake_exists(path: Path) -> bool:
        rel = path.relative_to(ROOT).as_posix()
        return rel not in {"PROGRAMBUILD/PROGRAMBUILD.md", "PROGRAMBUILD/FEASIBILITY.md"}

    monkeypatch.setattr(Path, "exists", fake_exists)
    monkeypatch.setattr("scripts.programstart_dashboard.has_required_metadata", lambda _text, _prefixes: ["Owner:"])
    lines = section_programbuild(registry)
    joined = "\n".join(lines)
    assert "### Missing Files" in joined
    assert "### Metadata Issues" in joined
    assert "Restore missing control files before using the workflow." in joined


def test_section_userjourney_not_attached(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_dashboard.system_is_attached", lambda _registry, _system: False)
    lines = section_userjourney(registry)
    assert any("not attached" in line for line in lines)


def test_section_userjourney_missing_files_and_open_items(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr(
        "scripts.programstart_dashboard.load_workflow_state", lambda _registry, _system: {"active_phase": "phase_1", "phases": {}}
    )
    monkeypatch.setattr("scripts.programstart_dashboard.workflow_active_step", lambda _registry, _system, _state=None: "phase_1")
    monkeypatch.setattr("scripts.programstart_dashboard.extract_numbered_items", lambda _text, _heading: ["Decision A"])
    monkeypatch.setattr(
        "scripts.programstart_dashboard.parse_markdown_table",
        lambda _text, _heading: [{"Phase": "Phase 1", "Goal": "Ship", "Blockers": "Legal", "Status": "in progress"}],
    )

    def fake_exists(path: Path) -> bool:
        rel = path.relative_to(ROOT).as_posix()
        return rel != "USERJOURNEY/PRODUCT_SPEC.md"

    monkeypatch.setattr(Path, "exists", fake_exists)
    lines = section_userjourney(registry)
    joined = "\n".join(lines)
    assert "### Missing Files" in joined
    assert "### Unresolved External Decisions" in joined
    assert "Restore missing core files before implementation planning." in joined


def test_section_userjourney_no_open_items(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_dashboard.extract_numbered_items", lambda _text, _heading: [])
    monkeypatch.setattr(
        "scripts.programstart_dashboard.parse_markdown_table",
        lambda _text, _heading: [{"Phase": "Phase 9", "Goal": "Done", "Blockers": "none", "Status": "completed"}],
    )
    lines = section_userjourney(registry)
    joined = "\n".join(lines)
    assert "Execute the next incomplete slice" in joined


def test_section_programbuild_reports_owner_not_assigned(monkeypatch) -> None:
    registry = load_registry()
    monkeypatch.setattr("scripts.programstart_dashboard.has_required_metadata", lambda _text, _prefixes: [])
    monkeypatch.setattr("scripts.programstart_dashboard.metadata_value", lambda _text, _prefix: "[ASSIGN]")
    lines = section_programbuild(registry)
    joined = "\n".join(lines)
    assert "owner not assigned" in joined


def test_section_programbuild_missing_output_next_action(monkeypatch) -> None:
    registry = load_registry()
    original_exists = Path.exists

    def fake_exists(path: Path) -> bool:
        try:
            rel = path.relative_to(ROOT).as_posix()
        except ValueError:
            return original_exists(path)
        return rel != "PROGRAMBUILD/FEASIBILITY.md"

    monkeypatch.setattr(Path, "exists", fake_exists)
    lines = section_programbuild(registry)
    joined = "\n".join(lines)
    assert "Create or restore `PROGRAMBUILD/FEASIBILITY.md`." in joined


def test_section_userjourney_reports_metadata_and_open_items(monkeypatch) -> None:
    registry = load_registry()
    registry = {
        **registry,
        "systems": {
            **registry["systems"],
            "userjourney": {
                **registry["systems"]["userjourney"],
                "metadata_required": ["USERJOURNEY/PRODUCT_SPEC.md"],
            },
        },
    }
    monkeypatch.setattr("scripts.programstart_dashboard.extract_numbered_items", lambda _text, _heading: ["Decision A"])
    monkeypatch.setattr(
        "scripts.programstart_dashboard.parse_markdown_table",
        lambda _text, _heading: [{"Phase": "Phase 1", "Goal": "Ship", "Blockers": "Legal", "Status": "in progress"}],
    )
    monkeypatch.setattr("scripts.programstart_dashboard.has_required_metadata", lambda _text, _prefixes: [])
    monkeypatch.setattr("scripts.programstart_dashboard.metadata_value", lambda _text, _prefix: "[ASSIGN]")
    lines = section_userjourney(registry)
    joined = "\n".join(lines)
    assert "### Metadata Issues" in joined
    assert "### Unresolved External Decisions" in joined
    assert "Close or explicitly defer the remaining items" in joined


def test_section_userjourney_reports_missing_metadata(monkeypatch) -> None:
    registry = load_registry()
    registry = {
        **registry,
        "systems": {
            **registry["systems"],
            "userjourney": {
                **registry["systems"]["userjourney"],
                "metadata_required": ["USERJOURNEY/PRODUCT_SPEC.md"],
            },
        },
    }
    monkeypatch.setattr("scripts.programstart_dashboard.extract_numbered_items", lambda _text, _heading: [])
    monkeypatch.setattr("scripts.programstart_dashboard.parse_markdown_table", lambda _text, _heading: [])
    monkeypatch.setattr("scripts.programstart_dashboard.has_required_metadata", lambda _text, _prefixes: ["Owner:"])
    lines = section_userjourney(registry)
    joined = "\n".join(lines)
    assert "PRODUCT_SPEC.md: missing Owner:" in joined
