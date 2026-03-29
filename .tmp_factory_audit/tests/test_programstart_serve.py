from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_serve import ALLOWED_COMMANDS, run_command, strip_ansi


def test_allowed_commands_contains_core_entries() -> None:
    assert "state.show" in ALLOWED_COMMANDS
    assert "validate" in ALLOWED_COMMANDS
    assert "status" in ALLOWED_COMMANDS
    assert "guide.programbuild" in ALLOWED_COMMANDS
    assert "guide.kickoff" in ALLOWED_COMMANDS
    assert "log" in ALLOWED_COMMANDS
    assert "drift" in ALLOWED_COMMANDS
    assert "progress" in ALLOWED_COMMANDS
    assert ALLOWED_COMMANDS["status"][:3] == [sys.executable, "-m", "scripts.programstart_cli"]


def test_run_command_unknown_returns_error() -> None:
    result = run_command("nonexistent.command")
    assert result["exit_code"] == 1
    assert "unknown command" in result["output"]


def test_run_command_rejects_disallowed_extra_args() -> None:
    result = run_command("status", ["--evil-arg"])
    assert result["exit_code"] == 1
    assert "not permitted" in result["output"]


def test_run_command_status_succeeds() -> None:
    result = run_command("status")
    assert result["exit_code"] == 0
    assert "PROGRAMBUILD" in result["output"]


def test_run_command_validate_succeeds() -> None:
    result = run_command("validate")
    assert result["exit_code"] == 0


def test_strip_ansi_removes_escape_codes() -> None:
    assert strip_ansi("\033[32mgreen\033[0m") == "green"
    assert strip_ansi("plain text") == "plain text"
    assert strip_ansi("\033[1;31mbold red\033[0m") == "bold red"


def test_allowed_commands_all_have_list_values() -> None:
    for key, value in ALLOWED_COMMANDS.items():
        assert isinstance(value, list), f"{key} should be a list"
        assert len(value) >= 1, f"{key} should have at least one element"
