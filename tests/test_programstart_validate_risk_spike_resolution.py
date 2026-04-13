"""Tests for validate_risk_spike_resolution."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.programstart_validate import validate_risk_spike_resolution


@pytest.fixture()
def _patch_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()

    def _workspace_path(rel: str) -> Path:
        return tmp_path / rel

    monkeypatch.setattr("scripts.programstart_validate.workspace_path", _workspace_path)
    return pb


SPIKE_REGISTER_HEADER = """\
# RISK_SPIKES.md

## Spike Register

| Spike | Risk source | Hypothesis | Method | Pass criteria | Result | Decision |
|---|---|---|---|---|---|---|
"""


def test_missing_file_passes(_patch_workspace: Path) -> None:
    """File absent → no problems (existence check is already in risk-spikes gate)."""
    problems = validate_risk_spike_resolution({})
    assert problems == []


def test_no_real_rows_passes(_patch_workspace: Path) -> None:
    """Header-only table (template placeholder row) → no problems."""
    pb = _patch_workspace
    (pb / "RISK_SPIKES.md").write_text(SPIKE_REGISTER_HEADER, encoding="utf-8")
    problems = validate_risk_spike_resolution({})
    assert problems == []


def test_all_resolved_passes(_patch_workspace: Path) -> None:
    """Every row has Result = 'Pass' → no problems."""
    pb = _patch_workspace
    text = SPIKE_REGISTER_HEADER + (
        "| S-001 | ARCHITECTURE | Auth library works | Prototype in 1 day | Unit tests pass | Pass | Use library X |\n"
    )
    (pb / "RISK_SPIKES.md").write_text(text, encoding="utf-8")
    problems = validate_risk_spike_resolution({})
    assert problems == []


def test_empty_result_fails(_patch_workspace: Path) -> None:
    """Row with both Result and Decision columns empty → reports problem."""
    pb = _patch_workspace
    text = SPIKE_REGISTER_HEADER + (
        "| S-001 | ARCHITECTURE | Auth library works | Prototype in 1 day | Unit tests pass |  |  |\n"
    )
    (pb / "RISK_SPIKES.md").write_text(text, encoding="utf-8")
    problems = validate_risk_spike_resolution({})
    assert any("S-001" in p for p in problems)
    assert any("unresolved" in p for p in problems)


def test_open_spike_fails(_patch_workspace: Path) -> None:
    """Row with Result = 'Pending' → reports problem with spike ID."""
    pb = _patch_workspace
    text = SPIKE_REGISTER_HEADER + (
        "| S-002 | PERFORMANCE | Redis scales | Load test | p99 < 200ms | Pending | TBD |\n"
    )
    (pb / "RISK_SPIKES.md").write_text(text, encoding="utf-8")
    problems = validate_risk_spike_resolution({})
    assert any("S-002" in p for p in problems)
    assert any("pending" in p.lower() for p in problems)
