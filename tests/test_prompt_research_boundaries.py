"""Real evaluation failures and generated prompt lifecycle in temporary outputs."""

import copy
import runpy
from datetime import date, timedelta
from pathlib import Path

import pytest

from scripts import programstart_prompt_build as builder
from scripts import programstart_prompt_eval as evaluation
from scripts import programstart_research_delta as research
from scripts import programstart_validate as validation


def test_scenario_reports_each_missing_requirement():
    scenario = copy.deepcopy(evaluation.load_scenarios()[0])
    scenario.expected_stacks = ["Nonexistent Stack"]
    scenario.required_prompt_terms = ["term-that-is-not-in-any-prompt"]
    scenario.required_plan_sections = ["section-that-does-not-exist"]
    scenario.expected_starter_root = "impossible-root"
    scenario.forbidden_prompt_terms = ["impossible-unseen-term"]
    result = evaluation.evaluate_scenario(scenario)
    assert result["passed"] is False
    for reason in [
        "missing expected stack",
        "generated prompt missing term",
        "factory plan missing section",
        "expected starter root",
    ]:
        assert any(reason in failure for failure in result["failures"])


def test_assessment_reports_missing_files_and_validate_capability(tmp_path, monkeypatch):
    monkeypatch.setattr(evaluation, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.delattr(validation, "validate_required_files")
    results = evaluation.evaluate_assessment_tools({})
    for name, reason in [
        ("assessment_validate_coverage", "missing function"),
        ("assessment_prompt_coverage", "missing assessment prompt"),
        ("assessment_agent_coverage", "missing agent definition"),
    ]:
        result = next(item for item in results if item["name"] == name)
        assert not result["passed"] and any(reason in item for item in result["failures"])


def test_standalone_assessment_uses_compatible_validate_import():
    raw = runpy.run_path(str(Path(evaluation.__file__)), run_name="assessment_probe")
    results = raw["evaluate_assessment_tools"]({})
    assert all(item["passed"] for item in results)


@pytest.mark.parametrize("as_json", [False, True])
def test_managed_prompt_cli_sync_and_eject_real_files(tmp_path, monkeypatch, capsys, as_json):
    registry = copy.deepcopy(builder.load_registry())
    output = tmp_path / "managed.prompt.md"
    registry["prompt_generation"]["managed_stage_prompts"] = [{"stage": "feasibility", "path": str(output)}]
    monkeypatch.setattr(builder, "load_registry", lambda: registry)
    monkeypatch.setattr(builder, "ROOT", tmp_path)
    assert builder.managed_stage_prompts() == [{"stage": "feasibility", "path": str(output)}]
    assert builder.main(["--sync-managed", *(["--json"] if as_json else [])]) == 0
    assert output.read_text().startswith(builder.AUTO_HEADER)
    out = capsys.readouterr().out
    assert "managed.prompt.md" in out
    assert builder.main(["--eject", str(output)]) == 0
    assert not output.read_text().startswith(builder.AUTO_HEADER)
    assert builder.main(["--eject", str(output)]) == 0


def test_research_status_missing_review_and_exact_due_date(monkeypatch):
    model = research.load_knowledge_base_model()
    tracks = model.research_ledger.tracks
    tracks[0].last_review_date = ""
    tracks[1].last_review_date = str(date(2026, 10, 20) - timedelta(days=tracks[1].freshness_days))
    monkeypatch.setattr(research, "load_knowledge_base_model", lambda: model)
    report = research.build_status("2026-10-20")
    assert report.tracks[0].status == "missing_review_date"
    assert report.tracks[1].status == "due_today"
    report.tracks = []
    report.domains = []
    assert research.render_status(report).count("none configured") == 2


def test_research_invalid_review_date_and_relative_output(tmp_path, monkeypatch):
    with pytest.raises(SystemExit, match="Invalid review date"):
        research.mark_track_reviewed("Python runtime and packaging", "invalid-date")
    original = research.workspace_path
    monkeypatch.setattr(
        research, "workspace_path", lambda relative: original(relative) if relative.startswith("config/") else tmp_path / relative
    )
    template = research.build_template("2026-10-20", None, "relative.md")
    assert template.output_path == str(tmp_path / "relative.md")
