from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_starter_scaffold as scaffold
from scripts.programstart_recommend import ProjectRecommendation

# ── helpers ────────────────────────────────────────────────────────────────────


def _make_recommendation(
    product_shape: str,
    stack_names: list[str] | None = None,
    service_names: list[str] | None = None,
    api_names: list[str] | None = None,
    suggested_companion_surfaces: list[str] | None = None,
) -> ProjectRecommendation:
    return ProjectRecommendation(
        product_shape=product_shape,
        variant="product",
        attach_userjourney=False,
        archetype="Test archetype",
        stack_names=stack_names or [],
        service_names=service_names or [],
        api_names=api_names or [],
        suggested_companion_surfaces=suggested_companion_surfaces or [],
    )


# ── slugify_project_name ───────────────────────────────────────────────────────


def test_slugify_replaces_spaces_with_underscores() -> None:
    assert scaffold.slugify_project_name("My Project") == "my_project"


def test_slugify_removes_special_characters() -> None:
    assert scaffold.slugify_project_name("App@v2.0!") == "app_v2_0"


def test_slugify_returns_fallback_for_blank_input() -> None:
    assert scaffold.slugify_project_name("") == "generated_app"


def test_slugify_lowercases_result() -> None:
    assert scaffold.slugify_project_name("UPPER") == "upper"


# ── has_stack / has_service / has_api ──────────────────────────────────────────


def test_has_stack_returns_true_for_present_stack() -> None:
    rec = _make_recommendation("web app", stack_names=["Next.js", "Playwright"])
    assert scaffold.has_stack(rec, "Next.js") is True


def test_has_stack_is_case_insensitive() -> None:
    rec = _make_recommendation("web app", stack_names=["NEXT.JS"])
    assert scaffold.has_stack(rec, "next.js") is True


def test_has_stack_returns_false_when_not_present() -> None:
    rec = _make_recommendation("web app", stack_names=["React"])
    assert scaffold.has_stack(rec, "Playwright") is False


def test_has_service_returns_true_for_present_service() -> None:
    rec = _make_recommendation("web app", service_names=["Supabase", "Vercel"])
    assert scaffold.has_service(rec, "Vercel") is True


def test_has_service_returns_false_when_not_present() -> None:
    rec = _make_recommendation("web app", service_names=["Supabase"])
    assert scaffold.has_service(rec, "Neon") is False


def test_has_api_returns_true_for_present_api() -> None:
    rec = _make_recommendation("web app", api_names=["OpenAI", "Stripe"])
    assert scaffold.has_api(rec, "Stripe") is True


def test_has_api_returns_false_when_not_present() -> None:
    rec = _make_recommendation("web app", api_names=["OpenAI"])
    assert scaffold.has_api(rec, "Anthropic") is False


# ── toml_string_list ───────────────────────────────────────────────────────────


def test_toml_string_list_empty_returns_bracket_pair() -> None:
    assert scaffold.toml_string_list([]) == "[]"


def test_toml_string_list_single_item() -> None:
    result = scaffold.toml_string_list(["pydantic>=2.0"])
    assert '"pydantic>=2.0"' in result


def test_toml_string_list_multiple_items_include_commas() -> None:
    result = scaffold.toml_string_list(["fastapi>=0.115", "pydantic>=2.0"])
    assert '"fastapi>=0.115",' in result
    assert '"pydantic>=2.0",' in result


# ── build_starter_scaffold_plan ────────────────────────────────────────────────


def test_build_starter_scaffold_plan_cli_tool_uses_starter_cli_root() -> None:
    rec = _make_recommendation("cli tool")
    plan = scaffold.build_starter_scaffold_plan("my-cli", rec)
    assert plan.root_dir == "starter/cli_tool"


def test_build_starter_scaffold_plan_api_service_uses_api_root() -> None:
    rec = _make_recommendation("api service")
    plan = scaffold.build_starter_scaffold_plan("my-api", rec)
    assert plan.root_dir == "starter/api_service"


def test_build_starter_scaffold_plan_web_app_uses_web_root() -> None:
    rec = _make_recommendation("web app")
    plan = scaffold.build_starter_scaffold_plan("my-web", rec)
    assert plan.root_dir == "starter/web_app"


def test_build_starter_scaffold_plan_mobile_app_uses_mobile_root() -> None:
    rec = _make_recommendation("mobile app")
    plan = scaffold.build_starter_scaffold_plan("my-mobile", rec)
    assert plan.root_dir == "starter/mobile_app"


def test_build_starter_scaffold_plan_data_pipeline_uses_pipeline_root() -> None:
    rec = _make_recommendation("data pipeline")
    plan = scaffold.build_starter_scaffold_plan("my-pipeline", rec)
    assert plan.root_dir == "starter/data_pipeline"


def test_build_starter_scaffold_plan_unknown_shape_uses_app_root() -> None:
    rec = _make_recommendation("desktop tool")
    plan = scaffold.build_starter_scaffold_plan("my-app", rec)
    assert plan.root_dir == "starter/app"


def test_build_starter_scaffold_plan_includes_starter_readme() -> None:
    rec = _make_recommendation("cli tool")
    plan = scaffold.build_starter_scaffold_plan("readme-test", rec)
    assert "starter/README.md" in plan.files


def test_build_starter_scaffold_plan_cli_produces_pyproject_toml() -> None:
    rec = _make_recommendation("cli tool")
    plan = scaffold.build_starter_scaffold_plan("my-cli", rec)
    toml_path = "starter/cli_tool/pyproject.toml"
    assert toml_path in plan.files
    assert "requires-python" in plan.files[toml_path]


def test_build_starter_scaffold_plan_adds_service_env_example_for_supabase() -> None:
    rec = _make_recommendation("web app", service_names=["Supabase"])
    plan = scaffold.build_starter_scaffold_plan("my-app", rec)
    env_path = "starter/web_app/.env.example"
    assert env_path in plan.files
    assert "SUPABASE_PROJECT_REF" in plan.files[env_path]


def test_build_starter_scaffold_plan_adds_api_env_example_for_openai() -> None:
    rec = _make_recommendation("api service", api_names=["OpenAI"])
    plan = scaffold.build_starter_scaffold_plan("my-api", rec)
    # At least one file should contain OPENAI_API_KEY
    all_content = "\n".join(plan.files.values())
    assert "OPENAI_API_KEY" in all_content


def test_build_starter_scaffold_plan_hypothesis_adds_property_test() -> None:
    rec = _make_recommendation("cli tool", stack_names=["Hypothesis", "pytest"])
    plan = scaffold.build_starter_scaffold_plan("my-cli", rec)
    hypothesis_path = "starter/cli_tool/tests/test_models_property.py"
    assert hypothesis_path in plan.files


# ── write_starter_scaffold ─────────────────────────────────────────────────────


def test_write_starter_scaffold_creates_all_files(tmp_path: Path) -> None:
    rec = _make_recommendation("cli tool")
    plan = scaffold.build_starter_scaffold_plan("write-test", rec)
    created = scaffold.write_starter_scaffold(tmp_path, plan)
    assert len(created) > 0
    for path in created:
        assert path.exists()


def test_write_starter_scaffold_creates_parent_directories(tmp_path: Path) -> None:
    rec = _make_recommendation("api service")
    plan = scaffold.build_starter_scaffold_plan("nested-test", rec)
    scaffold.write_starter_scaffold(tmp_path, plan)
    # Check deep nesting was created
    assert (tmp_path / "starter" / "api_service").is_dir()


def test_write_starter_scaffold_writes_correct_content(tmp_path: Path) -> None:
    rec = _make_recommendation("cli tool")
    plan = scaffold.build_starter_scaffold_plan("content-check", rec)
    scaffold.write_starter_scaffold(tmp_path, plan)
    readme = (tmp_path / "starter" / "README.md").read_text(encoding="utf-8")
    assert "content-check" in readme


# ── build_admin_dashboard_plan ─────────────────────────────────────────────────


def test_build_admin_dashboard_plan_returns_expected_files() -> None:
    files = scaffold.build_admin_dashboard_plan("My API")
    expected_paths = [
        "starter/admin_dashboard/package.json",
        "starter/admin_dashboard/vite.config.ts",
        "starter/admin_dashboard/src/main.tsx",
        "starter/admin_dashboard/src/DashboardLayout.tsx",
        "starter/admin_dashboard/src/api.ts",
        "starter/admin_dashboard/tests/dashboard.spec.ts",
        "starter/admin_dashboard/README.md",
    ]
    for path in expected_paths:
        assert path in files, f"Missing file: {path}"


def test_build_admin_dashboard_plan_uses_slugified_name_in_package_json() -> None:
    files = scaffold.build_admin_dashboard_plan("My API")
    package_json = files["starter/admin_dashboard/package.json"]
    assert '"my_api-admin"' in package_json


def test_build_admin_dashboard_plan_includes_react_dependency() -> None:
    files = scaffold.build_admin_dashboard_plan("test")
    package_json = files["starter/admin_dashboard/package.json"]
    assert '"react"' in package_json
    assert '"react-dom"' in package_json


def test_build_starter_scaffold_plan_includes_dashboard_when_companion_surface() -> None:
    rec = _make_recommendation(
        "api service",
        suggested_companion_surfaces=["admin dashboard"],
    )
    plan = scaffold.build_starter_scaffold_plan("dash-test", rec)
    assert "starter/admin_dashboard/package.json" in plan.files


def test_build_starter_scaffold_plan_excludes_dashboard_when_no_companion() -> None:
    rec = _make_recommendation("api service")
    plan = scaffold.build_starter_scaffold_plan("no-dash", rec)
    assert "starter/admin_dashboard/package.json" not in plan.files
