"""USERJOURNEY-specific project factory tests.

These tests require the USERJOURNEY directory to exist in the template repo
because they use it as an --attachment-source for init/create/attach operations.
Only copied to project repos when USERJOURNEY is attached.
"""

from __future__ import annotations

import json
from pathlib import Path

from scripts import (
    programstart_attach,
    programstart_create,
    programstart_init,
)

ROOT = Path(__file__).resolve().parents[1]

from conftest import requires_userjourney

pytestmark = requires_userjourney


def test_attach_userjourney_copies_from_source(tmp_path: Path) -> None:
    destination = tmp_path / "repo"
    destination.mkdir()
    (destination / "config").mkdir()
    project_registry = json.loads((ROOT / "config" / "process-registry.json").read_text(encoding="utf-8"))
    project_registry["workspace"] = dict(project_registry.get("workspace", {}))
    project_registry["workspace"]["repo_role"] = "project_repo"
    project_registry["workspace"]["bootstrap_assets"] = [
        asset
        for asset in project_registry["workspace"].get("bootstrap_assets", [])
        if asset
        not in {
            ".github/prompts/userjourney-next-slice.prompt.md",
            ".github/prompts/shape-uj-decision-freeze.prompt.md",
            ".github/prompts/shape-uj-legal-drafts.prompt.md",
            ".github/prompts/shape-uj-ux-surfaces.prompt.md",
        }
    ]
    project_registry["prompt_registry"] = dict(project_registry.get("prompt_registry", {}))
    project_registry["prompt_registry"]["workflow_prompt_files"] = [
        prompt
        for prompt in project_registry["prompt_registry"].get("workflow_prompt_files", [])
        if prompt
        not in {
            ".github/prompts/userjourney-next-slice.prompt.md",
            ".github/prompts/shape-uj-decision-freeze.prompt.md",
            ".github/prompts/shape-uj-legal-drafts.prompt.md",
            ".github/prompts/shape-uj-ux-surfaces.prompt.md",
        }
    ]
    project_registry["prompt_authority"] = {
        key: value
        for key, value in project_registry.get("prompt_authority", {}).items()
        if key
        not in {
            ".github/prompts/userjourney-next-slice.prompt.md",
            ".github/prompts/shape-uj-decision-freeze.prompt.md",
            ".github/prompts/shape-uj-legal-drafts.prompt.md",
            ".github/prompts/shape-uj-ux-surfaces.prompt.md",
        }
    }
    (destination / "config" / "process-registry.json").write_text(
        json.dumps(project_registry, indent=2) + "\n",
        encoding="utf-8",
    )
    source = ROOT / "USERJOURNEY"

    programstart_attach.attach_userjourney(destination, source)

    assert (destination / "USERJOURNEY" / "README.md").exists()
    assert (destination / "USERJOURNEY" / "USERJOURNEY_STATE.json").exists()
    assert (destination / ".github" / "prompts" / "userjourney-next-slice.prompt.md").exists()
    result = json.loads((destination / "config" / "process-registry.json").read_text(encoding="utf-8"))
    assert ".github/prompts/userjourney-next-slice.prompt.md" in result["prompt_registry"]["workflow_prompt_files"]
    assert ".github/prompts/shape-uj-ux-surfaces.prompt.md" in result["prompt_authority"]
    assert ".github/prompts/userjourney-next-slice.prompt.md" in result["workspace"]["bootstrap_assets"]


def test_init_can_attach_userjourney(tmp_path: Path) -> None:
    destination = tmp_path / "initialized"
    result = programstart_init.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "AcmeJourney",
            "--product-shape",
            "web app",
            "--attach-userjourney",
            "--attachment-source",
            str(ROOT / "USERJOURNEY"),
        ]
    )
    assert result == 0
    assert (destination / "USERJOURNEY" / "README.md").exists()


def test_create_can_attach_userjourney_and_emit_dynamic_plan(tmp_path: Path) -> None:
    destination = tmp_path / "created-web"
    source = ROOT / "USERJOURNEY"
    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "FactoryWeb",
            "--product-shape",
            "web app",
            "--attachment-source",
            str(source),
            "--owner",
            "Factory Owner",
        ]
    )

    assert result == 0
    plan_text = (destination / "outputs" / "factory" / "create-plan.md").read_text(encoding="utf-8")
    provisioning_text = (destination / "outputs" / "factory" / "provisioning-plan.md").read_text(encoding="utf-8")
    setup_surface = (destination / "outputs" / "factory" / "setup-surface.md").read_text(encoding="utf-8")
    package_json = (destination / "starter" / "web_app" / "package.json").read_text(encoding="utf-8")
    page_text = (destination / "starter" / "web_app" / "app" / "page.tsx").read_text(encoding="utf-8")
    env_example = (destination / "starter" / "web_app" / ".env.example").read_text(encoding="utf-8")
    assert "Dynamic Prompt Guidance" in plan_text
    assert "KB Decision Evidence" in plan_text
    assert "Rule Evidence" in plan_text
    assert "Actionability Summary" in plan_text
    assert "Repository Boundary And Provisioning" in plan_text
    assert "Supabase" in plan_text
    assert "Vercel" in plan_text
    assert "Kickoff Prompt" in plan_text
    assert "Starter Scaffold" in plan_text
    assert "Recommendation Context" in setup_surface
    assert "Matched Domains" in setup_surface
    assert "Actionability Summary" in setup_surface
    assert (
        "Review outputs/factory/provisioning-plan.md and execute automation-supported provisioning before manual setup"
        in plan_text
    )
    assert "GitHub Remote" in provisioning_text
    assert "Auto-Inferred Services" in provisioning_text
    assert (destination / "starter" / "web_app" / "package.json").exists()
    assert (destination / "starter" / "web_app" / "e2e" / "home.spec.ts").exists()
    assert '"next": "^16"' in package_json
    assert '"@playwright/test": "^1"' in package_json
    assert "recommended product stack" in page_text
    assert "NEXT_PUBLIC_SUPABASE_URL=" in env_example
    assert "VERCEL_PROJECT_ID=" in env_example
    assert (destination / "USERJOURNEY" / "README.md").exists()


def test_create_mobile_app_emits_expo_starter_and_subscription_surface(tmp_path: Path) -> None:
    destination = tmp_path / "created-mobile"
    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "FactoryMobile",
            "--product-shape",
            "mobile app",
            "--attachment-source",
            str(ROOT / "USERJOURNEY"),
            "--need",
            "subscriptions",
        ]
    )

    assert result == 0
    package_json = (destination / "starter" / "mobile_app" / "package.json").read_text(encoding="utf-8")
    app_text = (destination / "starter" / "mobile_app" / "App.tsx").read_text(encoding="utf-8")
    subscription_text = (destination / "starter" / "mobile_app" / "src" / "subscriptions.ts").read_text(encoding="utf-8")
    env_example = (destination / "starter" / "mobile_app" / ".env.example").read_text(encoding="utf-8")
    assert '"expo": "~53.0.20"' in package_json
    assert '"react-native": "^0.85"' in package_json
    assert "Expo starter aligned to the recommended mobile stack" in app_text
    assert "revenuecat" in subscription_text
    assert "EXPO_PUBLIC_REVENUECAT_API_KEY=" in env_example


def test_create_web_app_adds_realtime_and_commerce_optional_files(tmp_path: Path) -> None:
    destination = tmp_path / "created-integrations"
    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "FactoryIntegrations",
            "--product-shape",
            "web app",
            "--attachment-source",
            str(ROOT / "USERJOURNEY"),
            "--need",
            "realtime",
            "--need",
            "customer-data",
            "--need",
            "shipping",
            "--need",
            "tax",
        ]
    )

    assert result == 0
    realtime_module = (destination / "starter" / "web_app" / "lib" / "realtime.ts").read_text(encoding="utf-8")
    commerce_module = (destination / "starter" / "web_app" / "lib" / "commerce.ts").read_text(encoding="utf-8")
    env_example = (destination / "starter" / "web_app" / ".env.example").read_text(encoding="utf-8")
    assert "conflict resolution" in realtime_module
    assert "analytics-routing" in commerce_module
    assert "NEXT_PUBLIC_ABLY_CLIENT_KEY=" in env_example or "NEXT_PUBLIC_PUSHER_KEY=" in env_example
    assert "SEGMENT_WRITE_KEY=" in env_example
    assert "SHIPPO_API_TOKEN=" in env_example
    assert "TAXJAR_API_KEY=" in env_example


def test_create_can_provision_supabase_and_vercel(monkeypatch, tmp_path: Path, capsys) -> None:
    destination = tmp_path / "created-services"

    def fake_urlopen(http_request, timeout=60):
        class Response:
            def __init__(self, payload: dict[str, str]):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return json.dumps(self.payload).encode("utf-8")

        if http_request.full_url == "https://api.supabase.com/v1/projects":
            return Response({"ref": "abc123xyz", "name": "FactoryWeb"})
        if http_request.full_url == "https://api.vercel.com/v11/projects":
            return Response({"id": "prj_123", "name": "factoryweb"})
        raise AssertionError(http_request.full_url)

    monkeypatch.setenv("SUPABASE_ACCESS_TOKEN", "token")
    monkeypatch.setenv("VERCEL_ACCESS_TOKEN", "vercel-token")
    monkeypatch.setattr("scripts.programstart_create.request.urlopen", fake_urlopen)

    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "FactoryWeb",
            "--product-shape",
            "web app",
            "--attachment-source",
            str(ROOT / "USERJOURNEY"),
            "--provision-services",
            "--supabase-org-id",
            "org_123",
        ]
    )

    out = capsys.readouterr().out
    assert result == 0
    state_path = destination / "outputs" / "factory" / "provisioning-state.json"
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    env_example = (destination / "starter" / "web_app" / ".env.example").read_text(encoding="utf-8")
    service_names = {item["name"] for item in payload["services"]}
    assert service_names == {"Supabase", "Vercel"}
    supabase = next(item for item in payload["services"] if item["name"] == "Supabase")
    vercel = next(item for item in payload["services"] if item["name"] == "Vercel")
    assert supabase["status"] == "provisioning_started"
    assert supabase["automation_level"] == "partial"
    assert supabase["completion_status"] == "action_required"
    assert supabase["project"]["ref"] == "abc123xyz"
    assert vercel["status"] == "created"
    assert vercel["automation_level"] == "full"
    assert vercel["completion_status"] == "complete"
    assert payload["completion"]["status"] == "action_required"
    assert payload["completion"]["completed_services"] == ["Vercel"]
    assert payload["completion"]["pending_services"] == ["Supabase"]
    assert vercel["project"]["id"] == "prj_123"
    assert "SUPABASE_PROJECT_REF=abc123xyz" in env_example
    assert "SUPABASE_URL=https://abc123xyz.supabase.co" in env_example
    assert "NEXT_PUBLIC_SUPABASE_URL=https://abc123xyz.supabase.co" in env_example
    assert "VERCEL_PROJECT_ID=prj_123" in env_example
    assert "Wrote provisioning state" in out


def test_create_merges_explicit_and_inferred_services_without_duplicates(monkeypatch, tmp_path: Path, capsys) -> None:
    destination = tmp_path / "created-merged-services"

    def fake_urlopen(http_request, timeout=60):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                if "supabase" in http_request.full_url:
                    return json.dumps({"ref": "abc123xyz", "name": "FactoryWeb"}).encode("utf-8")
                return json.dumps({"id": "prj_123", "name": "factoryweb"}).encode("utf-8")

        return Response()

    monkeypatch.setenv("SUPABASE_ACCESS_TOKEN", "token")
    monkeypatch.setenv("VERCEL_ACCESS_TOKEN", "vercel-token")
    monkeypatch.setattr("scripts.programstart_create.request.urlopen", fake_urlopen)

    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "FactoryWeb",
            "--product-shape",
            "web app",
            "--attachment-source",
            str(ROOT / "USERJOURNEY"),
            "--service",
            "supabase",
            "--provision-services",
            "--supabase-org-id",
            "org_123",
        ]
    )

    capsys.readouterr()
    assert result == 0
    state_path = destination / "outputs" / "factory" / "provisioning-state.json"
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    service_names = [item["name"] for item in payload["services"]]
    assert service_names.count("Supabase") == 1
