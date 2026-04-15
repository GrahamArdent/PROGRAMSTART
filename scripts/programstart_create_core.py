from __future__ import annotations

import json
import os
import re
import secrets
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path
from urllib import error, request
from urllib.parse import urlencode, urlsplit, urlunsplit

try:
    from .programstart_common import generated_outputs_root, load_registry, workspace_path
    from .programstart_recommend import ProjectRecommendation
    from .programstart_starter_scaffold import StarterScaffoldPlan
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_recommend import ProjectRecommendation
    from programstart_starter_scaffold import StarterScaffoldPlan

    from programstart_common import generated_outputs_root, load_registry, workspace_path


def normalize_shape(value: str) -> str:
    return value.strip().lower()


def slugify_project_name(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "generated-project"


def default_github_repo_name(project_name: str) -> str:
    return slugify_project_name(project_name)


def merge_service_names(recommendation: ProjectRecommendation, explicit_services: list[str]) -> list[str]:
    merged: dict[str, str] = {}
    for item in [*recommendation.service_names, *explicit_services]:
        value = item.strip()
        if not value:
            continue
        merged.setdefault(value.lower(), value)
    return sorted(merged.values(), key=str.lower)


def mapping_value(payload: object) -> dict[str, object]:
    return payload if isinstance(payload, dict) else {}


def string_value(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    return value.strip() if isinstance(value, str) else ""


def string_list_value(payload: Mapping[str, object], key: str) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def sanitize_connection_uri(value: str) -> str:
    parsed = urlsplit(value)
    username = parsed.username or ""
    hostname = parsed.hostname or ""
    host = f"{hostname}:{parsed.port}" if parsed.port else hostname
    if not host:
        return value

    netloc = host
    if username:
        password_marker = ":<set-me>" if parsed.password is not None else ""
        netloc = f"{username}{password_marker}@{host}"
    return urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))


def first_connection_uri(payload: Mapping[str, object]) -> str:
    for key in ("connection_uri", "connectionString", "connection_string"):
        value = string_value(payload, key)
        if value:
            return value

    for key in ("connection_uris", "connectionUris"):
        items = payload.get(key)
        if not isinstance(items, list):
            continue
        for item in items:
            value = string_value(mapping_value(item), "connection_uri")
            if value:
                return value

    project_payload = mapping_value(payload.get("project"))
    if project_payload:
        return first_connection_uri(project_payload)
    return ""


def merge_env_values(base: dict[str, str], updates: dict[str, str]) -> dict[str, str]:
    merged = dict(base)
    for key, value in updates.items():
        if not value:
            continue
        merged[key] = value.replace("\n", " ").strip()
    return merged


def upsert_env_lines(existing_text: str, env_values: dict[str, str]) -> str:
    if not env_values:
        return existing_text

    lines = existing_text.splitlines()
    seen: set[str] = set()
    pattern = re.compile(r"^([A-Z0-9_]+)=(.*)$")
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        key = match.group(1)
        if key not in env_values:
            continue
        lines[index] = f"{key}={env_values[key]}"
        seen.add(key)

    missing = [key for key in env_values if key not in seen]
    if missing:
        if lines and lines[-1] != "":
            lines.append("")
        lines.append("# Provisioned service metadata")
        lines.extend(f"{key}={env_values[key]}" for key in missing)

    return "\n".join(lines).rstrip() + "\n"


def hydrate_starter_env_example(
    destination_root: Path, starter_plan: StarterScaffoldPlan, services: list[dict[str, object]]
) -> Path | None:
    env_values: dict[str, str] = {}
    for service in services:
        env_values = merge_env_values(env_values, {key: str(value) for key, value in mapping_value(service.get("env")).items()})

    if not env_values:
        return None

    env_path = destination_root / starter_plan.root_dir / ".env.example"
    if env_path.exists():
        existing_text = env_path.read_text(encoding="utf-8")
    else:
        existing_text = (
            "# Environment template\n"
            "# Non-secret values were hydrated from project provisioning results.\n"
            "# Secrets remain blank and must be stored outside version control.\n\n"
        )
    env_path.write_text(upsert_env_lines(existing_text, env_values), encoding="utf-8")
    return env_path


def knowledge_base_entries_by_name(entries: list[dict[str, object]], names: list[str]) -> list[dict[str, object]]:
    requested = {name.lower(): name for name in names}
    selected: list[dict[str, object]] = []
    for entry in entries:
        entry_name = str(entry.get("name", "")).strip()
        if entry_name.lower() in requested:
            selected.append(entry)
    selected.sort(key=lambda item: str(item.get("name", "")).lower())
    return selected


def write_provisioning_state(destination_root: Path, payload: dict[str, object]) -> Path:
    services_payload = payload.get("services")
    services: list[dict[str, object]] = []
    if isinstance(services_payload, list):
        services = enrich_provisioning_services(services_payload)
        payload = dict(payload)
        payload["services"] = services
        payload["completion"] = summarize_provisioning_results(services)

    registry = load_registry()
    outputs_root = generated_outputs_root(registry).relative_to(workspace_path("."))
    state_path = destination_root / outputs_root / "factory" / "provisioning-state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return state_path


def provider_manual_steps(service: Mapping[str, object]) -> list[str]:
    provider = string_value(service, "provider") or string_value(service, "name")
    manual_secrets = string_list_value(service, "manual_secrets")
    status = string_value(service, "status")
    reason = string_value(service, "reason")

    if provider == "Supabase":
        return [
            (
                "Retrieve SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, and "
                "NEXT_PUBLIC_SUPABASE_ANON_KEY from the project and store them in "
                "repo-scoped secrets."
            )
        ]
    if provider == "Neon":
        return [
            (
                "Replace the sanitized DATABASE_URL and DIRECT_DATABASE_URL values "
                "with the real password-backed connection strings in repo-scoped "
                "secrets."
            )
        ]
    if provider == "Vercel" and status == "created":
        return []
    if status == "manual_only":
        return [reason or f"Complete {provider} provisioning manually for this generated repo."]
    if manual_secrets:
        return [f"Store {', '.join(manual_secrets)} as repo-scoped secrets before first deploy."]
    return []


def annotate_provisioned_service(service: Mapping[str, object]) -> dict[str, object]:
    manual_secret_targets = string_list_value(service, "manual_secrets")
    manual_steps = provider_manual_steps(service)
    status = string_value(service, "status")

    if status == "manual_only":
        automation_level = "manual"
    elif manual_secret_targets or manual_steps:
        automation_level = "partial"
    else:
        automation_level = "full"

    completion_status = "complete" if automation_level == "full" else "action_required"
    annotated = dict(service)
    annotated["automation_level"] = automation_level
    annotated["completion_status"] = completion_status
    annotated["manual_secret_targets"] = manual_secret_targets
    annotated["manual_steps"] = manual_steps
    return annotated


def enrich_provisioning_services(services: list[dict[str, object]]) -> list[dict[str, object]]:
    return [annotate_provisioned_service(service) for service in services]


def summarize_provisioning_results(services: list[dict[str, object]]) -> dict[str, object]:
    enriched = enrich_provisioning_services(services)
    completed_services = [
        string_value(service, "name") for service in enriched if string_value(service, "completion_status") == "complete"
    ]
    pending_services = [
        string_value(service, "name") for service in enriched if string_value(service, "completion_status") != "complete"
    ]

    unresolved_env_keys = sorted(
        {key for service in enriched for key in string_list_value(service, "manual_secret_targets") if key.strip()}
    )
    next_steps: list[str] = []
    for service in enriched:
        for step in string_list_value(service, "manual_steps"):
            if step not in next_steps:
                next_steps.append(step)

    return {
        "status": "complete" if not pending_services else "action_required",
        "completed_services": completed_services,
        "pending_services": pending_services,
        "unresolved_env_keys": unresolved_env_keys,
        "next_steps": next_steps,
    }


def http_json_request(*, method: str, url: str, headers: dict[str, str], payload: dict[str, object] | None) -> dict[str, object]:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    http_request = request.Request(url, data=body, headers=headers, method=method)
    try:
        with request.urlopen(http_request, timeout=60) as response:
            response_body = response.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} while calling {url}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Network error while calling {url}: {exc.reason}") from exc

    if not response_body.strip():
        return {}
    parsed = json.loads(response_body)
    if isinstance(parsed, dict):
        return parsed
    raise RuntimeError(f"Expected JSON object from {url} but received {type(parsed).__name__}.")


def provision_supabase_project(
    *,
    project_name: str,
    organization_id: str,
    region: str,
    plan: str,
) -> dict[str, object]:
    access_token = os.environ.get("SUPABASE_ACCESS_TOKEN", "").strip()
    if not access_token:
        raise RuntimeError("SUPABASE_ACCESS_TOKEN is required to provision Supabase services.")

    db_password = secrets.token_urlsafe(24)

    payload: dict[str, object] = {
        "organization_id": organization_id,
        "name": project_name,
        "region": region,
        "plan": plan,
        "db_pass": db_password,
    }
    response_payload = http_json_request(
        method="POST",
        url="https://api.supabase.com/v1/projects",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        payload=payload,
    )
    project_ref = string_value(response_payload, "ref")
    project_url = f"https://{project_ref}.supabase.co" if project_ref else ""
    return {
        "name": "Supabase",
        "provider": "Supabase",
        "status": "provisioning_started",
        "mode": "management_api",
        "organization_id": organization_id,
        "region": region,
        "project": response_payload,
        "env": {
            "SUPABASE_PROJECT_REF": project_ref,
            "SUPABASE_REGION": region,
            "SUPABASE_URL": project_url,
            "NEXT_PUBLIC_SUPABASE_URL": project_url,
        },
        "manual_secrets": [
            "SUPABASE_ANON_KEY",
            "SUPABASE_SERVICE_ROLE_KEY",
            "NEXT_PUBLIC_SUPABASE_ANON_KEY",
        ],
    }


def provision_vercel_project(
    *,
    project_name: str,
    team_id: str,
    team_slug: str,
) -> dict[str, object]:
    access_token = os.environ.get("VERCEL_ACCESS_TOKEN", "").strip()
    if not access_token:
        raise RuntimeError("VERCEL_ACCESS_TOKEN is required to provision Vercel services.")

    query = urlencode({key: value for key, value in {"teamId": team_id, "slug": team_slug}.items() if value})
    url = "https://api.vercel.com/v11/projects"
    if query:
        url = f"{url}?{query}"
    response_payload = http_json_request(
        method="POST",
        url=url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        payload={
            "name": slugify_project_name(project_name),
            "publicSource": False,
        },
    )
    return {
        "name": "Vercel",
        "provider": "Vercel",
        "status": "created",
        "mode": "rest_api",
        "team_id": team_id,
        "team_slug": team_slug,
        "project": response_payload,
        "env": {
            "VERCEL_PROJECT_ID": string_value(response_payload, "id"),
            "VERCEL_PROJECT_NAME": string_value(response_payload, "name"),
            "VERCEL_TEAM_ID": team_id,
            "VERCEL_TEAM_SLUG": team_slug,
        },
    }


def provision_neon_project(
    *,
    project_name: str,
    organization_id: str,
    region: str,
    pg_version: int,
) -> dict[str, object]:
    access_token = os.environ.get("NEON_API_KEY", "").strip()
    if not access_token:
        raise RuntimeError("NEON_API_KEY is required to provision Neon services.")

    project_slug = slugify_project_name(project_name)
    payload: dict[str, object] = {
        "project": {
            "name": project_slug,
            "region_id": region,
            "pg_version": pg_version,
            "store_passwords": True,
            "branch": {
                "name": "main",
                "database_name": project_slug,
                "role_name": f"{project_slug}_owner",
            },
        }
    }
    if organization_id:
        mapping_value(payload["project"])["org_id"] = organization_id

    response_payload = http_json_request(
        method="POST",
        url="https://console.neon.tech/api/v2/projects",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        payload=payload,
    )

    project_payload = mapping_value(response_payload.get("project"))
    branch_payload = mapping_value(response_payload.get("branch"))
    sanitized_uri = sanitize_connection_uri(first_connection_uri(response_payload))
    database_name = project_slug
    databases = response_payload.get("databases")
    if isinstance(databases, list) and databases:
        database_name = string_value(mapping_value(databases[0]), "name") or database_name

    return {
        "name": "Neon",
        "provider": "Neon",
        "status": "provisioning_started",
        "mode": "rest_api",
        "organization_id": organization_id,
        "region": region,
        "pg_version": pg_version,
        "project": response_payload,
        "env": {
            "NEON_PROJECT_ID": string_value(project_payload, "id"),
            "NEON_BRANCH_ID": string_value(branch_payload, "id"),
            "NEON_REGION": string_value(project_payload, "region_id") or region,
            "NEON_HOST": string_value(project_payload, "proxy_host"),
            "NEON_DATABASE": database_name,
            "DATABASE_URL": sanitized_uri,
            "DIRECT_DATABASE_URL": sanitized_uri,
        },
        "manual_secrets": ["DATABASE_URL", "DIRECT_DATABASE_URL"],
    }


def provision_requested_services(
    *,
    project_name: str,
    services: list[str],
    supabase_org_id: str,
    supabase_region: str,
    supabase_plan: str,
    vercel_team_id: str,
    vercel_team_slug: str,
    neon_org_id: str,
    neon_region: str,
    neon_pg_version: int,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for service_name in services:
        normalized = service_name.strip().lower()
        if normalized == "supabase":
            organization_id = supabase_org_id or os.environ.get("SUPABASE_ORGANIZATION_ID", "").strip()
            if not organization_id:
                raise RuntimeError("Supabase provisioning requires --supabase-org-id or SUPABASE_ORGANIZATION_ID.")
            region = supabase_region or os.environ.get("SUPABASE_REGION", "us-east-1").strip() or "us-east-1"
            results.append(
                provision_supabase_project(
                    project_name=project_name,
                    organization_id=organization_id,
                    region=region,
                    plan=supabase_plan,
                )
            )
            continue
        if normalized == "vercel":
            results.append(
                provision_vercel_project(
                    project_name=project_name,
                    team_id=vercel_team_id,
                    team_slug=vercel_team_slug,
                )
            )
            continue
        if normalized == "neon":
            organization_id = neon_org_id or os.environ.get("NEON_ORG_ID", "").strip()
            results.append(
                provision_neon_project(
                    project_name=project_name,
                    organization_id=organization_id,
                    region=neon_region,
                    pg_version=neon_pg_version,
                )
            )
            continue

        results.append(
            {
                "name": service_name,
                "provider": service_name,
                "status": "manual_only",
                "mode": "not_implemented",
                "reason": "Automation is not implemented for this service yet.",
            }
        )

    return results


def create_github_repo(
    *,
    destination_root: Path,
    github_repo: str,
    github_visibility: str,
    dry_run: bool,
) -> None:
    gh_executable = shutil.which("gh")
    if not gh_executable:
        raise RuntimeError("GitHub CLI 'gh' is required when --create-github-repo is used.")
    command = [
        gh_executable,
        "repo",
        "create",
        github_repo,
        f"--{github_visibility}",
        "--source",
        ".",
        "--remote",
        "origin",
    ]
    if dry_run:
        print("RUN    " + " ".join(command))
        return
    subprocess.run(
        command,
        cwd=destination_root,
        check=True,
        capture_output=True,
        text=True,
    )
