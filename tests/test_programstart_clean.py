from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_clean import collect_cleanup_targets, main, remove_path


def test_collect_cleanup_targets_includes_default_artifacts(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / ".pytest_cache").mkdir()
    (tmp_path / ".tmp_bootstrap_alpha").mkdir()
    (tmp_path / "programstart_workflow.egg-info").mkdir()
    monkeypatch.setattr("scripts.programstart_clean.ROOT", tmp_path)
    monkeypatch.setattr("scripts.programstart_clean.generated_outputs_root", lambda: tmp_path / "outputs")

    targets = collect_cleanup_targets(include_dist=False, include_outputs=False)

    assert {path.name for path in targets} == {
        ".pytest_cache",
        ".tmp_bootstrap_alpha",
        "programstart_workflow.egg-info",
    }


def test_collect_cleanup_targets_optionally_includes_dist_and_outputs(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "dist").mkdir()
    (tmp_path / "outputs").mkdir()
    monkeypatch.setattr("scripts.programstart_clean.ROOT", tmp_path)
    monkeypatch.setattr("scripts.programstart_clean.generated_outputs_root", lambda: tmp_path / "outputs")

    targets = collect_cleanup_targets(include_dist=True, include_outputs=True)

    assert {path.name for path in targets} == {"dist", "outputs"}


def test_main_dry_run_reports_targets_without_removing(monkeypatch, tmp_path, capsys) -> None:
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    monkeypatch.setattr("scripts.programstart_clean.ROOT", tmp_path)
    monkeypatch.setattr("scripts.programstart_clean.generated_outputs_root", lambda: output_dir)
    monkeypatch.setattr("sys.argv", ["programstart_clean.py", "--dry-run", "--include-outputs"])

    result = main()

    assert result == 0
    assert output_dir.exists()
    assert "Would remove" in capsys.readouterr().out


def test_main_removes_targets(monkeypatch, tmp_path, capsys) -> None:
    cache_dir = tmp_path / ".pytest_cache"
    cache_dir.mkdir()
    monkeypatch.setattr("scripts.programstart_clean.ROOT", tmp_path)
    monkeypatch.setattr("scripts.programstart_clean.generated_outputs_root", lambda: tmp_path / "outputs")
    monkeypatch.setattr("sys.argv", ["programstart_clean.py"])

    result = main()

    assert result == 0
    assert not cache_dir.exists()
    assert "Removed" in capsys.readouterr().out


def test_collect_dist_not_existing(tmp_path: Path, monkeypatch) -> None:
    """include_dist=True when dist/ absent → dist not added to targets."""
    monkeypatch.setattr("scripts.programstart_clean.ROOT", tmp_path)
    monkeypatch.setattr("scripts.programstart_clean.generated_outputs_root", lambda: tmp_path / "outputs")
    targets = collect_cleanup_targets(include_dist=True, include_outputs=False)
    assert all(t.name != "dist" for t in targets)


def test_collect_outputs_not_existing(tmp_path: Path, monkeypatch) -> None:
    """include_outputs=True when outputs/ absent → outputs not added to targets."""
    monkeypatch.setattr("scripts.programstart_clean.ROOT", tmp_path)
    monkeypatch.setattr("scripts.programstart_clean.generated_outputs_root", lambda: tmp_path / "outputs")
    targets = collect_cleanup_targets(include_dist=False, include_outputs=True)
    assert all(t.name != "outputs" for t in targets)


def test_remove_path_unlinks_file(tmp_path: Path) -> None:
    """remove_path on a file calls unlink rather than rmtree."""
    f = tmp_path / "test.txt"
    f.write_text("hello", encoding="utf-8")
    remove_path(f)
    assert not f.exists()


def test_main_no_targets_prints_message(tmp_path: Path, monkeypatch, capsys) -> None:
    """When no artifacts exist, main prints a message and returns 0."""
    monkeypatch.setattr("scripts.programstart_clean.ROOT", tmp_path)
    monkeypatch.setattr("scripts.programstart_clean.generated_outputs_root", lambda: tmp_path / "outputs")
    monkeypatch.setattr("sys.argv", ["programstart_clean.py"])
    result = main()
    assert result == 0
    assert "No disposable artifacts found" in capsys.readouterr().out
