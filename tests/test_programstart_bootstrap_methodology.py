from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_bootstrap_methodology as methodology


def test_methodology_bootstrap_reuses_programbuild_without_factory_assets(tmp_path: Path) -> None:
    destination = tmp_path / "project"
    registry = {"systems": {"programbuild": {}}, "workflow_state": {"programbuild": {}}}

    with (
        patch.object(methodology, "load_registry", return_value=registry),
        patch.object(methodology, "ensure_external_project_repo"),
        patch.object(methodology, "bootstrap_programbuild") as bootstrap_programbuild,
        patch.object(methodology, "initialize_git_repository") as initialize_git_repository,
    ):
        methodology.bootstrap_methodology_repository(
            destination,
            project_name="CalendarBridge",
            variant="product",
        )

    readme = (destination / "README.md").read_text(encoding="utf-8")
    assert "CalendarBridge" in readme
    assert "PROGRAMBUILD variant: product" in readme
    assert "PROGRAMSTART's own test suite" in readme
    bootstrap_programbuild.assert_called_once_with(destination, registry, "product", False)
    initialize_git_repository.assert_called_once_with(destination, False)


def test_methodology_bootstrap_rejects_nonempty_destination_without_force(tmp_path: Path) -> None:
    destination = tmp_path / "project"
    destination.mkdir()
    (destination / "existing.txt").write_text("keep", encoding="utf-8")

    with (
        patch.object(methodology, "load_registry", return_value={}),
        patch.object(methodology, "ensure_external_project_repo"),
    ):
        with pytest.raises(FileExistsError, match="--force"):
            methodology.bootstrap_methodology_repository(
                destination,
                project_name="CalendarBridge",
                variant="product",
            )


def test_methodology_readme_dry_run_does_not_create_file(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    methodology.write_methodology_readme(tmp_path, "DryRun", "lite", dry_run=True)
    captured = capsys.readouterr()
    assert "CREATE" in captured.out
    assert not (tmp_path / "README.md").exists()
