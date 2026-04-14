"""Tests for _check_decision_log_entries helper."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.programstart_validate import _check_decision_log_entries


@pytest.fixture()
def _patch_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()

    def _workspace_path(rel: str) -> Path:
        return tmp_path / rel

    monkeypatch.setattr("scripts.programstart_validate.workspace_path", _workspace_path)
    return pb


DECISION_LOG_HEADER = """\
# DECISION_LOG.md

## Decision Register

| ID | Date | Stage | Decision | Status | Replaces | Owner | Related file |
|---|---|---|---|---|---|---|---|
"""


def test_missing_decision_log(_patch_workspace: Path) -> None:
    problems = _check_decision_log_entries("inputs_and_mode_selection")
    assert len(problems) == 1
    assert "does not exist" in problems[0]


def test_empty_decision_register(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    (pb / "DECISION_LOG.md").write_text(DECISION_LOG_HEADER, encoding="utf-8")
    problems = _check_decision_log_entries("inputs_and_mode_selection")
    assert len(problems) == 1
    assert "no entries" in problems[0]


def test_no_stage_reference(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = DECISION_LOG_HEADER + (
        "| DEC-001 | 2026-01-01 | other_stage | Some decision | ACTIVE | — | Solo | file.py |\n"
    )
    (pb / "DECISION_LOG.md").write_text(text, encoding="utf-8")
    problems = _check_decision_log_entries("inputs_and_mode_selection")
    assert len(problems) == 1
    assert "no entries reference stage" in problems[0]


def test_valid_stage_entry(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = DECISION_LOG_HEADER + (
        "| DEC-001 | 2026-01-01 | inputs_and_mode_selection | Decision | ACTIVE | — | Solo | f.py |\n"
    )
    (pb / "DECISION_LOG.md").write_text(text, encoding="utf-8")
    problems = _check_decision_log_entries("inputs_and_mode_selection")
    assert problems == []


def test_feasibility_stage_entry(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = DECISION_LOG_HEADER + (
        "| DEC-001 | 2026-01-01 | feasibility_and_kill_criteria | Go decision | ACTIVE | — | Solo | f.md |\n"
    )
    (pb / "DECISION_LOG.md").write_text(text, encoding="utf-8")
    problems = _check_decision_log_entries("feasibility_and_kill_criteria")
    assert problems == []


def test_architecture_stage_entry(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = DECISION_LOG_HEADER + (
        "| DEC-001 | 2026-01-01 | architecture_and_contracts | Stack choice | ACTIVE | — | Solo | arch.md |\n"
    )
    (pb / "DECISION_LOG.md").write_text(text, encoding="utf-8")
    problems = _check_decision_log_entries("architecture_and_contracts")
    assert problems == []
