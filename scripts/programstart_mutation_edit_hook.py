from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import subprocess
import textwrap
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from pprint import pformat
from typing import Callable
from unittest.mock import patch

try:
    from . import programstart_recommend as recommend
    from .programstart_common import load_json, warn_direct_script_invocation, workspace_path
except ImportError:  # pragma: no cover - standalone script execution fallback
    import programstart_recommend as recommend

    from programstart_common import load_json, warn_direct_script_invocation, workspace_path

SURVIVOR_KEY_RE = re.compile(r"^scripts\.programstart_recommend\.x_(.+)__mutmut_\d+$")
TEST_NAME_RE = re.compile(r"^def (test_[A-Za-z0-9_]+)\(", re.MULTILINE)


@dataclass(frozen=True, slots=True)
class GeneratedScenario:
    name: str
    hotspot: str
    render: Callable[[], str]


def _indent_literal(value: object, prefix: str = "    ") -> str:
    return textwrap.indent(pformat(value, width=100, sort_dicts=False), prefix)


def _capture_main_output(arguments: list[str], recommendation_obj: recommend.ProjectRecommendation) -> str:
    stream = io.StringIO()
    with (
        patch.object(recommend, "load_recommendation_inputs", return_value=(recommendation_obj.product_shape, {"generated"})),
        patch.object(recommend, "build_recommendation", return_value=recommendation_obj),
        contextlib.redirect_stdout(stream),
    ):
        recommend.main(arguments)
    return stream.getvalue()


def _capture_print_output(recommendation_obj: recommend.ProjectRecommendation) -> str:
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        recommend.print_recommendation(recommendation_obj)
    return stream.getvalue()


def scenario_build_stack_candidates_mobile_resilience() -> str:
    kb = {
        "stacks": [
            {"name": "React Native", "layer": "mobile", "strengths": ["ios", "android", "shared ui"]},
            {"name": "Expo", "layer": "mobile", "strengths": ["push notifications", "shared ui", "offline"]},
            {"name": "Firebase", "layer": "backend", "strengths": ["mobile auth", "push notifications", "analytics"]},
            {"name": "SQLite", "layer": "storage", "strengths": ["offline", "local sync"]},
            {"name": "Sentry", "layer": "observability", "strengths": ["crash reporting", "analytics"]},
        ],
        "coverage_domains": [
            {
                "name": "Mobile and cross-platform apps",
                "status": "strong",
                "summary": "Mobile coverage is mature",
                "current_gaps": [],
                "representative_tools": ["React Native", "Expo", "Firebase"],
            },
            {
                "name": "Desktop, local-first, and offline-capable software",
                "status": "partial",
                "summary": "Offline sync guidance is still emerging",
                "current_gaps": ["Conflict resolution"],
                "representative_tools": ["SQLite"],
            },
        ],
        "comparisons": [
            {
                "name": "Expo vs native shell",
                "related_items": ["Expo", "React Native"],
                "decision": "Expo is preferred for rapid mobile rollout and notification handling.",
                "summary": "Prefer Expo for faster mobile delivery.",
            }
        ],
        "relationships": [{"relation": "complements", "subject": "Expo", "object": "Sentry"}],
        "integration_patterns": [
            {
                "name": "Offline mobile engagement",
                "fit_for": ["mobile app", "push notifications", "offline"],
                "components": ["Expo", "SQLite", "Sentry"],
            }
        ],
        "decision_rules": [
            {
                "title": "Prefer resilient mobile stack",
                "because": "Offline and notification support",
                "confidence": "high",
                "match_product_shapes": ["mobile app"],
                "match_needs": ["push notifications", "offline"],
                "match_domains": ["Mobile and cross-platform apps"],
                "target_layers": ["stacks"],
                "prefer_items": ["Expo", "SQLite"],
                "avoid_items": [],
            }
        ],
    }
    expected = recommend.build_stack_candidates("mobile app", {"push notifications", "offline", "analytics"}, False, kb)
    return textwrap.dedent(
        f'''
        def test_build_stack_candidates_mobile_resilience_exact_output() -> None:
            kb = {_indent_literal(kb).lstrip()}

            assert recommend.build_stack_candidates(
                "mobile app", {{"push notifications", "offline", "analytics"}}, False, kb
            ) == {_indent_literal(expected).lstrip()}
        '''
    ).strip()


def scenario_build_stack_candidates_ops_console() -> str:
    kb = {
        "stacks": [
            {"name": "FastAPI", "layer": "backend", "strengths": ["typed", "automation"]},
            {"name": "OpenTelemetry", "layer": "observability", "strengths": ["observability", "metrics"]},
            {"name": "Keycloak", "layer": "auth", "strengths": ["sso", "authorization"]},
            {"name": "Next.js", "layer": "frontend", "strengths": ["dashboard", "interactive client state"]},
            {"name": "Redis", "layer": "cache", "strengths": ["realtime", "dashboard"]},
        ],
        "coverage_domains": [
            {
                "name": "API, workflow, and backend platforms",
                "status": "strong",
                "summary": "Backend guidance is mature",
                "current_gaps": [],
                "representative_tools": ["FastAPI", "OpenTelemetry", "Redis"],
            },
            {
                "name": "Identity, security, and regulated delivery",
                "status": "partial",
                "summary": "Auth guidance still needs hardening",
                "current_gaps": ["SCIM templates"],
                "representative_tools": ["Keycloak"],
            },
            {
                "name": "Web and frontend product delivery",
                "status": "strong",
                "summary": "Frontend guidance is mature",
                "current_gaps": [],
                "representative_tools": ["Next.js"],
            },
        ],
        "comparisons": [],
        "relationships": [{"relation": "complements", "subject": "FastAPI", "object": "Next.js"}],
        "integration_patterns": [
            {
                "name": "Ops control plane",
                "fit_for": ["api service", "dashboard", "authorization", "observability"],
                "components": ["OpenTelemetry", "Keycloak", "Next.js"],
            }
        ],
        "decision_rules": [
            {
                "title": "Prefer observable ops console",
                "because": "Operational visibility",
                "confidence": "high",
                "match_product_shapes": ["api service"],
                "match_needs": ["dashboard", "observability", "authorization"],
                "match_domains": ["API, workflow, and backend platforms"],
                "target_layers": ["stacks"],
                "prefer_items": ["OpenTelemetry", "Next.js", "Keycloak"],
                "avoid_items": [],
            }
        ],
    }
    expected = recommend.build_stack_candidates("api service", {"dashboard", "observability", "authorization"}, True, kb)
    return textwrap.dedent(
        f'''
        def test_build_stack_candidates_ops_console_exact_output() -> None:
            kb = {_indent_literal(kb).lstrip()}

            assert recommend.build_stack_candidates(
                "api service", {{"dashboard", "observability", "authorization"}}, True, kb
            ) == {_indent_literal(expected).lstrip()}
        '''
    ).strip()


def scenario_build_recommendation_api_attach_override() -> str:
    registry = {"workflow_guidance": {"kickoff": {"files": ["PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md"]}}}
    stack_return = (
        "Typed API and automation platform",
        ["FastAPI", "Next.js"],
        [
            {"name": "FastAPI", "score": 18, "reasons": ["Typed contracts", "Automation backend"]},
            {"name": "Next.js", "score": 16, "reasons": ["Operator dashboard", "Interactive surfaces"]},
        ],
        ["API, workflow, and backend platforms", "Web and frontend product delivery"],
        [],
        [{"item": "Retool", "category": "stack", "rationale": "Admin console alternative"}],
        [{"title": "Prefer API plus dashboard", "because": "Operator visibility", "confidence": "high"}],
        "high",
    )
    service_return = (
        ["Supabase"],
        ["configure auth tenancy"],
        [{"name": "Supabase", "score": 8, "reasons": ["Managed auth"]}],
        [],
    )
    api_return = (
        ["Stripe"],
        ["wire product ids"],
        [{"name": "Stripe", "score": 7, "reasons": ["Payments"]}],
        [{"item": "RevenueCat", "category": "api", "rationale": "Mobile billing alternative"}],
    )
    cli_return = (
        ["uv"],
        ["install Python tooling"],
        [{"name": "uv", "score": 5, "reasons": ["Fast installs"]}],
        [],
    )
    actionability = [
        {"name": "FastAPI", "category": "stack", "actionability": "advice-only", "reason": "Architecture input"},
        {"name": "Supabase", "category": "service", "actionability": "automation-supported", "reason": "Provisionable"},
        {"name": "Stripe", "category": "api", "actionability": "manual-setup", "reason": "Billing wiring"},
    ]
    with (
        patch.object(recommend, "load_registry", return_value=registry),
        patch.object(recommend, "load_knowledge_base", return_value={"prompt_engineering_guidance": {}}),
        patch.object(recommend, "build_stack_candidates", return_value=stack_return),
        patch.object(recommend, "choose_service_names", return_value=service_return),
        patch.object(recommend, "choose_api_names", return_value=api_return),
        patch.object(recommend, "choose_cli_tool_names", return_value=cli_return),
        patch.object(recommend, "build_actionability_summary", return_value=actionability),
        patch.object(recommend, "normalize_prompt_guidance", return_value=([], [], ["Do not invent"])),
    ):
        result = recommend.build_recommendation(
            product_shape="api service",
            needs={"dashboard", "payments"},
            regulated=False,
            attach_userjourney=True,
        )
    expected = {
        "variant": result.variant,
        "attach_userjourney": result.attach_userjourney,
        "rationale": result.rationale,
        "next_commands": result.next_commands,
        "coverage_warnings": result.coverage_warnings,
        "alternatives": result.alternatives,
        "suggested_companion_surfaces": result.suggested_companion_surfaces,
    }
    return textwrap.dedent(
        f'''
        def test_build_recommendation_api_attach_override_exact_output() -> None:
            registry = {_indent_literal(registry).lstrip()}
            stack_return = {_indent_literal(stack_return).lstrip()}
            service_return = {_indent_literal(service_return).lstrip()}
            api_return = {_indent_literal(api_return).lstrip()}
            cli_return = {_indent_literal(cli_return).lstrip()}
            actionability = {_indent_literal(actionability).lstrip()}

            with (
                patch.object(recommend, "load_registry", return_value=registry),
                patch.object(recommend, "load_knowledge_base", return_value={{"prompt_engineering_guidance": {{}}}}),
                patch.object(recommend, "build_stack_candidates", return_value=stack_return),
                patch.object(recommend, "choose_service_names", return_value=service_return),
                patch.object(recommend, "choose_api_names", return_value=api_return),
                patch.object(recommend, "choose_cli_tool_names", return_value=cli_return),
                patch.object(recommend, "build_actionability_summary", return_value=actionability),
                patch.object(recommend, "normalize_prompt_guidance", return_value=([], [], ["Do not invent"])),
            ):
                result = recommend.build_recommendation(
                    product_shape="api service",
                    needs={{"dashboard", "payments"}},
                    regulated=False,
                    attach_userjourney=True,
                )

            assert {{
                "variant": result.variant,
                "attach_userjourney": result.attach_userjourney,
                "rationale": result.rationale,
                "next_commands": result.next_commands,
                "coverage_warnings": result.coverage_warnings,
                "alternatives": result.alternatives,
                "suggested_companion_surfaces": result.suggested_companion_surfaces,
            }} == {_indent_literal(expected).lstrip()}
        '''
    ).strip()


def scenario_build_recommendation_cli_manual_only() -> str:
    registry = {"workflow_guidance": {"kickoff": {"files": ["PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md"]}}}
    stack_return = (
        "Type-safe CLI planning toolkit",
        ["Pydantic", "Ruff"],
        [{"name": "Pydantic", "score": 10, "reasons": ["Validation", "CLI config"]}],
        ["Developer experience, quality, and supply chain"],
        [],
        [],
        [],
        "medium",
    )
    service_return = ([], [], [], [])
    api_return = ([], [], [], [])
    cli_return = (
        ["uv"],
        ["install uv"],
        [{"name": "uv", "score": 5, "reasons": ["Fast installs"]}],
        [{"item": "pipx", "category": "cli", "rationale": "Alternative installer"}],
    )
    actionability = [
        {"name": "Pydantic", "category": "stack", "actionability": "advice-only", "reason": "Architecture input"},
        {"name": "uv", "category": "cli", "actionability": "manual-setup", "reason": "Local install"},
    ]
    with (
        patch.object(recommend, "load_registry", return_value=registry),
        patch.object(recommend, "load_knowledge_base", return_value={"prompt_engineering_guidance": {}}),
        patch.object(recommend, "build_stack_candidates", return_value=stack_return),
        patch.object(recommend, "choose_service_names", return_value=service_return),
        patch.object(recommend, "choose_api_names", return_value=api_return),
        patch.object(recommend, "choose_cli_tool_names", return_value=cli_return),
        patch.object(recommend, "build_actionability_summary", return_value=actionability),
        patch.object(recommend, "normalize_prompt_guidance", return_value=([], [], ["Do not invent"])),
    ):
        result = recommend.build_recommendation(
            product_shape="cli tool",
            needs={"offline"},
            regulated=False,
            attach_userjourney=None,
        )
    expected = {
        "variant": result.variant,
        "attach_userjourney": result.attach_userjourney,
        "rationale": result.rationale,
        "next_commands": result.next_commands,
        "alternatives": result.alternatives,
    }
    return textwrap.dedent(
        f'''
        def test_build_recommendation_cli_manual_only_exact_output() -> None:
            registry = {_indent_literal(registry).lstrip()}
            stack_return = {_indent_literal(stack_return).lstrip()}
            service_return = {_indent_literal(service_return).lstrip()}
            api_return = {_indent_literal(api_return).lstrip()}
            cli_return = {_indent_literal(cli_return).lstrip()}
            actionability = {_indent_literal(actionability).lstrip()}

            with (
                patch.object(recommend, "load_registry", return_value=registry),
                patch.object(recommend, "load_knowledge_base", return_value={{"prompt_engineering_guidance": {{}}}}),
                patch.object(recommend, "build_stack_candidates", return_value=stack_return),
                patch.object(recommend, "choose_service_names", return_value=service_return),
                patch.object(recommend, "choose_api_names", return_value=api_return),
                patch.object(recommend, "choose_cli_tool_names", return_value=cli_return),
                patch.object(recommend, "build_actionability_summary", return_value=actionability),
                patch.object(recommend, "normalize_prompt_guidance", return_value=([], [], ["Do not invent"])),
            ):
                result = recommend.build_recommendation(
                    product_shape="cli tool",
                    needs={{"offline"}},
                    regulated=False,
                    attach_userjourney=None,
                )

            assert {{
                "variant": result.variant,
                "attach_userjourney": result.attach_userjourney,
                "rationale": result.rationale,
                "next_commands": result.next_commands,
                "alternatives": result.alternatives,
            }} == {_indent_literal(expected).lstrip()}
        '''
    ).strip()


def scenario_select_triggered_entries_cli_tools() -> str:
    entries = [
        {"name": "uv", "trigger_shapes": ["cli tool"], "trigger_needs": ["automation"], "notes": ["fast resolver"]},
        {"name": "pipx", "trigger_shapes": ["cli tool"], "trigger_needs": ["automation"], "notes": ["user installs"]},
        {"name": "mise", "trigger_stacks": ["Pydantic"], "notes": ["toolchain manager"]},
    ]
    rules = [
        {
            "title": "Prefer uv for CLI toolchains",
            "because": "Fast installs",
            "confidence": "high",
            "match_product_shapes": ["cli tool"],
            "match_needs": ["automation"],
            "match_domains": ["Developer experience, quality, and supply chain"],
            "target_layers": ["cli_tools"],
            "prefer_items": ["uv"],
            "avoid_items": ["pipx"],
        }
    ]
    expected = recommend.select_triggered_entries(
        entries=entries,
        product_shape="cli tool",
        needs={"automation"},
        stack_names=["Pydantic"],
        service_names=[],
        api_names=[],
        comparisons=[],
        decision_rules=rules,
        matched_domains=["Developer experience, quality, and supply chain"],
        category="cli_tools",
        min_score=3,
    )
    return textwrap.dedent(
        f'''
        def test_select_triggered_entries_cli_tools_exact_output() -> None:
            entries = {_indent_literal(entries).lstrip()}
            rules = {_indent_literal(rules).lstrip()}

            assert recommend.select_triggered_entries(
                entries=entries,
                product_shape="cli tool",
                needs={{"automation"}},
                stack_names=["Pydantic"],
                service_names=[],
                api_names=[],
                comparisons=[],
                decision_rules=rules,
                matched_domains=["Developer experience, quality, and supply chain"],
                category="cli_tools",
                min_score=3,
            ) == {_indent_literal(expected).lstrip()}
        '''
    ).strip()


def scenario_main_text_output_detailed() -> str:
    recommendation_obj = recommend.ProjectRecommendation(
        product_shape="api service",
        variant="enterprise",
        attach_userjourney=True,
        archetype="Typed API and automation platform",
        stack_names=["FastAPI", "Next.js"],
        matched_domains=["API, workflow, and backend platforms", "Web and frontend product delivery"],
        service_names=["Supabase"],
        cli_tool_names=["uv"],
        api_names=["Stripe"],
        rationale=["API rationale", "Dashboard rationale"],
        coverage_warnings=[{"domain": "Ops", "status": "partial", "gaps": "On-call runbooks"}],
        kickoff_files=["PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md"],
        next_commands=["programstart next"],
    )
    output = _capture_main_output(["--product-shape", "api service", "--need", "dashboard"], recommendation_obj)
    return textwrap.dedent(
        f'''
        def test_main_text_output_detailed_exact(capsys) -> None:
            recommendation_obj = ProjectRecommendation(
                product_shape="api service",
                variant="enterprise",
                attach_userjourney=True,
                archetype="Typed API and automation platform",
                stack_names=["FastAPI", "Next.js"],
                matched_domains=["API, workflow, and backend platforms", "Web and frontend product delivery"],
                service_names=["Supabase"],
                cli_tool_names=["uv"],
                api_names=["Stripe"],
                rationale=["API rationale", "Dashboard rationale"],
                coverage_warnings=[{{"domain": "Ops", "status": "partial", "gaps": "On-call runbooks"}}],
                kickoff_files=["PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md"],
                next_commands=["programstart next"],
            )

            with (
                patch.object(recommend, "load_recommendation_inputs", return_value=("api service", {{"dashboard"}})),
                patch.object(recommend, "build_recommendation", return_value=recommendation_obj),
            ):
                result = recommend.main(["--product-shape", "api service", "--need", "dashboard"])

            assert result == 0
            assert capsys.readouterr().out == {output!r}
        '''
    ).strip()


def scenario_print_recommendation_sections() -> str:
    recommendation_obj = recommend.ProjectRecommendation(
        product_shape="api service",
        variant="product",
        attach_userjourney=False,
        archetype="Typed API and automation platform",
        stack_names=["FastAPI"],
        service_names=["Supabase"],
        cli_tool_names=["uv"],
        api_names=["Stripe"],
        rationale=["Primary rationale"],
        service_notes=["service note"],
        cli_notes=["cli note"],
        api_notes=["api note"],
        kickoff_files=["PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md"],
        next_commands=["programstart next"],
        coverage_warnings=[{"domain": "Ops", "status": "partial", "gaps": "On-call runbooks"}],
        alternatives=[{"item": "Retool", "category": "stack", "rationale": "Alt admin UI"}],
        actionability_summary=[{"name": "FastAPI", "category": "stack", "actionability": "advice-only", "reason": "Architecture input"}],
    )
    output = _capture_print_output(recommendation_obj)
    return textwrap.dedent(
        f'''
        def test_print_recommendation_sections_exact(capsys) -> None:
            recommendation_obj = ProjectRecommendation(
                product_shape="api service",
                variant="product",
                attach_userjourney=False,
                archetype="Typed API and automation platform",
                stack_names=["FastAPI"],
                service_names=["Supabase"],
                cli_tool_names=["uv"],
                api_names=["Stripe"],
                rationale=["Primary rationale"],
                service_notes=["service note"],
                cli_notes=["cli note"],
                api_notes=["api note"],
                kickoff_files=["PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md"],
                next_commands=["programstart next"],
                coverage_warnings=[{{"domain": "Ops", "status": "partial", "gaps": "On-call runbooks"}}],
                alternatives=[{{"item": "Retool", "category": "stack", "rationale": "Alt admin UI"}}],
                actionability_summary=[{{"name": "FastAPI", "category": "stack", "actionability": "advice-only", "reason": "Architecture input"}}],
            )

            recommend.print_recommendation(recommendation_obj)

            assert capsys.readouterr().out == {output!r}
        '''
    ).strip()


def scenario_infer_domain_names_desktop_security_ai() -> str:
    kb = {
        "coverage_domains": [
            {"name": "Developer experience, quality, and supply chain"},
            {"name": "Desktop, local-first, and offline-capable software"},
            {"name": "AI, retrieval, and agent systems"},
            {"name": "Identity, security, and regulated delivery"},
            {"name": "Cloud, infrastructure, and platform operations"},
        ]
    }
    expected = recommend.infer_domain_names("cli tool", {"offline", "llm", "audit readiness", "deploy"}, True, kb)
    return textwrap.dedent(
        f'''
        def test_infer_domain_names_desktop_security_ai_exact_output() -> None:
            kb = {_indent_literal(kb).lstrip()}

            assert recommend.infer_domain_names(
                "cli tool", {{"offline", "llm", "audit readiness", "deploy"}}, True, kb
            ) == {_indent_literal(expected).lstrip()}
        '''
    ).strip()


def scenario_re_evaluate_project_exact_output() -> str:
    return textwrap.dedent(
        '''
        def test_re_evaluate_project_exact_output(tmp_path) -> None:
            from datetime import UTC, datetime

            kickoff = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_KICKOFF_PACKET.md"
            kickoff.parent.mkdir(parents=True)
            kickoff.write_text(
                "PRODUCT_SHAPE: api service\nCORE_PROBLEM: Need dashboard and payments support\nKNOWN_CONSTRAINTS: compliance required\n",
                encoding="utf-8",
            )
            config_dir = tmp_path / "config"
            config_dir.mkdir()
            (config_dir / "process-registry.json").write_text('{"version": "2026.04"}', encoding="utf-8")
            state_dir = tmp_path / "PROGRAMBUILD"
            (state_dir / "PROGRAMBUILD_STATE.json").write_text('{"variant": "product"}', encoding="utf-8")

            fixed_now = datetime(2026, 4, 16, 12, 0, tzinfo=UTC)
            recommendation_obj = ProjectRecommendation(
                product_shape="api service",
                variant="enterprise",
                attach_userjourney=False,
                archetype="Typed API and automation platform",
                prompt_generated_at=fixed_now.isoformat(timespec="seconds"),
            )

            class FixedDateTime:
                @staticmethod
                def now(tz):
                    return fixed_now

            with (
                patch.object(recommend, "build_recommendation", return_value=recommendation_obj),
                patch.object(recommend, "load_knowledge_base", return_value={"version": "2026.04"}),
                patch.object(recommend, "load_registry", return_value={"version": "2026.05"}),
                patch.object(recommend, "datetime", FixedDateTime),
            ):
                result = recommend.re_evaluate_project(str(tmp_path))

            assert result == {
                "project_dir": str(tmp_path.resolve()),
                "kickoff_inputs": {
                    "PRODUCT_SHAPE": "api service",
                    "CORE_PROBLEM": "Need dashboard and payments support",
                    "KNOWN_CONSTRAINTS": "compliance required",
                },
                "product_shape": "api service",
                "inferred_needs": ["compliance", "dashboard", "payments"],
                "current_recommendation": {
                    "product_shape": "api service",
                    "variant": "enterprise",
                    "attach_userjourney": False,
                    "archetype": "Typed API and automation platform",
                    "stack_names": [],
                    "service_names": [],
                    "cli_tool_names": [],
                    "api_names": [],
                    "rationale": [],
                    "service_notes": [],
                    "cli_notes": [],
                    "api_notes": [],
                    "kickoff_files": [],
                    "next_commands": [],
                    "prompt_principles": [],
                    "prompt_patterns": [],
                    "prompt_anti_patterns": [],
                    "matched_domains": [],
                    "coverage_warnings": [],
                    "suggested_companion_surfaces": [],
                    "stack_evidence": [],
                    "service_evidence": [],
                    "api_evidence": [],
                    "cli_evidence": [],
                    "rule_evidence": [],
                    "actionability_summary": [],
                    "alternatives": [],
                    "confidence": "medium",
                    "generated_prompt": "",
                    "prompt_generated_at": "2026-04-16T12:00:00+00:00",
                },
                "kb_version": "2026.04",
                "project_state": {"registry_version": "2026.04", "variant": "product"},
                "deltas": [
                    "Variant drift: project uses 'product', current KB recommends 'enterprise'",
                    "Registry version drift: project has '2026.04', current is '2026.05'",
                ],
                "re_evaluated_at": "2026-04-16T12:00:00+00:00",
            }
        '''
    ).strip()


SCENARIOS: tuple[GeneratedScenario, ...] = (
    GeneratedScenario("test_build_stack_candidates_mobile_resilience_exact_output", "build_stack_candidates", scenario_build_stack_candidates_mobile_resilience),
    GeneratedScenario("test_build_stack_candidates_ops_console_exact_output", "build_stack_candidates", scenario_build_stack_candidates_ops_console),
    GeneratedScenario("test_build_recommendation_api_attach_override_exact_output", "build_recommendation", scenario_build_recommendation_api_attach_override),
    GeneratedScenario("test_build_recommendation_cli_manual_only_exact_output", "build_recommendation", scenario_build_recommendation_cli_manual_only),
    GeneratedScenario("test_select_triggered_entries_cli_tools_exact_output", "select_triggered_entries", scenario_select_triggered_entries_cli_tools),
    GeneratedScenario("test_main_text_output_detailed_exact", "main", scenario_main_text_output_detailed),
    GeneratedScenario("test_infer_domain_names_desktop_security_ai_exact_output", "infer_domain_names", scenario_infer_domain_names_desktop_security_ai),
    GeneratedScenario("test_re_evaluate_project_exact_output", "re_evaluate_project", scenario_re_evaluate_project_exact_output),
    GeneratedScenario("test_print_recommendation_sections_exact", "print_recommendation", scenario_print_recommendation_sections),
)


def existing_test_names(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return set(TEST_NAME_RE.findall(path.read_text(encoding="utf-8")))


def current_hotspots(limit: int = 10) -> list[str]:
    meta_path = workspace_path("mutants/scripts/programstart_recommend.py.meta")
    if not meta_path.exists():
        return []
    try:
        payload = load_json(meta_path)
    except (OSError, json.JSONDecodeError):
        return []
    exit_codes = dict(payload.get("exit_code_by_key", {}))
    counts: dict[str, int] = {}
    for key, exit_code in exit_codes.items():
        if exit_code != 0:
            continue
        match = SURVIVOR_KEY_RE.match(str(key))
        if not match:
            continue
        name = match.group(1)
        counts[name] = counts.get(name, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [name for name, _count in ordered[:limit]]


def choose_internal_scenario(existing_names: set[str], hotspots: list[str]) -> GeneratedScenario | None:
    for hotspot in hotspots:
        for scenario in SCENARIOS:
            if scenario.hotspot == hotspot and scenario.name not in existing_names:
                return scenario
    for scenario in SCENARIOS:
        if scenario.name not in existing_names:
            return scenario
    return None


def append_scenario(path: Path, snippet: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if text and not text.endswith("\n"):
        text += "\n"
    text += "\n\n" + snippet.strip() + "\n"
    path.write_text(text, encoding="utf-8")


def record_application(path: Path, *, scenario: GeneratedScenario, hotspots: list[str], target_file: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "applied_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "scenario": scenario.name,
        "hotspot": scenario.hotspot,
        "hotspots_seen": hotspots,
        "target_file": str(target_file),
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply the next autonomous exact-output mutation hardening test.")
    parser.add_argument(
        "--prompt-file",
        default="devlog/gameplans/mutation_15_cycle_autonomy_prompt.md",
        help="Prompt or instructions file to pass to an optional external command.",
    )
    parser.add_argument(
        "--command",
        help="Optional external command. If provided, the hook runs it instead of the built-in generator.",
    )
    parser.add_argument(
        "--allow-noop",
        action="store_true",
        help="Exit successfully when no external command is configured or no internal scenario remains.",
    )
    parser.add_argument(
        "--target-file",
        default="tests/test_programstart_recommend.py",
        help="Test file to receive generated exact-output scenarios.",
    )
    parser.add_argument(
        "--history-file",
        default="outputs/research/mutation_edit_hook_history.jsonl",
        help="JSONL history file recording which generated scenarios were applied.",
    )
    return parser


def run_external_command(command: str, prompt_path: Path) -> int:
    full_command = f'{command} "{prompt_path}"'
    print(f"Running external mutation edit hook command: {full_command}")
    return subprocess.call(full_command, cwd=workspace_path("."), shell=True)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    prompt_path = workspace_path(args.prompt_file)
    command = args.command or os.environ.get("PROGRAMSTART_MUTATION_EDIT_COMMAND", "").strip()
    if command:
        return run_external_command(command, prompt_path)

    target_path = workspace_path(args.target_file)
    history_path = workspace_path(args.history_file)
    existing_names = existing_test_names(target_path)
    hotspots = current_hotspots()
    scenario = choose_internal_scenario(existing_names, hotspots)
    if scenario is None:
        if args.allow_noop:
            print("No internal mutation scenario remains; hook is a no-op.")
            return 0
        raise SystemExit("No internal mutation scenario remains to apply.")

    append_scenario(target_path, scenario.render())
    record_application(history_path, scenario=scenario, hotspots=hotspots, target_file=target_path)
    print(f"Applied internal mutation scenario: {scenario.name} (hotspot: {scenario.hotspot})")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart mutation-edit-hook'")
    raise SystemExit(main())