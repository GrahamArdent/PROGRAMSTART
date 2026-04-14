"""Tests for programstart_health_probe.py."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.programstart_health_probe import (
    HealthProbeReport,
    SystemHealthReport,
    _active_step,
    _check_authority_sync,
    _check_metadata,
    _check_required_files,
    _check_step_order,
    _check_workflow_state,
    _checklist_progress,
    _classify_health,
    _entry_key,
    _files_changed_since_commit,
    _git_changed_files,
    _load_json_from,
    _load_target_registry,
    _load_target_state,
    _signoff_info,
    _step_order,
    _target_path,
    main,
    print_multi_summary,
    print_report,
    probe_multiple,
    probe_system,
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
    state = {
        "systems": {
            "programbuild": {
                "active_stage": "feasibility",
                "stages": {"feasibility": {"status": "in_progress", "signoff": {"decision": ""}}},
            }
        }
    }
    diffs = diff_states(state, state)
    assert diffs == []


# ---------------------------------------------------------------------------
# Phase J — push health_probe toward 95%
# ---------------------------------------------------------------------------


class TestTargetPath:
    def test_joins_relative(self, tmp_path: Path) -> None:
        assert _target_path(tmp_path, "foo/bar.md") == tmp_path / "foo" / "bar.md"


class TestLoadJsonFrom:
    def test_returns_empty_for_missing(self, tmp_path: Path) -> None:
        assert _load_json_from(tmp_path / "nope.json") == {}

    def test_loads_valid_json(self, tmp_path: Path) -> None:
        p = tmp_path / "data.json"
        p.write_text('{"key": 1}', encoding="utf-8")
        assert _load_json_from(p) == {"key": 1}


class TestLoadTargetRegistry:
    def test_loads_from_config_dir(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config"
        cfg.mkdir()
        (cfg / "process-registry.json").write_text('{"version": "2.0"}', encoding="utf-8")
        assert _load_target_registry(tmp_path) == {"version": "2.0"}

    def test_returns_empty_when_missing(self, tmp_path: Path) -> None:
        assert _load_target_registry(tmp_path) == {}


class TestLoadTargetState:
    def test_uses_registry_file(self, tmp_path: Path) -> None:
        (tmp_path / "state.json").write_text('{"active_stage": "s1"}', encoding="utf-8")
        registry = {"workflow_state": {"programbuild": {"file": "state.json"}}}
        state = _load_target_state(tmp_path, registry, "programbuild")
        assert state["active_stage"] == "s1"

    def test_fallback_programbuild(self, tmp_path: Path) -> None:
        pb = tmp_path / "PROGRAMBUILD"
        pb.mkdir()
        (pb / "PROGRAMBUILD_STATE.json").write_text('{"active_stage": "fb"}', encoding="utf-8")
        state = _load_target_state(tmp_path, {}, "programbuild")
        assert state["active_stage"] == "fb"

    def test_fallback_userjourney(self, tmp_path: Path) -> None:
        uj = tmp_path / "USERJOURNEY"
        uj.mkdir()
        (uj / "USERJOURNEY_STATE.json").write_text('{"active_phase": "p1"}', encoding="utf-8")
        state = _load_target_state(tmp_path, {}, "userjourney")
        assert state["active_phase"] == "p1"


class TestActiveStep:
    def test_returns_active_key(self) -> None:
        registry = {"workflow_state": {"programbuild": {"active_key": "active_stage"}}}
        state = {"active_stage": "requirements"}
        assert _active_step(registry, "programbuild", state) == "requirements"

    def test_returns_unknown_when_missing(self) -> None:
        assert _active_step({}, "programbuild", {}) == "unknown"


class TestStepOrder:
    def test_returns_names(self) -> None:
        registry = {
            "workflow_state": {
                "programbuild": {"step_order": [{"name": "a"}, {"name": "b"}]}
            }
        }
        assert _step_order(registry, "programbuild") == ["a", "b"]

    def test_handles_string_steps(self) -> None:
        registry = {"workflow_state": {"x": {"step_order": ["s1", "s2"]}}}
        assert _step_order(registry, "x") == ["s1", "s2"]


class TestEntryKey:
    def test_programbuild(self) -> None:
        assert _entry_key("programbuild") == "stages"

    def test_userjourney(self) -> None:
        assert _entry_key("userjourney") == "phases"


class TestGitChangedFiles:
    def test_returns_files_from_subprocess(self, monkeypatch: "pytest.MonkeyPatch", tmp_path: Path) -> None:
        import subprocess

        call_count = 0

        def fake_run(cmd, **_kw):
            nonlocal call_count
            call_count += 1
            out = "file1.md\nfile2.md\n" if call_count == 1 else "file3.md\n"
            return subprocess.CompletedProcess(cmd, 0, stdout=out, stderr="")

        monkeypatch.setattr("subprocess.run", fake_run)
        result = _git_changed_files(tmp_path)
        assert "file1.md" in result
        assert "file2.md" in result
        assert "file3.md" in result

    def test_handles_subprocess_failure(self, monkeypatch: "pytest.MonkeyPatch", tmp_path: Path) -> None:
        import subprocess

        def fake_run(cmd, **_kw):
            return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="error")

        monkeypatch.setattr("subprocess.run", fake_run)
        result = _git_changed_files(tmp_path)
        assert result == []

    def test_handles_os_error(self, monkeypatch: "pytest.MonkeyPatch", tmp_path: Path) -> None:
        def fake_run(cmd, **_kw):
            raise OSError("git not found")

        monkeypatch.setattr("subprocess.run", fake_run)
        result = _git_changed_files(tmp_path)
        assert result == []


class TestCheckMetadata:
    def test_detects_missing_header(self, tmp_path: Path) -> None:
        d = tmp_path / "PROGRAMBUILD"
        d.mkdir()
        (d / "DOC.md").write_text("# Just a heading\nSome content.\n", encoding="utf-8")
        registry = {"systems": {"programbuild": {"metadata_required": ["PROGRAMBUILD/DOC.md"]}}}
        problems = _check_metadata(tmp_path, registry, "programbuild")
        assert any("Missing metadata header" in p for p in problems)

    def test_accepts_valid_header(self, tmp_path: Path) -> None:
        d = tmp_path / "PROGRAMBUILD"
        d.mkdir()
        (d / "DOC.md").write_text("Purpose: something\nOwner: me\nAuthority: doc\n", encoding="utf-8")
        registry = {"systems": {"programbuild": {"metadata_required": ["PROGRAMBUILD/DOC.md"]}}}
        problems = _check_metadata(tmp_path, registry, "programbuild")
        assert problems == []

    def test_skips_missing_file(self, tmp_path: Path) -> None:
        registry = {"systems": {"programbuild": {"metadata_required": ["PROGRAMBUILD/NOPE.md"]}}}
        problems = _check_metadata(tmp_path, registry, "programbuild")
        assert problems == []

    def test_stops_at_frontmatter_delimiter(self, tmp_path: Path) -> None:
        d = tmp_path / "PROGRAMBUILD"
        d.mkdir()
        (d / "DOC.md").write_text("---\nPurpose: test\n---\n# Heading\n", encoding="utf-8")
        registry = {"systems": {"programbuild": {"metadata_required": ["PROGRAMBUILD/DOC.md"]}}}
        problems = _check_metadata(tmp_path, registry, "programbuild")
        # Frontmatter delimiter stops scanning before Purpose: is found
        assert any("Missing metadata header" in p for p in problems)


class TestCheckWorkflowState:
    def test_reports_no_state_file(self, tmp_path: Path) -> None:
        registry = {"workflow_state": {"programbuild": {"file": "PROGRAMBUILD/STATE.json", "active_key": "active_stage"}}}
        problems = _check_workflow_state(tmp_path, registry, "programbuild")
        assert any("No workflow state file" in p for p in problems)

    def test_reports_missing_active_key(self, tmp_path: Path) -> None:
        pb = tmp_path / "PROGRAMBUILD"
        pb.mkdir()
        (pb / "STATE.json").write_text('{"stages": {}}', encoding="utf-8")
        registry = {"workflow_state": {"programbuild": {"file": "PROGRAMBUILD/STATE.json", "active_key": "active_stage"}}}
        problems = _check_workflow_state(tmp_path, registry, "programbuild")
        assert any("Missing 'active_stage'" in p for p in problems)

    def test_reports_missing_steps(self, tmp_path: Path) -> None:
        pb = tmp_path / "PROGRAMBUILD"
        pb.mkdir()
        (pb / "STATE.json").write_text('{"active_stage": "s1", "stages": {}}', encoding="utf-8")
        registry = {
            "workflow_state": {
                "programbuild": {
                    "file": "PROGRAMBUILD/STATE.json",
                    "active_key": "active_stage",
                    "step_order": [{"name": "s1"}, {"name": "s2"}],
                }
            }
        }
        problems = _check_workflow_state(tmp_path, registry, "programbuild")
        assert any("'s1' missing" in p for p in problems)
        assert any("'s2' missing" in p for p in problems)

    def test_clean_state(self, tmp_path: Path) -> None:
        pb = tmp_path / "PROGRAMBUILD"
        pb.mkdir()
        (pb / "STATE.json").write_text(
            '{"active_stage": "s1", "stages": {"s1": {}, "s2": {}}}', encoding="utf-8"
        )
        registry = {
            "workflow_state": {
                "programbuild": {
                    "file": "PROGRAMBUILD/STATE.json",
                    "active_key": "active_stage",
                    "step_order": [{"name": "s1"}, {"name": "s2"}],
                }
            }
        }
        problems = _check_workflow_state(tmp_path, registry, "programbuild")
        assert problems == []


class TestCheckStepOrder:
    def _make_registry(self, *, is_template: bool = False) -> dict:
        reg: dict = {
            "workflow_state": {
                "programbuild": {
                    "active_key": "active_stage",
                    "step_order": [{"name": "s1"}, {"name": "s2"}, {"name": "s3"}],
                    "step_files": {"s1": ["a.md"], "s2": ["b.md"], "s3": ["c.md"]},
                }
            }
        }
        if is_template:
            reg["workspace"] = {"repo_role": "template_repo"}
        return reg

    def test_no_violations_for_active_file(self, tmp_path: Path) -> None:
        reg = self._make_registry()
        state = {"active_stage": "s2", "stages": {}}
        violations = _check_step_order(tmp_path, reg, "programbuild", state, ["b.md"])
        assert violations == []

    def test_detects_future_step_file(self, tmp_path: Path) -> None:
        reg = self._make_registry()
        state = {"active_stage": "s1", "stages": {}}
        violations = _check_step_order(tmp_path, reg, "programbuild", state, ["c.md"])
        assert any("future step" in v for v in violations)

    def test_template_repo_exempt(self, tmp_path: Path) -> None:
        reg = self._make_registry(is_template=True)
        state = {"active_stage": "s1", "stages": {}}
        violations = _check_step_order(tmp_path, reg, "programbuild", state, ["c.md"])
        assert violations == []

    def test_unknown_active_step(self, tmp_path: Path) -> None:
        reg = self._make_registry()
        state = {"active_stage": "unknown_step", "stages": {}}
        violations = _check_step_order(tmp_path, reg, "programbuild", state, ["c.md"])
        assert violations == []


class TestFilesChangedSinceCommit:
    def test_returns_count(self, monkeypatch: "pytest.MonkeyPatch", tmp_path: Path) -> None:
        import subprocess

        def fake_run(cmd, **_kw):
            return subprocess.CompletedProcess(cmd, 0, stdout="f1.md\nf2.md\n", stderr="")

        monkeypatch.setattr("subprocess.run", fake_run)
        assert _files_changed_since_commit(tmp_path, "abc123") == 2

    def test_returns_none_on_failure(self, monkeypatch: "pytest.MonkeyPatch", tmp_path: Path) -> None:
        import subprocess

        def fake_run(cmd, **_kw):
            return subprocess.CompletedProcess(cmd, 128, stdout="", stderr="bad")

        monkeypatch.setattr("subprocess.run", fake_run)
        assert _files_changed_since_commit(tmp_path, "abc123") is None

    def test_returns_none_on_timeout(self, monkeypatch: "pytest.MonkeyPatch", tmp_path: Path) -> None:
        import subprocess

        def fake_run(cmd, **_kw):
            raise subprocess.TimeoutExpired(cmd, 15)

        monkeypatch.setattr("subprocess.run", fake_run)
        assert _files_changed_since_commit(tmp_path, "abc123") is None


class TestClassifyHealthBranches:
    def test_warnings_branch(self) -> None:
        """signoff_drift without other issues triggers 'warnings'."""
        report = HealthProbeReport(
            systems=[
                SystemHealthReport(
                    system="programbuild",
                    present=True,
                    total_control_files=5,
                    present_control_files=5,
                    total_output_files=5,
                    present_output_files=5,
                    missing_files=["one.md"],
                )
            ]
        )
        health, _ = _classify_health(report)
        assert health == "warnings"

    def test_degraded_stale_signoff(self) -> None:
        report = HealthProbeReport(
            systems=[
                SystemHealthReport(
                    system="programbuild",
                    present=True,
                    total_control_files=5,
                    present_control_files=5,
                    last_signoff_date="2026-01-01",
                    days_since_last_signoff=60,
                )
            ]
        )
        health, _ = _classify_health(report)
        assert health == "degraded"

    def test_critical_many_problems(self) -> None:
        report = HealthProbeReport(
            systems=[
                SystemHealthReport(
                    system="programbuild",
                    present=True,
                    validation_problems=["p1", "p2", "p3", "p4"],
                )
            ]
        )
        health, _ = _classify_health(report)
        assert health == "critical"

    def test_critical_blocked_steps(self) -> None:
        report = HealthProbeReport(
            systems=[
                SystemHealthReport(
                    system="programbuild",
                    present=True,
                    blocked_steps=["s2"],
                )
            ]
        )
        health, _ = _classify_health(report)
        assert health == "critical"


class TestProbeSystem:
    def _make_target(self, tmp_path: Path) -> tuple[Path, dict]:
        pb = tmp_path / "PROGRAMBUILD"
        pb.mkdir()
        (pb / "DOC.md").write_text("Purpose: x\nOwner: y\nAuthority: z\n", encoding="utf-8")
        (pb / "STATE.json").write_text(
            json.dumps({"active_stage": "s1", "stages": {"s1": {"status": "in_progress"}}}),
            encoding="utf-8",
        )
        registry = {
            "systems": {
                "programbuild": {
                    "root": "PROGRAMBUILD",
                    "control_files": ["PROGRAMBUILD/DOC.md"],
                    "output_files": [],
                    "metadata_required": ["PROGRAMBUILD/DOC.md"],
                }
            },
            "workflow_state": {
                "programbuild": {
                    "file": "PROGRAMBUILD/STATE.json",
                    "active_key": "active_stage",
                    "step_order": [{"name": "s1"}],
                }
            },
            "sync_rules": [],
        }
        return tmp_path, registry

    def test_returns_report(self, tmp_path: Path) -> None:
        root, registry = self._make_target(tmp_path)
        report = probe_system(root, registry, "programbuild", [])
        assert report is not None
        assert report.system == "programbuild"
        assert report.present is True
        assert report.active_step == "s1"

    def test_returns_none_for_unknown_system(self, tmp_path: Path) -> None:
        assert probe_system(tmp_path, {"systems": {}}, "nope", []) is None

    def test_skips_optional_absent_system(self, tmp_path: Path) -> None:
        registry = {"systems": {"uj": {"root": "USERJOURNEY", "optional": True}}}
        assert probe_system(tmp_path, registry, "uj", []) is None


class TestProbeMultiple:
    def test_returns_list_of_reports(self, tmp_path: Path) -> None:
        a = tmp_path / "a"
        b = tmp_path / "b"
        a.mkdir()
        b.mkdir()
        reports = probe_multiple([a, b])
        assert len(reports) == 2
        assert all(r.overall_health == "critical" for r in reports)  # no registries


class TestPrintReport:
    def test_prints_output(self, capsys) -> None:
        report = HealthProbeReport(
            target="/tmp/test",
            probe_time="2026-04-14T00:00:00Z",
            registry_version="2.0",
            repo_role="template_repo",
            overall_health="healthy",
            summary="all good",
            structural_problems=["struct issue"],
            systems=[
                SystemHealthReport(
                    system="programbuild",
                    present=True,
                    active_step="s1",
                    variant="product",
                    total_control_files=3,
                    present_control_files=3,
                    total_output_files=2,
                    present_output_files=2,
                    checklist_checked=2,
                    checklist_total=5,
                    checklist_pct=40.0,
                    completed_steps=["s0"],
                    blocked_steps=["s2"],
                    last_signoff_date="2026-04-01",
                    last_signoff_decision="approved",
                    days_since_last_signoff=13,
                    missing_files=["X.md"],
                    validation_problems=["bad header"],
                    drift_violations=["sync rule"],
                    drift_notes=["authority note"],
                )
            ],
        )
        print_report(report)
        out = capsys.readouterr().out
        assert "HEALTHY" in out
        assert "struct issue" in out
        assert "s1" in out
        assert "product" in out
        assert "40.0%" in out
        assert "X.md" in out
        assert "bad header" in out
        assert "sync rule" in out
        assert "authority note" in out
        assert "s0" in out
        assert "Blocked" in out

    def test_prints_no_signoff(self, capsys) -> None:
        report = HealthProbeReport(
            target="/tmp/test",
            probe_time="now",
            registry_version="1",
            repo_role="r",
            overall_health="healthy",
            summary="ok",
            systems=[SystemHealthReport(system="programbuild", present=True)],
        )
        print_report(report)
        out = capsys.readouterr().out
        assert "none" in out


class TestPrintMultiSummary:
    def test_prints_table(self, capsys) -> None:
        reports = [
            HealthProbeReport(target="/tmp/a", overall_health="healthy", systems=[SystemHealthReport(system="prog", present=True)]),
            HealthProbeReport(target="/tmp/b", overall_health="critical", structural_problems=["missing"]),
        ]
        print_multi_summary(reports)
        out = capsys.readouterr().out
        assert "healthy" in out
        assert "critical" in out


class TestMain:
    def test_default_target_json(self, capsys) -> None:
        code = main(["--json"])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert "overall_health" in data
        assert isinstance(code, int)

    def test_default_target_text(self, capsys) -> None:
        code = main([])
        out = capsys.readouterr().out
        assert "Health Probe" in out
        assert isinstance(code, int)

    def test_explicit_target(self, capsys, tmp_path: Path) -> None:
        code = main(["--target", str(tmp_path), "--json"])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["overall_health"] == "critical"
        assert code == 1

    def test_multi_target(self, capsys, tmp_path: Path) -> None:
        a = tmp_path / "a"
        b = tmp_path / "b"
        a.mkdir()
        b.mkdir()
        code = main(["--target", str(a), "--target", str(b), "--json"])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert isinstance(data, list)
        assert len(data) == 2
        assert code == 1  # both are critical (no registry)

    def test_multi_target_text(self, capsys, tmp_path: Path) -> None:
        a = tmp_path / "a"
        a.mkdir()
        code = main(["--target", str(a), "--target", str(a)])
        out = capsys.readouterr().out
        assert "Health" in out or "Repo" in out
