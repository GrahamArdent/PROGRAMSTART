from __future__ import annotations

# ruff: noqa: I001

import argparse

try:
    from . import programstart_validate_core as validate_core
    from .programstart_common import load_registry, warn_direct_script_invocation
except ImportError:  # pragma: no cover - standalone script execution fallback
    import programstart_validate_core as validate_core
    from programstart_common import load_registry, warn_direct_script_invocation

# ---------------------------------------------------------------------------
# Re-export every public name from validate_core so that existing consumers
# (``from scripts.programstart_validate import X``) continue to work and
# monkeypatch targets on this module affect main()'s dispatch.
# ---------------------------------------------------------------------------
_check_decision_log_entries = validate_core._check_decision_log_entries
_PLACEHOLDER_PATTERNS = validate_core._PLACEHOLDER_PATTERNS
_relative_workspace_path = validate_core._relative_workspace_path
check_content_quality = validate_core.check_content_quality
placeholder_content_targets = validate_core.placeholder_content_targets
validate_placeholder_content = validate_core.validate_placeholder_content
stage_content_quality_warnings = validate_core.stage_content_quality_warnings
run_stage_gate_check = validate_core.run_stage_gate_check
validate_intake_complete = validate_core.validate_intake_complete
validate_feasibility_criteria = validate_core.validate_feasibility_criteria
validate_research_complete = validate_core.validate_research_complete
validate_requirements_complete = validate_core.validate_requirements_complete
validate_architecture_contracts = validate_core.validate_architecture_contracts
validate_risk_spikes = validate_core.validate_risk_spikes
validate_risk_spike_resolution = validate_core.validate_risk_spike_resolution
validate_test_strategy_complete = validate_core.validate_test_strategy_complete
validate_scaffold_complete = validate_core.validate_scaffold_complete
validate_implementation_entry_criteria = validate_core.validate_implementation_entry_criteria
validate_release_ready = validate_core.validate_release_ready
validate_audit_complete = validate_core.validate_audit_complete
validate_post_launch_review = validate_core.validate_post_launch_review
validate_registry = validate_core.validate_registry
clean_md = validate_core.clean_md
extract_bullets_after_marker = validate_core.extract_bullets_after_marker
iter_guidance_sections = validate_core.iter_guidance_sections
planning_reference_rules = validate_core.planning_reference_rules
load_external_reference_allowlist = validate_core.load_external_reference_allowlist
validate_authority_sync = validate_core.validate_authority_sync
validate_planning_references = validate_core.validate_planning_references
validate_required_files = validate_core.validate_required_files
validate_metadata = validate_core.validate_metadata
metadata_warnings = validate_core.metadata_warnings
validate_engineering_ready = validate_core.validate_engineering_ready
enforce_engineering_ready_in_all = validate_core.enforce_engineering_ready_in_all
expected_bootstrap_assets = validate_core.expected_bootstrap_assets
validate_bootstrap_assets = validate_core.validate_bootstrap_assets
validate_repo_boundary_policy = validate_core.validate_repo_boundary_policy
validate_prompt_registry_completeness = validate_core.validate_prompt_registry_completeness
_markdown_section = validate_core._markdown_section
validate_prompt_authority_metadata = validate_core.validate_prompt_authority_metadata
validate_prompt_generation_boundary = validate_core.validate_prompt_generation_boundary
validate_gameplan_prompt_pairing = validate_core.validate_gameplan_prompt_pairing
validate_rule_enforcement = validate_core.validate_rule_enforcement
validate_adr_coverage = validate_core.validate_adr_coverage
_parse_markdown_frontmatter = validate_core._parse_markdown_frontmatter
_adr_title = validate_core._adr_title
_normalize_adr_title = validate_core._normalize_adr_title
_adr_decision_link = validate_core._adr_decision_link
_adr_readme_entries = validate_core._adr_readme_entries
_legacy_pre_register_adr_ids = validate_core._legacy_pre_register_adr_ids
validate_adr_coherence = validate_core.validate_adr_coherence
validate_decision_log_reversal_invariants = validate_core.validate_decision_log_reversal_invariants
validate_test_coverage = validate_core.validate_test_coverage
validate_coverage_source_completeness = validate_core.validate_coverage_source_completeness
validate_kb_freshness = validate_core.validate_kb_freshness
validate_workflow_state = validate_core.validate_workflow_state
ALLOWED_ROOT_MD = validate_core.ALLOWED_ROOT_MD
ALLOWED_ROOT_NON_MD = validate_core.ALLOWED_ROOT_NON_MD
validate_file_hygiene = validate_core.validate_file_hygiene


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PROGRAMSTART structure and process metadata.")
    parser.add_argument(
        "--check",
        choices=[
            "all",
            "required-files",
            "metadata",
            "engineering-ready",
            "workflow-state",
            "authority-sync",
            "planning-references",
            "bootstrap-assets",
            "repo-boundary",
            "rule-enforcement",
            "test-coverage",
            "template-test-coverage",
            "adr-coverage",
            "adr-coherence",
            "decision-log-coherence",
            "prompt-authority",
            "prompt-generation",
            "gameplan-prompt-pairing",
            "placeholder-content",
            "kb-freshness",
            "intake-complete",
            "feasibility-criteria",
            "research-complete",
            "requirements-complete",
            "architecture-contracts",
            "risk-spikes",
            "risk-spikes-resolved",
            "test-strategy-complete",
            "scaffold-complete",
            "implementation-entry",
            "release-ready",
            "audit-complete",
            "post-launch-review",
            "coverage-source",
            "file-hygiene",
        ],
        default="all",
    )
    parser.add_argument(
        "--system",
        choices=["programbuild", "userjourney"],
        help="Only validate this system.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors (exit 1 if any warnings).",
    )
    args = parser.parse_args(argv)

    registry = load_registry()
    problems: list[str] = []
    warnings: list[str] = []

    sf = args.system
    if args.check == "all":
        problems.extend(validate_core.validate_registry(registry))
        problems.extend(validate_core.validate_required_files(registry, sf))
        problems.extend(validate_core.validate_metadata(registry, sf))
        problems.extend(validate_core.validate_workflow_state(registry, sf))
        problems.extend(validate_core.validate_authority_sync(registry))
        problems.extend(validate_core.validate_repo_boundary_policy(registry))
        problems.extend(validate_core.validate_rule_enforcement(registry))
        problems.extend(validate_core.validate_bootstrap_assets(registry))
        if validate_core.enforce_engineering_ready_in_all(registry, sf):
            problems.extend(validate_core.validate_engineering_ready(registry))
        reference_problems, reference_warnings = validate_core.validate_planning_references(registry)
        problems.extend(reference_problems)
        warnings.extend(validate_core.metadata_warnings(registry, sf))
        warnings.extend(reference_warnings)
        warnings.extend(validate_core.validate_test_coverage(registry))
        warnings.extend(validate_core.validate_coverage_source_completeness(registry))
        warnings.extend(validate_core.validate_adr_coverage(registry))
        problems.extend(validate_core.validate_adr_coherence(registry))
        problems.extend(validate_core.validate_decision_log_reversal_invariants(registry))
        problems.extend(validate_core.validate_prompt_authority_metadata(registry))
        problems.extend(validate_core.validate_prompt_generation_boundary(registry))
        problems.extend(validate_core.validate_gameplan_prompt_pairing(registry))
        placeholder_problems, placeholder_warnings = validate_core.validate_placeholder_content(registry)
        problems.extend(placeholder_problems)
        warnings.extend(placeholder_warnings)
        warnings.extend(validate_core.validate_kb_freshness(registry))
        warnings.extend(validate_core.validate_file_hygiene(registry))
    elif args.check == "required-files":
        problems.extend(validate_core.validate_registry(registry))
        problems.extend(validate_core.validate_required_files(registry, sf))
    elif args.check == "metadata":
        problems.extend(validate_core.validate_metadata(registry, sf))
        warnings.extend(validate_core.metadata_warnings(registry, sf))
    elif args.check == "workflow-state":
        problems.extend(validate_core.validate_workflow_state(registry, sf))
    elif args.check == "authority-sync":
        problems.extend(validate_core.validate_authority_sync(registry))
    elif args.check == "planning-references":
        reference_problems, reference_warnings = validate_core.validate_planning_references(registry)
        problems.extend(reference_problems)
        warnings.extend(reference_warnings)
    elif args.check == "repo-boundary":
        problems.extend(validate_core.validate_repo_boundary_policy(registry))
    elif args.check == "bootstrap-assets":
        problems.extend(validate_core.validate_bootstrap_assets(registry))
    elif args.check == "rule-enforcement":
        problems.extend(validate_core.validate_rule_enforcement(registry))
    elif args.check == "test-coverage" or args.check == "template-test-coverage":
        warnings.extend(validate_core.validate_test_coverage(registry))
    elif args.check == "adr-coverage":
        warnings.extend(validate_core.validate_adr_coverage(registry))
    elif args.check == "adr-coherence":
        problems.extend(validate_core.validate_adr_coherence(registry))
    elif args.check == "decision-log-coherence":
        problems.extend(validate_core.validate_decision_log_reversal_invariants(registry))
    elif args.check == "prompt-authority":
        problems.extend(validate_core.validate_prompt_authority_metadata(registry))
    elif args.check == "prompt-generation":
        problems.extend(validate_core.validate_prompt_generation_boundary(registry))
    elif args.check == "gameplan-prompt-pairing":
        problems.extend(validate_core.validate_gameplan_prompt_pairing(registry))
    elif args.check == "placeholder-content":
        placeholder_problems, placeholder_warnings = validate_core.validate_placeholder_content(registry)
        problems.extend(placeholder_problems)
        warnings.extend(placeholder_warnings)
    elif args.check == "kb-freshness":
        warnings.extend(validate_core.validate_kb_freshness(registry))
    elif args.check == "intake-complete":
        problems.extend(validate_core.validate_intake_complete(registry))
    elif args.check == "feasibility-criteria":
        problems.extend(validate_core.validate_feasibility_criteria(registry))
    elif args.check == "research-complete":
        problems.extend(validate_core.validate_research_complete(registry))
    elif args.check == "requirements-complete":
        problems.extend(validate_core.validate_requirements_complete(registry))
    elif args.check == "architecture-contracts":
        problems.extend(validate_core.validate_architecture_contracts(registry))
    elif args.check == "risk-spikes":
        problems.extend(validate_core.validate_risk_spikes(registry))
    elif args.check == "risk-spikes-resolved":
        problems.extend(validate_core.validate_risk_spike_resolution(registry))
    elif args.check == "engineering-ready":
        problems.extend(validate_core.validate_engineering_ready(registry))
    elif args.check == "test-strategy-complete":
        problems.extend(validate_core.validate_test_strategy_complete(registry))
    elif args.check == "scaffold-complete":
        problems.extend(validate_core.validate_scaffold_complete(registry))
    elif args.check == "implementation-entry":
        problems.extend(validate_core.validate_implementation_entry_criteria(registry))
    elif args.check == "release-ready":
        problems.extend(validate_core.validate_release_ready(registry))
    elif args.check == "audit-complete":
        problems.extend(validate_core.validate_audit_complete(registry))
    elif args.check == "post-launch-review":
        problems.extend(validate_core.validate_post_launch_review(registry))
    elif args.check == "coverage-source":
        warnings.extend(validate_core.validate_coverage_source_completeness(registry))
    elif args.check == "file-hygiene":
        warnings.extend(validate_core.validate_file_hygiene(registry))
    else:
        problems.extend(validate_core.validate_engineering_ready(registry))

    if problems:
        print("Validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    if args.strict and warnings:
        print("Validation failed (strict mode) — warnings treated as errors:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print(f"Validation passed for check: {args.check}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart validate' or 'pb validate'")
    raise SystemExit(main())
