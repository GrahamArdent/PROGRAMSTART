from __future__ import annotations

import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

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


# --- next_backup_destination suffix collision ---


def test_next_backup_destination_adds_suffix_when_dir_exists(tmp_path: Path) -> None:
    root = tmp_path / "BACKUPS"
    root.mkdir()
    fixed_time = datetime(2026, 4, 17, 12, 0, tzinfo=UTC)
    # Create the first candidate so we trigger the suffix loop
    first = root / "2026-04-17_my-label"
    first.mkdir()

    dest = programstart_backup.next_backup_destination(root, "my-label", current_time=fixed_time)
    assert dest.name == "2026-04-17_my-label_2"


def test_next_backup_destination_increments_suffix(tmp_path: Path) -> None:
    root = tmp_path / "BACKUPS"
    root.mkdir()
    fixed_time = datetime(2026, 4, 17, 12, 0, tzinfo=UTC)
    (root / "2026-04-17_dup").mkdir()
    (root / "2026-04-17_dup_2").mkdir()

    dest = programstart_backup.next_backup_destination(root, "dup", current_time=fixed_time)
    assert dest.name == "2026-04-17_dup_3"


# --- tracked_state_files edge cases ---


def test_tracked_state_files_skips_missing_state(tmp_path: Path, monkeypatch) -> None:
    """State file declared but not on disk → skipped."""
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(
        programstart_backup,
        "workflow_state_path",
        lambda reg, sys: tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json",
    )
    registry = {
        "systems": {"programbuild": {}},
        "workflow_state": {"programbuild": {"state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json"}},
    }
    # Don't create the state file
    assert programstart_backup.tracked_state_files(registry) == []


def test_tracked_state_files_skips_empty_state_file_path(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    registry = {
        "systems": {"programbuild": {}},
        "workflow_state": {"programbuild": {"state_file": ""}},
    }
    assert programstart_backup.tracked_state_files(registry) == []


# --- git_commit_hash / git_changed_files ---


def test_git_commit_hash_returns_unknown_on_failure(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    result = subprocess.CompletedProcess(args=[], returncode=128, stdout="", stderr="")
    with patch.object(subprocess, "run", return_value=result):
        assert programstart_backup.git_commit_hash() == "unknown"


def test_git_commit_hash_returns_unknown_on_empty_stdout(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    result = subprocess.CompletedProcess(args=[], returncode=0, stdout="  \n")
    with patch.object(subprocess, "run", return_value=result):
        assert programstart_backup.git_commit_hash() == "unknown"


def test_git_commit_hash_extracts_hash(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    fake_hash = "abc123def"  # pragma: allowlist secret
    result = subprocess.CompletedProcess(args=[], returncode=0, stdout=fake_hash + "\n")
    with patch.object(subprocess, "run", return_value=result):
        assert programstart_backup.git_commit_hash() == fake_hash


def test_git_changed_files_returns_empty_on_failure(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    result = subprocess.CompletedProcess(args=[], returncode=128, stdout="")
    with patch.object(subprocess, "run", return_value=result):
        assert programstart_backup.git_changed_files() == []


def test_git_changed_files_parses_short_status(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    result = subprocess.CompletedProcess(args=[], returncode=0, stdout="M  scripts/backup.py\n?? newfile.py\n")
    with patch.object(subprocess, "run", return_value=result):
        assert programstart_backup.git_changed_files() == ["scripts/backup.py", "newfile.py"]


def test_git_changed_files_skips_blank_lines(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    result = subprocess.CompletedProcess(args=[], returncode=0, stdout="\nM  a.py\n\n")
    with patch.object(subprocess, "run", return_value=result):
        assert programstart_backup.git_changed_files() == ["a.py"]


# --- write_manifest ---


def test_write_manifest_includes_no_changed_files(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(programstart_backup, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(programstart_backup, "git_commit_hash", lambda: "aaa")
    monkeypatch.setattr(programstart_backup, "git_changed_files", lambda: [])
    dest = tmp_path / "backup"
    dest.mkdir()
    copied = [dest / "a.json"]
    (dest / "a.json").write_text("{}", encoding="utf-8")

    path = programstart_backup.write_manifest(dest, created_at=datetime(2026, 4, 17, tzinfo=UTC), copied_files=copied)
    text = path.read_text(encoding="utf-8")
    assert "- none" in text


# --- sanitize_label edge cases ---


def test_sanitize_label_special_characters() -> None:
    assert programstart_backup.sanitize_label("Hello!@#World") == "helloworld"


def test_sanitize_label_empty_string() -> None:
    assert programstart_backup.sanitize_label("") == ""


def test_build_backup_dirname_no_label() -> None:
    fixed = datetime(2026, 4, 17, tzinfo=UTC)
    assert programstart_backup.build_backup_dirname("", current_time=fixed) == "2026-04-17"
