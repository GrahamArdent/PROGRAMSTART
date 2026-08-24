from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .programstart_common import load_workflow_state, workspace_path
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import load_workflow_state, workspace_path


def programbuild_variant(registry: dict[str, Any], state: dict[str, Any] | None = None) -> str:
    """Return the active PROGRAMBUILD variant, defaulting to product."""
    state = state or load_workflow_state(registry, "programbuild")
    variant = str(state.get("variant") or "product").strip().lower()
    return variant if variant in {"lite", "product", "enterprise"} else "product"


def artifact_profile(
    registry: dict[str, Any],
    *,
    variant: str | None = None,
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the configured artifact profile for the active variant, if any."""
    selected = (variant or programbuild_variant(registry, state)).strip().lower()
    system = registry.get("systems", {}).get("programbuild", {})
    profiles = system.get("artifact_profiles", {})
    profile = profiles.get(selected, {})
    return dict(profile) if isinstance(profile, dict) else {}


def core_output_files(
    registry: dict[str, Any],
    *,
    variant: str | None = None,
    state: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return outputs that are part of the normal operator workload for the variant."""
    system = registry.get("systems", {}).get("programbuild", {})
    profile = artifact_profile(registry, variant=variant, state=state)
    configured = profile.get("core_output_files")
    if isinstance(configured, list):
        return tuple(str(path) for path in configured)
    return tuple(str(path) for path in system.get("output_files", []))


def conditional_output_files(
    registry: dict[str, Any],
    *,
    variant: str | None = None,
    state: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return outputs that should enter active context only when they contain real work."""
    profile = artifact_profile(registry, variant=variant, state=state)
    configured = profile.get("conditional_output_files", [])
    if not isinstance(configured, list):
        return ()
    return tuple(str(path) for path in configured)


def artifact_has_body(path: Path) -> bool:
    """Return whether a stub-style artifact contains meaningful content below its metadata header."""
    if not path.exists():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    if "---" in text:
        text = text.split("---", 1)[1]
    meaningful = [line.strip() for line in text.splitlines() if line.strip()]
    return bool(meaningful)


def active_conditional_outputs(
    registry: dict[str, Any],
    *,
    variant: str | None = None,
    state: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return conditional outputs that currently contain meaningful project content."""
    return tuple(
        path
        for path in conditional_output_files(registry, variant=variant, state=state)
        if artifact_has_body(workspace_path(path))
    )


def filter_stage_files(
    registry: dict[str, Any],
    files: list[str],
    *,
    variant: str | None = None,
    state: dict[str, Any] | None = None,
) -> list[str]:
    """Remove dormant conditional outputs from JIT stage context while preserving active ones."""
    dormant = set(conditional_output_files(registry, variant=variant, state=state)) - set(
        active_conditional_outputs(registry, variant=variant, state=state)
    )
    return [path for path in files if path not in dormant]


def stage_check_required(
    registry: dict[str, Any],
    check_name: str,
    *,
    variant: str | None = None,
    state: dict[str, Any] | None = None,
) -> bool:
    """Return whether a conditional stage check currently has evidence to validate.

    Product and Enterprise have no artifact profile override today, so their checks remain
    unchanged. For Lite, checks mapped to conditional artifacts wake up automatically once
    the corresponding artifact contains meaningful content.
    """
    profile = artifact_profile(registry, variant=variant, state=state)
    mapping = profile.get("conditional_stage_checks", {})
    if not isinstance(mapping, dict):
        return True
    artifact = mapping.get(check_name)
    if not artifact:
        return True
    return artifact_has_body(workspace_path(str(artifact)))
