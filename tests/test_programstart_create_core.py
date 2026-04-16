from __future__ import annotations

import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_create_core as create_core
from scripts.programstart_recommend import ProjectRecommendation


def _make_recommendation() -> ProjectRecommendation:
    return ProjectRecommendation(
        product_shape="web app",
        variant="product",
        attach_userjourney=False,
        archetype="Test archetype",
        service_names=["Supabase"],
    )


def test_default_github_repo_name_slugifies_project_name() -> None:
    assert create_core.default_github_repo_name("My New App") == "my-new-app"


def test_merge_service_names_deduplicates_explicit_and_inferred_entries() -> None:
    recommendation = _make_recommendation()

    result = create_core.merge_service_names(recommendation, ["supabase", "Vercel"])

    assert result == ["Supabase", "Vercel"]


def test_annotate_provisioned_service_marks_partial_when_manual_secrets_remain() -> None:
    result = create_core.annotate_provisioned_service(
        {
            "name": "Supabase",
            "provider": "Supabase",
            "status": "provisioning_started",
            "manual_secrets": ["SUPABASE_ANON_KEY", "SUPABASE_SERVICE_ROLE_KEY"],
        }
    )

    assert result["automation_level"] == "partial"
    assert result["completion_status"] == "action_required"
    assert "SUPABASE_ANON_KEY" in cast(list[str], result["manual_secret_targets"])
    assert result["manual_steps"]


def test_summarize_provisioning_results_rolls_up_pending_and_completed_services() -> None:
    result = create_core.summarize_provisioning_results(
        [
            {
                "name": "Vercel",
                "provider": "Vercel",
                "status": "created",
            },
            {
                "name": "Neon",
                "provider": "Neon",
                "status": "provisioning_started",
                "manual_secrets": ["DATABASE_URL", "DIRECT_DATABASE_URL"],
            },
        ]
    )

    assert result["status"] == "action_required"
    assert result["completed_services"] == ["Vercel"]
    assert result["pending_services"] == ["Neon"]
    assert result["unresolved_env_keys"] == ["DATABASE_URL", "DIRECT_DATABASE_URL"]
