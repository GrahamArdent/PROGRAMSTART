"""Loopback server lifecycle and filesystem boundaries use real sockets/files."""

import sys
import threading
from http.server import HTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

from scripts import programstart_common as common
from scripts import programstart_serve as dashboard


@pytest.mark.parametrize("open_browser", [False, True])
def test_main_releases_listener_after_interrupt(monkeypatch, open_browser):
    servers, opened = [], []

    def interrupted(self):
        raise KeyboardInterrupt

    def factory(*args, **kwargs):
        server = HTTPServer(*args, **kwargs)
        servers.append(server)
        return server

    class ImmediateTimer:
        def __init__(self, delay, callback):
            self.callback = callback

        def start(self):
            self.callback()

    monkeypatch.setattr(HTTPServer, "serve_forever", interrupted)
    monkeypatch.setattr(dashboard, "HTTPServer", factory)
    monkeypatch.setattr(dashboard.threading, "Timer", ImmediateTimer)
    monkeypatch.setattr(dashboard.webbrowser, "open", lambda url: opened.append(url))
    monkeypatch.setattr(sys, "argv", ["serve", "--port", "0", *([] if open_browser else ["--no-open"])])
    try:
        assert dashboard.main() == 0
        assert bool(opened) is open_browser
        assert servers[0].fileno() == -1, "owned listening socket must be closed on shutdown"
    finally:
        for server in servers:
            server.server_close()


def test_static_symlink_cannot_escape_dashboard_directory(tmp_path, monkeypatch):
    assets = tmp_path / "dashboard"
    assets.mkdir()
    secret = tmp_path / "outside.css"
    secret.write_text("outside")
    (assets / "style.css").symlink_to(secret)
    monkeypatch.setattr(dashboard, "DASHBOARD_DIR", assets)
    server = HTTPServer(("127.0.0.1", 0), dashboard.DashboardHandler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        with pytest.raises(HTTPError) as exc:
            urlopen(f"http://127.0.0.1:{server.server_port}/static/style.css", timeout=5)
        assert exc.value.code == 403
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


def test_doc_disappearance_after_validation_is_bounded(tmp_path, monkeypatch):
    path = tmp_path / "PROGRAMBUILD/doc.md"
    path.parent.mkdir()
    path.write_text("preview")
    monkeypatch.setattr(dashboard, "ROOT", tmp_path)
    original = Path.stat
    reads = 0

    def disappearing(self, *args, **kwargs):
        nonlocal reads
        if self == path:
            reads += 1
            if reads == 4:
                raise OSError("disappeared after is_file")
        return original(self, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", disappearing)
    assert dashboard.get_doc_preview("PROGRAMBUILD/doc.md") == {"error": "unable to stat file"}


def test_catalog_ignores_blank_identifiers_and_missing_optional_questions(tmp_path, monkeypatch):
    registry = common.load_registry()
    monkeypatch.setattr(common, "ROOT", tmp_path)
    monkeypatch.setattr(dashboard, "ROOT", tmp_path)
    monkeypatch.setattr(dashboard, "load_registry", lambda: registry)
    pb = tmp_path / "PROGRAMBUILD"
    pb.mkdir()
    (tmp_path / "USERJOURNEY").mkdir()
    for name in [
        "PROGRAMBUILD_FILE_INDEX.md",
        "PROGRAMBUILD_KICKOFF_PACKET.md",
        "PROGRAMBUILD_SUBAGENTS.md",
        "PROGRAMBUILD.md",
        "PROGRAMBUILD_LITE.md",
        "PROGRAMBUILD_PRODUCT.md",
        "PROGRAMBUILD_ENTERPRISE.md",
    ]:
        (pb / name).write_text("")
    for name in ["EXECUTION_SLICES.md", "IMPLEMENTATION_TRACKER.md", "FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md"]:
        (tmp_path / "USERJOURNEY" / name).write_text("")
    (pb / "PROGRAMBUILD_FILE_INDEX.md").write_text("## 1. Control Files\n\n| File | Type |\n|---|---|\n| | blank |\n")
    (pb / "PROGRAMBUILD.md").write_text("## 7. Gate Model By Variant\n\n| Variant | Gate style |\n|---|---|\n| | blank |\n")
    result = dashboard.get_state_json()
    assert result["userjourney"]["open_questions"] == 0
    assert result["catalog"]["control_docs"] == []


def test_status_dashboard_relative_output_is_owned_by_workspace(tmp_path, monkeypatch, capsys):
    from scripts import programstart_dashboard as report

    original = report.workspace_path
    monkeypatch.setattr(report, "workspace_path", lambda path: tmp_path / path if path == "report.md" else original(path))
    monkeypatch.setattr(sys, "argv", ["dashboard", "--output", "report.md"])
    assert report.main() == 0
    assert (tmp_path / "report.md").read_text().startswith("#")


@pytest.fixture
def dashboard_state(tmp_path, monkeypatch):
    registry = common.load_registry()
    monkeypatch.setattr(common, "ROOT", tmp_path)
    monkeypatch.setattr(dashboard, "ROOT", tmp_path)
    monkeypatch.setattr(dashboard, "load_registry", lambda: registry)
    for system in ["programbuild", "userjourney"]:
        current = common.create_default_workflow_state(registry, system)
        key = common.workflow_entry_key(system)
        active = "research" if system == "programbuild" else common.workflow_steps(registry, system)[0]
        current[registry["workflow_state"][system]["active_key"]] = active
        for name, entry in current[key].items():
            entry["status"] = "in_progress" if name == active else "planned"
        common.save_workflow_state(registry, system, current)
    return tmp_path, registry


@pytest.mark.parametrize("system", ["programbuild", "userjourney"])
def test_real_state_advance_preserves_already_active_next_step(dashboard_state, system):
    root, registry = dashboard_state
    current = common.load_workflow_state(registry, system)
    active = common.workflow_active_step(registry, system, current)
    steps = common.workflow_steps(registry, system)
    next_step = steps[steps.index(active) + 1]
    current[common.workflow_entry_key(system)][next_step]["status"] = "in_progress"
    common.save_workflow_state(registry, system, current)
    result = dashboard.advance_workflow_with_signoff(system, "approved", "2026-10-20", "fixture", False, gate_result="clear")
    assert result["exit_code"] == 0
    changed = common.load_workflow_state(registry, system)
    assert common.workflow_active_step(registry, system, changed) == next_step
    assert changed[common.workflow_entry_key(system)][next_step]["status"] == "in_progress"


def test_real_objective_enrollment_appearing_under_lock_blocks_advance(dashboard_state, monkeypatch):
    from contextlib import contextmanager

    root, registry = dashboard_state
    before = common.workflow_state_path(registry, "programbuild").read_bytes()
    lock = dashboard.FileLock

    @contextmanager
    def concurrent(*args, **kwargs):
        with lock(*args, **kwargs):
            (root / "PROGRAMBUILD/RESEARCH_EVIDENCE.json").write_text("{}")
            yield

    monkeypatch.setattr(dashboard, "FileLock", concurrent)
    result = dashboard.advance_workflow_with_signoff(
        "programbuild", "approved", "2026-10-20", "fixture", False, gate_result="clear"
    )
    assert result["exit_code"] == 1 and "Objective proof gate blocked" in result["output"]
    assert common.workflow_state_path(registry, "programbuild").read_bytes() == before


def test_locked_advance_rechecks_current_objective_stage(dashboard_state, monkeypatch):
    from contextlib import contextmanager

    root, registry = dashboard_state
    lock = dashboard.FileLock

    @contextmanager
    def concurrent(*args, **kwargs):
        with lock(*args, **kwargs):
            current = common.load_workflow_state(registry, "programbuild")
            current["active_stage"] = "requirements_and_ux"
            common.save_workflow_state(registry, "programbuild", current, acquire_lock=False)
            yield

    monkeypatch.setattr(dashboard, "FileLock", concurrent)
    result = dashboard.advance_workflow_with_signoff(
        "programbuild", "approved", "2026-10-20", "fixture", False, gate_result="clear"
    )
    assert result["exit_code"] == 1
    assert common.load_workflow_state(registry, "programbuild")["active_stage"] == "requirements_and_ux"


def test_tracker_updates_without_metadata_do_not_invent_header(tmp_path, monkeypatch):
    tracker = tmp_path / "USERJOURNEY/IMPLEMENTATION_TRACKER.md"
    tracker.parent.mkdir()
    tracker.write_text("| 0 | Planned | gate | route | none | note |\n| Slice 1 | Pending | none | note |\n")
    monkeypatch.setattr(dashboard, "ROOT", tmp_path)
    assert dashboard.update_implementation_tracker_phase("0", "Completed", "")["exit_code"] == 0
    assert dashboard.update_implementation_tracker_slice("Slice 1", "Ready", "")["exit_code"] == 0
    assert "Last updated:" not in tracker.read_text()


def test_drift_requires_all_authorities_and_ignores_unowned_file(dashboard_state, monkeypatch):
    root, registry = dashboard_state
    registry["sync_rules"] = [
        {
            "name": "all",
            "authority_files": ["a", "b"],
            "dependent_files": ["c"],
            "authority_match": "all",
            "require_authority_when_dependents_change": True,
        }
    ]
    monkeypatch.setattr(dashboard, "git_changed_files", lambda: ["a", "c", "foreign.txt"])
    result = dashboard.build_drift_summary()
    assert any("all required authority" in value for value in result["violations"])


def test_http_rejected_empty_body_and_non_scalar_args_are_bounded(monkeypatch):
    import http.client
    import json

    server = HTTPServer(("127.0.0.1", 0), dashboard.DashboardHandler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        client = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
        monkeypatch.setattr(dashboard, "READONLY_MODE", True)
        client.request("POST", "/api/run", body="")
        assert client.getresponse().status == 405
        client.close()
        client = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
        monkeypatch.setattr(dashboard, "READONLY_MODE", False)
        client.request(
            "POST",
            "/api/run",
            body=json.dumps({"command": "absent", "args": [{"not": "scalar"}]}),
            headers={"Content-Type": "application/json"},
        )
        response = client.getresponse()
        payload = json.loads(response.read())
        assert response.status in {200, 400} and payload.get("exit_code") == 1
        client.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


def test_changed_file_owned_by_current_step_is_not_a_future_step_violation(dashboard_state, monkeypatch):
    root, registry = dashboard_state
    registry["sync_rules"] = []
    registry["workflow_state"]["programbuild"]["step_files"] = {"research": ["current.md"]}
    monkeypatch.setattr(dashboard, "git_changed_files", lambda: ["current.md"])
    result = dashboard.build_drift_summary()
    assert not any("future step" in value for value in result["violations"])
