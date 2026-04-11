from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_attach as attach

# ── helpers ────────────────────────────────────────────────────────────────────


def make_valid_source(base: Path) -> Path:
    """Create a USERJOURNEY source directory with all required files."""
    source = base / "source_uj"
    source.mkdir(parents=True, exist_ok=True)
    for name in attach.REQUIRED_USERJOURNEY_FILES:
        (source / name).write_text(f"# {name}", encoding="utf-8")
    return source


# ── resolve_attachment_source ──────────────────────────────────────────────────


def test_resolve_source_accepts_direct_userjourney_dir(tmp_path: Path) -> None:
    uj = tmp_path / "USERJOURNEY"
    uj.mkdir()
    result = attach.resolve_attachment_source(str(uj))
    assert result == uj


def test_resolve_source_accepts_parent_with_nested_userjourney(tmp_path: Path) -> None:
    uj = tmp_path / "USERJOURNEY"
    uj.mkdir()
    result = attach.resolve_attachment_source(str(tmp_path))
    assert result == uj


def test_resolve_source_raises_for_nonexistent_path(tmp_path: Path) -> None:
    bad = tmp_path / "no_such_thing"
    with pytest.raises(FileNotFoundError):
        attach.resolve_attachment_source(str(bad))


def test_resolve_source_raises_when_no_userjourney_child(tmp_path: Path) -> None:
    (tmp_path / "OTHER").mkdir()
    with pytest.raises(FileNotFoundError):
        attach.resolve_attachment_source(str(tmp_path))


# ── validate_attachment_source ─────────────────────────────────────────────────


def test_validate_returns_empty_when_all_required_files_present(tmp_path: Path) -> None:
    for name in attach.REQUIRED_USERJOURNEY_FILES:
        (tmp_path / name).write_text("x", encoding="utf-8")
    assert attach.validate_attachment_source(tmp_path) == []


def test_validate_returns_missing_file_names(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    missing = attach.validate_attachment_source(tmp_path)
    assert "DELIVERY_GAMEPLAN.md" in missing
    assert "USERJOURNEY_TEMPLATE_STARTER.md" in missing


def test_validate_returns_all_files_when_directory_empty(tmp_path: Path) -> None:
    missing = attach.validate_attachment_source(tmp_path)
    assert set(missing) == attach.REQUIRED_USERJOURNEY_FILES


# ── attach_userjourney ─────────────────────────────────────────────────────────


def test_attach_dry_run_prints_without_copying(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    source = make_valid_source(tmp_path)
    dest_root = tmp_path / "dest"
    dest_root.mkdir()
    attach.attach_userjourney(dest_root, source, dry_run=True)
    captured = capsys.readouterr()
    assert "ATTACH USERJOURNEY" in captured.out
    assert not (dest_root / "USERJOURNEY").exists()


def test_attach_copies_required_files(tmp_path: Path) -> None:
    source = make_valid_source(tmp_path)
    dest_root = tmp_path / "dest"
    dest_root.mkdir()
    with (
        patch.object(attach, "load_registry", return_value={}),
        patch.object(attach, "create_default_workflow_state", return_value={"stage": "kickoff"}),
        patch.object(attach, "write_json"),
    ):
        attach.attach_userjourney(dest_root, source)
    for name in attach.REQUIRED_USERJOURNEY_FILES:
        assert (dest_root / "USERJOURNEY" / name).exists()


def test_attach_writes_state_json_when_missing(tmp_path: Path) -> None:
    source = make_valid_source(tmp_path)
    dest_root = tmp_path / "dest"
    dest_root.mkdir()
    written: list[tuple] = []
    with (
        patch.object(attach, "load_registry", return_value={}),
        patch.object(attach, "create_default_workflow_state", return_value={"stage": "kickoff"}),
        patch.object(attach, "write_json", side_effect=lambda p, d: written.append((p, d))),
    ):
        attach.attach_userjourney(dest_root, source)
    assert any("USERJOURNEY_STATE.json" in str(p) for p, _ in written)


def test_attach_raises_fileexistserror_without_force(tmp_path: Path) -> None:
    source = make_valid_source(tmp_path)
    dest_root = tmp_path / "dest"
    (dest_root / "USERJOURNEY").mkdir(parents=True)
    with pytest.raises(FileExistsError, match="--force"):
        attach.attach_userjourney(dest_root, source)


def test_attach_force_replaces_existing_destination(tmp_path: Path) -> None:
    source = make_valid_source(tmp_path)
    dest_root = tmp_path / "dest"
    dest_uj = dest_root / "USERJOURNEY"
    dest_uj.mkdir(parents=True)
    (dest_uj / "stale.md").write_text("old content", encoding="utf-8")
    with (
        patch.object(attach, "load_registry", return_value={}),
        patch.object(attach, "create_default_workflow_state", return_value={}),
        patch.object(attach, "write_json"),
    ):
        attach.attach_userjourney(dest_root, source, force=True)
    assert not (dest_uj / "stale.md").exists()
    assert (dest_uj / "README.md").exists()


def test_attach_raises_filenotfounderror_for_missing_required_source_files(tmp_path: Path) -> None:
    source = tmp_path / "bad_source"
    source.mkdir()
    dest_root = tmp_path / "dest"
    dest_root.mkdir()
    with pytest.raises(FileNotFoundError, match="required files"):
        attach.attach_userjourney(dest_root, source)


# ── main ───────────────────────────────────────────────────────────────────────


def test_main_returns_zero_on_success(tmp_path: Path) -> None:
    resolved = tmp_path / "USERJOURNEY"
    resolved.mkdir()
    ws = tmp_path / "ws"
    ws.mkdir()
    with (
        patch.object(attach, "resolve_attachment_source", return_value=resolved),
        patch.object(attach, "workspace_path", return_value=ws),
        patch.object(attach, "attach_userjourney") as mock_attach,
    ):
        result = attach.main(["userjourney", "--source", str(resolved)])
    assert result == 0
    mock_attach.assert_called_once()


def test_main_passes_dry_run_flag(tmp_path: Path) -> None:
    resolved = tmp_path / "USERJOURNEY"
    resolved.mkdir()
    ws = tmp_path / "ws"
    ws.mkdir()
    with (
        patch.object(attach, "resolve_attachment_source", return_value=resolved),
        patch.object(attach, "workspace_path", return_value=ws),
        patch.object(attach, "attach_userjourney") as mock_attach,
    ):
        result = attach.main(["userjourney", "--source", str(resolved), "--dry-run"])
    assert result == 0
    _, kwargs = mock_attach.call_args
    assert kwargs.get("dry_run") is True


def test_main_passes_force_flag(tmp_path: Path) -> None:
    resolved = tmp_path / "USERJOURNEY"
    resolved.mkdir()
    ws = tmp_path / "ws"
    ws.mkdir()
    with (
        patch.object(attach, "resolve_attachment_source", return_value=resolved),
        patch.object(attach, "workspace_path", return_value=ws),
        patch.object(attach, "attach_userjourney") as mock_attach,
    ):
        result = attach.main(["userjourney", "--source", str(resolved), "--force"])
    assert result == 0
    _, kwargs = mock_attach.call_args
    assert kwargs.get("force") is True
