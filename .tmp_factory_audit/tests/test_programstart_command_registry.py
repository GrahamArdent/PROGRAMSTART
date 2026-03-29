from __future__ import annotations

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
        "init",
        "attach",
        "recommend",
        "impact",
        "status",
        "validate",
        "context",
        "retrieval",
        "state",
        "advance",
        "next",
        "log",
        "progress",
        "guide",
        "drift",
        "bootstrap",
        "clean",
        "refresh",
        "dashboard",
        "serve",
    )


def test_dashboard_allowed_commands_routes_workflow_actions_through_cli() -> None:
    commands = dashboard_allowed_commands("python", ROOT / "scripts")

    assert commands["status"] == ["python", "-m", "scripts.programstart_cli", "status"]
    assert commands["recommend"] == ["python", "-m", "scripts.programstart_cli", "recommend"]
    assert commands["context.summary"] == ["python", "-m", "scripts.programstart_cli", "context", "query"]
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
