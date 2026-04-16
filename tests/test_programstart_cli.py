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

    engineering_ready = run_command("scripts/programstart_validate.py", "--check", "engineering-ready", cwd=destination)
    assert engineering_ready.returncode == 0, engineering_ready.stdout + engineering_ready.stderr

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
    assert (destination / "docs" / "knowledge-ops.md").exists()
    assert (destination / "docs" / "retrieval-architecture.md").exists()
    assert (destination / "config" / "knowledge-base.json").exists()
    assert (destination / "QUICKSTART.md").exists()
    assert (destination / "scripts" / "programstart_models.py").exists()
    assert (destination / "scripts" / "programstart_init.py").exists()
    assert (destination / "scripts" / "programstart_attach.py").exists()
    assert (destination / "scripts" / "programstart_mutation_edit_hook.py").exists()
    assert (destination / "scripts" / "programstart_mutation_loop.py").exists()
    assert (destination / "scripts" / "programstart_recommend.py").exists()
    assert (destination / "scripts" / "programstart_research_delta.py").exists()
    assert (destination / "scripts" / "programstart_impact.py").exists()
    assert (destination / "scripts" / "programstart_dashboard_golden.py").exists()
    assert (destination / "scripts" / "programstart_context.py").exists()
    assert (destination / "tests" / "golden" / "dashboard" / "absent-shell.png").exists()
    assert (destination / "tests" / "golden" / "dashboard" / "attached-shell.png").exists()
    assert (destination / "tests" / "golden" / "dashboard" / "attached-signoff-modal.png").exists()
    assert (destination / "tests" / "test_programstart_mutation_edit_hook.py").exists()
    assert (destination / "tests" / "test_programstart_mutation_loop.py").exists()
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


def test_unified_cli_kb_search_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_retrieval_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(programstart_cli.programstart_retrieval, "main", fake_retrieval_main)
    assert programstart_cli.main(["kb", "search", "architecture"]) == 0
    assert captured == [["programstart kb", "search", "architecture"]]


def test_unified_cli_kb_ask_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_retrieval_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(programstart_cli.programstart_retrieval, "main", fake_retrieval_main)
    assert programstart_cli.main(["kb", "ask", "What is the architecture?"]) == 0
    assert captured == [["programstart kb", "ask", "What is the architecture?"]]


def test_unified_cli_diff_dispatch_translates_from_to(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_workflow_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(programstart_cli.programstart_workflow_state, "main", fake_workflow_main)
    assert programstart_cli.main(["diff", "--from", "old.json", "--to", "new.json"]) == 0
    assert captured == [["programstart diff", "diff", "--old", "old.json", "--new", "new.json"]]


def test_unified_cli_next_dispatch(monkeypatch) -> None:
    calls: list[tuple[str, list[str]]] = []

    def fake_status_main() -> int:
        calls.append(("status", sys.argv[:]))
        return 0

    def fake_guide_main() -> int:
        calls.append(("guide", sys.argv[:]))
        return 0

    def fake_drift_main() -> int:
        calls.append(("drift", sys.argv[:]))
        return 0

    monkeypatch.setattr(programstart_cli.programstart_status, "main", fake_status_main)
    monkeypatch.setattr(programstart_cli.programstart_step_guide, "main", fake_guide_main)
    monkeypatch.setattr(programstart_cli.programstart_drift_check, "main", fake_drift_main)
    assert programstart_cli.main(["next"]) == 0
    assert calls == [
        ("status", ["programstart status"]),
        ("guide", ["programstart guide", "--system", "programbuild"]),
        ("guide", ["programstart guide", "--system", "userjourney"]),
        ("drift", ["programstart drift"]),
    ]


def test_unified_cli_create_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_create_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(programstart_cli.programstart_create, "main", fake_create_main)
    assert programstart_cli.main(["create", "--dest", "tmp", "--project-name", "x", "--product-shape", "CLI tool"]) == 0
    assert captured == [["programstart create", "--dest", "tmp", "--project-name", "x", "--product-shape", "CLI tool"]]


def test_unified_cli_backup_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_backup_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(programstart_cli.programstart_backup, "main", fake_backup_main)
    assert programstart_cli.main(["backup", "create", "--label", "phase-i"]) == 0
    assert captured == [["programstart backup", "create", "--label", "phase-i"]]


def test_unified_cli_prompt_eval_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_prompt_eval_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(programstart_cli.programstart_prompt_eval, "main", fake_prompt_eval_main)
    assert programstart_cli.main(["prompt-eval", "--json"]) == 0
    assert captured == [["programstart prompt-eval", "--json"]]


def test_unified_cli_closeout_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_closeout_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(programstart_cli.programstart_closeout, "main", fake_closeout_main)
    assert programstart_cli.main(["closeout", "--label", "phase-k1", "--adr-result", "not-required"]) == 0
    assert captured == [["programstart closeout", "--label", "phase-k1", "--adr-result", "not-required"]]


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
            "create",
            "programstart_create",
            "programstart create",
            ["--dest", "tmp", "--project-name", "x", "--product-shape", "CLI tool", "--dry-run"],
            ["programstart create", "--dest", "tmp", "--project-name", "x", "--product-shape", "CLI tool", "--dry-run"],
        ),
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
            "research",
            "programstart_research_delta",
            "programstart research",
            ["--track", "Python runtime and packaging"],
            ["programstart research", "--track", "Python runtime and packaging"],
        ),
        (
            "context",
            "programstart_context",
            "programstart context",
            ["query", "--concern", "activation"],
            ["programstart context", "query", "--concern", "activation"],
        ),
        (
            "kb",
            "programstart_retrieval",
            "programstart kb",
            ["search", "architecture"],
            ["programstart kb", "search", "architecture"],
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
            "diff",
            "programstart_workflow_state",
            "programstart diff",
            ["--old", "a.json", "--new", "b.json"],
            ["programstart diff", "diff", "--old", "a.json", "--new", "b.json"],
        ),
        (
            "log",
            "programstart_log",
            "programstart log",
            ["--action", "edited"],
            ["programstart log", "--action", "edited"],
        ),
        (
            "prompt-eval",
            "programstart_prompt_eval",
            "programstart prompt-eval",
            ["--json"],
            ["programstart prompt-eval", "--json"],
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
        (
            "closeout",
            "programstart_closeout",
            "programstart closeout",
            ["--label", "phase-k1", "--adr-result", "not-required"],
            ["programstart closeout", "--label", "phase-k1", "--adr-result", "not-required"],
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
        (
            "mutation-edit-hook",
            "programstart_mutation_edit_hook",
            "programstart mutation-edit-hook",
            ["--allow-noop"],
            ["programstart mutation-edit-hook", "--allow-noop"],
        ),
        (
            "mutation-loop",
            "programstart_mutation_loop",
            "programstart mutation-loop",
            ["--cycles", "2", "--allow-repeat-without-edits", "--skip-gates"],
            ["programstart mutation-loop", "--cycles", "2", "--allow-repeat-without-edits", "--skip-gates"],
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
