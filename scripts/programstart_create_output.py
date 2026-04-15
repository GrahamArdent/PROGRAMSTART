from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

try:
    from .programstart_common import generated_outputs_root, load_registry, workspace_path
    from .programstart_context import load_knowledge_base
    from .programstart_create_core import knowledge_base_entries_by_name, string_list_value, string_value, summarize_provisioning_results
    from .programstart_recommend import ProjectRecommendation
    from .programstart_starter_scaffold import StarterScaffoldPlan
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import generated_outputs_root, load_registry, workspace_path
    from programstart_context import load_knowledge_base
    from programstart_create_core import knowledge_base_entries_by_name, string_list_value, string_value, summarize_provisioning_results
    from programstart_recommend import ProjectRecommendation
    from programstart_starter_scaffold import StarterScaffoldPlan


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
    provisioning_results: list[dict[str, object]] | None = None,
) -> str:
    service_lines = "\n".join(f"- {item}" for item in services) or "- none declared"
    inferred_lines = "\n".join(f"- {item}" for item in inferred_services) or "- none inferred"
    visibility_flag = f"--{github_visibility}"
    completion_section = ""
    if provisioning_results:
        completion = summarize_provisioning_results(provisioning_results)
        overall_status = string_value(completion, "status") or "unknown"
        completed_services = string_list_value(completion, "completed_services")
        pending_services = string_list_value(completion, "pending_services")
        unresolved_keys = "\n".join(f"- {item}" for item in string_list_value(completion, "unresolved_env_keys")) or "- none"
        next_steps = "\n".join(f"- {item}" for item in string_list_value(completion, "next_steps")) or "- none"
        service_sections: list[str] = []
        for service in provisioning_results:
            manual_secret_targets = string_list_value(service, "manual_secret_targets")
            manual_steps = string_list_value(service, "manual_steps")
            manual_secret_lines = "\n".join(f"- {item}" for item in manual_secret_targets) or "- none"
            manual_step_lines = "\n".join(f"- {item}" for item in manual_steps) or "- none"
            service_sections.append(
                f"### {service.get('name', '')}\n\n"
                f"- Provider status: {service.get('status', '') or 'unknown'}\n"
                f"- Automation level: {service.get('automation_level', '') or 'unknown'}\n"
                f"- Completion status: {service.get('completion_status', '') or 'unknown'}\n\n"
                "Manual secret targets:\n\n"
                f"{manual_secret_lines}\n\n"
                "Remaining steps:\n\n"
                f"{manual_step_lines}\n"
            )

        completion_section = (
            "## Provisioning Execution Status\n\n"
            f"- Overall status: {overall_status}\n"
            f"- Completed services: {', '.join(completed_services) or 'none'}\n"
            f"- Pending services: {', '.join(pending_services) or 'none'}\n\n"
            "### Unresolved Env Keys\n\n"
            f"{unresolved_keys}\n\n"
            "### Next Steps\n\n"
            f"{next_steps}\n\n"
            "### Service Status\n\n"
            f"{'\n\n'.join(service_sections)}\n\n"
        )
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
        f"{completion_section}"
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
    provisioning_results: list[dict[str, object]] | None = None,
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
            provisioning_results=provisioning_results,
        ),
        encoding="utf-8",
    )
    return plan_path