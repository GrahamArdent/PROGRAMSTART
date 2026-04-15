from __future__ import annotations

# ruff: noqa: I001

import argparse
import json
import os
import re
import secrets
import shutil
import subprocess
from collections.abc import Mapping
from dataclasses import asdict
from pathlib import Path
from urllib.parse import urlencode, urlsplit, urlunsplit
from urllib import error, request

try:
    from .programstart_init import main as init_main
    from .programstart_recommend import ProjectRecommendation, build_generated_prompt, build_recommendation
    from .programstart_common import generated_outputs_root, load_registry, warn_direct_script_invocation, workspace_path
    from .programstart_context import load_knowledge_base
    from .programstart_starter_scaffold import StarterScaffoldPlan, build_starter_scaffold_plan, write_starter_scaffold
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_init import main as init_main
    from programstart_recommend import ProjectRecommendation, build_generated_prompt, build_recommendation
    from programstart_common import generated_outputs_root, load_registry, warn_direct_script_invocation, workspace_path
    from programstart_context import load_knowledge_base
    from programstart_starter_scaffold import StarterScaffoldPlan, build_starter_scaffold_plan, write_starter_scaffold


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
    registry = load_registry()
    outputs_root = generated_outputs_root(registry).relative_to(workspace_path("."))
    state_path = destination_root / outputs_root / "factory" / "provisioning-state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return state_path


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


def render_factory_plan(
    *,
    project_name: str,
    recommendation: ProjectRecommendation,
    destination: Path,
    attachment_source: str,
    starter_plan: StarterScaffoldPlan,
    github_repo: str,
    github_visibility: str,
    services: list[str],
) -> str:
    payload = asdict(recommendation)
    rationale = "\n".join(f"- {item}" for item in payload["rationale"]) or "- none"
    kickoff_files = "\n".join(f"- {item}" for item in payload["kickoff_files"]) or "- none"
    next_commands = "\n".join(f"- {item}" for item in payload["next_commands"]) or "- none"
    prompt_principles = "\n".join(f"- {item}" for item in payload["prompt_principles"]) or "- none"
    prompt_patterns = "\n".join(f"- {item}" for item in payload["prompt_patterns"]) or "- none"
    prompt_anti_patterns = "\n".join(f"- {item}" for item in payload["prompt_anti_patterns"]) or "- none"
    stack_names = ", ".join(payload["stack_names"]) if payload["stack_names"] else "none matched current KB"
    matched_domains = "\n".join(f"- {item}" for item in payload.get("matched_domains", [])) or "- none"
    coverage_warnings = (
        "\n".join(f"- {item['domain']}: {item['status']} | {item['gaps']}" for item in payload.get("coverage_warnings", []))
        or "- none"
    )
    stack_evidence = (
        "\n".join(
            f"- {item['name']}: score={item['score']} | {'; '.join(item.get('reasons', [])[:2])}"
            for item in payload.get("stack_evidence", [])[:5]
        )
        or "- none"
    )
    service_evidence = (
        "\n".join(
            f"- {item['name']}: score={item['score']} | {'; '.join(item.get('reasons', [])[:2])}"
            for item in payload.get("service_evidence", [])[:5]
        )
        or "- none"
    )
    api_evidence = (
        "\n".join(
            f"- {item['name']}: score={item['score']} | {'; '.join(item.get('reasons', [])[:2])}"
            for item in payload.get("api_evidence", [])[:5]
        )
        or "- none"
    )
    cli_evidence = (
        "\n".join(
            f"- {item['name']}: score={item['score']} | {'; '.join(item.get('reasons', [])[:2])}"
            for item in payload.get("cli_evidence", [])[:5]
        )
        or "- none"
    )
    rule_evidence = (
        "\n".join(f"- {item['title']}: {item['because']} ({item['confidence']})" for item in payload.get("rule_evidence", [])[:5])
        or "- none"
    )
    actionability_summary = (
        "\n".join(
            f"- {item['name']} ({item['category']}): {item['actionability']} | {item['reason']}"
            for item in payload.get("actionability_summary", [])[:8]
        )
        or "- none"
    )
    alternatives = (
        "\n".join(f"- {item['item']} ({item['category']}): {item['rationale']}" for item in payload.get("alternatives", [])[:4])
        or "- none"
    )
    services_lines = "\n".join(f"- {item}" for item in services) or "- none declared"
    service_notes = "\n".join(f"- {item}" for item in payload.get("service_notes", [])) or "- none"
    cli_lines = "\n".join(f"- {item}" for item in payload.get("cli_tool_names", [])) or "- none"
    api_lines = "\n".join(f"- {item}" for item in payload.get("api_names", [])) or "- none"
    companion_surfaces = payload.get("suggested_companion_surfaces", [])
    companion_section = ""
    if companion_surfaces:
        surface_list = ", ".join(companion_surfaces)
        companion_section = (
            "## Companion UI Recommendation\n\n"
            f"This {payload['product_shape']} recommendation includes a suggested management UI.\n\n"
            f"- Recommended: {surface_list}\n"
            "- Stack: Vite + React (see starter scaffold)\n"
            "- Architecture: Separate frontend repo recommended for API services. "
            "Monorepo recommended for CLI tools with web configuration UI.\n\n"
        )
    return (
        f"# Factory Plan - {project_name}\n\n"
        f"Destination: {destination}\n\n"
        "## Selected Shape\n\n"
        f"- Product shape: {payload['product_shape']}\n"
        f"- Variant: {payload['variant']}\n"
        f"- Attach USERJOURNEY: {'yes' if payload['attach_userjourney'] else 'no'}\n"
        f"- Archetype: {payload['archetype']}\n"
        f"- Recommendation confidence: {payload.get('confidence', 'medium')}\n"
        f"- Suggested stacks: {stack_names}\n"
        f"- Attachment source: {attachment_source or 'not requested'}\n\n"
        "## Why This Path\n\n"
        f"{rationale}\n\n"
        "## KB Decision Evidence\n\n"
        "### Matched Domains\n\n"
        f"{matched_domains}\n\n"
        "### Coverage Warnings\n\n"
        f"{coverage_warnings}\n\n"
        "### Stack Evidence\n\n"
        f"{stack_evidence}\n\n"
        "### Service Evidence\n\n"
        f"{service_evidence}\n\n"
        "### API Evidence\n\n"
        f"{api_evidence}\n\n"
        "### CLI Evidence\n\n"
        f"{cli_evidence}\n\n"
        "### Rule Evidence\n\n"
        f"{rule_evidence}\n\n"
        "### Actionability Summary\n\n"
        f"{actionability_summary}\n\n"
        "### Alternatives Considered\n\n"
        f"{alternatives}\n\n"
        "## First Files To Open\n\n"
        f"{kickoff_files}\n\n"
        "## Recommended Commands\n\n"
        f"{next_commands}\n\n"
        "## Repository Boundary And Provisioning\n\n"
        "- Build the generated program in this new standalone repo, never inside PROGRAMSTART.\n"
        "- Local git repo: initialized during bootstrap.\n"
        f"- Suggested GitHub repo: {github_repo}\n"
        f"- Suggested visibility: {github_visibility}\n"
        "- Any project services must be provisioned for this generated repo, not shared with PROGRAMSTART.\n\n"
        "### Declared Service Dependencies\n\n"
        f"{services_lines}\n\n"
        "### Service Notes\n\n"
        f"{service_notes}\n\n"
        "### Recommended CLIs\n\n"
        f"{cli_lines}\n\n"
        "### Saved Third-Party API Templates\n\n"
        f"{api_lines}\n\n"
        "## Dynamic Prompt Guidance\n\n"
        "### Principles\n\n"
        f"{prompt_principles}\n\n"
        "### Patterns To Prefer\n\n"
        f"{prompt_patterns}\n\n"
        "### Anti-Patterns To Avoid\n\n"
        f"{prompt_anti_patterns}\n\n"
        "## Kickoff Prompt\n\n"
        "```text\n"
        f"{payload['generated_prompt']}\n"
        "```\n\n"
        f"{companion_section}"
        "## Starter Scaffold\n\n"
        f"- Label: {starter_plan.label}\n"
        f"- Root: {starter_plan.root_dir}\n"
        f"- Run hint: {starter_plan.run_hint}\n"
        f"- Files generated: {len(starter_plan.files)}\n"
    )


def write_factory_plan(
    destination_root: Path,
    project_name: str,
    recommendation: ProjectRecommendation,
    attachment_source: str,
    starter_plan: StarterScaffoldPlan,
    github_repo: str,
    github_visibility: str,
    services: list[str],
) -> Path:
    registry = load_registry()
    outputs_root = generated_outputs_root(registry).relative_to(workspace_path("."))
    plan_path = destination_root / outputs_root / "factory" / "create-plan.md"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(
        render_factory_plan(
            project_name=project_name,
            recommendation=recommendation,
            destination=destination_root,
            attachment_source=attachment_source,
            starter_plan=starter_plan,
            github_repo=github_repo,
            github_visibility=github_visibility,
            services=services,
        ),
        encoding="utf-8",
    )
    return plan_path


def render_setup_surface(
    *,
    project_name: str,
    recommendation: ProjectRecommendation,
    cli_entries: list[dict[str, object]],
    api_entries: list[dict[str, object]],
) -> str:
    matched_domains = "\n".join(f"- {item}" for item in recommendation.matched_domains) or "- none"
    coverage_warnings = (
        "\n".join(f"- {item['domain']}: {item['status']} | {item['gaps']}" for item in recommendation.coverage_warnings)
        or "- none"
    )
    cli_evidence = (
        "\n".join(
            f"- {item['name']}: score={item['score']} | {'; '.join(item.get('reasons', [])[:2])}"
            for item in recommendation.cli_evidence[:5]
        )
        or "- none"
    )
    api_evidence = (
        "\n".join(
            f"- {item['name']}: score={item['score']} | {'; '.join(item.get('reasons', [])[:2])}"
            for item in recommendation.api_evidence[:5]
        )
        or "- none"
    )
    rule_evidence = (
        "\n".join(f"- {item['title']}: {item['because']} ({item['confidence']})" for item in recommendation.rule_evidence[:5])
        or "- none"
    )
    actionability_summary = (
        "\n".join(
            f"- {item['name']} ({item['category']}): {item['actionability']} | {item['reason']}"
            for item in recommendation.actionability_summary[:8]
        )
        or "- none"
    )
    cli_sections: list[str] = []
    for entry in cli_entries:
        install_methods = "\n".join(f"- {item}" for item in string_list_value(entry, "install_methods")) or "- see provider docs"
        commands = "\n".join(f"- {item}" for item in string_list_value(entry, "recommended_commands")) or "- none"
        required_config = "\n".join(f"- {item}" for item in string_list_value(entry, "required_config")) or "- none"
        notes = "\n".join(f"- {item}" for item in string_list_value(entry, "notes")) or "- none"
        cli_sections.append(
            f"### {entry.get('name', '')}\n\n"
            f"- Provider: {entry.get('provider', '') or 'unknown'}\n"
            f"- Category: {entry.get('category', '') or 'general'}\n\n"
            "Install methods:\n\n"
            f"{install_methods}\n\n"
            "Recommended commands:\n\n"
            f"{commands}\n\n"
            "Required config:\n\n"
            f"{required_config}\n\n"
            "Notes:\n\n"
            f"{notes}\n"
        )

    api_sections: list[str] = []
    for entry in api_entries:
        server_env_vars = "\n".join(f"- {item}" for item in string_list_value(entry, "server_env_vars")) or "- none"
        public_env_vars = "\n".join(f"- {item}" for item in string_list_value(entry, "public_env_vars")) or "- none"
        notes = "\n".join(f"- {item}" for item in string_list_value(entry, "notes")) or "- none"
        api_sections.append(
            f"### {entry.get('name', '')}\n\n"
            f"- Provider: {entry.get('provider', '') or 'unknown'}\n"
            f"- Category: {entry.get('category', '') or 'general'}\n"
            f"- Base URL: {entry.get('base_url', '') or 'provider default'}\n"
            f"- Docs: {entry.get('docs_url', '') or 'provider docs'}\n"
            f"- Official CLI available: {'yes' if entry.get('has_official_cli') else 'no'}\n\n"
            "Server-side env vars:\n\n"
            f"{server_env_vars}\n\n"
            "Client/public env vars:\n\n"
            f"{public_env_vars}\n\n"
            "Notes:\n\n"
            f"{notes}\n"
        )

    return (
        f"# Setup Surface - {project_name}\n\n"
        "This artifact lists the recommended CLIs and saved third-party API templates inferred for the generated repo.\n\n"
        "## Recommendation Context\n\n"
        f"- Confidence: {recommendation.confidence}\n"
        "- These setup surfaces were inferred from the KB-driven recommendation "
        "and may include advice from partial coverage domains.\n\n"
        "### Matched Domains\n\n"
        f"{matched_domains}\n\n"
        "### Coverage Warnings\n\n"
        f"{coverage_warnings}\n\n"
        "### CLI Evidence\n\n"
        f"{cli_evidence}\n\n"
        "### API Evidence\n\n"
        f"{api_evidence}\n\n"
        "### Rule Evidence\n\n"
        f"{rule_evidence}\n\n"
        "### Actionability Summary\n\n"
        f"{actionability_summary}\n\n"
        "## Recommended CLIs\n\n"
        f"{'\n\n'.join(cli_sections) if cli_sections else 'No additional CLIs inferred.\n'}\n\n"
        "## Saved Third-Party APIs\n\n"
        f"{'\n\n'.join(api_sections) if api_sections else 'No additional third-party APIs inferred.\n'}"
    )


def write_setup_surface(
    destination_root: Path,
    *,
    project_name: str,
    recommendation: ProjectRecommendation,
) -> Path:
    knowledge_base = load_knowledge_base()
    cli_entries = knowledge_base_entries_by_name(knowledge_base.get("cli_tools", []), recommendation.cli_tool_names)
    api_entries = knowledge_base_entries_by_name(knowledge_base.get("third_party_apis", []), recommendation.api_names)
    registry = load_registry()
    outputs_root = generated_outputs_root(registry).relative_to(workspace_path("."))
    plan_path = destination_root / outputs_root / "factory" / "setup-surface.md"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(
        render_setup_surface(
            project_name=project_name,
            recommendation=recommendation,
            cli_entries=cli_entries,
            api_entries=api_entries,
        ),
        encoding="utf-8",
    )
    return plan_path


def render_provisioning_plan(
    *,
    project_name: str,
    destination_root: Path,
    github_repo: str,
    github_visibility: str,
    services: list[str],
    inferred_services: list[str],
) -> str:
    service_lines = "\n".join(f"- {item}" for item in services) or "- none declared"
    inferred_lines = "\n".join(f"- {item}" for item in inferred_services) or "- none inferred"
    visibility_flag = f"--{github_visibility}"
    return (
        f"# Provisioning Plan - {project_name}\n\n"
        "## Repo Boundary\n\n"
        f"- Local repo path: {destination_root}\n"
        "- This output is a separate project repo derived from PROGRAMSTART.\n"
        "- Do not add product code, remotes, or project infrastructure to the PROGRAMSTART template repo.\n\n"
        "## GitHub Remote\n\n"
        f"- Repo name: {github_repo}\n"
        f"- Visibility: {github_visibility}\n"
        "- Create the remote against the generated project repo, not PROGRAMSTART.\n"
        f"- CLI hint: gh repo create {github_repo} {visibility_flag} --source . --remote origin\n\n"
        "## External Services\n\n"
        "### Auto-Inferred Services\n\n"
        f"{inferred_lines}\n\n"
        "### Requested Services\n\n"
        "Provision each service as a project-scoped resource owned by this repo.\n\n"
        f"{service_lines}\n\n"
        "### Automation Support\n\n"
        "- GitHub repo creation can be executed during the factory run with --create-github-repo.\n"
        "- Supabase can be provisioned during the factory run with "
        "--provision-services plus SUPABASE_ACCESS_TOKEN and an organization id.\n"
        "- Vercel can be provisioned during the factory run with --provision-services plus VERCEL_ACCESS_TOKEN.\n"
        "- Neon can be provisioned during the factory run with --provision-services "
        "plus NEON_API_KEY and optional --neon-org-id.\n"
        "- Other services remain documented as manual follow-up until provider automation is added.\n\n"
        "Example: if the product needs Supabase, create a dedicated Supabase "
        "project for this generated repo and record its env vars in that repo only.\n"
    )


def write_provisioning_plan(
    destination_root: Path,
    *,
    project_name: str,
    github_repo: str,
    github_visibility: str,
    services: list[str],
    inferred_services: list[str],
) -> Path:
    registry = load_registry()
    outputs_root = generated_outputs_root(registry).relative_to(workspace_path("."))
    plan_path = destination_root / outputs_root / "factory" / "provisioning-plan.md"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(
        render_provisioning_plan(
            project_name=project_name,
            destination_root=destination_root,
            github_repo=github_repo,
            github_visibility=github_visibility,
            services=services,
            inferred_services=inferred_services,
        ),
        encoding="utf-8",
    )
    return plan_path


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a new standalone project repo in one pass using PROGRAMSTART guidance.")
    parser.add_argument("--dest", required=True, help="Destination directory for the new project repo.")
    parser.add_argument("--project-name", required=True, help="Project name to stamp into generated files.")
    parser.add_argument("--product-shape", required=True, help="Product shape, for example 'web app' or 'CLI tool'.")
    parser.add_argument("--variant", choices=["lite", "product", "enterprise"], help="Override the recommended variant.")
    parser.add_argument("--need", action="append", help="Repeated capability need, for example --need rag --need agents.")
    parser.add_argument(
        "--service", action="append", help="Repeated external service dependency, for example --service supabase."
    )
    parser.add_argument("--regulated", action="store_true", help="Use stronger governance defaults.")
    parser.add_argument("--attach-userjourney", dest="attach_userjourney", action="store_true")
    parser.add_argument("--no-attach-userjourney", dest="attach_userjourney", action="store_false")
    parser.add_argument("--attachment-source", default="", help="USERJOURNEY source path when attaching.")
    parser.add_argument(
        "--github-repo", default="", help="GitHub repo name to target for this generated project, for example owner/my-new-app."
    )
    parser.add_argument("--github-visibility", choices=["private", "public", "internal"], default="private")
    parser.add_argument(
        "--create-github-repo", action="store_true", help="Create the GitHub remote for the generated project via gh."
    )
    parser.add_argument(
        "--provision-services", action="store_true", help="Provision supported external services for the generated project."
    )
    parser.add_argument("--supabase-org-id", default="", help="Supabase organization id for hosted project provisioning.")
    parser.add_argument(
        "--supabase-region", default="", help="Supabase region for hosted project provisioning, for example us-east-1."
    )
    parser.add_argument("--supabase-plan", choices=["free", "pro"], default="free")
    parser.add_argument("--vercel-team-id", default="", help="Optional Vercel team id for project provisioning.")
    parser.add_argument("--vercel-team-slug", default="", help="Optional Vercel team slug for project provisioning.")
    parser.add_argument("--neon-org-id", default="", help="Optional Neon organization id for project provisioning.")
    parser.add_argument("--neon-region", default="aws-us-east-1", help="Neon region id for project provisioning.")
    parser.add_argument(
        "--neon-pg-version",
        type=int,
        choices=[14, 15, 16, 17],
        default=17,
        help="Neon PostgreSQL version for hosted project provisioning.",
    )
    parser.add_argument("--one-line-description", default="", help="Short project description.")
    parser.add_argument("--primary-user", default="", help="Primary user or operator.")
    parser.add_argument("--secondary-user", default="", help="Secondary user.")
    parser.add_argument("--core-problem", default="", help="Core problem statement.")
    parser.add_argument("--success-metric", default="", help="Success metric.")
    parser.add_argument("--known-constraints", default="", help="Known constraints.")
    parser.add_argument("--out-of-scope", default="", help="Out-of-scope items.")
    parser.add_argument("--compliance-or-security-needs", default="", help="Compliance or security needs.")
    parser.add_argument("--team-size", default="", help="Team size.")
    parser.add_argument("--delivery-target", default="", help="Delivery target.")
    parser.add_argument("--owner", default="", help="Owner name to stamp into planning docs.")
    parser.add_argument("--no-starter-scaffold", action="store_true", help="Skip emitting the runnable starter scaffold.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the selected plan as JSON in addition to creating the repo.",
    )
    parser.set_defaults(attach_userjourney=None)
    args = parser.parse_args(argv)
    github_repo = args.github_repo or default_github_repo_name(args.project_name)

    recommendation = build_recommendation(
        product_shape=normalize_shape(args.product_shape),
        needs={item.strip().lower() for item in (args.need or []) if item.strip()},
        regulated=args.regulated,
        attach_userjourney=args.attach_userjourney,
    )
    selected_variant = args.variant or recommendation.variant
    if recommendation.variant != selected_variant:
        recommendation.variant = selected_variant
        recommendation.generated_prompt = build_generated_prompt(
            product_shape=recommendation.product_shape,
            variant=selected_variant,
            attach_userjourney=recommendation.attach_userjourney,
            kickoff_files=recommendation.kickoff_files,
            rationale=recommendation.rationale,
            prompt_principles=recommendation.prompt_principles,
            prompt_patterns=recommendation.prompt_patterns,
            prompt_anti_patterns=recommendation.prompt_anti_patterns,
            coverage_warnings=recommendation.coverage_warnings,
            service_names=recommendation.service_names,
            cli_tool_names=recommendation.cli_tool_names,
            api_names=recommendation.api_names,
        )
    services = merge_service_names(recommendation, [item for item in (args.service or []) if item])
    recommendation.service_names = services
    init_args = [
        "--dest",
        args.dest,
        "--project-name",
        args.project_name,
        "--variant",
        selected_variant,
        "--product-shape",
        args.product_shape,
        "--one-line-description",
        args.one_line_description,
        "--primary-user",
        args.primary_user,
        "--secondary-user",
        args.secondary_user,
        "--core-problem",
        args.core_problem,
        "--success-metric",
        args.success_metric,
        "--known-constraints",
        args.known_constraints,
        "--out-of-scope",
        args.out_of_scope,
        "--compliance-or-security-needs",
        args.compliance_or_security_needs,
        "--team-size",
        args.team_size,
        "--delivery-target",
        args.delivery_target,
        "--owner",
        args.owner,
    ]
    if recommendation.attach_userjourney:
        init_args.append("--attach-userjourney")
        if args.attachment_source:
            init_args.extend(["--attachment-source", args.attachment_source])
    if args.dry_run:
        init_args.append("--dry-run")
    if args.force:
        init_args.append("--force")

    result = init_main(init_args)
    if result != 0:
        return result

    destination_root = Path(args.dest).expanduser().resolve()
    starter_plan = build_starter_scaffold_plan(args.project_name, recommendation)
    if not args.dry_run:
        if not args.no_starter_scaffold:
            created = write_starter_scaffold(destination_root, starter_plan)
            print(f"Wrote starter scaffold to {destination_root / starter_plan.root_dir} ({len(created)} files)")
        plan_path = write_factory_plan(
            destination_root,
            args.project_name,
            recommendation,
            args.attachment_source,
            starter_plan,
            github_repo,
            args.github_visibility,
            services,
        )
        provisioning_plan = write_provisioning_plan(
            destination_root,
            project_name=args.project_name,
            github_repo=github_repo,
            github_visibility=args.github_visibility,
            services=services,
            inferred_services=recommendation.service_names,
        )
        setup_surface = write_setup_surface(
            destination_root,
            project_name=args.project_name,
            recommendation=recommendation,
        )
        print(f"Wrote factory plan to {plan_path}")
        print(f"Wrote provisioning plan to {provisioning_plan}")
        print(f"Wrote setup surface to {setup_surface}")
        if args.create_github_repo:
            try:
                create_github_repo(
                    destination_root=destination_root,
                    github_repo=github_repo,
                    github_visibility=args.github_visibility,
                    dry_run=False,
                )
            except (RuntimeError, subprocess.CalledProcessError) as exc:
                print(str(exc))
                return 1
            print(f"Created GitHub repo {github_repo}")
        if args.provision_services:
            try:
                provisioning_results = provision_requested_services(
                    project_name=args.project_name,
                    services=services,
                    supabase_org_id=args.supabase_org_id,
                    supabase_region=args.supabase_region,
                    supabase_plan=args.supabase_plan,
                    vercel_team_id=args.vercel_team_id,
                    vercel_team_slug=args.vercel_team_slug,
                    neon_org_id=args.neon_org_id,
                    neon_region=args.neon_region,
                    neon_pg_version=args.neon_pg_version,
                )
            except RuntimeError as exc:
                print(str(exc))
                return 1
            env_path = hydrate_starter_env_example(destination_root, starter_plan, provisioning_results)
            state_path = write_provisioning_state(
                destination_root,
                {
                    "project_name": args.project_name,
                    "github_repo": github_repo,
                    "services": provisioning_results,
                },
            )
            if env_path is not None:
                print(f"Hydrated starter env template at {env_path}")
            print(f"Wrote provisioning state to {state_path}")
    elif args.create_github_repo:
        create_github_repo(
            destination_root=destination_root,
            github_repo=github_repo,
            github_visibility=args.github_visibility,
            dry_run=True,
        )
    if args.dry_run and args.provision_services and services:
        print("PLAN   provision services: " + ", ".join(services))

    if args.json:
        print(json.dumps(asdict(recommendation), indent=2))

    print("Factory create complete.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart create --dest <folder> --project-name <name> --product-shape <shape>'")
    raise SystemExit(main())
