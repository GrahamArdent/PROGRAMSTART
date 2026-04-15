from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .programstart_common import (
        display_workspace_path,
        generated_outputs_root,
        git_changed_files,
        load_registry,
        warn_direct_script_invocation,
        write_json,
    )
    from .programstart_drift_check import evaluate_drift
    from .programstart_validate import validate_adr_coherence, validate_adr_coverage, validate_authority_sync
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        display_workspace_path,
        generated_outputs_root,
        git_changed_files,
        load_registry,
        warn_direct_script_invocation,
        write_json,
    )
    from programstart_drift_check import evaluate_drift
    from programstart_validate import validate_adr_coherence, validate_adr_coverage, validate_authority_sync


ADR_RESULT_CHOICES = ("created", "updated", "not-required")


def slugify(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "closeout"


def default_output_path(label: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    return generated_outputs_root() / "governance" / f"{timestamp}_{slugify(label)}.json"


def validate_adr_inputs(adr_result: str, adr_ids: list[str]) -> list[str]:
    problems: list[str] = []
    if adr_result == "not-required" and adr_ids:
        problems.append("--adr-id cannot be used when --adr-result is 'not-required'")
    if adr_result in {"created", "updated"} and not adr_ids:
        problems.append(f"--adr-id is required when --adr-result is '{adr_result}'")
    for adr_id in adr_ids:
        if not re.fullmatch(r"ADR-\d{4}", adr_id):
            problems.append(f"Invalid ADR id '{adr_id}' (expected ADR-0000 format)")
    return problems


def build_evidence(
    *,
    label: str,
    adr_result: str,
    adr_ids: list[str],
    notes: str,
) -> dict[str, Any]:
    registry = load_registry()
    changed_files = git_changed_files()
    adr_coverage_warnings = validate_adr_coverage(registry)
    adr_coherence_problems = validate_adr_coherence(registry)
    authority_sync_problems = validate_authority_sync(registry)
    drift_violations, drift_notes = evaluate_drift(registry, changed_files)

    failed = bool(adr_coverage_warnings or adr_coherence_problems or authority_sync_problems or drift_violations)
    status = "failed" if failed else ("passed_with_notes" if drift_notes else "passed")

    return {
        "label": label,
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": status,
        "adr_result": adr_result,
        "adr_ids": adr_ids,
        "notes": notes,
        "changed_files": changed_files,
        "checks": {
            "adr_coverage": {
                "status": "failed" if adr_coverage_warnings else "passed",
                "warnings": adr_coverage_warnings,
            },
            "adr_coherence": {
                "status": "failed" if adr_coherence_problems else "passed",
                "problems": adr_coherence_problems,
            },
            "authority_sync": {
                "status": "failed" if authority_sync_problems else "passed",
                "problems": authority_sync_problems,
            },
            "drift": {
                "status": "failed" if drift_violations else ("passed_with_notes" if drift_notes else "passed"),
                "violations": drift_violations,
                "notes": drift_notes,
            },
        },
    }


def print_summary(evidence: dict[str, Any], output_path: Path) -> None:
    print(f"Close-out {evidence['status']}.")
    for check_name, result in evidence["checks"].items():
        print(f"- {check_name}: {result['status']}")
        for warning in result.get("warnings", []):
            print(f"  warning: {warning}")
        for problem in result.get("problems", []):
            print(f"  problem: {problem}")
        for note in result.get("notes", []):
            print(f"  note: {note}")
        for violation in result.get("violations", []):
            print(f"  violation: {violation}")
    print(f"Evidence: {display_workspace_path(output_path)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run durable-checkpoint close-out checks and persist evidence.")
    parser.add_argument("--label", default="closeout", help="Short checkpoint label used in the evidence filename.")
    parser.add_argument("--adr-result", choices=ADR_RESULT_CHOICES, required=True, help="ADR triage outcome.")
    parser.add_argument("--adr-id", action="append", default=[], help="ADR id(s) when triage created or updated ADRs.")
    parser.add_argument("--notes", default="", help="Optional close-out notes stored in the evidence file.")
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output path. Defaults to outputs/governance/<timestamp>_<label>.json",
    )
    parser.add_argument("--json", action="store_true", help="Print the written evidence payload as JSON.")
    args = parser.parse_args(argv)

    input_problems = validate_adr_inputs(args.adr_result, list(args.adr_id))
    if input_problems:
        for problem in input_problems:
            print(problem)
        return 1

    evidence = build_evidence(
        label=args.label,
        adr_result=args.adr_result,
        adr_ids=list(args.adr_id),
        notes=args.notes,
    )
    output_path = Path(args.output) if args.output else default_output_path(args.label)
    write_json(output_path, evidence)

    if args.json:
        print(json.dumps(evidence, indent=2))
    else:
        print_summary(evidence, output_path)

    return 0 if evidence["status"] != "failed" else 1


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart closeout' or 'pb closeout'")
    raise SystemExit(main())