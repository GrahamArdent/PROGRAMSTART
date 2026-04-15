"""Tests for scripts/programstart_doctor.py — environment health checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_doctor import (
    _check_git_repo,
    _check_playwright,
    _check_python_version,
    _check_registry_schema,
    _check_state_files,
    _check_tool_installed,
    main,
    run_checks,
)


class TestCheckPythonVersion:
    def test_passes_on_current_python(self) -> None:
        ok, msg = _check_python_version()
        # Running on Python 3.12+ so this must pass
        assert ok
        assert "Python" in msg

    def test_returns_version_string(self) -> None:
        ok, msg = _check_python_version()
        # Must contain a dotted version like 3.x.y
        import re

        assert re.search(r"\d+\.\d+\.\d+", msg)


class TestCheckToolInstalled:
    def test_tool_found_on_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("scripts.programstart_doctor.shutil.which", lambda name: "/usr/bin/uv")
        ok, msg = _check_tool_installed("uv")
        assert ok
        assert "uv" in msg
        assert "not found" not in msg

    def test_tool_not_found_on_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("scripts.programstart_doctor.shutil.which", lambda name: None)
        ok, msg = _check_tool_installed("missing-tool")
        assert not ok
        assert "not found on PATH" in msg


class TestCheckPlaywright:
    def test_playwright_not_on_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("scripts.programstart_doctor.shutil.which", lambda name: None)
        ok, msg = _check_playwright()
        assert not ok
        assert "playwright not found on PATH" in msg

    def test_playwright_version_ok(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "scripts.programstart_doctor.shutil.which",
            lambda name: "/usr/bin/playwright",
        )
        fake_result = SimpleNamespace(returncode=0, stdout="Version 1.40.0")
        monkeypatch.setattr(
            "scripts.programstart_doctor.subprocess.run",
            lambda *args, **kwargs: fake_result,
        )
        ok, msg = _check_playwright()
        assert ok
        assert "playwright" in msg

    def test_playwright_version_fails_nonzero(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "scripts.programstart_doctor.shutil.which",
            lambda name: "/usr/bin/playwright",
        )
        fake_result = SimpleNamespace(returncode=1, stdout="")
        monkeypatch.setattr(
            "scripts.programstart_doctor.subprocess.run",
            lambda *args, **kwargs: fake_result,
        )
        ok, msg = _check_playwright()
        assert not ok
        assert "version failed" in msg

    def test_playwright_version_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "scripts.programstart_doctor.shutil.which",
            lambda name: "/usr/bin/playwright",
        )

        def raise_timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired("playwright", 10)

        monkeypatch.setattr("scripts.programstart_doctor.subprocess.run", raise_timeout)
        ok, msg = _check_playwright()
        assert not ok
        assert "timed out" in msg

    def test_playwright_version_oserror(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "scripts.programstart_doctor.shutil.which",
            lambda name: "/usr/bin/playwright",
        )

        def raise_os(*args, **kwargs):
            raise OSError("no such file")

        monkeypatch.setattr("scripts.programstart_doctor.subprocess.run", raise_os)
        ok, msg = _check_playwright()
        assert not ok
        assert "timed out" in msg


class TestCheckGitRepo:
    def test_git_dir_present(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        monkeypatch.setattr("scripts.programstart_doctor.workspace_path", lambda name: tmp_path / name)
        ok, msg = _check_git_repo()
        assert ok
        assert "git repo" in msg

    def test_git_dir_missing(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setattr("scripts.programstart_doctor.workspace_path", lambda name: tmp_path / name)
        ok, msg = _check_git_repo()
        assert not ok
        assert "missing" in msg


class TestCheckRegistrySchema:
    def test_registry_not_found(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setattr("scripts.programstart_doctor.workspace_path", lambda name: tmp_path / name)
        ok, msg = _check_registry_schema()
        assert not ok
        assert "not found" in msg

    def test_schema_file_missing_skips_validation(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        registry = tmp_path / "config" / "process-registry.json"
        registry.parent.mkdir(parents=True)
        registry.write_text('{"version": "1"}', encoding="utf-8")
        monkeypatch.setattr("scripts.programstart_doctor.workspace_path", lambda name: tmp_path / name)
        ok, msg = _check_registry_schema()
        assert ok
        assert "schema file missing" in msg

    def test_valid_registry_json(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        registry = tmp_path / "config" / "process-registry.json"
        registry.parent.mkdir(parents=True)
        registry.write_text('{"version": "1"}', encoding="utf-8")
        schema = tmp_path / "schemas" / "process-registry.schema.json"
        schema.parent.mkdir(parents=True)
        schema.write_text('{"type": "object"}', encoding="utf-8")
        monkeypatch.setattr("scripts.programstart_doctor.workspace_path", lambda name: tmp_path / name)
        ok, msg = _check_registry_schema()
        assert ok
        assert "valid JSON" in msg

    def test_invalid_registry_json(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        registry = tmp_path / "config" / "process-registry.json"
        registry.parent.mkdir(parents=True)
        registry.write_text("not valid json {{{", encoding="utf-8")
        schema = tmp_path / "schemas" / "process-registry.schema.json"
        schema.parent.mkdir(parents=True)
        schema.write_text('{"type": "object"}', encoding="utf-8")
        monkeypatch.setattr("scripts.programstart_doctor.workspace_path", lambda name: tmp_path / name)
        ok, msg = _check_registry_schema()
        assert not ok
        assert "parse error" in msg


class TestCheckStateFiles:
    def test_state_file_missing(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setattr("scripts.programstart_doctor.workspace_path", lambda name: tmp_path / name)
        ok, msg = _check_state_files()
        assert not ok
        assert "missing" in msg

    def test_state_file_invalid_json(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        state = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json"
        state.parent.mkdir(parents=True)
        state.write_text("{invalid json", encoding="utf-8")
        monkeypatch.setattr("scripts.programstart_doctor.workspace_path", lambda name: tmp_path / name)
        ok, msg = _check_state_files()
        assert not ok

    def test_state_file_valid_json(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        state = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json"
        state.parent.mkdir(parents=True)
        state.write_text('{"stage": "feasibility"}', encoding="utf-8")
        monkeypatch.setattr("scripts.programstart_doctor.workspace_path", lambda name: tmp_path / name)
        ok, msg = _check_state_files()
        assert ok
        assert "valid JSON" in msg


class TestRunChecks:
    def test_returns_list_of_bool_str_tuples(self) -> None:
        results = run_checks()
        assert isinstance(results, list)
        assert len(results) > 0
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)

    def test_python_version_check_included(self) -> None:
        results = run_checks()
        messages = [msg for _, msg in results]
        assert any("Python" in msg for msg in messages)


class TestMain:
    def test_main_all_pass_returns_zero(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        monkeypatch.setattr(
            "scripts.programstart_doctor.run_checks",
            lambda: [(True, "check 1 ok"), (True, "check 2 ok")],
        )
        result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "All checks passed" in captured.out

    def test_main_some_fail_returns_one(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        monkeypatch.setattr(
            "scripts.programstart_doctor.run_checks",
            lambda: [(True, "ok"), (False, "something failed")],
        )
        result = main()
        assert result == 1
        captured = capsys.readouterr()
        assert "Some checks failed" in captured.out

    def test_main_prints_each_check(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        monkeypatch.setattr(
            "scripts.programstart_doctor.run_checks",
            lambda: [(True, "uv ok"), (False, "playwright not found on PATH")],
        )
        main()
        captured = capsys.readouterr()
        assert "uv ok" in captured.out
        assert "playwright not found on PATH" in captured.out
