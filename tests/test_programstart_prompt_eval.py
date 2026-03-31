from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_prompt_eval import evaluate_scenario, load_scenarios, main


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
