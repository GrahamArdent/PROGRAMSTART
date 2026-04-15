from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_smoke_helpers import (
    choose_port,
    request_json,
    request_text,
    safe_shutdown,
    start_dashboard_server,
    wait_for_class_state,
    wait_for_server,
    wait_for_text_value,
)


def test_choose_port_returns_positive_for_zero() -> None:
    port = choose_port(0)
    assert isinstance(port, int)
    assert port > 0


def test_choose_port_passes_through_explicit() -> None:
    assert choose_port(8080) == 8080


def test_choose_port_zero_returns_different_ports() -> None:
    """Ephemeral ports should typically differ across calls."""
    ports = {choose_port(0) for _ in range(3)}
    # At least 2 distinct ports out of 3 attempts (extremely unlikely to collide)
    assert len(ports) >= 2


def test_safe_shutdown_terminates_process() -> None:
    proc = MagicMock(spec=subprocess.Popen)
    proc.wait.return_value = 0
    safe_shutdown(proc, timeout=1.0)
    proc.terminate.assert_called_once()
    proc.wait.assert_called_once_with(timeout=1.0)
    proc.kill.assert_not_called()


def test_safe_shutdown_escalates_to_kill() -> None:
    proc = MagicMock(spec=subprocess.Popen)
    proc.wait.side_effect = [subprocess.TimeoutExpired(cmd="test", timeout=1), 0]
    safe_shutdown(proc, timeout=1.0)
    proc.terminate.assert_called_once()
    proc.kill.assert_called_once()
    assert proc.wait.call_count == 2


def test_wait_for_server_raises_on_early_exit() -> None:
    proc = MagicMock(spec=subprocess.Popen)
    proc.poll.return_value = 1
    proc.returncode = 1
    proc.stdout = MagicMock()
    proc.stdout.read.return_value = "crash output"
    with pytest.raises(RuntimeError, match="exited early"):
        wait_for_server("http://127.0.0.1:1", proc, timeout=0.5)


def test_wait_for_server_raises_on_timeout() -> None:
    proc = MagicMock(spec=subprocess.Popen)
    proc.poll.return_value = None  # still running

    with patch("scripts.programstart_smoke_helpers.urllib.request.urlopen", side_effect=ConnectionError):
        with pytest.raises(RuntimeError, match="did not become ready"):
            wait_for_server("http://127.0.0.1:1", proc, timeout=0.3)


def test_start_dashboard_server_returns_popen(tmp_path: Path) -> None:
    """start_dashboard_server returns a Popen-like object (tested via a no-op script)."""
    script = tmp_path / "fake_serve.py"
    script.write_text("import sys; sys.exit(0)\n", encoding="utf-8")
    proc = start_dashboard_server(port=9999, cwd=tmp_path, server_script=script)
    try:
        proc.wait(timeout=5)
    finally:
        if proc.poll() is None:
            proc.kill()
    assert proc.returncode == 0


def test_request_json_parses_response() -> None:
    """request_json should parse a JSON response body."""
    from http.client import HTTPResponse

    mock_response = MagicMock(spec=HTTPResponse)
    mock_response.read.return_value = b'{"ok": true}'
    mock_response.__enter__ = MagicMock(return_value=mock_response)
    mock_response.__exit__ = MagicMock(return_value=False)

    with patch("scripts.programstart_smoke_helpers.urllib.request.urlopen", return_value=mock_response):
        result = request_json("http://localhost:1234", "/api/test")
    assert result == {"ok": True}


def test_request_text_returns_string() -> None:
    from http.client import HTTPResponse

    mock_response = MagicMock(spec=HTTPResponse)
    mock_response.read.return_value = b"hello world"
    mock_response.__enter__ = MagicMock(return_value=mock_response)
    mock_response.__exit__ = MagicMock(return_value=False)

    with patch("scripts.programstart_smoke_helpers.urllib.request.urlopen", return_value=mock_response):
        result = request_text("http://localhost:1234", "/")
    assert result == "hello world"


def test_wait_for_text_value_returns_non_placeholder_text() -> None:
    locator = MagicMock()
    locator.text_content.side_effect = ["...", "ready"]

    result = wait_for_text_value(locator, timeout=0.5, poll_interval=0.0)

    assert result == "ready"


def test_wait_for_class_state_returns_when_expected_membership_met() -> None:
    locator = MagicMock()
    locator.get_attribute.side_effect = ["modal hidden", "modal"]

    wait_for_class_state(locator, class_name="hidden", present=False, timeout=0.5, poll_interval=0.0)
