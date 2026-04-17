"""Tests for scripts/install_hooks.py (Phase F-3 — git hook installation)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.install_hooks import (
    _HOOK_NAMES,
    HOOKS_SOURCE_DIR,
    check_hooks,
    install_hooks,
    main,
    uninstall_hooks,
)


def test_hook_source_files_exist() -> None:
    """All declared hook names must have source files in scripts/hooks/."""
    for name in _HOOK_NAMES:
        source = HOOKS_SOURCE_DIR / name
        assert source.exists(), f"Hook source missing: {source}"


def test_install_hooks_creates_hook_file(tmp_path: Path, monkeypatch) -> None:
    """install_hooks() copies the hook source to the git hooks directory."""
    import scripts.install_hooks as install_hooks_mod

    fake_git_hooks = tmp_path / ".git" / "hooks"
    fake_git_hooks.mkdir(parents=True)
    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", fake_git_hooks)

    result = install_hooks()

    assert result == 0
    for name in _HOOK_NAMES:
        assert (fake_git_hooks / name).exists(), f"Hook not installed: {name}"


def test_install_hooks_dry_run_does_not_create_file(tmp_path: Path, monkeypatch, capsys) -> None:
    """install_hooks(dry_run=True) prints action but does not create files."""
    import scripts.install_hooks as install_hooks_mod

    fake_git_hooks = tmp_path / ".git" / "hooks"
    fake_git_hooks.mkdir(parents=True)
    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", fake_git_hooks)

    result = install_hooks(dry_run=True)

    assert result == 0
    for name in _HOOK_NAMES:
        assert not (fake_git_hooks / name).exists(), f"Dry-run should not create: {name}"
    out = capsys.readouterr().out
    assert "dry-run" in out.lower()


def test_uninstall_hooks_removes_hook_file(tmp_path: Path, monkeypatch) -> None:
    """uninstall_hooks() removes previously installed hooks."""
    import scripts.install_hooks as install_hooks_mod

    fake_git_hooks = tmp_path / ".git" / "hooks"
    fake_git_hooks.mkdir(parents=True)
    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", fake_git_hooks)

    # Pre-create the hook
    for name in _HOOK_NAMES:
        (fake_git_hooks / name).write_text("#!/bin/sh\n", encoding="utf-8")

    result = uninstall_hooks()

    assert result == 0
    for name in _HOOK_NAMES:
        assert not (fake_git_hooks / name).exists()


def test_check_hooks_returns_1_when_not_installed(tmp_path: Path, monkeypatch, capsys) -> None:
    """check_hooks() returns 1 when hooks are missing."""
    import scripts.install_hooks as install_hooks_mod

    fake_git_hooks = tmp_path / ".git" / "hooks"
    fake_git_hooks.mkdir(parents=True)
    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", fake_git_hooks)

    result = check_hooks()

    assert result == 1


def test_check_hooks_returns_0_when_installed(tmp_path: Path, monkeypatch) -> None:
    """check_hooks() returns 0 when all hooks are present."""
    import scripts.install_hooks as install_hooks_mod

    fake_git_hooks = tmp_path / ".git" / "hooks"
    fake_git_hooks.mkdir(parents=True)
    for name in _HOOK_NAMES:
        (fake_git_hooks / name).write_text("#!/bin/sh\n", encoding="utf-8")
    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", fake_git_hooks)

    result = check_hooks()

    assert result == 0


def test_install_hooks_missing_git_hooks_dir(tmp_path: Path, monkeypatch, capsys) -> None:
    """install_hooks() returns 1 when .git/hooks does not exist."""
    import scripts.install_hooks as install_hooks_mod

    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", tmp_path / "_no_such_dir")

    result = install_hooks()

    assert result == 1
    assert "ERROR" in capsys.readouterr().err


def test_main_install_creates_hooks(tmp_path: Path, monkeypatch) -> None:
    """main() with no flags installs hooks."""
    import scripts.install_hooks as install_hooks_mod

    fake_git_hooks = tmp_path / ".git" / "hooks"
    fake_git_hooks.mkdir(parents=True)
    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", fake_git_hooks)

    result = main([])

    assert result == 0
    for name in _HOOK_NAMES:
        assert (fake_git_hooks / name).exists()


def test_main_uninstall_removes_hooks(tmp_path: Path, monkeypatch) -> None:
    """main(--uninstall) removes hooks."""
    import scripts.install_hooks as install_hooks_mod

    fake_git_hooks = tmp_path / ".git" / "hooks"
    fake_git_hooks.mkdir(parents=True)
    for name in _HOOK_NAMES:
        (fake_git_hooks / name).write_text("#!/bin/sh\n", encoding="utf-8")
    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", fake_git_hooks)

    result = main(["--uninstall"])

    assert result == 0
    for name in _HOOK_NAMES:
        assert not (fake_git_hooks / name).exists()


def test_main_check_dispatches(tmp_path: Path, monkeypatch, capsys) -> None:
    """main(--check) dispatches to check_hooks."""
    import scripts.install_hooks as install_hooks_mod

    fake_git_hooks = tmp_path / ".git" / "hooks"
    fake_git_hooks.mkdir(parents=True)
    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", fake_git_hooks)

    result = main(["--check"])
    assert result == 1
    assert "not installed" in capsys.readouterr().err.lower()


def test_install_hooks_warns_when_source_missing(tmp_path: Path, monkeypatch, capsys) -> None:
    """Hook source file missing → prints warning and continues."""
    import scripts.install_hooks as install_hooks_mod

    fake_git_hooks = tmp_path / ".git" / "hooks"
    fake_git_hooks.mkdir(parents=True)
    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", fake_git_hooks)
    monkeypatch.setattr(install_hooks_mod, "HOOKS_SOURCE_DIR", tmp_path / "no-hooks")

    result = install_hooks()
    assert result == 0
    assert "WARNING" in capsys.readouterr().err


def test_uninstall_hooks_dry_run(tmp_path: Path, monkeypatch, capsys) -> None:
    """uninstall_hooks(dry_run=True) prints but does not remove."""
    import scripts.install_hooks as install_hooks_mod

    fake_git_hooks = tmp_path / ".git" / "hooks"
    fake_git_hooks.mkdir(parents=True)
    for name in _HOOK_NAMES:
        (fake_git_hooks / name).write_text("#!/bin/sh\n", encoding="utf-8")
    monkeypatch.setattr(install_hooks_mod, "GIT_HOOKS_DIR", fake_git_hooks)

    result = uninstall_hooks(dry_run=True)
    assert result == 0
    for name in _HOOK_NAMES:
        assert (fake_git_hooks / name).exists(), "Dry run should not remove hook"
    assert "dry-run" in capsys.readouterr().out.lower()


def test_make_executable_on_non_windows(tmp_path: Path, monkeypatch) -> None:
    """_make_executable calls chmod with execute bits on non-Windows."""
    import stat

    import scripts.install_hooks as install_hooks_mod

    hook_file = tmp_path / "my-hook"
    hook_file.write_text("#!/bin/sh\n", encoding="utf-8")
    monkeypatch.setattr(install_hooks_mod.sys, "platform", "linux")

    chmod_calls: list[int] = []

    class FakeStat:
        st_mode = 0o100644

    monkeypatch.setattr(type(hook_file), "stat", lambda self: FakeStat())
    monkeypatch.setattr(type(hook_file), "chmod", lambda self, m: chmod_calls.append(m))

    install_hooks_mod._make_executable(hook_file)

    assert len(chmod_calls) == 1
    assert chmod_calls[0] & stat.S_IXUSR
    assert chmod_calls[0] & stat.S_IXGRP
    assert chmod_calls[0] & stat.S_IXOTH
