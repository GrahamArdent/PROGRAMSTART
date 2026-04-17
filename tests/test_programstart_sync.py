from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_attach as attach
from scripts import programstart_sync as sync

# ── helpers ────────────────────────────────────────────────────────────────────


def _write_manifest(dest: Path, files: list[str]) -> None:
    manifest = {
        "programstart_version": "0.9.0",
        "source_commit": "abc123",
        "attached_at": "2026-04-17T00:00:00+00:00",
        "files": files,
    }
    dest.mkdir(parents=True, exist_ok=True)
    (dest / attach.MANIFEST_FILENAME).write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def _make_template_and_dest(
    tmp_path: Path,
    files: dict[str, str],
    *,
    dest_overrides: dict[str, str] | None = None,
) -> tuple[Path, Path]:
    """Create template and destination with matching files. Return (template, dest)."""
    template = tmp_path / "template"
    dest = tmp_path / "dest"
    for relative_path, content in files.items():
        (template / relative_path).parent.mkdir(parents=True, exist_ok=True)
        (template / relative_path).write_text(content, encoding="utf-8")
        (dest / relative_path).parent.mkdir(parents=True, exist_ok=True)
        (dest / relative_path).write_text(content, encoding="utf-8")
    if dest_overrides:
        for relative_path, content in dest_overrides.items():
            (dest / relative_path).parent.mkdir(parents=True, exist_ok=True)
            (dest / relative_path).write_text(content, encoding="utf-8")
    _write_manifest(dest, list(files.keys()))
    return template, dest


# ── manifest tests ─────────────────────────────────────────────────────────────


class TestManifest:
    def test_attach_writes_manifest(self, tmp_path: Path) -> None:
        template = tmp_path / "template"
        (template / "PROGRAMBUILD").mkdir(parents=True, exist_ok=True)
        (template / "config").mkdir(parents=True, exist_ok=True)
        (template / "PROGRAMBUILD" / "PROGRAMBUILD.md").write_text("# PB\n", encoding="utf-8")
        (template / "README.md").write_text("readme\n", encoding="utf-8")
        (template / "pyproject.toml").write_text("[project]\nname='test'\n", encoding="utf-8")
        (template / "config" / "process-registry.json").write_text("{}\n", encoding="utf-8")

        registry = {
            "workspace": {
                "bootstrap_assets": [
                    "README.md",
                    "pyproject.toml",
                    "config/process-registry.json",
                ]
            },
            "systems": {
                "programbuild": {
                    "control_files": ["PROGRAMBUILD/PROGRAMBUILD.md"],
                    "output_files": [],
                }
            },
            "workflow_state": {
                "programbuild": {
                    "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                    "active_key": "current_stage",
                    "initial_step": "inputs_and_mode_selection",
                    "step_order": ["inputs_and_mode_selection"],
                }
            },
        }

        destination = tmp_path / "dest"
        destination.mkdir()
        with (
            patch.object(attach, "load_registry", return_value=registry),
            patch.object(
                attach,
                "workspace_path",
                side_effect=lambda relative: template if relative == "." else template / relative,
            ),
            patch.object(attach, "create_default_workflow_state", return_value={"stage": "inputs_and_mode_selection"}),
            patch.object(attach, "stamp_bootstrapped_registry"),
            patch.object(attach, "sanitize_bootstrapped_secrets_baseline"),
            patch.object(attach, "refresh_secrets_baseline"),
        ):
            attach.attach_programbuild(destination, project_name="TestProject")

        manifest_path = destination / attach.MANIFEST_FILENAME
        assert manifest_path.exists()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert "files" in manifest
        assert "attached_at" in manifest
        assert "programstart_version" in manifest
        assert "README.md" in manifest["files"]
        assert "pyproject.toml" in manifest["files"]

    def test_attach_dry_run_does_not_write_manifest(self, tmp_path: Path) -> None:
        template = tmp_path / "template"
        (template / "PROGRAMBUILD").mkdir(parents=True, exist_ok=True)
        (template / "README.md").write_text("readme\n", encoding="utf-8")

        registry = {
            "workspace": {"bootstrap_assets": ["README.md"]},
            "systems": {"programbuild": {"control_files": [], "output_files": []}},
            "workflow_state": {
                "programbuild": {
                    "state_file": "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
                    "active_key": "current_stage",
                    "initial_step": "inputs_and_mode_selection",
                    "step_order": ["inputs_and_mode_selection"],
                }
            },
        }

        destination = tmp_path / "dest"
        destination.mkdir()
        with (
            patch.object(attach, "load_registry", return_value=registry),
            patch.object(
                attach,
                "workspace_path",
                side_effect=lambda relative: template if relative == "." else template / relative,
            ),
        ):
            attach.attach_programbuild(destination, project_name="TestProject", dry_run=True)

        assert not (destination / attach.MANIFEST_FILENAME).exists()


# ── sync: no changes ──────────────────────────────────────────────────────────


class TestSyncNoChanges:
    def test_sync_up_to_date(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/process-registry.json": "{}", "scripts/programstart_cli.py": "code"}
        template, dest = _make_template_and_dest(tmp_path, files)
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.sync(dest)
        assert result == 0
        assert "up to date" in capsys.readouterr().out.lower()


# ── sync: changed files ───────────────────────────────────────────────────────


class TestSyncChangedFiles:
    def test_sync_dry_run_shows_changes(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/process-registry.json": "{}"}
        template, dest = _make_template_and_dest(tmp_path, files, dest_overrides={"config/process-registry.json": "old"})
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.sync(dest)
        assert result == 0
        output = capsys.readouterr().out
        assert "config/process-registry.json" in output
        assert "Dry-run" in output
        # File should NOT have been changed
        assert (dest / "config/process-registry.json").read_text(encoding="utf-8") == "old"

    def test_sync_confirm_copies_changed_files(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/process-registry.json": "new content"}
        template, dest = _make_template_and_dest(tmp_path, files, dest_overrides={"config/process-registry.json": "old"})
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.sync(dest, confirm=True)
        assert result == 0
        assert (dest / "config/process-registry.json").read_text(encoding="utf-8") == "new content"
        output = capsys.readouterr().out
        assert "SYNC" in output

    def test_sync_missing_in_dest_is_reported(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/process-registry.json": "{}"}
        template, dest = _make_template_and_dest(tmp_path, files)
        (dest / "config/process-registry.json").unlink()
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.sync(dest, confirm=True)
        assert result == 0
        assert (dest / "config/process-registry.json").exists()


# ── sync: preserve list ───────────────────────────────────────────────────────


class TestSyncPreserve:
    def test_sync_skips_preserved_files(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"README.md": "template readme", "config/reg.json": "new"}
        template, dest = _make_template_and_dest(
            tmp_path, files, dest_overrides={"README.md": "host readme", "config/reg.json": "old"}
        )
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.sync(dest, confirm=True)
        assert result == 0
        assert (dest / "README.md").read_text(encoding="utf-8") == "host readme"
        assert (dest / "config/reg.json").read_text(encoding="utf-8") == "new"

    def test_custom_preserve_file_is_respected(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/reg.json": "new", "scripts/custom.py": "new"}
        template, dest = _make_template_and_dest(
            tmp_path,
            files,
            dest_overrides={"config/reg.json": "old", "scripts/custom.py": "old"},
        )
        (dest / ".programstart-preserve").write_text("scripts/custom.py\n", encoding="utf-8")
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.sync(dest, confirm=True)
        assert result == 0
        assert (dest / "scripts/custom.py").read_text(encoding="utf-8") == "old"
        assert (dest / "config/reg.json").read_text(encoding="utf-8") == "new"


# ── sync: file filter ─────────────────────────────────────────────────────────


class TestSyncFilter:
    def test_file_filter_limits_scope(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/reg.json": "new", "scripts/cli.py": "new"}
        template, dest = _make_template_and_dest(
            tmp_path,
            files,
            dest_overrides={"config/reg.json": "old", "scripts/cli.py": "old"},
        )
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.sync(dest, confirm=True, file_filter="config/*")
        assert result == 0
        assert (dest / "config/reg.json").read_text(encoding="utf-8") == "new"
        assert (dest / "scripts/cli.py").read_text(encoding="utf-8") == "old"


# ── sync: missing manifest ────────────────────────────────────────────────────


class TestSyncMissingManifest:
    def test_sync_fails_without_manifest(self, tmp_path: Path) -> None:
        dest = tmp_path / "dest"
        dest.mkdir()
        with pytest.raises(SystemExit):
            sync.sync(dest)


# ── sync: removed from template ──────────────────────────────────────────────


class TestSyncRemovedFromTemplate:
    def test_sync_reports_removed_files(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/reg.json": "content"}
        template, dest = _make_template_and_dest(tmp_path, files)
        # Remove from template
        (template / "config/reg.json").unlink()
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.sync(dest, confirm=True)
        assert result == 0
        output = capsys.readouterr().out
        assert "removed-from-template" in output
        assert "SKIP" in output


# ── main CLI entry point ──────────────────────────────────────────────────────


class TestSyncMain:
    def test_main_dry_run(self, tmp_path: Path) -> None:
        files = {"config/reg.json": "content"}
        template, dest = _make_template_and_dest(tmp_path, files)
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.main(["--dest", str(dest)])
        assert result == 0

    def test_main_nonexistent_dest(self, tmp_path: Path) -> None:
        result = sync.main(["--dest", str(tmp_path / "nope")])
        assert result == 1

    def test_main_no_dest_no_from_template_exits(self) -> None:
        with pytest.raises(SystemExit):
            sync.main([])


# ── sync: --from-template (pull mode) ────────────────────────────────────────


class TestSyncFromTemplate:
    def test_from_template_dry_run(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/reg.json": "new content"}
        template, dest = _make_template_and_dest(tmp_path, files, dest_overrides={"config/reg.json": "old"})
        result = sync.sync(dest, template_root=template)
        assert result == 0
        output = capsys.readouterr().out
        assert "config/reg.json" in output
        assert "Dry-run" in output
        # File unchanged in dry-run
        assert (dest / "config/reg.json").read_text(encoding="utf-8") == "old"

    def test_from_template_confirm_copies(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/reg.json": "updated"}
        template, dest = _make_template_and_dest(tmp_path, files, dest_overrides={"config/reg.json": "old"})
        result = sync.sync(dest, confirm=True, template_root=template)
        assert result == 0
        assert (dest / "config/reg.json").read_text(encoding="utf-8") == "updated"

    def test_from_template_up_to_date(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/reg.json": "same"}
        template, dest = _make_template_and_dest(tmp_path, files)
        result = sync.sync(dest, template_root=template)
        assert result == 0
        assert "up to date" in capsys.readouterr().out.lower()

    def test_from_template_preserves_protected(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"README.md": "new readme", "config/reg.json": "new"}
        template, dest = _make_template_and_dest(
            tmp_path, files, dest_overrides={"README.md": "local readme", "config/reg.json": "old"}
        )
        result = sync.sync(dest, confirm=True, template_root=template)
        assert result == 0
        # README.md is in PROGRAMBUILD_PRESERVE_EXISTING_FILES
        assert (dest / "README.md").read_text(encoding="utf-8") == "local readme"
        assert (dest / "config/reg.json").read_text(encoding="utf-8") == "new"

    def test_from_template_with_file_filter(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/reg.json": "new", "scripts/cli.py": "new"}
        template, dest = _make_template_and_dest(
            tmp_path, files, dest_overrides={"config/reg.json": "old", "scripts/cli.py": "old"}
        )
        result = sync.sync(dest, confirm=True, file_filter="config/*", template_root=template)
        assert result == 0
        assert (dest / "config/reg.json").read_text(encoding="utf-8") == "new"
        assert (dest / "scripts/cli.py").read_text(encoding="utf-8") == "old"


class TestSyncFromTemplateMain:
    def test_main_from_template_dry_run(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        files = {"config/reg.json": "new"}
        template, dest = _make_template_and_dest(tmp_path, files, dest_overrides={"config/reg.json": "old"})
        result = sync.main(["--from-template", str(template), "--dest", str(dest)])
        assert result == 0
        output = capsys.readouterr().out
        assert "config/reg.json" in output

    def test_main_from_template_defaults_dest_to_cwd(self, tmp_path: Path, monkeypatch, capsys: pytest.CaptureFixture) -> None:
        files = {"config/reg.json": "new"}
        template, dest = _make_template_and_dest(tmp_path, files, dest_overrides={"config/reg.json": "old"})
        monkeypatch.chdir(dest)
        result = sync.main(["--from-template", str(template)])
        assert result == 0
        output = capsys.readouterr().out
        assert "config/reg.json" in output

    def test_main_from_template_nonexistent_exits(self, tmp_path: Path) -> None:
        result = sync.main(["--from-template", str(tmp_path / "nope")])
        assert result == 1

    def test_main_from_template_confirm(self, tmp_path: Path) -> None:
        files = {"config/reg.json": "latest"}
        template, dest = _make_template_and_dest(tmp_path, files, dest_overrides={"config/reg.json": "old"})
        result = sync.main(["--from-template", str(template), "--dest", str(dest), "--confirm"])
        assert result == 0
        assert (dest / "config/reg.json").read_text(encoding="utf-8") == "latest"

    def test_main_confirm(self, tmp_path: Path) -> None:
        files = {"config/reg.json": "new"}
        template, dest = _make_template_and_dest(tmp_path, files, dest_overrides={"config/reg.json": "old"})
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.main(["--dest", str(dest), "--confirm"])
        assert result == 0
        assert (dest / "config/reg.json").read_text(encoding="utf-8") == "new"

    def test_main_file_filter(self, tmp_path: Path) -> None:
        files = {"config/reg.json": "new", "scripts/cli.py": "new"}
        template, dest = _make_template_and_dest(
            tmp_path,
            files,
            dest_overrides={"config/reg.json": "old", "scripts/cli.py": "old"},
        )
        with patch.object(sync, "workspace_path", return_value=template):
            result = sync.main(["--dest", str(dest), "--confirm", "--files", "config/*"])
        assert result == 0
        assert (dest / "config/reg.json").read_text(encoding="utf-8") == "new"
        assert (dest / "scripts/cli.py").read_text(encoding="utf-8") == "old"
