"""Tests for Phase G new stage validators (Stages 5, 6, 7, 8, 9)."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.programstart_validate import (
    validate_audit_complete,
    validate_release_ready,
    validate_scaffold_complete,
    validate_test_strategy_complete,
)


@pytest.fixture()
def _patch_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()

    def _workspace_path(rel: str) -> Path:
        return tmp_path / rel

    monkeypatch.setattr("scripts.programstart_validate.workspace_path", _workspace_path)
    return pb


# ---------------------------------------------------------------------------
# validate_test_strategy_complete (Stage 6)
# ---------------------------------------------------------------------------


TEST_STRATEGY_HAPPY = """\
# TEST_STRATEGY.md

## Test Pyramid Targets

| Layer | Target | Notes |
|---|---|---|
| Unit | 400+ tests | Covers FR-001 and FR-002 |

## Other Section

Content here.
"""


def test_test_strategy_missing_file(_patch_workspace: Path) -> None:
    problems = validate_test_strategy_complete({})
    assert any("does not exist" in p for p in problems)


def test_test_strategy_no_categories(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = "# TEST_STRATEGY.md\n\n## Test Pyramid Targets\n\n| Layer | Target | Notes |\n|---|---|---|\n"
    (pb / "TEST_STRATEGY.md").write_text(text, encoding="utf-8")
    problems = validate_test_strategy_complete({})
    assert any("no test categories" in p for p in problems)


def test_test_strategy_no_requirement_refs(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = "# TEST_STRATEGY.md\n\n## Test Pyramid Targets\n\n| Layer | Target | Notes |\n|---|---|---|\n| Unit | Tests | No reqs listed |\n"
    (pb / "TEST_STRATEGY.md").write_text(text, encoding="utf-8")
    problems = validate_test_strategy_complete({})
    assert any("requirement IDs" in p for p in problems)


def test_test_strategy_happy_path(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    (pb / "TEST_STRATEGY.md").write_text(TEST_STRATEGY_HAPPY, encoding="utf-8")
    problems = validate_test_strategy_complete({})
    assert problems == []


# ---------------------------------------------------------------------------
# validate_scaffold_complete (Stage 5)
# ---------------------------------------------------------------------------


def test_scaffold_no_project_config(_patch_workspace: Path, tmp_path: Path) -> None:
    # No pyproject.toml or equivalent at tmp_path root
    problems = validate_scaffold_complete({})
    assert any("project configuration" in p for p in problems)


def test_scaffold_no_ci(_patch_workspace: Path, tmp_path: Path) -> None:
    # Create pyproject.toml but no CI
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'", encoding="utf-8")
    problems = validate_scaffold_complete({})
    assert any("CI configuration" in p for p in problems)


def test_scaffold_happy_path(_patch_workspace: Path, tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'", encoding="utf-8")
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("name: CI", encoding="utf-8")
    problems = validate_scaffold_complete({})
    assert problems == []


# ---------------------------------------------------------------------------
# validate_release_ready (Stage 8)
# ---------------------------------------------------------------------------


def test_release_ready_missing_file(_patch_workspace: Path) -> None:
    problems = validate_release_ready({})
    assert any("does not exist" in p for p in problems)


def test_release_ready_empty_decision(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = "# RELEASE_READINESS.md\n\n## Go / No-Go Decision\n\nDecision:\n"
    (pb / "RELEASE_READINESS.md").write_text(text, encoding="utf-8")
    problems = validate_release_ready({})
    assert any("empty" in p for p in problems)


def test_release_ready_no_keyword(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = "# RELEASE_READINESS.md\n\n## Go / No-Go Decision\n\nWe reviewed the checklist.\n"
    (pb / "RELEASE_READINESS.md").write_text(text, encoding="utf-8")
    problems = validate_release_ready({})
    assert any("clear decision keyword" in p for p in problems)


def test_release_ready_happy_path(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = "# RELEASE_READINESS.md\n\n## Go / No-Go Decision\n\nDecision: go — all checks passed.\n"
    (pb / "RELEASE_READINESS.md").write_text(text, encoding="utf-8")
    problems = validate_release_ready({})
    assert problems == []


# ---------------------------------------------------------------------------
# validate_audit_complete (Stage 9)
# ---------------------------------------------------------------------------

AUDIT_HEADER = """\
# AUDIT_REPORT.md

## Findings

| Severity | Category | Finding | Evidence | Impact | Minimum fix |
|---|---|---|---|---|---|
"""


def test_audit_missing_file(_patch_workspace: Path) -> None:
    problems = validate_audit_complete({})
    assert any("does not exist" in p for p in problems)


def test_audit_no_findings(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    (pb / "AUDIT_REPORT.md").write_text(AUDIT_HEADER, encoding="utf-8")
    problems = validate_audit_complete({})
    assert any("no entries" in p for p in problems)


def test_audit_happy_path(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = AUDIT_HEADER + "| Low | Docs | Missing docstring | f.py:10 | Minor | Add docstring |\n"
    (pb / "AUDIT_REPORT.md").write_text(text, encoding="utf-8")
    problems = validate_audit_complete({})
    assert problems == []
