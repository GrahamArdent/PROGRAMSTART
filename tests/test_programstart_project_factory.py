from __future__ import annotations

import json
from pathlib import Path

from scripts import (
    programstart_create,
    programstart_impact,
    programstart_init,
    programstart_recommend,
    programstart_research_delta,
    programstart_workflow_state,
)
from scripts.programstart_common import load_registry
from scripts.programstart_validate import validate_bootstrap_assets

ROOT = Path(__file__).resolve().parents[1]


def test_validate_bootstrap_assets_passes_current_repo() -> None:
    assert validate_bootstrap_assets(load_registry()) == []


def test_recommend_cli_json_for_cli_tool(capsys) -> None:
    result = programstart_recommend.main(["--product-shape", "CLI tool", "--json"])
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert payload["product_shape"] == "cli tool"
    assert payload["variant"] in {"lite", "product", "enterprise"}
    assert "uv" in [name.lower() for name in payload["stack_names"]]
    assert payload["service_names"] == []
    assert payload["api_names"] == []
    assert "GitHub CLI" in payload["cli_tool_names"]
    assert "uv" in [name.lower() for name in payload["cli_tool_names"]]
    assert payload["confidence"] == "high"
    assert payload["stack_evidence"]


def test_recommend_cli_json_for_web_app_infers_supabase(capsys) -> None:
    result = programstart_recommend.main(["--product-shape", "web app", "--json"])
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert "Supabase" in payload["service_names"]
    assert "Vercel" in payload["service_names"]


def test_recommend_cli_json_for_api_service_infers_neon(capsys) -> None:
    result = programstart_recommend.main(["--product-shape", "api service", "--json"])
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert "Neon" in payload["service_names"]
    assert "GitHub CLI" in payload["cli_tool_names"]
    assert "API, workflow, and backend platforms" in payload["matched_domains"]
    assert payload["alternatives"]


def test_recommend_api_service_ai_and_agents_uses_kb_rule_driven_stacks(capsys) -> None:
    result = programstart_recommend.main(
        [
            "--product-shape",
            "api service",
            "--need",
            "rag",
            "--need",
            "agents",
            "--json",
        ]
    )
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    stacks = {item.lower() for item in payload["stack_names"]}
    assert "litellm" in stacks
    assert "instructor" in stacks
    assert "chromadb" in stacks
    assert "temporal" in stacks
    assert "langgraph" in stacks
    assert any(
        item["title"] == "Prefer explicit LLM routing and typed response validation for AI product workflows"
        for item in payload["rule_evidence"]
    )
    assert any(
        item["title"] == "Prefer durable orchestration for agent and multi-step automation systems"
        for item in payload["rule_evidence"]
    )
    assert "Drata" not in payload["api_names"]
    assert "Vanta" not in payload["api_names"]
    assert any("provisioning-plan.md" in command for command in payload["next_commands"])
    assert any("setup-surface.md" in command for command in payload["next_commands"])


def test_recommend_mobile_app_flags_partial_domain_coverage(capsys) -> None:
    result = programstart_recommend.main(
        [
            "--product-shape",
            "mobile app",
            "--need",
            "subscriptions",
            "--json",
        ]
    )
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    stacks = {item.lower() for item in payload["stack_names"]}
    warning_domains = {item["domain"]: item["status"] for item in payload["coverage_warnings"]}
    assert "react native" in stacks or "expo" in stacks
    assert payload["confidence"] == "medium"
    assert warning_domains["Mobile and cross-platform apps"] == "partial"


def test_recommend_mobile_subscriptions_infers_revenuecat_with_comparison_context(capsys) -> None:
    result = programstart_recommend.main(
        [
            "--product-shape",
            "mobile app",
            "--need",
            "subscriptions",
            "--json",
        ]
    )
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert "RevenueCat" in payload["api_names"]
    assert payload["api_evidence"]
    assert payload["rule_evidence"]
    assert any(
        item["name"] == "RevenueCat" and item["actionability"] == "manual-setup" for item in payload["actionability_summary"]
    )
    assert any("Stripe Billing vs RevenueCat" in item["item"] for item in payload["alternatives"])


def test_recommend_commerce_integrations_infers_targeted_apis(capsys) -> None:
    result = programstart_recommend.main(
        [
            "--product-shape",
            "web app",
            "--need",
            "customer-data",
            "--need",
            "shipping",
            "--need",
            "tax",
            "--json",
        ]
    )
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert "Segment" in payload["api_names"]
    assert "Shippo" in payload["api_names"]
    assert "TaxJar" in payload["api_names"]
    assert payload["api_evidence"]
    assert any(
        item["title"] == "Prefer explicit commerce integration surfaces for product workflows"
        for item in payload["rule_evidence"]
    )


def test_recommend_web_app_includes_managed_hosting_rule_evidence(capsys) -> None:
    result = programstart_recommend.main(
        [
            "--product-shape",
            "web app",
            "--need",
            "hosting",
            "--need",
            "authentication",
            "--json",
        ]
    )
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert "Supabase" in payload["service_names"]
    assert "Vercel" in payload["service_names"]
    assert any(
        item["title"] == "Prefer managed web product hosting and data defaults for generated app repos"
        for item in payload["rule_evidence"]
    )


def test_impact_cli_returns_json(capsys) -> None:
    result = programstart_impact.main(["workflow", "--json"])
    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert "relations" in payload
    assert "decision_rules" in payload
    assert "comparisons" in payload


def test_research_cli_writes_delta_template(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "delta.md"
    result = programstart_research_delta.main(
        [
            "--track",
            "Python runtime and packaging",
            "--date",
            "2026-03-29",
            "--output",
            str(output_path),
        ]
    )
    out = capsys.readouterr().out
    assert result == 0
    assert "Wrote research delta template" in out
    text = output_path.read_text(encoding="utf-8")
    assert "# Research Delta - Python runtime and packaging" in text
    assert "Outcome: changed | unchanged | blocked pending evidence" in text


def test_init_stamps_kickoff_packet_and_readme(tmp_path: Path) -> None:
    destination = tmp_path / "initialized"
    result = programstart_init.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "AcmePlanner",
            "--product-shape",
            "CLI tool",
            "--one-line-description",
            "A planning CLI",
            "--owner",
            "Acme Owner",
        ]
    )
    assert result == 0
    kickoff_text = (destination / "PROGRAMBUILD" / "PROGRAMBUILD_KICKOFF_PACKET.md").read_text(encoding="utf-8")
    readme_text = (destination / "README.md").read_text(encoding="utf-8")
    assert "PROJECT_NAME: AcmePlanner" in kickoff_text
    assert "PRODUCT_SHAPE: CLI tool" in kickoff_text
    assert "# AcmePlanner" in readme_text
    assert "A planning CLI" in readme_text
    assert (destination / ".git").exists()


def test_create_builds_programbuild_only_repo_and_plan(tmp_path: Path) -> None:
    destination = tmp_path / "created"
    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "FactoryCLI",
            "--product-shape",
            "CLI tool",
            "--owner",
            "Factory Owner",
        ]
    )

    assert result == 0
    assert (destination / "outputs" / "factory" / "create-plan.md").exists()
    assert (destination / "outputs" / "factory" / "provisioning-plan.md").exists()
    assert (destination / "outputs" / "factory" / "setup-surface.md").exists()
    assert (destination / "starter" / "cli_tool" / "README.md").exists()
    assert (destination / "starter" / "cli_tool" / "src" / "factorycli" / "main.py").exists()
    cli_pyproject = (destination / "starter" / "cli_tool" / "pyproject.toml").read_text(encoding="utf-8")
    cli_models = (destination / "starter" / "cli_tool" / "src" / "factorycli" / "models.py").read_text(encoding="utf-8")
    cli_property_test = (destination / "starter" / "cli_tool" / "tests" / "test_models_property.py").read_text(encoding="utf-8")
    assert "pydantic>=2.0" in cli_pyproject
    assert "GreetingRequest" in cli_models
    assert "from hypothesis import given" in cli_property_test
    assert (destination / "config" / "process-registry.json").exists()
    assert (destination / ".git").exists()
    registry = json.loads((destination / "config" / "process-registry.json").read_text(encoding="utf-8"))
    assert registry["workspace"]["repo_role"] == "project_repo"
    assert registry["workspace"]["repo_boundary"] == "standalone_project_repo"
    assert registry["workspace"]["provisioning_scope"] == "project_repo_only"
    assert registry["validation"]["enforce_engineering_ready_in_all"] is True


def test_create_api_service_emits_fastapi_agent_stack_starter(tmp_path: Path) -> None:
    destination = tmp_path / "created-api"
    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "FactoryAPI",
            "--product-shape",
            "API service",
            "--need",
            "rag",
            "--need",
            "agents",
        ]
    )

    assert result == 0
    api_pyproject = (destination / "starter" / "api_service" / "pyproject.toml").read_text(encoding="utf-8")
    app_main = (destination / "starter" / "api_service" / "app" / "main.py").read_text(encoding="utf-8")
    ai_module = (destination / "starter" / "api_service" / "app" / "ai.py").read_text(encoding="utf-8")
    retrieval_module = (destination / "starter" / "api_service" / "app" / "retrieval.py").read_text(encoding="utf-8")
    workflow_module = (destination / "starter" / "api_service" / "app" / "workflows.py").read_text(encoding="utf-8")
    env_example = (destination / "starter" / "api_service" / ".env.example").read_text(encoding="utf-8")
    setup_surface = (destination / "outputs" / "factory" / "setup-surface.md").read_text(encoding="utf-8")
    assert "fastapi>=0.115.12,<0.116.0" in api_pyproject
    assert "litellm>=1.40.0" in api_pyproject
    assert "chromadb>=0.4.0" in api_pyproject
    assert "temporalio>=1.8.0" in api_pyproject
    assert "FastAPI" in app_main
    assert "litellm" in ai_module
    assert "chromadb" in retrieval_module
    assert "temporal" in workflow_module
    assert "NEON_PROJECT_ID=" in env_example
    assert "DATABASE_URL=" in env_example
    assert "OPENAI_API_KEY=" in env_example
    assert "ANTHROPIC_API_KEY=" in env_example
    assert "GitHub CLI" in setup_surface
    assert "OpenAI" in setup_surface


def test_create_can_skip_starter_scaffold(tmp_path: Path) -> None:
    destination = tmp_path / "created-no-starter"
    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "FactoryNoStarter",
            "--product-shape",
            "CLI tool",
            "--no-starter-scaffold",
        ]
    )

    assert result == 0
    assert not (destination / "starter").exists()


def test_create_rejects_destination_inside_template_repo(capsys) -> None:
    destination = ROOT / ".tmp_invalid_factory_dest"
    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "InvalidFactory",
            "--product-shape",
            "CLI tool",
            "--dry-run",
        ]
    )

    out = capsys.readouterr().out
    assert result == 1
    assert "outside the PROGRAMSTART template repo" in out


def test_create_can_request_github_repo_creation(monkeypatch, tmp_path: Path, capsys) -> None:
    destination = tmp_path / "created-gh"
    commands: list[list[str]] = []

    def fake_run(command, cwd=None, check=None, capture_output=None, text=None):
        commands.append(command)

        class Result:
            returncode = 0

        if command[0] == "git":
            assert cwd is not None
            (Path(cwd) / ".git").mkdir(exist_ok=True)
        return Result()

    monkeypatch.setattr("scripts.programstart_bootstrap.shutil.which", lambda name: name)
    monkeypatch.setattr("scripts.programstart_bootstrap.subprocess.run", fake_run)
    monkeypatch.setattr("scripts.programstart_create.shutil.which", lambda name: name)
    monkeypatch.setattr("scripts.programstart_create.subprocess.run", fake_run)

    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "FactoryGitHub",
            "--product-shape",
            "CLI tool",
            "--github-repo",
            "acme/factory-github",
            "--create-github-repo",
            "--service",
            "supabase",
        ]
    )

    out = capsys.readouterr().out
    assert result == 0
    assert any(command[:3] == ["gh", "repo", "create"] for command in commands)
    assert "Created GitHub repo acme/factory-github" in out


def test_create_can_provision_neon_and_hydrate_env(monkeypatch, tmp_path: Path, capsys) -> None:
    destination = tmp_path / "created-api-neon"

    def fake_urlopen(http_request, timeout=60):
        class Response:
            def __init__(self, payload: dict[str, object]):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return json.dumps(self.payload).encode("utf-8")

        if http_request.full_url == "https://console.neon.tech/api/v2/projects":
            return Response(
                {
                    "project": {
                        "id": "spring-example-302709",
                        "name": "factoryapi",
                        "region_id": "aws-us-east-2",
                        "proxy_host": "ep-cool-darkness-123456.us-east-2.aws.neon.tech",
                    },
                    "branch": {"id": "br-wispy-meadow-118737", "name": "main"},
                    "databases": [{"name": "factoryapi"}],
                    "connection_uris": [
                        {
                            "connection_uri": (
                                "postgresql://factoryapi_owner:supersecret@"  # pragma: allowlist secret
                                "ep-cool-darkness-123456.us-east-2.aws.neon.tech/"
                                "factoryapi?sslmode=require"
                            )
                        }
                    ],
                    "operations": [{"id": "op_123", "status": "running"}],
                }
            )
        raise AssertionError(http_request.full_url)

    monkeypatch.setenv("NEON_API_KEY", "neon-token")
    monkeypatch.setattr("scripts.programstart_create.request.urlopen", fake_urlopen)

    result = programstart_create.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "FactoryAPI",
            "--product-shape",
            "API service",
            "--provision-services",
            "--neon-region",
            "aws-us-east-2",
        ]
    )

    out = capsys.readouterr().out
    assert result == 0
    state_path = destination / "outputs" / "factory" / "provisioning-state.json"
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    env_example = (destination / "starter" / "api_service" / ".env.example").read_text(encoding="utf-8")
    neon = next(item for item in payload["services"] if item["name"] == "Neon")
    project_id = str(neon["env"]["NEON_PROJECT_ID"])
    branch_id = str(neon["env"]["NEON_BRANCH_ID"])
    host = str(neon["env"]["NEON_HOST"])
    assert neon["status"] == "provisioning_started"
    assert project_id == "spring-example-302709"
    assert neon["env"]["DATABASE_URL"].endswith("sslmode=require")
    assert f"NEON_PROJECT_ID={project_id}" in env_example
    assert f"NEON_BRANCH_ID={branch_id}" in env_example
    assert f"NEON_HOST={host}" in env_example
    assert (
        "DATABASE_URL=postgresql://factoryapi_owner:<set-me>@"  # pragma: allowlist secret
        "ep-cool-darkness-123456.us-east-2.aws.neon.tech/"
        "factoryapi?sslmode=require" in env_example  # pragma: allowlist secret
    )
    assert "Hydrated starter env template" in out


def test_impact_cli_handles_programbuild_only_repo(tmp_path: Path, monkeypatch, capsys) -> None:
    destination = tmp_path / "initialized"
    result = programstart_init.main(
        [
            "--dest",
            str(destination),
            "--project-name",
            "AcmePlanner",
            "--product-shape",
            "CLI tool",
        ]
    )

    assert result == 0
    capsys.readouterr()

    monkeypatch.chdir(destination)
    result = programstart_impact.main(["workflow", "--json"])

    out = capsys.readouterr().out
    assert result == 0
    payload = json.loads(out)
    assert "relations" in payload


def test_advance_preflight_blocks_when_problems(capsys, monkeypatch) -> None:
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.preflight_problems",
        lambda _registry, _system, _a=None: ["metadata incomplete"],
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "programbuild"])

    result = programstart_workflow_state.main()
    out = capsys.readouterr().out
    assert result == 1
    assert "Advance preflight failed" in out


def test_advance_skip_preflight_allows_progress(capsys, monkeypatch) -> None:
    saved: dict[str, object] = {}
    state = {
        "active_stage": "inputs_and_mode_selection",
        "stages": {
            "inputs_and_mode_selection": {"status": "in_progress", "signoff": {"decision": "", "date": "", "notes": ""}},
            "feasibility": {"status": "planned", "signoff": {"decision": "", "date": "", "notes": ""}},
        },
    }
    monkeypatch.setattr("scripts.programstart_workflow_state.load_workflow_state", lambda _registry, _system: state)
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_active_step",
        lambda _registry, _system, _state=None: "inputs_and_mode_selection",
    )
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.workflow_steps",
        lambda _registry, _system: ["inputs_and_mode_selection", "feasibility"],
    )
    monkeypatch.setattr("scripts.programstart_workflow_state.preflight_problems", lambda _r, _s, _a=None: ["bad"])
    monkeypatch.setattr(
        "scripts.programstart_workflow_state.save_workflow_state",
        lambda _registry, _system, value: saved.update(value),
    )
    monkeypatch.setattr("sys.argv", ["programstart_workflow_state.py", "advance", "--system", "programbuild", "--skip-preflight"])

    result = programstart_workflow_state.main()
    out = capsys.readouterr().out
    assert result == 0
    assert "Advanced programbuild" in out
    assert saved["active_stage"] == "feasibility"
