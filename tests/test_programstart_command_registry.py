from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_command_registry import CLI_COMMANDS, build_cli_module_command, dashboard_allowed_commands


def test_build_cli_module_command_uses_unified_cli_module() -> None:
    assert build_cli_module_command("python", ["status", "--system", "programbuild"]) == [
        "python",
        "-m",
        "scripts.programstart_cli",
        "status",
        "--system",
        "programbuild",
    ]


def test_cli_commands_contains_expected_public_commands() -> None:
    assert CLI_COMMANDS == (
        "create",
        "init",
        "attach",
        "backup",
        "recommend",
        "impact",
        "research",
        "status",
        "validate",
        "context",
        "retrieval",
        "kb",
        "state",
        "advance",
        "next",
        "log",
        "prompt-eval",
        "progress",
        "guide",
        "drift",
        "diff",
        "bootstrap",
        "clean",
        "closeout",
        "refresh",
        "dashboard",
        "serve",
        "health",
        "doctor",
        "prompt-build",
        "mutation-edit-hook",
        "mutation-loop",
    )


def test_dashboard_allowed_commands_routes_workflow_actions_through_cli() -> None:
    commands = dashboard_allowed_commands("python", ROOT / "scripts")

    assert commands["create.dry"] == [
        "python",
        "-m",
        "scripts.programstart_cli",
        "create",
        "--dest",
        ".tmp_dashboard_create",
        "--project-name",
        "DASHBOARD-CREATE",
        "--product-shape",
        "CLI tool",
        "--dry-run",
    ]
    assert commands["status"] == ["python", "-m", "scripts.programstart_cli", "status"]
    assert commands["recommend"] == ["python", "-m", "scripts.programstart_cli", "recommend"]
    assert commands["context.summary"] == ["python", "-m", "scripts.programstart_cli", "context", "query"]
    assert commands["research.python-runtime"] == [
        "python",
        "-m",
        "scripts.programstart_cli",
        "research",
        "--track",
        "Python runtime and packaging",
    ]
    assert commands["prompt-eval"] == ["python", "-m", "scripts.programstart_cli", "prompt-eval", "--json"]
    assert commands["state.show"] == ["python", "-m", "scripts.programstart_cli", "state", "show"]
    assert commands["advance.programbuild"] == [
        "python",
        "-m",
        "scripts.programstart_cli",
        "advance",
        "--system",
        "programbuild",
    ]
    assert commands["smoke.dashboard"][-1].endswith("programstart_dashboard_smoke.py")


def test_vscode_tasks_reference_valid_commands() -> None:
    """Every .vscode/tasks.json task that invokes 'programstart' must use a subcommand in CLI_COMMANDS."""
    tasks_path = ROOT / ".vscode" / "tasks.json"
    tasks_data = json.loads(tasks_path.read_text(encoding="utf-8"))

    checked = 0
    for task in tasks_data["tasks"]:
        args: list[str] = task.get("args", [])
        if "programstart" not in args:
            continue
        idx = args.index("programstart")
        if idx + 1 >= len(args):
            continue
        subcommand = args[idx + 1]
        # Skip flags (e.g. --dry-run) that aren't subcommands
        if subcommand.startswith("-"):
            continue
        assert subcommand in CLI_COMMANDS, f"Task {task['label']!r} uses unknown subcommand {subcommand!r}; valid: {CLI_COMMANDS}"
        checked += 1

    assert checked >= 5, f"Expected at least 5 programstart tasks, found {checked}"
