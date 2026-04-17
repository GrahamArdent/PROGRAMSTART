from __future__ import annotations

import json
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


# --- Scenario generators produce valid Python ---


@pytest.mark.parametrize("scenario", edit_hook.SCENARIOS, ids=[s.name for s in edit_hook.SCENARIOS])
def test_scenario_renders_valid_python(scenario: edit_hook.GeneratedScenario) -> None:
    code = scenario.render()
    assert code.strip(), f"Scenario {scenario.name} produced empty output"
    compile(code, f"<{scenario.name}>", "exec")


# --- current_hotspots ---


def test_current_hotspots_returns_empty_when_no_meta(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(edit_hook, "workspace_path", lambda relative: tmp_path / relative)
    assert edit_hook.current_hotspots() == []


def test_current_hotspots_returns_empty_on_bad_json(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(edit_hook, "workspace_path", lambda relative: tmp_path / relative)
    meta = tmp_path / "mutants" / "scripts" / "programstart_recommend.py.meta"
    meta.parent.mkdir(parents=True)
    meta.write_text("not-json!", encoding="utf-8")
    assert edit_hook.current_hotspots() == []


def test_current_hotspots_counts_survivors(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(edit_hook, "workspace_path", lambda relative: tmp_path / relative)
    meta = tmp_path / "mutants" / "scripts" / "programstart_recommend.py.meta"
    meta.parent.mkdir(parents=True)
    meta.write_text(
        json.dumps(
            {
                "exit_code_by_key": {
                    "scripts.programstart_recommend.x_build_stack_candidates__mutmut_1": 0,
                    "scripts.programstart_recommend.x_build_stack_candidates__mutmut_2": 0,
                    "scripts.programstart_recommend.x_main__mutmut_1": 1,
                }
            }
        ),
        encoding="utf-8",
    )
    result = edit_hook.current_hotspots(limit=5)
    assert result == ["build_stack_candidates"]


# --- append_scenario / record_application ---


def test_append_scenario_creates_file(tmp_path: Path) -> None:
    target = tmp_path / "test_file.py"
    edit_hook.append_scenario(target, "def test_hello(): pass")
    text = target.read_text(encoding="utf-8")
    assert "def test_hello(): pass" in text


def test_append_scenario_appends_to_existing(tmp_path: Path) -> None:
    target = tmp_path / "test_file.py"
    target.write_text("# existing\n", encoding="utf-8")
    edit_hook.append_scenario(target, "def test_new(): pass")
    text = target.read_text(encoding="utf-8")
    assert "# existing" in text
    assert "def test_new(): pass" in text


def test_record_application_writes_jsonl(tmp_path: Path) -> None:
    history = tmp_path / "history.jsonl"
    scenario = edit_hook.SCENARIOS[0]
    edit_hook.record_application(
        history, scenario=scenario, hotspots=["build_stack_candidates"], target_file=tmp_path / "test.py"
    )
    data = json.loads(history.read_text(encoding="utf-8").strip())
    assert data["scenario"] == scenario.name


# --- run_external_command ---


def test_run_external_command_dispatches(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(edit_hook, "workspace_path", lambda relative: tmp_path / relative)
    import subprocess

    monkeypatch.setattr(subprocess, "call", lambda *_a, **_kw: 42)
    result = edit_hook.run_external_command("echo", tmp_path / "prompt.md")
    assert result == 42


# --- main with --command ---


def test_main_with_external_command(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(edit_hook, "workspace_path", lambda relative: tmp_path / relative)
    import subprocess

    monkeypatch.setattr(subprocess, "call", lambda *_a, **_kw: 0)
    result = edit_hook.main(["--command", "echo"])
    assert result == 0


def test_main_picks_up_env_command(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(edit_hook, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setenv("PROGRAMSTART_MUTATION_EDIT_COMMAND", "echo")
    import subprocess

    monkeypatch.setattr(subprocess, "call", lambda *_a, **_kw: 0)
    result = edit_hook.main([])
    assert result == 0


# --- existing_test_names ---


def test_existing_test_names_returns_empty_for_missing_file(tmp_path: Path) -> None:
    assert edit_hook.existing_test_names(tmp_path / "no_such.py") == set()
