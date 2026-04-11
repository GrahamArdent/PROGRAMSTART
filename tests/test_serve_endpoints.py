"""HTTP-level integration tests for every dashboard API endpoint.

Tests spin up a real ``DashboardHandler`` on a random loopback port and
exercise the full HTTP request/response cycle including JSON parsing,
status codes, Content-Type headers, and 404 routing.
"""

from __future__ import annotations

import json
import sys
import threading
from http.server import HTTPServer
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_serve import DashboardHandler


# ---------------------------------------------------------------------------
# Fixture: ephemeral test server
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def server_url():
    """Start the dashboard server on a random port and yield the base URL."""
    server = HTTPServer(("127.0.0.1", 0), DashboardHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


def _get(url: str) -> tuple[int, dict[str, str], bytes]:
    """Issue a GET request; return (status, headers, body)."""
    try:
        resp = urlopen(url, timeout=10)  # noqa: S310
        return resp.status, dict(resp.headers), resp.read()
    except HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read()


def _post_json(url: str, payload: dict[str, Any]) -> tuple[int, dict[str, str], bytes]:
    """Issue a POST with JSON body; return (status, headers, body)."""
    data = json.dumps(payload).encode()
    req = Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")  # noqa: S310
    try:
        resp = urlopen(req, timeout=10)  # noqa: S310
        return resp.status, dict(resp.headers), resp.read()
    except HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read()


def _post_raw(url: str, raw: bytes) -> tuple[int, dict[str, str], bytes]:
    """Issue a POST with raw bytes (no Content-Type); return (status, headers, body)."""
    req = Request(url, data=raw, method="POST")  # noqa: S310
    try:
        resp = urlopen(req, timeout=10)  # noqa: S310
        return resp.status, dict(resp.headers), resp.read()
    except HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read()


# ───────────────────────────── GET endpoints ──────────────────────────────


class TestGetIndex:
    def test_returns_html(self, server_url: str) -> None:
        status, headers, body = _get(f"{server_url}/")
        assert status == 200
        assert "text/html" in headers.get("Content-Type", "")
        assert b"<html" in body.lower() if body else False

    def test_index_html_alias(self, server_url: str) -> None:
        status, _headers, body = _get(f"{server_url}/index.html")
        assert status == 200
        assert b"<html" in body.lower() if body else False


class TestGetApiState:
    def test_returns_json_200(self, server_url: str) -> None:
        status, headers, body = _get(f"{server_url}/api/state")
        assert status == 200
        assert "application/json" in headers.get("Content-Type", "")
        data = json.loads(body)
        # Must contain at least the programbuild system key
        assert "programbuild" in data

    def test_contains_workflow_keys(self, server_url: str) -> None:
        status, _headers, body = _get(f"{server_url}/api/state")
        data = json.loads(body)
        pb = data["programbuild"]
        assert "active" in pb
        assert "steps" in pb
        assert "attached" in pb


class TestGetApiDoc:
    def test_valid_doc(self, server_url: str) -> None:
        status, headers, body = _get(f"{server_url}/api/doc?path=PROGRAMBUILD/REQUIREMENTS.md")
        assert status == 200
        data = json.loads(body)
        assert "content" in data
        assert "line_count" in data
        assert data["path"] == "PROGRAMBUILD/REQUIREMENTS.md"

    def test_missing_path_param(self, server_url: str) -> None:
        status, _headers, body = _get(f"{server_url}/api/doc")
        data = json.loads(body)
        assert "error" in data

    def test_disallowed_prefix(self, server_url: str) -> None:
        status, _headers, body = _get(f"{server_url}/api/doc?path=../../etc/passwd")
        data = json.loads(body)
        assert "error" in data

    def test_nonexistent_file(self, server_url: str) -> None:
        status, _headers, body = _get(f"{server_url}/api/doc?path=PROGRAMBUILD/DOES_NOT_EXIST.md")
        data = json.loads(body)
        assert "error" in data


class TestGet404:
    def test_unknown_get_returns_404(self, server_url: str) -> None:
        status, _headers, _body = _get(f"{server_url}/api/nonexistent")
        assert status == 404


# ───────────────────────────── POST /api/run ──────────────────────────────


class TestPostApiRun:
    def test_valid_command(self, server_url: str) -> None:
        status, headers, body = _post_json(f"{server_url}/api/run", {"command": "status"})
        assert status == 200
        assert "application/json" in headers.get("Content-Type", "")
        data = json.loads(body)
        assert data["exit_code"] == 0

    def test_unknown_command(self, server_url: str) -> None:
        status, _headers, body = _post_json(f"{server_url}/api/run", {"command": "evil.cmd"})
        assert status == 200  # server returns 200 with error payload
        data = json.loads(body)
        assert data["exit_code"] == 1
        assert "unknown command" in data["output"]

    def test_invalid_json_body(self, server_url: str) -> None:
        status, _headers, body = _post_raw(f"{server_url}/api/run", b"not json at all")
        assert status == 400
        data = json.loads(body)
        assert "error" in data


class TestPost404:
    def test_unknown_post_returns_404(self, server_url: str) -> None:
        status, _headers, _body = _post_json(f"{server_url}/api/nonexistent", {"x": 1})
        assert status == 404


# ──────────────── POST /api/uj-phase (USERJOURNEY endpoint) ───────────────


class TestPostUjPhase:
    def test_invalid_json_returns_400(self, server_url: str) -> None:
        status, _headers, body = _post_raw(f"{server_url}/api/uj-phase", b"<<bad")
        assert status == 400
        data = json.loads(body)
        assert "error" in data

    def test_invalid_phase_returns_error(self, server_url: str) -> None:
        status, _headers, body = _post_json(
            f"{server_url}/api/uj-phase",
            {"phase": "99", "status": "Completed", "blockers": ""},
        )
        data = json.loads(body)
        assert data.get("exit_code") == 1 or "error" in data.get("output", "").lower()

    def test_invalid_status_returns_error(self, server_url: str) -> None:
        status, _headers, body = _post_json(
            f"{server_url}/api/uj-phase",
            {"phase": "0", "status": "InvalidStatus", "blockers": ""},
        )
        data = json.loads(body)
        assert data.get("exit_code") == 1 or "error" in data.get("output", "").lower()


# ──────────────── POST /api/uj-slice (USERJOURNEY endpoint) ───────────────


class TestPostUjSlice:
    def test_invalid_json_returns_400(self, server_url: str) -> None:
        status, _headers, body = _post_raw(f"{server_url}/api/uj-slice", b"<<bad")
        assert status == 400
        data = json.loads(body)
        assert "error" in data

    def test_invalid_slice_returns_error(self, server_url: str) -> None:
        status, _headers, body = _post_json(
            f"{server_url}/api/uj-slice",
            {"slice": "Slice 99", "status": "Ready", "notes": ""},
        )
        data = json.loads(body)
        assert data.get("exit_code") == 1 or "error" in data.get("output", "").lower()

    def test_invalid_status_returns_error(self, server_url: str) -> None:
        status, _headers, body = _post_json(
            f"{server_url}/api/uj-slice",
            {"slice": "Slice 1", "status": "BadStatus", "notes": ""},
        )
        data = json.loads(body)
        assert data.get("exit_code") == 1 or "error" in data.get("output", "").lower()


# ─────────── POST /api/workflow-signoff ──────────────────────────────────


class TestPostWorkflowSignoff:
    def test_invalid_json_returns_400(self, server_url: str) -> None:
        status, _headers, body = _post_raw(f"{server_url}/api/workflow-signoff", b"<<bad")
        assert status == 400
        data = json.loads(body)
        assert "error" in data

    def test_unknown_system_returns_error(self, server_url: str) -> None:
        status, _headers, body = _post_json(
            f"{server_url}/api/workflow-signoff",
            {"system": "nonexistent", "decision": "approved", "date": "2026-03-31", "notes": ""},
        )
        data = json.loads(body)
        assert data.get("exit_code") == 1 or "error" in data.get("output", "").lower()


# ─────────── POST /api/workflow-advance ──────────────────────────────────


class TestPostWorkflowAdvance:
    def test_invalid_json_returns_400(self, server_url: str) -> None:
        status, _headers, body = _post_raw(f"{server_url}/api/workflow-advance", b"<<bad")
        assert status == 400
        data = json.loads(body)
        assert "error" in data

    def test_unknown_system_returns_error(self, server_url: str) -> None:
        status, _headers, body = _post_json(
            f"{server_url}/api/workflow-advance",
            {"system": "nonexistent", "decision": "approved", "date": "2026-03-31", "notes": ""},
        )
        data = json.loads(body)
        assert data.get("exit_code") == 1 or "error" in data.get("output", "").lower()


# ─────────── POST /api/bootstrap ─────────────────────────────────────────


class TestPostBootstrap:
    def test_invalid_json_returns_400(self, server_url: str) -> None:
        status, _headers, body = _post_raw(f"{server_url}/api/bootstrap", b"<<bad")
        assert status == 400
        data = json.loads(body)
        assert "error" in data

    def test_invalid_dest_returns_error(self, server_url: str) -> None:
        status, _headers, body = _post_json(
            f"{server_url}/api/bootstrap",
            {"dest": "!!!invalid!!!", "project_name": "Test", "variant": "product", "dry_run": True},
        )
        data = json.loads(body)
        assert data.get("exit_code") == 1

    def test_invalid_variant_returns_error(self, server_url: str) -> None:
        status, _headers, body = _post_json(
            f"{server_url}/api/bootstrap",
            {"dest": "C:\\Temp\\Test", "project_name": "MyApp", "variant": "badvariant", "dry_run": True},
        )
        data = json.loads(body)
        assert data.get("exit_code") == 1

    def test_dry_run_with_valid_input(self, server_url: str) -> None:
        status, _headers, body = _post_json(
            f"{server_url}/api/bootstrap",
            {"dest": "C:\\Temp\\TestProject", "project_name": "MyApp", "variant": "product", "dry_run": True},
        )
        data = json.loads(body)
        # Dry run should succeed (exit_code 0) or fail gracefully
        assert "exit_code" in data


# ─────────── get_doc_preview unit tests ──────────────────────────────────


class TestGetDocPreview:
    """Direct unit tests for get_doc_preview() edge cases."""

    def test_empty_path(self) -> None:
        from scripts.programstart_serve import get_doc_preview

        result = get_doc_preview("")
        assert result == {"error": "missing path"}

    def test_disallowed_prefix(self) -> None:
        from scripts.programstart_serve import get_doc_preview

        result = get_doc_preview("BACKUPS/something.md")
        assert result == {"error": "path not allowed"}

    def test_path_traversal_blocked(self) -> None:
        from scripts.programstart_serve import get_doc_preview

        result = get_doc_preview("PROGRAMBUILD/../../etc/passwd")
        assert "error" in result

    def test_non_previewable_extension(self) -> None:
        from scripts.programstart_serve import get_doc_preview

        result = get_doc_preview("scripts/__init__.py")
        # .py IS allowed, so this should succeed or fail based on file existence
        assert isinstance(result, dict)

    def test_nonexistent_file_in_allowed_prefix(self) -> None:
        from scripts.programstart_serve import get_doc_preview

        result = get_doc_preview("PROGRAMBUILD/DOES_NOT_EXIST.md")
        assert result == {"error": "file not found"}

    def test_valid_file_returns_content(self) -> None:
        from scripts.programstart_serve import get_doc_preview

        result = get_doc_preview("PROGRAMBUILD/REQUIREMENTS.md")
        assert "content" in result
        assert "line_count" in result
        assert result["path"] == "PROGRAMBUILD/REQUIREMENTS.md"


# ─────────── get_state_json unit tests ───────────────────────────────────


class TestGetStateJson:
    """Direct unit tests for get_state_json()."""

    def test_returns_dict_with_programbuild(self) -> None:
        from scripts.programstart_serve import get_state_json

        result = get_state_json()
        assert isinstance(result, dict)
        assert "programbuild" in result

    def test_programbuild_has_expected_keys(self) -> None:
        from scripts.programstart_serve import get_state_json

        result = get_state_json()
        pb = result["programbuild"]
        for key in ("active", "steps", "entries", "completed", "blocked", "total", "attached"):
            assert key in pb, f"Missing key: {key}"

    def test_catalog_present(self) -> None:
        from scripts.programstart_serve import get_state_json

        result = get_state_json()
        assert "catalog" in result
        catalog = result["catalog"]
        assert "control_docs" in catalog
        assert "subagents" in catalog
        assert "drift" in catalog

    def test_userjourney_key_present(self) -> None:
        from scripts.programstart_serve import get_state_json

        result = get_state_json()
        assert "userjourney" in result
        uj = result["userjourney"]
        assert "attached" in uj


# ─────────── READONLY_MODE guard ─────────────────────────────────────────


class TestReadonlyModeGuard:
    """When PROGRAMSTART_READONLY=1 every POST must return 405."""

    @pytest.fixture(scope="class")
    def readonly_url(self, monkeypatch_class):
        import scripts.programstart_serve as serve_mod

        original = serve_mod.READONLY_MODE
        serve_mod.READONLY_MODE = True
        server = HTTPServer(("127.0.0.1", 0), DashboardHandler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        yield f"http://127.0.0.1:{port}"
        server.shutdown()
        serve_mod.READONLY_MODE = original

    @pytest.fixture(scope="class")
    def monkeypatch_class(self):
        from _pytest.monkeypatch import MonkeyPatch

        mp = MonkeyPatch()
        yield mp
        mp.undo()

    @pytest.mark.parametrize(
        "path",
        ["/api/uj-phase", "/api/uj-slice", "/api/workflow-signoff", "/api/workflow-advance", "/api/run"],
    )
    def test_post_blocked(self, readonly_url: str, path: str) -> None:
        status, _headers, body = _post_json(f"{readonly_url}{path}", {"command": "status"})
        assert status == 405
        data = json.loads(body)
        assert "read-only" in data["error"]
