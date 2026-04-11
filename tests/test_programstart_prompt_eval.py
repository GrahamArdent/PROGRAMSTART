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
