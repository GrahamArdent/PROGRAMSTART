from __future__ import annotations

import sys
from pathlib import Path
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
            {"title": "Use JWT", "match_product_shapes": ["web app"], "match_needs": [], "match_domains": [],
             "layer": "auth", "preferred_items": ["JWT"]},
        ],
    }
    rules = recommend.matching_decision_rules(
        product_shape="web app", needs=set(), matched_domains=[], knowledge_base=kb,
    )
    assert len(rules) == 1
    assert rules[0]["title"] == "Use JWT"


def test_matching_decision_rules_no_match() -> None:
    kb = {
        "decision_rules": [
            {"title": "Use JWT", "match_product_shapes": ["mobile app"], "match_needs": [], "match_domains": [],
             "layer": "auth", "preferred_items": ["JWT"]},
        ],
    }
    rules = recommend.matching_decision_rules(
        product_shape="cli tool", needs=set(), matched_domains=[], knowledge_base=kb,
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
    rules = [{"title": "Use FastAPI", "match_product_shapes": ["api service"], "match_needs": [], "match_domains": [],
              "target_layers": [], "prefer_items": ["FastAPI"], "avoid_items": []}]
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
        actionability_summary=[{"name": "Vercel", "category": "service", "actionability": "automation-supported", "reason": "API available"}],
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
    ns = type("NS", (), {"product_shape": "cli tool", "need": ["rag"]})()
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
        knowledge_base={
            "provisioning_services": [
                {"name": "other_service", "automation_supported": False}
            ]
        },
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
        any("integration pattern" in str(r).lower() for r in item.get("reasons", []))
        for item in rec.stack_evidence
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
        any("integration pattern" in str(r).lower() for r in item.get("reasons", []))
        for item in rec.stack_evidence
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
