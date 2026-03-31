from __future__ import annotations

# ruff: noqa: I001

import argparse
import re
from datetime import date
from pathlib import Path

try:
    from .programstart_attach import attach_userjourney, resolve_attachment_source
    from .programstart_bootstrap import bootstrap_repository, refresh_secrets_baseline, stamp_owner_and_dates
    from .programstart_common import warn_direct_script_invocation
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_attach import attach_userjourney, resolve_attachment_source  # type: ignore
    from programstart_bootstrap import (  # type: ignore
        bootstrap_repository,
        refresh_secrets_baseline,
        stamp_owner_and_dates,
    )
    from programstart_common import warn_direct_script_invocation  # type: ignore


def replace_starter_inputs_block(path: Path, values: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    replacement = "```text\n" + "\n".join(f"{key}: {value}" for key, value in values.items()) + "\n```"
    updated = re.sub(r"```text\n.*?\n```", replacement, text, count=1, flags=re.DOTALL)
    path.write_text(updated, encoding="utf-8")


def write_project_readme(
    path: Path,
    *,
    project_name: str,
    one_line_description: str,
    variant: str,
    product_shape: str,
    attach_userjourney_enabled: bool,
) -> None:
    lines = [
        f"# {project_name}",
        "",
        one_line_description or "This standalone project repository was bootstrapped from PROGRAMSTART.",
        "",
        "## Project Setup",
        "",
        f"- PROGRAMBUILD variant: {variant}",
        f"- Product shape: {product_shape}",
        f"- USERJOURNEY attached: {'yes' if attach_userjourney_enabled else 'no'}",
        "- Repo boundary: separate project repo; do not build inside PROGRAMSTART",
        "",
        "## Start Here",
        "",
        "```powershell",
        "uv sync --extra dev",
        "uv run programstart validate --check bootstrap-assets",
        "uv run programstart validate --check engineering-ready",
        "uv run programstart next",
        "```",
        "",
        (
            "Use `programstart create` for the one-shot project-factory path, or `programstart recommend` "
            "to inspect the current stack and workflow fit before filling stage outputs."
        ),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=("Initialize a new PROGRAMSTART project repo with stamped inputs and optional USERJOURNEY attachment.")
    )
    parser.add_argument("--dest", required=True, help="Destination directory for the new project repo.")
    parser.add_argument("--project-name", required=True, help="Project name to stamp into generated files.")
    parser.add_argument("--variant", choices=["lite", "product", "enterprise"], default="product")
    parser.add_argument("--product-shape", required=True, help="Product shape, for example 'web app' or 'CLI tool'.")
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
    parser.add_argument("--attach-userjourney", action="store_true", help="Attach USERJOURNEY as part of initialization.")
    parser.add_argument("--attachment-source", default="", help="Source USERJOURNEY path when attaching.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    destination_root = Path(args.dest).expanduser().resolve()
    try:
        bootstrap_repository(
            destination_root,
            project_name=args.project_name,
            variant=args.variant,
            dry_run=args.dry_run,
            force=args.force,
        )
    except (FileExistsError, RuntimeError, ValueError) as exc:
        print(str(exc))
        return 1

    if args.dry_run:
        print(f"STAMP  {destination_root / 'PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md'}")
        print(f"STAMP  {destination_root / 'README.md'}")
        if args.attach_userjourney:
            source = resolve_attachment_source(args.attachment_source) if args.attachment_source else Path("USERJOURNEY")
            print(f"ATTACH USERJOURNEY {source} -> {destination_root / 'USERJOURNEY'}")
        return 0

    kickoff_values = {
        "PROJECT_NAME": args.project_name,
        "ONE_LINE_DESCRIPTION": args.one_line_description,
        "PRIMARY_USER": args.primary_user,
        "SECONDARY_USER": args.secondary_user,
        "CORE_PROBLEM": args.core_problem,
        "SUCCESS_METRIC": args.success_metric,
        "PRODUCT_SHAPE": args.product_shape,
        "KNOWN_CONSTRAINTS": args.known_constraints,
        "OUT_OF_SCOPE": args.out_of_scope,
        "COMPLIANCE_OR_SECURITY_NEEDS": args.compliance_or_security_needs,
        "TEAM_SIZE": args.team_size,
        "DELIVERY_TARGET": args.delivery_target,
    }
    replace_starter_inputs_block(destination_root / "PROGRAMBUILD" / "PROGRAMBUILD_KICKOFF_PACKET.md", kickoff_values)
    write_project_readme(
        destination_root / "README.md",
        project_name=args.project_name,
        one_line_description=args.one_line_description,
        variant=args.variant,
        product_shape=args.product_shape,
        attach_userjourney_enabled=args.attach_userjourney,
    )
    if args.owner:
        stamp_owner_and_dates(destination_root, owner=args.owner, last_updated=date.today().isoformat())
    if args.attach_userjourney:
        if not args.attachment_source:
            raise SystemExit("--attachment-source is required when --attach-userjourney is used")
        attach_userjourney(destination_root, resolve_attachment_source(args.attachment_source), force=args.force, dry_run=False)
    refresh_secrets_baseline(destination_root, dry_run=False)

    print(f"Initialized project repository at {destination_root}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation(
        "'uv run programstart init --dest <folder> --project-name <name> --product-shape <shape>' or 'pb init ...'"
    )
    raise SystemExit(main())
