from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_dashboard_golden import (
    MAX_DIFF_PIXELS,
    capture_specs,
    compare_or_update,
    count_different_pixels,
    default_artifact_dir,
    default_golden_dir,
)


def test_capture_specs_include_modal_only_for_attached() -> None:
    assert [spec.name for spec in capture_specs(attached=True)] == ["attached-shell", "attached-signoff-modal"]
    assert [spec.name for spec in capture_specs(attached=False)] == ["absent-shell"]


def test_default_golden_dir_points_into_tests_assets() -> None:
    assert default_golden_dir() == ROOT / "tests" / "golden" / "dashboard"


def test_default_artifact_dir_points_into_outputs() -> None:
    assert default_artifact_dir() == ROOT / "outputs" / "golden-failures"


def test_count_different_pixels_detects_exact_matches(tmp_path: Path) -> None:
    first = tmp_path / "first.png"
    second = tmp_path / "second.png"
    Image.new("RGBA", (2, 2), (10, 20, 30, 255)).save(first)
    Image.new("RGBA", (2, 2), (10, 20, 30, 255)).save(second)

    assert count_different_pixels(first, second) == 0


def test_count_different_pixels_counts_changed_pixels(tmp_path: Path) -> None:
    first = tmp_path / "first.png"
    second = tmp_path / "second.png"
    Image.new("RGBA", (2, 2), (10, 20, 30, 255)).save(first)
    changed = Image.new("RGBA", (2, 2), (10, 20, 30, 255))
    changed.putpixel((1, 1), (200, 210, 220, 255))
    changed.save(second)

    assert count_different_pixels(first, second) == 1


def test_compare_or_update_honors_custom_diff_threshold(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    Image.new("RGBA", (2, 2), (10, 20, 30, 255)).save(baseline)
    changed = Image.new("RGBA", (2, 2), (10, 20, 30, 255))
    changed.putpixel((1, 1), (200, 210, 220, 255))

    locator = MagicMock()

    def write_changed_image(*, path: str, animations: str, scale: str) -> None:
        assert animations == "disabled"
        assert scale == "css"
        changed.save(path)

    locator.screenshot.side_effect = write_changed_image

    ok, _detail = compare_or_update(locator, baseline, actual, False, max_diff_pixels=MAX_DIFF_PIXELS)

    assert ok is True


def test_compare_or_update_reports_threshold_mismatch(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    Image.new("RGBA", (2, 2), (10, 20, 30, 255)).save(baseline)
    changed = Image.new("RGBA", (2, 2), (10, 20, 30, 255))
    changed.putpixel((1, 1), (200, 210, 220, 255))

    locator = MagicMock()
    locator.screenshot.side_effect = lambda *, path, animations, scale: changed.save(path)

    ok, detail = compare_or_update(locator, baseline, actual, False, max_diff_pixels=0)

    assert ok is False
    assert "screenshot mismatch (1 px)" in detail
