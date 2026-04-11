from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib import error as urllib_error

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_create as create
from scripts.programstart_recommend import ProjectRecommendation


# ── helpers ────────────────────────────────────────────────────────────────────

def _make_recommendation(
    product_shape: str = "web app",
    variant: str = "product",
    attach_userjourney: bool = False,
    stack_names: list[str] | None = None,
    service_names: list[str] | None = None,
) -> ProjectRecommendation:
    return ProjectRecommendation(
        product_shape=product_shape,
        variant=variant,
        attach_userjourney=attach_userjourney,
        archetype="Test archetype",
        stack_names=stack_names or [],
        service_names=service_names or [],
    )


# ── normalize_shape ────────────────────────────────────────────────────────────

def test_normalize_shape_lowercases_and_strips() -> None:
    assert create.normalize_shape("  Web App  ") == "web app"


def test_normalize_shape_handles_empty_string() -> None:
    assert create.normalize_shape("") == ""


# ── slugify_project_name ───────────────────────────────────────────────────────

def test_slugify_replaces_spaces_with_dashes() -> None:
    assert create.slugify_project_name("My Cool App") == "my-cool-app"


def test_slugify_removes_special_characters() -> None:
    assert create.slugify_project_name("app@v2!.0") == "app-v2-0"


def test_slugify_returns_fallback_for_blank() -> None:
    assert create.slugify_project_name("") == "generated-project"


# ── default_github_repo_name ───────────────────────────────────────────────────

def test_default_github_repo_name_slugifies_project_name() -> None:
    result = create.default_github_repo_name("My New App")
    assert result == "my-new-app"


# ── merge_service_names ────────────────────────────────────────────────────────

def test_merge_service_names_combines_recommendation_and_explicit() -> None:
    rec = _make_recommendation(service_names=["Supabase"])
    result = create.merge_service_names(rec, ["Vercel"])
    assert "Supabase" in result
    assert "Vercel" in result


def test_merge_service_names_deduplicates_case_insensitive() -> None:
    rec = _make_recommendation(service_names=["Supabase"])
    result = create.merge_service_names(rec, ["supabase"])
    # Only one entry for Supabase
    lower_result = [item.lower() for item in result]
    assert lower_result.count("supabase") == 1


def test_merge_service_names_ignores_blank_explicit_entries() -> None:
    rec = _make_recommendation(service_names=[])
    result = create.merge_service_names(rec, ["", "  ", "Neon"])
    assert "" not in result
    assert "  " not in result
    assert "Neon" in result


def test_merge_service_names_returns_sorted() -> None:
    rec = _make_recommendation(service_names=["Vercel", "Supabase"])
    result = create.merge_service_names(rec, [])
    assert result == sorted(result, key=str.lower)


# ── sanitize_connection_uri ────────────────────────────────────────────────────

def test_sanitize_connection_uri_removes_password() -> None:
    uri = "postgresql://user:supersecret@db.example.com:5432/mydb"
    result = create.sanitize_connection_uri(uri)
    assert "supersecret" not in result
    assert "user" in result
    assert "db.example.com" in result


def test_sanitize_connection_uri_preserves_no_password_uri() -> None:
    uri = "postgresql://user@db.example.com/mydb"
    result = create.sanitize_connection_uri(uri)
    assert "user" in result
    assert "db.example.com" in result


def test_sanitize_connection_uri_returns_original_when_no_host() -> None:
    uri = "sqlite:///local.db"
    result = create.sanitize_connection_uri(uri)
    assert result == uri


def test_sanitize_connection_uri_redacts_password_marker() -> None:
    uri = "postgresql://user:secret@host.io/db"
    result = create.sanitize_connection_uri(uri)
    assert ":<set-me>" in result


# ── first_connection_uri ───────────────────────────────────────────────────────

def test_first_connection_uri_reads_connection_uri_key() -> None:
    payload = {"connection_uri": "postgresql://user@host/db"}
    result = create.first_connection_uri(payload)
    assert result == "postgresql://user@host/db"


def test_first_connection_uri_falls_back_to_connection_uris_list() -> None:
    payload = {"connection_uris": [{"connection_uri": "postgresql://user@host/db"}]}
    result = create.first_connection_uri(payload)
    assert result == "postgresql://user@host/db"


def test_first_connection_uri_searches_nested_project_key() -> None:
    payload = {"project": {"connection_uri": "postgresql://user@nested/db"}}
    result = create.first_connection_uri(payload)
    assert result == "postgresql://user@nested/db"


def test_first_connection_uri_returns_empty_when_not_found() -> None:
    payload = {"irrelevant": "data"}
    result = create.first_connection_uri(payload)
    assert result == ""


# ── merge_env_values ───────────────────────────────────────────────────────────

def test_merge_env_values_applies_updates() -> None:
    base = {"KEY_A": "old", "KEY_B": "unchanged"}
    updates = {"KEY_A": "new"}
    result = create.merge_env_values(base, updates)
    assert result["KEY_A"] == "new"
    assert result["KEY_B"] == "unchanged"


def test_merge_env_values_ignores_empty_update_values() -> None:
    base = {"KEY": "original"}
    result = create.merge_env_values(base, {"KEY": ""})
    assert result["KEY"] == "original"


def test_merge_env_values_strips_newlines_from_values() -> None:
    base = {}
    result = create.merge_env_values(base, {"KEY": "value\nwith\nnewlines"})
    assert "\n" not in result["KEY"]


# ── upsert_env_lines ───────────────────────────────────────────────────────────

def test_upsert_env_lines_updates_existing_key() -> None:
    existing = "KEY_A=old\nKEY_B=keep\n"
    result = create.upsert_env_lines(existing, {"KEY_A": "new"})
    assert "KEY_A=new" in result
    assert "KEY_B=keep" in result


def test_upsert_env_lines_appends_missing_keys() -> None:
    existing = "KEY_A=existing\n"
    result = create.upsert_env_lines(existing, {"KEY_NEW": "added"})
    assert "KEY_NEW=added" in result


def test_upsert_env_lines_does_nothing_for_empty_env_values() -> None:
    existing = "KEY=value\n"
    result = create.upsert_env_lines(existing, {})
    assert result == existing


def test_upsert_env_lines_preserves_comments() -> None:
    existing = "# comment\nKEY=value\n"
    result = create.upsert_env_lines(existing, {"KEY": "updated"})
    assert "# comment" in result


# ── http_json_request error handling ──────────────────────────────────────────

def test_http_json_request_raises_runtime_on_http_error() -> None:
    mock_exc = urllib_error.HTTPError(
        url="https://example.com",
        code=401,
        msg="Unauthorized",
        hdrs=None,  # type: ignore[arg-type]
        fp=None,  # type: ignore[arg-type]
    )
    mock_exc.read = lambda: b"token invalid"
    with patch("scripts.programstart_create.request.urlopen", side_effect=mock_exc):
        with pytest.raises(RuntimeError, match="HTTP 401"):
            create.http_json_request(
                method="POST",
                url="https://example.com/api",
                headers={"Authorization": "Bearer bad-token"},
                payload={"key": "value"},
            )


def test_http_json_request_raises_runtime_on_url_error() -> None:
    mock_exc = urllib_error.URLError(reason="Name resolution failure")
    with patch("scripts.programstart_create.request.urlopen", side_effect=mock_exc):
        with pytest.raises(RuntimeError, match="Network error"):
            create.http_json_request(
                method="GET",
                url="https://unreachable.example.com",
                headers={},
                payload=None,
            )


# ── main (integration via mocked dependencies) ────────────────────────────────

def test_main_returns_zero_on_dry_run(tmp_path: Path) -> None:
    dest = tmp_path / "new_project"
    mock_rec = _make_recommendation(product_shape="cli tool", variant="lite")

    with (
        patch.object(create, "build_recommendation", return_value=mock_rec),
        patch.object(create, "init_main", return_value=0),
        patch.object(create, "write_factory_plan", return_value=tmp_path / "plan.md"),
        patch.object(create, "write_setup_surface", return_value=tmp_path / "setup.md"),
        patch.object(create, "write_provisioning_plan", return_value=tmp_path / "prov.md"),
        patch.object(create, "write_starter_scaffold"),
        patch.object(create, "write_provisioning_state"),
    ):
        result = create.main(
            [
                "--dest", str(dest),
                "--project-name", "test-cli",
                "--product-shape", "cli tool",
                "--dry-run",
            ]
        )
    assert result == 0


def test_main_passes_product_shape_to_build_recommendation(tmp_path: Path) -> None:
    dest = tmp_path / "proj"
    mock_rec = _make_recommendation(product_shape="api service")
    captured_kwargs: list[dict] = []

    def fake_build(**kwargs):
        captured_kwargs.append(kwargs)
        return mock_rec

    with (
        patch.object(create, "build_recommendation", side_effect=fake_build),
        patch.object(create, "init_main", return_value=0),
        patch.object(create, "write_factory_plan", return_value=tmp_path / "plan.md"),
        patch.object(create, "write_setup_surface", return_value=tmp_path / "setup.md"),
        patch.object(create, "write_provisioning_plan", return_value=tmp_path / "prov.md"),
        patch.object(create, "write_starter_scaffold"),
        patch.object(create, "write_provisioning_state"),
    ):
        create.main(
            [
                "--dest", str(dest),
                "--project-name", "my-api",
                "--product-shape", "api service",
                "--dry-run",
            ]
        )
    assert len(captured_kwargs) == 1
    assert captured_kwargs[0]["product_shape"] == "api service"
