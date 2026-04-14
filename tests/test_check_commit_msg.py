"""Tests for scripts/check_commit_msg.py — Conventional Commits validation."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_commit_msg import main, validate


# ── validate ───────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "msg",
    [
        "feat: add new feature",
        "fix(schema): correct field type",
        "docs: update README",
        "chore: bump dependencies",
        "ci: add lint step",
        "refactor(cli): simplify parser",
        "test: add coverage for validate",
        "feat!: breaking change without scope",
        "feat(schema)!: breaking change with scope",
    ],
    ids=[
        "feat",
        "fix-with-scope",
        "docs",
        "chore",
        "ci",
        "refactor-with-scope",
        "test",
        "breaking-no-scope",
        "breaking-with-scope",
    ],
)
def test_validate_valid_messages(msg: str) -> None:
    assert validate(msg) == []


@pytest.mark.parametrize(
    "msg",
    [
        "Merge branch 'main'",
        "WIP: work in progress",
        "Revert \"feat: something\"",
        "chore(release): v1.0.0",
    ],
    ids=["merge", "wip", "revert", "release"],
)
def test_validate_exempt_messages(msg: str) -> None:
    assert validate(msg) == []


def test_validate_empty_message() -> None:
    errors = validate("")
    assert len(errors) == 1
    assert "empty" in errors[0].lower()


def test_validate_bad_type() -> None:
    errors = validate("yolo: did stuff")
    assert len(errors) >= 1
    assert "Conventional Commits" in errors[0]


def test_validate_missing_colon() -> None:
    errors = validate("feat add feature")
    assert len(errors) >= 1


def test_validate_subject_too_long() -> None:
    long_subject = "feat: " + "x" * 100
    errors = validate(long_subject)
    assert any("too long" in e for e in errors)


def test_validate_body_line_too_long() -> None:
    msg = "feat: short subject\n\n" + "y" * 130
    errors = validate(msg)
    assert any("Body line" in e for e in errors)


def test_validate_body_lines_ok() -> None:
    msg = "feat: short subject\n\nThis is a normal body line."
    assert validate(msg) == []


# ── main ───────────────────────────────────────────────────────────────────────


def test_main_no_args(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["check_commit_msg.py"])
    assert main() == 1


def test_main_missing_file(monkeypatch, tmp_path) -> None:
    fake = tmp_path / "nonexistent"
    monkeypatch.setattr("sys.argv", ["check_commit_msg.py", str(fake)])
    assert main() == 1


def test_main_valid_message(monkeypatch, tmp_path) -> None:
    msg_file = tmp_path / "COMMIT_EDITMSG"
    msg_file.write_text("feat: add new feature\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["check_commit_msg.py", str(msg_file)])
    assert main() == 0


def test_main_invalid_message(monkeypatch, tmp_path) -> None:
    msg_file = tmp_path / "COMMIT_EDITMSG"
    msg_file.write_text("bad commit\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["check_commit_msg.py", str(msg_file)])
    assert main() == 1
