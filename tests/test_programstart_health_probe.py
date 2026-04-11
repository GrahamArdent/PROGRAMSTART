"""Tests for programstart_health_probe.py."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.programstart_health_probe import (
    HealthProbeReport,
    SystemHealthReport,
    _check_authority_sync,
    _check_required_files,
    _checklist_progress,
    _classify_health,
    _signoff_info,
    probe_target,
)
from scripts.programstart_workflow_state import diff_states


def test_probe_target_on_current_workspace() -> None:
    """Health probe should produce a valid report when run against the actual workspace."""
    from scripts.programstart_common import ROOT

    report = probe_target(ROOT)
    assert report.probe_time
    assert report.registry_version
    assert report.overall_health in {"healthy", "warnings", "degraded", "critical"}
    assert len(report.systems) >= 1
    pb = next((s for s in report.systems if s.system == "programbuild"), None)
    assert pb is not None
    assert pb.present is True
    assert pb.total_control_files > 0


def test_probe_target_missing_registry(tmp_path: Path) -> None:
    """Probe should report critical if no registry exists."""
    report = probe_target(tmp_path)
    assert report.overall_health == "critical"
    assert any("process-registry.json" in p for p in report.structural_problems)


def test_classify_health_healthy() -> None:
    report = HealthProbeReport(
        systems=[
            SystemHealthReport(
                system="programbuild",
                present=True,
                total_control_files=5,
                present_control_files=5,
                total_output_files=5,
                present_output_files=5,
            )
        ]
    )
    health, summary = _classify_health(report)
    assert health == "healthy"


def test_classify_health_degraded_missing_files() -> None:
    report = HealthProbeReport(
        systems=[
            SystemHealthReport(
                system="programbuild",
                present=True,
                missing_files=["a.md", "b.md", "c.md", "d.md"],
                total_control_files=10,
                present_control_files=6,
            )
        ]
    )
    health, _ = _classify_health(report)
    assert health == "degraded"


def test_classify_health_critical_violations() -> None:
    report = HealthProbeReport(
        systems=[
            SystemHealthReport(
                system="programbuild",
                present=True,
                drift_violations=["sync violation"],
            )
        ]
    )
    health, _ = _classify_health(report)
    assert health == "critical"


def test_check_required_files(tmp_path: Path) -> None:
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "A.md").write_text("a", encoding="utf-8")
    registry = {
        "systems": {
            "programbuild": {
                "control_files": ["PROGRAMBUILD/A.md", "PROGRAMBUILD/B.md"],
                "output_files": ["PROGRAMBUILD/C.md"],
            }
        }
    }
    missing, cp, ct, op, ot = _check_required_files(tmp_path, registry, "programbuild")
    assert "PROGRAMBUILD/B.md" in missing
    assert "PROGRAMBUILD/C.md" in missing
    assert cp == 1
    assert ct == 2
    assert op == 0
    assert ot == 1


def test_check_authority_sync() -> None:
    registry = {
        "sync_rules": [
            {
                "name": "test_rule",
                "system": "programbuild",
                "authority_files": ["AUTH.md"],
                "dependent_files": ["DEP.md"],
                "require_authority_when_dependents_change": True,
            }
        ]
    }
    violations, notes = _check_authority_sync(Path("."), registry, ["DEP.md"], "programbuild")
    assert len(violations) == 1
    assert "test_rule" in violations[0]

    violations2, notes2 = _check_authority_sync(Path("."), registry, ["AUTH.md"], "programbuild")
    assert len(violations2) == 0
    assert len(notes2) == 1


def test_checklist_progress(tmp_path: Path) -> None:
    (tmp_path / "PROGRAMBUILD").mkdir()
    (tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_CHECKLIST.md").write_text(
        "## Setup\n- [x] done\n- [ ] not done\n- [x] also done\n", encoding="utf-8"
    )
    checked, total = _checklist_progress(tmp_path, "programbuild")
    assert checked == 2
    assert total == 3


def test_signoff_info() -> None:
    state = {
        "stages": {
            "feasibility": {
                "status": "completed",
                "signoff": {"decision": "approved", "date": "2026-03-01"},
            },
            "research": {
                "status": "blocked",
                "signoff": {"decision": "hold", "date": "2026-03-15"},
            },
            "requirements": {
                "status": "planned",
                "signoff": {},
            },
        }
    }
    last_date, last_decision, last_commit_hash, days, completed, blocked = _signoff_info(state, "programbuild")
    assert last_date == "2026-03-15"
    assert last_decision == "hold"
    assert last_commit_hash == ""
    assert "feasibility" in completed
    assert "research" in blocked
    assert days is not None


def test_diff_states_detects_changes() -> None:
    old = {
        "systems": {
            "programbuild": {
                "active_stage": "feasibility",
                "stages": {
                    "feasibility": {"status": "in_progress", "signoff": {"decision": ""}},
                    "research": {"status": "planned", "signoff": {"decision": ""}},
                },
            }
        }
    }
    new = {
        "systems": {
            "programbuild": {
                "active_stage": "research",
                "stages": {
                    "feasibility": {"status": "completed", "signoff": {"decision": "approved"}},
                    "research": {"status": "in_progress", "signoff": {"decision": ""}},
                },
            }
        }
    }
    diffs = diff_states(old, new)
    assert any("status" in d and "feasibility" in d for d in diffs)
    assert any("active step" in d for d in diffs)
    assert len(diffs) >= 3  # status change, signoff change, active step change


def test_diff_states_no_changes() -> None:
    state = {"systems": {"programbuild": {"active_stage": "feasibility", "stages": {"feasibility": {"status": "in_progress", "signoff": {"decision": ""}}}}}}
    diffs = diff_states(state, state)
    assert diffs == []
