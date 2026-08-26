from __future__ import annotations

from scripts import programstart_cli


def test_unified_cli_orchestrate_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_run(arguments: list[str]) -> int:
        captured.append(arguments)
        return 0

    monkeypatch.setattr(programstart_cli, "_run_orchestrate", fake_run)

    assert programstart_cli.main(["orchestrate", "--request", "Build the next capability"]) == 0
    assert captured == [["--request", "Build the next capability"]]
