from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
SERVER = ROOT / "scripts" / "programstart_serve.py"


def choose_port(port: int) -> int:
    if port > 0:
        return port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request_json(base_url: str, path: str, method: str = "GET", body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(f"{base_url}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def request_text(base_url: str, path: str) -> str:
    with urllib.request.urlopen(f"{base_url}{path}", timeout=10) as response:
        return response.read().decode("utf-8")


def wait_for_server(base_url: str, process: subprocess.Popen[str], timeout: float) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if process.poll() is not None:
            output = process.stdout.read() if process.stdout else ""
            raise RuntimeError(f"Dashboard server exited early with code {process.returncode}.\n{output}")
        try:
            request_json(base_url, "/api/state")
            return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"Dashboard server did not become ready within {timeout:.1f}s")


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test the PROGRAMSTART dashboard APIs.")
    parser.add_argument("--port", type=int, default=0, help="Port to use. Default: choose a free ephemeral port.")
    parser.add_argument("--startup-timeout", type=float, default=12.0, help="Seconds to wait for the server to start.")
    args = parser.parse_args()

    port = choose_port(args.port)
    base_url = f"http://127.0.0.1:{port}"
    env = {**os.environ, "NO_COLOR": "1"}
    process = subprocess.Popen(
        [PYTHON, str(SERVER), "--port", str(port), "--no-open"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    checks: list[tuple[str, bool, str]] = []
    try:
        wait_for_server(base_url, process, args.startup_timeout)

        state = request_json(base_url, "/api/state")
        userjourney_attached = bool(state.get("userjourney", {}).get("attached", True))
        has_execution = bool(state.get("catalog", {}).get("userjourney_execution", {}).get("phase_overview"))
        checks.append(
            (
                "GET /api/state",
                has_execution if userjourney_attached else not has_execution,
                "execution payload present" if userjourney_attached else "USERJOURNEY execution omitted as expected",
            )
        )

        html = request_text(base_url, "/")
        html_markers = ["Recent Projects", "Sync And Drift", "uj-slice-status", "modal-date"]
        for marker in html_markers:
            checks.append((f"GET / marker {marker}", marker in html, "found" if marker in html else "missing"))

        if userjourney_attached:
            doc = request_json(base_url, "/api/doc?path=" + urllib.parse.quote("USERJOURNEY/IMPLEMENTATION_TRACKER.md"))
            checks.append(
                ("GET /api/doc", doc.get("path") == "USERJOURNEY/IMPLEMENTATION_TRACKER.md", doc.get("path", "wrong path"))
            )

            execution = state.get("catalog", {}).get("userjourney_execution", {})
            phase_rows = execution.get("phase_overview", [])
            first_phase = phase_rows[0] if phase_rows else {}
            phase_result = request_json(
                base_url,
                "/api/uj-phase",
                method="POST",
                body={
                    "phase": str(first_phase.get("Phase", "0")),
                    "status": str(first_phase.get("Status", "Planned")),
                    "blockers": str(first_phase.get("Blockers", "")),
                },
            )
            checks.append(("POST /api/uj-phase", phase_result.get("exit_code") == 0, phase_result.get("output", "no output")))

            slice_rows = execution.get("slice_readiness", [])
            active_slice = next(
                (row for row in slice_rows if str(row.get("Status", "")).strip() in {"Selected", "Ready", "Blocked"}),
                slice_rows[0] if slice_rows else {},
            )
            slice_result = request_json(
                base_url,
                "/api/uj-slice",
                method="POST",
                body={
                    "slice": str(active_slice.get("Slice", "Slice 1")),
                    "status": str(active_slice.get("Status", "Pending")),
                    "notes": str(active_slice.get("Notes", "")),
                },
            )
            checks.append(("POST /api/uj-slice", slice_result.get("exit_code") == 0, slice_result.get("output", "no output")))

            active_step = str(state.get("userjourney", {}).get("active", ""))
            active_entry = state.get("userjourney", {}).get("entries", {}).get(active_step, {})
            signoff = active_entry.get("signoff", {})
            signoff_result = request_json(
                base_url,
                "/api/workflow-signoff",
                method="POST",
                body={
                    "system": "userjourney",
                    "decision": str(signoff.get("decision", "")),
                    "date": str(signoff.get("date", "")),
                    "notes": str(signoff.get("notes", "")),
                },
            )
            checks.append(
                ("POST /api/workflow-signoff", signoff_result.get("exit_code") == 0, signoff_result.get("output", "no output"))
            )

            advance_result = request_json(
                base_url,
                "/api/workflow-advance",
                method="POST",
                body={
                    "system": "userjourney",
                    "decision": str(signoff.get("decision", "approved")) or "approved",
                    "date": str(signoff.get("date", date.today().isoformat())) or date.today().isoformat(),
                    "notes": str(signoff.get("notes", "")),
                    "dry_run": True,
                },
            )
            checks.append(
                (
                    "POST /api/workflow-advance dry-run",
                    advance_result.get("exit_code") == 0,
                    advance_result.get("output", "no output"),
                )
            )
        else:
            checks.append(("GET /api/doc skipped", True, "USERJOURNEY not attached"))
            checks.append(("POST /api/uj-phase skipped", True, "USERJOURNEY not attached"))
            checks.append(("POST /api/uj-slice skipped", True, "USERJOURNEY not attached"))
            checks.append(("POST /api/workflow-signoff skipped", True, "USERJOURNEY not attached"))
            checks.append(("POST /api/workflow-advance dry-run skipped", True, "USERJOURNEY not attached"))

    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        checks.append((f"HTTP error {exc.code}", False, body))
    except Exception as exc:
        checks.append(("Smoke test runtime", False, str(exc)))
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

    failures = [item for item in checks if not item[1]]
    for name, ok, detail in checks:
        marker = "PASS" if ok else "FAIL"
        print(f"[{marker}] {name}: {detail}")
    if failures:
        print(f"\nDashboard smoke test failed: {len(failures)} check(s) failed.")
        return 1
    print(f"\nDashboard smoke test passed: {len(checks)} check(s) succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
