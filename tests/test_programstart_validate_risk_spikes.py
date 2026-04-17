"""Tests for validate_risk_spikes."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.programstart_validate import validate_risk_spikes


@pytest.fixture()
def _patch_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()

    def _workspace_path(rel: str) -> Path:
        return tmp_path / rel

    monkeypatch.setattr("scripts.programstart_validate_core.workspace_path", _workspace_path)
    return pb


SPIKE_REGISTER_HEADER = """\
# RISK_SPIKES.md

## Spike Register

| Spike | Risk source | Hypothesis | Method | Pass criteria | Result | Decision |
|---|---|---|---|---|---|---|
"""


def test_missing_file(_patch_workspace: Path) -> None:
    problems = validate_risk_spikes({})
    assert any("does not exist" in p for p in problems)


def test_empty_file(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    (pb / "RISK_SPIKES.md").write_text("", encoding="utf-8")
    problems = validate_risk_spikes({})
    assert any("empty" in p for p in problems)


def test_no_spike_entries(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    (pb / "RISK_SPIKES.md").write_text(SPIKE_REGISTER_HEADER, encoding="utf-8")
    problems = validate_risk_spikes({})
    assert any("no entries" in p for p in problems)


def test_spike_without_pass_criteria(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = SPIKE_REGISTER_HEADER + ("| S-001 | ARCHITECTURE | Hypothesis | Prototype in 1 day |  | Pending | TBD |\n")
    (pb / "RISK_SPIKES.md").write_text(text, encoding="utf-8")
    problems = validate_risk_spikes({})
    assert any("pass criteria" in p for p in problems)


def test_spike_without_method(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = SPIKE_REGISTER_HEADER + ("| S-001 | ARCHITECTURE | Hypothesis |  | Test passes in CI | Pending | TBD |\n")
    (pb / "RISK_SPIKES.md").write_text(text, encoding="utf-8")
    problems = validate_risk_spikes({})
    assert any("method" in p for p in problems)


def test_happy_path(_patch_workspace: Path) -> None:
    pb = _patch_workspace
    text = SPIKE_REGISTER_HEADER + (
        "| S-001 | ARCHITECTURE | Auth library works | Prototype in 1 day | Unit tests pass | Pass | Use library X |\n"
    )
    (pb / "RISK_SPIKES.md").write_text(text, encoding="utf-8")
    problems = validate_risk_spikes({})
    assert problems == []
