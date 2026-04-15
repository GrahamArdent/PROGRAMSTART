"""Tests for validate_intake_complete stage-gate check."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.programstart_validate import validate_intake_complete


@pytest.fixture()
def _kickoff(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Return a KICKOFF_PACKET path and patch workspace_path for PROGRAMBUILD/."""
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()

    def _workspace_path(rel: str) -> Path:
        return tmp_path / rel

    monkeypatch.setattr("scripts.programstart_validate.workspace_path", _workspace_path)
    return pb


def _write_kickoff(pb: Path, fields: dict[str, str]) -> None:
    lines = ["# Kickoff Packet\n\n```text"]
    default_fields = {
        "PROJECT_NAME": "",
        "ONE_LINE_DESCRIPTION": "",
        "PRIMARY_USER": "",
        "SECONDARY_USER": "",
        "CORE_PROBLEM": "",
        "SUCCESS_METRIC": "",
        "PRODUCT_SHAPE": "[web app | mobile app | CLI tool | desktop app | API service | data pipeline | library | other]",
        "KNOWN_CONSTRAINTS": "",
        "OUT_OF_SCOPE": "",
        "COMPLIANCE_OR_SECURITY_NEEDS": "",
        "TEAM_SIZE": "",
        "DELIVERY_TARGET": "",
    }
    default_fields.update(fields)
    for k, v in default_fields.items():
        lines.append(f"{k}: {v}")
    lines.append("```")
    (pb / "PROGRAMBUILD_KICKOFF_PACKET.md").write_text("\n".join(lines), encoding="utf-8")


def _write_intake(pb: Path, fields: dict[str, str] | None = None) -> None:
    default = {
        "PROBLEM_RAW": "",
        "WHO_HAS_THIS_PROBLEM": "",
        "CURRENT_SOLUTION": "",
        "SUCCESS_OUTCOME": "",
        "CHEAPEST_VALIDATION": "",
        "NOT_BUILDING_1": "",
        "NOT_BUILDING_2": "",
        "NOT_BUILDING_3": "",
        "KILL_SIGNAL_1": "",
        "KILL_SIGNAL_2": "",
        "KILL_SIGNAL_3": "",
    }
    if fields:
        default.update(fields)
    lines = ["# Idea Intake\n"]
    for k, v in default.items():
        lines.append(f"{k}: {v}")
    (pb / "PROGRAMBUILD_IDEA_INTAKE.md").write_text("\n".join(lines), encoding="utf-8")


def _filled_kickoff_fields() -> dict[str, str]:
    return {
        "PROJECT_NAME": "TestProject",
        "ONE_LINE_DESCRIPTION": "A test tool",
        "PRIMARY_USER": "Developer",
        "CORE_PROBLEM": "Testing is hard",
        "SUCCESS_METRIC": "50% fewer bugs",
        "PRODUCT_SHAPE": "CLI tool",
    }


def _filled_intake_fields() -> dict[str, str]:
    return {
        "PROBLEM_RAW": "Testing is hard",
        "WHO_HAS_THIS_PROBLEM": "Developers",
        "CURRENT_SOLUTION": "Manual testing",
        "SUCCESS_OUTCOME": "50% fewer bugs",
        "CHEAPEST_VALIDATION": "Run a pilot",
        "NOT_BUILDING_1": "No IDE plugin",
        "NOT_BUILDING_2": "No CI integration",
        "NOT_BUILDING_3": "No mobile app",
        "KILL_SIGNAL_1": "If adoption < 5 users in 30 days, stop",
        "KILL_SIGNAL_2": "If no bug reduction after 2 sprints, pivot",
        "KILL_SIGNAL_3": "If team rejects workflow, stop",
    }


# --- Missing file tests ---


def test_missing_kickoff_file(_kickoff: Path) -> None:
    pb = _kickoff
    _write_intake(pb, _filled_intake_fields())
    # No kickoff file written
    problems = validate_intake_complete({})
    assert any("PROGRAMBUILD_KICKOFF_PACKET.md does not exist" in p for p in problems)


def test_missing_intake_file(_kickoff: Path) -> None:
    pb = _kickoff
    _write_kickoff(pb, _filled_kickoff_fields())
    # No intake file written
    problems = validate_intake_complete({})
    assert any("PROGRAMBUILD_IDEA_INTAKE.md does not exist" in p for p in problems)


# --- Blank template tests ---


def test_blank_kickoff_all_fields_reported(_kickoff: Path) -> None:
    pb = _kickoff
    _write_kickoff(pb, {})  # All defaults = empty
    _write_intake(pb, _filled_intake_fields())
    problems = validate_intake_complete({})
    for field in ["PROJECT_NAME", "ONE_LINE_DESCRIPTION", "PRIMARY_USER", "CORE_PROBLEM", "SUCCESS_METRIC", "PRODUCT_SHAPE"]:
        assert any(field in p for p in problems), f"Expected error for {field}"


def test_blank_intake_all_fields_reported(_kickoff: Path) -> None:
    pb = _kickoff
    _write_kickoff(pb, _filled_kickoff_fields())
    _write_intake(pb, {})  # All defaults = empty
    problems = validate_intake_complete({})
    for field in ["PROBLEM_RAW", "WHO_HAS_THIS_PROBLEM", "CURRENT_SOLUTION", "SUCCESS_OUTCOME", "CHEAPEST_VALIDATION"]:
        assert any(field in p for p in problems), f"Expected error for {field}"
    assert any("NOT_BUILDING" in p for p in problems)
    assert any("KILL_SIGNAL" in p for p in problems)


# --- Partial fill tests ---


def test_partial_kickoff(_kickoff: Path) -> None:
    pb = _kickoff
    fields = _filled_kickoff_fields()
    fields["SUCCESS_METRIC"] = ""
    fields["PRODUCT_SHAPE"] = ""
    _write_kickoff(pb, fields)
    _write_intake(pb, _filled_intake_fields())
    problems = validate_intake_complete({})
    assert any("SUCCESS_METRIC" in p for p in problems)
    assert any("PRODUCT_SHAPE" in p for p in problems)
    assert not any("PROJECT_NAME" in p for p in problems)


def test_product_shape_hint_stripped(_kickoff: Path) -> None:
    """PRODUCT_SHAPE with only the hint text should count as empty."""
    pb = _kickoff
    fields = _filled_kickoff_fields()
    fields["PRODUCT_SHAPE"] = "[web app | mobile app | CLI tool | desktop app | API service | data pipeline | library | other]"
    _write_kickoff(pb, fields)
    _write_intake(pb, _filled_intake_fields())
    problems = validate_intake_complete({})
    assert any("PRODUCT_SHAPE" in p and "empty" in p for p in problems)


# --- NOT_BUILDING / KILL_SIGNAL tests ---


def test_insufficient_not_building(_kickoff: Path) -> None:
    pb = _kickoff
    _write_kickoff(pb, _filled_kickoff_fields())
    fields = _filled_intake_fields()
    fields["NOT_BUILDING_3"] = ""
    _write_intake(pb, fields)
    problems = validate_intake_complete({})
    assert any("NOT_BUILDING" in p and "2" in p and "need at least 3" in p for p in problems)


def test_insufficient_kill_signals(_kickoff: Path) -> None:
    pb = _kickoff
    _write_kickoff(pb, _filled_kickoff_fields())
    fields = _filled_intake_fields()
    fields["KILL_SIGNAL_2"] = ""
    fields["KILL_SIGNAL_3"] = ""
    _write_intake(pb, fields)
    problems = validate_intake_complete({})
    assert any("KILL_SIGNAL" in p and "1" in p and "need at least 3" in p for p in problems)


# --- Fully filled = clean ---


_INTAKE_DECISION_LOG = """\
# DECISION_LOG.md

## Decision Register

| ID | Date | Stage | Decision | Status | Replaces | Owner | Related file |
|---|---|---|---|---|---|---|---|
| DEC-001 | 2026-01-01 | inputs_and_mode_selection | Mode selected | ACTIVE | — | Solo | intake.md |
"""


def test_fully_filled_no_problems(_kickoff: Path) -> None:
    pb = _kickoff
    _write_kickoff(pb, _filled_kickoff_fields())
    _write_intake(pb, _filled_intake_fields())
    (pb / "DECISION_LOG.md").write_text(_INTAKE_DECISION_LOG, encoding="utf-8")
    problems = validate_intake_complete({})
    assert problems == []


def test_invalid_product_shape_fails(_kickoff: Path) -> None:
    """PRODUCT_SHAPE not in whitelist → reports problem."""
    pb = _kickoff
    fields = _filled_kickoff_fields()
    fields["PRODUCT_SHAPE"] = "gadget-app"
    _write_kickoff(pb, fields)
    _write_intake(pb, _filled_intake_fields())
    (pb / "DECISION_LOG.md").write_text(_INTAKE_DECISION_LOG, encoding="utf-8")
    problems = validate_intake_complete({})
    assert any("PRODUCT_SHAPE" in p and "not a recognized shape" in p for p in problems)
