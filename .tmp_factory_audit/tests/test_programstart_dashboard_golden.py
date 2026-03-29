from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_dashboard_golden import (
    capture_specs,
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
