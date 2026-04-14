"""Tests for validate_feasibility_criteria stage-gate check."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.programstart_validate import validate_feasibility_criteria


_FEAS_DECISION_LOG = """\
# DECISION_LOG.md

## Decision Register

| ID | Date | Stage | Decision | Status | Replaces | Owner | Related file |
|---|---|---|---|---|---|---|---|
| DEC-001 | 2026-01-01 | feasibility_and_kill_criteria | Go decision | ACTIVE | — | Solo | feas.md |
"""


@pytest.fixture()
def _feas(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()
    (pb / "DECISION_LOG.md").write_text(_FEAS_DECISION_LOG, encoding="utf-8")

    def _workspace_path(rel: str) -> Path:
        return tmp_path / rel

    monkeypatch.setattr("scripts.programstart_validate.workspace_path", _workspace_path)
    return pb


def _write_feasibility(pb: Path, kill_criteria: list[str] | None = None,
                        recommendation: str | None = None) -> None:
    lines = ["# FEASIBILITY.md\n"]
    lines.append("## Kill Criteria\n")
    if kill_criteria is not None:
        for c in kill_criteria:
            lines.append(f"- {c}")
    else:
        lines.append("- criterion")
        lines.append("- criterion")
        lines.append("- criterion")
    lines.append("")
    lines.append("## Recommendation\n")
    if recommendation is not None:
        lines.append(recommendation)
    else:
        lines.append("Decision: go / limited spike / no-go")
    lines.append("")
    (pb / "FEASIBILITY.md").write_text("\n".join(lines), encoding="utf-8")


_GOOD_CRITERIA = [
    "If user adoption is below 5 users in 30 days, stop",
    "If infrastructure cost exceeds $500/month, pivot",
    "When no measurable improvement after 2 sprints, kill",
]


# --- Missing file ---

def test_missing_feasibility(_feas: Path) -> None:
    problems = validate_feasibility_criteria({})
    assert any("FEASIBILITY.md does not exist" in p for p in problems)


# --- Template placeholders ---

def test_template_kill_criteria_rejected(_feas: Path) -> None:
    _write_feasibility(_feas)  # default = template placeholders
    problems = validate_feasibility_criteria({})
    assert any("0 kill criteria found" in p for p in problems)


def test_template_recommendation_rejected(_feas: Path) -> None:
    _write_feasibility(_feas, kill_criteria=_GOOD_CRITERIA)
    problems = validate_feasibility_criteria({})
    assert any("template option list" in p for p in problems)


# --- Insufficient criteria ---

def test_fewer_than_3_criteria(_feas: Path) -> None:
    _write_feasibility(_feas, kill_criteria=_GOOD_CRITERIA[:2],
                        recommendation="Decision: go")
    problems = validate_feasibility_criteria({})
    assert any("2 kill criteria found" in p for p in problems)


# --- Format check ---

def test_bad_format_detected(_feas: Path) -> None:
    criteria = [
        "If user adoption is below 5 users, stop",
        "If cost exceeds budget, pivot",
        "users do not like it",  # no If/When ... action pattern
    ]
    _write_feasibility(_feas, kill_criteria=criteria, recommendation="Decision: go")
    problems = validate_feasibility_criteria({})
    assert any("kill criterion 3" in p and "format" in p for p in problems)
    # First two should pass format check
    assert not any("kill criterion 1" in p for p in problems)
    assert not any("kill criterion 2" in p for p in problems)


# --- Valid recommendation ---

def test_go_recommendation_accepted(_feas: Path) -> None:
    _write_feasibility(_feas, kill_criteria=_GOOD_CRITERIA,
                        recommendation="Decision: go\n\nReasoning: evidence supports viability.")
    problems = validate_feasibility_criteria({})
    assert problems == []


def test_no_go_recommendation_accepted(_feas: Path) -> None:
    _write_feasibility(_feas, kill_criteria=_GOOD_CRITERIA,
                        recommendation="Decision: no-go\n\nReasoning: market too small.")
    problems = validate_feasibility_criteria({})
    assert problems == []


def test_limited_spike_accepted(_feas: Path) -> None:
    _write_feasibility(_feas, kill_criteria=_GOOD_CRITERIA,
                        recommendation="Decision: limited spike\n\nReasoning: need more data.")
    problems = validate_feasibility_criteria({})
    assert problems == []


# --- No decision word ---

def test_empty_recommendation(_feas: Path) -> None:
    _write_feasibility(_feas, kill_criteria=_GOOD_CRITERIA,
                        recommendation="We should think about this more.")
    problems = validate_feasibility_criteria({})
    assert any("no go/no-go decision" in p for p in problems)


# --- Clean pass ---

def test_fully_filled_no_problems(_feas: Path) -> None:
    _write_feasibility(_feas, kill_criteria=_GOOD_CRITERIA,
                        recommendation="Decision: go\n\nAll criteria met.")
    problems = validate_feasibility_criteria({})
    assert problems == []
