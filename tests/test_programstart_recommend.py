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
