from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

try:
    from . import programstart_drift_check, programstart_validate_core, programstart_workflow_state
    from .programstart_artifact_profiles import stage_check_required
    from .programstart_common import load_registry, load_workflow_state, workflow_active_step
except ImportError:  # pragma: no cover - standalone script execution fallback
    import programstart_drift_check
    import programstart_validate_core
    import programstart_workflow_state

    from programstart_artifact_profiles import stage_check_required
    from programstart_common import load_registry, load_workflow_state, workflow_active_step


_PROGRAMBUILD_STAGE_CHECKS: dict[str, tuple[str, ...]] = {
    "inputs_and_mode_selection": ("intake-complete",),
    "feasibility": ("feasibility-criteria",),
    "research": ("research-complete",),
    "requirements_and_ux": ("requirements-complete",),
    "architecture_and_risk_spikes": ("architecture-contracts", "risk-spikes", "risk-spikes-resolved"),
    "scaffold_and_guardrails": ("scaffold-complete",),
    "test_strategy": ("test-strategy-complete",),
    # Keep implementation-entry semantics explicit so dormant Lite risk artifacts can
    # suppress only their own checks without bypassing architecture/test readiness.
    "implementation_loop": ("architecture-contracts", "test-strategy-complete", "risk-spikes", "risk-spikes-resolved"),
    "release_readiness": ("release-ready",),
    "audit_and_drift_control": ("audit-complete",),
    "post_launch_review": ("post-launch-review",),
}


@contextmanager
def _temporary_argv(arguments: list[str]) -> Iterator[None]:
    original = sys.argv[:]
    # Preserve the historical unified-CLI argv shape for downstream consumers/tests.
    sys.argv = ["programstart advance", "advance", *arguments]
    try:
        yield
    finally:
        sys.argv = original


def _delegate(arguments: list[str]) -> int:
    with _temporary_argv(arguments):
        return int(programstart_workflow_state.main())


def variant_aware_preflight(
    registry: dict[str, Any],
    *,
    active_step: str,
) -> list[str]:
    """Run PROGRAMBUILD advance preflight with artifact-profile-aware stage checks."""
    problems: list[str] = []
    problems.extend(programstart_validate_core.validate_required_files(registry, "programbuild"))
    problems.extend(programstart_validate_core.validate_metadata(registry, "programbuild"))
    problems.extend(programstart_validate_core.validate_workflow_state(registry, "programbuild"))
    problems.extend(programstart_validate_core.validate_authority_sync(registry))

    changed_files = programstart_drift_check.load_changed_files(
        argparse.Namespace(changed_file_list=None, files=None)
    )
    if changed_files:
        drift_problems, _ = programstart_drift_check.evaluate_drift(registry, changed_files, "programbuild")
        problems.extend(drift_problems)

    state = load_workflow_state(registry, "programbuild")
    for check_name in _PROGRAMBUILD_STAGE_CHECKS.get(active_step, ()):
        if not stage_check_required(registry, check_name, state=state):
            continue
        problems.extend(programstart_validate_core.run_stage_gate_check(registry, check_name))

    return problems


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--system", choices=["programbuild", "userjourney"], required=True)
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args, _unknown = parser.parse_known_args(arguments)

    # Preserve the mature state engine for non-PROGRAMBUILD workflows, explicit bypasses,
    # and dry runs (the underlying engine already skips mutation preflight for dry runs).
    if args.system != "programbuild" or args.skip_preflight or args.dry_run:
        return _delegate(arguments)

    registry = load_registry()
    state = load_workflow_state(registry, "programbuild")
    active_step = workflow_active_step(registry, "programbuild", state)
    problems = variant_aware_preflight(registry, active_step=active_step)
    if problems:
        print("Advance preflight failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    # Delegate all mutation, Challenge Gate, snapshot/signoff, and post-advance behavior to
    # the existing state engine after replacing only its non-profile-aware preflight.
    return _delegate([*arguments, "--skip-preflight"])


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())