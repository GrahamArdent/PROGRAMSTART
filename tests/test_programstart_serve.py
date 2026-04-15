from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_serve
from scripts.programstart_serve import (
    ALLOWED_COMMANDS,
    advance_workflow_with_signoff,
    get_doc_preview,
    run_command,
    save_workflow_signoff,
    strip_ansi,
    update_implementation_tracker_phase,
    update_implementation_tracker_slice,
)


def test_allowed_commands_contains_core_entries() -> None:
    assert "state.show" in ALLOWED_COMMANDS
    assert "validate" in ALLOWED_COMMANDS
    assert "status" in ALLOWED_COMMANDS
    assert "guide.programbuild" in ALLOWED_COMMANDS
    assert "guide.kickoff" in ALLOWED_COMMANDS
    assert "log" in ALLOWED_COMMANDS
    assert "drift" in ALLOWED_COMMANDS
    assert "progress" in ALLOWED_COMMANDS
    assert ALLOWED_COMMANDS["status"][:3] == [sys.executable, "-m", "scripts.programstart_cli"]


def test_run_command_unknown_returns_error() -> None:
    result = run_command("nonexistent.command")
    assert result["exit_code"] == 1
    assert "unknown command" in result["output"]


def test_run_command_rejects_disallowed_extra_args() -> None:
    result = run_command("status", ["--evil-arg"])
    assert result["exit_code"] == 1
    assert "not permitted" in result["output"]


def test_run_command_status_succeeds() -> None:
    result = run_command("status")
    assert result["exit_code"] == 0
    assert "PROGRAMBUILD" in result["output"]


def test_run_command_validate_succeeds() -> None:
    result = run_command("validate")
    assert result["exit_code"] == 0


def test_strip_ansi_removes_escape_codes() -> None:
    assert strip_ansi("\033[32mgreen\033[0m") == "green"
    assert strip_ansi("plain text") == "plain text"
    assert strip_ansi("\033[1;31mbold red\033[0m") == "bold red"


def test_allowed_commands_all_have_list_values() -> None:
    for key, value in ALLOWED_COMMANDS.items():
        assert isinstance(value, list), f"{key} should be a list"
        assert len(value) >= 1, f"{key} should have at least one element"


def test_update_implementation_tracker_phase_updates_status_and_sanitizes_blockers(tmp_path: Path, monkeypatch) -> None:
    tracker = tmp_path / "USERJOURNEY" / "IMPLEMENTATION_TRACKER.md"
    tracker.parent.mkdir(parents=True)
    tracker.write_text(
        "# Implementation Tracker\n"
        "Last updated: 2026-03-27\n\n"
        "| Phase | Status | Exit Gate | Target Route | Current blockers | Notes |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| 2 | Planned | Gate | /activate | none | note |\n\n"
        "| Slice | Status | Window | Notes |\n"
        "| --- | --- | --- | --- |\n"
        "| Slice 3 | Pending | Soon | initial |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(programstart_serve, "ROOT", tmp_path)

    result = update_implementation_tracker_phase("2", "Blocked", "Need | review\nnow")

    updated = tracker.read_text(encoding="utf-8")
    assert result["exit_code"] == 0
    assert "| 2 | Blocked | Gate | /activate | Need ¦ review now | note |" in updated
    assert "Last updated:" in updated


def test_update_implementation_tracker_slice_updates_notes_and_status(tmp_path: Path, monkeypatch) -> None:
    tracker = tmp_path / "USERJOURNEY" / "IMPLEMENTATION_TRACKER.md"
    tracker.parent.mkdir(parents=True)
    tracker.write_text(
        "# Implementation Tracker\n"
        "Last updated: 2026-03-27\n\n"
        "| Phase | Status | Exit Gate | Target Route | Current blockers | Notes |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| 2 | Planned | Gate | /activate | none | note |\n\n"
        "| Slice | Status | Window | Notes |\n"
        "| --- | --- | --- | --- |\n"
        "| Slice 3 | Pending | Soon | initial |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(programstart_serve, "ROOT", tmp_path)

    result = update_implementation_tracker_slice("Slice 3", "Ready", "Ship | this\nweek")

    updated = tracker.read_text(encoding="utf-8")
    assert result["exit_code"] == 0
    assert "| Slice 3 | Ready | Soon | Ship ¦ this week |" in updated


def test_save_workflow_signoff_persists_signoff_history(monkeypatch, tmp_path) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {}, "signoff_history": []},
        },
    }
    registry = {"systems": {"programbuild": {}}}

    monkeypatch.setattr(programstart_serve, "load_registry", lambda: registry)
    monkeypatch.setattr(programstart_serve, "load_workflow_state", lambda _registry, _system: deepcopy(state))
    monkeypatch.setattr(
        programstart_serve,
        "workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(programstart_serve, "workflow_entry_key", lambda _system: "stages")
    monkeypatch.setattr(programstart_serve, "save_workflow_state", lambda _registry, _system, value: saved.update(value))
    monkeypatch.setattr(programstart_serve, "workflow_state_path", lambda _r, _s: tmp_path / "state.json")

    result = save_workflow_signoff("programbuild", "approved", "2026-04-01", "Ship | it\nnow")

    assert result["exit_code"] == 0
    signoff = saved["stages"]["inputs_and_mode_selection"]["signoff"]
    assert signoff["decision"] == "approved"
    assert signoff["date"] == "2026-04-01"
    assert signoff["notes"] == "Ship ¦ it now"
    assert saved["stages"]["inputs_and_mode_selection"]["signoff_history"][0]["notes"] == "Ship ¦ it now"


def test_advance_workflow_with_signoff_completes_current_and_promotes_next(monkeypatch, tmp_path) -> None:
    saved: dict[str, Any] = {}
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {}, "signoff_history": []},
            "feasibility": {"status": "planned", "signoff": {}, "signoff_history": []},
        },
    }
    registry = {"systems": {"programbuild": {}}}

    monkeypatch.setattr(programstart_serve, "load_registry", lambda: registry)
    monkeypatch.setattr(programstart_serve, "load_workflow_state", lambda _registry, _system: deepcopy(state))
    monkeypatch.setattr(
        programstart_serve,
        "workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(programstart_serve, "workflow_entry_key", lambda _system: "stages")
    monkeypatch.setattr(
        programstart_serve,
        "workflow_steps",
        lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr(programstart_serve, "save_workflow_state", lambda _registry, _system, value: saved.update(value))
    monkeypatch.setattr(programstart_serve, "workflow_state_path", lambda _r, _s: tmp_path / "state.json")

    result = advance_workflow_with_signoff("programbuild", "approved", "2026-04-02", "Ready | now", False)

    assert result["exit_code"] == 0
    assert saved["active_stage"] == "feasibility"
    assert saved["stages"]["inputs_and_mode_selection"]["status"] == "completed"
    assert saved["stages"]["feasibility"]["status"] == "in_progress"
    assert saved["stages"]["inputs_and_mode_selection"]["signoff_history"][0]["notes"] == "Ready ¦ now"


def test_run_command_rejects_too_many_extra_args() -> None:
    result = run_command("status", ["--json"] * 10)
    assert result["exit_code"] == 1
    assert "too many extra args" in result["output"]


def test_run_command_rejects_extra_arg_exceeding_length() -> None:
    result = run_command("status", ["x" * 2001])
    assert result["exit_code"] == 1
    assert "char limit" in result["output"]


def test_run_bootstrap_invalid_dest() -> None:
    from scripts.programstart_serve import run_bootstrap

    result = run_bootstrap("../../../etc/passwd", "TestApp", "product", False)
    assert result["exit_code"] == 1
    assert "invalid" in result["output"].lower()


def test_run_bootstrap_invalid_project_name() -> None:
    from scripts.programstart_serve import run_bootstrap

    result = run_bootstrap("C:\\Projects\\Test", "123-bad-name!", "product", False)
    assert result["exit_code"] == 1
    assert "project name" in result["output"].lower()


def test_run_bootstrap_invalid_variant() -> None:
    from scripts.programstart_serve import run_bootstrap

    result = run_bootstrap("C:\\Projects\\Test", "ValidName", "unknown", False)
    assert result["exit_code"] == 1
    assert "variant" in result["output"].lower()


def test_advance_non_in_progress_step_returns_error(monkeypatch, tmp_path) -> None:
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "planned", "signoff": {}, "signoff_history": []},
        },
    }
    registry = {"systems": {"programbuild": {}}}

    monkeypatch.setattr(programstart_serve, "load_registry", lambda: registry)
    monkeypatch.setattr(programstart_serve, "load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(programstart_serve, "workflow_active_step", lambda _r, _s, _st=None: "inputs_and_mode_selection")
    monkeypatch.setattr(programstart_serve, "workflow_entry_key", lambda _s: "stages")
    monkeypatch.setattr(programstart_serve, "workflow_steps", lambda _r, _s: ["inputs_and_mode_selection"])
    monkeypatch.setattr(programstart_serve, "workflow_state_path", lambda _r, _s: tmp_path / "state.json")

    result = advance_workflow_with_signoff("programbuild", "approved", "2026-04-02", "", False)
    assert result["exit_code"] == 1
    assert "not in_progress" in result["output"]


def test_advance_dry_run_returns_preview(monkeypatch, tmp_path) -> None:
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {}, "signoff_history": []},
            "feasibility": {"status": "planned", "signoff": {}, "signoff_history": []},
        },
    }
    registry = {"systems": {"programbuild": {}}}

    monkeypatch.setattr(programstart_serve, "load_registry", lambda: registry)
    monkeypatch.setattr(programstart_serve, "load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(programstart_serve, "workflow_active_step", lambda _r, _s, _st=None: "inputs_and_mode_selection")
    monkeypatch.setattr(programstart_serve, "workflow_entry_key", lambda _s: "stages")
    monkeypatch.setattr(programstart_serve, "workflow_steps", lambda _r, _s: ["inputs_and_mode_selection", "feasibility"])
    monkeypatch.setattr(programstart_serve, "workflow_state_path", lambda _r, _s: tmp_path / "state.json")

    result = advance_workflow_with_signoff("programbuild", "approved", "2026-04-02", "", True)
    assert result["exit_code"] == 0
    assert "[dry-run]" in result["output"]
    assert "feasibility" in result["output"]


def test_signoff_history_capped_at_max(monkeypatch, tmp_path) -> None:
    """signoff_history must not exceed MAX_SIGNOFF_HISTORY entries (T3)."""
    saved: dict[str, Any] = {}
    existing_history = [
        {"decision": "approved", "date": f"2026-01-{i:02d}", "notes": f"entry {i}", "saved_at": f"2026-01-{i:02d}"}
        for i in range(1, 106)  # 105 existing entries
    ]
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {
                "status": "in_progress",
                "signoff": {},
                "signoff_history": list(existing_history),
            },
        },
    }
    registry = {"systems": {"programbuild": {}}}

    monkeypatch.setattr(programstart_serve, "load_registry", lambda: registry)
    monkeypatch.setattr(programstart_serve, "load_workflow_state", lambda _registry, _system: deepcopy(state))
    monkeypatch.setattr(
        programstart_serve,
        "workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(programstart_serve, "workflow_entry_key", lambda _system: "stages")
    monkeypatch.setattr(programstart_serve, "save_workflow_state", lambda _registry, _system, value: saved.update(value))
    monkeypatch.setattr(programstart_serve, "workflow_state_path", lambda _r, _s: tmp_path / "state.json")

    result = save_workflow_signoff("programbuild", "approved", "2026-06-01", "cap test")

    assert result["exit_code"] == 0
    history = saved["stages"]["inputs_and_mode_selection"]["signoff_history"]
    assert len(history) <= programstart_serve.MAX_SIGNOFF_HISTORY
    assert history[-1]["notes"] == "cap test"
    # Oldest entries should have been trimmed
    assert history[0]["notes"] != "entry 1"


# ── API endpoint/docs sync ────────────────────────────────────────────────────


def test_api_routes_documented_in_dashboard_api_md() -> None:
    """Every /api/* route in programstart_serve.py must have a matching section in docs/dashboard-api.md."""
    import re

    serve_path = ROOT / "scripts" / "programstart_serve.py"
    docs_path = ROOT / "docs" / "dashboard-api.md"

    serve_src = serve_path.read_text(encoding="utf-8")
    route_pattern = re.compile(r'parsed\.path\s*(?:==|in)\s*["\(]([^")\n]+)')
    raw_routes: set[str] = set()
    for m in route_pattern.finditer(serve_src):
        value = m.group(1)
        for segment in value.replace('"', "").replace("'", "").split(","):
            segment = segment.strip()
            if segment.startswith("/api/"):
                raw_routes.add(segment)

    docs_text = docs_path.read_text(encoding="utf-8")
    missing = [route for route in sorted(raw_routes) if route not in docs_text]
    assert not missing, f"API routes not documented in dashboard-api.md: {missing}"


# ---------------------------------------------------------------------------
# Phase C: coverage push — previously uncovered branches in serve.py
# ---------------------------------------------------------------------------


def test_get_state_json_returns_error_dict_on_load_failure(monkeypatch) -> None:
    """Lines 347-349: exception inside get_state_json try block → {'error': ...}."""
    monkeypatch.setattr(programstart_serve, "load_registry", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    result = programstart_serve.get_state_json()
    assert "error" in result
    assert "boom" in result["error"]


def test_get_state_json_userjourney_optional_not_attached_sets_placeholder(monkeypatch) -> None:
    """Lines 195-207: optional+not-attached system gets a placeholder dict with active='not attached'."""
    original_attached = programstart_serve.system_is_attached

    def mock_is_attached(registry: dict, system: str) -> bool:
        if system == "userjourney":
            return False
        return original_attached(registry, system)

    monkeypatch.setattr(programstart_serve, "system_is_attached", mock_is_attached)
    result = programstart_serve.get_state_json()
    uj = result.get("userjourney", {})
    assert uj.get("active") == "not attached"
    assert uj.get("attached") is False


def test_load_dashboard_html_returns_fallback_when_index_html_missing(monkeypatch, tmp_path: Path) -> None:
    """Line 660: dashboard/index.html missing → fallback placeholder HTML returned."""
    monkeypatch.setattr(programstart_serve, "DASHBOARD_DIR", tmp_path / "no_dashboard_here")
    html = programstart_serve._load_dashboard_html()
    assert "Dashboard files not found" in html


def test_advance_workflow_with_signoff_dry_run_final_step_shows_completion(monkeypatch, tmp_path: Path) -> None:
    """Lines 572-576: dry_run=True with no next step → '[dry-run] Would mark final ...' message."""
    state = {
        "active_stage": "release",
        "stages": {
            "release": {"status": "in_progress", "signoff": {}, "signoff_history": []},
        },
    }
    registry = {"systems": {"programbuild": {}}}
    monkeypatch.setattr(programstart_serve, "load_registry", lambda: registry)
    monkeypatch.setattr(programstart_serve, "load_workflow_state", lambda _r, _s: state)
    monkeypatch.setattr(programstart_serve, "workflow_active_step", lambda _r, _s, _st=None: "release")
    monkeypatch.setattr(programstart_serve, "workflow_entry_key", lambda _s: "stages")
    monkeypatch.setattr(programstart_serve, "workflow_steps", lambda _r, _s: ["release"])  # only step
    monkeypatch.setattr(programstart_serve, "workflow_state_path", lambda _r, _s: tmp_path / "state.json")

    result = advance_workflow_with_signoff("programbuild", "approved", "2026-05-01", "", True)

    assert result["exit_code"] == 0
    assert "[dry-run]" in result["output"]
    assert "final" in result["output"]


def test_run_bootstrap_dry_run_false_does_not_add_dry_run_arg(monkeypatch, tmp_path: Path) -> None:
    """Line 173->175: dry_run=False branch omits --dry-run from subprocess command."""
    import subprocess

    captured_cmd: list[list[str]] = []

    class _FakeResult:
        stdout = "Bootstrap done"
        stderr = ""
        returncode = 0

    def _fake_run(cmd: list[str], **kwargs: object) -> _FakeResult:
        captured_cmd.append(list(cmd))
        return _FakeResult()

    monkeypatch.setattr(subprocess, "run", _fake_run)
    from scripts.programstart_serve import run_bootstrap

    result = run_bootstrap("C:\\Projects\\TestApp", "MyValidApp", "product", False)
    assert "--dry-run" not in captured_cmd[0]
    assert result["exit_code"] == 0


def test_update_implementation_tracker_phase_phase_not_found_returns_error(tmp_path: Path, monkeypatch) -> None:
    """Lines 408->421, 422: for loop exhausted without matching phase → error returned."""
    tracker = tmp_path / "USERJOURNEY" / "IMPLEMENTATION_TRACKER.md"
    tracker.parent.mkdir(parents=True)
    tracker.write_text(
        "# Tracker\n"
        "Last updated: 2026-03-27\n\n"
        "| Phase | Status | Exit Gate | Target Route | Current blockers | Notes |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| 5 | Planned | G | /r | none | x |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(programstart_serve, "ROOT", tmp_path)
    result = update_implementation_tracker_phase("3", "Completed", "")  # phase 3 absent
    assert result["exit_code"] == 1
    assert "not found" in result["output"]


def test_update_implementation_tracker_slice_no_userjourney_dir_returns_error(tmp_path: Path, monkeypatch) -> None:
    """Line 436: USERJOURNEY directory absent → early-return error."""
    monkeypatch.setattr(programstart_serve, "ROOT", tmp_path)  # no USERJOURNEY subdir
    result = update_implementation_tracker_slice("Slice 1", "Ready", "")
    assert result["exit_code"] == 1
    assert "not attached" in result["output"]


# ── run_command extra paths ───────────────────────────────────────────────────


def test_run_command_with_valid_extra_arg() -> None:
    """Passing an allowed extra arg should reach cmd.extend rather than early return."""
    result = run_command("log", ["approved"])
    # Validation passed — no rejection messages
    assert "not permitted" not in result["output"]
    assert "char limit" not in result["output"]
    assert "too many extra args" not in result["output"]


def test_run_command_timeout(monkeypatch) -> None:
    """subprocess.TimeoutExpired should be caught and reported."""
    import subprocess

    def _raise_timeout(*args: object, **kwargs: object) -> None:
        raise subprocess.TimeoutExpired("cmd", 60)

    monkeypatch.setattr("scripts.programstart_serve.subprocess.run", _raise_timeout)
    result = run_command("status")
    assert result["exit_code"] == 1
    assert "timed out" in result["output"]


# ── get_doc_preview edge cases ────────────────────────────────────────────────


def test_get_doc_preview_empty_path() -> None:
    result = get_doc_preview("")
    assert result == {"error": "missing path"}


def test_get_doc_preview_file_type_not_previewable(tmp_path: Path, monkeypatch) -> None:
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()
    (pb / "data.bin").write_bytes(b"binary")
    monkeypatch.setattr(programstart_serve, "ROOT", tmp_path)
    result = get_doc_preview("PROGRAMBUILD/data.bin")
    assert result == {"error": "file type not previewable"}


def test_get_doc_preview_file_too_large(tmp_path: Path, monkeypatch) -> None:
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()
    (pb / "huge.md").write_bytes(b"x" * 70_000)
    monkeypatch.setattr(programstart_serve, "ROOT", tmp_path)
    result = get_doc_preview("PROGRAMBUILD/huge.md")
    assert "too large" in result.get("error", "")


# ── update_implementation_tracker_phase malformed row ────────────────────────


def test_update_tracker_phase_malformed_row(tmp_path: Path, monkeypatch) -> None:
    """A phase row with ≠ 6 cells should return an error."""
    uj = tmp_path / "USERJOURNEY"
    uj.mkdir()
    (uj / "IMPLEMENTATION_TRACKER.md").write_text(
        "| Phase | Status |\n| --- | --- |\n| 2 | Planned |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(programstart_serve, "ROOT", tmp_path)
    result = update_implementation_tracker_phase("2", "Blocked", "")
    assert result["exit_code"] == 1


def test_update_tracker_phase_no_userjourney(tmp_path: Path, monkeypatch) -> None:
    """Missing USERJOURNEY dir should return 'not attached' error (covers line 392)."""
    monkeypatch.setattr(programstart_serve, "ROOT", tmp_path)
    result = update_implementation_tracker_phase("2", "Blocked", "")
    assert result["exit_code"] == 1
    assert "not attached" in result["output"]


def test_run_bootstrap_timeout(monkeypatch) -> None:
    """subprocess.TimeoutExpired in run_bootstrap should return a timed-out error."""
    import subprocess

    def _raise_timeout(*args: object, **kwargs: object) -> None:
        raise subprocess.TimeoutExpired("cmd", 60)

    monkeypatch.setattr("scripts.programstart_serve.subprocess.run", _raise_timeout)
    result = programstart_serve.run_bootstrap(
        dest=r"C:\Temp\testdest",
        project_name="TestProject",
        variant="lite",
        dry_run=True,
    )
    assert result["exit_code"] == 1
    assert "timed out" in result["output"]
