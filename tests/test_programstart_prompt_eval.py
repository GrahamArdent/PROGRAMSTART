from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_prompt_eval
from scripts.programstart_prompt_eval import PromptEvalScenario, evaluate_scenario, load_scenarios, main
from scripts.programstart_recommend import ProjectRecommendation


def test_load_scenarios_reads_config() -> None:
    scenarios = load_scenarios()

    assert scenarios
    assert any(item.name == "cli_tool_baseline" for item in scenarios)


def test_evaluate_scenario_passes_for_cli_tool_baseline() -> None:
    scenario = next(item for item in load_scenarios() if item.name == "cli_tool_baseline")

    result = evaluate_scenario(scenario)

    assert result["passed"] is True
    assert result["starter_root"] == "starter/cli_tool"


def test_evaluate_scenario_passes_for_api_service_stack_starter() -> None:
    scenario = next(item for item in load_scenarios() if item.name == "api_service_rag_agents")

    result = evaluate_scenario(scenario)

    assert result["passed"] is True
    assert result["starter_root"] == "starter/api_service"


def test_evaluate_scenario_passes_for_web_app_stack_starter() -> None:
    scenario = next(item for item in load_scenarios() if item.name == "web_app_with_userjourney")

    result = evaluate_scenario(scenario)

    assert result["passed"] is True
    assert result["starter_root"] == "starter/web_app"


def test_evaluate_extended_recommend_v2_scenarios() -> None:
    scenario_names = {
        "mobile_subscription_product",
        "regulated_b2b_web_app",
        "realtime_collaboration_web_app",
        "commerce_integration_web_app",
    }

    results = [evaluate_scenario(item) for item in load_scenarios() if item.name in scenario_names]

    assert len(results) == 4
    assert all(item["passed"] is True for item in results)


def test_prompt_eval_main_emits_json(capsys) -> None:
    result = main(["--scenario", "web_app_with_userjourney", "--json"])
    out = capsys.readouterr().out

    assert result == 0
    payload = json.loads(out)
    assert payload["scenario_count"] == 1
    assert payload["failed"] == 0


def test_evaluate_scenario_fails_when_prompt_guidance_is_missing(monkeypatch) -> None:
    scenario = PromptEvalScenario(
        name="negative_guidance_case",
        product_shape="CLI tool",
        needs=[],
        regulated=False,
        attach_userjourney=False,
        expected_variant="lite",
        expected_attach_userjourney=False,
        expected_stacks=["Pydantic"],
        required_prompt_terms=["Product shape: cli tool."],
        required_prompt_sections=["Prompt principles:"],
        forbidden_prompt_terms=["FORBIDDEN_TOKEN"],
        required_plan_sections=["## Kickoff Prompt"],
        expected_starter_root="starter/cli_tool",
        require_prompt_guidance=True,
    )
    recommendation = ProjectRecommendation(
        product_shape="cli tool",
        variant="lite",
        attach_userjourney=False,
        archetype="cli",
        stack_names=["Pydantic"],
        generated_prompt="Product shape: cli tool. FORBIDDEN_TOKEN",
    )

    monkeypatch.setattr(programstart_prompt_eval, "build_recommendation", lambda **_kwargs: recommendation)
    monkeypatch.setattr(
        programstart_prompt_eval,
        "build_starter_scaffold_plan",
        lambda _name, _recommendation: SimpleNamespace(root_dir="starter/cli_tool", files={}),
    )
    monkeypatch.setattr(programstart_prompt_eval, "render_factory_plan", lambda **_kwargs: "## Kickoff Prompt")

    result = evaluate_scenario(scenario)

    assert result["passed"] is False
    assert "prompt guidance missing principles" in result["failures"]
    assert "prompt guidance missing patterns" in result["failures"]
    assert "generated prompt missing section marker: Prompt principles:" in result["failures"]
    assert "generated prompt contains forbidden term: FORBIDDEN_TOKEN" in result["failures"]


# ---------------------------------------------------------------------------
# Phase J — push prompt_eval toward 95%
# ---------------------------------------------------------------------------


def test_evaluate_assessment_tools_all_pass(monkeypatch) -> None:
    """evaluate_assessment_tools should pass when probe and workspace assets exist."""
    from scripts.programstart_common import load_registry

    registry = load_registry()
    results = programstart_prompt_eval.evaluate_assessment_tools(registry)
    assert len(results) == 4
    assert all(r["passed"] is True for r in results), [r for r in results if not r["passed"]]


def test_evaluate_assessment_tools_probe_failure(monkeypatch) -> None:
    """When health probe returns an empty report, assessment should detect issues."""
    from scripts.programstart_health_probe import HealthProbeReport

    monkeypatch.setattr(
        programstart_prompt_eval,
        "probe_target",
        lambda _root: HealthProbeReport(),
    )
    from scripts.programstart_common import load_registry

    registry = load_registry()
    results = programstart_prompt_eval.evaluate_assessment_tools(registry)
    probe_result = next(r for r in results if r["name"] == "assessment_health_probe")
    assert probe_result["passed"] is False
    assert any("probe_time" in f for f in probe_result["failures"])


def test_main_text_output(capsys) -> None:
    """main without --json should emit text summary."""
    result = main(["--scenario", "cli_tool_baseline"])
    out = capsys.readouterr().out
    assert result == 0
    assert "Prompt Evaluation" in out
    assert "cli_tool_baseline" in out


def test_main_include_assessment_json(capsys) -> None:
    """main with --include-assessment adds assessment results."""
    result = main(["--include-assessment", "--json"])
    out = capsys.readouterr().out
    payload = json.loads(out)
    names = [r["name"] for r in payload["results"]]
    assert "assessment_health_probe" in names
    assert result == 0


def test_main_returns_1_on_failure(monkeypatch, capsys) -> None:
    """main should return 1 when any scenario fails."""
    failing = PromptEvalScenario(
        name="will_fail",
        product_shape="CLI tool",
        needs=[],
        regulated=False,
        attach_userjourney=False,
        expected_variant="enterprise",  # wrong on purpose
        expected_attach_userjourney=False,
        expected_stacks=[],
        required_prompt_terms=[],
        required_prompt_sections=[],
        required_plan_sections=[],
        expected_starter_root="starter/cli_tool",
    )
    monkeypatch.setattr(programstart_prompt_eval, "load_scenarios", lambda: [failing])
    result = main(["--json"])
    assert result == 1


def test_evaluate_scenario_checks_services_apis_clis_domains(monkeypatch) -> None:
    """evaluate_scenario should detect missing services, apis, clis, and domains."""
    scenario = PromptEvalScenario(
        name="multi_check",
        product_shape="Web app",
        needs=[],
        regulated=False,
        attach_userjourney=False,
        expected_variant="lite",
        expected_attach_userjourney=False,
        expected_stacks=[],
        required_prompt_terms=[],
        required_prompt_sections=[],
        required_plan_sections=[],
        expected_starter_root="starter/web_app",
        expected_services=["MISSING_SVC"],
        expected_apis=["MISSING_API"],
        expected_clis=["MISSING_CLI"],
        expected_domains=["MISSING_DOMAIN"],
        expected_confidence="extreme",
        required_warning_domains=["MISSING_WARN"],
        expected_starter_files=["MISSING_FILE"],
        required_starter_terms=["MISSING_TERM"],
    )
    rec = ProjectRecommendation(
        product_shape="web app",
        variant="lite",
        attach_userjourney=False,
        archetype="web",
        generated_prompt="ok",
        prompt_principles=["p"],
        prompt_patterns=["p"],
    )
    monkeypatch.setattr(programstart_prompt_eval, "build_recommendation", lambda **_kw: rec)
    monkeypatch.setattr(
        programstart_prompt_eval,
        "build_starter_scaffold_plan",
        lambda _n, _r: SimpleNamespace(root_dir="starter/web_app", files={}),
    )
    monkeypatch.setattr(programstart_prompt_eval, "render_factory_plan", lambda **_kw: "")

    result = evaluate_scenario(scenario)
    assert result["passed"] is False
    assert any("missing expected service: MISSING_SVC" in f for f in result["failures"])
    assert any("missing expected api: MISSING_API" in f for f in result["failures"])
    assert any("missing expected cli: MISSING_CLI" in f for f in result["failures"])
    assert any("missing expected domain: MISSING_DOMAIN" in f for f in result["failures"])
    assert any("expected confidence extreme" in f for f in result["failures"])
    assert any("missing expected warning domain: MISSING_WARN" in f for f in result["failures"])
    assert any("missing expected starter file: MISSING_FILE" in f for f in result["failures"])
    assert any("starter scaffold missing term: MISSING_TERM" in f for f in result["failures"])


def test_main_text_with_failures(monkeypatch, capsys) -> None:
    """Text output should list individual failures."""
    failing = PromptEvalScenario(
        name="text_fail",
        product_shape="CLI tool",
        needs=[],
        regulated=False,
        attach_userjourney=False,
        expected_variant="enterprise",  # will differ
        expected_attach_userjourney=False,
        expected_stacks=[],
        required_prompt_terms=[],
        required_prompt_sections=[],
        required_plan_sections=[],
        expected_starter_root="starter/cli_tool",
    )
    monkeypatch.setattr(programstart_prompt_eval, "load_scenarios", lambda: [failing])
    result = main([])
    out = capsys.readouterr().out
    assert result == 1
    assert "FAIL" in out
    assert "text_fail" in out


# ── migrated from test_audit_fixes.py ──────────────────────────────────────────


def test_data_pipeline_ml_training_scenario_passes() -> None:
    scenario = next(item for item in load_scenarios() if item.name == "data_pipeline_ml_training")
    result = evaluate_scenario(scenario)
    assert result["passed"] is True
    assert result["starter_root"] == "starter/data_pipeline"


def test_cli_tool_ml_agents_scenario_passes() -> None:
    scenario = next(item for item in load_scenarios() if item.name == "cli_tool_ml_agents")
    result = evaluate_scenario(scenario)
    assert result["passed"] is True
    assert result["starter_root"] == "starter/cli_tool"


# ---------------------------------------------------------------------------
# Phase A: coverage push — prompt_eval.py uncovered branches
# ---------------------------------------------------------------------------


def test_evaluate_assessment_tools_detects_empty_system_name(monkeypatch) -> None:
    """Lines 200, 202: probe loop should append failures for empty system name and zero control files."""
    from scripts.programstart_common import load_registry
    from scripts.programstart_health_probe import HealthProbeReport, SystemHealthReport

    bad_report = HealthProbeReport(
        probe_time="2026-01-01T00:00:00",
        registry_version="1.0",
        overall_health="healthy",
        systems=[
            SystemHealthReport(system="", total_control_files=1),
            SystemHealthReport(system="programbuild", total_control_files=0),
        ],
    )
    monkeypatch.setattr(programstart_prompt_eval, "probe_target", lambda _root: bad_report)
    registry = load_registry()
    results = programstart_prompt_eval.evaluate_assessment_tools(registry)
    probe_result = next(r for r in results if r["name"] == "assessment_health_probe")
    assert probe_result["passed"] is False
    failure_text = " ".join(probe_result["failures"])
    assert "system name is empty" in failure_text
    assert "0 total control files" in failure_text


def test_evaluate_scenario_fails_on_variant_and_attach_mismatch(monkeypatch) -> None:
    """Lines 77–86: variant and attach_userjourney mismatches both produce failure entries."""
    from types import SimpleNamespace

    rec = ProjectRecommendation(
        product_shape="cli tool",
        variant="enterprise",
        attach_userjourney=True,
        archetype="cli",
        generated_prompt="ok",
        prompt_principles=["p"],
        prompt_patterns=["p"],
    )
    monkeypatch.setattr(programstart_prompt_eval, "build_recommendation", lambda **_kw: rec)
    monkeypatch.setattr(
        programstart_prompt_eval,
        "build_starter_scaffold_plan",
        lambda _n, _r: SimpleNamespace(root_dir="starter/cli_tool", files={}),
    )
    monkeypatch.setattr(programstart_prompt_eval, "render_factory_plan", lambda **_kw: "")

    scenario = PromptEvalScenario(
        name="mismatch_test",
        product_shape="cli tool",
        needs=[],
        regulated=False,
        attach_userjourney=False,
        expected_variant="lite",
        expected_attach_userjourney=False,
        expected_stacks=[],
        required_prompt_terms=[],
        required_prompt_sections=[],
        required_plan_sections=[],
        expected_starter_root="starter/cli_tool",
        require_prompt_guidance=False,
    )
    result = evaluate_scenario(scenario)
    assert result["passed"] is False
    failure_text = " ".join(result["failures"])
    assert "expected variant lite" in failure_text
    assert "expected attach_userjourney=False" in failure_text
