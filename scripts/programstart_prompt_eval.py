from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from .programstart_common import ROOT, load_registry, warn_direct_script_invocation, workspace_path
    from .programstart_create import default_github_repo_name, render_factory_plan
    from .programstart_health_probe import probe_target
    from .programstart_recommend import build_recommendation
    from .programstart_starter_scaffold import build_starter_scaffold_plan
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_create import default_github_repo_name, render_factory_plan
    from programstart_health_probe import probe_target
    from programstart_recommend import build_recommendation
    from programstart_starter_scaffold import build_starter_scaffold_plan

    from programstart_common import ROOT, load_registry, warn_direct_script_invocation, workspace_path


@dataclass(slots=True)
class PromptEvalScenario:
    name: str
    product_shape: str
    needs: list[str]
    regulated: bool
    attach_userjourney: bool | None
    expected_variant: str
    expected_attach_userjourney: bool
    expected_stacks: list[str]
    required_prompt_terms: list[str]
    required_plan_sections: list[str]
    expected_starter_root: str
    expected_services: list[str] = field(default_factory=list)
    expected_apis: list[str] = field(default_factory=list)
    expected_clis: list[str] = field(default_factory=list)
    expected_domains: list[str] = field(default_factory=list)
    expected_confidence: str = ""
    required_warning_domains: list[str] = field(default_factory=list)
    expected_starter_files: list[str] = field(default_factory=list)
    required_starter_terms: list[str] = field(default_factory=list)
    required_prompt_sections: list[str] = field(default_factory=list)
    forbidden_prompt_terms: list[str] = field(default_factory=list)
    require_prompt_guidance: bool = True


def load_scenarios() -> list[PromptEvalScenario]:
    payload = json.loads(workspace_path("config/prompt-eval-scenarios.json").read_text(encoding="utf-8"))
    return [PromptEvalScenario(**scenario) for scenario in payload.get("scenarios", [])]


def evaluate_scenario(scenario: PromptEvalScenario) -> dict[str, Any]:
    recommendation = build_recommendation(
        product_shape=scenario.product_shape.lower(),
        needs={item.lower() for item in scenario.needs},
        regulated=scenario.regulated,
        attach_userjourney=scenario.attach_userjourney,
    )
    starter_plan = build_starter_scaffold_plan(scenario.name, recommendation)
    starter_text = "\n".join(starter_plan.files.values())
    plan_text = render_factory_plan(
        project_name=scenario.name,
        recommendation=recommendation,
        destination=Path("EVAL"),
        attachment_source="",
        starter_plan=starter_plan,
        github_repo=default_github_repo_name(scenario.name),
        github_visibility="private",
        services=recommendation.service_names,
    )

    failures: list[str] = []
    if recommendation.variant != scenario.expected_variant:
        failures.append(f"expected variant {scenario.expected_variant}, got {recommendation.variant}")
    if recommendation.attach_userjourney != scenario.expected_attach_userjourney:
        failures.append(
            f"expected attach_userjourney={scenario.expected_attach_userjourney}, got {recommendation.attach_userjourney}"
        )

    stacks_lower = {item.lower() for item in recommendation.stack_names}
    for expected in scenario.expected_stacks:
        if expected.lower() not in stacks_lower:
            failures.append(f"missing expected stack: {expected}")

    services_lower = {item.lower() for item in recommendation.service_names}
    for expected in scenario.expected_services:
        if expected.lower() not in services_lower:
            failures.append(f"missing expected service: {expected}")

    apis_lower = {item.lower() for item in recommendation.api_names}
    for expected in scenario.expected_apis:
        if expected.lower() not in apis_lower:
            failures.append(f"missing expected api: {expected}")

    clis_lower = {item.lower() for item in recommendation.cli_tool_names}
    for expected in scenario.expected_clis:
        if expected.lower() not in clis_lower:
            failures.append(f"missing expected cli: {expected}")

    domains_lower = {item.lower() for item in recommendation.matched_domains}
    for expected in scenario.expected_domains:
        if expected.lower() not in domains_lower:
            failures.append(f"missing expected domain: {expected}")

    if scenario.expected_confidence and recommendation.confidence != scenario.expected_confidence:
        failures.append(f"expected confidence {scenario.expected_confidence}, got {recommendation.confidence}")

    warning_domains_lower = {item["domain"].lower() for item in recommendation.coverage_warnings}
    for expected in scenario.required_warning_domains:
        if expected.lower() not in warning_domains_lower:
            failures.append(f"missing expected warning domain: {expected}")

    for term in scenario.required_prompt_terms:
        if term not in recommendation.generated_prompt:
            failures.append(f"generated prompt missing term: {term}")

    for section in scenario.required_prompt_sections:
        if section not in recommendation.generated_prompt:
            failures.append(f"generated prompt missing section marker: {section}")

    for term in scenario.forbidden_prompt_terms:
        if term in recommendation.generated_prompt:
            failures.append(f"generated prompt contains forbidden term: {term}")

    if scenario.require_prompt_guidance:
        if not recommendation.prompt_principles:
            failures.append("prompt guidance missing principles")
        if not recommendation.prompt_patterns:
            failures.append("prompt guidance missing patterns")

    for section in scenario.required_plan_sections:
        if section not in plan_text:
            failures.append(f"factory plan missing section: {section}")

    if starter_plan.root_dir != scenario.expected_starter_root:
        failures.append(f"expected starter root {scenario.expected_starter_root}, got {starter_plan.root_dir}")

    starter_files = set(starter_plan.files)
    for expected in scenario.expected_starter_files:
        if expected not in starter_files:
            failures.append(f"missing expected starter file: {expected}")

    for term in scenario.required_starter_terms:
        if term not in starter_text:
            failures.append(f"starter scaffold missing term: {term}")

    score_total = (
        4
        + len(scenario.expected_stacks)
        + len(scenario.expected_services)
        + len(scenario.expected_apis)
        + len(scenario.expected_clis)
        + len(scenario.expected_domains)
        + (1 if scenario.expected_confidence else 0)
        + len(scenario.required_warning_domains)
        + len(scenario.required_prompt_terms)
        + len(scenario.required_prompt_sections)
        + len(scenario.forbidden_prompt_terms)
        + (2 if scenario.require_prompt_guidance else 0)
        + len(scenario.required_plan_sections)
        + len(scenario.expected_starter_files)
        + len(scenario.required_starter_terms)
    )
    score = score_total - len(failures)
    return {
        "name": scenario.name,
        "passed": not failures,
        "score": score,
        "score_total": score_total,
        "variant": recommendation.variant,
        "attach_userjourney": recommendation.attach_userjourney,
        "confidence": recommendation.confidence,
        "starter_root": starter_plan.root_dir,
        "failures": failures,
    }


def evaluate_assessment_tools(registry: dict[str, Any]) -> list[dict[str, Any]]:
    """Run assessment tool coverage checks against the current workspace."""
    results: list[dict[str, Any]] = []

    # 1. Health probe produces valid report
    probe_failures: list[str] = []
    report = probe_target(ROOT)
    if not report.probe_time:
        probe_failures.append("probe_time is empty")
    if not report.registry_version:
        probe_failures.append("registry_version is empty")
    if not report.overall_health:
        probe_failures.append("overall_health is empty")
    if report.overall_health not in {"healthy", "warnings", "degraded", "critical"}:
        probe_failures.append(f"unexpected health classification: {report.overall_health}")
    if not report.systems:
        probe_failures.append("no systems found in probe report")
    for sys_report in report.systems:
        if not sys_report.system:
            probe_failures.append("system name is empty in system report")
        if sys_report.total_control_files == 0 and sys_report.system == "programbuild":
            probe_failures.append("programbuild has 0 total control files")
    checks = 6 + len(report.systems)
    results.append(
        {
            "name": "assessment_health_probe",
            "passed": not probe_failures,
            "score": checks - len(probe_failures),
            "score_total": checks,
            "failures": probe_failures,
        }
    )

    # 2. Validate script covers all check types
    validate_failures: list[str] = []
    expected_checks = [
        "required-files",
        "metadata",
        "workflow-state",
        "authority-sync",
        "planning-references",
        "bootstrap-assets",
        "repo-boundary-policy",
    ]
    try:
        from . import programstart_validate as pv
    except ImportError:
        import programstart_validate as pv  # type: ignore[no-redef]
    for check_name in expected_checks:
        fn_name = f"validate_{check_name.replace('-', '_')}"
        if not hasattr(pv, fn_name):
            validate_failures.append(f"validate script missing function: {fn_name}")
    results.append(
        {
            "name": "assessment_validate_coverage",
            "passed": not validate_failures,
            "score": len(expected_checks) - len(validate_failures),
            "score_total": len(expected_checks),
            "failures": validate_failures,
        }
    )

    # 3. Assessment prompts exist
    prompt_failures: list[str] = []
    required_prompts = [
        ".github/prompts/audit-process-drift.prompt.md",
        ".github/prompts/programstart-cross-stage-validation.prompt.md",
        ".github/prompts/programstart-what-next.prompt.md",
        ".github/prompts/programstart-stage-transition.prompt.md",
        ".github/prompts/propagate-canonical-change.prompt.md",
    ]
    for prompt_path in required_prompts:
        if not workspace_path(prompt_path).exists():
            prompt_failures.append(f"missing assessment prompt: {prompt_path}")
    results.append(
        {
            "name": "assessment_prompt_coverage",
            "passed": not prompt_failures,
            "score": len(required_prompts) - len(prompt_failures),
            "score_total": len(required_prompts),
            "failures": prompt_failures,
        }
    )

    # 4. Agent definitions exist
    agent_failures: list[str] = []
    required_agents = [
        ".github/agents/architecture-security.agent.md",
        ".github/agents/discovery-scoping.agent.md",
        ".github/agents/quality-release.agent.md",
    ]
    for agent_path in required_agents:
        if not workspace_path(agent_path).exists():
            agent_failures.append(f"missing agent definition: {agent_path}")
    results.append(
        {
            "name": "assessment_agent_coverage",
            "passed": not agent_failures,
            "score": len(required_agents) - len(agent_failures),
            "score_total": len(required_agents),
            "failures": agent_failures,
        }
    )

    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate generated kickoff prompts and starter scaffolds against fixed scenarios."
    )
    parser.add_argument("--scenario", action="append", help="Optional scenario name filter. Can be used multiple times.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument(
        "--include-assessment",
        action="store_true",
        help="Also run assessment tool coverage checks (health probe, validate, drift).",
    )
    args = parser.parse_args(argv)

    registry = load_registry()
    scenarios = load_scenarios()
    allowed = {item.strip() for item in (args.scenario or []) if item.strip()}
    if allowed:
        scenarios = [scenario for scenario in scenarios if scenario.name in allowed]

    results = [evaluate_scenario(scenario) for scenario in scenarios]

    assessment_results: list[dict[str, Any]] = []
    if args.include_assessment:
        assessment_results = evaluate_assessment_tools(registry)
        results.extend(assessment_results)

    passed = sum(1 for item in results if item["passed"])
    payload = {
        "workspace": registry.get("workspace", {}).get("name", "PROGRAMSTART"),
        "scenario_count": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "results": results,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print("PROGRAMSTART Prompt Evaluation")
        print(f"- scenarios: {payload['scenario_count']}")
        print(f"- passed: {passed}")
        print(f"- failed: {payload['failed']}")
        for item in results:
            print(f"- {item['name']}: {'PASS' if item['passed'] else 'FAIL'} ({item['score']}/{item['score_total']})")
            for failure in item["failures"]:
                print(f"  - {failure}")
    return 0 if payload["failed"] == 0 else 1


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart prompt-eval' or 'pb prompt-eval'")
    raise SystemExit(main())
