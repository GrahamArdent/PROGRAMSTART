"""Shared lifecycle helpers for dashboard smoke scripts.

Extracts the duplicated server startup, health polling, port selection,
and shutdown patterns from the three dashboard smoke scripts into a
single testable module.
"""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any


def choose_port(port: int) -> int:
    """Return *port* if positive, otherwise bind an ephemeral port and return it."""
    if port > 0:
        return port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request_json(base_url: str, path: str) -> dict[str, Any]:
    """GET a JSON endpoint and return the parsed body."""
    with urllib.request.urlopen(f"{base_url}{path}", timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def request_text(base_url: str, path: str) -> str:
    """GET an endpoint and return the UTF-8 body."""
    with urllib.request.urlopen(f"{base_url}{path}", timeout=10) as response:
        return response.read().decode("utf-8")


def wait_for_server(
    base_url: str,
    process: subprocess.Popen[str],
    timeout: float,
    *,
    readiness_path: str = "/api/state",
) -> None:
    """Poll *readiness_path* until the server returns HTTP 200 or *timeout* expires."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if process.poll() is not None:
            output = process.stdout.read() if process.stdout else ""
            raise RuntimeError(f"Dashboard server exited early with code {process.returncode}.\n{output}")
        try:
            urllib.request.urlopen(f"{base_url}{readiness_path}", timeout=3)
            return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"Dashboard server did not become ready within {timeout:.1f}s")


def wait_for_text_value(
    locator,
    *,
    placeholder: str = "...",
    timeout: float = 8.0,
    poll_interval: float = 0.1,
) -> str:
    """Poll a Playwright locator until it exposes a non-placeholder text value."""
    deadline = time.time() + timeout
    last_text = ""
    while time.time() < deadline:
        text = locator.text_content()
        last_text = (text or "").strip()
        if last_text and last_text != placeholder:
            return last_text
        time.sleep(poll_interval)
    raise TimeoutError(f"Locator text did not change from {placeholder!r} within {timeout:.1f}s")


def wait_for_class_state(
    locator,
    *,
    class_name: str,
    present: bool,
    timeout: float = 3.0,
    poll_interval: float = 0.05,
) -> None:
    """Poll a Playwright locator until *class_name* is present or absent."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        classes = (locator.get_attribute("class") or "").split()
        if (class_name in classes) is present:
            return
        time.sleep(poll_interval)
    expectation = "present" if present else "absent"
    raise TimeoutError(f"Class {class_name!r} did not become {expectation} within {timeout:.1f}s")


def safe_shutdown(process: subprocess.Popen[str], timeout: float = 5.0) -> None:
    """Terminate *process* gracefully, escalating to kill if it does not stop."""
    process.terminate()
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=timeout)


def start_dashboard_server(
    *,
    port: int,
    cwd: Path,
    server_script: Path | None = None,
    extra_env: dict[str, str] | None = None,
) -> subprocess.Popen[str]:
    """Launch the dashboard server as a subprocess and return the Popen handle."""
    import os  # noqa: PLC0415

    if server_script is None:
        server_script = cwd / "scripts" / "programstart_serve.py"
    env = {**os.environ, "NO_COLOR": "1", **(extra_env or {})}
    return subprocess.Popen(
        [sys.executable, str(server_script), "--port", str(port), "--no-open"],
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
