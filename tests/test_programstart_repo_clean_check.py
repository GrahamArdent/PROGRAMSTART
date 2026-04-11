from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_repo_clean_check import (
    assert_repo_clean,
    assert_repo_unchanged,
    capture_git_status,
    main,
)


def _fake_git_status(stdout: str):
    """Return a mock CompletedProcess for ``git status --porcelain``."""
    return subprocess.CompletedProcess(args=["git", "status", "--porcelain"], returncode=0, stdout=stdout, stderr="")


class TestCaptureGitStatus:
    def test_clean_repo(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "scripts.programstart_repo_clean_check.subprocess.run",
            lambda *a, **kw: _fake_git_status(""),
        )
        assert capture_git_status() == set()

    def test_dirty_repo(self, monkeypatch: pytest.MonkeyPatch) -> None:
        porcelain = " M file1.py\n?? newfile.txt\n M dir/file2.md\n"
        monkeypatch.setattr(
            "scripts.programstart_repo_clean_check.subprocess.run",
            lambda *a, **kw: _fake_git_status(porcelain),
        )
        result = capture_git_status()
        assert result == {"file1.py", "newfile.txt", "dir/file2.md"}

    def test_passes_repo_path_as_cwd(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        calls: list[dict] = []

        def _record(*args, **kwargs):
            calls.append(kwargs)
            return _fake_git_status("")

        monkeypatch.setattr("scripts.programstart_repo_clean_check.subprocess.run", _record)
        capture_git_status(tmp_path)
        assert calls[0]["cwd"] == str(tmp_path)


class TestAssertRepoClean:
    def test_passes_when_clean(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "scripts.programstart_repo_clean_check.capture_git_status",
            lambda repo=None: set(),
        )
        assert_repo_clean("test")  # should not raise

    def test_fails_when_dirty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "scripts.programstart_repo_clean_check.capture_git_status",
            lambda repo=None: {"dirty.txt"},
        )
        with pytest.raises(SystemExit, match="1"):
            assert_repo_clean("test")


class TestAssertRepoUnchanged:
    def test_passes_when_same(self) -> None:
        before = {"a.py", "b.py"}
        after = {"a.py", "b.py"}
        assert_repo_unchanged(before, after, "test")  # should not raise

    def test_passes_when_files_removed(self) -> None:
        before = {"a.py", "b.py"}
        after = {"a.py"}
        assert_repo_unchanged(before, after, "test")  # removals are OK

    def test_fails_when_new_files_appear(self) -> None:
        before = {"a.py"}
        after = {"a.py", "new.txt"}
        with pytest.raises(SystemExit, match="1"):
            assert_repo_unchanged(before, after, "test")


class TestMain:
    def test_clean(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        monkeypatch.setattr(
            "scripts.programstart_repo_clean_check.capture_git_status",
            lambda repo=None: set(),
        )
        assert main() == 0
        assert "clean" in capsys.readouterr().out.lower()

    def test_dirty(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        monkeypatch.setattr(
            "scripts.programstart_repo_clean_check.capture_git_status",
            lambda repo=None: {"dirty.txt"},
        )
        assert main() == 1
        assert "dirty" in capsys.readouterr().out.lower()
