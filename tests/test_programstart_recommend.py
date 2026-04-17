from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_recommend as recommend
from scripts.programstart_recommend import ProjectRecommendation

# ── normalize_text ─────────────────────────────────────────────────────────────


def test_normalize_text_lowercases() -> None:
    assert recommend.normalize_text("Hello World") == "hello world"


def test_normalize_text_collapses_separators() -> None:
    assert recommend.normalize_text("AI/ML--platform") == "ai ml platform"


def test_normalize_text_strips_whitespace() -> None:
    assert recommend.normalize_text("  spaces  ") == "spaces"


def test_normalize_text_empty_string() -> None:
    assert recommend.normalize_text("") == ""


# ── tokenize_text ──────────────────────────────────────────────────────────────


def test_tokenize_text_returns_set_of_tokens() -> None:
    tokens = recommend.tokenize_text("web app with auth")
    assert "web" in tokens
    assert "app" in tokens
    assert "auth" in tokens


def test_tokenize_text_ignores_empty_tokens() -> None:
    tokens = recommend.tokenize_text("a--b")
    assert "" not in tokens


# ── expand_capability_terms ────────────────────────────────────────────────────


def test_expand_capability_terms_maps_alias_to_canonical() -> None:
    expanded = recommend.expand_capability_terms({"llm"})
    assert "ai" in expanded


def test_expand_capability_terms_maps_retrieval_to_rag() -> None:
    expanded = recommend.expand_capability_terms({"retrieval"})
    assert "rag" in expanded


def test_expand_capability_terms_includes_original_term() -> None:
    expanded = recommend.expand_capability_terms({"database"})
    assert "database" in expanded


def test_expand_capability_terms_empty_input() -> None:
    assert recommend.expand_capability_terms(set()) == set()


# ── normalized_trigger_set ─────────────────────────────────────────────────────


def test_normalized_trigger_set_lowercases_values() -> None:
    result = recommend.normalized_trigger_set(["Web App", "CLI Tool"])
    assert "web app" in result
    assert "cli tool" in result


def test_normalized_trigger_set_drops_empty_strings() -> None:
    result = recommend.normalized_trigger_set(["", "valid"])
    assert "" not in result


# ── normalize_shape ────────────────────────────────────────────────────────────


def test_normalize_shape_lowercases_and_strips() -> None:
    assert recommend.normalize_shape("  Web App  ") == "web app"


def test_normalize_shape_returns_other_for_empty() -> None:
    assert recommend.normalize_shape("") == "other"


def test_normalize_shape_returns_other_for_none() -> None:
    assert recommend.normalize_shape(None) == "other"  # type: ignore[arg-type]


# ── infer_variant ──────────────────────────────────────────────────────────────


def test_infer_variant_regulated_returns_enterprise() -> None:
    assert recommend.infer_variant("web app", set(), regulated=True) == "enterprise"


def test_infer_variant_cli_with_no_complex_needs_returns_lite() -> None:
    assert recommend.infer_variant("cli tool", set(), regulated=False) == "lite"


def test_infer_variant_cli_with_agents_returns_product() -> None:
    assert recommend.infer_variant("cli tool", {"agents"}, regulated=False) == "product"


def test_infer_variant_web_app_returns_product() -> None:
    # web app doesn't hit the cli/library fast path -> should return "product"
    result = recommend.infer_variant("web app", set(), regulated=False)
    assert result == "product"


def test_infer_variant_audit_need_returns_enterprise() -> None:
    result = recommend.infer_variant("api service", {"audit"}, regulated=False)
    assert result == "enterprise"


# ── build_recommendation (integration via mocked KB) ──────────────────────────


def _minimal_kb() -> dict:
    return {
        "stacks": [],
        "provisioning_services": [],
        "third_party_apis": [],
        "cli_tools": [],
        "coverage_domains": [],
        "comparisons": [],
        "relationships": [],
        "integration_patterns": [],
        "decision_rules": [],
        "prompt_engineering_guidance": {},
    }


def _minimal_registry() -> dict:
    return {
        "workflow_guidance": {
            "kickoff": {"files": ["PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md"]},
        },
    }


def test_build_recommendation_returns_correct_shape() -> None:
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        result = recommend.build_recommendation(
            product_shape="web app",
            needs=set(),
            regulated=False,
            attach_userjourney=None,
        )
    assert isinstance(result, ProjectRecommendation)
    assert result.product_shape == "web app"


def test_build_recommendation_attaches_userjourney_for_web_app() -> None:
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        result = recommend.build_recommendation(
            product_shape="web app",
            needs=set(),
            regulated=False,
            attach_userjourney=None,
        )
    assert result.attach_userjourney is True


def test_build_recommendation_explicit_attach_false_overrides_default() -> None:
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        result = recommend.build_recommendation(
            product_shape="web app",
            needs=set(),
            regulated=False,
            attach_userjourney=False,
        )
    assert result.attach_userjourney is False


def test_build_recommendation_regulated_flag_produces_enterprise() -> None:
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        result = recommend.build_recommendation(
            product_shape="api service",
            needs=set(),
            regulated=True,
            attach_userjourney=False,
        )
    assert result.variant == "enterprise"


def test_build_recommendation_cli_tool_no_complex_needs_is_lite() -> None:
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        result = recommend.build_recommendation(
            product_shape="cli tool",
            needs=set(),
            regulated=False,
            attach_userjourney=False,
        )
    assert result.variant == "lite"


# ── main ───────────────────────────────────────────────────────────────────────


def test_main_text_mode_returns_zero() -> None:
    mock_rec = ProjectRecommendation(
        product_shape="web app",
        variant="product",
        attach_userjourney=True,
        archetype="Interactive product workflow",
    )
    with (
        patch.object(recommend, "load_recommendation_inputs", return_value=("web app", set())),
        patch.object(recommend, "build_recommendation", return_value=mock_rec),
        patch.object(recommend, "print_recommendation"),
    ):
        result = recommend.main(["--product-shape", "web app"])
    assert result == 0


def test_main_json_mode_emits_json(capsys) -> None:
    import json as json_mod

    mock_rec = ProjectRecommendation(
        product_shape="api service",
        variant="product",
        attach_userjourney=False,
        archetype="Typed API and automation platform",
    )
    with (
        patch.object(recommend, "load_recommendation_inputs", return_value=("api service", set())),
        patch.object(recommend, "build_recommendation", return_value=mock_rec),
    ):
        result = recommend.main(["--product-shape", "api service", "--json"])
    assert result == 0
    captured = capsys.readouterr()
    data = json_mod.loads(captured.out)
    assert data["product_shape"] == "api service"


# ── classify_actionability ─────────────────────────────────────────────────────


def test_classify_actionability_service_automated() -> None:
    assert recommend.classify_actionability(category="service", entry={"automation_supported": True}) == "automation-supported"


def test_classify_actionability_service_manual() -> None:
    assert recommend.classify_actionability(category="service", entry={}) == "manual-setup"


def test_classify_actionability_api() -> None:
    assert recommend.classify_actionability(category="api", entry={}) == "manual-setup"


def test_classify_actionability_cli() -> None:
    assert recommend.classify_actionability(category="cli", entry={}) == "manual-setup"


def test_classify_actionability_other() -> None:
    assert recommend.classify_actionability(category="unknown", entry={}) == "advice-only"


# ── shape_profile ──────────────────────────────────────────────────────────────


def test_shape_profile_cli_tool() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("cli tool")
    assert "CLI" in archetype
    assert "uv" in baselines


def test_shape_profile_api_service() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("api service")
    assert "API" in archetype
    assert "FastAPI" in baselines


def test_shape_profile_web_app() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("web app")
    assert "Interactive" in archetype
    assert "Next.js" in baselines


def test_shape_profile_mobile_app() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("mobile app")
    assert "Mobile" in archetype
    assert "React Native" in baselines


def test_shape_profile_data_pipeline() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("data pipeline")
    assert "Data" in archetype
    assert "DuckDB" in baselines


def test_shape_profile_unknown_fallback() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("unknown shape")
    assert "Balanced" in archetype


# ── stack_entry_text / stack_risk_text ─────────────────────────────────────────


def test_stack_entry_text_concatenates() -> None:
    entry = {"name": "FastAPI", "layer": "backend", "aliases": ["fastapi"], "strengths": ["fast", "typed"]}
    text = recommend.stack_entry_text(entry)
    assert "fastapi" in text
    assert "backend" in text
    assert "typed" in text


def test_stack_risk_text_extracts_risk_fields() -> None:
    entry = {"tradeoffs": ["complexity"], "avoid_when": ["small teams"], "risks": ["vendor lock-in"]}
    text = recommend.stack_risk_text(entry)
    assert "complexity" in text.lower() or "vendor" in text.lower()


# ── merge_unique_names ─────────────────────────────────────────────────────────


def test_merge_unique_names_deduplicates() -> None:
    result = recommend.merge_unique_names(["FastAPI", "fastapi", "PostgreSQL", "FASTAPI"])
    assert len(result) == 2
    assert "FastAPI" in result


# ── matching_decision_rules ────────────────────────────────────────────────────


def test_matching_decision_rules_by_shape() -> None:
    kb = {
        "decision_rules": [
            {
                "title": "Use JWT",
                "match_product_shapes": ["web app"],
                "match_needs": [],
                "match_domains": [],
                "layer": "auth",
                "preferred_items": ["JWT"],
            },
        ],
    }
    rules = recommend.matching_decision_rules(
        product_shape="web app",
        needs=set(),
        matched_domains=[],
        knowledge_base=kb,
    )
    assert len(rules) == 1
    assert rules[0]["title"] == "Use JWT"


def test_matching_decision_rules_no_match() -> None:
    kb = {
        "decision_rules": [
            {
                "title": "Use JWT",
                "match_product_shapes": ["mobile app"],
                "match_needs": [],
                "match_domains": [],
                "layer": "auth",
                "preferred_items": ["JWT"],
            },
        ],
    }
    rules = recommend.matching_decision_rules(
        product_shape="cli tool",
        needs=set(),
        matched_domains=[],
        knowledge_base=kb,
    )
    assert len(rules) == 0


# ── matching_integration_patterns ──────────────────────────────────────────────


def test_matching_integration_patterns_by_need() -> None:
    kb = {
        "integration_patterns": [
            {"name": "OAuth flow", "fit_for": ["authentication"], "components": ["Supabase", "Next.js"]},
        ],
    }
    result = recommend.matching_integration_patterns(product_shape="web app", needs={"authentication"}, knowledge_base=kb)
    assert "supabase" in result or "next.js" in result


def test_matching_integration_patterns_no_match() -> None:
    kb = {
        "integration_patterns": [
            {"name": "OAuth flow", "fit_for": ["mobile auth"], "components": ["Firebase"]},
        ],
    }
    result = recommend.matching_integration_patterns(product_shape="cli tool", needs=set(), knowledge_base=kb)
    assert len(result) == 0


# ── build_actionability_summary ────────────────────────────────────────────────


def test_build_actionability_summary_basic() -> None:
    kb = {
        "provisioning_services": [{"name": "Vercel", "automation_supported": True}],
        "third_party_apis": [{"name": "Stripe"}],
        "cli_tools": [{"name": "uv"}],
    }
    summary = recommend.build_actionability_summary(
        stack_evidence=[{"name": "Next.js"}],
        service_names=["Vercel"],
        api_names=["Stripe"],
        cli_names=["uv"],
        knowledge_base=kb,
    )
    categories = {item["category"] for item in summary}
    assert "stack" in categories
    assert "service" in categories


# ── normalize_prompt_guidance ──────────────────────────────────────────────────


def test_normalize_prompt_guidance_extracts_fields() -> None:
    guidance = {
        "principles": ["Be explicit", "Be explicit"],
        "patterns": [{"name": "P1", "description": "d1"}],
        "anti_patterns": [{"name": "A1", "description": "bad"}],
    }
    principles, patterns, anti_patterns = recommend.normalize_prompt_guidance(guidance)
    assert "Be explicit" in principles
    assert len(principles) == 1  # deduplication
    assert len(patterns) >= 1


def test_normalize_prompt_guidance_empty_kb() -> None:
    guidance: dict = {}
    principles, patterns, anti_patterns = recommend.normalize_prompt_guidance(guidance)
    assert principles == []
    assert patterns == []
    # Hardcoded defaults are returned when anti_patterns is empty
    assert len(anti_patterns) == 3


# ── actionability_follow_up_commands ───────────────────────────────────────────


def test_actionability_follow_up_commands() -> None:
    summary = [
        {"name": "Vercel", "category": "service", "actionability": "automation-supported"},
        {"name": "Stripe", "category": "api", "actionability": "manual-setup"},
    ]
    cmds = recommend.actionability_follow_up_commands(summary)
    assert isinstance(cmds, list)


# ── comparison_bonus ───────────────────────────────────────────────────────────


def test_comparison_bonus_returns_tuple() -> None:
    comparisons = [
        {"name": "X vs Y", "items": [{"name": "X", "verdict": "preferred"}], "context": "speed"},
    ]
    result = recommend.comparison_bonus(
        item_name="X",
        selected_stacks={"Y"},
        needs=set(),
        comparisons=comparisons,
    )
    assert isinstance(result, tuple)
    assert isinstance(result[0], int)


# ── infer_domain_names ─────────────────────────────────────────────────────────


def test_infer_domain_names_basic() -> None:
    kb = {
        "coverage_domains": [
            {"name": "Developer experience, quality, and supply chain"},
            {"name": "Web and frontend product delivery"},
        ],
    }
    domains = recommend.infer_domain_names("web app", set(), False, kb)
    assert isinstance(domains, list)
    assert len(domains) >= 1


# ── print_recommendation ──────────────────────────────────────────────────────


def test_print_recommendation_text(capsys) -> None:
    rec = ProjectRecommendation(
        product_shape="web app",
        variant="product",
        attach_userjourney=True,
        archetype="Interactive product workflow",
        stack_evidence=[{"name": "Next.js", "score": 1.0}],
        service_names=["Vercel"],
        api_names=["Stripe"],
        cli_tool_names=["uv"],
    )
    recommend.print_recommendation(rec)
    out = capsys.readouterr().out
    assert "web app" in out


# ── parse_kickoff_inputs ──────────────────────────────────────────────────────


def test_parse_kickoff_inputs(tmp_path) -> None:
    kickoff = tmp_path / "PROGRAMBUILD" / "PROGRAMBUILD_KICKOFF_PACKET.md"
    kickoff.parent.mkdir()
    kickoff.write_text(
        "```text\nPROJECT_NAME: TestApp\nPRODUCT_SHAPE: web app\nSUCCESS_METRIC: 100 users\n```",
        encoding="utf-8",
    )
    result = recommend.parse_kickoff_inputs(kickoff)
    assert result.get("PROJECT_NAME") == "TestApp"
    assert result.get("PRODUCT_SHAPE") == "web app"


# ── preferred_rule_items_for_layer ─────────────────────────────────────────────


def test_preferred_rule_items_for_layer() -> None:
    rules = [
        {"target_layers": ["stacks"], "prefer_items": ["FastAPI", "Django"]},
        {"target_layers": ["cli_tools"], "prefer_items": ["uv"]},
    ]
    kb = {
        "stacks": [{"name": "FastAPI"}, {"name": "Django"}],
        "cli_tools": [{"name": "uv"}],
    }
    result = recommend.preferred_rule_items_for_layer(rules=rules, knowledge_base=kb, layer="stacks")
    assert "FastAPI" in result
    assert "uv" not in result


# ── select_triggered_entries ───────────────────────────────────────────────────


def test_select_triggered_entries_by_shape() -> None:
    entries = [
        {"name": "Vercel", "trigger_shapes": ["web app"], "trigger_needs": [], "notes": ["Deploy to edge"]},
        {"name": "Railway", "trigger_shapes": ["api service"], "trigger_needs": []},
    ]
    names, notes, evidence, alts = recommend.select_triggered_entries(
        entries=entries,
        product_shape="web app",
        needs=set(),
        stack_names=[],
    )
    assert "Vercel" in names
    assert "Railway" not in names


def test_select_triggered_entries_by_need() -> None:
    entries = [
        {"name": "Stripe", "trigger_shapes": [], "trigger_needs": ["payments"]},
    ]
    names, notes, evidence, alts = recommend.select_triggered_entries(
        entries=entries,
        product_shape="web app",
        needs={"payments"},
        stack_names=[],
        category="third_party_apis",
        min_score=1,
    )
    assert "Stripe" in names


def test_select_triggered_entries_filters_low_score() -> None:
    entries = [
        {"name": "Obscure", "trigger_shapes": [], "trigger_needs": []},
    ]
    names, notes, evidence, alts = recommend.select_triggered_entries(
        entries=entries,
        product_shape="web app",
        needs=set(),
        stack_names=[],
        min_score=4,
    )
    assert "Obscure" not in names


def test_select_triggered_entries_with_decision_rules() -> None:
    entries = [
        {"name": "FastAPI", "trigger_shapes": ["api service"], "trigger_needs": []},
    ]
    rules = [
        {
            "title": "Use FastAPI",
            "match_product_shapes": ["api service"],
            "match_needs": [],
            "match_domains": [],
            "target_layers": [],
            "prefer_items": ["FastAPI"],
            "avoid_items": [],
        }
    ]
    names, notes, evidence, alts = recommend.select_triggered_entries(
        entries=entries,
        product_shape="api service",
        needs=set(),
        stack_names=[],
        decision_rules=rules,
    )
    assert "FastAPI" in names


def test_select_triggered_entries_api_requires_trigger() -> None:
    """Third-party APIs with no matching triggers should be excluded."""
    entries = [
        {"name": "RandomAPI", "trigger_shapes": [], "trigger_needs": []},
    ]
    names, notes, evidence, alts = recommend.select_triggered_entries(
        entries=entries,
        product_shape="web app",
        needs=set(),
        stack_names=[],
        category="third_party_apis",
    )
    assert "RandomAPI" not in names


# ── build_stack_candidates ─────────────────────────────────────────────────────


def test_build_stack_candidates_basic() -> None:
    kb = _minimal_kb()
    kb["stacks"] = [
        {"name": "Next.js", "trigger_shapes": ["web app"], "strengths": ["fast"], "layer": "frontend"},
        {"name": "FastAPI", "trigger_shapes": ["api service"], "strengths": ["typed"], "layer": "backend"},
    ]
    kb["coverage_domains"] = [
        {"name": "Web and frontend product delivery", "status": "strong", "representative_tools": ["Next.js"]},
    ]
    kb.setdefault("comparisons", [])
    kb.setdefault("relationships", [])
    kb.setdefault("integration_patterns", [])
    kb.setdefault("decision_rules", [])

    result = recommend.build_stack_candidates("web app", set(), False, kb)
    assert isinstance(result, tuple)
    assert len(result) == 8
    archetype = result[0]
    assert isinstance(archetype, str)


# ── print_recommendation (full branches) ──────────────────────────────────────


def test_print_recommendation_full_branches(capsys) -> None:
    rec = ProjectRecommendation(
        product_shape="api service",
        variant="product",
        attach_userjourney=True,
        archetype="API-first service",
        stack_names=["FastAPI"],
        service_names=["Vercel"],
        cli_tool_names=["uv"],
        api_names=["Stripe"],
        rationale=["Chosen for speed"],
        coverage_warnings=[{"domain": "Auth", "status": "partial", "gaps": "No SSO yet"}],
        stack_evidence=[{"name": "FastAPI", "score": 10, "reasons": ["fast", "typed"]}],
        service_evidence=[{"name": "Vercel", "score": 8, "reasons": ["edge deploy"]}],
        api_evidence=[{"name": "Stripe", "score": 7, "reasons": ["payments"]}],
        cli_evidence=[{"name": "uv", "score": 6, "reasons": ["fast installs"]}],
        rule_evidence=[{"title": "Use FastAPI", "because": "typed", "confidence": "high"}],
        actionability_summary=[
            {"name": "Vercel", "category": "service", "actionability": "automation-supported", "reason": "API available"}
        ],
        alternatives=[{"item": "Django", "category": "stack", "rationale": "monolithic"}],
        service_notes=["Needs API key"],
        cli_notes=["Install via pipx"],
        api_notes=["Rate limited"],
        kickoff_files=["KICKOFF.md"],
        next_commands=["programstart guide"],
    )
    recommend.print_recommendation(rec)
    out = capsys.readouterr().out
    assert "api service" in out
    assert "FastAPI" in out
    assert "Vercel" in out
    assert "Stripe" in out
    assert "coverage warnings" in out
    assert "stack evidence" in out
    assert "rule evidence" in out
    assert "actionability summary" in out
    assert "alternatives" in out
    assert "service notes" in out
    assert "cli notes" in out
    assert "api notes" in out


# ── re_evaluate_project ───────────────────────────────────────────────────────


def test_re_evaluate_project(tmp_path) -> None:
    kickoff_dir = tmp_path / "PROGRAMBUILD"
    kickoff_dir.mkdir()
    (kickoff_dir / "PROGRAMBUILD_KICKOFF_PACKET.md").write_text(
        "```text\nPROJECT_NAME: TestApp\nPRODUCT_SHAPE: web app\n```",
        encoding="utf-8",
    )
    result = recommend.re_evaluate_project(str(tmp_path))
    assert result["product_shape"] == "web app"
    assert "current_recommendation" in result
    assert "deltas" in result


# ── load_recommendation_inputs ─────────────────────────────────────────────────


def test_load_recommendation_inputs_explicit_shape() -> None:
    ns = argparse.Namespace(product_shape="cli tool", need=["rag"])
    with patch.object(recommend, "parse_kickoff_inputs", return_value={}):
        shape, needs = recommend.load_recommendation_inputs(ns)
    assert shape == "cli tool"
    assert "rag" in needs


# ---------------------------------------------------------------------------
# Phase B: coverage push — previously uncovered branches in recommend.py
# ---------------------------------------------------------------------------


def test_matching_decision_rules_filters_domain_mismatch() -> None:
    """Line 143: rule with match_domains that doesn't match product domains → filtered out."""
    rules = [
        {
            "title": "healthcare niche rule",
            "match_domains": ["healthcare"],
            "prefer_items": [],
            "avoid_items": [],
        }
    ]
    result = recommend.matching_decision_rules(
        product_shape="cli tool",
        needs=set(),
        matched_domains=["devops"],  # no "healthcare" → domain filter fires
        knowledge_base={"decision_rules": rules},
    )
    assert result == []


def test_build_actionability_summary_skips_unknown_service_name() -> None:
    """Line 180: service name not found in provisioning_services entries → skipped."""
    result = recommend.build_actionability_summary(
        stack_evidence=[],
        service_names=["NONEXISTENT_SERVICE_PHASE_B"],
        api_names=[],
        cli_names=[],
        knowledge_base={"provisioning_services": [{"name": "other_service", "automation_supported": False}]},
    )
    names_in_result = [item.get("name") for item in result]
    assert "NONEXISTENT_SERVICE_PHASE_B" not in names_in_result


# ── stack_exists ───────────────────────────────────────────────────────────────


def test_stack_exists_true() -> None:
    kb = {"stacks": [{"name": "FastAPI"}, {"name": "Next.js"}]}
    assert recommend.stack_exists(kb, "FastAPI") is True


def test_stack_exists_false() -> None:
    kb = {"stacks": [{"name": "FastAPI"}]}
    assert recommend.stack_exists(kb, "Django") is False


# ── Phase B: UI capability alias tests ────────────────────────────────────────


def test_expand_capability_terms_dashboard_alias() -> None:
    expanded = recommend.expand_capability_terms({"admin dashboard"})
    assert "dashboard" in expanded


def test_expand_capability_terms_web_ui_alias() -> None:
    expanded = recommend.expand_capability_terms({"web portal"})
    assert "web interface" in expanded


def test_expand_capability_terms_monitoring_ui_alias() -> None:
    expanded = recommend.expand_capability_terms({"status page"})
    assert "monitoring ui" in expanded


def test_need_dashboard_maps_to_frontend_domain() -> None:
    kb = {
        "coverage_domains": [
            {"name": "Web and frontend product delivery"},
        ],
    }
    domains = recommend.infer_domain_names("api service", {"dashboard"}, False, kb)
    assert "Web and frontend product delivery" in domains


def test_api_shape_with_dashboard_need_includes_frontend() -> None:
    """API service shape + --need dashboard should surface frontend domain."""
    kb = {
        "coverage_domains": [
            {"name": "Web and frontend product delivery"},
            {"name": "API, workflow, and backend platforms"},
        ],
    }
    domains = recommend.infer_domain_names("api service", {"dashboard"}, False, kb)
    assert "Web and frontend product delivery" in domains


# ── ui_tier ────────────────────────────────────────────────────────────────────


def test_ui_tier_web_app_returns_full_product_ui() -> None:
    assert recommend.ui_tier("web app", set()) == "full-product-ui"


def test_ui_tier_mobile_app_returns_full_product_ui() -> None:
    assert recommend.ui_tier("mobile app", set()) == "full-product-ui"


def test_ui_tier_api_with_dashboard_need_returns_minimal_admin() -> None:
    assert recommend.ui_tier("api service", {"dashboard"}) == "minimal-admin"


def test_ui_tier_cli_with_monitoring_ui_need_returns_minimal_admin() -> None:
    assert recommend.ui_tier("cli tool", {"monitoring ui"}) == "minimal-admin"


def test_ui_tier_library_returns_docs_only() -> None:
    assert recommend.ui_tier("library", set()) == "docs-only"


def test_ui_tier_api_no_ui_needs_returns_none() -> None:
    assert recommend.ui_tier("api service", set()) == "none"


def test_ui_tier_data_pipeline_with_admin_ui_returns_minimal_admin() -> None:
    assert recommend.ui_tier("data pipeline", {"admin ui"}) == "minimal-admin"


# ── companion surface advisory (build_recommendation) ──────────────────────────


def test_build_recommendation_api_with_dashboard_need_adds_companion_surface() -> None:
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        result = recommend.build_recommendation(
            product_shape="api service",
            needs={"dashboard"},
            regulated=False,
            attach_userjourney=False,
        )
    assert "admin dashboard" in result.suggested_companion_surfaces
    companion_warnings = [w for w in result.coverage_warnings if w.get("domain") == "Companion UI"]
    assert len(companion_warnings) == 1
    assert companion_warnings[0]["status"] == "advisory"


def test_build_recommendation_web_app_no_companion_surface() -> None:
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        result = recommend.build_recommendation(
            product_shape="web app",
            needs={"dashboard"},
            regulated=False,
            attach_userjourney=None,
        )
    assert result.suggested_companion_surfaces == []


def test_build_recommendation_api_no_frontend_domain_adds_advisory() -> None:
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        result = recommend.build_recommendation(
            product_shape="api service",
            needs=set(),
            regulated=False,
            attach_userjourney=False,
        )
    frontend_warnings = [w for w in result.coverage_warnings if w.get("domain") == "Frontend coverage"]
    assert len(frontend_warnings) == 1
    assert frontend_warnings[0]["status"] == "advisory"


# ── migrated from test_audit_fixes.py ──────────────────────────────────────────


def test_data_pipeline_ml_training_selects_ml_stacks() -> None:
    rec = recommend.build_recommendation(
        product_shape="data pipeline",
        needs={"ml", "training"},
        regulated=False,
        attach_userjourney=False,
    )
    stacks_lower = {s.lower() for s in rec.stack_names}
    assert "weights & biases" in stacks_lower
    assert "hugging face transformers" in stacks_lower
    assert "polars" in stacks_lower
    assert rec.variant == "product"
    assert rec.confidence == "high"


def test_cli_tool_ml_agents_fires_all_three_rules() -> None:
    rec = recommend.build_recommendation(
        product_shape="cli tool",
        needs={"ml", "agents"},
        regulated=False,
        attach_userjourney=False,
    )
    rule_titles = {item["title"] for item in rec.rule_evidence}
    assert "Prefer explicit LLM routing and typed response validation for AI product workflows" in rule_titles
    assert "Prefer durable orchestration for agent and multi-step automation systems" in rule_titles
    assert "Prefer explicit experiment tracking and typed data pipelines for ML training workloads" in rule_titles
    assert rec.variant == "product"


def test_cli_tool_baseline_still_lite() -> None:
    rec = recommend.build_recommendation(
        product_shape="cli tool",
        needs=set(),
        regulated=False,
        attach_userjourney=False,
    )
    assert rec.variant == "lite"


def test_matching_integration_patterns_real_kb_rag_needs() -> None:
    kb = {
        "integration_patterns": [
            {
                "name": "RAG pipeline with evaluation",
                "fit_for": ["knowledge-base Q&A", "document search", "context-augmented generation"],
                "components": ["Pydantic", "pytest"],
            },
            {
                "name": "Unrelated pattern",
                "fit_for": ["admin-heavy apps"],
                "components": ["Django"],
            },
        ]
    }
    result = recommend.matching_integration_patterns(
        product_shape="api service",
        needs={"search"},
        knowledge_base=kb,
    )
    assert "pydantic" in result
    assert "django" not in result


def test_integration_patterns_boost_stacks_in_real_kb() -> None:
    rec = recommend.build_recommendation(
        product_shape="api service",
        needs={"agents", "rag"},
        regulated=False,
        attach_userjourney=False,
    )
    pattern_mentioned = any(
        any("integration pattern" in str(r).lower() for r in item.get("reasons", [])) for item in rec.stack_evidence
    )
    assert pattern_mentioned, "Expected at least one stack to mention integration pattern matching"


def test_integration_patterns_do_not_inflate_unrelated_shapes() -> None:
    rec = recommend.build_recommendation(
        product_shape="cli tool",
        needs=set(),
        regulated=False,
        attach_userjourney=False,
    )
    pattern_mentioned = any(
        any("integration pattern" in str(r).lower() for r in item.get("reasons", [])) for item in rec.stack_evidence
    )
    assert not pattern_mentioned, "Plain CLI tool should not get integration pattern boosts"


def test_prompt_guidance_normalization_uses_keyed_kb_fields() -> None:
    guidance = {
        "output_contracts": "Define exact sections.",
        "verification_loops": "Check correctness and grounding.",
        "completeness_contracts": "Track deliverables.",
        "tool_persistence": "Retry with alternate strategy on empty results.",
        "citation_rules": "Only cite retrieved sources.",
    }

    principles, patterns, anti_patterns = recommend.normalize_prompt_guidance(guidance)

    assert "Define exact sections." in principles
    assert "Check correctness and grounding." in principles
    assert "Retry with alternate strategy on empty results." in patterns
    assert "Only cite retrieved sources." in patterns
    assert anti_patterns == [
        "Do not invent unsupported files, rules, or citations.",
        "Do not skip verification or assume tool output is complete.",
        "Do not add features, stages, or documents outside the registry authority model.",
    ]


# ── build_stack_candidates: assertion-dense mutation-killing tests ─────────────


def _scoring_kb() -> dict:
    """KB fixture with controlled stacks, domains, rules, comparisons, and relationships."""
    return {
        "stacks": [
            {
                "name": "Next.js",
                "trigger_shapes": ["web app"],
                "strengths": ["ssr", "route driven rendering"],
                "layer": "frontend",
                "tradeoffs": ["complexity"],
            },
            {
                "name": "FastAPI",
                "trigger_shapes": ["api service"],
                "strengths": ["typed", "async io", "validation"],
                "layer": "backend",
            },
            {
                "name": "PostgreSQL",
                "trigger_shapes": ["web app", "api service"],
                "strengths": ["database", "sql"],
                "layer": "data",
            },
            {
                "name": "Playwright",
                "trigger_shapes": ["web app"],
                "strengths": ["browser testing"],
                "layer": "testing",
            },
            {
                "name": "Pydantic",
                "trigger_shapes": ["web app", "cli tool", "api service"],
                "strengths": ["validation", "typed"],
                "layer": "core",
            },
            {
                "name": "OpenTelemetry",
                "trigger_shapes": ["api service"],
                "strengths": ["observability", "audit"],
                "layer": "observability",
            },
            {
                "name": "Ruff",
                "trigger_shapes": ["cli tool"],
                "strengths": ["lint"],
                "layer": "dev",
            },
            {
                "name": "Hypothesis",
                "trigger_shapes": ["cli tool"],
                "strengths": ["testing"],
                "layer": "testing",
            },
        ],
        "coverage_domains": [
            {
                "name": "Web and frontend product delivery",
                "status": "strong",
                "representative_tools": ["Next.js"],
                "summary": "Frontend delivery",
                "current_gaps": [],
            },
            {
                "name": "Cloud, infrastructure, and platform operations",
                "status": "partial",
                "representative_tools": ["PostgreSQL"],
                "summary": "Cloud ops",
                "current_gaps": ["No CDN coverage"],
            },
            {
                "name": "Developer experience, quality, and supply chain",
                "status": "seed",
                "representative_tools": ["Ruff"],
                "summary": "DevEx",
                "current_gaps": ["Early stage"],
            },
        ],
        "comparisons": [
            {
                "name": "Next.js vs Remix",
                "related_items": ["Next.js", "Remix"],
                "compared_versions": [],
                "decision": "Prefer Next.js for SSR-first applications.",
                "summary": "Both support SSR.",
            },
        ],
        "relationships": [
            {
                "subject": "Next.js",
                "object": "PostgreSQL",
                "relation": "complements",
            },
        ],
        "integration_patterns": [
            {
                "name": "Full-stack SSR",
                "fit_for": ["web app", "ssr"],
                "components": ["Next.js", "PostgreSQL"],
            },
        ],
        "decision_rules": [
            {
                "title": "Prefer Playwright for web apps",
                "match_product_shapes": ["web app"],
                "match_needs": [],
                "match_domains": [],
                "target_layers": ["stacks"],
                "prefer_items": ["Playwright"],
                "avoid_items": [],
                "because": "E2E testing is critical for web apps",
                "confidence": "high",
            },
            {
                "title": "Avoid OpenTelemetry for web apps",
                "match_product_shapes": ["web app"],
                "match_needs": [],
                "match_domains": [],
                "target_layers": ["stacks"],
                "prefer_items": [],
                "avoid_items": ["OpenTelemetry"],
                "because": "Overhead in browser context",
                "confidence": "medium",
            },
        ],
        "provisioning_services": [],
        "third_party_apis": [],
        "cli_tools": [],
        "prompt_engineering_guidance": {},
    }


def test_build_stack_candidates_baseline_fit_score() -> None:
    """Baseline stacks get +12 from preferred_lookup match."""
    kb = _scoring_kb()
    _archetype, stacks, evidence, _domains, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    # Next.js is a baseline stack for web app; it should be selected
    assert "Next.js" in stacks
    nextjs_ev = next(e for e in evidence if e["name"] == "Next.js")
    # Baseline fit gives +12; domain representative (strong) gives +8;
    # integration pattern match gives +3; comparison bonus (decision mentions Next.js) gives +3
    assert nextjs_ev["score"] >= 12, f"Expected baseline score >= 12, got {nextjs_ev['score']}"
    assert any("Baseline fit" in r for r in nextjs_ev["reasons"])


def test_build_stack_candidates_domain_representative_scores() -> None:
    """Domain representative stacks get scored by domain status: strong=8, partial=6, seed=4."""
    kb = _scoring_kb()
    _a, _s, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    # Next.js is representative of "Web and frontend" (strong → +8)
    nextjs_ev = next(e for e in evidence if e["name"] == "Next.js")
    assert any("Representative tool" in r and "strong" in r for r in nextjs_ev["reasons"])

    # PostgreSQL is representative of "Cloud, infrastructure" (partial → +6)
    pg_ev = next((e for e in evidence if e["name"] == "PostgreSQL"), None)
    if pg_ev:
        assert any("Representative tool" in r and "partial" in r for r in pg_ev["reasons"])


def test_build_stack_candidates_regulation_bonus() -> None:
    """Regulated flag adds +3 for stacks with security/audit/observability terms."""
    kb = _scoring_kb()
    # OpenTelemetry strengths include 'observability' → regulated bonus
    # But it also gets avoid_items penalty -3 from the "Avoid OpenTelemetry for web apps" rule
    # Use api service shape where no avoid rule applies
    _a, stacks_unreg, evidence_unreg, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates(
        "api service", set(), False, kb
    )
    _a2, stacks_reg, evidence_reg, _d2, _cw2, _alts2, _re2, _conf2 = recommend.build_stack_candidates(
        "api service", set(), True, kb
    )
    otel_unreg = next((e for e in evidence_unreg if e["name"] == "OpenTelemetry"), None)
    otel_reg = next((e for e in evidence_reg if e["name"] == "OpenTelemetry"), None)
    if otel_unreg and otel_reg:
        assert otel_reg["score"] > otel_unreg["score"], "Regulated flag should boost observability stacks"
        assert any("governance" in r.lower() or "observability" in r.lower() for r in otel_reg["reasons"])


def test_build_stack_candidates_decision_rule_prefer() -> None:
    """Decision rule prefer_items adds +4."""
    kb = _scoring_kb()
    _a, stacks, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    # "Prefer Playwright for web apps" rule should add +4
    pw_ev = next((e for e in evidence if e["name"] == "Playwright"), None)
    assert pw_ev is not None, "Playwright should be selected"
    assert any("KB rule preference" in r for r in pw_ev["reasons"])


def test_build_stack_candidates_decision_rule_avoid() -> None:
    """Decision rule avoid_items subtracts -3."""
    kb = _scoring_kb()
    _a, stacks, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    # "Avoid OpenTelemetry for web apps" rule should apply -3
    otel = next((e for e in evidence if e["name"] == "OpenTelemetry"), None)
    if otel:
        assert any("KB rule caution" in r for r in otel["reasons"])


def test_build_stack_candidates_intent_term_scoring() -> None:
    """Intent terms from needs boost stack scores (+2 per term, capped at 10)."""
    kb = _scoring_kb()
    # "validation" is in the intent terms for web app baseline AND matches Pydantic strengths
    _a, stacks, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", {"validation"}, False, kb)
    pydantic_ev = next((e for e in evidence if e["name"] == "Pydantic"), None)
    assert pydantic_ev is not None, "Pydantic should be selected (matches intent term 'validation')"
    assert any("intent terms" in r.lower() for r in pydantic_ev["reasons"])


def test_build_stack_candidates_integration_pattern_boost() -> None:
    """Integration pattern matches give score bonus (+3 per pattern, capped at 6)."""
    kb = _scoring_kb()
    _a, stacks, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    # "Full-stack SSR" pattern matches web app → boosts Next.js and PostgreSQL
    nextjs_ev = next(e for e in evidence if e["name"] == "Next.js")
    assert any("integration pattern" in r.lower() for r in nextjs_ev["reasons"])


def test_build_stack_candidates_complement_relationship_bonus() -> None:
    """Complement relationships add +2 when one partner is in preferred_lookup."""
    kb = _scoring_kb()
    _a, stacks, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    # Next.js complements PostgreSQL; Next.js is baseline → PostgreSQL gets +2
    pg_ev = next((e for e in evidence if e["name"] == "PostgreSQL"), None)
    if pg_ev:
        assert any("Complements" in r for r in pg_ev["reasons"])


def test_build_stack_candidates_comparison_in_alternatives() -> None:
    """Comparisons referencing selected stacks appear in alternatives."""
    kb = _scoring_kb()
    _a, stacks, evidence, _d, _cw, alternatives, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    # "Next.js vs Remix" comparison should produce an alternative entry
    comparison_alts = [a for a in alternatives if a.get("category") == "comparison"]
    assert any("Next.js vs Remix" in a.get("item", "") for a in comparison_alts), (
        f"Expected 'Next.js vs Remix' in comparison alternatives, got {comparison_alts}"
    )


def test_build_stack_candidates_tradeoff_penalty() -> None:
    """Stacks with tradeoffs matching intent terms get score penalty (-1 per caution, capped at -4)."""
    kb = _scoring_kb()
    # Next.js has tradeoffs=["complexity"]; if "complexity" becomes an intent term AND appears in risk_blob
    # We need to craft needs so "complexity" ends up in intent_terms
    # Actually, the penalty applies when matched_terms overlap with risk_blob
    # risk_blob = stack_risk_text(entry) which reads tradeoffs/avoid_when/risks
    # For Next.js: risk_blob = "complexity"
    # matched_terms are intent_terms that appear in text_blob (strengths+trigger_shapes)
    # "complexity" would need to be in text_blob too, which it's not (it's in tradeoffs not strengths)
    # So this penalty is hard to trigger with Next.js
    # Let's test with a custom stack
    kb["stacks"].append(
        {
            "name": "HeavyFramework",
            "trigger_shapes": ["web app"],
            "strengths": ["ssr", "security", "validation"],
            "tradeoffs": ["validation overhead"],
        }
    )
    _a, stacks, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", {"validation"}, False, kb)
    heavy_ev = next((e for e in evidence if e["name"] == "HeavyFramework"), None)
    if heavy_ev:
        assert any("tradeoffs" in r.lower() for r in heavy_ev["reasons"])


def test_build_stack_candidates_zero_score_excluded() -> None:
    """Stacks with score <= 0 are excluded from candidates."""
    kb = _scoring_kb()
    # FastAPI has trigger_shapes=["api service"] — for "web app" shape it gets no baseline score
    # and no domain representative score, so it should be excluded or score very low
    _a, stacks, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    # Ruff/Hypothesis have trigger_shapes=["cli tool"] so unlikely to appear for web app
    ruff_ev = next((e for e in evidence if e["name"] == "Ruff"), None)
    hypothesis_ev = next((e for e in evidence if e["name"] == "Hypothesis"), None)
    assert ruff_ev is None, "Ruff should not appear for web app"
    assert hypothesis_ev is None, "Hypothesis should not appear for web app"


def test_build_stack_candidates_ordering_by_score_then_name() -> None:
    """Candidates are ordered by descending score then ascending name."""
    kb = _scoring_kb()
    _a, stacks, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    scores = [e["score"] for e in evidence]
    # Scores must be non-increasing
    for i in range(len(scores) - 1):
        assert scores[i] >= scores[i + 1], f"Evidence not sorted by score: {scores}"


def test_build_stack_candidates_selection_budget_limits() -> None:
    """Selection budget is len(preferred) + 2 + extra from rules."""
    kb = _scoring_kb()
    # web app baseline has 4 stacks: Next.js, PostgreSQL, Playwright, Pydantic
    # budget = 4 + 2 + max(0, rule_preferred - baseline) = 6 + extras
    _a, stacks, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    # Should not exceed reasonable bounds
    assert len(stacks) <= 10, f"Too many stacks selected: {len(stacks)}"
    assert len(stacks) >= 1, "Should select at least one stack"


def test_build_stack_candidates_coverage_warnings_partial_seed() -> None:
    """Coverage warnings appear for domains with status partial or seed."""
    kb = _scoring_kb()
    _a, _s, _ev, _d, coverage_warnings, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    # "Web and frontend" is strong — should NOT appear in warnings
    assert not any(w["status"] == "strong" for w in coverage_warnings), "Strong domains should not produce warnings"
    # Each warning should have domain, status, summary, gaps fields
    for w in coverage_warnings:
        assert "domain" in w
        assert "status" in w
        assert "summary" in w
        assert "gaps" in w


def test_build_stack_candidates_confidence_seed_is_low() -> None:
    """Confidence is 'low' when any selected domain has seed status."""
    kb = _scoring_kb()
    # cli tool baseline maps to "Developer experience, quality, and supply chain" which is seed
    _a, _s, _ev, _d, cw, _alts, _re, confidence = recommend.build_stack_candidates("cli tool", set(), False, kb)
    if any(w["status"] == "seed" for w in cw):
        assert confidence == "low", f"Expected 'low' confidence with seed domain, got '{confidence}'"


def test_build_stack_candidates_confidence_partial_is_medium() -> None:
    """Confidence is 'medium' when coverage_warnings exist but no seed domain."""
    kb = _scoring_kb()
    # Remove seed domain, keep only partial
    kb["coverage_domains"] = [d for d in kb["coverage_domains"] if d["status"] != "seed"]
    _a, _s, _ev, _d, cw, _alts, _re, confidence = recommend.build_stack_candidates("api service", set(), False, kb)
    if cw and not any(w["status"] == "seed" for w in cw):
        assert confidence == "medium", f"Expected 'medium' confidence with partial domain, got '{confidence}'"


def test_build_stack_candidates_confidence_high_when_no_warnings() -> None:
    """Confidence is 'high' when no coverage warnings and >= 3 candidates."""
    kb = _scoring_kb()
    # Make all domains strong so no warnings
    for d in kb["coverage_domains"]:
        d["status"] = "strong"
    _a, _s, _ev, _d, cw, _alts, _re, confidence = recommend.build_stack_candidates("web app", set(), False, kb)
    if not cw:
        assert confidence == "high", f"Expected 'high' confidence with no warnings, got '{confidence}'"


def test_build_stack_candidates_alternatives_are_non_selected() -> None:
    """Alternatives are candidates that scored but weren't selected."""
    kb = _scoring_kb()
    _a, stacks, _ev, _d, _cw, alternatives, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    for alt in alternatives:
        assert "item" in alt
        assert "category" in alt
        assert "rationale" in alt
        # Alternatives with category "stack" should not be in selected stacks
        if alt["category"] == "stack":
            assert alt["item"] not in stacks, f"Alternative {alt['item']} is also in selected stacks"


def test_build_stack_candidates_rule_evidence_structure() -> None:
    """Rule evidence has title, because, confidence fields."""
    kb = _scoring_kb()
    _a, _s, _ev, _d, _cw, _alts, rule_evidence, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    assert len(rule_evidence) >= 1, "web app should trigger at least one decision rule"
    for item in rule_evidence:
        assert "title" in item
        assert "because" in item
        assert "confidence" in item
        assert isinstance(item["title"], str) and item["title"]
        assert isinstance(item["because"], str) and item["because"]
        assert item["confidence"] in {"low", "medium", "high"}


def test_build_stack_candidates_matched_domains_returned() -> None:
    """matched_domain_names reflects actual selected domains."""
    kb = _scoring_kb()
    _a, _s, _ev, matched_domains, _cw, _alts, _re, _conf = recommend.build_stack_candidates("web app", set(), False, kb)
    assert isinstance(matched_domains, list)
    # web app baseline maps to "Web and frontend" and "Cloud, infrastructure"
    # At least the first one should appear since it exists in the KB
    assert len(matched_domains) >= 1


def test_build_stack_candidates_evidence_reasons_capped() -> None:
    """Stack evidence reasons are capped at 4 items."""
    kb = _scoring_kb()
    _a, _s, evidence, _d, _cw, _alts, _re, _conf = recommend.build_stack_candidates(
        "web app", {"validation", "testing", "ssr", "authentication"}, False, kb
    )
    for item in evidence:
        assert len(item["reasons"]) <= 4, f"{item['name']} has {len(item['reasons'])} reasons, expected <= 4"


# ── build_recommendation: assertion-dense mutation-killing tests ───────────────


def test_build_recommendation_rationale_includes_shape() -> None:
    """Rationale always includes a sentence about the product shape."""
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="cli tool",
            needs=set(),
            regulated=False,
            attach_userjourney=False,
        )
    assert any("cli tool" in r for r in rec.rationale)


def test_build_recommendation_rationale_mentions_domains_when_matched() -> None:
    """Rationale includes domain names when matched_domains is non-empty."""
    rec = recommend.build_recommendation(
        product_shape="web app",
        needs=set(),
        regulated=False,
        attach_userjourney=False,
    )
    if rec.matched_domains:
        assert any("Most relevant KB domains" in r for r in rec.rationale)


def test_build_recommendation_rationale_mentions_rules_when_applied() -> None:
    """Rationale includes rule titles when rule_evidence is non-empty."""
    rec = recommend.build_recommendation(
        product_shape="web app",
        needs=set(),
        regulated=False,
        attach_userjourney=False,
    )
    if rec.rule_evidence:
        assert any("KB decision rules applied" in r for r in rec.rationale)


def test_build_recommendation_next_commands_starts_with_create() -> None:
    """First next_command is always the create command."""
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="api service",
            needs=set(),
            regulated=False,
            attach_userjourney=False,
        )
    assert rec.next_commands[0].startswith("programstart create")


def test_build_recommendation_next_commands_includes_attach_for_web_app() -> None:
    """Web app with default attach_userjourney=None includes attach command."""
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="web app",
            needs=set(),
            regulated=False,
            attach_userjourney=None,
        )
    assert rec.attach_userjourney is True
    assert any("attach" in cmd for cmd in rec.next_commands)


def test_build_recommendation_next_commands_excludes_attach_when_forced_off() -> None:
    """attach_userjourney=False suppresses the attach command."""
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="web app",
            needs=set(),
            regulated=False,
            attach_userjourney=False,
        )
    assert rec.attach_userjourney is False
    assert not any("attach userjourney" in cmd.lower() for cmd in rec.next_commands)


def test_build_recommendation_unrecognized_needs_warning() -> None:
    """Unrecognized needs appear in rationale warning."""
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="api service",
            needs={"rag", "xyzzy_nonexistent_need"},
            regulated=False,
            attach_userjourney=False,
        )
    assert any("Unrecognized capability needs" in r and "xyzzy_nonexistent_need" in r for r in rec.rationale)


def test_build_recommendation_companion_surface_for_api_with_dashboard() -> None:
    """API service + dashboard need adds companion surface advisory."""
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="api service",
            needs={"dashboard"},
            regulated=False,
            attach_userjourney=False,
        )
    assert "admin dashboard" in rec.suggested_companion_surfaces


# ── Unit-level exact-value tests for high-survivor-rate helpers ─────────────


# ── comparison_bonus unit tests ────────────────────────────────────────────


def test_comparison_bonus_no_comparisons_returns_zero() -> None:
    bonus, reasons, alternatives = recommend.comparison_bonus(
        item_name="Next.js",
        selected_stacks={"fastapi"},
        needs={"ssr"},
        comparisons=[],
    )
    assert bonus == 0
    assert reasons == []
    assert alternatives == []


def test_comparison_bonus_no_match_returns_zero() -> None:
    comp = {
        "name": "X vs Y",
        "related_items": ["X", "Y"],
        "compared_versions": [],
        "decision": "X wins",
        "summary": "X is better",
    }
    bonus, reasons, alternatives = recommend.comparison_bonus(
        item_name="Next.js",
        selected_stacks=set(),
        needs=set(),
        comparisons=[comp],
    )
    assert bonus == 0
    assert reasons == []
    assert alternatives == []


def test_comparison_bonus_related_item_match_with_stack_overlap() -> None:
    comp = {
        "name": "FastAPI vs Flask",
        "related_items": ["FastAPI", "Flask"],
        "compared_versions": [],
        "decision": "FastAPI recommended for APIs",
        "summary": "Good API framework",
    }
    bonus, reasons, alternatives = recommend.comparison_bonus(
        item_name="FastAPI",
        selected_stacks={"Flask"},
        needs=set(),
        comparisons=[comp],
    )
    # "fastapi" in normalize_text("FastAPI recommended for APIs") → True → bonus += 3
    assert bonus == 3
    assert len(reasons) == 1
    assert reasons[0] == "FastAPI recommended for APIs"
    assert len(alternatives) == 1
    assert alternatives[0]["item"] == "FastAPI vs Flask"
    assert alternatives[0]["category"] == "comparison"
    assert alternatives[0]["rationale"] == "FastAPI recommended for APIs"


def test_comparison_bonus_summary_fallback_when_item_not_in_decision() -> None:
    comp = {
        "name": "Nuxt vs Remix",
        "related_items": ["Nuxt", "Remix"],
        "compared_versions": [],
        "decision": "Remix recommended",
        "summary": "Nuxt SSR is solid",
    }
    bonus, reasons, alternatives = recommend.comparison_bonus(
        item_name="Nuxt",
        selected_stacks={"Remix"},
        needs=set(),
        comparisons=[comp],
    )
    # "nuxt" not in normalize_text("Remix recommended") → else branch → bonus += 1
    assert bonus == 1
    assert reasons == ["Nuxt SSR is solid"]
    assert alternatives[0]["rationale"] == "Remix recommended"


def test_comparison_bonus_needs_overlap_triggers_match() -> None:
    comp = {
        "name": "A vs B",
        "related_items": ["React", "Vue"],
        "compared_versions": [],
        "decision": "React for SPA",
        "summary": "Both good",
    }
    bonus, reasons, alternatives = recommend.comparison_bonus(
        item_name="React",
        selected_stacks=set(),
        needs={"react"},
        comparisons=[comp],
    )
    assert bonus == 3
    assert len(alternatives) == 1


def test_comparison_bonus_compared_versions_match() -> None:
    comp = {
        "name": "FastAPI 0.100 vs 0.111",
        "related_items": [],
        "compared_versions": ["FastAPI"],
        "decision": "Upgrade to FastAPI 0.111",
        "summary": "Minor improvements",
    }
    bonus, reasons, alternatives = recommend.comparison_bonus(
        item_name="FastAPI",
        selected_stacks=set(),
        needs={"fastapi"},
        comparisons=[comp],
    )
    assert bonus == 3
    assert "Upgrade to FastAPI 0.111" in reasons


def test_comparison_bonus_multiple_comparisons_accumulate() -> None:
    comps = [
        {
            "name": "A vs B",
            "related_items": ["FastAPI", "Flask"],
            "compared_versions": [],
            "decision": "FastAPI wins",
            "summary": "FastAPI is faster",
        },
        {
            "name": "C vs D",
            "related_items": ["FastAPI", "Django"],
            "compared_versions": [],
            "decision": "Use FastAPI for APIs",
            "summary": "Django REST alt",
        },
    ]
    bonus, reasons, alternatives = recommend.comparison_bonus(
        item_name="FastAPI",
        selected_stacks={"Flask", "Django"},
        needs=set(),
        comparisons=comps,
    )
    # Both match: 3 + 3 = 6
    assert bonus == 6
    assert len(reasons) == 2
    assert len(alternatives) == 2


def test_comparison_bonus_rationale_uses_decision_when_present() -> None:
    bonus, reasons, alternatives = recommend.comparison_bonus(
        item_name="X",
        selected_stacks={"X"},
        needs=set(),
        comparisons=[{"related_items": ["X"], "compared_versions": [], "name": "comp1", "decision": "", "summary": "fallback"}],
    )
    # decision is empty → "x" not in normalize_text("") → else branch, bonus += 1
    assert bonus == 1
    assert alternatives[0]["rationale"] == "fallback"


def test_comparison_bonus_empty_decision_falls_through_to_summary() -> None:
    comp = {
        "name": "comp",
        "related_items": ["X"],
        "compared_versions": [],
        "decision": "",
        "summary": "summary only",
    }
    bonus, reasons, alternatives = recommend.comparison_bonus(
        item_name="X",
        selected_stacks={"X"},
        needs=set(),
        comparisons=[comp],
    )
    assert bonus == 1
    assert reasons == ["summary only"]
    assert alternatives[0]["rationale"] == "summary only"


# ── actionability_follow_up_commands unit tests ────────────────────────────


def test_actionability_follow_up_commands_empty_returns_empty() -> None:
    assert recommend.actionability_follow_up_commands([]) == []


def test_actionability_follow_up_commands_advice_only() -> None:
    cmds = recommend.actionability_follow_up_commands([{"actionability": "advice-only"}])
    assert len(cmds) == 1
    assert "create-plan.md" in cmds[0]


def test_actionability_follow_up_commands_automation_supported() -> None:
    cmds = recommend.actionability_follow_up_commands([{"actionability": "automation-supported"}])
    assert len(cmds) == 1
    assert "provisioning-plan.md" in cmds[0]


def test_actionability_follow_up_commands_manual_setup() -> None:
    cmds = recommend.actionability_follow_up_commands([{"actionability": "manual-setup"}])
    assert len(cmds) == 1
    assert "setup-surface.md" in cmds[0]


def test_actionability_follow_up_commands_all_three() -> None:
    items = [
        {"actionability": "advice-only"},
        {"actionability": "automation-supported"},
        {"actionability": "manual-setup"},
    ]
    cmds = recommend.actionability_follow_up_commands(items)
    assert len(cmds) == 3
    assert "create-plan.md" in cmds[0]
    assert "provisioning-plan.md" in cmds[1]
    assert "setup-surface.md" in cmds[2]


def test_actionability_follow_up_commands_unknown_category_ignored() -> None:
    cmds = recommend.actionability_follow_up_commands([{"actionability": "unknown-type"}])
    assert cmds == []


def test_actionability_follow_up_commands_missing_key_ignored() -> None:
    cmds = recommend.actionability_follow_up_commands([{"name": "SomeService"}])
    assert cmds == []


def test_actionability_follow_up_commands_duplicate_category() -> None:
    items = [
        {"actionability": "advice-only"},
        {"actionability": "advice-only"},
    ]
    cmds = recommend.actionability_follow_up_commands(items)
    # advice-only matched by `any()`, so only one command
    assert len(cmds) == 1


# ── shape_profile exact-value unit tests ───────────────────────────────────


def test_shape_profile_cli_tool_exact() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("cli tool")
    assert archetype == "Type-safe CLI planning toolkit"
    assert baselines == ["Pydantic", "pytest", "Hypothesis", "Ruff", "uv"]
    assert intents == {"cli", "validation", "testing", "automation", "developer tooling"}
    assert domains == ["Developer experience, quality, and supply chain"]


def test_shape_profile_api_service_exact() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("api service")
    assert archetype == "Typed API and automation platform"
    assert baselines == ["FastAPI", "PostgreSQL", "Pydantic", "OpenTelemetry", "pytest"]
    assert "api contracts" in intents
    assert "async io" in intents
    assert len(domains) == 2


def test_shape_profile_web_app_exact() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("web app")
    assert archetype == "Interactive product workflow"
    assert baselines == ["Next.js", "PostgreSQL", "Playwright", "Pydantic"]
    assert "ssr" in intents
    assert "authentication" in intents
    assert "Web and frontend product delivery" in domains


def test_shape_profile_mobile_app_exact() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("mobile app")
    assert archetype == "Mobile product workflow"
    assert baselines == ["React Native", "Expo", "Firebase", "Pydantic"]
    assert "ios" in intents
    assert "android" in intents
    assert "push notifications" in intents
    assert "in app purchases" in intents


def test_shape_profile_data_pipeline_exact() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("data pipeline")
    assert archetype == "Data and automation workflow"
    assert baselines == ["FastAPI", "DuckDB", "Polars", "Pydantic"]
    assert "etl" in intents
    assert "columnar processing" in intents
    assert "Data engineering and analytics" in domains


def test_shape_profile_unknown_exact() -> None:
    archetype, baselines, intents, domains = recommend.shape_profile("something weird")
    assert archetype == "Balanced production workflow"
    assert baselines == ["Pydantic", "pytest", "Ruff", "uv"]
    assert intents == {"validation", "testing", "automation"}
    assert domains == ["Developer experience, quality, and supply chain"]


# ── infer_domain_names exact-value unit tests ──────────────────────────────


def _domain_kb() -> dict[str, Any]:
    """KB with all coverage domains for domain inference tests."""
    return {
        "coverage_domains": [
            {"name": "Developer experience, quality, and supply chain"},
            {"name": "Web and frontend product delivery"},
            {"name": "Cloud, infrastructure, and platform operations"},
            {"name": "API, workflow, and backend platforms"},
            {"name": "AI, retrieval, and agent systems"},
            {"name": "Data engineering and analytics"},
            {"name": "Identity, security, and regulated delivery"},
            {"name": "Realtime collaboration, messaging, and eventing"},
            {"name": "Commerce, communication, and product integrations"},
            {"name": "Mobile and cross-platform apps"},
            {"name": "Desktop, local-first, and offline-capable software"},
        ],
    }


def test_infer_domain_names_cli_no_needs() -> None:
    domains = recommend.infer_domain_names("cli tool", set(), False, _domain_kb())
    assert domains == ["Developer experience, quality, and supply chain"]


def test_infer_domain_names_web_app_no_needs() -> None:
    domains = recommend.infer_domain_names("web app", set(), False, _domain_kb())
    assert "Web and frontend product delivery" in domains
    assert "Cloud, infrastructure, and platform operations" in domains


def test_infer_domain_names_ai_need_adds_ai_domain() -> None:
    domains = recommend.infer_domain_names("cli tool", {"ai"}, False, _domain_kb())
    assert "AI, retrieval, and agent systems" in domains
    assert "Developer experience, quality, and supply chain" in domains


def test_infer_domain_names_realtime_need() -> None:
    domains = recommend.infer_domain_names("api service", {"realtime"}, False, _domain_kb())
    assert "Realtime collaboration, messaging, and eventing" in domains


def test_infer_domain_names_payments_need() -> None:
    domains = recommend.infer_domain_names("web app", {"payments"}, False, _domain_kb())
    assert "Commerce, communication, and product integrations" in domains


def test_infer_domain_names_regulated_adds_identity_domain() -> None:
    domains = recommend.infer_domain_names("cli tool", set(), True, _domain_kb())
    assert "Identity, security, and regulated delivery" in domains


def test_infer_domain_names_regulated_with_auth_need() -> None:
    domains = recommend.infer_domain_names("api service", {"authentication"}, True, _domain_kb())
    assert "Identity, security, and regulated delivery" in domains


def test_infer_domain_names_desktop_need() -> None:
    domains = recommend.infer_domain_names("cli tool", {"desktop"}, False, _domain_kb())
    assert "Desktop, local-first, and offline-capable software" in domains


def test_infer_domain_names_observability_need() -> None:
    domains = recommend.infer_domain_names("api service", {"observability"}, False, _domain_kb())
    assert "Cloud, infrastructure, and platform operations" in domains


def test_infer_domain_names_mobile_need() -> None:
    domains = recommend.infer_domain_names("cli tool", {"mobile"}, False, _domain_kb())
    assert "Mobile and cross-platform apps" in domains


def test_infer_domain_names_multiple_needs() -> None:
    domains = recommend.infer_domain_names("web app", {"payments", "ai", "realtime"}, False, _domain_kb())
    assert "Commerce, communication, and product integrations" in domains
    assert "AI, retrieval, and agent systems" in domains
    assert "Realtime collaboration, messaging, and eventing" in domains


def test_infer_domain_names_data_pipeline_base_domains() -> None:
    domains = recommend.infer_domain_names("data pipeline", set(), False, _domain_kb())
    assert "Data engineering and analytics" in domains
    assert "API, workflow, and backend platforms" in domains


def test_infer_domain_names_no_duplicate_domains() -> None:
    # observability maps to Cloud domain; api service base already has Cloud domain
    domains = recommend.infer_domain_names("api service", {"observability"}, False, _domain_kb())
    cloud_count = domains.count("Cloud, infrastructure, and platform operations")
    assert cloud_count == 1


def test_infer_domain_names_unknown_need_ignored() -> None:
    domains = recommend.infer_domain_names("cli tool", {"completely_unknown_xyzzy"}, False, _domain_kb())
    assert domains == ["Developer experience, quality, and supply chain"]


def test_infer_domain_names_missing_kb_domain_skipped() -> None:
    # KB missing the AI domain → even with 'ai' need, it won't appear
    kb = {"coverage_domains": [{"name": "Developer experience, quality, and supply chain"}]}
    domains = recommend.infer_domain_names("cli tool", {"ai"}, False, kb)
    assert "AI, retrieval, and agent systems" not in domains


# ── build_generated_prompt exact-value unit tests ──────────────────────────


def test_build_generated_prompt_basic_structure() -> None:
    prompt = recommend.build_generated_prompt(
        product_shape="cli tool",
        variant="standard",
        attach_userjourney=False,
        kickoff_files=["KICKOFF.md"],
        rationale=["reason1"],
        prompt_principles=["principle1"],
        prompt_patterns=["pattern1"],
        prompt_anti_patterns=["anti1"],
        coverage_warnings=[],
        service_names=["Supabase"],
        cli_tool_names=["uv"],
        api_names=["Stripe"],
    )
    assert "## Task" in prompt
    assert "## Project Context" in prompt
    assert "Product shape: cli tool" in prompt
    assert "Variant: standard" in prompt
    assert "USERJOURNEY attached: no" in prompt
    assert "KICKOFF.md" in prompt
    assert "## Infrastructure" in prompt
    assert "Supabase" in prompt
    assert "uv" in prompt
    assert "Stripe" in prompt
    assert "## Decision Rationale" in prompt
    assert "reason1" in prompt
    assert "## Prompt Principles" in prompt
    assert "principle1" in prompt
    assert "## Prompt Patterns" in prompt
    assert "pattern1" in prompt
    assert "## Anti-Patterns" in prompt
    assert "anti1" in prompt
    assert "## Coverage Warnings" in prompt
    assert "none" in prompt
    assert "## Constraints" in prompt


def test_build_generated_prompt_userjourney_attached() -> None:
    prompt = recommend.build_generated_prompt(
        product_shape="web app",
        variant="product",
        attach_userjourney=True,
        kickoff_files=[],
        rationale=[],
        prompt_principles=[],
        prompt_patterns=[],
        prompt_anti_patterns=[],
        coverage_warnings=[],
        service_names=[],
        cli_tool_names=[],
        api_names=[],
    )
    assert "USERJOURNEY attached: yes" in prompt
    assert "registry kickoff files" in prompt
    assert "none inferred" in prompt


def test_build_generated_prompt_coverage_warnings() -> None:
    warnings = [
        {"domain": "Cloud ops", "gaps": "no observability stack"},
        {"domain": "Identity", "gaps": "no auth provider"},
    ]
    prompt = recommend.build_generated_prompt(
        product_shape="api service",
        variant="product",
        attach_userjourney=False,
        kickoff_files=["F1.md"],
        rationale=["r"],
        prompt_principles=["p"],
        prompt_patterns=["pat"],
        prompt_anti_patterns=["ap"],
        coverage_warnings=warnings,
        service_names=[],
        cli_tool_names=[],
        api_names=[],
    )
    assert "Cloud ops: no observability stack" in prompt
    assert "Identity: no auth provider" in prompt


def test_build_generated_prompt_default_anti_patterns() -> None:
    prompt = recommend.build_generated_prompt(
        product_shape="cli tool",
        variant="standard",
        attach_userjourney=False,
        kickoff_files=[],
        rationale=[],
        prompt_principles=[],
        prompt_patterns=[],
        prompt_anti_patterns=[],
        coverage_warnings=[],
        service_names=[],
        cli_tool_names=[],
        api_names=[],
    )
    assert "Do not invent unsupported files" in prompt


def test_build_generated_prompt_rationale_capped_at_6() -> None:
    rationale = [f"reason{i}" for i in range(10)]
    prompt = recommend.build_generated_prompt(
        product_shape="cli tool",
        variant="standard",
        attach_userjourney=False,
        kickoff_files=[],
        rationale=rationale,
        prompt_principles=[],
        prompt_patterns=[],
        prompt_anti_patterns=[],
        coverage_warnings=[],
        service_names=[],
        cli_tool_names=[],
        api_names=[],
    )
    assert "reason5" in prompt
    assert "reason6" not in prompt


def test_build_generated_prompt_principles_capped_at_8() -> None:
    principles = [f"principle{i}" for i in range(12)]
    prompt = recommend.build_generated_prompt(
        product_shape="cli tool",
        variant="standard",
        attach_userjourney=False,
        kickoff_files=[],
        rationale=[],
        prompt_principles=principles,
        prompt_patterns=[],
        prompt_anti_patterns=[],
        coverage_warnings=[],
        service_names=[],
        cli_tool_names=[],
        api_names=[],
    )
    assert "principle7" in prompt
    assert "principle8" not in prompt


def test_build_generated_prompt_coverage_warnings_capped_at_4() -> None:
    warnings = [{"domain": f"D{i}", "gaps": f"gap{i}"} for i in range(6)]
    prompt = recommend.build_generated_prompt(
        product_shape="cli tool",
        variant="standard",
        attach_userjourney=False,
        kickoff_files=[],
        rationale=[],
        prompt_principles=[],
        prompt_patterns=[],
        prompt_anti_patterns=[],
        coverage_warnings=warnings,
        service_names=[],
        cli_tool_names=[],
        api_names=[],
    )
    assert "D3: gap3" in prompt
    assert "D4: gap4" not in prompt


def test_build_generated_prompt_reasoning_steps() -> None:
    prompt = recommend.build_generated_prompt(
        product_shape="cli tool",
        variant="standard",
        attach_userjourney=False,
        kickoff_files=[],
        rationale=[],
        prompt_principles=[],
        prompt_patterns=[],
        prompt_anti_patterns=[],
        coverage_warnings=[],
        service_names=[],
        cli_tool_names=[],
        api_names=[],
    )
    assert "1. Identify which authority files" in prompt
    assert "5. Produce the plan" in prompt


def test_build_recommendation_companion_surface_coverage_warning() -> None:
    """Companion surface advisory generates a coverage warning."""
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="api service",
            needs={"dashboard"},
            regulated=False,
            attach_userjourney=False,
        )
    assert any(w.get("domain") == "Companion UI" and w.get("status") == "advisory" for w in rec.coverage_warnings)


def test_build_recommendation_no_companion_surface_for_web_app() -> None:
    """Web app does not get companion surface advisory (it IS a UI)."""
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="web app",
            needs={"dashboard"},
            regulated=False,
            attach_userjourney=False,
        )
    assert "admin dashboard" not in rec.suggested_companion_surfaces


def test_build_recommendation_frontend_coverage_advisory_for_api() -> None:
    """API service with no frontend domain gets frontend coverage advisory."""
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="api service",
            needs=set(),
            regulated=False,
            attach_userjourney=False,
        )
    if "Web and frontend product delivery" not in rec.matched_domains:
        assert any(w.get("domain") == "Frontend coverage" and w.get("status") == "advisory" for w in rec.coverage_warnings)


def test_build_recommendation_combined_alternatives_deduplication() -> None:
    """Combined alternatives are deduplicated by (item, category) key."""
    rec = recommend.build_recommendation(
        product_shape="web app",
        needs={"rag"},
        regulated=False,
        attach_userjourney=False,
    )
    keys = [(a.get("item"), a.get("category")) for a in rec.alternatives]
    assert len(keys) == len(set(keys)), f"Duplicate alternatives found: {keys}"


def test_build_recommendation_generated_prompt_non_empty() -> None:
    """Generated prompt is always a non-empty string."""
    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="cli tool",
            needs=set(),
            regulated=False,
            attach_userjourney=False,
        )
    assert isinstance(rec.generated_prompt, str)
    assert len(rec.generated_prompt) > 0


def test_build_recommendation_prompt_generated_at_is_iso() -> None:
    """prompt_generated_at is a valid ISO 8601 timestamp."""
    from datetime import datetime

    with (
        patch.object(recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(recommend, "load_knowledge_base", return_value=_minimal_kb()),
    ):
        rec = recommend.build_recommendation(
            product_shape="cli tool",
            needs=set(),
            regulated=False,
            attach_userjourney=False,
        )
    # Should parse without error
    datetime.fromisoformat(rec.prompt_generated_at)


def test_build_recommendation_coverage_warnings_mentions_review() -> None:
    """When coverage_warnings exist, next_commands includes review guidance."""
    rec = recommend.build_recommendation(
        product_shape="web app",
        needs=set(),
        regulated=False,
        attach_userjourney=False,
    )
    if rec.coverage_warnings:
        assert any("coverage warnings" in r.lower() for r in rec.rationale)


def test_build_recommendation_services_and_clis_populated() -> None:
    """Real KB run should populate at least some service/cli/api names."""
    rec = recommend.build_recommendation(
        product_shape="web app",
        needs={"authentication"},
        regulated=False,
        attach_userjourney=False,
    )
    # At least one of these should be non-empty for a web app with auth need
    has_some = rec.service_names or rec.cli_tool_names or rec.api_names
    assert has_some, "Expected at least one of service/cli/api names for web app with auth"


# ── main: assertion-dense mutation-killing tests ───────────────────────────────


def test_main_list_shapes_text_format(capsys) -> None:
    """--list-shapes prints 'Known product shapes:' header and indented entries."""
    rc = recommend.main(["--list-shapes"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Known product shapes:" in out
    assert "cli tool" in out
    assert "api service" in out
    assert "web app" in out
    assert "mobile app" in out
    assert "data pipeline" in out
    # Each line should show archetype description
    for line in out.strip().split("\n")[1:]:
        assert line.startswith("  "), f"Expected indented line: {line!r}"


def test_main_list_shapes_json_format(capsys) -> None:
    """--list-shapes --json emits a JSON array with shape/archetype keys."""
    import json as json_mod

    rc = recommend.main(["--list-shapes", "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json_mod.loads(out)
    assert isinstance(data, list)
    assert len(data) == 5  # 5 known shapes
    for entry in data:
        assert "shape" in entry
        assert "archetype" in entry


def test_main_re_evaluate_text_format(capsys, tmp_path) -> None:
    """--re-evaluate prints structured text report."""
    kickoff_dir = tmp_path / "PROGRAMBUILD"
    kickoff_dir.mkdir()
    (kickoff_dir / "PROGRAMBUILD_KICKOFF_PACKET.md").write_text(
        "```text\nPROJECT_NAME: TestApp\nPRODUCT_SHAPE: web app\n```",
        encoding="utf-8",
    )
    rc = recommend.main(["--re-evaluate", str(tmp_path)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "PROGRAMSTART Re-evaluation Report" in out
    assert "project:" in out
    assert "product shape:" in out
    assert "inferred needs:" in out
    assert "KB version:" in out
    assert "re-evaluated at:" in out
    assert "recommended variant:" in out
    assert "recommended stacks:" in out
    assert "confidence:" in out


def test_main_re_evaluate_json_format(capsys, tmp_path) -> None:
    """--re-evaluate --json emits a JSON object with expected keys."""
    import json as json_mod

    kickoff_dir = tmp_path / "PROGRAMBUILD"
    kickoff_dir.mkdir()
    (kickoff_dir / "PROGRAMBUILD_KICKOFF_PACKET.md").write_text(
        "```text\nPROJECT_NAME: TestApp\nPRODUCT_SHAPE: api service\n```",
        encoding="utf-8",
    )
    rc = recommend.main(["--re-evaluate", str(tmp_path), "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json_mod.loads(out)
    assert "project_dir" in data
    assert "product_shape" in data
    assert data["product_shape"] == "api service"
    assert "current_recommendation" in data
    assert "deltas" in data


def test_main_standard_text_output_sections(capsys) -> None:
    """Standard text output includes all key sections."""
    rc = recommend.main(["--product-shape", "web app"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "PROGRAMSTART Recommendation" in out
    assert "product shape:" in out
    assert "variant:" in out
    assert "attach USERJOURNEY:" in out
    assert "archetype:" in out
    assert "confidence:" in out
    assert "suggested stacks:" in out
    assert "matched domains:" in out
    assert "rationale:" in out
    assert "kickoff files:" in out
    assert "next commands:" in out


def test_main_standard_json_output_keys(capsys) -> None:
    """Standard --json output includes all ProjectRecommendation fields."""
    import json as json_mod

    rc = recommend.main(["--product-shape", "cli tool", "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json_mod.loads(out)
    expected_keys = {
        "product_shape",
        "variant",
        "attach_userjourney",
        "archetype",
        "stack_names",
        "service_names",
        "cli_tool_names",
        "api_names",
        "rationale",
        "kickoff_files",
        "next_commands",
        "matched_domains",
        "coverage_warnings",
        "stack_evidence",
        "rule_evidence",
        "confidence",
        "generated_prompt",
        "prompt_generated_at",
    }
    assert expected_keys <= set(data.keys()), f"Missing keys: {expected_keys - set(data.keys())}"


def test_main_standard_text_shows_stacks_or_none(capsys) -> None:
    """Text output shows stack names or 'none matched current KB'."""
    rc = recommend.main(["--product-shape", "web app"])
    assert rc == 0
    out = capsys.readouterr().out
    # Either shows stack names or the fallback message
    assert "suggested stacks:" in out
    stacks_line = [line for line in out.split("\n") if "suggested stacks:" in line][0]
    assert stacks_line.strip().startswith("- suggested stacks:")


def test_main_text_mode_with_needs(capsys) -> None:
    """Text mode with --need flags reflects them in output."""
    rc = recommend.main(["--product-shape", "api service", "--need", "rag", "--need", "authentication"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "api service" in out


def test_main_regulated_flag_changes_variant(capsys) -> None:
    """--regulated flag selects enterprise variant."""
    import json as json_mod

    rc = recommend.main(["--product-shape", "api service", "--regulated", "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json_mod.loads(out)
    assert data["variant"] == "enterprise"


def test_main_attach_userjourney_flag(capsys) -> None:
    """--attach-userjourney forces attach=True in output."""
    import json as json_mod

    rc = recommend.main(["--product-shape", "cli tool", "--attach-userjourney", "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json_mod.loads(out)
    assert data["attach_userjourney"] is True


def test_main_no_attach_userjourney_flag(capsys) -> None:
    """--no-attach-userjourney forces attach=False in output."""
    import json as json_mod

    rc = recommend.main(["--product-shape", "web app", "--no-attach-userjourney", "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json_mod.loads(out)
    assert data["attach_userjourney"] is False


# ── print_recommendation: exact output assertion ──────────────────────────────


def test_print_recommendation_exact_header_lines(capsys) -> None:
    """print_recommendation emits exact header lines in order."""
    rec = ProjectRecommendation(
        product_shape="cli tool",
        variant="lite",
        attach_userjourney=False,
        archetype="Type-safe CLI",
        stack_names=["uv", "Ruff"],
        service_names=[],
        cli_tool_names=[],
        api_names=[],
        rationale=["Chosen for simplicity"],
        kickoff_files=["K.md"],
        next_commands=["programstart next"],
    )
    recommend.print_recommendation(rec)
    out = capsys.readouterr().out
    lines = out.strip().split("\n")
    assert lines[0] == "PROGRAMSTART Recommendation"
    assert lines[1] == "- product shape: cli tool"
    assert lines[2] == "- variant: lite"
    assert lines[3] == "- attach USERJOURNEY: no"
    assert lines[4] == "- archetype: Type-safe CLI"
    assert lines[5] == "- confidence: medium"
    assert lines[6] == "- suggested stacks: uv, Ruff"


def test_print_recommendation_no_stacks_shows_fallback(capsys) -> None:
    """When stack_names is empty, shows 'none matched current KB'."""
    rec = ProjectRecommendation(
        product_shape="other",
        variant="lite",
        attach_userjourney=False,
        archetype="Generic",
        stack_names=[],
        service_names=[],
        cli_tool_names=[],
        api_names=[],
        rationale=["Test"],
        kickoff_files=["K.md"],
        next_commands=["programstart next"],
    )
    recommend.print_recommendation(rec)
    out = capsys.readouterr().out
    assert "none matched current KB" in out


def test_print_recommendation_no_services_shows_fallback(capsys) -> None:
    """When service_names is empty, shows 'none inferred'."""
    rec = ProjectRecommendation(
        product_shape="other",
        variant="lite",
        attach_userjourney=False,
        archetype="Generic",
        stack_names=["X"],
        service_names=[],
        cli_tool_names=[],
        api_names=[],
        rationale=["Test"],
        kickoff_files=["K.md"],
        next_commands=["programstart next"],
    )
    recommend.print_recommendation(rec)
    out = capsys.readouterr().out
    assert "suggested services: none inferred" in out
    assert "recommended clis: none inferred" in out
    assert "saved api templates: none inferred" in out


def test_print_recommendation_matched_domains_none_shows_fallback(capsys) -> None:
    """When matched_domains is empty, shows 'none matched'."""
    rec = ProjectRecommendation(
        product_shape="other",
        variant="lite",
        attach_userjourney=False,
        archetype="Generic",
        stack_names=[],
        service_names=[],
        cli_tool_names=[],
        api_names=[],
        rationale=["Test"],
        kickoff_files=[],
        next_commands=[],
        matched_domains=[],
    )
    recommend.print_recommendation(rec)
    out = capsys.readouterr().out
    assert "matched domains: none matched" in out
