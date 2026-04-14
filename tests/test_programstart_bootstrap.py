from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_bootstrap as bootstrap

# ── helpers ────────────────────────────────────────────────────────────────────


def _minimal_registry(tmp_path: Path) -> dict:
    return {
        "systems": {
            "programbuild": {
                "control_files": ["PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md"],
                "output_files": [],
                "metadata_required": [],
            },
        },
        "workflow_state": {
            "programbuild": {
                "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                "valid_statuses": ["planned", "in_progress", "completed", "blocked"],
            },
        },
        "workspace": {
            "bootstrap_assets": [],
        },
    }


# ── write_file ─────────────────────────────────────────────────────────────────


def test_write_file_dry_run_prints_create(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    target = tmp_path / "sub" / "file.txt"
    bootstrap.write_file(target, "hello", dry_run=True)
    captured = capsys.readouterr()
    assert "CREATE" in captured.out
    assert not target.exists()


def test_write_file_creates_file_with_content(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "file.txt"
    bootstrap.write_file(target, "hello world", dry_run=False)
    assert target.read_text(encoding="utf-8") == "hello world"


# ── copy_file ──────────────────────────────────────────────────────────────────


def test_copy_file_dry_run_prints_copy(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    src = tmp_path / "source.md"
    src.write_text("content", encoding="utf-8")
    dst = tmp_path / "out" / "dest.md"
    bootstrap.copy_file(src, dst, dry_run=True)
    captured = capsys.readouterr()
    assert "COPY" in captured.out
    assert not dst.exists()


def test_copy_file_copies_text_content(tmp_path: Path) -> None:
    src = tmp_path / "source.md"
    src.write_text("# Hello", encoding="utf-8")
    dst = tmp_path / "out" / "dest.md"
    bootstrap.copy_file(src, dst, dry_run=False)
    assert dst.read_text(encoding="utf-8") == "# Hello"


# ── ensure_external_project_repo ──────────────────────────────────────────────


def test_ensure_external_raises_when_dest_inside_template(tmp_path: Path) -> None:
    nested = tmp_path / "nested_project"
    nested.mkdir()
    with patch.object(bootstrap, "workspace_path", return_value=tmp_path):
        with pytest.raises(ValueError, match="outside"):
            bootstrap.ensure_external_project_repo(nested)


def test_ensure_external_passes_when_dest_is_sibling(tmp_path: Path) -> None:
    template = tmp_path / "PROGRAMSTART"
    template.mkdir()
    sibling = tmp_path / "my_new_project"
    sibling.mkdir()
    with patch.object(bootstrap, "workspace_path", return_value=template):
        bootstrap.ensure_external_project_repo(sibling)  # should not raise


# ── stamp_bootstrapped_registry ───────────────────────────────────────────────


def test_stamp_bootstrapped_registry_dry_run_prints(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    bootstrap.stamp_bootstrapped_registry(tmp_path, project_name="my-app", dry_run=True)
    captured = capsys.readouterr()
    assert "STAMP" in captured.out


def test_stamp_bootstrapped_registry_writes_correct_fields(tmp_path: Path) -> None:
    config = tmp_path / "config"
    config.mkdir()
    registry_path = config / "process-registry.json"
    registry_path.write_text(json.dumps({"workspace": {}, "validation": {}, "integrity": {}}), encoding="utf-8")
    bootstrap.stamp_bootstrapped_registry(tmp_path, project_name="acme", dry_run=False)
    result = json.loads(registry_path.read_text(encoding="utf-8"))
    assert result["workspace"]["repo_role"] == "project_repo"
    assert result["workspace"]["project_name"] == "acme"
    assert result["workspace"]["source_template_repo"] == "PROGRAMSTART"
    assert result["validation"]["enforce_engineering_ready_in_all"] is True


# ── sanitize_bootstrapped_secrets_baseline ────────────────────────────────────


def test_sanitize_removes_registry_from_baseline(tmp_path: Path) -> None:
    baseline = {"results": {"config/process-registry.json": ["secret"], "other.py": ["hit"]}}
    baseline_path = tmp_path / ".secrets.baseline"
    baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
    bootstrap.sanitize_bootstrapped_secrets_baseline(tmp_path, dry_run=False)
    result = json.loads(baseline_path.read_text(encoding="utf-8"))
    assert "config/process-registry.json" not in result["results"]
    assert "other.py" in result["results"]


def test_sanitize_no_op_when_baseline_missing(tmp_path: Path) -> None:
    # Should not raise when baseline does not exist
    bootstrap.sanitize_bootstrapped_secrets_baseline(tmp_path, dry_run=False)


def test_sanitize_dry_run_skips_file(tmp_path: Path) -> None:
    baseline = {"results": {"config/process-registry.json": ["secret"]}}
    baseline_path = tmp_path / ".secrets.baseline"
    baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
    bootstrap.sanitize_bootstrapped_secrets_baseline(tmp_path, dry_run=True)
    # File should be unchanged in dry_run mode
    result = json.loads(baseline_path.read_text(encoding="utf-8"))
    assert "config/process-registry.json" in result["results"]


# ── write_bootstrap_readme ─────────────────────────────────────────────────────


def test_write_bootstrap_readme_contains_project_name(tmp_path: Path) -> None:
    bootstrap.write_bootstrap_readme(tmp_path, "FancyProject", "product", dry_run=False)
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "FancyProject" in readme


def test_write_bootstrap_readme_contains_variant(tmp_path: Path) -> None:
    bootstrap.write_bootstrap_readme(tmp_path, "MyApp", "enterprise", dry_run=False)
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "enterprise" in readme


def test_write_bootstrap_readme_dry_run_prints_without_creating(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    bootstrap.write_bootstrap_readme(tmp_path, "DryRunProject", "lite", dry_run=True)
    captured = capsys.readouterr()
    assert "CREATE" in captured.out
    assert not (tmp_path / "README.md").exists()


# ── bootstrap_repository (error paths) ────────────────────────────────────────


def test_bootstrap_repository_raises_on_nonempty_dest_without_force(tmp_path: Path) -> None:
    dest = tmp_path / "dest"
    dest.mkdir()
    (dest / "existing_file.txt").write_text("x", encoding="utf-8")
    template = tmp_path / "template"
    template.mkdir()
    with patch.object(bootstrap, "workspace_path", return_value=template):
        with pytest.raises(FileExistsError, match="--force"):
            bootstrap.bootstrap_repository(dest, project_name="test", variant="product")


def test_bootstrap_repository_raises_when_dest_inside_template(tmp_path: Path) -> None:
    with patch.object(bootstrap, "workspace_path", return_value=tmp_path):
        with pytest.raises(ValueError, match="outside"):
            bootstrap.bootstrap_repository(
                tmp_path / "nested",
                project_name="test",
                variant="product",
            )


# ── main ───────────────────────────────────────────────────────────────────────


def test_main_returns_one_on_fileexistserror(tmp_path: Path) -> None:
    import sys as _sys

    dest = tmp_path / "dest"
    dest.mkdir()
    (dest / "existing.txt").write_text("x")
    template = tmp_path / "template"
    template.mkdir()
    argv = ["programstart", "--dest", str(dest), "--project-name", "test", "--variant", "product"]
    with (
        patch.object(bootstrap, "workspace_path", return_value=template),
        patch.object(_sys, "argv", argv),
    ):
        result = bootstrap.main()
    assert result == 1


def test_main_dry_run_delegates_to_bootstrap_repository(tmp_path: Path) -> None:
    import sys as _sys

    dest = tmp_path / "new_project"
    argv = ["programstart", "--dest", str(dest), "--project-name", "alpha", "--variant", "lite", "--dry-run"]
    with (
        patch.object(_sys, "argv", argv),
        patch.object(bootstrap, "bootstrap_repository") as mock_bootstrap,
    ):
        bootstrap.main()
    mock_bootstrap.assert_called_once()
    _, kwargs = mock_bootstrap.call_args
    assert kwargs.get("dry_run") is True
    assert kwargs.get("project_name") == "alpha"
    assert kwargs.get("variant") == "lite"


# ── migrated from test_audit_fixes.py ──────────────────────────────────────────


def test_stamp_bootstrapped_registry_raises_on_malformed_json(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    registry_path = config_dir / "process-registry.json"
    registry_path.write_text("NOT VALID JSON {{{", encoding="utf-8")

    try:
        bootstrap.stamp_bootstrapped_registry(tmp_path, project_name="test", dry_run=False)
        assert False, "Should have raised ValueError"
    except ValueError as exc:
        assert "Cannot parse bootstrapped registry" in str(exc)
        assert "process-registry.json" in str(exc)


def test_sanitize_secrets_baseline_raises_on_malformed_json(tmp_path: Path) -> None:
    baseline_path = tmp_path / ".secrets.baseline"
    baseline_path.write_text("{broken json!!!", encoding="utf-8")

    try:
        bootstrap.sanitize_bootstrapped_secrets_baseline(tmp_path, dry_run=False)
        assert False, "Should have raised ValueError"
    except ValueError as exc:
        assert "Cannot parse secrets baseline" in str(exc)
        assert ".secrets.baseline" in str(exc)


def test_stamp_bootstrapped_registry_dry_run_skips_parsing(tmp_path: Path, capsys) -> None:
    """Dry run should print the stamp line without reading the file at all."""
    bootstrap.stamp_bootstrapped_registry(tmp_path, project_name="test", dry_run=True)
    out = capsys.readouterr().out
    assert "STAMP" in out
