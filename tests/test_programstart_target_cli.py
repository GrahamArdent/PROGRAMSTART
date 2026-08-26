from __future__ import annotations

from scripts import programstart_cli


def test_unified_cli_target_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_run_target(arguments: list[str]) -> int:
        captured.append(arguments)
        return 0

    monkeypatch.setattr(programstart_cli, "_run_target", fake_run_target)
    assert programstart_cli.main(["target", "--repo", "../EmailBridge", "status"]) == 0
    assert captured == [["--repo", "../EmailBridge", "status"]]
