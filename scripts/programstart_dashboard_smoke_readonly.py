"""Read-only dashboard smoke — safe to run against the root workspace at any time.

Exercises only GET endpoints. Never sends POST requests;
never mutates workspace files, state, or tracker tables.
"""

from __future__ import annotations

import argparse
import urllib.error
import urllib.parse
from pathlib import Path

from programstart_smoke_helpers import (
    choose_port,
    request_json,
    request_text,
    safe_shutdown,
    start_dashboard_server,
    wait_for_server,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only dashboard smoke test.")
    parser.add_argument("--port", type=int, default=0, help="Port to use. Default: choose a free ephemeral port.")
    parser.add_argument("--startup-timeout", type=float, default=12.0, help="Seconds to wait for the server to start.")
    args = parser.parse_args()

    port = choose_port(args.port)
    base_url = f"http://127.0.0.1:{port}"
    process = start_dashboard_server(port=port, cwd=ROOT)

    checks: list[tuple[str, bool, str]] = []
    try:
        wait_for_server(base_url, process, args.startup_timeout)

        # --- GET /api/state ---
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

        # --- GET / (HTML) ---
        html = request_text(base_url, "/")
        for marker in ["Recent Projects", "Workflow Health", "uj-slice-status", "modal-date"]:
            checks.append((f"GET / marker {marker}", marker in html, "found" if marker in html else "missing"))

        # --- GET /api/doc (read-only doc preview) ---
        if userjourney_attached:
            doc = request_json(base_url, "/api/doc?path=" + urllib.parse.quote("USERJOURNEY/IMPLEMENTATION_TRACKER.md"))
            checks.append(
                (
                    "GET /api/doc",
                    doc.get("path") == "USERJOURNEY/IMPLEMENTATION_TRACKER.md",
                    doc.get("path", "wrong path"),
                )
            )
        else:
            checks.append(("GET /api/doc skipped", True, "USERJOURNEY not attached"))

    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        checks.append((f"HTTP error {exc.code}", False, body))
    except Exception as exc:
        checks.append(("Smoke test runtime", False, str(exc)))
    finally:
        safe_shutdown(process)

    failures = [item for item in checks if not item[1]]
    for name, ok, detail in checks:
        marker = "PASS" if ok else "FAIL"
        print(f"[{marker}] {name}: {detail}")
    if failures:
        print(f"\nRead-only dashboard smoke test failed: {len(failures)} check(s) failed.")
        return 1
    print(f"\nRead-only dashboard smoke test passed: {len(checks)} check(s) succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
