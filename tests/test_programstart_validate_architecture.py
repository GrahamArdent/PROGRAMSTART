"""Tests for validate_architecture_contracts stage-gate check."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.programstart_validate import validate_architecture_contracts


@pytest.fixture()
def _arch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()

    def _workspace_path(rel: str) -> Path:
        return tmp_path / rel

    monkeypatch.setattr("scripts.programstart_validate_core.workspace_path", _workspace_path)
    return pb


_FULL_ARCH = """\
# ARCHITECTURE.md

## System Topology

Local CLI tool with script modules.

## Technology Decision Table

| Tier | Choice | Alternatives | Reason |
|---|---|---|---|
| Language | Python | Go | Rich ecosystem |

## Data Model And Ownership

| Entity | Owner | Key fields | Access notes |
|---|---|---|---|
| config | config/ | systems | Read by CLI |

## Command Surface

| Command | Module | Purpose |
|---|---|---|
| run | main | Entrypoint |
"""


# --- Missing file ---


def test_missing_architecture(_arch: Path) -> None:
    problems = validate_architecture_contracts({})
    assert any("ARCHITECTURE.md does not exist" in p for p in problems)


# --- Empty topology ---


def test_empty_topology(_arch: Path) -> None:
    text = _FULL_ARCH.replace(
        "Local CLI tool with script modules.",
        "",
    )
    (_arch / "ARCHITECTURE.md").write_text(text, encoding="utf-8")
    problems = validate_architecture_contracts({})
    assert any("System Topology section is empty" in p for p in problems)


# --- Missing sections ---


def test_no_data_model(_arch: Path) -> None:
    text = _FULL_ARCH.replace("## Data Model And Ownership", "## Other Section")
    (_arch / "ARCHITECTURE.md").write_text(text, encoding="utf-8")
    problems = validate_architecture_contracts({})
    assert any("no data model section" in p for p in problems)


def test_no_contracts_section(_arch: Path) -> None:
    text = _FULL_ARCH.replace("## Command Surface", "## Other Section")
    (_arch / "ARCHITECTURE.md").write_text(text, encoding="utf-8")
    problems = validate_architecture_contracts({})
    assert any("no contracts" in p for p in problems)


# --- Empty tech table ---


def test_empty_tech_table(_arch: Path) -> None:
    text = _FULL_ARCH.replace("| Language | Python | Go | Rich ecosystem |", "")
    (_arch / "ARCHITECTURE.md").write_text(text, encoding="utf-8")
    problems = validate_architecture_contracts({})
    assert any("Technology Decision Table has no entries" in p for p in problems)


# --- Alternative section names ---


def test_api_contracts_accepted(_arch: Path) -> None:
    text = _FULL_ARCH.replace("## Command Surface", "## API Contracts")
    (_arch / "ARCHITECTURE.md").write_text(text, encoding="utf-8")
    problems = validate_architecture_contracts({})
    assert not any("no contracts" in p for p in problems)


def test_system_boundaries_accepted(_arch: Path) -> None:
    text = _FULL_ARCH.replace("## Command Surface", "## System Boundaries")
    (_arch / "ARCHITECTURE.md").write_text(text, encoding="utf-8")
    problems = validate_architecture_contracts({})
    assert not any("no contracts" in p for p in problems)


_DECISION_LOG = """\
# DECISION_LOG.md

## Decision Register

| ID | Date | Stage | Decision | Status | Replaces | Owner | Related file |
|---|---|---|---|---|---|---|---|
| DEC-001 | 2026-01-01 | architecture_and_contracts | Stack choice | ACTIVE | — | Solo | arch.md |
"""


# --- Clean pass ---


def test_fully_filled_no_problems(_arch: Path) -> None:
    (_arch / "ARCHITECTURE.md").write_text(_FULL_ARCH, encoding="utf-8")
    (_arch / "DECISION_LOG.md").write_text(_DECISION_LOG, encoding="utf-8")
    problems = validate_architecture_contracts({})
    assert problems == []
