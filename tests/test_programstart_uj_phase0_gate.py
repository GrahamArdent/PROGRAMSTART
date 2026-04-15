"""Tests for USERJOURNEY phase_0 engineering-ready gate wired via preflight_problems."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry
from scripts.programstart_workflow_state import preflight_problems


def test_uj_phase0_advance_blocked_on_unresolved_questions(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """preflight returns problem when OPEN_QUESTIONS has unresolved items at UJ phase_0."""
    uj = tmp_path / "USERJOURNEY"
    uj.mkdir()
    (uj / "OPEN_QUESTIONS.md").write_text(
        "## Remaining Operational And Legal Decisions\n\n"
        "1. Do we need a DPA with the data processor?\n"
        "2. Which jurisdiction governs the ToS?\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("scripts.programstart_validate.workspace_path", lambda rel: tmp_path / rel)
    # Skip unrelated file checks that would fail in tmp_path
    monkeypatch.setattr("scripts.programstart_validate.validate_required_files", lambda _r, *_a: [])
    monkeypatch.setattr("scripts.programstart_validate.validate_metadata", lambda _r, *_a: [])
    monkeypatch.setattr("scripts.programstart_validate.validate_workflow_state", lambda _r, *_a: [])
    monkeypatch.setattr("scripts.programstart_drift_check.load_changed_files", lambda *_a: [])

    registry = load_registry()
    problems = preflight_problems(registry, "userjourney", active_step="phase_0")

    assert isinstance(problems, list)
    eng_errors = [p for p in problems if "engineering-ready" in p or "unresolved" in p.lower()]
    assert eng_errors, f"Expected engineering-ready gate error, got: {problems}"


def test_uj_phase0_advance_passes_on_resolved_questions(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """No problems when OPEN_QUESTIONS has no numbered items under the decisions heading."""
    uj = tmp_path / "USERJOURNEY"
    uj.mkdir()
    (uj / "OPEN_QUESTIONS.md").write_text(
        "## Remaining Operational And Legal Decisions\n\nAll decisions resolved.\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("scripts.programstart_validate.workspace_path", lambda rel: tmp_path / rel)
    monkeypatch.setattr("scripts.programstart_validate.validate_required_files", lambda _r, *_a: [])
    monkeypatch.setattr("scripts.programstart_validate.validate_metadata", lambda _r, *_a: [])
    monkeypatch.setattr("scripts.programstart_validate.validate_workflow_state", lambda _r, *_a: [])
    monkeypatch.setattr("scripts.programstart_drift_check.load_changed_files", lambda *_a: [])

    registry = load_registry()
    problems = preflight_problems(registry, "userjourney", active_step="phase_0")

    eng_errors = [p for p in problems if "engineering-ready" in p or "unresolved" in p.lower()]
    assert eng_errors == [], f"Expected no engineering-ready errors, got: {eng_errors}"


def test_uj_non_phase0_advance_not_checked(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """preflight at phase_1 does not run the engineering-ready gate."""
    uj = tmp_path / "USERJOURNEY"
    uj.mkdir()
    # Put unresolved items that WOULD trigger the gate at phase_0
    (uj / "OPEN_QUESTIONS.md").write_text(
        "## Remaining Operational And Legal Decisions\n\n1. Unresolved item that should not block phase_1.\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("scripts.programstart_validate.workspace_path", lambda rel: tmp_path / rel)
    monkeypatch.setattr("scripts.programstart_validate.validate_required_files", lambda _r, *_a: [])
    monkeypatch.setattr("scripts.programstart_validate.validate_metadata", lambda _r, *_a: [])
    monkeypatch.setattr("scripts.programstart_validate.validate_workflow_state", lambda _r, *_a: [])
    monkeypatch.setattr("scripts.programstart_drift_check.load_changed_files", lambda *_a: [])

    registry = load_registry()
    problems = preflight_problems(registry, "userjourney", active_step="phase_1")

    eng_errors = [p for p in problems if "engineering-ready" in p or "unresolved" in p.lower()]
    assert eng_errors == [], f"engineering-ready gate must not fire at phase_1, got: {eng_errors}"
