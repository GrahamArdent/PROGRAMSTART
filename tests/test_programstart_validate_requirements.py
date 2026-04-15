"""Tests for validate_requirements_complete stage-gate check."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.programstart_validate import validate_requirements_complete


@pytest.fixture()
def _reqs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()

    def _workspace_path(rel: str) -> Path:
        return tmp_path / rel

    monkeypatch.setattr("scripts.programstart_validate.workspace_path", _workspace_path)
    return pb


def _write_requirements(pb: Path, table_rows: list[dict[str, str]] | None = None, stories: str | None = None) -> None:
    lines = ["# REQUIREMENTS.md\n"]
    lines.append("## Functional Requirements\n")
    lines.append("| ID | Requirement | Priority | Notes |")
    lines.append("|---|---|---|---|")
    if table_rows:
        for r in table_rows:
            lines.append(f"| {r.get('ID', '')} | {r.get('Requirement', '')} | {r.get('Priority', '')} | {r.get('Notes', '')} |")
    else:
        lines.append("| FR-001 | | P0 | |")
    lines.append("")
    if stories:
        lines.append("## User Stories\n")
        lines.append(stories)
    lines.append("")
    (pb / "REQUIREMENTS.md").write_text("\n".join(lines), encoding="utf-8")


def _write_user_flows(pb: Path, content: str = "") -> None:
    text = f"# USER_FLOWS.md\n\n## User Flows\n\n{content}\n"
    (pb / "USER_FLOWS.md").write_text(text, encoding="utf-8")


_GOOD_ROWS = [
    {"ID": "FR-001", "Requirement": "Create receipts", "Priority": "P0", "Notes": ""},
    {"ID": "FR-002", "Requirement": "Export CSV", "Priority": "P1", "Notes": ""},
    {"ID": "FR-003", "Requirement": "Dark mode", "Priority": "P2", "Notes": ""},
]


# --- Missing file ---


def test_missing_requirements_file(_reqs: Path) -> None:
    problems = validate_requirements_complete({})
    assert any("REQUIREMENTS.md does not exist" in p for p in problems)


# --- Template (no real rows) ---


def test_template_no_requirements(_reqs: Path) -> None:
    _write_requirements(_reqs)  # default = template placeholder
    _write_user_flows(_reqs, "FR-001")
    problems = validate_requirements_complete({})
    assert any("no functional requirements defined" in p for p in problems)


# --- Missing priority ---


def test_missing_priority(_reqs: Path) -> None:
    rows = [{"ID": "FR-001", "Requirement": "Do something", "Priority": "", "Notes": ""}]
    _write_requirements(_reqs, table_rows=rows)
    _write_user_flows(_reqs, "FR-001")
    problems = validate_requirements_complete({})
    assert any("FR-001 has no priority" in p for p in problems)


# --- Invalid priority ---


def test_invalid_priority(_reqs: Path) -> None:
    rows = [{"ID": "FR-001", "Requirement": "Do something", "Priority": "High", "Notes": ""}]
    _write_requirements(_reqs, table_rows=rows)
    _write_user_flows(_reqs, "FR-001")
    problems = validate_requirements_complete({})
    assert any("invalid priority" in p for p in problems)


# --- Missing ID ---


def test_missing_id(_reqs: Path) -> None:
    rows = [{"ID": "", "Requirement": "Do something", "Priority": "P0", "Notes": ""}]
    _write_requirements(_reqs, table_rows=rows)
    _write_user_flows(_reqs)
    problems = validate_requirements_complete({})
    assert any("has no ID" in p for p in problems)


# --- Empty acceptance criteria ---


def test_empty_acceptance_criteria(_reqs: Path) -> None:
    stories = "### Story 1\n\nAs a user\nI want to do things\nSo that life is good\n\nAcceptance criteria:\n-\n-\n"
    _write_requirements(_reqs, table_rows=_GOOD_ROWS, stories=stories)
    _write_user_flows(_reqs, "FR-001 FR-002 FR-003")
    problems = validate_requirements_complete({})
    assert any("Story 1 has empty acceptance criteria" in p for p in problems)


# --- Flow cross-reference ---


def test_missing_flow_reference(_reqs: Path) -> None:
    _write_requirements(_reqs, table_rows=_GOOD_ROWS)
    _write_user_flows(_reqs, "FR-001")  # Missing FR-002, FR-003
    problems = validate_requirements_complete({})
    assert any("FR-002" in p for p in problems)
    assert any("FR-003" in p for p in problems)
    assert not any("FR-001" in p for p in problems)


def test_flow_cross_ref_no_substring_false_positive(_reqs: Path) -> None:
    """FR-001 must not match FR-0010 — word-boundary regex prevents substring hits."""
    rows = [
        {"ID": "FR-001", "Requirement": "Create receipt", "Priority": "P0", "Notes": ""},
        {"ID": "FR-0010", "Requirement": "Delete receipt", "Priority": "P1", "Notes": ""},
    ]
    _write_requirements(_reqs, table_rows=rows)
    # Flow text contains only FR-0010 — FR-001 should be reported as missing
    _write_user_flows(_reqs, "FR-0010")
    problems = validate_requirements_complete({})
    assert any("FR-001" in p and "FR-0010" not in p for p in problems)


def test_missing_user_flows_file(_reqs: Path) -> None:
    _write_requirements(_reqs, table_rows=_GOOD_ROWS)
    # No USER_FLOWS.md written
    problems = validate_requirements_complete({})
    assert any("USER_FLOWS.md does not exist" in p for p in problems)


# --- Clean pass ---


def test_fully_filled_no_problems(_reqs: Path) -> None:
    stories = (
        "### Story 1\n\nAs a user\nI want to create receipts\nSo that I can track expenses\n\n"
        "Acceptance criteria:\n- Receipt is saved\n- Receipt has date\n"
    )
    _write_requirements(_reqs, table_rows=_GOOD_ROWS, stories=stories)
    _write_user_flows(_reqs, "FR-001 FR-002 FR-003")
    problems = validate_requirements_complete({})
    assert problems == []


def test_user_flows_no_section_heading_fails(_reqs: Path) -> None:
    """USER_FLOWS.md with no ## or ### headings → reports problem."""
    _write_requirements(_reqs, table_rows=_GOOD_ROWS)
    # Write flat content with no ## headings
    flow_path = _reqs / "USER_FLOWS.md"
    flow_path.write_text("# USER_FLOWS.md\n\nFR-001 FR-002 FR-003\n", encoding="utf-8")
    problems = validate_requirements_complete({})
    assert any("no ## or ### section headings" in p for p in problems)
