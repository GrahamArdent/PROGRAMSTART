"""Browser-level smoke test for the PROGRAMSTART dashboard.

Uses Playwright (headless Chromium) to exercise the client-side JS layer —
catching regressions like broken select bindings, modal pre-population
failures, and missing DOM elements that the API-level smoke test cannot see.

Usage:
    python scripts/programstart_dashboard_browser_smoke.py
    python scripts/programstart_dashboard_browser_smoke.py --port 7799
    python scripts/programstart_dashboard_browser_smoke.py --headed   # visual
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
SERVER = ROOT / "scripts" / "programstart_serve.py"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def choose_port(port: int) -> int:
    if port > 0:
        return port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_server(base_url: str, process: subprocess.Popen[str], timeout: float) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if process.poll() is not None:
            output = process.stdout.read() if process.stdout else ""
            raise RuntimeError(f"Dashboard server exited early with code {process.returncode}.\n{output}")
        try:
            urllib.request.urlopen(f"{base_url}/api/state", timeout=3)
            return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"Dashboard server did not become ready within {timeout:.1f}s")


def main() -> int:
    parser = argparse.ArgumentParser(description="Browser-level smoke test for the PROGRAMSTART dashboard.")
    parser.add_argument(
        "--port",
        type=int,
        default=0,
        help="Port to use. Default: choose a free ephemeral port.",
    )
    parser.add_argument(
        "--startup-timeout",
        type=float,
        default=15.0,
        help="Seconds to wait for the server to start.",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run with a visible browser window.",
    )
    parser.add_argument(
        "--expect-userjourney",
        choices=["auto", "attached", "absent"],
        default="auto",
        help="Assert whether USERJOURNEY should be attached in this workspace.",
    )
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        print("ERROR: playwright not installed.")
        print("  pip install playwright && playwright install chromium")
        return 1

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

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=not args.headed)
            page = browser.new_page()
            page.goto(base_url, wait_until="domcontentloaded")
            with urllib.request.urlopen(f"{base_url}/api/state", timeout=5) as response:
                state = json.loads(response.read().decode("utf-8"))
            userjourney_attached = bool(state.get("userjourney", {}).get("attached", True))
            expected_attached = (
                userjourney_attached if args.expect_userjourney == "auto" else args.expect_userjourney == "attached"
            )

            checks.append(
                (
                    "USERJOURNEY attachment expectation",
                    userjourney_attached == expected_attached,
                    f"expected {'attached' if expected_attached else 'absent'}, got {'attached' if userjourney_attached else 'absent'}",
                )
            )

            # 1. Page title
            title = page.title()
            checks.append(
                (
                    "Page title",
                    title == "PROGRAMSTART Dashboard",
                    f"got: {title!r}",
                )
            )

            # 2. USERJOURNEY card is visible
            uj_card = page.locator("#card-uj")
            checks.append(
                (
                    "UJ card visible",
                    uj_card.is_visible(),
                    "visible" if uj_card.is_visible() else "not found",
                )
            )

            # 3. Signoff button exists on the UJ card when attached
            uj_signoff_btn = page.locator("#card-uj .actions button", has_text="Signoff")
            checks.append(
                (
                    "UJ Signoff button present",
                    (uj_signoff_btn.count() > 0) if userjourney_attached else True,
                    f"{uj_signoff_btn.count()} found" if userjourney_attached else "USERJOURNEY not attached",
                )
            )

            # 4. Slice status select has the correct 5 option values when attached
            status_options = page.locator("#uj-slice-status option").all_inner_texts()
            expected_opts = {"Pending", "Selected", "Ready", "Blocked", "Completed"}
            actual_opts = set(status_options)
            checks.append(
                (
                    "#uj-slice-status has correct 5 options",
                    (actual_opts == expected_opts) if userjourney_attached else True,
                    f"got: {sorted(actual_opts)}" if userjourney_attached else "USERJOURNEY not attached",
                )
            )

            # 5. Wait for async state hydration (uj-active badge leaves "...")
            try:
                page.wait_for_function(
                    "document.getElementById('uj-active')?.textContent?.trim() !== '...'",
                    timeout=8000,
                )
                state_loaded = True
            except Exception:
                state_loaded = False
            checks.append(
                (
                    "State hydrated (uj-active ≠ '...')",
                    state_loaded,
                    "loaded" if state_loaded else "timeout — state never hydrated",
                )
            )

            # 6. uj-active badge has legible content after hydration
            uj_active_text = page.locator("#uj-active").inner_text().strip()
            checks.append(
                (
                    "#uj-active badge has content",
                    bool(uj_active_text) and uj_active_text != "...",
                    f"text: {uj_active_text!r}",
                )
            )

            # 7. pb-active badge has legible content after hydration
            pb_active_text = page.locator("#pb-active").inner_text().strip()
            checks.append(
                (
                    "#pb-active badge has content",
                    bool(pb_active_text) and pb_active_text != "...",
                    f"text: {pb_active_text!r}",
                )
            )

            uj_exec_summary = page.locator("#uj-exec-summary").inner_text().strip()
            checks.append(
                (
                    "USERJOURNEY execution summary matches mode",
                    (
                        "not attached" not in uj_exec_summary.lower()
                        if userjourney_attached
                        else "programbuild-only mode" in uj_exec_summary.lower()
                    ),
                    f"summary: {uj_exec_summary!r}",
                )
            )

            # 8. Slice select is populated from the canonical tracker when attached
            slice_opts = page.locator("#uj-slice-select option").all_inner_texts()
            slice_opts_ok = any("Slice" in o for o in slice_opts)
            checks.append(
                (
                    "#uj-slice-select populated from tracker",
                    slice_opts_ok if userjourney_attached else True,
                    f"options: {slice_opts[:3]}" if userjourney_attached else "USERJOURNEY not attached",
                )
            )

            # 9. Slice status select value is bound to the active tracker row when attached
            slice_status_val = page.locator("#uj-slice-status").input_value()
            checks.append(
                (
                    "#uj-slice-status value bound to tracker",
                    (slice_status_val in expected_opts) if userjourney_attached else True,
                    f"value: {slice_status_val!r}" if userjourney_attached else "USERJOURNEY not attached",
                )
            )

            if userjourney_attached:
                # 10. Clicking UJ Signoff button opens the advance modal
                uj_signoff_btn.first.click()
                try:
                    page.wait_for_function(
                        "!document.getElementById('advance-modal').classList.contains('hidden')",
                        timeout=3000,
                    )
                    modal_opened = True
                except Exception:
                    modal_opened = False
                checks.append(
                    (
                        "Signoff click opens advance modal",
                        modal_opened,
                        "opened" if modal_opened else "modal stayed hidden",
                    )
                )

                # 11. Modal title reflects signoff mode (not advance mode)
                modal_title = page.locator("#modal-title").inner_text().strip()
                checks.append(
                    (
                        "Modal title contains 'Signoff'",
                        "Signoff" in modal_title,
                        f"title: {modal_title!r}",
                    )
                )

                # 12. Modal date input is pre-populated (not blank)
                modal_date_val = page.locator("#modal-date").input_value()
                checks.append(
                    (
                        "#modal-date is pre-populated",
                        bool(modal_date_val),
                        f"value: {modal_date_val!r}",
                    )
                )

                # 13. Dry-run button is hidden in signoff mode
                dry_btn_display = page.locator("#modal-dry-btn").evaluate("el => getComputedStyle(el).display")
                checks.append(
                    (
                        "Dry-run button hidden in signoff mode",
                        dry_btn_display == "none",
                        f"display: {dry_btn_display!r}",
                    )
                )

                # 14. Cancel button closes the modal
                page.locator("#advance-modal .modal-actions .btn.ghost").first.click()
                try:
                    page.wait_for_function(
                        "document.getElementById('advance-modal').classList.contains('hidden')",
                        timeout=3000,
                    )
                    modal_closed = True
                except Exception:
                    modal_closed = False
                checks.append(
                    (
                        "Cancel closes modal",
                        modal_closed,
                        "closed" if modal_closed else "modal still visible after Cancel",
                    )
                )
            else:
                checks.append(
                    (
                        "USERJOURNEY status badge shows optional mode",
                        page.locator("#uj-active").inner_text().strip() == "Optional attachment not present",
                        f"text: {page.locator('#uj-active').inner_text().strip()!r}",
                    )
                )
                checks.append(("Signoff modal flow skipped", True, "USERJOURNEY not attached"))
                checks.append(("Modal title skipped", True, "USERJOURNEY not attached"))
                checks.append(("Modal date skipped", True, "USERJOURNEY not attached"))
                checks.append(("Dry-run button visibility skipped", True, "USERJOURNEY not attached"))
                checks.append(("Modal close flow skipped", True, "USERJOURNEY not attached"))

            browser.close()

    except Exception as exc:
        checks.append(("Browser smoke runtime", False, str(exc)))
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
        print(f"\nBrowser smoke test failed: {len(failures)} check(s) failed.")
        return 1
    print(f"\nBrowser smoke test passed: {len(checks)} check(s) succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
