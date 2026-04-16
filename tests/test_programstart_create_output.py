from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_create_output as create_output


def test_render_provisioning_plan_keeps_project_repo_boundary_guidance() -> None:
    result = create_output.render_provisioning_plan(
        project_name="FactoryWeb",
        destination_root=Path("/tmp/factory-web"),
        github_repo="acme/factory-web",
        github_visibility="private",
        services=["Supabase"],
        inferred_services=["Supabase", "Vercel"],
    )

    assert "separate project repo derived from PROGRAMSTART" in result
    assert "acme/factory-web" in result
    assert "Supabase" in result


def test_render_provisioning_plan_includes_execution_status_when_results_exist() -> None:
    result = create_output.render_provisioning_plan(
        project_name="FactoryWeb",
        destination_root=Path("/tmp/factory-web"),
        github_repo="acme/factory-web",
        github_visibility="private",
        services=["Supabase", "Vercel"],
        inferred_services=["Supabase", "Vercel"],
        provisioning_results=[
            {
                "name": "Supabase",
                "provider": "Supabase",
                "status": "provisioning_started",
                "manual_secret_targets": ["SUPABASE_ANON_KEY"],
                "manual_steps": ["Retrieve SUPABASE_ANON_KEY."],
                "automation_level": "partial",
                "completion_status": "action_required",
            },
            {
                "name": "Vercel",
                "provider": "Vercel",
                "status": "created",
                "manual_secret_targets": [],
                "manual_steps": [],
                "automation_level": "full",
                "completion_status": "complete",
            },
        ],
    )

    assert "Provisioning Execution Status" in result
    assert "Overall status: action_required" in result
    assert "Pending services: Supabase" in result
    assert "Completed services: Vercel" in result
