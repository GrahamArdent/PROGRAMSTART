from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from programstart_smoke_helpers import (
    choose_port,
    safe_shutdown,
    start_dashboard_server,
    wait_for_class_state,
    wait_for_server,
    wait_for_text_value,
)

if TYPE_CHECKING:
    from playwright.sync_api import ViewportSize

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
SERVER = ROOT / "scripts" / "programstart_serve.py"

VIEWPORT: ViewportSize = {"width": 1440, "height": 1400}
MAX_DIFF_PIXELS = 20
FREEZE_STYLE = """
*, *::before, *::after {
  animation: none !important;
  transition: none !important;
  caret-color: transparent !important;
  scroll-behavior: auto !important;
}
body {
  background: #f3f4ee !important;
}
#command-output,
#command-output-section,
#guide-section,
#subagents-section,
#kickoff-section,
#execution-section,
#pb-summary,
#uj-summary,
#pb-more-actions,
#uj-more-actions,
#pb-continue-btn,
#pb-advance-btn,
#uj-continue-btn,
#uj-advance-btn,
#doc-preview-overlay,
#bootstrap-modal {
  display: none !important;
}
#card-pb .actions,
#card-pb .disclosure,
#card-uj .actions,
#card-uj .disclosure {
  display: none !important;
}
#golden-frame {
  display: grid;
  gap: 16px;
}
"""


@dataclass(frozen=True, slots=True)
class CaptureSpec:
    name: str
    locator: str


def capture_specs(attached: bool) -> list[CaptureSpec]:
    specs = [CaptureSpec("attached-shell" if attached else "absent-shell", "#golden-frame")]
    if attached:
        specs.append(CaptureSpec("attached-signoff-modal", "#golden-modal-frame .modal"))
    return specs


def default_golden_dir() -> Path:
    return ROOT / "tests" / "golden" / "dashboard"


def default_artifact_dir() -> Path:
    return ROOT / "outputs" / "golden-failures"


def add_golden_styles(page) -> None:
    page.add_style_tag(content=FREEZE_STYLE)


def wait_for_dashboard_state(page, attached: bool) -> None:
    wait_for_text_value(page.locator("#pb-active"), timeout=8.0)
    if attached:
        wait_for_text_value(page.locator("#uj-active"), timeout=8.0)


def normalize_dashboard(page, attached: bool) -> None:
    page.evaluate(
        """
        ({ attached }) => {
          const setText = (selector, text) => {
            const element = document.querySelector(selector);
            if (element) {
              element.textContent = text;
            }
          };

          const setValue = (selector, value) => {
            const element = document.querySelector(selector);
            if (element) {
              element.value = value;
            }
          };

          const pbBar = document.getElementById('pb-bar');
          if (pbBar) pbBar.style.width = '36%';
          const ujBar = document.getElementById('uj-bar');
          if (ujBar) ujBar.style.width = attached ? '44%' : '0%';

          setText('#lastUpdated', 'Updated just now');
          setText('#sb-updated', 'Updated just now');
          setText('#sb-pb', 'healthy');
          setText('#sb-uj', attached ? 'active' : 'optional');
          setText('#sb-blockers', attached ? '5 blockers' : 'optional attachment');
          setText('#pb-variant', 'product');
          setText('#pb-active', 'Stage: preview');
          setText('#pb-progress-label', '4/11 (36%)');
          setText('#uj-active', attached ? 'Phase: preview' : 'Optional attachment not present');
          setText('#uj-progress-label', attached ? '4/9 (44%)' : 'optional attachment');
          setText(
            '#uj-exec-summary',
            attached
              ? 'Current planning phase: preview. Current slice: Slice preview (Ready).'
              : 'USERJOURNEY is not attached. This workspace is operating in PROGRAMBUILD-only mode.',
          );

          const blockerBadge = document.getElementById('uj-blockers');
          if (blockerBadge) {
            blockerBadge.style.display = attached ? '' : 'none';
            blockerBadge.textContent = attached ? '5 blockers' : '';
          }

          const renderSteps = (selector, rows) => {
            const container = document.querySelector(selector);
            if (!container) {
              return;
            }
            container.innerHTML = '';
            for (const row of rows) {
              const div = document.createElement('div');
              div.className = `step${row.status === 'active' ? ' active' : ''}`;
              const signoff = row.signoff ? `<span class="step-signoff">${row.signoff}</span>` : '';
              div.innerHTML = `
                <span class="step-dot ${row.status}"></span>
                <div class="step-body">
                  <span class="step-name${row.status === 'active' ? ' active' : ''}">${row.name}</span>
                  <div class="step-desc">${row.desc}</div>
                </div>
                ${signoff}`;
              container.appendChild(div);
            }
          };

          renderSteps('#pb-steps', [
            { status: 'completed', name: 'Inputs', desc: 'Control files locked', signoff: 'approved · 2026-03-28' },
            { status: 'active', name: 'Feasibility', desc: 'Active checkpoint' },
            { status: 'planned', name: 'Research', desc: 'Next checkpoint' },
          ]);

          renderSteps(
            '#uj-steps',
            attached
              ? [
                  { status: 'completed', name: 'Phase 0', desc: 'Foundations locked', signoff: 'approved · 2026-03-28' },
                  { status: 'active', name: 'Phase 1', desc: 'Consent model review' },
                  { status: 'planned', name: 'Phase 2', desc: 'Activation slice' },
                ]
              : [
                  { status: 'planned', name: 'Optional attachment', desc: 'Attach USERJOURNEY when needed' },
                ],
          );

          const header = document.querySelector('header');
          const main = document.querySelector('main');
          const status = main?.querySelector('.status-bar');
          const row = main?.querySelector('.row');
          let frame = document.getElementById('golden-frame');
          if (!frame) {
            frame = document.createElement('div');
            frame.id = 'golden-frame';
          }
          if (header) frame.appendChild(header);
          if (status) frame.appendChild(status);
          if (row) frame.appendChild(row);
          document.body.prepend(frame);

          setValue('#modal-date', '2026-03-28');
        }
        """,
        {"attached": attached},
    )


def open_and_normalize_modal(page) -> None:
    page.evaluate("openAdvanceModal('userjourney', 'signoff')")
    wait_for_class_state(page.locator("#advance-modal"), class_name="hidden", present=False, timeout=3.0)
    page.evaluate(
        """
        () => {
          const overlay = document.getElementById('advance-modal');
          if (overlay) {
            overlay.scrollTop = 0;
            overlay.style.alignItems = 'flex-start';
            overlay.style.paddingTop = '24px';
          }
          const modal = document.querySelector('#advance-modal .modal');
          if (modal) {
            modal.style.position = 'fixed';
            modal.style.top = '24px';
            modal.style.left = '50%';
            modal.style.margin = '0';
            modal.style.transform = 'translateX(-50%)';
          }

          const setText = (selector, text) => {
            const element = document.querySelector(selector);
            if (element) {
              element.textContent = text;
            }
          };
          const setValue = (selector, value) => {
            const element = document.querySelector(selector);
            if (element) {
              element.value = value;
            }
          };
          const normalizeDateInput = (selector, value) => {
            const element = document.querySelector(selector);
            if (!(element instanceof HTMLInputElement)) {
              return;
            }
            element.type = 'text';
            element.value = value;
            element.inputMode = 'none';
          };

          setText('#modal-title', 'Save USERJOURNEY Phase Signoff');
          setText('#modal-desc', 'Capture a signoff snapshot before advancing implementation.');
          setText('#modal-preflight', 'Preflight checks passed.');
          setValue('#modal-decision', 'approved');
          normalizeDateInput('#modal-date', '2026-03-28');
          setValue('#modal-notes', 'Checkpoint signoff notes.');
          const historySection = document.getElementById('modal-history-section');
          if (historySection) historySection.style.display = 'block';
          setText('#modal-history', 'approved · 2026-03-27\\nblocked · 2026-03-20');

          const modalFrame = document.getElementById('golden-modal-frame') || document.createElement('div');
          modalFrame.id = 'golden-modal-frame';
          modalFrame.innerHTML = '';
          modalFrame.style.display = 'grid';
          modalFrame.style.justifyItems = 'center';
          modalFrame.style.paddingTop = '24px';
          modalFrame.style.background = '#f3f4ee';
          if (modal) {
            const clone = modal.cloneNode(true);
            clone.style.position = 'static';
            clone.style.top = 'auto';
            clone.style.left = 'auto';
            clone.style.margin = '0';
            clone.style.transform = 'none';
            modalFrame.appendChild(clone);
          }
          document.body.prepend(modalFrame);
        }
        """
    )


def count_different_pixels(baseline_path: Path, actual_path: Path) -> int:
    from PIL import Image as PILImage  # noqa: PLC0415
    from PIL import ImageChops  # noqa: PLC0415

    with PILImage.open(baseline_path) as baseline_image, PILImage.open(actual_path) as actual_image:
        baseline_rgba = baseline_image.convert("RGBA")
        actual_rgba = actual_image.convert("RGBA")
        if baseline_rgba.size != actual_rgba.size:
            return -1

        diff = ImageChops.difference(baseline_rgba, actual_rgba)
        width, height = diff.size
        return int(sum(1 for y in range(height) for x in range(width) if diff.getpixel((x, y)) != (0, 0, 0, 0)))


def compare_or_update(
    locator,
    baseline_path: Path,
    actual_path: Path,
    update: bool,
    max_diff_pixels: int,
) -> tuple[bool, str]:
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    actual_path.parent.mkdir(parents=True, exist_ok=True)
    locator.scroll_into_view_if_needed()
    locator.screenshot(path=str(actual_path), animations="disabled", scale="css")
    if update:
        actual_path.replace(baseline_path)
        return True, f"updated {baseline_path.name}"
    if not baseline_path.exists():
        return False, f"missing baseline {baseline_path.name}; run with --update"
    diff_pixels = count_different_pixels(baseline_path, actual_path)
    if diff_pixels < 0:
        return False, f"screenshot size mismatch; wrote {actual_path.as_posix()}"
    if diff_pixels > max_diff_pixels:
        return False, f"screenshot mismatch ({diff_pixels} px); wrote {actual_path.as_posix()}"
    actual_path.unlink(missing_ok=True)
    return True, baseline_path.name


def main() -> int:
    parser = argparse.ArgumentParser(description="Purpose-based Playwright golden tests for the PROGRAMSTART dashboard.")
    parser.add_argument("--port", type=int, default=0, help="Port to use. Default: choose a free ephemeral port.")
    parser.add_argument("--startup-timeout", type=float, default=15.0, help="Seconds to wait for the server to start.")
    parser.add_argument("--headed", action="store_true", help="Run with a visible browser window.")
    parser.add_argument(
        "--expect-userjourney",
        choices=["auto", "attached", "absent"],
        default="auto",
        help="Assert whether USERJOURNEY should be attached in this workspace.",
    )
    parser.add_argument("--update", action="store_true", help="Refresh the golden screenshots instead of comparing them.")
    parser.add_argument("--golden-dir", default=None, help="Directory containing baseline screenshots.")
    parser.add_argument("--artifact-dir", default=None, help="Directory for mismatch screenshots.")
    parser.add_argument(
        "--max-diff-pixels",
        type=int,
        default=MAX_DIFF_PIXELS,
        help="Maximum pixel difference allowed before a capture fails.",
    )
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        print("ERROR: playwright not installed.")
        print("  pip install playwright && playwright install chromium")
        return 1

    golden_dir = Path(args.golden_dir) if args.golden_dir else default_golden_dir()
    artifact_dir = Path(args.artifact_dir) if args.artifact_dir else default_artifact_dir()
    if not golden_dir.is_absolute():
        golden_dir = ROOT / golden_dir
    if not artifact_dir.is_absolute():
        artifact_dir = ROOT / artifact_dir

    port = choose_port(args.port)
    base_url = f"http://127.0.0.1:{port}"
    process = start_dashboard_server(port=port, cwd=ROOT, server_script=SERVER)

    checks: list[tuple[str, bool, str]] = []
    try:
        wait_for_server(base_url, process, args.startup_timeout)

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=not args.headed)
            page = browser.new_page(viewport=VIEWPORT)
            page.emulate_media(color_scheme="light", reduced_motion="reduce")
            page.goto(base_url, wait_until="domcontentloaded")
            wait_for_dashboard_state(page, attached=False)
            attached = "Optional attachment not present" not in page.locator("#uj-active").inner_text().strip()
            expected_attached = attached if args.expect_userjourney == "auto" else args.expect_userjourney == "attached"
            checks.append(
                (
                    "USERJOURNEY attachment expectation",
                    attached == expected_attached,
                    f"expected {'attached' if expected_attached else 'absent'}, got {'attached' if attached else 'absent'}",
                )
            )
            if attached != expected_attached:
                browser.close()
                for name, ok, detail in checks:
                    marker = "PASS" if ok else "FAIL"
                    print(f"[{marker}] {name}: {detail}")
                print("\nGolden test failed: attachment mode mismatch.")
                return 1

            wait_for_dashboard_state(page, attached=attached)
            add_golden_styles(page)
            normalize_dashboard(page, attached)

            for spec in capture_specs(attached):
                if spec.name == "attached-signoff-modal":
                    open_and_normalize_modal(page)
                locator = page.locator(spec.locator)
                baseline_path = golden_dir / f"{spec.name}.png"
                actual_path = artifact_dir / f"{spec.name}.actual.png"
                ok, detail = compare_or_update(
                    locator,
                    baseline_path,
                    actual_path,
                    args.update,
                    args.max_diff_pixels,
                )
                checks.append((spec.name, ok, detail))

            browser.close()
    except Exception as exc:
        checks.append(("Golden runtime", False, str(exc)))
    finally:
        safe_shutdown(process)

    failures = [item for item in checks if not item[1]]
    for name, ok, detail in checks:
        marker = "PASS" if ok else "FAIL"
        print(f"[{marker}] {name}: {detail}")
    if failures:
        print(f"\nGolden test failed: {len(failures)} capture(s) mismatched.")
        return 1
    print(f"\nGolden test passed: {len(checks)} check(s) succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
