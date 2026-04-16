from __future__ import annotations

from pathlib import Path

import pytest

from scripts import programstart_mutation_edit_hook as edit_hook


def test_mutation_edit_hook_noop_when_allowed(monkeypatch, capsys, tmp_path: Path) -> None:
    target = tmp_path / "test_programstart_recommend.py"
    target.write_text(
        "\n".join(f"def {scenario.name}() -> None:\n    pass\n" for scenario in edit_hook.SCENARIOS),
        encoding="utf-8",
    )

    assert edit_hook.main(["--allow-noop", "--target-file", str(target)]) == 0
    assert "no-op" in capsys.readouterr().out.lower()


def test_choose_internal_scenario_prefers_hotspot_order() -> None:
    scenario = edit_hook.choose_internal_scenario(
        existing_names={"test_build_stack_candidates_mobile_resilience_exact_output"},
        hotspots=["build_stack_candidates", "main"],
    )

    assert scenario is not None
    assert scenario.name == "test_build_stack_candidates_ops_console_exact_output"


def test_mutation_edit_hook_generates_internal_scenario(monkeypatch, tmp_path: Path, capsys) -> None:
    target = tmp_path / "test_programstart_recommend.py"
    history = tmp_path / "history.jsonl"

    monkeypatch.setattr(edit_hook, "current_hotspots", lambda limit=10: ["select_triggered_entries"])

    assert edit_hook.main(["--target-file", str(target), "--history-file", str(history)]) == 0

    contents = target.read_text(encoding="utf-8")
    assert "def test_select_triggered_entries_cli_tools_exact_output()" in contents
    assert "select_triggered_entries" in contents
    assert "Applied internal mutation scenario" in capsys.readouterr().out

    history_lines = history.read_text(encoding="utf-8").strip().splitlines()
    assert len(history_lines) == 1
    assert "test_select_triggered_entries_cli_tools_exact_output" in history_lines[0]


def test_mutation_edit_hook_requires_internal_scenario_without_allow_noop(tmp_path: Path) -> None:
    target = tmp_path / "test_programstart_recommend.py"
    target.write_text(
        "\n".join(f"def {scenario.name}() -> None:\n    pass\n" for scenario in edit_hook.SCENARIOS),
        encoding="utf-8",
    )

    with pytest.raises(SystemExit, match="No internal mutation scenario remains"):
        edit_hook.main(["--target-file", str(target)])
