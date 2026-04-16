from __future__ import annotations

import subprocess
import sys
import warnings
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _tracked_devlog_files() -> list[Path]:
    return sorted(path for path in (ROOT / "devlog").rglob("*") if path.is_file())


def _last_touched_at(path: Path) -> datetime | None:
    result = subprocess.run(
        ["git", "log", "-1", "--follow", "--format=%ai", "--", str(path.relative_to(ROOT))],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    stamp = result.stdout.strip()
    if not stamp:
        return None
    return datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S %z")


def test_devlog_retention_policy() -> None:
    now = datetime.now(UTC)
    threshold = timedelta(days=365)
    warning_threshold = timedelta(days=335)
    stale_files: list[str] = []

    for path in _tracked_devlog_files():
        touched = _last_touched_at(path)
        if touched is None:
            continue
        age = now - touched.astimezone(UTC)
        if age > threshold:
            stale_files.append(path.relative_to(ROOT).as_posix())
        elif age > warning_threshold:
            warnings.warn(
                f"devlog retention warning: {path.relative_to(ROOT).as_posix()} is {age.days} days old and approaching archival",
                stacklevel=2,
            )

    assert not stale_files, f"devlog files exceed 12-month retention and should be archived: {stale_files}"


def test_devlog_archive_placeholder_exists() -> None:
    assert (ROOT / "devlog" / "archive" / ".gitkeep").exists()


def test_contributing_documents_devlog_retention_policy() -> None:
    text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "Entries in `devlog/` older than 12 months SHOULD be archived" in text
