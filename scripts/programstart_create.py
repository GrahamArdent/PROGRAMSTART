from __future__ import annotations

# ruff: noqa: I001

import argparse
import json
from dataclasses import asdict
from pathlib import Path

try:
    from . import programstart_create_core as create_core
    from . import programstart_create_output as create_output
    from .programstart_common import warn_direct_script_invocation
    from .programstart_init import main as init_main
    from .programstart_recommend import build_generated_prompt, build_recommendation
    from .programstart_starter_scaffold import build_starter_scaffold_plan, write_starter_scaffold
except ImportError:  # pragma: no cover - standalone script execution fallback
    import programstart_create_core as create_core
    import programstart_create_output as create_output
    from programstart_common import warn_direct_script_invocation
    from programstart_init import main as init_main
    from programstart_recommend import build_generated_prompt, build_recommendation
    from programstart_starter_scaffold import build_starter_scaffold_plan, write_starter_scaffold

normalize_shape = create_core.normalize_shape
slugify_project_name = create_core.slugify_project_name
default_github_repo_name = create_core.default_github_repo_name
merge_service_names = create_core.merge_service_names
mapping_value = create_core.mapping_value
string_value = create_core.string_value
string_list_value = create_core.string_list_value
sanitize_connection_uri = create_core.sanitize_connection_uri
first_connection_uri = create_core.first_connection_uri
merge_env_values = create_core.merge_env_values
upsert_env_lines = create_core.upsert_env_lines
hydrate_starter_env_example = create_core.hydrate_starter_env_example
knowledge_base_entries_by_name = create_core.knowledge_base_entries_by_name
write_provisioning_state = create_core.write_provisioning_state
http_json_request = create_core.http_json_request
provision_supabase_project = create_core.provision_supabase_project
provision_vercel_project = create_core.provision_vercel_project
provision_neon_project = create_core.provision_neon_project
provision_requested_services = create_core.provision_requested_services
render_factory_plan = create_output.render_factory_plan
write_factory_plan = create_output.write_factory_plan
render_setup_surface = create_output.render_setup_surface
write_setup_surface = create_output.write_setup_surface
render_provisioning_plan = create_output.render_provisioning_plan
write_provisioning_plan = create_output.write_provisioning_plan
create_github_repo = create_core.create_github_repo

# Preserve existing monkeypatch targets used by tests.
request = create_core.request
subprocess = create_core.subprocess
shutil = create_core.shutil


def build_parser() -> argparse.ArgumentParser:
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
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
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
        setup_surface = write_setup_surface(
            destination_root,
            project_name=args.project_name,
            recommendation=recommendation,
        )
        provisioning_results: list[dict[str, object]] | None = None
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
        provisioning_plan = write_provisioning_plan(
            destination_root,
            project_name=args.project_name,
            github_repo=github_repo,
            github_visibility=args.github_visibility,
            services=services,
            inferred_services=recommendation.service_names,
            provisioning_results=provisioning_results,
        )
        print(f"Wrote factory plan to {plan_path}")
        print(f"Wrote provisioning plan to {provisioning_plan}")
        print(f"Wrote setup surface to {setup_surface}")
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
