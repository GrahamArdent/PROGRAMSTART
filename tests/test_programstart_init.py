from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_init as init_script


# ── replace_starter_inputs_block ──────────────────────────────────────────────

_KICKOFF_TEMPLATE = """\
# PROGRAMBUILD Kickoff Packet

```text
PROJECT_NAME: PLACEHOLDER
ONE_LINE_DESCRIPTION: PLACEHOLDER
PRODUCT_SHAPE: PLACEHOLDER
```

Additional content here.
"""


def test_replace_starter_inputs_block_updates_values(tmp_path: Path) -> None:
    path = tmp_path / "kickoff.md"
    path.write_text(_KICKOFF_TEMPLATE, encoding="utf-8")
    init_script.replace_starter_inputs_block(path, {"PROJECT_NAME": "MyApp", "PRODUCT_SHAPE": "web app"})
    text = path.read_text(encoding="utf-8")
    assert "PROJECT_NAME: MyApp" in text
    assert "PRODUCT_SHAPE: web app" in text


def test_replace_starter_inputs_block_preserves_surrounding_content(tmp_path: Path) -> None:
    path = tmp_path / "kickoff.md"
    path.write_text(_KICKOFF_TEMPLATE, encoding="utf-8")
    init_script.replace_starter_inputs_block(path, {"PROJECT_NAME": "Zeta"})
    text = path.read_text(encoding="utf-8")
    assert "# PROGRAMBUILD Kickoff Packet" in text
    assert "Additional content here." in text


def test_replace_starter_inputs_block_only_replaces_first_block(tmp_path: Path) -> None:
    content = (
        "```text\nKEY: value1\n```\n\nOther:\n\n```text\nKEY: value2\n```\n"
    )
    path = tmp_path / "doc.md"
    path.write_text(content, encoding="utf-8")
    init_script.replace_starter_inputs_block(path, {"KEY": "replaced"})
    text = path.read_text(encoding="utf-8")
    # First block replaced
    assert "KEY: replaced" in text
    # Second block untouched
    assert "KEY: value2" in text


# ── write_project_readme ───────────────────────────────────────────────────────

def test_write_project_readme_contains_project_name(tmp_path: Path) -> None:
    path = tmp_path / "README.md"
    init_script.write_project_readme(
        path,
        project_name="Acme Platform",
        one_line_description="A great product.",
        variant="product",
        product_shape="web app",
        attach_userjourney_enabled=True,
    )
    text = path.read_text(encoding="utf-8")
    assert "Acme Platform" in text


def test_write_project_readme_contains_variant_and_shape(tmp_path: Path) -> None:
    path = tmp_path / "README.md"
    init_script.write_project_readme(
        path,
        project_name="TestProject",
        one_line_description="",
        variant="enterprise",
        product_shape="api service",
        attach_userjourney_enabled=False,
    )
    text = path.read_text(encoding="utf-8")
    assert "enterprise" in text
    assert "api service" in text


def test_write_project_readme_shows_userjourney_attachment_status(tmp_path: Path) -> None:
    path = tmp_path / "README.md"
    init_script.write_project_readme(
        path,
        project_name="WithJourney",
        one_line_description="",
        variant="product",
        product_shape="web app",
        attach_userjourney_enabled=True,
    )
    text = path.read_text(encoding="utf-8")
    assert "yes" in text


def test_write_project_readme_shows_no_when_userjourney_not_attached(tmp_path: Path) -> None:
    path = tmp_path / "README.md"
    init_script.write_project_readme(
        path,
        project_name="NoJourney",
        one_line_description="",
        variant="lite",
        product_shape="cli tool",
        attach_userjourney_enabled=False,
    )
    text = path.read_text(encoding="utf-8")
    assert "no" in text


def test_write_project_readme_uses_one_line_description(tmp_path: Path) -> None:
    path = tmp_path / "README.md"
    init_script.write_project_readme(
        path,
        project_name="Demo",
        one_line_description="A real-time analytics engine.",
        variant="product",
        product_shape="api service",
        attach_userjourney_enabled=False,
    )
    text = path.read_text(encoding="utf-8")
    assert "A real-time analytics engine." in text


# ── main (integration via mocked dependencies) ────────────────────────────────

def test_main_returns_one_on_bootstrap_fileexistserror(tmp_path: Path) -> None:
    dest = tmp_path / "dest"
    with patch.object(
        init_script, "bootstrap_repository", side_effect=FileExistsError("already exists")
    ):
        result = init_script.main(
            [
                "--dest", str(dest),
                "--project-name", "MyApp",
                "--product-shape", "web app",
            ]
        )
    assert result == 1


def test_main_dry_run_prints_stamp_lines(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    dest = tmp_path / "dest"
    with patch.object(init_script, "bootstrap_repository"):
        result = init_script.main(
            [
                "--dest", str(dest),
                "--project-name", "DryApp",
                "--product-shape", "cli tool",
                "--dry-run",
            ]
        )
    captured = capsys.readouterr()
    assert result == 0
    assert "STAMP" in captured.out


def test_main_stamps_kickoff_packet_and_readme(tmp_path: Path) -> None:
    dest = tmp_path / "dest"
    programbuild = dest / "PROGRAMBUILD"
    programbuild.mkdir(parents=True)
    kickoff = programbuild / "PROGRAMBUILD_KICKOFF_PACKET.md"
    kickoff.write_text("```text\nPROJECT_NAME: PLACEHOLDER\n```\n", encoding="utf-8")

    with (
        patch.object(init_script, "bootstrap_repository"),
        patch.object(init_script, "refresh_secrets_baseline"),
    ):
        result = init_script.main(
            [
                "--dest", str(dest),
                "--project-name", "RealApp",
                "--product-shape", "web app",
            ]
        )
    assert result == 0
    assert (dest / "README.md").exists()
    kickoff_text = kickoff.read_text(encoding="utf-8")
    assert "PROJECT_NAME: RealApp" in kickoff_text


def test_main_calls_stamp_owner_when_owner_provided(tmp_path: Path) -> None:
    dest = tmp_path / "dest"
    programbuild = dest / "PROGRAMBUILD"
    programbuild.mkdir(parents=True)
    kickoff = programbuild / "PROGRAMBUILD_KICKOFF_PACKET.md"
    kickoff.write_text("```text\nPROJECT_NAME: PLACEHOLDER\n```\n", encoding="utf-8")

    with (
        patch.object(init_script, "bootstrap_repository"),
        patch.object(init_script, "refresh_secrets_baseline"),
        patch.object(init_script, "stamp_owner_and_dates") as mock_stamp,
    ):
        init_script.main(
            [
                "--dest", str(dest),
                "--project-name", "BrandedApp",
                "--product-shape", "api service",
                "--owner", "Alice",
            ]
        )
    mock_stamp.assert_called_once()
    args, kwargs = mock_stamp.call_args
    assert kwargs.get("owner") == "Alice" or args[1] == "Alice"
