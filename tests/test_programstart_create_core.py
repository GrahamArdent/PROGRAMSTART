from __future__ import annotations

import sys
from pathlib import Path
from typing import cast

import pytest

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


# ---------------------------------------------------------------------------
# Phase C: boundary consolidation — create_core.py → ≥93%
# ---------------------------------------------------------------------------


def test_provider_manual_steps_vercel_created_returns_empty() -> None:
    """Vercel with status=created returns no manual steps (line 213)."""
    result = create_core.provider_manual_steps({"provider": "Vercel", "status": "created"})
    assert result == []


def test_provider_manual_steps_manual_only_returns_reason() -> None:
    """manual_only status returns reason text (line 215)."""
    result = create_core.provider_manual_steps({"provider": "Custom", "status": "manual_only", "reason": "Not automated yet."})
    assert result == ["Not automated yet."]


def test_provider_manual_steps_manual_only_default_reason() -> None:
    """manual_only without reason gets default message."""
    result = create_core.provider_manual_steps({"provider": "Custom", "status": "manual_only"})
    assert "Custom" in result[0]


def test_provider_manual_steps_with_manual_secrets() -> None:
    """manual_secrets present returns store instructions (line 213-214)."""
    result = create_core.provider_manual_steps({"provider": "Vercel", "status": "partial", "manual_secrets": ["TOKEN_A"]})
    assert len(result) == 1
    assert "TOKEN_A" in result[0]


def test_provider_manual_steps_no_match_returns_empty() -> None:
    """No matching condition returns empty list (line 215)."""
    result = create_core.provider_manual_steps({"provider": "Vercel", "status": "partial"})
    assert result == []


def test_http_json_request_returns_empty_dict_on_blank_body(monkeypatch) -> None:
    """Empty response body returns {} (line 283)."""
    from urllib import request as urllib_request

    class FakeResponse:
        def read(self) -> bytes:
            return b"   "

        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *args: object) -> None:
            pass

    monkeypatch.setattr(urllib_request, "urlopen", lambda req, **kw: FakeResponse())
    result = create_core.http_json_request(method="GET", url="https://example.com/test", headers={}, payload=None)
    assert result == {}


def test_http_json_request_raises_on_non_dict_response(monkeypatch) -> None:
    """Non-dict JSON response raises RuntimeError (line 287)."""
    from urllib import request as urllib_request

    class FakeResponse:
        def read(self) -> bytes:
            return b'["a", "b"]'

        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *args: object) -> None:
            pass

    monkeypatch.setattr(urllib_request, "urlopen", lambda req, **kw: FakeResponse())
    with pytest.raises(RuntimeError, match="Expected JSON object"):
        create_core.http_json_request(method="GET", url="https://example.com/test", headers={}, payload=None)


def test_provision_services_unknown_returns_manual_only() -> None:
    """Unknown service name returns manual_only result (line 474)."""
    results = create_core.provision_requested_services(
        project_name="test",
        services=["UnknownDB"],
        supabase_org_id="",
        supabase_region="",
        supabase_plan="free",
        vercel_team_id="",
        vercel_team_slug="",
        neon_org_id="",
        neon_region="aws-us-east-1",
        neon_pg_version=16,
    )
    assert len(results) == 1
    assert results[0]["status"] == "manual_only"
    assert results[0]["provider"] == "UnknownDB"


def test_hydrate_starter_env_example_with_existing_file(tmp_path: Path) -> None:
    """hydrate_starter_env_example merges into existing .env.example (line 148)."""
    root_dir = tmp_path / "my-app"
    root_dir.mkdir()
    env_file = root_dir / ".env.example"
    env_file.write_text("# Existing\nOLD_KEY=old\n", encoding="utf-8")

    plan = create_core.StarterScaffoldPlan(label="test", root_dir="my-app", run_hint="npm start", files={})
    services: list[dict[str, object]] = [{"env": {"NEW_KEY": "new_value"}}]

    result = create_core.hydrate_starter_env_example(tmp_path, plan, services)
    assert result == env_file
    content = env_file.read_text(encoding="utf-8")
    assert "NEW_KEY=new_value" in content
    assert "OLD_KEY=old" in content


def test_hydrate_starter_env_example_creates_new_file(tmp_path: Path) -> None:
    """hydrate_starter_env_example creates default template when .env.example missing (line 150)."""
    root_dir = tmp_path / "my-app"
    root_dir.mkdir()

    plan = create_core.StarterScaffoldPlan(label="test", root_dir="my-app", run_hint="npm start", files={})
    services: list[dict[str, object]] = [{"env": {"API_KEY": "test123"}}]

    result = create_core.hydrate_starter_env_example(tmp_path, plan, services)
    assert result is not None
    content = result.read_text(encoding="utf-8")
    assert "API_KEY=test123" in content
    assert "Environment template" in content


def test_hydrate_starter_env_example_returns_none_when_no_env(tmp_path: Path) -> None:
    """hydrate_starter_env_example returns None when no env values (line 144)."""
    plan = create_core.StarterScaffoldPlan(label="test", root_dir="my-app", run_hint="npm start", files={})
    result = create_core.hydrate_starter_env_example(tmp_path, plan, [{}])
    assert result is None


def test_create_github_repo_dry_run_prints_command(tmp_path: Path, capsys) -> None:
    """dry_run=True prints command instead of running subprocess (line 528)."""
    create_core.create_github_repo(
        destination_root=tmp_path,
        github_repo="owner/test-repo",
        github_visibility="private",
        dry_run=True,
    )
    out = capsys.readouterr().out
    assert "RUN" in out
    assert "owner/test-repo" in out


def test_provision_supabase_missing_token_raises(monkeypatch) -> None:
    """Missing SUPABASE_ACCESS_TOKEN raises RuntimeError (line 299)."""
    monkeypatch.delenv("SUPABASE_ACCESS_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="SUPABASE_ACCESS_TOKEN"):
        create_core.provision_supabase_project(project_name="test", organization_id="org-1", region="us-east-1", plan="free")


def test_provision_vercel_missing_token_raises(monkeypatch) -> None:
    """Missing VERCEL_ACCESS_TOKEN raises RuntimeError (line 351)."""
    monkeypatch.delenv("VERCEL_ACCESS_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="VERCEL_ACCESS_TOKEN"):
        create_core.provision_vercel_project(project_name="test", team_id="", team_slug="")


def test_provision_neon_missing_token_raises(monkeypatch) -> None:
    """Missing NEON_API_KEY raises RuntimeError (line 395)."""
    monkeypatch.delenv("NEON_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="NEON_API_KEY"):
        create_core.provision_neon_project(project_name="test", organization_id="", region="aws-us-east-1", pg_version=16)
