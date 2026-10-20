"""Unified command forwarding preserves help and missing-runtime diagnostics."""

import builtins
import runpy
from pathlib import Path

import pytest

from scripts import programstart_cli as cli


@pytest.mark.parametrize("command", [name for name in cli.CLI_COMMANDS if name not in {"next", "advance"}])
def test_forwarded_parser_help_is_read_only(command, capsys):
    with pytest.raises(SystemExit) as exc:
        cli.dispatch(command, ["--help"], cli.build_parser())
    assert exc.value.code == 0
    assert "usage:" in capsys.readouterr().out.lower()


def test_raw_script_can_load_lazy_central_runtime_commands(capsys):
    raw = runpy.run_path(str(Path(cli.__file__)), run_name="standalone_probe")
    for name in ["_run_target", "_run_orchestrate"]:
        with pytest.raises(SystemExit) as exc:
            raw[name](["--help"])
        assert exc.value.code == 0
    assert "usage:" in capsys.readouterr().out.lower()


@pytest.mark.parametrize(
    "name,module,reason",
    [
        ("_run_target", "programstart_target", "central PROGRAMSTART control-plane"),
        ("_run_orchestrate", "programstart_orchestrate", "current PROGRAMSTART runtime"),
    ],
)
def test_vendored_runtime_reports_absent_lazy_module(monkeypatch, name, module, reason):
    original = builtins.__import__

    def missing(requested, globals=None, locals=None, fromlist=(), level=0):
        if requested == module or module in (fromlist or ()):
            raise ImportError("runtime module absent")
        return original(requested, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", missing)
    with pytest.raises(SystemExit, match=reason):
        getattr(cli, name)([])


def test_jit_without_applicable_sync_rules_still_runs_real_guide_and_drift(monkeypatch, capsys):
    from scripts import programstart_cli as cli

    registry = cli.load_registry()
    registry["sync_rules"] = []
    monkeypatch.setattr(cli, "load_registry", lambda: registry)
    assert cli.run_jit_check(["--system", "programbuild"]) in {0, 1}
    assert "Sync rules (authority" not in capsys.readouterr().out
