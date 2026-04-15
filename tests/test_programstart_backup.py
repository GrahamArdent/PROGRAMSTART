from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_backup


def _registry_with_states(tmp_path: Path) -> dict:
    programbuild_state = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json"
    userjourney_state = tmp_path / "USERJOURNEY" / "USERJOURNEY_STATE.json"
    programbuild_state.parent.mkdir(parents=True, exist_ok=True)
    userjourney_state.parent.mkdir(parents=True, exist_ok=True)
    programbuild_state.write_text('{"system": "programbuild"}\n', encoding="utf-8")
    userjourney_state.write_text('{"system": "userjourney"}\n', encoding="utf-8")
    return {
        "systems": {
            "programbuild": {},
            "userjourney": {},
        },
        "workflow_state": {
            "programbuild": {"state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json"},
            "userjourney": {"state_file": "USERJOURNEY/USERJOURNEY_STATE.json"},
        },
    }


def test_create_backup_copies_state_files_and_manifest(tmp_path: Path, monkeypatch) -> None:
    registry = _registry_with_states(tmp_path)
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(programstart_backup, "git_commit_hash", lambda: "abc123")
    monkeypatch.setattr(programstart_backup, "git_changed_files", lambda: ["scripts/programstart_backup.py"])

    destination = programstart_backup.create_backup(registry, label="phase-i")

    assert destination.name.endswith("phase-i")
    assert (destination / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json").exists()
    assert (destination / "USERJOURNEY" / "USERJOURNEY_STATE.json").exists()

    manifest = (destination / "MANIFEST.txt").read_text(encoding="utf-8")
    assert "Git commit: abc123" in manifest
    assert "- PROGRAMBUILD/PROGRAMBUILD_STATE.json" in manifest
    assert "- USERJOURNEY/USERJOURNEY_STATE.json" in manifest
    assert "- scripts/programstart_backup.py" in manifest


def test_create_backup_uses_label_in_directory_name(tmp_path: Path, monkeypatch) -> None:
    registry = _registry_with_states(tmp_path)
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(programstart_backup, "git_commit_hash", lambda: "abc123")
    monkeypatch.setattr(programstart_backup, "git_changed_files", lambda: [])

    destination = programstart_backup.create_backup(registry, label="Test Phase I")

    assert destination.name.endswith("test-phase-i")


def test_backup_main_create_dispatches(capsys, monkeypatch, tmp_path: Path) -> None:
    registry = _registry_with_states(tmp_path)
    monkeypatch.setattr(programstart_backup, "load_registry", lambda: registry)
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(programstart_backup, "git_commit_hash", lambda: "abc123")
    monkeypatch.setattr(programstart_backup, "git_changed_files", lambda: [])

    result = programstart_backup.main(["create", "--label", "phase-i"])

    out = capsys.readouterr().out
    assert result == 0
    assert "Backup created:" in out