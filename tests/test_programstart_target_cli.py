from __future__ import annotations

import sys

from scripts import programstart_cli


def test_unified_cli_target_dispatch(monkeypatch) -> None:
    captured: list[list[str]] = []

    def fake_target_main() -> int:
        captured.append(sys.argv[:])
        return 0

    monkeypatch.setattr(programstart_cli.programstart_target, "main", fake_target_main)
    assert programstart_cli.main(["target", "--repo", "../EmailBridge", "status"]) == 0
    assert captured == [["programstart target", "--repo", "../EmailBridge", "status"]]
