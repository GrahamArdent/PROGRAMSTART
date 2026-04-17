"""Tests for validate_research_complete."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.programstart_validate import validate_research_complete


@pytest.fixture()
def _patch_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()

    def _workspace_path(rel: str) -> Path:
        return tmp_path / rel

    monkeypatch.setattr("scripts.programstart_validate_core.workspace_path", _workspace_path)
    return pb


def test_missing_file(_patch_workspace: Path) -> None:
    problems = validate_research_complete({})
    assert any("does not exist" in p for p in problems)


def test_empty_file(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    (pb / "RESEARCH_SUMMARY.md").write_text("", encoding="utf-8")
    problems = validate_research_complete({})
    assert any("section headings" in p for p in problems)


def test_no_section_headings(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    (pb / "RESEARCH_SUMMARY.md").write_text(
        "# RESEARCH_SUMMARY\n\nSome prose with no section headings.\n",
        encoding="utf-8",
    )
    problems = validate_research_complete({})
    assert any("section headings" in p for p in problems)


def test_happy_path(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    (pb / "RESEARCH_SUMMARY.md").write_text(
        "# RESEARCH_SUMMARY\n\n## Key Findings\n\nResearch content here.\n",
        encoding="utf-8",
    )
    problems = validate_research_complete({})
    assert problems == []
