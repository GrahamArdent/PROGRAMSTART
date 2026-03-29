from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from scripts import programstart_cli
from scripts.programstart_bootstrap import bootstrap_programbuild, bootstrap_shared_assets
from scripts.programstart_common import create_default_workflow_state, load_registry, workspace_path
from scripts.programstart_validate import (
    validate_bootstrap_assets,
    validate_registry,
    validate_required_files,
    validate_workflow_state,
)

ROOT = Path(__file__).resolve().parents[1]


def run_command(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd or ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_validate_all_passes() -> None:
    result = run_command("scripts/programstart_validate.py", "--check", "all")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Validation passed" in result.stdout
    assert "deprecated" in result.stderr.lower()


def test_bootstrap_repo_stays_programbuild_only(tmp_path: Path) -> None:
    destination = tmp_path / "bootstrapped"
    bootstrap = run_command(
        "scripts/programstart_bootstrap.py",
        "--dest",
        str(destination),
        "--project-name",
        "PytestProj",
        "--variant",
        "product",
    )
    assert bootstrap.returncode == 0, bootstrap.stdout + bootstrap.stderr

    validate = run_command("scripts/programstart_validate.py", "--check", "all", cwd=destination)
    assert validate.returncode == 0, validate.stdout + validate.stderr

    guide = run_command("scripts/programstart_step_guide.py", "--system", "userjourney", cwd=destination)
    assert guide.returncode == 0, guide.stdout + guide.stderr
    assert "not attached" in guide.stdout.lower()


def test_unified_cli_direct_script_warns_and_runs() -> None:
    result = run_command("scripts/programstart_cli.py", "status", "--system", "programbuild")

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PROGRAMBUILD" in result.stdout
    assert "deprecated" in result.stderr.lower()


def test_validation_helpers_pass_on_current_registry() -> None:
    registry = load_registry()
    assert validate_registry(registry) == []
    assert validate_required_files(registry, "programbuild") == []
    assert validate_workflow_state(registry, "programbuild") == []
    assert validate_bootstrap_assets(registry) == []


def test_bootstrap_helpers_copy_core_assets(tmp_path: Path) -> None:
    registry = load_registry()
    destination = tmp_path / "helper-bootstrap"
    bootstrap_shared_assets(destination, registry, dry_run=False)
    bootstrap_programbuild(destination, registry, "product", dry_run=False)

    assert (destination / ".secrets.baseline").exists()
    assert (destination / "pyproject.toml").exists()
    assert (destination / "docs" / "context-layer.md").exists()
    assert (destination / "docs" / "knowledge-base.md").exists()
    assert (destination / "docs" / "retrieval-architecture.md").exists()
    assert (destination / "config" / "knowledge-base.json").exists()
    assert (destination / "QUICKSTART.md").exists()
    assert (destination / "scripts" / "programstart_models.py").exists()
    assert (destination / "scripts" / "programstart_init.py").exists()
    assert (destination / "scripts" / "programstart_attach.py").exists()
    assert (destination / "scripts" / "programstart_recommend.py").exists()
    assert (destination / "scripts" / "programstart_impact.py").exists()
    assert (destination / "scripts" / "programstart_dashboard_golden.py").exists()
    assert (destination / "scripts" / "programstart_context.py").exists()
    assert (destination / "tests" / "golden" / "dashboard" / "absent-shell.png").exists()
    assert (destination / "tests" / "golden" / "dashboard" / "attached-shell.png").exists()
    assert (destination / "tests" / "golden" / "dashboard" / "attached-signoff-modal.png").exists()
    assert (destination / "PROGRAMBUILD" / "PROGRAMBUILD.md").exists()
    assert (destination / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json").exists()
    assert b"\r\n" not in (destination / "scripts" / "programstart_cli.py").read_bytes()


def test_default_programbuild_state_matches_template() -> None:
    registry = load_registry()
    default_state = create_default_workflow_state(registry, "programbuild")
    template_state = workspace_path("PROGRAMBUILD/PROGRAMBUILD_STATE.json").read_text(encoding="utf-8")
    assert default_state["active_stage"] == "inputs_and_mode_selection"
    assert '"active_stage": "inputs_and_mode_selection"' in template_state


def test_unified_cli_status_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_status_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(programstart_cli.programstart_status, "main", fake_status_main)
    assert programstart_cli.main(["status", "--system", "programbuild"]) == 0
    assert captured == [["programstart status", "--system", "programbuild"]]


def test_unified_cli_advance_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_workflow_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(programstart_cli.programstart_workflow_state, "main", fake_workflow_main)
    assert programstart_cli.main(["advance", "--system", "programbuild", "--dry-run"]) == 0
    assert captured == [["programstart advance", "advance", "--system", "programbuild", "--dry-run"]]


def test_unified_cli_next_dispatch(monkeypatch) -> None:
    calls: list[tuple[str, list[str]]] = []

    def fake_status_main() -> int:
        calls.append(("status", sys.argv[:]))
        return 0

    def fake_guide_main() -> int:
        calls.append(("guide", sys.argv[:]))
        return 0

    monkeypatch.setattr(programstart_cli.programstart_status, "main", fake_status_main)
    monkeypatch.setattr(programstart_cli.programstart_step_guide, "main", fake_guide_main)
    assert programstart_cli.main(["next"]) == 0
    assert calls == [
        ("status", ["programstart status"]),
        ("guide", ["programstart guide", "--system", "programbuild"]),
        ("guide", ["programstart guide", "--system", "userjourney"]),
    ]


def test_unified_cli_help_command(capsys) -> None:
    assert programstart_cli.main(["help"]) == 0
    assert "Unified PROGRAMSTART command-line interface" in capsys.readouterr().out


def test_unified_cli_next_rejects_extra_args() -> None:
    try:
        programstart_cli.main(["next", "unexpected"])
    except SystemExit as exc:
        assert str(exc) == "'next' does not accept additional arguments"
    else:
        raise AssertionError("Expected SystemExit for extra next arguments")


@pytest.mark.parametrize(
    ("command", "module_name", "argv0", "arguments", "expected_argv"),
    [
        (
            "init",
            "programstart_init",
            "programstart init",
            ["--dest", "tmp", "--project-name", "x", "--product-shape", "CLI tool", "--dry-run"],
            ["programstart init", "--dest", "tmp", "--project-name", "x", "--product-shape", "CLI tool", "--dry-run"],
        ),
        (
            "attach",
            "programstart_attach",
            "programstart attach",
            ["userjourney", "--source", "template/USERJOURNEY", "--dry-run"],
            ["programstart attach", "userjourney", "--source", "template/USERJOURNEY", "--dry-run"],
        ),
        (
            "recommend",
            "programstart_recommend",
            "programstart recommend",
            ["--product-shape", "CLI tool"],
            ["programstart recommend", "--product-shape", "CLI tool"],
        ),
        (
            "impact",
            "programstart_impact",
            "programstart impact",
            ["workflow"],
            ["programstart impact", "workflow"],
        ),
        (
            "context",
            "programstart_context",
            "programstart context",
            ["query", "--concern", "activation"],
            ["programstart context", "query", "--concern", "activation"],
        ),
        (
            "validate",
            "programstart_validate",
            "programstart validate",
            ["--check", "all"],
            ["programstart validate", "--check", "all"],
        ),
        ("state", "programstart_workflow_state", "programstart state", ["show"], ["programstart state", "show"]),
        (
            "log",
            "programstart_log",
            "programstart log",
            ["--action", "edited"],
            ["programstart log", "--action", "edited"],
        ),
        ("progress", "programstart_checklist_progress", "programstart progress", [], ["programstart progress"]),
        (
            "guide",
            "programstart_step_guide",
            "programstart guide",
            ["--system", "programbuild"],
            ["programstart guide", "--system", "programbuild"],
        ),
        ("drift", "programstart_drift_check", "programstart drift", [], ["programstart drift"]),
        (
            "bootstrap",
            "programstart_bootstrap",
            "programstart bootstrap",
            ["--dest", "tmp"],
            ["programstart bootstrap", "--dest", "tmp"],
        ),
        (
            "clean",
            "programstart_clean",
            "programstart clean",
            ["--dry-run"],
            ["programstart clean", "--dry-run"],
        ),
        ("refresh", "programstart_refresh_integrity", "programstart refresh", [], ["programstart refresh"]),
        (
            "dashboard",
            "programstart_dashboard",
            "programstart dashboard",
            ["--port", "9000"],
            ["programstart dashboard", "--port", "9000"],
        ),
        (
            "serve",
            "programstart_serve",
            "programstart serve",
            ["--host", "127.0.0.1"],
            ["programstart serve", "--host", "127.0.0.1"],
        ),
    ],
)
def test_unified_cli_passthrough_commands(
    monkeypatch,
    command: str,
    module_name: str,
    argv0: str,
    arguments: list[str],
    expected_argv: list[str],
) -> None:
    captured: list[list[str]] = []

    def fake_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(getattr(programstart_cli, module_name), "main", fake_main)
    assert programstart_cli.main([command, *arguments]) == 0
    assert captured == [expected_argv]


def test_unified_cli_dispatch_rejects_unknown_command() -> None:
    parser = programstart_cli.build_parser()

    with pytest.raises(SystemExit, match="Unknown command: unknown"):
        programstart_cli.dispatch("unknown", [], parser)
